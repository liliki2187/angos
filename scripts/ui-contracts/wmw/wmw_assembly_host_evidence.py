from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
FUNCTION_REFERENCE = ROOT / "docs" / "screenshots" / "2026-06-23-world-map-clean-lowpoly-style-target" / "30-v2-2-3-clean-right-function.png"
VISUAL_REFERENCE = OUT_DIR / "575-world-map-wmw-v0-8-6-right-dossier-full-screen-reinsert.png"
COLLAPSED = OUT_DIR / "645-world-map-wmw-assembly-host-collapsed.png"
EXPANDED = OUT_DIR / "646-world-map-wmw-assembly-host-expanded.png"
LOCKED = OUT_DIR / "647-world-map-wmw-assembly-host-locked.png"
QA = OUT_DIR / "648-world-map-wmw-assembly-host-geometry-qa.png"
BOARD = OUT_DIR / "644-world-map-wmw-assembly-host-dual-reference-board.png"
GIF = OUT_DIR / "649-world-map-wmw-assembly-host-state-cycle.gif"
MANIFEST = OUT_DIR / "650-world-map-wmw-assembly-host-integration-manifest.json"


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/msyhbd.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


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
        if colors < 160 or non_black_ratio < 0.95:
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


def build_dual_reference_board() -> None:
    panel_size = (1280, 720)
    header_height = 72
    labels = [
        "功能参考 30：只看三区职责与信息层级",
        "真实运行态 645：本轮独立整屏宿主",
        "视觉参考 575：只看形状、色彩与材质",
    ]
    paths = [FUNCTION_REFERENCE, COLLAPSED, VISUAL_REFERENCE]
    board = Image.new("RGB", (panel_size[0] * 3, panel_size[1] + header_height), (5, 16, 19))
    draw = ImageDraw.Draw(board)
    font = load_font(24)
    for index, (label, path) in enumerate(zip(labels, paths, strict=True)):
        with Image.open(path) as source:
            frame = source.convert("RGB").resize(panel_size, Image.Resampling.LANCZOS)
        x = index * panel_size[0]
        board.paste(frame, (x, header_height))
        draw.rectangle((x, 0, x + panel_size[0], header_height), fill=(10, 37, 41))
        draw.text((x + 28, 20), label, font=font, fill=(235, 225, 191))
        if index > 0:
            draw.line((x, 0, x, board.height), fill=(214, 195, 107), width=2)
    board.save(BOARD)


def build_gif() -> None:
    source_paths = [COLLAPSED, EXPANDED, EXPANDED, LOCKED, LOCKED, COLLAPSED]
    durations = [900, 900, 500, 1100, 500, 900]
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


def localized_disclosure_diff() -> dict[str, object]:
    with Image.open(COLLAPSED) as collapsed_source, Image.open(EXPANDED) as expanded_source:
        collapsed = collapsed_source.convert("RGB")
        expanded = expanded_source.convert("RGB")
        diff = ImageChops.difference(collapsed, expanded)
        bbox = diff.getbbox()
        if bbox is None:
            raise SystemExit("Collapsed and expanded runtime states are identical")
        right_dossier_boundary_x = 1398
        outside = diff.crop((0, 0, right_dossier_boundary_x, 1080)).getbbox()
        if outside is not None:
            raise SystemExit(
                "Collapsed/expanded disclosure changed pixels outside A5.1: "
                f"{outside}"
            )
        return {
            "diff_bbox": list(bbox),
            "outside_right_dossier_bbox": None,
            "expected_boundary": [right_dossier_boundary_x, 0, 1920, 1080],
        }


def main() -> None:
    captures = [image_metrics(path) for path in (COLLAPSED, EXPANDED, LOCKED, QA)]
    disclosure_diff = localized_disclosure_diff()
    build_dual_reference_board()
    build_gif()
    manifest = {
        "schema_version": "1.0",
        "candidate": "WMW independent full-screen assembly host",
        "decision": "A223",
        "source_scene": "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn",
        "assembly_scene": "res://scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssembly.tscn",
        "capture_script": "res://tests/capture_world_map_wmw_assembly_host.gd",
        "dual_reference": {
            "functional_only": str(FUNCTION_REFERENCE.relative_to(ROOT)).replace("\\", "/"),
            "visual_only": str(VISUAL_REFERENCE.relative_to(ROOT)).replace("\\", "/"),
            "comparison_board": BOARD.name,
        },
        "godot": {
            "version": "4.6.2-stable",
            "mode": "windowed",
            "renderer": "opengl3",
            "audio_driver": "Dummy",
            "frame_post_draw_waits": 2,
            "all_black_rejection": True,
        },
        "captures": captures,
        "animation": {"file": GIF.name, "frames": 6, "size": [960, 540]},
        "localized_disclosure_diff": disclosure_diff,
        "geometry_contract_1280x720": {
            "left": [24, 16, 228, 688],
            "center": [268, 16, 648, 688],
            "right": [932, 16, 320, 688],
            "minimum_gap": 16,
            "center_safe_right_edge": 916,
            "a51": [932, 30, 320, 520],
        },
        "runtime_behavior": {
            "sole_state_source": "selected_region_id",
            "synchronized_endpoints": ["left_card", "map_pin", "right_dossier", "primary_cta"],
            "mission_disclosure": "in_place / max_2_read_only_rows",
            "interactive_buttons_in_a51": ["MissionSummaryButton", "PrimaryEnterButton"],
            "locked_preview_rows": 0,
            "locked_disclosure_disabled": True,
            "locked_primary_cta_disabled": True,
            "enter_region_task_board_day_cost": 0,
            "map_layers": ["MapBaseLayer", "RouteLayer", "SelectedRegionLayer", "PinLayer", "LabelLayer"],
        },
        "formal_reused_components": {
            "left_region_card": "B2.12 frozen geometry",
            "right_dossier": "A5.1 frozen geometry",
        },
        "provisional_items": {
            "map_panel": "structure_only; runtime-drawn placeholder; not a production art asset",
            "left_region_card_photos": "fixed per region to prevent state drift; composition examples, not formal region identity assets",
            "north_america_dossier_photo": "composition placeholder retained from A5.1",
            "other_region_dossier_photos": "not provided; dark fallback only",
            "locked_region_copy": "production payload copy, pending final content polish",
        },
        "gates": {
            "screen_identity": "pass_independent_wmw_host",
            "legacy_global_channel_hidden": "pass",
            "old_a51_mount_removed": "pass",
            "macro_responsibility_geometry": "pass",
            "center_x916_safe_boundary": "pass",
            "b212_geometry": "pass",
            "a51_geometry": "pass",
            "a51_frozen_position_932_30": "pass",
            "selected_region_atomic_sync": "pass",
            "locked_state_no_task_leak": "pass",
            "zero_day_entry": "pass",
            "dynamic_evidence": "pass",
            "non_black_and_color_diversity": "pass",
            "production_map_visual": "pending_structure_only",
        },
        "status": "runtime_structure_integration_pass_map_visual_pending",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(BOARD)
    print(GIF)
    print(MANIFEST)


if __name__ == "__main__":
    main()
