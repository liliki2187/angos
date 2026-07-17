from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from wmw_text_layout_metrics import (
    draw_text_by_raster_bbox,
    fit_font_by_raster,
    raster_text_size,
)


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
DOSSIER_CONTRACT_PATH = ROOT / "design" / "ui-contracts" / "world-map" / "right_dossier_page.json"
LANE_CONTRACT_PATH = ROOT / "design" / "ui-contracts" / "world-map" / "right_action_lane.json"
FULLSCREEN_SOURCE = BASE / "365-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-full.png"

OUT_DECISION = BASE / "559-world-map-wmw-right-dossier-a184-contract-decision-board.png"
OUT_STRESS = BASE / "560-world-map-wmw-right-dossier-a184-proposed-state-stress.png"
OUT_REINSERT = BASE / "561-world-map-wmw-right-dossier-a184-proposed-reinsert.png"
OUT_MANIFEST = BASE / "562-world-map-wmw-right-dossier-a184-capacity-manifest.json"

FONT_BOLD = [
    Path(r"C:\Windows\Fonts\msyhbd.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
]
FONT_REGULAR = [
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\arial.ttf"),
]

BG = (6, 19, 21)
PAPER = (222, 211, 184)
PAPER_DARK = (194, 181, 150)
INK = (29, 31, 27)
MUTED = (73, 76, 65)
CREAM = (239, 230, 198)
CYAN = (35, 99, 109)
RED = (145, 54, 40)
OLIVE = (78, 91, 47)
GOLD = (169, 117, 25)
GREEN = (103, 229, 148)


CURRENT_SCENARIOS = [
    {
        "id": "default",
        "title": "太平洋失航带",
        "stamp": ["可进入", "推荐2"],
        "meta": "卫星阵列 · 普通风险",
        "actions": [
            ["warning", "查看地区风险 · 普通"],
            ["info", "查看任务情报 · 12项"],
            ["enter", "进入选定地区"],
        ],
    },
    {
        "id": "warning",
        "title": "北美禁区警戒带",
        "stamp": ["高危", "推荐12"],
        "meta": "军方封锁 · 红线持续升温",
        "actions": [
            ["warning", "查看风险说明 · 截止4日"],
            ["info", "查看任务情报 · 12项"],
            ["enter", "进入选定地区"],
        ],
    },
    {
        "id": "locked",
        "title": "东亚神秘地带",
        "stamp": ["锁定", "31/55"],
        "meta": "许可不足 · 需档案残页",
        "actions": [
            ["warning", "查看解锁条件 · 声望还差24"],
            ["info_disabled", "任务情报未解锁"],
            ["enter_disabled", "暂不可进入"],
        ],
    },
]


PROPOSED_SCENARIOS = [
    {
        "id": "default",
        "title": "太平洋失航带",
        "stamp": ["可进入", "推荐2"],
        "summary": ["地区特征：卫星阵列与异常航线交叠", "本周异变：普通线报持续汇入"],
        "facts": "限时1 · 线索3 · 深链1 · 任务耗时1-2天",
        "secondary": "查看任务情报 · 4项",
        "primary": "进入选定地区",
        "disabled": False,
    },
    {
        "id": "warning",
        "title": "北美禁区警戒带",
        "stamp": ["高危", "推荐12"],
        "summary": ["地区特征：军事封锁与低频干扰交叠", "本周异变：红线持续升温，窗口缩短"],
        "facts": "限时4 · 线索12 · 深链2 · 任务耗时2-3天",
        "secondary": "查看任务情报 · 12项",
        "primary": "进入选定地区",
        "disabled": False,
    },
    {
        "id": "locked",
        "title": "东亚神秘地带",
        "stamp": ["锁定", "31/55"],
        "summary": ["地区特征：港口回声与失踪航线交叠", "阻断原因：缺少罗斯威尔档案残页"],
        "facts": "声望31/55 · 还差24 · 需档案残页",
        "secondary": "查看解锁条件",
        "primary": "暂不可进入",
        "disabled": True,
    },
]


PROPOSED_SLOTS = {
    "region_body": [22, 288, 276, 54],
    "decision_facts": [22, 346, 276, 32],
    "mission_intel_button": [22, 390, 276, 44],
    "primary_enter_cta": [16, 444, 284, 50],
}

# 559-562 是 v0.8.4 的历史预检证据。合同升版后仍固定使用当时的
# 槽位快照，避免重跑历史脚本时被当前合同语义污染。
LEGACY_CURRENT_SLOTS = {
    "meta_slot": [22, 288, 196, 22],
    "action_stack": [16, 318, 284, 160],
}
LEGACY_LANE_EXPORT_SIZE = [284, 50]
LEGACY_LANE_GAP = 5
LEGACY_CONTRACT_VERSIONS = ["0.8.4", "0.8.4"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


DOSSIER_CONTRACT = load_json(DOSSIER_CONTRACT_PATH)
LANE_CONTRACT = load_json(LANE_CONTRACT_PATH)


def font(paths: list[Path], size: int) -> ImageFont.ImageFont:
    for path in paths:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                pass
    return ImageFont.load_default()


def rect_xyxy(rect: list[int], origin: tuple[int, int], scale: float) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    ox, oy = origin
    return (
        round(ox + x * scale),
        round(oy + y * scale),
        round(ox + (x + w) * scale),
        round(oy + (y + h) * scale),
    )


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    return raster_text_size(text, fnt)


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    paths: list[Path],
    max_size: int,
    min_size: int,
    box: tuple[int, int],
) -> tuple[ImageFont.ImageFont, int, bool, dict[str, Any]]:
    return fit_font_by_raster(text, lambda size: font(paths, size), max_size, min_size, box)


def draw_text_in_rect(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    text: str,
    paths: list[Path],
    max_size: int,
    min_size: int,
    fill: tuple[int, int, int],
    align: str = "left",
    pad_x: int = 7,
) -> dict[str, Any]:
    width = rect[2] - rect[0] - pad_x * 2
    height = rect[3] - rect[1] - 4
    fnt, size, size_fits, fit_metrics = fit_text(draw, text, paths, max_size, min_size, (width, height))
    placement = draw_text_by_raster_bbox(
        draw,
        rect,
        text,
        fnt,
        fill,
        align="center" if align == "center" else "left",
        pad_x=pad_x,
        pad_y=2,
    )
    fits = size_fits and placement["glyph_bbox_inside_inner_rect"]
    return {
        "text": text,
        "font_size": size,
        "fits": fits,
        "text_size": list(fit_metrics["raster_size"]),
        "rect": list(rect),
        "bbox": list(placement["raster_glyph_bbox"]),
        **placement,
    }


def draw_shell(draw: ImageDraw.ImageDraw, origin: tuple[int, int], scale: float, state: str) -> None:
    ox, oy = origin
    width, height = DOSSIER_CONTRACT["frozen"]["export_size"]
    outer = (ox, oy, round(ox + width * scale), round(oy + height * scale))
    shadow = (outer[0] + round(8 * scale), outer[1] + round(10 * scale), outer[2] + round(8 * scale), outer[3] + round(10 * scale))
    draw.rectangle(shadow, fill=(0, 0, 0, 120))
    draw.rectangle(outer, fill=(*PAPER, 255), outline=(*CREAM, 255), width=max(2, round(2 * scale)))
    inset = round(8 * scale)
    draw.rectangle((outer[0] + inset, outer[1] + inset, outer[2] - inset, outer[3] - inset), outline=(*MUTED, 150), width=max(1, round(scale)))

    tab_color = {"default": OLIVE, "warning": RED, "locked": (91, 91, 84)}[state]
    draw.rectangle(
        (outer[2] + round(3 * scale), outer[1] + round(22 * scale), outer[2] + round(16 * scale), outer[3] - round(20 * scale)),
        fill=(*tab_color, 220),
    )

    slots = DOSSIER_CONTRACT["frozen"]["slots"]
    icon = rect_xyxy(slots["header_icon"], origin, scale)
    cx = (icon[0] + icon[2]) // 2
    cy = (icon[1] + icon[3]) // 2
    radius = min(icon[2] - icon[0], icon[3] - icon[1]) // 2
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(*MUTED, 255), width=max(1, round(2 * scale)))
    draw.line((cx - radius, cy, cx + radius, cy), fill=(*MUTED, 230), width=max(1, round(scale)))
    draw.line((cx, cy - radius, cx, cy + radius), fill=(*MUTED, 230), width=max(1, round(scale)))

    photo = rect_xyxy(slots["photo_slot"], origin, scale)
    draw.rectangle(photo, fill=(48, 72, 79), outline=(30, 43, 44), width=max(1, round(2 * scale)))
    px0, py0, px1, py1 = photo
    draw.polygon([(px0, py0), (px0 + (px1 - px0) * 0.35, py0), (px0 + (px1 - px0) * 0.20, py1), (px0, py1)], fill=(61, 91, 99))
    draw.polygon([(px0 + (px1 - px0) * 0.35, py0), (px0 + (px1 - px0) * 0.68, py0), (px0 + (px1 - px0) * 0.58, py1), (px0 + (px1 - px0) * 0.20, py1)], fill=(86, 108, 113))
    draw.polygon([(px0 + (px1 - px0) * 0.68, py0), (px1, py0), (px1, py1), (px0 + (px1 - px0) * 0.58, py1)], fill=(43, 62, 67))
    draw.polygon([(px0 + (px1 - px0) * 0.40, py0 + (py1 - py0) * 0.30), (px0 + (px1 - px0) * 0.62, py0 + (py1 - py0) * 0.47), (px0 + (px1 - px0) * 0.56, py1), (px0 + (px1 - px0) * 0.30, py1)], fill=(28, 37, 39))


def draw_header(
    draw: ImageDraw.ImageDraw,
    origin: tuple[int, int],
    scale: float,
    scenario: dict[str, Any],
    reports: list[dict[str, Any]],
) -> None:
    slots = DOSSIER_CONTRACT["frozen"]["slots"]
    title = rect_xyxy(slots["title_slot"], origin, scale)
    stamp = rect_xyxy(slots["status_stamp"], origin, scale)
    draw.rectangle(title, fill=(*PAPER_DARK, 190))
    stamp_outline = RED if scenario["id"] == "warning" else MUTED
    draw.rectangle(stamp, fill=(*CREAM, 215), outline=(*stamp_outline, 255), width=max(1, round(2 * scale)))

    title_report = draw_text_in_rect(
        draw,
        title,
        scenario["title"],
        FONT_BOLD,
        round(26 * scale),
        round(18 * scale),
        INK,
        pad_x=round(7 * scale),
    )
    title_report["field"] = "title"
    reports.append(title_report)

    stamp_top = (stamp[0] + 2, stamp[1] + round(5 * scale), stamp[2] - 2, stamp[1] + round(29 * scale))
    stamp_bottom = (stamp[0] + 2, stamp[1] + round(30 * scale), stamp[2] - 2, stamp[3] - round(4 * scale))
    top_report = draw_text_in_rect(draw, stamp_top, scenario["stamp"][0], FONT_BOLD, round(17 * scale), round(12 * scale), RED if scenario["id"] == "warning" else INK, align="center", pad_x=2)
    bottom_report = draw_text_in_rect(draw, stamp_bottom, scenario["stamp"][1], FONT_BOLD, round(12 * scale), round(9 * scale), INK, align="center", pad_x=2)
    top_report["field"] = "status_stamp_primary"
    bottom_report["field"] = "status_stamp_secondary"
    reports.extend([top_report, bottom_report])


def action_tone(kind: str) -> tuple[int, int, int]:
    if kind.startswith("warning"):
        return RED
    if kind.startswith("info"):
        return CYAN
    if kind.startswith("enter"):
        return OLIVE
    return MUTED


def draw_action(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    text: str,
    tone: tuple[int, int, int],
    scale: float,
    disabled: bool = False,
) -> dict[str, Any]:
    fill_tone = tuple(round(v * 0.55) for v in tone) if disabled else tone
    draw.rectangle(rect, fill=(*fill_tone, 235), outline=(*CREAM, 235), width=max(1, round(2 * scale)))
    icon_width = round(47 * scale)
    badge_width = round(44 * scale)
    draw.line((rect[0] + icon_width, rect[1], rect[0] + icon_width, rect[3]), fill=(*CREAM, 80), width=max(1, round(scale)))
    draw.line((rect[2] - badge_width, rect[1], rect[2] - badge_width, rect[3]), fill=(*CREAM, 80), width=max(1, round(scale)))
    cy = (rect[1] + rect[3]) // 2
    radius = round(14 * scale)
    draw.ellipse((rect[0] + round(13 * scale), cy - radius, rect[0] + round(13 * scale) + radius * 2, cy + radius), outline=(*CREAM, 220), width=max(1, round(2 * scale)))
    label = (rect[0] + round(58 * scale), rect[1] + round(7 * scale), rect[2] - round(48 * scale), rect[3] - round(7 * scale))
    draw.rectangle(label, fill=(*PAPER, 238), outline=(*CREAM, 130), width=max(1, round(scale)))
    report = draw_text_in_rect(draw, label, text, FONT_BOLD, round(17 * scale), round(12 * scale), INK, align="center", pad_x=round(5 * scale))
    report["field"] = "action"
    return report


def draw_current(
    image: Image.Image,
    origin: tuple[int, int],
    scale: float,
    scenario: dict[str, Any],
    qa: bool = False,
) -> list[dict[str, Any]]:
    draw = ImageDraw.Draw(image, "RGBA")
    reports: list[dict[str, Any]] = []
    draw_shell(draw, origin, scale, scenario["id"])
    draw_header(draw, origin, scale, scenario, reports)
    slots = LEGACY_CURRENT_SLOTS
    meta = rect_xyxy(slots["meta_slot"], origin, scale)
    draw.rectangle(meta, fill=(*PAPER_DARK, 175))
    meta_report = draw_text_in_rect(draw, meta, scenario["meta"], FONT_REGULAR, round(13 * scale), round(10 * scale), INK, pad_x=round(5 * scale))
    meta_report["field"] = "meta"
    reports.append(meta_report)

    stack_x, stack_y, _, _ = slots["action_stack"]
    lane_w, lane_h = LEGACY_LANE_EXPORT_SIZE
    gap = LEGACY_LANE_GAP
    for index, (kind, label) in enumerate(scenario["actions"]):
        local = [stack_x, stack_y + index * (lane_h + gap), lane_w, lane_h]
        lane_rect = rect_xyxy(local, origin, scale)
        report = draw_action(draw, lane_rect, label, action_tone(kind), scale, disabled="disabled" in kind)
        report["field"] = f"action_{index + 1}_{kind}"
        reports.append(report)

    if qa:
        for report in reports:
            draw.rectangle(tuple(report["bbox"]), outline=(255, 70, 190, 230), width=max(1, round(scale)))
    return reports


def draw_proposed(
    image: Image.Image,
    origin: tuple[int, int],
    scale: float,
    scenario: dict[str, Any],
    qa: bool = False,
) -> list[dict[str, Any]]:
    draw = ImageDraw.Draw(image, "RGBA")
    reports: list[dict[str, Any]] = []
    draw_shell(draw, origin, scale, scenario["id"])
    draw_header(draw, origin, scale, scenario, reports)

    summary = rect_xyxy(PROPOSED_SLOTS["region_body"], origin, scale)
    facts = rect_xyxy(PROPOSED_SLOTS["decision_facts"], origin, scale)
    secondary = rect_xyxy(PROPOSED_SLOTS["mission_intel_button"], origin, scale)
    primary = rect_xyxy(PROPOSED_SLOTS["primary_enter_cta"], origin, scale)

    draw.rectangle(summary, fill=(*PAPER, 230))
    draw.line((summary[0], summary[1], summary[2], summary[1]), fill=(*PAPER_DARK, 220), width=max(1, round(scale)))
    line_height = (summary[3] - summary[1]) // 2
    for index, line in enumerate(scenario["summary"]):
        line_rect = (summary[0], summary[1] + index * line_height, summary[2], summary[1] + (index + 1) * line_height)
        report = draw_text_in_rect(draw, line_rect, line, FONT_REGULAR, round(13 * scale), round(11 * scale), INK, pad_x=round(5 * scale))
        report["field"] = f"summary_{index + 1}"
        reports.append(report)

    draw.rectangle(facts, fill=(*PAPER_DARK, 190), outline=(*MUTED, 90), width=max(1, round(scale)))
    fact_report = draw_text_in_rect(draw, facts, scenario["facts"], FONT_BOLD, round(14 * scale), round(11 * scale), MUTED, align="center", pad_x=round(5 * scale))
    fact_report["field"] = "decision_facts"
    reports.append(fact_report)

    secondary_report = draw_action(draw, secondary, scenario["secondary"], CYAN if not scenario["disabled"] else MUTED, scale, disabled=False)
    secondary_report["field"] = "mission_intel_button"
    reports.append(secondary_report)
    primary_report = draw_action(draw, primary, scenario["primary"], GOLD if not scenario["disabled"] else MUTED, scale, disabled=scenario["disabled"])
    primary_report["field"] = "primary_enter_cta"
    reports.append(primary_report)

    if qa:
        slot_colors = {
            "region_body": (105, 220, 255, 230),
            "decision_facts": (255, 215, 80, 230),
            "mission_intel_button": (75, 225, 225, 230),
            "primary_enter_cta": (255, 155, 70, 230),
        }
        for name, slot in PROPOSED_SLOTS.items():
            draw.rectangle(rect_xyxy(slot, origin, scale), outline=slot_colors[name], width=max(2, round(2 * scale)))
        for report in reports:
            draw.rectangle(tuple(report["bbox"]), outline=(255, 70, 190, 230), width=max(1, round(scale)))
    return reports


def draw_heading(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int, color: tuple[int, int, int] = CREAM) -> None:
    draw.text(xy, text, font=font(FONT_BOLD, size), fill=color)


def build_decision_board() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    canvas = Image.new("RGB", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_heading(draw, (42, 28), "WMW 右侧 dossier：A184 容量与合同决策板", 30)
    draw.text((44, 70), "本板只验证信息归属、主次动作与文字容量；不是生产美术，也未修改 frozen 合同。", font=font(FONT_REGULAR, 16), fill=(203, 220, 203))

    draw_heading(draw, (74, 122), "A  现合同最小改法", 22, (255, 188, 145))
    draw.text((74, 151), "外框与所有槽位不动；三条 lane 必须都是真动作。", font=font(FONT_REGULAR, 14), fill=(220, 220, 200))
    current_reports = draw_current(canvas, (70, 190), 1.35, CURRENT_SCENARIOS[1], qa=False)

    x0 = 548
    draw.rectangle((x0, 116, 1318, 1010), fill=(12, 36, 37, 235), outline=(75, 129, 118, 220), width=2)
    draw_heading(draw, (580, 145), "现合同审计", 22)
    audit = [
        ("字符容量", "A184 短 token 可塞入：标题 / meta / 3 行动作均不越框", GREEN),
        ("动作层级", "把进入 CTA 移到最下行后可恢复“读完再进入”的终点", GREEN),
        ("交互语义", "full hit_rect 使三行都必须可点击，不能拿来冒充只读字段", (255, 205, 115)),
        ("地区正文", "只有 196×22 的 meta；无法承载 A75 的地区特征 / 本周异变", (255, 105, 95)),
        ("结论", "能救 A184，救不了 A75；只能作为低成本保底方案", (255, 188, 145)),
    ]
    for index, (label, body, color) in enumerate(audit):
        y = 195 + index * 94
        draw.text((580, y), label, font=font(FONT_BOLD, 16), fill=color)
        draw.text((580, y + 31), body, font=font(FONT_REGULAR, 15), fill=(229, 229, 207))

    draw_heading(draw, (580, 690), "A184 字段唯一归属", 19)
    ownership = [
        "推荐人数 → 顶部 status_stamp",
        "风险短因 / 地区理解 → summary（现合同仅 meta）",
        "可见目标 → “查看任务情报 · N”次级按钮",
        "解锁缺口 → locked 摘要 + “查看解锁条件”",
        "任务耗时预览 → 决策事实条；进入地区本身不扣天数（待确认）",
        "主 CTA → dossier 最底部，唯一最高权重动作",
    ]
    for index, line in enumerate(ownership):
        draw.text((584, 730 + index * 37), line, font=font(FONT_REGULAR, 15), fill=(217, 228, 209))

    draw_heading(draw, (1382, 122), "B  推荐升版结构", 22, GREEN)
    draw.text((1382, 151), "外框 / 标题 / 状态章 / 图片不动，只重构下半部。", font=font(FONT_REGULAR, 14), fill=(220, 220, 200))
    proposed_reports = draw_proposed(canvas, (1380, 190), 1.35, PROPOSED_SCENARIOS[1], qa=False)
    draw.text((1382, 910), "2 行地区摘要 + 决策事实条", font=font(FONT_BOLD, 15), fill=(110, 220, 255))
    draw.text((1382, 945), "次级任务情报 + 底部唯一 CTA", font=font(FONT_BOLD, 15), fill=(255, 198, 94))
    draw.text((1382, 985), "代价：需升合同版本并重跑回填", font=font(FONT_REGULAR, 14), fill=(255, 176, 142))

    canvas.save(OUT_DECISION)
    return current_reports, proposed_reports


def build_stress_board() -> dict[str, list[dict[str, Any]]]:
    canvas = Image.new("RGB", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_heading(draw, (40, 24), "推荐升版结构：default / warning / locked 真实文案压力", 28)
    draw.text((42, 63), "1.5× = 1920×1080 运行时尺度；彩框=提议 carrier，洋红框=glyph bbox。", font=font(FONT_REGULAR, 15), fill=(203, 220, 203))

    x_positions = [70, 650, 1230]
    state_names = {"default": "DEFAULT 可进入", "warning": "WARNING 高危", "locked": "LOCKED 锁定"}
    reports: dict[str, list[dict[str, Any]]] = {}
    for x, scenario in zip(x_positions, PROPOSED_SCENARIOS):
        draw_heading(draw, (x, 105), state_names[scenario["id"]], 19)
        state_reports = draw_proposed(canvas, (x, 145), 1.5, scenario, qa=True)
        reports[scenario["id"]] = state_reports
        passed = sum(1 for item in state_reports if item["fits"])
        minimum = min(item["font_size"] for item in state_reports)
        draw.text((x, 946), f"fit {passed}/{len(state_reports)} · 最小字号 {minimum}px（运行时）", font=font(FONT_BOLD, 15), fill=GREEN if passed == len(state_reports) else (255, 100, 90))
        draw.text((x, 979), "主 CTA 固定在底部；锁定态不提供进入动作。", font=font(FONT_REGULAR, 14), fill=(220, 220, 200))

    draw.text((42, 1041), "注意：本板证明容量和归属，不证明最终纸张质感；生产美术仍需真实 carrier / inner / glyph 三层验收。", font=font(FONT_REGULAR, 14), fill=(255, 194, 145))
    canvas.save(OUT_STRESS)
    return reports


def build_reinsert() -> list[dict[str, Any]]:
    if FULLSCREEN_SOURCE.exists():
        canvas = Image.open(FULLSCREEN_SOURCE).convert("RGB")
    else:
        canvas = Image.new("RGB", (1280, 720), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((918, 18, 1279, 574), fill=(*BG, 248))
    reports = draw_proposed(canvas, tuple(DOSSIER_CONTRACT["frozen"]["positions"][0]), 1.0, PROPOSED_SCENARIOS[1], qa=False)
    draw.rectangle((280, 28, 760, 78), fill=(*BG, 220), outline=(74, 130, 119, 220), width=1)
    draw.text((294, 39), "A184 preflight：推荐升版结构 / warning state", font=font(FONT_BOLD, 16), fill=CREAM)
    canvas.save(OUT_REINSERT)
    return reports


def normalized_metrics(reports: list[dict[str, Any]], scale: float) -> list[dict[str, Any]]:
    normalized = []
    for item in reports:
        copy = dict(item)
        copy["font_size_reference"] = round(item["font_size"] / scale, 2)
        normalized.append(copy)
    return normalized


def write_manifest(
    current_reports: list[dict[str, Any]],
    proposed_reports: list[dict[str, Any]],
    stress_reports: dict[str, list[dict[str, Any]]],
    reinsert_reports: list[dict[str, Any]],
) -> None:
    current_all_fit = all(item["fits"] for item in current_reports)
    proposed_all_fit = all(item["fits"] for state in stress_reports.values() for item in state)
    data = {
        "artifact": "WMW right dossier A184 capacity and information architecture preflight",
        "date": "2026-07-13",
        "artifact_type": "component_contract_preflight / text_capacity_stress / structure_review / not production art / not atlas",
        "status": "evidence_ready_pending_user_contract_decision",
        "source_contracts": {
            "right_dossier_page": str(DOSSIER_CONTRACT_PATH.relative_to(ROOT)).replace("\\", "/"),
            "right_action_lane": str(LANE_CONTRACT_PATH.relative_to(ROOT)).replace("\\", "/"),
            "versions": LEGACY_CONTRACT_VERSIONS,
            "geometry_source": "embedded v0.8.4 pre-decision snapshot",
        },
        "contract_mutation": {
            "performed": False,
            "frozen_fields_modified": [],
        },
        "outputs": {
            "decision_board": str(OUT_DECISION.relative_to(ROOT)).replace("\\", "/"),
            "state_stress": str(OUT_STRESS.relative_to(ROOT)).replace("\\", "/"),
            "full_screen_reinsert": str(OUT_REINSERT.relative_to(ROOT)).replace("\\", "/"),
            "manifest": str(OUT_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        },
        "option_a_existing_frozen_contract": {
            "description": "Keep all frozen geometry. Reorder the three instantiated lanes to context/risk, task intel, and bottom primary CTA; every full-hit-rect lane remains a real action.",
            "a184_short_token_capacity": "partial_only" if current_all_fit else "fail",
            "a75_region_understanding_body": "fail_no_carrier",
            "primary_cta_bottom": "pass_in_semantic_proposal",
            "read_only_content_disguised_as_button": "pass_none",
            "reports_warning_state_scale_1_35": normalized_metrics(current_reports, 1.35),
        },
        "option_b_recommended_contract_revision": {
            "description": "Keep 320x520 shell, header, stamp, and photo geometry; replace the lower meta/action stack with a two-line region summary, a compact decision strip, one secondary task/condition action, and one bottom primary CTA.",
            "proposed_slots_reference": PROPOSED_SLOTS,
            "touches_frozen": ["right_dossier_page.frozen.slots.meta_slot", "right_dossier_page.frozen.slots.action_stack", "right_action_lane.frozen.positions/role semantics"],
            "a184_information_ownership": "pass",
            "a75_region_understanding_body": "pass",
            "a80_secondary_task_intel_and_bottom_primary_cta": "pass",
            "all_state_text_capacity": "pass" if proposed_all_fit else "fail",
            "reports_decision_board_warning_scale_1_35": normalized_metrics(proposed_reports, 1.35),
            "reports_state_stress_scale_1_5": {
                key: normalized_metrics(value, 1.5) for key, value in stress_reports.items()
            },
            "reports_full_screen_warning_scale_1_0": normalized_metrics(reinsert_reports, 1.0),
        },
        "field_ownership": {
            "recommendation": "status_stamp secondary line",
            "risk_reason_and_region_understanding": "region_body",
            "visible_target_count": "mission_intel_button count, explicitly measured in 项",
            "unlock_gap": "locked region_body + decision_facts + mission_intel_button becomes unlock-condition action",
            "entry_cost": "pending_user_clarification: current exploration rule says entering a region costs no days; the board uses region-task duration preview in decision_facts instead",
            "primary_cta": "primary_enter_cta bottom row",
        },
        "semantic_conflict": "A184 says entry cost belongs to the dossier, while the adopted exploration flow says entering a region costs no days and only dispatch execution consumes days. The board does not attach a day cost to the enter CTA; it labels the fact as region-task duration preview pending user clarification.",
        "decision": "Recommend option B because option A only partially rescues A184 short-token capacity and still violates the adopted A75 region-understanding requirement. Option B and the entry-cost terminology both require explicit user approval before any contract version bump or production art.",
        "next_gate": "User chooses option A or B. Only after that decision may the relevant contracts be versioned and a no-text clean-sprite brief be authored.",
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    current_reports, proposed_reports = build_decision_board()
    stress_reports = build_stress_board()
    reinsert_reports = build_reinsert()
    write_manifest(current_reports, proposed_reports, stress_reports, reinsert_reports)
    for path in [OUT_DECISION, OUT_STRESS, OUT_REINSERT, OUT_MANIFEST]:
        print(path)


if __name__ == "__main__":
    main()
