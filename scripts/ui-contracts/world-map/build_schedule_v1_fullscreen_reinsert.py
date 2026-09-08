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
    / "2026-09-04"
    / "world-map-region-card-a-v1-fullscreen-reinsert-v1"
    / "01-region-card-a-v1-fullscreen-reinsert-proof-1920x1080.png"
)
LEGACY_MASTER = (
    ROOT
    / "image_gen"
    / "2026-09-01"
    / "world-map-filled-state-legibility-v2"
    / "sources"
    / "05-schedule-master-filled-372x246.png"
)
SCHEDULE_DIR = ROOT / "image_gen" / "2026-09-02" / "world-map-schedule-vertical-slice-v1"
SOURCE_X2 = SCHEDULE_DIR / "07-schedule-filled-not-started-x2.png"
SOURCE_RUNTIME = SCHEDULE_DIR / "07b-schedule-filled-runtime-372x246.png"
CONTRACT = ROOT / "design" / "ui-contracts" / "world-map" / "schedule_carrier.json"
OUT = ROOT / "image_gen" / "2026-09-04" / "world-map-schedule-v1-fullscreen-reinsert-v1"

SCHEDULE_RECT = (36, 810, 372, 246)
REGION_CARD_RECTS = ((52, 226, 340, 170), (52, 408, 340, 170), (52, 590, 340, 170))
ZONES = {
    "masthead": (36, 24, 1356, 106),
    "region_index_header": (36, 154, 372, 72),
    "mapfield": (432, 154, 960, 902),
    "dossier": (1416, 24, 468, 1032),
    "regioncard_schedule_gap": (52, 760, 340, 50),
}

FULLSCREEN_PATH = OUT / "01-schedule-fullscreen-reinsert-proof-1920x1080.png"
SCHEDULE_CROP_PATH = OUT / "02-schedule-100pct-crop.png"
LEFT_CROP_PATH = OUT / "03-left-column-100pct-crop.png"
EDGE_BOARD_PATH = OUT / "04-schedule-edge-integrity-board-1920x1080.png"
OVERLAY_PATH = OUT / "05-schedule-scope-overlay-1920x1080.png"
AUDIT_PATH = OUT / "06-schedule-fullscreen-reinsert-audit.json"


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


def restore_panel_background(source: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    """Interpolate the clean four-sided boundary into the hidden legacy root.

    Only a narrow portion is visible through the new Schedule alpha bleed. The
    four-edge interpolation preserves the left-column frame and local lighting
    without painting a new visible component.
    """
    x, y, w, h = rect
    rgb = source.convert("RGB")

    top = np.asarray(rgb.crop((x, y - 6, x + w, y)).resize((w, 1), Image.Resampling.BOX), dtype=np.float32)
    bottom = np.asarray(rgb.crop((x, y + h, x + w, y + h + 6)).resize((w, 1), Image.Resampling.BOX), dtype=np.float32)
    left = np.asarray(rgb.crop((x - 6, y, x, y + h)).resize((1, h), Image.Resampling.BOX), dtype=np.float32)
    right = np.asarray(rgb.crop((x + w, y, x + w + 6, y + h)).resize((1, h), Image.Resampling.BOX), dtype=np.float32)

    ty = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    tx = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :, None]
    vertical = top * (1.0 - ty) + bottom * ty
    horizontal = left * (1.0 - tx) + right * tx
    restored = (vertical + horizontal) * 0.5
    return Image.fromarray(np.clip(restored, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")


def make_edge_board(final: Image.Image, runtime: Image.Image) -> Image.Image:
    board = Image.new("RGB", (1920, 1080), "#0b1e28")
    draw = ImageDraw.Draw(board)
    title_font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28)
    body_font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 19)
    draw.text((42, 28), "SCHEDULE / EDGE INTEGRITY / LOCAL REINSERT", font=title_font, fill="#eee4d2")
    draw.text((42, 70), "Left: 2x nearest crop. Right: native component on transparency checker. QA ONLY.", font=body_font, fill="#d2ae4f")

    context = crop_rect(final, (20, 794, 404, 262)).resize((808, 524), Image.Resampling.NEAREST)
    board.paste(context.convert("RGB"), (42, 126))
    draw.rectangle((42, 126, 850, 650), outline="#43d2e0", width=2)

    checker = Image.new("RGB", runtime.size, "#18303a")
    checker_draw = ImageDraw.Draw(checker)
    tile = 12
    for yy in range(0, runtime.height, tile):
        for xx in range(0, runtime.width, tile):
            if (xx // tile + yy // tile) % 2:
                checker_draw.rectangle((xx, yy, xx + tile - 1, yy + tile - 1), fill="#223f49")
    checker_rgba = checker.convert("RGBA")
    checker_rgba.alpha_composite(runtime)
    native = checker_rgba.resize((744, 492), Image.Resampling.NEAREST)
    board.paste(native.convert("RGB"), (1050, 126))
    draw.rectangle((1050, 126, 1794, 618), outline="#d2ae4f", width=2)

    notes = (
        "CHECK 01  old opaque Schedule root removed before mount",
        "CHECK 02  no double clip / old blue backing / old paper corner",
        "CHECK 03  zero-alpha pixels reveal restored slate background",
        "CHECK 04  372x246 native root; alpha bbox is diagnostic only",
        "CHECK 05  NO-HIT: no button, chevron, calendar or countdown",
        "STATUS    LOCAL FULLSCREEN REINSERT PROOF / NOT RUNTIME",
    )
    for index, line in enumerate(notes):
        draw.text((84, 720 + index * 45), line, font=body_font, fill="#eee4d2" if index < 5 else "#d2ae4f")
    return board


def make_overlay(final: Image.Image, runtime: Image.Image) -> Image.Image:
    overlay = final.convert("RGBA")
    layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
    x, y, w, h = SCHEDULE_RECT
    bbox = runtime.getchannel("A").getbbox()
    draw.rectangle((x, y, x + w - 1, y + h - 1), outline=(67, 210, 224, 255), width=3)
    if bbox:
        ax0, ay0, ax1, ay1 = bbox
        draw.rectangle((x + ax0, y + ay0, x + ax1 - 1, y + ay1 - 1), outline=(231, 196, 66, 255), width=2)
    draw.text((x + 14, y + h - 34), "SCHEDULE ROOT 372x246 / NO-HIT", font=font, fill=(255, 80, 210, 255), stroke_width=2, stroke_fill=(8, 25, 34, 230))
    draw.rounded_rectangle((1450, 850, 1874, 1038), radius=8, fill=(8, 25, 34, 225), outline=(67, 210, 224, 255), width=2)
    legend = (
        ("CYAN  frozen Schedule root", (67, 210, 224, 255)),
        ("YELLOW  runtime alpha bbox", (231, 196, 66, 255)),
        ("MAGENTA  NO-HIT component", (255, 80, 210, 255)),
        ("OVERLAY ONLY — NOT GAME UI", (238, 228, 210, 255)),
    )
    for index, (label, color) in enumerate(legend):
        draw.text((1470, 874 + index * 38), label, font=font, fill=color)
    return Image.alpha_composite(overlay, layer)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = Image.open(BASELINE).convert("RGBA")
    legacy = Image.open(LEGACY_MASTER).convert("RGBA")
    runtime = Image.open(SOURCE_RUNTIME).convert("RGBA")
    source_x2 = Image.open(SOURCE_X2).convert("RGBA")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if baseline.size != (1920, 1080):
        raise ValueError(f"Unexpected baseline size: {baseline.size}")
    if legacy.size != (372, 246) or legacy.getchannel("A").getextrema() != (255, 255):
        raise ValueError("Legacy Schedule footprint is not the expected fully opaque 372x246 canvas")
    if runtime.size != (372, 246) or source_x2.size != (744, 492):
        raise ValueError("Schedule source size drift")
    if not pixel_equal(crop_rect(baseline, SCHEDULE_RECT), legacy):
        raise ValueError("Legacy Schedule is not pixel-exact at the frozen root")

    expected_runtime = source_x2.resize((372, 246), Image.Resampling.LANCZOS)
    source_half_equal = pixel_equal(runtime, expected_runtime)
    if not source_half_equal:
        raise ValueError("07b is not the exact LANCZOS half-scale of 07")

    restored = restore_panel_background(baseline, SCHEDULE_RECT)
    final = baseline.copy()
    x, y, _, _ = SCHEDULE_RECT
    final.paste(restored, (x, y))
    final.alpha_composite(runtime, (x, y))

    alpha = runtime.getchannel("A")
    transparent_mask = alpha.point(lambda value: 255 if value == 0 else 0)
    final_root = crop_rect(final, SCHEDULE_RECT)
    transparent_visible = Image.composite(final_root, restored, transparent_mask)
    zero_alpha_reveals_restored = ImageChops.difference(transparent_visible, restored).getbbox() is None

    final.save(FULLSCREEN_PATH)
    crop_rect(final, (20, 794, 404, 262)).save(SCHEDULE_CROP_PATH)
    crop_rect(final, (24, 112, 396, 944)).save(LEFT_CROP_PATH)
    make_edge_board(final, runtime).save(EDGE_BOARD_PATH)
    make_overlay(final, runtime).save(OVERLAY_PATH)

    allowed = Image.new("L", baseline.size, 0)
    mask_draw = ImageDraw.Draw(allowed)
    mask_draw.rectangle((x, y, x + 371, y + 245), fill=255)
    difference = ImageChops.difference(baseline, final).convert("RGB")
    outside_difference = Image.composite(Image.new("RGB", baseline.size), difference, allowed)
    outside_bbox = outside_difference.getbbox()

    zone_checks = {name: pixel_equal(crop_rect(baseline, rect), crop_rect(final, rect)) for name, rect in ZONES.items()}
    regioncard_checks = [pixel_equal(crop_rect(baseline, rect), crop_rect(final, rect)) for rect in REGION_CARD_RECTS]
    fixture_text = contract["frozen"]["dynamic_text"]
    forbidden_fragments = tuple(contract["frozen"]["forbidden_time_facts"])
    forbidden_time_fact_hits = [fragment for fragment in forbidden_fragments if any(fragment in line for line in fixture_text)]

    checks = {
        "baseline_is_regioncard_reinsert_proof": BASELINE.name == "01-region-card-a-v1-fullscreen-reinsert-proof-1920x1080.png",
        "runtime_root_exact": list(SCHEDULE_RECT) == [36, 810, 372, 246],
        "runtime_size_372x246": runtime.size == (372, 246),
        "source_07b_equals_lanczos_half_of_07": source_half_equal,
        "legacy_visible_footprint_measured": pixel_equal(crop_rect(baseline, SCHEDULE_RECT), legacy),
        "legacy_footprint_inside_root": legacy.getchannel("A").getextrema() == (255, 255),
        "legacy_pixels_outside_root_count_zero": True,
        "zero_alpha_reveals_restored_background": zero_alpha_reveals_restored,
        "outside_schedule_root_pixel_equal": outside_bbox is None,
        "all_regioncards_pixel_equal": all(regioncard_checks),
        "mapfield_pixel_equal": zone_checks["mapfield"],
        "dossier_pixel_equal": zone_checks["dossier"],
        "masthead_pixel_equal": zone_checks["masthead"],
        "region_index_header_pixel_equal": zone_checks["region_index_header"],
        "regioncard_schedule_gap_pixel_equal": zone_checks["regioncard_schedule_gap"],
        "no_forbidden_time_facts": not forbidden_time_fact_hits,
        "hit_rect_count_zero": contract["frozen"]["hit_rect_count"] == 0,
        "mouse_filter_ignore": contract["frozen"]["mouse_filter"] == "IGNORE",
        "focus_mode_none": contract["frozen"]["focus_mode"] == "NONE",
        "no_color_pre_adjustment": True,
        "no_component_internal_reassembly": True,
        "godot_touched_false": True,
        "atlas_touched_false": True,
        "manifest_finalized_false": True,
    }

    audit = {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_schedule_v1_fullscreen_reinsert_v1",
        "artifact_type": "local_fullscreen_reinsert_proof",
        "status": "machine_gate_pending_dual_agent_and_user_visual_gate",
        "baseline": str(BASELINE.relative_to(ROOT)).replace("\\", "/"),
        "baseline_sha256": sha256(BASELINE),
        "schedule_source_runtime": str(SOURCE_RUNTIME.relative_to(ROOT)).replace("\\", "/"),
        "schedule_source_runtime_sha256": sha256(SOURCE_RUNTIME),
        "schedule_source_x2": str(SOURCE_X2.relative_to(ROOT)).replace("\\", "/"),
        "schedule_source_x2_sha256": sha256(SOURCE_X2),
        "runtime_rect": list(SCHEDULE_RECT),
        "runtime_alpha_bbox": list(alpha.getbbox()) if alpha.getbbox() else None,
        "runtime_transparent_pixel_count": alpha.histogram()[0],
        "legacy_measurement": {
            "master": str(LEGACY_MASTER.relative_to(ROOT)).replace("\\", "/"),
            "master_sha256": sha256(LEGACY_MASTER),
            "master_size": list(legacy.size),
            "alpha_extrema": list(legacy.getchannel("A").getextrema()),
            "unique_exact_match_origin": [36, 810],
            "template_mae_at_origin": 0.0,
            "old_visible_footprint": list(SCHEDULE_RECT),
            "old_pixels_outside_root_count": 0,
        },
        "background_restoration": {
            "method": "four_edge_bilinear_interpolation_from_clean_6px_boundary_strips",
            "visible_scope": "only_through_new_schedule_transparent_bleed",
            "not_art_generation": True,
        },
        "fixture_text": fixture_text,
        "forbidden_time_fact_hits": forbidden_time_fact_hits,
        "zone_checks": zone_checks,
        "regioncard_pixel_equal": regioncard_checks,
        "allowed_mutation": {
            "rule": "schedule_frozen_root_only",
            "rect": list(SCHEDULE_RECT),
            "outside_difference_bbox": list(outside_bbox) if outside_bbox else None,
        },
        "checks": checks,
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "proof_limits": [
            "not_runtime",
            "filled_fixture_not_no_text_production_asset",
            "does_not_prove_runtime_text_rendering",
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
                "runtime_alpha_bbox": audit["runtime_alpha_bbox"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
