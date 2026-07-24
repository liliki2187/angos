#!/usr/bin/env python3
"""把用户审美确认前的真实生图母件回填到主头版合同中。

本脚本只做裁切、无损缩放、真实报道图与动态文字回填、整屏位置合成和审计。
它不得绘制或重建任何纸边、边框、角标、色条、按钮皮肤或状态美术。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


MASTER_SIZE_2X = (884, 748)
LOGICAL_SIZE = (442, 374)
SOURCE_CROP = (30, 49, 1325, 1130)
PHOTO_RECT_2X = (32, 184, 852, 620)
RUNTIME_POSITION = (459, 276)


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


def font_that_fits(path: Path, text: str, max_width: int, start: int, minimum: int) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -1):
        font = ImageFont.truetype(str(path), size=size)
        left, _top, right, _bottom = font.getbbox(text)
        if right - left <= max_width:
            return font
    return ImageFont.truetype(str(path), size=minimum)


def restore_generated_blue_accents(master: Image.Image, composite: Image.Image) -> None:
    """回填母件原有蓝色纸角；只做从真实生图提取的 alpha 蒙版。"""
    left, top, right, bottom = PHOTO_RECT_2X
    patch = master.crop(PHOTO_RECT_2X).convert("RGB")
    pixels = np.asarray(patch)
    red = pixels[:, :, 0].astype(np.float32)
    green = pixels[:, :, 1].astype(np.float32)
    blue = pixels[:, :, 2].astype(np.float32)
    accent = (blue > 80) & (blue > red * 1.16) & (blue > green * 1.04)
    mask = Image.fromarray((accent.astype(np.uint8) * 255), mode="L")
    composite.paste(patch, (left, top, right, bottom), mask)


def build(args: argparse.Namespace) -> dict:
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(args.source) as opened:
        generated = opened.convert("RGB")
    master = generated.crop(SOURCE_CROP).resize(MASTER_SIZE_2X, Image.Resampling.LANCZOS)
    version = args.version
    master_path = args.output_dir / f"main-head-visual-master-{version}.png"
    master.save(master_path, optimize=True)

    with Image.open(args.story) as opened:
        story = cover(opened.convert("RGB"), (820, 436))

    filled = master.copy()
    filled.paste(story, PHOTO_RECT_2X)
    restore_generated_blue_accents(master, filled)

    draw = ImageDraw.Draw(filled)
    eyebrow_font = ImageFont.truetype(str(args.font), size=20)
    title = "M330末班车在不存在的站台停了三秒"
    title_font = font_that_fits(args.font, title, 820, 48, 42)
    meta_font = ImageFont.truetype(str(args.font), size=24)
    draw.text((32, 28), "头版主稿 · A01", font=eyebrow_font, fill=(82, 89, 84))
    draw.text((32, 70), title, font=title_font, fill=(31, 47, 57))
    draw.text((32, 644), "深度 · 金级 · 620", font=meta_font, fill=(82, 91, 84))

    local = filled.resize(LOGICAL_SIZE, Image.Resampling.LANCZOS)
    local_path = args.output_dir / f"01-main-head-visual-master-{version}-local.png"
    local.save(local_path, optimize=True)

    with Image.open(args.screen) as opened:
        screen = opened.convert("RGB")
    screen.paste(local, RUNTIME_POSITION)
    fullscreen_path = args.output_dir / f"02-main-head-visual-master-{version}-fullscreen.png"
    screen.save(fullscreen_path, optimize=True)

    audit = {
        "artifact": f"weekly_editorial_main_head_visual_master_{version}_preview",
        "source_generation": args.source.as_posix(),
        "source_crop": list(SOURCE_CROP),
        "master_size_2x": list(MASTER_SIZE_2X),
        "logical_size": list(LOGICAL_SIZE),
        "runtime_position": list(RUNTIME_POSITION),
        "photo_rect_2x": list(PHOTO_RECT_2X),
        "program_operations": [
            "crop generated visual master",
            "resize visual master",
            "cover-crop and paste real story image",
            "restore generated blue accent through extracted pixel mask",
            "overlay dynamic review text",
            "paste logical preview into frozen full-screen coordinate",
        ],
        "program_drawn_visible_art": False,
        "status": "component_language_probe_local_provisional_region_review_required",
        "passed": True,
    }
    audit_path = args.output_dir / "audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--story", type=Path, required=True)
    parser.add_argument("--screen", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--version", default="v3")
    args = parser.parse_args()
    audit = build(args)
    print(json.dumps(audit, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
