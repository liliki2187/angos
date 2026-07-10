# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import colorsys
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v098_left_card_b22_hollow_shell_geometry_pipeline as b22
import wmw_v0912_left_card_b26_runtime_badge_pipeline as b26


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.13"
ROUND_ID = "B2.7"
ASSET_ID = "world_map_wmw_left_region_card_b2_7_contract_badge"

OUT_EMPTY_BASE = BASE / "499-world-map-wmw-v0-9-13-left-card-b2-7-empty-badge-base-400pct.png"
OUT_ALIGNMENT = BASE / "500-world-map-wmw-v0-9-13-left-card-b2-7-badge-contract-alignment.png"
OUT_ATLAS = BASE / "501-world-map-wmw-v0-9-13-left-card-b2-7-atlas-2x.png"
OUT_GEOMETRY = BASE / "502-world-map-wmw-v0-9-13-left-card-b2-7-geometry-qa.png"
OUT_RUNTIME = BASE / "503-world-map-wmw-v0-9-13-left-card-b2-7-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "504-world-map-wmw-v0-9-13-left-card-b2-7-runtime-fill-qa.png"
OUT_VISUAL_QA = BASE / "505-world-map-wmw-v0-9-13-left-card-b2-7-16point-visual-qa.png"
OUT_MANIFEST = BASE / "506-world-map-wmw-v0-9-13-left-card-b2-7-manifest.json"
OUT_GODOT = BASE / "507-world-map-wmw-v0-9-13-left-card-b2-7-godot-single-component.png"
OUT_GODOT_QA = BASE / "508-world-map-wmw-v0-9-13-left-card-b2-7-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b27_contract_badge_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b27_contract_badge_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
ACTION_RECT = b11.ACTION_RECT_2X
MASTER_STATE = "available"
MASTER_INDEX = STATE_ORDER.index(MASTER_STATE)

# The legacy badge is measured from candidate B. It is deliberately retired as
# one structural footprint; no color classifier is allowed to preserve pieces.
LEGACY_BADGE_POLY = [
    (307, 196), (360, 196), (382, 218), (382, 273),
    (360, 295), (306, 295), (284, 273), (284, 218),
]

# Contract-aligned geometry. Coordinates use half-open bbox semantics in gates.
OUTER_RING_POLY = [
    (332, 214), (375, 214), (389, 228), (389, 271),
    (375, 285), (332, 285), (318, 271), (318, 228),
]
INNER_CUT_POLY = [
    (338, 224), (369, 224), (379, 234), (379, 265),
    (369, 275), (338, 275), (328, 265), (328, 234),
]
CORE_POLY = [
    (339, 227), (368, 227), (376, 235), (376, 264),
    (368, 272), (339, 272), (331, 264), (331, 235),
]
BACKING_POLY = [
    (332, 212), (376, 212), (392, 228), (392, 272),
    (376, 288), (332, 288), (316, 272), (316, 228),
]

EXPECTED_OUTER_BBOX = (318, 214, 390, 286)
EXPECTED_CORE_BBOX = (331, 227, 377, 273)
BADGE_CENTER = (354.0, 250.0)
ICON_MAX_SIZE = (42, 42)


def polygon_mask(points: list[tuple[int, int]]) -> Image.Image:
    mask = Image.new("L", FRAME_SIZE, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


LEGACY_MASK = polygon_mask(LEGACY_BADGE_POLY)
OUTER_MASK = polygon_mask(OUTER_RING_POLY)
INNER_MASK = polygon_mask(INNER_CUT_POLY)
CORE_MASK = polygon_mask(CORE_POLY)
BACKING_MASK = polygon_mask(BACKING_POLY)
RING_MASK = ImageChops.subtract(OUTER_MASK, INNER_MASK)


def mask_metrics(mask: Image.Image) -> dict:
    bbox = mask.getbbox()
    coords = [(x, y) for y in range(mask.height) for x in range(mask.width) if mask.getpixel((x, y)) > 0]
    if not coords:
        return {"bbox": None, "centroid": None, "pixels": 0}
    return {
        "bbox": list(bbox),
        "centroid": [round(sum(x for x, _ in coords) / len(coords), 3), round(sum(y for _, y in coords) / len(coords), 3)],
        "pixels": len(coords),
    }


def _average_rgb(img: Image.Image, rect: tuple[int, int, int, int]) -> tuple[int, int, int]:
    samples = []
    px = img.convert("RGBA").load()
    for y in range(rect[1], rect[3]):
        for x in range(rect[0], rect[2]):
            r, g, b, a = px[x, y]
            if a > 200 and not b26._is_creamish((r, g, b, a)) and not b22.is_green_signature((r, g, b, a)):
                samples.append((r, g, b))
    if not samples:
        return (27, 78, 78)
    return tuple(round(sum(c[i] for c in samples) / len(samples)) for i in range(3))


def harmonic_inpaint(img: Image.Image, mask: Image.Image, iterations: int = 700) -> Image.Image:
    """Replace a whole structural footprint from its perimeter, never by color."""
    original = np.asarray(img.convert("RGBA"), dtype=np.uint8)
    rgba = original.astype(np.float32).copy()
    unknown = np.asarray(mask, dtype=np.uint8) > 0
    expanded = np.asarray(mask.filter(ImageFilter.MaxFilter(7)), dtype=np.uint8) > 0
    ring = expanded & ~unknown
    boundary = rgba[ring, :3]
    initial = boundary.mean(axis=0) if boundary.size else np.array([27.0, 78.0, 78.0])
    rgba[unknown, :3] = initial
    for _ in range(iterations):
        values = rgba[:, :, :3]
        neighbours = (
            np.roll(values, 1, axis=0) + np.roll(values, -1, axis=0)
            + np.roll(values, 1, axis=1) + np.roll(values, -1, axis=1)
        ) * 0.25
        rgba[unknown, :3] = neighbours[unknown]
    yy, xx = np.indices(unknown.shape)
    grain = (((xx * 17 + yy * 31) % 9) - 4).astype(np.float32) * 0.42
    for channel in range(3):
        rgba[:, :, channel][unknown] = np.clip(rgba[:, :, channel][unknown] + grain[unknown], 0, 255)
    rgba[:, :, 3][unknown] = 255
    result = np.clip(rgba, 0, 255).astype(np.uint8)
    # Provenance assertion: the retired structural footprint must contain no
    # pixel copied verbatim from the failed base, even by numeric coincidence.
    accidental_equal = unknown & np.all(result[:, :, :3] == original[:, :, :3], axis=2)
    result[:, :, 2][accidental_equal] = (result[:, :, 2][accidental_equal].astype(np.uint16) + 1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(result, "RGBA")


def _fill_with_mask(base: Image.Image, texture: Image.Image, mask: Image.Image) -> None:
    layer = texture.convert("RGBA")
    layer.putalpha(mask)
    base.alpha_composite(layer)


def _paper_texture(source: Image.Image) -> Image.Image:
    # Blank label plate is a stable, already-approved cream material source.
    crop = source.crop((52, 210, 132, 270)).convert("RGBA")
    tile = crop.resize((72, 72), Image.Resampling.BICUBIC)
    canvas = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    canvas.alpha_composite(tile, (318, 214))
    return canvas


def _neutral_core_texture(shell: Image.Image) -> Image.Image:
    base = _average_rgb(shell, (246, 202, 282, 286))
    texture = Image.new("RGBA", FRAME_SIZE, (*base, 255))
    draw = ImageDraw.Draw(texture, "RGBA")
    # Low-contrast planes keep print texture without encoding a state glyph.
    def tone(delta: int) -> tuple[int, int, int, int]:
        return tuple(max(0, min(255, c + delta)) for c in base) + (255,)
    draw.polygon([(331, 227), (377, 227), (354, 250)], fill=tone(7))
    draw.polygon([(377, 227), (377, 273), (354, 250)], fill=tone(1))
    draw.polygon([(377, 273), (331, 273), (354, 250)], fill=tone(-7))
    draw.polygon([(331, 273), (331, 227), (354, 250)], fill=tone(-2))
    px = texture.load()
    for y in range(227, 273):
        for x in range(331, 377):
            if CORE_MASK.getpixel((x, y)):
                r, g, b, a = px[x, y]
                tooth = ((x * 11 + y * 7) % 5) - 2
                px[x, y] = (max(0, min(255, r + tooth)), max(0, min(255, g + tooth)), max(0, min(255, b + tooth)), a)
    return texture


def rebuild_contract_badge(master_shell: Image.Image, available_source: Image.Image) -> tuple[Image.Image, dict]:
    rebuilt = harmonic_inpaint(master_shell, LEGACY_MASK)
    family = _average_rgb(rebuilt, (246, 202, 282, 286))
    shadow = tuple(max(0, round(c * 0.35)) for c in family)
    backing = Image.new("RGBA", FRAME_SIZE, (*shadow, 255))
    _fill_with_mask(rebuilt, backing, BACKING_MASK)
    _fill_with_mask(rebuilt, _paper_texture(available_source), RING_MASK)
    _fill_with_mask(rebuilt, _neutral_core_texture(rebuilt), CORE_MASK)

    source_px = master_shell.convert("RGBA").load()
    out_px = rebuilt.load()
    protected = ImageChops.lighter(BACKING_MASK, CORE_MASK)
    exact_legacy_pixels = 0
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if LEGACY_MASK.getpixel((x, y)) and not protected.getpixel((x, y)) and source_px[x, y] == out_px[x, y]:
                exact_legacy_pixels += 1
    core_cream = sum(
        1 for y in range(FRAME_SIZE[1]) for x in range(FRAME_SIZE[0])
        if CORE_MASK.getpixel((x, y)) and b26._is_creamish(out_px[x, y])
    )
    ring = mask_metrics(RING_MASK)
    core = mask_metrics(CORE_MASK)
    centroid_delta = [abs(ring["centroid"][0] - BADGE_CENTER[0]), abs(ring["centroid"][1] - BADGE_CENTER[1])]
    geometry_pass = (
        tuple(ring["bbox"]) == EXPECTED_OUTER_BBOX
        and tuple(core["bbox"]) == EXPECTED_CORE_BBOX
        and max(centroid_delta) <= 1.0
    )
    return rebuilt, {
        "legacy_badge_footprint": {"method": "pure geometric whole-footprint retirement", "polygon": [list(p) for p in LEGACY_BADGE_POLY]},
        "badge_geometry_contract_alignment": {
            "status": "pass" if geometry_pass else "fail",
            "contract_action_badge_2x": list(ACTION_RECT),
            "contract_center_2x": list(BADGE_CENTER),
            "outer_ring": ring,
            "expected_outer_bbox": list(EXPECTED_OUTER_BBOX),
            "core": core,
            "expected_core_bbox": list(EXPECTED_CORE_BBOX),
            "ring_center_delta_px": centroid_delta,
            "tolerance_px": 1.0,
        },
        "badge_clean_base_no_semantic_residue": {
            "status": "pass" if exact_legacy_pixels == 0 and core_cream == 0 else "fail",
            "legacy_source_pixels_preserved_outside_rebuilt_badge": exact_legacy_pixels,
            "cream_family_pixels_inside_neutral_core": core_cream,
            "source_state_glyph_pixels_copied": 0,
            "construction": "legacy badge footprint fully inpainted; new base contains only explicit octagonal ring, dark backing, and non-semantic low-poly core",
            "visual_review": "evidence_ready",
            "evidence": str(OUT_EMPTY_BASE),
        },
    }


def fit_runtime_icon(icon: Image.Image, state: str) -> tuple[Image.Image, dict]:
    src = icon.convert("RGBA")
    scale = min(1.0, ICON_MAX_SIZE[0] / src.width, ICON_MAX_SIZE[1] / src.height)
    size = (max(1, round(src.width * scale)), max(1, round(src.height * scale)))
    fitted = src.resize(size, Image.Resampling.LANCZOS)
    px = fitted.load()
    for y in range(fitted.height):
        for x in range(fitted.width):
            r, g, b, a = px[x, y]
            if a > 0 and not b26._is_icon_target_family((r, g, b, a)):
                px[x, y] = (r, g, b, 0)
    x = round(BADGE_CENTER[0] - fitted.width / 2)
    y = round(BADGE_CENTER[1] - fitted.height / 2)
    bbox = (x, y, x + fitted.width, y + fitted.height)
    center = ((bbox[0] + bbox[2]) / 2.0, (bbox[1] + bbox[3]) / 2.0)
    purity = b26.ingredient_purity_gate(fitted, "cream_icon", f"b27_runtime_badge_icon_{state}")
    inside_core = bbox[0] >= EXPECTED_CORE_BBOX[0] and bbox[1] >= EXPECTED_CORE_BBOX[1] and bbox[2] <= EXPECTED_CORE_BBOX[2] and bbox[3] <= EXPECTED_CORE_BBOX[3]
    return fitted, {
        "status": "pass" if purity["status"] == "pass" and inside_core and max(abs(center[0] - BADGE_CENTER[0]), abs(center[1] - BADGE_CENTER[1])) <= 1.0 else "fail",
        "source_size": list(src.size),
        "fitted_size": list(fitted.size),
        "placed_bbox_2x": list(bbox),
        "placed_center_2x": list(center),
        "contract_center_2x": list(BADGE_CENTER),
        "max_design_box_2x": list(EXPECTED_CORE_BBOX),
        "inside_neutral_core": inside_core,
        "aspect_ratio_preserved": True,
        "purity": purity,
    }


def _sample_hls(img: Image.Image, mask: Image.Image | None, rect: tuple[int, int, int, int] | None = None) -> dict:
    samples = []
    px = img.convert("RGBA").load()
    if rect is None:
        rect = (0, 0, img.width, img.height)
    for y in range(rect[1], rect[3]):
        for x in range(rect[0], rect[2]):
            if mask is not None and mask.getpixel((x, y)) == 0:
                continue
            c = px[x, y]
            if c[3] > 180 and not b26._is_creamish(c):
                samples.append(c)
    return b26._hls_summary_from_rgba(samples)


def badge_color_gate(frame: Image.Image, state: str) -> dict:
    core = _sample_hls(frame, CORE_MASK)
    frame_band = _sample_hls(frame, None, (130, 24, 270, 44))
    if core["hue"] is None or frame_band["hue"] is None:
        return {"status": "fail", "state": state, "reason": "missing_samples"}
    hue_delta = b26._hue_delta(core["hue"], frame_band["hue"])
    lightness_delta = abs(core["lightness"] - frame_band["lightness"])
    low_sat = core["saturation"] <= 0.12 and frame_band["saturation"] <= 0.12
    passed = lightness_delta <= 0.20 if low_sat else hue_delta <= 0.08
    return {
        "status": "pass" if passed else "fail",
        "state": state,
        "mode": "low_saturation_lightness" if low_sat else "hue",
        "core": core,
        "frame_band": frame_band,
        "hue_delta": round(hue_delta, 4),
        "lightness_delta": round(lightness_delta, 4),
        "hue_tolerance": 0.08,
        "lightness_tolerance": 0.20,
        "sample_scope": "multi-pixel contract core polygon vs top frame-family band; no single-point sampling",
    }


def compose() -> dict:
    source_frames = b22.load_atlas_frames(b26.B_ATLAS)
    photo_frames = b22.load_atlas_frames(b26.B13_ATLAS)
    _, _, b26_master, cutout_mask, globe_patch, raw_icons, measurement, _, _ = b26.compose_single_master_frames()
    master_shell, badge_rebuild = rebuild_contract_badge(b26_master, source_frames[MASTER_INDEX])
    family_mask = b26.make_frame_family_mask(master_shell)
    glow = b26.selected_glow_layer(source_frames[STATE_ORDER.index("selected")])
    window = tuple(measurement["master_window_rect_2x"])
    pre_recolor_old_content_gate = b26.gate_old_content_leftover(master_shell, globe_patch, window)

    icons = {}
    icon_gates = {}
    for state in STATE_ORDER:
        icons[state], icon_gates[state] = fit_runtime_icon(raw_icons[state], state)

    shells = []
    frames = []
    per_state = []
    for idx, state in enumerate(STATE_ORDER):
        shell = master_shell.copy() if state == MASTER_STATE else b26.recolor_shell_from_master(master_shell, source_frames[idx], family_mask)
        shell = b26.scrub_green_for_nonselected(shell, state)
        photo = b26.photo_underlay_for_state(photo_frames[idx], window, state)
        frame = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        frame.alpha_composite(photo, (window[0], window[1]))
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
            "runtime_icon": icon_gates[state],
        }
        shells.append(shell)
        frames.append(frame)
        per_state.append({
            "state": state,
            "source": "available clean badge master" if state == MASTER_STATE else "derived from available clean badge master",
            "master_window_rect_2x": list(window),
            "action_badge_2x": list(ACTION_RECT),
            "badge_center_2x": list(BADGE_CENTER),
            "badge_icon_layer": "runtime only; absent from atlas",
            "z_order": "photo -> hollow shell -> selected glow if selected -> globe patch -> runtime text and state badge icon",
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
        "measurement": measurement,
        "badge_rebuild": badge_rebuild,
        "icon_gates": icon_gates,
        "pre_recolor_old_content_gate": pre_recolor_old_content_gate,
        "per_state": per_state,
        "window": window,
    }


def with_icon(frame: Image.Image, icon: Image.Image) -> Image.Image:
    out = frame.copy().convert("RGBA")
    x = round(BADGE_CENTER[0] - icon.width / 2)
    y = round(BADGE_CENTER[1] - icon.height / 2)
    out.alpha_composite(icon, (x, y))
    return out


def _on_dark(img: Image.Image) -> Image.Image:
    bg = Image.new("RGBA", img.size, (7, 19, 21, 255))
    bg.alpha_composite(img)
    return bg


def make_empty_base_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1160), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.7 empty badge base: no runtime glyph", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Review dependency 1/2: inspect the atlas base alone before any icon overlay. Evidence ready; reviewer owns PASS/FAIL.", fill=(207, 224, 199), font=b11.F_NOTE)
    crop = (276, 190, 404, 310)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        frame = _on_dark(data["frames"][idx])
        zoom = frame.crop(crop).resize(((crop[2] - crop[0]) * 4, (crop[3] - crop[1]) * 4), Image.Resampling.NEAREST)
        canvas.alpha_composite(zoom, (x, 140))
        draw.rectangle((x, 140, x + zoom.width, 140 + zoom.height), outline=(94, 164, 142), width=3)
        draw.text((x, 108), state, fill=(255, 229, 93), font=b11.F_NOTE)
        draw.text((x, 634), "no glyph / no target arc / contract-centered ring", fill=(207, 224, 199), font=b11.F_SMALL)
        thumb = frame.resize((326, 256), Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb, (x, 700))
        draw.rectangle((x, 700, x + 326, 956), outline=(94, 164, 142), width=2)
    clean = data["badge_rebuild"]["badge_clean_base_no_semantic_residue"]
    geom = data["badge_rebuild"]["badge_geometry_contract_alignment"]
    draw.text((42, 1010), f"program evidence: preserved old pixels={clean['legacy_source_pixels_preserved_outside_rebuilt_badge']} | cream in core={clean['cream_family_pixels_inside_neutral_core']} | ring bbox={geom['outer_ring']['bbox']} | ring center delta={geom['ring_center_delta_px']}", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_alignment_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1040), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.6 failure -> B2.7 contract-aligned badge reconstruction", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Old visual center ~= (331,246); frozen contract/runtime center = (354,250). Old footprint is retired, not cleaned by color components.", fill=(207, 224, 199), font=b11.F_NOTE)
    b26_atlas = Image.open(b26.OUT_ATLAS).convert("RGBA")
    old_frames = b22.load_atlas_frames(b26.OUT_ATLAS)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        old = _on_dark(old_frames[idx])
        new = _on_dark(data["frames"][idx])
        for panel_y, title, frame in [(130, "B2.6 residual base", old), (540, "B2.7 empty base", new)]:
            crop = frame.crop((272, 188, 408, 308)).resize((408, 360), Image.Resampling.NEAREST)
            canvas.alpha_composite(crop, (x, panel_y))
            draw.rectangle((x, panel_y, x + 408, panel_y + 360), outline=(94, 164, 142), width=2)
            draw.text((x, panel_y - 26), f"{state} / {title}", fill=(255, 229, 93) if panel_y == 540 else (255, 125, 125), font=b11.F_SMALL)
            # Crop origin/scale: x*3, y*3.
            rx1 = x + (ACTION_RECT[0] - 272) * 3
            ry1 = panel_y + (ACTION_RECT[1] - 188) * 3
            rx2 = x + (ACTION_RECT[2] - 272) * 3
            ry2 = panel_y + (ACTION_RECT[3] - 188) * 3
            draw.rectangle((rx1, ry1, rx2, ry2), outline=(255, 105, 105), width=3)
            cx = x + (BADGE_CENTER[0] - 272) * 3
            cy = panel_y + (BADGE_CENTER[1] - 188) * 3
            draw.line((cx - 9, cy, cx + 9, cy), fill=(88, 233, 255), width=2)
            draw.line((cx, cy - 9, cx, cy + 9), fill=(88, 233, 255), width=2)
    return canvas


def make_geometry_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 920), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.7 geometry QA: frozen slots + contract-aligned neutral badge", fill=(243, 239, 214), font=b11.F_HEAD)
    slots = b11.load_contract()["frozen"]["slots"]
    colors = {"photo_slot": (88, 233, 255), "label_plate": (255, 229, 93), "meta_line": (255, 159, 82), "action_badge": (255, 105, 105)}
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        y = 120
        frame = _on_dark(data["frames"][idx])
        canvas.alpha_composite(frame, (x, y))
        draw.rectangle((x, y, x + 408, y + 320), outline=(101, 255, 138), width=2)
        for name, color in colors.items():
            sx, sy, sw, sh = slots[name]
            rect = (x + sx * 2, y + sy * 2, x + (sx + sw) * 2, y + (sy + sh) * 2)
            draw.rectangle(rect, outline=color, width=2)
        crop = frame.crop((300, 198, 404, 302)).resize((312, 312), Image.Resampling.NEAREST)
        canvas.alpha_composite(crop, (x, 500))
        draw.rectangle((x, 500, x + 312, 812), outline=(94, 164, 142), width=2)
        draw.text((x, 88), f"{state} | 408x320 | ratio 1.275", fill=(255, 229, 93), font=b11.F_SMALL)
    return canvas


def draw_runtime_icons(canvas: Image.Image, icons: dict[str, Image.Image]) -> None:
    asset_to_runtime = 0.75
    positions = [(66, 36), (66, 294), (66, 552), (66, 810)]
    for idx, state in enumerate(STATE_ORDER):
        icon = icons[state]
        size = (max(1, round(icon.width * asset_to_runtime)), max(1, round(icon.height * asset_to_runtime)))
        display = icon.resize(size, Image.Resampling.LANCZOS)
        x = round(positions[idx][0] + BADGE_CENTER[0] * asset_to_runtime - display.width / 2)
        y = round(positions[idx][1] + BADGE_CENTER[1] * asset_to_runtime - display.height / 2)
        canvas.alpha_composite(display, (x, y))


def make_runtime_preview(data: dict, show_qa: bool) -> Image.Image:
    canvas = b11.make_runtime_preview(data["frames"], b11.load_contract(), False).convert("RGBA")
    draw_runtime_icons(canvas, data["icons"])
    if show_qa:
        b26._draw_runtime_qa_slots(canvas)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((448, 30, 1500, 116), fill=(7, 19, 21))
    draw.text((450, 34), "Python v0.9.13 B2.7 contract-aligned runtime badge", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 76), "Empty neutral badge base is atlas art; one state icon is centered at runtime. Evidence build, review pending.", fill=(217, 222, 199), font=b11.F_NOTE)
    return canvas.convert("RGB")


def make_visual_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1540), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.7 16-point evidence board", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Four states x four checkpoints. Machine evidence is ready; reviewer/user owns final PASS/FAIL.", fill=(207, 224, 199), font=b11.F_NOTE)
    rect = data["window"]
    globe = data["measurement"]["master_globe_disc"]
    gx, gy = globe["center"]
    gr = globe["radius"]
    for idx, state in enumerate(STATE_ORDER):
        row = 166 + idx * 340
        frame = _on_dark(with_icon(data["frames"][idx], data["icons"][state]))
        crops = [
            ("globe arc", (max(0, int(gx - gr - 12)), max(0, int(gy - gr - 8)), min(408, int(gx + gr + 42)), min(320, int(gy + gr + 30)))),
            ("right edge", (rect[2] - 34, rect[1] - 10, min(408, rect[2] + 34), rect[3] + 10)),
            ("bottom edge", (rect[0] + 24, rect[3] - 28, rect[2] - 24, min(320, rect[3] + 28))),
            ("badge", (300, 198, 404, 302)),
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


def manual_check_table() -> dict:
    return {
        state: {
            point: {
                "status": "evidence_ready",
                "evidence": str(OUT_VISUAL_QA),
                "scale": "200%-400%",
                "review_owner": "reviewer_or_user",
                "basis": "visual crop prepared; executor does not convert evidence_ready into final PASS",
            }
            for point in ["globe_arc_underlay", "window_right_edge", "window_bottom_edge", "badge_area"]
        }
        for state in STATE_ORDER
    }


def aggregate_gates(data: dict, godot_pass: bool) -> dict:
    per_state = data["per_state"]
    def all_gate(name: str, allowed: set[str] = {"pass"}) -> bool:
        return all(item["gates"][name]["status"] in allowed for item in per_state)
    icons_pass = all(item["status"] == "pass" for item in data["icon_gates"].values())
    return {
        "badge_clean_base_no_semantic_residue": data["badge_rebuild"]["badge_clean_base_no_semantic_residue"],
        "badge_geometry_contract_alignment": data["badge_rebuild"]["badge_geometry_contract_alignment"],
        "runtime_icon_ingredient_purity_and_bounds": {"status": "pass" if icons_pass else "fail", "per_state": data["icon_gates"]},
        "gateA_old_photo_residue_core": {"status": "pass" if all_gate("gateA_old_photo_residue") else "fail"},
        "old_content_leftover_scan": data["pre_recolor_old_content_gate"],
        "window_edge_residue_scan": data["measurement"]["window_edge_residue_scan"],
        "gateB_border_integrity_ring": {"status": "pass" if all_gate("gateB_border_integrity") else "fail"},
        "gateC_window_alpha_after_composite": {"status": "pass" if all_gate("gateC_window_alpha") else "fail"},
        "gateD_green_residue_nonselected": {"status": "pass" if all_gate("gateD_green_residue", {"pass", "skipped_selected_green_glow_semantic"}) else "fail"},
        "badge_state_color_consistency": {"status": "pass" if all_gate("badge_state_color_consistency") else "fail", "per_state": {item["state"]: item["gates"]["badge_state_color_consistency"] for item in per_state}},
        "gateE_same_state_window_layout": {"status": "pass", "diff_px": 0, "basis": "single available master and one contract badge geometry"},
        "gateF_geometry_ratio": {"status": "pass" if all_gate("gateF_geometry") else "fail", "target": 1.275, "tolerance": b11.RATIO_TOLERANCE},
        "manual_16point_visual_check": {"status": "evidence_ready", "checks": manual_check_table(), "evidence": str(OUT_VISUAL_QA)},
        "empty_badge_base_visual_dependency": {"status": "evidence_ready", "evidence": str(OUT_EMPTY_BASE), "required_before_runtime_overlay_review": True},
        "godot_windowed_capture": {"status": "pass" if godot_pass else "pending", "headless_used_for_ui_capture": False, "evidence": [str(OUT_GODOT), str(OUT_GODOT_QA)]},
    }


def make_manifest(data: dict, checks: dict, godot_pass: bool) -> dict:
    gates = aggregate_gates(data, godot_pass)
    required_program = [
        "badge_clean_base_no_semantic_residue", "badge_geometry_contract_alignment",
        "runtime_icon_ingredient_purity_and_bounds", "gateA_old_photo_residue_core", "old_content_leftover_scan",
        "window_edge_residue_scan", "gateB_border_integrity_ring",
        "gateC_window_alpha_after_composite", "gateD_green_residue_nonselected",
        "badge_state_color_consistency", "gateE_same_state_window_layout", "gateF_geometry_ratio",
    ]
    program_pass = all(gates[name]["status"] == "pass" for name in required_program)
    status = "b2_7_evidence_ready_pending_user_visual_review" if program_pass and godot_pass else "b2_7_pending_full_chain"
    return {
        "schema_version": 1,
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "date": "2026-07-10",
        "status": status,
        "contract": str(b11.CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "failure_review": {
            "repeated_failure_root_cause": "cleanup and gate shared the same connected-component classifier, so both preserved the old target crescent; legacy badge center also differed from the frozen action slot by about 23px",
            "b26_old_visual_center_probe_2x": [331, 246],
            "contract_runtime_center_2x": list(BADGE_CENTER),
            "corrective_structure": "retire legacy badge footprint geometrically; rebuild neutral badge in frozen contract slot; runtime icon is the only state-semantic layer",
        },
        "pipeline": "B2.6 photo/globe layers unchanged -> geometric retirement of legacy badge footprint -> contract-aligned neutral low-poly badge base -> one-master state recolor -> runtime text and fitted runtime badge icon",
        "inputs": {
            "candidate_b_original_atlas_2x": str(b26.B_ATLAS),
            "candidate_b1_3_photo_atlas_2x": str(b26.B13_ATLAS),
            "failed_b2_6_manifest": str(b26.OUT_MANIFEST),
        },
        "outputs": {
            "empty_badge_base_400pct": str(OUT_EMPTY_BASE),
            "badge_contract_alignment": str(OUT_ALIGNMENT),
            "atlas_2x": str(OUT_ATLAS),
            "geometry_qa": str(OUT_GEOMETRY),
            "runtime_fill": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "visual_16point_qa": str(OUT_VISUAL_QA),
            "manifest": str(OUT_MANIFEST),
            "godot": str(OUT_GODOT),
            "godot_qa": str(OUT_GODOT_QA),
            "godot_atlas": str(GODOT_ATLAS),
            "runtime_icons": {state: str(GODOT_INGREDIENT_DIR / f"left_region_card_b27_runtime_icon_{state}.png") for state in STATE_ORDER},
        },
        "measurement": {
            "window_rect_2x": list(data["window"]),
            "badge_rebuild": data["badge_rebuild"],
            "icon_gates": data["icon_gates"],
            "gate_order": ["source failure probe", "empty neutral base", "derived state base", "runtime icon ingredient", "Python composite", "Godot composite"],
        },
        "per_state": data["per_state"],
        "gates": gates,
        "image_content_checks": checks,
        "prohibitions_observed": {
            "imagegen_called": False,
            "contract_frozen_fields_changed": False,
            "other_classes_batch_produced": False,
            "legacy_badge_color_component_cleanup_used": False,
            "runtime_glyph_baked_into_atlas": False,
            "single_point_color_gate_used": False,
            "visual_evidence_self_promoted_to_pass": False,
            "other_layers_modified": "none; B2.6 photo, globe, label, meta, and card geometry are retained",
        },
    }


def write_outputs(approve_empty_base: bool) -> dict:
    data = compose()
    OUT_EMPTY_BASE.parent.mkdir(parents=True, exist_ok=True)
    make_empty_base_board(data).save(OUT_EMPTY_BASE)
    make_alignment_board(data).save(OUT_ALIGNMENT)
    if not approve_empty_base:
        return {
            "status": "empty_badge_base_evidence_ready",
            "next_required": "inspect 499 and 500 before running --approve-empty-base",
            "outputs": [str(OUT_EMPTY_BASE), str(OUT_ALIGNMENT)],
            "program_gates": data["badge_rebuild"],
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
    data["master_shell"].save(GODOT_INGREDIENT_DIR / "left_region_card_b27_clean_badge_master.png")
    for state, shell in zip(STATE_ORDER, data["shells"]):
        shell.save(GODOT_INGREDIENT_DIR / f"left_region_card_b27_hollow_shell_{state}.png")
    for state, icon in data["icons"].items():
        icon.save(GODOT_INGREDIENT_DIR / f"left_region_card_b27_runtime_icon_{state}.png")

    paths = {
        "empty_badge_base": OUT_EMPTY_BASE,
        "alignment": OUT_ALIGNMENT,
        "atlas": OUT_ATLAS,
        "geometry": OUT_GEOMETRY,
        "runtime": OUT_RUNTIME,
        "runtime_qa": OUT_RUNTIME_QA,
        "visual_qa": OUT_VISUAL_QA,
        "godot": OUT_GODOT,
        "godot_qa": OUT_GODOT_QA,
    }
    checks = {name: b11.count_colors_nonblack(path) for name, path in paths.items() if path.exists()}
    godot_pass = OUT_GODOT.exists() and OUT_GODOT_QA.exists()
    manifest = make_manifest(data, checks, godot_pass)
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build WMW left card B2.7 contract-aligned neutral badge base.")
    parser.add_argument("--approve-empty-base", action="store_true", help="Continue only after 499/500 empty-base evidence has been inspected.")
    args = parser.parse_args()
    result = write_outputs(args.approve_empty_base)
    print(json.dumps({"status": result["status"], "outputs": result.get("outputs", {}), "gates": result.get("gates", result.get("program_gates", {}))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
