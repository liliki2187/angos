from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
COLLAPSED = OUT_DIR / "639-world-map-wmw-right-dossier-a5-1-live-collapsed.png"
EXPANDED = OUT_DIR / "640-world-map-wmw-right-dossier-a5-1-live-expanded.png"
QA = OUT_DIR / "641-world-map-wmw-right-dossier-a5-1-live-contract-qa.png"
GIF = OUT_DIR / "642-world-map-wmw-right-dossier-a5-1-live-toggle.gif"
MANIFEST = OUT_DIR / "643-world-map-wmw-right-dossier-a5-1-live-integration-manifest.json"


def image_metrics(path: Path) -> dict[str, object]:
    with Image.open(path) as source:
        rgba = source.convert("RGBA")
        alpha_range = rgba.getchannel("A").getextrema()
        if alpha_range != (255, 255):
            raise SystemExit(f"Incomplete frame alpha for {path.name}: {alpha_range}")
        image = rgba.convert("RGB")
        if image.size != (1920, 1080):
            raise SystemExit(f"Unexpected capture size for {path.name}: {image.size}")
        sample = image.resize((240, 135), Image.Resampling.BOX)
        pixels = list(sample.get_flattened_data())
        colors = len(set(pixels))
        non_black = sum(1 for pixel in pixels if max(pixel) > 3)
        non_black_ratio = non_black / (240 * 135)
        if colors < 240 or non_black_ratio < 0.95:
            raise SystemExit(
                f"Capture content check failed for {path.name}: "
                f"colors={colors} non_black_ratio={non_black_ratio:.4f}"
            )
        return {
            "file": path.name,
            "size": list(image.size),
            "sampled_unique_colors": colors,
            "sampled_non_black_ratio": round(non_black_ratio, 6),
            "alpha_range": list(alpha_range),
            "bytes": path.stat().st_size,
        }


def build_gif() -> None:
    source_paths = [COLLAPSED, EXPANDED, EXPANDED, COLLAPSED]
    durations = [900, 1300, 500, 900]
    frames: list[Image.Image] = []
    for path in source_paths:
        with Image.open(path) as source:
            frame = source.convert("RGB").resize((960, 540), Image.Resampling.LANCZOS)
            frames.append(frame.quantize(colors=192, method=Image.Quantize.MEDIANCUT))
    frames[0].save(
        GIF,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )


def localized_diff_metrics() -> dict[str, object]:
    with Image.open(COLLAPSED) as collapsed_source, Image.open(EXPANDED) as expanded_source:
        collapsed = collapsed_source.convert("RGB")
        expanded = expanded_source.convert("RGB")
        diff = ImageChops.difference(collapsed, expanded)
        bbox = diff.getbbox()
        if bbox is None:
            raise SystemExit("Collapsed and expanded runtime states are identical")
        outside_right_dossier = diff.crop((0, 0, 1400, 1080)).getbbox()
        if outside_right_dossier is not None:
            raise SystemExit(
                "Collapsed/expanded state changed pixels outside the right dossier boundary: "
                f"{outside_right_dossier}"
            )
        return {
            "diff_bbox": list(bbox),
            "outside_right_dossier_bbox": None,
            "expected_boundary": [1400, 0, 1920, 1080],
        }


def main() -> None:
    captures = [image_metrics(path) for path in (COLLAPSED, EXPANDED, QA)]
    diff_metrics = localized_diff_metrics()
    build_gif()
    manifest = {
        "schema_version": "1.0",
        "candidate": "right_dossier_page A5.1",
        "visual_version": "v0.9.6",
        "integration": "production WeeklyRunGame world view",
        "source_scene": "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn",
        "capture_script": "res://tests/capture_world_map_right_dossier_a51_live.gd",
        "godot": {
            "version": "4.6.2-stable",
            "mode": "windowed",
            "renderer": "opengl3",
            "frame_post_draw_waits": 2,
            "all_black_rejection": True,
        },
        "captures": captures,
        "animation": {"file": GIF.name, "frames": 4, "size": [960, 540]},
        "state_diff": diff_metrics,
        "production_behavior": {
            "interactive_buttons": ["MissionSummaryButton", "PrimaryEnterButton"],
            "task_row_hit_rects": 0,
            "collapsed_preview_rows": 0,
            "expanded_preview_rows": 2,
            "production_preview_total": 4,
            "locked_region_task_rows": 0,
            "locked_region_summary_disabled": True,
            "locked_region_primary_disabled": True,
            "host_global_rect": [1480, 120, 414, 843],
            "paper_texture_rect": [320, 520],
            "photo_texture_rect": [276, 176],
            "primary_skin_rect": [284, 50],
        },
        "gates": {
            "screen_identity": "fail_wrong_host_global_channel",
            "production_payload_binding": "pass",
            "single_summary_hit_target": "pass",
            "read_only_preview_rows": "pass",
            "in_place_expansion": "pass",
            "localized_state_diff": "pass",
            "non_black_and_color_diversity": "pass",
            "full_frame_alpha_opaque": "pass",
            "four_region_frame_completeness": "pass",
            "legacy_right_vbox_hidden": "pass",
            "legacy_baked_dossier_isolated": "pass",
            "texture_rect_reference_geometry": "pass",
            "visible_focus_ring": "pass",
            "narrow_dossier_view_model": "pass",
        },
        "placeholder_disclosure": {
            "north_america_photo": "composition placeholder only",
            "formal_region_art": False,
        },
        "status": "invalidated_wrong_host_do_not_use_for_wmw_full_screen_acceptance",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(GIF)
    print(MANIFEST)


if __name__ == "__main__":
    main()
