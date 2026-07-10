# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
CONTRACT_PATH = ROOT / "design/ui-contracts/world-map/left_region_card.json"

ATLAS = BASE / "385-world-map-wmw-v0-9-1-left-card-candidate-b-atlas-2x.png"
RUNTIME_GODOT = BASE / "389-world-map-wmw-v0-9-1-left-card-candidate-b-godot-single-component.png"
BENCHMARK = BASE / "258-world-map-wmw-benchmark-shell-reference-v0-1.png"

OUT_TEXT_PRESSURE = BASE / "391-world-map-wmw-v0-9-1-left-card-candidate-b-text-pressure.png"
OUT_REVIEW_BOARD = BASE / "392-world-map-wmw-v0-9-1-left-card-candidate-b-review-board.png"
OUT_LIGHT_CONTRACT = BASE / "393-world-map-wmw-v0-9-1-light-contract-merge-board.png"

STATE_FRAMES = {
    "selected": (0, 0, 408, 320),
    "available": (408, 0, 816, 320),
    "warning": (816, 0, 1224, 320),
    "locked": (1224, 0, 1632, 320),
}

PRESSURE_CASES = [
    ("当前最长地区名", "selected", "北美禁区带", "红线升温  推荐2"),
    ("当前最长 meta", "warning", "非洲禁区带", "异常升温  高危"),
    ("压力地区名", "available", "北美禁区警戒带", "红线升温  推荐12"),
    ("压力 meta", "locked", "南美禁区带", "锁定  需12线报"),
]


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


FONT_BOLD = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]
FONT_REGULAR = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]


def f_bold(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return font(FONT_BOLD, size)


def f_regular(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return font(FONT_REGULAR, size)


F_TITLE = f_bold(34)
F_SUBTITLE = f_regular(20)
F_BODY = f_regular(18)
F_SMALL = f_regular(15)
F_TINY = f_regular(13)


def text_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font_obj, fill: str, max_width: int) -> int:
    x, y = xy
    line = ""
    for raw in text.split("\n"):
        for token in raw.split(" "):
            candidate = token if not line else f"{line} {token}"
            if draw.textbbox((0, 0), candidate, font=font_obj)[2] <= max_width:
                line = candidate
            else:
                if line:
                    draw.text((x, y), line, font=font_obj, fill=fill)
                    y += draw.textbbox((0, 0), line, font=font_obj)[3] + 5
                line = token
        if line:
            draw.text((x, y), line, font=font_obj, fill=fill)
            y += draw.textbbox((0, 0), line, font=font_obj)[3] + 5
            line = ""
    return y


def text_metrics(text: str, size: int, bold: bool) -> tuple[int, int]:
    font_obj = f_bold(size) if bold else f_regular(size)
    probe = Image.new("RGB", (4, 4))
    draw = ImageDraw.Draw(probe)
    box = draw.textbbox((0, 0), text, font=font_obj)
    return box[2] - box[0], box[3] - box[1]


def fit_size(text: str, target_size: int, min_size: int, max_w: int, max_h: int, bold: bool) -> int:
    for size in range(target_size, min_size - 1, -1):
        w, h = text_metrics(text, size, bold)
        if w <= max_w and h <= max_h:
            return size
    return min_size


def paste_contain(canvas: Image.Image, img: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    fitted = ImageOps.contain(img.convert("RGB"), (x2 - x1, y2 - y1), Image.Resampling.LANCZOS)
    px = x1 + (x2 - x1 - fitted.width) // 2
    py = y1 + (y2 - y1 - fitted.height) // 2
    canvas.paste(fitted, (px, py))
    return px, py, px + fitted.width, py + fitted.height


def draw_slot(draw: ImageDraw.ImageDraw, origin: tuple[int, int], rect: list[int], scale: float, color: str, label: str) -> None:
    x, y, w, h = rect
    ox, oy = origin
    box = [
        round(ox + x * scale),
        round(oy + y * scale),
        round(ox + (x + w) * scale),
        round(oy + (y + h) * scale),
    ]
    draw.rectangle(box, outline=color, width=2)
    draw.text((box[0] + 5, box[1] + 2), label, font=F_TINY, fill=color)


def image_stats(path: Path) -> dict:
    img = Image.open(path).convert("RGB")
    colors = img.getcolors(maxcolors=16_777_216)
    non_black = 0
    for _count, (r, g, b) in colors or []:
        if r + g + b > 24:
            non_black += _count
    return {"path": str(path), "size": list(img.size), "unique_colors": len(colors or []), "non_black_pixels": non_black}


def build_text_pressure_board(contract: dict) -> list[dict]:
    atlas = Image.open(ATLAS).convert("RGBA")
    frozen = contract["frozen"]
    slots = frozen["slots"]
    label = slots["label_plate"]
    meta = slots["meta_line"]
    scale = contract["export_scale"]
    label_inner_w = (label[2] - 16) * scale
    label_inner_h = label[3] * scale
    meta_inner_w = (meta[2] - 8) * scale
    meta_inner_h = meta[3] * scale

    canvas = Image.new("RGB", (1920, 1080), "#141914")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, 1920, 1080), fill="#141914")
    draw.text((42, 32), "left_region_card 候选 B｜文字压力检查", font=F_TITLE, fill="#f4efd9")
    draw.text(
        (42, 78),
        "合同槽位不变：label_plate 114x32，meta_line 96x10；本板只验证文案 / 字体 token，不改 frozen。",
        font=F_SUBTITLE,
        fill="#cfd7be",
    )

    metrics: list[dict] = []
    display_scale = 0.75
    slot_scale = scale * display_scale
    card_size = (round(408 * display_scale), round(320 * display_scale))
    positions = [(54, 138), (54, 362), (54, 586), (54, 810)]
    table_x = 430
    draw.text((table_x, 138), "压力指标（按 2x 合同槽实际测量）", font=F_SUBTITLE, fill="#f4efd9")
    draw.line((table_x, 178, 1110, 178), fill="#5d6c52", width=2)
    for i, (case_name, state, title, meta_text) in enumerate(PRESSURE_CASES):
        ox, oy = positions[i]
        frame = atlas.crop(STATE_FRAMES[state]).resize(card_size, Image.Resampling.LANCZOS)
        canvas.paste(frame, (ox, oy), frame)
        draw_slot(draw, (ox, oy), label, slot_scale, "#5ee2ff", "label_plate")
        draw_slot(draw, (ox, oy), meta, slot_scale, "#ffc84a", "meta_line")

        title_w, title_h = text_metrics(title, 38, True)
        meta_w, meta_h = text_metrics(meta_text, 20, False)
        title_fit = fit_size(title, 38, 30, label_inner_w, label_inner_h, True)
        meta_fit = fit_size(meta_text, 20, 16, meta_inner_w, meta_inner_h, False)
        title_pass = title_w <= label_inner_w and title_h <= label_inner_h
        meta_pass = meta_w <= meta_inner_w and meta_h <= meta_inner_h

        tx = round(ox + label[0] * slot_scale + 12)
        ty = round(oy + label[1] * slot_scale + 13)
        mx = round(ox + meta[0] * slot_scale + 7)
        my = round(oy + meta[1] * slot_scale - 1)
        title_font = f_bold(round((38 if title_pass else title_fit) * display_scale))
        meta_font = f_regular(round((20 if meta_pass else meta_fit) * display_scale))
        draw.text((tx, ty), title, font=title_font, fill="#14201b")
        draw.text((mx, my), meta_text, font=meta_font, fill="#1d2a22")

        status = "PASS" if title_pass and meta_pass else "TOKEN TODO"
        status_color = "#88ff9b" if status == "PASS" else "#ffcf66"
        row_y = 205 + i * 172
        draw.text((table_x, row_y), case_name, font=F_BODY, fill="#f3ecd0")
        draw.text((table_x, row_y + 32), f"{state} / {status}", font=F_BODY, fill=status_color)
        draw.text((table_x, row_y + 67), f"title: {title_w}x{title_h} / inner {label_inner_w}x{label_inner_h}", font=F_SMALL, fill="#d7ddc8")
        draw.text((table_x, row_y + 94), f"meta:  {meta_w}x{meta_h} / inner {meta_inner_w}x{meta_inner_h}", font=F_SMALL, fill="#d7ddc8")
        if not title_pass:
            draw.text((table_x, row_y + 124), f"title 需降至 {title_fit}px 或缩短文案", font=F_SMALL, fill="#ffcf66")
        if not meta_pass:
            draw.text((table_x, row_y + 124), f"meta 需降至 {meta_fit}px 或改短 token", font=F_SMALL, fill="#ffcf66")

        metrics.append(
            {
                "case": case_name,
                "state": state,
                "title": title,
                "meta": meta_text,
                "title_px": [title_w, title_h],
                "meta_px": [meta_w, meta_h],
                "title_inner_px": [label_inner_w, label_inner_h],
                "meta_inner_px": [meta_inner_w, meta_inner_h],
                "title_pass_at_target": title_pass,
                "meta_pass_at_target": meta_pass,
                "title_fit_px": title_fit,
                "meta_fit_px": meta_fit,
            }
        )

    note_x = 1174
    draw.rounded_rectangle((1140, 140, 1856, 970), radius=8, fill="#20251d", outline="#4d5b43", width=2)
    draw.text((note_x, 166), "结论", font=F_TITLE, fill="#f4efd9")
    body = (
        "1. 当前已用文案在 label_plate 内可读；运行时 389 也能落入合同槽。\n"
        "2. meta_line 的几何槽只有 10px 高，是当前主风险：能塞下，但远景读感偏贴边。\n"
        "3. 7 字地区名与两位数条件属于压力文案：不扩槽，优先缩短为 token（如 缺3线报 / 高危 / 荐2），"
        "或记录最终字体确定后重跑。\n"
        "4. 本板不代表冻结字体；只作为候选 B 复审与 UX 裁决证据。"
    )
    text_box(draw, (note_x, 230), body, F_BODY, "#d9deca", 640)
    draw.text((note_x, 520), "源证据", font=F_SUBTITLE, fill="#f4efd9")
    source = (
        "386/387: Python runtime fill\n"
        "389/390: Godot windowed opengl3 real capture\n"
        "Contract: left_region_card.json v0.8.2"
    )
    text_box(draw, (note_x, 560), source, F_BODY, "#c6ceb6", 640)
    canvas.save(OUT_TEXT_PRESSURE)
    return metrics


def build_review_board() -> None:
    runtime = Image.open(RUNTIME_GODOT).convert("RGB")
    benchmark = Image.open(BENCHMARK).convert("RGB")

    canvas = Image.new("RGB", (1920, 1080), "#111716")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((46, 30), "候选 B 复审板｜Godot 运行截图 vs WMW 标杆左栏", font=F_TITLE, fill="#f4efd9")
    draw.text(
        (46, 76),
        "左：389 真实运行回填截图（B 四状态）。右：258 标杆截图对应左栏区域。B 仍为候选，等待观感裁决。",
        font=F_SUBTITLE,
        fill="#cfd7be",
    )

    runtime_crop = runtime.crop((18, 0, 458, 1080))
    bench_crop = benchmark.crop((20, 80, 470, min(1080, benchmark.height)))
    paste_contain(canvas, runtime_crop, (54, 138, 514, 1008))
    paste_contain(canvas, bench_crop, (566, 138, 1026, 1008))
    draw.rectangle((54, 138, 514, 1008), outline="#6ec6ff", width=3)
    draw.rectangle((566, 138, 1026, 1008), outline="#f1c05f", width=3)
    draw.text((54, 111), "候选 B / 389 Godot runtime", font=F_BODY, fill="#9be6ff")
    draw.text((566, 111), "标杆 / 258 benchmark crop", font=F_BODY, fill="#ffd98c")

    panel_x = 1080
    draw.rounded_rectangle((1058, 138, 1860, 1008), radius=8, fill="#20261f", outline="#4b5b45", width=2)
    draw.text((panel_x, 166), "差异点供裁决", font=F_TITLE, fill="#f4efd9")
    diffs = (
        "卡片厚度：B 的外框更厚、更像单独 UI 卡；标杆更薄，更贴近整屏地图板。\n"
        "label 纸签：B 纸签干净、方正、可写区稳定；标杆纸签更融入纸张/油墨，但运行时可写安全性更难。\n"
        "图片槽气质：B 是通用低多边形风景，安全但地区识别弱；标杆有更强的场景/物件暗示。\n"
        "状态矩阵：B 四状态同构已成立；但非 selected 也有绿边，selected 独占性被削弱。\n"
        "文字融合：B 可读，但 meta_line 像测试字贴上去；需要文案 token 与墨色/字号 token 微调。"
    )
    text_box(draw, (panel_x, 230), diffs, F_BODY, "#dce2d0", 720)
    draw.text((panel_x, 620), "建议裁决口径", font=F_SUBTITLE, fill="#f4efd9")
    verdict = (
        "若接受 B：进入局部美术微调（减薄外框、清理绿边、增强 photo_slot 地区感）并重跑 atlas/Godot。\n"
        "若不接受 B：回 brief 再生/手修，仍沿用 382 wireframe anchor 与 v0.8.2 合同槽。"
    )
    text_box(draw, (panel_x, 666), verdict, F_BODY, "#cfd8c2", 720)
    canvas.save(OUT_REVIEW_BOARD)


def build_light_contract_board() -> None:
    canvas = Image.new("RGB", (1920, 1080), "#151a18")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((44, 34), "WMW 轻合同合并板｜map_panel / top_status_strip / icon_badge", font=F_TITLE, fill="#f4efd9")
    draw.text(
        (44, 80),
        "草案，不写 frozen，不阻塞 left_region_card 候选 B 裁决；后续 atlas 前再升为正式合同或图集清单。",
        font=F_SUBTITLE,
        fill="#cfd7be",
    )

    sections = [
        (44, 136, 606, 970, "map_panel 烘焙分界"),
        (680, 136, 1236, 970, "top_status_strip 低密度轻合同"),
        (1310, 136, 1876, 970, "icon_badge 清单 + 尺寸网格"),
    ]
    for x1, y1, x2, y2, title in sections:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=8, fill="#20261f", outline="#4b5b45", width=2)
        draw.text((x1 + 26, y1 + 24), title, font=F_SUBTITLE, fill="#f4efd9")

    # map_panel
    x, y = 70, 205
    draw.rectangle((x, y, x + 500, y + 280), fill="#17242a", outline="#7b8f78", width=2)
    for gx in range(x + 40, x + 500, 80):
        draw.line((gx, y, gx, y + 280), fill="#2c3d3f", width=1)
    for gy in range(y + 40, y + 280, 56):
        draw.line((x, gy, x + 500, gy), fill="#2c3d3f", width=1)
    draw.polygon([(x + 60, y + 120), (x + 130, y + 70), (x + 220, y + 105), (x + 180, y + 190)], fill="#5f7656")
    draw.polygon([(x + 260, y + 82), (x + 420, y + 112), (x + 460, y + 220), (x + 300, y + 204)], fill="#78815a")
    draw.line((x + 118, y + 118, x + 314, y + 148, x + 408, y + 178), fill="#f4cf58", width=5)
    for px, py, color in [(118, 118, "#f25d5d"), (314, 148, "#e7e07c"), (408, 178, "#78e48f")]:
        draw.ellipse((x + px - 10, y + py - 10, x + px + 10, y + py + 10), fill=color, outline="#101410", width=2)
    draw.text((70, 520), "烘焙到底图", font=F_BODY, fill="#f4efd9")
    text_box(draw, (70, 555), "深色地图板、低多边形陆块、网格/海线、静态纸张边框、无文字的地域底纹。", F_SMALL, "#d7ddc8", 490)
    draw.text((70, 690), "全部运行时", font=F_BODY, fill="#f4efd9")
    text_box(draw, (70, 725), "pin、路线、选中环、hover、locked/heat overlay、tooltip、文字与点击热区。", F_SMALL, "#d7ddc8", 490)

    # top_status_strip
    x, y = 716, 230
    draw.rectangle((x, y, x + 484, y + 68), fill="#26302b", outline="#7b8f78", width=2)
    for i, label in enumerate(["周 03", "线报 12", "压力 47", "发行 2/4"]):
        cx = x + 28 + i * 118
        draw.ellipse((cx, y + 22, cx + 24, y + 46), fill="#d8d082", outline="#111")
        draw.text((cx + 34, y + 22), label, font=F_SMALL, fill="#f4efd9")
    draw.text((706, 344), "建议约束", font=F_BODY, fill="#f4efd9")
    text_box(
        draw,
        (706, 382),
        "参考高度 44-48px；运行时 66-72px。只放 3-5 个低密度状态项，每项 icon 24-32px + 一行短数字；不承载长说明，不做移动断点。",
        F_SMALL,
        "#d7ddc8",
        492,
    )
    draw.text((706, 590), "运行时优先级", font=F_BODY, fill="#f4efd9")
    text_box(draw, (706, 628), "数字 / 短标签运行时；背景条、分隔线、轻纹理可烘焙；红黄警示只做局部 token。", F_SMALL, "#d7ddc8", 492)

    # icon badge
    x, y = 1350, 230
    draw.text((x, y), "基础格：32x32 ref / 64x64 atlas", font=F_BODY, fill="#f4efd9")
    grid_x, grid_y = x, y + 58
    labels = ["world", "target", "warn", "lock", "check", "dispatch", "dossier", "eye", "pin", "route"]
    colors = ["#8fd0ff", "#f0cd72", "#f25d5d", "#9aa0a0", "#85dd90"] * 2
    for i, label in enumerate(labels):
        gx = grid_x + (i % 5) * 94
        gy = grid_y + (i // 5) * 108
        draw.rectangle((gx, gy, gx + 64, gy + 64), outline="#7b8f78", width=2)
        draw.ellipse((gx + 12, gy + 12, gx + 52, gy + 52), fill=colors[i], outline="#111", width=2)
        draw.text((gx, gy + 72), label, font=F_TINY, fill="#d7ddc8")
    draw.text((1350, 560), "规则", font=F_BODY, fill="#f4efd9")
    text_box(
        draw,
        (1350, 596),
        "图标内芯 22-24px ref；外贴纸/徽章可占满 32px。不得烘焙文字、数字、地区名；状态色由 token 控制，别把 selected 绿边扩散到所有状态。",
        F_SMALL,
        "#d7ddc8",
        475,
    )
    canvas.save(OUT_LIGHT_CONTRACT)


def main() -> None:
    contract = load_contract()
    metrics = build_text_pressure_board(contract)
    build_review_board()
    build_light_contract_board()
    print(json.dumps({"text_pressure_metrics": metrics}, ensure_ascii=False, indent=2))
    print(json.dumps({"image_stats": [image_stats(p) for p in [OUT_TEXT_PRESSURE, OUT_REVIEW_BOARD, OUT_LIGHT_CONTRACT]]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
