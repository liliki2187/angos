#!/usr/bin/env python3
"""世界地图视觉返修局部预演：只调整既有装饰层合成，不改运行时合同。"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import build_world_map_backdecor_state_decor_v1 as v1


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "image_gen/2026-08-07/world-map-backdecor-state-decor-v1"
OUT_DIR = ROOT / "image_gen/2026-08-07/world-map-visual-refinement-preview-v1"
MAP_BOARD = ROOT / "gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/world_map_board_960x902.png"
PRESSURE = ROOT / "image_gen/2026-08-07/world-map-internal-slot-pressure-v1"
SYMBOL = ROOT / "image_gen/2026-08-06/world-map-runtime-symbol-pack-v1/sources"

CANVAS = (1920, 1080)
NO_DECOR_TEXT_SAFE_RECT = (714, 328, 156, 62)
NOTE_TEXT_SAFE_REL = (8, 74, 98, 44)
CLIP_BBOX = (1624, 4, 52, 48)
CLIP_CONTACT_RECT = (1626, 24, 48, 12)
CONNECTOR_SEGMENTS = [
    [(692, 368), (704, 368)],
    [(880, 368), (910, 368), (940, 338), (1392, 338)],
]


def load_assets() -> dict[str, Image.Image]:
    source_white = Image.open(SOURCE_DIR / "02-schedule-back-page-alpha.png").convert("RGBA")
    evidence_white, _ = v1.normalize_rect_asset(source_white, (212, 148))
    clip_source = Image.open(SOURCE_DIR / "03-binder-clip-alpha.png").convert("RGBA")
    clip, _ = v1.fit_trimmed(clip_source, (52, 48), 1)
    return {
        "dossier_page": Image.open(SOURCE_DIR / "runtime-dossier-page.png").convert("RGBA"),
        "schedule_page": Image.open(SOURCE_DIR / "runtime-schedule-page.png").convert("RGBA"),
        "evidence_white": evidence_white,
        "evidence_blue": Image.open(SOURCE_DIR / "runtime-evidence-blue.png").convert("RGBA"),
        "eye_base": Image.open(SOURCE_DIR / "runtime-eye-base.png").convert("RGBA"),
        "selected_underlay": Image.open(SOURCE_DIR / "runtime-selected-underlay.png").convert("RGBA"),
        "warning_notch": Image.open(SOURCE_DIR / "runtime-warning-notch.png").convert("RGBA"),
        "clip": clip,
    }


def contact_shadow_rect(size: tuple[int, int], blur: int, opacity: int) -> Image.Image:
    alpha = Image.new("L", size, 0)
    ImageDraw.Draw(alpha).rounded_rectangle((2, 2, size[0] - 3, size[1] - 3), radius=3, fill=opacity)
    alpha = alpha.filter(ImageFilter.GaussianBlur(blur))
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    result.paste((0, 15, 19, 255), (0, 0, size[0], size[1]), alpha)
    return result


def compose_paper_layers(base: Image.Image, assets: dict[str, Image.Image]) -> None:
    # Dossier: two differently tinted pages, unequal exposed edges, restrained contact shadows.
    far = v1.rotate(v1.tint(assets["dossier_page"], (142, 164, 169), 0.16), 0.35)
    near = v1.rotate(v1.tint(assets["dossier_page"], (220, 218, 202), 0.08), -0.25)
    v1.paste_with_contact(base, far, (1424, 16), (4, 6), 6, 50)
    v1.paste_with_contact(base, near, (1408, 30), (3, 5), 4, 46)

    dossier = Image.open(PRESSURE / "04-dossier-real-collapsed-runtime.png").convert("RGBA")
    base.alpha_composite(v1.shadow(dossier, 4, 50), (1420, 30))
    base.alpha_composite(dossier, v1.DOSSIER_RECT[:2])

    contact = contact_shadow_rect((48, 12), blur=3, opacity=84)
    base.alpha_composite(contact, CLIP_CONTACT_RECT[:2])
    base.alpha_composite(assets["clip"], CLIP_BBOX[:2])

    # Schedule: lighter two-page stack; no clip, no arrow, no third page.
    schedule_far = v1.rotate(v1.tint(assets["schedule_page"], (172, 185, 185), 0.12), -0.15)
    schedule_near = v1.rotate(v1.tint(assets["schedule_page"], (222, 218, 204), 0.07), 0.12)
    v1.paste_with_contact(base, schedule_far, (32, 814), (3, 4), 4, 44)
    v1.paste_with_contact(base, schedule_near, (40, 806), (2, 3), 3, 38)
    schedule = Image.open(PRESSURE / "08-schedule-real-disabled-runtime.png").convert("RGBA")
    base.alpha_composite(v1.shadow(schedule, 3, 40), (39, 814))
    base.alpha_composite(schedule, v1.SCHEDULE_RECT[:2])


def replace_cluster_background(base: Image.Image) -> None:
    map_board = Image.open(MAP_BOARD).convert("RGBA")
    screen_rect = (480, 188, 910, 430)
    local_rect = (
        screen_rect[0] - 432,
        screen_rect[1] - 154,
        screen_rect[2] - 432,
        screen_rect[3] - 154,
    )
    base.alpha_composite(map_board.crop(local_rect), screen_rect[:2])


def compose_selected_cluster(base: Image.Image, assets: dict[str, Image.Image]) -> None:
    replace_cluster_background(base)
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))

    # The connector remains institutional UI and stays below all evidence and text.
    line = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    line_draw = ImageDraw.Draw(line)
    for segment in CONNECTOR_SEGMENTS:
        line_draw.line(segment, fill=(72, 161, 174, 104), width=2)
    base.alpha_composite(line)

    blue = v1.rotate(assets["evidence_blue"], 0.45)
    white = ImageEnhance.Brightness(assets["evidence_white"]).enhance(0.955)
    white = v1.rotate(white, -0.35)
    v1.paste_with_contact(layer, blue, (490, 214), (3, 5), 4, 42)
    v1.paste_with_contact(layer, white, (502, 204), (3, 5), 3, 46)

    canonical = Image.open(v1.NORTH_STORY).convert("RGBA").resize((207, 132), Image.Resampling.LANCZOS)
    layer.alpha_composite(v1.shadow(canonical, 2, 36), (508, 214))
    layer.alpha_composite(canonical, (505, 212))

    note, _ = v1.fit_trimmed(Image.open(SYMBOL / "01-ufo-note-alpha.png").convert("RGBA"), (114, 128), 2)
    layer.alpha_composite(v1.shadow(note, 2, 34), (699, 195))
    layer.alpha_composite(note, (696, 192))
    note_draw = ImageDraw.Draw(layer)
    note_draw.text((706, 270), "不是飞碟。", font=v1.font(12, True), fill=(40, 48, 35, 255))
    note_draw.text((718, 290), "大概。", font=v1.font(12, True), fill=(40, 48, 35, 255))

    layer.alpha_composite(assets["selected_underlay"], (624, 332))
    layer.alpha_composite(assets["eye_base"], (628, 336))
    layer.alpha_composite(assets["warning_notch"], (624, 332))

    # The same no-decor rectangle protects all dynamic label glyphs.
    layer.paste((0, 0, 0, 0), (
        NO_DECOR_TEXT_SAFE_RECT[0],
        NO_DECOR_TEXT_SAFE_RECT[1],
        NO_DECOR_TEXT_SAFE_RECT[0] + NO_DECOR_TEXT_SAFE_RECT[2],
        NO_DECOR_TEXT_SAFE_RECT[1] + NO_DECOR_TEXT_SAFE_RECT[3],
    ))
    base.alpha_composite(layer)

    # One map label, no repeated red risk sentence. Dossier owns the complete risk wording.
    draw = ImageDraw.Draw(base)
    draw.text((714, 340), "01  北美禁区带", font=v1.font(17), fill=(224, 222, 205, 255))


def build_after(assets: dict[str, Image.Image]) -> Image.Image:
    base = v1.cover_runtime_regions(Image.open(v1.RUNTIME_SCREEN))
    compose_paper_layers(base, assets)
    compose_selected_cluster(base, assets)
    return base


def crop_panel(image: Image.Image, rect: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    x, y, w, h = rect
    crop = image.crop((x, y, x + w, y + h)).convert("RGB")
    scale = min(size[0] / crop.width, size[1] / crop.height)
    resized = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    result = Image.new("RGB", size, (7, 35, 45))
    result.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return result


def paper_pair_panel(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    result = Image.new("RGB", size, (7, 35, 45))
    draw = ImageDraw.Draw(result)
    half = (size[0] - 18) // 2
    schedule = crop_panel(image, (20, 790, 410, 280), (half, size[1] - 42))
    dossier = crop_panel(image, (1392, 0, 516, 240), (half, size[1] - 42))
    result.paste(schedule, (0, 42))
    result.paste(dossier, (half + 18, 42))
    draw.text((10, 8), "Schedule", font=v1.font(17, True), fill=(236, 230, 207))
    draw.text((half + 28, 8), "Dossier 顶部 / 夹具", font=v1.font(17, True), fill=(236, 230, 207))
    draw.rectangle((half + 7, 0, half + 11, size[1]), fill=(116, 145, 104))
    return result


def build_comparison(before: Image.Image, after: Image.Image) -> Image.Image:
    board = Image.new("RGB", CANVAS, (7, 31, 39))
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "世界地图视觉返修 · 局部改前 / 改后预演", font=v1.font(36, True), fill=(236, 230, 207))
    draw.text((44, 76), "只重排现有 BackDecor / StateDecor；FrontCarrier、图源、文字槽和 HitRect 不动", font=v1.font(18), fill=(151, 179, 176))

    columns = [(42, "改前", before), (974, "改后", after)]
    for x, label, image in columns:
        draw.text((x, 122), label, font=v1.font(28, True), fill=(236, 230, 207))
        evidence = crop_panel(image, (488, 180, 410, 250), (864, 430))
        paper = paper_pair_panel(image, (864, 360))
        board.paste(evidence, (x, 166))
        board.paste(paper, (x, 628))
        draw.rectangle((x, 166, x + 864, 596), outline=(194, 83, 63), width=3)
        draw.rectangle((x, 628, x + 864, 988), outline=(116, 145, 104), width=3)

    draw.text((42, 1012), "证据簇：照片为主证据、Eye为状态、便签为趣味；地图不再重复红字。", font=v1.font(18, True), fill=(236, 230, 207))
    draw.text((974, 1012), "纸层：Dossier更重、Schedule更轻；厚度来自色差与接触，不靠新增物件。", font=v1.font(18, True), fill=(236, 230, 207))
    return board


def alpha_bbox_on_canvas(asset: Image.Image, xy: tuple[int, int]) -> list[int]:
    bbox = v1.alpha_bbox(asset)
    return [xy[0] + bbox[0], xy[1] + bbox[1], xy[0] + bbox[2], xy[1] + bbox[3]]


def connector_safe_rect_intersection() -> bool:
    safe_x0, safe_y0, safe_w, safe_h = NO_DECOR_TEXT_SAFE_RECT
    safe_x1, safe_y1 = safe_x0 + safe_w, safe_y0 + safe_h
    for segment in CONNECTOR_SEGMENTS:
        for start, end in zip(segment, segment[1:]):
            min_x, max_x = sorted((start[0], end[0]))
            min_y, max_y = sorted((start[1], end[1]))
            if max_x >= safe_x0 and min_x <= safe_x1 and max_y >= safe_y0 and min_y <= safe_y1:
                return True
    return False


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assets = load_assets()
    before = Image.open(SOURCE_DIR / "06-real-ui-backdecor-reinsert-preview.png").convert("RGBA")
    after = build_after(assets)
    comparison = build_comparison(before, after)

    after_path = OUT_DIR / "01-full-screen-refined-preview.png"
    comparison_path = OUT_DIR / "02-before-after-local-comparison.png"
    audit_path = OUT_DIR / "03-visual-refinement-audit.json"
    after.save(after_path, optimize=True)
    comparison.save(comparison_path, optimize=True)

    clip_alpha = alpha_bbox_on_canvas(assets["clip"], CLIP_BBOX[:2])
    audit = {
        "classification": "visual_previsualization_only_no_runtime_landing",
        "canvas": list(CANVAS),
        "frozen_rects": {
            "dossier": list(v1.DOSSIER_RECT),
            "schedule": list(v1.SCHEDULE_RECT),
            "hero": [1443, 174, 414, 264],
            "disclosure": [1443, 596, 414, 56],
            "cta": [1443, 956, 414, 76],
        },
        "selected_cluster": {
            "no_decor_text_safe_rect": list(NO_DECOR_TEXT_SAFE_RECT),
            "note_text_safe_rel": list(NOTE_TEXT_SAFE_REL),
            "connector_segments": CONNECTOR_SEGMENTS,
            "connector_vs_text_safe_rect_intersection": connector_safe_rect_intersection(),
            "connector_vs_text_safe_rect_pass": not connector_safe_rect_intersection(),
            "map_risk_text": "removed; warning notch only",
            "canonical_size": [207, 132],
            "canonical_ratio_pass": 207 * 44 == 132 * 69,
        },
        "clip": {
            "clip_bbox_contract": list(CLIP_BBOX),
            "contact_rect": list(CLIP_CONTACT_RECT),
            "final_alpha_bbox": clip_alpha,
            "top_clearance_pass": clip_alpha[1] >= 4,
            "inside_canvas_pass": 0 <= clip_alpha[0] and clip_alpha[2] <= 1920 and clip_alpha[3] <= 1080,
        },
        "interaction": {
            "new_controls": 0,
            "new_hit_rects": 0,
            "front_carrier_moved": False,
            "runtime_landing": False,
        },
        "outputs": [str(after_path.relative_to(ROOT)), str(comparison_path.relative_to(ROOT))],
    }
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(after_path)
    print(comparison_path)
    print(audit_path)


if __name__ == "__main__":
    main()
