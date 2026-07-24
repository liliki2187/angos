#!/usr/bin/env python3
"""将生图输出裁切、等比缩放并装入 dossier 的 2× 生产画布。

本脚本只做透明边界裁切与尺寸归一，不绘制或重构美术内容。
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "image_gen/2026-07-22/region-task-dossier-assetization-v1/prepared"
OUTPUT_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1"

ASSETS = {
    "rt-dossier-shell-v1-2x.png": ("rt-dossier-shell-alpha-v1.png", (824, 1920), 10),
    "rt-dossier-section-plate-v1-2x.png": ("rt-dossier-section-alpha-v2-edge-clean.png", (728, 288), 8),
    "rt-dispatch-cta-mother-v1-2x.png": ("rt-dispatch-cta-alpha-v1.png", (712, 224), 8),
}


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value >= 2 else 0).getbbox()
    if bbox is None:
        raise ValueError("输入图像没有非透明像素")
    left, top, right, bottom = bbox
    return max(0, left - 2), max(0, top - 2), min(image.width, right + 2), min(image.height, bottom + 2)


def prepare(source: Path, destination: Path, size: tuple[int, int], padding: int) -> dict[str, object]:
    image = Image.open(source).convert("RGBA")
    bbox = alpha_bbox(image)
    cropped = image.crop(bbox)

    available_width = size[0] - padding * 2
    available_height = size[1] - padding * 2
    scale = min(available_width / cropped.width, available_height / cropped.height)
    resized_size = (
        max(1, round(cropped.width * scale)),
        max(1, round(cropped.height * scale)),
    )
    resized = cropped.resize(resized_size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    offset = ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2)
    canvas.alpha_composite(resized, offset)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, "PNG", optimize=True)

    final_bbox = canvas.getchannel("A").point(lambda value: 255 if value >= 2 else 0).getbbox()
    return {
        "source": source.relative_to(ROOT).as_posix(),
        "destination": destination.relative_to(ROOT).as_posix(),
        "source_size": list(image.size),
        "source_alpha_bbox": list(bbox),
        "target_size": list(size),
        "resized_art_size": list(resized_size),
        "target_alpha_bbox": list(final_bbox) if final_bbox else None,
        "padding_minimum": padding,
        "scale_mode": "uniform_fit",
    }


def main() -> None:
    report: list[dict[str, object]] = []
    for destination_name, (source_name, size, padding) in ASSETS.items():
        report.append(
            prepare(
                SOURCE_DIR / source_name,
                OUTPUT_DIR / destination_name,
                size,
                padding,
            )
        )
    report_path = OUTPUT_DIR / "preparation-report-v1.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
