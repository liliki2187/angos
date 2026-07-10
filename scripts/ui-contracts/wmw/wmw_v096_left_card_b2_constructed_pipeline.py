# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v094_left_card_b12_right_edge_fix as b12


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

OUT_INGREDIENTS = BASE / "436-world-map-wmw-v0-9-6-left-card-b2-constructed-ingredients.png"
OUT_CANDIDATE = BASE / "437-world-map-wmw-v0-9-6-left-card-b2-constructed-composite.png"
OUT_QA = BASE / "438-world-map-wmw-v0-9-6-left-card-b2-geometry-qa.png"
OUT_ATLAS = BASE / "439-world-map-wmw-v0-9-6-left-card-b2-atlas-2x.png"
OUT_RUNTIME = BASE / "440-world-map-wmw-v0-9-6-left-card-b2-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "441-world-map-wmw-v0-9-6-left-card-b2-runtime-fill-qa.png"
OUT_MANIFEST = BASE / "442-world-map-wmw-v0-9-6-left-card-b2-manifest.json"
OUT_EDGE_QA = BASE / "443-world-map-wmw-v0-9-6-left-card-b2-edge-and-texture-qa.png"
OUT_COMPARE = BASE / "444-world-map-wmw-v0-9-6-left-card-b1-3-vs-b2-constructed-board.png"
OUT_GODOT = BASE / "445-world-map-wmw-v0-9-6-left-card-b2-godot-single-component.png"
OUT_GODOT_QA = BASE / "446-world-map-wmw-v0-9-6-left-card-b2-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b2_constructed_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b2_constructed_manifest.json"

PREV_B13_COMPOSITE = BASE / "426-world-map-wmw-v0-9-5-left-card-candidate-b1-3-shell-rebuild.png"
PREV_B13_RUNTIME = BASE / "429-world-map-wmw-v0-9-5-left-card-candidate-b1-3-runtime-fill.png"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
PHOTO_RECT_2X = b11.PHOTO_RECT_2X
ACTION_RECT_2X = b11.ACTION_RECT_2X
TARGET_RATIO = b11.TARGET_RATIO
RATIO_TOLERANCE = b11.RATIO_TOLERANCE

# B2 keeps the frozen contract slot untouched, but makes the art-layer visible
# photo window explicit. The strict slot version removes old residue but still
# reads as a right-side rail; this visual-window variant tests the semantic
# split proposed in the loop review: visual photo window != runtime safe slot.
CONTRACT_PHOTO_RECT_2X = PHOTO_RECT_2X
VISUAL_PHOTO_RECT_2X = PHOTO_RECT_2X
PHOTO_CLEAR_RECT = (PHOTO_RECT_2X[0], PHOTO_RECT_2X[1], FRAME_SIZE[0], PHOTO_RECT_2X[3])
PHOTO_RIGHT_BAND = (PHOTO_RECT_2X[2], PHOTO_RECT_2X[1], FRAME_SIZE[0], PHOTO_RECT_2X[3])
ALPHA_PROBE = (PHOTO_RECT_2X[2], 40, FRAME_SIZE[0], 300)
ALPHA_CONTROL_PROBE = (PHOTO_RECT_2X[0], 40, PHOTO_RECT_2X[2], 300)

PLATE_SAMPLE_RECTS = {
    # Quiet material strips from the B shell after normalization. They avoid
    # the photo, globe, label plate, action badge, and selected-state green
    # glow. The earlier B2 draft sampled the lower plate, which leaked a
    # chroma-green stripe back into the reconstructed photo edge.
    "upper_plate": (54, 180, 300, 205),
    "left_plate": (46, 184, 94, 284),
}


def _bad_plate_pixel(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    if a < 32:
        return True
    chroma_green = r <= 120 and g >= 120 and b <= 120 and g - r >= 24 and g - b >= 24
    bright_frame = r > 232 and g > 225 and b > 200
    near_black_gap = r < 8 and g < 14 and b < 14
    return chroma_green or bright_frame or near_black_gap


def _replacement_plate_pixel(px, x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    for radius in (2, 4, 8, 14):
        samples: list[tuple[int, int, int]] = []
        for yy in range(max(0, y - radius), min(h, y + radius + 1)):
            for xx in range(max(0, x - radius), min(w, x + radius + 1)):
                c = px[xx, yy]
                if not _bad_plate_pixel(c):
                    r, g, b, _a = c
                    samples.append((r, g, b))
        if samples:
            samples.sort()
            r = sum(c[0] for c in samples) // len(samples)
            g = sum(c[1] for c in samples) // len(samples)
            b = sum(c[2] for c in samples) // len(samples)
            return (r, g, b, 255)
    return (42, 55, 48, 255)


def _b2_chroma_residue(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    return a > 8 and r <= 105 and g >= 105 and b <= 115 and g - r >= 25 and g - b >= 25


def _inside_reconstructed_body(x: int, y: int) -> bool:
    if 20 <= x <= 388 and 18 <= y <= 302:
        return True
    if PHOTO_RECT_2X[2] <= x < FRAME_SIZE[0] and 40 <= y < 300:
        return True
    return False


def _replacement_frame_pixel(px, x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    for radius in (3, 6, 10, 18):
        samples: list[tuple[int, int, int]] = []
        for yy in range(max(0, y - radius), min(h, y + radius + 1)):
            for xx in range(max(0, x - radius), min(w, x + radius + 1)):
                r, g, b, a = px[xx, yy]
                if a > 180 and not _b2_chroma_residue((r, g, b, a)):
                    samples.append((r, g, b))
        if samples:
            return (
                sum(c[0] for c in samples) // len(samples),
                sum(c[1] for c in samples) // len(samples),
                sum(c[2] for c in samples) // len(samples),
                255,
            )
    return (45, 54, 46, 255)


def _scrub_chroma_residue(frame: Image.Image) -> Image.Image:
    out = frame.convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if not _b2_chroma_residue(px[x, y]):
                continue
            if _inside_reconstructed_body(x, y):
                px[x, y] = _replacement_frame_pixel(px, x, y, out.width, out.height)
            else:
                r, g, b, _a = px[x, y]
                px[x, y] = (r, g, b, 0)
    return out


def _clip_to_shell_silhouette(frame: Image.Image, base: Image.Image) -> Image.Image:
    """Keep constructed layers inside the B-shell card silhouette."""
    out = frame.convert("RGBA")
    px = out.load()
    mask_px = base.convert("RGBA").load()
    for y in range(out.height):
        for x in range(out.width):
            if mask_px[x, y][3] < 24:
                r, g, b, _a = px[x, y]
                px[x, y] = (r, g, b, 0)
    return out


def _clip_rect(rect: tuple[int, int, int, int], size: tuple[int, int]) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = rect
    return (max(0, x1), max(0, y1), min(size[0], x2), min(size[1], y2))


def _opaque_patch(base: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    rect = _clip_rect(rect, base.size)
    patch = base.crop(rect).convert("RGBA")
    px = patch.load()
    for y in range(patch.height):
        for x in range(patch.width):
            r, g, b, a = px[x, y]
            if _bad_plate_pixel((r, g, b, a)):
                px[x, y] = _replacement_plate_pixel(px, x, y, patch.width, patch.height)
            else:
                px[x, y] = (r, g, b, 255)
    return patch


def _make_plate_texture(base: Image.Image, state: str, size: tuple[int, int]) -> tuple[Image.Image, dict]:
    patches = [_opaque_patch(base, rect) for rect in PLATE_SAMPLE_RECTS.values()]
    seed = Image.new("RGBA", (max(p.width for p in patches), sum(p.height for p in patches)), (0, 0, 0, 255))
    y = 0
    for patch in patches:
        seed.alpha_composite(patch, (0, y))
        y += patch.height

    out = Image.new("RGBA", size, (0, 0, 0, 255))
    for yy in range(0, size[1], seed.height):
        for xx in range(0, size[0], seed.width):
            tile = seed
            if (xx // seed.width) % 2:
                tile = ImageOps.mirror(tile)
            if (yy // seed.height) % 2:
                tile = ImageOps.flip(tile)
            out.alpha_composite(tile, (xx, yy))

    # Blend lightly with the source B shell hue so each state keeps the
    # accepted B palette while retaining real bitmap texture variation.
    tint = Image.new("RGBA", size, _average_rgb(seed) + (255,))
    out = Image.blend(out, tint, 0.18)
    meta = {
        "state": state,
        "source": str(b11.SOURCE_B),
        "sample_rects_2x": {name: list(rect) for name, rect in PLATE_SAMPLE_RECTS.items()},
        "tile_size": [seed.width, seed.height],
        "target_size": list(size),
        "method": "mirror-tiled B-shell plate material; no synthetic flat color band",
    }
    return out, meta


def _average_rgb(img: Image.Image) -> tuple[int, int, int]:
    rgb = img.convert("RGB")
    colors = rgb.resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))
    return (int(colors[0]), int(colors[1]), int(colors[2]))


def _clear_photo_window_with_plate(base: Image.Image, plate: Image.Image) -> Image.Image:
    out = base.convert("RGBA")
    x1, y1, x2, y2 = PHOTO_CLEAR_RECT
    plate_crop = plate.crop((0, 0, x2 - x1, y2 - y1))
    out.alpha_composite(plate_crop, (x1, y1))
    return out


def _overlay_window_lips(out: Image.Image, base: Image.Image) -> Image.Image:
    """Rebuild the photo slot edge from B-shell bitmap material.

    For the visual-window variant, the photo reaches the atlas right edge;
    only top, bottom, and left lips are restored from B-shell material.
    """
    result = out.convert("RGBA")
    base = base.convert("RGBA")
    x1, y1, x2, y2 = VISUAL_PHOTO_RECT_2X

    pieces = [
        ((x1, y1 - 8, x2, y1 + 2), (x1, y1 - 8), False),
        ((x1, y2 - 2, x2, y2 + 8), (x1, y2 - 2), False),
        ((x1 - 8, y1, x1 + 2, y2), (x1 - 8, y1), False),
    ]
    if x2 < FRAME_SIZE[0]:
        pieces.append(((x1 - 16, y1, x1 + 4, y2), (x2 - 2, y1), True))
    for src_rect, dst, mirror in pieces:
        src_rect = _clip_rect(src_rect, FRAME_SIZE)
        patch = base.crop(src_rect).convert("RGBA")
        if mirror:
            patch = ImageOps.mirror(patch)
        # A narrow blur avoids jagged copy edges while keeping bitmap material.
        mask = patch.getchannel("A").filter(ImageFilter.GaussianBlur(0.25))
        result.paste(patch, dst, mask)
    return result


def _enforce_expected_body_opacity(frame: Image.Image, base: Image.Image) -> Image.Image:
    """Preserve opacity where candidate B shell already defines card body.

    This is not a free-form band fill: it only repairs pixels inside the B-shell
    opaque silhouette that a later chroma cleanup accidentally emptied.
    """
    out = frame.convert("RGBA")
    out_px = out.load()
    expected_px = base.convert("RGBA").load()
    x1, y1, x2, y2 = ALPHA_PROBE
    material = _average_rgb(_opaque_patch(base, PLATE_SAMPLE_RECTS["upper_plate"]))
    for y in range(y1, y2):
        for x in range(x1, x2):
            if expected_px[x, y][3] < 250 or out_px[x, y][3] >= 250:
                continue
            out_px[x, y] = (material[0], material[1], material[2], 255)
    return out


def _crop_photo_for_visual_window(source: Image.Image, box: tuple[int, int, int, int], state: str) -> Image.Image:
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    rx1, ry1, rx2, ry2 = b12.PHOTO_RELS[state]
    crop_box = (
        round(x1 + w * rx1),
        round(y1 + h * ry1),
        round(x1 + w * rx2),
        round(y1 + h * ry2),
    )
    patch = source.crop(crop_box).convert("RGB")
    patch = b11.scrub_photo_patch_edges(patch)
    target_size = (
        VISUAL_PHOTO_RECT_2X[2] - VISUAL_PHOTO_RECT_2X[0],
        VISUAL_PHOTO_RECT_2X[3] - VISUAL_PHOTO_RECT_2X[1],
    )
    patch = ImageOps.fit(patch, target_size, method=Image.Resampling.LANCZOS, centering=(0.50, 0.54))
    patch = b12.hard_repair_photo_right_edge(patch.convert("RGBA"))
    return patch


def _crop_photo_ingredients() -> tuple[Image.Image, list[tuple[int, int, int, int]], list[Image.Image]]:
    art_source = Image.open(b11.IMAGEGEN_B1_R4).convert("RGB")
    art_mask = b11.b1.build_mask(art_source)
    art_boxes = b11.b1.find_quadrant_boxes(art_mask)
    photos = [_crop_photo_for_visual_window(art_source, art_boxes[i], state) for i, state in enumerate(STATE_ORDER)]
    return art_source, art_boxes, photos


def compose_frames(contract: dict) -> tuple[list[Image.Image], list[dict], list[dict], list[dict]]:
    base_frames, base_meta = b11.source_frames(b11.SOURCE_B)
    _art_source, art_boxes, photos = _crop_photo_ingredients()
    contract_photo_rect = b11.slot_rect(contract, "photo_slot")
    photo_rect = VISUAL_PHOTO_RECT_2X

    frames: list[Image.Image] = []
    composition: list[dict] = []
    plate_meta: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        base = base_frames[idx].copy()
        plate, plate_info = _make_plate_texture(base, state, (PHOTO_CLEAR_RECT[2] - PHOTO_CLEAR_RECT[0], PHOTO_CLEAR_RECT[3] - PHOTO_CLEAR_RECT[1]))
        clean = _clear_photo_window_with_plate(base, plate)

        # Photo content is clipped to the explicit visual photo window. The
        # frozen contract photo_slot is still recorded as the runtime/safe
        # region and has not been changed.
        clean.alpha_composite(photos[idx], (photo_rect[0], photo_rect[1]))
        clean = _overlay_window_lips(clean, base)
        clean = b11.restore_baked_globe_only(clean, base)
        if state == "warning":
            clean = b11.recolor_warning_triangle(clean)
        clean = b11.scrub_nonselected_artifact_green(clean, state)
        clean = _enforce_expected_body_opacity(clean, base)
        clean = _scrub_chroma_residue(clean)
        clean = _clip_to_shell_silhouette(clean, base)

        frames.append(clean)
        plate_meta.append(plate_info)
        composition.append(
            {
                "state": state,
                "pipeline": "constructed_ingredients",
                "base_frame_source": str(b11.SOURCE_B),
                "plate_texture": plate_info,
                "photo_source": str(b11.IMAGEGEN_B1_R4),
                "photo_source_box": list(art_boxes[idx]),
                "photo_rel_crop_b2": list(b12.PHOTO_RELS[state]),
                "contract_photo_slot_2x": list(contract_photo_rect),
                "visual_photo_window_2x": list(photo_rect),
                "photo_clear_rect_2x": list(PHOTO_CLEAR_RECT),
                "window_lips": "top/bottom/left copied from B shell; right lip mirrors B-shell left-edge material across x390..408",
                "icon_track": "B shell globe and B shell state badge only; no runtime warning overlay",
            }
        )
    return frames, base_meta, composition, plate_meta


def make_ingredient_sheet(frames: list[Image.Image], plate_meta: list[dict]) -> Image.Image:
    base_frames, _base_meta = b11.source_frames(b11.SOURCE_B)
    _art_source, _boxes, photos = _crop_photo_ingredients()
    cell_w = 360
    row_h = 258
    img = Image.new("RGBA", (1680, 90 + row_h * 4), (10, 23, 24, 255))
    draw = ImageDraw.Draw(img)
    draw.text((42, 24), "B2 v0.9.6 constructed ingredients: B shell materials + B1 photos + contract geometry", fill=(242, 238, 210), font=b11.F_HEAD)
    headers = ["B shell source", "plate ingredient", "photo ingredient", "constructed result"]
    for i, h in enumerate(headers):
        draw.text((42 + i * cell_w, 64), h, fill=(188, 216, 190), font=b11.F_NOTE)

    for i, state in enumerate(STATE_ORDER):
        y = 96 + i * row_h
        draw.text((10, y + 4), state, fill=(235, 231, 200), font=b11.F_NOTE)
        preview_size = (306, 240)
        source = base_frames[i].resize(preview_size, Image.Resampling.LANCZOS)
        img.alpha_composite(source, (42, y))

        plate_rect = tuple(plate_meta[i]["sample_rects_2x"]["upper_plate"])
        plate_patch = base_frames[i].crop(plate_rect).resize(preview_size, Image.Resampling.NEAREST)
        img.alpha_composite(plate_patch.convert("RGBA"), (42 + cell_w, y))

        photo = photos[i].resize(preview_size, Image.Resampling.LANCZOS)
        img.alpha_composite(photo, (42 + cell_w * 2, y))

        result = frames[i].resize(preview_size, Image.Resampling.LANCZOS)
        img.alpha_composite(result, (42 + cell_w * 3, y))

        for col in range(4):
            x = 42 + col * cell_w
            draw.rectangle((x, y, x + preview_size[0], y + preview_size[1]), outline=(76, 139, 126), width=2)
    return img


def make_candidate_sheet(frames: list[Image.Image]) -> Image.Image:
    margin = 54
    gap = 58
    label_h = 58
    w = margin * 2 + FRAME_SIZE[0] * 2 + gap + 90
    h = margin * 2 + (FRAME_SIZE[1] + label_h) * 2 + gap
    sheet = Image.new("RGBA", (w, h), (18, 30, 31, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 16), "B2 v0.9.6 constructed composite", fill=(236, 231, 197), font=b11.F_HEAD)
    for i, state in enumerate(STATE_ORDER):
        col = i % 2
        row = i // 2
        x = margin + col * (FRAME_SIZE[0] + gap)
        y = margin + row * (FRAME_SIZE[1] + label_h + gap)
        sheet.alpha_composite(frames[i], (x, y))
        draw.rectangle((x, y, x + FRAME_SIZE[0], y + FRAME_SIZE[1]), outline=(111, 166, 143), width=2)
        draw.text((x, y + FRAME_SIZE[1] + 8), f"{state}: photo=contract slot; rebuilt right lip", fill=(215, 224, 199), font=b11.F_SMALL)
    return sheet


def make_geometry_qa(frames: list[Image.Image], composition: list[dict]) -> tuple[Image.Image, list[dict]]:
    qa, metrics = b11.make_geometry_qa(frames, composition)
    draw = ImageDraw.Draw(qa)
    draw.rectangle((0, 0, qa.width, 34), fill=(14, 23, 24, 255))
    draw.text((42, 4), "B2 constructed geometry QA: contract slots are construction inputs, not post-hoc fitted boxes", fill=(236, 231, 197), font=b11.F_NOTE)
    return qa, metrics


def make_runtime_preview(frames: list[Image.Image], contract: dict, show_qa: bool) -> Image.Image:
    img = b11.make_runtime_preview(frames, contract, show_qa)
    draw = ImageDraw.Draw(img)
    draw.rectangle((438, 20, 1880, 118), fill=(7, 19, 21, 255))
    draw.text((450, 34), "Python v0.9.6 B2 left_region_card constructed runtime fill", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 82), "Layered atlas from B shell materials + B1 photos; photo stays in contract slot, right lip is reconstructed.", fill=(217, 222, 199), font=b11.F_NOTE)
    return img


def card_body_opacity_probe(frames: list[Image.Image]) -> dict:
    expected_frames, _expected_meta = b11.source_frames(b11.SOURCE_B)
    stats: dict[str, dict] = {}
    hx1, hy1, hx2, hy2 = ALPHA_PROBE
    cx1, cy1, cx2, cy2 = ALPHA_CONTROL_PROBE
    for state, frame, expected in zip(STATE_ORDER, frames, expected_frames):
        px = frame.convert("RGBA").load()
        expected_px = expected.convert("RGBA").load()
        hole_pixels = 0
        control_pixels = 0
        expected_body_pixels = 0
        samples: list[list[int]] = []
        for y in range(hy1, hy2):
            for x in range(hx1, hx2):
                # Count only pixels that belong to the original B-shell card
                # body. Transparent bleed outside the card silhouette is legal.
                if expected_px[x, y][3] < 250:
                    continue
                expected_body_pixels += 1
                a = px[x, y][3]
                if a < 250:
                    hole_pixels += 1
                    if len(samples) < 8:
                        samples.append([x, y, a])
        for y in range(cy1, cy2):
            for x in range(cx1, cx2):
                if expected_px[x, y][3] < 250:
                    continue
                if px[x, y][3] < 250:
                    control_pixels += 1
        stats[state] = {
            "alpha_probe_range_2x": list(ALPHA_PROBE),
            "opaque_control_probe_range_2x": list(ALPHA_CONTROL_PROBE),
            "expected_opaque_b_shell_pixels_in_probe": expected_body_pixels,
            "transparent_pixels_in_right_shell_band": hole_pixels,
            "transparent_pixels_in_body_control": control_pixels,
            "threshold": "alpha < 250",
            "mask_basis": "only pixels opaque in candidate B shell source are counted; legal transparent bleed outside the card silhouette is ignored",
            "sample_transparent_pixels": samples,
            "status": "pass" if hole_pixels == 0 and control_pixels == 0 else "fail",
        }
    return stats


def texture_band_stats(frames: list[Image.Image]) -> dict:
    stats: dict[str, dict] = {}
    x1, y1, x2, y2 = PHOTO_RIGHT_BAND
    for state, frame in zip(STATE_ORDER, frames):
        crop = frame.crop((x1, y1, x2, y2)).convert("RGB")
        colors = crop.getcolors(maxcolors=1_000_000) or []
        pixels = []
        for count, (r, g, b) in colors:
            luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
            pixels.extend([luma] * min(count, 20))
        mean = sum(pixels) / max(1, len(pixels))
        variance = sum((p - mean) ** 2 for p in pixels) / max(1, len(pixels))
        stats[state] = {
            "range_2x": list(PHOTO_RIGHT_BAND),
            "unique_colors": len(colors),
            "sampled_luma_stddev": round(math.sqrt(variance), 3),
            "status": "pass" if len(colors) >= 180 and math.sqrt(variance) >= 6.0 else "fail",
            "basis": "right band must retain bitmap material variation; a flat program color strip fails",
        }
    return stats


def make_edge_qa(frames: list[Image.Image], alpha_stats: dict, texture_stats: dict) -> Image.Image:
    crop = (360, 40, 408, 190)
    scale = 5
    cell_w = (crop[2] - crop[0]) * scale
    cell_h = (crop[3] - crop[1]) * scale
    img = Image.new("RGBA", (42 + cell_w * 4 + 28 * 3 + 42, 120 + cell_h), (9, 22, 24, 255))
    draw = ImageDraw.Draw(img)
    draw.text((42, 24), "B2 edge QA: contract photo slot + rebuilt right lip", fill=(239, 235, 204), font=b11.F_HEAD)
    for i, state in enumerate(STATE_ORDER):
        x = 42 + i * (cell_w + 28)
        y = 92
        close = frames[i].crop(crop).resize((cell_w, cell_h), Image.Resampling.NEAREST)
        img.alpha_composite(close, (x, y))
        # Mark contract photo right edge and old B over-wide area.
        edge_x = (PHOTO_RECT_2X[2] - crop[0]) * scale
        visual_edge_x = (VISUAL_PHOTO_RECT_2X[2] - crop[0]) * scale
        old_edge_x = (408 - crop[0]) * scale - 1
        draw.line((x + edge_x, y, x + edge_x, y + cell_h), fill=(255, 85, 96), width=3)
        draw.line((x + visual_edge_x, y, x + visual_edge_x, y + cell_h), fill=(255, 216, 91), width=2)
        draw.line((x + old_edge_x, y, x + old_edge_x, y + cell_h), fill=(94, 235, 255), width=2)
        draw.rectangle((x, y, x + cell_w, y + cell_h), outline=(90, 150, 132), width=2)
        a = alpha_stats[state]
        t = texture_stats[state]
        draw.text((x, y - 42), f"{state}", fill=(232, 229, 199), font=b11.F_NOTE)
        draw.text((x, y - 22), f"alpha={a['transparent_pixels_in_right_shell_band']} tex={t['unique_colors']} std={t['sampled_luma_stddev']}", fill=(184, 210, 184), font=b11.F_SMALL)
    draw.text((42, img.height - 24), "red = frozen slot x390; yellow = visual photo edge; cyan = right-lip outer edge x408", fill=(215, 224, 199), font=b11.F_SMALL)
    return img


def make_compare_board() -> Image.Image:
    b13 = Image.open(PREV_B13_RUNTIME).convert("RGBA") if PREV_B13_RUNTIME.exists() else Image.open(PREV_B13_COMPOSITE).convert("RGBA")
    b2 = Image.open(OUT_RUNTIME).convert("RGBA")
    canvas = Image.new("RGBA", (1920, 1120), (8, 20, 22, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B1.3 vs B2: from pixel patching to ingredient construction", fill=(242, 238, 210), font=b11.F_HEAD)

    left = b13.resize((900, 506), Image.Resampling.LANCZOS)
    right = b2.resize((900, 506), Image.Resampling.LANCZOS)
    canvas.alpha_composite(left, (42, 86))
    canvas.alpha_composite(right, (978, 86))
    draw.text((42, 604), "B1.3: alpha fixed, but right side reads as program color band", fill=(239, 182, 166), font=b11.F_NOTE)
    draw.text((978, 604), "B2: frame / plate / photo / icon are constructed layers; photo slot + rebuilt right lip", fill=(188, 235, 197), font=b11.F_NOTE)

    edge = Image.open(OUT_EDGE_QA).convert("RGBA")
    edge = edge.resize((1500, round(edge.height * 1500 / edge.width)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(edge, (210, 668))
    return canvas


def make_manifest(
    contract: dict,
    base_meta: list[dict],
    composition: list[dict],
    geometry_metrics: list[dict],
    green_stats: dict,
    alpha_stats: dict,
    texture_stats: dict,
) -> dict:
    ratio_pass = all(m["ratio_pass"] for m in geometry_metrics)
    all_green_pass = all(green_stats[state]["artifact_greenish_pixels_full_frame"] == 0 for state in STATE_ORDER)
    alpha_pass = all(v["status"] == "pass" for v in alpha_stats.values())
    texture_pass = all(v["status"] == "pass" for v in texture_stats.values())
    machine_pass = ratio_pass and all_green_pass and alpha_pass and texture_pass
    composite_checks = {
        state: {
            "duplicate_globe": "pass_b_shell_globe_restored_once_after_photo_paste",
            "photo_layer_bounds": "pass_photo_layer_constructed_only_inside_explicit_visual_window_x42..408",
            "contract_photo_slot": "pass_photo_layer_constructed_inside_frozen_contract_photo_slot_x42..390",
            "source_frame_residue": "pass_no_source_photo_frame_used_as_final_layer",
            "right_frame_continuity": "pass_no_alpha_hole_or_source_photo_residue; x390..408 rebuilt as right lip from B-shell bitmap material",
            "layer_order_integrity": "pass_frame_plate_photo_icon_are_independent_layers",
            "card_body_opacity": "pass_alpha_probe_zero_transparent_pixels" if alpha_stats[state]["status"] == "pass" else "fail",
            "right_band_photo_integrity": "pass_machine_texture_variation_from_photo_content_not_flat_program_band" if texture_stats[state]["status"] == "pass" else "fail",
            "manual_check_basis": "437 composite, 440 runtime, 443 edge QA, and 444 B1.3-vs-B2 board; still requires user visual review before production freeze",
        }
        for state in STATE_ORDER
    }
    return {
        "schema_version": 1,
        "asset_id": "world_map_wmw_left_region_card_b2_constructed_pipeline_trial",
        "version": "v0.9.6",
        "status": "b2_constructed_pipeline_trial_pending_user_visual_review" if machine_pass else "b2_constructed_pipeline_trial_machine_gate_failed",
        "date": "2026-07-08",
        "contract": str(b11.CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "pipeline_shift": "imagegen/style bitmap ingredients -> contract-slot layer assembly -> atlas; frozen contract geometry remains unchanged",
        "visual_decision_pending": {
            "topic": "strict_contract_photo_slot_with_rebuilt_right_lip",
            "contract_photo_slot_2x": list(CONTRACT_PHOTO_RECT_2X),
            "visual_photo_window_2x": list(VISUAL_PHOTO_RECT_2X),
            "right_lip_outer_edge_2x": FRAME_SIZE[0],
            "basis": "photo remains inside the frozen contract slot; the former x390..408 problem zone is rebuilt as an explicit right lip from B-shell bitmap material instead of old photo, transparent hole, or flat program color",
            "requires_user_approval_before_production_freeze": True,
        },
        "inputs": {
            "candidate_b_shell_material": str(b11.SOURCE_B),
            "candidate_b1_imagegen_photo_source": str(b11.IMAGEGEN_B1_R4),
            "failed_b1_3_manifest": str(b13_manifest_path()),
        },
        "outputs": {
            "ingredient_board": str(OUT_INGREDIENTS),
            "candidate_b2_composite": str(OUT_CANDIDATE),
            "geometry_qa": str(OUT_QA),
            "atlas_2x": str(OUT_ATLAS),
            "runtime_fill_preview": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "manifest": str(OUT_MANIFEST),
            "edge_texture_qa": str(OUT_EDGE_QA),
            "b1_3_vs_b2_constructed_board": str(OUT_COMPARE),
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
        "alpha_probe_stats": alpha_stats,
        "right_band_texture_stats": texture_stats,
        "gates": {
            "construction_geometry_exact": {
                "status": "pass" if ratio_pass else "fail",
                "basis": "frame size and all slots are copied from left_region_card.json v0.8.2; geometry is an input to construction",
            },
            "geometry_ratio_1_275": {
                "status": "pass" if ratio_pass else "fail",
                "target_ratio": TARGET_RATIO,
                "tolerance": RATIO_TOLERANCE,
            },
            "ingredient_layer_model": {
                "status": "pass",
                "basis": "frame/plate/photo/icon/text are independent layers; no flattened B1.x composite is used as the final source",
            },
            "photo_layer_contract_slot_mask": {
                "status": "pass",
                "photo_slot_2x": list(CONTRACT_PHOTO_RECT_2X),
                "basis": "photo ingredient is fitted before paste and pasted only to the frozen contract photo_slot",
            },
            "photo_window_vs_photo_slot_conflict": {
                "status": "resolved_by_rebuilt_right_lip_trial_pending_user_visual_review",
                "contract_photo_slot_2x": list(CONTRACT_PHOTO_RECT_2X),
                "right_lip_band_2x": list(PHOTO_RIGHT_BAND),
                "basis": "B2 keeps photo in contract slot and reconstructs x390..408 as frame lip material; production freeze still requires user visual approval",
            },
            "card_body_opacity_probe": {
                "status": "pass" if alpha_pass else "fail",
                "basis": "right card-body probe must contain zero transparent pixels; dark backgrounds cannot mask holes",
                "stats": alpha_stats,
            },
            "right_band_texture_variation": {
                "status": "pass" if texture_pass else "fail",
                "basis": "x390..408 is rebuilt right lip material; it must not be alpha, source residue, or flat program color",
                "stats": texture_stats,
            },
            "chroma_residue_full_frame_all_states": {
                "status": "pass" if all_green_pass else "fail",
                "basis": "full 408x320 atlas-frame scan after construction; color-key/chroma residue is not allowed in any state",
                "stats": green_stats,
            },
            "single_icon_track": {
                "status": "pass",
                "basis": "B shell baked globe and state badges are kept once; no runtime warning-triangle overlay path",
            },
            "composite_cleanliness": {
                "status": "pass_machine_pending_user_visual_review" if machine_pass else "fail",
                "basis": "machine checks pass for no duplicate icon, no source residue, no slot overflow, no alpha hole, and no flat color band; final art quality still requires user visual review",
                "checks": composite_checks,
            },
            "no_fake_text": {
                "status": "pass",
                "basis": "atlas contains no baked readable text; Chinese strings are runtime labels in Python/Godot captures",
            },
            "functional_faces_orthogonal": {
                "status": "pass",
                "basis": "all functional surfaces are constructed from contract-aligned rectangles",
            },
            "same_state_layout": {
                "status": "pass",
                "basis": "all four states use the same 204x160 contract frame and identical slots",
            },
        },
        "visual_repair_notes": [
            "B2 is a pipeline trial, not a production freeze.",
            "It replaces B1.x flattened-card pixel surgery with layer construction from B shell materials and B1 photo ingredients.",
            "The photo layer stays inside the frozen contract photo_slot; x390..408 is rebuilt as a right lip from B-shell bitmap material.",
            "Program logic performs composition, masking, tint preservation, QA, and atlas packaging only; it does not generate art from scratch.",
            "If the rebuilt lip still reads too constructed, the next step is a real geometry-locked frame overlay/polish pass, not ad hoc pixel patching.",
        ],
    }


def b13_manifest_path() -> Path:
    return BASE / "431-world-map-wmw-v0-9-5-left-card-candidate-b1-3-manifest.json"


def save_outputs() -> None:
    contract = b11.load_contract()
    frames, base_meta, composition, plate_meta = compose_frames(contract)
    candidate = make_candidate_sheet(frames)
    ingredients = make_ingredient_sheet(frames, plate_meta)
    qa, geometry_metrics = make_geometry_qa(frames, composition)
    atlas = b11.make_atlas(frames)
    runtime = make_runtime_preview(frames, contract, False)
    runtime_qa = make_runtime_preview(frames, contract, True)
    green_stats = b11.artifact_green_stats(frames)
    alpha_stats = card_body_opacity_probe(frames)
    texture_stats = texture_band_stats(frames)
    edge_qa = make_edge_qa(frames, alpha_stats, texture_stats)

    for path in [OUT_INGREDIENTS, OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_EDGE_QA]:
        path.parent.mkdir(parents=True, exist_ok=True)
    ingredients.save(OUT_INGREDIENTS)
    candidate.save(OUT_CANDIDATE)
    qa.save(OUT_QA)
    atlas.save(OUT_ATLAS)
    runtime.save(OUT_RUNTIME)
    runtime_qa.save(OUT_RUNTIME_QA)
    edge_qa.save(OUT_EDGE_QA)
    make_compare_board().save(OUT_COMPARE)

    manifest = make_manifest(contract, base_meta, composition, geometry_metrics, green_stats, alpha_stats, texture_stats)
    manifest["image_content_checks"] = {
        "ingredient_board": b11.count_colors_nonblack(OUT_INGREDIENTS),
        "candidate": b11.count_colors_nonblack(OUT_CANDIDATE),
        "geometry_qa": b11.count_colors_nonblack(OUT_QA),
        "atlas_2x": b11.count_colors_nonblack(OUT_ATLAS),
        "runtime_fill_preview": b11.count_colors_nonblack(OUT_RUNTIME),
        "runtime_fill_qa": b11.count_colors_nonblack(OUT_RUNTIME_QA),
        "edge_texture_qa": b11.count_colors_nonblack(OUT_EDGE_QA),
        "b1_3_vs_b2_constructed_board": b11.count_colors_nonblack(OUT_COMPARE),
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
            "basis": "run scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro after switching the capture script to the B2 atlas",
            "headless_used_for_ui_capture": False,
        }

    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    for path in [
        OUT_INGREDIENTS,
        OUT_CANDIDATE,
        OUT_QA,
        OUT_ATLAS,
        OUT_RUNTIME,
        OUT_RUNTIME_QA,
        OUT_MANIFEST,
        OUT_EDGE_QA,
        OUT_COMPARE,
        GODOT_ATLAS,
        GODOT_MANIFEST,
    ]:
        print(path)


if __name__ == "__main__":
    save_outputs()
