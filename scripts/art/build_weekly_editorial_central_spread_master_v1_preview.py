#!/usr/bin/env python3
"""准备并装配发刊编辑中央双版区域母件审阅图。

程序只负责真实生图母件的缩放、真实报道图回填、动态文字覆盖和整屏位置合成；
不绘制或重建纸张、书脊、照片框、折角、裁切标记、工具栏或其他可见美术。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


REGION_RECT = (420, 96, 1460, 1016)
REGION_SIZE = (1040, 920)

HEADLINE_RECTS = {
    "main": (55, 194, 465, 262),
    "secondary": (575, 194, 985, 248),
    "feature_1": (51, 582, 240, 630),
    "feature_2": (280, 582, 469, 630),
    "inner_1": (571, 550, 760, 600),
    "inner_2": (800, 550, 989, 600),
}

PHOTO_RECTS = {
    "main": (55, 272, 465, 490),
    "secondary": (575, 258, 985, 468),
    "feature_1": (51, 638, 240, 808),
    "feature_2": (280, 638, 469, 808),
    "inner_1": (571, 616, 760, 790),
    "inner_2": (800, 616, 989, 790),
}

META_RECTS = {
    "main": (55, 498, 415, 540),
    "secondary": (575, 480, 935, 510),
    "feature_1": (51, 818, 188, 842),
    "feature_2": (280, 818, 417, 842),
    "inner_1": (571, 802, 708, 828),
    "inner_2": (800, 802, 937, 828),
}

WELL_TEXTURE_RECT = (90, 205, 440, 430)
ACCENT_SOURCE_RECT = (47, 164, 83, 201)

STORIES = {
    "main": {
        "title": "M330末班车在不存在的站台停了三秒",
        "id": "A01",
        "role": "头版主稿",
        "meta": "深度 · 金级 · 620",
    },
    "feature_1": {
        "title": "51区夜班货车携带会呼吸的路牌",
        "id": "A02",
        "role": "重点专题1",
        "meta": "爆料 · 金级 · 500",
    },
    "feature_2": {
        "title": "市政厅新增了一个不存在的影子部门",
        "id": "A05",
        "role": "重点专题2",
        "meta": "专栏 · 铜级 · 410",
    },
    "secondary": {
        "title": "港口广播连续七晚播报明天的潮汐",
        "id": "A03",
        "role": "副头版",
        "meta": "快讯 · 银级 · 450",
    },
    "inner_1": {
        "title": "郊区猫群一致拒绝经过蓝色电话亭",
        "id": "A06",
        "role": "内页1",
        "meta": "快讯 · 铜级 · 380",
    },
    "inner_2": {
        "title": "罗斯威尔档案第十四页拒绝复印",
        "id": "A07",
        "role": "内页2",
        "meta": "深度 · 银级 · 360",
    },
}


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_ratio = size[0] / size[1]
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        width = round(image.height * target_ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / target_ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    return image.resize(size, Image.Resampling.LANCZOS)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def font_that_fits(
    path: Path,
    text: str,
    max_width: int,
    start: int,
    minimum: int,
) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -1):
        candidate = font(path, size)
        left, _top, right, _bottom = candidate.getbbox(text)
        if right - left <= max_width:
            return candidate
    return font(path, minimum)


def wrap_chinese(
    draw: ImageDraw.ImageDraw,
    text: str,
    used_font: ImageFont.FreeTypeFont,
    max_width: int,
    max_lines: int,
) -> list[str]:
    lines: list[str] = []
    remaining = text
    while remaining and len(lines) < max_lines:
        line = ""
        for char in remaining:
            candidate = line + char
            bbox = draw.textbbox((0, 0), candidate, font=used_font)
            if bbox[2] - bbox[0] > max_width and line:
                break
            line = candidate
        lines.append(line)
        remaining = remaining[len(line) :]
    if remaining and lines:
        while lines[-1]:
            candidate = lines[-1] + "…"
            bbox = draw.textbbox((0, 0), candidate, font=used_font)
            if bbox[2] - bbox[0] <= max_width:
                lines[-1] = candidate
                break
            lines[-1] = lines[-1][:-1]
    return lines


def blue_alpha(patch: Image.Image) -> Image.Image:
    """从真实生图折角中提取蓝色 alpha。"""
    pixels = np.asarray(patch.convert("RGB"))
    red = pixels[:, :, 0].astype(np.float32)
    green = pixels[:, :, 1].astype(np.float32)
    blue = pixels[:, :, 2].astype(np.float32)
    accent = (blue > 78) & (blue > red * 1.12) & (blue > green * 1.03)
    return Image.fromarray((accent.astype(np.uint8) * 255), mode="L")


def paste_generated_accents(well_source: Image.Image, composite: Image.Image) -> None:
    """把同一个真实生图折角按合同照片框重新定位。"""
    source_patch = well_source.crop(ACCENT_SOURCE_RECT).convert("RGB")
    placements = {
        "main": (34, False),
        "secondary": (34, False),
        "feature_1": (27, False),
        "feature_2": (27, True),
        "inner_1": (27, False),
        "inner_2": (27, True),
    }
    for key, (size, mirror) in placements.items():
        patch = source_patch.resize((size, size), Image.Resampling.LANCZOS)
        mask = blue_alpha(patch)
        if mirror:
            patch = patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            mask = mask.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        left, top, right, _bottom = PHOTO_RECTS[key]
        x = right - size if mirror else left
        composite.paste(patch, (x, top), mask)


def draw_text_layer(image: Image.Image, font_path: Path) -> None:
    draw = ImageDraw.Draw(image)
    ink = (28, 43, 51)
    muted = (79, 87, 82)
    toolbar = (225, 224, 204)

    draw.text((28, 25), "本期双版", font=font(font_path, 20), fill=toolbar)
    draw.text((165, 29), "已上版6/6 · 空位0", font=font(font_path, 14), fill=(161, 171, 164))
    draw.text((930, 29), "版面就绪", font=font(font_path, 13), fill=(161, 171, 164))

    draw.text((55, 120), "第1版 · 主版", font=font(font_path, 14), fill=muted)
    main = STORIES["main"]
    draw.text((55, 195), f"{main['role']} · {main['id']}", font=font(font_path, 11), fill=muted)
    main_font = font_that_fits(font_path, main["title"], 410, 28, 22)
    draw.text((55, 214), main["title"], font=main_font, fill=ink)
    draw.text((55, 506), main["meta"], font=font(font_path, 13), fill=muted)

    draw.text((575, 120), "第2版 · 副版", font=font(font_path, 14), fill=muted)
    secondary = STORIES["secondary"]
    draw.text((575, 195), f"{secondary['role']} · {secondary['id']}", font=font(font_path, 11), fill=muted)
    secondary_font = font_that_fits(font_path, secondary["title"], 410, 22, 18)
    draw.text((575, 212), secondary["title"], font=secondary_font, fill=ink)
    draw.text((575, 485), secondary["meta"], font=font(font_path, 12), fill=muted)

    small_layout = {
        "feature_1": (51, 583, 189, 822),
        "feature_2": (280, 583, 189, 822),
        "inner_1": (571, 551, 189, 806),
        "inner_2": (800, 551, 189, 806),
    }
    for key, (x, y, width, meta_y) in small_layout.items():
        story = STORIES[key]
        draw.text((x, y), f"{story['role']} · {story['id']}", font=font(font_path, 10), fill=muted)
        title_font = font(font_path, 14)
        for index, line in enumerate(wrap_chinese(draw, story["title"], title_font, width, 2)):
            draw.text((x, y + 16 + index * 16), line, font=title_font, fill=ink)
        draw.text((x, meta_y), story["meta"], font=font(font_path, 11), fill=muted)


def prepare_geometry(screen_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(screen_path) as opened:
        screen = opened.convert("RGB")
    region = screen.crop(REGION_RECT)
    if region.size != REGION_SIZE:
        raise ValueError(f"Unexpected region size: {region.size}")
    region.save(output_path, optimize=True)


def build(args: argparse.Namespace) -> dict:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(args.source) as opened:
        generated = opened.convert("RGB")
    with Image.open(args.well_source) as opened:
        well_generated = opened.convert("RGB")
    native = generated.resize(REGION_SIZE, Image.Resampling.LANCZOS)
    well_source = well_generated.resize(REGION_SIZE, Image.Resampling.LANCZOS)
    well_texture = well_source.crop(WELL_TEXTURE_RECT)
    for rect in PHOTO_RECTS.values():
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        native.paste(well_texture.resize((width, height), Image.Resampling.LANCZOS), rect)
    paste_generated_accents(well_source, native)
    native_path = args.output_dir / "01-central-spread-master-v1-native.png"
    native.save(native_path, optimize=True)

    filled = native.copy()
    for key, rect in PHOTO_RECTS.items():
        story_path = getattr(args, key)
        with Image.open(story_path) as opened:
            story = opened.convert("RGB")
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        filled.paste(cover(story, (width, height)), rect)
    paste_generated_accents(well_source, filled)
    draw_text_layer(filled, args.font)
    filled_path = args.output_dir / "02-central-spread-master-v1-filled.png"
    filled.save(filled_path, optimize=True)

    with Image.open(args.proxy) as opened:
        future = opened.convert("RGB")
    if future.size != (1920, 1080):
        raise ValueError(f"future proxy must be 1920x1080, got {future.size}")
    future.paste(filled, (REGION_RECT[0], REGION_RECT[1]))
    future_path = args.output_dir / "03-weekly-editorial-future-state-v1.png"
    future.save(future_path, optimize=True)

    audit = {
        "artifact": "weekly_editorial_central_spread_master_v1",
        "source_generation": args.source.as_posix(),
        "well_source_generation": args.well_source.as_posix(),
        "native_size": list(native.size),
        "filled_size": list(filled.size),
        "future_state_size": list(future.size),
        "runtime_region_rect": list(REGION_RECT),
        "headline_rects": {key: list(value) for key, value in HEADLINE_RECTS.items()},
        "photo_rects": {key: list(value) for key, value in PHOTO_RECTS.items()},
        "meta_rects": {key: list(value) for key, value in META_RECTS.items()},
        "program_operations": [
            "resize real generated blank weekly master",
            "crop and resize real generated well texture into frozen contract rectangles",
            "move real generated blue-corner accents with the frozen photo rectangles",
            "cover-crop and paste six real story images",
            "reapply generated blue-corner accents after story fill",
            "overlay dynamic review text",
            "paste completed region into full-screen style proxy",
        ],
        "program_drawn_visible_art": False,
        "formal_godot_modified": False,
        "formal_ui_contract_modified": False,
        "technical_build_passed": True,
        "status": "user_rejected_editorial_layout_rework_required",
        "passed": False,
    }
    audit_path = args.output_dir / "audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-geometry", action="store_true")
    parser.add_argument("--screen", type=Path)
    parser.add_argument("--geometry-output", type=Path)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--well-source", type=Path)
    parser.add_argument("--proxy", type=Path)
    parser.add_argument("--font", type=Path)
    parser.add_argument("--main", type=Path)
    parser.add_argument("--feature-1", dest="feature_1", type=Path)
    parser.add_argument("--feature-2", dest="feature_2", type=Path)
    parser.add_argument("--secondary", type=Path)
    parser.add_argument("--inner-1", dest="inner_1", type=Path)
    parser.add_argument("--inner-2", dest="inner_2", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.prepare_geometry:
        if args.screen is None or args.geometry_output is None:
            parser.error("--prepare-geometry requires --screen and --geometry-output")
        prepare_geometry(args.screen, args.geometry_output)
        print(args.geometry_output.as_posix())
        return 0
    required = [
        args.source,
        args.well_source,
        args.proxy,
        args.font,
        args.main,
        args.feature_1,
        args.feature_2,
        args.secondary,
        args.inner_1,
        args.inner_2,
        args.output_dir,
    ]
    if any(value is None for value in required):
        parser.error("build mode requires source, proxy, font, six stories, and output-dir")
    print(json.dumps(build(args), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
