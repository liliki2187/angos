from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[3]
FRONT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-front-carriers-v1"
OUT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-internal-slot-pressure-v1"
RUNTIME_ART_DIR = ROOT / "gd_project" / "Assets" / "prototypes" / "world_map_integrated" / "a_style_v2_runtime"

CANVAS = (1920, 1080)
BG = (1, 24, 41)
PAPER = (238, 232, 215)
INK = (23, 39, 44)
BODY_INK = (40, 54, 57)
MUTED = (89, 100, 104)
COBALT = (53, 103, 131)
OLIVE = (112, 121, 91)
RUST = (161, 73, 55)
WARM_WHITE = (241, 234, 220)
QA_GREEN = (73, 222, 161)
QA_MAGENTA = (238, 91, 184)
QA_AMBER = (244, 193, 75)
QA_RED = (236, 78, 75)

DOSSIER_SIZE = (468, 1032)
SCHEDULE_SIZE = (372, 246)
CTA_SIZE = (414, 76)

DOSSIER_SLOTS = {
    "kicker": (27, 24, 414, 24),
    "title": (27, 58, 286, 76),
    "status": (325, 60, 116, 42),
    "image": (27, 150, 414, 264),
    "headline": (27, 426, 414, 40),
    "summary": (27, 472, 414, 84),
    "disclosure": (27, 572, 414, 56),
    "preview": (27, 640, 414, 248),
    "cost": (27, 898, 414, 22),
    "cta": (27, 932, 414, 76),
}

REAL = {
    "kicker": "NEWS LEAD · 01 / 今夜校样",
    "title": "北美禁区带",
    "status": "红线升温",
    "image": "north_america_story_1104x704.png",
    "headline": "洗衣店里出现了一片海",
    "summary": "断电两小时后，潮线仍在三扇滚筒窗之间保持水平。\n店外道路干燥，最近海岸线在一千公里外。",
    "disclosure_collapsed": "任务情报    限时 1 · 线索 2 · 深链 1",
    "disclosure_expanded": "任务情报    收起",
    "collapsed_rows": [
        "4 项已知任务",
        "常驻 2 · 限时 1 · 深链 1",
        "最早截止：第 4 天",
        "展开查看完整任务列表",
    ],
    "expanded_rows": [
        "01  51 区外圈公路｜科学纪实｜2 天｜常驻",
        "02  罗斯威尔档案残页｜科学纪实｜1 天｜常驻",
        "03  雷达异常光点｜大众热度｜2 天｜限时第 4 天",
        "04  M330 末班车空白段｜神秘玄学｜2 天｜深链",
    ],
    "cost": "本次进入：0 天",
    "cta": "进入地区任务台  →",
}

CAPACITY = {
    "kicker": "NEWS LEAD · 99 / 最长字段容量测试",
    "title": "北境深层雷达异常",
    "status": "暂不可进入",
    "image": "north_america_story_1104x704.png",
    "headline": "洗衣店停电后滚筒窗里仍有潮线",
    "summary": "断电九十九小时后，潮线仍在三扇滚筒窗之间保持水平。\n店外道路完全干燥，最近海岸线在一千公里外。",
    "disclosure_collapsed": "任务情报  限时 99 · 线索 99 · 深链 99+",
    "disclosure_expanded": "任务情报    收起（已显示 4 / 99+）",
    "collapsed_rows": [
        "99+ 项已知任务",
        "常驻 99 · 限时 99 · 深链 99+",
        "最早截止：第 99 天",
        "展开查看完整任务列表",
    ],
    "expanded_rows": [
        "01  北境深层雷达异常｜科学纪实｜耗时99天｜限时第99天",
        "02  北境深层雷达异常｜科学纪实｜耗时99天｜限时第99天",
        "03  北境深层雷达异常｜科学纪实｜耗时99天｜限时第99天",
        "04  北境深层雷达异常｜科学纪实｜耗时99天｜限时第99天",
    ],
    "cost": "地区任务预计耗时：99 天",
    "cta": "进入地区任务台  →",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def runtime_asset(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.size == (size[0] * 2, size[1] * 2):
        return image.resize(size, Image.Resampling.LANCZOS)
    if image.size == size:
        return image.copy()
    raise ValueError(f"{path} has {image.size}, expected {size} or exact 2x")


def overlay_rect(image: Image.Image, box: tuple[int, int, int, int], fill: tuple[int, int, int, int]) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y, w, h = box
    draw.rectangle((x, y, x + w - 1, y + h - 1), fill=fill)
    image.paste(Image.alpha_composite(image.convert("RGBA"), layer).convert("RGB"))


def luminance(rgb: tuple[int, int, int]) -> float:
    def channel(value: int) -> float:
        value = value / 255.0
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    light = max(luminance(fg), luminance(bg))
    dark = min(luminance(fg), luminance(bg))
    return (light + 0.05) / (dark + 0.05)


def average_rgb(image: Image.Image, rect: tuple[int, int, int, int]) -> tuple[int, int, int]:
    x, y, w, h = rect
    stat = ImageStat.Stat(image.crop((x, y, x + w, y + h)).resize((1, 1), Image.Resampling.BOX))
    return tuple(round(value) for value in stat.mean[:3])


def line_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont) -> float:
    return float(draw.textlength(text, font=face))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and line_width(draw, candidate, face) > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        lines.append(current)
    return lines


def draw_text_slot(
    image: Image.Image,
    audit: list[dict[str, Any]],
    name: str,
    rect: tuple[int, int, int, int],
    text: str,
    size: int,
    color: tuple[int, int, int],
    *,
    bold: bool = False,
    align: str = "left",
    valign: str = "center",
    wrap: bool = False,
    max_lines: int = 1,
    line_height: int | None = None,
    inset_x: int = 0,
    min_contrast: float = 4.5,
    fixture_source: str = "runtime_truth",
) -> None:
    before = image.copy()
    draw = ImageDraw.Draw(image)
    face = font(size, bold)
    x, y, w, h = rect
    available_w = max(1, w - inset_x * 2)
    lines = wrap_text(draw, text, face, available_w) if wrap else text.split("\n")
    lines = lines[:max_lines]
    step = line_height or size + 5
    total_h = step * len(lines)
    if valign == "top":
        top = y
    elif valign == "bottom":
        top = y + h - total_h
    else:
        top = y + (h - total_h) // 2

    union: tuple[int, int, int, int] | None = None
    for index, line in enumerate(lines):
        width = line_width(draw, line, face)
        if align == "right":
            tx = x + w - inset_x - width
        elif align == "center":
            tx = x + (w - width) / 2
        else:
            tx = x + inset_x
        ty = top + index * step
        draw.text((round(tx), round(ty)), line, font=face, fill=color, anchor="lt")
        bbox = draw.textbbox((round(tx), round(ty)), line, font=face, anchor="lt")
        union = bbox if union is None else (
            min(union[0], bbox[0]),
            min(union[1], bbox[1]),
            max(union[2], bbox[2]),
            max(union[3], bbox[3]),
        )

    if union is None:
        union = (x, y, x, y)
    fits = union[0] >= x and union[1] >= y and union[2] <= x + w and union[3] <= y + h
    source_bg = average_rgb(before, rect)
    ratio = contrast_ratio(color, source_bg)
    audit.append({
        "name": name,
        "text": text,
        "slot_rect": list(rect),
        "glyph_bbox": list(union),
        "font_size": size,
        "font_bold": bold,
        "line_count": len(lines),
        "max_lines": max_lines,
        "fits": fits,
        "foreground_rgb": list(color),
        "sampled_background_rgb": list(source_bg),
        "contrast_ratio": round(ratio, 3),
        "minimum_contrast": min_contrast,
        "contrast_pass": ratio >= min_contrast,
        "fixture_source": fixture_source,
    })


def draw_dossier(data: dict[str, Any], expanded: bool, fixture_id: str) -> tuple[Image.Image, dict[str, Any]]:
    image = runtime_asset(FRONT_DIR / "06-front-carrier-dossier-2x.png", DOSSIER_SIZE)
    audit: list[dict[str, Any]] = []

    # Deterministic UI geometry only. Paper material remains the approved ImageGen FrontCarrier.
    overlay_rect(image, DOSSIER_SLOTS["status"], (*RUST, 22))
    draw = ImageDraw.Draw(image)
    sx, sy, sw, sh = DOSSIER_SLOTS["status"]
    draw.rectangle((sx, sy, sx + sw - 1, sy + sh - 1), outline=RUST, width=2)

    image_slot = DOSSIER_SLOTS["image"]
    ix, iy, iw, ih = image_slot
    draw.rectangle((ix - 4, iy - 4, ix + iw + 3, iy + ih + 3), fill=(20, 41, 50))
    canonical = Image.open(RUNTIME_ART_DIR / str(data["image"])).convert("RGB")
    runtime_image = canonical.resize((iw, ih), Image.Resampling.LANCZOS)
    image.paste(runtime_image, (ix, iy))
    draw.rectangle((ix - 1, iy - 1, ix + iw, iy + ih), outline=(45, 60, 61), width=1)

    dossier_source = "capacity_fixture_only" if data is CAPACITY else "runtime_truth"
    draw_text_slot(image, audit, f"{fixture_id}.kicker", DOSSIER_SLOTS["kicker"], data["kicker"], 14, MUTED, min_contrast=4.5, fixture_source=dossier_source)
    draw_text_slot(image, audit, f"{fixture_id}.title", DOSSIER_SLOTS["title"], data["title"], 32, INK, bold=True, align="left", wrap=True, max_lines=2, line_height=38, min_contrast=3.0, fixture_source=dossier_source)
    draw_text_slot(image, audit, f"{fixture_id}.status", DOSSIER_SLOTS["status"], data["status"], 15, RUST, bold=True, align="center", min_contrast=3.0, fixture_source=dossier_source)
    draw_text_slot(image, audit, f"{fixture_id}.headline", DOSSIER_SLOTS["headline"], data["headline"], 24, INK, bold=True, min_contrast=3.0, fixture_source="capacity_fixture_only" if data is CAPACITY else "runtime_truth")
    draw_text_slot(image, audit, f"{fixture_id}.summary", DOSSIER_SLOTS["summary"], data["summary"], 16, BODY_INK, valign="top", wrap=True, max_lines=3, line_height=24, min_contrast=4.5, fixture_source="capacity_fixture_only" if data is CAPACITY else "runtime_truth")

    dx, dy, dw, dh = DOSSIER_SLOTS["disclosure"]
    overlay_rect(image, (dx, dy, dw, dh), (*PAPER, 112))
    draw = ImageDraw.Draw(image)
    draw.rectangle((dx, dy, dx + dw - 1, dy + dh - 1), outline=(112, 121, 91), width=1)
    draw.rectangle((dx, dy, dx + 6, dy + dh - 1), fill=COBALT if expanded else OLIVE)
    disclosure = data["disclosure_expanded"] if expanded else data["disclosure_collapsed"]
    draw_text_slot(image, audit, f"{fixture_id}.disclosure", (dx + 18, dy, dw - 70, dh), disclosure, 16, INK, bold=True, min_contrast=4.5, fixture_source="capacity_fixture_only" if data is CAPACITY else "runtime_truth")
    draw_text_slot(image, audit, f"{fixture_id}.disclosure_symbol", (dx + dw - 52, dy, 44, dh), "−" if expanded else "+", 20, MUTED, bold=True, align="center", min_contrast=4.5)

    px, py, pw, ph = DOSSIER_SLOTS["preview"]
    overlay_rect(image, (px, py, pw, ph), (73, 90, 81, 12 if not expanded else 18))
    draw = ImageDraw.Draw(image)
    draw.rectangle((px, py, px + pw - 1, py + ph - 1), outline=(95, 107, 94), width=1)
    rows = data["expanded_rows"] if expanded else data["collapsed_rows"]
    if expanded:
        row_y = [650, 704, 758, 812]
        row_colors = [COBALT, OLIVE, RUST, (89, 111, 114)]
        for index, row in enumerate(rows):
            y0 = row_y[index]
            draw.rectangle((35, y0, 40, y0 + 34), fill=row_colors[index])
            draw_text_slot(
                image,
                audit,
                f"{fixture_id}.preview_row_{index + 1}",
                (48, y0, 380, 36),
                row,
                14,
                INK,
                min_contrast=4.5,
                fixture_source="capacity_fixture_only" if data is CAPACITY else "runtime_truth",
            )
            if index < 3:
                draw.line((48, y0 + 42, 429, y0 + 42), fill=(110, 120, 109), width=1)
    else:
        row_y = [658, 706, 770, 830]
        for index, row in enumerate(rows):
            draw_text_slot(
                image,
                audit,
                f"{fixture_id}.preview_summary_{index + 1}",
                (39, row_y[index], 390, 32),
                row,
                16 if index < 2 else 14,
                INK if index < 3 else MUTED,
                bold=index == 0,
                min_contrast=4.5,
                fixture_source="capacity_fixture_only" if data is CAPACITY else "runtime_truth",
            )

    draw_text_slot(image, audit, f"{fixture_id}.cost", DOSSIER_SLOTS["cost"], data["cost"], 14, MUTED, align="right", min_contrast=4.5, fixture_source="capacity_fixture_only" if data is CAPACITY else "runtime_truth")
    cta, cta_audit = draw_cta("default", data["cta"], f"{fixture_id}.cta")
    image.paste(cta, (DOSSIER_SLOTS["cta"][0], DOSSIER_SLOTS["cta"][1]))
    for item in cta_audit:
        shifted = dict(item)
        shifted["slot_rect"] = [
            item["slot_rect"][0] + DOSSIER_SLOTS["cta"][0],
            item["slot_rect"][1] + DOSSIER_SLOTS["cta"][1],
            item["slot_rect"][2],
            item["slot_rect"][3],
        ]
        shifted["glyph_bbox"] = [
            item["glyph_bbox"][0] + DOSSIER_SLOTS["cta"][0],
            item["glyph_bbox"][1] + DOSSIER_SLOTS["cta"][1],
            item["glyph_bbox"][2] + DOSSIER_SLOTS["cta"][0],
            item["glyph_bbox"][3] + DOSSIER_SLOTS["cta"][1],
        ]
        audit.append(shifted)

    return image, {
        "fixture_id": fixture_id,
        "fixture_type": "capacity_fixture_only" if data is CAPACITY else "runtime_truth",
        "expanded": expanded,
        "size": list(image.size),
        "slots": {key: list(value) for key, value in DOSSIER_SLOTS.items()},
        "glyph_checks": audit,
        "image_contract": {
            "source": str((RUNTIME_ART_DIR / str(data["image"])).relative_to(ROOT)).replace("\\", "/"),
            "source_size": list(canonical.size),
            "runtime_rect": list(image_slot),
            "source_ratio": canonical.width / canonical.height,
            "runtime_ratio": iw / ih,
            "ratio_error": abs(canonical.width / canonical.height - iw / ih) / (canonical.width / canonical.height),
            "full_uv": True,
            "crop": False,
            "upsample": iw > canonical.width or ih > canonical.height,
        },
        "input_contract": {
            "root": "MOUSE_FILTER_PASS; not a full-page Button",
            "interactive_rects": {
                "MissionDisclosure": list(DOSSIER_SLOTS["disclosure"]),
                "PrimaryEnterCta": list(DOSSIER_SLOTS["cta"]),
            },
            "preview_rows_interactive": False,
        },
    }


def draw_cta(state: str, text: str, audit_id: str) -> tuple[Image.Image, list[dict[str, Any]]]:
    base = runtime_asset(FRONT_DIR / "08-front-carrier-cta-default-2x.png", CTA_SIZE)
    if state == "hover":
        base = ImageEnhance.Brightness(base).enhance(1.08)
    elif state == "pressed":
        base = ImageEnhance.Brightness(base).enhance(0.92)
    elif state == "disabled":
        muted = ImageEnhance.Color(base).enhance(0.60)
        base = Image.blend(muted, Image.new("RGB", CTA_SIZE, (119, 120, 104)), 0.20)

    draw = ImageDraw.Draw(base)
    draw.rectangle((0, 0, 6, CTA_SIZE[1] - 1), fill=RUST if state != "disabled" else (120, 101, 91))
    if state == "hover":
        draw.rectangle((11, 8, CTA_SIZE[0] - 12, CTA_SIZE[1] - 9), outline=(177, 179, 139), width=1)
    elif state == "pressed":
        draw.rectangle((10, 7, CTA_SIZE[0] - 11, CTA_SIZE[1] - 8), outline=(61, 67, 48), width=2)
    if state == "focus":
        draw.rectangle((1, 1, CTA_SIZE[0] - 2, CTA_SIZE[1] - 2), outline=(102, 151, 165), width=2)
    audit: list[dict[str, Any]] = []
    draw_text_slot(
        base,
        audit,
        audit_id,
        (24, 10, 366, 56),
        text,
        22,
        WARM_WHITE if state != "disabled" else (196, 195, 179),
        bold=True,
        align="center",
        min_contrast=3.0,
        fixture_source="ui_state_fixture",
    )
    return base, audit


def draw_schedule(mode: str, fixture_id: str) -> tuple[Image.Image, dict[str, Any]]:
    image = runtime_asset(FRONT_DIR / "07-front-carrier-schedule-2x.png", SCHEDULE_SIZE)
    if mode == "real":
        current, remaining = "当前第 1 天", "剩余 7 天"
        title, note = "日程推进暂未开放", "当前版本不可操作"
        impact, zero = "当前：无任务到期", "日程归零：进入编辑部阶段"
        source = "runtime_truth"
    elif mode == "two_digit":
        current, remaining = "当前第 99 天", "剩余 99 天"
        title, note = "日程推进暂未开放", "两位数容量测试｜仍不可操作"
        impact, zero = "当前：99 项任务待复核", "日程归零：进入编辑部阶段"
        source = "capacity_fixture_only"
    elif mode == "zero_day":
        current, remaining = "本周日程结束", "剩余 0 天"
        title, note = "不可继续推进", "下一阶段：编辑部"
        impact, zero = "当前：结算周刊版面", "日程归零：进入编辑部阶段"
        source = "boundary_fixture_only"
    else:
        raise ValueError(mode)

    audit: list[dict[str, Any]] = []
    draw = ImageDraw.Draw(image)
    draw_text_slot(image, audit, f"{fixture_id}.kicker", (16, 8, 220, 18), "GLOBAL SCHEDULE / 全局日程", 11, MUTED, valign="top", min_contrast=4.5, fixture_source=source)
    draw_text_slot(image, audit, f"{fixture_id}.current", (16, 28, 156, 34), current, 23, INK, bold=True, min_contrast=3.0, fixture_source=source)
    draw_text_slot(image, audit, f"{fixture_id}.remaining", (188, 30, 168, 30), remaining, 16, COBALT, bold=True, align="right", min_contrast=3.0, fixture_source=source)

    overlay_rect(image, (16, 72, 340, 94), (112, 121, 91, 28))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 72, 355, 165), outline=(112, 121, 91), width=1)
    draw.rectangle((28, 84, 97, 153), fill=(214, 212, 198), outline=(165, 167, 153), width=1)
    draw_text_slot(image, audit, f"{fixture_id}.static_mark", (28, 84, 70, 70), "—", 24, (72, 84, 84), align="center", min_contrast=4.5, fixture_source=source)
    draw_text_slot(image, audit, f"{fixture_id}.action", (116, 84, 220, 34), title, 18, INK, bold=True, min_contrast=3.0, fixture_source=source)
    draw_text_slot(image, audit, f"{fixture_id}.note", (116, 122, 220, 28), note, 13, (70, 84, 87), min_contrast=4.5, fixture_source=source)
    draw_text_slot(image, audit, f"{fixture_id}.impact", (16, 176, 340, 24), impact, 13, INK, min_contrast=4.5, fixture_source=source)
    draw.line((16, 202, 356, 202), fill=(164, 164, 147), width=1)
    draw_text_slot(image, audit, f"{fixture_id}.zero", (16, 206, 340, 24), zero, 13, RUST, min_contrast=4.5, fixture_source=source)
    return image, {
        "fixture_id": fixture_id,
        "mode": mode,
        "fixture_type": source,
        "size": list(image.size),
        "safe_rect": [16, 8, 356, 230],
        "glyph_checks": audit,
        "input_contract": {
            "root": "MOUSE_FILTER_IGNORE / FOCUS_NONE",
            "interactive_rects": {},
            "descendant_pointer_consumers": 0,
            "descendant_focusables": 0,
        },
    }


def label_board(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color: tuple[int, int, int] = WARM_WHITE) -> None:
    draw.text(xy, text, font=font(12, True), fill=color, anchor="lt")


def build_board(
    left: Image.Image,
    collapsed: Image.Image,
    expanded: Image.Image,
    cta_states: list[tuple[str, Image.Image]],
    title: str,
    left_secondary: Image.Image | None = None,
) -> Image.Image:
    board = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(board)
    draw.text((24, 10), title, font=font(17, True), fill=WARM_WHITE, anchor="lt")
    draw.text((24, 38), "QA ONLY / 正交 FrontCarrier / 原生运行时尺寸 / 非最终美术", font=font(12), fill=(147, 174, 171), anchor="lt")

    left_y = 120
    board.paste(left, (24, left_y))
    label_board(draw, (24, left_y - 22), "SCHEDULE · 372×246 · NO INPUT", QA_GREEN)
    if left_secondary is not None:
        board.paste(left_secondary, (24, left_y + 286))
        label_board(draw, (24, left_y + 264), "SCHEDULE BOUNDARY · 372×246 · NO INPUT", QA_AMBER)

    collapsed_xy = (420, 24)
    expanded_xy = (912, 24)
    board.paste(collapsed, collapsed_xy)
    board.paste(expanded, expanded_xy)
    label_board(draw, (collapsed_xy[0] + 278, 4), "COLLAPSED · 468×1032", QA_GREEN)
    label_board(draw, (expanded_xy[0] + 278, 4), "EXPANDED · 468×1032", QA_GREEN)

    cta_x = 1404
    cta_y = 118
    draw.text((cta_x, 72), "PRIMARY CTA · 414×76 / ZERO SHIFT", font=font(13, True), fill=QA_GREEN, anchor="lt")
    for index, (state, cta) in enumerate(cta_states):
        y = cta_y + index * 116
        label_board(draw, (cta_x, y - 20), state.upper(), QA_AMBER if state == "disabled" else (165, 187, 178))
        board.paste(cta, (cta_x, y))

    draw.text((24, 840), "固定交互", font=font(14, True), fill=WARM_WHITE, anchor="lt")
    draw.text((24, 870), "Dossier：仅 Disclosure + CTA", font=font(13), fill=(174, 193, 185), anchor="lt")
    draw.text((24, 896), "Schedule：整棵树忽略输入", font=font(13), fill=(174, 193, 185), anchor="lt")
    draw.text((24, 922), "Preview：只读，任务行无热区", font=font(13), fill=(174, 193, 185), anchor="lt")
    draw.text((24, 966), "图片同源", font=font(14, True), fill=WARM_WHITE, anchor="lt")
    draw.text((24, 996), "1104×704 → 414×264", font=font(13), fill=(174, 193, 185), anchor="lt")
    draw.text((24, 1022), "69:44 · 全幅UV · 无裁切", font=font(13), fill=QA_GREEN, anchor="lt")
    return board


def qa_overlay(board: Image.Image) -> Image.Image:
    qa = board.copy()
    draw = ImageDraw.Draw(qa)
    for origin in [(420, 24), (912, 24)]:
        ox, oy = origin
        draw.rectangle((ox, oy, ox + DOSSIER_SIZE[0] - 1, oy + DOSSIER_SIZE[1] - 1), outline=QA_GREEN, width=2)
        for name, rect in DOSSIER_SLOTS.items():
            x, y, w, h = rect
            color = QA_MAGENTA if name in {"disclosure", "cta"} else QA_AMBER if name == "image" else QA_GREEN
            draw.rectangle((ox + x, oy + y, ox + x + w - 1, oy + y + h - 1), outline=color, width=1)
            draw.text((ox + x + 2, oy + y + 2), name, font=font(9, True), fill=color, anchor="lt")
    draw.text((1404, 900), "green = frozen slot", font=font(12, True), fill=QA_GREEN, anchor="lt")
    draw.text((1404, 926), "amber = canonical image", font=font(12, True), fill=QA_AMBER, anchor="lt")
    draw.text((1404, 952), "magenta = only hit rects", font=font(12, True), fill=QA_MAGENTA, anchor="lt")
    return qa


def diff_contract(collapsed: Image.Image, expanded: Image.Image) -> dict[str, Any]:
    mutable = {"disclosure", "preview"}
    results: dict[str, Any] = {}
    for name, rect in DOSSIER_SLOTS.items():
        x, y, w, h = rect
        bbox = ImageChops.difference(
            collapsed.crop((x, y, x + w, y + h)),
            expanded.crop((x, y, x + w, y + h)),
        ).getbbox()
        results[name] = {
            "rect": list(rect),
            "mutable_by_contract": name in mutable,
            "pixel_delta_bbox": list(bbox) if bbox else None,
            "zero_shift_pass": (bbox is None) if name not in mutable else True,
        }
    return results


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    real_collapsed, real_c = draw_dossier(REAL, False, "D1_real_collapsed")
    real_expanded, real_e = draw_dossier(REAL, True, "D2_real_expanded")
    capacity_collapsed, capacity_c = draw_dossier(CAPACITY, False, "D5_capacity_collapsed")
    capacity_expanded, capacity_e = draw_dossier(CAPACITY, True, "D6_capacity_expanded")

    schedule_real, schedule_r = draw_schedule("real", "S1_real_disabled")
    schedule_digits, schedule_d = draw_schedule("two_digit", "S2_two_digit_disabled")
    schedule_zero, schedule_z = draw_schedule("zero_day", "S3_zero_day_disabled")

    cta_specs = [
        ("default", "进入地区任务台  →"),
        ("hover", "进入地区任务台  →"),
        ("pressed", "进入地区任务台  →"),
        ("focus", "进入地区任务台  →"),
        ("disabled", "暂不可进入"),
    ]
    cta_states: list[tuple[str, Image.Image]] = []
    cta_audits: dict[str, Any] = {}
    for state, label in cta_specs:
        bitmap, checks = draw_cta(state, label, f"CTA_{state}")
        cta_states.append((state, bitmap))
        cta_audits[state] = {
            "size": list(bitmap.size),
            "hit_rect": [0, 0, 414, 76] if state != "disabled" else None,
            "focusable": state != "disabled",
            "pointer_enabled": state != "disabled",
            "glyph_checks": checks,
        }

    real_board = build_board(
        schedule_real,
        real_collapsed,
        real_expanded,
        cta_states,
        "INTERNAL SLOT PRESSURE · REAL CONTENT",
    )
    capacity_board = build_board(
        schedule_digits,
        capacity_collapsed,
        capacity_expanded,
        cta_states,
        "INTERNAL SLOT PRESSURE · CAPACITY FIXTURE ONLY",
        left_secondary=schedule_zero,
    )
    overlay = qa_overlay(real_board)

    outputs = {
        "01-internal-slot-pressure-clean-real.png": real_board,
        "02-internal-slot-pressure-qa-overlay.png": overlay,
        "03-internal-slot-pressure-capacity.png": capacity_board,
        "04-dossier-real-collapsed-runtime.png": real_collapsed,
        "05-dossier-real-expanded-runtime.png": real_expanded,
        "06-dossier-capacity-collapsed-runtime.png": capacity_collapsed,
        "07-dossier-capacity-expanded-runtime.png": capacity_expanded,
        "08-schedule-real-disabled-runtime.png": schedule_real,
        "09-schedule-two-digit-disabled-runtime.png": schedule_digits,
        "10-schedule-zero-day-disabled-runtime.png": schedule_zero,
    }
    for name, image in outputs.items():
        image.save(OUT_DIR / name)

    audit = {
        "stage": "internal_slot_pressure_board_v1",
        "board_role": "deterministic runtime content/geometry QA; not final art",
        "imagegen_role": "approved FrontCarrier materials and canonical region art only",
        "program_role": "orthogonal runtime layout, exact text raster, state tint and QA overlays",
        "locked_dossier_status": "not_rendered_pending_product_semantics; current runtime keeps selected dossier when locked region is clicked",
        "boards": {name: list(image.size) for name, image in outputs.items() if name.startswith(("01-", "02-", "03-"))},
        "dossiers": {
            real_c["fixture_id"]: real_c,
            real_e["fixture_id"]: real_e,
            capacity_c["fixture_id"]: capacity_c,
            capacity_e["fixture_id"]: capacity_e,
        },
        "schedules": {
            schedule_r["fixture_id"]: schedule_r,
            schedule_d["fixture_id"]: schedule_d,
            schedule_z["fixture_id"]: schedule_z,
        },
        "cta_states": cta_audits,
        "zero_shift": {
            "real_collapsed_vs_expanded": diff_contract(real_collapsed, real_expanded),
            "capacity_collapsed_vs_expanded": diff_contract(capacity_collapsed, capacity_expanded),
        },
        "release": {
            "internal_slot_pressure_board": "pending_independent_validation_and_dual_review",
            "atlas_manifest_godot": "blocked",
            "backdecor_composition": "blocked",
        },
    }
    (OUT_DIR / "11-internal-slot-pressure-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
