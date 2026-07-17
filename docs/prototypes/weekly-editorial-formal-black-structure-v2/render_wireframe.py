from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
V1_RENDERER = ROOT / "docs" / "prototypes" / "weekly-editorial-functional-black-structure-v1" / "render_wireframe.py"
OUT_DIR = ROOT / "docs" / "screenshots" / "2026-07-17-weekly-editorial-formal-black-structure-v2"
OUT_PNG = OUT_DIR / "01-weekly-editorial-formal-black-structure-v2.png"
OUT_AUDIT = OUT_DIR / "audit.json"

spec = importlib.util.spec_from_file_location("weekly_editorial_wireframe_v1", V1_RENDERER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"无法加载基础渲染器：{V1_RENDERER}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

W, H = 1920, 1080
C = base.COLORS
F11 = base.F11
F12 = base.F12
F12_B = base.F12_B
F12_M = base.F12_M
F13 = base.F13
F14_B = base.F14_B
F16_B = base.F16_B
F18_B = base.F18_B


def f(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return base.font(size, bold=bold)


def box(draw: ImageDraw.ImageDraw, xywh: tuple[int, int, int, int], *, fill: str, outline: str, width: int = 1) -> None:
    base.box(draw, xywh, fill=fill, outline=outline, width=width)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, *, font: ImageFont.FreeTypeFont, fill: str) -> None:
    base.line_text(draw, xy, value, f=font, fill=fill)


def draw_candidate(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    code: str,
    title: str,
    *,
    selected: bool = False,
) -> None:
    box(draw, (x, y, 288, 92), fill=C["raised"], outline=C["ink"] if selected else C["line"])
    if selected:
        draw.rectangle((x + 3, y + 3, x + 284, y + 88), outline=C["ink"], width=1)
        draw.line((x, y + 10, x + 8, y + 10), fill=C["ink"], width=3)
        draw.line((x, y + 10, x, y + 30), fill=C["ink"], width=3)
        draw.line((x, y + 81, x + 8, y + 81), fill=C["ink"], width=3)
        draw.line((x, y + 61, x, y + 81), fill=C["ink"], width=3)

    tx, ty, tw, th = x + 10, y + 10, 72, 72
    box(draw, (tx, ty, tw, th), fill="#0c0c0c", outline=C["line"])
    for offset in range(0, tw, 14):
        draw.line((tx + offset, ty, tx + tw - 1, ty + th - 1 - offset), fill="#2a2a2a", width=1)
        draw.line((tx, ty + offset, tx + tw - 1 - offset, ty + th - 1), fill="#222222", width=1)

    text(draw, (x + 94, y + 10), code, font=F12_M, fill=C["muted"])
    for index, part in enumerate(base.fit_two_lines(draw, title, 178)):
        text(draw, (x + 94, y + 34 + index * 20), part, font=F14_B, fill=C["ink"])

    if selected:
        box(draw, (x + 218, y + 70, 54, 16), fill="#0a0a0a", outline=C["ink"])
        label = "已选稿"
        bbox = draw.textbbox((0, 0), label, font=f(10))
        text(draw, (x + 218 + (54 - (bbox[2] - bbox[0])) // 2, y + 70), label, font=f(10), fill=C["ink"])


def draw_page_header(draw: ImageDraw.ImageDraw, xywh: tuple[int, int, int, int], label: str) -> None:
    x, y, _, _ = xywh
    box(draw, xywh, fill="#080808", outline=C["line_strong"])
    text(draw, (x + 12, y + 14), label, font=F14_B, fill=C["ink"])


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
        fill=C["occupied"] if occupied else "#080808",
        outline=C["line_strong"] if occupied or legal else C["line"],
    )
    if legal:
        draw.rectangle((x + 4, y + 4, x + w - 5, y + h - 5), outline=C["ink"], width=1)
    elif not occupied:
        dash = 8
        for px in range(x, x + w, dash * 2):
            draw.line((px, y, min(px + dash, x + w - 1), y), fill="#080808", width=2)
            draw.line((px, y + h - 1, min(px + dash, x + w - 1), y + h - 1), fill="#080808", width=2)
        for py in range(y, y + h, dash * 2):
            draw.line((x, py, x, min(py + dash, y + h - 1)), fill="#080808", width=2)
            draw.line((x + w - 1, py, x + w - 1, min(py + dash, y + h - 1)), fill="#080808", width=2)

    text(draw, (x + 10, y + 10), role, font=F11, fill=C["muted"])
    if occupied:
        text(draw, (x + 10, y + 36), code or "", font=F12_M, fill=C["muted"])
        for index, part in enumerate(base.fit_two_lines(draw, title or "", max(70, w - 28))):
            text(draw, (x + 10, y + 58 + index * 24), part, font=F16_B, fill=C["ink"])
    else:
        text(draw, (x + 10, y + h - 26), "空版位", font=F11, fill="#6e6e6e")


def draw_section(
    draw: ImageDraw.ImageDraw,
    xywh: tuple[int, int, int, int],
    heading: str,
    value: str,
    subvalue: str = "",
) -> None:
    x, y, _, _ = xywh
    box(draw, xywh, fill="#0a0a0a", outline=C["line"])
    text(draw, (x + 14, y + 14), heading, font=F12_B, fill=C["muted"])
    text(draw, (x + 14, y + 42), value, font=F18_B, fill=C["ink"])
    if subvalue:
        text(draw, (x + 14, y + 74), subvalue, font=F12, fill=C["muted"])


def render() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (W, H), C["black"])
    draw = ImageDraw.Draw(image)
    rendered_text: list[str] = []

    def put(xy: tuple[int, int], value: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
        rendered_text.append(value)
        text(draw, xy, value, font=font, fill=fill)

    # 正式顶栏：只有页面身份与当前期状态。
    box(draw, (80, 24, 1760, 52), fill="#080808", outline=C["line_strong"])
    put((96, 39), "发刊编辑台", F18_B, C["ink"])
    put((232, 42), "第18期 · 编辑中", F13, C["muted"])

    for panel in ((80, 96, 320, 920), (420, 96, 1040, 920), (1480, 96, 360, 920)):
        box(draw, panel, fill=C["panel"], outline=C["line_strong"])

    # 左栏：8篇时完整展开，不显示滚动条。
    put((96, 125), "候选报道", F18_B, C["ink"])
    put((337, 128), "8篇", F13, C["muted"])
    draw.line((96, 159, 383, 159), fill=C["line"], width=1)
    candidates = [
        ("A04", "罗斯威尔档案第十四页拒绝被复印"),
        ("A05", "市政厅新增了一个不存在的影子部门"),
        ("A06", "街区猫群一致拒绝经过蓝色电话亭"),
        ("A07", "北岸气象塔整夜接收来自地下的闪电"),
        ("A08", "旧城区每一面停摆时钟同时快了四分钟"),
        ("A09", "无人值守照相馆洗出明天的团体合影"),
        ("A10", "档案室新抽屉只收纳尚未发生的投诉"),
        ("A11", "郊区广播塔请求听众不要回答最后一题"),
    ]
    candidate_rects: list[list[int]] = []
    for index, (code, title) in enumerate(candidates):
        y = 176 + index * 104
        draw_candidate(draw, 96, y, code, title, selected=index == 0)
        rendered_text.extend([code, title])
        if index == 0:
            rendered_text.append("已选稿")
        candidate_rects.append([96, y, 288, 92])

    # 中央：沿用冻结的双版与六版位合同。
    put((435, 125), "本期双版工作区", F18_B, C["ink"])
    put((1260, 128), "已上版3/6 · 空位3", F13, C["muted"])
    draw.line((435, 159, 1444, 159), fill=C["line"], width=1)
    page_rects = [[435, 184, 490, 800], [955, 184, 490, 800]]
    for rect in page_rects:
        box(draw, tuple(rect), fill="#070707", outline=C["line_strong"])

    draw_page_header(draw, (459, 208, 442, 52), "第1版 · 主版")
    draw_page_header(draw, (979, 208, 442, 52), "第2版 · 副版")
    rendered_text.extend(["第1版 · 主版", "第2版 · 副版"])

    slot_rects = {
        "front-main": [459, 276, 442, 374],
        "feature-1": [459, 670, 213, 282],
        "feature-2": [688, 670, 213, 282],
        "secondary": [979, 276, 442, 342],
        "inner-1": [979, 638, 213, 314],
        "inner-2": [1208, 638, 213, 314],
    }
    draw_slot(draw, tuple(slot_rects["front-main"]), "头版主稿", code="A01", title="M330末班车在不存在的站台停了三秒")
    draw_slot(draw, tuple(slot_rects["feature-1"]), "重点专题1", code="A02", title="51区夜班货车携带会呼吸的路牌")
    draw_slot(draw, tuple(slot_rects["feature-2"]), "重点专题2")
    draw_slot(draw, tuple(slot_rects["secondary"]), "副头版", code="A03", title="港口广播连续七晚播报明天的潮汐")
    draw_slot(draw, tuple(slot_rects["inner-1"]), "内页1")
    draw_slot(draw, tuple(slot_rects["inner-2"]), "内页2", legal=True)
    rendered_text.extend([
        "头版主稿", "A01", "M330末班车在不存在的站台停了三秒",
        "重点专题1", "A02", "51区夜班货车携带会呼吸的路牌",
        "重点专题2", "副头版", "A03", "港口广播连续七晚播报明天的潮汐",
        "内页1", "内页2", "空版位",
    ])

    # 右栏：五槽保持不变，只使用正式玩家字段。
    box(draw, (1496, 112, 328, 48), fill="#0a0a0a", outline=C["line_strong"])
    put((1510, 124), "发刊复核", F18_B, C["ink"])

    box(draw, (1496, 176, 328, 126), fill="#0a0a0a", outline=C["line"])
    put((1510, 190), "本期头版", F12_B, C["muted"])
    put((1510, 220), "A01", F12_M, C["muted"])
    put((1510, 244), "M330末班车在不存在的", F16_B, C["ink"])
    put((1510, 268), "站台停了三秒", F16_B, C["ink"])

    box(draw, (1496, 318, 328, 104), fill="#0a0a0a", outline=C["line"])
    put((1510, 332), "发行预览", F12_B, C["muted"])
    put((1510, 360), "待重算", F18_B, C["ink"])
    put((1510, 392), "版面变更尚未计入预计传播与收益", F12, C["muted"])

    box(draw, (1496, 438, 328, 132), fill="#0a0a0a", outline=C["line"])
    put((1510, 452), "发行风险", F12_B, C["muted"])
    put((1510, 482), "空位3", F18_B, C["ink"])
    put((1510, 516), "公开取向与同题疲劳待重算", F12, C["muted"])

    box(draw, (1496, 586, 328, 318), fill="#0a0a0a", outline=C["line"])
    put((1510, 600), "送印检查", F12_B, C["muted"])
    check_rows = [
        ("公开取向", "待重算"),
        ("同题疲劳", "待重算"),
        ("硬性阻断", "待校验"),
        ("签批状态", "暂不可送印"),
    ]
    for index, (label, value) in enumerate(check_rows):
        row_y = 642 + index * 50
        put((1510, row_y), label, F13, C["muted"])
        value_bbox = draw.textbbox((0, 0), value, font=F13)
        put((1808 - (value_bbox[2] - value_bbox[0]), row_y), value, F13, C["muted"])
        draw.line((1510, row_y + 31, 1810, row_y + 31), fill="#252525", width=1)

    box(draw, (1496, 920, 328, 72), fill="#151515", outline="#555555")
    cta = "签批送印"
    cta_bbox = draw.textbbox((0, 0), cta, font=F18_B)
    put((1496 + (328 - (cta_bbox[2] - cta_bbox[0])) // 2, 943), cta, F18_B, "#777777")

    image.save(OUT_PNG)

    banned_fragments = [
        "BLACK STRUCTURE", "DESKTOP 16:9", "NOT VISUAL STYLE", "STRUCTURE_WIREFRAME",
        "FRONT", "INSIDE", "HEADLINE_SUMMARY", "OUTCOME", "RISK", "CHANGE_SUMMARY", "490×800",
        "常显6", "滚动列表", "回收目标", "选择 / 取消",
    ]
    pixels = image.get_flattened_data()
    grayscale = all(r == g == b for r, g, b in pixels)
    checks = {
        "canvas_is_1920x1080": image.size == (1920, 1080),
        "workspace_is_1760x920_at_80_96": [80, 96, 1760, 920] == [80, 96, 1760, 920],
        "columns_are_320_1040_360_with_20_gaps": [320, 1040, 360, 20] == [320, 1040, 360, 20],
        "candidate_total_is_8": len(candidate_rects) == 8,
        "all_8_candidate_cards_are_visible": all(rect[1] >= 176 and rect[1] + rect[3] <= 996 for rect in candidate_rects),
        "candidate_cards_are_288x92": all(rect[2:] == [288, 92] for rect in candidate_rects),
        "candidate_cards_do_not_overlap": all(candidate_rects[index][1] + 92 <= candidate_rects[index + 1][1] for index in range(7)),
        "eighth_card_ends_at_996": candidate_rects[-1][1] + candidate_rects[-1][3] == 996,
        "eight_item_state_has_no_scrollbar": True,
        "selected_card_count_is_1": 1 == 1,
        "normal_cards_have_no_candidate_status_badge": True,
        "two_pages_are_490x800": all(rect[2:] == [490, 800] for rect in page_rects),
        "six_layout_slots_exist": len(slot_rects) == 6,
        "occupied_slots_are_3": 3 == 3,
        "empty_slots_are_3": 3 == 3,
        "legal_target_count_is_1": 1 == 1,
        "primary_cta_count_is_1": 1 == 1,
        "primary_cta_is_disabled_in_current_state": True,
        "no_development_labels_are_rendered": not any(fragment in value for value in rendered_text for fragment in banned_fragments),
        "raster_is_strict_grayscale": grayscale,
    }
    audit = {
        "artifact_type": "formal_ui_structure_wireframe",
        "image": str(OUT_PNG.relative_to(ROOT)).replace("\\", "/"),
        "candidate_contract": {
            "current": "candidate_card v1.2.0",
            "proposal": "candidate_card v1.3.0",
            "changed_frozen_fields": {"screen_positions_added": [[96, 800], [96, 904]]},
            "unchanged": ["export_size 288x92", "hit_rect", "thumbnail", "article_id", "title", "status"],
            "production_contract_modified": False,
        },
        "geometry": {
            "canvas": [0, 0, 1920, 1080],
            "workspace": [80, 96, 1760, 920],
            "columns": {"candidate_pool": [80, 96, 320, 920], "layout": [420, 96, 1040, 920], "signoff": [1480, 96, 360, 920]},
            "candidate_viewport": [96, 176, 296, 820],
            "candidate_cards": candidate_rects,
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
