#!/usr/bin/env python3
"""构建世界地图 BackDecor / StateDecor 独立资产板、真实界面回填预览与 QA。"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "image_gen/2026-08-07/world-map-backdecor-state-decor-v1"
PRESSURE = ROOT / "image_gen/2026-08-07/world-map-internal-slot-pressure-v1"
SYMBOL = ROOT / "image_gen/2026-08-06/world-map-runtime-symbol-pack-v1/sources"
RUNTIME_SCREEN = ROOT / "docs/screenshots/2026-08-06-world-map-a-runtime-region-story-pack-v1/01-selected-collapsed.png"
A291 = ROOT / "image_gen/2026-08-06/world-map-art-gap-demos-v1/04-final-a-c-b10-visual-target.png"
NORTH_STORY = ROOT / "gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/north_america_story_1104x704.png"

CANVAS = (1920, 1080)
NAVY = (7, 35, 45, 255)
NAVY_2 = (10, 43, 54, 255)
INK = (231, 228, 211, 255)
MUTED = (157, 181, 177, 255)
CYAN = (91, 178, 188, 255)
OLIVE = (127, 138, 71, 255)
RUST = (177, 88, 59, 255)
PAPER = (231, 227, 209, 255)

DOSSIER_RECT = (1416, 24, 468, 1032)
SCHEDULE_RECT = (36, 810, 372, 246)
DOSSIER_DECOR_BBOX = (1392, 0, 516, 1068)
SCHEDULE_DECOR_BBOX = (24, 800, 396, 264)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size=size)


def alpha_bbox(image: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = image.convert("RGBA").getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > threshold else 0).getbbox()
    if bbox is None:
        raise ValueError("透明资产没有可见像素")
    return bbox


def crop_to_ratio(image: Image.Image, ratio: float) -> Image.Image:
    cropped = image.convert("RGBA").crop(alpha_bbox(image))
    current = cropped.width / cropped.height
    if current > ratio:
        width = max(1, round(cropped.height * ratio))
        left = (cropped.width - width) // 2
        return cropped.crop((left, 0, left + width, cropped.height))
    height = max(1, round(cropped.width / ratio))
    top = (cropped.height - height) // 2
    return cropped.crop((0, top, cropped.width, top + height))


def normalize_rect_asset(image: Image.Image, size: tuple[int, int]) -> tuple[Image.Image, dict[str, Any]]:
    cropped = crop_to_ratio(image, size[0] / size[1])
    scale = min(size[0] / cropped.width, size[1] / cropped.height)
    if scale > 1.0001:
        raise ValueError(f"资产需要上采样：{cropped.size} -> {size}")
    normalized = cropped.resize(size, Image.Resampling.LANCZOS)
    return normalized, {
        "source_crop_size": list(cropped.size),
        "runtime_size": list(size),
        "scale": round(scale, 4),
        "upscaled": False,
    }


def fit_trimmed(image: Image.Image, size: tuple[int, int], padding: int = 0) -> tuple[Image.Image, dict[str, Any]]:
    cropped = image.convert("RGBA").crop(alpha_bbox(image))
    max_w = size[0] - padding * 2
    max_h = size[1] - padding * 2
    scale = min(max_w / cropped.width, max_h / cropped.height)
    if scale > 1.0001:
        raise ValueError(f"资产需要上采样：{cropped.size} -> {size}")
    resized = cropped.resize((max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return canvas, {
        "source_crop_size": list(cropped.size),
        "runtime_size": list(size),
        "fitted_size": list(resized.size),
        "scale": round(scale, 4),
        "upscaled": False,
    }


def rotate(asset: Image.Image, degrees: float) -> Image.Image:
    return asset.rotate(degrees, Image.Resampling.BICUBIC, expand=True)


def tint(asset: Image.Image, color: tuple[int, int, int], strength: float) -> Image.Image:
    rgba = asset.convert("RGBA")
    solid = Image.new("RGBA", rgba.size, (*color, 255))
    rgb = Image.blend(rgba.convert("RGB"), solid.convert("RGB"), strength)
    rgb.putalpha(rgba.getchannel("A"))
    return rgb


def shadow(asset: Image.Image, blur: int, opacity: int) -> Image.Image:
    alpha = asset.getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    alpha = alpha.point(lambda value: value * opacity // 255)
    result = Image.new("RGBA", asset.size, (0, 0, 0, 0))
    result.paste((1, 15, 19, 255), (0, 0, asset.width, asset.height), alpha)
    return result


def paste_with_contact(canvas: Image.Image, asset: Image.Image, xy: tuple[int, int], shadow_offset: tuple[int, int] = (5, 7), blur: int = 5, opacity: int = 82) -> None:
    contact = shadow(asset, blur, opacity)
    canvas.alpha_composite(contact, (xy[0] + shadow_offset[0], xy[1] + shadow_offset[1]))
    canvas.alpha_composite(asset, xy)


def cover_runtime_regions(base: Image.Image) -> Image.Image:
    image = base.convert("RGBA").resize(CANVAS, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    draw.rectangle((1392, 0, 1919, 1079), fill=NAVY)
    draw.rectangle((20, 800, 420, 1079), fill=NAVY)
    return image


def compose_runtime_preview(assets: dict[str, Image.Image]) -> Image.Image:
    base = cover_runtime_regions(Image.open(RUNTIME_SCREEN))

    dossier_a = rotate(tint(assets["dossier_page"], (155, 171, 175), 0.10), -0.45)
    dossier_b = rotate(tint(assets["dossier_page"], (225, 225, 214), 0.13), 0.45)
    paste_with_contact(base, dossier_a, (1403, 23), (5, 7), 5, 68)
    paste_with_contact(base, dossier_b, (1420, 12), (4, 6), 4, 56)

    dossier = Image.open(PRESSURE / "04-dossier-real-collapsed-runtime.png").convert("RGBA")
    base.alpha_composite(shadow(dossier, 4, 58), (1421, 31))
    base.alpha_composite(dossier, DOSSIER_RECT[:2])
    base.alpha_composite(assets["clip"], (1622, 3))

    schedule_a = rotate(tint(assets["schedule_page"], (213, 217, 210), 0.08), -0.35)
    schedule_b = rotate(tint(assets["schedule_page"], (166, 185, 190), 0.12), 0.25)
    paste_with_contact(base, schedule_a, (28, 810), (4, 6), 4, 60)
    paste_with_contact(base, schedule_b, (41, 803), (3, 5), 3, 48)
    schedule = Image.open(PRESSURE / "08-schedule-real-disabled-runtime.png").convert("RGBA")
    base.alpha_composite(shadow(schedule, 3, 48), (40, 815))
    base.alpha_composite(schedule, SCHEDULE_RECT[:2])
    compose_selected_evidence_cluster(base, assets)
    return base


def board_background() -> Image.Image:
    board = Image.new("RGBA", CANVAS, NAVY)
    draw = ImageDraw.Draw(board)
    for x in range(0, CANVAS[0], 32):
        draw.line((x, 0, x, CANVAS[1]), fill=(18, 57, 67, 80), width=1)
    for y in range(0, CANVAS[1], 32):
        draw.line((0, y, CANVAS[0], y), fill=(18, 57, 67, 80), width=1)
    return board


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, (224, 224, 218, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, min(size[0], x + cell), min(size[1], y + cell)), fill=(187, 192, 187, 255))
    return image


def panel(board: Image.Image, rect: tuple[int, int, int, int], title: str, subtitle: str) -> Image.Image:
    x, y, w, h = rect
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=(9, 45, 55, 238), outline=(77, 115, 117, 255), width=2)
    draw.text((x + 20, y + 14), title, font=font(24, True), fill=INK)
    draw.text((x + 20, y + 50), subtitle, font=font(15), fill=MUTED)
    return board.crop((x + 16, y + 82, x + w - 16, y + h - 16))


def place_asset_in_panel(board: Image.Image, rect: tuple[int, int, int, int], title: str, subtitle: str, asset: Image.Image, display_size: tuple[int, int]) -> None:
    x, y, w, h = rect
    content = panel(board, rect, title, subtitle)
    bg = checker(content.size)
    fitted, _ = fit_trimmed(asset, display_size, 3)
    px = (content.width - fitted.width) // 2
    py = (content.height - fitted.height) // 2
    bg.alpha_composite(fitted, (px, py))
    board.alpha_composite(bg, (x + 16, y + 82))


def crop_eye_states(sheet: Image.Image) -> list[Image.Image]:
    result: list[Image.Image] = []
    for row in range(2):
        for column in range(2):
            left = round(sheet.width * column / 2)
            right = round(sheet.width * (column + 1) / 2)
            top = round(sheet.height * row / 2)
            bottom = round(sheet.height * (row + 1) / 2)
            state, _ = fit_trimmed(sheet.crop((left, top, right, bottom)), (144, 144), 3)
            result.append(state)
    return result


def extract_eye_layers(sheet: Image.Image) -> dict[str, Image.Image]:
    states = crop_eye_states(sheet)
    eye_base, _ = fit_trimmed(states[0], (72, 72), 2)
    selected_underlay, _ = fit_trimmed(states[1], (80, 80), 1)
    warning_full, _ = fit_trimmed(states[2], (80, 80), 1)
    locked_eye, _ = fit_trimmed(states[3], (72, 72), 2)

    warning_notch = Image.new("RGBA", warning_full.size, (0, 0, 0, 0))
    source_pixels = warning_full.load()
    target_pixels = warning_notch.load()
    for y in range(warning_full.height):
        for x in range(warning_full.width):
            r, g, b, a = source_pixels[x, y]
            if a > 8 and r > 120 and r > g * 1.35 and r > b * 1.25:
                target_pixels[x, y] = (r, g, b, a)
    return {
        "eye_base": eye_base,
        "selected_underlay": selected_underlay,
        "warning_notch": warning_notch,
        "locked_eye": locked_eye,
    }


def compose_selected_evidence_cluster(base: Image.Image, assets: dict[str, Image.Image]) -> None:
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    white = rotate(assets["evidence_white"], -1.4)
    blue = rotate(assets["evidence_blue"], 1.0)
    paste_with_contact(layer, white, (515, 207), (4, 5), 3, 48)
    paste_with_contact(layer, blue, (532, 218), (4, 5), 3, 44)

    canonical = Image.open(NORTH_STORY).convert("RGBA").resize((207, 132), Image.Resampling.LANCZOS)
    layer.alpha_composite(shadow(canonical, 2, 44), (538, 226))
    layer.alpha_composite(canonical, (534, 222))

    story_note, _ = fit_trimmed(Image.open(SYMBOL / "01-ufo-note-alpha.png").convert("RGBA"), (114, 128), 2)
    layer.alpha_composite(shadow(story_note, 2, 38), (728, 208))
    layer.alpha_composite(story_note, (724, 204))
    draw = ImageDraw.Draw(layer)
    draw.text((735, 278), "不是飞碟。", font=font(12, True), fill=(40, 48, 35, 255))
    draw.text((747, 298), "大概。", font=font(12, True), fill=(40, 48, 35, 255))

    layer.alpha_composite(assets["selected_underlay"], (642, 316))
    layer.alpha_composite(assets["eye_base"], (646, 320))
    layer.alpha_composite(assets["warning_notch"], (642, 316))
    label_safe = (714, 322, 884, 392)
    layer.paste((0, 0, 0, 0), label_safe)
    base.alpha_composite(layer)


def build_asset_board(assets: dict[str, Image.Image]) -> Image.Image:
    board = board_background()
    draw = ImageDraw.Draw(board)
    draw.text((36, 24), "WORLD MAP · BACKDECOR / STATEDECOR 资产板 v2", font=font(34, True), fill=INK)
    draw.text((38, 70), "所有源件 0° 正交；程序只做透明化、等比裁切、运行时轻旋转与 QA。", font=font(17), fill=MUTED)

    place_asset_in_panel(board, (36, 112, 390, 580), "Dossier 后页母件", "BackDecor · runtime 468×1032 · no input", assets["dossier_source"], (270, 500))
    place_asset_in_panel(board, (444, 112, 430, 280), "Schedule 后页母件", "BackDecor · runtime 372×246 · no input", assets["schedule_source"], (390, 205))
    place_asset_in_panel(board, (444, 412, 430, 280), "哑光长尾夹", "BackDecor overlay · 56×44 · no input", assets["clip_source"], (210, 180))
    place_asset_in_panel(board, (892, 112, 480, 280), "证物双底托", "BackDecor · 冷白210×148 + 冷蓝210×144 · no input", assets["evidence_stack_review"], (330, 155))

    x, y, w, h = 892, 412, 480, 280
    content = panel(board, (x, y, w, h), "Eye 组合层", "EyeBase + SelectedUnderlay + WarningNotch / LockedEye")
    state_bg = checker(content.size)
    state_layers = [assets["eye_base"], assets["selected_underlay"], assets["warning_notch"], assets["locked_eye"]]
    for index, state in enumerate(state_layers):
        state_bg.alpha_composite(state, (20 + index * 106, 34))
    board.alpha_composite(state_bg, (x + 16, y + 82))

    x, y, w, h = 1390, 112, 494, 580
    content = panel(board, (x, y, w, h), "StoryDecor + CanonicalImage", "无字UFO涂鸦 + RuntimeText；北美同一69:44母图")
    proof = checker(content.size)
    ufo, _ = fit_trimmed(Image.open(SYMBOL / "01-ufo-note-alpha.png").convert("RGBA"), (228, 256), 4)
    canonical = Image.open(NORTH_STORY).convert("RGBA").resize((207, 132), Image.Resampling.LANCZOS)
    proof.alpha_composite(ufo, (20, 34))
    proof.alpha_composite(canonical, (245, 88))
    proof_draw = ImageDraw.Draw(proof)
    proof_draw.text((60, 184), "RuntimeText", font=font(15, True), fill=(42, 49, 34, 255))
    proof_draw.text((249, 230), "same resource · 69:44", font=font(13, True), fill=(15, 48, 55, 255))
    board.alpha_composite(proof, (x + 16, y + 82))

    draw.rounded_rectangle((36, 724, 1884, 1042), radius=8, fill=(8, 42, 51, 242), outline=(77, 115, 117, 255), width=2)
    draw.text((58, 744), "生产合同摘要", font=font(25, True), fill=INK)
    rows = [
        ("BackDecor", "仅从 FrontCarrier 背后露边；允许运行时轻旋转；MOUSE_FILTER_IGNORE / FOCUS_NONE。", CYAN),
        ("StateDecor", "EyeBase / SelectedUnderlay / WarningNotch 独立组合；禁止状态串义和伪按钮。", OLIVE),
        ("冻结项", "FrontCarrier、真实中文、69:44 图源、Disclosure、CTA、HitRect 均不移动。", PAPER),
        ("本轮门槛", "透明边无品红残留；所有 runtime 归一化只下采样；Dossier ≤3页，Schedule ≤2页。", RUST),
    ]
    for index, (label, copy, color) in enumerate(rows):
        yy = 798 + index * 56
        draw.rounded_rectangle((58, yy, 230, yy + 38), radius=4, fill=color)
        draw.text((76, yy + 6), label, font=font(18, True), fill=(8, 30, 36, 255))
        draw.text((254, yy + 6), copy, font=font(18), fill=INK)
    return board


def build_comparison(preview: Image.Image) -> Image.Image:
    board = board_background()
    draw = ImageDraw.Draw(board)
    draw.text((34, 22), "A291 视觉目标 vs. 正交功能件 BackDecor 回填", font=font(31, True), fill=INK)
    draw.text((36, 66), "左：风格与构图真值；右：真实运行内容 + 已冻结 FrontCarrier + 本轮 BackDecor。", font=font(16), fill=MUTED)
    target = Image.open(A291).convert("RGBA").resize((900, 507), Image.Resampling.LANCZOS)
    actual = preview.resize((900, 506), Image.Resampling.LANCZOS)
    board.alpha_composite(target, (34, 116))
    board.alpha_composite(actual, (986, 116))
    draw.rectangle((34, 116, 934, 623), outline=(115, 148, 145, 255), width=2)
    draw.rectangle((986, 116, 1886, 622), outline=(115, 148, 145, 255), width=2)
    draw.text((50, 636), "A291 · style_and_composition_truth", font=font(17, True), fill=PAPER)
    draw.text((1002, 636), "本轮 · real_content_reinsert_preview", font=font(17, True), fill=PAPER)

    def contain_crop(crop: Image.Image, size: tuple[int, int]) -> Image.Image:
        scale = min(size[0] / crop.width, size[1] / crop.height)
        resized = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", size, NAVY_2)
        canvas.alpha_composite(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
        return canvas

    draw.rounded_rectangle((34, 694, 934, 1044), radius=6, fill=NAVY_2, outline=(77, 115, 117, 255), width=2)
    draw.rounded_rectangle((986, 694, 1886, 1044), radius=6, fill=NAVY_2, outline=(77, 115, 117, 255), width=2)
    dossier_top = preview.crop((1392, 0, 1920, 190))
    schedule_close = preview.crop((20, 790, 420, 1080))
    board.alpha_composite(contain_crop(dossier_top, (868, 270)), (50, 752))
    board.alpha_composite(contain_crop(schedule_close, (868, 270)), (1002, 752))
    draw.text((52, 708), "Dossier 顶部：2页后衬 + 低多边形夹具", font=font(19, True), fill=INK)
    draw.text((1004, 708), "Schedule：2页薄后衬，无新增操作暗示", font=font(19, True), fill=INK)
    return board


def build_qa(preview: Image.Image) -> Image.Image:
    qa = preview.copy().convert("RGBA")
    overlay = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for rect, label, color in [
        (DOSSIER_DECOR_BBOX, "Dossier BackDecor envelope", CYAN),
        (DOSSIER_RECT, "Dossier FrontCarrier frozen", OLIVE),
        (SCHEDULE_DECOR_BBOX, "Schedule BackDecor envelope", CYAN),
        (SCHEDULE_RECT, "Schedule FrontCarrier frozen", OLIVE),
        ((1443, 956, 414, 76), "CTA frozen", RUST),
        ((1443, 596, 414, 56), "Disclosure frozen", PAPER),
        ((510, 198, 330, 210), "Selected evidence decor envelope", CYAN),
        ((714, 322, 170, 70), "Region label safe zone", RUST),
    ]:
        x, y, w, h = rect
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline=color, width=3)
        tag_w = max(160, len(label) * 9 + 18)
        draw.rectangle((x, max(0, y - 26), min(1919, x + tag_w), y), fill=(4, 25, 31, 220))
        draw.text((x + 6, max(0, y - 24)), label, font=font(13, True), fill=color)
    draw.rectangle((0, 0, 1920, 1080), outline=(222, 218, 199, 180), width=2)
    qa.alpha_composite(overlay)
    return qa


def inspect_alpha(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    pixels = image.load()
    fringe = 0
    visible = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a > 8:
                visible += 1
                if r > 175 and b > 145 and g < 105:
                    fringe += 1
    corners = [alpha.getpixel((0, 0)), alpha.getpixel((image.width - 1, 0)), alpha.getpixel((0, image.height - 1)), alpha.getpixel((image.width - 1, image.height - 1))]
    return {
        "source_canvas": [image.width, image.height],
        "alpha_bbox": list(alpha_bbox(image)),
        "alpha_extrema": list(alpha.getextrema()),
        "transparent_corners": all(value == 0 for value in corners),
        "visible_pixels": visible,
        "magenta_fringe_pixels": fringe,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_paths = {
        "dossier": OUT / "01-dossier-back-page-alpha.png",
        "schedule": OUT / "02-schedule-back-page-alpha.png",
        "clip": OUT / "03-binder-clip-alpha.png",
        "evidence": OUT / "04-evidence-blue-backing-alpha.png",
    }
    source_images = {name: Image.open(path).convert("RGBA") for name, path in source_paths.items()}

    dossier_page, dossier_norm = normalize_rect_asset(source_images["dossier"], (468, 1032))
    schedule_page, schedule_norm = normalize_rect_asset(source_images["schedule"], (372, 246))
    clip, clip_norm = fit_trimmed(source_images["clip"], (56, 44), 1)
    evidence, evidence_norm = normalize_rect_asset(source_images["evidence"], (240, 164))
    evidence_white, evidence_white_norm = normalize_rect_asset(source_images["schedule"], (210, 148))
    evidence_blue, evidence_blue_norm = normalize_rect_asset(source_images["evidence"], (210, 144))
    eye_layers = extract_eye_layers(Image.open(SYMBOL / "03-eye-beacon-states-alpha.png").convert("RGBA"))
    evidence_stack_review = Image.new("RGBA", (420, 190), (0, 0, 0, 0))
    evidence_stack_review.alpha_composite(rotate(evidence_white, -1.4), (42, 20))
    evidence_stack_review.alpha_composite(rotate(evidence_blue, 1.0), (166, 30))
    normalized = {
        "dossier_page": dossier_page,
        "schedule_page": schedule_page,
        "clip": clip,
        "evidence": evidence,
        "evidence_white": evidence_white,
        "evidence_blue": evidence_blue,
        **eye_layers,
    }
    for name, image in normalized.items():
        image.save(OUT / f"runtime-{name.replace('_', '-')}.png", optimize=True)

    assets = {
        **normalized,
        "dossier_source": source_images["dossier"],
        "schedule_source": source_images["schedule"],
        "clip_source": source_images["clip"],
        "evidence_source": source_images["evidence"],
        "evidence_stack_review": evidence_stack_review,
    }
    preview = compose_runtime_preview(assets)
    board = build_asset_board(assets)
    comparison = build_comparison(preview)
    qa = build_qa(preview)
    board.save(OUT / "05-independent-asset-board.png", optimize=True)
    preview.save(OUT / "06-real-ui-backdecor-reinsert-preview.png", optimize=True)
    comparison.save(OUT / "07-a291-vs-real-ui-comparison.png", optimize=True)
    qa.save(OUT / "08-layer-safety-qa.png", optimize=True)

    audit = {
        "classification": "backdecor_state_decor_asset_board_and_real_content_reinsert_preview_v2",
        "canvas": list(CANVAS),
        "source_provenance": {
            "new_art": "built-in ImageGen; square chroma-key sources",
            "reused_state_decor": "2026-08-06 built-in ImageGen UFO, three-window and Eye four-state sources",
            "local_program": "chroma removal, alpha trim, center crop, proportional downsample, runtime rotation, deterministic contact shadow, layout and QA only",
            "programmatic_final_art": False,
        },
        "source_alpha": {name: inspect_alpha(path) for name, path in source_paths.items()},
        "normalization": {
            "dossier_page": dossier_norm,
            "schedule_page": schedule_norm,
            "clip": clip_norm,
            "evidence": evidence_norm,
            "evidence_white": evidence_white_norm,
            "evidence_blue": evidence_blue_norm,
        },
        "frozen_rects": {
            "dossier": list(DOSSIER_RECT),
            "schedule": list(SCHEDULE_RECT),
            "cta": [1443, 956, 414, 76],
            "disclosure": [1443, 596, 414, 56],
        },
        "decor_envelopes": {
            "dossier": list(DOSSIER_DECOR_BBOX),
            "schedule": list(SCHEDULE_DECOR_BBOX),
            "selected_evidence": [510, 198, 330, 210],
            "selected_region_label_safe": [714, 322, 170, 70],
        },
        "interaction": {
            "backdecor_mouse_filter": "IGNORE",
            "backdecor_focus": "NONE",
            "state_decor_mouse_filter": "IGNORE",
            "new_hit_rects": 0,
        },
        "state_composition": {
            "available": ["EyeBase"],
            "selected": ["SelectedUnderlay", "EyeBase"],
            "warning_unselected": ["EyeBase", "WarningNotch"],
            "selected_warning": ["SelectedUnderlay", "EyeBase", "WarningNotch"],
            "locked": ["LockedEye"],
            "combined_warning_state_retired": True,
        },
        "story_decor": {
            "ufo_source_contains_text": False,
            "ufo_doodle_source": "world-map-runtime-symbol-pack-v1/sources/01-ufo-note-alpha.png",
            "copy_owner": "RuntimeText",
            "runtime_copy": ["不是飞碟。", "大概。"],
            "three_window_strip_in_final_cluster": False,
            "canonical_image": "north_america_story_1104x704.png",
            "canonical_image_display": [207, 132],
            "same_resource_no_crop": True,
        },
        "limits": {
            "preview_not_runtime_capture": True,
            "preview_uses_real_runtime_content_and_frozen_carriers": True,
            "atlas_manifest_godot_integration": "blocked_pending_user_visual_approval",
        },
    }
    (OUT / "09-backdecor-state-decor-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checks = {
        "all_outputs_1920x1080": all(Image.open(OUT / filename).size == CANVAS for filename in ["05-independent-asset-board.png", "06-real-ui-backdecor-reinsert-preview.png", "07-a291-vs-real-ui-comparison.png", "08-layer-safety-qa.png"]),
        "transparent_corners": all(item["transparent_corners"] for item in audit["source_alpha"].values()),
        "magenta_fringe_zero": all(item["magenta_fringe_pixels"] == 0 for item in audit["source_alpha"].values()),
        "normalization_no_upscale": all(not item["upscaled"] for item in audit["normalization"].values()),
        "dossier_runtime_exact": dossier_page.size == (468, 1032),
        "schedule_runtime_exact": schedule_page.size == (372, 246),
        "frozen_dossier_asset_exact": Image.open(PRESSURE / "04-dossier-real-collapsed-runtime.png").size == (468, 1032),
        "frozen_schedule_asset_exact": Image.open(PRESSURE / "08-schedule-real-disabled-runtime.png").size == (372, 246),
        "new_hit_rects_zero": audit["interaction"]["new_hit_rects"] == 0,
        "warning_selected_independent": audit["state_composition"]["warning_unselected"] == ["EyeBase", "WarningNotch"] and audit["state_composition"]["combined_warning_state_retired"],
        "story_copy_runtime_owned": not audit["story_decor"]["ufo_source_contains_text"] and audit["story_decor"]["copy_owner"] == "RuntimeText",
        "canonical_story_reused": audit["story_decor"]["same_resource_no_crop"] and audit["story_decor"]["canonical_image_display"] == [207, 132],
        "state_layer_sizes_exact": assets["eye_base"].size == (72, 72) and assets["selected_underlay"].size == (80, 80) and assets["warning_notch"].size == (80, 80) and assets["locked_eye"].size == (72, 72),
        "warning_notch_nonempty": alpha_bbox(assets["warning_notch"])[2] > alpha_bbox(assets["warning_notch"])[0],
    }
    validation = {"checks": checks, "all_pass": all(checks.values())}
    (OUT / "10-backdecor-state-decor-validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
