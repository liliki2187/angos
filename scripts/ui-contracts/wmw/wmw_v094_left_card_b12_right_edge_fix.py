# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

OUT_CANDIDATE = BASE / "416-world-map-wmw-v0-9-4-left-card-candidate-b1-2-right-edge-clean.png"
OUT_QA = BASE / "417-world-map-wmw-v0-9-4-left-card-candidate-b1-2-geometry-qa.png"
OUT_ATLAS = BASE / "418-world-map-wmw-v0-9-4-left-card-candidate-b1-2-atlas-2x.png"
OUT_RUNTIME = BASE / "419-world-map-wmw-v0-9-4-left-card-candidate-b1-2-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "420-world-map-wmw-v0-9-4-left-card-candidate-b1-2-runtime-fill-qa.png"
OUT_MANIFEST = BASE / "421-world-map-wmw-v0-9-4-left-card-candidate-b1-2-manifest.json"
OUT_EDGE_QA = BASE / "422-world-map-wmw-v0-9-4-left-card-candidate-b1-2-right-edge-closeup-qa.png"
OUT_GODOT = BASE / "423-world-map-wmw-v0-9-4-left-card-candidate-b1-2-godot-single-component.png"
OUT_GODOT_QA = BASE / "424-world-map-wmw-v0-9-4-left-card-candidate-b1-2-godot-single-component-qa.png"
OUT_COMPARE = BASE / "425-world-map-wmw-v0-9-4-left-card-b1-1-vs-b1-2-right-edge-fix-board.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_candidate_b12_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_candidate_b12_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
PHOTO_RECT_2X = b11.PHOTO_RECT_2X
TARGET_RATIO = b11.TARGET_RATIO
RATIO_TOLERANCE = b11.RATIO_TOLERANCE

# B1.2 crops are narrower on the right than B1.1, because the B1.1 failure was
# a source-frame edge carried into the photo patch.
PHOTO_RELS = {
    "selected": (0.31, 0.09, 0.86, 0.59),
    "available": (0.31, 0.09, 0.80, 0.59),
    "warning": (0.29, 0.09, 0.84, 0.60),
    "locked": (0.31, 0.09, 0.80, 0.60),
}

RIGHT_EDGE_CROP = (300, 24, 408, 288)
RIGHT_EDGE_REPAIR_PX = 42
PHOTO_OUTER_BAND = (PHOTO_RECT_2X[2], PHOTO_RECT_2X[1], FRAME_SIZE[0], PHOTO_RECT_2X[3])
ALPHA_HOLE_PROBE = (PHOTO_RECT_2X[2], 40, FRAME_SIZE[0], 300)
ALPHA_CONTROL_PROBE = (42, 40, PHOTO_RECT_2X[2], 300)


def crop_source_photo(source: Image.Image, box: tuple[int, int, int, int], state: str) -> Image.Image:
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    rx1, ry1, rx2, ry2 = PHOTO_RELS[state]
    crop_box = (
        round(x1 + w * rx1),
        round(y1 + h * ry1),
        round(x1 + w * rx2),
        round(y1 + h * ry2),
    )
    patch = source.crop(crop_box).convert("RGB")
    patch = b11.scrub_photo_patch_edges(patch)
    target_size = (PHOTO_RECT_2X[2] - PHOTO_RECT_2X[0], PHOTO_RECT_2X[3] - PHOTO_RECT_2X[1])
    patch = ImageOps.fit(patch, target_size, method=Image.Resampling.LANCZOS, centering=(0.48, 0.54))
    patch = hard_repair_photo_right_edge(patch.convert("RGBA"))
    return patch


def hard_repair_photo_right_edge(patch: Image.Image) -> Image.Image:
    out = patch.convert("RGBA")
    px = out.load()
    w, h = out.size
    repair_start = max(0, w - RIGHT_EDGE_REPAIR_PX)
    ref_start = max(0, repair_start - RIGHT_EDGE_REPAIR_PX - 14)
    for y in range(h):
        for x in range(repair_start, w):
            src_x = ref_start + ((x - repair_start) % max(1, RIGHT_EDGE_REPAIR_PX))
            r1, g1, b1, a1 = px[src_x, y]
            r0, g0, b0, a0 = px[max(0, repair_start - 1), y]
            t = (x - repair_start) / max(1, w - repair_start - 1)
            px[x, y] = (
                round(r1 * (0.72 + 0.18 * t) + r0 * (0.28 - 0.18 * t)),
                round(g1 * (0.72 + 0.18 * t) + g0 * (0.28 - 0.18 * t)),
                round(b1 * (0.72 + 0.18 * t) + b0 * (0.28 - 0.18 * t)),
                max(a1, a0),
            )
    return out


def repair_photo_outer_band(clean: Image.Image, base: Image.Image) -> Image.Image:
    out = clean.convert("RGBA")
    px = out.load()
    x1, y1, x2, y2 = PHOTO_OUTER_BAND
    # The band outside photo_slot must not carry photo-source or source-shell
    # vertical texture. Keep only a tiny inner shadow at the slot edge, then let
    # the rest return to transparent bleed.
    for y in range(y1, y2):
        for x in range(x1, x2):
            if x - x1 <= 2:
                r, g, b, a = px[max(0, x1 - 1), y]
                px[x, y] = (round(r * 0.30), round(g * 0.30), round(b * 0.30), max(a, 210))
            else:
                px[x, y] = (0, 0, 0, 0)
    return out


def scrub_right_outer_bleed(frame: Image.Image) -> Image.Image:
    out = frame.convert("RGBA")
    px = out.load()
    # B1.2 failure note: this treated legitimate right-shell material as
    # disposable bleed. Keep the behavior only to regenerate the failed
    # evidence/manifest; do not use this as a production repair path.
    for y in range(24, 288):
        for x in range(393, FRAME_SIZE[0]):
            px[x, y] = (0, 0, 0, 0)
    return out


def compose_frames(contract: dict) -> tuple[list[Image.Image], list[dict], list[dict]]:
    base_frames, base_meta = b11.source_frames(b11.SOURCE_B)
    art_source = Image.open(b11.IMAGEGEN_B1_R4).convert("RGB")
    art_mask = b11.b1.build_mask(art_source)
    art_boxes = b11.b1.find_quadrant_boxes(art_mask)
    photo_rect = b11.slot_rect(contract, "photo_slot")

    frames: list[Image.Image] = []
    composition: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        base = base_frames[idx].copy()
        photo = crop_source_photo(art_source, art_boxes[idx], state)
        clean = base.copy()
        clean.alpha_composite(photo, (photo_rect[0], photo_rect[1]))
        clean = repair_photo_outer_band(clean, base)
        clean = scrub_right_outer_bleed(clean)
        clean = b11.restore_baked_globe_only(clean, base)
        if state == "warning":
            clean = b11.recolor_warning_triangle(clean)
        clean = b11.b1.zero_chroma_alpha(clean)
        clean = b11.scrub_nonselected_artifact_green(clean, state)
        frames.append(clean)
        composition.append(
            {
                "state": state,
                "base_source": str(b11.SOURCE_B),
                "photo_source": str(b11.IMAGEGEN_B1_R4),
                "photo_source_box": list(art_boxes[idx]),
                "photo_rel_crop_b1_2": list(PHOTO_RELS[state]),
                "photo_slot_2x": list(photo_rect),
                "photo_right_edge_repair_px": RIGHT_EDGE_REPAIR_PX,
                "photo_outer_band_2x": list(PHOTO_OUTER_BAND),
                "runtime_warning_triangle_overlay": "removed",
            }
        )
    return frames, base_meta, composition


def make_candidate_sheet(frames: list[Image.Image]) -> Image.Image:
    sheet = b11.make_candidate_sheet(frames)
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, sheet.width, 48), fill=(18, 30, 31, 255))
    draw.text((54, 16), "B1.2 v0.9.4 right-edge clean source", fill=(236, 231, 197), font=b11.F_HEAD)
    return sheet


def make_runtime_preview(frames: list[Image.Image], contract: dict, show_qa: bool) -> Image.Image:
    img = b11.make_runtime_preview(frames, contract, show_qa)
    draw = ImageDraw.Draw(img)
    draw.rectangle((445, 30, 1120, 72), fill=(7, 19, 21))
    draw.text((450, 34), "Python v0.9.4 B1.2 left_region_card runtime fill", fill=(243, 239, 214), font=b11.F_HEAD)
    return img


def make_right_edge_qa(frames: list[Image.Image], title: str) -> Image.Image:
    crop = RIGHT_EDGE_CROP
    scale = 4
    gap = 18
    panel_w = (crop[2] - crop[0]) * scale
    panel_h = (crop[3] - crop[1]) * scale
    out = Image.new("RGB", (40 + len(frames) * panel_w + (len(frames) - 1) * gap + 40, panel_h + 110), (12, 23, 24))
    draw = ImageDraw.Draw(out)
    draw.text((24, 16), title, fill=(240, 236, 205), font=b11.F_NOTE)
    x = 24
    y = 56
    for i, state in enumerate(STATE_ORDER):
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(frames[i])
        c = bg.crop(crop).resize((panel_w, panel_h), Image.Resampling.NEAREST).convert("RGB")
        out.paste(c, (x, y))
        draw.rectangle((x, y, x + panel_w, y + panel_h), outline=(190, 196, 184), width=2)
        for xx, color, label in [
            (PHOTO_RECT_2X[2], (255, 85, 85), "photo x390"),
        ]:
            if crop[0] <= xx <= crop[2]:
                px = x + (xx - crop[0]) * scale
                draw.line((px, y, px, y + panel_h), fill=color, width=2)
                draw.text((px + 3, y + 4), label, fill=color, font=b11.F_SMALL)
        draw.text((x, y + panel_h + 8), f"{state}: FAIL, alpha hole in x390..408", fill=(255, 150, 132), font=b11.F_SMALL)
        x += panel_w + gap
    return out


def right_edge_band_stats(frames: list[Image.Image]) -> dict:
    stats: dict[str, dict] = {}
    x1, y1, x2, y2 = PHOTO_OUTER_BAND
    for state, frame in zip(STATE_ORDER, frames):
        img = frame.convert("RGBA")
        px = img.load()
        high_chroma = 0
        transparent_bleed = 0
        vertical_jump = 0
        for y in range(y1, y2):
            prev = None
            for x in range(x1, x2):
                r, g, b, a = px[x, y]
                if a < 220:
                    transparent_bleed += 1
                if g > 145 and g > r * 1.22 and g > b * 1.12:
                    high_chroma += 1
                lum = (r + g + b) / 3
                if prev is not None and abs(lum - prev) > 55:
                    vertical_jump += 1
                prev = lum
        stats[state] = {
            "range_2x": list(PHOTO_OUTER_BAND),
            "high_chroma_green_pixels": high_chroma,
            "transparent_bleed_pixels": transparent_bleed,
            "vertical_luminance_jumps_gt55": vertical_jump,
            "status": "pass" if high_chroma == 0 and vertical_jump <= 6 else "fail",
        }
    return stats


def alpha_hole_probe_stats(frames: list[Image.Image]) -> dict:
    stats: dict[str, dict] = {}
    hx1, hy1, hx2, hy2 = ALPHA_HOLE_PROBE
    cx1, cy1, cx2, cy2 = ALPHA_CONTROL_PROBE
    for state, frame in zip(STATE_ORDER, frames):
        img = frame.convert("RGBA")
        px = img.load()
        hole_pixels = 0
        control_pixels = 0
        samples: list[list[int]] = []
        for y in range(hy1, hy2):
            for x in range(hx1, hx2):
                a = px[x, y][3]
                if a < 250:
                    hole_pixels += 1
                    if len(samples) < 8:
                        samples.append([x, y, a])
        for y in range(cy1, cy2):
            for x in range(cx1, cx2):
                if px[x, y][3] < 250:
                    control_pixels += 1
        stats[state] = {
            "alpha_hole_probe_range_2x": list(ALPHA_HOLE_PROBE),
            "opaque_control_probe_range_2x": list(ALPHA_CONTROL_PROBE),
            "transparent_pixels_in_right_shell_band": hole_pixels,
            "transparent_pixels_in_body_control": control_pixels,
            "threshold": "alpha < 250",
            "sample_transparent_pixels": samples,
            "status": "fail" if hole_pixels > 0 else "pass",
        }
    return stats


def make_manifest(
    contract: dict,
    base_meta: list[dict],
    composition: list[dict],
    geometry_metrics: list[dict],
    green_stats: dict,
    edge_stats: dict,
    alpha_hole_stats: dict,
) -> dict:
    manifest = b11.make_manifest(contract, base_meta, composition, geometry_metrics, green_stats)
    manifest["asset_id"] = "world_map_wmw_left_region_card_candidate_b1_2"
    manifest["version"] = "v0.9.4"
    manifest["status"] = "candidate_b1_2_failed_user_review_right_frame_interrupted_and_layer_leakage"
    manifest["outputs"] = {
        "candidate_b1_2_composite": str(OUT_CANDIDATE),
        "geometry_qa": str(OUT_QA),
        "atlas_2x": str(OUT_ATLAS),
        "runtime_fill_preview": str(OUT_RUNTIME),
        "runtime_fill_qa": str(OUT_RUNTIME_QA),
        "right_edge_closeup_qa": str(OUT_EDGE_QA),
        "godot_single_component": str(OUT_GODOT),
        "godot_single_component_qa": str(OUT_GODOT_QA),
        "b1_1_vs_b1_2_right_edge_fix_board": str(OUT_COMPARE),
        "godot_atlas_copy": str(GODOT_ATLAS),
        "godot_manifest_copy": str(GODOT_MANIFEST),
    }
    manifest["composition"] = composition
    manifest["right_edge_band_stats"] = edge_stats
    manifest["alpha_hole_probe_stats"] = alpha_hole_stats
    checks = {}
    for state in STATE_ORDER:
        checks[state] = {
            "duplicate_globe": "pass_none_visible",
            "source_frame_residue": "fail_gate_target_incomplete; right-edge stats did not protect shell continuity",
            "photo_slot_overflow": "pass_none_visible; photo pixels clipped before paste to 2x slot",
            "right_edge_strip": "fail_user_review: strip symptom hidden by over-erasing legitimate frame pixels",
            "right_frame_continuity": "fail_user_review: right shell/frame is interrupted by a transparent hole",
            "layer_order_integrity": "fail_user_review: the transparent hole reveals background/underlay and reads as covered image content",
            "card_body_opacity": "fail_alpha_probe: x390..408,y40..300 contains transparent pixels inside the visible card body",
            "manual_check_basis": "User review of 419 runtime fill screenshot on 2026-07-08; warning state is direct evidence and same repair path applies to all states",
        }
    manifest["gates"]["composite_cleanliness"] = {
        "status": "fail",
        "basis": "B1.2 removed the visible source strip by erasing x393..408, but that band includes legitimate right-shell pixels; alpha probe confirms a transparent hole inside the card body",
        "checks": checks,
    }
    manifest["gates"]["right_edge_closeup"] = {
        "status": "fail",
        "basis": "422 only measured chroma/vertical jumps and missed frame continuity plus layer-order integrity; numeric stats are retained as non-authoritative diagnostics",
        "stats": edge_stats,
    }
    manifest["gates"]["right_frame_continuity"] = {
        "status": "fail",
        "basis": "The right border must remain a continuous opaque shell layer above the photo slot; B1.2 over-erased that shell band.",
    }
    manifest["gates"]["layer_order_integrity"] = {
        "status": "fail",
        "basis": "The photo layer must be clipped below a preserved shell/frame mask; B1.2 creates a transparent hole that reads as background/underlay leakage.",
    }
    manifest["gates"]["card_body_opacity_probe"] = {
        "status": "fail" if any(v["transparent_pixels_in_right_shell_band"] > 0 for v in alpha_hole_stats.values()) else "pass",
        "basis": "Visible card-body pixels must be opaque; probe x390..408,y40..300 catches the B1.2 transparent vertical hole that dark backgrounds hide.",
        "stats": alpha_hole_stats,
    }
    manifest["visual_repair_notes"] = [
        "B1.2 does not reroll imagegen and does not change the left_region_card contract.",
        "B1.2 is rejected as failed evidence: it optimized for removing the visible right-edge strip by creating a transparent hole inside the card body.",
        "Root cause: a flattened-card pixel scrub was used where a layered composite was required: photo clipped to slot below, shell/frame mask above, badge/icon above, runtime text above.",
        "The right-edge close-up gate was incomplete because it checked green/chroma/jump stats but not card-body opacity, frame continuity, or hidden underlay visibility.",
        "B1.1 and B1.2 remain archived as failed evidence; do not promote either to production.",
    ]
    return manifest


def make_compare_board() -> None:
    b11_img = Image.open(BASE / "415-world-map-wmw-v0-9-4-left-card-b1-1-right-edge-diagnostic-closeup.png").convert("RGB")
    b12_img = Image.open(OUT_EDGE_QA).convert("RGB")
    w = max(b11_img.width, b12_img.width) + 96
    h = b11_img.height + b12_img.height + 150
    out = Image.new("RGB", (w, h), (12, 23, 24))
    draw = ImageDraw.Draw(out)
    draw.text((48, 30), "B1.1 -> B1.2 right-edge failure board", fill=(245, 239, 209), font=b11.F_HEAD)
    draw.text((48, 72), "Top: failed B1.1; bottom: failed B1.2, strip removed but right frame/layering broken.", fill=(218, 226, 206), font=b11.F_NOTE)
    out.paste(b11_img, (48, 120))
    out.paste(b12_img, (48, 120 + b11_img.height + 28))
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT_COMPARE)


def save_outputs() -> None:
    contract = b11.load_contract()
    frames, base_meta, composition = compose_frames(contract)
    candidate = make_candidate_sheet(frames)
    qa, geometry_metrics = b11.make_geometry_qa(frames, composition)
    atlas = b11.make_atlas(frames)
    runtime = make_runtime_preview(frames, contract, show_qa=False)
    runtime_qa = make_runtime_preview(frames, contract, show_qa=True)
    edge_qa = make_right_edge_qa(frames, "B1.2 right-edge close-up QA 400%: failed alpha-hole probe at x390..408")
    green_stats = b11.artifact_green_stats(frames)
    edge_stats = right_edge_band_stats(frames)
    alpha_hole_stats = alpha_hole_probe_stats(frames)
    manifest = make_manifest(contract, base_meta, composition, geometry_metrics, green_stats, edge_stats, alpha_hole_stats)

    for path in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_EDGE_QA]:
        path.parent.mkdir(parents=True, exist_ok=True)
    candidate.save(OUT_CANDIDATE)
    qa.save(OUT_QA)
    atlas.save(OUT_ATLAS)
    runtime.save(OUT_RUNTIME)
    runtime_qa.save(OUT_RUNTIME_QA)
    edge_qa.save(OUT_EDGE_QA)
    make_compare_board()

    manifest["image_content_checks"] = {
        "candidate": b11.count_colors_nonblack(OUT_CANDIDATE),
        "geometry_qa": b11.count_colors_nonblack(OUT_QA),
        "atlas_2x": b11.count_colors_nonblack(OUT_ATLAS),
        "runtime_fill_preview": b11.count_colors_nonblack(OUT_RUNTIME),
        "runtime_fill_qa": b11.count_colors_nonblack(OUT_RUNTIME_QA),
        "right_edge_closeup_qa": b11.count_colors_nonblack(OUT_EDGE_QA),
        "b1_1_vs_b1_2_right_edge_fix_board": b11.count_colors_nonblack(OUT_COMPARE),
    }
    if OUT_GODOT.exists() and OUT_GODOT_QA.exists():
        manifest["image_content_checks"]["godot_single_component"] = b11.count_colors_nonblack(OUT_GODOT)
        manifest["image_content_checks"]["godot_single_component_qa"] = b11.count_colors_nonblack(OUT_GODOT_QA)
        manifest["gates"]["godot_windowed_capture"] = {
            "status": "pass",
            "basis": "windowed opengl3 capture via scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro; nonblack and color-diversity checks recorded",
            "headless_used_for_ui_capture": False,
        }
    else:
        manifest["gates"]["godot_windowed_capture"] = {
            "status": "pending",
            "basis": "run scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro after switching the capture script to the B1.2 atlas",
            "headless_used_for_ui_capture": False,
        }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    for path in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_MANIFEST, OUT_EDGE_QA, OUT_COMPARE, GODOT_ATLAS, GODOT_MANIFEST]:
        print(path)


if __name__ == "__main__":
    save_outputs()
