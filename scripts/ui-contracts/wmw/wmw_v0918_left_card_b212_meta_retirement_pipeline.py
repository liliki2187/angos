# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import colorsys
import json
import random
from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v0916_left_card_b210_symmetric_core_pipeline as b210


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.18"
ROUND_ID = "B2.12"
ASSET_ID = "world_map_wmw_left_region_card_b2_12_meta_retired"

OUT_COMPARE = BASE / "549-world-map-wmw-v0-9-18-left-card-b2-12-meta-retirement-compare.png"
OUT_INGREDIENTS = BASE / "550-world-map-wmw-v0-9-18-left-card-b2-12-clean-substrate-qa.png"
OUT_ATLAS = BASE / "551-world-map-wmw-v0-9-18-left-card-b2-12-atlas-2x.png"
OUT_GEOMETRY = BASE / "552-world-map-wmw-v0-9-18-left-card-b2-12-geometry-qa.png"
OUT_RUNTIME = BASE / "553-world-map-wmw-v0-9-18-left-card-b2-12-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "554-world-map-wmw-v0-9-18-left-card-b2-12-runtime-fill-qa.png"
OUT_VISUAL_QA = BASE / "555-world-map-wmw-v0-9-18-left-card-b2-12-16point-visual-qa.png"
OUT_MANIFEST = BASE / "556-world-map-wmw-v0-9-18-left-card-b2-12-manifest.json"
OUT_GODOT = BASE / "557-world-map-wmw-v0-9-18-left-card-b2-12-godot-single-component.png"
OUT_GODOT_QA = BASE / "558-world-map-wmw-v0-9-18-left-card-b2-12-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b212_meta_retired_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b212_meta_retired_manifest.json"

B211_ATLAS = BASE / "541-world-map-wmw-v0-9-17-left-card-b2-11-atlas-2x.png"
B211_META_RECT_1X = (22, 138, 112, 14)

CONTRACT = b11.load_contract()
STATE_ORDER = b210.STATE_ORDER
FRAME_SIZE = b210.FRAME_SIZE
EXPORT_SIZE = b210.EXPORT_SIZE
MASTER_INDEX = b210.MASTER_INDEX
MASTER_STATE = b210.MASTER_STATE

COPY = [
    {"title": "北美禁区带", "old_meta": "红线升温 · 推荐2"},
    {"title": "欧洲灰域", "old_meta": "可派遣 · 线报2"},
    {"title": "非洲禁区带", "old_meta": "异常升温 · 高危"},
    {"title": "南美禁区带", "old_meta": "锁定 · 需3线报"},
]

# The lower content plane is rebuilt as one layer. The old strip is never used
# as a source and therefore cannot leak through a local rectangular patch.
LOWER_PANEL_RECT = (26, 198, 382, 302)
OLD_META_CORE = (35, 276, 209, 294)
OLD_META_OUTER = (31, 272, 213, 298)
TEXTURE_SOURCE_RECT = (222, 276, 280, 300)
MASTER_SAMPLE_POINTS = [
    (50, 195),
    (280, 200),
    (380, 250),
    (270, 280),
    (260, 300),
    (100, 300),
    (30, 250),
    (240, 285),
]

MAX_OLD_BOUNDARY_MEAN_GRADIENT = 18.0
SUBSTRATE_GRAIN_SEED = 184
SUBSTRATE_GRAIN_TARGET_RATIO = 0.08
MIN_RETIRED_FACET_COUNT = 3
MAX_RETIRED_DOMINANT_FACET_RATIO = 0.45
MIN_SUBSTRATE_GRAIN_RATIO = 0.075


def rect_2x(name: str) -> tuple[int, int, int, int]:
    x, y, w, h = CONTRACT["frozen"]["slots"][name]
    return (x * 2, y * 2, (x + w) * 2, (y + h) * 2)


LABEL_RECT_2X = rect_2x("label_plate")
ACTION_RECT_2X = rect_2x("action_badge")


def is_paper_cream(px: tuple[int, int, int, int]) -> bool:
    r, g, b, a = px
    return a > 200 and r > 150 and g > 120 and b > 80 and r > b + 20


def _largest_component_mask(
    image: Image.Image,
    search: tuple[int, int, int, int],
    predicate,
) -> tuple[Image.Image, tuple[int, int, int, int], int]:
    rgba = image.convert("RGBA")
    px = rgba.load()
    points = {
        (x, y)
        for y in range(search[1], search[3])
        for x in range(search[0], search[2])
        if predicate(px[x, y])
    }
    components: list[list[tuple[int, int]]] = []
    while points:
        seed = points.pop()
        queue = deque([seed])
        component = [seed]
        while queue:
            x, y = queue.popleft()
            for nxt in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if nxt in points:
                    points.remove(nxt)
                    queue.append(nxt)
                    component.append(nxt)
        components.append(component)
    if not components:
        raise RuntimeError(f"component not found in {search}")
    component = max(components, key=len)
    mask = Image.new("L", FRAME_SIZE, 0)
    mp = mask.load()
    for x, y in component:
        mp[x, y] = 255
    xs = [p[0] for p in component]
    ys = [p[1] for p in component]
    bbox = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    return mask, bbox, len(component)


def title_keep_mask(master_shell: Image.Image) -> tuple[Image.Image, dict]:
    component, bbox, count = _largest_component_mask(
        master_shell,
        (20, 188, 280, 274),
        is_paper_cream,
    )
    mask = component.filter(ImageFilter.MaxFilter(5))
    mp = mask.load()
    # The title paper ends above the retired carrier. This clip prevents the
    # carrier's top shadow from being mistaken for the title contact shadow.
    for y in range(272, FRAME_SIZE[1]):
        for x in range(FRAME_SIZE[0]):
            mp[x, y] = 0
    return mask, {
        "cream_component_bbox_2x": list(bbox),
        "cream_component_pixels": count,
        "dilation_radius_px": 2,
        "hard_bottom_clip_y_exclusive": 272,
    }


def badge_keep_mask(master_shell: Image.Image) -> tuple[Image.Image, dict]:
    _component, bbox, count = _largest_component_mask(
        master_shell,
        (270, 188, 390, 306),
        is_paper_cream,
    )
    x1 = max(0, bbox[0] - 8)
    y1 = max(0, bbox[1] - 8)
    x2 = min(FRAME_SIZE[0], bbox[2] + 8)
    y2 = min(FRAME_SIZE[1], bbox[3] + 8)
    cut = min(18, (x2 - x1) // 4, (y2 - y1) // 4)
    polygon = [
        (x1 + cut, y1),
        (x2 - cut, y1),
        (x2, y1 + cut),
        (x2, y2 - cut),
        (x2 - cut, y2),
        (x1 + cut, y2),
        (x1, y2 - cut),
        (x1, y1 + cut),
    ]
    mask = Image.new("L", FRAME_SIZE, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    return mask, {
        "ring_cream_bbox_2x": list(bbox),
        "ring_cream_pixels": count,
        "preserve_polygon_2x": [list(p) for p in polygon],
    }


def _sample_color(image: Image.Image, point: tuple[int, int]) -> tuple[int, int, int, int]:
    color = image.convert("RGBA").getpixel(point)
    if color[3] != 255 or is_paper_cream(color):
        raise RuntimeError(f"invalid lower-panel palette sample {point}: {color}")
    return color


def _average_hls(colors: list[tuple[int, int, int, int]]) -> tuple[float, float, float]:
    values = [colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0) for r, g, b, _a in colors]
    return (
        sum(v[0] for v in values) / len(values),
        sum(v[1] for v in values) / len(values),
        sum(v[2] for v in values) / len(values),
    )


def build_master_substrate(master_shell: Image.Image) -> tuple[Image.Image, dict]:
    samples = [_sample_color(master_shell, p) for p in MASTER_SAMPLE_POINTS]
    average = tuple(round(sum(color[channel] for color in samples) / len(samples)) for channel in range(3))
    # Preserve the measured palette hierarchy while keeping the lower plate
    # quieter than the photo and title. These remain flat low-poly faces, not
    # a gradient; only their contrast is pulled toward the sampled mean.
    facet_colors = [
        tuple(round(average[channel] * 0.45 + color[channel] * 0.55) for channel in range(3)) + (255,)
        for color in samples
    ]
    l, t, r, b = LOWER_PANEL_RECT
    rr = r - 1
    bb = b - 1
    cx = l + (r - l) * 52 // 100
    cy = t + (b - t) * 47 // 100
    top = [(l, t), (140, t), (270, t), (rr, t)]
    middle = [(l, 248), (118, 244), (242, 250), (rr, 244)]
    bottom = [(l, bb), (145, bb), (275, bb), (rr, bb)]
    polygons: list[list[tuple[int, int]]] = []
    for row_index, (upper, lower) in enumerate(((top, middle), (middle, bottom))):
        for column in range(3):
            a, b_point = upper[column], upper[column + 1]
            c, d = lower[column], lower[column + 1]
            if (row_index + column) % 2 == 0:
                polygons.extend([[a, b_point, c], [b_point, d, c]])
            else:
                polygons.extend([[a, b_point, d], [a, d, c]])
    facet_source_indices = [0, 1, 6, 7, 2, 3, 5, 4, 1, 6, 3, 0]
    facet_colors = [facet_colors[index] for index in facet_source_indices]
    layer = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for polygon, color in zip(polygons, facet_colors):
        draw.polygon(polygon, fill=color)

    texture = master_shell.crop(TEXTURE_SOURCE_RECT).convert("RGBA")
    colors = [px for px in texture.getdata() if px[3] == 255 and not is_paper_cream(px)]
    if len(colors) != texture.width * texture.height:
        raise RuntimeError("clean substrate texture source contains alpha or paper pixels")
    mean = tuple(sum(px[i] for px in colors) / len(colors) for i in range(3))
    lp = layer.load()
    residual_palette = sorted({
        tuple(max(-4, min(4, round(color[channel] - mean[channel]))) for channel in range(3))
        for color in colors
    } - {(0, 0, 0)})
    if len(residual_palette) < 12:
        raise RuntimeError(f"clean texture residual palette too small: {len(residual_palette)}")
    rng = random.Random(SUBSTRATE_GRAIN_SEED)
    target_grain_pixels = round((r - l) * (b - t) * SUBSTRATE_GRAIN_TARGET_RATIO)
    covered = 0
    clusters = 0
    occupied: set[tuple[int, int]] = set()
    while covered < target_grain_pixels and clusters < 2000:
        size = rng.randint(2, 4)
        gx = rng.randint(l, max(l, r - size))
        gy = rng.randint(t, max(t, b - size))
        residual = residual_palette[rng.randrange(len(residual_palette))]
        added = 0
        for py in range(gy, min(gy + size, b)):
            for px in range(gx, min(gx + size, r)):
                if (px, py) in occupied:
                    continue
                occupied.add((px, py))
                base = lp[px, py]
                lp[px, py] = tuple(max(0, min(255, base[channel] + residual[channel])) for channel in range(3)) + (255,)
                added += 1
        if added:
            covered += added
            clusters += 1

    facet_map = Image.new("I", FRAME_SIZE, 0)
    facet_draw = ImageDraw.Draw(facet_map)
    for index, polygon in enumerate(polygons, start=1):
        facet_draw.polygon(polygon, fill=index)
    retired_facet_counts = Counter(facet_map.crop(OLD_META_OUTER).getdata())
    retired_facet_counts.pop(0, None)
    retired_facet_pixels = sum(retired_facet_counts.values())
    retired_dominant_facet_ratio = (
        max(retired_facet_counts.values()) / max(1, retired_facet_pixels)
        if retired_facet_counts
        else 1.0
    )

    return layer, {
        "construction": "single available-state master; twelve explicit low-poly facets plus non-periodic sparse grain clusters whose RGB residuals are sampled from a clean same-card substrate chip",
        "panel_rect_2x": list(LOWER_PANEL_RECT),
        "facet_center_2x": [cx, cy],
        "facet_polygons_2x": [[list(p) for p in polygon] for polygon in polygons],
        "palette_sample_points_2x": [list(p) for p in MASTER_SAMPLE_POINTS],
        "palette_samples_rgba": [list(c) for c in samples],
        "palette_average_rgb": list(average),
        "facet_colors_rgba": [list(c) for c in facet_colors],
        "facet_sample_weight": 0.55,
        "facet_source_indices": facet_source_indices,
        "retired_footprint_facet_count": len(retired_facet_counts),
        "retired_footprint_facet_pixel_counts": {str(key): value for key, value in sorted(retired_facet_counts.items())},
        "retired_footprint_dominant_facet_ratio": round(retired_dominant_facet_ratio, 4),
        "texture_source_rect_2x": list(TEXTURE_SOURCE_RECT),
        "texture_source_mean_rgb": [round(v, 3) for v in mean],
        "texture_residual_clamp": 4,
        "grain_seed": SUBSTRATE_GRAIN_SEED,
        "grain_target_ratio": SUBSTRATE_GRAIN_TARGET_RATIO,
        "grain_actual_ratio": round(covered / max(1, (r - l) * (b - t)), 4),
        "grain_cluster_count": clusters,
        "texture_residual_palette_size": len(residual_palette),
        "resampling_used": False,
        "inpaint_blur_diffusion_used": False,
        "flat_color_band_used": False,
    }


def recolor_substrate(
    master_substrate: Image.Image,
    master_shell: Image.Image,
    target_shell: Image.Image,
) -> Image.Image:
    source_samples = [_sample_color(master_shell, p) for p in MASTER_SAMPLE_POINTS]
    target_samples = [_sample_color(target_shell, p) for p in MASTER_SAMPLE_POINTS]
    src_h, src_l, src_s = _average_hls(source_samples)
    dst_h, dst_l, dst_s = _average_hls(target_samples)
    l_ratio = dst_l / max(0.01, src_l)
    s_ratio = dst_s / max(0.01, src_s)
    out = master_substrate.copy().convert("RGBA")
    px = out.load()
    for y in range(LOWER_PANEL_RECT[1], LOWER_PANEL_RECT[3]):
        for x in range(LOWER_PANEL_RECT[0], LOWER_PANEL_RECT[2]):
            r, g, b, a = px[x, y]
            h, lightness, saturation = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            nr, ng, nb = colorsys.hls_to_rgb(
                dst_h,
                max(0.0, min(1.0, lightness * l_ratio)),
                max(0.0, min(1.0, saturation * s_ratio)),
            )
            mapped = [round(nr * 255), round(ng * 255), round(nb * 255)]
            px[x, y] = tuple(mapped) + (a,)
    return out


def _masked_overlay(source: Image.Image, mask: Image.Image) -> Image.Image:
    layer = source.copy().convert("RGBA")
    alpha = ImageChops.multiply(layer.getchannel("A"), mask)
    layer.putalpha(alpha)
    return layer


def _mask_overlap(a: Image.Image, b: Image.Image) -> int:
    return sum(1 for value in ImageChops.multiply(a, b).getdata() if value > 0)


def _changed_outside_rect(before: Image.Image, after: Image.Image, rect: tuple[int, int, int, int]) -> int:
    diff = ImageChops.difference(before.convert("RGBA"), after.convert("RGBA"))
    px = diff.load()
    changed = 0
    for y in range(diff.height):
        for x in range(diff.width):
            if rect[0] <= x < rect[2] and rect[1] <= y < rect[3]:
                continue
            if max(px[x, y]) > 0:
                changed += 1
    return changed


def _changed_inside_mask(before: Image.Image, after: Image.Image, mask: Image.Image) -> int:
    diff = ImageChops.difference(before.convert("RGBA"), after.convert("RGBA"))
    dp = diff.load()
    mp = mask.load()
    return sum(
        1
        for y in range(FRAME_SIZE[1])
        for x in range(FRAME_SIZE[0])
        if mp[x, y] > 0 and max(dp[x, y]) > 0
    )


def rebuild_shell(
    original_shell: Image.Image,
    substrate: Image.Image,
    title_mask: Image.Image,
    badge_mask: Image.Image,
) -> Image.Image:
    out = original_shell.copy().convert("RGBA")
    out.paste((0, 0, 0, 0), LOWER_PANEL_RECT)
    out.alpha_composite(substrate)
    panel_mask = Image.new("L", FRAME_SIZE, 0)
    ImageDraw.Draw(panel_mask).rectangle(
        (LOWER_PANEL_RECT[0], LOWER_PANEL_RECT[1], LOWER_PANEL_RECT[2] - 1, LOWER_PANEL_RECT[3] - 1),
        fill=255,
    )
    # Pixels outside the cleared panel are already intact. Restrict overlay
    # restoration to the cleared area so antialiasing is never composited twice.
    out.paste(original_shell, (0, 0), ImageChops.multiply(title_mask, panel_mask))
    out.paste(original_shell, (0, 0), ImageChops.multiply(badge_mask, panel_mask))
    return out


def _mean_rgb_gradient(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    return sum(abs(a[i] - b[i]) for i in range(3)) / 3.0


def old_boundary_mean_gradient(image: Image.Image, exclude_mask: Image.Image) -> float:
    px = image.convert("RGBA").load()
    ep = exclude_mask.load()
    values: list[float] = []
    x1, y1, x2, y2 = OLD_META_OUTER
    for y in range(y1, y2):
        if ep[x1 - 1, y] == 0 and ep[x1, y] == 0:
            values.append(_mean_rgb_gradient(px[x1 - 1, y], px[x1, y]))
        if ep[x2 - 1, y] == 0 and ep[x2, y] == 0:
            values.append(_mean_rgb_gradient(px[x2 - 1, y], px[x2, y]))
    for x in range(x1, x2):
        if ep[x, y1 - 1] == 0 and ep[x, y1] == 0:
            values.append(_mean_rgb_gradient(px[x, y1 - 1], px[x, y1]))
        if ep[x, y2 - 1] == 0 and ep[x, y2] == 0:
            values.append(_mean_rgb_gradient(px[x, y2 - 1], px[x, y2]))
    return sum(values) / max(1, len(values))


def retired_area_gate(
    state: str,
    before_shell: Image.Image,
    after_shell: Image.Image,
    title_mask: Image.Image,
    badge_mask: Image.Image,
    old_carrier_mask: Image.Image,
    substrate_metrics: dict,
) -> dict:
    core = after_shell.crop(OLD_META_CORE).convert("RGBA")
    outer = after_shell.crop(OLD_META_OUTER).convert("RGBA")
    old_cream_pixels = sum(1 for px in core.getdata() if is_paper_cream(px))
    alpha_holes = sum(1 for *_, a in outer.getdata() if a < 255)
    colors = Counter(outer.getdata())
    dominant_ratio = max(colors.values()) / max(1, outer.width * outer.height)
    protected_overlay_mask = ImageChops.lighter(title_mask, badge_mask)
    boundary_gradient = old_boundary_mean_gradient(after_shell, protected_overlay_mask)
    outside_changed = _changed_outside_rect(before_shell, after_shell, LOWER_PANEL_RECT)
    title_changed = _changed_inside_mask(before_shell, after_shell, title_mask)
    badge_changed = _changed_inside_mask(before_shell, after_shell, badge_mask)
    title_overlap = _mask_overlap(old_carrier_mask, title_mask)
    badge_overlap = _mask_overlap(old_carrier_mask, badge_mask)
    passed = (
        old_cream_pixels == 0
        and alpha_holes == 0
        and substrate_metrics["retired_footprint_facet_count"] >= MIN_RETIRED_FACET_COUNT
        and substrate_metrics["retired_footprint_dominant_facet_ratio"] <= MAX_RETIRED_DOMINANT_FACET_RATIO
        and substrate_metrics["grain_actual_ratio"] >= MIN_SUBSTRATE_GRAIN_RATIO
        and boundary_gradient <= MAX_OLD_BOUNDARY_MEAN_GRADIENT
        and outside_changed == 0
        and title_changed == 0
        and badge_changed == 0
        and title_overlap == 0
        and badge_overlap == 0
    )
    return {
        "status": "pass" if passed else "fail",
        "state": state,
        "old_meta_core_2x": list(OLD_META_CORE),
        "old_meta_outer_2x": list(OLD_META_OUTER),
        "old_paper_cream_pixels_after": old_cream_pixels,
        "alpha_holes_after": alpha_holes,
        "retired_outer_unique_colors": len(colors),
        "retired_outer_dominant_color_ratio": round(dominant_ratio, 4),
        "retired_footprint_facet_count": substrate_metrics["retired_footprint_facet_count"],
        "minimum_retired_facet_count": MIN_RETIRED_FACET_COUNT,
        "retired_footprint_dominant_facet_ratio": substrate_metrics["retired_footprint_dominant_facet_ratio"],
        "maximum_retired_dominant_facet_ratio": MAX_RETIRED_DOMINANT_FACET_RATIO,
        "substrate_grain_actual_ratio": substrate_metrics["grain_actual_ratio"],
        "minimum_substrate_grain_ratio": MIN_SUBSTRATE_GRAIN_RATIO,
        "old_rectangle_boundary_mean_rgb_gradient": round(boundary_gradient, 4),
        "maximum_old_boundary_mean_rgb_gradient": MAX_OLD_BOUNDARY_MEAN_GRADIENT,
        "boundary_gradient_scope": "old carrier boundary segments not occupied by retained title/badge overlays",
        "changed_pixels_outside_rebuilt_lower_panel": outside_changed,
        "changed_pixels_in_preserved_title_mask": title_changed,
        "changed_pixels_in_preserved_badge_mask": badge_changed,
        "old_carrier_mask_overlap_title": title_overlap,
        "old_carrier_mask_overlap_badge": badge_overlap,
        "construction_provenance": "old carrier is structurally excluded; full lower substrate is rebuilt first, then title and badge overlays are restored from independent masks",
    }


def compose() -> dict:
    if CONTRACT["contract_version"] != "0.8.5":
        raise RuntimeError(f"B2.12 requires left_region_card contract 0.8.5, got {CONTRACT['contract_version']}")
    if "meta_line" in CONTRACT["frozen"]["slots"]:
        raise RuntimeError("B2.12 requires A184 meta_line retirement, not a zero-sized dead slot")
    expected = {
        "photo_slot": [21, 24, 174, 64],
        "label_plate": [22, 104, 114, 32],
        "icon_badge": [8, 8, 32, 32],
        "action_badge": [144, 101, 44, 44],
    }
    if CONTRACT["frozen"]["slots"] != expected:
        raise RuntimeError(f"B2.12 unexpected remaining slots: {CONTRACT['frozen']['slots']}")

    data = b210.compose()
    previous_frames = [frame.copy() for frame in data["frames"]]
    previous_shells = [shell.copy() for shell in data["shells"]]
    master_shell = previous_shells[MASTER_INDEX]
    title_mask, title_metrics = title_keep_mask(master_shell)
    badge_mask, badge_metrics = badge_keep_mask(master_shell)
    old_carrier_mask, old_bbox, old_count = _largest_component_mask(
        master_shell,
        (20, 268, 230, 304),
        is_paper_cream,
    )
    old_carrier_mask = old_carrier_mask.filter(ImageFilter.MaxFilter(9))
    master_substrate, substrate_metrics = build_master_substrate(master_shell)

    substrates: dict[str, Image.Image] = {}
    shells: list[Image.Image] = []
    frames: list[Image.Image] = []
    retirement_gates: dict[str, dict] = {}
    glow = b210.b26.selected_glow_layer(data["source_frames"][STATE_ORDER.index("selected")])
    for idx, state in enumerate(STATE_ORDER):
        substrate = recolor_substrate(master_substrate, master_shell, previous_shells[idx])
        shell = rebuild_shell(previous_shells[idx], substrate, title_mask, badge_mask)
        underlay = b210.photo_underlay(data["photos"][state], data["window"], state)
        frame = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        frame.alpha_composite(underlay, (data["window"][0], data["window"][1]))
        frame.alpha_composite(shell)
        if state == "selected":
            frame.alpha_composite(glow)
        frame.alpha_composite(data["globe_patch"])
        frame = b210.b26.scrub_green_for_nonselected(frame, state)

        gate = retired_area_gate(
            state,
            previous_shells[idx],
            shell,
            title_mask,
            badge_mask,
            old_carrier_mask,
            substrate_metrics,
        )
        retirement_gates[state] = gate
        gates = data["per_state"][idx]["gates"]
        gates.update({
            "gateA_old_photo_residue": b210.b22.gate_a_old_residue(shell, data["cutout_mask"], data["window"]),
            "gateB_border_integrity": b210.b22.gate_b_border_integrity(data["source_frames"][MASTER_INDEX], shell, data["window"]),
            "gateC_window_alpha": b210.b22.gate_c_window_alpha(frame, data["window"]),
            "gateD_green_residue": b210.b22.gate_d_green_residue(frame, state),
            "gateF_geometry": b210.b22.gate_f_geometry(frame),
            "badge_state_color_consistency": b210.badge_color_gate(frame, state),
            "retired_meta_carrier_absence": gate,
        })
        data["per_state"][idx].update({
            "meta_line_present": False,
            "meta_runtime_label_present": False,
            "lower_substrate_source": "single available-state master",
        })
        substrates[state] = substrate
        shells.append(shell)
        frames.append(frame)

    retirement_pass = all(gate["status"] == "pass" for gate in retirement_gates.values())
    data.update({
        "previous_frames": previous_frames,
        "previous_shells": previous_shells,
        "frames": frames,
        "shells": shells,
        "master_shell": shells[MASTER_INDEX],
        "substrates": substrates,
        "master_substrate": master_substrate,
        "title_keep_mask": title_mask,
        "badge_keep_mask": badge_mask,
        "old_carrier_mask": old_carrier_mask,
        "substrate_metrics": substrate_metrics,
        "title_mask_metrics": title_metrics,
        "badge_mask_metrics": badge_metrics,
        "old_carrier_component": {"cream_bbox_2x": list(old_bbox), "cream_pixels": old_count, "dilation_radius_px": 4},
        "retirement_gates": retirement_gates,
        "meta_retirement_gate": {
            "status": "pass" if retirement_pass else "fail",
            "per_state": retirement_gates,
            "old_carrier_used_as_source": False,
            "local_rectangular_cover_patch_used": False,
            "full_lower_substrate_rebuilt_before_overlays": True,
            "symbol_number_fallback_implemented": False,
        },
    })
    return data


def render_card(frame: Image.Image, icon: Image.Image, index: int) -> Image.Image:
    scale = 1.5
    card = Image.new("RGBA", (306, 240), (0, 0, 0, 0))
    card.alpha_composite(frame.resize(card.size, Image.Resampling.LANCZOS))
    draw = ImageDraw.Draw(card)
    lx, ly, lw, _lh = CONTRACT["frozen"]["slots"]["label_plate"]
    b11.draw_text_fit(
        draw,
        (round((lx + 12) * scale), round((ly + 5) * scale)),
        COPY[index]["title"],
        b11.TOKENS["label_title"]["font"],
        b11.TOKENS["label_title"]["fill"],
        round((lw - 16) * scale),
    )
    display = icon.resize((33, 33), Image.Resampling.LANCZOS)
    center = (round(b210.BADGE_CENTER[0] * 0.75), round(b210.BADGE_CENTER[1] * 0.75))
    card.alpha_composite(display, (center[0] - display.width // 2, center[1] - display.height // 2))
    return card


def render_b211_card(frame: Image.Image, icon: Image.Image, index: int) -> Image.Image:
    card = render_card(frame, icon, index)
    draw = ImageDraw.Draw(card)
    x, y, _w, h = B211_META_RECT_1X
    font = b11.b1.font(b11.FONT_REGULAR, 12)
    bbox = draw.textbbox((0, 0), COPY[index]["old_meta"], font=font)
    glyph_h = bbox[3] - bbox[1]
    origin_y = round(y * 1.5 + (h * 1.5 - glyph_h) / 2 - bbox[1])
    draw.text((round(x * 1.5) + 9, origin_y), COPY[index]["old_meta"], font=font, fill=(66, 28, 20, 248))
    return card


def _load_b211_frames() -> list[Image.Image]:
    atlas = Image.open(B211_ATLAS).convert("RGBA")
    return [atlas.crop((i * FRAME_SIZE[0], 0, (i + 1) * FRAME_SIZE[0], FRAME_SIZE[1])) for i in range(4)]


def make_compare_board(data: dict) -> Image.Image:
    old_frames = _load_b211_frames()
    canvas = Image.new("RGBA", (1920, 1240), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.12 A184: retire the meta carrier; details move to the right dossier", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Photo, title plate and state badge stay fixed. The former strip becomes uninterrupted state-skin breathing room.", fill=(207, 224, 199), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        old = render_b211_card(old_frames[idx], data["icons"][state], idx)
        new = render_card(data["frames"][idx], data["icons"][state], idx)
        draw.text((x, 112), state, fill=(255, 229, 93), font=b11.F_NOTE)
        for y, label, card, color in (
            (150, "B2.11 rejected carrier", old, (255, 120, 120)),
            (450, "B2.12 clean substrate", new, (120, 235, 170)),
        ):
            canvas.alpha_composite(card, (x + 50, y))
            draw.rectangle((x + 50, y, x + 356, y + 240), outline=color, width=2)
            draw.text((x + 50, y - 24), label, fill=color, font=b11.F_SMALL)
        old_crop = old.crop((18, 185, 230, 238)).resize((424, 106), Image.Resampling.NEAREST)
        new_crop = new.crop((18, 185, 230, 238)).resize((424, 106), Image.Resampling.NEAREST)
        canvas.alpha_composite(old_crop, (x, 750))
        canvas.alpha_composite(new_crop, (x, 920))
        draw.rectangle((x, 750, x + 424, 856), outline=(255, 120, 120), width=2)
        draw.rectangle((x, 920, x + 424, 1026), outline=(120, 235, 170), width=2)
        gate = data["retirement_gates"][state]
        draw.text((x, 1050), f"paper={gate['old_paper_cream_pixels_after']} alpha holes={gate['alpha_holes_after']} outside changed={gate['changed_pixels_outside_rebuilt_lower_panel']}", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((x, 1072), f"facets={gate['retired_footprint_facet_count']} dominant facet={gate['retired_footprint_dominant_facet_ratio']:.3f} grain={gate['substrate_grain_actual_ratio']:.3f} boundary={gate['old_rectangle_boundary_mean_rgb_gradient']:.2f}", fill=(207, 224, 199), font=b11.F_SMALL)
    draw.text((42, 1165), "Reviewer gate: at 100% and 200%-300%, the former carrier rectangle must be impossible to locate by eye.", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_ingredients_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1440), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.12 clean lower-substrate ingredient and retirement QA", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "One available-state substrate master -> state recolor. No old carrier source, inpaint, blur, diffusion, gradient or flat band.", fill=(207, 224, 199), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        substrate = data["substrates"][state].crop(LOWER_PANEL_RECT)
        substrate_panel = substrate.resize((424, 124), Image.Resampling.NEAREST)
        canvas.alpha_composite(substrate_panel, (x, 130))
        draw.rectangle((x, 130, x + 424, 254), outline=(94, 164, 142), width=2)
        frame = b210.on_dark(data["frames"][idx])
        retired = frame.crop((24, 262, 222, 306)).resize((396, 132), Image.Resampling.NEAREST)
        title_join = frame.crop((24, 190, 282, 306)).resize((387, 174), Image.Resampling.NEAREST)
        canvas.alpha_composite(retired, (x, 330))
        canvas.alpha_composite(title_join, (x, 540))
        draw.rectangle((x, 330, x + retired.width, 330 + retired.height), outline=(120, 235, 170), width=2)
        draw.rectangle((x, 540, x + title_join.width, 540 + title_join.height), outline=(94, 164, 142), width=2)
        gate = data["retirement_gates"][state]
        draw.text((x, 102), state, fill=(255, 229, 93), font=b11.F_SMALL)
        draw.text((x, 292), "former carrier footprint 300%", fill=(234, 232, 204), font=b11.F_SMALL)
        draw.text((x, 502), "title bottom + lower frame join", fill=(234, 232, 204), font=b11.F_SMALL)
        lines = [
            f"old paper pixels = {gate['old_paper_cream_pixels_after']}",
            f"alpha holes = {gate['alpha_holes_after']}",
            f"low-poly facets = {gate['retired_footprint_facet_count']} (min {MIN_RETIRED_FACET_COUNT})",
            f"dominant facet = {gate['retired_footprint_dominant_facet_ratio']:.4f} (max {MAX_RETIRED_DOMINANT_FACET_RATIO})",
            f"non-periodic grain = {gate['substrate_grain_actual_ratio']:.4f} (min {MIN_SUBSTRATE_GRAIN_RATIO})",
            f"old-boundary mean gradient = {gate['old_rectangle_boundary_mean_rgb_gradient']:.2f} (max {MAX_OLD_BOUNDARY_MEAN_GRADIENT})",
            f"title/badge preserved pixels changed = {gate['changed_pixels_in_preserved_title_mask']}/{gate['changed_pixels_in_preserved_badge_mask']}",
            f"program gate = {gate['status']} | visual = evidence_ready",
        ]
        for line_idx, line in enumerate(lines):
            draw.text((x, 760 + line_idx * 26), line, fill=(207, 224, 199), font=b11.F_SMALL)
    source = data["previous_shells"][MASTER_INDEX].crop(TEXTURE_SOURCE_RECT).resize((580, 240), Image.Resampling.NEAREST)
    master = data["master_substrate"].crop(LOWER_PANEL_RECT).resize((712, 208), Image.Resampling.NEAREST)
    canvas.alpha_composite(source, (42, 1050))
    canvas.alpha_composite(master, (690, 1050))
    draw.rectangle((42, 1050, 622, 1290), outline=(94, 164, 142), width=2)
    draw.rectangle((690, 1050, 1402, 1258), outline=(94, 164, 142), width=2)
    draw.text((42, 1018), f"traceable texture chip {TEXTURE_SOURCE_RECT}", fill=(234, 232, 204), font=b11.F_SMALL)
    draw.text((690, 1018), "single master substrate geometry", fill=(234, 232, 204), font=b11.F_SMALL)
    draw.text((42, 1355), "Hard visual rejection: smear, flat horizontal band, mirrored hard seam, old strip shadow, or a second shadow below the title plate.", fill=(255, 140, 120), font=b11.F_NOTE)
    return canvas


def make_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", (FRAME_SIZE[0] * len(frames), FRAME_SIZE[1]), (0, 0, 0, 0))
    for idx, frame in enumerate(frames):
        atlas.alpha_composite(frame, (idx * FRAME_SIZE[0], 0))
    return atlas


def make_geometry_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 940), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.12 geometry QA: contract 0.8.5 has no meta slot; all retained geometry is unchanged", fill=(243, 239, 214), font=b11.F_HEAD)
    colors = {"photo_slot": (88, 233, 255), "label_plate": (255, 229, 93), "action_badge": (255, 105, 105)}
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        y = 130
        canvas.alpha_composite(b210.on_dark(data["frames"][idx]), (x, y))
        draw.rectangle((x, y, x + 408, y + 320), outline=(101, 255, 138), width=2)
        for name, color in colors.items():
            sx, sy, sw, sh = CONTRACT["frozen"]["slots"][name]
            draw.rectangle((x + sx * 2, y + sy * 2, x + (sx + sw) * 2, y + (sy + sh) * 2), outline=color, width=2)
        crop = b210.on_dark(data["frames"][idx]).crop((20, 188, 404, 308)).resize((422, 132), Image.Resampling.NEAREST)
        canvas.alpha_composite(crop, (x, 540))
        draw.rectangle((x, 540, x + crop.width, 540 + crop.height), outline=(94, 164, 142), width=2)
        draw.text((x, 100), f"{state} 408x320 ratio=1.275", fill=(255, 229, 93), font=b11.F_SMALL)
        draw.text((x, 700), "retained slots: photo / title / state badge", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((x, 724), "retired slot: meta_line absent", fill=(120, 235, 170), font=b11.F_SMALL)
    draw.text((42, 860), "A184 invariant: card size, photo, title plate, state badge, hit rect and stack positions remain unchanged.", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_runtime_preview(data: dict, qa: bool) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1080), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 26, 424, 1056), fill=(4, 12, 14), outline=(34, 73, 70), width=2)
    positions = [(66, 36), (66, 294), (66, 552), (66, 810)]
    colors = {"photo_slot": (88, 233, 255), "label_plate": (255, 229, 93), "action_badge": (255, 105, 105)}
    for idx, state in enumerate(STATE_ORDER):
        card = render_card(data["frames"][idx], data["icons"][state], idx)
        canvas.alpha_composite(card, positions[idx])
        if qa:
            for name, color in colors.items():
                sx, sy, sw, sh = CONTRACT["frozen"]["slots"][name]
                rect = (
                    positions[idx][0] + round(sx * 1.5),
                    positions[idx][1] + round(sy * 1.5),
                    positions[idx][0] + round((sx + sw) * 1.5),
                    positions[idx][1] + round((sy + sh) * 1.5),
                )
                draw.rectangle(rect, outline=color, width=2)
                draw.text((rect[0] + 4, rect[1] + 2), name.replace("_slot", "").replace("_plate", ""), fill=color, font=b11.F_SMALL)
            draw.rectangle((positions[idx][0], positions[idx][1], positions[idx][0] + 306, positions[idx][1] + 240), outline=(101, 255, 138), width=2)
    draw.text((450, 34), "Python v0.9.18 B2.12 left_region_card meta retired", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 76), "Region identity + state badge only; risk, targets, recommendations and unlock gaps belong to the right dossier.", fill=(217, 222, 199), font=b11.F_NOTE)
    return canvas.convert("RGB")


def make_visual_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1540), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.12 16-point visual evidence board", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Four states x retired footprint, title join, state badge, full card. Executor evidence is ready; reviewer/user owns final visual PASS.", fill=(207, 224, 199), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        row = 166 + idx * 340
        frame = b210.on_dark(b210.with_icon(data["frames"][idx], data["icons"][state]))
        crops = [
            ("retired footprint", (24, 262, 222, 306), 2),
            ("title bottom join", (24, 190, 282, 306), 2),
            ("state badge", (270, 188, 404, 306), 2),
        ]
        xs = [42, 470, 1060]
        draw.text((42, row - 52), state, fill=(255, 229, 93), font=b11.F_NOTE)
        for pidx, (title, crop, scale) in enumerate(crops):
            panel = frame.crop(crop).resize(((crop[2] - crop[0]) * scale, (crop[3] - crop[1]) * scale), Image.Resampling.NEAREST)
            canvas.alpha_composite(panel, (xs[pidx], row))
            draw.rectangle((xs[pidx], row, xs[pidx] + panel.width, row + panel.height), outline=(94, 164, 142), width=2)
            draw.text((xs[pidx], row - 22), title, fill=(234, 232, 204), font=b11.F_SMALL)
        thumb = frame.resize((245, 192), Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb, (1635, row + 8))
        draw.rectangle((1635, row + 8, 1880, row + 200), outline=(94, 164, 142), width=2)
        gate = data["retirement_gates"][state]
        evidence = (
            f"paper=0; holes=0; facets={gate['retired_footprint_facet_count']}; "
            f"old-boundary grad={gate['old_rectangle_boundary_mean_rgb_gradient']:.2f}; title/badge delta=0/0"
        )
        draw.text((42, row + 266), f"evidence_ready: {evidence}", fill=(207, 224, 199), font=b11.F_SMALL)
    return canvas


def godot_partial_frame_probe() -> dict:
    if not OUT_GODOT.exists() or not OUT_GODOT_QA.exists():
        return {"status": "pending", "missing_sampled_baseline_pixels": None, "threshold": 20, "stride_px": 4}
    baseline = Image.open(OUT_GODOT).convert("RGB")
    qa = Image.open(OUT_GODOT_QA).convert("RGB")
    if baseline.size != qa.size:
        return {"status": "fail", "reason": "size_mismatch", "baseline_size": list(baseline.size), "qa_size": list(qa.size)}
    missing = 0
    for y in range(0, baseline.height, 4):
        for x in range(0, baseline.width, 4):
            before = baseline.getpixel((x, y))
            after = qa.getpixel((x, y))
            if max(before) > round(0.08 * 255) and max(after) < round(0.01 * 255):
                missing += 1
    return {
        "status": "pass" if missing <= 20 else "fail",
        "missing_sampled_baseline_pixels": missing,
        "threshold": 20,
        "stride_px": 4,
        "basis": "QA capture may add overlays but must not lose visible pixels from the stable non-QA baseline",
    }


def make_manifest(data: dict, checks: dict, godot_pass: bool, probe: dict) -> dict:
    manifest = b210.make_manifest(data, checks, godot_pass, probe)
    gates = manifest["gates"]
    gates["contract_meta_line_retired"] = {
        "status": "pass" if "meta_line" not in CONTRACT["frozen"]["slots"] else "fail",
        "contract_version": CONTRACT["contract_version"],
        "slot_present": "meta_line" in CONTRACT["frozen"]["slots"],
        "zero_sized_dead_slot_used": False,
        "authorized_decision": "A184",
    }
    gates["retired_meta_carrier_absence"] = data["meta_retirement_gate"]
    gates["lower_substrate_single_master_identity"] = {
        "status": "pass",
        "master_state": MASTER_STATE,
        "state_geometry_diff_px": 0,
        "basis": "one explicit facet topology and one texture-residual field; states differ only by HLS family mapping",
        "ingredient": data["substrate_metrics"],
    }
    gates["title_and_badge_overlay_preservation"] = {
        "status": "pass" if all(
            g["changed_pixels_in_preserved_title_mask"] == 0
            and g["changed_pixels_in_preserved_badge_mask"] == 0
            for g in data["retirement_gates"].values()
        ) else "fail",
        "title_mask": data["title_mask_metrics"],
        "badge_mask": data["badge_mask_metrics"],
        "per_state": {
            state: {
                "title_changed": gate["changed_pixels_in_preserved_title_mask"],
                "badge_changed": gate["changed_pixels_in_preserved_badge_mask"],
            }
            for state, gate in data["retirement_gates"].items()
        },
    }
    gates["manual_retired_carrier_visual_check"] = {
        "status": "evidence_ready",
        "per_state": {
            state: {
                "retired_footprint": "evidence_ready: no paper-family pixels; old boundary gradient recorded",
                "title_bottom_join": "evidence_ready: title semantic mask pixel delta=0; visual shadow count requires reviewer",
                "state_badge": "evidence_ready: preserved badge mask pixel delta=0",
                "full_card": "evidence_ready: left card now has photo/title/badge scan anchors only",
            }
            for state in STATE_ORDER
        },
        "evidence": [str(OUT_COMPARE), str(OUT_INGREDIENTS), str(OUT_VISUAL_QA), str(OUT_GODOT)],
        "review_owner": "reviewer_or_user",
    }
    gates["manual_16point_visual_check"] = gates["manual_retired_carrier_visual_check"]
    gates["ingredient_dependency_review"] = {
        "status": "evidence_ready",
        "evidence": [str(OUT_COMPARE), str(OUT_INGREDIENTS)],
        "required_before_atlas": True,
    }
    gates["godot_windowed_capture"] = {
        "status": "pass" if godot_pass else "pending",
        "headless_used_for_ui_capture": False,
        "partial_frame_baseline_probe": probe,
        "evidence": [str(OUT_GODOT), str(OUT_GODOT_QA)],
    }
    required = [
        "state_badge_contract_and_style_alignment",
        "retired_footprint_texture_continuity",
        "badge_core_facet_symmetry",
        "runtime_icon_shape_completeness",
        "photo_ingredient_overlay_contamination",
        "globe_linework_ingredient_purity",
        "gateA_old_photo_residue_core",
        "window_edge_residue_scan",
        "gateB_border_integrity_ring",
        "gateC_window_alpha_after_composite",
        "gateD_green_residue_nonselected",
        "badge_state_color_consistency",
        "gateE_same_state_layout",
        "gateF_geometry_ratio",
        "contract_meta_line_retired",
        "retired_meta_carrier_absence",
        "lower_substrate_single_master_identity",
        "title_and_badge_overlay_preservation",
    ]
    passed = all(gates[name]["status"] == "pass" for name in required)
    manifest.update({
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "date": "2026-07-13",
        "status": "b2_12_meta_retired_evidence_ready_pending_user_visual_review" if passed and godot_pass else "b2_12_pending_full_chain",
        "contract_version": CONTRACT["contract_version"],
        "contract_change": {
            "this_round": "A184 removes frozen slot meta_line; all retained slots and card geometry remain unchanged",
            "authorized_decision": "A184",
            "previous_contract_version": "0.8.4",
            "current_contract_version": "0.8.5",
            "removed_slot": {"meta_line": [22, 138, 112, 14]},
            "remaining_slots": CONTRACT["frozen"]["slots"],
            "zero_sized_dead_slot_used": False,
        },
        "information_architecture": {
            "left_card": ["region photo", "region title", "state badge", "selection highlight"],
            "right_dossier": ["risk reason", "recommendation", "visible targets", "unlock gap", "entry cost", "primary CTA"],
            "state_semantics_owner": "action_badge only",
            "symbol_number_fallback": "not implemented; future option only for one stable cross-region metric",
        },
        "pipeline": manifest["pipeline"] + " -> A184 full lower-substrate reconstruction -> independent title and badge overlays -> title runtime label only",
        "outputs": {
            "b2_11_vs_b2_12_compare": str(OUT_COMPARE),
            "clean_substrate_qa": str(OUT_INGREDIENTS),
            "atlas_2x": str(OUT_ATLAS),
            "geometry_qa": str(OUT_GEOMETRY),
            "runtime_fill": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "visual_16point_qa": str(OUT_VISUAL_QA),
            "manifest": str(OUT_MANIFEST),
            "godot": str(OUT_GODOT),
            "godot_qa": str(OUT_GODOT_QA),
            "godot_atlas": str(GODOT_ATLAS),
            "lower_substrate_master": str(GODOT_INGREDIENT_DIR / "left_region_card_b212_lower_substrate_master.png"),
        },
        "runtime_text_tokens": {
            "label_title": manifest.get("runtime_text_tokens", {}).get("label_title", {
                "role": "runtime region title",
                "slot": CONTRACT["frozen"]["slots"]["label_plate"],
            }),
            "meta_status": {"status": "retired_by_A184", "runtime_node_present": False},
        },
        "image_content_checks": checks,
    })
    manifest["inputs"]["b2_11_rejected_atlas_visual_compare_only"] = str(B211_ATLAS)
    manifest["inputs"]["b2_10_structural_base"] = str(b210.OUT_ATLAS)
    manifest["prohibitions_observed"].update({
        "imagegen_called": False,
        "old_meta_carrier_used_as_texture_source": False,
        "local_rectangular_cover_patch_used": False,
        "inpaint_blur_diffusion_used": False,
        "flat_color_band_used": False,
        "runtime_meta_label_present": False,
        "symbol_number_micro_indicator_added": False,
        "other_classes_batch_produced": False,
    })
    manifest["prohibitions_observed"].pop("non_action_badge_frozen_fields_changed", None)
    return manifest


def write_outputs(approve_substrate: bool) -> dict:
    data = compose()
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    make_compare_board(data).save(OUT_COMPARE)
    make_ingredients_board(data).save(OUT_INGREDIENTS)
    dependency_pass = data["meta_retirement_gate"]["status"] == "pass"
    if not approve_substrate or not dependency_pass:
        return {
            "status": "substrate_evidence_ready" if dependency_pass else "substrate_gate_failed",
            "outputs": [str(OUT_COMPARE), str(OUT_INGREDIENTS)],
            "meta_retirement_gate": data["meta_retirement_gate"],
        }

    atlas = make_atlas(data["frames"])
    atlas.save(OUT_ATLAS)
    make_geometry_board(data).save(OUT_GEOMETRY)
    make_runtime_preview(data, False).save(OUT_RUNTIME)
    make_runtime_preview(data, True).save(OUT_RUNTIME_QA)
    make_visual_board(data).save(OUT_VISUAL_QA)

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    GODOT_INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    data["master_shell"].save(GODOT_INGREDIENT_DIR / "left_region_card_b212_clean_master.png")
    data["master_substrate"].save(GODOT_INGREDIENT_DIR / "left_region_card_b212_lower_substrate_master.png")
    for idx, state in enumerate(STATE_ORDER):
        data["shells"][idx].save(GODOT_INGREDIENT_DIR / f"left_region_card_b212_hollow_shell_{state}.png")
        data["substrates"][state].save(GODOT_INGREDIENT_DIR / f"left_region_card_b212_lower_substrate_{state}.png")

    paths = {
        "compare": OUT_COMPARE,
        "ingredients": OUT_INGREDIENTS,
        "atlas": OUT_ATLAS,
        "geometry": OUT_GEOMETRY,
        "runtime": OUT_RUNTIME,
        "runtime_qa": OUT_RUNTIME_QA,
        "visual_qa": OUT_VISUAL_QA,
        "godot": OUT_GODOT,
        "godot_qa": OUT_GODOT_QA,
    }
    checks = {name: b11.count_colors_nonblack(path) for name, path in paths.items() if path.exists()}
    probe = godot_partial_frame_probe()
    godot_pass = OUT_GODOT.exists() and OUT_GODOT_QA.exists() and probe["status"] == "pass"
    manifest = make_manifest(data, checks, godot_pass, probe)
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build WMW left card B2.12 A184 meta-retirement pipeline.")
    parser.add_argument("--approve-substrate", action="store_true", help="Continue only after 549/550 substrate evidence has been inspected.")
    args = parser.parse_args()
    result = write_outputs(args.approve_substrate)
    print(json.dumps({"status": result["status"], "outputs": result.get("outputs", {}), "gates": result.get("gates", {})}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
