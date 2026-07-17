# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps

import wmw_v093_left_card_b11_vertical_slice as b11
import wmw_v0916_left_card_b210_symmetric_core_pipeline as b210


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"

VERSION = "v0.9.17"
ROUND_ID = "B2.11"
ASSET_ID = "world_map_wmw_left_region_card_b2_11_meta_carrier"

OUT_COMPARE = BASE / "539-world-map-wmw-v0-9-17-left-card-b2-11-meta-carrier-compare.png"
OUT_STRESS = BASE / "540-world-map-wmw-v0-9-17-left-card-b2-11-meta-text-stress.png"
OUT_ATLAS = BASE / "541-world-map-wmw-v0-9-17-left-card-b2-11-atlas-2x.png"
OUT_GEOMETRY = BASE / "542-world-map-wmw-v0-9-17-left-card-b2-11-geometry-qa.png"
OUT_RUNTIME = BASE / "543-world-map-wmw-v0-9-17-left-card-b2-11-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "544-world-map-wmw-v0-9-17-left-card-b2-11-runtime-fill-qa.png"
OUT_VISUAL_QA = BASE / "545-world-map-wmw-v0-9-17-left-card-b2-11-meta-regression-qa.png"
OUT_MANIFEST = BASE / "546-world-map-wmw-v0-9-17-left-card-b2-11-manifest.json"
OUT_GODOT = BASE / "547-world-map-wmw-v0-9-17-left-card-b2-11-godot-single-component.png"
OUT_GODOT_QA = BASE / "548-world-map-wmw-v0-9-17-left-card-b2-11-godot-single-component-qa.png"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_INGREDIENT_DIR = GODOT_ASSET_DIR / "ingredients"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_b211_meta_carrier_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_b211_meta_carrier_manifest.json"

CONTRACT = b11.load_contract()
STATE_ORDER = b210.STATE_ORDER
FRAME_SIZE = b210.FRAME_SIZE
EXPORT_SIZE = b210.EXPORT_SIZE

COPY = [
    {"title": "北美禁区带", "meta": "红线升温 · 推荐2"},
    {"title": "欧洲灰域", "meta": "可派遣 · 线报2"},
    {"title": "非洲禁区带", "meta": "异常升温 · 高危"},
    {"title": "南美禁区带", "meta": "锁定 · 需3线报"},
]
STRESS_COPY = [
    "异常升温 · 需3线报",
    "红线升温 · 推荐2",
    "可派遣 · 线报2",
    "锁定 · 需3线报",
]

OLD_META_RECT_1X = (22, 138, 96, 10)
META_FONT = b11.b1.font(b11.FONT_REGULAR, 12)
META_GODOT_FONT_SIZE = 15
META_COLOR = (66, 28, 20, 248)
META_GODOT_COLOR = "#421c14"
META_PADDING_RUNTIME_X = 9
META_MIN_VERTICAL_MARGIN_RUNTIME = 2
META_MIN_RIGHT_MARGIN_RUNTIME = 6


def rect_2x(name: str) -> tuple[int, int, int, int]:
    x, y, w, h = CONTRACT["frozen"]["slots"][name]
    return (x * 2, y * 2, (x + w) * 2, (y + h) * 2)


META_RECT_2X = rect_2x("meta_line")
ACTION_RECT_2X = rect_2x("action_badge")


def is_paper_cream(px: tuple[int, int, int, int]) -> bool:
    r, g, b, a = px
    return a > 200 and r > 150 and g > 120 and b > 80 and r > b + 20


def measure_old_meta_paper(frame: Image.Image) -> tuple[int, int, int, int]:
    search = (20, 272, 280, 306)
    rgba = frame.convert("RGBA")
    px = rgba.load()
    points = {
        (x, y)
        for y in range(search[1], search[3])
        for x in range(search[0], search[2])
        if is_paper_cream(px[x, y])
    }
    if not points:
        raise RuntimeError("meta paper cream component not found")

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
    component = max(components, key=len)
    xs = [p[0] for p in component]
    ys = [p[1] for p in component]
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def tile_region(dst: Image.Image, tile: Image.Image, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    if right <= left or bottom <= top or tile.width <= 0 or tile.height <= 0:
        return
    iy = 0
    y = top
    while y < bottom:
        ix = 0
        x = left
        while x < right:
            piece = tile
            if ix % 2:
                piece = ImageOps.mirror(piece)
            if iy % 2:
                piece = ImageOps.flip(piece)
            width = min(piece.width, right - x)
            height = min(piece.height, bottom - y)
            dst.alpha_composite(piece.crop((0, 0, width, height)), (x, y))
            x += width
            ix += 1
        y += min(tile.height, bottom - y)
        iy += 1


def nine_slice_tile(source: Image.Image, target_size: tuple[int, int], center_texture: Image.Image) -> Image.Image:
    source = source.convert("RGBA")
    sw, sh = source.size
    tw, th = target_size
    left = right = 6
    top = bottom = 4
    if sw <= left + right or sh <= top + bottom:
        raise RuntimeError(f"meta source too small for nine-slice: {source.size}")

    out = Image.new("RGBA", target_size, (0, 0, 0, 0))
    out.alpha_composite(source.crop((0, 0, left, top)), (0, 0))
    out.alpha_composite(source.crop((sw - right, 0, sw, top)), (tw - right, 0))
    out.alpha_composite(source.crop((0, sh - bottom, left, sh)), (0, th - bottom))
    out.alpha_composite(source.crop((sw - right, sh - bottom, sw, sh)), (tw - right, th - bottom))

    tile_region(out, source.crop((left, 0, sw - right, top)), (left, 0, tw - right, top))
    tile_region(out, source.crop((left, sh - bottom, sw - right, sh)), (left, th - bottom, tw - right, th))
    tile_region(out, source.crop((0, top, left, sh - bottom)), (0, top, left, th - bottom))
    tile_region(out, source.crop((sw - right, top, sw, sh - bottom)), (tw - right, top, tw, th - bottom))
    tile_region(out, center_texture.convert("RGBA"), (left, top, tw - right, th - bottom))
    return out


def count_changed_outside(before: Image.Image, after: Image.Image, box: tuple[int, int, int, int]) -> int:
    diff = ImageChops.difference(before.convert("RGBA"), after.convert("RGBA"))
    px = diff.load()
    changed = 0
    for y in range(diff.height):
        for x in range(diff.width):
            if box[0] <= x < box[2] and box[1] <= y < box[3]:
                continue
            if max(px[x, y]) > 0:
                changed += 1
    return changed


def rebuild_meta_carrier(frame: Image.Image, state: str) -> tuple[Image.Image, Image.Image, dict]:
    old_cream = measure_old_meta_paper(frame)
    source_outer = (
        max(0, old_cream[0] - 4),
        max(0, old_cream[1] - 4),
        min(frame.width, old_cream[2] + 4),
        min(frame.height, old_cream[3] + 4),
    )
    target_outer = (
        source_outer[0],
        META_RECT_2X[1] - 4,
        META_RECT_2X[2] + 10,
        META_RECT_2X[3] + 6,
    )
    if not (
        target_outer[2] <= ACTION_RECT_2X[0]
        or target_outer[0] >= ACTION_RECT_2X[2]
        or target_outer[3] <= ACTION_RECT_2X[1]
        or target_outer[1] >= ACTION_RECT_2X[3]
    ):
        raise RuntimeError(f"meta carrier overlaps action badge: {target_outer} vs {ACTION_RECT_2X}")

    source = frame.crop(source_outer)
    # The old narrow strip contains a faint vertical paper-texture landmark. If
    # that landmark is used as the center tile it repeats as visible dividers.
    # Sample a quiet, text-free patch from the approved title paper instead;
    # old-strip corners and border bands still define the carrier silhouette.
    center_texture_box = (80, 220, 144, 244)
    center_texture = frame.crop(center_texture_box)
    center_texture_cream_ratio = sum(
        1 for px in center_texture.convert("RGBA").getdata() if is_paper_cream(px)
    ) / max(1, center_texture.width * center_texture.height)
    carrier = nine_slice_tile(
        source,
        (target_outer[2] - target_outer[0], target_outer[3] - target_outer[1]),
        center_texture,
    )
    out = frame.copy().convert("RGBA")
    out.alpha_composite(carrier, (target_outer[0], target_outer[1]))

    target_crop = out.crop(target_outer).convert("RGBA")
    alpha_holes = sum(1 for *_, a in target_crop.getdata() if a < 255)
    colors = Counter(target_crop.getdata())
    dominant_ratio = max(colors.values()) / max(1, target_crop.width * target_crop.height)
    inner = out.crop(META_RECT_2X).convert("RGBA")
    cream_ratio = sum(1 for px in inner.getdata() if is_paper_cream(px)) / max(1, inner.width * inner.height)
    outside_changed = count_changed_outside(frame, out, target_outer)
    old_contained = (
        target_outer[0] <= source_outer[0]
        and target_outer[1] <= source_outer[1]
        and target_outer[2] >= source_outer[2]
        and target_outer[3] >= source_outer[3]
    )
    badge_gap = ACTION_RECT_2X[0] - target_outer[2]
    card_bottom_gap = FRAME_SIZE[1] - target_outer[3]
    passed = (
        old_contained
        and alpha_holes == 0
        and outside_changed == 0
        and cream_ratio >= 0.72
        and dominant_ratio <= 0.25
        and center_texture_cream_ratio >= 0.95
        and badge_gap >= 10
        and card_bottom_gap >= 10
    )
    gate = {
        "status": "pass" if passed else "fail",
        "state": state,
        "source_cream_bbox_2x": list(old_cream),
        "source_outer_bbox_2x": list(source_outer),
        "target_outer_bbox_2x": list(target_outer),
        "contract_meta_line_2x": list(META_RECT_2X),
        "old_carrier_fully_covered": old_contained,
        "alpha_holes_in_target": alpha_holes,
        "changed_pixels_outside_target": outside_changed,
        "inner_cream_coverage_ratio": round(cream_ratio, 4),
        "target_unique_colors": len(colors),
        "target_dominant_color_ratio": round(dominant_ratio, 4),
        "center_texture_source_bbox_2x": list(center_texture_box),
        "center_texture_cream_ratio": round(center_texture_cream_ratio, 4),
        "target_to_action_badge_gap_px_2x": badge_gap,
        "target_to_card_bottom_gap_px_2x": card_bottom_gap,
        "construction": "old meta-strip corners/borders + measured quiet title-paper center texture; exact mirrored tiling, no resize, blur, inpaint, diffusion, or flat fill",
    }
    return out, carrier, gate


def runtime_slot_rect() -> tuple[int, int, int, int]:
    x, y, w, h = CONTRACT["frozen"]["slots"]["meta_line"]
    return (round(x * 1.5), round(y * 1.5), round((x + w) * 1.5), round((y + h) * 1.5))


def meta_text_layout(text: str) -> dict:
    slot = runtime_slot_rect()
    probe = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    raw = draw.textbbox((0, 0), text, font=META_FONT)
    glyph_w = raw[2] - raw[0]
    glyph_h = raw[3] - raw[1]
    x = slot[0] + META_PADDING_RUNTIME_X - raw[0]
    y = slot[1] + ((slot[3] - slot[1] - glyph_h) // 2) - raw[1]
    bbox = (x + raw[0], y + raw[1], x + raw[2], y + raw[3])
    margins = {
        "left": bbox[0] - slot[0],
        "top": bbox[1] - slot[1],
        "right": slot[2] - bbox[2],
        "bottom": slot[3] - bbox[3],
    }
    passed = (
        margins["left"] >= META_PADDING_RUNTIME_X
        and margins["right"] >= META_MIN_RIGHT_MARGIN_RUNTIME
        and margins["top"] >= META_MIN_VERTICAL_MARGIN_RUNTIME
        and margins["bottom"] >= META_MIN_VERTICAL_MARGIN_RUNTIME
    )
    return {
        "status": "pass" if passed else "fail",
        "text": text,
        "slot_runtime_px": list(slot),
        "draw_origin_runtime_px": [x, y],
        "glyph_bbox_runtime_px": list(bbox),
        "glyph_size_runtime_px": [glyph_w, glyph_h],
        "margins_runtime_px": margins,
        "font_size_python_px": 12,
        "godot_font_size": META_GODOT_FONT_SIZE,
    }


def compose() -> dict:
    data = b210.compose()
    if CONTRACT["contract_version"] != "0.8.4":
        raise RuntimeError(f"B2.11 requires left_region_card contract 0.8.4, got {CONTRACT['contract_version']}")
    if tuple(CONTRACT["frozen"]["slots"]["meta_line"]) != (22, 138, 112, 14):
        raise RuntimeError("B2.11 requires A179 meta_line [22,138,112,14]")

    previous_frames = [frame.copy() for frame in data["frames"]]
    previous_shells = [shell.copy() for shell in data["shells"]]
    frames: list[Image.Image] = []
    shells: list[Image.Image] = []
    carrier_patches: dict[str, Image.Image] = {}
    carrier_gates: dict[str, dict] = {}
    for idx, state in enumerate(STATE_ORDER):
        shell, _, _ = rebuild_meta_carrier(previous_shells[idx], state)
        frame, carrier, gate = rebuild_meta_carrier(previous_frames[idx], state)
        frames.append(frame)
        shells.append(shell)
        carrier_patches[state] = carrier
        carrier_gates[state] = gate
        data["per_state"][idx]["gates"]["meta_carrier_rebuild_integrity"] = gate

    actual_text = {state: meta_text_layout(COPY[idx]["meta"]) for idx, state in enumerate(STATE_ORDER)}
    stress_text = {text: meta_text_layout(text) for text in STRESS_COPY}
    text_pass = all(item["status"] == "pass" for item in [*actual_text.values(), *stress_text.values()])
    carrier_pass = all(item["status"] == "pass" for item in carrier_gates.values())

    data.update({
        "previous_frames": previous_frames,
        "frames": frames,
        "shells": shells,
        "master_shell": shells[b210.MASTER_INDEX],
        "carrier_patches": carrier_patches,
        "carrier_gates": carrier_gates,
        "meta_carrier_gate": {
            "status": "pass" if carrier_pass else "fail",
            "per_state": carrier_gates,
            "outside_target_change_required": 0,
            "no_resampling_used": True,
            "no_inpaint_or_blur_used": True,
        },
        "meta_text_capacity_gate": {
            "status": "pass" if text_pass else "fail",
            "actual_per_state": actual_text,
            "stress_strings": stress_text,
            "separator": "single middle dot with one ASCII space on each side",
            "wrap_allowed": False,
            "automatic_font_compression_allowed": False,
        },
    })
    return data


def render_card(frame: Image.Image, icon: Image.Image, index: int, revised: bool) -> Image.Image:
    scale = 1.5
    card = Image.new("RGBA", (306, 240), (0, 0, 0, 0))
    resized = frame.resize(card.size, Image.Resampling.LANCZOS)
    card.alpha_composite(resized)
    draw = ImageDraw.Draw(card)
    slots = CONTRACT["frozen"]["slots"]
    lx, ly, lw, _ = slots["label_plate"]
    b11.draw_text_fit(
        draw,
        (round((lx + 12) * scale), round((ly + 5) * scale)),
        COPY[index]["title"],
        b11.TOKENS["label_title"]["font"],
        b11.TOKENS["label_title"]["fill"],
        round((lw - 16) * scale),
    )
    if revised:
        layout = meta_text_layout(COPY[index]["meta"])
        slot = runtime_slot_rect()
        origin = layout["draw_origin_runtime_px"]
        draw.text((origin[0], origin[1]), COPY[index]["meta"], font=META_FONT, fill=META_COLOR)
    else:
        ox, oy, _, _ = OLD_META_RECT_1X
        old_text = b11.STATE_LABELS[index][1]
        draw.text((round((ox + 5) * scale), round((oy - 2) * scale)), old_text, font=b11.F_META, fill=b11.TOKENS["meta_status"]["fill"])

    display = icon.resize((33, 33), Image.Resampling.LANCZOS)
    center = (round(b210.BADGE_CENTER[0] * 0.75), round(b210.BADGE_CENTER[1] * 0.75))
    card.alpha_composite(display, (center[0] - display.width // 2, center[1] - display.height // 2))
    return card


def make_compare_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1160), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.11 meta carrier: B2.10 cramped strip -> A179 expanded paper + centered token", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Card, photo, title plate and state badge stay fixed. The paper carrier and its runtime text safe area expand together.", fill=(207, 224, 199), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        draw.text((x, 112), state, fill=(255, 229, 93), font=b11.F_NOTE)
        old = render_card(data["previous_frames"][idx], data["icons"][state], idx, False)
        new = render_card(data["frames"][idx], data["icons"][state], idx, True)
        for y, label, card, color in (
            (150, "B2.10 current", old, (255, 120, 120)),
            (450, "B2.11 expanded", new, (120, 235, 170)),
        ):
            canvas.alpha_composite(card, (x + 50, y))
            draw.rectangle((x + 50, y, x + 356, y + 240), outline=color, width=2)
            draw.text((x + 50, y - 24), label, fill=color, font=b11.F_SMALL)
        old_crop = old.crop((18, 190, 220, 236)).resize((404, 92), Image.Resampling.NEAREST)
        new_crop = new.crop((18, 190, 220, 236)).resize((404, 92), Image.Resampling.NEAREST)
        canvas.alpha_composite(old_crop, (x, 750))
        canvas.alpha_composite(new_crop, (x, 890))
        draw.rectangle((x, 750, x + 404, 842), outline=(255, 120, 120), width=2)
        draw.rectangle((x, 890, x + 404, 982), outline=(120, 235, 170), width=2)
        gate = data["carrier_gates"][state]
        margins = data["meta_text_capacity_gate"]["actual_per_state"][state]["margins_runtime_px"]
        draw.text((x, 1000), f"outside changed={gate['changed_pixels_outside_target']} | carrier/action gap={gate['target_to_action_badge_gap_px_2x']}px@2x", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((x, 1022), f"glyph margins L{margins['left']} T{margins['top']} R{margins['right']} B{margins['bottom']}px runtime", fill=(207, 224, 199), font=b11.F_SMALL)
    draw.text((42, 1090), "A179: meta_line 96x10 -> 112x14 | runtime 144x15 -> 168x21 | y=-2 removed | separator: ' · '", fill=(235, 206, 158), font=b11.F_NOTE)
    return canvas


def make_stress_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1060), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.11 meta carrier close-up + 4x text-capacity evidence", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Top: carrier close-up for texture review. Bottom: actual 168x21 runtime slot enlarged exactly 4x for glyph margins.", fill=(207, 224, 199), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        x = 42 + idx * 460
        card = render_card(data["frames"][idx], data["icons"][state], idx, True)
        crop = card.crop((18, 188, 226, 238)).resize((416, 200), Image.Resampling.NEAREST)
        canvas.alpha_composite(crop, (x, 130))
        draw.rectangle((x, 130, x + 416, 330), outline=(94, 164, 142), width=2)
        draw.text((x, 105), state, fill=(255, 229, 93), font=b11.F_SMALL)
        gate = data["carrier_gates"][state]
        draw.text((x, 350), f"source cream={gate['source_cream_bbox_2x']}", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((x, 372), f"target outer={gate['target_outer_bbox_2x']}", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((x, 394), f"colors={gate['target_unique_colors']} dominant={gate['target_dominant_color_ratio']:.3f} cream={gate['inner_cream_coverage_ratio']:.3f}", fill=(207, 224, 199), font=b11.F_SMALL)

    draw.text((42, 470), "Runtime text pressure (15px Godot token; 12px Python evidence)", fill=(243, 239, 214), font=b11.F_NOTE)
    rows = list(data["meta_text_capacity_gate"]["stress_strings"].values())
    for idx, item in enumerate(rows):
        y = 510 + idx * 110
        origin = item["draw_origin_runtime_px"]
        slot = item["slot_runtime_px"]
        slot_w = slot[2] - slot[0]
        slot_h = slot[3] - slot[1]
        base_card = data["frames"][b210.MASTER_INDEX].resize((306, 240), Image.Resampling.LANCZOS)
        slot_image = base_card.crop(tuple(slot))
        slot_draw = ImageDraw.Draw(slot_image)
        slot_draw.text(
            (origin[0] - slot[0], origin[1] - slot[1]),
            item["text"],
            font=META_FONT,
            fill=META_COLOR,
        )
        enlarged = slot_image.resize((slot_w * 4, slot_h * 4), Image.Resampling.NEAREST)
        canvas.alpha_composite(enlarged, (42, y))
        draw.rectangle((42, y, 42 + enlarged.width, y + enlarged.height), outline=(94, 164, 142), width=2)
        margins = item["margins_runtime_px"]
        draw.text((748, y + 8), item["text"], fill=(255, 229, 93), font=b11.F_NOTE)
        draw.text((748, y + 38), f"actual slot={slot_w}x{slot_h}px, shown 4x", fill=(207, 224, 199), font=b11.F_SMALL)
        draw.text((748, y + 60), f"bbox={item['glyph_bbox_runtime_px']} margins=L{margins['left']} T{margins['top']} R{margins['right']} B{margins['bottom']} status={item['status']}", fill=(207, 224, 199), font=b11.F_SMALL)
    draw.text((42, 970), "Gate: all actual + stress strings inside carrier; top/bottom >=2px, right >=6px, no wrap, no auto compression.", fill=(120, 235, 170), font=b11.F_NOTE)
    return canvas


def make_runtime_preview(data: dict, qa: bool) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1080), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 26, 424, 1056), fill=(4, 12, 14), outline=(34, 73, 70), width=2)
    positions = [(66, 36), (66, 294), (66, 552), (66, 810)]
    for idx, state in enumerate(STATE_ORDER):
        card = render_card(data["frames"][idx], data["icons"][state], idx, True)
        canvas.alpha_composite(card, positions[idx])
        if qa:
            for name, color in {
                "photo_slot": (88, 233, 255),
                "label_plate": (255, 229, 93),
                "meta_line": (255, 159, 82),
                "action_badge": (255, 105, 105),
            }.items():
                sx, sy, sw, sh = CONTRACT["frozen"]["slots"][name]
                rect = (
                    positions[idx][0] + round(sx * 1.5),
                    positions[idx][1] + round(sy * 1.5),
                    positions[idx][0] + round((sx + sw) * 1.5),
                    positions[idx][1] + round((sy + sh) * 1.5),
                )
                draw.rectangle(rect, outline=color, width=2)
            draw.rectangle((positions[idx][0], positions[idx][1], positions[idx][0] + 306, positions[idx][1] + 240), outline=(101, 255, 138), width=2)
    draw.text((450, 34), "Python v0.9.17 B2.11 left_region_card meta carrier", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((450, 76), "Expanded paper carrier + vertically centered runtime meta token; all B2.10 visual layers are preserved.", fill=(217, 222, 199), font=b11.F_NOTE)
    return canvas.convert("RGB")


def make_geometry_board(data: dict) -> Image.Image:
    board = b210.make_geometry_board(data).convert("RGBA")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1920, 84), fill=(7, 19, 21, 255))
    draw.text((42, 24), "B2.11 geometry QA: A179 meta_line 112x14; all other B2.10 geometry preserved", fill=(243, 239, 214), font=b11.F_HEAD)
    return board


def make_visual_board(data: dict) -> Image.Image:
    canvas = Image.new("RGBA", (1920, 1260), (7, 19, 21, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 24), "B2.11 per-state meta carrier regression board", fill=(243, 239, 214), font=b11.F_HEAD)
    draw.text((42, 66), "Each row: B2.10 meta -> B2.11 meta -> action badge regression -> full runtime card. Final visual PASS belongs to reviewer/user.", fill=(207, 224, 199), font=b11.F_NOTE)
    for idx, state in enumerate(STATE_ORDER):
        y = 150 + idx * 270
        old = render_card(data["previous_frames"][idx], data["icons"][state], idx, False)
        new = render_card(data["frames"][idx], data["icons"][state], idx, True)
        old_meta = old.crop((18, 188, 226, 238)).resize((416, 100), Image.Resampling.NEAREST)
        new_meta = new.crop((18, 188, 226, 238)).resize((416, 100), Image.Resampling.NEAREST)
        badge = new.crop((200, 145, 304, 238)).resize((312, 279), Image.Resampling.NEAREST)
        canvas.alpha_composite(old_meta, (190, y))
        canvas.alpha_composite(new_meta, (650, y))
        canvas.alpha_composite(badge, (1110, y - 40))
        canvas.alpha_composite(new.resize((245, 192), Image.Resampling.LANCZOS), (1570, y - 10))
        draw.text((42, y + 30), state, fill=(255, 229, 93), font=b11.F_NOTE)
        draw.text((190, y - 26), "B2.10 cramped", fill=(255, 120, 120), font=b11.F_SMALL)
        draw.text((650, y - 26), "B2.11 expanded", fill=(120, 235, 170), font=b11.F_SMALL)
        draw.text((1110, y - 66), "unchanged state badge", fill=(234, 232, 204), font=b11.F_SMALL)
        draw.text((1570, y - 36), "runtime card", fill=(234, 232, 204), font=b11.F_SMALL)
        draw.rectangle((190, y, 606, y + 100), outline=(255, 120, 120), width=2)
        draw.rectangle((650, y, 1066, y + 100), outline=(120, 235, 170), width=2)
        draw.rectangle((1110, y - 40, 1422, y + 239), outline=(94, 164, 142), width=2)
        draw.rectangle((1570, y - 10, 1815, y + 182), outline=(94, 164, 142), width=2)
        margins = data["meta_text_capacity_gate"]["actual_per_state"][state]["margins_runtime_px"]
        draw.text((650, y + 118), f"margins L{margins['left']} T{margins['top']} R{margins['right']} B{margins['bottom']} | outside target changed=0", fill=(207, 224, 199), font=b11.F_SMALL)
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
    gates["meta_carrier_rebuild_integrity"] = data["meta_carrier_gate"]
    gates["meta_text_capacity_stress"] = data["meta_text_capacity_gate"]
    gates["text_carrier_capacity"] = {
        "status": "pass" if (
            data["meta_carrier_gate"]["status"] == "pass"
            and data["meta_text_capacity_gate"]["status"] == "pass"
            and godot_pass
        ) else "pending",
        "chain": "visible_color_module_rect -> carrier_rect -> inner_rect -> runtime_glyph_bbox",
        "visible_carrier_contains_contract_slot": True,
        "normal_and_stress_copy_fit_without_wrap_or_compression": data["meta_text_capacity_gate"]["status"] == "pass",
        "target_engine_font_and_scale_verified": godot_pass,
        "carrier_texture_continuity": data["meta_carrier_gate"]["status"],
        "evidence": [str(OUT_COMPARE), str(OUT_STRESS), str(OUT_GODOT)],
    }
    gates["manual_meta_visual_check"] = {
        "status": "evidence_ready",
        "evidence": [str(OUT_COMPARE), str(OUT_STRESS), str(OUT_VISUAL_QA)],
        "review_owner": "reviewer_or_user",
    }
    gates["manual_16point_visual_check"]["evidence"] = [str(b210.OUT_VISUAL_QA), str(OUT_VISUAL_QA)]
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
        "meta_carrier_rebuild_integrity",
        "meta_text_capacity_stress",
        "text_carrier_capacity",
    ]
    passed = all(gates[name]["status"] == "pass" for name in required)
    manifest.update({
        "asset_id": ASSET_ID,
        "version": VERSION,
        "round": ROUND_ID,
        "date": "2026-07-13",
        "status": "b2_11_evidence_ready_pending_user_visual_review" if passed and godot_pass else "b2_11_pending_full_chain",
        "contract_version": CONTRACT["contract_version"],
        "contract_change": {
            "this_round": "A179 authorized meta_line [22,138,96,10] -> [22,138,112,14]",
            "authorized_decision": "A179",
            "export_size_changed": False,
            "other_frozen_fields_changed": False,
        },
        "pipeline": manifest["pipeline"] + " -> A179 measured paper nine-slice -> centered runtime meta token",
        "outputs": {
            "compare": str(OUT_COMPARE),
            "text_stress": str(OUT_STRESS),
            "atlas_2x": str(OUT_ATLAS),
            "geometry_qa": str(OUT_GEOMETRY),
            "runtime_fill": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "meta_regression_qa": str(OUT_VISUAL_QA),
            "manifest": str(OUT_MANIFEST),
            "godot": str(OUT_GODOT),
            "godot_qa": str(OUT_GODOT_QA),
            "godot_atlas": str(GODOT_ATLAS),
        },
        "runtime_text_tokens": {
            "label_title": manifest.get("runtime_text_tokens", {}).get("label_title", {}),
            "meta_status": {
                "godot_font_size": META_GODOT_FONT_SIZE,
                "python_font_px": 12,
                "color": META_GODOT_COLOR,
                "horizontal_padding_runtime_px": META_PADDING_RUNTIME_X,
                "vertical_alignment": "center",
                "manual_y_offset": 0,
                "separator": " · ",
            },
        },
        "image_content_checks": checks,
    })
    manifest["inputs"]["b2_10_atlas"] = str(b210.OUT_ATLAS)
    manifest["prohibitions_observed"].update({
        "meta_carrier_resized_or_blurred": False,
        "meta_carrier_inpainted": False,
        "meta_text_auto_compressed": False,
        "other_b2_10_layers_changed": False,
    })
    manifest["prohibitions_observed"].pop("non_action_badge_frozen_fields_changed", None)
    return manifest


def write_outputs(approve_carrier: bool) -> dict:
    data = compose()
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    make_compare_board(data).save(OUT_COMPARE)
    make_stress_board(data).save(OUT_STRESS)
    dependency_pass = data["meta_carrier_gate"]["status"] == "pass" and data["meta_text_capacity_gate"]["status"] == "pass"
    if not approve_carrier or not dependency_pass:
        return {
            "status": "carrier_evidence_ready" if dependency_pass else "carrier_gate_failed",
            "outputs": [str(OUT_COMPARE), str(OUT_STRESS)],
            "meta_carrier_gate": data["meta_carrier_gate"],
            "meta_text_capacity_gate": data["meta_text_capacity_gate"],
        }

    atlas = b11.make_atlas(data["frames"])
    atlas.save(OUT_ATLAS)
    make_geometry_board(data).save(OUT_GEOMETRY)
    make_runtime_preview(data, False).save(OUT_RUNTIME)
    make_runtime_preview(data, True).save(OUT_RUNTIME_QA)
    make_visual_board(data).save(OUT_VISUAL_QA)

    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    GODOT_INGREDIENT_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    for idx, state in enumerate(STATE_ORDER):
        data["shells"][idx].save(GODOT_INGREDIENT_DIR / f"left_region_card_b211_hollow_shell_{state}.png")
        data["carrier_patches"][state].save(GODOT_INGREDIENT_DIR / f"left_region_card_b211_meta_carrier_{state}.png")

    paths = {
        "compare": OUT_COMPARE,
        "stress": OUT_STRESS,
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
    parser = argparse.ArgumentParser(description="Build WMW left card B2.11 expanded meta carrier pipeline.")
    parser.add_argument("--approve-carrier", action="store_true", help="Continue only after 539/540 carrier evidence has been inspected.")
    args = parser.parse_args()
    result = write_outputs(args.approve_carrier)
    print(json.dumps({"status": result["status"], "outputs": result.get("outputs", {}), "gates": result.get("gates", {})}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
