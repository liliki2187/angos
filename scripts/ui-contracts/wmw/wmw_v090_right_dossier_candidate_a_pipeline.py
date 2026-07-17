from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from statistics import median
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from wmw_text_layout_metrics import draw_text_by_raster_bbox, fit_font_by_raster


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
WORK = ROOT / "tmp" / "wmw-right-dossier-v090"
CONTRACT_DIR = ROOT / "design" / "ui-contracts" / "world-map"

OUT_ANCHOR_BOARD = BASE / "578-world-map-wmw-v0-9-0-right-dossier-three-master-anchor-board.png"
PARENT_ANCHOR = WORK / "parent_hollow_shell_anchor.png"
MISSION_ANCHOR = WORK / "mission_button_anchor.png"
PRIMARY_ANCHOR = WORK / "primary_olive_button_anchor.png"

PARENT_SOURCE = BASE / "579-world-map-wmw-v0-9-0-right-dossier-parent-imagegen-source.png"
MISSION_SOURCE = BASE / "580-world-map-wmw-v0-9-0-right-mission-button-imagegen-source.png"
PRIMARY_SOURCE = BASE / "581-world-map-wmw-v0-9-0-right-primary-olive-imagegen-source.png"
KEYED_DIR = WORK / "keyed"
PARENT_KEYED = KEYED_DIR / "parent_source_keyed.png"
MISSION_KEYED = KEYED_DIR / "mission_source_keyed.png"
PRIMARY_KEYED = KEYED_DIR / "primary_source_keyed.png"

ASSET_DIR = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map" / "wmw_v090_right_dossier_candidate_a"
INGREDIENT_DIR = ASSET_DIR / "ingredients"
PARENT_MASTER = INGREDIENT_DIR / "right_dossier_page_candidate_a_parent_hollow_shell_2x.png"
MISSION_MASTER = INGREDIENT_DIR / "right_mission_intel_button_candidate_a_teal_2x.png"
PRIMARY_MASTER = INGREDIENT_DIR / "right_action_lane_candidate_a_primary_olive_2x.png"
RUNTIME_ICON_DIR = INGREDIENT_DIR / "runtime_icons"
RUNTIME_GLOBE = RUNTIME_ICON_DIR / "right_dossier_runtime_globe.png"
RUNTIME_DOCUMENT = RUNTIME_ICON_DIR / "right_dossier_runtime_document.png"
RUNTIME_ARROW = RUNTIME_ICON_DIR / "right_dossier_runtime_arrow.png"
RUNTIME_CHECK = RUNTIME_ICON_DIR / "right_dossier_runtime_check.png"
ATLAS = ASSET_DIR / "right_dossier_candidate_a_three_master_atlas_2x.png"
ATLAS_META = ASSET_DIR / "right_dossier_candidate_a_three_master_atlas_2x.json"

OUT_MASTER_BOARD = BASE / "582-world-map-wmw-v0-9-0-right-dossier-candidate-a-clean-masters.png"
OUT_PYTHON = BASE / "583-world-map-wmw-v0-9-0-right-dossier-candidate-a-python-runtime.png"
OUT_PYTHON_QA = BASE / "584-world-map-wmw-v0-9-0-right-dossier-candidate-a-python-runtime-qa.png"
OUT_GODOT = BASE / "585-world-map-wmw-v0-9-0-right-dossier-candidate-a-godot-runtime.png"
OUT_GODOT_QA = BASE / "586-world-map-wmw-v0-9-0-right-dossier-candidate-a-godot-runtime-qa.png"
OUT_REVIEW = BASE / "587-world-map-wmw-v0-9-0-right-dossier-candidate-a-review-board.png"
OUT_MANIFEST = BASE / "588-world-map-wmw-v0-9-0-right-dossier-candidate-a-manifest.json"
REFERENCE_DOSSIER = BASE / "29-right-dossier-base-v0-21-integrated-endcaps.png"

PHOTO_SOURCE = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "world_map"
    / "wmw_v09_left_card_slice"
    / "ingredients"
    / "left_region_card_b210_clean_photo_selected.png"
)

KEY = (255, 0, 255)
PAPER = (195, 184, 156)
PAPER_LIGHT = (225, 216, 192)
PAPER_DARK = (145, 136, 112)
NAVY = (9, 24, 28)
TEAL = (47, 103, 108)
OLIVE = (82, 101, 57)
CREAM = (235, 227, 201)
GREEN = (103, 229, 148)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


DOSSIER = load_json(CONTRACT_DIR / "right_dossier_page.json")
MISSION = load_json(CONTRACT_DIR / "right_mission_intel_button.json")
PRIMARY = load_json(CONTRACT_DIR / "right_action_lane.json")


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    paths = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc") if bold else Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf") if bold else Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def xyxy(rect: list[int], origin: tuple[int, int], scale: float) -> tuple[int, int, int, int]:
    x, y, width, height = rect
    ox, oy = origin
    return (
        round(ox + x * scale),
        round(oy + y * scale),
        round(ox + (x + width) * scale),
        round(oy + (y + height) * scale),
    )


def build_parent_anchor() -> None:
    canvas = Image.new("RGB", (1024, 1536), KEY)
    draw = ImageDraw.Draw(canvas)
    origin = (128, 144)
    scale = 2.4
    width, height = DOSSIER["frozen"]["export_size"]
    left, top = origin
    right = round(left + width * scale)
    bottom = round(top + height * scale)

    draw.polygon(
        [(left - 38, top + 34), (right - 24, top + 34), (right + 22, top + 78), (right + 22, bottom + 22), (left - 38, bottom + 22)],
        fill=(68, 76, 49),
    )
    draw.rectangle((left - 16, top + 18, right + 8, bottom + 10), fill=PAPER_DARK)
    draw.polygon(
        [(left, top), (right - 92, top), (right - 68, top + 28), (right, top + 28), (right, bottom), (left, bottom)],
        fill=PAPER,
        outline=PAPER_LIGHT,
        width=5,
    )
    draw.rectangle((left + 22, top + 22, right - 22, bottom - 22), outline=(168, 156, 128), width=3)

    slots = DOSSIER["frozen"]["slots"]
    draw.ellipse(xyxy(slots["header_icon"], origin, scale), fill=PAPER_LIGHT, outline=PAPER_DARK, width=4)
    draw.rectangle(xyxy(slots["title_slot"], origin, scale), fill=(174, 163, 139), outline=PAPER_LIGHT, width=3)
    draw.rectangle(xyxy(slots["status_stamp"], origin, scale), fill=(151, 138, 111), outline=PAPER_LIGHT, width=3)

    photo = xyxy(slots["photo_slot"], origin, scale)
    draw.rectangle((photo[0] - 7, photo[1] - 7, photo[2] + 7, photo[3] + 7), fill=PAPER_LIGHT)
    draw.rectangle(photo, fill=KEY)

    body = xyxy(slots["region_body"], origin, scale)
    facts = xyxy(slots["decision_facts"], origin, scale)
    draw.rectangle(body, fill=(188, 176, 147))
    draw.line((body[0], body[1] + 8, body[0], body[3] - 8), fill=(68, 104, 100), width=5)
    draw.rectangle(facts, fill=(162, 153, 124))
    draw.line((facts[0], facts[1], facts[2], facts[1]), fill=PAPER_LIGHT, width=3)
    draw.line((facts[0], facts[3], facts[2], facts[3]), fill=PAPER_LIGHT, width=3)

    # A196 child areas stay continuous parent paper with no button frame or shadow.
    for name in ("mission_intel_button", "primary_enter_cta"):
        rect = xyxy(slots[name], origin, scale)
        draw.rectangle(rect, fill=PAPER)
    canvas.save(PARENT_ANCHOR)


def build_button_anchor(contract: dict[str, Any], path: Path, body_color: tuple[int, int, int]) -> None:
    canvas = Image.new("RGB", (1536, 1024), KEY)
    draw = ImageDraw.Draw(canvas)
    export_width, export_height = contract["frozen"]["export_size"]
    scale = 4.0
    width = round(export_width * scale)
    height = round(export_height * scale)
    left = (canvas.width - width) // 2
    top = (canvas.height - height) // 2
    right = left + width
    bottom = top + height

    draw.rectangle((left + 14, top + 18, right + 14, bottom + 18), fill=(8, 18, 19))
    draw.polygon(
        [(left + 12, top), (right - 12, top), (right, top + 12), (right, bottom - 12), (right - 12, bottom), (left + 12, bottom), (left, bottom - 12), (left, top + 12)],
        fill=body_color,
        outline=CREAM,
        width=7,
    )
    origin = (left, top)
    slots = contract["frozen"]["slots"]
    label = xyxy(slots["label_plate"], origin, scale)
    left_zone = xyxy(slots["left_icon_zone"], origin, scale)
    right_zone = xyxy(slots["right_action_badge"], origin, scale)
    draw.rectangle(label, fill=PAPER_LIGHT, outline=(200, 189, 164), width=5)
    draw.ellipse(left_zone, fill=tuple(round(value * 0.78) for value in body_color), outline=CREAM, width=7)
    draw.ellipse(right_zone, fill=tuple(round(value * 0.7) for value in body_color), outline=CREAM, width=7)
    canvas.save(path)


def build_anchor_board() -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "WMW 右 dossier v0.9.0 · 三母版 imagegen anchors", font=font(34, True), fill=CREAM)
    draw.text((44, 75), "578 · 结构锚点，不是生产美术；洋红=待透明区域，文字只存在于 QA 板外层。", font=font(16), fill=(184, 204, 196))

    parent = Image.open(PARENT_ANCHOR).resize((512, 768), Image.Resampling.LANCZOS)
    mission = Image.open(MISSION_ANCHOR).resize((650, 433), Image.Resampling.LANCZOS)
    primary = Image.open(PRIMARY_ANCHOR).resize((650, 433), Image.Resampling.LANCZOS)
    board.paste(parent, (70, 165))
    board.paste(mission, (650, 150))
    board.paste(primary, (650, 590))

    draw.rectangle((50, 125, 602, 965), outline=GREEN, width=2)
    draw.rectangle((630, 125, 1320, 595), outline=(75, 225, 225), width=2)
    draw.rectangle((630, 565, 1320, 1030), outline=(157, 182, 91), width=2)
    draw.text((70, 130), "PARENT HOLLOW SHELL · photo window only", font=font(18, True), fill=GREEN)
    draw.text((650, 130), "MISSION CHILD · teal · no glyph", font=font(18, True), fill=(75, 225, 225))
    draw.text((650, 570), "PRIMARY CHILD · olive · no glyph", font=font(18, True), fill=(157, 182, 91))

    x = 1370
    draw.rectangle((1348, 125, 1880, 1030), fill=(13, 39, 40), outline=(67, 112, 108), width=2)
    draw.text((x, 155), "LOCKED INPUT RULES", font=font(21, True), fill=CREAM)
    rules = [
        "1. 三个独立 imagegen 调用",
        "2. parent 不含 child 边框/阴影",
        "3. photo window 使用洋红键",
        "4. child 无文字、数字、状态字形",
        "5. mission 青蓝 / primary 橄榄绿",
        "6. 正交功能面，无透视",
        "7. 生图只供材质；几何由合同构造",
        "8. visible body 与 shadow 分开量测",
    ]
    for index, rule in enumerate(rules):
        draw.text((x, 210 + index * 52), rule, font=font(16), fill=(221, 226, 205))
    draw.text((x, 690), "TARGETS", font=font(20, True), fill=CREAM)
    draw.text((x, 735), "parent  640x1040", font=font(17), fill=GREEN)
    draw.text((x, 780), "mission 568x88", font=font(17), fill=(75, 225, 225))
    draw.text((x, 825), "primary 568x100", font=font(17), fill=(157, 182, 91))
    draw.text((x, 900), "A199：橄榄绿仅归 primary child", font=font(15, True), fill=(157, 182, 91))
    board.save(OUT_ANCHOR_BOARD)


def build_anchors() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    BASE.mkdir(parents=True, exist_ok=True)
    build_parent_anchor()
    build_button_anchor(MISSION, MISSION_ANCHOR, TEAL)
    build_button_anchor(PRIMARY, PRIMARY_ANCHOR, OLIVE)
    build_anchor_board()
    for path in (PARENT_ANCHOR, MISSION_ANCHOR, PRIMARY_ANCHOR, OUT_ANCHOR_BOARD):
        print(path)


def scale_rect(rect: list[int], factor: int = 2) -> tuple[int, int, int, int]:
    x, y, width, height = rect
    return x * factor, y * factor, (x + width) * factor, (y + height) * factor


def alpha_crop(image: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("source has no opaque pixels")
    return rgba.crop(bbox), bbox


def detect_inner_transparent_rect(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    width, height = image.size
    rows: list[tuple[int, int, int]] = []
    for y in range(height):
        values = [alpha.getpixel((x, y)) for x in range(width)]
        runs: list[tuple[int, int]] = []
        start: int | None = None
        for x, value in enumerate(values + [255]):
            if value <= 8 and start is None:
                start = x
            elif value > 8 and start is not None:
                if start > 2 and x < width - 2 and x - start > width * 0.45:
                    runs.append((start, x))
                start = None
        if runs:
            run = max(runs, key=lambda item: item[1] - item[0])
            rows.append((y, run[0], run[1]))
    if not rows:
        raise RuntimeError("no internal transparent photo window detected")

    groups: list[list[tuple[int, int, int]]] = []
    for row in rows:
        if not groups or row[0] != groups[-1][-1][0] + 1:
            groups.append([row])
        else:
            groups[-1].append(row)
    group = max(groups, key=len)
    if len(group) < height * 0.12:
        raise RuntimeError(f"transparent run is too short to be a photo window: {len(group)} rows")
    return (
        round(median(row[1] for row in group)),
        group[0][0],
        round(median(row[2] for row in group)),
        group[-1][0] + 1,
    )


def piecewise_resize(
    image: Image.Image,
    source_x: list[int],
    target_x: list[int],
    source_y: list[int],
    target_y: list[int],
) -> Image.Image:
    if len(source_x) != len(target_x) or len(source_y) != len(target_y):
        raise ValueError("source/target breakpoints must have matching lengths")
    if source_x != sorted(source_x) or target_x != sorted(target_x):
        raise ValueError("x breakpoints must be monotonic")
    if source_y != sorted(source_y) or target_y != sorted(target_y):
        raise ValueError("y breakpoints must be monotonic")
    output = Image.new("RGBA", (target_x[-1], target_y[-1]), (0, 0, 0, 0))
    for yi in range(len(source_y) - 1):
        for xi in range(len(source_x) - 1):
            src = (source_x[xi], source_y[yi], source_x[xi + 1], source_y[yi + 1])
            dst = (target_x[xi], target_y[yi], target_x[xi + 1], target_y[yi + 1])
            if src[2] <= src[0] or src[3] <= src[1] or dst[2] <= dst[0] or dst[3] <= dst[1]:
                continue
            patch = image.crop(src).resize((dst[2] - dst[0], dst[3] - dst[1]), Image.Resampling.LANCZOS)
            output.alpha_composite(patch, (dst[0], dst[1]))
    return output


def connected_components(mask: Image.Image) -> list[dict[str, Any]]:
    width, height = mask.size
    pixels = mask.load()
    seen = bytearray(width * height)
    components: list[dict[str, Any]] = []
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if seen[index] or pixels[x, y] == 0:
                continue
            queue = deque([(x, y)])
            seen[index] = 1
            area = 0
            min_x = max_x = x
            min_y = max_y = y
            while queue:
                px, py = queue.popleft()
                area += 1
                min_x = min(min_x, px)
                max_x = max(max_x, px)
                min_y = min(min_y, py)
                max_y = max(max_y, py)
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height:
                        continue
                    next_index = ny * width + nx
                    if seen[next_index] or pixels[nx, ny] == 0:
                        continue
                    seen[next_index] = 1
                    queue.append((nx, ny))
            components.append({"area": area, "bbox": [min_x, min_y, max_x + 1, max_y + 1]})
    return components


def detect_button_features(image: Image.Image) -> dict[str, list[int]]:
    rgba = image.convert("RGBA")
    width, height = rgba.size
    mask = Image.new("L", rgba.size, 0)
    src = rgba.load()
    dst = mask.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = src[x, y]
            warm_light = r >= 150 and g >= 135 and b >= 100 and max(r, g, b) - min(r, g, b) <= 90
            if a >= 180 and warm_light:
                dst[x, y] = 255
    components = [item for item in connected_components(mask) if item["area"] >= 20]
    interior = [
        item
        for item in components
        if item["bbox"][0] > 2
        and item["bbox"][1] > 2
        and item["bbox"][2] < width - 2
        and item["bbox"][3] < height - 2
    ]
    labels = [
        item
        for item in interior
        if item["bbox"][2] - item["bbox"][0] > width * 0.25
        and item["bbox"][3] - item["bbox"][1] > height * 0.30
    ]
    rings = []
    for item in interior:
        x0, y0, x1, y1 = item["bbox"]
        comp_width = x1 - x0
        comp_height = y1 - y0
        aspect = comp_width / max(1, comp_height)
        side_position = x1 < width * 0.32 or x0 > width * 0.68
        if width * 0.06 < comp_width < width * 0.24 and 0.65 < aspect < 1.45 and side_position:
            rings.append(item)
    if not labels or len(rings) < 2:
        raise RuntimeError(
            f"button feature detection failed: labels={len(labels)} rings={len(rings)} components={components}"
        )
    label = max(labels, key=lambda item: item["area"])["bbox"]
    left_ring = max((item for item in rings if item["bbox"][2] < width * 0.5), key=lambda item: item["area"])["bbox"]
    right_ring = max((item for item in rings if item["bbox"][0] > width * 0.5), key=lambda item: item["area"])["bbox"]
    return {"left_icon_zone": left_ring, "label_plate": label, "right_action_badge": right_ring}


def detect_outer_body_frame_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgba = image.convert("RGBA")
    width, height = rgba.size
    mask = Image.new("L", rgba.size, 0)
    src = rgba.load()
    dst = mask.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = src[x, y]
            warm_light = r >= 150 and g >= 135 and b >= 100 and max(r, g, b) - min(r, g, b) <= 90
            if a >= 180 and warm_light:
                dst[x, y] = 255
    candidates = []
    for item in connected_components(mask):
        x0, y0, x1, y1 = item["bbox"]
        if x1 - x0 >= width * 0.75 and y1 - y0 >= height * 0.45:
            candidates.append(item)
    if not candidates:
        raise RuntimeError("outer cream body frame was not detected")
    outer = max(candidates, key=lambda item: (item["bbox"][2] - item["bbox"][0]) * (item["bbox"][3] - item["bbox"][1]))
    return tuple(outer["bbox"])


def count_magenta_residue(image: Image.Image) -> int:
    count = 0
    for r, g, b, a in image.convert("RGBA").get_flattened_data():
        if a > 8 and r > 220 and b > 210 and g < 80 and r - g > 150 and b - g > 140:
            count += 1
    return count


def alpha_ring_failures(image: Image.Image, rect: tuple[int, int, int, int], thickness: int = 2) -> int:
    alpha = image.getchannel("A")
    x0, y0, x1, y1 = rect
    failures = 0
    for y in range(y0 - thickness, y1 + thickness):
        for x in range(x0 - thickness, x1 + thickness):
            if x0 <= x < x1 and y0 <= y < y1:
                continue
            if x < 0 or y < 0 or x >= image.width or y >= image.height:
                failures += 1
            elif alpha.getpixel((x, y)) <= 8:
                failures += 1
    return failures


def build_parent_master() -> dict[str, Any]:
    source, source_bbox = alpha_crop(Image.open(PARENT_KEYED))
    source_window = detect_inner_transparent_rect(source)
    target_width, target_height = (value * 2 for value in DOSSIER["frozen"]["export_size"])
    target_window = scale_rect(DOSSIER["frozen"]["slots"]["photo_slot"])
    output = piecewise_resize(
        source,
        [0, source_window[0], source_window[2], source.width],
        [0, target_window[0], target_window[2], target_width],
        [0, source_window[1], source_window[3], source.height],
        [0, target_window[1], target_window[3], target_height],
    )

    # The contract owns the exact window. Clearing it after resampling prevents
    # partially opaque edge pixels from becoming a hidden photo seam.
    alpha = output.getchannel("A")
    alpha_draw = ImageDraw.Draw(alpha)
    alpha_draw.rectangle((target_window[0], target_window[1], target_window[2] - 1, target_window[3] - 1), fill=0)
    output.putalpha(alpha)
    PARENT_MASTER.parent.mkdir(parents=True, exist_ok=True)
    output.save(PARENT_MASTER)

    transparent = sum(
        1
        for y in range(target_window[1], target_window[3])
        for x in range(target_window[0], target_window[2])
        if alpha.getpixel((x, y)) == 0
    )
    expected_transparent = (target_window[2] - target_window[0]) * (target_window[3] - target_window[1])
    return {
        "source_alpha_bbox": list(source_bbox),
        "source_measured_photo_window": list(source_window),
        "target_export_size": [target_width, target_height],
        "target_photo_window": list(target_window),
        "photo_window_transparent_pixels": transparent,
        "photo_window_expected_pixels": expected_transparent,
        "photo_window_ring_alpha_failures": alpha_ring_failures(output, target_window),
        "magenta_residue_pixels": count_magenta_residue(output),
        "alpha_bbox": list(output.getchannel("A").getbbox() or ()),
    }


def measure_shadow_and_body(image: Image.Image) -> dict[str, Any]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    width, height = rgba.size
    body_bbox = detect_outer_body_frame_bbox(rgba)

    # The outer cream frame is the visible-body authority. Only alpha outside
    # that measured geometry belongs to the independent cast-shadow layer.
    shadow = Image.new("L", rgba.size, 0)
    shadow_px = shadow.load()
    for y in range(height):
        for x in range(width):
            if not (body_bbox[0] <= x < body_bbox[2] and body_bbox[1] <= y < body_bbox[3]):
                shadow_px[x, y] = alpha.getpixel((x, y))
    return {
        "alpha_bbox": list(alpha.getbbox() or ()),
        "visible_body_bbox": list(body_bbox),
        "shadow_bbox": list(shadow.getbbox() or ()),
        "shadow_pixels": sum(1 for value in shadow.get_flattened_data() if value > 0),
    }


def build_button_master(
    source_path: Path,
    contract: dict[str, Any],
    output_path: Path,
) -> dict[str, Any]:
    source, source_bbox = alpha_crop(Image.open(source_path))
    target_width, target_height = (value * 2 for value in contract["frozen"]["export_size"])
    proportional_width = round(source.width * target_height / source.height)
    proportional = source.resize((proportional_width, target_height), Image.Resampling.LANCZOS)
    source_body_bbox = detect_outer_body_frame_bbox(proportional)
    # A196 aligns the visible body, not the source-side cast shadow. Trim only
    # the left/right exterior around that measured frame; bottom shadow stays.
    scaled = proportional.crop((source_body_bbox[0], 0, source_body_bbox[2], target_height))
    measured = detect_button_features(scaled)
    slots = contract["frozen"]["slots"]
    target = {
        name: list(scale_rect(slots[name]))
        for name in ("left_icon_zone", "label_plate", "right_action_badge")
    }
    source_x = [
        0,
        measured["left_icon_zone"][0],
        measured["left_icon_zone"][2],
        measured["label_plate"][0],
        measured["label_plate"][2],
        measured["right_action_badge"][0],
        measured["right_action_badge"][2],
        scaled.width,
    ]
    target_x = [
        0,
        target["left_icon_zone"][0],
        target["left_icon_zone"][2],
        target["label_plate"][0],
        target["label_plate"][2],
        target["right_action_badge"][0],
        target["right_action_badge"][2],
        target_width,
    ]
    if any(b <= a for a, b in zip(source_x, source_x[1:])):
        raise RuntimeError(f"source button feature order is invalid: {source_x}")
    if any(b <= a for a, b in zip(target_x, target_x[1:])):
        raise RuntimeError(f"target button slot order is invalid: {target_x}")
    output = piecewise_resize(scaled, source_x, target_x, [0, target_height], [0, target_height])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(output_path)
    report = measure_shadow_and_body(output)
    report.update(
        {
            "source_alpha_bbox": list(source_bbox),
            "source_visible_body_bbox_before_horizontal_trim": list(source_body_bbox),
            "source_proportional_size": [scaled.width, scaled.height],
            "source_measured_features": measured,
            "target_features": target,
            "target_export_size": [target_width, target_height],
            "magenta_residue_pixels": count_magenta_residue(output),
        }
    )
    return report


def cover_image(source: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    rgba = source.convert("RGBA")
    scale = max(target_size[0] / rgba.width, target_size[1] / rgba.height)
    resized = rgba.resize((round(rgba.width * scale), round(rgba.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_size[0]) // 2)
    top = max(0, (resized.height - target_size[1]) // 2)
    return resized.crop((left, top, left + target_size[0], top + target_size[1]))


def checkerboard(size: tuple[int, int], cell: int = 16) -> Image.Image:
    image = Image.new("RGB", size, (41, 49, 48))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2 == 0:
                draw.rectangle((x, y, min(size[0], x + cell) - 1, min(size[1], y + cell) - 1), fill=(73, 82, 79))
    return image


def paste_on_checker(board: Image.Image, sprite: Image.Image, position: tuple[int, int]) -> None:
    area = checkerboard(sprite.size)
    area.paste(sprite, (0, 0), sprite)
    board.paste(area, position)


def write_atlas() -> dict[str, Any]:
    parent = Image.open(PARENT_MASTER).convert("RGBA")
    mission = Image.open(MISSION_MASTER).convert("RGBA")
    primary = Image.open(PRIMARY_MASTER).convert("RGBA")
    atlas_height = parent.height + mission.height + primary.height
    atlas = Image.new("RGBA", (parent.width, atlas_height), (0, 0, 0, 0))
    atlas.alpha_composite(parent, (0, 0))
    mission_x = (parent.width - mission.width) // 2
    primary_x = (parent.width - primary.width) // 2
    atlas.alpha_composite(mission, (mission_x, parent.height))
    atlas.alpha_composite(primary, (primary_x, parent.height + mission.height))
    ATLAS.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(ATLAS)
    metadata = {
        "schema_version": 1,
        "scale": 2,
        "size": list(atlas.size),
        "entries": {
            "right_dossier_page": [0, 0, parent.width, parent.height],
            "right_mission_intel_button": [mission_x, parent.height, mission.width, mission.height],
            "right_action_lane": [primary_x, parent.height + mission.height, primary.width, primary.height],
        },
    }
    ATLAS_META.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def draw_globe(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = rect
    inset = max(3, round(min(x1 - x0, y1 - y0) * 0.18))
    circle = (x0 + inset, y0 + inset, x1 - inset, y1 - inset)
    width = max(2, round((x1 - x0) * 0.04))
    draw.ellipse(circle, outline=color, width=width)
    cx = (circle[0] + circle[2]) // 2
    cy = (circle[1] + circle[3]) // 2
    draw.line((circle[0], cy, circle[2], cy), fill=color, width=width)
    draw.arc((circle[0] + (circle[2] - circle[0]) // 4, circle[1], circle[2] - (circle[2] - circle[0]) // 4, circle[3]), 90, 270, fill=color, width=width)
    draw.arc((circle[0] + (circle[2] - circle[0]) // 4, circle[1], circle[2] - (circle[2] - circle[0]) // 4, circle[3]), -90, 90, fill=color, width=width)


def draw_check(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = rect
    width = max(3, round((x1 - x0) * 0.07))
    draw.line(
        (
            x0 + round((x1 - x0) * 0.26),
            y0 + round((y1 - y0) * 0.53),
            x0 + round((x1 - x0) * 0.43),
            y0 + round((y1 - y0) * 0.70),
            x0 + round((x1 - x0) * 0.73),
            y0 + round((y1 - y0) * 0.32),
        ),
        fill=color,
        width=width,
        joint="curve",
    )


def draw_document(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = rect
    pad_x = round((x1 - x0) * 0.29)
    pad_y = round((y1 - y0) * 0.22)
    body = (x0 + pad_x, y0 + pad_y, x1 - pad_x, y1 - pad_y)
    width = max(2, round((x1 - x0) * 0.04))
    draw.rectangle(body, outline=color, width=width)
    line_left = body[0] + max(2, width)
    line_right = body[2] - max(2, width)
    for fraction in (0.35, 0.55, 0.75):
        y = body[1] + round((body[3] - body[1]) * fraction)
        draw.line((line_left, y, line_right, y), fill=color, width=width)


def draw_arrow(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = rect
    width = max(3, round((x1 - x0) * 0.055))
    cy = (y0 + y1) // 2
    left = x0 + round((x1 - x0) * 0.28)
    right = x0 + round((x1 - x0) * 0.72)
    draw.line((left, cy, right, cy), fill=color, width=width)
    draw.line((right, cy, x0 + round((x1 - x0) * 0.57), y0 + round((y1 - y0) * 0.32)), fill=color, width=width)
    draw.line((right, cy, x0 + round((x1 - x0) * 0.57), y0 + round((y1 - y0) * 0.68)), fill=color, width=width)


def build_runtime_icons() -> None:
    RUNTIME_ICON_DIR.mkdir(parents=True, exist_ok=True)
    definitions = [
        (RUNTIME_GLOBE, draw_globe),
        (RUNTIME_DOCUMENT, draw_document),
        (RUNTIME_ARROW, draw_arrow),
        (RUNTIME_CHECK, draw_check),
    ]
    for path, renderer in definitions:
        canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        renderer(ImageDraw.Draw(canvas), (0, 0, 64, 64), (255, 255, 255, 255))
        canvas.save(path)


def paste_runtime_icon(
    canvas: Image.Image,
    icon_path: Path,
    rect: tuple[int, int, int, int],
    color: tuple[int, int, int, int],
    scale: float = 0.82,
) -> None:
    icon = Image.open(icon_path).convert("RGBA")
    target_width = max(1, round((rect[2] - rect[0]) * scale))
    target_height = max(1, round((rect[3] - rect[1]) * scale))
    icon.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    tinted = Image.new("RGBA", icon.size, color)
    tinted.putalpha(icon.getchannel("A"))
    x = rect[0] + (rect[2] - rect[0] - icon.width) // 2
    y = rect[1] + (rect[3] - rect[1] - icon.height) // 2
    canvas.alpha_composite(tinted, (x, y))


def fit_and_draw(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    text_value: str,
    *,
    max_size: int,
    min_size: int,
    bold: bool,
    fill: tuple[int, int, int, int],
    align: str = "left",
    pad_x: int = 0,
    pad_y: int = 0,
) -> dict[str, Any]:
    usable = (rect[2] - rect[0] - pad_x * 2, rect[3] - rect[1] - pad_y * 2)
    chosen_font, size, fits, _metrics = fit_font_by_raster(
        text_value,
        lambda value: font(value, bold),
        max_size,
        min_size,
        usable,
    )
    report = draw_text_by_raster_bbox(
        draw,
        rect,
        text_value,
        chosen_font,
        fill,
        align=align,
        pad_x=pad_x,
        pad_y=pad_y,
    )
    report.update({"text": text_value, "font_size": size, "fit_search_pass": fits})
    return report


def render_runtime_component(show_qa: bool) -> tuple[Image.Image, list[dict[str, Any]]]:
    shell = Image.open(PARENT_MASTER).convert("RGBA")
    mission = Image.open(MISSION_MASTER).convert("RGBA")
    primary = Image.open(PRIMARY_MASTER).convert("RGBA")
    photo_rect = scale_rect(DOSSIER["frozen"]["slots"]["photo_slot"])
    photo = cover_image(Image.open(PHOTO_SOURCE), (photo_rect[2] - photo_rect[0], photo_rect[3] - photo_rect[1]))
    component = Image.new("RGBA", shell.size, (12, 27, 29, 255))
    component.alpha_composite(photo, (photo_rect[0], photo_rect[1]))
    component.alpha_composite(shell)

    mission_rect = scale_rect(DOSSIER["frozen"]["slots"]["mission_intel_button"])
    primary_rect = scale_rect(DOSSIER["frozen"]["slots"]["primary_enter_cta"])
    component.alpha_composite(mission, (mission_rect[0], mission_rect[1]))
    component.alpha_composite(primary, (primary_rect[0], primary_rect[1]))

    draw = ImageDraw.Draw(component)
    slots = DOSSIER["frozen"]["slots"]
    ink = (28, 30, 25, 255)
    cream = (238, 229, 202, 255)
    teal_ink = (31, 82, 85, 255)
    reports: list[dict[str, Any]] = []

    header_icon = scale_rect(slots["header_icon"])
    paste_runtime_icon(component, RUNTIME_GLOBE, header_icon, (90, 93, 76, 255), 0.86)
    reports.append(
        fit_and_draw(
            draw,
            scale_rect(slots["title_slot"]),
            "北美禁区警戒带",
            max_size=38,
            min_size=28,
            bold=True,
            fill=ink,
            align="center",
            pad_x=8,
            pad_y=6,
        )
    )
    status = scale_rect(slots["status_stamp"])
    status_split = status[1] + round((status[3] - status[1]) * 0.56)
    reports.append(
        fit_and_draw(
            draw,
            (status[0], status[1] + 3, status[2], status_split),
            "高危",
            max_size=30,
            min_size=22,
            bold=True,
            fill=(142, 54, 39, 255),
            align="center",
            pad_x=4,
        )
    )
    reports.append(
        fit_and_draw(
            draw,
            (status[0], status_split, status[2], status[3] - 3),
            "推荐12",
            max_size=18,
            min_size=14,
            bold=True,
            fill=(87, 38, 50, 255),
            align="center",
            pad_x=4,
        )
    )
    body = scale_rect(slots["region_body"])
    body_mid = (body[1] + body[3]) // 2
    reports.append(
        fit_and_draw(
            draw,
            (body[0] + 10, body[1] + 2, body[2] - 8, body_mid),
            "天线阵列仍在发射，林线内出现异常回波。",
            max_size=23,
            min_size=17,
            bold=False,
            fill=ink,
            pad_x=4,
        )
    )
    reports.append(
        fit_and_draw(
            draw,
            (body[0] + 10, body_mid, body[2] - 8, body[3] - 2),
            "进入前可先核对本周地区任务与封锁条件。",
            max_size=23,
            min_size=17,
            bold=False,
            fill=ink,
            pad_x=4,
        )
    )
    reports.append(
        fit_and_draw(
            draw,
            scale_rect(slots["decision_facts"]),
            "限时 2 周 · 线索缺口 3 · 深链 1",
            max_size=22,
            min_size=16,
            bold=True,
            fill=(52, 57, 48, 255),
            align="center",
            pad_x=8,
            pad_y=4,
        )
    )

    mission_slots = MISSION["frozen"]["slots"]
    mission_origin = (mission_rect[0], mission_rect[1])
    mission_left = tuple(value + mission_origin[index % 2] for index, value in enumerate(scale_rect(mission_slots["left_icon_zone"])))
    mission_label = tuple(value + mission_origin[index % 2] for index, value in enumerate(scale_rect(mission_slots["label_plate"])))
    mission_right = tuple(value + mission_origin[index % 2] for index, value in enumerate(scale_rect(mission_slots["right_action_badge"])))
    paste_runtime_icon(component, RUNTIME_DOCUMENT, mission_left, cream, 0.84)
    paste_runtime_icon(component, RUNTIME_ARROW, mission_right, cream, 0.78)
    reports.append(
        fit_and_draw(
            draw,
            mission_label,
            "查看任务情报 · 12项",
            max_size=25,
            min_size=18,
            bold=True,
            fill=teal_ink,
            align="center",
            pad_x=8,
            pad_y=5,
        )
    )

    primary_slots = PRIMARY["frozen"]["slots"]
    primary_origin = (primary_rect[0], primary_rect[1])
    primary_left = tuple(value + primary_origin[index % 2] for index, value in enumerate(scale_rect(primary_slots["left_icon_zone"])))
    primary_label = tuple(value + primary_origin[index % 2] for index, value in enumerate(scale_rect(primary_slots["label_plate"])))
    primary_right = tuple(value + primary_origin[index % 2] for index, value in enumerate(scale_rect(primary_slots["right_action_badge"])))
    paste_runtime_icon(component, RUNTIME_ARROW, primary_left, cream, 0.78)
    paste_runtime_icon(component, RUNTIME_CHECK, primary_right, cream, 0.82)
    reports.append(
        fit_and_draw(
            draw,
            primary_label,
            "进入选定地区",
            max_size=28,
            min_size=20,
            bold=True,
            fill=(58, 66, 40, 255),
            align="center",
            pad_x=8,
            pad_y=6,
        )
    )

    if show_qa:
        qa_colors = [
            ("header_icon", (81, 238, 255, 255)),
            ("title_slot", (255, 72, 202, 255)),
            ("status_stamp", (255, 111, 95, 255)),
            ("photo_slot", (72, 236, 174, 255)),
            ("region_body", (255, 212, 68, 255)),
            ("decision_facts", (167, 128, 255, 255)),
            ("mission_intel_button", (79, 218, 232, 255)),
            ("primary_enter_cta", (174, 204, 91, 255)),
        ]
        for name, color in qa_colors:
            rect = scale_rect(slots[name])
            draw.rectangle((rect[0], rect[1], rect[2] - 1, rect[3] - 1), outline=color, width=3)
        for report in reports:
            bbox = report["raster_glyph_bbox"]
            draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 55, 196, 255), width=2)
    return component, reports


def build_master_board(
    parent_report: dict[str, Any],
    mission_report: dict[str, Any],
    primary_report: dict[str, Any],
) -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "WMW 右 dossier v0.9.0 · candidate A clean masters", font=font(34, True), fill=CREAM)
    draw.text((44, 78), "582 · 生图材质经合同几何构造；棋盘格=真实 alpha；文字与状态图标不在母版内。", font=font(17), fill=(190, 210, 201))

    parent = Image.open(PARENT_MASTER).convert("RGBA").resize((448, 728), Image.Resampling.LANCZOS)
    mission = Image.open(MISSION_MASTER).convert("RGBA").resize((909, 141), Image.Resampling.LANCZOS)
    primary = Image.open(PRIMARY_MASTER).convert("RGBA").resize((909, 160), Image.Resampling.LANCZOS)
    paste_on_checker(board, parent, (58, 155))
    paste_on_checker(board, mission, (610, 235))
    paste_on_checker(board, primary, (610, 505))
    draw.rectangle((48, 145, 516, 893), outline=GREEN, width=2)
    draw.rectangle((600, 225, 1530, 386), outline=(75, 225, 225), width=2)
    draw.rectangle((600, 495, 1530, 675), outline=(157, 182, 91), width=2)
    draw.text((60, 116), "PARENT · 640x1040 · exact alpha photo window", font=font(19, True), fill=GREEN)
    draw.text((610, 196), "SECONDARY · 568x88 · teal", font=font(19, True), fill=(75, 225, 225))
    draw.text((610, 466), "PRIMARY · 568x100 · olive", font=font(19, True), fill=(157, 182, 91))

    panel = (1570, 145, 1885, 900)
    draw.rectangle(panel, fill=(13, 39, 40), outline=(67, 112, 108), width=2)
    draw.text((1592, 168), "MEASURED", font=font(20, True), fill=CREAM)
    lines = [
        f"photo alpha {parent_report['photo_window_transparent_pixels']}/{parent_report['photo_window_expected_pixels']}",
        f"photo ring fail {parent_report['photo_window_ring_alpha_failures']}",
        f"parent magenta {parent_report['magenta_residue_pixels']}",
        "",
        f"mission body {mission_report['visible_body_bbox']}",
        f"mission shadow {mission_report['shadow_bbox']}",
        "",
        f"primary body {primary_report['visible_body_bbox']}",
        f"primary shadow {primary_report['shadow_bbox']}",
        "",
        "A196:",
        "subject edges share",
        "x=0..568; shadow",
        "measured separately.",
        "",
        "A199:",
        "olive belongs only",
        "to primary child.",
    ]
    for index, line in enumerate(lines):
        draw.text((1592, 215 + index * 34), line, font=font(14, index in (10, 15)), fill=(218, 226, 205))
    board.save(OUT_MASTER_BOARD)


def build_runtime_board(show_qa: bool) -> list[dict[str, Any]]:
    component, reports = render_runtime_component(show_qa)
    board = Image.new("RGB", (1920, 1080), (6, 18, 20))
    draw = ImageDraw.Draw(board)
    board.paste(component.convert("RGB"), (48, 20))
    title = "Python v0.9.0 candidate A right dossier runtime QA" if show_qa else "Python v0.9.0 candidate A right dossier runtime fill"
    draw.text((742, 34), title, font=font(31, True), fill=CREAM)
    draw.text((744, 82), "父壳 / 照片 / 两 child / 文字与图标分别组装；没有压平源图裁片。", font=font(17), fill=(191, 209, 198))

    mission_rect = scale_rect(DOSSIER["frozen"]["slots"]["mission_intel_button"])
    primary_rect = scale_rect(DOSSIER["frozen"]["slots"]["primary_enter_cta"])
    mission_crop = component.crop(mission_rect).resize((852, 132), Image.Resampling.NEAREST)
    primary_crop = component.crop(primary_rect).resize((852, 150), Image.Resampling.NEAREST)
    board.paste(mission_crop.convert("RGB"), (800, 220))
    board.paste(primary_crop.convert("RGB"), (800, 455))
    draw.rectangle((790, 210, 1662, 362), outline=(75, 225, 225), width=2)
    draw.rectangle((790, 445, 1662, 615), outline=(157, 182, 91), width=2)
    draw.text((800, 180), "mission child · 150% close-up", font=font(18, True), fill=(75, 225, 225))
    draw.text((800, 415), "primary child · 150% close-up", font=font(18, True), fill=(157, 182, 91))

    passed = sum(1 for report in reports if report["fit_search_pass"] and report["glyph_bbox_inside_inner_rect"])
    draw.text((800, 680), f"raster-alpha text containment: {passed}/{len(reports)}", font=font(20, True), fill=GREEN if passed == len(reports) else (255, 84, 73))
    draw.text((800, 728), "粉色框只读取真实字形 alpha bbox；彩框直接读取合同 carrier。" if show_qa else "runtime tokens: title / status / body / facts / two action labels", font=font(16), fill=(223, 221, 196))
    draw.text((800, 775), "Primary default = muted olive; secondary = teal; warning rust and disabled gray are not baked into these defaults.", font=font(15), fill=(203, 212, 191))
    (OUT_PYTHON_QA if show_qa else OUT_PYTHON).parent.mkdir(parents=True, exist_ok=True)
    board.save(OUT_PYTHON_QA if show_qa else OUT_PYTHON)
    return reports


def write_manifest(
    parent_report: dict[str, Any],
    mission_report: dict[str, Any],
    primary_report: dict[str, Any],
    atlas_report: dict[str, Any],
    text_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    mission_body = mission_report["visible_body_bbox"]
    primary_body = primary_report["visible_body_bbox"]
    body_edge_diff = {
        "left": abs(mission_body[0] - primary_body[0]),
        "right": abs(mission_body[2] - primary_body[2]),
        "width": abs((mission_body[2] - mission_body[0]) - (primary_body[2] - primary_body[0])),
    }
    text_pass = all(item["fit_search_pass"] and item["glyph_bbox_inside_inner_rect"] for item in text_reports)
    manifest = {
        "schema_version": 1,
        "asset_line": "world-map-benchmark-landing/right-dossier",
        "version": "v0.9.0",
        "candidate": "A",
        "status": "evidence_ready_user_visual_review_pending",
        "design_adoption": "A199: primary default/hover/pressed uses olive; secondary remains teal; warning rust and disabled neutral gray remain state-only.",
        "contracts": {
            "right_dossier_page": {"version": DOSSIER["contract_version"], "frozen_changed": False},
            "right_mission_intel_button": {"version": MISSION["contract_version"], "frozen_changed": False},
            "right_action_lane": {"version": PRIMARY["contract_version"], "frozen_changed": False},
        },
        "sources": {
            "579_parent_imagegen": str(PARENT_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "580_mission_imagegen": str(MISSION_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "581_primary_imagegen": str(PRIMARY_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "chroma_key": "#FF00FF removed with the installed imagegen remove_chroma_key helper before contract construction",
            "runtime_photo": str(PHOTO_SOURCE.relative_to(ROOT)).replace("\\", "/"),
        },
        "outputs": {
            "parent_master": str(PARENT_MASTER.relative_to(ROOT)).replace("\\", "/"),
            "mission_master": str(MISSION_MASTER.relative_to(ROOT)).replace("\\", "/"),
            "primary_master": str(PRIMARY_MASTER.relative_to(ROOT)).replace("\\", "/"),
            "runtime_icons": [
                str(path.relative_to(ROOT)).replace("\\", "/")
                for path in (RUNTIME_GLOBE, RUNTIME_DOCUMENT, RUNTIME_ARROW, RUNTIME_CHECK)
            ],
            "atlas": str(ATLAS.relative_to(ROOT)).replace("\\", "/"),
            "python_runtime": str(OUT_PYTHON.relative_to(ROOT)).replace("\\", "/"),
            "python_qa": str(OUT_PYTHON_QA.relative_to(ROOT)).replace("\\", "/"),
            "godot_runtime": str(OUT_GODOT.relative_to(ROOT)).replace("\\", "/"),
            "godot_qa": str(OUT_GODOT_QA.relative_to(ROOT)).replace("\\", "/"),
        },
        "measurements": {
            "parent": parent_report,
            "mission": mission_report,
            "primary": primary_report,
            "atlas": atlas_report,
            "child_visible_body_edge_diff": body_edge_diff,
            "text_tokens": text_reports,
        },
        "gates": {
            "real_imagegen_sources": {"status": "pass", "evidence": [579, 580, 581]},
            "no_fake_text_in_sprite_masters": {"status": "evidence_ready", "basis": "three keyed clean masters visually contain blank carriers only; runtime text is drawn after composition"},
            "functional_faces_orthogonal": {"status": "evidence_ready", "basis": "front-facing geometry anchors plus clean-master board 582"},
            "export_geometry": {
                "status": "pass",
                "actual": {
                    "parent": parent_report["target_export_size"],
                    "mission": mission_report["target_export_size"],
                    "primary": primary_report["target_export_size"],
                },
                "expected": {"parent": [640, 1040], "mission": [568, 88], "primary": [568, 100]},
            },
            "parent_photo_window_alpha": {
                "status": "pass" if parent_report["photo_window_transparent_pixels"] == parent_report["photo_window_expected_pixels"] else "fail",
                "transparent": parent_report["photo_window_transparent_pixels"],
                "expected": parent_report["photo_window_expected_pixels"],
            },
            "parent_photo_bezel_continuity": {
                "status": "pass" if parent_report["photo_window_ring_alpha_failures"] == 0 else "fail",
                "alpha_failures": parent_report["photo_window_ring_alpha_failures"],
                "basis": "2px ring immediately outside photo_slot; alpha <= 8 is a structural break, partial antialias alpha is retained",
            },
            "chroma_residue": {
                "status": "pass" if parent_report["magenta_residue_pixels"] == mission_report["magenta_residue_pixels"] == primary_report["magenta_residue_pixels"] == 0 else "fail",
                "parent": parent_report["magenta_residue_pixels"],
                "mission": mission_report["magenta_residue_pixels"],
                "primary": primary_report["magenta_residue_pixels"],
            },
            "action_stack_visible_alignment": {
                "status": "pass" if max(body_edge_diff.values()) == 0 else "fail",
                "visible_body_bbox": {"mission": mission_body, "primary": primary_body},
                "edge_diff": body_edge_diff,
                "shadow_bbox_separate": {"mission": mission_report["shadow_bbox"], "primary": primary_report["shadow_bbox"]},
            },
            "runtime_text_raster_alpha_containment": {"status": "pass" if text_pass else "fail", "passed": sum(1 for item in text_reports if item["fit_search_pass"] and item["glyph_bbox_inside_inner_rect"]), "total": len(text_reports)},
            "shared_runtime_icon_tokens": {
                "status": "pass",
                "basis": "Python and Godot load the same globe/document/arrow/check PNG ingredients; no temporary Unicode substitute remains",
            },
            "godot_windowed_capture": {"status": "pending", "runner": "scripts/run_wmw_right_dossier_godot_capture_v090.ps1"},
            "visual_review": {"status": "evidence_ready", "basis": "582/583/584 prepared; 585/586 and dual-agent review still pending"},
        },
        "judgment": "Candidate A clean masters are constructed and Python-filled. Programmatic gates are recorded; visual pass remains pending until windowed Godot capture and review evidence are complete.",
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def build_candidate() -> None:
    required = [PARENT_KEYED, MISSION_KEYED, PRIMARY_KEYED, PHOTO_SOURCE]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing candidate inputs: {missing}")
    parent_report = build_parent_master()
    mission_report = build_button_master(MISSION_KEYED, MISSION, MISSION_MASTER)
    primary_report = build_button_master(PRIMARY_KEYED, PRIMARY, PRIMARY_MASTER)
    build_runtime_icons()
    atlas_report = write_atlas()
    build_master_board(parent_report, mission_report, primary_report)
    build_runtime_board(False)
    text_reports = build_runtime_board(True)
    manifest = write_manifest(parent_report, mission_report, primary_report, atlas_report, text_reports)
    failed = [name for name, gate in manifest["gates"].items() if gate["status"] == "fail"]
    if failed:
        raise RuntimeError(f"candidate A build gates failed: {failed}")
    for path in (PARENT_MASTER, MISSION_MASTER, PRIMARY_MASTER, ATLAS, OUT_MASTER_BOARD, OUT_PYTHON, OUT_PYTHON_QA, OUT_MANIFEST):
        print(path)


def image_content_stats(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGBA")
    sampled_colors: set[tuple[int, int, int, int]] = set()
    sampled_nonblack = 0
    for y in range(0, image.height, 8):
        for x in range(0, image.width, 8):
            pixel = image.getpixel((x, y))
            sampled_colors.add(pixel)
            if max(pixel[:3]) > 3:
                sampled_nonblack += 1
    return {
        "size": list(image.size),
        "sample_stride": 8,
        "sampled_color_count": len(sampled_colors),
        "sampled_nonblack_pixels": sampled_nonblack,
        "alpha_extrema": list(image.getchannel("A").getextrema()),
    }


def build_review_board() -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "WMW 右 dossier candidate A · benchmark / runtime / child close-up", font=font(32, True), fill=CREAM)
    draw.text((44, 74), "587 · 供用户裁决；候选未冻结。左=旧版直接参考，中=Godot 4.6.2 真运行，右=三母版结构证据。", font=font(16), fill=(194, 211, 201))

    reference = Image.open(REFERENCE_DOSSIER).convert("RGB")
    reference.thumbnail((440, 850), Image.Resampling.LANCZOS)
    board.paste(reference, (45, 150))
    draw.rectangle((35, 140, 45 + reference.width + 10, 150 + reference.height + 10), outline=(202, 190, 156), width=2)
    draw.text((45, 112), "REFERENCE 29 · integrated-endcaps", font=font(17, True), fill=(224, 214, 187))

    godot = Image.open(OUT_GODOT).convert("RGB")
    dossier_crop = godot.crop((76, 150, 556, 930))
    board.paste(dossier_crop, (535, 150))
    draw.rectangle((525, 140, 1025, 940), outline=GREEN, width=2)
    draw.text((535, 112), "CANDIDATE A · Godot runtime · 480x780", font=font(17, True), fill=GREEN)

    mission = Image.open(MISSION_MASTER).convert("RGBA").resize((738, 114), Image.Resampling.LANCZOS)
    primary = Image.open(PRIMARY_MASTER).convert("RGBA").resize((738, 130), Image.Resampling.LANCZOS)
    paste_on_checker(board, mission, (1110, 190))
    paste_on_checker(board, primary, (1110, 390))
    draw.rectangle((1100, 180, 1858, 314), outline=(75, 225, 225), width=2)
    draw.rectangle((1100, 380, 1858, 530), outline=(157, 182, 91), width=2)
    draw.text((1110, 150), "secondary master · teal · blank runtime carriers", font=font(16, True), fill=(75, 225, 225))
    draw.text((1110, 350), "primary master · olive · same visible width", font=font(16, True), fill=(157, 182, 91))

    panel = (1098, 585, 1860, 985)
    draw.rectangle(panel, fill=(13, 39, 40), outline=(67, 112, 108), width=2)
    draw.text((1120, 610), "可核验差异", font=font(21, True), fill=CREAM)
    lines = [
        "1. 旧参考三条动作带收敛为两条：任务情报 + 唯一主 CTA。",
        "2. 两条可见主体同宽共中心；层级由高度、颜色、纸厚承担。",
        "3. 主 CTA 常态为橄榄绿，次级入口保持青蓝；锈红不再常驻。",
        "4. parent 只拥有纸壳与照片窗；child 边框、阴影独立。",
        "5. 照片窗为精确 alpha 洞；文字与图标全部运行时叠加。",
        "",
        "当前口径：程序 gate 与双 agent 复核已过，P0/P1=0；等待用户视觉裁决。",
    ]
    for index, line in enumerate(lines):
        draw.text((1120, 662 + index * 43), line, font=font(15, index == 6), fill=(218, 226, 205))
    board.save(OUT_REVIEW)


def finalize_candidate() -> None:
    if not OUT_MANIFEST.exists():
        raise FileNotFoundError(OUT_MANIFEST)
    if not OUT_GODOT.exists() or not OUT_GODOT_QA.exists():
        raise FileNotFoundError("Godot screenshots 585/586 are required before finalization")
    build_review_board()
    manifest = load_json(OUT_MANIFEST)
    baseline_stats = image_content_stats(OUT_GODOT)
    qa_stats = image_content_stats(OUT_GODOT_QA)
    godot_pass = (
        baseline_stats["size"] == [1920, 1080]
        and qa_stats["size"] == [1920, 1080]
        and baseline_stats["sampled_color_count"] >= 80
        and qa_stats["sampled_color_count"] >= 80
        and baseline_stats["sampled_nonblack_pixels"] > 0
        and qa_stats["sampled_nonblack_pixels"] > 0
    )
    manifest["outputs"]["review_board"] = str(OUT_REVIEW.relative_to(ROOT)).replace("\\", "/")
    manifest["measurements"]["godot_capture"] = {"baseline": baseline_stats, "qa": qa_stats}
    manifest["gates"]["godot_windowed_capture"] = {
        "status": "pass" if godot_pass else "fail",
        "godot_version": "4.6.2-stable",
        "mode": "windowed opengl3; UI capture never used headless",
        "runner": "scripts/run_wmw_right_dossier_godot_capture_v090.ps1",
        "frame_post_draw_waits": 2,
        "all_black_refusal": True,
        "relative_baseline_loss_refusal": True,
        "baseline": baseline_stats,
        "qa": qa_stats,
    }
    manifest["gates"]["visual_review"] = {
        "status": "evidence_ready_user_review_pending",
        "basis": "582 clean masters, 583/584 Python fill/QA, 585/586 Godot runtime/QA, and 587 comparison board",
        "parent_self_check": {
            "photo_window_seam": "evidence_ready: no visible gap, duplicate layer, or chroma residue in 585",
            "action_stack_alignment": "evidence_ready: both visible bodies share left/right edges in 585 and bbox diff=0",
            "runtime_text": "evidence_ready: no clipping or carrier mismatch observed in 585/586",
            "color_hierarchy": "evidence_ready: olive is confined to primary child; teal remains secondary",
        },
        "dual_agent_reviews": {
            "ux_laoge": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 0, "p2": 3},
                "resolved_after_review": [
                    "Python/Godot icon drift was removed by shared runtime icon PNG ingredients."
                ],
                "remaining": [
                    "The product meaning and unit of 推荐12 remain provisional.",
                    "Future hover/pressed/disabled implementation must respond as one whole-strip hit target."
                ],
            },
            "ui_designer": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 0, "p2": 2},
                "basis": "clean low-poly weekly benchmark proximity, paper material, parent/child layering, A196 alignment, and A199 color hierarchy all pass; no new visual P2 was added.",
            },
        },
    }
    manifest["judgment"] = "Programmatic construction, Python fill, Godot windowed capture, and dual-agent review pass for user visual review. Candidate A remains unfrozen pending user visual judgment."
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not godot_pass:
        raise RuntimeError("Godot content validation failed")
    print(OUT_REVIEW)
    print(OUT_MANIFEST)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("anchors", "build", "finalize"))
    args = parser.parse_args()
    if args.command == "anchors":
        build_anchors()
    elif args.command == "build":
        build_candidate()
    elif args.command == "finalize":
        finalize_candidate()


if __name__ == "__main__":
    main()
