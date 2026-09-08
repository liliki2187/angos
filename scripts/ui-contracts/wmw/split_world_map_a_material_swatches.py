"""把 imagegen 的 2×2 材质板拆成四张运行时纹理。

程序只裁切、缩放和保存，不生成或重画任何纹理。
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


OUTPUTS = (
    "paper_warm_ivory_512.png",
    "paper_cool_locked_512.png",
    "paper_olive_ticket_512.png",
    "paper_steel_blue_512.png",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(args.source) as source:
        image = source.convert("RGBA")
        width, height = image.size
        mid_x, mid_y = width // 2, height // 2
        margin = max(8, round(min(width, height) * 0.012))
        boxes = (
            (margin, margin, mid_x - margin, mid_y - margin),
            (mid_x + margin, margin, width - margin, mid_y - margin),
            (margin, mid_y + margin, mid_x - margin, height - margin),
            (mid_x + margin, mid_y + margin, width - margin, height - margin),
        )
        for name, box in zip(OUTPUTS, boxes, strict=True):
            swatch = image.crop(box).resize((512, 512), Image.Resampling.LANCZOS)
            swatch.save(args.output_dir / name, optimize=True)
            print(f"prepared {args.output_dir / name}")


if __name__ == "__main__":
    main()
