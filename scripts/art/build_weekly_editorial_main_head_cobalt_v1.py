#!/usr/bin/env python3
"""把真实生图源整理为主头版 exact-size 分层预演资源。

真实生图负责纸张、钴蓝墨线和印务材质。本脚本只负责按既有合同重排到
2×画布、拆分固定层/状态层、生成透明图层与机器可读 manifest。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


LOGICAL_SIZE = (442, 374)
SOURCE_SIZE = (884, 748)
CONTENT_RECTS = {
    "headline": [16, 14, 410, 68],
    "photo": [16, 92, 410, 218],
    "meta": [16, 318, 360, 42],
    "local_replace_action": [390, 322, 44, 44],
}


def fit_ratio(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_ratio = size[0] / size[1]
    width, height = image.size
    source_ratio = width / height
    if source_ratio > target_ratio:
        crop_width = round(height * target_ratio)
        left = (width - crop_width) // 2
        image = image.crop((left, 0, left + crop_width, height))
    elif source_ratio < target_ratio:
        crop_height = round(width / target_ratio)
        top = (height - crop_height) // 2
        image = image.crop((0, top, width, top + crop_height))
    return image.resize(size, Image.Resampling.LANCZOS)


def logical_rect(rect: list[int]) -> tuple[int, int, int, int]:
    x, y, width, height = rect
    return x * 2, y * 2, (x + width) * 2, (y + height) * 2


def bracket(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: tuple[int, int, int, int], length: int, width: int) -> None:
    left, top, right, bottom = box
    points = [
        ((left, top + length), (left, top), (left + length, top)),
        ((right - length, top), (right, top), (right, top + length)),
        ((left, bottom - length), (left, bottom), (left + length, bottom)),
        ((right - length, bottom), (right, bottom), (right, bottom - length)),
    ]
    for a, b, c in points:
        draw.line([a, b, c], fill=color, width=width, joint="curve")


def alpha_stats(image: Image.Image) -> dict[str, int | float]:
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    total = image.width * image.height
    transparent = histogram[0]
    opaque = histogram[255]
    return {
        "transparent_pixels": transparent,
        "opaque_pixels": opaque,
        "partial_alpha_pixels": total - transparent - opaque,
        "nontransparent_fraction": round((total - transparent) / total, 6),
    }


def build(source_path: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(source_path) as opened:
        source = opened.convert("RGB")

    fitted = fit_ratio(source, SOURCE_SIZE)

    # 从真实生图的无字纸面与照片凹槽提取材质；程序仅做 exact-size 重排。
    paper_patch = source.crop((280, 118, 1084, 236)).resize(SOURCE_SIZE, Image.Resampling.BICUBIC)
    paper_patch = ImageEnhance.Contrast(paper_patch).enhance(0.96)
    paper_patch = ImageEnhance.Brightness(paper_patch).enhance(1.025)
    paper = paper_patch.convert("RGBA")

    # 以极低透明度回填源稿的整体低多边形纸面变化，不保留旧槽线。
    soft_source = fitted.filter(ImageFilter.GaussianBlur(radius=22)).convert("RGBA")
    soft_source.putalpha(26)
    paper = Image.alpha_composite(paper, soft_source)

    # 主头版属于页面内部槽，纸面只保留轻纹理覆盖，让母页纸色连续透出。
    paper.putalpha(54)

    base = paper.copy()
    photo_crop = source.crop((82, 278, 1282, 880)).resize((820, 436), Image.Resampling.LANCZOS)
    photo_crop = ImageEnhance.Contrast(photo_crop).enhance(0.92)
    base.alpha_composite(photo_crop.convert("RGBA"), (32, 184))

    fixed = Image.new("RGBA", SOURCE_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(fixed)
    cobalt = (18, 55, 85, 238)
    cobalt_soft = (34, 72, 104, 168)
    olive = (112, 121, 72, 224)
    mustard = (190, 153, 67, 230)
    ivory = (238, 231, 214, 232)
    deep = (5, 22, 35, 230)

    # 16px 2×安全边内的固定纸壳与印务标记。
    headline_box = logical_rect(CONTENT_RECTS["headline"])
    draw.line((headline_box[0], headline_box[3], headline_box[2], headline_box[3]), fill=cobalt_soft, width=2)
    draw.rectangle(logical_rect(CONTENT_RECTS["photo"]), outline=ivory, width=5)
    draw.rectangle(logical_rect(CONTENT_RECTS["photo"]), outline=cobalt, width=2)
    meta_box = logical_rect(CONTENT_RECTS["meta"])
    draw.line((meta_box[0], meta_box[1], meta_box[2], meta_box[1]), fill=cobalt_soft, width=2)
    bracket(draw, (28, 28, 856, 724), cobalt, 25, 5)
    bracket(draw, (32, 184, 852, 620), ivory, 18, 4)
    draw.rectangle((48, 44, 148, 54), fill=olive)
    draw.rectangle((742, 44, 812, 54), fill=mustard)
    draw.rectangle((820, 44, 842, 54), fill=mustard)

    legal = Image.new("RGBA", SOURCE_SIZE, (0, 0, 0, 0))
    legal_draw = ImageDraw.Draw(legal)
    bracket(legal_draw, (20, 20, 864, 728), (127, 145, 91, 238), 46, 7)
    bracket(legal_draw, (28, 180, 856, 624), (127, 145, 91, 198), 28, 5)

    hover = Image.new("RGBA", SOURCE_SIZE, (0, 0, 0, 0))
    hover_draw = ImageDraw.Draw(hover)
    bracket(hover_draw, (24, 24, 860, 724), (213, 225, 211, 248), 42, 7)
    bracket(hover_draw, (28, 180, 856, 624), (80, 137, 184, 228), 32, 6)

    focused = Image.new("RGBA", SOURCE_SIZE, (0, 0, 0, 0))
    focused_draw = ImageDraw.Draw(focused)
    bracket(focused_draw, (18, 18, 866, 730), (213, 193, 111, 246), 50, 8)
    action_box = logical_rect(CONTENT_RECTS["local_replace_action"])
    focused_draw.rectangle(action_box, outline=(220, 205, 150, 245), width=4)

    button = Image.new("RGBA", (88, 88), (0, 0, 0, 0))
    button_draw = ImageDraw.Draw(button)
    button_draw.polygon([(4, 12), (12, 4), (76, 4), (84, 12), (84, 76), (76, 84), (12, 84), (4, 76)], fill=(19, 65, 91, 250), outline=(226, 215, 190, 255))
    button_draw.line((12, 16, 72, 16), fill=(73, 123, 144, 255), width=3)
    button_draw.line((16, 72, 70, 72), fill=(7, 30, 43, 255), width=3)
    button_draw.polygon([(62, 8), (80, 8), (80, 26)], fill=(184, 151, 72, 238))

    assets = {
        "base-paper": base,
        "fixed-decoration": fixed,
        "state-legal": legal,
        "state-hover": hover,
        "state-focused": focused,
        "replace-action-skin": button,
    }
    entries = []
    for name, image in assets.items():
        path = output_dir / f"{name}.png"
        image.save(path, optimize=True)
        entries.append(
            {
                "id": name.replace("-", "_"),
                "path": path.as_posix(),
                "size": list(image.size),
                "mode": image.mode,
                "alpha": alpha_stats(image),
            }
        )

    composite = Image.alpha_composite(base, fixed)
    composite.save(output_dir / "assembled-idle.png", optimize=True)
    Image.alpha_composite(composite, legal).save(output_dir / "assembled-legal.png", optimize=True)
    Image.alpha_composite(composite, hover).save(output_dir / "assembled-hover.png", optimize=True)
    focused_composite = Image.alpha_composite(composite, focused)
    focused_composite.alpha_composite(button, (780, 644))
    focused_composite.save(output_dir / "assembled-focused.png", optimize=True)

    manifest = {
        "schema_version": 1,
        "artifact": "weekly_editorial_main_head_cobalt_assetization_preflight_v1",
        "source_generation": source_path.as_posix(),
        "contract": "design/ui-contracts/weekly-editorial/main_head_slot.json",
        "logical_size": list(LOGICAL_SIZE),
        "source_size_2x": list(SOURCE_SIZE),
        "runtime_position": [459, 276],
        "content_rects": CONTENT_RECTS,
        "geometry_rules": {
            "root_rotation_degrees": 0,
            "hit_rect": [0, 0, 442, 374],
            "visual_overlays_receive_input": False,
            "dynamic_text_baked": False,
            "story_art_baked": False,
            "button_text_baked": False,
        },
        "assets": entries,
        "composites": [
            "assembled-idle.png",
            "assembled-legal.png",
            "assembled-hover.png",
            "assembled-focused.png",
        ],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.source.resolve(), args.output_dir.resolve())
    print(json.dumps({"artifact": manifest["artifact"], "assets": len(manifest["assets"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
