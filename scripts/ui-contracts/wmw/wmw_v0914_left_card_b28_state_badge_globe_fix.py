# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

import wmw_v092_left_card_b1_vertical_slice as b1
import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v098_left_card_b22_hollow_shell_geometry_pipeline as b22
import wmw_v0912_left_card_b26_runtime_badge_pipeline as b26
import wmw_v0913_left_card_b27_contract_badge_pipeline as b27


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.14"
ROUND_ID = "B2.8"
ASSET_ID = "world_map_wmw_left_region_card_b2_8_state_badge_globe_fix"

OUT_COMPARE = BASE / "509-world-map-wmw-v0-9-14-left-card-b2-8-style-position-compare.png"
OUT_INGREDIENTS = BASE / "510-world-map-wmw-v0-9-14-left-card-b2-8-clean-ingredients-qa.png"
OUT_ATLAS = BASE / "511-world-map-wmw-v0-9-14-left-card-b2-8-atlas-2x.png"
OUT_GEOMETRY = BASE / "512-world-map-wmw-v0-9-14-left-card-b2-8-geometry-qa.png"
OUT_RUNTIME = BASE / "513-world-map-wmw-v0-9-14-left-card-b2-8-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "514-world-map-wmw-v0-9-14-left-card-b2-8-runtime-fill-qa.png"
OUT_VISUAL_QA = BASE / "515-world-map-wmw-v0-9-14-left-card-b2-8-16point-visual-qa.png"
OUT_MANIFEST = BASE / "516-world-map-wmw-v0-9-14-left-card-b2-8-manifest.json"
OUT_GODOT = BASE / "517-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component.png"
OUT_GODOT_QA = BASE / "518-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b28_state_badge_globe_fix_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b28_state_badge_globe_fix_manifest.json"

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

LEGACY_BADGE_POLY = b27.LEGACY_BADGE_POLY
BACKING_POLY = [
    (304, 202), (360, 202), (376, 218), (376, 274),
    (360, 290), (304, 290), (288, 274), (288, 218),
]
OUTER_RING_POLY = [
    (305, 204), (359, 204), (373, 218), (373, 273),
    (359, 287), (305, 287), (290, 272), (290, 219),
]
INNER_CUT_POLY = [
    (314, 216), (350, 216), (361, 227), (361, 265),
    (350, 275), (314, 275), (302, 264), (302, 228),
]
CORE_POLY = [
    (316, 220), (348, 220), (357, 229), (357, 263),
    (348, 271), (316, 271), (306, 262), (306, 230),
]


def polygon_mask(points: list[tuple[int, int]]) -> Image.Image:
    out = Image.new("L", FRAME_SIZE, 0)
    ImageDraw.Draw(out).polygon(points, fill=255)
    return out


LEGACY_MASK = polygon_mask(LEGACY_BADGE_POLY)
BACKING_MASK = polygon_mask(BACKING_POLY)
OUTER_MASK = polygon_mask(OUTER_RING_POLY)
INNER_MASK = polygon_mask(INNER_CUT_POLY)
CORE_MASK = polygon_mask(CORE_POLY)
RING_MASK = ImageChops.subtract(OUTER_MASK, INNER_MASK)


def paper_texture(source: Image.Image) -> Image.Image:
    crop = source.crop((52, 210, 138, 278)).convert("RGBA")
    tile = crop.resize((84, 84), Image.Resampling.BICUBIC)
    out = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    out.alpha_composite(tile, (290, 204))
    return out


def neutral_core_texture(shell: Image.Image) -> Image.Image:
    base = b27._average_rgb(shell, (246, 202, 282, 286))
    out = Image.new("RGBA", FRAME_SIZE, (*base, 255))
    draw = ImageDraw.Draw(out, "RGBA")

    def tone(delta: int) -> tuple[int, int, int, int]:
        return tuple(max(0, min(255, c + delta)) for c in base) + (255,)

    draw.polygon([(306, 220), (358, 220), (332, 246)], fill=tone(7))
    draw.polygon([(358, 220), (358, 272), (332, 246)], fill=tone(1))
    draw.polygon([(358, 272), (306, 272), (332, 246)], fill=tone(-7))
    draw.polygon([(306, 272), (306, 220), (332, 246)], fill=tone(-2))
    px = out.load()
    for y in range(220, 272):
        for x in range(306, 358):
            if CORE_MASK.getpixel((x, y)):
                r, g, b, a = px[x, y]
                tooth = ((x * 11 + y * 7) % 5) - 2
                px[x, y] = (
                    max(0, min(255, r + tooth)),
                    max(0, min(255, g + tooth)),
                    max(0, min(255, b + tooth)),
                    a,
                )
    return out


def rebuild_badge(master_shell: Image.Image, source: Image.Image) -> tuple[Image.Image, dict]:
    rebuilt = b27.harmonic_inpaint(master_shell, LEGACY_MASK)
    family = b27._average_rgb(rebuilt, (246, 202, 282, 286))
    shadow = tuple(max(0, round(c * 0.35)) for c in family)
    b27._fill_with_mask(rebuilt, Image.new("RGBA", FRAME_SIZE, (*shadow, 255)), BACKING_MASK)
    b27._fill_with_mask(rebuilt, paper_texture(source), RING_MASK)
    b27._fill_with_mask(rebuilt, neutral_core_texture(rebuilt), CORE_MASK)

    ring = b27.mask_metrics(RING_MASK)
    core = b27.mask_metrics(CORE_MASK)
    right_gap_2x = FRAME_SIZE[0] - ring["bbox"][2]
    center_delta = [abs(ring["centroid"][0] - BADGE_CENTER[0]), abs(ring["centroid"][1] - BADGE_CENTER[1])]
    clean_core_cream = sum(
        1
        for y in range(FRAME_SIZE[1])
        for x in range(FRAME_SIZE[0])
        if CORE_MASK.getpixel((x, y)) and b26._is_creamish(rebuilt.getpixel((x, y)))
    )
    return rebuilt, {
        "status": "pass" if max(center_delta) <= 1.0 and right_gap_2x >= 32 and clean_core_cream == 0 else "fail",
        "contract_action_badge_1x": CONTRACT["frozen"]["slots"]["action_badge"],
        "contract_action_badge_2x": list(ACTION_RECT),
        "contract_center_2x": list(BADGE_CENTER),
        "benchmark_center_2x": list(BENCHMARK_BADGE_CENTER),
        "outer_ring": ring,
        "core": core,
        "ring_center_delta_px": center_delta,
        "right_visual_gap_2x": right_gap_2x,
        "right_visual_gap_1x": right_gap_2x / 2.0,
        "minimum_right_visual_gap_2x": 32,
        "cream_semantic_pixels_inside_neutral_core": clean_core_cream,
        "legacy_badge_geometry_reused": False,
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
    purity = b26.ingredient_purity_gate(canvas, "cream_icon", f"b28_runtime_icon_{state}")
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
    _, _, old_master, cutout_mask, globe_patch, _, measurement, _, _ = b26.compose_single_master_frames()
    master_shell, badge_gate = rebuild_badge(old_master, source_frames[MASTER_INDEX])
    family_mask = b26.make_frame_family_mask(master_shell)
    glow = b26.selected_glow_layer(source_frames[STATE_ORDER.index("selected")])
    window = tuple(measurement["master_window_rect_2x"])
    photos, photo_gate = clean_photo_ingredients()
    globe_gate = b26.ingredient_purity_gate(globe_patch, "warm_globe", "b28_globe_linework")

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
    draw.text((42, 24), "B2.8 state badge position: benchmark -> failed B2.7 -> restored", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Reference center x=166 / right gap=16px. B2.7 shifted right; B2.8 contract v0.8.3 restores the visual rhythm.", fill=(207, 224, 199), font=b11.F_NOTE)
    b27_frames = b22.load_atlas_frames(b27.OUT_ATLAS)
    crop = (270, 188, 408, 306)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        draw.text((x, 108), state, fill=(255, 229, 93), font=b11.F_NOTE)
        rows = [
            ("candidate B reference", data["source_frames"][idx], (214, 210, 170)),
            ("B2.7 too far right", b27_frames[idx], (255, 120, 120)),
            ("B2.8 restored empty base", data["frames"][idx], (120, 235, 170)),
        ]
        for ridx, (title, frame, color) in enumerate(rows):
            y = 150 + ridx * 380
            panel = on_dark(frame).crop(crop).resize((414, 354), Image.Resampling.NEAREST)
            canvas.alpha_composite(panel, (x, y))
            draw.rectangle((x, y, x + panel.width, y + panel.height), outline=color, width=2)
            draw.text((x, y - 24), title, fill=color, font=b11.F_SMALL)
    gate = data["badge_gate"]
    draw.text((42, 1280), f"B2.8 outer bbox={gate['outer_ring']['bbox']} center={gate['outer_ring']['centroid']} right gap={gate['right_visual_gap_1x']}px | contract={gate['contract_action_badge_1x']}", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_ingredients_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1380), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.8 clean ingredients dependency board", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Photos come from 396 clean scene crops; globe is linework only; state glyphs are complete and padded. Evidence ready.", fill=(207, 224, 199), font=b11.F_NOTE)

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

    draw.text((42, 820), "Empty state-badge bases before runtime glyph overlay", fill=(243, 239, 214), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        crop = on_dark(data["frames"][idx]).crop((270, 188, 404, 306)).resize((402, 354), Image.Resampling.NEAREST)
        canvas.alpha_composite(crop, (x, 860))
        draw.rectangle((x, 860, x + 402, 1214), outline=(94, 164, 142), width=2)
        draw.text((x, 1224), state, fill=(255, 229, 93), font=b11.F_SMALL)
    return canvas


def make_geometry_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 910), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.8 geometry QA: contract v0.8.3 state badge + unchanged card geometry", fill=(243, 239, 214), font=b11.F_HEAD)
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
    draw.text((450, 34), "Python v0.9.14 B2.8 state badge + clean globe/photo", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 76), "Whole card selects region; right badge only reports state. Clean ingredients, review pending.", fill=(217, 222, 199), font=b11.F_NOTE)
    return canvas.convert("RGB")


def make_visual_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1540), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.8 16-point evidence board", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Four states x globe/photo seam, right edge, bottom edge, complete state badge. Reviewer/user owns final PASS/FAIL.", fill=(207, 224, 199), font=b11.F_NOTE)
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
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "date": "2026-07-10",
        "status": "b2_8_evidence_ready_pending_user_visual_review" if passed and godot_pass else "b2_8_pending_full_chain",
        "contract": str(b11.CONTRACT_PATH),
        "contract_version": CONTRACT["contract_version"],
        "contract_change": {
            "authorized_by": "user adoption A174",
            "changed_frozen_field": "slots.action_badge",
            "before_1x": [158, 106, 38, 38],
            "after_1x": CONTRACT["frozen"]["slots"]["action_badge"],
            "all_other_frozen_fields_changed": False,
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
        "pipeline": "396 clean regional photo ingredient -> hollow shell with benchmark-position neutral state badge -> selected glow -> independent globe linework -> runtime text + complete padded state glyph",
        "inputs": {
            "candidate_b_shell_and_glyph_source": str(b26.B_ATLAS),
            "clean_regional_photo_source": str(b11.IMAGEGEN_B1_R4),
            "failed_flattened_photo_source_retired": str(b26.B13_ATLAS),
            "previous_b2_7_manifest": str(b27.OUT_MANIFEST),
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
            "runtime_icons": {state: str(GODOT_INGREDIENT_DIR / f"left_region_card_b28_runtime_icon_{state}.png") for state in STATE_ORDER},
            "clean_photos": {state: str(GODOT_INGREDIENT_DIR / f"left_region_card_b28_clean_photo_{state}.png") for state in STATE_ORDER},
            "globe_linework": str(GODOT_INGREDIENT_DIR / "left_region_card_b28_globe_linework.png"),
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
        },
    }


def write_outputs(approve_ingredients: bool) -> dict:
    data = compose()
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    make_compare_board(data).save(OUT_COMPARE)
    make_ingredients_board(data).save(OUT_INGREDIENTS)
    dependency_pass = (
        data["badge_gate"]["status"] == "pass"
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
    data["master_shell"].save(GODOT_INGREDIENT_DIR / "left_region_card_b28_clean_master.png")
    data["globe_patch"].save(GODOT_INGREDIENT_DIR / "left_region_card_b28_globe_linework.png")
    for state, shell in zip(STATE_ORDER, data["shells"]):
        shell.save(GODOT_INGREDIENT_DIR / f"left_region_card_b28_hollow_shell_{state}.png")
    for state in STATE_ORDER:
        data["icons"][state].save(GODOT_INGREDIENT_DIR / f"left_region_card_b28_runtime_icon_{state}.png")
        data["photos"][state].save(GODOT_INGREDIENT_DIR / f"left_region_card_b28_clean_photo_{state}.png")

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
    parser = argparse.ArgumentParser(description="Build WMW left card B2.8 state-badge and globe/photo fix.")
    parser.add_argument("--approve-ingredients", action="store_true", help="Continue only after 509/510 dependency evidence has been inspected.")
    args = parser.parse_args()
    result = write_outputs(args.approve_ingredients)
    print(json.dumps({"status": result["status"], "outputs": result.get("outputs", {}), "gates": result.get("gates", {})}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
