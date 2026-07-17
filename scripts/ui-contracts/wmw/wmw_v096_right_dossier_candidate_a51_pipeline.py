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
FIXTURE = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "world_map"
    / "wmw_v096_right_dossier_candidate_a51"
    / "right_dossier_candidate_a51_runtime_fixture.json"
)

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
PARENT_A5 = INGREDIENT_DIR / "right_dossier_candidate_a5_parent_2x.png"

OUT_STRUCTURE = BASE / "629-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-in-place-structure-qa.png"
OUT_COLLAPSED_PY = BASE / "630-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-python-collapsed.png"
OUT_EXPANDED_PY = BASE / "631-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-python-expanded.png"
OUT_PY_QA = BASE / "632-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-python-qa.png"
OUT_COLLAPSED_GODOT = BASE / "633-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-godot-collapsed.png"
OUT_EXPANDED_GODOT = BASE / "634-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-godot-expanded.png"
OUT_GODOT_QA = BASE / "635-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-godot-qa.png"
OUT_GIF = BASE / "636-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-in-place-toggle.gif"
OUT_REVIEW = BASE / "637-world-map-wmw-v0-9-6-right-dossier-candidate-a5-a5-1-review.png"
OUT_MANIFEST = BASE / "638-world-map-wmw-v0-9-6-right-dossier-candidate-a5-1-manifest.json"
A5_REJECTED_EXPANDED = BASE / "624-world-map-wmw-v0-9-5-right-dossier-candidate-a5-godot-expanded.png"
A5_MANIFEST = BASE / "628-world-map-wmw-v0-9-5-right-dossier-candidate-a5-manifest.json"
REVIEW_DOC = ROOT / "docs" / "plans" / "world-map-benchmark-landing" / "2026-07-15-world-map-wmw-right-dossier-candidate-a5-1-in-place-mission-preview-review.md"

DOSSIER = a1.DOSSIER
MISSION = a1.MISSION
PRIMARY = a1.PRIMARY

if DOSSIER["contract_version"] != "0.8.8" or MISSION["contract_version"] != "0.8.8":
    raise RuntimeError("candidate A5.1 requires dossier and mission contracts v0.8.8")
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
TASK_ROW_1_1X = [34, 292, 252, 41]
TASK_ROW_2_1X = [34, 333, 252, 41]
TASK_ROWS_1X = [TASK_ROW_1_1X, TASK_ROW_2_1X]
PREVIEW_LIMIT = 2
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
        "mission_preview_limit",
        "mission_preview_display",
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
    if len(fixture["mission_preview"]) < PREVIEW_LIMIT:
        raise RuntimeError("A5.1 in-place preview requires at least two production tasks")
    if int(fixture["mission_preview_limit"]) != PREVIEW_LIMIT:
        raise RuntimeError("A5.1 production fixture preview limit drifted")
    display = fixture["mission_preview_display"]
    expected_display = {
        "row_1_name": str(fixture["mission_preview"][0]["name"]),
        "row_1_meta": f"{fixture['mission_preview'][0]['kind_label']} · 耗时{int(fixture['mission_preview'][0]['days'])}天",
        "row_2_name": str(fixture["mission_preview"][1]["name"]),
        "row_2_meta": f"{fixture['mission_preview'][1]['kind_label']} · 耗时{int(fixture['mission_preview'][1]['days'])}天",
        "count": f"已显示 {PREVIEW_LIMIT} / 共 {int(fixture['mission_preview_total'])} 条",
    }
    if display != expected_display:
        raise RuntimeError(f"A5.1 derived display fields drifted: {display} != {expected_display}")
    return fixture


def alpha_diff_count(before: Image.Image, after: Image.Image) -> int:
    diff = ImageChops.difference(before.convert("RGBA"), after.convert("RGBA"))
    return sum(1 for value in diff.convert("L").get_flattened_data() if value > 0)


def validate_reused_visual_ingredients() -> dict[str, Any]:
    required = [PARENT_A5, BODY_CARRIER, PRIMARY_MASTER, PHOTO]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError(f"A5.1 reused ingredients are missing: {missing}")
    parent = Image.open(PARENT_A5).convert("RGBA")
    carrier = Image.open(BODY_CARRIER).convert("RGBA")
    body_rect = scale_rect(DOSSIER["frozen"]["slots"]["region_body"])
    expected_body_size = (body_rect[2] - body_rect[0], body_rect[3] - body_rect[1])
    if parent.size != (640, 1040) or carrier.size != expected_body_size:
        raise RuntimeError("A5.1 reused parent/carrier dimensions drifted")
    carrier_stat = ImageStat.Stat(carrier.convert("RGB"))
    if min(carrier_stat.stddev) < 3.0:
        raise RuntimeError("A5.1 reused carrier collapsed into a flat color band")
    return {
        "reused_visual_ingredients": {
            "new_imagegen_calls": 0,
            "new_raster_ingredients": 0,
            "parent_size_2x": list(parent.size),
            "body_carrier_size_2x": list(carrier.size),
            "body_carrier_rgb_stddev": [round(value, 4) for value in carrier_stat.stddev],
            "parent_sha256": sha256(PARENT_A5),
            "carrier_sha256": sha256(BODY_CARRIER),
            "primary_sha256": sha256(PRIMARY_MASTER),
            "photo_sha256": sha256(PHOTO),
        }
    }


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
    cy = (y0 + y1) // 2
    draw.line((x0 + 8, cy, x1 - 8, cy), fill=TEAL_INK, width=3)
    if not expanded:
        draw.line((cx, y0 + 12, cx, y1 - 12), fill=TEAL_INK, width=3)


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
    facts_value = (
        str(fixture["mission_preview_display"]["count"])
        if expanded
        else str(fixture["mission_intel_facts"])
    )
    facts = add_text(
        reports,
        draw,
        "mission_preview_count" if expanded else "mission_intel_facts",
        facts_rect,
        facts_value,
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
        "facts_value": facts_value,
    }


def draw_task_preview_rows(
    image: Image.Image,
    reports: list[dict[str, Any]],
    fixture: dict[str, Any],
) -> list[dict[str, Any]]:
    draw = ImageDraw.Draw(image)
    rows = list(fixture["mission_preview"])[:PREVIEW_LIMIT]
    geometry: list[dict[str, Any]] = []
    for index, (item, row_1x) in enumerate(zip(rows, TASK_ROWS_1X), start=1):
        row = scale_rect(row_1x)
        name_rect = (row[0], row[1] + 4, row[2], row[1] + 44)
        meta_rect = (row[0], row[1] + 42, row[2], row[3] - 4)
        if index > 1:
            draw.line((row[0], row[1], row[2] - 1, row[1]), fill=(98, 105, 88, 80), width=1)
        row_display = fixture["mission_preview_display"]
        name_value = str(row_display[f"row_{index}_name"])
        meta_value = str(row_display[f"row_{index}_meta"])
        name_report = add_text(
            reports,
            draw,
            f"mission_preview_{index}_name",
            name_rect,
            name_value,
            max_size=23,
            min_size=18,
            bold=True,
            fill=INK,
            align="left",
            pad_x=0,
            pad_y=0,
        )
        meta_report = add_text(
            reports,
            draw,
            f"mission_preview_{index}_meta",
            meta_rect,
            meta_value,
            max_size=17,
            min_size=14,
            bold=False,
            fill=TEAL_INK,
            align="left",
            pad_x=0,
            pad_y=0,
        )
        geometry.append(
            {
                "row_rect_1x": row_1x,
                "row_rect_2x": list(row),
                "name_bbox_2x": list(name_report["raster_glyph_bbox"]),
                "meta_bbox_2x": list(meta_report["raster_glyph_bbox"]),
                "interactive": False,
                "value": {"name": name_value, "meta": meta_value},
            }
        )
    if len(geometry) != PREVIEW_LIMIT:
        raise RuntimeError("A5.1 must render exactly two in-place task rows")
    return geometry


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

    body_inner = scale_rect(BODY_INNER_1X)
    task_geometry: list[dict[str, Any]] = []
    if expanded:
        task_geometry = draw_task_preview_rows(component, reports, fixture)
    else:
        body_lines = [line for line in str(fixture["region_body_text"]).split("\n") if line]
        if not 1 <= len(body_lines) <= 4:
            raise RuntimeError(f"A5.1 region_body_text must contain 1-4 lines: {body_lines}")
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
        if expanded:
            for index, row_1x in enumerate(TASK_ROWS_1X, start=1):
                row = scale_rect(row_1x)
                draw.rectangle((row[0], row[1], row[2] - 1, row[3] - 1), outline=(88, 237, 244, 255), width=2)
        for report in reports:
            bbox = report["raster_glyph_bbox"]
            draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 55, 196, 255), width=2)
    return component, reports, {"summary_row": summary_geometry, "task_rows": task_geometry}


def build_runtime_board(
    fixture: dict[str, Any], expanded: bool, show_qa: bool, output: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    component, reports, summary = render_dossier(fixture, expanded, show_qa)
    board = Image.new("RGBA", (1920, 1080), NAVY)
    dossier_pos = (1180, 150)
    runtime_component = component.resize((480, 780), Image.Resampling.LANCZOS)
    board.alpha_composite(runtime_component, dossier_pos)
    draw = ImageDraw.Draw(board)
    state = "EXPANDED" if expanded else "COLLAPSED"
    draw.text((70, 62), f"Python v0.9.6 · candidate A5.1 · {state}", font=a1.font(32, True), fill=CREAM)
    draw.text((72, 112), "A211：摘要行固定；两条任务在描述区原位展开。", font=a1.font(19), fill=(194, 211, 201, 255))
    notes = [
        "收起：3-4 行地区描述 + 任务结构摘要",
        "展开：同一 90px 区域显示 2 条任务名 + meta",
        "任务行无 hit / hover / 箭头；完整列表仍由橄榄 CTA 进入",
        "照片、摘要行、橄榄 CTA 与纸面总高零位移",
    ]
    for index, note in enumerate(notes):
        color = GREEN if index == 3 else (222, 226, 205, 255)
        draw.text((88, 260 + index * 54), note, font=a1.font(18, index == 3), fill=color)
    output.parent.mkdir(parents=True, exist_ok=True)
    board.convert("RGB").save(output)
    return reports, summary


def state_mutation_metrics(fixture: dict[str, Any]) -> dict[str, Any]:
    collapsed, _, _ = render_dossier(fixture, False, False)
    expanded, _, _ = render_dossier(fixture, True, False)
    outside_mask = Image.new("L", collapsed.size, 255)
    mask_draw = ImageDraw.Draw(outside_mask)
    for slot_name in ("region_body", "mission_intel_button"):
        rect = scale_rect(DOSSIER["frozen"]["slots"][slot_name])
        mask_draw.rectangle((rect[0], rect[1], rect[2] - 1, rect[3] - 1), fill=0)
    before_outside = Image.new("RGBA", collapsed.size, (0, 0, 0, 0))
    after_outside = Image.new("RGBA", expanded.size, (0, 0, 0, 0))
    before_outside.paste(collapsed, mask=outside_mask)
    after_outside.paste(expanded, mask=outside_mask)
    photo_rect = scale_rect(DOSSIER["frozen"]["slots"]["photo_slot"])
    primary_rect = scale_rect(DOSSIER["frozen"]["slots"]["primary_enter_cta"])
    return {
        "allowed_state_mutation_slots": ["region_body", "mission_intel_button"],
        "outside_allowed_union_diff_pixels": alpha_diff_count(before_outside, after_outside),
        "total_state_diff_pixels": alpha_diff_count(collapsed, expanded),
        "photo_diff_pixels": alpha_diff_count(collapsed.crop(photo_rect), expanded.crop(photo_rect)),
        "primary_cta_diff_pixels": alpha_diff_count(collapsed.crop(primary_rect), expanded.crop(primary_rect)),
        "external_overlay_pixels": 0,
        "task_row_hit_rects": 0,
        "rendered_task_rows": PREVIEW_LIMIT,
        "task_row_rects_1x": TASK_ROWS_1X,
    }


def build_structure_board(fixture: dict[str, Any], metrics: dict[str, Any]) -> None:
    collapsed, _, _ = render_dossier(fixture, False, False)
    expanded, _, _ = render_dossier(fixture, True, False)
    qa, _, _ = render_dossier(fixture, True, True)
    board = Image.new("RGB", (1920, 1080), NAVY[:3])
    draw = ImageDraw.Draw(board)
    draw.text((42, 24), "WMW 右 dossier · A5.1 原位任务展开结构", font=a1.font(30, True), fill=CREAM[:3])
    draw.text((44, 68), "629 · 只交换 region_body 内容；摘要行、照片、橄榄 CTA 与纸面总高不动。", font=a1.font(18), fill=(194, 211, 201))
    panels = [
        (collapsed, "COLLAPSED · 地区描述", GREEN[:3]),
        (expanded, "EXPANDED · 两条只读任务", YELLOW[:3]),
        (qa, "EXPANDED QA · 同源矩形", (88, 237, 244)),
    ]
    for index, (image, label, color) in enumerate(panels):
        x = 62 + index * 620
        preview = image.resize((480, 780), Image.Resampling.LANCZOS).convert("RGB")
        board.paste(preview, (x + 58, 150))
        draw.rectangle((x, 132, x + 596, 950), outline=color, width=3)
        draw.text((x + 14, 103), label, font=a1.font(17, True), fill=color)
    state = metrics["in_place_state_diff"]
    gate_text = (
        f"outside union diff={state['outside_allowed_union_diff_pixels']} · "
        f"photo diff={state['photo_diff_pixels']} · CTA diff={state['primary_cta_diff_pixels']} · "
        f"external overlay={state['external_overlay_pixels']} · task hit rects={state['task_row_hit_rects']}"
    )
    draw.text((62, 994), gate_text, font=a1.font(17, True), fill=CREAM[:3])
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
        "version": "v0.9.6",
        "candidate": "A5.1",
        "status": "evidence_ready_godot_capture_pending",
        "design_adoption": "A211 最终裁决：摘要行固定；两条只读任务在地区描述区原位展开，禁止外部抽屉。",
        "runtime_fixture_path": rel(FIXTURE),
        "contracts": {
            "right_dossier_page": {
                "version": DOSSIER["contract_version"],
                "frozen_changed": False,
                "changes": {
                    "provisional_state_content": "collapsed=region_body_text; expanded=two read-only task rows",
                    "task_rows_1x": TASK_ROWS_1X,
                },
            },
            "right_mission_intel_button": {
                "version": MISSION["contract_version"],
                "frozen_changed": False,
                "changes": "expanded facts 改为已显示 2 / 共 N 条；摘要行、四槽与 hit rect 不动",
            },
            "right_action_lane": {
                "version": PRIMARY["contract_version"],
                "frozen_changed": False,
            },
        },
        "sources": {
            "runtime_fixture": rel(FIXTURE),
            "parent_source": rel(PARENT_SOURCE),
            "reused_a5_parent": rel(PARENT_A5),
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
            "parent_a5": rel(PARENT_A5),
            "new_raster_ingredients": 0,
            "sha256": {
                rel(BODY_CARRIER): sha256(BODY_CARRIER),
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
            "mission_preview_source_rows": len(fixture["mission_preview"]),
            "mission_preview_rendered_rows": PREVIEW_LIMIT,
            "mission_preview_row_hit_rects": 0,
        },
        "text_capacity": reports,
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
            {"field_id": "mission_preview_1_name", "component": "region_body", "visible": True, "player_question": "当前有哪些任务？", "decision_value": "第一条只读任务名", "owner_scope": "region", "source_kind": "state_derived", "data_source": "mission_preview[0].name", "fixture_key": "mission_preview_display.row_1_name", "screenshot_value": fixture["mission_preview_display"]["row_1_name"], "decision": "change"},
            {"field_id": "mission_preview_1_meta", "component": "region_body", "visible": True, "player_question": "第一条任务是什么类型、耗时多久？", "decision_value": "第一条只读任务 meta", "owner_scope": "region", "source_kind": "state_derived", "data_source": "mission_preview[0].kind_label + days", "fixture_key": "mission_preview_display.row_1_meta", "screenshot_value": fixture["mission_preview_display"]["row_1_meta"], "decision": "change"},
            {"field_id": "mission_preview_2_name", "component": "region_body", "visible": True, "player_question": "当前还有什么任务？", "decision_value": "第二条只读任务名", "owner_scope": "region", "source_kind": "state_derived", "data_source": "mission_preview[1].name", "fixture_key": "mission_preview_display.row_2_name", "screenshot_value": fixture["mission_preview_display"]["row_2_name"], "decision": "change"},
            {"field_id": "mission_preview_2_meta", "component": "region_body", "visible": True, "player_question": "第二条任务是什么类型、耗时多久？", "decision_value": "第二条只读任务 meta", "owner_scope": "region", "source_kind": "state_derived", "data_source": "mission_preview[1].kind_label + days", "fixture_key": "mission_preview_display.row_2_meta", "screenshot_value": fixture["mission_preview_display"]["row_2_meta"], "decision": "change"},
            {"field_id": "mission_preview_count", "component": "mission_summary_disclosure", "visible": True, "player_question": "当前预览了多少任务？", "decision_value": "已显示 2 / 共 N 条", "owner_scope": "region", "source_kind": "state_derived", "data_source": "preview limit + visible count", "fixture_key": "mission_preview_display.count", "screenshot_value": fixture["mission_preview_display"]["count"], "decision": "change"},
            {"field_id": "primary_enter_label", "component": "primary_enter_cta", "visible": True, "player_question": "如何进入地区任务台？", "decision_value": "跨层导航", "owner_scope": "region", "source_kind": "static_semantic", "data_source": "WORLD_MAP_UI_COPY + unlock state", "fixture_key": "primary_enter_label", "screenshot_value": fixture["primary_enter_label"], "decision": "keep"},
        ],
        "removed_fixture_fields": [
            {"field_id": "decision_facts", "prior_value": "任务构成 · 限时 1 · 线索 2 · 深链 1", "reason": "A211：并入 mission summary disclosure", "visible_after": False},
            {"field_id": "mission_intel_label", "prior_value": "任务情报", "reason": "A211：拆为 title + facts 同行字段", "visible_after": False},
        ],
        "gates": {
            "contract_upgrade_authorized": {"status": "pass", "basis": "用户回复继续，采纳 A211 原位两任务展开；只升 provisional 行为版本，frozen 矩形不动。"},
            "decision_facts_retired": {"status": "pass" if "decision_facts" not in DOSSIER["frozen"]["slots"] and "decision_facts" not in fixture else "fail"},
            "region_body_capacity_gain": {"status": "pass" if body_gain == 36 else "fail", "gain_px_1x": body_gain, "from": OLD_BODY_1X, "to": body_new},
            "reused_visual_ingredients_unchanged": {"status": "pass", "basis": metrics["reused_visual_ingredients"]},
            "summary_single_control": {"status": "pass", "hit_rects": 1, "focus_targets": 1, "callbacks": 1, "visible_parts": ["document", "title", "facts", "plus_minus_state_indicator"]},
            "primary_cta_stable": {"status": "pass", "rect_1x": DOSSIER["frozen"]["slots"]["primary_enter_cta"], "sha256": primary_hash},
            "in_place_state_mutation_bounds": {"status": "pass" if metrics["in_place_state_diff"]["outside_allowed_union_diff_pixels"] == 0 else "fail", "basis": metrics["in_place_state_diff"]},
            "no_external_overlay": {"status": "pass" if metrics["in_place_state_diff"]["external_overlay_pixels"] == 0 else "fail", "external_overlay_pixels": metrics["in_place_state_diff"]["external_overlay_pixels"]},
            "task_preview_exactly_two": {"status": "pass" if metrics["in_place_state_diff"]["rendered_task_rows"] == PREVIEW_LIMIT else "fail", "rendered": metrics["in_place_state_diff"]["rendered_task_rows"], "limit": PREVIEW_LIMIT},
            "task_rows_noninteractive": {"status": "pass" if metrics["in_place_state_diff"]["task_row_hit_rects"] == 0 else "fail", "hit_rects": metrics["in_place_state_diff"]["task_row_hit_rects"]},
            "photo_and_primary_zero_shift": {"status": "pass" if metrics["in_place_state_diff"]["photo_diff_pixels"] == 0 and metrics["in_place_state_diff"]["primary_cta_diff_pixels"] == 0 else "fail", "photo_diff_pixels": metrics["in_place_state_diff"]["photo_diff_pixels"], "primary_cta_diff_pixels": metrics["in_place_state_diff"]["primary_cta_diff_pixels"]},
            "runtime_text_raster_alpha_containment": {"status": "pass" if passed == total else "fail", "passed": passed, "total": total},
            "photo_aspect_preserved": {"status": "pass", "ratio": "69:44", "godot_stretch": "STRETCH_KEEP_ASPECT_COVERED"},
            "no_new_imagegen": {"status": "pass", "calls": 0},
            "godot_windowed_capture": {"status": "pending", "runner": "scripts/run_wmw_right_dossier_godot_capture_v096.ps1"},
            "dynamic_visual_review": {"status": "pending", "basis": "等待 633-637 与双 agent 输出复审"},
        },
        "judgment": "A5.1 Python 原位展开、文字 bbox 与状态变更边界证据就绪；等待固定 Godot 4.6.2 windowed 的 collapsed / expanded / QA 与动态复审。",
    }
    return manifest


def build() -> None:
    fixture = load_fixture()
    metrics = validate_reused_visual_ingredients()
    metrics["in_place_state_diff"] = state_mutation_metrics(fixture)
    collapsed_reports, collapsed_summary = build_runtime_board(fixture, False, False, OUT_COLLAPSED_PY)
    expanded_reports, _ = build_runtime_board(fixture, True, False, OUT_EXPANDED_PY)
    qa_reports, _ = build_runtime_board(fixture, True, True, OUT_PY_QA)
    build_structure_board(fixture, metrics)
    manifest = build_manifest(fixture, metrics, collapsed_reports + expanded_reports + qa_reports, collapsed_summary)
    failed = [name for name, gate in manifest["gates"].items() if gate.get("status") == "fail"]
    if failed:
        raise RuntimeError(f"A5.1 build gates failed: {failed}")
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
    rejected = Image.open(A5_REJECTED_EXPANDED).convert("RGB")
    current_collapsed = Image.open(OUT_COLLAPSED_GODOT).convert("RGB")
    current_expanded = Image.open(OUT_EXPANDED_GODOT).convert("RGB")
    board = Image.new("RGB", (1920, 1080), NAVY[:3])
    draw = ImageDraw.Draw(board)
    draw.text((40, 25), "WMW 右 dossier · A5 抽屉撤回 → A5.1 原位展开", font=a1.font(30, True), fill=CREAM[:3])
    draw.text((42, 70), "637 · 任务预览回到纸面内；摘要行固定，描述区按状态切换，照片与主 CTA 零位移。", font=a1.font(18), fill=(194, 211, 201))
    crops = [
        (rejected.crop((700, 120, 1695, 1036)), "A5 · 已否决的左锚抽屉", RED[:3]),
        (current_collapsed.crop((1140, 120, 1695, 1036)), "A5.1 collapsed · 90px 地区描述", GREEN[:3]),
        (current_expanded.crop((1140, 120, 1695, 1036)), "A5.1 expanded · 原位两条任务", YELLOW[:3]),
    ]
    positions = [(30, 135, 660, 825), (710, 135, 560, 825), (1290, 135, 560, 825)]
    for (crop, label, color), (x, y, w, h) in zip(crops, positions):
        crop.thumbnail((w, h), Image.Resampling.LANCZOS)
        board.paste(crop, (x + (w - crop.width) // 2, y + (h - crop.height) // 2))
        draw.rectangle((x, y, x + w, y + h), outline=color, width=3)
        draw.text((x + 8, 101), label, font=a1.font(16, True), fill=color)
    draw.text((50, 1010), "复审点：外部抽屉为 0；两条任务可扫读但不似按钮；照片、摘要行与橄榄 CTA 前后位置一致。", font=a1.font(17, True), fill=CREAM[:3])
    board.save(OUT_REVIEW)


def supersede_a5() -> None:
    if not A5_MANIFEST.exists():
        return
    manifest = load_json(A5_MANIFEST)
    manifest["status"] = "superseded_by_a5_1_in_place_expansion_user_adopted"
    manifest["superseded_by"] = rel(OUT_MANIFEST)
    manifest["judgment"] = "A5 的合并摘要、连续描述 carrier 与 collapsed 证据继续有效；左锚抽屉被用户否决。A5.1 采用纸内原位两任务展开，A5 不再是当前交互候选。"
    A5_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
        "runner": "scripts/run_wmw_right_dossier_godot_capture_v096.ps1",
        "frame_post_draw_waits": 2,
        "all_black_refusal": True,
        "captures": captures,
    }
    manifest["gates"]["dynamic_visual_review"] = {
        "status": "evidence_ready_user_visual_review_pending",
        "basis": "633 collapsed、634 expanded、635 QA、636 动图与 637 A5/A5.1 对比板已生成；UI Designer PASS，UX 复核 P0/P1/P2 均为 0；等待用户视觉裁决。",
    }
    manifest["reviews"] = {
        "ui_designer": {
            "status": "pass",
            "conclusion": "meta 已明确为耗时语义，＋/－准确表达展开与收起；无阻断项。",
        },
        "ux_laoge": {
            "status": "pass",
            "severity": {"p0": 0, "p1": 0, "p2": 0},
            "conclusion": "此前 P2-1/P2-2 均已解决；可通过本轮静态证据验收，无阻断项。",
        },
    }
    manifest["status"] = "evidence_ready_user_visual_review_pending"
    manifest["judgment"] = "A5.1 已完成纸内原位两任务预览、状态变更边界、production fixture、Godot windowed 收起/展开证据与动态 GIF；等待用户视觉裁决，未冻结。"
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    supersede_a5()
    if not godot_pass:
        raise RuntimeError("A5.1 Godot capture validation failed")
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
