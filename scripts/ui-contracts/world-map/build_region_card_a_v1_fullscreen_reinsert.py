from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
BASELINE = (
    ROOT
    / "image_gen"
    / "2026-09-03"
    / "world-map-mapfield-dynamic-overlay-fixture-v1"
    / "12-fullscreen-north-mapfield-only-corrected-1920x1080.png"
)
UPSTREAM = (
    ROOT
    / "image_gen"
    / "2026-09-01"
    / "world-map-filled-state-legibility-v2"
    / "01-filled-state-visual-target-1920x1080.png"
)
LEGACY_MASTER = (
    ROOT
    / "image_gen"
    / "2026-09-01"
    / "world-map-filled-state-legibility-v2"
    / "sources"
    / "04-region-card-master-340x170.png"
)
CARD_DIR = ROOT / "image_gen" / "2026-09-04" / "world-map-region-card-a-v1-contract-fit"
OUT = ROOT / "image_gen" / "2026-09-04" / "world-map-region-card-a-v1-fullscreen-reinsert-v1"

CARD_INPUTS = (
    ("north_selected_warning", CARD_DIR / "07-north-selected-warning-bound-x2.png", (52, 226, 340, 170)),
    ("east_unselected_locked", CARD_DIR / "08-east-unselected-locked-bound-x2.png", (52, 408, 340, 170)),
    ("pacific_unselected_locked", CARD_DIR / "10-pacific-unselected-locked-bound-x2.png", (52, 590, 340, 170)),
)

ZONES = {
    "masthead": (36, 24, 1356, 106),
    "region_index_header": (36, 154, 372, 72),
    "mapfield": (432, 154, 960, 902),
    "schedule": (36, 810, 372, 246),
    "dossier": (1416, 24, 468, 1032),
    "gap_north_east": (52, 396, 340, 12),
    "gap_east_pacific": (52, 578, 340, 12),
    "gap_pacific_schedule": (52, 760, 340, 50),
}

FULLSCREEN_PATH = OUT / "01-region-card-a-v1-fullscreen-reinsert-proof-1920x1080.png"
LEFT_CROP_PATH = OUT / "02-left-column-100pct-crop.png"
STACK_CROP_PATH = OUT / "03-three-card-stack-100pct-crop.png"
EDGE_BOARD_PATH = OUT / "04-three-card-edge-integrity-board-1920x1080.png"
OVERLAY_PATH = OUT / "05-scope-and-registration-overlay-1920x1080.png"
AUDIT_PATH = OUT / "06-region-card-fullscreen-reinsert-audit.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rect_box(rect: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    return x, y, x + w, y + h


def crop_rect(image: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    return image.crop(rect_box(rect))


def pixel_equal(a: Image.Image, b: Image.Image) -> bool:
    return ImageChops.difference(a.convert("RGBA"), b.convert("RGBA")).getbbox() is None


def locate_legacy_master(baseline: Image.Image) -> dict:
    """Measure the old card's page origin; never use the new alpha bbox as layout."""
    old = np.asarray(Image.open(LEGACY_MASTER).convert("RGB"), dtype=np.int16)
    base = np.asarray(baseline.convert("RGB"), dtype=np.int16)
    scores: list[tuple[float, int, int]] = []
    for y in range(214, 239):
        for x in range(40, 65):
            candidate = base[y : y + 170, x : x + 340]
            scores.append((float(np.abs(candidate - old).mean()), x, y))
    scores.sort()
    best = scores[0]
    return {
        "search_window": [40, 214, 364, 194],
        "best_origin": [best[1], best[2]],
        "mean_absolute_rgb_error": round(best[0], 4),
        "next_best_origin": [scores[1][1], scores[1][2]],
        "next_best_error": round(scores[1][0], 4),
        "legacy_master_mode": Image.open(LEGACY_MASTER).mode,
        "legacy_master_alpha_extrema": list(Image.open(LEGACY_MASTER).getchannel("A").getextrema()),
        "measured_visible_footprint": [best[1], best[2], 340, 170],
        "measurement_note": "The fully opaque legacy 340x170 canvas is uniquely best-aligned at the frozen root. Its compositing footprint cannot extend outside that canvas.",
    }


def restore_panel_under_card(source: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    """Restore only the old opaque root using clean pixels immediately beside it.

    The replacement is visible only through the new asset's narrow transparent
    bleed. Row-wise interpolation preserves the panel's vertical lighting and
    avoids a flat painted rectangle.
    """
    x, y, w, h = rect
    rgb = source.convert("RGB")
    left = rgb.crop((x - 6, y, x, y + h)).resize((1, h), Image.Resampling.BOX)
    right = rgb.crop((x + w, y, x + w + 6, y + h)).resize((1, h), Image.Resampling.BOX)
    left_arr = np.asarray(left, dtype=np.float32)
    right_arr = np.asarray(right, dtype=np.float32)
    t = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :, None]
    restored = left_arr * (1.0 - t) + right_arr * t
    restored = np.repeat(restored, h, axis=0) if restored.shape[0] == 1 else restored
    return Image.fromarray(np.clip(restored, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")


def alpha_bbox_runtime(card_x2: Image.Image) -> list[int] | None:
    runtime = card_x2.resize((340, 170), Image.Resampling.LANCZOS)
    bbox = runtime.getchannel("A").getbbox()
    return list(bbox) if bbox else None


def make_edge_board(final: Image.Image) -> Image.Image:
    board = Image.new("RGB", (1920, 1080), "#0b1e28")
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24)
    small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
    draw.text((40, 28), "REGIONCARD A / EDGE INTEGRITY / 2X NEAREST", font=font, fill="#eee4d2")
    draw.text((40, 66), "100% source crop shown at 2x only for edge inspection — NOT GAME UI", font=small, fill="#d2ae4f")

    windows = (
        ("NORTH", (40, 214, 364, 194), (40, 120)),
        ("EAST", (40, 396, 364, 194), (800, 120)),
        ("PACIFIC", (40, 578, 364, 194), (40, 570)),
    )
    for label, rect, pos in windows:
        crop = crop_rect(final, rect).resize((728, 388), Image.Resampling.NEAREST)
        board.paste(crop.convert("RGB"), pos)
        draw.rectangle((pos[0], pos[1], pos[0] + 728, pos[1] + 388), outline="#43d2e0", width=2)
        draw.text((pos[0], pos[1] - 28), label, font=small, fill="#43d2e0")

    draw.rounded_rectangle((800, 570, 1880, 958), radius=10, fill="#102c38", outline="#355866", width=2)
    notes = (
        "CHECK 01  no old blue/olive frame in transparent bleed",
        "CHECK 02  three roots remain 340x170",
        "CHECK 03  gaps remain 12px / 12px / 50px",
        "CHECK 04  no pre-color adjustment",
        "CHECK 05  page outside three roots is pixel-identical",
        "STATUS    LOCAL FULLSCREEN REINSERT PROOF / NOT RUNTIME",
    )
    for index, line in enumerate(notes):
        draw.text((836, 616 + index * 50), line, font=small, fill="#eee4d2" if index < 5 else "#d2ae4f")
    return board


def make_overlay(final: Image.Image, runtime_cards: dict[str, Image.Image]) -> Image.Image:
    overlay = final.convert("RGBA")
    layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
    for name, _, rect in CARD_INPUTS:
        x, y, w, h = rect
        bbox = runtime_cards[name].getchannel("A").getbbox()
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline=(67, 210, 224, 255), width=3)
        if bbox:
            ax0, ay0, ax1, ay1 = bbox
            draw.rectangle((x + ax0, y + ay0, x + ax1 - 1, y + ay1 - 1), outline=(231, 196, 66, 255), width=2)
        draw.text((x + 8, y + 142), name.upper(), font=font, fill=(255, 80, 210, 255), stroke_width=2, stroke_fill=(9, 26, 34, 230))
    draw.rounded_rectangle((1450, 842, 1874, 1038), radius=8, fill=(8, 25, 34, 225), outline=(67, 210, 224, 255), width=2)
    legend = (
        ("CYAN  frozen component root", (67, 210, 224, 255)),
        ("YELLOW  runtime alpha bbox", (231, 196, 66, 255)),
        ("MAGENTA  measured old footprint = root", (255, 80, 210, 255)),
        ("OVERLAY ONLY — NOT GAME UI", (238, 228, 210, 255)),
    )
    for index, (label, color) in enumerate(legend):
        draw.text((1470, 868 + index * 40), label, font=font, fill=color)
    return Image.alpha_composite(overlay, layer)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = Image.open(BASELINE).convert("RGBA")
    upstream = Image.open(UPSTREAM).convert("RGBA")
    if baseline.size != (1920, 1080):
        raise ValueError(f"Unexpected baseline size: {baseline.size}")

    legacy_measurement = locate_legacy_master(baseline)
    if legacy_measurement["best_origin"] != [52, 226]:
        raise ValueError(f"Legacy origin drifted: {legacy_measurement['best_origin']}")
    if legacy_measurement["legacy_master_alpha_extrema"] != [255, 255]:
        raise ValueError("Legacy RegionCard master is not fully opaque; footprint inference is unsafe")

    final = baseline.copy()
    runtime_cards: dict[str, Image.Image] = {}
    card_meta: dict[str, dict] = {}
    for name, source_path, rect in CARD_INPUTS:
        source_x2 = Image.open(source_path).convert("RGBA")
        if source_x2.size != (680, 340):
            raise ValueError(f"Unexpected card size for {name}: {source_x2.size}")
        runtime = source_x2.resize((340, 170), Image.Resampling.LANCZOS)
        runtime_cards[name] = runtime
        restored = restore_panel_under_card(baseline, rect)
        x, y, _, _ = rect
        final.paste(restored, (x, y))
        final.alpha_composite(runtime, (x, y))

        alpha = runtime.getchannel("A")
        transparent_mask = alpha.point(lambda value: 255 if value == 0 else 0)
        final_root = crop_rect(final, rect)
        restored_visible = Image.composite(final_root, restored, transparent_mask)
        transparent_residual = ImageChops.difference(restored_visible, restored).getbbox()
        card_meta[name] = {
            "source": str(source_path.relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": sha256(source_path),
            "source_size": list(source_x2.size),
            "runtime_rect": list(rect),
            "runtime_size": list(runtime.size),
            "runtime_alpha_bbox": list(alpha.getbbox()) if alpha.getbbox() else None,
            "transparent_pixel_count": alpha.histogram()[0],
            "transparent_zero_alpha_reveals_restored_background": transparent_residual is None,
        }

    final.save(FULLSCREEN_PATH)
    crop_rect(final, (24, 112, 396, 944)).save(LEFT_CROP_PATH)
    crop_rect(final, (44, 216, 356, 554)).save(STACK_CROP_PATH)
    make_edge_board(final).save(EDGE_BOARD_PATH)
    make_overlay(final, runtime_cards).save(OVERLAY_PATH)

    allowed = Image.new("L", baseline.size, 0)
    mask_draw = ImageDraw.Draw(allowed)
    for _, _, rect in CARD_INPUTS:
        x, y, w, h = rect
        mask_draw.rectangle((x, y, x + w - 1, y + h - 1), fill=255)
    difference = ImageChops.difference(baseline, final).convert("RGB")
    outside_difference = Image.composite(Image.new("RGB", baseline.size), difference, allowed)
    outside_bbox = outside_difference.getbbox()

    zone_checks = {name: pixel_equal(crop_rect(baseline, rect), crop_rect(final, rect)) for name, rect in ZONES.items()}
    baseline_scope_checks = {
        "left_column_equal_to_upstream": pixel_equal(crop_rect(baseline, (36, 154, 372, 902)), crop_rect(upstream, (36, 154, 372, 902))),
        "dossier_equal_to_upstream": pixel_equal(crop_rect(baseline, ZONES["dossier"]), crop_rect(upstream, ZONES["dossier"])),
        "masthead_equal_to_upstream": pixel_equal(crop_rect(baseline, ZONES["masthead"]), crop_rect(upstream, ZONES["masthead"])),
    }

    checks = {
        "baseline_is_corrected_12": BASELINE.name == "12-fullscreen-north-mapfield-only-corrected-1920x1080.png",
        "legacy_visible_footprint_measured": legacy_measurement["best_origin"] == [52, 226],
        "legacy_footprint_confined_to_opaque_runtime_root": legacy_measurement["legacy_master_alpha_extrema"] == [255, 255],
        "three_runtime_rects_exact": [list(item[2]) for item in CARD_INPUTS] == [[52, 226, 340, 170], [52, 408, 340, 170], [52, 590, 340, 170]],
        "all_card_sources_680x340": all(meta["source_size"] == [680, 340] for meta in card_meta.values()),
        "all_runtime_cards_340x170": all(meta["runtime_size"] == [340, 170] for meta in card_meta.values()),
        "all_zero_alpha_pixels_reveal_restored_background": all(meta["transparent_zero_alpha_reveals_restored_background"] for meta in card_meta.values()),
        "outside_three_roots_pixel_equal": outside_bbox is None,
        "masthead_pixel_equal": zone_checks["masthead"],
        "region_index_header_pixel_equal": zone_checks["region_index_header"],
        "mapfield_pixel_equal": zone_checks["mapfield"],
        "schedule_pixel_equal": zone_checks["schedule"],
        "dossier_pixel_equal": zone_checks["dossier"],
        "north_east_gap_pixel_equal": zone_checks["gap_north_east"],
        "east_pacific_gap_pixel_equal": zone_checks["gap_east_pacific"],
        "pacific_schedule_gap_pixel_equal": zone_checks["gap_pacific_schedule"],
        "no_color_pre_adjustment": True,
        "no_component_internal_reassembly": True,
        "godot_touched_false": True,
        "atlas_touched_false": True,
        "manifest_finalized_false": True,
    }
    audit = {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_region_card_a_v1_fullscreen_reinsert_v1",
        "artifact_type": "local_fullscreen_reinsert_proof",
        "status": "machine_gate_pending_dual_agent_and_user_visual_gate",
        "baseline": str(BASELINE.relative_to(ROOT)).replace("\\", "/"),
        "baseline_sha256": sha256(BASELINE),
        "baseline_scope_inheritance": baseline_scope_checks,
        "allowed_mutation": {
            "rule": "union_of_three_frozen_region_card_roots",
            "rects": [list(item[2]) for item in CARD_INPUTS],
            "outside_difference_bbox": list(outside_bbox) if outside_bbox else None,
        },
        "legacy_measurement": legacy_measurement,
        "background_restoration": {
            "role": "remove_fully_opaque_legacy_card_canvas_before_mounting_new_whole_component",
            "method": "rowwise_rgb_interpolation_from_clean_6px_strips_immediately_left_and_right_of_each_root",
            "visible_scope": "only_through_new_component_transparent_bleed",
            "not_art_generation": True,
        },
        "cards": card_meta,
        "zone_checks": zone_checks,
        "checks": checks,
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "proof_limits": [
            "not_runtime",
            "does_not_prove_hit_hover_focus_pressed",
            "does_not_prove_atomic_cross_component_state_switching",
            "not_fullscreen_visual_target",
            "does_not_authorize_Godot_atlas_manifest_or_WeeklyRunGame",
        ],
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "output": str(OUT),
                "machine_pass": audit["machine_pass"],
                "failed_checks": [name for name, passed in checks.items() if not passed],
                "outside_difference_bbox": audit["allowed_mutation"]["outside_difference_bbox"],
                "legacy_best_origin": legacy_measurement["best_origin"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
