from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/artboard_v3"
OUT_IMAGE = OUT_DIR / "rt-artboard-full.png"
REFERENCE_COPY = OUT_DIR / "source-user-approved-reference.png"
TARGET_SIZE = (1920, 1080)


def resize_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGBA")
    scale = max(size[0] / image.width, size[1] / image.height)
    scaled_size = (round(image.width * scale), round(image.height * scale))
    scaled = image.resize(scaled_size, Image.Resampling.LANCZOS)
    left = (scaled.width - size[0]) // 2
    top = (scaled.height - size[1]) // 2
    return scaled.crop((left, top, left + size[0], top + size[1]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build region task artboard v3 from the user-approved reference.")
    parser.add_argument("source", type=Path, help="Path to the user-approved reference PNG.")
    args = parser.parse_args()

    if not args.source.exists():
        raise FileNotFoundError(args.source)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = Image.open(args.source)
    source.convert("RGBA").save(REFERENCE_COPY)
    artboard = resize_cover(source, TARGET_SIZE)
    artboard.save(OUT_IMAGE)

    print(f"source: {source.size}")
    print(f"wrote: {OUT_IMAGE.relative_to(ROOT)} {artboard.size}")
    print(f"copied: {REFERENCE_COPY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
