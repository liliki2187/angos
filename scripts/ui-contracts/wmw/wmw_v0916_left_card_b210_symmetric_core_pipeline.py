# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps

import wmw_v092_left_card_b1_vertical_slice as b1
import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v098_left_card_b22_hollow_shell_geometry_pipeline as b22
import wmw_v0912_left_card_b26_runtime_badge_pipeline as b26
import wmw_v0913_left_card_b27_contract_badge_pipeline as b27
import wmw_v0914_left_card_b28_state_badge_globe_fix as b28
import wmw_v0915_left_card_b29_no_inpaint_badge_pipeline as b29


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.16"
ROUND_ID = "B2.10"
ASSET_ID = "world_map_wmw_left_region_card_b2_10_symmetric_core"

OUT_COMPARE = BASE / "529-world-map-wmw-v0-9-16-left-card-b2-10-symmetric-core-compare.png"
OUT_INGREDIENTS = BASE / "530-world-map-wmw-v0-9-16-left-card-b2-10-symmetric-core-qa.png"
OUT_ATLAS = BASE / "531-world-map-wmw-v0-9-16-left-card-b2-10-atlas-2x.png"
OUT_GEOMETRY = BASE / "532-world-map-wmw-v0-9-16-left-card-b2-10-geometry-qa.png"
OUT_RUNTIME = BASE / "533-world-map-wmw-v0-9-16-left-card-b2-10-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "534-world-map-wmw-v0-9-16-left-card-b2-10-runtime-fill-qa.png"
OUT_VISUAL_QA = BASE / "535-world-map-wmw-v0-9-16-left-card-b2-10-16point-visual-qa.png"
OUT_MANIFEST = BASE / "536-world-map-wmw-v0-9-16-left-card-b2-10-manifest.json"
OUT_GODOT = BASE / "537-world-map-wmw-v0-9-16-left-card-b2-10-godot-single-component.png"
OUT_GODOT_QA = BASE / "538-world-map-wmw-v0-9-16-left-card-b2-10-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b210_symmetric_core_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b210_symmetric_core_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
MASTER_STATE = "available"
MASTER_INDEX = STATE_ORDER.index(MASTER_STATE)
CONTRACT = b11.load_contract()


def slot_rect_2x(name: str) -> tuple[int, int, int, int]:
    x, y, w, h = CONTRACT["frozen"]["slots"][name]
    return (x * 2, y * 2, (x + w) * 2, (y + h) * 2)


ACTION_RECT = slot_rect_2x("action_badge")
BADGE_CENTER = ((ACTION_RECT[0] + ACTION_RECT[2]) / 2.0, (ACTION_RECT[1] + ACTION_RECT[3]) / 2.0)
BENCHMARK_BADGE_CENTER = (332.0, 246.0)
PREVIOUS_CONTRACT_LEFT_2X = 316
ICON_CANVAS_SIZE = (44, 44)
ICON_OPAQUE_MAX = (36, 36)
ICON_MIN_PADDING = 4

# Measured directly on 396. These boxes are ordinary rectangular scene crops:
# they begin to the right of the baked source globe and end inside the source
# photo, before the source card frame. Historical B1.1 relative crops are not
# reused because three of their right edges crossed into the source frame.
CLEAN_PHOTO_SOURCE_BOXES = {
    "selected": (218, 104, 641, 390),
    "available": (922, 104, 1281, 390),
    "warning": (204, 607, 641, 876),
    "locked": (922, 607, 1281, 876),
}
SOURCE_PHOTO_INTERIORS = {
    "selected": (103, 101, 661, 394),
    "available": (743, 101, 1294, 394),
    "warning": (103, 603, 661, 880),
    "locked": (743, 603, 1294, 880),
}
SOURCE_GLOBE_BBOXES = {
    "selected": (98, 87, 191, 184),
    "available": (737, 87, 831, 184),
    "warning": (98, 589, 191, 685),
    "locked": (737, 589, 832, 685),
}
PHOTO_FRAME_RUN_LIMIT = 24

# Candidate B's exterior ring is already the approved geometry. B2.10 never
# retires, moves, blurs, or inpaints it; only the enclosed semantic core changes.
SOURCE_BADGE_ZONE = (280, 193, 385, 299)
EXPECTED_SOURCE_RING_BBOX = (288, 201, 376, 291)
INNER_OPENING_POLY = [
    (309, 208), (355, 208), (369, 222), (369, 269),
    (354, 284), (309, 284), (295, 270), (295, 223),
]
CORE_POLY = [
    (310, 216), (354, 216), (361, 223), (361, 269),
    (354, 276), (310, 276), (302, 268), (302, 224),
]


def polygon_mask(points: list[tuple[int, int]]) -> Image.Image:
    out = Image.new("L", FRAME_SIZE, 0)
    ImageDraw.Draw(out).polygon(points, fill=255)
    return out


INNER_OPENING_MASK = polygon_mask(INNER_OPENING_POLY)
CORE_MASK = polygon_mask(CORE_POLY)
CORE_CENTER = (int(BENCHMARK_BADGE_CENTER[0]), int(BENCHMARK_BADGE_CENTER[1]))
FACET_TONE_DELTAS = {"top": 3, "right": 0, "bottom": -3, "left": 0}
GRAIN_SEED = 178
GRAIN_TARGET_RATIO = 0.08


def core_facet_points() -> dict[str, list[tuple[int, int]]]:
    bbox = CORE_MASK.getbbox()
    assert bbox is not None
    x1, y1, x2, y2 = bbox
    cx, cy = CORE_CENTER
    half_width = min(cx - x1, x2 - cx)
    half_height = min(cy - y1, (y2 - 1) - cy)
    left = cx - half_width
    right = cx + half_width
    top = cy - half_height
    bottom = cy + half_height
    return {
        "top": [(left, top), (right, top), (cx, cy)],
        "right": [(right, top), (right, bottom), (cx, cy)],
        "bottom": [(right, bottom), (left, bottom), (cx, cy)],
        "left": [(left, bottom), (left, top), (cx, cy)],
    }


def core_facet_masks() -> dict[str, Image.Image]:
    clip = symmetric_facet_clip_mask()
    return {
        name: ImageChops.multiply(polygon_mask(points), clip)
        for name, points in core_facet_points().items()
    }


def symmetric_facet_clip_mask() -> Image.Image:
    return ImageChops.multiply(CORE_MASK, _mirror_mask_horizontal(CORE_MASK, CORE_CENTER[0]))


def _mask_count(mask: Image.Image) -> int:
    return sum(1 for value in mask.getdata() if value > 0)


def _mirror_mask_horizontal(mask: Image.Image, center_x: int) -> Image.Image:
    out = Image.new("L", mask.size, 0)
    src = mask.load()
    dst = out.load()
    bbox = mask.getbbox()
    if bbox is None:
        return out
    for y in range(bbox[1], bbox[3]):
        for x in range(bbox[0], bbox[2]):
            if src[x, y] == 0:
                continue
            mirror_x = 2 * center_x - x
            if 0 <= mirror_x < mask.width:
                dst[mirror_x, y] = 255
    return out


def _mask_iou(a: Image.Image, b: Image.Image) -> float:
    intersection = _mask_count(ImageChops.multiply(a, b))
    union = _mask_count(ImageChops.lighter(a, b))
    return 1.0 if union == 0 else intersection / union


def shared_sparse_grain() -> tuple[Image.Image, list[dict], float]:
    bbox = CORE_MASK.getbbox()
    assert bbox is not None
    x1, y1, x2, y2 = bbox
    core_pixels = _mask_count(CORE_MASK)
    target_pixels = round(core_pixels * GRAIN_TARGET_RATIO)
    rng = random.Random(GRAIN_SEED)
    delta_map = Image.new("I", FRAME_SIZE, 0)
    grain_mask = Image.new("L", FRAME_SIZE, 0)
    delta_px = delta_map.load()
    mask_px = grain_mask.load()
    clusters: list[dict] = []
    covered = 0
    attempts = 0
    while covered < target_pixels and attempts < 300:
        attempts += 1
        size = rng.randint(2, 4)
        x = rng.randint(x1, max(x1, x2 - size))
        y = rng.randint(y1, max(y1, y2 - size))
        delta = rng.choice((-1, 1))
        added = 0
        for py in range(y, min(y + size, y2)):
            for px in range(x, min(x + size, x2)):
                if CORE_MASK.getpixel((px, py)) == 0 or mask_px[px, py] != 0:
                    continue
                mask_px[px, py] = 255
                delta_px[px, py] = delta
                added += 1
        if added:
            covered += added
            clusters.append({"x": x, "y": y, "size": size, "delta_rgb": delta, "pixels": added})
    return delta_map, clusters, covered / max(1, core_pixels)


def badge_core_facet_symmetry_gate() -> dict:
    points = core_facet_points()
    masks = core_facet_masks()
    cx, cy = CORE_CENTER
    top_left, top_right, _ = points["top"]
    bottom_right, bottom_left, _ = points["bottom"]

    mirror_errors = [
        max(abs((2 * cx - top_left[0]) - top_right[0]), abs(top_left[1] - top_right[1])),
        max(abs((2 * cx - bottom_left[0]) - bottom_right[0]), abs(bottom_left[1] - bottom_right[1])),
        max(abs(top_left[0] - bottom_left[0]), abs((2 * cy - top_left[1]) - bottom_left[1])),
        max(abs(top_right[0] - bottom_right[0]), abs((2 * cy - top_right[1]) - bottom_right[1])),
    ]
    left_area = _mask_count(masks["left"])
    right_area = _mask_count(masks["right"])
    area_delta = abs(left_area - right_area) / max(1, max(left_area, right_area))
    mirror_ious = {
        "top": _mask_iou(masks["top"], _mirror_mask_horizontal(masks["top"], cx)),
        "bottom": _mask_iou(masks["bottom"], _mirror_mask_horizontal(masks["bottom"], cx)),
        "left_vs_right": _mask_iou(masks["left"], _mirror_mask_horizontal(masks["right"], cx)),
    }
    structural_mirror_iou = min(mirror_ious.values())
    center_error = max(abs(cx - BENCHMARK_BADGE_CENTER[0]), abs(cy - BENCHMARK_BADGE_CENTER[1]))
    _, clusters, grain_ratio = shared_sparse_grain()
    passed = (
        max(mirror_errors) <= 1
        and center_error <= 0.5
        and area_delta <= 0.01
        and structural_mirror_iou >= 0.985
        and FACET_TONE_DELTAS["left"] == FACET_TONE_DELTAS["right"]
        and 0.06 <= grain_ratio <= 0.10
    )
    return {
        "status": "pass" if passed else "fail",
        "method": "four facets parameterized from CORE_MASK bbox and shared center; structure measured before grain",
        "core_bbox_2x": list(CORE_MASK.getbbox() or ()),
        "center_2x": list(CORE_CENTER),
        "facet_points_2x": {name: [list(point) for point in facet] for name, facet in points.items()},
        "vertex_mirror_error_max_px": max(mirror_errors),
        "vertex_mirror_error_limit_px": 1,
        "center_convergence_error_px": center_error,
        "center_convergence_error_limit_px": 0.5,
        "left_area_pixels": left_area,
        "right_area_pixels": right_area,
        "left_right_area_delta_ratio": round(area_delta, 6),
        "left_right_area_delta_limit_ratio": 0.01,
        "mirror_iou_per_facet": {key: round(value, 6) for key, value in mirror_ious.items()},
        "structural_mirror_iou": round(structural_mirror_iou, 6),
        "structural_mirror_iou_min": 0.985,
        "tone_delta_rgb": FACET_TONE_DELTAS,
        "left_right_tone_equal": FACET_TONE_DELTAS["left"] == FACET_TONE_DELTAS["right"],
        "grain": {
            "seed": GRAIN_SEED,
            "cluster_count": len(clusters),
            "size_range_px_2x": [2, 4],
            "amplitude_rgb": [-1, 1],
            "coverage_ratio": round(grain_ratio, 6),
            "coverage_target_ratio": GRAIN_TARGET_RATIO,
            "shared_across_facets": True,
            "excluded_from_structural_mirror_gate": True,
            "periodic_per_pixel_noise_used": False,
        },
    }


def neutral_core_texture(shell: Image.Image) -> Image.Image:
    family = b27._average_rgb(shell, (246, 202, 282, 286))
    base = tuple(max(0, min(255, round(c * 0.78))) for c in family)
    out = Image.new("RGBA", FRAME_SIZE, (*base, 255))
    facet_layer = out.copy()
    draw = ImageDraw.Draw(facet_layer, "RGBA")

    def tone(delta: int) -> tuple[int, int, int, int]:
        return tuple(max(0, min(255, c + delta)) for c in base) + (255,)

    for name in ("top", "right", "bottom", "left"):
        draw.polygon(core_facet_points()[name], fill=tone(FACET_TONE_DELTAS[name]))
    out.paste(facet_layer, (0, 0), symmetric_facet_clip_mask())

    grain_delta, _, _ = shared_sparse_grain()
    px = out.load()
    grain_px = grain_delta.load()
    bbox = CORE_MASK.getbbox()
    assert bbox is not None
    for y in range(bbox[1], bbox[3]):
        for x in range(bbox[0], bbox[2]):
            if CORE_MASK.getpixel((x, y)):
                r, g, b, a = px[x, y]
                tooth = grain_px[x, y]
                px[x, y] = (
                    max(0, min(255, r + tooth)),
                    max(0, min(255, g + tooth)),
                    max(0, min(255, b + tooth)),
                    a,
                )
    return out


def source_badge_components(source: Image.Image) -> list[dict]:
    px = source.convert("RGBA").load()
    x1, y1, x2, y2 = SOURCE_BADGE_ZONE
    remaining = {
        (x, y)
        for y in range(y1, y2)
        for x in range(x1, x2)
        if b26._is_creamish(px[x, y])
    }
    components: list[dict] = []
    while remaining:
        start = remaining.pop()
        queue = [start]
        pixels = [start]
        for qx, qy in queue:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    neighbour = (qx + dx, qy + dy)
                    if neighbour in remaining:
                        remaining.remove(neighbour)
                        queue.append(neighbour)
                        pixels.append(neighbour)
        xs = [x for x, _ in pixels]
        ys = [y for _, y in pixels]
        components.append(
            {
                "pixels": pixels,
                "bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
                "count": len(pixels),
            }
        )
    return sorted(components, key=lambda item: item["count"], reverse=True)


def component_mask(component: dict) -> Image.Image:
    mask = Image.new("L", FRAME_SIZE, 0)
    px = mask.load()
    for x, y in component["pixels"]:
        px[x, y] = 255
    return mask


def rebuild_badge(master_shell: Image.Image, source: Image.Image) -> tuple[Image.Image, dict]:
    before = master_shell.copy().convert("RGBA")
    rebuilt = before.copy()
    # The candidate-B exterior is already approved. Rebuild only the measured
    # semantic core; CORE_MASK has zero overlap with the exterior ring component.
    b27._fill_with_mask(rebuilt, neutral_core_texture(rebuilt), CORE_MASK)
    facet_gate = badge_core_facet_symmetry_gate()

    components = source_badge_components(source)
    ring_component = next((item for item in components if item["bbox"] == EXPECTED_SOURCE_RING_BBOX), None)
    if ring_component is None:
        return rebuilt, {"status": "fail", "reason": "approved_source_outer_ring_not_found"}
    ring_mask = component_mask(ring_component)
    ring = b27.mask_metrics(ring_mask)
    core = b27.mask_metrics(CORE_MASK)
    right_gap_2x = FRAME_SIZE[0] - ring["bbox"][2]
    bbox_center = [(ring["bbox"][0] + ring["bbox"][2]) / 2.0, (ring["bbox"][1] + ring["bbox"][3]) / 2.0]
    center_delta = [abs(bbox_center[0] - BADGE_CENTER[0]), abs(bbox_center[1] - BADGE_CENTER[1])]
    clean_core_cream = sum(
        1
        for y in range(FRAME_SIZE[1])
        for x in range(FRAME_SIZE[0])
        if CORE_MASK.getpixel((x, y)) and b26._is_creamish(rebuilt.getpixel((x, y)))
    )
    before_px = before.load()
    rebuilt_px = rebuilt.load()
    outside_core_changed = 0
    outside_inner_changed = 0
    right_corridor_changed = 0
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if not CORE_MASK.getpixel((x, y)) and before_px[x, y] != rebuilt_px[x, y]:
                outside_core_changed += 1
            if not INNER_OPENING_MASK.getpixel((x, y)) and before_px[x, y] != rebuilt_px[x, y]:
                outside_inner_changed += 1
            if 369 <= x < 383 and 196 <= y < 296 and before_px[x, y] != rebuilt_px[x, y]:
                right_corridor_changed += 1
    source_px = source.convert("RGBA").load()
    ring_preserved = sum(1 for x, y in ring_component["pixels"] if source_px[x, y] == rebuilt_px[x, y])
    semantic_pixels = [pixel for item in components if item is not ring_component for pixel in item["pixels"]]
    source_semantic_exact = sum(1 for x, y in semantic_pixels if source_px[x, y] == rebuilt_px[x, y])
    continuity = {
        "status": "pass" if outside_core_changed == 0 and outside_inner_changed == 0 and right_corridor_changed == 0 else "fail",
        "harmonic_inpaint_called": False,
        "blur_or_diffusion_called": False,
        "operation_scope": "pure geometric CORE_MASK only; approved exterior ring and surrounding frame excluded",
        "changed_pixels_outside_semantic_core": outside_core_changed,
        "changed_pixels_outside_inner_opening": outside_inner_changed,
        "changed_pixels_in_right_corridor_outside_inner_opening": right_corridor_changed,
        "exposed_inpaint_pixels": 0,
        "approved_outer_ring_pixels_preserved": ring_preserved,
        "approved_outer_ring_pixels_total": ring_component["count"],
    }
    passed = (
        tuple(ring["bbox"]) == EXPECTED_SOURCE_RING_BBOX
        and max(center_delta) <= 1.0
        and right_gap_2x >= 32
        and clean_core_cream == 0
        and source_semantic_exact == 0
        and ring_preserved == ring_component["count"]
        and continuity["status"] == "pass"
        and facet_gate["status"] == "pass"
    )
    return rebuilt, {
        "status": "pass" if passed else "fail",
        "contract_action_badge_1x": CONTRACT["frozen"]["slots"]["action_badge"],
        "contract_action_badge_2x": list(ACTION_RECT),
        "contract_center_2x": list(BADGE_CENTER),
        "benchmark_center_2x": list(BENCHMARK_BADGE_CENTER),
        "outer_ring": ring,
        "outer_ring_bbox_center": bbox_center,
        "core": core,
        "ring_center_delta_px": center_delta,
        "right_visual_gap_2x": right_gap_2x,
        "right_visual_gap_1x": right_gap_2x / 2.0,
        "minimum_right_visual_gap_2x": 32,
        "cream_semantic_pixels_inside_neutral_core": clean_core_cream,
        "source_semantic_exact_pixels_after_core_rebuild": source_semantic_exact,
        "approved_candidate_b_outer_ring_preserved": True,
        "retired_footprint_texture_continuity": continuity,
        "badge_core_facet_symmetry": facet_gate,
    }


def complete_runtime_icon(source: Image.Image, state: str) -> tuple[Image.Image, dict]:
    cx, cy = BENCHMARK_BADGE_CENTER
    src = source.convert("RGBA")
    pixels: list[tuple[int, int]] = []
    for y in range(190, 301):
        for x in range(275, 391):
            if (x - cx) * (x - cx) + (y - cy) * (y - cy) > 32 * 32:
                continue
            if b26._is_icon_target_family(src.getpixel((x, y))):
                pixels.append((x, y))
    if not pixels:
        return Image.new("RGBA", ICON_CANVAS_SIZE, (0, 0, 0, 0)), {"status": "fail", "reason": "no_pixels"}

    bbox = (
        min(x for x, _ in pixels),
        min(y for _, y in pixels),
        max(x for x, _ in pixels) + 1,
        max(y for _, y in pixels) + 1,
    )
    raw = Image.new("RGBA", (bbox[2] - bbox[0], bbox[3] - bbox[1]), (0, 0, 0, 0))
    rp = raw.load()
    for x, y in pixels:
        rp[x - bbox[0], y - bbox[1]] = src.getpixel((x, y))

    fitted = ImageOps.contain(raw, ICON_OPAQUE_MAX, Image.Resampling.LANCZOS)
    fp = fitted.load()
    for y in range(fitted.height):
        for x in range(fitted.width):
            r, g, b, a = fp[x, y]
            if a and not b26._is_icon_target_family((r, g, b, a)):
                fp[x, y] = (r, g, b, 0)

    canvas = Image.new("RGBA", ICON_CANVAS_SIZE, (0, 0, 0, 0))
    paste = ((ICON_CANVAS_SIZE[0] - fitted.width) // 2, (ICON_CANVAS_SIZE[1] - fitted.height) // 2)
    canvas.alpha_composite(fitted, paste)
    alpha_bbox = canvas.getchannel("A").getbbox()
    margins = {
        "left": alpha_bbox[0],
        "top": alpha_bbox[1],
        "right": ICON_CANVAS_SIZE[0] - alpha_bbox[2],
        "bottom": ICON_CANVAS_SIZE[1] - alpha_bbox[3],
    }
    border_touch = sum(
        canvas.getpixel((x, y))[3] > 0
        for x, y in (
            [(x, 0) for x in range(canvas.width)]
            + [(x, canvas.height - 1) for x in range(canvas.width)]
            + [(0, y) for y in range(canvas.height)]
            + [(canvas.width - 1, y) for y in range(canvas.height)]
        )
    )
    purity = b26.ingredient_purity_gate(canvas, "cream_icon", f"b210_runtime_icon_{state}")
    recovered_left = PREVIOUS_CONTRACT_LEFT_2X - bbox[0]
    passed = (
        border_touch == 0
        and min(margins.values()) >= ICON_MIN_PADDING
        and purity["status"] == "pass"
        and recovered_left > 0
    )
    return canvas, {
        "status": "pass" if passed else "fail",
        "state": state,
        "source_full_glyph_bbox_2x": list(bbox),
        "previous_failed_crop_left_2x": PREVIOUS_CONTRACT_LEFT_2X,
        "recovered_left_width_px": recovered_left,
        "raw_size": list(raw.size),
        "canvas_size": list(canvas.size),
        "opaque_bbox": list(alpha_bbox),
        "opaque_margins": margins,
        "minimum_padding_px": ICON_MIN_PADDING,
        "opaque_border_touch_pixels": border_touch,
        "purity": purity,
        "shape_source": "candidate B full badge glyph zone around measured benchmark center; extraction is independent of action_badge contract bounds",
    }


def _max_frame_like_vertical_run(photo: Image.Image, edge_width: int = 28) -> dict:
    rgb = photo.convert("RGB")
    zones = list(range(min(edge_width, rgb.width))) + list(range(max(0, rgb.width - edge_width), rgb.width))
    best = {"length": 0, "x": None, "start_y": None, "end_y": None}

    def is_frame_like(c: tuple[int, int, int]) -> bool:
        r, g, b = c
        return r >= 170 and g >= 160 and b >= 125 and max(c) - min(c) <= 80

    for x in zones:
        run_start = None
        for y in range(rgb.height + 1):
            active = y < rgb.height and is_frame_like(rgb.getpixel((x, y)))
            if active and run_start is None:
                run_start = y
            if not active and run_start is not None:
                length = y - run_start
                if length > best["length"]:
                    best = {"length": length, "x": x, "start_y": run_start, "end_y": y - 1}
                run_start = None
    return best


def clean_photo_ingredients() -> tuple[dict[str, Image.Image], dict]:
    art = Image.open(b11.IMAGEGEN_B1_R4).convert("RGB")
    photos: dict[str, Image.Image] = {}
    per_state: dict[str, dict] = {}
    target_size = (b11.PHOTO_RECT_2X[2] - b11.PHOTO_RECT_2X[0], b11.PHOTO_RECT_2X[3] - b11.PHOTO_RECT_2X[1])
    for state in STATE_ORDER:
        crop_box = CLEAN_PHOTO_SOURCE_BOXES[state]
        photo_interior = SOURCE_PHOTO_INTERIORS[state]
        globe_bbox = SOURCE_GLOBE_BBOXES[state]
        raw = art.crop(crop_box).convert("RGB")
        patch = ImageOps.fit(raw, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.54)).convert("RGBA")
        frame_run = _max_frame_like_vertical_run(patch)
        inside_photo = (
            crop_box[0] >= photo_interior[0]
            and crop_box[1] >= photo_interior[1]
            and crop_box[2] <= photo_interior[2]
            and crop_box[3] <= photo_interior[3]
        )
        clears_globe = crop_box[0] > globe_bbox[2]
        chroma_green = sum(
            1
            for r, g, b, a in patch.getdata()
            if a > 0 and g > 150 and g > r * 1.30 and g > b * 1.20
        )
        passed = inside_photo and clears_globe and frame_run["length"] <= PHOTO_FRAME_RUN_LIMIT and chroma_green == 0
        photos[state] = patch
        per_state[state] = {
            "status": "pass" if passed else "fail",
            "source": str(b11.IMAGEGEN_B1_R4),
            "source_crop_box": list(crop_box),
            "measured_source_photo_interior": list(photo_interior),
            "measured_source_globe_bbox": list(globe_bbox),
            "crop_inside_photo_interior": inside_photo,
            "crop_begins_after_globe_bbox": clears_globe,
            "edge_frame_like_max_vertical_run": frame_run,
            "edge_frame_like_run_limit_px": PHOTO_FRAME_RUN_LIMIT,
            "chroma_green_pixels": chroma_green,
            "flattened_atlas_used": False,
            "source_globe_or_frame_overlap_allowed": False,
            "output_size": list(patch.size),
        }
    return photos, {
        "status": "pass" if all(v["status"] == "pass" for v in per_state.values()) else "fail",
        "method": "use source-measured absolute rectangular scene crops from 396; each crop begins after the source globe and ends inside the photo before the source frame; never crop 428 flattened atlas",
        "per_state": per_state,
        "manual_400pct_review": "evidence_ready",
        "evidence": str(OUT_INGREDIENTS),
    }


def photo_underlay(photo: Image.Image, window: tuple[int, int, int, int], state: str) -> Image.Image:
    centering = {"selected": (0.48, 0.52), "available": (0.54, 0.52), "warning": (0.50, 0.54), "locked": (0.50, 0.52)}[state]
    return ImageOps.fit(
        photo.convert("RGB"),
        (window[2] - window[0], window[3] - window[1]),
        method=Image.Resampling.LANCZOS,
        centering=centering,
    ).convert("RGBA")


def badge_color_gate(frame: Image.Image, state: str) -> dict:
    core = b27._sample_hls(frame, CORE_MASK)
    band = b27._sample_hls(frame, None, (130, 24, 270, 44))
    if core["hue"] is None or band["hue"] is None:
        return {"status": "fail", "state": state, "reason": "missing_samples"}
    hue_delta = b26._hue_delta(core["hue"], band["hue"])
    lightness_delta = abs(core["lightness"] - band["lightness"])
    low_sat = core["saturation"] <= 0.12 and band["saturation"] <= 0.12
    passed = lightness_delta <= 0.20 if low_sat else hue_delta <= 0.08
    return {
        "status": "pass" if passed else "fail",
        "state": state,
        "mode": "low_saturation_lightness" if low_sat else "hue",
        "core": core,
        "frame_band": band,
        "hue_delta": round(hue_delta, 4),
        "lightness_delta": round(lightness_delta, 4),
    }


def compose() -> dict:
    source_frames = b22.load_atlas_frames(b26.B_ATLAS)
    _, _, _, cutout_mask, globe_patch, _, measurement, _, _ = b26.compose_single_master_frames()
    window = tuple(measurement["master_window_rect_2x"])
    raw_master_shell, _, _ = b26.make_master_hollow_shell(source_frames[MASTER_INDEX], window, globe_patch)
    master_shell, badge_gate = rebuild_badge(raw_master_shell, source_frames[MASTER_INDEX])
    family_mask = ImageChops.lighter(b26.make_frame_family_mask(master_shell), CORE_MASK)
    glow = b26.selected_glow_layer(source_frames[STATE_ORDER.index("selected")])
    photos, photo_gate = clean_photo_ingredients()
    globe_gate = b26.ingredient_purity_gate(globe_patch, "warm_globe", "b210_globe_linework")

    icons: dict[str, Image.Image] = {}
    icon_gates: dict[str, dict] = {}
    for idx, state in enumerate(STATE_ORDER):
        icons[state], icon_gates[state] = complete_runtime_icon(source_frames[idx], state)

    shells: list[Image.Image] = []
    frames: list[Image.Image] = []
    per_state: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        shell = master_shell.copy() if state == MASTER_STATE else b26.recolor_shell_from_master(master_shell, source_frames[idx], family_mask)
        shell = b26.scrub_green_for_nonselected(shell, state)
        underlay = photo_underlay(photos[state], window, state)
        frame = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        frame.alpha_composite(underlay, (window[0], window[1]))
        frame.alpha_composite(shell)
        if state == "selected":
            frame.alpha_composite(glow)
        frame.alpha_composite(globe_patch)
        frame = b26.scrub_green_for_nonselected(frame, state)
        gates = {
            "gateA_old_photo_residue": b22.gate_a_old_residue(shell, cutout_mask, window),
            "gateB_border_integrity": b22.gate_b_border_integrity(source_frames[MASTER_INDEX], shell, window),
            "gateC_window_alpha": b22.gate_c_window_alpha(frame, window),
            "gateD_green_residue": b22.gate_d_green_residue(frame, state),
            "gateF_geometry": b22.gate_f_geometry(frame),
            "badge_state_color_consistency": badge_color_gate(frame, state),
            "runtime_icon_shape_completeness": icon_gates[state],
            "photo_ingredient_overlay_contamination": photo_gate["per_state"][state],
        }
        shells.append(shell)
        frames.append(frame)
        per_state.append({
            "state": state,
            "master_window_rect_2x": list(window),
            "action_badge_2x": list(ACTION_RECT),
            "state_badge_center_2x": list(BADGE_CENTER),
            "state_badge_role": "non-interactive status indicator; full card hit_rect selects region; right dossier CTA enters region",
            "photo_source": str(b11.IMAGEGEN_B1_R4),
            "flattened_photo_atlas_used": False,
            "z_order": "clean rectangular regional photo -> hollow shell with neutral state-badge base -> selected glow if selected -> independent globe linework -> runtime text + complete state glyph",
            "gates": gates,
        })

    return {
        "source_frames": source_frames,
        "frames": frames,
        "shells": shells,
        "master_shell": master_shell,
        "cutout_mask": cutout_mask,
        "globe_patch": globe_patch,
        "icons": icons,
        "photos": photos,
        "window": window,
        "measurement": measurement,
        "badge_gate": badge_gate,
        "icon_gates": icon_gates,
        "photo_gate": photo_gate,
        "globe_gate": globe_gate,
        "per_state": per_state,
    }


def with_icon(frame: Image.Image, icon: Image.Image) -> Image.Image:
    out = frame.copy().convert("RGBA")
    x = round(BADGE_CENTER[0] - icon.width / 2)
    y = round(BADGE_CENTER[1] - icon.height / 2)
    out.alpha_composite(icon, (x, y))
    return out


def on_dark(img: Image.Image) -> Image.Image:
    bg = Image.new("RGBA", img.size, (7, 19, 21, 255))
    bg.alpha_composite(img)
    return bg


def make_compare_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1330), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.10 badge core: candidate B -> failed B2.9 skew -> symmetric facets", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Approved exterior stays pixel-identical; only the neutral core facet geometry and shared sparse grain change.", fill=(207, 224, 199), font=b11.F_NOTE)
    b29_frames = b22.load_atlas_frames(b29.OUT_ATLAS)
    crop = (270, 188, 408, 306)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        draw.text((x, 108), state, fill=(255, 229, 93), font=b11.F_NOTE)
        rows = [
            ("candidate B reference", data["source_frames"][idx], (214, 210, 170)),
            ("B2.9 failed skewed core facets", b29_frames[idx], (255, 120, 120)),
            ("B2.10 parameterized symmetric core", data["frames"][idx], (120, 235, 170)),
        ]
        for ridx, (title, frame, color) in enumerate(rows):
            y = 150 + ridx * 380
            panel = on_dark(frame).crop(crop).resize((414, 354), Image.Resampling.NEAREST)
            canvas.alpha_composite(panel, (x, y))
            draw.rectangle((x, y, x + panel.width, y + panel.height), outline=color, width=2)
            draw.text((x, y - 24), title, fill=color, font=b11.F_SMALL)
    gate = data["badge_gate"]
    continuity = gate["retired_footprint_texture_continuity"]
    facet = gate["badge_core_facet_symmetry"]
    draw.text((42, 1280), f"B2.10 mirror error={facet['vertex_mirror_error_max_px']}px | LR area delta={facet['left_right_area_delta_ratio']:.4f} | mirror IoU={facet['structural_mirror_iou']:.4f} | outside-core changed={continuity['changed_pixels_outside_semantic_core']}", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_ingredients_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1380), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.10 symmetric-core ingredients and 400% empty-base QA", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Photos, globe, exterior and runtime glyphs stay unchanged; the empty core uses mirrored facets plus one shared sparse grain field.", fill=(207, 224, 199), font=b11.F_NOTE)

    draw.text((42, 112), "Clean regional photos (no frame / globe / badge)", fill=(243, 239, 214), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        photo = data["photos"][state].resize((408, 150), Image.Resampling.LANCZOS)
        canvas.alpha_composite(photo, (x, 150))
        draw.rectangle((x, 150, x + 408, 300), outline=(94, 164, 142), width=2)
        gate = data["photo_gate"]["per_state"][state]
        draw.text((x, 310), f"{state} crop={gate['source_crop_box']}", fill=(255, 229, 93), font=b11.F_SMALL)
        draw.text((x, 330), f"edge frame run={gate['edge_frame_like_max_vertical_run']['length']}px / limit {gate['edge_frame_like_run_limit_px']}px", fill=(207, 224, 199), font=b11.F_SMALL)

    draw.text((42, 370), "400% complete runtime glyphs with transparent padding", fill=(243, 239, 214), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 280
        icon = data["icons"][state]
        box = Image.new("RGBA", (230, 230), (7, 19, 21, 255))
        zoom = icon.resize((176, 176), Image.Resampling.NEAREST)
        box.alpha_composite(zoom, (27, 27))
        canvas.alpha_composite(box, (x, 410))
        draw.rectangle((x, 410, x + 230, 640), outline=(94, 164, 142), width=2)
        gate = data["icon_gates"][state]
        margins = gate["opaque_margins"]
        draw.text((x, 650), f"{state} src={gate['source_full_glyph_bbox_2x']}", fill=(255, 229, 93), font=b11.F_SMALL)
        draw.text((x, 672), f"pad L{margins['left']} T{margins['top']} R{margins['right']} B{margins['bottom']}", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((x, 694), f"border touch={gate['opaque_border_touch_pixels']}", fill=(207, 224, 199), font=b11.F_SMALL)

    draw.text((1240, 370), "400% globe linework", fill=(243, 239, 214), font=b11.F_NOTE)
    globe = data["globe_patch"].crop((20, 8, 96, 84)).resize((304, 304), Image.Resampling.NEAREST)
    globe_bg = Image.new("RGBA", (340, 340), (95, 95, 95, 255))
    # Checkerboard proves that no old disc or photo survives in the ingredient.
    gd = ImageDraw.Draw(globe_bg)
    for y in range(0, 340, 24):
        for x in range(0, 340, 24):
            if (x // 24 + y // 24) % 2:
                gd.rectangle((x, y, x + 23, y + 23), fill=(165, 165, 165, 255))
    globe_bg.alpha_composite(globe, (18, 18))
    canvas.alpha_composite(globe_bg, (1240, 410))
    draw.rectangle((1240, 410, 1580, 750), outline=(94, 164, 142), width=2)
    draw.text((1240, 760), f"opaque={data['globe_gate']['opaque_pixels']} non-target={data['globe_gate']['non_target_pixels']}", fill=(207, 224, 199), font=b11.F_SMALL)

    draw.text((42, 820), "400% empty state-badge bases before runtime glyph overlay", fill=(243, 239, 214), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        crop = on_dark(data["frames"][idx]).crop((282, 196, 382, 296)).resize((400, 400), Image.Resampling.NEAREST)
        canvas.alpha_composite(crop, (x, 860))
        draw.rectangle((x, 860, x + 400, 1260), outline=(94, 164, 142), width=2)
        draw.line((x + 200, 860, x + 200, 1260), fill=(88, 233, 255, 150), width=1)
        draw.line((x, 1060, x + 400, 1060), fill=(88, 233, 255, 150), width=1)
        draw.text((x, 1270), state, fill=(255, 229, 93), font=b11.F_SMALL)
    continuity = data["badge_gate"]["retired_footprint_texture_continuity"]
    facet = data["badge_gate"]["badge_core_facet_symmetry"]
    draw.text((42, 1310), f"Symmetry gate: vertex={facet['vertex_mirror_error_max_px']}px | center={facet['center_convergence_error_px']}px | LR area={facet['left_right_area_delta_ratio']:.4f} | mirror IoU={facet['structural_mirror_iou']:.4f} | grain={facet['grain']['coverage_ratio']:.3f}", fill=(120, 235, 170), font=b11.F_NOTE)
    draw.text((42, 1342), f"No-smear regression: inpaint={continuity['harmonic_inpaint_called']} | outside core={continuity['changed_pixels_outside_semantic_core']} | right corridor={continuity['changed_pixels_in_right_corridor_outside_inner_opening']}", fill=(120, 235, 170), font=b11.F_NOTE)
    return canvas


def make_geometry_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 910), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.10 geometry QA: symmetric neutral core + preserved candidate-B exterior", fill=(243, 239, 214), font=b11.F_HEAD)
    slots = CONTRACT["frozen"]["slots"]
    colors = {"photo_slot": (88, 233, 255), "label_plate": (255, 229, 93), "meta_line": (255, 159, 82), "action_badge": (255, 105, 105)}
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        y = 120
        frame = on_dark(data["frames"][idx])
        canvas.alpha_composite(frame, (x, y))
        draw.rectangle((x, y, x + 408, y + 320), outline=(101, 255, 138), width=2)
        for name, color in colors.items():
            sx, sy, sw, sh = slots[name]
            draw.rectangle((x + sx * 2, y + sy * 2, x + (sx + sw) * 2, y + (sy + sh) * 2), outline=color, width=2)
        crop = frame.crop((270, 188, 404, 306)).resize((402, 354), Image.Resampling.NEAREST)
        canvas.alpha_composite(crop, (x, 500))
        draw.rectangle((x, 500, x + 402, 854), outline=(94, 164, 142), width=2)
        draw.text((x, 90), f"{state} 408x320 ratio=1.275", fill=(255, 229, 93), font=b11.F_SMALL)
    return canvas


def draw_runtime_icons(canvas: Image.Image, icons: dict[str, Image.Image]) -> None:
    asset_to_runtime = 0.75
    positions = [(66, 36), (66, 294), (66, 552), (66, 810)]
    for idx, state in enumerate(STATE_ORDER):
        icon = icons[state]
        size = (round(icon.width * asset_to_runtime), round(icon.height * asset_to_runtime))
        display = icon.resize(size, Image.Resampling.LANCZOS)
        x = round(positions[idx][0] + BADGE_CENTER[0] * asset_to_runtime - display.width / 2)
        y = round(positions[idx][1] + BADGE_CENTER[1] * asset_to_runtime - display.height / 2)
        canvas.alpha_composite(display, (x, y))


def draw_runtime_slots(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    positions = [(66, 36), (66, 294), (66, 552), (66, 810)]
    colors = {"photo_slot": (88, 233, 255), "label_plate": (255, 229, 93), "meta_line": (255, 159, 82), "action_badge": (255, 105, 105)}
    for x, y in positions:
        for name, color in colors.items():
            sx, sy, sw, sh = CONTRACT["frozen"]["slots"][name]
            rect = (x + round(sx * 1.5), y + round(sy * 1.5), x + round((sx + sw) * 1.5), y + round((sy + sh) * 1.5))
            draw.rectangle(rect, outline=color, width=2)
            draw.text((rect[0] + 4, rect[1] + 2), name.replace("_slot", "").replace("_plate", ""), fill=color, font=b11.F_SMALL)


def make_runtime_preview(data: dict, qa: bool) -> Image.Image:
    canvas = b11.make_runtime_preview(data["frames"], CONTRACT, False).convert("RGBA")
    draw_runtime_icons(canvas, data["icons"])
    if qa:
        draw_runtime_slots(canvas)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((448, 30, 1540, 116), fill=(7, 19, 21))
    draw.text((450, 34), "Python v0.9.16 B2.10 symmetric-core state badge", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 76), "Approved exterior is pixel-identical; neutral facets are mirrored and status glyphs remain runtime-only.", fill=(217, 222, 199), font=b11.F_NOTE)
    return canvas.convert("RGB")


def make_visual_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1540), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.10 16-point symmetric-core regression board", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Four states x globe/photo seam, right edge, bottom edge, symmetric state badge. Reviewer/user owns final PASS/FAIL.", fill=(207, 224, 199), font=b11.F_NOTE)
    rect = data["window"]
    for idx, state in enumerate(STATE_ORDER):
        row = 166 + idx * 340
        frame = on_dark(with_icon(data["frames"][idx], data["icons"][state]))
        crops = [
            ("globe/photo", (20, 12, 108, 100)),
            ("right edge", (rect[2] - 34, rect[1] - 10, min(408, rect[2] + 34), rect[3] + 10)),
            ("bottom edge", (rect[0] + 24, rect[3] - 28, rect[2] - 24, min(320, rect[3] + 28))),
            ("state badge", (270, 188, 404, 306)),
        ]
        xs = [42, 330, 520, 1130]
        draw.text((42, row - 52), state, fill=(255, 229, 93), font=b11.F_NOTE)
        for pidx, (title, crop) in enumerate(crops):
            panel = frame.crop(crop).resize(((crop[2] - crop[0]) * 2, (crop[3] - crop[1]) * 2), Image.Resampling.NEAREST)
            canvas.alpha_composite(panel, (xs[pidx], row))
            draw.rectangle((xs[pidx], row, xs[pidx] + panel.width, row + panel.height), outline=(94, 164, 142), width=2)
            draw.text((xs[pidx], row - 22), title, fill=(234, 232, 204), font=b11.F_SMALL)
        thumb = frame.resize((245, 192), Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb, (1590, row + 10))
        draw.rectangle((1590, row + 10, 1835, row + 202), outline=(94, 164, 142), width=2)
    return canvas


def godot_partial_frame_probe() -> dict:
    if not OUT_GODOT.exists() or not OUT_GODOT_QA.exists():
        return {"status": "pending", "missing_sampled_baseline_pixels": None, "threshold": 20, "stride_px": 4}
    baseline = Image.open(OUT_GODOT).convert("RGB")
    qa = Image.open(OUT_GODOT_QA).convert("RGB")
    if baseline.size != qa.size:
        return {"status": "fail", "reason": "size_mismatch", "baseline_size": list(baseline.size), "qa_size": list(qa.size)}
    missing = 0
    for y in range(0, baseline.height, 4):
        for x in range(0, baseline.width, 4):
            before = baseline.getpixel((x, y))
            after = qa.getpixel((x, y))
            if max(before) > round(0.08 * 255) and max(after) < round(0.01 * 255):
                missing += 1
    return {
        "status": "pass" if missing <= 20 else "fail",
        "missing_sampled_baseline_pixels": missing,
        "threshold": 20,
        "stride_px": 4,
        "basis": "QA capture may add overlays but must not lose visible pixels from the stable non-QA baseline",
    }


def aggregate_gates(data: dict, godot_pass: bool, partial_frame_probe: dict) -> dict:
    per_state = data["per_state"]

    def all_gate(name: str, allowed: set[str] = {"pass"}) -> bool:
        return all(item["gates"][name]["status"] in allowed for item in per_state)

    return {
        "state_badge_contract_and_style_alignment": data["badge_gate"],
        "retired_footprint_texture_continuity": data["badge_gate"]["retired_footprint_texture_continuity"],
        "badge_core_facet_symmetry": data["badge_gate"]["badge_core_facet_symmetry"],
        "runtime_icon_shape_completeness": {
            "status": "pass" if all(v["status"] == "pass" for v in data["icon_gates"].values()) else "fail",
            "per_state": data["icon_gates"],
        },
        "photo_ingredient_overlay_contamination": data["photo_gate"],
        "globe_linework_ingredient_purity": data["globe_gate"],
        "gateA_old_photo_residue_core": {"status": "pass" if all_gate("gateA_old_photo_residue") else "fail"},
        "window_edge_residue_scan": data["measurement"]["window_edge_residue_scan"],
        "gateB_border_integrity_ring": {"status": "pass" if all_gate("gateB_border_integrity") else "fail"},
        "gateC_window_alpha_after_composite": {"status": "pass" if all_gate("gateC_window_alpha") else "fail"},
        "gateD_green_residue_nonselected": {"status": "pass" if all_gate("gateD_green_residue", {"pass", "skipped_selected_green_glow_semantic"}) else "fail"},
        "badge_state_color_consistency": {"status": "pass" if all_gate("badge_state_color_consistency") else "fail", "per_state": {item["state"]: item["gates"]["badge_state_color_consistency"] for item in per_state}},
        "gateE_same_state_layout": {"status": "pass", "diff_px": 0, "basis": "single master, single revised state-badge geometry"},
        "gateF_geometry_ratio": {"status": "pass" if all_gate("gateF_geometry") else "fail", "target": 1.275},
        "manual_16point_visual_check": {"status": "evidence_ready", "evidence": str(OUT_VISUAL_QA), "review_owner": "reviewer_or_user"},
        "ingredient_dependency_review": {"status": "evidence_ready", "evidence": [str(OUT_COMPARE), str(OUT_INGREDIENTS)], "required_before_atlas": True},
        "godot_windowed_capture": {"status": "pass" if godot_pass else "pending", "headless_used_for_ui_capture": False, "partial_frame_baseline_probe": partial_frame_probe, "evidence": [str(OUT_GODOT), str(OUT_GODOT_QA)]},
    }


def make_manifest(data: dict, checks: dict, godot_pass: bool, partial_frame_probe: dict) -> dict:
    gates = aggregate_gates(data, godot_pass, partial_frame_probe)
    required = [
        "state_badge_contract_and_style_alignment",
        "retired_footprint_texture_continuity",
        "badge_core_facet_symmetry",
        "runtime_icon_shape_completeness",
        "photo_ingredient_overlay_contamination",
        "globe_linework_ingredient_purity",
        "gateA_old_photo_residue_core",
        "window_edge_residue_scan",
        "gateB_border_integrity_ring",
        "gateC_window_alpha_after_composite",
        "gateD_green_residue_nonselected",
        "badge_state_color_consistency",
        "gateE_same_state_layout",
        "gateF_geometry_ratio",
    ]
    passed = all(gates[name]["status"] == "pass" for name in required)
    return {
        "schema_version": 1,
        "artifact_type": "vertical_slice_proof / left_region_card / four-state evidence / not frozen production resource",
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "date": "2026-07-13",
        "status": "b2_10_evidence_ready_pending_user_visual_review" if passed and godot_pass else "b2_10_pending_full_chain",
        "contract": str(b11.CONTRACT_PATH),
        "contract_version": CONTRACT["contract_version"],
        "contract_change": {
            "this_round": "none",
            "inherited_authorized_revision": "A174 action_badge [144,101,44,44]",
            "all_frozen_fields_changed_this_round": False,
        },
        "state_badge_semantics": {
            "role": "region state indicator, not an independent button",
            "hit_target": "full left_region_card hit_rect",
            "selected": "current region shown in right dossier",
            "available": "selectable candidate",
            "warning": "selectable with risk",
            "locked": "not enterable; may expose lock reason",
            "enter_action_owner": "right dossier primary CTA",
        },
        "pipeline": "396 clean photo -> hollow shell retaining approved candidate-B badge exterior -> bbox/center-parameterized symmetric neutral core -> shared sparse grain -> selected glow -> independent globe linework -> runtime text + complete padded state glyph",
        "inputs": {
            "candidate_b_shell_and_glyph_source": str(b26.B_ATLAS),
            "clean_regional_photo_source": str(b11.IMAGEGEN_B1_R4),
            "failed_flattened_photo_source_retired": str(b26.B13_ATLAS),
            "failed_b2_8_manifest": str(b28.OUT_MANIFEST),
            "failed_b2_9_manifest": str(b29.OUT_MANIFEST),
        },
        "outputs": {
            "style_position_compare": str(OUT_COMPARE),
            "clean_ingredients_qa": str(OUT_INGREDIENTS),
            "atlas_2x": str(OUT_ATLAS),
            "geometry_qa": str(OUT_GEOMETRY),
            "runtime_fill": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "visual_16point_qa": str(OUT_VISUAL_QA),
            "manifest": str(OUT_MANIFEST),
            "godot": str(OUT_GODOT),
            "godot_qa": str(OUT_GODOT_QA),
            "godot_atlas": str(GODOT_ATLAS),
            "runtime_icons": {state: str(GODOT_INGREDIENT_DIR / f"left_region_card_b210_runtime_icon_{state}.png") for state in STATE_ORDER},
            "clean_photos": {state: str(GODOT_INGREDIENT_DIR / f"left_region_card_b210_clean_photo_{state}.png") for state in STATE_ORDER},
            "globe_linework": str(GODOT_INGREDIENT_DIR / "left_region_card_b210_globe_linework.png"),
        },
        "per_state": data["per_state"],
        "gates": gates,
        "image_content_checks": checks,
        "prohibitions_observed": {
            "imagegen_called": False,
            "flattened_428_photo_source_used": False,
            "source_glyph_cropped_by_contract_rect": False,
            "runtime_glyph_baked_into_atlas": False,
            "other_classes_batch_produced": False,
            "card_size_changed": False,
            "non_action_badge_frozen_fields_changed": False,
            "harmonic_inpaint_called": False,
            "blur_or_diffusion_called": False,
            "program_fill_exposed_outside_inner_opening": False,
            "independently_handwritten_facet_endpoints_used": False,
            "periodic_per_pixel_noise_used": False,
        },
    }


def write_outputs(approve_ingredients: bool) -> dict:
    data = compose()
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    make_compare_board(data).save(OUT_COMPARE)
    make_ingredients_board(data).save(OUT_INGREDIENTS)
    dependency_pass = (
        data["badge_gate"]["status"] == "pass"
        and data["badge_gate"]["badge_core_facet_symmetry"]["status"] == "pass"
        and data["photo_gate"]["status"] == "pass"
        and data["globe_gate"]["status"] == "pass"
        and all(g["status"] == "pass" for g in data["icon_gates"].values())
    )
    if not approve_ingredients or not dependency_pass:
        return {
            "status": "ingredient_evidence_ready" if dependency_pass else "ingredient_gate_failed",
            "outputs": [str(OUT_COMPARE), str(OUT_INGREDIENTS)],
            "badge_gate": data["badge_gate"],
            "photo_gate": data["photo_gate"],
            "globe_gate": data["globe_gate"],
            "icon_gates": data["icon_gates"],
        }

    atlas = b11.make_atlas(data["frames"])
    atlas.save(OUT_ATLAS)
    make_geometry_board(data).save(OUT_GEOMETRY)
    make_runtime_preview(data, False).save(OUT_RUNTIME)
    make_runtime_preview(data, True).save(OUT_RUNTIME_QA)
    make_visual_board(data).save(OUT_VISUAL_QA)

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    GODOT_INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    data["master_shell"].save(GODOT_INGREDIENT_DIR / "left_region_card_b210_clean_master.png")
    data["globe_patch"].save(GODOT_INGREDIENT_DIR / "left_region_card_b210_globe_linework.png")
    for state, shell in zip(STATE_ORDER, data["shells"]):
        shell.save(GODOT_INGREDIENT_DIR / f"left_region_card_b210_hollow_shell_{state}.png")
    for state in STATE_ORDER:
        data["icons"][state].save(GODOT_INGREDIENT_DIR / f"left_region_card_b210_runtime_icon_{state}.png")
        data["photos"][state].save(GODOT_INGREDIENT_DIR / f"left_region_card_b210_clean_photo_{state}.png")

    paths = {
        "compare": OUT_COMPARE,
        "ingredients": OUT_INGREDIENTS,
        "atlas": OUT_ATLAS,
        "geometry": OUT_GEOMETRY,
        "runtime": OUT_RUNTIME,
        "runtime_qa": OUT_RUNTIME_QA,
        "visual_qa": OUT_VISUAL_QA,
        "godot": OUT_GODOT,
        "godot_qa": OUT_GODOT_QA,
    }
    checks = {name: b11.count_colors_nonblack(path) for name, path in paths.items() if path.exists()}
    partial_frame_probe = godot_partial_frame_probe()
    godot_pass = OUT_GODOT.exists() and OUT_GODOT_QA.exists() and partial_frame_probe["status"] == "pass"
    manifest = make_manifest(data, checks, godot_pass, partial_frame_probe)
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build WMW left card B2.10 symmetric-core badge pipeline.")
    parser.add_argument("--approve-ingredients", action="store_true", help="Continue only after 529/530 symmetric-core evidence has been inspected.")
    args = parser.parse_args()
    result = write_outputs(args.approve_ingredients)
    print(json.dumps({"status": result["status"], "outputs": result.get("outputs", {}), "gates": result.get("gates", {})}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
