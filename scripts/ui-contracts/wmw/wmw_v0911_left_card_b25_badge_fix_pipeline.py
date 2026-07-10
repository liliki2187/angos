# -*- coding: utf-8 -*-
from __future__ import annotations

import colorsys
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v098_left_card_b22_hollow_shell_geometry_pipeline as b22


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.11"
ROUND_ID = "B2.5"
ASSET_ID = "world_map_wmw_left_region_card_b2_5_badge_fix"

B_ATLAS = b22.B_ATLAS
B13_ATLAS = b22.B13_ATLAS

OUT_COMPARE = BASE / "479-world-map-wmw-v0-9-11-left-card-b2-5-badge-fix-compare.png"
OUT_INGREDIENTS = BASE / "480-world-map-wmw-v0-9-11-left-card-b2-5-ingredients.png"
OUT_ATLAS = BASE / "481-world-map-wmw-v0-9-11-left-card-b2-5-atlas-2x.png"
OUT_GEOMETRY_QA = BASE / "482-world-map-wmw-v0-9-11-left-card-b2-5-geometry-qa.png"
OUT_RUNTIME = BASE / "483-world-map-wmw-v0-9-11-left-card-b2-5-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "484-world-map-wmw-v0-9-11-left-card-b2-5-runtime-fill-qa.png"
OUT_FIT_QA = BASE / "485-world-map-wmw-v0-9-11-left-card-b2-5-16point-visual-qa.png"
OUT_MANIFEST = BASE / "486-world-map-wmw-v0-9-11-left-card-b2-5-manifest.json"
OUT_GODOT = BASE / "487-world-map-wmw-v0-9-11-left-card-b2-5-godot-single-component.png"
OUT_GODOT_QA = BASE / "488-world-map-wmw-v0-9-11-left-card-b2-5-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b25_badge_fix_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b25_badge_fix_manifest.json"

STATE_ORDER = b11.STATE_ORDER
FRAME_SIZE = b11.FRAME_SIZE
EXPORT_SIZE = b11.EXPORT_SIZE
TARGET_RATIO = b11.TARGET_RATIO
RATIO_TOLERANCE = b11.RATIO_TOLERANCE
PHOTO_RECT_2X = b11.PHOTO_RECT_2X
ACTION_RECT_2X = b11.ACTION_RECT_2X
MASTER_STATE = "available"
MASTER_INDEX = STATE_ORDER.index(MASTER_STATE)
EDGE_SCAN_MAX_EXPAND_PX = 8
BADGE_GLYPH_RADIUS = 27.0
BADGE_GLYPH_CLEAR_EXPAND = 3
BADGE_HUE_TOLERANCE = 0.08
BADGE_LOW_SATURATION = 0.12
BADGE_LIGHTNESS_TOLERANCE = 0.18


def _is_creamish(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    return a > 180 and r > 145 and g > 120 and b > 85 and r > b + 18


def _is_action_rect(x: int, y: int) -> bool:
    x1, y1, x2, y2 = ACTION_RECT_2X
    return x1 <= x < x2 and y1 <= y < y2


def _is_badge_core_pixel(c: tuple[int, int, int, int], x: int, y: int) -> bool:
    if not _is_action_rect(x, y):
        return False
    r, g, b, a = c
    if a < 120:
        return False
    if _is_creamish(c) or b22.is_green_signature(c):
        return False
    return True


def _is_globe_area(x: int, y: int) -> bool:
    return x < 105 and y < 105


def _is_old_photo_signature(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    if a <= 180 or _is_creamish(c):
        return False
    return b > g + 8 and b > 40


def _is_globe_antialias(c: tuple[int, int, int, int]) -> bool:
    r, g, b, a = c
    return a > 120 and r > 110 and g > 90 and b > 65 and r > b + 14


def _badge_center() -> tuple[float, float]:
    x1, y1, x2, y2 = ACTION_RECT_2X
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def _inside_badge_glyph_zone(x: int, y: int) -> bool:
    cx, cy = _badge_center()
    return (x - cx) * (x - cx) + (y - cy) * (y - cy) <= BADGE_GLYPH_RADIUS * BADGE_GLYPH_RADIUS


def badge_cream_components(img: Image.Image) -> list[dict]:
    px = img.convert("RGBA").load()
    x1, y1, x2, y2 = ACTION_RECT_2X
    remaining: set[tuple[int, int]] = set()
    for y in range(y1, y2):
        for x in range(x1, x2):
            if _is_creamish(px[x, y]):
                remaining.add((x, y))
    comps: list[dict] = []
    while remaining:
        start = remaining.pop()
        queue = [start]
        pixels = [start]
        for qx, qy in queue:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nb = (qx + dx, qy + dy)
                    if nb in remaining:
                        remaining.remove(nb)
                        queue.append(nb)
                        pixels.append(nb)
        xs = [x for x, _y in pixels]
        ys = [y for _x, y in pixels]
        comps.append(
            {
                "pixels": pixels,
                "bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
                "centroid": (sum(xs) / len(xs), sum(ys) / len(ys)),
                "count": len(pixels),
            }
        )
    comps.sort(key=lambda item: item["count"], reverse=True)
    return comps


def is_badge_outer_ring_component(comp: dict) -> bool:
    _x1, y1, x2, y2 = ACTION_RECT_2X
    bx1, by1, bx2, by2 = comp["bbox"]
    cx, _cy = comp["centroid"]
    badge_cx, _badge_cy = _badge_center()
    return bx2 >= x2 - 18 and by2 >= y2 - 2 and by1 <= y1 + 6 and cx >= badge_cx + 4


def badge_glyph_pixels(img: Image.Image) -> set[tuple[int, int]]:
    pixels: set[tuple[int, int]] = set()
    for comp in badge_cream_components(img):
        if not is_badge_outer_ring_component(comp):
            pixels.update(comp["pixels"])
    return pixels


def badge_outer_ring_pixels(img: Image.Image) -> set[tuple[int, int]]:
    pixels: set[tuple[int, int]] = set()
    for comp in badge_cream_components(img):
        if is_badge_outer_ring_component(comp):
            pixels.update(comp["pixels"])
    return pixels


def badge_glyph_clear_pixels(img: Image.Image) -> set[tuple[int, int]]:
    x1, y1, x2, y2 = ACTION_RECT_2X
    glyph = badge_glyph_pixels(img)
    outer = badge_outer_ring_pixels(img)
    clear: set[tuple[int, int]] = set()
    for gx, gy in glyph:
        for dy in range(-BADGE_GLYPH_CLEAR_EXPAND, BADGE_GLYPH_CLEAR_EXPAND + 1):
            for dx in range(-BADGE_GLYPH_CLEAR_EXPAND, BADGE_GLYPH_CLEAR_EXPAND + 1):
                if dx * dx + dy * dy > BADGE_GLYPH_CLEAR_EXPAND * BADGE_GLYPH_CLEAR_EXPAND:
                    continue
                x = gx + dx
                y = gy + dy
                if x1 <= x < x2 and y1 <= y < y2 and (x, y) not in outer:
                    clear.add((x, y))
    return clear


def _frame_family_mask_pixel(c: tuple[int, int, int, int], x: int, y: int) -> bool:
    r, g, b, a = c
    if a < 80:
        return False
    if _is_action_rect(x, y):
        return _is_badge_core_pixel(c, x, y)
    if _is_creamish(c):
        return False
    if _is_globe_area(x, y) and (r > 110 and g > 95 and b > 70):
        return False
    # The available master frame family is teal/cyan or dark teal. B2.5
    # deliberately includes badge core pixels so state hue mapping owns them.
    return g >= r + 8 and b >= r + 6 and g >= 42


def _average_hls(img: Image.Image, mask: Image.Image | None = None) -> tuple[float, float, float]:
    px = img.convert("RGBA").load()
    mp = mask.load() if mask is not None else None
    hs: list[float] = []
    ls: list[float] = []
    ss: list[float] = []
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if mp is not None and mp[x, y] == 0:
                continue
            r, g, b, a = px[x, y]
            if a < 120:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            hs.append(h)
            ls.append(l)
            ss.append(s)
    if not hs:
        return (0.5, 0.45, 0.35)
    # Hue is circular. For this narrow range, a direct mean is stable enough.
    return (sum(hs) / len(hs), sum(ls) / len(ls), sum(ss) / len(ss))


def _hue_delta(a: float, b: float) -> float:
    diff = abs(a - b)
    return min(diff, 1.0 - diff)


def _hls_summary_from_rgba(samples: list[tuple[int, int, int, int]]) -> dict:
    if not samples:
        return {
            "count": 0,
            "hue": None,
            "hue_degrees": None,
            "lightness": None,
            "saturation": None,
            "avg_rgb": None,
        }
    sin_sum = 0.0
    cos_sum = 0.0
    lightness: list[float] = []
    saturation: list[float] = []
    rs: list[int] = []
    gs: list[int] = []
    bs: list[int] = []
    for r, g, b, _a in samples:
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        sin_sum += math.sin(h * math.tau)
        cos_sum += math.cos(h * math.tau)
        lightness.append(l)
        saturation.append(s)
        rs.append(r)
        gs.append(g)
        bs.append(b)
    hue = (math.atan2(sin_sum, cos_sum) / math.tau) % 1.0
    return {
        "count": len(samples),
        "hue": round(hue, 4),
        "hue_degrees": round(hue * 360.0, 1),
        "lightness": round(sum(lightness) / len(lightness), 4),
        "saturation": round(sum(saturation) / len(saturation), 4),
        "avg_rgb": [
            round(sum(rs) / len(rs), 1),
            round(sum(gs) / len(gs), 1),
            round(sum(bs) / len(bs), 1),
        ],
    }


def gate_badge_state_color_consistency(frame: Image.Image, family_mask: Image.Image, state: str, glyph_metrics: dict) -> dict:
    px = frame.convert("RGBA").load()
    mp = family_mask.load()
    frame_samples: list[tuple[int, int, int, int]] = []
    badge_samples: list[tuple[int, int, int, int]] = []
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            c = px[x, y]
            if c[3] <= 180 or _is_creamish(c) or b22.is_green_signature(c):
                continue
            if _is_badge_core_pixel(c, x, y):
                badge_samples.append(c)
            elif mp[x, y] > 0 and not _is_action_rect(x, y):
                frame_samples.append(c)
    frame_summary = _hls_summary_from_rgba(frame_samples)
    badge_summary = _hls_summary_from_rgba(badge_samples)
    enough_samples = frame_summary["count"] >= 100 and badge_summary["count"] >= 80
    if frame_summary["hue"] is None or badge_summary["hue"] is None:
        hue_delta = None
        color_consistent = False
        mode = "missing_samples"
    else:
        hue_delta = round(_hue_delta(frame_summary["hue"], badge_summary["hue"]), 4)
        low_sat_mode = frame_summary["saturation"] <= BADGE_LOW_SATURATION and badge_summary["saturation"] <= BADGE_LOW_SATURATION
        if low_sat_mode:
            lightness_delta = abs(frame_summary["lightness"] - badge_summary["lightness"])
            color_consistent = lightness_delta <= BADGE_LIGHTNESS_TOLERANCE
            mode = "low_saturation_lightness_compare"
        else:
            lightness_delta = abs(frame_summary["lightness"] - badge_summary["lightness"])
            color_consistent = hue_delta <= BADGE_HUE_TOLERANCE
            mode = "hue_compare"
    glyph_ok = glyph_metrics.get("status") == "pass" and glyph_metrics.get("rectangular_patch_used") is False
    return {
        "status": "pass" if enough_samples and color_consistent and glyph_ok else "fail",
        "state": state,
        "mode": mode,
        "frame_family_summary": frame_summary,
        "badge_core_summary": badge_summary,
        "hue_delta": hue_delta,
        "hue_tolerance": BADGE_HUE_TOLERANCE,
        "low_saturation_threshold": BADGE_LOW_SATURATION,
        "lightness_tolerance_when_low_saturation": BADGE_LIGHTNESS_TOLERANCE,
        "sample_scope": "frame family mask excluding action badge vs action badge inner core; both use multi-pixel samples, not single-point probes",
        "sample_count_minimum": {"frame": 100, "badge": 80},
        "glyph_shape_alpha_mask": glyph_metrics,
    }


def make_frame_family_mask(master_shell: Image.Image) -> Image.Image:
    mask = Image.new("L", FRAME_SIZE, 0)
    px = master_shell.convert("RGBA").load()
    mp = mask.load()
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if _frame_family_mask_pixel(px[x, y], x, y):
                mp[x, y] = 255
    return mask


def recolor_shell_from_master(master_shell: Image.Image, target_original: Image.Image, family_mask: Image.Image) -> Image.Image:
    src_h, src_l, src_s = _average_hls(master_shell, family_mask)
    dst_h, dst_l, dst_s = _average_hls(target_original, family_mask)
    l_ratio = dst_l / max(0.01, src_l)
    s_ratio = dst_s / max(0.01, src_s)
    out = master_shell.copy().convert("RGBA")
    px = out.load()
    mp = family_mask.load()
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if mp[x, y] == 0:
                continue
            r, g, b, a = px[x, y]
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            nr, ng, nb = colorsys.hls_to_rgb(dst_h, max(0.0, min(1.0, l * l_ratio)), max(0.0, min(1.0, s * s_ratio)))
            px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
    return out


def extract_globe_patch(master_frame: Image.Image) -> Image.Image:
    src = master_frame.convert("RGBA")
    primary = Image.new("L", FRAME_SIZE, 0)
    pp = primary.load()
    sp = src.load()
    for y in range(0, min(112, FRAME_SIZE[1])):
        for x in range(0, min(112, FRAME_SIZE[0])):
            if b22.is_cream(sp[x, y]):
                pp[x, y] = 255
    expanded = primary.filter(ImageFilter.MaxFilter(5))
    ep = expanded.load()
    patch = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    qp = patch.load()
    for y in range(0, min(112, FRAME_SIZE[1])):
        for x in range(0, min(112, FRAME_SIZE[0])):
            c = sp[x, y]
            if pp[x, y] or (ep[x, y] and _is_globe_antialias(c)):
                qp[x, y] = c
    return patch


def extract_badge_glyph(source_state_frame: Image.Image) -> tuple[Image.Image, dict]:
    src = source_state_frame.convert("RGBA")
    sp = src.load()
    raw_coords = sorted(badge_glyph_pixels(src))
    mask = Image.new("L", FRAME_SIZE, 0)
    mp = mask.load()
    for x, y in raw_coords:
        mp[x, y] = 255
    eroded = mask.filter(ImageFilter.MinFilter(3))
    ep = eroded.load()
    coords = sorted((x, y) for x, y in raw_coords if ep[x, y] > 0)
    if not coords:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0)), {
            "status": "fail",
            "raw_cream_glyph_pixels": len(raw_coords),
            "shape_alpha_pixels_after_1px_inset": 0,
            "non_cream_opaque_pixels": 0,
            "transparent_background_pixels": 1,
            "method": "cream glyph components excluding master outer badge ring, then 1px inset alpha mask",
        }
    bx1 = min(x for x, _y in coords)
    by1 = min(y for _x, y in coords)
    bx2 = max(x for x, _y in coords) + 1
    by2 = max(y for _x, y in coords) + 1
    glyph = Image.new("RGBA", (bx2 - bx1, by2 - by1), (0, 0, 0, 0))
    gp = glyph.load()
    for x, y in coords:
        gp[x - bx1, y - by1] = sp[x, y]
    non_cream = 0
    opaque = 0
    for y in range(glyph.height):
        for x in range(glyph.width):
            c = gp[x, y]
            if c[3] > 0:
                opaque += 1
                if not _is_creamish(c):
                    non_cream += 1
    return glyph, {
        "status": "pass" if non_cream == 0 and opaque == len(coords) else "fail",
        "raw_cream_glyph_pixels": len(raw_coords),
        "shape_alpha_pixels_after_1px_inset": len(coords),
        "non_cream_opaque_pixels": non_cream,
        "transparent_background_pixels": glyph.width * glyph.height - opaque,
        "crop_bbox_2x": [bx1, by1, bx2, by2],
        "method": "cream glyph components excluding master outer badge ring, then 1px inset alpha mask; no rectangular background pixels retained",
    }


def clear_badge_glyph_area(shell: Image.Image) -> Image.Image:
    out = shell.copy().convert("RGBA")
    px = out.load()
    base_samples: list[tuple[int, int, int]] = []
    x1, y1, x2, y2 = ACTION_RECT_2X
    clear_pixels = badge_glyph_clear_pixels(out)
    for y in range(y1, y2):
        for x in range(x1, x2):
            r, g, b, a = px[x, y]
            if (
                a > 180
                and (x, y) not in clear_pixels
                and not is_badge_outer_ring_component(
                    {
                        "bbox": (x, y, x + 1, y + 1),
                        "centroid": (float(x), float(y)),
                        "count": 1,
                    }
                )
                and x1 + 8 <= x < x2 - 8
                and y1 + 8 <= y < y2 - 8
                and not _is_creamish((r, g, b, a))
                and not b22.is_green_signature((r, g, b, a))
            ):
                base_samples.append((r, g, b))
    if not base_samples:
        for y in range(y1, y2):
            for x in range(x1, x2):
                r, g, b, a = px[x, y]
                if (
                    a > 180
                    and (x, y) not in clear_pixels
                    and not _is_creamish((r, g, b, a))
                    and not b22.is_green_signature((r, g, b, a))
                ):
                    base_samples.append((r, g, b))
    base = (27, 72, 70)
    if base_samples:
        base = (
            sum(c[0] for c in base_samples) // len(base_samples),
            sum(c[1] for c in base_samples) // len(base_samples),
            sum(c[2] for c in base_samples) // len(base_samples),
        )
    for x, y in clear_pixels:
        px[x, y] = (base[0], base[1], base[2], 255)
    return out


def paste_badge_glyph(shell: Image.Image, source_state_frame: Image.Image, state: str) -> tuple[Image.Image, dict]:
    if state == MASTER_STATE:
        return shell, {
            "status": "pass",
            "method": "available master keeps its original target glyph; no source rectangle pasted",
            "rectangular_patch_used": False,
            "non_cream_opaque_pixels": 0,
        }
    out = clear_badge_glyph_area(shell)
    glyph, metrics = extract_badge_glyph(source_state_frame)
    cx, cy = _badge_center()
    out.alpha_composite(glyph, (round(cx - glyph.width / 2), round(cy - glyph.height / 2)))
    metrics["rectangular_patch_used"] = False
    metrics["paste_anchor"] = "badge center"
    metrics["pasted_size"] = [glyph.width, glyph.height]
    return out, metrics


def selected_glow_layer(selected_source: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    lp = layer.load()
    sp = selected_source.convert("RGBA").load()
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            c = sp[x, y]
            if b22.is_green_signature(c):
                lp[x, y] = c
    return layer


def scrub_green_for_nonselected(img: Image.Image, state: str) -> Image.Image:
    if state == "selected":
        return img
    out = img.copy().convert("RGBA")
    px = out.load()
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if b22.is_green_signature(px[x, y]):
                r, g, b, _a = px[x, y]
                px[x, y] = (r, g, b, 0)
    return out


def full_rect_cutout_mask(window: tuple[int, int, int, int]) -> Image.Image:
    mask = Image.new("L", FRAME_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((window[0], window[1], window[2] - 1, window[3] - 1), fill=255)
    return mask


def count_old_signature_in_rect(img: Image.Image, rect: tuple[int, int, int, int]) -> tuple[int, list[list[int]]]:
    px = img.convert("RGBA").load()
    hits = 0
    samples: list[list[int]] = []
    x1, y1, x2, y2 = rect
    for y in range(max(0, y1), min(FRAME_SIZE[1], y2)):
        for x in range(max(0, x1), min(FRAME_SIZE[0], x2)):
            c = px[x, y]
            if _is_old_photo_signature(c):
                hits += 1
                if len(samples) < 10:
                    samples.append([x, y, c[0], c[1], c[2], c[3]])
    return hits, samples


def side_scan_rect(window: tuple[int, int, int, int], side: str) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = window
    if side == "top":
        return (x1, y1 - 1, x2, y1)
    if side == "bottom":
        return (x1, y2, x2, y2 + 1)
    if side == "left":
        return (x1 - 1, y1, x1, y2)
    if side == "right":
        return (x2, y1, x2 + 1, y2)
    raise ValueError(side)


def count_side_residue(frame: Image.Image, window: tuple[int, int, int, int], side: str) -> tuple[int, list[list[int]]]:
    return count_old_signature_in_rect(frame, side_scan_rect(window, side))


def expand_window_for_edge_residue(master_frame: Image.Image, base_window: tuple[int, int, int, int]) -> tuple[tuple[int, int, int, int], dict]:
    window = list(base_window)
    expansions = {"top": 0, "right": 0, "bottom": 0, "left": 0}
    before = {side: count_side_residue(master_frame, tuple(window), side)[0] for side in expansions}
    for _ in range(EDGE_SCAN_MAX_EXPAND_PX * 4):
        changed = False
        for side in ["top", "right", "bottom", "left"]:
            if expansions[side] >= EDGE_SCAN_MAX_EXPAND_PX:
                continue
            count, _samples = count_side_residue(master_frame, tuple(window), side)
            if count == 0:
                continue
            if side == "top" and window[1] > 0:
                window[1] -= 1
            elif side == "bottom" and window[3] < FRAME_SIZE[1]:
                window[3] += 1
            elif side == "left" and window[0] > 0:
                window[0] -= 1
            elif side == "right" and window[2] < FRAME_SIZE[0]:
                window[2] += 1
            expansions[side] += 1
            changed = True
        if not changed:
            break
    final_window = tuple(window)
    after: dict[str, dict] = {}
    for side in expansions:
        hits, samples = count_side_residue(master_frame, final_window, side)
        after[side] = {"old_photo_signature_pixels": hits, "sample_pixels": samples}
    return final_window, {
        "base_window_rect_2x": list(base_window),
        "expanded_window_rect_2x": list(final_window),
        "max_expand_px_per_side": EDGE_SCAN_MAX_EXPAND_PX,
        "old_photo_signature": "alpha>180 and b>g+8 and b>40, excluding warm cream globe/badge pixels",
        "before": before,
        "expansions_px": expansions,
        "after": after,
        "status": "pass" if all(item["old_photo_signature_pixels"] == 0 for item in after.values()) else "fail",
    }


def gate_old_content_leftover(shell: Image.Image, globe_patch: Image.Image, window: tuple[int, int, int, int]) -> dict:
    shell_hits, shell_samples = count_old_signature_in_rect(shell, window)
    globe_hits, globe_samples = count_old_signature_in_rect(globe_patch, window)
    total = shell_hits + globe_hits
    return {
        "status": "pass" if total == 0 else "fail",
        "scope": "hollow shell plus independent globe patch, full expanded window including coverage-element area; photo layer is excluded because it intentionally contains new content",
        "old_photo_signature_pixels": total,
        "shell_hits": shell_hits,
        "globe_patch_hits": globe_hits,
        "sample_pixels": shell_samples + globe_samples,
    }


def make_master_hollow_shell(master_frame: Image.Image, window: tuple[int, int, int, int], globe_patch: Image.Image) -> tuple[Image.Image, Image.Image, dict]:
    shell = master_frame.copy().convert("RGBA")
    mask = full_rect_cutout_mask(window)
    px = shell.load()
    mp = mask.load()
    cut_pixels = 0
    for y in range(FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            if mp[x, y]:
                r, g, b, _a = px[x, y]
                px[x, y] = (r, g, b, 0)
                cut_pixels += 1
    shell = scrub_green_for_nonselected(shell, MASTER_STATE)
    return shell, mask, {
        "master_state": MASTER_STATE,
        "window_rect_2x": list(window),
        "cutout_pixels": cut_pixels,
        "globe_patch_pixels": sum(1 for _y in range(FRAME_SIZE[1]) for _x in range(FRAME_SIZE[0]) if globe_patch.getpixel((_x, _y))[3] > 0),
        "method": "single available-state master; full measured-and-edge-expanded window cutout; no globe protection zone; globe linework is an independent top patch",
    }


def photo_underlay_for_state(photo_frame: Image.Image, window: tuple[int, int, int, int], state: str) -> Image.Image:
    photo = photo_frame.crop(b22.SOURCE_PHOTO_RECT_2X).convert("RGBA")
    return b22.cover_photo_to_window(photo, window, state)


def compose_single_master_frames() -> tuple[list[Image.Image], list[Image.Image], Image.Image, Image.Image, Image.Image, dict, list[dict], list[dict]]:
    source_frames = b22.load_atlas_frames(B_ATLAS)
    photo_frames = b22.load_atlas_frames(B13_ATLAS)
    master_frame = source_frames[MASTER_INDEX]
    base_window, measurement_meta = b22.measure_window(master_frame)
    window, edge_residue_scan = expand_window_for_edge_residue(master_frame, base_window)
    globes = b22.measure_globes(source_frames)
    globe = globes[MASTER_INDEX]
    globe_patch = extract_globe_patch(master_frame)
    master_shell, cutout_mask, master_meta = make_master_hollow_shell(master_frame, window, globe_patch)
    family_mask = make_frame_family_mask(master_shell)
    glow = selected_glow_layer(source_frames[STATE_ORDER.index("selected")])

    shells: list[Image.Image] = []
    frames: list[Image.Image] = []
    per_state: list[dict] = []
    for idx, state in enumerate(STATE_ORDER):
        badge_glyph_metrics = {
            "status": "pass",
            "method": "available master keeps original target glyph; derived states replace glyph through shape alpha mask",
            "rectangular_patch_used": False,
            "non_cream_opaque_pixels": 0,
        }
        if state == MASTER_STATE:
            shell = master_shell.copy()
        else:
            shell = recolor_shell_from_master(master_shell, source_frames[idx], family_mask)
            shell, badge_glyph_metrics = paste_badge_glyph(shell, source_frames[idx], state)
        shell = scrub_green_for_nonselected(shell, state)

        photo = photo_underlay_for_state(photo_frames[idx], window, state)
        frame = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        frame.alpha_composite(photo, (window[0], window[1]))
        frame.alpha_composite(shell)
        if state == "selected":
            frame.alpha_composite(glow)
        frame.alpha_composite(globe_patch)
        frame = scrub_green_for_nonselected(frame, state)

        gates = {
            "gateA_old_photo_residue": b22.gate_a_old_residue(shell, cutout_mask, window),
            "old_content_leftover_scan": gate_old_content_leftover(shell, globe_patch, window),
            "window_edge_residue_scan": edge_residue_scan,
            "gateB_border_integrity": b22.gate_b_border_integrity(master_frame, shell, window),
            "gateC_window_alpha": b22.gate_c_window_alpha(frame, window),
            "gateD_green_residue": b22.gate_d_green_residue(frame, state),
            "badge_state_color_consistency": gate_badge_state_color_consistency(frame, family_mask, state, badge_glyph_metrics),
            "gateF_geometry": b22.gate_f_geometry(frame),
        }
        shells.append(shell)
        frames.append(frame)
        per_state.append(
            {
                "state": state,
                "source": "single_master_available" if state == MASTER_STATE else "derived_from_available_master",
                "base_measured_window_rect_2x": list(base_window),
                "master_window_rect_2x": list(window),
                "photo_underlay_rect_2x": list(window),
                "globe_disc": globe,
                "photo_shape_clipping": "forbidden_not_used",
                "color_derivation": "available frame-family hue/lightness mapping" if state != MASTER_STATE else "master_no_recolor",
                "badge_icon_source": "available master" if state == MASTER_STATE else f"candidate B original {state} cream glyph only, 1px-inset shape alpha mask centered inside master badge ring",
                "badge_glyph_alpha_mask": badge_glyph_metrics,
                "selected_glow_layer": "selected outer green glow extracted from original selected frame" if state == "selected" else "not_applied",
                "z_order": "transparent base -> rectangular B1.3 photo underlay -> single-master derived hollow shell -> selected glow if selected -> independent globe patch -> runtime text",
                "gates": gates,
            }
        )

    measurement = {
        "master_state": MASTER_STATE,
        "measurement_rule_version": "wmw_hollow_shell_photo_pipeline_v1_1_single_master_b2_5_badge_fix",
        "base_measured_window_rect_2x": list(base_window),
        "master_window_rect_2x": list(window),
        "master_adaptive_classifier_samples": measurement_meta,
        "master_globe_disc": globe,
        "globe_layering": "independent warm-cream globe patch; window cutout has no globe protection zone",
        "window_edge_residue_scan": edge_residue_scan,
        "gateE_same_state_layout": {
            "status": "pass",
            "basis": "all four derived states use the exact same master window rectangle; source per-frame windows are no longer production geometry input",
            "diff_px": 0,
        },
    }
    return frames, shells, master_shell, cutout_mask, globe_patch, measurement, per_state, [
        {
            "state": state,
            "export_size_2x": list(FRAME_SIZE),
            "export_size_1x": list(EXPORT_SIZE),
            "ratio": FRAME_SIZE[0] / FRAME_SIZE[1],
            "ratio_target": TARGET_RATIO,
            "ratio_delta": abs(FRAME_SIZE[0] / FRAME_SIZE[1] - TARGET_RATIO),
            "ratio_pass": abs(FRAME_SIZE[0] / FRAME_SIZE[1] - TARGET_RATIO) <= RATIO_TOLERANCE,
            "master_window_rect_2x": list(window),
            "photo_slot_2x": list(PHOTO_RECT_2X),
            "action_badge_2x": list(ACTION_RECT_2X),
        }
        for state in STATE_ORDER
    ]


def make_compare_board(source_frames: list[Image.Image], derived_frames: list[Image.Image], measurement: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1780, 1040), (8, 20, 22, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.5 v0.9.11 badge-fix derivation QA", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 64), f"master={MASTER_STATE} base={measurement['base_measured_window_rect_2x']} expanded={measurement['master_window_rect_2x']}  GateE=diff 0", fill=(205, 224, 198), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 420
        y = 112
        src = source_frames[idx].resize((326, 256), Image.Resampling.LANCZOS)
        dst_bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        dst_bg.alpha_composite(derived_frames[idx])
        dst = dst_bg.resize((326, 256), Image.Resampling.LANCZOS)
        canvas.alpha_composite(src, (x, y))
        canvas.alpha_composite(dst, (x, y + 342))
        draw.rectangle((x, y, x + 326, y + 256), outline=(110, 150, 134), width=2)
        draw.rectangle((x, y + 342, x + 326, y + 598), outline=(110, 150, 134), width=2)
        draw.text((x, y - 26), f"{state} original B", fill=(232, 229, 199), font=b11.F_SMALL)
        draw.text((x, y + 316), f"{state} derived", fill=(188, 235, 197), font=b11.F_SMALL)
    draw.text((42, 760), "B2.5 fixes: badge core joins state recolor; glyph swap uses shape-alpha mask only.", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_ingredient_board(shells: list[Image.Image], master_shell: Image.Image, mask: Image.Image, globe_patch: Image.Image, measurement: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1060), (9, 22, 24, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.5 single-master ingredients", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 64), "available hollow shell is the only geometry source; globe is an independent top patch; other states are hue/glyph/glow derivations.", fill=(205, 224, 198), font=b11.F_NOTE)
    headers = ["master hollow shell", "cutout mask", "globe patch", "selected", "available", "warning", "locked"]
    for i, header in enumerate(headers):
        draw.text((42 + i * 260, 104), header, fill=(188, 216, 190), font=b11.F_SMALL)
    previews = [
        master_shell,
        ImageOps.colorize(mask, black="#071315", white="#58e9ff").convert("RGBA"),
        globe_patch,
        *shells,
    ]
    for i, img in enumerate(previews):
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(img)
        preview = bg.resize((245, 192), Image.Resampling.LANCZOS if i != 1 else Image.Resampling.NEAREST)
        x = 42 + i * 260
        y = 136
        canvas.alpha_composite(preview, (x, y))
        draw.rectangle((x, y, x + 245, y + 192), outline=(76, 139, 126), width=2)
    draw.text((42, 390), json.dumps(measurement, ensure_ascii=False, indent=2)[:1800], fill=(210, 220, 200), font=b11.F_SMALL)
    return canvas


def make_fit_qa(frames: list[Image.Image], measurement: dict) -> Image.Image:
    rect = tuple(measurement["master_window_rect_2x"])
    globe = measurement["master_globe_disc"]
    canvas = Image.new("RGBA", (1920, 1540), (8, 20, 22, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.5 v0.9.11 16-point visual QA: badge-core recolor + shape-alpha glyph", fill=(242, 238, 210), font=b11.F_HEAD)
    draw.text((42, 64), "Each state has four 200% checkpoints: globe arc / right edge / bottom edge / badge. Manifest must record each point separately.", fill=(205, 224, 198), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        row_y = 126 + idx * 350
        bg = Image.new("RGBA", FRAME_SIZE, (7, 19, 21, 255))
        bg.alpha_composite(frames[idx])
        gx, gy = globe["center"]
        gr = globe["radius"]
        draw.text((42, row_y - 30), state, fill=(255, 229, 93), font=b11.F_NOTE)
        badge_crop = (
            max(0, ACTION_RECT_2X[0] - 10),
            max(0, ACTION_RECT_2X[1] - 10),
            min(FRAME_SIZE[0], ACTION_RECT_2X[2] + 10),
            min(FRAME_SIZE[1], ACTION_RECT_2X[3] + 10),
        )
        for panel_idx, (title, crop) in enumerate(
            [
                ("globe arc", (max(0, int(gx - gr - 12)), max(0, int(gy - gr - 8)), min(FRAME_SIZE[0], int(gx + gr + 42)), min(FRAME_SIZE[1], int(gy + gr + 30)))),
                ("right edge", (rect[2] - 34, rect[1] - 10, min(FRAME_SIZE[0], rect[2] + 34), rect[3] + 10)),
                ("bottom edge", (rect[0] + 24, rect[3] - 28, rect[2] - 24, min(FRAME_SIZE[1], rect[3] + 28))),
                ("badge", badge_crop),
            ]
        ):
            x = [42, 330, 520, 1130][panel_idx]
            panel = bg.crop(crop).resize(((crop[2] - crop[0]) * 2, (crop[3] - crop[1]) * 2), Image.Resampling.NEAREST)
            canvas.alpha_composite(panel, (x, row_y))
            draw.rectangle((x, row_y, x + panel.width, row_y + panel.height), outline=(94, 164, 142), width=2)
            draw.text((x, row_y - 23), title, fill=(234, 232, 204), font=b11.F_SMALL)
        thumb = bg.resize((245, 192), Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb, (1590, row_y + 10))
        draw.rectangle((1590, row_y + 10, 1835, row_y + 202), outline=(94, 164, 142), width=2)
    return canvas


def make_manual_visual_check_table(manual_pass: bool) -> dict:
    status = "evidence_ready"
    return {
        state: {
            point: {
                "status": status,
                "evidence": str(OUT_FIT_QA),
                "scale": "200%",
                "review_owner": "reviewer_or_user",
                "self_check_scope": "evidence prepared only; execution self-check is not final PASS",
            }
            for point in ["globe_arc_underlay", "window_right_edge", "window_bottom_edge", "badge_area"]
        }
        for state in STATE_ORDER
    }


def make_runtime_preview(frames: list[Image.Image], show_qa: bool) -> Image.Image:
    canvas = b11.make_runtime_preview(frames, b11.load_contract(), show_qa)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((448, 30, 1400, 112), fill=(7, 19, 21))
    draw.text((450, 34), "Python v0.9.11 B2.5 left_region_card runtime fill", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 76), "Badge core uses state color family; badge glyphs are shape-alpha masks, not rectangular patches.", fill=(217, 222, 199), font=b11.F_NOTE)
    return canvas


def aggregate_gates(per_state: list[dict], measurement: dict, manual_pass: bool, godot_pass: bool) -> dict:
    def all_status(name: str, allowed: set[str] = {"pass"}) -> bool:
        return all(item["gates"][name]["status"] in allowed for item in per_state)

    manual_checks = make_manual_visual_check_table(manual_pass)
    manual_status = "evidence_ready" if all(
        check["status"] == "evidence_ready"
        for state_checks in manual_checks.values()
        for check in state_checks.values()
    ) else "pending_evidence"
    return {
        "gateA_old_photo_residue_core": {
            "status": "pass" if all_status("gateA_old_photo_residue") else "fail",
            "basis": "single master hollow-shell cutout core contains zero opaque shell pixels",
        },
        "old_content_leftover_scan": {
            "status": "pass" if all_status("old_content_leftover_scan") else "fail",
            "basis": "full expanded window scan on shell/globe-patch layers contains zero old source photo signature pixels",
        },
        "window_edge_residue_scan": {
            "status": "pass" if measurement["window_edge_residue_scan"]["status"] == "pass" else "fail",
            "basis": "after edge expansion, all four sides outside the window contain zero old photo signature pixels",
            "scan": measurement["window_edge_residue_scan"],
        },
        "gateB_border_integrity_ring": {
            "status": "pass" if all_status("gateB_border_integrity") else "fail",
            "basis": "3px ring outside master window remains opaque wherever available master was opaque",
        },
        "gateC_window_alpha_after_composite": {
            "status": "pass" if all_status("gateC_window_alpha") else "fail",
            "basis": "photo underlay fills the master window; final alpha inside window is 255",
        },
        "gateD_green_residue_nonselected": {
            "status": "pass" if all_status("gateD_green_residue", {"pass", "skipped_selected_green_glow_semantic"}) else "fail",
            "basis": "selected is exempt; available/warning/locked full-frame green signature must be zero",
        },
        "badge_state_color_consistency": {
            "status": "pass" if all_status("badge_state_color_consistency") else "fail",
            "basis": "badge inner core belongs to frame-color family; hue/lightness comparison uses multi-pixel samples and glyph alpha-mask metrics",
            "per_state": {
                item["state"]: item["gates"]["badge_state_color_consistency"]
                for item in per_state
            },
        },
        "gateE_same_state_window_layout": measurement["gateE_same_state_layout"],
        "gateF_geometry_ratio": {
            "status": "pass" if all_status("gateF_geometry") else "fail",
            "basis": "all derived frames are 408x320; ratio 1.275 unchanged",
            "target_ratio": TARGET_RATIO,
            "tolerance": RATIO_TOLERANCE,
        },
        "manual_16point_visual_check": {
            "status": manual_status,
            "basis": "inspect 485: four states x four checkpoints (globe arc/right edge/bottom edge/badge); execution output is evidence-ready only, reviewer/user owns PASS/FAIL",
            "evidence": str(OUT_FIT_QA),
            "checks": manual_checks,
        },
        "derived_art_quality_check": {
            "status": "evidence_ready",
            "basis": "inspect 479: derived status colors/material comparison is prepared for reviewer; execution self-check is not final PASS",
            "evidence": str(OUT_COMPARE),
        },
        "godot_windowed_capture": {
            "status": "pass" if godot_pass else "pending",
            "basis": "windowed opengl3 capture via scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro",
            "headless_used_for_ui_capture": False,
        },
    }


def make_manifest(measurement: dict, per_state: list[dict], geometry_metrics: list[dict], checks: dict, manual_pass: bool, godot_pass: bool) -> dict:
    gates = aggregate_gates(per_state, measurement, manual_pass, godot_pass)
    program_gate_names = [
        "gateA_old_photo_residue_core",
        "old_content_leftover_scan",
        "window_edge_residue_scan",
        "gateB_border_integrity_ring",
        "gateC_window_alpha_after_composite",
        "gateD_green_residue_nonselected",
        "badge_state_color_consistency",
        "gateE_same_state_window_layout",
        "gateF_geometry_ratio",
        "godot_windowed_capture",
    ]
    evidence_ready = (
        all(gates[name]["status"] == "pass" for name in program_gate_names)
        and gates["manual_16point_visual_check"]["status"] == "evidence_ready"
        and gates["derived_art_quality_check"]["status"] == "evidence_ready"
    )
    return {
        "schema_version": 1,
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "date": "2026-07-09",
        "status": "b2_5_badge_fix_evidence_ready_pending_review" if evidence_ready else "b2_5_badge_fix_pending_full_chain",
        "contract": str(b11.CONTRACT_PATH),
        "contract_frozen_fields_changed": False,
        "pipeline": "available single master -> edge-expanded full-window cutout -> derived state skins with badge-core recolor -> shape-alpha badge glyph swap -> rectangular photo underlay -> independent globe patch -> runtime text",
        "inputs": {
            "candidate_b_original_atlas_2x": str(B_ATLAS),
            "candidate_b1_3_photo_atlas_2x": str(B13_ATLAS),
            "previous_b2_2_overlay": str(b22.OUT_MEASURE_QA),
            "previous_b2_3_manifest": str(BASE / "466-world-map-wmw-v0-9-9-left-card-b2-3-manifest.json"),
            "previous_b2_4_manifest": str(BASE / "476-world-map-wmw-v0-9-10-left-card-b2-4-manifest.json"),
        },
        "outputs": {
            "derive_compare": str(OUT_COMPARE),
            "ingredients": str(OUT_INGREDIENTS),
            "atlas_2x": str(OUT_ATLAS),
            "geometry_qa": str(OUT_GEOMETRY_QA),
            "runtime_fill_preview": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "visual_16point_qa": str(OUT_FIT_QA),
            "manifest": str(OUT_MANIFEST),
            "godot_single_component": str(OUT_GODOT),
            "godot_single_component_qa": str(OUT_GODOT_QA),
            "godot_atlas_copy": str(GODOT_ATLAS),
            "godot_manifest_copy": str(GODOT_MANIFEST),
            "godot_ingredients_dir": str(GODOT_INGREDIENT_DIR),
        },
        "runtime_tokens": {
            "label_title": {"python_font_px": 19, "godot_font_size": b11.TOKENS["label_title"]["godot_font_size"], "color": b11.TOKENS["label_title"]["godot_color"]},
            "meta_status": {"python_font_px": 11, "godot_font_size": b11.TOKENS["meta_status"]["godot_font_size"], "color": b11.TOKENS["meta_status"]["godot_color"]},
        },
        "measurement": measurement,
        "per_state": per_state,
        "geometry_metrics": geometry_metrics,
        "gates": gates,
        "image_content_checks": checks,
        "prohibitions_observed": {
            "imagegen_called": False,
            "photo_shape_clipping_used": False,
            "per_state_window_sources_used": False,
            "selected_green_cleanup_used": False,
            "globe_protection_zone_used": False,
            "source_frame_badge_slot_crop_used": False,
            "badge_rectangular_patch_used": False,
            "contract_frozen_fields_changed": False,
            "other_classes_batch_produced": False,
            "other_layers_modified": "badge layer and derived recolor only; B2.4 globe patch, edge scan, and photo layer logic retained",
        },
    }


def write_outputs(manual_pass: bool = False) -> dict:
    source_frames = b22.load_atlas_frames(B_ATLAS)
    frames, shells, master_shell, mask, globe_patch, measurement, per_state, geometry_metrics = compose_single_master_frames()
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    make_compare_board(source_frames, frames, measurement).save(OUT_COMPARE)
    make_ingredient_board(shells, master_shell, mask, globe_patch, measurement).save(OUT_INGREDIENTS)
    b11.make_atlas(frames).save(OUT_ATLAS)
    geometry_qa, _ = b11.make_geometry_qa(frames, [{"state": item["state"], "pipeline": item["z_order"], "master_window_rect_2x": item["master_window_rect_2x"]} for item in per_state])
    geometry_qa.save(OUT_GEOMETRY_QA)
    make_runtime_preview(frames, False).save(OUT_RUNTIME)
    make_runtime_preview(frames, True).save(OUT_RUNTIME_QA)
    make_fit_qa(frames, measurement).save(OUT_FIT_QA)

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    GODOT_INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    b11.make_atlas(frames).save(GODOT_ATLAS)
    globe_patch.save(GODOT_INGREDIENT_DIR / "left_region_card_b25_independent_globe_patch.png")
    for state, shell in zip(STATE_ORDER, shells):
        shell.save(GODOT_INGREDIENT_DIR / f"left_region_card_b25_badge_fix_hollow_shell_{state}.png")

    checks = {
        name: b11.count_colors_nonblack(path)
        for name, path in {
            "derive_compare": OUT_COMPARE,
            "ingredients": OUT_INGREDIENTS,
            "atlas_2x": OUT_ATLAS,
            "geometry_qa": OUT_GEOMETRY_QA,
            "runtime_fill_preview": OUT_RUNTIME,
            "runtime_fill_qa": OUT_RUNTIME_QA,
            "visual_16point_qa": OUT_FIT_QA,
            "godot_single_component": OUT_GODOT,
            "godot_single_component_qa": OUT_GODOT_QA,
        }.items()
        if path.exists()
    }
    godot_pass = OUT_GODOT.exists() and OUT_GODOT_QA.exists()
    manifest = make_manifest(measurement, per_state, geometry_metrics, checks, manual_pass=manual_pass, godot_pass=godot_pass)
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build WMW left card B2.5 badge-fix single-master atlas.")
    parser.add_argument(
        "--manual-ok",
        action="store_true",
        help="Deprecated compatibility flag; B2.5 only marks visual checks evidence_ready pending reviewer/user judgment.",
    )
    args = parser.parse_args()
    manifest = write_outputs(manual_pass=args.manual_ok)
    print(json.dumps(
        {
            "status": manifest["status"],
            "master_window": manifest["measurement"]["master_window_rect_2x"],
            "gateE": manifest["gates"]["gateE_same_state_window_layout"],
            "outputs": manifest["outputs"],
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
