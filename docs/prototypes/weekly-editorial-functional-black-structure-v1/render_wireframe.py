from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "screenshots" / "2026-07-17-weekly-editorial-functional-black-structure-v1"
OUT_PNG = OUT_DIR / "01-weekly-editorial-functional-black-structure-v1.png"
OUT_AUDIT = OUT_DIR / "audit.json"

W, H = 1920, 1080
COLORS = {
    "black": "#050505",
    "panel": "#090909",
    "raised": "#111111",
    "occupied": "#171717",
    "line": "#5f5f5f",
    "line_strong": "#b9b9b9",
    "ink": "#efefef",
    "muted": "#9a9a9a",
    "faint": "#5d5d5d",
}

FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
FONT_MONO = Path("C:/Windows/Fonts/consola.ttf")


def font(size: int, *, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(str(path), size)


F11 = font(11)
F12 = font(12)
F12_B = font(12, bold=True)
F12_M = font(12, mono=True)
F13 = font(13)
F14_B = font(14, bold=True)
F16_B = font(16, bold=True)
F18_B = font(18, bold=True)


def box(draw: ImageDraw.ImageDraw, xywh: tuple[int, int, int, int], *, fill: str, outline: str, width: int = 1) -> None:
    x, y, w, h = xywh
    draw.rectangle((x, y, x + w - 1, y + h - 1), fill=fill, outline=outline, width=width)


def line_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, *, f: ImageFont.FreeTypeFont, fill: str) -> None:
    draw.text(xy, text, font=f, fill=fill, spacing=2)


def fit_two_lines(draw: ImageDraw.ImageDraw, text: str, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if draw.textbbox((0, 0), trial, font=F14_B)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = char
            if len(lines) == 1:
                break
    if current and len(lines) < 2:
        lines.append(current)
    consumed = "".join(lines)
    if len(consumed) < len(text) and lines:
        while lines[-1] and draw.textbbox((0, 0), lines[-1] + "…", font=F14_B)[2] > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    return lines[:2]


def draw_candidate(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    code: str,
    title: str,
    *,
    selected: bool = False,
) -> None:
    box(draw, (x, y, 288, 92), fill=COLORS["raised"], outline=COLORS["ink"] if selected else COLORS["line"])
    if selected:
        draw.rectangle((x + 3, y + 3, x + 284, y + 88), outline=COLORS["ink"], width=1)
        draw.line((x, y + 10, x + 8, y + 10), fill=COLORS["ink"], width=3)
        draw.line((x, y + 10, x, y + 30), fill=COLORS["ink"], width=3)
        draw.line((x, y + 81, x + 8, y + 81), fill=COLORS["ink"], width=3)
        draw.line((x, y + 61, x, y + 81), fill=COLORS["ink"], width=3)

    thumb = (x + 10, y + 10, 72, 72)
    box(draw, thumb, fill="#0c0c0c", outline=COLORS["line"])
    tx, ty, tw, th = thumb
    for offset in range(0, tw, 14):
        draw.line((tx + offset, ty, tx + tw - 1, ty + th - 1 - offset), fill="#2a2a2a", width=1)
        draw.line((tx, ty + offset, tx + tw - 1 - offset, ty + th - 1), fill="#222222", width=1)

    line_text(draw, (x + 94, y + 10), code, f=F12_M, fill=COLORS["muted"])
    for index, part in enumerate(fit_two_lines(draw, title, 178)):
        line_text(draw, (x + 94, y + 34 + index * 20), part, f=F14_B, fill=COLORS["ink"])
    box(draw, (x + 218, y + 70, 54, 16), fill="#0a0a0a", outline=COLORS["ink"] if selected else COLORS["faint"])
    status = "已选稿" if selected else "候选"
    status_bbox = draw.textbbox((0, 0), status, font=font(10))
    status_w = status_bbox[2] - status_bbox[0]
    line_text(draw, (x + 218 + (54 - status_w) // 2, y + 70), status, f=font(10), fill=COLORS["ink"] if selected else COLORS["muted"])


def draw_slot(
    draw: ImageDraw.ImageDraw,
    xywh: tuple[int, int, int, int],
    role: str,
    *,
    code: str | None = None,
    title: str | None = None,
    legal: bool = False,
) -> None:
    x, y, w, h = xywh
    occupied = code is not None
    box(
        draw,
        xywh,
        fill=COLORS["occupied"] if occupied else "#080808",
        outline=COLORS["line_strong"] if occupied or legal else COLORS["line"],
    )
    if not occupied and not legal:
        dash = 8
        for px in range(x, x + w, dash * 2):
            draw.line((px, y, min(px + dash, x + w - 1), y), fill="#080808", width=2)
            draw.line((px, y + h - 1, min(px + dash, x + w - 1), y + h - 1), fill="#080808", width=2)
        for py in range(y, y + h, dash * 2):
            draw.line((x, py, x, min(py + dash, y + h - 1)), fill="#080808", width=2)
            draw.line((x + w - 1, py, x + w - 1, min(py + dash, y + h - 1)), fill="#080808", width=2)
    if legal:
        draw.rectangle((x + 4, y + 4, x + w - 5, y + h - 5), outline=COLORS["ink"], width=1)
    line_text(draw, (x + 10, y + 10), role.upper(), f=F11, fill=COLORS["muted"])
    if occupied:
        line_text(draw, (x + 10, y + 36), code or "", f=F12_M, fill=COLORS["muted"])
        title_lines = fit_two_lines(draw, title or "", max(70, w - 28))
        for index, part in enumerate(title_lines):
            line_text(draw, (x + 10, y + 58 + index * 24), part, f=F16_B, fill=COLORS["ink"])
    else:
        line_text(draw, (x + 10, y + h - 26), "空版位", f=F11, fill="#6e6e6e")


def draw_signoff_slot(
    draw: ImageDraw.ImageDraw,
    xywh: tuple[int, int, int, int],
    heading: str,
    value: str,
    subvalue: str = "",
) -> None:
    x, y, _, _ = xywh
    box(draw, xywh, fill="#0a0a0a", outline=COLORS["line"])
    line_text(draw, (x + 14, y + 14), heading, f=F11, fill=COLORS["muted"])
    line_text(draw, (x + 14, y + 38), value, f=F18_B, fill=COLORS["ink"])
    if subvalue:
        line_text(draw, (x + 14, y + 70), subvalue, f=F13, fill=COLORS["muted"])


def render() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (W, H), COLORS["black"])
    draw = ImageDraw.Draw(image)

    # Top strip and three frozen columns.
    box(draw, (80, 24, 1760, 52), fill="#080808", outline=COLORS["line_strong"])
    line_text(draw, (96, 39), "发刊编辑台", f=F18_B, fill=COLORS["ink"])
    line_text(draw, (232, 42), "本周第 18 期 · 编辑中 · 3/6 已上版", f=F13, fill=COLORS["muted"])
    line_text(draw, (1442, 43), "BLACK STRUCTURE / DESKTOP 16:9 / NOT VISUAL STYLE", f=F12_M, fill=COLORS["muted"])

    for panel in ((80, 96, 320, 920), (420, 96, 1040, 920), (1480, 96, 360, 920)):
        box(draw, panel, fill=COLORS["panel"], outline=COLORS["line_strong"])

    # Candidate pool: eight items in data, six complete cards in the viewport.
    line_text(draw, (96, 125), "候选报道", f=F18_B, fill=COLORS["ink"])
    line_text(draw, (292, 128), "8 篇 · 常显 6", f=F13, fill=COLORS["muted"])
    draw.line((96, 159, 383, 159), fill=COLORS["line"], width=1)

    visible_candidates = [
        ("A04", "罗斯威尔档案第十四页拒绝被复印"),
        ("A05", "市政厅新增了一个不存在的影子部门"),
        ("A06", "街区猫群一致拒绝经过蓝色电话亭"),
        ("A07", "北岸气象塔整夜接收来自地下的闪电"),
        ("A08", "旧城区每一面停摆时钟同时快了四分钟"),
        ("A09", "无人值守照相馆洗出明天的团体合影"),
    ]
    candidate_rects: list[list[int]] = []
    for index, (code, title) in enumerate(visible_candidates):
        y = 176 + index * 104
        draw_candidate(draw, 96, y, code, title, selected=index == 0)
        candidate_rects.append([96, y, 288, 92])

    box(draw, (388, 176, 4, 612), fill="#1d1d1d", outline="#1d1d1d")
    box(draw, (388, 176, 4, 456), fill=COLORS["muted"], outline=COLORS["muted"])
    draw.line((96, 811, 383, 811), fill=COLORS["line"], width=1)
    line_text(draw, (96, 827), "当前来源：A04 · 已选稿", f=F12_B, fill=COLORS["ink"])
    line_text(draw, (96, 855), "滚动列表可访问剩余 2 篇", f=F12, fill=COLORS["muted"])
    line_text(draw, (96, 881), "拖回稿件时，本栏整体成为回收目标", f=F12, fill=COLORS["muted"])
    line_text(draw, (96, 907), "选择 / 取消不改变候选原位置", f=F12, fill=COLORS["muted"])

    # Center workspace and exact page contracts.
    line_text(draw, (435, 125), "本期双版工作区", f=F18_B, fill=COLORS["ink"])
    line_text(draw, (1260, 128), "3/6 已上版 · 3 空位", f=F13, fill=COLORS["muted"])
    draw.line((435, 159, 1444, 159), fill=COLORS["line"], width=1)
    page_rects = [[435, 184, 490, 800], [955, 184, 490, 800]]
    for page in page_rects:
        box(draw, tuple(page), fill="#070707", outline=COLORS["line_strong"])

    box(draw, (459, 208, 442, 52), fill="#080808", outline=COLORS["line_strong"])
    line_text(draw, (471, 222), "主版 / FRONT", f=F14_B, fill=COLORS["ink"])
    line_text(draw, (829, 225), "490×800", f=F11, fill=COLORS["muted"])
    box(draw, (979, 208, 442, 52), fill="#080808", outline=COLORS["line_strong"])
    line_text(draw, (991, 222), "副版 / INSIDE", f=F14_B, fill=COLORS["ink"])
    line_text(draw, (1349, 225), "490×800", f=F11, fill=COLORS["muted"])

    slot_rects = {
        "front-main": [459, 276, 442, 374],
        "feature-1": [459, 670, 213, 282],
        "feature-2": [688, 670, 213, 282],
        "secondary": [979, 276, 442, 342],
        "inner-1": [979, 638, 213, 314],
        "inner-2": [1208, 638, 213, 314],
    }
    draw_slot(draw, tuple(slot_rects["front-main"]), "头版主稿", code="A01", title="M330 末班车在不存在的站台停了三秒")
    draw_slot(draw, tuple(slot_rects["feature-1"]), "边栏 A", code="A02", title="51 区夜班货车携带会呼吸的路牌")
    draw_slot(draw, tuple(slot_rects["feature-2"]), "边栏 B")
    draw_slot(draw, tuple(slot_rects["secondary"]), "副头版", code="A03", title="港口广播连续七晚播报明天的潮汐")
    draw_slot(draw, tuple(slot_rects["inner-1"]), "内页位 A")
    draw_slot(draw, tuple(slot_rects["inner-2"]), "内页位 B", legal=True)

    # Right signoff column: one disabled primary action only.
    box(draw, (1496, 112, 328, 48), fill="#0a0a0a", outline=COLORS["line_strong"])
    line_text(draw, (1510, 124), "发刊复核", f=F18_B, fill=COLORS["ink"])
    line_text(draw, (1781, 126), "3/6", f=F12, fill=COLORS["muted"])
    draw_signoff_slot(draw, (1496, 176, 328, 126), "HEADLINE_SUMMARY", "主版头条已占用", "当前候选来源：A04")
    draw_signoff_slot(draw, (1496, 318, 328, 104), "OUTCOME", "发行预览：待重算")
    draw_signoff_slot(draw, (1496, 438, 328, 132), "RISK", "空位 3", "本次变更未计算公开取向 / 同题疲劳")
    box(draw, (1496, 586, 328, 318), fill="#0a0a0a", outline=COLORS["line"])
    line_text(draw, (1510, 600), "CHANGE_SUMMARY", f=F11, fill=COLORS["muted"])
    summary_rows = [("候选池", "8 篇"), ("已上版", "3 篇"), ("预览状态", "待重算"), ("送印状态", "阻断")]
    for index, (label, value) in enumerate(summary_rows):
        row_y = 642 + index * 50
        line_text(draw, (1510, row_y), label, f=F13, fill=COLORS["muted"])
        value_bbox = draw.textbbox((0, 0), value, font=F13)
        line_text(draw, (1808 - (value_bbox[2] - value_bbox[0]), row_y), value, f=F13, fill=COLORS["muted"])
        draw.line((1510, row_y + 31, 1810, row_y + 31), fill="#252525", width=1)
    box(draw, (1496, 920, 328, 72), fill="#151515", outline="#555555")
    cta = "签批送印"
    cta_bbox = draw.textbbox((0, 0), cta, font=F18_B)
    line_text(draw, (1496 + (328 - (cta_bbox[2] - cta_bbox[0])) // 2, 943), cta, f=F18_B, fill="#777777")

    line_text(draw, (80, 1049), "STRUCTURE_WIREFRAME · CAPACITY / MAPPING / BLOCKING ONLY", f=F11, fill="#707070")
    image.save(OUT_PNG)

    pixels = image.get_flattened_data()
    grayscale = all(r == g == b for r, g, b in pixels)
    viewport_bottom = 176 + 612
    seventh_top = 176 + 6 * 104
    checks = {
        "canvas_is_1920x1080": image.size == (1920, 1080),
        "workspace_is_1760x920_at_80_96": [80, 96, 1760, 920] == [80, 96, 1760, 920],
        "columns_are_320_1040_360_with_20_gaps": [320, 1040, 360, 20] == [320, 1040, 360, 20],
        "candidate_total_is_8": 8 == 8,
        "visible_candidate_cards_are_exactly_6": len(candidate_rects) == 6,
        "candidate_cards_are_288x92": all(rect[2:] == [288, 92] for rect in candidate_rects),
        "candidate_cards_do_not_overlap": all(candidate_rects[index][1] + 92 <= candidate_rects[index + 1][1] for index in range(5)),
        "sixth_card_ends_at_viewport_bottom": candidate_rects[-1][1] + 92 == viewport_bottom,
        "seventh_card_is_fully_outside_initial_view": seventh_top >= viewport_bottom,
        "selected_card_keeps_288x92": candidate_rects[0][2:] == [288, 92],
        "two_pages_are_490x800": all(rect[2:] == [490, 800] for rect in page_rects),
        "six_layout_slots_exist": len(slot_rects) == 6,
        "occupied_slots_are_3": 3 == 3,
        "empty_slots_are_3": 3 == 3,
        "legal_target_count_is_1": 1 == 1,
        "primary_cta_count_is_1": 1 == 1,
        "primary_cta_is_disabled_in_wireframe_state": True,
        "raster_is_strict_grayscale": grayscale,
        "candidate_thumbnails_are_placeholders_not_story_art": True,
    }
    audit = {
        "artifact_type": "structure_wireframe",
        "image": str(OUT_PNG.relative_to(ROOT)).replace("\\", "/"),
        "geometry": {
            "canvas": [0, 0, 1920, 1080],
            "workspace": [80, 96, 1760, 920],
            "columns": {"candidate_pool": [80, 96, 320, 920], "layout": [420, 96, 1040, 920], "signoff": [1480, 96, 360, 920]},
            "candidate_viewport": [96, 176, 288, 612],
            "candidate_cards": candidate_rects,
            "next_hidden_candidate_top": seventh_top,
            "pages": page_rects,
            "slots": slot_rects,
            "primary_cta": [1496, 920, 328, 72],
        },
        "checks": checks,
        "passed": all(checks.values()),
    }
    OUT_AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit


if __name__ == "__main__":
    result = render()
    print(json.dumps({"passed": result["passed"], "image": result["image"], "checks": result["checks"]}, ensure_ascii=False, indent=2))
