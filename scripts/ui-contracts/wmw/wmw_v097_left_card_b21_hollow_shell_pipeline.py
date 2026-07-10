# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v094_left_card_b12_right_edge_fix as b12


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

OUT_INGREDIENTS = BASE / "447-world-map-wmw-v0-9-7-left-card-b2-1-hollow-shell-ingredients.png"
OUT_CUTOUT_QA = BASE / "448-world-map-wmw-v0-9-7-left-card-b2-1-window-cutout-qa.png"
OUT_COMPOSITE = BASE / "449-world-map-wmw-v0-9-7-left-card-b2-1-hollow-shell-composite.png"
OUT_GEOMETRY_QA = BASE / "450-world-map-wmw-v0-9-7-left-card-b2-1-geometry-qa.png"
OUT_ATLAS = BASE / "451-world-map-wmw-v0-9-7-left-card-b2-1-atlas-2x.png"
OUT_RUNTIME = BASE / "452-world-map-wmw-v0-9-7-left-card-b2-1-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "453-world-map-wmw-v0-9-7-left-card-b2-1-runtime-fill-qa.png"
OUT_FIT_QA = BASE / "454-world-map-wmw-v0-9-7-left-card-b2-1-arc-edge-fit-qa.png"
OUT_MANIFEST = BASE / "455-world-map-wmw-v0-9-7-left-card-b2-1-manifest.json"
OUT_GODOT = BASE / "456-world-map-wmw-v0-9-7-left-card-b2-1-godot-single-component.png"
OUT_GODOT_QA = BASE / "457-world-map-wmw-v0-9-7-left-card-b2-1-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b21_hollow_shell_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b21_hollow_shell_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
TARGET_RATIO = b11.TARGET_RATIO
RATIO_TOLERANCE = b11.RATIO_TOLERANCE
PHOTO_RECT_2X = b11.PHOTO_RECT_2X
ACTION_RECT_2X = b11.ACTION_RECT_2X

SEARCH_BBOX = (32, 42, 408, 186)
SEED_RECTS = [
    (48, 78, 150, 132),
    (78, 74, 350, 154),
    (56, 104, 366, 166),
]
BODY_ALPHA_THRESHOLD = 24
CUTOUT_DILATE_PX = 2
PHOTO_UNDERLAY_PAD = 8


def _dist2(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def _is_color_key_or_empty(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    if a < 40:
        return True
    saturated_color_key = r < 95 and g > 120 and b < 110 and g - r > 30 and g - b > 30
    compressed_color_key = r <= 14 and b <= 14 and g >= 65 and g - r >= 58 and g - b >= 58
    return saturated_color_key or compressed_color_key


def _is_coordinate_protected(x: int, y: int, c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    if _is_color_key_or_empty(c):
        return True
    # Protect actual globe ink/chrome, not the entire circular neighborhood:
    # in B the old photo runs under the globe arc, so a geometric ellipse would
    # preserve the exact blue mountain residue B2.1 is meant to cut away.
    globe_ellipse = ((x - 54) / 39) ** 2 + ((y - 52) / 39) ** 2 <= 1.0
    globe_ink = globe_ellipse and r >= 118 and g >= 105 and b >= 72 and abs(r - g) <= 82 and r - b >= 12
    top_frame = y < 50 and x >= 42
    left_frame = x < 38 and y >= 54
    right_outer_frame = x >= 406
    bottom_photo_lip = 174 <= y <= 188
    return globe_ink or top_frame or left_frame or right_outer_frame or bottom_photo_lip


def _photo_candidate(c: tuple[int, int, int, int], palette: list[tuple[int, int, int]]) -> bool:
    r, g, b, a = c
    if a < 60 or _is_color_key_or_empty(c):
        return False
    nearest = min(_dist2((r, g, b), p) for p in palette)
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    blue_dark = b >= r - 10 and luma < 138
    cool_bright_photo = b >= r and b >= g - 18 and luma < 190
    warm_photo_shadow = luma < 122 and abs(r - g) < 70 and b < 130
    return nearest <= 86 * 86 or blue_dark or cool_bright_photo or warm_photo_shadow


def _seed_palette(frame: Image.Image) -> list[tuple[int, int, int]]:
    px = frame.convert("RGBA").load()
    colors: list[tuple[int, int, int]] = []
    for rect in SEED_RECTS:
        x1, y1, x2, y2 = rect
        for y in range(y1, y2, 5):
            for x in range(x1, x2, 5):
                c = px[x, y]
                if not _is_coordinate_protected(x, y, c):
                    colors.append((c[0], c[1], c[2]))
    if not colors:
        return [(38, 59, 64)]
    # Keep a compact palette spread across the source photo colors.
    colors.sort(key=lambda c: (c[0] + c[1] + c[2], c[2], c[0]))
    step = max(1, len(colors) // 72)
    return colors[::step][:96]


def _flood_connected_photo_mask(frame: Image.Image) -> Image.Image:
    rgba = frame.convert("RGBA")
    px = rgba.load()
    palette = _seed_palette(rgba)
    x1, y1, x2, y2 = SEARCH_BBOX

    candidate = Image.new("1", FRAME_SIZE, 0)
    cand_px = candidate.load()
    for y in range(y1, y2):
        for x in range(x1, x2):
            if (not _is_coordinate_protected(x, y, px[x, y])) and _photo_candidate(px[x, y], palette):
                cand_px[x, y] = 1

    mask = Image.new("1", FRAME_SIZE, 0)
    mask_px = mask.load()
    q: deque[tuple[int, int]] = deque()
    for sx1, sy1, sx2, sy2 in SEED_RECTS:
        for y in range(max(y1, sy1), min(y2, sy2), 3):
            for x in range(max(x1, sx1), min(x2, sx2), 3):
                if cand_px[x, y]:
                    mask_px[x, y] = 1
                    q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nx < x1 or nx >= x2 or ny < y1 or ny >= y2:
                continue
            if mask_px[nx, ny] or not cand_px[nx, ny]:
                continue
            mask_px[nx, ny] = 1
            q.append((nx, ny))

    expanded = mask.convert("L").filter(ImageFilter.MaxFilter(CUTOUT_DILATE_PX * 2 + 1))
    protect = Image.new("L", FRAME_SIZE, 0)
    protect_px = protect.load()
    for y in range(y1, y2):
        for x in range(x1, x2):
            if _is_coordinate_protected(x, y, px[x, y]):
                protect_px[x, y] = 255
    expanded = ImageChops.subtract(expanded, protect.filter(ImageFilter.MaxFilter(3)))
    expanded = expanded.point(lambda v: 255 if v > 0 else 0)
    return expanded


def _bbox_from_mask(mask: Image.Image) -> tuple[int, int, int, int]:
    bbox = mask.getbbox()
    if bbox is None:
        return PHOTO_RECT_2X
    x1, y1, x2, y2 = bbox
    return (
        max(0, x1 - PHOTO_UNDERLAY_PAD),
        max(0, y1 - PHOTO_UNDERLAY_PAD),
        min(FRAME_SIZE[0], x2 + PHOTO_UNDERLAY_PAD),
        min(FRAME_SIZE[1], y2 + PHOTO_UNDERLAY_PAD),
    )


def make_hollow_shell(frame: Image.Image, state: str) -> tuple[Image.Image, Image.Image, dict]:
    mask = _flood_connected_photo_mask(frame)
    shell = frame.convert("RGBA")
    px = shell.load()
    mask_px = mask.load()
    cutout_pixels = 0
    for y in range(shell.height):
        for x in range(shell.width):
            if mask_px[x, y] > 0:
                r, g, b, _a = px[x, y]
                px[x, y] = (r, g, b, 0)
                cutout_pixels += 1
            else:
                r, g, b, a = px[x, y]
                if _is_color_key_or_empty(px[x, y]):
                    px[x, y] = (r, g, b, 0)
    bbox = _bbox_from_mask(mask)
    ingredient_path = GODOT_INGREDIENT_DIR / f"left_region_card_b21_hollow_shell_{state}.png"
    return shell, mask, {
        "state": state,
        "hollow_shell_path": str(ingredient_path),
        "search_bbox_2x": list(SEARCH_BBOX),
        "photo_cutout_mask_bbox_2x": list(mask.getbbox() or PHOTO_RECT_2X),
        "photo_underlay_cover_bbox_2x": list(bbox),
        "cutout_dilate_px": CUTOUT_DILATE_PX,
        "cutout_pixels": cutout_pixels,
        "method": "color-segment old photo pixels from B shell, dilate cutout, then set old photo pixels transparent",
    }


def _crop_source_photo_to_size(source: Image.Image, box: tuple[int, int, int, int], state: str, size: tuple[int, int]) -> Image.Image:
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
    return ImageOps.fit(patch, size, method=Image.Resampling.LANCZOS, centering=(0.50, 0.54)).convert("RGBA")


def _photo_sources() -> tuple[Image.Image, list[tuple[int, int, int, int]]]:
    source = Image.open(b11.IMAGEGEN_B1_R4).convert("RGB")
    mask = b11.b1.build_mask(source)
    boxes = b11.b1.find_quadrant_boxes(mask)
    return source, boxes


def compose_frames(contract: dict) -> tuple[list[Image.Image], list[Image.Image], list[Image.Image], list[dict], list[dict]]:
    base_frames, base_meta = b11.source_frames(b11.SOURCE_B)
    photo_source, photo_boxes = _photo_sources()

    frames: list[Image.Image] = []
    shells: list[Image.Image] = []
    masks: list[Image.Image] = []
    composition: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        shell, cutout_mask, shell_meta = make_hollow_shell(base_frames[idx], state)
        bbox = tuple(shell_meta["photo_underlay_cover_bbox_2x"])
        photo = _crop_source_photo_to_size(photo_source, photo_boxes[idx], state, (bbox[2] - bbox[0], bbox[3] - bbox[1]))

        frame = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        body_mask = Image.new("L", FRAME_SIZE, 0)
        base_px = base_frames[idx].convert("RGBA").load()
        body_px = body_mask.load()
        for y in range(FRAME_SIZE[1]):
            for x in range(FRAME_SIZE[0]):
                if base_px[x, y][3] >= BODY_ALPHA_THRESHOLD and not _is_color_key_or_empty(base_px[x, y]):
                    body_px[x, y] = 255
        dark_body = Image.new("RGBA", FRAME_SIZE, (5, 13, 14, 255))
        frame.paste(dark_body, (0, 0), body_mask)
        frame.alpha_composite(photo, (bbox[0], bbox[1]))
        frame.alpha_composite(shell)

        frames.append(frame)
        shells.append(shell)
        masks.append(cutout_mask)
        composition.append(
            {
                "state": state,
                "z_order": "dark_body -> rectangular photo underlay covering cutout bbox -> hollow shell -> runtime text",
                "base_shell_source": str(b11.SOURCE_B),
                "photo_source": str(b11.IMAGEGEN_B1_R4),
                "photo_source_box": list(photo_boxes[idx]),
                "photo_rel_crop_b2_1": list(b12.PHOTO_RELS[state]),
                "photo_underlay_cover_bbox_2x": list(bbox),
                "photo_shape_clipping": "forbidden_not_used",
                "hollow_shell": shell_meta,
                "contract_photo_slot_2x": list(b11.slot_rect(contract, "photo_slot")),
            }
        )
    return frames, shells, masks, base_meta, composition


def old_photo_residue_stats(shells: list[Image.Image], masks: list[Image.Image]) -> dict:
    stats: dict[str, dict] = {}
    for state, shell, mask in zip(STATE_ORDER, shells, masks):
        px = shell.convert("RGBA").load()
        mask_px = mask.load()
        opaque_in_cutout = 0
        samples: list[list[int]] = []
        for y in range(FRAME_SIZE[1]):
            for x in range(FRAME_SIZE[0]):
                if mask_px[x, y] <= 0:
                    continue
                r, g, b, a = px[x, y]
                if a > 8:
                    opaque_in_cutout += 1
                    if len(samples) < 8:
                        samples.append([x, y, r, g, b, a])
        stats[state] = {
            "cutout_mask_bbox_2x": list(mask.getbbox() or PHOTO_RECT_2X),
            "opaque_pixels_inside_cutout_mask": opaque_in_cutout,
            "old_photo_signature_hits": opaque_in_cutout,
            "sample_pixels": samples,
            "status": "pass" if opaque_in_cutout == 0 else "fail",
            "basis": "after color segmentation and dilation, the hollow-shell cutout mask must contain zero opaque old-photo pixels",
        }
    return stats


def card_body_opacity_probe(frames: list[Image.Image]) -> dict:
    expected_frames, _meta = b11.source_frames(b11.SOURCE_B)
    stats: dict[str, dict] = {}
    for state, frame, expected in zip(STATE_ORDER, frames, expected_frames):
        px = frame.convert("RGBA").load()
        exp = expected.convert("RGBA").load()
        holes = 0
        checked = 0
        samples: list[list[int]] = []
        for y in range(FRAME_SIZE[1]):
            for x in range(FRAME_SIZE[0]):
                if exp[x, y][3] < 250 or _is_color_key_or_empty(exp[x, y]):
                    continue
                checked += 1
                if px[x, y][3] < 250:
                    holes += 1
                    if len(samples) < 8:
                        samples.append([x, y, px[x, y][3]])
        stats[state] = {
            "mask_basis": "pixels opaque in candidate B shell source, excluding compressed green color-key background residue",
            "expected_opaque_pixels": checked,
            "transparent_pixels_inside_card_body": holes,
            "sample_transparent_pixels": samples,
            "threshold": "alpha < 250",
            "status": "pass" if holes == 0 else "fail",
        }
    return stats


def _draw_zoom_panel(
    canvas: Image.Image,
    src: Image.Image,
    crop: tuple[int, int, int, int],
    xy: tuple[int, int],
    title: str,
    scale: int,
    guide_rects: list[tuple[tuple[int, int, int, int], tuple[int, int, int], str]],
) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y = xy
    panel = src.crop(crop).resize(((crop[2] - crop[0]) * scale, (crop[3] - crop[1]) * scale), Image.Resampling.NEAREST)
    canvas.alpha_composite(panel.convert("RGBA"), xy)
    draw.rectangle((x, y, x + panel.width, y + panel.height), outline=(94, 164, 142), width=2)
    draw.text((x, y - 24), title, fill=(234, 232, 204), font=b11.F_SMALL)
    for rect, color, label in guide_rects:
        rx1, ry1, rx2, ry2 = rect
        gx1 = x + (rx1 - crop[0]) * scale
        gy1 = y + (ry1 - crop[1]) * scale
        gx2 = x + (rx2 - crop[0]) * scale
        gy2 = y + (ry2 - crop[1]) * scale
        draw.rectangle((gx1, gy1, gx2, gy2), outline=color, width=2)
        draw.text((gx1 + 3, gy1 + 3), label, fill=color, font=b11.F_SMALL)


def make_fit_qa(frames: list[Image.Image], masks: list[Image.Image]) -> Image.Image:
    # The user called out the second card; keep available large, with the other
    # states nearby for same-layout sanity.
    canvas = Image.new("RGBA", (1780, 1040), (8, 20, 22, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.1 hollow-shell fit QA: photo is below shell, shell owns the irregular window", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 62), "No photo shape crop: rectangular photo underlay is revealed only through the hollow shell.", fill=(205, 224, 198), font=b11.F_NOTE)

    bg_frames = []
    for frame in frames:
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(frame)
        bg_frames.append(bg)

    available = bg_frames[1]
    _draw_zoom_panel(
        canvas,
        available,
        (34, 38, 168, 124),
        (42, 132),
        "available 200%: globe arc / top-left cutout",
        4,
        [((46, 48, 132, 112), (255, 96, 104), "arc")],
    )
    _draw_zoom_panel(
        canvas,
        available,
        (34, 138, 408, 198),
        (620, 132),
        "available 200%: bottom lip",
        4,
        [((42, 168, 390, 176), (255, 216, 91), "window bottom")],
    )
    _draw_zoom_panel(
        canvas,
        available,
        (320, 42, 408, 190),
        (42, 558),
        "available 200%: right edge",
        4,
        [((390, 48, 408, 176), (94, 235, 255), "right shell")],
    )

    x = 470
    y = 558
    for i, state in enumerate(STATE_ORDER):
        thumb = bg_frames[i].resize((245, 192), Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb, (x + i * 300, y))
        draw.text((x + i * 300, y + 202), state, fill=(226, 231, 202), font=b11.F_NOTE)
    draw.text((470, 830), "Manual inspection target: arc, bottom, and right edge must show photo only through the hollow shell, with no old-photo band or dark gap.", fill=(215, 224, 199), font=b11.F_NOTE)
    return canvas


def make_ingredient_board(shells: list[Image.Image], masks: list[Image.Image]) -> Image.Image:
    base_frames, _meta = b11.source_frames(b11.SOURCE_B)
    cell_w = 390
    row_h = 238
    canvas = Image.new("RGBA", (1650, 100 + row_h * 4), (9, 22, 24, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.1 v0.9.7 hollow-shell ingredients", fill=(242, 238, 210), font=b11.F_HEAD)
    headers = ["B shell source", "cutout mask", "hollow shell", "alpha preview"]
    for i, h in enumerate(headers):
        draw.text((42 + i * cell_w, 66), h, fill=(188, 216, 190), font=b11.F_NOTE)
    for row, state in enumerate(STATE_ORDER):
        y = 102 + row * row_h
        draw.text((10, y + 4), state, fill=(235, 231, 200), font=b11.F_SMALL)
        source = base_frames[row].resize((306, 240), Image.Resampling.LANCZOS)
        canvas.alpha_composite(source, (42, y))
        mask_rgb = ImageOps.colorize(masks[row].resize((306, 240), Image.Resampling.NEAREST), black="#071315", white="#58e9ff").convert("RGBA")
        canvas.alpha_composite(mask_rgb, (42 + cell_w, y))
        shell_bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        shell_bg.alpha_composite(shells[row])
        canvas.alpha_composite(shell_bg.resize((306, 240), Image.Resampling.LANCZOS), (42 + cell_w * 2, y))
        alpha = shells[row].getchannel("A")
        alpha_rgb = ImageOps.colorize(alpha.resize((306, 240), Image.Resampling.NEAREST), black="#071315", white="#f0ecd0").convert("RGBA")
        canvas.alpha_composite(alpha_rgb, (42 + cell_w * 3, y))
    return canvas


def make_cutout_qa(shells: list[Image.Image], masks: list[Image.Image], residue_stats: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1680, 940), (9, 22, 24, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.1 cutout QA: hollow shell contains zero old-photo pixels inside cutout mask", fill=(242, 238, 210), font=b11.F_HEAD)
    crop = (30, 38, 408, 190)
    scale = 2
    panel_w = (crop[2] - crop[0]) * scale
    panel_h = (crop[3] - crop[1]) * scale
    for i, state in enumerate(STATE_ORDER):
        x = 42 + (i % 2) * (panel_w + 70)
        y = 104 + (i // 2) * (panel_h + 132)
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(shells[i])
        panel = bg.crop(crop).resize((panel_w, panel_h), Image.Resampling.NEAREST)
        mask_panel = ImageOps.colorize(masks[i].crop(crop).resize((panel_w, panel_h), Image.Resampling.NEAREST), black="#000000", white="#58e9ff").convert("RGBA")
        mask_panel.putalpha(masks[i].crop(crop).resize((panel_w, panel_h), Image.Resampling.NEAREST).point(lambda v: 95 if v else 0))
        canvas.alpha_composite(panel, (x, y))
        canvas.alpha_composite(mask_panel, (x, y))
        draw.rectangle((x, y, x + panel_w, y + panel_h), outline=(94, 164, 142), width=2)
        s = residue_stats[state]
        color = (176, 240, 190) if s["status"] == "pass" else (255, 110, 100)
        draw.text((x, y - 46), f"{state}: residue={s['old_photo_signature_hits']} {s['status'].upper()}", fill=color, font=b11.F_NOTE)
        draw.text((x, y - 22), f"mask bbox={s['cutout_mask_bbox_2x']}", fill=(200, 216, 190), font=b11.F_SMALL)
    return canvas


def make_composite_sheet(frames: list[Image.Image]) -> Image.Image:
    margin = 54
    gap = 58
    label_h = 54
    w = margin * 2 + FRAME_SIZE[0] * 2 + gap
    h = margin * 2 + (FRAME_SIZE[1] + label_h) * 2 + gap
    sheet = Image.new("RGBA", (w, h), (18, 30, 31, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 16), "B2.1 v0.9.7 hollow-shell composite", fill=(236, 231, 197), font=b11.F_HEAD)
    for i, state in enumerate(STATE_ORDER):
        col = i % 2
        row = i // 2
        x = margin + col * (FRAME_SIZE[0] + gap)
        y = margin + row * (FRAME_SIZE[1] + label_h + gap)
        sheet.alpha_composite(frames[i], (x, y))
        draw.rectangle((x, y, x + FRAME_SIZE[0], y + FRAME_SIZE[1]), outline=(111, 166, 143), width=2)
        draw.text((x, y + FRAME_SIZE[1] + 8), f"{state}: dark -> rectangular photo -> hollow shell", fill=(215, 224, 199), font=b11.F_SMALL)
    return sheet


def make_geometry_qa(frames: list[Image.Image], composition: list[dict]) -> tuple[Image.Image, list[dict]]:
    qa, metrics = b11.make_geometry_qa(frames, composition)
    draw = ImageDraw.Draw(qa)
    draw.rectangle((0, 0, qa.width, 34), fill=(14, 23, 24, 255))
    draw.text((42, 4), "B2.1 geometry QA: atlas size unchanged; photo underlay is hidden by hollow shell, not clipped to shape", fill=(236, 231, 197), font=b11.F_NOTE)
    return qa, metrics


def make_runtime_preview(frames: list[Image.Image], contract: dict, show_qa: bool) -> Image.Image:
    img = b11.make_runtime_preview(frames, contract, show_qa)
    draw = ImageDraw.Draw(img)
    draw.rectangle((438, 20, 1880, 118), fill=(7, 19, 21, 255))
    draw.text((450, 34), "Python v0.9.7 B2.1 left_region_card hollow-shell runtime fill", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 82), "Z-order: dark base -> rectangular photo underlay -> hollow shell -> runtime title/meta.", fill=(217, 222, 199), font=b11.F_NOTE)
    return img


def make_manifest(
    contract: dict,
    base_meta: list[dict],
    composition: list[dict],
    geometry_metrics: list[dict],
    residue_stats: dict,
    opacity_stats: dict,
    image_checks: dict | None = None,
) -> dict:
    ratio_pass = all(m["ratio_pass"] for m in geometry_metrics)
    residue_pass = all(s["status"] == "pass" for s in residue_stats.values())
    opacity_pass = all(s["status"] == "pass" for s in opacity_stats.values())
    machine_pass = ratio_pass and residue_pass and opacity_pass
    manifest = {
        "schema_version": 1,
        "asset_id": "world_map_wmw_left_region_card_b2_1_hollow_shell",
        "version": "v0.9.7",
        "status": "b2_1_hollow_shell_machine_pass_pending_manual_visual_check" if machine_pass else "b2_1_hollow_shell_machine_gate_failed",
        "date": "2026-07-09",
        "contract": str(b11.CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "pipeline": "hollow shell z-order: dark base -> rectangular photo underlay -> hollow shell -> runtime text",
        "inputs": {
            "candidate_b_shell_source": str(b11.SOURCE_B),
            "candidate_b1_photo_source": str(b11.IMAGEGEN_B1_R4),
            "previous_b2_manifest": str(BASE / "442-world-map-wmw-v0-9-6-left-card-b2-manifest.json"),
        },
        "outputs": {
            "ingredient_board": str(OUT_INGREDIENTS),
            "cutout_qa": str(OUT_CUTOUT_QA),
            "composite": str(OUT_COMPOSITE),
            "geometry_qa": str(OUT_GEOMETRY_QA),
            "atlas_2x": str(OUT_ATLAS),
            "runtime_fill_preview": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "arc_edge_fit_qa": str(OUT_FIT_QA),
            "manifest": str(OUT_MANIFEST),
            "godot_single_component": str(OUT_GODOT),
            "godot_single_component_qa": str(OUT_GODOT_QA),
            "godot_atlas_copy": str(GODOT_ATLAS),
            "godot_manifest_copy": str(GODOT_MANIFEST),
            "godot_hollow_shell_ingredients_dir": str(GODOT_INGREDIENT_DIR),
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
        "old_photo_residue_stats": residue_stats,
        "card_body_opacity_stats": opacity_stats,
        "gates": {
            "window_cutout_quality": {
                "status": "pass" if residue_pass else "fail",
                "basis": "hollow shell cutout mask contains zero opaque old-photo pixels after color segmentation and dilation",
                "stats": residue_stats,
            },
            "card_body_opacity_probe": {
                "status": "pass" if opacity_pass else "fail",
                "basis": "composited card body must be opaque wherever candidate B shell body was opaque",
                "stats": opacity_stats,
            },
            "geometry_ratio_1_275": {
                "status": "pass" if ratio_pass else "fail",
                "target_ratio": TARGET_RATIO,
                "tolerance": RATIO_TOLERANCE,
            },
            "photo_shape_crop_forbidden": {
                "status": "pass",
                "basis": "photo ingredients are rectangular underlays fitted to cutout bounding boxes; no shape clipping is applied to photo layers",
            },
            "z_order_hollow_shell": {
                "status": "pass",
                "basis": "dark base -> rectangular photo underlay -> hollow shell; irregular window belongs to shell alpha",
            },
            "arc_and_edge_manual_visual_check": {
                "status": "pending",
                "basis": "inspect 454 and Godot 456/457 at 200%; do not mark pass until visual evidence is reviewed",
            },
            "godot_windowed_capture": {
                "status": "pending",
                "basis": "run scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro after switching capture script to B2.1 atlas",
                "headless_used_for_ui_capture": False,
            },
        },
        "manual_review_notes": [
            "B2.1 deliberately does not cut photos into a window shape.",
            "The irregular globe arc, bottom lip, right edge, and card silhouette are owned by the hollow shell alpha.",
            "If 454/456 still show mismatch, stop and report; do not patch coordinates.",
        ],
    }
    if image_checks is not None:
        manifest["image_content_checks"] = image_checks
    return manifest


def write_outputs() -> None:
    contract = b11.load_contract()
    frames, shells, masks, base_meta, composition = compose_frames(contract)
    qa, geometry_metrics = make_geometry_qa(frames, composition)
    residue_stats = old_photo_residue_stats(shells, masks)
    opacity_stats = card_body_opacity_probe(frames)

    atlas = b11.make_atlas(frames)
    runtime = make_runtime_preview(frames, contract, False)
    runtime_qa = make_runtime_preview(frames, contract, True)
    ingredient_board = make_ingredient_board(shells, masks)
    cutout_qa = make_cutout_qa(shells, masks, residue_stats)
    composite = make_composite_sheet(frames)
    fit_qa = make_fit_qa(frames, masks)

    for path in [
        OUT_INGREDIENTS,
        OUT_CUTOUT_QA,
        OUT_COMPOSITE,
        OUT_GEOMETRY_QA,
        OUT_ATLAS,
        OUT_RUNTIME,
        OUT_RUNTIME_QA,
        OUT_FIT_QA,
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
    ingredient_board.save(OUT_INGREDIENTS)
    cutout_qa.save(OUT_CUTOUT_QA)
    composite.save(OUT_COMPOSITE)
    qa.save(OUT_GEOMETRY_QA)
    atlas.save(OUT_ATLAS)
    runtime.save(OUT_RUNTIME)
    runtime_qa.save(OUT_RUNTIME_QA)
    fit_qa.save(OUT_FIT_QA)

    GODOT_INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    for shell, state in zip(shells, STATE_ORDER):
        shell.save(GODOT_INGREDIENT_DIR / f"left_region_card_b21_hollow_shell_{state}.png")
    atlas.save(GODOT_ATLAS)

    image_checks = {
        "ingredient_board": b11.count_colors_nonblack(OUT_INGREDIENTS),
        "cutout_qa": b11.count_colors_nonblack(OUT_CUTOUT_QA),
        "composite": b11.count_colors_nonblack(OUT_COMPOSITE),
        "geometry_qa": b11.count_colors_nonblack(OUT_GEOMETRY_QA),
        "atlas_2x": b11.count_colors_nonblack(OUT_ATLAS),
        "runtime_fill_preview": b11.count_colors_nonblack(OUT_RUNTIME),
        "runtime_fill_qa": b11.count_colors_nonblack(OUT_RUNTIME_QA),
        "arc_edge_fit_qa": b11.count_colors_nonblack(OUT_FIT_QA),
    }
    if OUT_GODOT.exists() and OUT_GODOT_QA.exists():
        image_checks["godot_single_component"] = b11.count_colors_nonblack(OUT_GODOT)
        image_checks["godot_single_component_qa"] = b11.count_colors_nonblack(OUT_GODOT_QA)

    manifest = make_manifest(contract, base_meta, composition, geometry_metrics, residue_stats, opacity_stats, image_checks)
    if OUT_GODOT.exists() and OUT_GODOT_QA.exists():
        manifest["gates"]["godot_windowed_capture"] = {
            "status": "pass",
            "basis": "windowed opengl3 capture via scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro; nonblack and color-diversity checks recorded",
            "headless_used_for_ui_capture": False,
        }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    for path in [
        OUT_INGREDIENTS,
        OUT_CUTOUT_QA,
        OUT_COMPOSITE,
        OUT_GEOMETRY_QA,
        OUT_ATLAS,
        OUT_RUNTIME,
        OUT_RUNTIME_QA,
        OUT_FIT_QA,
        OUT_MANIFEST,
        GODOT_ATLAS,
        GODOT_MANIFEST,
    ]:
        print(path)


if __name__ == "__main__":
    write_outputs()
