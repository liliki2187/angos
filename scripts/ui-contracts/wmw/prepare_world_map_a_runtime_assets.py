"""整理世界地图 A 风格运行切片的生图母件。

本脚本只做格式整理：中心裁切、缩放和 PNG 写出，不重画美术内容。
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def center_crop_to_ratio(image: Image.Image, ratio: float) -> Image.Image:
    width, height = image.size
    current_ratio = width / height
    if abs(current_ratio - ratio) < 1e-6:
        return image
    if current_ratio > ratio:
        crop_width = round(height * ratio)
        left = (width - crop_width) // 2
        return image.crop((left, 0, left + crop_width, height))
    crop_height = round(width / ratio)
    top = (height - crop_height) // 2
    return image.crop((0, top, width, top + crop_height))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1104)
    parser.add_argument("--height", type=int, default=704)
    args = parser.parse_args()

    # 尺寸来自运行时合同；脚本不推断或重设计画幅。
    target_size = (args.width, args.height)
    target_ratio = target_size[0] / target_size[1]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(args.source) as source:
        normalized = source.convert("RGBA")
        cropped = center_crop_to_ratio(normalized, target_ratio)
        resized = cropped.resize(target_size, Image.Resampling.LANCZOS)
        resized.save(args.output, optimize=True)

    with Image.open(args.output) as result:
        if result.size != target_size:
            raise SystemExit(f"尺寸错误：{result.size} != {target_size}")
    print(f"prepared {args.output} at {target_size[0]}x{target_size[1]}")


if __name__ == "__main__":
    main()
