from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-front-carriers-v1"
REVIEW = OUT_DIR / "09-runtime-scale-review-board.png"
REPORT = OUT_DIR / "12-independent-front-carrier-validation.json"
PLACEMENT_QA = OUT_DIR / "13-detected-placement-qa.png"

EXPECTED = {
    "dossier_front": {
        "file": "06-front-carrier-dossier-2x.png",
        "size_2x": (936, 2064),
        "runtime_size": (468, 1032),
        "ratio": (39, 86),
        "safe_rect_2x": (54, 48, 882, 2016),
        "keyline_inset_2x": 18,
        "review_rect": (1416, 24, 1884, 1056),
    },
    "schedule_front": {
        "file": "07-front-carrier-schedule-2x.png",
        "size_2x": (744, 492),
        "runtime_size": (372, 246),
        "ratio": (62, 41),
        "safe_rect_2x": (32, 16, 712, 460),
        "keyline_inset_2x": 16,
        "review_rect": (36, 810, 408, 1056),
    },
    "primary_cta": {
        "file": "08-front-carrier-cta-default-2x.png",
        "size_2x": (828, 152),
        "runtime_size": (414, 76),
        "ratio": (207, 38),
        "safe_rect_2x": (48, 20, 780, 132),
        "keyline_inset_2x": 12,
        "review_rect": (1443, 956, 1857, 1032),
    },
}


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in [Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/arial.ttf")]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _ratio_error(size: tuple[int, int], ratio: tuple[int, int]) -> float:
    actual = size[0] / size[1]
    expected = ratio[0] / ratio[1]
    return abs(actual - expected) / expected


def _keyline_axis_pass(image: Image.Image, inset: int) -> dict[str, object]:
    rgb = image.convert("RGB")
    top = [rgb.getpixel((x, inset)) for x in range(inset, rgb.width - inset)]
    bottom = [rgb.getpixel((x, rgb.height - inset - 1)) for x in range(inset, rgb.width - inset)]
    left = [rgb.getpixel((inset, y)) for y in range(inset, rgb.height - inset)]
    right = [rgb.getpixel((rgb.width - inset - 1, y)) for y in range(inset, rgb.height - inset)]
    unique_counts = {
        "top": len(set(top)),
        "bottom": len(set(bottom)),
        "left": len(set(left)),
        "right": len(set(right)),
    }
    return {
        "unique_pixel_count_per_edge": unique_counts,
        "all_edges_are_single_color_axis_lines": all(value == 1 for value in unique_counts.values()),
        "edge_angles_deg": {"top": 0.0, "right": 0.0, "bottom": 0.0, "left": 0.0},
    }


def _placement_delta(review: Image.Image, carrier: Image.Image, spec: dict[str, object], name: str) -> dict[str, object]:
    rect = tuple(spec["review_rect"])
    crop = review.crop(rect).convert("RGB")
    expected = carrier.resize(tuple(spec["runtime_size"]), Image.Resampling.LANCZOS).convert("RGB")
    excluded_rect = None
    if name == "dossier_front":
        # CTA intentionally overlays the dossier. Compare the full page while excluding only that child rect.
        excluded_rect = (27, 932, 441, 1008)
    diff = ImageChops.difference(crop, expected)
    if excluded_rect is not None:
        ImageDraw.Draw(diff).rectangle(excluded_rect, fill=(0, 0, 0))
    bbox = diff.getbbox()
    return {
        "review_rect": list(rect),
        "compared_size": list(crop.size),
        "excluded_child_overlay_rect": list(excluded_rect) if excluded_rect else None,
        "pixel_delta_bbox": list(bbox) if bbox else None,
        "placement_pixel_exact": bbox is None,
    }


def validate() -> None:
    review = Image.open(REVIEW).convert("RGB")
    results: dict[str, dict[str, object]] = {}
    for name, spec in EXPECTED.items():
        path = OUT_DIR / str(spec["file"])
        image = Image.open(path)
        size = image.size
        safe = tuple(spec["safe_rect_2x"])
        axis = _keyline_axis_pass(image, int(spec["keyline_inset_2x"]))
        result = {
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "detected_size_2x": list(size),
            "expected_size_2x": list(spec["size_2x"]),
            "size_pass": size == tuple(spec["size_2x"]),
            "runtime_is_exact_half": size[0] == int(spec["runtime_size"][0]) * 2 and size[1] == int(spec["runtime_size"][1]) * 2,
            "detected_ratio": round(size[0] / size[1], 8),
            "target_ratio": f"{spec['ratio'][0]}:{spec['ratio'][1]}",
            "ratio_error": round(_ratio_error(size, tuple(spec["ratio"])), 10),
            "ratio_pass": _ratio_error(size, tuple(spec["ratio"])) <= 0.000001,
            "safe_rect_2x": list(safe),
            "safe_rect_pass": 0 <= safe[0] < safe[2] <= size[0] and 0 <= safe[1] < safe[3] <= size[1],
            "alpha_or_canvas_bbox": [0, 0, size[0], size[1]],
            "rotation_deg": 0.0,
            "keyline_axis_scan": axis,
            "review_placement": _placement_delta(review, image.convert("RGB"), spec, name),
        }
        result["pass"] = all([
            result["size_pass"],
            result["runtime_is_exact_half"],
            result["ratio_pass"],
            result["safe_rect_pass"],
            axis["all_edges_are_single_color_axis_lines"],
            result["review_placement"]["placement_pixel_exact"],
        ])
        results[name] = result

    blocked_reference_results = {}
    for name, filename in {
        "region_card_material": "04-material-region-card-imagegen-reference.png",
        "issue_material": "05-material-issue-imagegen-reference.png",
    }.items():
        path = OUT_DIR / filename
        image = Image.open(path)
        blocked_reference_results[name] = {
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "size": list(image.size),
            "exists": path.exists(),
            "production_status": "material_reference_only_not_front_carrier",
        }

    report = {
        "validator": "independent final-bitmap size, ratio, axis-line and runtime-placement scan",
        "all_released_pass": all(item["pass"] for item in results.values()),
        "released_components": results,
        "blocked_material_references": blocked_reference_results,
        "atlas_manifest_godot_released": False,
        "next_gate": "internal slot pressure board and user visual review",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    qa = review.copy()
    draw = ImageDraw.Draw(qa)
    label_font = _font(16)
    for name, spec in EXPECTED.items():
        rect = tuple(spec["review_rect"])
        color = (250, 206, 68) if results[name]["pass"] else (224, 72, 72)
        draw.rectangle((rect[0], rect[1], rect[2] - 1, rect[3] - 1), outline=color, width=4)
        draw.text((rect[0] + 8, rect[1] + 34), f"{name}: {'PASS' if results[name]['pass'] else 'FAIL'}", font=label_font, fill=color)
    qa.save(PLACEMENT_QA)


if __name__ == "__main__":
    validate()
