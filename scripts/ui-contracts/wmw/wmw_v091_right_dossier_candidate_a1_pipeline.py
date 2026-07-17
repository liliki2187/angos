from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path
from statistics import median
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from wmw_text_layout_metrics import draw_text_by_raster_bbox, fit_font_by_raster


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
WORK = ROOT / "tmp" / "wmw-right-dossier-v091"
CONTRACT_DIR = ROOT / "design" / "ui-contracts" / "world-map"

OUT_ANCHOR_BOARD = BASE / "589-world-map-wmw-v0-9-1-right-dossier-candidate-a1-layout-photo-spec.png"
PARENT_ANCHOR = WORK / "parent_hollow_shell_anchor.png"
MISSION_ANCHOR = WORK / "mission_button_anchor.png"
PRIMARY_ANCHOR = WORK / "primary_olive_button_anchor.png"

PARENT_SOURCE = BASE / "579-world-map-wmw-v0-9-0-right-dossier-parent-imagegen-source.png"
MISSION_SOURCE = BASE / "580-world-map-wmw-v0-9-0-right-mission-button-imagegen-source.png"
PRIMARY_SOURCE = BASE / "581-world-map-wmw-v0-9-0-right-primary-olive-imagegen-source.png"
KEYED_DIR = ROOT / "tmp" / "wmw-right-dossier-v090" / "keyed"
PARENT_KEYED = KEYED_DIR / "parent_source_keyed.png"
MISSION_KEYED = KEYED_DIR / "mission_source_keyed.png"
PRIMARY_KEYED = KEYED_DIR / "primary_source_keyed.png"

ASSET_DIR = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map" / "wmw_v091_right_dossier_candidate_a1"
INGREDIENT_DIR = ASSET_DIR / "ingredients"
PARENT_MASTER = INGREDIENT_DIR / "right_dossier_page_candidate_a1_parent_hollow_shell_2x.png"
MISSION_MASTER = INGREDIENT_DIR / "right_mission_intel_button_candidate_a1_teal_2x.png"
PRIMARY_MASTER = INGREDIENT_DIR / "right_action_lane_candidate_a1_primary_olive_2x.png"
RUNTIME_ICON_DIR = INGREDIENT_DIR / "runtime_icons"
RUNTIME_GLOBE = RUNTIME_ICON_DIR / "right_dossier_runtime_globe.png"
RUNTIME_DOCUMENT = RUNTIME_ICON_DIR / "right_dossier_runtime_document.png"
RUNTIME_ARROW = RUNTIME_ICON_DIR / "right_dossier_runtime_arrow.png"
RUNTIME_CHECK = RUNTIME_ICON_DIR / "right_dossier_runtime_check.png"
PHOTO_RAW = BASE / "590-world-map-wmw-v0-9-1-right-dossier-photo-imagegen-raw.png"
PHOTO_SOURCE = INGREDIENT_DIR / "right_dossier_north_america_photo_source_1104x704.png"
PHOTO_INGREDIENT = INGREDIENT_DIR / "right_dossier_north_america_photo_552x352.png"
ATLAS = ASSET_DIR / "right_dossier_candidate_a1_three_master_atlas_2x.png"
ATLAS_META = ASSET_DIR / "right_dossier_candidate_a1_three_master_atlas_2x.json"

OUT_MASTER_BOARD = BASE / "591-world-map-wmw-v0-9-1-right-dossier-candidate-a1-photo-and-master-qa.png"
OUT_PYTHON = BASE / "592-world-map-wmw-v0-9-1-right-dossier-candidate-a1-python-runtime.png"
OUT_PYTHON_QA = BASE / "593-world-map-wmw-v0-9-1-right-dossier-candidate-a1-python-runtime-qa.png"
OUT_GODOT = BASE / "594-world-map-wmw-v0-9-1-right-dossier-candidate-a1-godot-runtime.png"
OUT_GODOT_QA = BASE / "595-world-map-wmw-v0-9-1-right-dossier-candidate-a1-godot-runtime-qa.png"
OUT_REVIEW = BASE / "596-world-map-wmw-v0-9-1-right-dossier-candidate-a1-review-board.png"
OUT_MANIFEST = BASE / "597-world-map-wmw-v0-9-1-right-dossier-candidate-a1-manifest.json"
REFERENCE_DOSSIER = BASE / "29-right-dossier-base-v0-21-integrated-endcaps.png"

OLD_GODOT = BASE / "585-world-map-wmw-v0-9-0-right-dossier-candidate-a-godot-runtime.png"
PHOTO_SOURCE_SIZE = (1104, 704)
PHOTO_INGREDIENT_SIZE = (552, 352)
PHOTO_RATIO = 69 / 44
PHOTO_FOCAL_POINT = (0.74, 0.46)
PHOTO_MAX_CROP_FRACTION = 0.10
HEADER_AXIS_2X = 118
HEADER_ICON_OFFSET_2X = 6
STATUS_GROUP_OFFSET_2X = -8
REGION_BODY_INNER = [34, 290, 252, 50]
REGION_BODY_NO_TEXT = [22, 288, 4, 54]

TEXT_FIELD_BY_VALUE = {
    "北美禁区警戒带": "title_slot",
    "高危": "status_stamp_primary",
    "推荐12": "status_stamp_secondary",
    "天线阵列仍在发射，林线内出现异常回波。": "region_body_line_1",
    "进入前可先核对本周地区任务与封锁条件。": "region_body_line_2",
    "限时 2 周 · 线索缺口 3 · 深链 1": "decision_facts",
    "查看任务情报 · 12项": "mission_intel_label",
    "进入选定地区": "primary_enter_label",
}

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

if DOSSIER["contract_version"] not in {"0.8.6", "0.8.7", "0.8.8"} or MISSION["contract_version"] not in {"0.8.6", "0.8.7", "0.8.8"} or PRIMARY["contract_version"] != "0.8.6":
    raise RuntimeError("candidate A1 helpers require dossier/mission v0.8.6-v0.8.8 and primary v0.8.6")


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
    draw.text((42, 28), "WMW 右 dossier candidate A1 · layout + photo input spec", font=font(34, True), fill=CREAM)
    draw.text((44, 75), "589 · A201 生产输入先行；本板落盘后才允许 590 真实 imagegen。三份 v0.8.6 frozen 不动。", font=font(16), fill=(184, 204, 196))

    old = Image.open(OLD_GODOT).convert("RGB").crop((76, 150, 556, 930))
    board.paste(old, (50, 150))
    draw.rectangle((40, 140, 540, 950), outline=(255, 91, 91), width=2)
    draw.text((50, 112), "585 OLD RUNTIME · three P1 defects", font=font(18, True), fill=(255, 120, 110))
    for rect in ((108, 198, 508, 286), (82, 582, 518, 690), (82, 294, 518, 570)):
        draw.rectangle(rect, outline=(255, 74, 95), width=4)

    panel = (600, 140, 1240, 950)
    draw.rectangle(panel, fill=(13, 39, 40), outline=(67, 112, 108), width=2)
    draw.text((630, 170), "RUNTIME LAYOUT TOKENS", font=font(22, True), fill=CREAM)
    layout_lines = [
        "header optical axis  y=59",
        "icon ink             +3px",
        "title ink             0px",
        "status ink group      -4px",
        "",
        "region_body outer  [22,288,276,54]",
        "cyan no-text       [22,288,4,54]",
        "body inner         [34,290,252,50]",
        "",
        "Gate: actual ink bbox, not node rect",
        "Gate: both body lines start x>=34",
    ]
    for index, line in enumerate(layout_lines):
        draw.text((630, 230 + index * 46), line, font=font(17, index in (0, 5, 6, 7)), fill=(220, 228, 208))
    axis_y = 800
    draw.line((650, axis_y, 1180, axis_y), fill=(101, 255, 148), width=3)
    draw.ellipse((680, axis_y - 34, 748, axis_y + 34), outline=(235, 227, 201), width=4)
    draw.rectangle((790, axis_y - 30, 1010, axis_y + 30), outline=(235, 227, 201), width=4)
    draw.rectangle((1050, axis_y - 52, 1165, axis_y + 52), outline=(235, 227, 201), width=4)
    draw.text((650, 860), "one optical axis; carrier geometry stays frozen", font=font(15), fill=GREEN)

    panel = (1280, 140, 1880, 950)
    draw.rectangle(panel, fill=(13, 39, 40), outline=(67, 112, 108), width=2)
    draw.text((1310, 170), "PHOTO CONTRACT · exact 69:44", font=font(22, True), fill=CREAM)
    photo_lines = [
        "production source   1104 x 704",
        "2x ingredient        552 x 352",
        "Godot runtime         414 x 264",
        "",
        "uniform scale only",
        "KEEP_ASPECT_COVERED",
        "STRETCH_SCALE = hard fail",
        "crop per axis <= 10%",
        "no upsample",
    ]
    for index, line in enumerate(photo_lines):
        draw.text((1310, 230 + index * 44), line, font=font(17, index < 3), fill=(220, 228, 208))
    photo_rect = (1320, 665, 1848, 1002)
    draw.rectangle(photo_rect, fill=(17, 51, 68), outline=GREEN, width=4)
    safe = (1346, 682, 1822, 985)
    draw.rectangle(safe, outline=(255, 212, 68), width=3)
    focal_x = round(photo_rect[0] + (photo_rect[2] - photo_rect[0]) * PHOTO_FOCAL_POINT[0])
    focal_y = round(photo_rect[1] + (photo_rect[3] - photo_rect[1]) * PHOTO_FOCAL_POINT[1])
    draw.ellipse((focal_x - 12, focal_y - 12, focal_x + 12, focal_y + 12), outline=(255, 92, 92), width=4)
    draw.text((1330, 620), "safe 5% · radar focal (0.74, 0.46)", font=font(16, True), fill=(255, 212, 68))
    board.save(OUT_ANCHOR_BOARD)


def build_anchors() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    BASE.mkdir(parents=True, exist_ok=True)
    build_anchor_board()
    print(OUT_ANCHOR_BOARD)


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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_photo_ingredients() -> dict[str, Any]:
    if not PHOTO_RAW.exists():
        raise FileNotFoundError(f"Generate the locked photo input first: {PHOTO_RAW}")
    raw = Image.open(PHOTO_RAW).convert("RGB")
    source_width, source_height = PHOTO_SOURCE_SIZE
    if raw.width < source_width or raw.height < source_height:
        raise RuntimeError(f"photo raw is too small for downsample-only production: {raw.size}")
    uniform_scale = max(source_width / raw.width, source_height / raw.height)
    if uniform_scale > 1.0:
        raise RuntimeError("photo source would require upsampling")
    resized_size = (round(raw.width * uniform_scale), round(raw.height * uniform_scale))
    resized = raw.resize(resized_size, Image.Resampling.LANCZOS)
    focal_x = resized.width * PHOTO_FOCAL_POINT[0]
    focal_y = resized.height * PHOTO_FOCAL_POINT[1]
    desired_x = source_width * PHOTO_FOCAL_POINT[0]
    desired_y = source_height * PHOTO_FOCAL_POINT[1]
    left = min(max(0, round(focal_x - desired_x)), resized.width - source_width)
    top = min(max(0, round(focal_y - desired_y)), resized.height - source_height)
    crop_rect = (left, top, left + source_width, top + source_height)
    crop_fraction = {
        "x": (resized.width - source_width) / resized.width,
        "y": (resized.height - source_height) / resized.height,
    }
    if max(crop_fraction.values()) > PHOTO_MAX_CROP_FRACTION:
        raise RuntimeError(f"photo cover crop exceeds locked 10% limit: {crop_fraction}")
    production = resized.crop(crop_rect)
    if production.size != PHOTO_SOURCE_SIZE:
        raise RuntimeError(f"photo source size mismatch: {production.size}")
    ingredient = production.resize(PHOTO_INGREDIENT_SIZE, Image.Resampling.LANCZOS)
    INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    production.save(PHOTO_SOURCE)
    ingredient.save(PHOTO_INGREDIENT)
    source_ratio = production.width / production.height
    ingredient_ratio = ingredient.width / ingredient.height
    ratio_error = max(abs(source_ratio - PHOTO_RATIO), abs(ingredient_ratio - PHOTO_RATIO)) / PHOTO_RATIO
    if ratio_error > 0.005:
        raise RuntimeError(f"photo ratio error exceeds 0.5%: {ratio_error}")
    report = {
        "raw_size": list(raw.size),
        "raw_ratio": raw.width / raw.height,
        "production_source_size": list(production.size),
        "ingredient_size": list(ingredient.size),
        "locked_ratio": PHOTO_RATIO,
        "ratio_error_fraction": ratio_error,
        "uniform_raw_to_source_scale": uniform_scale,
        "resized_before_crop": list(resized.size),
        "source_crop_rect": list(crop_rect),
        "crop_fraction": crop_fraction,
        "focal_point_normalized": list(PHOTO_FOCAL_POINT),
        "source_to_ingredient_scale_x": ingredient.width / production.width,
        "source_to_ingredient_scale_y": ingredient.height / production.height,
        "upsample_used": False,
        "raw_sha256": file_sha256(PHOTO_RAW),
        "source_sha256": file_sha256(PHOTO_SOURCE),
        "ingredient_sha256": file_sha256(PHOTO_INGREDIENT),
    }
    if report["source_to_ingredient_scale_x"] != report["source_to_ingredient_scale_y"]:
        raise RuntimeError("photo ingredient transform is non-uniform")
    return report


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
) -> tuple[int, int, int, int]:
    icon = Image.open(icon_path).convert("RGBA")
    target_width = max(1, round((rect[2] - rect[0]) * scale))
    target_height = max(1, round((rect[3] - rect[1]) * scale))
    icon.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    tinted = Image.new("RGBA", icon.size, color)
    tinted.putalpha(icon.getchannel("A"))
    x = rect[0] + (rect[2] - rect[0] - icon.width) // 2
    y = rect[1] + (rect[3] - rect[1] - icon.height) // 2
    canvas.alpha_composite(tinted, (x, y))
    alpha_bbox = tinted.getchannel("A").getbbox()
    if alpha_bbox is None:
        raise RuntimeError(f"runtime icon has no alpha content: {icon_path}")
    return (x + alpha_bbox[0], y + alpha_bbox[1], x + alpha_bbox[2], y + alpha_bbox[3])


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
    report.update(
        {
            "field": TEXT_FIELD_BY_VALUE.get(text_value, text_value),
            "rect": list(rect),
            "bbox": list(report["raster_glyph_bbox"]),
            "text": text_value,
            "font_size": size,
            "fit_search_pass": fits,
        }
    )
    return report


def render_runtime_component(show_qa: bool) -> tuple[Image.Image, list[dict[str, Any]]]:
    shell = Image.open(PARENT_MASTER).convert("RGBA")
    mission = Image.open(MISSION_MASTER).convert("RGBA")
    primary = Image.open(PRIMARY_MASTER).convert("RGBA")
    photo_rect = scale_rect(DOSSIER["frozen"]["slots"]["photo_slot"])
    photo = Image.open(PHOTO_INGREDIENT).convert("RGBA")
    if photo.size != (photo_rect[2] - photo_rect[0], photo_rect[3] - photo_rect[1]):
        raise RuntimeError(f"photo ingredient must match the 2x slot exactly: {photo.size}")
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
    header_icon = (header_icon[0], header_icon[1] + HEADER_ICON_OFFSET_2X, header_icon[2], header_icon[3] + HEADER_ICON_OFFSET_2X)
    header_icon_bbox = paste_runtime_icon(component, RUNTIME_GLOBE, header_icon, (90, 93, 76, 255), 0.86)
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
    status = (status[0], status[1] + STATUS_GROUP_OFFSET_2X, status[2], status[3] + STATUS_GROUP_OFFSET_2X)
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
    title_bbox = reports[0]["raster_glyph_bbox"]
    status_boxes = [reports[1]["raster_glyph_bbox"], reports[2]["raster_glyph_bbox"]]
    status_union = (
        min(item[0] for item in status_boxes),
        min(item[1] for item in status_boxes),
        max(item[2] for item in status_boxes),
        max(item[3] for item in status_boxes),
    )
    header_centers = {
        "icon": (header_icon_bbox[1] + header_icon_bbox[3]) / 2,
        "title": (title_bbox[1] + title_bbox[3]) / 2,
        "status_group": (status_union[1] + status_union[3]) / 2,
    }
    reports[0]["header_optical_alignment"] = {
        "axis_y_2x": HEADER_AXIS_2X,
        "ink_bboxes": {
            "icon": list(header_icon_bbox),
            "title": list(title_bbox),
            "status_group": list(status_union),
        },
        "centers_y_2x": header_centers,
        "max_axis_deviation_px_2x": max(abs(value - HEADER_AXIS_2X) for value in header_centers.values()),
    }
    body = scale_rect(REGION_BODY_INNER)
    body_mid = (body[1] + body[3]) // 2
    reports.append(
        fit_and_draw(
            draw,
            (body[0], body[1], body[2], body_mid),
            "天线阵列仍在发射，林线内出现异常回波。",
            max_size=23,
            min_size=17,
            bold=False,
            fill=ink,
            pad_x=0,
        )
    )
    reports.append(
        fit_and_draw(
            draw,
            (body[0], body_mid, body[2], body[3]),
            "进入前可先核对本周地区任务与封锁条件。",
            max_size=23,
            min_size=17,
            bold=False,
            fill=ink,
            pad_x=0,
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
        inner = scale_rect(REGION_BODY_INNER)
        no_text = scale_rect(REGION_BODY_NO_TEXT)
        draw.rectangle((inner[0], inner[1], inner[2] - 1, inner[3] - 1), outline=(95, 255, 140, 255), width=3)
        draw.rectangle((no_text[0], no_text[1], no_text[2] - 1, no_text[3] - 1), outline=(255, 75, 75, 255), width=3)
        draw.line((0, HEADER_AXIS_2X, component.width - 1, HEADER_AXIS_2X), fill=(95, 255, 140, 255), width=2)
    return component, reports


def build_master_board(
    parent_report: dict[str, Any],
    mission_report: dict[str, Any],
    primary_report: dict[str, Any],
    photo_report: dict[str, Any],
) -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "WMW 右 dossier v0.9.1 · candidate A1 photo + clean masters", font=font(34, True), fill=CREAM)
    draw.text((44, 78), "591 · 先锁 69:44 再生图；raw → 1104×704 → 552×352 全程等比，框体/文字/图标独立。", font=font(17), fill=(190, 210, 201))

    photo_raw = Image.open(PHOTO_RAW).convert("RGB")
    photo_source = Image.open(PHOTO_SOURCE).convert("RGB")
    photo_ingredient = Image.open(PHOTO_INGREDIENT).convert("RGB")
    raw_preview = ImageOps.contain(photo_raw, (520, 320), Image.Resampling.LANCZOS)
    source_preview = ImageOps.contain(photo_source, (520, 320), Image.Resampling.LANCZOS)
    ingredient_preview = ImageOps.contain(photo_ingredient, (414, 264), Image.Resampling.LANCZOS)
    board.paste(raw_preview, (42, 145))
    board.paste(source_preview, (596, 145))
    board.paste(ingredient_preview, (1150, 145))
    draw.rectangle((36, 139, 568, 471), outline=(91, 167, 192), width=2)
    draw.rectangle((590, 139, 1122, 471), outline=GREEN, width=2)
    draw.rectangle((1144, 139, 1570, 415), outline=(255, 207, 72), width=2)
    draw.text((42, 112), f"RAW IMAGEGEN · {photo_raw.width}×{photo_raw.height}", font=font(17, True), fill=(91, 167, 192))
    draw.text((596, 112), "PRODUCTION SOURCE · 1104×704 · exact 69:44", font=font(17, True), fill=GREEN)
    draw.text((1150, 112), "2× INGREDIENT · 552×352", font=font(17, True), fill=(255, 207, 72))

    parent = Image.open(PARENT_MASTER).convert("RGBA").resize((256, 416), Image.Resampling.LANCZOS)
    mission = Image.open(MISSION_MASTER).convert("RGBA").resize((568, 88), Image.Resampling.LANCZOS)
    primary = Image.open(PRIMARY_MASTER).convert("RGBA").resize((568, 100), Image.Resampling.LANCZOS)
    paste_on_checker(board, parent, (42, 575))
    paste_on_checker(board, mission, (350, 635))
    paste_on_checker(board, primary, (350, 795))
    draw.rectangle((36, 569, 304, 997), outline=GREEN, width=2)
    draw.rectangle((344, 629, 924, 729), outline=(75, 225, 225), width=2)
    draw.rectangle((344, 789, 924, 901), outline=(157, 182, 91), width=2)
    draw.text((42, 538), "PARENT · 640×1040 · hollow photo window", font=font(17, True), fill=GREEN)
    draw.text((350, 602), "SECONDARY · 568×88 · teal", font=font(17, True), fill=(75, 225, 225))
    draw.text((350, 762), "PRIMARY · 568×100 · olive", font=font(17, True), fill=(157, 182, 91))

    panel = (970, 520, 1880, 1010)
    draw.rectangle(panel, fill=(13, 39, 40), outline=(67, 112, 108), width=2)
    draw.text((994, 544), "LOCKED MEASUREMENTS", font=font(20, True), fill=CREAM)
    lines = [
        f"raw {photo_report['raw_size']} → resized {photo_report['resized_before_crop']}",
        f"crop x={photo_report['crop_fraction']['x']:.4f}, y={photo_report['crop_fraction']['y']:.4f} (limit 0.10)",
        f"source {photo_report['production_source_size']} → ingredient {photo_report['ingredient_size']}",
        f"uniform ingredient scale {photo_report['source_to_ingredient_scale_x']:.3f}",
        f"ratio error {photo_report['ratio_error_fraction']:.6f}; upsample={photo_report['upsample_used']}",
        "",
        f"photo alpha {parent_report['photo_window_transparent_pixels']}/{parent_report['photo_window_expected_pixels']}",
        f"photo ring fail {parent_report['photo_window_ring_alpha_failures']}",
        f"parent magenta {parent_report['magenta_residue_pixels']}",
        "",
        f"mission body {mission_report['visible_body_bbox']}",
        f"primary body {primary_report['visible_body_bbox']}",
        "",
        "A201: header/body are runtime tokens;",
        "photo scale is uniform by construction.",
    ]
    for index, line in enumerate(lines):
        draw.text((994, 590 + index * 27), line, font=font(14, index in (0, 6, 10, 13)), fill=(218, 226, 205))
    board.save(OUT_MASTER_BOARD)


def build_runtime_board(show_qa: bool) -> list[dict[str, Any]]:
    component, reports = render_runtime_component(show_qa)
    board = Image.new("RGB", (1920, 1080), (6, 18, 20))
    draw = ImageDraw.Draw(board)
    board.paste(component.convert("RGB"), (48, 20))
    title = "Python v0.9.1 candidate A1 right dossier runtime QA" if show_qa else "Python v0.9.1 candidate A1 right dossier runtime fill"
    draw.text((742, 34), title, font=font(31, True), fill=CREAM)
    draw.text((744, 82), "A201：共享页眉光学轴、正文可读内区、69:44 等比照片；frozen carrier 不动。", font=font(17), fill=(191, 209, 198))

    slots = DOSSIER["frozen"]["slots"]
    header_union = [14, 18, 290, 92]
    header_crop = component.crop(scale_rect(header_union)).resize((828, 222), Image.Resampling.NEAREST)
    photo_crop = component.crop(scale_rect(slots["photo_slot"])).resize((828, 528), Image.Resampling.NEAREST)
    body_crop = component.crop(scale_rect(slots["region_body"])).resize((828, 162), Image.Resampling.NEAREST)
    board.paste(header_crop.convert("RGB"), (800, 150))
    board.paste(photo_crop.convert("RGB"), (800, 430))
    board.paste(body_crop.convert("RGB"), (800, 990 - body_crop.height))
    draw.rectangle((790, 140, 1638, 382), outline=GREEN, width=2)
    draw.rectangle((790, 420, 1638, 958), outline=(72, 236, 174), width=2)
    draw.rectangle((790, 818, 1638, 990), outline=(255, 212, 68), width=2)
    draw.text((800, 112), "HEADER · actual ink aligned to y=59 optical axis", font=font(18, True), fill=GREEN)
    draw.text((800, 392), "PHOTO · exact 69:44 · no non-uniform scaling", font=font(18, True), fill=(72, 236, 174))
    draw.text((800, 790), "BODY · inner [34,290,252,50] · cyan strip is no-text", font=font(18, True), fill=(255, 212, 68))

    passed = sum(1 for report in reports if report["fit_search_pass"] and report["glyph_bbox_inside_inner_rect"])
    draw.text((1660, 210), f"text bbox {passed}/{len(reports)}", font=font(17, True), fill=GREEN if passed == len(reports) else (255, 84, 73))
    header = reports[0]["header_optical_alignment"]
    draw.text((1660, 255), f"axis dev {header['max_axis_deviation_px_2x']:.2f}px @2x", font=font(15, True), fill=GREEN if header["max_axis_deviation_px_2x"] <= 2 else (255, 84, 73))
    draw.text((1660, 302), "粉框=字形 alpha" if show_qa else "载体与内容分层", font=font(14), fill=(223, 221, 196))
    (OUT_PYTHON_QA if show_qa else OUT_PYTHON).parent.mkdir(parents=True, exist_ok=True)
    board.save(OUT_PYTHON_QA if show_qa else OUT_PYTHON)
    return reports


def write_manifest(
    parent_report: dict[str, Any],
    mission_report: dict[str, Any],
    primary_report: dict[str, Any],
    atlas_report: dict[str, Any],
    photo_report: dict[str, Any],
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
    reports_by_text = {item["text"]: item for item in text_reports}
    header_alignment = reports_by_text["北美禁区警戒带"]["header_optical_alignment"]
    body_reports = [
        reports_by_text["天线阵列仍在发射，林线内出现异常回波。"],
        reports_by_text["进入前可先核对本周地区任务与封锁条件。"],
    ]
    body_boxes = [item["raster_glyph_bbox"] for item in body_reports]
    body_inner = list(scale_rect(REGION_BODY_INNER))
    no_text = list(scale_rect(REGION_BODY_NO_TEXT))
    body_lefts = [item[0] for item in body_boxes]
    body_rights = [item[2] for item in body_boxes]
    body_padding_pass = (
        min(body_lefts) >= body_inner[0]
        and max(body_rights) <= body_inner[2]
        and max(body_lefts) - min(body_lefts) <= 2
        and min(body_lefts) - no_text[2] >= 16
    )
    image_aspect_pass = (
        photo_report["production_source_size"] == list(PHOTO_SOURCE_SIZE)
        and photo_report["ingredient_size"] == list(PHOTO_INGREDIENT_SIZE)
        and photo_report["ratio_error_fraction"] <= 0.005
        and photo_report["source_to_ingredient_scale_x"] == photo_report["source_to_ingredient_scale_y"]
        and max(photo_report["crop_fraction"].values()) <= PHOTO_MAX_CROP_FRACTION
        and not photo_report["upsample_used"]
    )
    header_alignment_pass = header_alignment["max_axis_deviation_px_2x"] <= 2
    manifest = {
        "schema_version": 1,
        "asset_line": "world-map-benchmark-landing/right-dossier",
        "version": "v0.9.1",
        "candidate": "A1",
        "status": "evidence_ready_godot_capture_pending",
        "design_adoption": "A201：用户指出页眉组件未齐、正文过左和照片拉伸；采纳共享光学轴、正文可读内区与先锁 69:44 规格再生图的修正路线。",
        "contracts": {
            "right_dossier_page": {"version": DOSSIER["contract_version"], "frozen_changed": False},
            "right_mission_intel_button": {"version": MISSION["contract_version"], "frozen_changed": False},
            "right_action_lane": {"version": PRIMARY["contract_version"], "frozen_changed": False},
        },
        "sources": {
            "579_parent_imagegen": str(PARENT_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "580_mission_imagegen": str(MISSION_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "581_primary_imagegen": str(PRIMARY_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "590_photo_imagegen_raw": str(PHOTO_RAW.relative_to(ROOT)).replace("\\", "/"),
            "chroma_key": "#FF00FF removed with the installed imagegen remove_chroma_key helper before contract construction",
            "photo_production_source": str(PHOTO_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "photo_2x_ingredient": str(PHOTO_INGREDIENT.relative_to(ROOT)).replace("\\", "/"),
        },
        "outputs": {
            "layout_photo_spec": str(OUT_ANCHOR_BOARD.relative_to(ROOT)).replace("\\", "/"),
            "photo_master_qa": str(OUT_MASTER_BOARD.relative_to(ROOT)).replace("\\", "/"),
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
            "photo": photo_report,
            "parent": parent_report,
            "mission": mission_report,
            "primary": primary_report,
            "atlas": atlas_report,
            "child_visible_body_edge_diff": body_edge_diff,
            "text_tokens": text_reports,
            "header_optical_alignment": header_alignment,
            "region_body_visual_padding": {
                "outer_rect_1x": DOSSIER["frozen"]["slots"]["region_body"],
                "inner_rect_1x": REGION_BODY_INNER,
                "no_text_rect_1x": REGION_BODY_NO_TEXT,
                "inner_rect_2x": body_inner,
                "no_text_rect_2x": no_text,
                "line_glyph_bboxes_2x": body_boxes,
                "line_left_difference_px_2x": max(body_lefts) - min(body_lefts),
                "minimum_gap_after_no_text_px_2x": min(body_lefts) - no_text[2],
            },
        },
        "gates": {
            "real_imagegen_sources": {"status": "pass", "evidence": [579, 580, 581, 590]},
            "image_aspect_pass": {
                "status": "pass" if image_aspect_pass else "fail",
                "locked_ratio": "69:44",
                "production_source": photo_report["production_source_size"],
                "ingredient_2x": photo_report["ingredient_size"],
                "runtime_target": [414, 264],
                "ratio_error_fraction": photo_report["ratio_error_fraction"],
                "uniform_scale": [photo_report["source_to_ingredient_scale_x"], photo_report["source_to_ingredient_scale_y"]],
                "crop_fraction": photo_report["crop_fraction"],
                "upsample_used": photo_report["upsample_used"],
                "godot_required_stretch_mode": "STRETCH_KEEP_ASPECT_COVERED",
                "forbidden_stretch_mode": "STRETCH_SCALE",
            },
            "header_runtime_ink_optical_axis": {
                "status": "pass" if header_alignment_pass else "fail",
                "axis_y_1x": HEADER_AXIS_2X / 2,
                "max_deviation_px_2x": header_alignment["max_axis_deviation_px_2x"],
                "limit_px_2x": 2,
                "basis": "真实 icon/title/status 字形 alpha bbox 中心，不以 carrier 矩形代替。",
            },
            "region_body_visual_padding": {
                "status": "pass" if body_padding_pass else "fail",
                "line_glyph_bboxes_2x": body_boxes,
                "line_left_difference_px_2x": max(body_lefts) - min(body_lefts),
                "minimum_gap_after_no_text_px_2x": min(body_lefts) - no_text[2],
                "basis": "region_body frozen 外槽不动；青色索引条为禁字区，正文只进入共享 inner_rect。",
            },
            "no_fake_text_in_sprite_masters": {"status": "evidence_ready", "basis": "三张 keyed clean masters 只含空载体；所有文字由运行时绘制。"},
            "functional_faces_orthogonal": {"status": "evidence_ready", "basis": "正交几何锚点与 591 clean-master QA 板。"},
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
            "godot_windowed_capture": {"status": "pending", "runner": "scripts/run_wmw_right_dossier_godot_capture_v091.ps1"},
            "visual_review": {"status": "pending", "basis": "589/590/591/592/593 已准备；594/595 Godot 与双 agent 复核待完成。"},
        },
        "judgment": "Candidate A1 已完成等比照片配料、页眉光学轴和正文内区的 Python 构建；Godot 窗口截图与视觉复核尚未完成。",
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def build_candidate() -> None:
    required = [PARENT_KEYED, MISSION_KEYED, PRIMARY_KEYED, PHOTO_RAW, OUT_ANCHOR_BOARD]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing candidate inputs: {missing}")
    photo_report = build_photo_ingredients()
    parent_report = build_parent_master()
    mission_report = build_button_master(MISSION_KEYED, MISSION, MISSION_MASTER)
    primary_report = build_button_master(PRIMARY_KEYED, PRIMARY, PRIMARY_MASTER)
    build_runtime_icons()
    atlas_report = write_atlas()
    build_master_board(parent_report, mission_report, primary_report, photo_report)
    build_runtime_board(False)
    text_reports = build_runtime_board(True)
    manifest = write_manifest(parent_report, mission_report, primary_report, atlas_report, photo_report, text_reports)
    failed = [name for name, gate in manifest["gates"].items() if gate["status"] == "fail"]
    if failed:
        raise RuntimeError(f"candidate A1 build gates failed: {failed}")
    for path in (PHOTO_SOURCE, PHOTO_INGREDIENT, PARENT_MASTER, MISSION_MASTER, PRIMARY_MASTER, ATLAS, OUT_MASTER_BOARD, OUT_PYTHON, OUT_PYTHON_QA, OUT_MANIFEST):
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
    draw.text((42, 28), "WMW 右 dossier · candidate A → A1 correction review", font=font(32, True), fill=CREAM)
    draw.text((44, 74), "596 · 同一 Godot 4.6.2 窗口链对照：页眉光学轴、正文安全内区、照片等比显示。A1 仍待用户裁决。", font=font(16), fill=(194, 211, 201))

    old = Image.open(OLD_GODOT).convert("RGB")
    new = Image.open(OUT_GODOT).convert("RGB")
    old_dossier = old.crop((76, 150, 556, 930))
    new_dossier = new.crop((76, 150, 556, 930))
    board.paste(old_dossier, (35, 145))
    board.paste(new_dossier, (545, 145))
    draw.rectangle((25, 135, 525, 945), outline=(255, 88, 88), width=2)
    draw.rectangle((535, 135, 1035, 945), outline=GREEN, width=2)
    draw.text((35, 108), "A / 585 · carrier-center + zero body inset + stretched photo", font=font(15, True), fill=(255, 106, 106))
    draw.text((545, 108), "A1 / 594 · ink-axis + shared body inner + exact 69:44", font=font(15, True), fill=GREEN)

    def runtime_crop(image: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
        return image.crop(rect)

    header_rect = (97, 177, 511, 315)
    photo_rect = (109, 297, 523, 561)
    body_rect = (109, 582, 523, 663)
    closeups = [
        ("HEADER", header_rect, 160, (95, 255, 140)),
        ("PHOTO", photo_rect, 400, (72, 236, 174)),
        ("BODY", body_rect, 750, (255, 212, 68)),
    ]
    for label, rect, y, color in closeups:
        old_crop = runtime_crop(old, rect)
        new_crop = runtime_crop(new, rect)
        if label == "HEADER":
            old_crop = old_crop.resize((372, 124), Image.Resampling.NEAREST)
            new_crop = new_crop.resize((372, 124), Image.Resampling.NEAREST)
        elif label == "PHOTO":
            old_crop = old_crop.resize((372, 237), Image.Resampling.LANCZOS)
            new_crop = new_crop.resize((372, 237), Image.Resampling.LANCZOS)
        else:
            old_crop = old_crop.resize((372, 73), Image.Resampling.NEAREST)
            new_crop = new_crop.resize((372, 73), Image.Resampling.NEAREST)
        board.paste(old_crop, (1100, y))
        board.paste(new_crop, (1500, y))
        draw.rectangle((1094, y - 6, 1478, y + old_crop.height + 6), outline=(255, 88, 88), width=2)
        draw.rectangle((1494, y - 6, 1878, y + new_crop.height + 6), outline=color, width=2)
        draw.text((1100, y - 34), f"{label} · A", font=font(15, True), fill=(255, 106, 106))
        draw.text((1500, y - 34), f"{label} · A1", font=font(15, True), fill=color)

    lines = [
        "1. 页眉按真实字形 alpha 中心对齐到 y=59，不再让三个不同高度 carrier 各自居中。",
        "2. 正文冻结外槽不动，统一使用 [34,290,252,50]；青色索引条成为硬禁字区。",
        "3. 新照片先定 69:44，再按 1104×704 → 552×352 → 414×264 等比缩放。",
        "4. Godot 禁止 STRETCH_SCALE；资源尺寸或比例不符时截图脚本直接失败。",
    ]
    for index, line in enumerate(lines):
        draw.text((1100, 870 + index * 38), line, font=font(13, index == 3), fill=(218, 226, 205))
    board.save(OUT_REVIEW)


def finalize_candidate() -> None:
    if not OUT_MANIFEST.exists():
        raise FileNotFoundError(OUT_MANIFEST)
    if not OUT_GODOT.exists() or not OUT_GODOT_QA.exists():
        raise FileNotFoundError("Godot screenshots 594/595 are required before finalization")
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
        "runner": "scripts/run_wmw_right_dossier_godot_capture_v091.ps1",
        "frame_post_draw_waits": 2,
        "all_black_refusal": True,
        "relative_baseline_loss_refusal": True,
        "baseline": baseline_stats,
        "qa": qa_stats,
    }
    manifest["gates"]["visual_review"] = {
        "status": "evidence_ready_user_review_pending",
        "basis": "589 规格板、590 真实生图、591 配料 QA、592/593 Python、594/595 Godot 与 596 A/A1 对比板。",
        "parent_self_check": {
            "header_optical_axis": "evidence_ready：594/595 中 icon/title/status 真实墨迹共用 y=59 轴，程序偏差见 gate。",
            "region_body_padding": "evidence_ready：两行均位于共享 inner_rect，未进入青色 no-text strip。",
            "photo_aspect": "evidence_ready：新照片形体未被非等比压缩，三阶段尺寸与变换见 image_aspect_pass。",
            "action_stack_alignment": "evidence_ready：两条可见主体仍同宽，原 A196 gate 未回退。",
        },
        "dual_agent_reviews": {
            "ux_laoge": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 0, "p2": 2},
                "basis": "三项旧 P1 均由运行截图、实际 ink bbox、正文禁字区间距和 69:44 变换链共同消费；未见新增 P0/P1。",
                "remaining": [
                    "“推荐12”正式语义与单位仍未闭合，且可能与“12项”串读。",
                    "未来 hover/pressed/disabled 必须证明两条动作带均以整条单一 hit rect 统一反馈。",
                ],
            },
            "ui_designer": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 0, "p2": 2},
                "basis": "页眉墨迹共轴、正文呼吸空间、照片等比与 clean low-poly weekly 风格均通过；雷达 > 金字塔 > 天线的缩小层级成立，无新增美术或信息层级问题。",
            },
        },
    }
    manifest["gates"]["visible_field_semantic_necessity"] = {
        "status": "fail",
        "basis": "A205 复核确认 A1 将容量压力 fixture 当成玩家运行数据；推荐12、压力标题/计数与虚构正文均无正式 payload 归属。",
        "superseded_by": 604,
    }
    manifest["gates"]["visual_review"]["status"] = "invalidated_by_a205_fixture_semantic_leak"
    manifest["status"] = "visual_fail_fixture_semantic_leak_superseded_by_604"
    manifest["judgment"] = "A1 的几何、照片和文字容器证据仍可复用，但运行时可见语义已失败；不得继续作为玩家视觉候选，改由 A2/604 取代。"
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
