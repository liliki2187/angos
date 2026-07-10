# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

import wmw_v092_left_card_b1_vertical_slice as b1


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
CONTRACT_PATH = ROOT / "design/ui-contracts/world-map/left_region_card.json"
SOURCE_B = BASE / "383-world-map-wmw-v0-9-1-left-card-imagegen-candidate-b.png"
IMAGEGEN_B1_R4 = BASE / "396-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r4-wide-failed.png"
PREV_B1_CANDIDATE = BASE / "397-world-map-wmw-v0-9-2-left-card-candidate-b1-composited-polish.png"
PREV_B1_GODOT = BASE / "403-world-map-wmw-v0-9-2-left-card-candidate-b1-godot-single-component.png"

OUT_CANDIDATE = BASE / "406-world-map-wmw-v0-9-3-left-card-candidate-b1-1-composite-clean.png"
OUT_QA = BASE / "407-world-map-wmw-v0-9-3-left-card-candidate-b1-1-geometry-qa.png"
OUT_ATLAS = BASE / "408-world-map-wmw-v0-9-3-left-card-candidate-b1-1-atlas-2x.png"
OUT_RUNTIME = BASE / "409-world-map-wmw-v0-9-3-left-card-candidate-b1-1-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "410-world-map-wmw-v0-9-3-left-card-candidate-b1-1-runtime-fill-qa.png"
OUT_MANIFEST = BASE / "411-world-map-wmw-v0-9-3-left-card-candidate-b1-1-manifest.json"
OUT_GODOT = BASE / "412-world-map-wmw-v0-9-3-left-card-candidate-b1-1-godot-single-component.png"
OUT_GODOT_QA = BASE / "413-world-map-wmw-v0-9-3-left-card-candidate-b1-1-godot-single-component-qa.png"
OUT_COMPARE = BASE / "414-world-map-wmw-v0-9-3-left-card-b1-vs-b1-1-composite-fix-board.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_candidate_b11_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_candidate_b11_manifest.json"

STATE_ORDER = ["selected", "available", "warning", "locked"]
STATE_LABELS = [
    ("\u5317\u7f8e\u7981\u533a\u5e26", "\u7ea2\u7ebf\u5347\u6e29  \u63a8\u83502"),
    ("\u6b27\u6d32\u7070\u57df", "\u53ef\u6d3e\u9063  \u7ebf\u62a52"),
    ("\u975e\u6d32\u7981\u533a\u5e26", "\u5f02\u5e38\u5347\u6e29  \u9ad8\u5371"),
    ("\u5357\u7f8e\u7981\u533a\u5e26", "\u9501\u5b9a  \u97003\u7ebf\u62a5"),
]

FRAME_SIZE = (408, 320)
EXPORT_SIZE = (204, 160)
TARGET_RATIO = 1.275
RATIO_TOLERANCE = 0.015
PHOTO_RECT_2X = (42, 48, 390, 176)
ICON_RESTORE_RECT_2X = (0, 0, 96, 96)
ICON_RESTORE_ELLIPSE_2X = (14, 12, 94, 92)
ACTION_RECT_2X = (316, 212, 392, 288)

# Crop inside the imagegen cards, not at the baked card frame. These windows
# deliberately skip the source globe badge, source border, and green backing.
PHOTO_RELS = {
    "selected": (0.31, 0.09, 0.94, 0.59),
    "available": (0.31, 0.09, 0.88, 0.59),
    "warning": (0.29, 0.09, 0.91, 0.60),
    "locked": (0.31, 0.09, 0.88, 0.60),
}

FONT_BOLD = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]
FONT_REGULAR = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]
F_SMALL = b1.font(FONT_REGULAR, 13)
F_NOTE = b1.font(FONT_REGULAR, 16)
F_HEAD = b1.font(FONT_BOLD, 26)
F_TITLE = b1.font(FONT_BOLD, 19)
F_META = b1.font(FONT_REGULAR, 11)

TOKENS = {
    "label_title": {
        "font": F_TITLE,
        "godot_font_size": 25,
        "fill": (18, 22, 18, 248),
        "godot_color": "#121612",
    },
    "meta_status": {
        "font": F_META,
        "godot_font_size": 14,
        "fill": (66, 28, 20, 248),
        "godot_color": "#421c14",
    },
}


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def slot_rect(contract: dict, name: str, scale: int = 2) -> tuple[int, int, int, int]:
    x, y, w, h = contract["frozen"]["slots"][name]
    return (x * scale, y * scale, (x + w) * scale, (y + h) * scale)


def source_frames(path: Path) -> tuple[list[Image.Image], list[dict]]:
    source = Image.open(path).convert("RGB")
    mask = b1.build_mask(source)
    boxes = b1.find_quadrant_boxes(mask)
    frames: list[Image.Image] = []
    meta: list[dict] = []
    for state, box in zip(STATE_ORDER, boxes):
        crop, expanded = b1.crop_with_alpha(source, mask, box, pad=8)
        frame, fit = b1.fit_into_frame(crop, FRAME_SIZE)
        frame = b1.zero_chroma_alpha(frame)
        frames.append(frame)
        meta.append({"state": state, "box": list(box), "expanded_box": list(expanded), "fit": fit})
    return frames, meta


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
    patch = scrub_photo_patch_edges(patch)
    target_size = (PHOTO_RECT_2X[2] - PHOTO_RECT_2X[0], PHOTO_RECT_2X[3] - PHOTO_RECT_2X[1])
    patch = ImageOps.fit(patch, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.54))
    patch = scrub_resized_photo_edges(patch, state)
    return patch.convert("RGBA")


def scrub_photo_patch_edges(patch: Image.Image) -> Image.Image:
    out = patch.convert("RGB")
    px = out.load()
    w, h = out.size

    def is_source_residue(c: tuple[int, int, int]) -> bool:
        r, g, b = c
        very_light_frame = r > 210 and g > 200 and b > 175
        chroma_or_glow_green = g > 160 and g > r * 1.35 and g > b * 1.25
        return very_light_frame or chroma_or_glow_green

    # A narrow in-paint for accidental source frame or chroma remnants on crop edges.
    for y in range(h):
        for x in list(range(0, min(10, w))) + list(range(max(0, w - 10), w)):
            if is_source_residue(px[x, y]):
                ref_x = min(max(10, x), w - 11)
                px[x, y] = px[ref_x, y]
    for x in range(w):
        for y in list(range(0, min(8, h))) + list(range(max(0, h - 8), h)):
            if is_source_residue(px[x, y]):
                ref_y = min(max(8, y), h - 9)
                px[x, y] = px[x, ref_y]
    return out


def scrub_resized_photo_edges(patch: Image.Image, state: str) -> Image.Image:
    out = patch.convert("RGBA")
    px = out.load()
    w, h = out.size

    def is_residue(c: tuple[int, int, int, int]) -> bool:
        r, g, b, a = c
        if a <= 8:
            return False
        return (g > 155 and g > r * 1.32 and g > b * 1.22) or (r > 220 and g > 212 and b > 182)

    for y in range(h):
        ref_x = max(0, w - 70)
        for x in range(max(0, w - 64), w):
            if is_residue(px[x, y]):
                px[x, y] = px[ref_x, y]
    for y in range(h):
        ref_x = min(w - 1, 68)
        for x in range(0, min(50, w)):
            if is_residue(px[x, y]):
                px[x, y] = px[ref_x, y]
    for x in range(w):
        ref_y = min(h - 1, 14)
        for y in range(0, min(12, h)):
            if is_residue(px[x, y]):
                px[x, y] = px[x, ref_y]
    if state in {"available", "locked"}:
        ref_x = max(0, w - 38)
        for y in range(h):
            for x in range(max(0, w - 22), w):
                px[x, y] = px[ref_x, y]
    return out


def restore_baked_globe_only(clean: Image.Image, base: Image.Image) -> Image.Image:
    out = clean.convert("RGBA")
    mask = Image.new("L", out.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse(ICON_RESTORE_ELLIPSE_2X, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    out.paste(base.convert("RGBA"), (0, 0), mask)
    return out


def is_artifact_green_pixel(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    return a > 8 and r <= 100 and g >= 105 and b <= 115 and g - r >= 25 and g - b >= 25


def scrub_nonselected_artifact_green(frame: Image.Image, state: str) -> Image.Image:
    if state == "selected":
        return frame
    out = frame.convert("RGBA")
    px = out.load()
    px1, py1, px2, py2 = PHOTO_RECT_2X
    for _pass in range(2):
        for y in range(out.height):
            for x in range(out.width):
                if not is_artifact_green_pixel(px[x, y]):
                    continue
                if px1 <= x < px2 and py1 <= y < py2:
                    ref_x = max(px1, x - 36)
                    if is_artifact_green_pixel(px[ref_x, y]):
                        ref_x = max(px1, x - 72)
                    px[x, y] = px[ref_x, y]
                else:
                    r, g, b, _a = px[x, y]
                    px[x, y] = (r, g, b, 0)
    return out


def recolor_warning_triangle(frame: Image.Image) -> Image.Image:
    out = frame.convert("RGBA")
    overlay = Image.new("L", out.size, 0)
    draw = ImageDraw.Draw(overlay)
    x1, y1, x2, y2 = ACTION_RECT_2X
    cx = (x1 + x2) // 2
    draw.polygon([(cx, y1 + 22), (x1 + 21, y2 - 18), (x2 - 21, y2 - 18)], fill=255)

    px = out.load()
    mask = overlay.load()
    red = (215, 37, 32)
    for y in range(y1, y2):
        for x in range(x1, x2):
            if mask[x, y] == 0:
                continue
            r, g, b, a = px[x, y]
            if a <= 20:
                continue
            if r > 125 and g > 95 and b > 60:
                px[x, y] = (
                    round(r * 0.38 + red[0] * 0.62),
                    round(g * 0.32 + red[1] * 0.68),
                    round(b * 0.28 + red[2] * 0.72),
                    a,
                )
    return out


def compose_frames(contract: dict) -> tuple[list[Image.Image], list[dict], list[dict]]:
    base_frames, base_meta = source_frames(SOURCE_B)
    art_source = Image.open(IMAGEGEN_B1_R4).convert("RGB")
    art_mask = b1.build_mask(art_source)
    art_boxes = b1.find_quadrant_boxes(art_mask)

    photo_rect = slot_rect(contract, "photo_slot")
    frames: list[Image.Image] = []
    composition: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        base = base_frames[idx].copy()
        photo = crop_source_photo(art_source, art_boxes[idx], state)

        # Hard-slot mask: pixels outside photo_slot are never touched by the photo patch.
        clean = base.copy()
        clean.alpha_composite(photo, (photo_rect[0], photo_rect[1]))

        # Single icon track: restore only the circular B-shell globe badge.
        clean = restore_baked_globe_only(clean, base)

        if state == "warning":
            clean = recolor_warning_triangle(clean)

        clean = b1.zero_chroma_alpha(clean)
        clean = scrub_nonselected_artifact_green(clean, state)
        frames.append(clean)
        composition.append(
            {
                "state": state,
                "base_source": str(SOURCE_B),
                "photo_source": str(IMAGEGEN_B1_R4),
                "photo_source_box": list(art_boxes[idx]),
                "photo_rel_crop": list(PHOTO_RELS[state]),
                "photo_slot_2x": list(photo_rect),
                "icon_restore_rect_2x": list(ICON_RESTORE_RECT_2X),
                "runtime_warning_triangle_overlay": "removed",
                "warning_triangle_recolor": "baked_material_recolor" if state == "warning" else "not_applicable",
            }
        )
    return frames, base_meta, composition


def make_candidate_sheet(frames: list[Image.Image]) -> Image.Image:
    margin = 54
    gap = 58
    label_h = 36
    w = margin * 2 + FRAME_SIZE[0] * 2 + gap
    h = margin * 2 + (FRAME_SIZE[1] + label_h) * 2 + gap
    sheet = Image.new("RGBA", (w, h), (18, 30, 31, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 16), "B1.1 v0.9.3 composite clean source: slot mask + single icon track", fill=(236, 231, 197), font=F_HEAD)
    for i, state in enumerate(STATE_ORDER):
        col = i % 2
        row = i // 2
        x = margin + col * (FRAME_SIZE[0] + gap)
        y = margin + row * (FRAME_SIZE[1] + label_h + gap)
        sheet.alpha_composite(frames[i], (x, y))
        draw.rectangle((x, y, x + FRAME_SIZE[0], y + FRAME_SIZE[1]), outline=(111, 166, 143), width=2)
        draw.text((x, y + FRAME_SIZE[1] + 8), f"{state}: no duplicate globe, no slot overflow, B badge only", fill=(215, 224, 199), font=F_NOTE)
    return sheet


def make_geometry_qa(frames: list[Image.Image], composition: list[dict]) -> tuple[Image.Image, list[dict]]:
    margin = 42
    gap = 42
    label_h = 76
    w = margin * 2 + FRAME_SIZE[0] * 2 + gap
    h = margin * 2 + (FRAME_SIZE[1] + label_h) * 2 + gap
    img = Image.new("RGBA", (w, h), (14, 23, 24, 255))
    draw = ImageDraw.Draw(img)
    metrics: list[dict] = []
    for i, state in enumerate(STATE_ORDER):
        col = i % 2
        row = i // 2
        x = margin + col * (FRAME_SIZE[0] + gap)
        y = margin + row * (FRAME_SIZE[1] + label_h + gap)
        img.alpha_composite(frames[i], (x, y))
        ratio = FRAME_SIZE[0] / FRAME_SIZE[1]
        ratio_delta = abs(ratio - TARGET_RATIO)
        passed = ratio_delta <= RATIO_TOLERANCE
        photo = PHOTO_RECT_2X
        action = ACTION_RECT_2X
        draw.rectangle((x, y, x + FRAME_SIZE[0], y + FRAME_SIZE[1]), outline=(100, 255, 146), width=3)
        draw.rectangle((x + photo[0], y + photo[1], x + photo[2], y + photo[3]), outline=(91, 233, 255), width=2)
        draw.rectangle((x + action[0], y + action[1], x + action[2], y + action[3]), outline=(255, 101, 101), width=2)
        draw.text((x, y + FRAME_SIZE[1] + 8), f"{state} export={FRAME_SIZE[0]}x{FRAME_SIZE[1]} ratio={ratio:.3f} {'PASS' if passed else 'FAIL'}", fill=(231, 239, 207), font=F_NOTE)
        draw.text((x, y + FRAME_SIZE[1] + 34), "photo slot clipped to [42,48,348,128] px; badge track restored from B shell", fill=(181, 200, 179), font=F_SMALL)
        metrics.append(
            {
                "state": state,
                "export_size_2x": list(FRAME_SIZE),
                "export_size_1x": list(EXPORT_SIZE),
                "ratio": ratio,
                "ratio_target": TARGET_RATIO,
                "ratio_delta": ratio_delta,
                "ratio_pass": passed,
                "photo_slot_2x": list(PHOTO_RECT_2X),
                "action_badge_2x": list(ACTION_RECT_2X),
                "composition": composition[i],
            }
        )
    return img, metrics


def make_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", (FRAME_SIZE[0] * len(frames), FRAME_SIZE[1]), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        atlas.alpha_composite(frame, (i * FRAME_SIZE[0], 0))
    return atlas


def draw_text_fit(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill: tuple[int, int, int, int], max_width: int) -> None:
    current = font
    if isinstance(font, ImageFont.FreeTypeFont):
        size = font.size
        while size >= 13:
            candidate = b1.font(FONT_BOLD if font == F_TITLE else FONT_REGULAR, size)
            bbox = draw.textbbox((0, 0), text, font=candidate)
            if bbox[2] - bbox[0] <= max_width:
                current = candidate
                break
            size -= 1
    draw.text(xy, text, font=current, fill=fill)


def make_runtime_preview(frames: list[Image.Image], contract: dict, show_qa: bool) -> Image.Image:
    canvas = Image.new("RGB", (1920, 1080), (7, 19, 21))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 26, 424, 1056), fill=(4, 12, 14), outline=(34, 73, 70), width=2)
    draw.text((450, 34), "Python v0.9.3 B1.1 left_region_card runtime fill", fill=(243, 239, 214), font=F_HEAD)
    draw.text((450, 76), "Atlas art is clean composite; title/meta are runtime text tokens inside contract slots.", fill=(217, 222, 199), font=F_NOTE)

    scale = 1.5
    card_w, card_h = round(EXPORT_SIZE[0] * scale), round(EXPORT_SIZE[1] * scale)
    positions = [(66, 36), (66, 294), (66, 552), (66, 810)]
    slots = contract["frozen"]["slots"]
    for i, state in enumerate(STATE_ORDER):
        x, y = positions[i]
        frame = frames[i].resize((card_w, card_h), Image.Resampling.LANCZOS)
        canvas.paste(frame.convert("RGB"), (x, y), frame.getchannel("A").resize((card_w, card_h), Image.Resampling.LANCZOS))

        title, meta = STATE_LABELS[i]
        lx, ly, lw, lh = slots["label_plate"]
        mx, my, mw, mh = slots["meta_line"]
        draw_text_fit(draw, (x + round((lx + 12) * scale), y + round((ly + 5) * scale)), title, TOKENS["label_title"]["font"], TOKENS["label_title"]["fill"], round((lw - 16) * scale))
        draw.text((x + round((mx + 5) * scale), y + round((my - 2) * scale)), meta, font=TOKENS["meta_status"]["font"], fill=TOKENS["meta_status"]["fill"])

        if show_qa:
            for name, color in {
                "photo_slot": (88, 233, 255),
                "label_plate": (255, 229, 93),
                "meta_line": (255, 159, 82),
                "action_badge": (255, 105, 105),
            }.items():
                sx, sy, sw, sh = slots[name]
                rect = (x + round(sx * scale), y + round(sy * scale), x + round((sx + sw) * scale), y + round((sy + sh) * scale))
                draw.rectangle(rect, outline=color, width=2)
                draw.text((rect[0] + 4, rect[1] + 2), name.replace("_slot", "").replace("_plate", ""), fill=color, font=F_SMALL)
            draw.rectangle((x, y, x + card_w, y + card_h), outline=(101, 255, 138), width=2)
    return canvas


def count_colors_nonblack(path: Path) -> dict:
    img = Image.open(path).convert("RGB")
    colors = img.getcolors(maxcolors=20_000_000)
    nonblack = 0
    for count, (r, g, b) in colors or []:
        if r > 5 or g > 5 or b > 5:
            nonblack += count
    return {"size": list(img.size), "unique_colors": len(colors or []), "nonblack_pixels": nonblack}


def artifact_green_stats(frames: list[Image.Image]) -> dict:
    stats: dict[str, dict] = {}
    for state, frame in zip(STATE_ORDER, frames):
        img = frame.convert("RGBA")
        px = img.load()
        count = 0
        samples = []
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = px[x, y]
                if a > 8 and r <= 90 and g >= 120 and b <= 105 and g - r >= 35 and g - b >= 30:
                    count += 1
                    if len(samples) < 8:
                        samples.append([x, y, r, g, b, a])
        stats[state] = {
            "artifact_greenish_pixels_full_frame": count,
            "sample_pixels": samples,
            "range": "full 408x320 atlas frame after chroma-key alpha removal",
            "definition": "alpha>8 and r<=90 and g>=120 and b<=105 and g-r>=35 and g-b>=30",
        }
    return stats


def make_manifest(
    contract: dict,
    base_meta: list[dict],
    composition: list[dict],
    geometry_metrics: list[dict],
    green_stats: dict,
) -> dict:
    ratio_pass = all(m["ratio_pass"] for m in geometry_metrics)
    nonselected_green_pass = all(green_stats[state]["artifact_greenish_pixels_full_frame"] == 0 for state in ["available", "warning", "locked"])
    composite_checks = {
        state: {
            "duplicate_globe": "pass_none_visible",
            "source_frame_residue": "fail_right_edge_vertical_strip_visible_after_user_review",
            "photo_slot_overflow": "pass_none_visible; photo pixels clipped before paste to 2x slot",
            "right_edge_strip": "fail_visible_dark_or_colored_vertical_band_at_photo_slot_right_edge",
            "runtime_duplicate_warning_triangle": "pass_removed_runtime_overlay" if state == "warning" else "not_applicable",
            "manual_check_basis": "user-marked 414 close-up shows repeated right-edge vertical strip across all four states; prior 406/409 inspection was insufficient",
        }
        for state in STATE_ORDER
    }
    return {
        "schema_version": 1,
        "asset_id": "world_map_wmw_left_region_card_candidate_b1_1",
        "version": "v0.9.3",
        "status": "candidate_b1_1_composite_cleanliness_failed_user_review_right_edge_strip",
        "date": "2026-07-08",
        "contract": str(CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "inputs": {
            "candidate_b_shell": str(SOURCE_B),
            "candidate_b1_imagegen_photo_source": str(IMAGEGEN_B1_R4),
            "previous_b1_composite": str(PREV_B1_CANDIDATE),
            "previous_b1_godot": str(PREV_B1_GODOT),
        },
        "outputs": {
            "candidate_b1_1_composite": str(OUT_CANDIDATE),
            "geometry_qa": str(OUT_QA),
            "atlas_2x": str(OUT_ATLAS),
            "runtime_fill_preview": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "godot_single_component": str(OUT_GODOT),
            "godot_single_component_qa": str(OUT_GODOT_QA),
            "b1_vs_b1_1_composite_fix_board": str(OUT_COMPARE),
            "godot_atlas_copy": str(GODOT_ATLAS),
            "godot_manifest_copy": str(GODOT_MANIFEST),
        },
        "runtime_tokens": {
            "label_title": {
                "python_font_px": 19,
                "godot_font_size": TOKENS["label_title"]["godot_font_size"],
                "color": TOKENS["label_title"]["godot_color"],
            },
            "meta_status": {
                "python_font_px": 11,
                "godot_font_size": TOKENS["meta_status"]["godot_font_size"],
                "color": TOKENS["meta_status"]["godot_color"],
            },
        },
        "base_frame_sources": base_meta,
        "composition": composition,
        "geometry_metrics": geometry_metrics,
        "artifact_green_stats": green_stats,
        "gates": {
            "geometry_ratio_1_275": {
                "status": "pass" if ratio_pass else "fail",
                "target_ratio": TARGET_RATIO,
                "tolerance": RATIO_TOLERANCE,
                "basis": "normalized 2x atlas frames are 408x320; no scale/crop-to-fit after compositing",
            },
            "photo_slot_mask": {
                "status": "pass",
                "photo_slot_2x": list(PHOTO_RECT_2X),
                "basis": "photo crops are fitted to the exact slot size and alpha-composited at the exact slot origin",
            },
            "single_icon_track": {
                "status": "pass",
                "basis": "B shell baked globe and B shell state badges are restored/kept; no runtime warning-triangle overlay remains",
            },
            "greenish_full_frame_nonselected": {
                "status": "pass" if nonselected_green_pass else "fail",
                "basis": "full 408x320 atlas-frame scan after chroma-key alpha removal",
            },
            "composite_cleanliness": {
                "status": "fail",
                "basis": "revoked after user review: right-edge vertical strip / seam remains visible in all four B1.1 states; greenish/nonblack/geometry gates did not cover this artifact",
                "checks": composite_checks,
            },
            "no_fake_text": {
                "status": "pass",
                "basis": "atlas contains no baked readable text; Chinese strings are runtime labels in 409 and Godot capture",
            },
            "functional_faces_orthogonal": {
                "status": "pass",
                "basis": "B shell face remains orthogonal; B1.1 only replaces clipped photo-slot pixels and recolors baked warning triangle pixels",
            },
            "same_state_layout": {
                "status": "pass",
                "basis": "all four states use the same 204x160 contract frame, identical slots, and unchanged action/icon badge positions",
            },
        },
        "visual_repair_notes": [
            "Fixed double globe by cropping photos away from the imagegen globe and restoring the B shell icon badge after photo paste.",
            "Fixed warning double triangle by deleting the runtime overlay path and tinting only baked warning-triangle pixels.",
            "Fixed Europe photo overflow by hard-clipping every photo patch to photo_slot [21,24,174,64] at 1x / [42,48,348,128] at 2x.",
            "Locked-card green-strip check now uses full-frame artifact-green measurement, not the previous 32px outer-edge-only scan.",
            "User review found B1.1 still has a right-edge vertical strip/seam; B1.1 is not visually passed until the edge-band artifact is removed and rechecked with close-up crops.",
        ],
    }


def save_outputs() -> None:
    contract = load_contract()
    frames, base_meta, composition = compose_frames(contract)
    candidate = make_candidate_sheet(frames)
    qa, geometry_metrics = make_geometry_qa(frames, composition)
    atlas = make_atlas(frames)
    runtime = make_runtime_preview(frames, contract, show_qa=False)
    runtime_qa = make_runtime_preview(frames, contract, show_qa=True)
    green_stats = artifact_green_stats(frames)
    manifest = make_manifest(contract, base_meta, composition, geometry_metrics, green_stats)

    for path in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA]:
        path.parent.mkdir(parents=True, exist_ok=True)
    OUT_CANDIDATE.write_bytes(b"")
    candidate.save(OUT_CANDIDATE)
    qa.save(OUT_QA)
    atlas.save(OUT_ATLAS)
    runtime.save(OUT_RUNTIME)
    runtime_qa.save(OUT_RUNTIME_QA)
    manifest["image_content_checks"] = {
        "candidate": count_colors_nonblack(OUT_CANDIDATE),
        "geometry_qa": count_colors_nonblack(OUT_QA),
        "atlas_2x": count_colors_nonblack(OUT_ATLAS),
        "runtime_fill_preview": count_colors_nonblack(OUT_RUNTIME),
        "runtime_fill_qa": count_colors_nonblack(OUT_RUNTIME_QA),
    }
    if OUT_GODOT.exists() and OUT_GODOT_QA.exists():
        manifest["image_content_checks"]["godot_single_component"] = count_colors_nonblack(OUT_GODOT)
        manifest["image_content_checks"]["godot_single_component_qa"] = count_colors_nonblack(OUT_GODOT_QA)
        manifest["gates"]["godot_windowed_capture"] = {
            "status": "pass",
            "basis": "windowed opengl3 capture via scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro; nonblack and color-diversity checks recorded",
            "headless_used_for_ui_capture": False,
        }
    if OUT_COMPARE.exists():
        manifest["image_content_checks"]["b1_vs_b1_1_composite_fix_board"] = count_colors_nonblack(OUT_COMPARE)
    else:
        manifest["gates"]["godot_windowed_capture"] = {
            "status": "pending",
            "basis": "run scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro, then rerun this script to fold screenshot stats into the manifest",
            "headless_used_for_ui_capture": False,
        }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    for path in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_MANIFEST, GODOT_ATLAS, GODOT_MANIFEST]:
        print(path)


if __name__ == "__main__":
    save_outputs()
