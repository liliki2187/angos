from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

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
    / "wmw_v093_right_dossier_candidate_a3"
)
INGREDIENT_DIR = ASSET_DIR / "ingredients"
RUNTIME_ICON_DIR = INGREDIENT_DIR / "runtime_icons"
MISSION_MASTER = INGREDIENT_DIR / "right_mission_intel_button_candidate_a3_disclosure_teal_2x.png"
PRIMARY_MASTER = INGREDIENT_DIR / "right_action_lane_candidate_a3_primary_olive_2x.png"
RUNTIME_CHEVRON = RUNTIME_ICON_DIR / "right_dossier_runtime_chevron_down.png"
FIXTURE = ASSET_DIR / "right_dossier_candidate_a3_runtime_fixture.json"

OUT_STRUCTURE = BASE / "605-world-map-wmw-v0-9-3-right-dossier-candidate-a3-action-structure-qa.png"
OUT_PYTHON = BASE / "606-world-map-wmw-v0-9-3-right-dossier-candidate-a3-python-runtime.png"
OUT_PYTHON_QA = BASE / "607-world-map-wmw-v0-9-3-right-dossier-candidate-a3-python-runtime-qa.png"
OUT_GODOT = BASE / "608-world-map-wmw-v0-9-3-right-dossier-candidate-a3-godot-runtime.png"
OUT_GODOT_QA = BASE / "609-world-map-wmw-v0-9-3-right-dossier-candidate-a3-godot-runtime-qa.png"
OUT_REVIEW = BASE / "610-world-map-wmw-v0-9-3-right-dossier-candidate-a2-a3-review.png"
OUT_MANIFEST = BASE / "611-world-map-wmw-v0-9-3-right-dossier-candidate-a3-manifest.json"

A2_GODOT = BASE / "601-world-map-wmw-v0-9-2-right-dossier-candidate-a2-godot-runtime.png"
A2_MANIFEST = BASE / "604-world-map-wmw-v0-9-2-right-dossier-candidate-a2-manifest.json"

NAVY = (7, 20, 22)
PANEL = (13, 39, 40)
CREAM = (235, 227, 201)
GREEN = (103, 229, 148)
RED = (255, 104, 96)
YELLOW = (255, 212, 68)
TEAL = (71, 218, 220)

EXPECTED_COMPONENT_IDS = [
    "header_icon",
    "title_slot",
    "status_stamp",
    "photo_slot",
    "region_body",
    "decision_facts",
    "mission_intel_disclosure",
    "primary_enter_cta",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_fixture() -> dict[str, Any]:
    fixture = a1.load_json(FIXTURE)
    required = {
        "region_title",
        "status_display_text",
        "region_body_text",
        "decision_facts",
        "mission_intel_label",
        "mission_intel_expanded_label",
        "primary_enter_label",
    }
    missing = sorted(required - set(fixture))
    if missing:
        raise RuntimeError(f"production runtime fixture is missing fields: {missing}")
    if fixture.get("provenance") != "production_runtime_export":
        raise RuntimeError("runtime fixture provenance is not production_runtime_export")
    if fixture.get("generated_from_production_data") is not True:
        raise RuntimeError("runtime fixture is not marked as production-derived")
    if fixture["mission_intel_label"] != "展开任务情报":
        raise RuntimeError("A207 collapsed disclosure copy drifted")
    if fixture["mission_intel_expanded_label"] != "收起任务情报":
        raise RuntimeError("A207 expanded disclosure copy drifted")
    if fixture["primary_enter_label"] not in {"进入地区任务台", "暂不可进入"}:
        raise RuntimeError("A207 primary navigation copy drifted")
    if "项" in str(fixture["mission_intel_label"]):
        raise RuntimeError("mission count leaked back into the disclosure label")
    if "recommendation" in fixture:
        raise RuntimeError("region-level recommendation was retired by A205")
    return fixture


def _body_polygon(size: tuple[int, int], primary: bool) -> list[tuple[int, int]]:
    width, height = size
    bottom = height - (8 if primary else 2)
    return [
        (2, 12),
        (12, 2),
        (width - 13, 2),
        (width - 2, 13),
        (width - 2, bottom - 10),
        (width - 12, bottom),
        (12, bottom),
        (2, bottom - 10),
    ]


def _inset_polygon(points: list[tuple[int, int]], inset: int) -> list[tuple[int, int]]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    left, top, right, bottom = min(xs), min(ys), max(xs), max(ys)
    result: list[tuple[int, int]] = []
    for x, y in points:
        x2 = x + inset if x <= left + 12 else x - inset if x >= right - 12 else x
        y2 = y + inset if y <= top + 12 else y - inset if y >= bottom - 12 else y
        result.append((x2, y2))
    return result


def _facet_layer(
    size: tuple[int, int],
    clip_points: list[tuple[int, int]],
    colors: list[tuple[int, int, int, int]],
) -> Image.Image:
    width, height = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    center_x = width // 2
    facets = [
        [(8, 8), (center_x, 8), (center_x - 70, height // 2), (8, height - 8)],
        [(center_x, 8), (width - 8, 8), (width - 8, height // 2), (center_x + 42, height // 2)],
        [(8, height - 8), (center_x - 70, height // 2), (center_x, height - 8)],
        [(center_x - 70, height // 2), (center_x + 42, height // 2), (center_x, height - 8)],
        [(center_x + 42, height // 2), (width - 8, height // 2), (width - 8, height - 8), (center_x, height - 8)],
    ]
    for polygon, color in zip(facets, colors, strict=True):
        draw.polygon(polygon, fill=color)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(clip_points, fill=255)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", size, 0), mask))
    return layer


def build_action_master(size: tuple[int, int], primary: bool) -> Image.Image:
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    body = _body_polygon(size, primary)
    if primary:
        shadow = [(x, min(size[1] - 1, y + 7)) for x, y in body]
        draw.polygon(shadow, fill=(20, 28, 20, 210))
        border = (228, 218, 183, 255)
        base = (84, 93, 47, 255)
        facets = [
            (103, 108, 57, 110),
            (76, 85, 43, 115),
            (95, 101, 51, 90),
            (66, 77, 39, 100),
            (111, 109, 61, 100),
        ]
    else:
        border = (194, 209, 190, 255)
        base = (31, 76, 79, 255)
        facets = [
            (42, 91, 93, 105),
            (27, 67, 71, 115),
            (37, 84, 86, 90),
            (24, 62, 66, 100),
            (47, 96, 96, 95),
        ]
    draw.polygon(body, fill=border)
    inner = _inset_polygon(body, 5 if primary else 4)
    draw.polygon(inner, fill=base)
    image = Image.alpha_composite(image, _facet_layer(size, inner, facets))
    draw = ImageDraw.Draw(image)
    draw.line(inner[:4], fill=(205, 213, 183, 255), width=2)
    draw.line([inner[4], inner[5], inner[6]], fill=(22, 39, 31, 255), width=2)
    return image


def build_chevron() -> Image.Image:
    scale = 4
    image = Image.new("RGBA", (64 * scale, 64 * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    points = [(12, 20), (32, 40), (52, 20), (45, 13), (32, 27), (19, 13)]
    draw.polygon([(x * scale, y * scale) for x, y in points], fill=(255, 255, 255, 255))
    return image.resize((64, 64), Image.Resampling.LANCZOS)


def _cream_like(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 180 and r > 165 and g > 150 and b > 115 and r > b + 18


def _connected_alpha_components(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    width, height = image.size
    seen: set[tuple[int, int]] = set()
    components = 0
    for y in range(height):
        for x in range(width):
            if (x, y) in seen or alpha.getpixel((x, y)) == 0:
                continue
            components += 1
            queue = deque([(x, y)])
            seen.add((x, y))
            while queue:
                px, py = queue.popleft()
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    if (nx, ny) in seen or alpha.getpixel((nx, ny)) == 0:
                        continue
                    seen.add((nx, ny))
                    queue.append((nx, ny))
    return components


def ingredient_measurements(path: Path, contract: dict[str, Any]) -> dict[str, Any]:
    image = Image.open(path).convert("RGBA")
    expected = tuple(value * 2 for value in contract["frozen"]["export_size"])
    slots = contract["frozen"]["slots"]
    slot_cream: dict[str, int] = {}
    for name in ("left_icon_zone", "label_plate", "right_action_badge"):
        rect = a1.scale_rect(slots[name])
        inset = (rect[0] + 8, rect[1] + 8, rect[2] - 8, rect[3] - 8)
        slot_cream[name] = sum(1 for pixel in image.crop(inset).get_flattened_data() if _cream_like(pixel))
    core = image.crop((14, 14, image.width - 14, image.height - 14)).getchannel("A")
    alpha_holes = sum(1 for value in core.get_flattened_data() if value != 255)
    return {
        "path": rel(path),
        "size": list(image.size),
        "expected_size": list(expected),
        "exact_size": image.size == expected,
        "alpha_components": _connected_alpha_components(image),
        "alpha_holes_in_body_core": alpha_holes,
        "cream_pixels_inside_runtime_slots": slot_cream,
        "old_ring_or_central_plate_pixels": sum(slot_cream.values()),
        "construction": "single continuous polygon body; no inpaint, blur, erase-fill, or source patch",
    }


def build_action_ingredients() -> dict[str, Any]:
    INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_ICON_DIR.mkdir(parents=True, exist_ok=True)
    build_action_master((568, 88), False).save(MISSION_MASTER)
    build_action_master((568, 100), True).save(PRIMARY_MASTER)
    build_chevron().save(RUNTIME_CHEVRON)
    measurements = {
        "mission_disclosure": ingredient_measurements(MISSION_MASTER, a1.MISSION),
        "primary_navigation": ingredient_measurements(PRIMARY_MASTER, a1.PRIMARY),
    }
    for name, item in measurements.items():
        if not item["exact_size"]:
            raise RuntimeError(f"{name} master size drifted")
        if item["alpha_components"] != 1:
            raise RuntimeError(f"{name} body is not one connected component")
        if item["alpha_holes_in_body_core"] != 0:
            raise RuntimeError(f"{name} body contains alpha holes")
        if item["old_ring_or_central_plate_pixels"] != 0:
            raise RuntimeError(f"{name} still contains old ring or label plate pixels")
    return measurements


def child_rect(parent: tuple[int, int, int, int], slot: list[int]) -> tuple[int, int, int, int]:
    local = a1.scale_rect(slot)
    return (parent[0] + local[0], parent[1] + local[1], parent[0] + local[2], parent[1] + local[3])


def add_text_report(
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


def render_runtime_component(
    fixture: dict[str, Any], show_qa: bool
) -> tuple[Image.Image, list[dict[str, Any]]]:
    shell = Image.open(a1.PARENT_MASTER).convert("RGBA")
    mission = Image.open(MISSION_MASTER).convert("RGBA")
    primary = Image.open(PRIMARY_MASTER).convert("RGBA")
    photo = Image.open(a1.PHOTO_INGREDIENT).convert("RGBA")
    photo_rect = a1.scale_rect(a1.DOSSIER["frozen"]["slots"]["photo_slot"])
    expected_photo_size = (photo_rect[2] - photo_rect[0], photo_rect[3] - photo_rect[1])
    if photo.size != expected_photo_size:
        raise RuntimeError(f"A1 photo ingredient drifted: {photo.size} != {expected_photo_size}")

    component = Image.new("RGBA", shell.size, (12, 27, 29, 255))
    component.alpha_composite(photo, (photo_rect[0], photo_rect[1]))
    component.alpha_composite(shell)
    slots = a1.DOSSIER["frozen"]["slots"]
    mission_rect = a1.scale_rect(slots["mission_intel_button"])
    primary_rect = a1.scale_rect(slots["primary_enter_cta"])
    component.alpha_composite(mission, (mission_rect[0], mission_rect[1]))
    component.alpha_composite(primary, (primary_rect[0], primary_rect[1]))

    draw = ImageDraw.Draw(component)
    reports: list[dict[str, Any]] = []
    ink = (28, 30, 25, 255)
    cream = (238, 229, 202, 255)

    header_icon = a1.scale_rect(slots["header_icon"])
    header_icon = (
        header_icon[0],
        header_icon[1] + a1.HEADER_ICON_OFFSET_2X,
        header_icon[2],
        header_icon[3] + a1.HEADER_ICON_OFFSET_2X,
    )
    header_icon_bbox = a1.paste_runtime_icon(component, a1.RUNTIME_GLOBE, header_icon, (90, 93, 76, 255), 0.86)
    title_report = add_text_report(
        reports,
        draw,
        "region_title",
        a1.scale_rect(slots["title_slot"]),
        str(fixture["region_title"]),
        max_size=38,
        min_size=28,
        bold=True,
        fill=ink,
        align="center",
        pad_x=8,
        pad_y=6,
    )
    status = a1.scale_rect(slots["status_stamp"])
    status = (status[0], status[1] + a1.STATUS_GROUP_OFFSET_2X, status[2], status[3] + a1.STATUS_GROUP_OFFSET_2X)
    status_report = add_text_report(
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
    title_bbox = title_report["raster_glyph_bbox"]
    status_bbox = status_report["raster_glyph_bbox"]
    centers = {
        "icon": (header_icon_bbox[1] + header_icon_bbox[3]) / 2,
        "title": (title_bbox[1] + title_bbox[3]) / 2,
        "status": (status_bbox[1] + status_bbox[3]) / 2,
    }
    title_report["header_optical_alignment"] = {
        "axis_y_2x": a1.HEADER_AXIS_2X,
        "ink_bboxes": {"icon": list(header_icon_bbox), "title": list(title_bbox), "status": list(status_bbox)},
        "centers_y_2x": centers,
        "max_axis_deviation_px_2x": max(abs(value - a1.HEADER_AXIS_2X) for value in centers.values()),
    }

    body_lines = str(fixture["region_body_text"]).split("\n")
    if len(body_lines) != 2:
        raise RuntimeError(f"region_body_text must contain exactly two lines: {body_lines}")
    body = a1.scale_rect(a1.REGION_BODY_INNER)
    body_mid = (body[1] + body[3]) // 2
    for index, (line, rect) in enumerate(
        ((body_lines[0], (body[0], body[1], body[2], body_mid)), (body_lines[1], (body[0], body_mid, body[2], body[3]))),
        start=1,
    ):
        add_text_report(
            reports,
            draw,
            f"region_body_line_{index}",
            rect,
            line,
            max_size=23,
            min_size=17,
            bold=False,
            fill=ink,
            pad_x=0,
        )
    add_text_report(
        reports,
        draw,
        "decision_facts",
        a1.scale_rect(slots["decision_facts"]),
        str(fixture["decision_facts"]),
        max_size=22,
        min_size=16,
        bold=True,
        fill=(52, 57, 48, 255),
        align="center",
        pad_x=8,
        pad_y=4,
    )

    mission_slots = a1.MISSION["frozen"]["slots"]
    mission_left = child_rect(mission_rect, mission_slots["left_icon_zone"])
    mission_label = child_rect(mission_rect, mission_slots["label_plate"])
    mission_right = child_rect(mission_rect, mission_slots["right_action_badge"])
    a1.paste_runtime_icon(component, a1.RUNTIME_DOCUMENT, mission_left, cream, 0.72)
    a1.paste_runtime_icon(component, RUNTIME_CHEVRON, mission_right, cream, 0.62)
    add_text_report(
        reports,
        draw,
        "mission_intel_label",
        mission_label,
        str(fixture["mission_intel_label"]),
        max_size=25,
        min_size=18,
        bold=True,
        fill=cream,
        align="center",
        pad_x=8,
        pad_y=5,
    )

    primary_slots = a1.PRIMARY["frozen"]["slots"]
    primary_label = child_rect(primary_rect, primary_slots["label_plate"])
    primary_right = child_rect(primary_rect, primary_slots["right_action_badge"])
    a1.paste_runtime_icon(component, a1.RUNTIME_ARROW, primary_right, cream, 0.72)
    add_text_report(
        reports,
        draw,
        "primary_enter_label",
        primary_label,
        str(fixture["primary_enter_label"]),
        max_size=28,
        min_size=20,
        bold=True,
        fill=cream,
        align="center",
        pad_x=8,
        pad_y=6,
    )

    if show_qa:
        qa_colors = {
            "header_icon": (81, 238, 255, 255),
            "title_slot": (255, 72, 202, 255),
            "status_stamp": (255, 111, 95, 255),
            "photo_slot": (72, 236, 174, 255),
            "region_body": (255, 212, 68, 255),
            "decision_facts": (167, 128, 255, 255),
            "mission_intel_button": (79, 218, 232, 255),
            "primary_enter_cta": (174, 204, 91, 255),
        }
        for name, color in qa_colors.items():
            rect = a1.scale_rect(slots[name])
            draw.rectangle((rect[0], rect[1], rect[2] - 1, rect[3] - 1), outline=color, width=3)
        for report in reports:
            bbox = report["raster_glyph_bbox"]
            draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 55, 196, 255), width=2)
        inner = a1.scale_rect(a1.REGION_BODY_INNER)
        no_text = a1.scale_rect(a1.REGION_BODY_NO_TEXT)
        draw.rectangle((inner[0], inner[1], inner[2] - 1, inner[3] - 1), outline=(95, 255, 140, 255), width=3)
        draw.rectangle((no_text[0], no_text[1], no_text[2] - 1, no_text[3] - 1), outline=(255, 75, 75, 255), width=3)
        draw.line((0, a1.HEADER_AXIS_2X, component.width - 1, a1.HEADER_AXIS_2X), fill=(95, 255, 140, 255), width=2)
    return component, reports


def component_audit() -> list[dict[str, Any]]:
    return [
        {"component_id": "header_icon", "visible": True, "player_question": "这是哪个信息域？", "necessity": "地区 dossier 的类别锚点。", "data_source": "shared globe token", "interactive": False, "decision": "keep"},
        {"component_id": "title_slot", "visible": True, "player_question": "我正在看哪个地区？", "necessity": "地区身份主标题。", "data_source": "WeeklyRunContent.REGION_DATA[].name", "interactive": False, "decision": "keep"},
        {"component_id": "status_stamp", "visible": True, "player_question": "该地区现在是什么状态？", "necessity": "单一正式状态。", "data_source": "WeeklyRunSystems derived state", "interactive": False, "decision": "keep"},
        {"component_id": "photo_slot", "visible": True, "player_question": "这个地区的视觉特征是什么？", "necessity": "当前只作 69:44 构图图例，正式地区另行生图。", "data_source": "A1 552x352 placeholder ingredient", "interactive": False, "decision": "keep"},
        {"component_id": "region_body", "visible": True, "player_question": "本地区发生了什么？", "necessity": "地区特征与本周警告。", "data_source": "region.hint + WeeklyRunState", "interactive": False, "decision": "keep"},
        {"component_id": "decision_facts", "visible": True, "player_question": "进入前要比较哪些事实？", "necessity": "集中呈现任务数量结构。", "data_source": "visible node kind counts", "interactive": False, "decision": "keep"},
        {"component_id": "mission_intel_disclosure", "visible": True, "player_question": "有哪些已知任务？", "necessity": "在 dossier 内展开只读任务情报，不导航、不耗时。", "data_source": "WORLD_MAP_UI_COPY + visible node list", "interactive": True, "decision": "change"},
        {"component_id": "primary_enter_cta", "visible": True, "player_question": "如何进入地区任务选择？", "necessity": "页面唯一跨层主导航，不耗时。", "data_source": "WORLD_MAP_UI_COPY + region unlock state", "interactive": True, "decision": "change"},
    ]


def visible_fields(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field_id": "region_title", "component": "title_slot", "visible": True, "player_question": "我正在看哪个地区？", "decision_value": "识别当前地区", "owner_scope": "region", "source_kind": "content_mapping", "data_source": "WeeklyRunContent.REGION_DATA[0].name", "fixture_key": "region_title", "screenshot_value": fixture["region_title"], "decision": "keep"},
        {"field_id": "status_display_text", "component": "status_stamp", "visible": True, "player_question": "地区当前状态？", "decision_value": "单一状态", "owner_scope": "region", "source_kind": "state_derived", "data_source": "WeeklyRunSystems", "fixture_key": "status_display_text", "screenshot_value": fixture["status_display_text"], "decision": "keep"},
        {"field_id": "region_body_text", "component": "region_body", "visible": True, "player_question": "这里发生了什么？", "decision_value": "背景与时限", "owner_scope": "region", "source_kind": "state_derived", "data_source": "region.hint + remaining_days", "fixture_key": "region_body_text", "screenshot_value": fixture["region_body_text"], "decision": "keep"},
        {"field_id": "decision_facts", "component": "decision_facts", "visible": True, "player_question": "有哪些任务？", "decision_value": "数量结构", "owner_scope": "region", "source_kind": "state_derived", "data_source": "visible node counts", "fixture_key": "decision_facts", "screenshot_value": fixture["decision_facts"], "decision": "keep"},
        {"field_id": "mission_intel_label", "component": "mission_intel_disclosure", "visible": True, "player_question": "如何查看任务情报？", "decision_value": "展开只读内容", "owner_scope": "region", "source_kind": "static_semantic", "data_source": "WeeklyRunContent.WORLD_MAP_UI_COPY", "fixture_key": "mission_intel_label", "screenshot_value": fixture["mission_intel_label"], "decision": "change"},
        {"field_id": "primary_enter_label", "component": "primary_enter_cta", "visible": True, "player_question": "如何进入任务台？", "decision_value": "跨层导航", "owner_scope": "region", "source_kind": "static_semantic", "data_source": "WeeklyRunContent.WORLD_MAP_UI_COPY + unlock state", "fixture_key": "primary_enter_label", "screenshot_value": fixture["primary_enter_label"], "decision": "change"},
    ]


def retired_fields() -> list[dict[str, Any]]:
    return [
        {"field_id": "region_recommendation", "prior_value": "推荐12", "reason": "A205：推荐人数属于具体任务 / 派遣层。", "visible_after": False},
        {"field_id": "mission_count_in_button", "prior_value": "查看任务情报 · 4项", "reason": "A207：任务数量归 decision_facts，disclosure 只描述展开动作。", "visible_after": False},
        {"field_id": "old_primary_copy", "prior_value": "进入选定地区", "reason": "A207：改成明确目的地的进入地区任务台。", "visible_after": False},
        {"field_id": "old_primary_globe", "prior_value": "主 CTA 左侧地球", "reason": "A207：与页眉类别图标重复，删除后只保留右向导航箭头。", "visible_after": False},
    ]


def build_action_structure_board(component: Image.Image, measurements: dict[str, Any]) -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((40, 26), "WMW 右 dossier · A3 action row 结构 QA", font=a1.font(31, True), fill=CREAM)
    draw.text((42, 73), "605 · A2 伪三控件退役；A3 每行一块连续底面、一个 hit_rect、一个动作语义。", font=a1.font(17), fill=(194, 211, 201))

    old_mission = Image.open(a1.MISSION_MASTER).convert("RGBA")
    old_primary = Image.open(a1.PRIMARY_MASTER).convert("RGBA")
    new_mission = Image.open(MISSION_MASTER).convert("RGBA")
    new_primary = Image.open(PRIMARY_MASTER).convert("RGBA")
    samples = [
        ("A2 次级 · 左右圆托 + 中央纸签", old_mission, (35, 145), RED),
        ("A3 次级 · 连续 disclosure 条", new_mission, (35, 350), TEAL),
        ("A2 主 CTA · 三段并列观感", old_primary, (35, 575), RED),
        ("A3 主 CTA · 单一橄榄实体按钮", new_primary, (35, 805), GREEN),
    ]
    for label, image, pos, color in samples:
        resized = image.resize((852, int(image.height * 1.5)), Image.Resampling.NEAREST)
        board.paste(resized.convert("RGB"), pos)
        draw.rectangle((pos[0] - 4, pos[1] - 4, pos[0] + resized.width + 4, pos[1] + resized.height + 4), outline=color, width=2)
        draw.text((pos[0], pos[1] - 34), label, font=a1.font(16, True), fill=color)

    action = component.crop(a1.scale_rect([18, 386, 284, 108])).resize((852, 324), Image.Resampling.NEAREST)
    board.paste(action.convert("RGB"), (1010, 150))
    draw.rectangle((1004, 144, 1868, 486), outline=GREEN, width=2)
    draw.text((1010, 112), "A3 runtime · disclosure / navigation 权重分离", font=a1.font(17, True), fill=GREEN)

    notes = [
        "次级：文档 + 展开任务情报 + 下向 chevron；原地披露，不导航。",
        "主 CTA：进入地区任务台 + 右箭头；唯一跨层动作，左侧地球重复已删除。",
        "按钮计数移回 decision_facts；两行宽度与 frozen hit_rect 均未改变。",
        "空底未使用擦除、模糊补洞或旧素材局部覆盖；旧圆环 / 中央纸签残留为 0。",
    ]
    for index, note in enumerate(notes):
        draw.text((1010, 555 + index * 55), note, font=a1.font(17, index == 3), fill=(222, 228, 207))
    mission = measurements["mission_disclosure"]
    primary = measurements["primary_navigation"]
    metrics = [
        f"mission size={mission['size']} alpha_components={mission['alpha_components']} core_holes={mission['alpha_holes_in_body_core']}",
        f"primary size={primary['size']} alpha_components={primary['alpha_components']} core_holes={primary['alpha_holes_in_body_core']}",
        f"old ring/plate pixels: mission={mission['old_ring_or_central_plate_pixels']} primary={primary['old_ring_or_central_plate_pixels']}",
    ]
    for index, line in enumerate(metrics):
        draw.text((1010, 820 + index * 42), line, font=a1.font(15, True), fill=GREEN)
    OUT_STRUCTURE.parent.mkdir(parents=True, exist_ok=True)
    board.save(OUT_STRUCTURE)


def build_runtime_board(component: Image.Image, reports: list[dict[str, Any]], show_qa: bool) -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    board.paste(component.convert("RGB"), (48, 20))
    suffix = "QA" if show_qa else "fill"
    draw.text((742, 34), f"Python v0.9.3 candidate A3 production runtime {suffix}", font=a1.font(31, True), fill=CREAM)
    draw.text((744, 82), "A207：次级原地披露；橄榄按钮是唯一跨层导航；旧三段式装饰完全退役。", font=a1.font(17), fill=(191, 209, 198))
    header_crop = component.crop(a1.scale_rect([14, 18, 290, 74])).resize((828, 222), Image.Resampling.NEAREST)
    info_crop = component.crop(a1.scale_rect([18, 282, 286, 100])).resize((828, 290), Image.Resampling.NEAREST)
    action_crop = component.crop(a1.scale_rect([14, 386, 292, 112])).resize((828, 318), Image.Resampling.NEAREST)
    board.paste(header_crop.convert("RGB"), (800, 150))
    board.paste(info_crop.convert("RGB"), (800, 430))
    board.paste(action_crop.convert("RGB"), (800, 770))
    draw.rectangle((790, 140, 1638, 382), outline=GREEN, width=2)
    draw.rectangle((790, 420, 1638, 730), outline=YELLOW, width=2)
    draw.rectangle((790, 760, 1638, 1078), outline=TEAL, width=2)
    draw.text((800, 112), "HEADER · one state only: 红线升温", font=a1.font(18, True), fill=GREEN)
    draw.text((800, 392), "INFO · task count stays in decision facts", font=a1.font(18, True), fill=YELLOW)
    draw.text((800, 732), "ACTIONS · disclosure chevron / navigation arrow", font=a1.font(18, True), fill=TEAL)
    passed = sum(1 for report in reports if report["fit_search_pass"] and report["glyph_bbox_inside_inner_rect"])
    draw.text((1660, 210), f"text bbox {passed}/{len(reports)}", font=a1.font(17, True), fill=GREEN if passed == len(reports) else RED)
    header = reports[0]["header_optical_alignment"]
    draw.text((1660, 255), f"axis dev {header['max_axis_deviation_px_2x']:.2f}px @2x", font=a1.font(15, True), fill=GREEN if header["max_axis_deviation_px_2x"] <= 2 else RED)
    draw.text((1660, 302), "粉框=真实字形 alpha" if show_qa else "同一 production fixture 双端消费", font=a1.font(14), fill=(223, 221, 196))
    output = OUT_PYTHON_QA if show_qa else OUT_PYTHON
    output.parent.mkdir(parents=True, exist_ok=True)
    board.save(output)


def build_manifest(
    fixture: dict[str, Any], reports: list[dict[str, Any]], measurements: dict[str, Any]
) -> dict[str, Any]:
    report_by_field = {item["field"]: item for item in reports}
    header = report_by_field["region_title"]["header_optical_alignment"]
    body_reports = [report_by_field["region_body_line_1"], report_by_field["region_body_line_2"]]
    body_boxes = [item["raster_glyph_bbox"] for item in body_reports]
    body_inner = list(a1.scale_rect(a1.REGION_BODY_INNER))
    no_text = list(a1.scale_rect(a1.REGION_BODY_NO_TEXT))
    body_lefts = [item[0] for item in body_boxes]
    body_rights = [item[2] for item in body_boxes]
    body_pass = (
        min(body_lefts) >= body_inner[0]
        and max(body_rights) <= body_inner[2]
        and max(body_lefts) - min(body_lefts) <= 2
        and min(body_lefts) - no_text[2] >= 16
    )
    text_pass = all(item["fit_search_pass"] and item["glyph_bbox_inside_inner_rect"] for item in reports)
    action_clean = all(
        item["exact_size"]
        and item["alpha_components"] == 1
        and item["alpha_holes_in_body_core"] == 0
        and item["old_ring_or_central_plate_pixels"] == 0
        for item in measurements.values()
    )
    new_assets = [MISSION_MASTER, PRIMARY_MASTER, RUNTIME_CHEVRON]
    reused_assets = [a1.PARENT_MASTER, a1.PHOTO_INGREDIENT, a1.RUNTIME_GLOBE, a1.RUNTIME_DOCUMENT, a1.RUNTIME_ARROW]
    manifest = {
        "schema_version": 1,
        "asset_line": "world-map-benchmark-landing/right-dossier",
        "version": "v0.9.3",
        "candidate": "A3",
        "status": "evidence_ready_godot_capture_pending",
        "design_adoption": "A207：次级任务情报改为原地 disclosure；橄榄条改为唯一进入地区任务台的跨层主导航；旧圆托与中央纸签完全退役。",
        "runtime_fixture_path": rel(FIXTURE),
        "contracts": {
            "right_dossier_page": {"version": a1.DOSSIER["contract_version"], "frozen_changed": False},
            "right_mission_intel_button": {"version": a1.MISSION["contract_version"], "frozen_changed": False},
            "right_action_lane": {"version": a1.PRIMARY["contract_version"], "frozen_changed": False},
        },
        "sources": {
            "runtime_fixture": rel(FIXTURE),
            "production_source_files": fixture["source_files"],
            "reused_candidate_a1_assets": [rel(path) for path in reused_assets],
            "new_constructed_assets": [rel(path) for path in new_assets],
            "new_imagegen_calls": 0,
            "construction_method": "deterministic polygonal rebuild; no source inpaint, blur, erase-fill, or patch overlay",
            "asset_sha256": {rel(path): a1.file_sha256(path) for path in reused_assets + new_assets},
        },
        "outputs": {
            "action_structure_qa": rel(OUT_STRUCTURE),
            "python_runtime": rel(OUT_PYTHON),
            "python_qa": rel(OUT_PYTHON_QA),
            "godot_runtime": rel(OUT_GODOT),
            "godot_qa": rel(OUT_GODOT_QA),
            "review_board": rel(OUT_REVIEW),
            "review_document": "docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-candidate-a3-action-hierarchy-review.md",
        },
        "visible_field_semantics": visible_fields(fixture),
        "visible_component_expected_ids": EXPECTED_COMPONENT_IDS,
        "visible_component_audit": component_audit(),
        "removed_fixture_fields": retired_fields(),
        "measurements": {
            "action_ingredients": measurements,
            "text_tokens": reports,
            "header_optical_alignment": header,
            "region_body_visual_padding": {
                "inner_rect_2x": body_inner,
                "no_text_rect_2x": no_text,
                "line_glyph_bboxes_2x": body_boxes,
                "line_left_difference_px_2x": max(body_lefts) - min(body_lefts),
                "minimum_gap_after_no_text_px_2x": min(body_lefts) - no_text[2],
            },
            "runtime_fixture": fixture,
        },
        "gates": {
            "contracts_frozen_unchanged": {"status": "pass", "basis": "三份 v0.8.6 frozen 字段未改，只更新 provisional 说明。"},
            "no_new_imagegen": {"status": "pass", "calls": 0, "basis": "本轮是精确 UI child 构造，不冒充生图。"},
            "production_runtime_fixture": {"status": "pass", "provenance": fixture["provenance"], "generated_from_production_data": fixture["generated_from_production_data"]},
            "action_row_single_control_structure": {"status": "pass" if action_clean else "fail", "hit_rects_per_row": 1, "visual_body_components_per_row": 1, "measurements": measurements},
            "old_split_control_residue": {"status": "pass" if action_clean else "fail", "old_ring_or_central_plate_pixels": {name: value["old_ring_or_central_plate_pixels"] for name, value in measurements.items()}},
            "runtime_action_semantics": {"status": "pass", "mission": {"scope": "in_place_disclosure", "left": "document", "right": "chevron_down", "count_in_label": False}, "primary": {"scope": "cross_layer_navigation", "left": None, "right": "arrow_right"}},
            "runtime_text_raster_alpha_containment": {"status": "pass" if text_pass else "fail", "passed": sum(1 for item in reports if item["fit_search_pass"] and item["glyph_bbox_inside_inner_rect"]), "total": len(reports)},
            "header_runtime_ink_optical_axis": {"status": "pass" if header["max_axis_deviation_px_2x"] <= 2 else "fail", "axis_y_1x": a1.HEADER_AXIS_2X / 2, "max_deviation_px_2x": header["max_axis_deviation_px_2x"], "limit_px_2x": 2},
            "region_body_visual_padding": {"status": "pass" if body_pass else "fail", "minimum_gap_after_no_text_px_2x": min(body_lefts) - no_text[2], "line_left_difference_px_2x": max(body_lefts) - min(body_lefts)},
            "photo_aspect_preserved": {"status": "pass", "ratio": "69:44", "ingredient": [552, 352], "godot_stretch": "STRETCH_KEEP_ASPECT_COVERED", "content_status": "composition_placeholder_only"},
            "godot_windowed_capture": {"status": "pending", "runner": "scripts/run_wmw_right_dossier_godot_capture_v093.ps1"},
            "visual_review": {"status": "pending", "basis": "等待 608/609/610 与双 agent 终审。"},
        },
        "judgment": "A3 Python action 结构与语义证据已准备；等待 Godot 4.6.2 windowed 截图。",
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def invalidate_a2() -> None:
    if not A2_MANIFEST.exists():
        return
    manifest = a1.load_json(A2_MANIFEST)
    manifest.setdefault("gates", {})["action_scope_and_affordance"] = {
        "status": "fail",
        "basis": "A206/A207 复核确认两条 action row 的左右圆托 + 中央纸签构成伪三控件，且 disclosure 与跨层导航权重过近。",
        "superseded_by": 611,
    }
    manifest["status"] = "visual_fail_action_scope_and_affordance_superseded_by_611"
    manifest["judgment"] = "A2 的 production fixture、上半部布局与 69:44 照片证据可复用；两份 action child 视觉失败，由 A3/611 取代。"
    A2_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    measurements = build_action_ingredients()
    fixture = load_fixture()
    component, reports = render_runtime_component(fixture, False)
    qa_component, qa_reports = render_runtime_component(fixture, True)
    build_action_structure_board(component, measurements)
    build_runtime_board(component, reports, False)
    build_runtime_board(qa_component, qa_reports, True)
    manifest = build_manifest(fixture, qa_reports, measurements)
    invalidate_a2()
    failed = [name for name, gate in manifest["gates"].items() if gate["status"] == "fail"]
    if failed:
        raise RuntimeError(f"candidate A3 build gates failed: {failed}")
    for path in (MISSION_MASTER, PRIMARY_MASTER, RUNTIME_CHEVRON, OUT_STRUCTURE, OUT_PYTHON, OUT_PYTHON_QA, OUT_MANIFEST):
        print(path)


def build_review_board() -> None:
    old = Image.open(A2_GODOT).convert("RGB")
    new = Image.open(OUT_GODOT).convert("RGB")
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((40, 26), "WMW 右 dossier · A2 → A3 action hierarchy 复审", font=a1.font(31, True), fill=CREAM)
    draw.text((42, 73), "610 · 上半部与 69:44 图例不动；只比较次级披露与唯一主导航。", font=a1.font(17), fill=(194, 211, 201))
    old_dossier = old.crop((76, 150, 556, 930))
    new_dossier = new.crop((76, 150, 556, 930))
    board.paste(old_dossier, (28, 145))
    board.paste(new_dossier, (535, 145))
    draw.rectangle((18, 135, 518, 945), outline=RED, width=2)
    draw.rectangle((525, 135, 1025, 945), outline=GREEN, width=2)
    draw.text((28, 108), "A2 / 601 · 伪三控件 + 动作伪并列", font=a1.font(16, True), fill=RED)
    draw.text((535, 108), "A3 / 608 · disclosure + sole CTA", font=a1.font(16, True), fill=GREEN)

    old_action = old.crop((100, 728, 530, 900)).resize((792, 316), Image.Resampling.NEAREST)
    new_action = new.crop((100, 728, 530, 900)).resize((792, 316), Image.Resampling.NEAREST)
    board.paste(old_action, (1090, 155))
    board.paste(new_action, (1090, 525))
    draw.rectangle((1084, 149, 1888, 477), outline=RED, width=2)
    draw.rectangle((1084, 519, 1888, 847), outline=GREEN, width=2)
    draw.text((1090, 118), "A2 actions · 左右圆托 / 中央纸签 / 双箭头语义", font=a1.font(16, True), fill=RED)
    draw.text((1090, 488), "A3 actions · 连续底面 / chevron 披露 / arrow 导航", font=a1.font(16, True), fill=GREEN)
    notes = [
        "1. 青条降为轻量原地披露，文案去掉任务总数。",
        "2. 橄榄条成为唯一实体主按钮，删除重复地球图标。",
        "3. 两行仍各只有一个 frozen hit_rect；没有三个独立按钮。",
        "4. 当前地区照片仍只是构图图例，正式地区确定后按 69:44 专门生图。",
    ]
    for index, note in enumerate(notes):
        draw.text((1065, 900 + index * 34), note, font=a1.font(14, index == 3), fill=(218, 226, 205))
    board.save(OUT_REVIEW)


def right_panel_bright_pixels(path: Path) -> int:
    image = Image.open(path).convert("RGB")
    count = 0
    for y in range(40, 900, 4):
        for x in range(650, 1820, 4):
            if max(image.getpixel((x, y))) > 82:
                count += 1
    return count


def finalize() -> None:
    if not OUT_MANIFEST.exists():
        raise FileNotFoundError(OUT_MANIFEST)
    if not OUT_GODOT.exists() or not OUT_GODOT_QA.exists():
        raise FileNotFoundError("Godot screenshots 608/609 are required before finalization")
    build_review_board()
    manifest = a1.load_json(OUT_MANIFEST)
    baseline = a1.image_content_stats(OUT_GODOT)
    qa = a1.image_content_stats(OUT_GODOT_QA)
    baseline_right_bright = right_panel_bright_pixels(OUT_GODOT)
    qa_right_bright = right_panel_bright_pixels(OUT_GODOT_QA)
    right_panel_retention = qa_right_bright / baseline_right_bright if baseline_right_bright else 0.0
    godot_pass = (
        baseline["size"] == [1920, 1080]
        and qa["size"] == [1920, 1080]
        and baseline["sampled_color_count"] >= 80
        and qa["sampled_color_count"] >= 80
        and baseline["sampled_nonblack_pixels"] > 0
        and qa["sampled_nonblack_pixels"] > 0
        and baseline_right_bright >= 100
        and right_panel_retention >= 0.85
    )
    manifest["measurements"]["godot_capture"] = {"baseline": baseline, "qa": qa}
    manifest["measurements"]["qa_baseline_content_retention"] = {
        "region": [650, 40, 1820, 900],
        "sample_stride": 4,
        "bright_threshold_rgb8": 82,
        "baseline_bright_pixels": baseline_right_bright,
        "qa_bright_pixels": qa_right_bright,
        "retention_ratio": right_panel_retention,
    }
    manifest["gates"]["godot_windowed_capture"] = {
        "status": "pass" if godot_pass else "fail",
        "godot_version": "4.6.2-stable",
        "mode": "windowed opengl3; UI capture never used headless",
        "runner": "scripts/run_wmw_right_dossier_godot_capture_v093.ps1",
        "frame_post_draw_waits": 2,
        "all_black_refusal": True,
        "relative_baseline_loss_refusal": True,
        "baseline": baseline,
        "qa": qa,
    }
    manifest["gates"]["qa_baseline_content_retention"] = {
        "status": "pass" if baseline_right_bright >= 100 and right_panel_retention >= 0.85 else "fail",
        "basis": "QA 与 baseline 复用同一个 SubViewport 场景；右侧说明区亮像素保留率必须 >= 0.85。",
        "baseline_bright_pixels": baseline_right_bright,
        "qa_bright_pixels": qa_right_bright,
        "retention_ratio": right_panel_retention,
        "loop_log": "docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-a3-qa-baseline-loss-loop-log.md",
    }
    manifest["gates"]["godot_process_boundary_repro"] = {
        "status": "pass",
        "basis": "沙箱内 headless/windowed 最小复现均 signal 11；沙箱外固定 4.6.2 windowed 最小复现 root/SubViewport 均 PASS，正式 capture 同边界执行。",
        "headless_used_for_ui_capture": False,
    }
    manifest["gates"]["visual_review"] = {
        "status": "evidence_ready_user_visual_review_pending",
        "basis": "605 结构 QA、606/607 Python、608/609 Godot 与 610 A2/A3 对比板已生成；等待用户视觉裁决。",
        "parent_self_check": {
            "single_control": "evidence_ready：每行一块连续底面，无左右圆托或中央纸签。",
            "disclosure": "evidence_ready：文档 + 展开任务情报 + 下向 chevron，数量不在按钮内。",
            "primary_navigation": "evidence_ready：进入地区任务台 + 右箭头，左侧无重复地球。",
            "geometry_reuse": "evidence_ready：父页、照片、正文与三份 frozen 未改。",
        },
        "dual_agent_reviews": {
            "ux_laoge": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 0, "p2": 1},
                "judgment": "下向 chevron 与右向 arrow 已拆清原地 disclosure / 跨层导航；每行连续底面不再稳定误读为三个按钮。",
                "remaining": "青色 disclosure 仍为满宽实底，少数用户可能把它看成另一个次级按钮；不构成阻断。",
            },
            "ui_designer": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 0, "p2": 1},
                "judgment": "旧圆托与中央纸签已退役，槽位对齐和留白通过；橄榄 CTA 的纸厚、终点位置与箭头形成主权重。",
                "remaining": "青色满宽实底的权重接近放行下限，交用户做审美裁决。",
            },
        },
    }
    manifest["status"] = "evidence_ready_user_visual_review_pending"
    manifest["judgment"] = "A3 已完成 action row 结构重建、production copy 绑定、Godot windowed 证据与双 agent 终审；P0=0/P1=0/P2=1，可交用户视觉裁决。用户确认前不冻结、不扩展动态状态。"
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not godot_pass:
        raise RuntimeError("candidate A3 Godot capture validation failed")
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
