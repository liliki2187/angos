#!/usr/bin/env python3
"""整理世界地图 A 风格生图符号：仅裁切、等比缩放、拆分与透明度校验。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def alpha_bbox(image: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("输入图没有可见像素")
    return bbox


def fit_trimmed(image: Image.Image, output_size: tuple[int, int], padding: int) -> Image.Image:
    cropped = image.crop(alpha_bbox(image))
    max_width = output_size[0] - padding * 2
    max_height = output_size[1] - padding * 2
    scale = min(max_width / cropped.width, max_height / cropped.height)
    resized = cropped.resize(
        (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", output_size, (0, 0, 0, 0))
    position = ((output_size[0] - resized.width) // 2, (output_size[1] - resized.height) // 2)
    canvas.alpha_composite(resized, position)
    return canvas


def crop_quadrant(image: Image.Image, column: int, row: int) -> Image.Image:
    left = round(image.width * column / 2)
    right = round(image.width * (column + 1) / 2)
    top = round(image.height * row / 2)
    bottom = round(image.height * (row + 1) / 2)
    return image.crop((left, top, right, bottom))


def describe(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    extrema = alpha.getextrema()
    visible = sum(1 for value in alpha.get_flattened_data() if value > 8)
    total = image.width * image.height
    corners = [
        alpha.getpixel((0, 0)),
        alpha.getpixel((image.width - 1, 0)),
        alpha.getpixel((0, image.height - 1)),
        alpha.getpixel((image.width - 1, image.height - 1)),
    ]
    return {
        "size": [image.width, image.height],
        "alpha_extrema": list(extrema),
        "transparent_corners": all(value == 0 for value in corners),
        "visible_pixel_ratio": round(visible / total, 4),
        "alpha_bbox": list(alpha_bbox(image)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    ufo = Image.open(args.source_dir / "01-ufo-note-alpha.png").convert("RGBA")
    event = Image.open(args.source_dir / "02-three-window-event-alpha.png").convert("RGBA")
    beacon_sheet = Image.open(args.source_dir / "03-eye-beacon-states-alpha.png").convert("RGBA")

    outputs: dict[str, Image.Image] = {
        "ufo_note_228x256.png": fit_trimmed(ufo, (228, 256), 5),
        "three_window_event_224x84.png": fit_trimmed(event, (224, 84), 3),
        "eye_default_144.png": fit_trimmed(crop_quadrant(beacon_sheet, 0, 0), (144, 144), 7),
        "eye_selected_144.png": fit_trimmed(crop_quadrant(beacon_sheet, 1, 0), (144, 144), 2),
        "eye_selected_warning_144.png": fit_trimmed(crop_quadrant(beacon_sheet, 0, 1), (144, 144), 2),
        "eye_locked_144.png": fit_trimmed(crop_quadrant(beacon_sheet, 1, 1), (144, 144), 7),
    }

    manifest_assets: dict[str, object] = {}
    for filename, image in outputs.items():
        destination = args.output_dir / filename
        image.save(destination, optimize=True)
        manifest_assets[filename] = describe(image)

    manifest = {
        "classification": "runtime_state_preview_symbol_replacement_v1",
        "provenance": {
            "visual_forms": "built-in imagegen reference-driven generation",
            "local_processing": "chroma-key removal, alpha trim, proportional resize, quadrant split only",
            "runtime_owns": ["dynamic Chinese copy", "region number", "region name", "state copy", "hit rect", "focus", "visibility"],
            "programmatic_final_art": False,
        },
        "assets": manifest_assets,
    }
    (args.output_dir / "world_map_a_symbol_pack_v1_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
