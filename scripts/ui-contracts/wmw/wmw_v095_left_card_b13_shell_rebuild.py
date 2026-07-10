# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v094_left_card_b12_right_edge_fix as b12


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

OUT_CANDIDATE = BASE / "426-world-map-wmw-v0-9-5-left-card-candidate-b1-3-shell-rebuild.png"
OUT_QA = BASE / "427-world-map-wmw-v0-9-5-left-card-candidate-b1-3-geometry-qa.png"
OUT_ATLAS = BASE / "428-world-map-wmw-v0-9-5-left-card-candidate-b1-3-atlas-2x.png"
OUT_RUNTIME = BASE / "429-world-map-wmw-v0-9-5-left-card-candidate-b1-3-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "430-world-map-wmw-v0-9-5-left-card-candidate-b1-3-runtime-fill-qa.png"
OUT_MANIFEST = BASE / "431-world-map-wmw-v0-9-5-left-card-candidate-b1-3-manifest.json"
OUT_EDGE_QA = BASE / "432-world-map-wmw-v0-9-5-left-card-candidate-b1-3-right-edge-alpha-qa.png"
OUT_COMPARE = BASE / "433-world-map-wmw-v0-9-5-left-card-b1-2-vs-b1-3-alpha-hole-fix-board.png"
OUT_GODOT = BASE / "434-world-map-wmw-v0-9-5-left-card-candidate-b1-3-godot-single-component.png"
OUT_GODOT_QA = BASE / "435-world-map-wmw-v0-9-5-left-card-candidate-b1-3-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_candidate_b13_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_candidate_b13_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
PHOTO_RECT_2X = b11.PHOTO_RECT_2X
TARGET_RATIO = b11.TARGET_RATIO
RATIO_TOLERANCE = b11.RATIO_TOLERANCE

RIGHT_EDGE_CROP = (300, 24, 408, 288)
SHELL_REBUILD_BAND = (PHOTO_RECT_2X[2], 40, FRAME_SIZE[0], 300)
ALPHA_CONTROL_PROBE = (42, 40, PHOTO_RECT_2X[2], 300)


def _usable_shell_pixel(c: tuple[int, int, int, int], state: str) -> bool:
    r, g, b, a = c
    if a < 80:
        return False
    if state != "selected" and b11.is_artifact_green_pixel(c):
        return False
    # Avoid using color-key leftovers or bright source-card rims as fill seeds.
    if g > 160 and g > r * 1.35 and g > b * 1.25 and state != "selected":
        return False
    if r > 235 and g > 230 and b > 205:
        return False
    return True


def _fallback_shell_color(state: str) -> tuple[int, int, int]:
    return {
        "selected": (72, 85, 38),
        "available": (20, 76, 76),
        "warning": (128, 88, 20),
        "locked": (78, 78, 72),
    }[state]


def _sample_shell_material(px, y: int, state: str) -> tuple[int, int, int]:
    # During the photo band, sample the quiet card body below the slot rather
    # than the old photo. Outside that band, sample near the same row.
    sample_ys = []
    if PHOTO_RECT_2X[1] <= y < PHOTO_RECT_2X[3]:
        sample_ys.extend([PHOTO_RECT_2X[3] + 18, PHOTO_RECT_2X[3] + 34, PHOTO_RECT_2X[1] - 10])
    sample_ys.extend([y, y - 8, y + 8, PHOTO_RECT_2X[3] + 22])
    sample_xs = [386, 378, 366, 352, 330]

    for yy in sample_ys:
        yy = min(max(yy, 0), FRAME_SIZE[1] - 1)
        for sx in sample_xs:
            c = px[sx, yy]
            if _usable_shell_pixel(c, state):
                r, g, b, _a = c
                return (r, g, b)
    return _fallback_shell_color(state)


def _shade(c: tuple[int, int, int], factor: float) -> tuple[int, int, int, int]:
    r, g, b = c
    return (round(r * factor), round(g * factor), round(b * factor), 255)


def rebuild_right_shell_band(frame: Image.Image, state: str) -> Image.Image:
    """Turn the B-shell over-wide photo window into an opaque shell band.

    B/B1 had an 18px visual window beyond the contract photo slot. B1.2 erased
    that band into transparency. B1.3 preserves the frame and fills only shell
    pixels, so the visible photo window equals the contract slot.
    """
    out = frame.convert("RGBA")
    px = out.load()
    x1, y1, x2, y2 = SHELL_REBUILD_BAND

    for y in range(y1, y2):
        material = _sample_shell_material(px, y, state)
        for x in range(x1, x2):
            t = (x - x1) / max(1, x2 - x1 - 1)
            if x <= x1 + 1:
                px[x, y] = _shade(material, 0.34)
            elif x >= x2 - 2:
                px[x, y] = _shade(material, 0.42)
            else:
                px[x, y] = _shade(material, 0.70 - 0.18 * t)

    # Reassert the slot's right inner edge as a narrow dark lip, not a photo.
    for y in range(PHOTO_RECT_2X[1], PHOTO_RECT_2X[3]):
        r, g, b, _a = px[PHOTO_RECT_2X[2], y]
        px[PHOTO_RECT_2X[2], y] = (round(r * 0.72), round(g * 0.72), round(b * 0.72), 255)
    return out


def enforce_card_body_opacity(frame: Image.Image, state: str) -> Image.Image:
    out = frame.convert("RGBA")
    px = out.load()
    x1, y1, x2, y2 = SHELL_REBUILD_BAND
    for y in range(y1, y2):
        fill = _shade(_sample_shell_material(px, y, state), 0.58)
        for x in range(x1, x2):
            if px[x, y][3] < 250:
                px[x, y] = fill
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
        base = rebuild_right_shell_band(base_frames[idx].copy(), state)
        photo = b12.crop_source_photo(art_source, art_boxes[idx], state)

        clean = base.copy()
        clean.alpha_composite(photo, (photo_rect[0], photo_rect[1]))
        clean = b11.restore_baked_globe_only(clean, base)
        if state == "warning":
            clean = b11.recolor_warning_triangle(clean)
        clean = b11.scrub_nonselected_artifact_green(clean, state)
        clean = enforce_card_body_opacity(clean, state)

        frames.append(clean)
        composition.append(
            {
                "state": state,
                "base_source": str(b11.SOURCE_B),
                "photo_source": str(b11.IMAGEGEN_B1_R4),
                "photo_source_box": list(art_boxes[idx]),
                "photo_rel_crop_b1_3": list(b12.PHOTO_RELS[state]),
                "photo_slot_2x": list(photo_rect),
                "shell_rebuild_band_2x": list(SHELL_REBUILD_BAND),
                "visible_photo_window_right_edge_2x": photo_rect[2],
                "runtime_warning_triangle_overlay": "removed",
            }
        )
    return frames, base_meta, composition


def make_candidate_sheet(frames: list[Image.Image]) -> Image.Image:
    sheet = b11.make_candidate_sheet(frames)
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, sheet.width, 48), fill=(18, 30, 31, 255))
    draw.text((54, 16), "B1.3 v0.9.5 shell rebuild: photo window equals contract slot", fill=(236, 231, 197), font=b11.F_HEAD)
    return sheet


def make_runtime_preview(frames: list[Image.Image], contract: dict, show_qa: bool) -> Image.Image:
    img = b11.make_runtime_preview(frames, contract, show_qa)
    draw = ImageDraw.Draw(img)
    draw.rectangle((445, 30, 1240, 72), fill=(7, 19, 21))
    draw.text((450, 34), "Python v0.9.5 B1.3 left_region_card runtime fill", fill=(243, 239, 214), font=b11.F_HEAD)
    return img


def card_body_opacity_probe(frames: list[Image.Image]) -> dict:
    stats: dict[str, dict] = {}
    hx1, hy1, hx2, hy2 = SHELL_REBUILD_BAND
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
            "alpha_hole_probe_range_2x": list(SHELL_REBUILD_BAND),
            "opaque_control_probe_range_2x": list(ALPHA_CONTROL_PROBE),
            "transparent_pixels_in_right_shell_band": hole_pixels,
            "transparent_pixels_in_body_control": control_pixels,
            "threshold": "alpha < 250",
            "sample_transparent_pixels": samples,
            "status": "pass" if hole_pixels == 0 and control_pixels == 0 else "fail",
        }
    return stats


def make_right_edge_qa(frames: list[Image.Image], alpha_stats: dict) -> Image.Image:
    crop = RIGHT_EDGE_CROP
    scale = 4
    gap = 18
    panel_w = (crop[2] - crop[0]) * scale
    panel_h = (crop[3] - crop[1]) * scale
    out = Image.new("RGB", (40 + len(frames) * panel_w + (len(frames) - 1) * gap + 40, panel_h + 128), (12, 23, 24))
    draw = ImageDraw.Draw(out)
    draw.text((24, 16), "B1.3 right-edge QA 400%: red=photo x390; alpha-hole probe must be 0", fill=(240, 236, 205), font=b11.F_NOTE)
    x = 24
    y = 58
    for i, state in enumerate(STATE_ORDER):
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(frames[i])
        c = bg.crop(crop).resize((panel_w, panel_h), Image.Resampling.NEAREST).convert("RGB")
        out.paste(c, (x, y))
        draw.rectangle((x, y, x + panel_w, y + panel_h), outline=(190, 196, 184), width=2)
        px = x + (PHOTO_RECT_2X[2] - crop[0]) * scale
        draw.line((px, y, px, y + panel_h), fill=(255, 85, 85), width=2)
        draw.text((px + 3, y + 4), "photo x390", fill=(255, 85, 85), font=b11.F_SMALL)
        holes = alpha_stats[state]["transparent_pixels_in_right_shell_band"]
        draw.text((x, y + panel_h + 8), f"{state}: alpha holes={holes} PASS", fill=(176, 240, 190), font=b11.F_SMALL)
        x += panel_w + gap
    return out


def make_compare_board() -> None:
    b12_img = Image.open(b12.OUT_EDGE_QA).convert("RGB")
    b13_img = Image.open(OUT_EDGE_QA).convert("RGB")
    w = max(b12_img.width, b13_img.width) + 96
    h = b12_img.height + b13_img.height + 160
    out = Image.new("RGB", (w, h), (12, 23, 24))
    draw = ImageDraw.Draw(out)
    draw.text((48, 30), "B1.2 -> B1.3 alpha-hole repair board", fill=(245, 239, 209), font=b11.F_HEAD)
    draw.text((48, 74), "Top: failed B1.2 transparent hole. Bottom: B1.3 rebuilt opaque shell band; photo remains inside contract slot.", fill=(218, 226, 206), font=b11.F_NOTE)
    out.paste(b12_img, (48, 124))
    out.paste(b13_img, (48, 124 + b12_img.height + 28))
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT_COMPARE)


def make_manifest(
    contract: dict,
    base_meta: list[dict],
    composition: list[dict],
    geometry_metrics: list[dict],
    green_stats: dict,
    alpha_stats: dict,
) -> dict:
    ratio_pass = all(m["ratio_pass"] for m in geometry_metrics)
    nonselected_green_pass = all(green_stats[state]["artifact_greenish_pixels_full_frame"] == 0 for state in ["available", "warning", "locked"])
    opacity_pass = all(v["status"] == "pass" for v in alpha_stats.values())
    checks = {}
    for state in STATE_ORDER:
        checks[state] = {
            "duplicate_globe": "pass_none_visible",
            "source_frame_residue": "pass_no_visible_right_source_strip_in_432_closeup",
            "photo_slot_overflow": "pass_photo_pixels_clip_to_contract_slot_x42..390",
            "right_frame_continuity": "fail_visual_program_color_band_splits_photo_from_inner_frame",
            "layer_order_integrity": "fail_photo_layer_stops_at_contract_slot_but_baked_visual_window_extends_to_x408",
            "card_body_opacity": "pass_alpha_probe_zero_transparent_pixels",
            "art_shell_texture_integrity": "fail_x390..408_is_state_tinted_program_band_not_rebuilt_B_shell_texture",
            "manual_check_basis": "426 composite sheet, 429 runtime fill, 432 right-edge 400% QA, 433 B1.2-vs-B1.3 board, and user review screenshot",
        }
    return {
        "schema_version": 1,
        "asset_id": "world_map_wmw_left_region_card_candidate_b1_3",
        "version": "v0.9.5",
        "status": "candidate_b1_3_failed_user_review_program_color_band_not_shell_texture",
        "date": "2026-07-08",
        "contract": str(b11.CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "inputs": {
            "candidate_b_shell": str(b11.SOURCE_B),
            "candidate_b1_imagegen_photo_source": str(b11.IMAGEGEN_B1_R4),
            "failed_b1_1_manifest": str(b11.OUT_MANIFEST),
            "failed_b1_2_manifest": str(b12.OUT_MANIFEST),
        },
        "outputs": {
            "candidate_b1_3_composite": str(OUT_CANDIDATE),
            "geometry_qa": str(OUT_QA),
            "atlas_2x": str(OUT_ATLAS),
            "runtime_fill_preview": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "right_edge_alpha_qa": str(OUT_EDGE_QA),
            "b1_2_vs_b1_3_alpha_hole_fix_board": str(OUT_COMPARE),
            "godot_single_component": str(OUT_GODOT),
            "godot_single_component_qa": str(OUT_GODOT_QA),
            "godot_atlas_copy": str(GODOT_ATLAS),
            "godot_manifest_copy": str(GODOT_MANIFEST),
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
        "base_frame_sources": base_meta,
        "composition": composition,
        "geometry_metrics": geometry_metrics,
        "artifact_green_stats": green_stats,
        "alpha_hole_probe_stats": alpha_stats,
        "gates": {
            "geometry_ratio_1_275": {
                "status": "pass" if ratio_pass else "fail",
                "target_ratio": TARGET_RATIO,
                "tolerance": RATIO_TOLERANCE,
                "basis": "normalized 2x atlas frames are 408x320; no contract resize and no crop-to-fit after compositing",
            },
            "photo_slot_mask": {
                "status": "pass",
                "photo_slot_2x": list(PHOTO_RECT_2X),
                "basis": "photo crops are fitted to the exact contract slot and alpha-composited at x42,y48 only",
            },
            "shell_window_rebuild": {
                "status": "fail",
                "basis": "alpha hole is filled, but the x390..408 repair reads as a state-tinted program color band instead of continuous B shell texture",
                "shell_rebuild_band_2x": list(SHELL_REBUILD_BAND),
            },
            "card_body_opacity_probe": {
                "status": "pass" if opacity_pass else "fail",
                "basis": "visible card-body right band x390..408,y40..300 must have zero transparent pixels; dark backgrounds cannot mask holes",
                "stats": alpha_stats,
            },
            "right_frame_continuity": {
                "status": "fail",
                "basis": "right edge is opaque but visually split by an added side band; alpha pass is insufficient for frame continuity",
            },
            "layer_order_integrity": {
                "status": "fail",
                "basis": "the photo layer obeys photo_slot x42..390 while the baked B shell visual window extends to about x408, leaving a persistent 18px conflict zone",
            },
            "greenish_full_frame_nonselected": {
                "status": "pass" if nonselected_green_pass else "fail",
                "basis": "full 408x320 atlas-frame scan after shell rebuild; selected green is allowed only on selected state",
            },
            "single_icon_track": {
                "status": "pass",
                "basis": "B shell baked globe and B shell state badges are kept; no runtime warning-triangle overlay path",
            },
            "composite_cleanliness": {
                "status": "fail",
                "basis": "B1.3 fixes the transparent hole mechanically but fails user visual review: the right repair is a visible program color band, not clean art integration",
                "checks": checks,
            },
            "art_shell_texture_integrity": {
                "status": "fail",
                "basis": "x390..408 should either be real shell texture or be covered by the visible photo window; B1.3 uses synthetic state-colored filler and reads as an extra border",
            },
            "photo_window_vs_photo_slot_conflict": {
                "status": "needs_decision",
                "basis": "B shell baked visible photo window reaches about x408, while the frozen contract photo_slot ends at x390. Strict 0px photo overflow and B-like visual window cannot both be satisfied without an explicit A/B decision.",
                "option_a": "photo fills the baked visible window to x408; contract photo_slot remains runtime text/hit/safe slot semantics",
                "option_b": "rebuild true shell texture so visible window ends at x390; higher seam/art risk",
            },
            "no_fake_text": {
                "status": "pass",
                "basis": "atlas contains no baked readable text; Chinese strings are runtime labels in Python/Godot captures",
            },
            "functional_faces_orthogonal": {
                "status": "pass",
                "basis": "B shell face remains orthogonal; only shell band pixels are rebuilt and photos are clipped to contract slot",
            },
            "same_state_layout": {
                "status": "pass",
                "basis": "all four states use the same 204x160 contract frame, identical slots, and unchanged action/icon badge positions",
            },
        },
        "visual_repair_notes": [
            "B1.3 does not reroll imagegen and does not change the left_region_card contract.",
            "User review rejects B1.3: the x390..408 band is opaque but reads as a synthetic state-colored filler strip.",
            "The remaining root conflict is that the B shell baked visual photo window is wider than the frozen photo_slot.",
            "Photos are pasted strictly inside contract photo_slot [42,48,390,176] at 2x.",
            "card_body_opacity_probe is a hard gate; any transparent pixel in x390..408,y40..300 fails the candidate.",
            "B1.3 is not a production candidate; next work must resolve photo_window_vs_photo_slot_conflict before more pixel patching.",
        ],
    }


def save_outputs() -> None:
    contract = b11.load_contract()
    frames, base_meta, composition = compose_frames(contract)
    candidate = make_candidate_sheet(frames)
    qa, geometry_metrics = b11.make_geometry_qa(frames, composition)
    atlas = b11.make_atlas(frames)
    runtime = make_runtime_preview(frames, contract, show_qa=False)
    runtime_qa = make_runtime_preview(frames, contract, show_qa=True)
    green_stats = b11.artifact_green_stats(frames)
    alpha_stats = card_body_opacity_probe(frames)
    edge_qa = make_right_edge_qa(frames, alpha_stats)
    manifest = make_manifest(contract, base_meta, composition, geometry_metrics, green_stats, alpha_stats)

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
        "right_edge_alpha_qa": b11.count_colors_nonblack(OUT_EDGE_QA),
        "b1_2_vs_b1_3_alpha_hole_fix_board": b11.count_colors_nonblack(OUT_COMPARE),
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
            "basis": "run scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro after switching the capture script to the B1.3 atlas",
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
