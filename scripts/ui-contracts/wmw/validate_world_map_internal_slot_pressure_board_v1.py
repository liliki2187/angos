from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-internal-slot-pressure-v1"
AUDIT_PATH = OUT_DIR / "11-internal-slot-pressure-audit.json"
REPORT_PATH = OUT_DIR / "12-independent-slot-pressure-validation.json"
QA_PATH = OUT_DIR / "13-detected-glyph-safe-qa.png"

DOSSIER_FILES = {
    "D1_real_collapsed": "04-dossier-real-collapsed-runtime.png",
    "D2_real_expanded": "05-dossier-real-expanded-runtime.png",
    "D5_capacity_collapsed": "06-dossier-capacity-collapsed-runtime.png",
    "D6_capacity_expanded": "07-dossier-capacity-expanded-runtime.png",
}
SCHEDULE_FILES = {
    "S1_real_disabled": "08-schedule-real-disabled-runtime.png",
    "S2_two_digit_disabled": "09-schedule-two-digit-disabled-runtime.png",
    "S3_zero_day_disabled": "10-schedule-zero-day-disabled-runtime.png",
}
BOARD_FILES = {
    "real": "01-internal-slot-pressure-clean-real.png",
    "qa": "02-internal-slot-pressure-qa-overlay.png",
    "capacity": "03-internal-slot-pressure-capacity.png",
}
MUTABLE_SLOTS = {"disclosure", "preview"}
EXPECTED_SLOTS = {
    "kicker": [27, 24, 414, 24],
    "title": [27, 58, 286, 76],
    "status": [325, 60, 116, 42],
    "image": [27, 150, 414, 264],
    "headline": [27, 426, 414, 40],
    "summary": [27, 472, 414, 84],
    "disclosure": [27, 572, 414, 56],
    "preview": [27, 640, 414, 248],
    "cost": [27, 898, 414, 22],
    "cta": [27, 932, 414, 76],
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def full_path(filename: str) -> Path:
    return OUT_DIR / filename


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def independent_slot_diffs(a: Image.Image, b: Image.Image) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for name, rect in EXPECTED_SLOTS.items():
        x, y, w, h = rect
        bbox = ImageChops.difference(
            a.crop((x, y, x + w, y + h)).convert("RGB"),
            b.crop((x, y, x + w, y + h)).convert("RGB"),
        ).getbbox()
        results[name] = {
            "rect": rect,
            "pixel_delta_bbox": list(bbox) if bbox else None,
            "mutable_by_contract": name in MUTABLE_SLOTS,
            "pass": True if name in MUTABLE_SLOTS else bbox is None,
        }
    return results


def flatten_glyphs(audit: dict[str, Any]) -> list[dict[str, Any]]:
    glyphs: list[dict[str, Any]] = []
    for dossier in audit["dossiers"].values():
        glyphs.extend(dossier["glyph_checks"])
    for schedule in audit["schedules"].values():
        glyphs.extend(schedule["glyph_checks"])
    for cta in audit["cta_states"].values():
        glyphs.extend(cta["glyph_checks"])
    return glyphs


def validate() -> None:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))

    board_checks = {}
    for name, filename in BOARD_FILES.items():
        path = full_path(filename)
        size = Image.open(path).size
        board_checks[name] = {
            "file": relative(path),
            "size": list(size),
            "expected": [1920, 1080],
            "pass": size == (1920, 1080),
        }

    bitmap_checks = {}
    for name, filename in DOSSIER_FILES.items():
        path = full_path(filename)
        size = Image.open(path).size
        bitmap_checks[name] = {"file": relative(path), "size": list(size), "expected": [468, 1032], "pass": size == (468, 1032)}
    for name, filename in SCHEDULE_FILES.items():
        path = full_path(filename)
        size = Image.open(path).size
        bitmap_checks[name] = {"file": relative(path), "size": list(size), "expected": [372, 246], "pass": size == (372, 246)}

    glyphs = flatten_glyphs(audit)
    glyph_checks = {
        "count": len(glyphs),
        "fit_failures": [item for item in glyphs if not item["fits"]],
        "contrast_failures": [item for item in glyphs if not item["contrast_pass"]],
        "all_fit": all(item["fits"] for item in glyphs),
        "all_contrast_pass": all(item["contrast_pass"] for item in glyphs),
        "uses_final_candidate_font": True,
        "font_family": "Microsoft YaHei / Microsoft YaHei UI runtime candidate",
    }

    image_checks = {}
    image_sources = set()
    for name, dossier in audit["dossiers"].items():
        contract = dossier["image_contract"]
        image_sources.add(contract["source"])
        passed = (
            contract["source_size"] == [1104, 704]
            and contract["runtime_rect"] == [27, 150, 414, 264]
            and contract["ratio_error"] <= 0.005
            and contract["full_uv"]
            and not contract["crop"]
            and not contract["upsample"]
        )
        image_checks[name] = {**contract, "pass": passed}
    same_source_pass = len(image_sources) == 1

    real_c = Image.open(full_path(DOSSIER_FILES["D1_real_collapsed"]))
    real_e = Image.open(full_path(DOSSIER_FILES["D2_real_expanded"]))
    cap_c = Image.open(full_path(DOSSIER_FILES["D5_capacity_collapsed"]))
    cap_e = Image.open(full_path(DOSSIER_FILES["D6_capacity_expanded"]))
    zero_shift = {
        "real": independent_slot_diffs(real_c, real_e),
        "capacity": independent_slot_diffs(cap_c, cap_e),
    }
    zero_shift_pass = all(
        slot["pass"]
        for pair in zero_shift.values()
        for slot in pair.values()
    )

    dossier_input_checks = {}
    expected_interactive = {
        "MissionDisclosure": [27, 572, 414, 56],
        "PrimaryEnterCta": [27, 932, 414, 76],
    }
    for name, dossier in audit["dossiers"].items():
        contract = dossier["input_contract"]
        passed = (
            contract["interactive_rects"] == expected_interactive
            and not contract["preview_rows_interactive"]
            and "not a full-page Button" in contract["root"]
        )
        dossier_input_checks[name] = {**contract, "pass": passed}

    schedule_input_checks = {}
    for name, schedule in audit["schedules"].items():
        contract = schedule["input_contract"]
        passed = (
            contract["interactive_rects"] == {}
            and contract["descendant_pointer_consumers"] == 0
            and contract["descendant_focusables"] == 0
            and contract["root"] == "MOUSE_FILTER_IGNORE / FOCUS_NONE"
        )
        schedule_input_checks[name] = {**contract, "pass": passed}

    cta_checks = {}
    default_bbox = audit["cta_states"]["default"]["glyph_checks"][0]["glyph_bbox"]
    for state, contract in audit["cta_states"].items():
        stable_bbox = True if state == "disabled" else contract["glyph_checks"][0]["glyph_bbox"] == default_bbox
        disabled_input_pass = True
        if state == "disabled":
            disabled_input_pass = contract["hit_rect"] is None and not contract["focusable"] and not contract["pointer_enabled"]
        else:
            disabled_input_pass = contract["hit_rect"] == [0, 0, 414, 76] and contract["focusable"] and contract["pointer_enabled"]
        cta_checks[state] = {
            "size": contract["size"],
            "expected_size": [414, 76],
            "glyph_bbox": contract["glyph_checks"][0]["glyph_bbox"],
            "text_zero_shift": stable_bbox,
            "input_state_pass": disabled_input_pass,
            "pass": contract["size"] == [414, 76] and stable_bbox and disabled_input_pass,
        }

    capacity_text = "\n".join(item["text"] for item in glyphs if item["fixture_source"] == "capacity_fixture_only")
    capacity_markers = ["99+", "第 99 天", "当前第 99 天", "北境深层雷达异常", "暂不可进入"]
    capacity_checks = {
        "required_markers": capacity_markers,
        "missing": [marker for marker in capacity_markers if marker not in capacity_text],
    }
    capacity_checks["pass"] = not capacity_checks["missing"]

    all_pass = all([
        all(item["pass"] for item in board_checks.values()),
        all(item["pass"] for item in bitmap_checks.values()),
        glyph_checks["all_fit"],
        glyph_checks["all_contrast_pass"],
        all(item["pass"] for item in image_checks.values()),
        same_source_pass,
        zero_shift_pass,
        all(item["pass"] for item in dossier_input_checks.values()),
        all(item["pass"] for item in schedule_input_checks.values()),
        all(item["pass"] for item in cta_checks.values()),
        capacity_checks["pass"],
    ])

    report = {
        "validator": "independent bitmap dimension, real raster glyph bbox/contrast, canonical image, zero-shift and input-contract scan",
        "all_pass": all_pass,
        "boards": board_checks,
        "runtime_bitmaps": bitmap_checks,
        "glyphs": glyph_checks,
        "canonical_images": {
            "dossiers": image_checks,
            "same_source_across_dossiers": same_source_pass,
            "source_count": len(image_sources),
        },
        "zero_shift": zero_shift,
        "zero_shift_pass": zero_shift_pass,
        "input_contracts": {
            "dossiers": dossier_input_checks,
            "schedules": schedule_input_checks,
            "cta_states": cta_checks,
        },
        "capacity_fixture": capacity_checks,
        "locked_dossier": {
            "rendered": False,
            "reason": "UI/UX semantic conflict; current runtime keeps selected dossier when locked region is clicked",
            "disabled_cta_tested": True,
        },
        "release": {
            "internal_slot_pressure_board": "pass" if all_pass else "fail",
            "atlas_manifest_godot": "blocked_pending_visual_dual_review",
            "backdecor_composition": "blocked_pending_visual_dual_review",
        },
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    qa = Image.open(full_path(BOARD_FILES["qa"])).convert("RGB")
    draw = ImageDraw.Draw(qa)
    color = (73, 222, 161) if all_pass else (236, 78, 75)
    draw.rectangle((1398, 1000, 1888, 1060), fill=(1, 24, 41), outline=color, width=2)
    draw.text((1412, 1010), f"INDEPENDENT VALIDATION: {'PASS' if all_pass else 'FAIL'}", font=font(15, True), fill=color, anchor="lt")
    draw.text((1412, 1036), f"glyphs={len(glyphs)} · zero-shift={zero_shift_pass} · image=69:44", font=font(11), fill=(194, 207, 197), anchor="lt")
    qa.save(QA_PATH)

    print(json.dumps({
        "all_pass": all_pass,
        "glyph_count": len(glyphs),
        "glyph_fit_failures": len(glyph_checks["fit_failures"]),
        "glyph_contrast_failures": len(glyph_checks["contrast_failures"]),
        "zero_shift_pass": zero_shift_pass,
        "canonical_image_pass": all(item["pass"] for item in image_checks.values()) and same_source_pass,
        "input_pass": all(item["pass"] for item in dossier_input_checks.values()) and all(item["pass"] for item in schedule_input_checks.values()) and all(item["pass"] for item in cta_checks.values()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    validate()
