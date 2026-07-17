#!/usr/bin/env python3
"""准备发刊主头版 vertical slice 的两张真实生图资产。

程序只负责中心裁切、等比缩小、文件复制和尺寸量测，不生成或重绘美术内容。
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image


def crop_to_ratio(image: Image.Image, target_ratio: float) -> tuple[Image.Image, list[int]]:
    width, height = image.size
    source_ratio = width / height
    if abs(source_ratio - target_ratio) < 1e-9:
        return image, [0, 0, width, height]
    if source_ratio > target_ratio:
        crop_width = round(height * target_ratio)
        left = (width - crop_width) // 2
        box = (left, 0, left + crop_width, height)
    else:
        crop_height = round(width / target_ratio)
        top = (height - crop_height) // 2
        box = (0, top, width, top + crop_height)
    return image.crop(box), list(box)


def prepare(source: Path, output: Path, size: tuple[int, int]) -> dict:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
        original_size = list(image.size)
        target_ratio = size[0] / size[1]
        cropped, crop_box = crop_to_ratio(image, target_ratio)
        resized = cropped.resize(size, Image.Resampling.LANCZOS)
        output.parent.mkdir(parents=True, exist_ok=True)
        resized.save(output, optimize=True)
    crop_width = crop_box[2] - crop_box[0]
    crop_height = crop_box[3] - crop_box[1]
    return {
        "source": source.as_posix(),
        "output": output.as_posix(),
        "original_size": original_size,
        "crop_box": crop_box,
        "crop_fraction": round(1.0 - (crop_width * crop_height) / (original_size[0] * original_size[1]), 6),
        "output_size": list(size),
        "output_ratio": round(size[0] / size[1], 6),
        "upscaled": size[0] > crop_width or size[1] > crop_height,
        "non_uniform_scale": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shell-source", type=Path, required=True)
    parser.add_argument("--story-source", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo.resolve()
    imagegen_dir = repo / "image_gen" / "2026-07-14"
    runtime_dir = repo / "gd_project" / "Assets" / "ui" / "angus_packaging" / "weekly_editorial" / "assetized"
    evidence_dir = repo / "docs" / "screenshots" / "2026-07-14-weekly-editorial-assetized-vertical-slice"

    shell_original = imagegen_dir / "20260714-weekly-editorial-main-head-shell-v2-original.png"
    story_original = imagegen_dir / "20260714-weekly-editorial-m330-story-v1-original.png"
    imagegen_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.shell_source, shell_original)
    shutil.copy2(args.story_source, story_original)

    shell_output = runtime_dir / "editorial-main-head-slot-base-v1.png"
    story_output = runtime_dir / "editorial-story-m330-last-train-v1.png"
    manifest = {
        "schema_version": 1,
        "generated_asset_policy": "真实生图提供美术内容；本脚本只做中心裁切、等比缩小与量测。",
        "contract": "design/ui-contracts/weekly-editorial/main_head_slot.json",
        "assets": [
            prepare(shell_original, shell_output, (884, 748)),
            prepare(story_original, story_output, (1640, 872)),
        ],
    }
    evidence_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = evidence_dir / "main-head-vertical-slice-asset-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(manifest_path)
    for asset in manifest["assets"]:
        print(asset["output"], asset["output_size"], "crop", asset["crop_fraction"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
