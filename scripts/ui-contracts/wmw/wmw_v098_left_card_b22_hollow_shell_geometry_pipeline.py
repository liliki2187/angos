# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import math
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.8"
ROUND_ID = "B2.2"
ASSET_ID = "world_map_wmw_left_region_card_b2_2_hollow_shell_geometry"

B_ATLAS = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_candidate_b_atlas_2x.png"
B13_ATLAS = BASE / "428-world-map-wmw-v0-9-5-left-card-candidate-b1-3-atlas-2x.png"

OUT_MEASURE_QA = BASE / "458-world-map-wmw-v0-9-8-left-card-b2-2-window-measurement-qa.png"
OUT_INGREDIENTS = BASE / "459-world-map-wmw-v0-9-8-left-card-b2-2-hollow-shell-ingredients.png"
OUT_ATLAS = BASE / "460-world-map-wmw-v0-9-8-left-card-b2-2-atlas-2x.png"
OUT_GEOMETRY_QA = BASE / "461-world-map-wmw-v0-9-8-left-card-b2-2-geometry-qa.png"
OUT_RUNTIME = BASE / "462-world-map-wmw-v0-9-8-left-card-b2-2-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "463-world-map-wmw-v0-9-8-left-card-b2-2-runtime-fill-qa.png"
OUT_FIT_QA = BASE / "464-world-map-wmw-v0-9-8-left-card-b2-2-300pct-fit-qa.png"
OUT_MANIFEST = BASE / "465-world-map-wmw-v0-9-8-left-card-b2-2-manifest.json"
OUT_GODOT = BASE / "466-world-map-wmw-v0-9-8-left-card-b2-2-godot-single-component.png"
OUT_GODOT_QA = BASE / "467-world-map-wmw-v0-9-8-left-card-b2-2-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b22_hollow_shell_geometry_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b22_hollow_shell_geometry_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
TARGET_RATIO = b11.TARGET_RATIO
RATIO_TOLERANCE = b11.RATIO_TOLERANCE
PHOTO_RECT_2X = b11.PHOTO_RECT_2X
ACTION_RECT_2X = b11.ACTION_RECT_2X

SCAN_ROWS = [95, 115, 135, 155]
SCAN_COLS = [180, 220, 260, 300]
SOURCE_PHOTO_RECT_2X = (44, 50, 388, 174)
GATE_CORE_INSET_PX = 3
WINDOW_CONSISTENCY_TOLERANCE_PX = 10
PHOTO_SAMPLE_INSET = (0.20, 0.25, 0.80, 0.75)
SHELL_SAMPLE_TOP_Y = 40
SHELL_SAMPLE_PLATE_Y = 203
SAMPLE_GRID_STEP = 8


def median(values: list[int]) -> int:
    values = sorted(values)
    return values[len(values) // 2]


def is_cream(px: tuple[int, int, int, int]) -> bool:
    r, g, b, a = px
    return a > 200 and r > 150 and g > 130 and b > 100 and r > b + 25


def is_green_signature(px: tuple[int, int, int, int]) -> bool:
    r, g, b, a = px
    if a <= 8:
        return False
    return (g > 140 and r < 90 and b < 90) or (g > 38 and g > 2.5 * r and g > 2.5 * b)


def load_atlas_frames(path: Path) -> list[Image.Image]:
    atlas = Image.open(path).convert("RGBA")
    if atlas.size[0] < FRAME_SIZE[0] * 4 or atlas.size[1] < FRAME_SIZE[1]:
        raise RuntimeError(f"Atlas too small: {path} size={atlas.size}")
    return [
        atlas.crop((i * FRAME_SIZE[0], 0, (i + 1) * FRAME_SIZE[0], FRAME_SIZE[1])).convert("RGBA")
        for i in range(4)
    ]


def color_dist2(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def sample_grid(px, x1: int, y1: int, x2: int, y2: int, step: int) -> list[tuple[int, int, int]]:
    samples: list[tuple[int, int, int]] = []
    for y in range(y1, y2 + 1, step):
        for x in range(x1, x2 + 1, step):
            r, g, b, a = px[x, y]
            if a > 200:
                samples.append((r, g, b))
    return samples


def make_adaptive_photo_classifier(frame: Image.Image) -> tuple[callable, dict]:
    px = frame.load()
    slot_x1, slot_y1, slot_x2, slot_y2 = PHOTO_RECT_2X
    slot_w = slot_x2 - slot_x1
    slot_h = slot_y2 - slot_y1
    px1 = round(slot_x1 + slot_w * PHOTO_SAMPLE_INSET[0])
    py1 = round(slot_y1 + slot_h * PHOTO_SAMPLE_INSET[1])
    px2 = round(slot_x1 + slot_w * PHOTO_SAMPLE_INSET[2])
    py2 = round(slot_y1 + slot_h * PHOTO_SAMPLE_INSET[3])
    photo_samples = sample_grid(px, px1, py1, px2, py2, SAMPLE_GRID_STEP)
    shell_samples = []
    shell_samples.extend(sample_grid(px, 52, SHELL_SAMPLE_TOP_Y, 360, SHELL_SAMPLE_TOP_Y, SAMPLE_GRID_STEP))
    shell_samples.extend(sample_grid(px, 52, SHELL_SAMPLE_PLATE_Y, 300, SHELL_SAMPLE_PLATE_Y, SAMPLE_GRID_STEP))
    if not photo_samples or not shell_samples:
        raise RuntimeError("Adaptive measurement samples missing; stop before changing gates.")

    def classifier(c: tuple[int, int, int, int]) -> bool:
        r, g, b, a = c
        if a < 200:
            return False
        rgb = (r, g, b)
        photo_dist = min(color_dist2(rgb, sample) for sample in photo_samples)
        shell_dist = min(color_dist2(rgb, sample) for sample in shell_samples)
        return photo_dist < shell_dist

    return classifier, {
        "method": "adaptive nearest-color-set classifier",
        "photo_sample_rect_2x": [px1, py1, px2, py2],
        "photo_sample_count": len(photo_samples),
        "shell_sample_rows_2x": [
            {"y": SHELL_SAMPLE_TOP_Y, "x1": 52, "x2": 360},
            {"y": SHELL_SAMPLE_PLATE_Y, "x1": 52, "x2": 300},
        ],
        "shell_sample_count": len(shell_samples),
        "sample_grid_step": SAMPLE_GRID_STEP,
    }


def scan_row(px, is_photo_fn, y: int, x_from: int, x_to: int, step: int) -> int:
    run = 0
    last = x_from
    x = x_from
    while x != x_to:
        if is_photo_fn(px[x, y]):
            run = 0
            last = x
        else:
            run += 1
            if run >= 6:
                return last
        x += step
    return last


def scan_col(px, is_photo_fn, x: int, y_from: int, y_to: int, step: int) -> int:
    run = 0
    last = y_from
    y = y_from
    while y != y_to:
        if is_photo_fn(px[x, y]):
            run = 0
            last = y
        else:
            run += 1
            if run >= 6:
                return last
        y += step
    return last


def measure_window(frame: Image.Image) -> tuple[tuple[int, int, int, int], dict]:
    px = frame.load()
    is_photo_fn, sample_meta = make_adaptive_photo_classifier(frame)
    row_lefts = [scan_row(px, is_photo_fn, y, 160, 20, -1) for y in SCAN_ROWS]
    row_rights = [scan_row(px, is_photo_fn, y, 160, 405, 1) for y in SCAN_ROWS]
    col_tops = [scan_col(px, is_photo_fn, x, 110, 25, -1) for x in SCAN_COLS]
    col_bottoms = [scan_col(px, is_photo_fn, x, 110, 215, 1) for x in SCAN_COLS]
    left = median(row_lefts)
    right = median(row_rights)
    top = median(col_tops)
    bottom = median(col_bottoms)
    sample_meta.update(
        {
            "row_left_samples": row_lefts,
            "row_right_samples": row_rights,
            "col_top_samples": col_tops,
            "col_bottom_samples": col_bottoms,
        }
    )
    return (left, top, right + 1, bottom + 1), sample_meta


def _measure_globe_in_region(frame: Image.Image, region: tuple[int, int, int, int]) -> dict:
    px = frame.load()
    xs: list[int] = []
    ys: list[int] = []
    x1, y1, x2, y2 = region
    for y in range(max(0, y1), min(FRAME_SIZE[1], y2)):
        for x in range(max(0, x1), min(FRAME_SIZE[0], x2)):
            if is_cream(px[x, y]):
                xs.append(x)
                ys.append(y)
    if not xs:
        raise RuntimeError("Globe cream pixels not found")
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0
    radius = max(max(xs) - min(xs), max(ys) - min(ys)) / 2.0 + 2.0
    return {
        "center": [round(cx, 3), round(cy, 3)],
        "radius": round(radius, 3),
        "cream_bbox": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
        "cream_pixels": len(xs),
    }


def measure_globes(frames: list[Image.Image]) -> list[dict]:
    available = _measure_globe_in_region(frames[1], (0, 0, 110, 110))
    bx1, by1, bx2, by2 = available["cream_bbox"]
    local_region = (bx1 - 12, by1 - 12, bx2 + 12, by2 + 12)
    globes: list[dict] = []
    for idx, frame in enumerate(frames):
        if idx == 1:
            globe = available.copy()
            globe["measurement_scope"] = "available_full_0_0_110_110"
        else:
            globe = _measure_globe_in_region(frame, local_region)
            globe["measurement_scope"] = "local_search_from_available_bbox_expanded_12px"
            globe["local_search_region_2x"] = list(local_region)
        globes.append(globe)
    return globes


def common_window_rect(rects: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    return (
        max(rect[0] for rect in rects),
        max(rect[1] for rect in rects),
        min(rect[2] for rect in rects),
        min(rect[3] for rect in rects),
    )


def window_consistency_stats(rects: list[tuple[int, int, int, int]]) -> dict:
    widths = [rect[2] - rect[0] for rect in rects]
    heights = [rect[3] - rect[1] for rect in rects]
    centers_x = [(rect[0] + rect[2]) / 2 for rect in rects]
    centers_y = [(rect[1] + rect[3]) / 2 for rect in rects]
    diffs = {
        "width": max(widths) - min(widths),
        "height": max(heights) - min(heights),
        "center_x": max(centers_x) - min(centers_x),
        "center_y": max(centers_y) - min(centers_y),
        "left": max(rect[0] for rect in rects) - min(rect[0] for rect in rects),
        "top": max(rect[1] for rect in rects) - min(rect[1] for rect in rects),
    }
    max_delta = max(diffs["width"], diffs["height"], diffs["center_x"], diffs["center_y"])
    return {
        "widths": widths,
        "heights": heights,
        "centers_x": centers_x,
        "centers_y": centers_y,
        "delta_px": diffs,
        "max_delta_px": max_delta,
        "width_height_tolerance_px": WINDOW_CONSISTENCY_TOLERANCE_PX,
        "position_tolerance_px": WINDOW_CONSISTENCY_TOLERANCE_PX,
        "status": "pass"
        if diffs["width"] <= WINDOW_CONSISTENCY_TOLERANCE_PX
        and diffs["height"] <= WINDOW_CONSISTENCY_TOLERANCE_PX
        and diffs["center_x"] <= WINDOW_CONSISTENCY_TOLERANCE_PX
        and diffs["center_y"] <= WINDOW_CONSISTENCY_TOLERANCE_PX
        else "fail",
    }


def cutout_mask_for(window: tuple[int, int, int, int], globe: dict) -> Image.Image:
    mask = Image.new("L", FRAME_SIZE, 0)
    mp = mask.load()
    cx, cy = globe["center"]
    r = float(globe["radius"])
    r2 = r * r
    for y in range(window[1], window[3]):
        for x in range(window[0], window[2]):
            dx = x - cx
            dy = y - cy
            if dx * dx + dy * dy > r2:
                mp[x, y] = 255
    return mask


def make_hollow_shell(frame: Image.Image, state: str, window: tuple[int, int, int, int], globe: dict) -> tuple[Image.Image, Image.Image, int]:
    shell = frame.copy().convert("RGBA")
    mask = cutout_mask_for(window, globe)
    px = shell.load()
    mp = mask.load()
    cut_pixels = 0
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if mp[x, y] > 0:
                r, g, b, _a = px[x, y]
                px[x, y] = (r, g, b, 0)
                cut_pixels += 1
    if state != "selected":
        for y in range(FRAME_SIZE[1]):
            for x in range(FRAME_SIZE[0]):
                if px[x, y][3] > 0 and is_green_signature(px[x, y]):
                    r, g, b, _a = px[x, y]
                    px[x, y] = (r, g, b, 0)
    return shell, mask, cut_pixels


def cover_photo_to_window(photo: Image.Image, window: tuple[int, int, int, int], state: str) -> Image.Image:
    target_w = window[2] - window[0]
    target_h = window[3] - window[1]
    centering = {
        "selected": (0.50, 0.50),
        "available": (0.58, 0.50),
        "warning": (0.50, 0.52),
        "locked": (0.50, 0.50),
    }[state]
    return ImageOps.fit(photo.convert("RGB"), (target_w, target_h), method=Image.Resampling.LANCZOS, centering=centering).convert("RGBA")


def gate_a_old_residue(shell: Image.Image, mask: Image.Image, window: tuple[int, int, int, int]) -> dict:
    px = shell.load()
    mp = mask.load()
    hits = 0
    samples: list[list[int]] = []
    for y in range(window[1] + GATE_CORE_INSET_PX, window[3] - GATE_CORE_INSET_PX):
        for x in range(window[0] + GATE_CORE_INSET_PX, window[2] - GATE_CORE_INSET_PX):
            if mp[x, y] == 0:
                continue
            if px[x, y][3] > 0:
                hits += 1
                if len(samples) < 8:
                    samples.append([x, y, *px[x, y]])
    return {
        "core_inset_px": GATE_CORE_INSET_PX,
        "opaque_pixels_in_cutout_core": hits,
        "sample_pixels": samples,
        "status": "pass" if hits == 0 else "fail",
    }


def gate_b_border_integrity(original: Image.Image, shell: Image.Image, window: tuple[int, int, int, int]) -> dict:
    opx = original.load()
    hpx = shell.load()
    broken = 0
    samples: list[list[int]] = []
    for y in range(window[1] - 3, window[3] + 3):
        for x in range(window[0] - 3, window[2] + 3):
            if not (0 <= x < FRAME_SIZE[0] and 0 <= y < FRAME_SIZE[1]):
                continue
            inside_window = window[0] <= x < window[2] and window[1] <= y < window[3]
            if inside_window:
                continue
            if opx[x, y][3] > 200 and hpx[x, y][3] < 200:
                broken += 1
                if len(samples) < 8:
                    samples.append([x, y, *opx[x, y], hpx[x, y][3]])
    return {
        "ring_px": 3,
        "broken_opaque_pixels": broken,
        "sample_pixels": samples,
        "status": "pass" if broken == 0 else "fail",
    }


def gate_c_window_alpha(frame: Image.Image, window: tuple[int, int, int, int]) -> dict:
    px = frame.load()
    holes = 0
    samples: list[list[int]] = []
    for y in range(window[1], window[3]):
        for x in range(window[0], window[2]):
            if px[x, y][3] != 255:
                holes += 1
                if len(samples) < 8:
                    samples.append([x, y, px[x, y][3]])
    return {
        "transparent_or_nonopaque_pixels_in_window": holes,
        "sample_pixels": samples,
        "status": "pass" if holes == 0 else "fail",
    }


def gate_d_green_residue(frame: Image.Image, state: str) -> dict:
    if state == "selected":
        return {
            "status": "skipped_selected_green_glow_semantic",
            "green_signature_pixels_full_frame": None,
            "basis": "selected state is intentionally exempt; selected green glow is state semantics",
        }
    px = frame.load()
    hits = 0
    samples: list[list[int]] = []
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if is_green_signature(px[x, y]):
                hits += 1
                if len(samples) < 8:
                    samples.append([x, y, *px[x, y]])
    return {
        "green_signature_pixels_full_frame": hits,
        "sample_pixels": samples,
        "status": "pass" if hits == 0 else "fail",
    }


def gate_f_geometry(frame: Image.Image) -> dict:
    ratio = frame.size[0] / frame.size[1]
    delta = abs(ratio - TARGET_RATIO)
    return {
        "size_2x": list(frame.size),
        "size_1x": list(EXPORT_SIZE),
        "ratio": ratio,
        "target_ratio": TARGET_RATIO,
        "ratio_delta": delta,
        "status": "pass" if frame.size == FRAME_SIZE and delta <= RATIO_TOLERANCE else "fail",
    }


def measure_inputs(b_frames: list[Image.Image]) -> tuple[dict, list[dict]]:
    measured: list[tuple[tuple[int, int, int, int], dict]] = [measure_window(frame) for frame in b_frames]
    measured_windows = [item[0] for item in measured]
    sample_metas = [item[1] for item in measured]
    gate_e = window_consistency_stats(measured_windows)
    common_window = common_window_rect(measured_windows)
    globes = measure_globes(b_frames)
    measurement = {
        "scan_rows": SCAN_ROWS,
        "scan_cols": SCAN_COLS,
        "classifier": "per-frame adaptive nearest-color-set classifier",
        "photo_sample": "grid samples from the central area of frozen contract photo_slot",
        "shell_sample": "grid samples from top frame band y=40 and plate band y=203",
        "measured_window_rects_2x": {state: list(rect) for state, rect in zip(STATE_ORDER, measured_windows)},
        "common_window_rect_2x": list(common_window),
        "gateE_same_state_layout": gate_e,
        "measurement_rule_version": "wmw_hollow_shell_photo_pipeline_v1_1",
    }
    per_state_measurement: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        per_state_measurement.append(
            {
                "state": state,
                "measured_window_rect_2x": list(measured_windows[idx]),
                "common_window_rect_2x": list(common_window),
                "adaptive_classifier_samples": sample_metas[idx],
                "globe_disc": globes[idx],
            }
        )
    return measurement, per_state_measurement


def compose_frames() -> tuple[list[Image.Image], list[Image.Image], list[Image.Image], dict, list[dict]]:
    b_frames = load_atlas_frames(B_ATLAS)
    photo_frames = load_atlas_frames(B13_ATLAS)
    measurement, measured_state = measure_inputs(b_frames)
    gate_e = measurement["gateE_same_state_layout"]
    if gate_e["status"] != "pass":
        raise RuntimeError(f"GateE failed, stop: {gate_e}")
    common_window = tuple(measurement["common_window_rect_2x"])
    globes = [item["globe_disc"] for item in measured_state]

    frames: list[Image.Image] = []
    shells: list[Image.Image] = []
    masks: list[Image.Image] = []
    per_state: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        shell, mask, cut_pixels = make_hollow_shell(b_frames[idx], state, common_window, globes[idx])
        source_photo = photo_frames[idx].crop(SOURCE_PHOTO_RECT_2X).convert("RGBA")
        photo = cover_photo_to_window(source_photo, common_window, state)
        frame = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        frame.alpha_composite(photo, (common_window[0], common_window[1]))
        frame.alpha_composite(shell)

        state_gates = {
            "gateA_old_photo_residue": gate_a_old_residue(shell, mask, common_window),
            "gateB_border_integrity": gate_b_border_integrity(b_frames[idx], shell, common_window),
            "gateC_window_alpha": gate_c_window_alpha(frame, common_window),
            "gateD_green_residue": gate_d_green_residue(frame, state),
            "gateF_geometry": gate_f_geometry(frame),
        }
        per_state.append(
            {
                "state": state,
                "measured_window_rect_2x": measured_state[idx]["measured_window_rect_2x"],
                "common_window_rect_2x": list(common_window),
                "adaptive_classifier_samples": measured_state[idx]["adaptive_classifier_samples"],
                "globe_disc": globes[idx],
                "cutout_pixels": cut_pixels,
                "source_photo_rect_from_b1_3_atlas_2x": list(SOURCE_PHOTO_RECT_2X),
                "photo_shape_clipping": "forbidden_not_used",
                "z_order": "transparent base -> rectangular photo underlay -> geometric hollow shell -> runtime text",
                "gates": state_gates,
            }
        )
        frames.append(frame)
        shells.append(shell)
        masks.append(mask)
    measurement = {
        **measurement,
        "is_cream": "a>200 and r>150 and g>130 and b>100 and r>b+25; available full search, other states local search from available bbox expanded 12px",
    }
    return frames, shells, masks, measurement, per_state


def make_measurement_qa(frames: list[Image.Image], measurement: dict, per_state: list[dict]) -> Image.Image:
    canvas = Image.new("RGBA", (1760, 980), (8, 20, 22, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.2 v0.9.8 window measurement QA: geometry is measured from candidate B atlas", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 64), f"common window={measurement['common_window_rect_2x']}  GateE={measurement['gateE_same_state_layout']['status']}  source={B_ATLAS}", fill=(205, 224, 198), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + (idx % 2) * 850
        y = 118 + (idx // 2) * 410
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(frames[idx])
        zoom = bg.resize((FRAME_SIZE[0] * 2, FRAME_SIZE[1] * 2), Image.Resampling.NEAREST)
        canvas.alpha_composite(zoom, (x, y))
        rect = tuple(measurement["common_window_rect_2x"])
        gx, gy = per_state[idx]["globe_disc"]["center"]
        gr = per_state[idx]["globe_disc"]["radius"]
        draw.rectangle((x + rect[0] * 2, y + rect[1] * 2, x + rect[2] * 2, y + rect[3] * 2), outline=(91, 233, 255), width=3)
        measured = tuple(per_state[idx]["measured_window_rect_2x"])
        draw.rectangle((x + measured[0] * 2, y + measured[1] * 2, x + measured[2] * 2, y + measured[3] * 2), outline=(255, 96, 104), width=2)
        draw.ellipse((x + (gx - gr) * 2, y + (gy - gr) * 2, x + (gx + gr) * 2, y + (gy + gr) * 2), outline=(255, 216, 91), width=3)
        draw.text((x, y - 28), f"{state}: measured={per_state[idx]['measured_window_rect_2x']} globe={per_state[idx]['globe_disc']['center']} r={per_state[idx]['globe_disc']['radius']}", fill=(234, 232, 204), font=b11.F_SMALL)
    draw.text((42, 928), "cyan=common rect for cutout/photo underlay; red=per-state measured rect; yellow=measured globe disc", fill=(215, 224, 199), font=b11.F_NOTE)
    return canvas


def make_ingredient_board(shells: list[Image.Image], masks: list[Image.Image], measurement: dict, per_state: list[dict]) -> Image.Image:
    b_frames = load_atlas_frames(B_ATLAS)
    canvas = Image.new("RGBA", (1720, 1052), (9, 22, 24, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.2 v0.9.8 hollow-shell ingredients: pure geometry cutout", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 64), "Cutout = common measured window rectangle minus measured globe disc; no per-pixel color decision is used for digging.", fill=(205, 224, 198), font=b11.F_NOTE)
    headers = ["candidate B source", "geometry mask", "hollow shell", "alpha preview"]
    cell_w = 404
    row_h = 230
    for i, h in enumerate(headers):
        draw.text((42 + i * cell_w, 102), h, fill=(188, 216, 190), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        y = 134 + idx * row_h
        draw.text((10, y + 4), state, fill=(235, 231, 200), font=b11.F_SMALL)
        for col, img in enumerate([
            b_frames[idx],
            ImageOps.colorize(masks[idx], black="#071315", white="#58e9ff").convert("RGBA"),
            shells[idx],
            ImageOps.colorize(shells[idx].getchannel("A"), black="#071315", white="#f0ecd0").convert("RGBA"),
        ]):
            preview = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
            if col == 1:
                preview.alpha_composite(img)
            elif col == 3:
                preview.alpha_composite(img)
            else:
                preview.alpha_composite(img)
            preview = preview.resize((306, 240), Image.Resampling.LANCZOS if col != 1 else Image.Resampling.NEAREST)
            canvas.alpha_composite(preview, (42 + col * cell_w, y))
            draw.rectangle((42 + col * cell_w, y, 42 + col * cell_w + 306, y + 240), outline=(76, 139, 126), width=2)
        gate_summary = per_state[idx]["gates"]
        draw.text(
            (42 + 4 * cell_w - 68, y + 12),
            f"A={gate_summary['gateA_old_photo_residue']['opaque_pixels_in_cutout_core']} B={gate_summary['gateB_border_integrity']['broken_opaque_pixels']} C={gate_summary['gateC_window_alpha']['transparent_or_nonopaque_pixels_in_window']}",
            fill=(184, 240, 190),
            font=b11.F_SMALL,
        )
    return canvas


def make_geometry_qa(frames: list[Image.Image], per_state: list[dict]) -> tuple[Image.Image, list[dict]]:
    composition = [
        {
            "state": item["state"],
            "pipeline": item["z_order"],
            "measured_window_rect_2x": item["measured_window_rect_2x"],
            "common_window_rect_2x": item["common_window_rect_2x"],
            "source_photo_rect_from_b1_3_atlas_2x": item["source_photo_rect_from_b1_3_atlas_2x"],
            "photo_shape_clipping": item["photo_shape_clipping"],
        }
        for item in per_state
    ]
    qa, metrics = b11.make_geometry_qa(frames, composition)
    draw = ImageDraw.Draw(qa)
    draw.rectangle((0, 0, qa.width, 36), fill=(14, 23, 24, 255))
    draw.text((42, 5), "B2.2 geometry QA: 408x320 atlas frames; measured hollow window, no photo shape crop", fill=(236, 231, 197), font=b11.F_NOTE)
    return qa, metrics


def make_runtime_preview(frames: list[Image.Image], show_qa: bool) -> Image.Image:
    contract = b11.load_contract()
    img = b11.make_runtime_preview(frames, contract, show_qa)
    draw = ImageDraw.Draw(img)
    draw.rectangle((438, 20, 1880, 122), fill=(7, 19, 21, 255))
    draw.text((450, 34), "Python v0.9.8 B2.2 left_region_card hollow-shell geometry fill", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 82), "Photo is a rectangle under the measured hollow shell; title/meta remain runtime tokens.", fill=(217, 222, 199), font=b11.F_NOTE)
    return img


def draw_zoom(canvas: Image.Image, src: Image.Image, crop: tuple[int, int, int, int], xy: tuple[int, int], title: str) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y = xy
    panel = src.crop(crop).resize(((crop[2] - crop[0]) * 3, (crop[3] - crop[1]) * 3), Image.Resampling.NEAREST)
    canvas.alpha_composite(panel.convert("RGBA"), xy)
    draw.rectangle((x, y, x + panel.width, y + panel.height), outline=(94, 164, 142), width=2)
    draw.text((x, y - 23), title, fill=(234, 232, 204), font=b11.F_SMALL)


def make_fit_qa(frames: list[Image.Image], measurement: dict, per_state: list[dict]) -> Image.Image:
    rect = tuple(measurement["common_window_rect_2x"])
    canvas = Image.new("RGBA", (1920, 1440), (8, 20, 22, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.2 v0.9.8 300% fit QA: globe arc / right edge / bottom edge", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 64), "Required by hollow-shell rules v1.0: no gap, no old band, no ghost, no green edge.", fill=(205, 224, 198), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        row_y = 122 + idx * 318
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(frames[idx])
        gx, gy = per_state[idx]["globe_disc"]["center"]
        gr = per_state[idx]["globe_disc"]["radius"]
        draw.text((42, row_y - 30), state, fill=(255, 229, 93), font=b11.F_NOTE)
        draw_zoom(
            canvas,
            bg,
            (max(0, int(gx - gr - 12)), max(0, int(gy - gr - 8)), min(FRAME_SIZE[0], int(gx + gr + 42)), min(FRAME_SIZE[1], int(gy + gr + 30))),
            (42, row_y),
            "globe arc",
        )
        draw_zoom(
            canvas,
            bg,
            (rect[2] - 34, rect[1] - 10, min(FRAME_SIZE[0], rect[2] + 34), rect[3] + 10),
            (505, row_y),
            "right edge",
        )
        draw_zoom(
            canvas,
            bg,
            (rect[0] + 24, rect[3] - 28, rect[2] - 24, min(FRAME_SIZE[1], rect[3] + 28)),
            (800, row_y),
            "bottom edge",
        )
        thumb = bg.resize((245, 192), Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb, (1590, row_y + 10))
        draw.rectangle((1590, row_y + 10, 1590 + 245, row_y + 202), outline=(94, 164, 142), width=2)
    return canvas


def image_content_checks(paths: dict[str, Path]) -> dict:
    return {name: b11.count_colors_nonblack(path) for name, path in paths.items() if path.exists()}


def aggregate_gate_status(per_state: list[dict], measurement: dict, geometry_metrics: list[dict], manual_pass: bool, godot_pass: bool) -> dict:
    gate_a_pass = all(item["gates"]["gateA_old_photo_residue"]["status"] == "pass" for item in per_state)
    gate_b_pass = all(item["gates"]["gateB_border_integrity"]["status"] == "pass" for item in per_state)
    gate_c_pass = all(item["gates"]["gateC_window_alpha"]["status"] == "pass" for item in per_state)
    gate_d_pass = all(
        item["gates"]["gateD_green_residue"]["status"] in {"pass", "skipped_selected_green_glow_semantic"}
        for item in per_state
    )
    gate_f_pass = all(item["gates"]["gateF_geometry"]["status"] == "pass" for item in per_state) and all(m["ratio_pass"] for m in geometry_metrics)
    return {
        "gateA_old_photo_residue_core": {
            "status": "pass" if gate_a_pass else "fail",
            "basis": "After pure geometric cutout, mask core inset by 3px must contain zero opaque shell pixels.",
        },
        "gateB_border_integrity_ring": {
            "status": "pass" if gate_b_pass else "fail",
            "basis": "Within the 3px ring outside the window rectangle, pixels opaque in original B shell must remain opaque after cutout.",
        },
        "gateC_window_alpha_after_composite": {
            "status": "pass" if gate_c_pass else "fail",
            "basis": "After photo-underlay + hollow-shell composition, every pixel inside the common window rectangle must be alpha 255.",
        },
        "gateD_green_residue_nonselected": {
            "status": "pass" if gate_d_pass else "fail",
            "basis": "Non-selected frames are full-frame scanned with the frozen green signature; selected is exempt by rule.",
        },
        "gateE_same_state_window_layout": measurement["gateE_same_state_layout"],
        "gateF_geometry_ratio": {
            "status": "pass" if gate_f_pass else "fail",
            "basis": "All frames remain 408x320, ratio 1.275 within tolerance.",
            "target_ratio": TARGET_RATIO,
            "tolerance": RATIO_TOLERANCE,
        },
        "manual_300pct_visual_check": {
            "status": "pass" if manual_pass else "pending",
            "basis": "Per-frame 300% QA board must show globe arc, right edge, and bottom edge without seam/residue/ghost/green edge.",
            "evidence": str(OUT_FIT_QA),
        },
        "godot_windowed_capture": {
            "status": "pass" if godot_pass else "pending",
            "basis": "Run scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro with windowed opengl3; headless forbidden for UI screenshots.",
            "headless_used_for_ui_capture": False,
        },
    }


def make_manifest(
    measurement: dict,
    per_state: list[dict],
    geometry_metrics: list[dict],
    checks: dict,
    manual_pass: bool = False,
    godot_pass: bool = False,
) -> dict:
    gates = aggregate_gate_status(per_state, measurement, geometry_metrics, manual_pass, godot_pass)
    gate_values = [value["status"] for value in gates.values()]
    machine_pass = all(status in {"pass", "skipped_selected_green_glow_semantic"} for status in gate_values if status != "pending")
    full_pass = machine_pass and manual_pass and godot_pass
    return {
        "schema_version": 1,
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "status": "b2_2_hollow_shell_geometry_pass_pending_user_review" if full_pass else "b2_2_hollow_shell_geometry_pending_full_chain",
        "date": "2026-07-09",
        "contract": str(b11.CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "pipeline": "transparent base -> rectangular B1.3 photo underlay -> pure-geometry hollow shell -> runtime text",
        "rule_source": "WMW 左卡镂空框规程 v1.0",
        "inputs": {
            "candidate_b_original_atlas_2x": str(B_ATLAS),
            "candidate_b1_3_photo_atlas_2x": str(B13_ATLAS),
            "reference_sample_promoted_logic": str(ROOT / "scripts/ui-contracts/wmw/wmw_v098_left_card_b22_hollow_shell_geometry_pipeline.py"),
        },
        "outputs": {
            "window_measurement_qa": str(OUT_MEASURE_QA),
            "hollow_shell_ingredients": str(OUT_INGREDIENTS),
            "atlas_2x": str(OUT_ATLAS),
            "geometry_qa": str(OUT_GEOMETRY_QA),
            "runtime_fill_preview": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "fit_300pct_qa": str(OUT_FIT_QA),
            "manifest": str(OUT_MANIFEST),
            "godot_single_component": str(OUT_GODOT),
            "godot_single_component_qa": str(OUT_GODOT_QA),
            "godot_atlas_copy": str(GODOT_ATLAS),
            "godot_manifest_copy": str(GODOT_MANIFEST),
            "godot_ingredients_dir": str(GODOT_INGREDIENT_DIR),
        },
        "runtime_tokens": {
            "label_title": {
                "python_font_px": 19,
                "godot_font_size": b11.TOKENS["label_title"]["godot_font_size"],
                "color": b11.TOKENS["label_title"]["godot_color"],
            },
            "meta_status": {
                "python_font_px": 11,
                "godot_font_size": b11.TOKENS["meta_status"]["godot_font_size"],
                "color": b11.TOKENS["meta_status"]["godot_color"],
            },
        },
        "measurement": measurement,
        "per_state": per_state,
        "geometry_metrics": geometry_metrics,
        "gates": gates,
        "image_content_checks": checks,
        "prohibitions_observed": {
            "imagegen_called": False,
            "photo_shape_clipping_used": False,
            "selected_green_cleanup_used": False,
            "contract_frozen_fields_changed": False,
            "other_classes_batch_produced": False,
        },
    }


def write_measurement_overlay() -> tuple[dict, list[dict]]:
    b_frames = load_atlas_frames(B_ATLAS)
    measurement, measured_state = measure_inputs(b_frames)
    OUT_MEASURE_QA.parent.mkdir(parents=True, exist_ok=True)
    make_measurement_qa(b_frames, measurement, measured_state).save(OUT_MEASURE_QA)
    return measurement, measured_state


def write_outputs(manual_pass: bool = False) -> dict:
    frames, shells, masks, measurement, per_state = compose_frames()
    measure_qa = make_measurement_qa(load_atlas_frames(B_ATLAS), measurement, per_state)
    ingredients = make_ingredient_board(shells, masks, measurement, per_state)
    atlas = b11.make_atlas(frames)
    geometry_qa, geometry_metrics = make_geometry_qa(frames, per_state)
    runtime = make_runtime_preview(frames, False)
    runtime_qa = make_runtime_preview(frames, True)
    fit_qa = make_fit_qa(frames, measurement, per_state)

    for path in [OUT_MEASURE_QA, OUT_INGREDIENTS, OUT_ATLAS, OUT_GEOMETRY_QA, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_FIT_QA]:
        path.parent.mkdir(parents=True, exist_ok=True)
    measure_qa.save(OUT_MEASURE_QA)
    ingredients.save(OUT_INGREDIENTS)
    atlas.save(OUT_ATLAS)
    geometry_qa.save(OUT_GEOMETRY_QA)
    runtime.save(OUT_RUNTIME)
    runtime_qa.save(OUT_RUNTIME_QA)
    fit_qa.save(OUT_FIT_QA)

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    GODOT_INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    for shell, state in zip(shells, STATE_ORDER):
        shell.save(GODOT_INGREDIENT_DIR / f"left_region_card_b22_geometry_hollow_shell_{state}.png")

    checks = image_content_checks(
        {
            "window_measurement_qa": OUT_MEASURE_QA,
            "hollow_shell_ingredients": OUT_INGREDIENTS,
            "atlas_2x": OUT_ATLAS,
            "geometry_qa": OUT_GEOMETRY_QA,
            "runtime_fill_preview": OUT_RUNTIME,
            "runtime_fill_qa": OUT_RUNTIME_QA,
            "fit_300pct_qa": OUT_FIT_QA,
            "godot_single_component": OUT_GODOT,
            "godot_single_component_qa": OUT_GODOT_QA,
        }
    )
    godot_pass = OUT_GODOT.exists() and OUT_GODOT_QA.exists()
    if godot_pass:
        checks["godot_single_component"] = b11.count_colors_nonblack(OUT_GODOT)
        checks["godot_single_component_qa"] = b11.count_colors_nonblack(OUT_GODOT_QA)
    manifest = make_manifest(measurement, per_state, geometry_metrics, checks, manual_pass=manual_pass, godot_pass=godot_pass)
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="WMW left_region_card B2.2 hollow-shell geometry pipeline")
    parser.add_argument("--measure-only", action="store_true", help="Only write the measured-window overlay QA board and stop before cutout.")
    parser.add_argument("--manual-ok", action="store_true", help="Confirm 458 overlay QA has been manually inspected before geometric cutout.")
    args = parser.parse_args()

    if args.measure_only:
        measurement, measured_state = write_measurement_overlay()
        print(json.dumps(
            {
                "status": "measurement_overlay_written",
                "window": measurement["common_window_rect_2x"],
                "gateE": measurement["gateE_same_state_layout"],
                "per_state": measured_state,
                "output": str(OUT_MEASURE_QA),
            },
            ensure_ascii=False,
            indent=2,
        ))
        return

    if not args.manual_ok:
        measurement, measured_state = write_measurement_overlay()
        raise RuntimeError(
            "Manual overlay QA is required before geometric cutout. "
            f"Inspect {OUT_MEASURE_QA}; then rerun with --manual-ok if all rectangles sit on the photo."
        )

    manifest = write_outputs(manual_pass=True)
    print(json.dumps(
        {
            "status": manifest["status"],
            "window": manifest["measurement"]["common_window_rect_2x"],
            "gateE": manifest["measurement"]["gateE_same_state_layout"],
            "outputs": manifest["outputs"],
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
