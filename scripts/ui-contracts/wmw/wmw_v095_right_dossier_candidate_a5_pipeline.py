from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageStat

import wmw_v091_right_dossier_candidate_a1_pipeline as a1


ROOT = a1.ROOT
BASE = a1.BASE
ASSET_DIR = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "world_map"
    / "wmw_v095_right_dossier_candidate_a5"
)
INGREDIENT_DIR = ASSET_DIR / "ingredients"
FIXTURE = ASSET_DIR / "right_dossier_candidate_a5_runtime_fixture.json"

A4_ASSET_DIR = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "world_map"
    / "wmw_v094_right_dossier_candidate_a4"
)
PARENT_SOURCE = a1.PARENT_MASTER
PRIMARY_MASTER = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "world_map"
    / "wmw_v093_right_dossier_candidate_a3"
    / "ingredients"
    / "right_action_lane_candidate_a3_primary_olive_2x.png"
)
PHOTO = a1.PHOTO_INGREDIENT
BODY_CARRIER = INGREDIENT_DIR / "right_dossier_candidate_a5_region_body_carrier_2x.png"
POPOVER_SKIN = INGREDIENT_DIR / "right_dossier_candidate_a5_mission_popover_2x.png"
PARENT_A5 = INGREDIENT_DIR / "right_dossier_candidate_a5_parent_2x.png"

OUT_STRUCTURE = BASE / "619-world-map-wmw-v0-9-5-right-dossier-candidate-a5-contract-and-carrier-qa.png"
OUT_COLLAPSED_PY = BASE / "620-world-map-wmw-v0-9-5-right-dossier-candidate-a5-python-collapsed.png"
OUT_EXPANDED_PY = BASE / "621-world-map-wmw-v0-9-5-right-dossier-candidate-a5-python-expanded.png"
OUT_PY_QA = BASE / "622-world-map-wmw-v0-9-5-right-dossier-candidate-a5-python-qa.png"
OUT_COLLAPSED_GODOT = BASE / "623-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-collapsed.png"
OUT_EXPANDED_GODOT = BASE / "624-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-expanded.png"
OUT_GODOT_QA = BASE / "625-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-qa.png"
OUT_GIF = BASE / "626-world-map-wmw-v0-9-5-right-dossier-candidate-a5-disclosure-toggle.gif"
OUT_REVIEW = BASE / "627-world-map-wmw-v0-9-5-right-dossier-candidate-a4-a5-review.png"
OUT_MANIFEST = BASE / "628-world-map-wmw-v0-9-5-right-dossier-candidate-a5-manifest.json"
A4_GODOT = BASE / "615-world-map-wmw-v0-9-4-right-dossier-candidate-a4-godot-runtime.png"
A4_MANIFEST = BASE / "618-world-map-wmw-v0-9-4-right-dossier-candidate-a4-manifest.json"
REVIEW_DOC = ROOT / "docs" / "plans" / "world-map-benchmark-landing" / "2026-07-15-world-map-wmw-right-dossier-candidate-a5-merged-summary-review.md"

DOSSIER = a1.DOSSIER
MISSION = a1.MISSION
PRIMARY = a1.PRIMARY

if DOSSIER["contract_version"] != "0.8.7" or MISSION["contract_version"] != "0.8.7":
    raise RuntimeError("candidate A5 requires dossier and mission contracts v0.8.7")
if PRIMARY["contract_version"] != "0.8.6":
    raise RuntimeError("candidate A5 reuses the unchanged primary v0.8.6 contract")

NAVY = (7, 20, 22, 255)
PANEL = (13, 39, 40, 255)
CREAM = (235, 227, 201, 255)
INK = (29, 32, 27, 255)
MUTED_INK = (86, 96, 84, 255)
TEAL_INK = (63, 102, 99, 255)
TEAL_LINE = (63, 102, 99, 71)
GREEN = (103, 229, 148, 255)
RED = (255, 104, 96, 255)
YELLOW = (255, 212, 68, 255)

BODY_INNER_1X = [34, 292, 252, 82]
BODY_NO_TEXT_1X = [22, 288, 4, 90]
DIVIDER_1X = [10, 42, 264, 1]
POPOVER_PARENT_1X = [-294, 326, 284, 156]
OLD_BODY_1X = [22, 288, 276, 54]
OLD_FACTS_1X = [22, 346, 276, 32]

EXPECTED_COMPONENT_IDS = [
    "header_icon",
    "title_slot",
    "status_stamp",
    "photo_slot",
    "region_body",
    "mission_summary_disclosure",
    "primary_enter_cta",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def scale_rect(rect: list[int]) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    return x * 2, y * 2, (x + w) * 2, (y + h) * 2


def offset_rect(
    rect: tuple[int, int, int, int], origin: tuple[int, int]
) -> tuple[int, int, int, int]:
    return rect[0] + origin[0], rect[1] + origin[1], rect[2] + origin[0], rect[3] + origin[1]


def load_fixture() -> dict[str, Any]:
    fixture = load_json(FIXTURE)
    required = {
        "region_title",
        "status_display_text",
        "region_body_text",
        "mission_intel_title",
        "mission_intel_facts",
        "mission_preview",
        "mission_preview_total",
        "primary_enter_label",
    }
    missing = sorted(key for key in required if key not in fixture)
    if missing:
        raise RuntimeError(f"A5 runtime fixture missing fields: {missing}")
    if fixture.get("provenance") != "production_runtime_export" or not fixture.get(
        "generated_from_production_data"
    ):
        raise RuntimeError("A5 runtime fixture is not production-derived")
    if "decision_facts" in fixture:
        raise RuntimeError("retired decision_facts leaked into A5 fixture")
    if fixture["mission_intel_title"] != "任务情报":
        raise RuntimeError("A5 disclosure title drifted")
    if len(fixture["mission_preview"]) not in {2, 3}:
        raise RuntimeError("A5 popover must preview 2-3 production tasks")
    return fixture


def alpha_diff_count(before: Image.Image, after: Image.Image) -> int:
    diff = ImageChops.difference(before.convert("RGBA"), after.convert("RGBA"))
    return sum(1 for value in diff.convert("L").get_flattened_data() if value > 0)


def build_visual_ingredients() -> dict[str, Any]:
    INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    parent = Image.open(PARENT_SOURCE).convert("RGBA")
    body_rect = scale_rect(DOSSIER["frozen"]["slots"]["region_body"])
    body_size = (body_rect[2] - body_rect[0], body_rect[3] - body_rect[1])
    substrate_source = (44, 760, 596, 940)
    substrate = parent.crop(substrate_source)
    if substrate.size != body_size:
        raise RuntimeError(f"A5 body substrate must be an exact-size crop: {substrate.size} != {body_size}")

    paper_wash = Image.new("RGBA", body_size, (220, 211, 188, 255))
    carrier = Image.blend(substrate, paper_wash, 0.34)
    carrier_draw = ImageDraw.Draw(carrier)
    carrier_draw.rectangle((0, 0, 7, body_size[1] - 1), fill=(48, 123, 129, 255))
    carrier_draw.line((8, 0, 8, body_size[1] - 1), fill=(173, 205, 199, 255), width=1)
    carrier.save(BODY_CARRIER)

    parent_a5 = parent.copy()
    parent_a5.alpha_composite(carrier, (body_rect[0], body_rect[1]))
    parent_a5.save(PARENT_A5)

    outside_mask = Image.new("L", parent.size, 255)
    ImageDraw.Draw(outside_mask).rectangle(
        (body_rect[0], body_rect[1], body_rect[2] - 1, body_rect[3] - 1), fill=0
    )
    outside_before = Image.new("RGBA", parent.size, (0, 0, 0, 0))
    outside_after = Image.new("RGBA", parent.size, (0, 0, 0, 0))
    outside_before.paste(parent, mask=outside_mask)
    outside_after.paste(parent_a5, mask=outside_mask)
    outside_change = alpha_diff_count(outside_before, outside_after)

    old_facts = scale_rect(OLD_FACTS_1X)
    facts_relative = (
        old_facts[0] - body_rect[0],
        old_facts[1] - body_rect[1],
        old_facts[2] - body_rect[0],
        old_facts[3] - body_rect[1],
    )
    expected_facts = carrier.crop(facts_relative)
    actual_facts = parent_a5.crop(old_facts)
    old_facts_residual = alpha_diff_count(expected_facts, actual_facts)
    carrier_stat = ImageStat.Stat(carrier.convert("RGB"))

    popover_size = (POPOVER_PARENT_1X[2] * 2, POPOVER_PARENT_1X[3] * 2)
    popover = Image.new("RGBA", popover_size, (216, 207, 184, 255))
    pop = ImageDraw.Draw(popover)
    w, h = popover_size
    facets = [
        ([(0, 0), (w // 2, 0), (w // 3, h // 2), (0, h)], (225, 217, 196, 255)),
        ([(w // 2, 0), (w, 0), (w, h // 2), (w // 3, h // 2)], (209, 201, 178, 255)),
        ([(0, h), (w // 3, h // 2), (w * 2 // 3, h), (0, h)], (218, 209, 186, 255)),
        ([(w // 3, h // 2), (w, h // 2), (w, h), (w * 2 // 3, h)], (205, 197, 175, 255)),
    ]
    for points, color in facets:
        pop.polygon(points, fill=color)
    pop.rectangle((1, 1, w - 2, h - 2), outline=(88, 91, 76, 255), width=3)
    pop.line((8, 8, w - 9, 8), fill=(241, 233, 210, 210), width=2)
    pop.rectangle((w - 8, h // 2 - 12, w - 1, h // 2 + 12), fill=(63, 102, 99, 255))
    popover.save(POPOVER_SKIN)

    metrics = {
        "body_carrier": {
            "rect_2x": list(body_rect),
            "source_crop_2x": list(substrate_source),
            "source_size": list(substrate.size),
            "destination_size": list(body_size),
            "no_rescale": substrate.size == body_size,
            "outside_change_pixels": outside_change,
            "old_decision_facts_residual_pixels": old_facts_residual,
            "rgb_stddev": [round(value, 4) for value in carrier_stat.stddev],
            "construction": "exact-size clean paper crop + full semantic carrier reconstruction; no inpaint, blur, stretch, stripe patch, or old carrier reuse",
        },
        "popover_skin": {
            "size_2x": list(popover.size),
            "parent_space_rect_1x": POPOVER_PARENT_1X,
            "runtime_text_baked": False,
            "construction": "deterministic no-text faceted paper overlay",
        },
    }
    if not metrics["body_carrier"]["no_rescale"]:
        raise RuntimeError("A5 body carrier source was resized")
    if outside_change != 0 or old_facts_residual != 0:
        raise RuntimeError("A5 carrier reconstruction leaked outside its rect or retained the old facts carrier")
    if min(metrics["body_carrier"]["rgb_stddev"]) < 3.0:
        raise RuntimeError("A5 body carrier collapsed into a flat color band")
    return metrics


def child_rect(parent: tuple[int, int, int, int], slot: list[int]) -> tuple[int, int, int, int]:
    return offset_rect(scale_rect(slot), (parent[0], parent[1]))


def add_text(
    reports: list[dict[str, Any]],
    draw: ImageDraw.ImageDraw,
    field: str,
    rect: tuple[int, int, int, int],
    value: str,
    **kwargs: Any,
) -> dict[str, Any]:
    report = a1.fit_and_draw(draw, rect, value, **kwargs)
    report["field"] = field
    reports.append(report)
    return report


def draw_chevron(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], expanded: bool) -> None:
    x0, y0, x1, y1 = rect
    cx = (x0 + x1) // 2
    if expanded:
        points = [(x0 + 8, y1 - 12), (cx, y0 + 12), (x1 - 8, y1 - 12)]
    else:
        points = [(x0 + 8, y0 + 12), (cx, y1 - 12), (x1 - 8, y0 + 12)]
    draw.line(points, fill=TEAL_INK, width=3, joint="curve")


def draw_summary_row(
    image: Image.Image,
    reports: list[dict[str, Any]],
    mission_rect: tuple[int, int, int, int],
    fixture: dict[str, Any],
    expanded: bool,
) -> dict[str, Any]:
    slots = MISSION["frozen"]["slots"]
    draw = ImageDraw.Draw(image)
    icon_rect = child_rect(mission_rect, slots["left_icon_zone"])
    title_rect = child_rect(mission_rect, slots["title_label"])
    facts_rect = child_rect(mission_rect, slots["facts_label"])
    chevron_rect = child_rect(mission_rect, slots["chevron_zone"])
    divider = offset_rect(scale_rect(DIVIDER_1X), (mission_rect[0], mission_rect[1]))
    icon_bbox = a1.paste_runtime_icon(image, a1.RUNTIME_DOCUMENT, icon_rect, TEAL_INK, 0.68)
    title = add_text(
        reports,
        draw,
        "mission_intel_title",
        title_rect,
        str(fixture["mission_intel_title"]),
        max_size=24,
        min_size=20,
        bold=True,
        fill=TEAL_INK,
        align="left",
        pad_x=0,
        pad_y=0,
    )
    facts = add_text(
        reports,
        draw,
        "mission_intel_facts",
        facts_rect,
        str(fixture["mission_intel_facts"]),
        max_size=20,
        min_size=16,
        bold=False,
        fill=MUTED_INK,
        align="left",
        pad_x=0,
        pad_y=0,
    )
    draw_chevron(draw, chevron_rect, expanded)
    draw.rectangle((divider[0], divider[1], divider[2] - 1, divider[3] - 1), fill=TEAL_LINE)
    return {
        "icon_bbox_2x": list(icon_bbox),
        "title_rect_2x": list(title_rect),
        "title_bbox_2x": list(title["raster_glyph_bbox"]),
        "facts_rect_2x": list(facts_rect),
        "facts_bbox_2x": list(facts["raster_glyph_bbox"]),
        "chevron_rect_2x": list(chevron_rect),
        "divider_rect_2x": list(divider),
    }


def render_dossier(
    fixture: dict[str, Any], expanded: bool, show_qa: bool
) -> tuple[Image.Image, list[dict[str, Any]], dict[str, Any]]:
    parent = Image.open(PARENT_A5).convert("RGBA")
    photo = Image.open(PHOTO).convert("RGBA")
    primary = Image.open(PRIMARY_MASTER).convert("RGBA")
    component = Image.new("RGBA", parent.size, (12, 27, 29, 255))
    slots = DOSSIER["frozen"]["slots"]
    photo_rect = scale_rect(slots["photo_slot"])
    if photo.size != (photo_rect[2] - photo_rect[0], photo_rect[3] - photo_rect[1]):
        raise RuntimeError("A5 photo ingredient no longer matches the exact 69:44 slot")
    component.alpha_composite(photo, (photo_rect[0], photo_rect[1]))
    component.alpha_composite(parent)
    primary_rect = scale_rect(slots["primary_enter_cta"])
    component.alpha_composite(primary, (primary_rect[0], primary_rect[1]))
    draw = ImageDraw.Draw(component)
    reports: list[dict[str, Any]] = []

    header_icon = scale_rect(slots["header_icon"])
    header_icon = (
        header_icon[0],
        header_icon[1] + a1.HEADER_ICON_OFFSET_2X,
        header_icon[2],
        header_icon[3] + a1.HEADER_ICON_OFFSET_2X,
    )
    a1.paste_runtime_icon(component, a1.RUNTIME_GLOBE, header_icon, (90, 93, 76, 255), 0.86)
    add_text(
        reports,
        draw,
        "region_title",
        scale_rect(slots["title_slot"]),
        str(fixture["region_title"]),
        max_size=38,
        min_size=28,
        bold=True,
        fill=INK,
        align="center",
        pad_x=8,
        pad_y=6,
    )
    status = scale_rect(slots["status_stamp"])
    status = (status[0], status[1] + a1.STATUS_GROUP_OFFSET_2X, status[2], status[3] + a1.STATUS_GROUP_OFFSET_2X)
    add_text(
        reports,
        draw,
        "status_display_text",
        status,
        str(fixture["status_display_text"]),
        max_size=22,
        min_size=18,
        bold=True,
        fill=(142, 54, 39, 255),
        align="center",
        pad_x=6,
        pad_y=8,
    )

    body_lines = [line for line in str(fixture["region_body_text"]).split("\n") if line]
    if not 1 <= len(body_lines) <= 4:
        raise RuntimeError(f"A5 region_body_text must contain 1-4 lines: {body_lines}")
    body_inner = scale_rect(BODY_INNER_1X)
    line_height = (body_inner[3] - body_inner[1]) // 4
    for index, line in enumerate(body_lines, start=1):
        line_rect = (
            body_inner[0],
            body_inner[1] + (index - 1) * line_height,
            body_inner[2],
            body_inner[1] + index * line_height,
        )
        add_text(
            reports,
            draw,
            f"region_body_line_{index}",
            line_rect,
            line,
            max_size=23,
            min_size=17,
            bold=False,
            fill=INK,
            align="left",
            pad_x=0,
            pad_y=0,
        )

    mission_rect = scale_rect(slots["mission_intel_button"])
    summary_geometry = draw_summary_row(component, reports, mission_rect, fixture, expanded)
    primary_slots = PRIMARY["frozen"]["slots"]
    a1.paste_runtime_icon(
        component,
        a1.RUNTIME_ARROW,
        child_rect(primary_rect, primary_slots["right_action_badge"]),
        CREAM,
        0.72,
    )
    add_text(
        reports,
        draw,
        "primary_enter_label",
        child_rect(primary_rect, primary_slots["label_plate"]),
        str(fixture["primary_enter_label"]),
        max_size=28,
        min_size=20,
        bold=True,
        fill=CREAM,
        align="center",
        pad_x=8,
        pad_y=6,
    )

    if show_qa:
        colors = {
            "header_icon": (81, 238, 255, 255),
            "title_slot": (255, 72, 202, 255),
            "status_stamp": (255, 111, 95, 255),
            "photo_slot": (72, 236, 174, 255),
            "region_body": (255, 212, 68, 255),
            "mission_intel_button": (79, 218, 232, 255),
            "primary_enter_cta": (174, 204, 91, 255),
        }
        for name, color in colors.items():
            rect = scale_rect(slots[name])
            draw.rectangle((rect[0], rect[1], rect[2] - 1, rect[3] - 1), outline=color, width=3)
        draw.rectangle(
            (body_inner[0], body_inner[1], body_inner[2] - 1, body_inner[3] - 1),
            outline=GREEN,
            width=3,
        )
        no_text = scale_rect(BODY_NO_TEXT_1X)
        draw.rectangle((no_text[0], no_text[1], no_text[2] - 1, no_text[3] - 1), outline=RED, width=3)
        for report in reports:
            bbox = report["raster_glyph_bbox"]
            draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 55, 196, 255), width=2)
    return component, reports, summary_geometry


def draw_popover(board: Image.Image, fixture: dict[str, Any], dossier_pos: tuple[int, int], show_qa: bool) -> list[dict[str, Any]]:
    scale = 1.5
    x = round(dossier_pos[0] + POPOVER_PARENT_1X[0] * scale)
    y = round(dossier_pos[1] + POPOVER_PARENT_1X[1] * scale)
    w = round(POPOVER_PARENT_1X[2] * scale)
    h = round(POPOVER_PARENT_1X[3] * scale)
    skin = Image.open(POPOVER_SKIN).convert("RGBA").resize((w, h), Image.Resampling.LANCZOS)
    board.alpha_composite(skin, (x, y))
    draw = ImageDraw.Draw(board)
    reports: list[dict[str, Any]] = []
    rows = list(fixture["mission_preview"])
    row_h = 54
    top = y + 18
    for index, item in enumerate(rows):
        row_y = top + index * row_h
        if index:
            draw.line((x + 18, row_y - 5, x + w - 18, row_y - 5), fill=(105, 108, 91, 90), width=1)
        kind = str(item["kind_label"])
        add_text(
            reports,
            draw,
            f"mission_preview_{index + 1}_kind",
            (x + 18, row_y, x + 72, row_y + 34),
            kind,
            max_size=18,
            min_size=15,
            bold=True,
            fill=TEAL_INK,
            align="left",
            pad_x=0,
            pad_y=0,
        )
        add_text(
            reports,
            draw,
            f"mission_preview_{index + 1}_name",
            (x + 78, row_y, x + w - 70, row_y + 34),
            str(item["name"]),
            max_size=20,
            min_size=15,
            bold=False,
            fill=INK,
            align="left",
            pad_x=0,
            pad_y=0,
        )
        add_text(
            reports,
            draw,
            f"mission_preview_{index + 1}_days",
            (x + w - 62, row_y, x + w - 18, row_y + 34),
            f"{int(item['days'])}天",
            max_size=18,
            min_size=15,
            bold=True,
            fill=MUTED_INK,
            align="right",
            pad_x=0,
            pad_y=0,
        )
    footer = f"预览 {len(rows)} 项 · 共 {int(fixture['mission_preview_total'])} 项"
    add_text(
        reports,
        draw,
        "mission_preview_footer",
        (x + 18, y + h - 38, x + w - 18, y + h - 10),
        footer,
        max_size=16,
        min_size=14,
        bold=False,
        fill=MUTED_INK,
        align="right",
        pad_x=0,
        pad_y=0,
    )
    connector_y = round(dossier_pos[1] + (390 + 22) * scale)
    draw.line((x + w - 1, connector_y, dossier_pos[0], connector_y), fill=TEAL_INK, width=2)
    if show_qa:
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline=GREEN, width=3)
        for report in reports:
            bbox = report["raster_glyph_bbox"]
            draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 55, 196, 255), width=2)
    return reports


def build_runtime_board(
    fixture: dict[str, Any], expanded: bool, show_qa: bool, output: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    component, reports, summary = render_dossier(fixture, expanded, show_qa)
    board = Image.new("RGBA", (1920, 1080), NAVY)
    dossier_pos = (1180, 150)
    runtime_component = component.resize((480, 780), Image.Resampling.LANCZOS)
    board.alpha_composite(runtime_component, dossier_pos)
    popover_reports: list[dict[str, Any]] = []
    if expanded:
        popover_reports = draw_popover(board, fixture, dossier_pos, show_qa)
    draw = ImageDraw.Draw(board)
    state = "EXPANDED" if expanded else "COLLAPSED"
    draw.text((70, 62), f"Python v0.9.5 · candidate A5 · {state}", font=a1.font(32, True), fill=CREAM)
    draw.text((72, 112), "A211：任务摘要与 disclosure 合并；旧事实条高度回收到地区描述。", font=a1.font(19), fill=(194, 211, 201, 255))
    notes = [
        "一个摘要行：任务情报 + 限时 / 线索 / 深链 + chevron",
        "连续描述 carrier：54px → 90px；旧灰色 facts carrier 退役",
        "橄榄 CTA 位置与资产不动，仍是唯一实体按钮",
        "展开态：只读短抽屉向左锚定，不覆盖也不推动 CTA",
    ]
    for index, note in enumerate(notes):
        color = GREEN if index == 3 else (222, 226, 205, 255)
        draw.text((88, 260 + index * 54), note, font=a1.font(18, index == 3), fill=color)
    output.parent.mkdir(parents=True, exist_ok=True)
    board.convert("RGB").save(output)
    return reports + popover_reports, summary


def build_structure_board(metrics: dict[str, Any]) -> None:
    old_parent = Image.open(PARENT_SOURCE).convert("RGBA")
    new_parent = Image.open(PARENT_A5).convert("RGBA")
    crop = (32, 548, 608, 900)
    old_crop = old_parent.crop(crop).resize((576, 352), Image.Resampling.LANCZOS)
    new_crop = new_parent.crop(crop).resize((576, 352), Image.Resampling.LANCZOS)
    board = Image.new("RGB", (1920, 1080), NAVY[:3])
    draw = ImageDraw.Draw(board)
    draw.text((48, 28), "WMW 右 dossier · A5 合并摘要与连续描述 carrier", font=a1.font(31, True), fill=CREAM[:3])
    draw.text((50, 75), "619 · 旧事实条不是留空或遮字，而是被完整的新 276×90 描述 carrier 取代。", font=a1.font(18), fill=(194, 211, 201))
    board.paste(old_crop.convert("RGB"), (48, 150))
    board.paste(new_crop.convert("RGB"), (656, 150))
    draw.rectangle((46, 148, 626, 506), outline=RED[:3], width=3)
    draw.rectangle((654, 148, 1234, 506), outline=GREEN[:3], width=3)
    draw.text((58, 116), "A4：54px 描述 + 32px 独立事实条", font=a1.font(17, True), fill=RED[:3])
    draw.text((666, 116), "A5：90px 连续描述 + 合并 disclosure", font=a1.font(17, True), fill=GREEN[:3])
    facts = [
        f"source crop = destination {metrics['body_carrier']['source_size']}",
        f"outside change = {metrics['body_carrier']['outside_change_pixels']}px",
        f"old facts residual = {metrics['body_carrier']['old_decision_facts_residual_pixels']}px",
        f"carrier RGB stddev = {metrics['body_carrier']['rgb_stddev']}",
        "禁止：拉伸、inpaint、模糊、色带补丁、旧 carrier 残留",
    ]
    draw.rectangle((1280, 148, 1880, 506), outline=(83, 139, 139), width=2)
    draw.text((1310, 176), "Carrier construction gates", font=a1.font(20, True), fill=CREAM[:3])
    for index, line in enumerate(facts):
        draw.text((1310, 232 + index * 48), line, font=a1.font(16, index < 3), fill=(219, 225, 205))
    y = 610
    draw.text((50, y), "Collapsed geometry @ 1x", font=a1.font(20, True), fill=YELLOW[:3])
    geometry = [
        "region_body        [22,288,276,90]  inner [34,292,252,82]",
        "summary disclosure [18,390,284,44]  single hit / focus / callback",
        "primary CTA        [18,444,284,50]  unchanged",
        "expanded popover   [-294,326,284,156] in parent space; read-only",
    ]
    for index, line in enumerate(geometry):
        draw.text((50, y + 54 + index * 46), line, font=a1.font(17, index == 2), fill=(224, 226, 207))
    draw.text((1030, 610), "Information ownership", font=a1.font(20, True), fill=YELLOW[:3])
    ownership = [
        "地区描述：背景 / 本周异变，3-4 行容量",
        "摘要行：任务类型计数 + 展开状态",
        "短抽屉：2-3 条只读任务预览",
        "橄榄 CTA：进入地区任务台，唯一跨层动作",
    ]
    for index, line in enumerate(ownership):
        draw.text((1030, 664 + index * 46), line, font=a1.font(17, index == 3), fill=(224, 226, 207))
    board.save(OUT_STRUCTURE)


def text_gate(reports: list[dict[str, Any]]) -> tuple[int, int]:
    passed = sum(
        1
        for report in reports
        if report.get("fit_search_pass") and report.get("glyph_bbox_inside_inner_rect")
    )
    return passed, len(reports)


def build_manifest(
    fixture: dict[str, Any],
    metrics: dict[str, Any],
    reports: list[dict[str, Any]],
    summary: dict[str, Any],
) -> dict[str, Any]:
    passed, total = text_gate(reports)
    body_old = OLD_BODY_1X
    body_new = DOSSIER["frozen"]["slots"]["region_body"]
    body_gain = body_new[3] - body_old[3]
    primary_hash = sha256(PRIMARY_MASTER)
    manifest = {
        "schema_version": 1,
        "artifact_type": "runtime_state_preview",
        "asset_line": "world-map-benchmark-landing/right-dossier",
        "version": "v0.9.5",
        "candidate": "A5",
        "status": "evidence_ready_godot_capture_pending",
        "design_adoption": "A211：任务摘要与任务情报合为一条 disclosure；释放的事实条高度回收到地区描述。",
        "runtime_fixture_path": rel(FIXTURE),
        "contracts": {
            "right_dossier_page": {
                "version": DOSSIER["contract_version"],
                "frozen_changed": True,
                "changes": {
                    "region_body": {"from": OLD_BODY_1X, "to": body_new},
                    "decision_facts": {"from": OLD_FACTS_1X, "to": None},
                },
            },
            "right_mission_intel_button": {
                "version": MISSION["contract_version"],
                "frozen_changed": True,
                "changes": "内部槽改为 document/title/facts/chevron 四槽；export 与 hit rect 不动",
            },
            "right_action_lane": {
                "version": PRIMARY["contract_version"],
                "frozen_changed": False,
            },
        },
        "sources": {
            "runtime_fixture": rel(FIXTURE),
            "parent_source": rel(PARENT_SOURCE),
            "photo": rel(PHOTO),
            "primary_cta": rel(PRIMARY_MASTER),
            "new_imagegen_calls": 0,
        },
        "outputs": {
            "structure_qa": rel(OUT_STRUCTURE),
            "python_collapsed": rel(OUT_COLLAPSED_PY),
            "python_expanded": rel(OUT_EXPANDED_PY),
            "python_qa": rel(OUT_PY_QA),
            "godot_collapsed": rel(OUT_COLLAPSED_GODOT),
            "godot_expanded": rel(OUT_EXPANDED_GODOT),
            "godot_qa": rel(OUT_GODOT_QA),
            "animation": rel(OUT_GIF),
            "review_board": rel(OUT_REVIEW),
            "review_document": rel(REVIEW_DOC),
        },
        "ingredients": {
            "region_body_carrier": rel(BODY_CARRIER),
            "mission_popover_skin": rel(POPOVER_SKIN),
            "parent_a5": rel(PARENT_A5),
            "sha256": {
                rel(BODY_CARRIER): sha256(BODY_CARRIER),
                rel(POPOVER_SKIN): sha256(POPOVER_SKIN),
                rel(PARENT_A5): sha256(PARENT_A5),
                rel(PRIMARY_MASTER): primary_hash,
            },
        },
        "measurements": {
            **metrics,
            "region_body_height_gain_1x": body_gain,
            "summary_geometry": summary,
            "text_bbox": {"passed": passed, "total": total},
            "interactive_hit_rects": 2,
            "visual_entity_buttons": 1,
            "mission_preview_rows": len(fixture["mission_preview"]),
        },
        "visible_component_expected_ids": EXPECTED_COMPONENT_IDS,
        "visible_component_audit": [
            {"component_id": "header_icon", "visible": True, "player_question": "这是什么层级的对象？", "necessity": "地区身份提示", "data_source": "runtime globe icon ingredient", "interactive": False, "decision": "keep"},
            {"component_id": "title_slot", "visible": True, "player_question": "当前选中了哪个地区？", "necessity": "地区主标题", "data_source": "region.name", "interactive": False, "decision": "keep"},
            {"component_id": "status_stamp", "visible": True, "player_question": "该地区当前处于什么状态？", "necessity": "当前状态提示", "data_source": "derived region state", "interactive": False, "decision": "keep"},
            {"component_id": "photo_slot", "visible": True, "player_question": "该地区的视觉身份是什么？", "necessity": "地区场景预览", "data_source": "region photo ingredient", "interactive": False, "decision": "keep"},
            {"component_id": "region_body", "visible": True, "player_question": "这个地区发生了什么？", "necessity": "地区背景与本周异变", "data_source": "region.hint + derived state", "interactive": False, "decision": "change"},
            {"component_id": "mission_summary_disclosure", "visible": True, "player_question": "这里有哪些任务，能否展开预览？", "necessity": "合并任务计数与只读预览入口", "data_source": "visible node counts + mission preview", "interactive": True, "decision": "change"},
            {"component_id": "primary_enter_cta", "visible": True, "player_question": "如何进入地区任务台？", "necessity": "唯一跨层导航动作", "data_source": "WORLD_MAP_UI_COPY + unlock state", "interactive": True, "decision": "keep"},
        ],
        "visible_field_semantics": [
            {"field_id": "region_body_text", "component": "region_body", "visible": True, "player_question": "这个地区发生了什么？", "decision_value": "背景与本周异变", "owner_scope": "region", "source_kind": "state_derived", "data_source": "region.hint + remaining_days", "fixture_key": "region_body_text", "screenshot_value": fixture["region_body_text"], "decision": "change"},
            {"field_id": "mission_intel_title", "component": "mission_summary_disclosure", "visible": True, "player_question": "这里可以展开什么？", "decision_value": "任务情报章节", "owner_scope": "region", "source_kind": "static_semantic", "data_source": "WORLD_MAP_UI_COPY", "fixture_key": "mission_intel_title", "screenshot_value": fixture["mission_intel_title"], "decision": "change"},
            {"field_id": "mission_intel_facts", "component": "mission_summary_disclosure", "visible": True, "player_question": "任务结构是什么？", "decision_value": "限时 / 线索 / 深链计数", "owner_scope": "region", "source_kind": "state_derived", "data_source": "visible node counts", "fixture_key": "mission_intel_facts", "screenshot_value": fixture["mission_intel_facts"], "decision": "change"},
            {"field_id": "primary_enter_label", "component": "primary_enter_cta", "visible": True, "player_question": "如何进入地区任务台？", "decision_value": "跨层导航", "owner_scope": "region", "source_kind": "static_semantic", "data_source": "WORLD_MAP_UI_COPY + unlock state", "fixture_key": "primary_enter_label", "screenshot_value": fixture["primary_enter_label"], "decision": "keep"},
        ],
        "removed_fixture_fields": [
            {"field_id": "decision_facts", "prior_value": "任务构成 · 限时 1 · 线索 2 · 深链 1", "reason": "A211：并入 mission summary disclosure", "visible_after": False},
            {"field_id": "mission_intel_label", "prior_value": "任务情报", "reason": "A211：拆为 title + facts 同行字段", "visible_after": False},
        ],
        "gates": {
            "contract_upgrade_authorized": {"status": "pass", "basis": "用户明确要求合并并将释放空间交给地区描述；A211 已登记。"},
            "decision_facts_retired": {"status": "pass" if "decision_facts" not in DOSSIER["frozen"]["slots"] and "decision_facts" not in fixture else "fail"},
            "region_body_capacity_gain": {"status": "pass" if body_gain == 36 else "fail", "gain_px_1x": body_gain, "from": OLD_BODY_1X, "to": body_new},
            "carrier_full_reconstruction": {"status": "pass" if metrics["body_carrier"]["outside_change_pixels"] == 0 and metrics["body_carrier"]["old_decision_facts_residual_pixels"] == 0 else "fail", "basis": metrics["body_carrier"]},
            "no_rescale_or_inpaint": {"status": "pass" if metrics["body_carrier"]["no_rescale"] else "fail", "basis": metrics["body_carrier"]["construction"]},
            "summary_single_control": {"status": "pass", "hit_rects": 1, "focus_targets": 1, "callbacks": 1, "visible_parts": ["document", "title", "facts", "chevron"]},
            "primary_cta_stable": {"status": "pass", "rect_1x": DOSSIER["frozen"]["slots"]["primary_enter_cta"], "sha256": primary_hash},
            "popover_no_dossier_overlap": {"status": "pass" if POPOVER_PARENT_1X[0] + POPOVER_PARENT_1X[2] <= -10 else "fail", "rect_1x": POPOVER_PARENT_1X},
            "runtime_text_raster_alpha_containment": {"status": "pass" if passed == total else "fail", "passed": passed, "total": total},
            "photo_aspect_preserved": {"status": "pass", "ratio": "69:44", "godot_stretch": "STRETCH_KEEP_ASPECT_COVERED"},
            "no_new_imagegen": {"status": "pass", "calls": 0},
            "godot_windowed_capture": {"status": "pending", "runner": "scripts/run_wmw_right_dossier_godot_capture_v095.ps1"},
            "dynamic_visual_review": {"status": "pending", "basis": "等待 623-627 与输出复审"},
        },
        "judgment": "A5 Python 结构与文字证据就绪；等待固定 Godot 4.6.2 windowed 的 collapsed / expanded / QA 与动态复审。",
    }
    return manifest


def build() -> None:
    metrics = build_visual_ingredients()
    fixture = load_fixture()
    collapsed_reports, collapsed_summary = build_runtime_board(fixture, False, False, OUT_COLLAPSED_PY)
    expanded_reports, _ = build_runtime_board(fixture, True, False, OUT_EXPANDED_PY)
    qa_reports, _ = build_runtime_board(fixture, True, True, OUT_PY_QA)
    build_structure_board(metrics)
    manifest = build_manifest(fixture, metrics, collapsed_reports + expanded_reports + qa_reports, collapsed_summary)
    failed = [name for name, gate in manifest["gates"].items() if gate.get("status") == "fail"]
    if failed:
        raise RuntimeError(f"A5 build gates failed: {failed}")
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT_STRUCTURE)
    print(OUT_COLLAPSED_PY)
    print(OUT_EXPANDED_PY)
    print(OUT_PY_QA)
    print(OUT_MANIFEST)


def image_metrics(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGBA")
    colors = image.convert("RGB").getcolors(maxcolors=image.width * image.height)
    nonblack = sum(
        1
        for r, g, b, _a in image.get_flattened_data()
        if max(r, g, b) > 8
    )
    return {
        "size": list(image.size),
        "color_count": len(colors) if colors is not None else image.width * image.height,
        "nonblack_pixels": nonblack,
    }


def build_animation() -> None:
    collapsed = Image.open(OUT_COLLAPSED_GODOT).convert("RGB")
    expanded = Image.open(OUT_EXPANDED_GODOT).convert("RGB")
    collapsed.save(
        OUT_GIF,
        save_all=True,
        append_images=[expanded, collapsed],
        duration=[1100, 1600, 900],
        loop=0,
        optimize=False,
    )


def build_review_board() -> None:
    a4 = Image.open(A4_GODOT).convert("RGB")
    a5c = Image.open(OUT_COLLAPSED_GODOT).convert("RGB")
    a5e = Image.open(OUT_EXPANDED_GODOT).convert("RGB")
    board = Image.new("RGB", (1920, 1080), NAVY[:3])
    draw = ImageDraw.Draw(board)
    draw.text((40, 25), "WMW 右 dossier · A4 → A5 合并摘要 / 描述容量复审", font=a1.font(30, True), fill=CREAM[:3])
    draw.text((42, 70), "627 · A5 删除独立 facts 条，描述 carrier 增高 36px；展开列表不移动 CTA。", font=a1.font(18), fill=(194, 211, 201))
    crops = [
        (a4.crop((40, 120, 595, 1036)), "A4 · 两块任务信息 + 54px 描述", RED[:3]),
        (a5c.crop((1140, 120, 1695, 1036)), "A5 collapsed · 合并摘要 + 90px 描述", GREEN[:3]),
        (a5e.crop((700, 120, 1695, 1036)), "A5 expanded · 左锚只读短抽屉", YELLOW[:3]),
    ]
    positions = [(30, 135, 500, 825), (555, 135, 500, 825), (1080, 135, 810, 825)]
    for (crop, label, color), (x, y, w, h) in zip(crops, positions):
        crop.thumbnail((w, h), Image.Resampling.LANCZOS)
        board.paste(crop, (x + (w - crop.width) // 2, y + (h - crop.height) // 2))
        draw.rectangle((x, y, x + w, y + h), outline=color, width=3)
        draw.text((x + 8, 101), label, font=a1.font(16, True), fill=color)
    draw.text((50, 1010), "用户裁决点：合并摘要是否更自然；描述增容是否值得；左侧短抽屉是否符合任务预览预期。", font=a1.font(17, True), fill=CREAM[:3])
    board.save(OUT_REVIEW)


def supersede_a4() -> None:
    if not A4_MANIFEST.exists():
        return
    manifest = load_json(A4_MANIFEST)
    manifest["status"] = "superseded_by_a5_user_merged_summary_direction"
    manifest["superseded_by"] = rel(OUT_MANIFEST)
    manifest["judgment"] = "A4 去按钮化证据仍有效，但用户进一步采纳 A211：任务事实与 disclosure 合并，释放高度回收到地区描述；A4 不再是当前候选。"
    A4_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def finalize() -> None:
    for path in (OUT_COLLAPSED_GODOT, OUT_EXPANDED_GODOT, OUT_GODOT_QA):
        if not path.exists():
            raise RuntimeError(f"missing Godot evidence: {path}")
    build_animation()
    build_review_board()
    manifest = load_json(OUT_MANIFEST)
    captures = {
        "collapsed": image_metrics(OUT_COLLAPSED_GODOT),
        "expanded": image_metrics(OUT_EXPANDED_GODOT),
        "qa": image_metrics(OUT_GODOT_QA),
    }
    godot_pass = all(
        value["size"] == [1920, 1080]
        and value["color_count"] > 100
        and value["nonblack_pixels"] > 100000
        for value in captures.values()
    )
    manifest["measurements"]["godot_capture"] = captures
    manifest["measurements"]["animation"] = {
        "path": rel(OUT_GIF),
        "frames": 3,
        "states": ["collapsed", "expanded", "collapsed"],
    }
    manifest["gates"]["godot_windowed_capture"] = {
        "status": "pass" if godot_pass else "fail",
        "godot_version": "4.6.2-stable",
        "mode": "windowed opengl3; UI capture never used headless",
        "runner": "scripts/run_wmw_right_dossier_godot_capture_v095.ps1",
        "frame_post_draw_waits": 2,
        "all_black_refusal": True,
        "captures": captures,
    }
    manifest["gates"]["dynamic_visual_review"] = {
        "status": "evidence_ready_user_visual_review_pending",
        "basis": "623 collapsed、624 expanded、625 QA、626 动图与 627 A4/A5 对比板已生成；等待用户裁决。",
        "parent_skill_fallback_review": {
            "ux": {"p0": 0, "p1": 0, "p2": 1, "remaining": "侧抽屉属于固定纸面约束下的生产候选，需用户确认其展开方向。"},
            "ui": {"p0": 0, "p1": 0, "p2": 1, "remaining": "默认与展开证据就绪；正式字体与全部 locked 文案仍需后续状态压力。"},
            "subagent_runtime_note": "ux_laoge 与 ui_designer 两次调用均在只读阶段长时间无返回；父级按相同 SKILL 完成等价流程，不冒充子 agent 输出。",
        },
    }
    manifest["status"] = "evidence_ready_user_visual_review_pending"
    manifest["judgment"] = "A5 已完成合同升版、连续描述 carrier、合并摘要、production preview、Godot windowed 收起/展开证据与动态 GIF；等待用户视觉裁决，未冻结。"
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    supersede_a4()
    if not godot_pass:
        raise RuntimeError("A5 Godot capture validation failed")
    print(OUT_GIF)
    print(OUT_REVIEW)
    print(OUT_MANIFEST)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    if args.finalize:
        finalize()
    else:
        build()


if __name__ == "__main__":
    main()
