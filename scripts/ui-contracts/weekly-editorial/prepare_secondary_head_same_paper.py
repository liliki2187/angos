#!/usr/bin/env python3
"""准备同纸色副头版真实生图资产。

真实生图提供全部美术内容；本脚本只复制原图、中心裁切、等比缩小与记录尺寸。
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image


PROMPT = """Generate one production-ready opaque raster UI component: the SECONDARY HEADLINE SLOT BASE for a desktop 16:9 newspaper/magazine editing interface. Reference roles are strict: image 1 is the HARD COLOR, PAPER, EDGE, AND MATERIAL REFERENCE; image 2 is ONLY the HARD GEOMETRY AND SAFE-ZONE LAYOUT REFERENCE; images 3 and 4 are the clean low-poly weekly style references. Output one flat orthographic rectangular component filled edge-to-edge, exact aspect ratio 442:342 (export intended at 884x684). It must look like it belongs to the same physical issue and the same warm paper stock as image 1: warm gray-beige / ivory paper, broad subtle low-poly value facets, restrained print tooth, narrow ivory rules, muted olive structural accent. Match image 1 paper hue and luminance closely; the main and secondary headline bases must read as two pieces of the same magazine, not two color-coded pages. Preserve image 2's geometry: outer edge, headline safe region [16,14,410,54], photo aperture [16,78,410,210], meta safe region [16,300,360,30], quiet local-action reserve [390,290,44,44]. The photo aperture itself should be a flat very dark neutral blue-black placeholder only inside that exact aperture; all surrounding page/paper surface must remain warm beige. Make the secondary hierarchy slightly quieter than the main: thinner olive rule, slightly more breathing room, but identical paper family and material. No readable text, no letters, no numbers, no glyphs, no icons, no barcode, no buttons, no status badges, no labels, no perspective, no drop shadow outside the component, no blue/cobalt/navy page surface, no yellowed antique newspaper, no dirty archival stains, no photorealistic noise. Keep all headline/meta/action safe zones visually calm and free of texture crossings."""


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo.resolve()
    original = repo / "image_gen" / "2026-07-15" / "20260715-weekly-editorial-secondary-head-same-paper-v2-original.png"
    output = repo / "gd_project" / "Assets" / "ui" / "angus_packaging" / "weekly_editorial" / "assetized" / "editorial-secondary-head-slot-base-v2.png"
    evidence = repo / "docs" / "screenshots" / "2026-07-15-weekly-editorial-same-paper-local-replace" / "secondary-head-v2-imagegen-manifest.json"

    original.parent.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.source, original)

    with Image.open(original) as opened:
        image = opened.convert("RGB")
        original_size = list(image.size)
        cropped, crop_box = crop_to_ratio(image, 884 / 684)
        resized = cropped.resize((884, 684), Image.Resampling.LANCZOS)
        resized.save(output, optimize=True)

    crop_width = crop_box[2] - crop_box[0]
    crop_height = crop_box[3] - crop_box[1]
    manifest = {
        "schema_version": 1,
        "generated_asset_policy": "真实生图提供美术内容；本脚本只做中心裁切、等比缩小与量测。",
        "asset_id": "editorial_secondary_head_slot_base",
        "prompt": PROMPT,
        "references": [
            {"path": "gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-main-head-slot-base-v1.png", "role": "纸张、颜色、边线与材质硬参考"},
            {"path": "gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-secondary-head-slot-base-v1.png", "role": "仅几何和安全区硬参考；蓝色材质已否决"},
            {"path": "design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png", "role": "clean low-poly weekly 风格参考"},
            {"path": "design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png", "role": "clean low-poly weekly 纸张与正交 UI 参考"},
        ],
        "source": original.relative_to(repo).as_posix(),
        "output": output.relative_to(repo).as_posix(),
        "original_size": original_size,
        "crop_box": crop_box,
        "crop_fraction": round(1.0 - (crop_width * crop_height) / (original_size[0] * original_size[1]), 6),
        "output_size": [884, 684],
        "non_uniform_scale": False,
        "previous_rejected_asset": "gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-secondary-head-slot-base-v1.png",
    }
    evidence.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(evidence)
    print(output, [884, 684], "crop", manifest["crop_fraction"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
