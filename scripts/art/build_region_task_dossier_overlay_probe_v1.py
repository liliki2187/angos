#!/usr/bin/env python3
"""从同一张生图母件提取 dossier 叠印层，并生成可复核的拆分板。

本脚本只做尺寸归一、裁切、透明遮罩、缩放、拼接和 QA 标注；
不程序绘制任何正式美术纹理。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
TARGET_SIZE = (824, 1920)

BASE_PATH = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1/rt-dossier-shell-v1-2x.png"
CTA_PATH = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1/rt-dispatch-cta-mother-v1-2x.png"

ART_ROOT = ROOT / "design/art-direction/region-task-board/dossier-overlay-stitch-probe-v1"
SOURCE_DIR = ART_ROOT / "source"
LAYER_DIR = ART_ROOT / "layers"
REVIEW_DIR = ART_ROOT / "review"
GODOT_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_overlay_probe_v1"

# 目标区严格沿用 dossier_contract 的 2x 几何。
SUMMARY_RECT = (48, 296, 776, 904)
METADATA_RECT = (48, 944, 776, 1224)
RISK_RECT = (40, 1244, 784, 1592)
CTA_RECT = (56, 1640, 768, 1864)

# 文字安全区保持 RISK_RECT 不变；美术叠印向上出血 20px（运行时 10px），
# 吃掉 metadata / risk 之间的中性纸缝，避免视觉上重新变成两张卡。
RISK_ART_RECT = (40, 1224, 784, 1592)

# 生图母件中的自然色区边界。只作为取样区，随后归一到合同矩形。
METADATA_SAMPLE_RECT = (48, 882, 776, 1206)
RISK_SAMPLE_RECT = (40, 1206, 784, 1528)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="imagegen 输出的无字视觉母件")
    return parser.parse_args()


def ensure_dirs() -> None:
    for directory in (SOURCE_DIR, LAYER_DIR, REVIEW_DIR, GODOT_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def paper_mask(base: Image.Image) -> Image.Image:
    """只允许叠印覆盖原始暖纸，不覆盖透明区或橄榄色外背板。"""
    rgba = base.convert("RGBA")
    pixels = rgba.load()
    mask = Image.new("L", rgba.size, 0)
    out = mask.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = pixels[x, y]
            if a > 8 and b > 105 and r > 155 and g > 145:
                out[x, y] = a
    return mask


def extract_summary_accent(master: Image.Image, base_paper_mask: Image.Image) -> Image.Image:
    """仅抽取母件中的深青色竖线，避免把中性纸纹做成补丁。"""
    layer = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
    src = master.load()
    dst = layer.load()
    paper = base_paper_mask.load()
    x0, y0, x1, y1 = SUMMARY_RECT
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = src[x, y]
            is_teal_rule = (
                a > 8
                and g - r > 15
                and b - r > 15
                and g < 160
                and b < 170
            )
            if is_teal_rule and paper[x, y] > 0:
                dst[x, y] = (r, g, b, min(a, paper[x, y]))
    return layer


def extract_printed_zone(
    master: Image.Image,
    sample_rect: tuple[int, int, int, int],
    target_rect: tuple[int, int, int, int],
    base_paper_mask: Image.Image,
) -> Image.Image:
    target_w = target_rect[2] - target_rect[0]
    target_h = target_rect[3] - target_rect[1]
    sample = master.crop(sample_rect).resize((target_w, target_h), Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
    layer.paste(sample, (target_rect[0], target_rect[1]))

    rect_mask = Image.new("L", TARGET_SIZE, 0)
    rect_mask.paste(255, (target_rect[0], target_rect[1], target_rect[2], target_rect[3]))
    combined_mask = Image.new("L", TARGET_SIZE, 0)
    paper = base_paper_mask.load()
    rect = rect_mask.load()
    out = combined_mask.load()
    for y in range(target_rect[1], target_rect[3]):
        for x in range(target_rect[0], target_rect[2]):
            out[x, y] = min(paper[x, y], rect[x, y])
    layer.putalpha(combined_mask)
    return layer


def checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGB", size, (39, 59, 70))
    draw = ImageDraw.Draw(image)
    colors = ((48, 72, 83), (56, 82, 92))
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=colors[(x // cell + y // cell) % 2])
    return image


def thumbnail_on_checker(layer: Image.Image, size: tuple[int, int]) -> Image.Image:
    thumb = layer.copy()
    thumb.thumbnail(size, Image.Resampling.LANCZOS)
    bg = checkerboard(size)
    x = (size[0] - thumb.width) // 2
    y = (size[1] - thumb.height) // 2
    bg.paste(thumb, (x, y), thumb)
    return bg


def build_exploded_board(
    base: Image.Image,
    summary: Image.Image,
    metadata: Image.Image,
    risk: Image.Image,
    cta: Image.Image,
    recomposed: Image.Image,
) -> Image.Image:
    canvas = Image.new("RGB", (1920, 1080), (6, 31, 45))
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(34, bold=True)
    label_font = load_font(22, bold=True)
    body_font = load_font(18)
    muted = (141, 185, 180)
    paper = (232, 224, 201)

    draw.text((52, 28), "区域任务 dossier：同源叠印层拆分证明", font=title_font, fill=paper)
    draw.text((52, 76), "程序只负责裁切 / 透明遮罩 / 1× 拼接；正式纹理全部来自美术母件。", font=body_font, fill=muted)

    tile_size = (206, 480)
    layer_items = [
        ("01  完整底纸", base),
        ("02  摘要竖线", summary),
        ("03  青色信息叠印", metadata),
        ("04  锈色风险叠印", risk),
    ]
    x_positions = [52, 282, 512, 742]
    for (label, layer), x in zip(layer_items, x_positions):
        tile = thumbnail_on_checker(layer, tile_size)
        canvas.paste(tile, (x, 154))
        draw.rounded_rectangle((x - 2, 152, x + tile_size[0] + 1, 635), radius=7, outline=(92, 128, 128), width=2)
        draw.text((x, 652), label, font=label_font, fill=paper)
        if x != x_positions[-1]:
            draw.text((x + 209, 356), "+", font=title_font, fill=(160, 187, 122))

    cta_tile = checkerboard((436, 168), cell=12)
    cta_view = cta.copy()
    cta_view.thumbnail((356, 112), Image.Resampling.LANCZOS)
    cta_tile.paste(cta_view, ((436 - cta_view.width) // 2, (168 - cta_view.height) // 2), cta_view)
    canvas.paste(cta_tile, (512, 746))
    draw.rounded_rectangle((510, 744, 949, 915), radius=7, outline=(92, 128, 128), width=2)
    draw.text((512, 932), "05  独立 CTA（既有资源）", font=label_font, fill=paper)

    draw.text((1020, 470), "=", font=title_font, fill=(160, 187, 122))
    composed_1x = recomposed.resize((412, 960), Image.Resampling.LANCZOS)
    canvas.paste(composed_1x, (1160, 82), composed_1x)
    draw.rounded_rectangle((1157, 79, 1574, 1044), radius=8, outline=(218, 197, 143), width=3)
    draw.text((1604, 140), "1× 重组规则", font=label_font, fill=paper)
    notes = [
        "• 底纸单独成立",
        "• 色区无边框 / 无阴影",
        "• 叠印严格裁进纸面",
        "• 文字永远由 Godot 渲染",
        "• CTA 保持独立交互资源",
    ]
    y = 194
    for note in notes:
        draw.text((1604, y), note, font=body_font, fill=muted)
        y += 42
    draw.text((1604, 448), "后续只替换叠印纹理，\n不需要重切整张 dossier。", font=body_font, fill=(219, 174, 123), spacing=10)
    return canvas


def alpha_count(image: Image.Image) -> int:
    return sum(1 for value in image.getchannel("A").getdata() if value > 0)


def main() -> None:
    args = parse_args()
    ensure_dirs()

    raw = Image.open(args.source).convert("RGBA")
    base = Image.open(BASE_PATH).convert("RGBA")
    cta = Image.open(CTA_PATH).convert("RGBA")
    if base.size != TARGET_SIZE:
        raise SystemExit(f"底纸尺寸错误：{base.size}，预期 {TARGET_SIZE}")
    if cta.size != (712, 224):
        raise SystemExit(f"CTA 尺寸错误：{cta.size}，预期 (712, 224)")

    raw.save(SOURCE_DIR / "01-imagegen-no-text-dossier-master-v1.png")
    normalized = raw.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
    # 生图工具可能把透明棋盘格烘进输出。归一母件只借用正式底纸 alpha，
    # 实际运行时仍不会直接使用整张归一母件。
    normalized.putalpha(base.getchannel("A"))
    normalized.save(SOURCE_DIR / "02-imagegen-no-text-dossier-master-normalized-v1.png")

    mask = paper_mask(base)
    summary = extract_summary_accent(normalized, mask)
    metadata = extract_printed_zone(normalized, METADATA_SAMPLE_RECT, METADATA_RECT, mask)
    risk = extract_printed_zone(normalized, RISK_SAMPLE_RECT, RISK_ART_RECT, mask)

    base.save(LAYER_DIR / "rt-dossier-base-shell-probe-v1-2x.png")
    summary.save(LAYER_DIR / "rt-dossier-summary-accent-probe-v1-2x.png")
    metadata.save(LAYER_DIR / "rt-dossier-metadata-wash-probe-v1-2x.png")
    risk.save(LAYER_DIR / "rt-dossier-risk-wash-probe-v1-2x.png")
    cta.save(LAYER_DIR / "rt-dossier-cta-probe-v1-2x.png")

    recomposed = base.copy()
    recomposed.alpha_composite(summary)
    recomposed.alpha_composite(metadata)
    recomposed.alpha_composite(risk)
    recomposed.alpha_composite(cta, (CTA_RECT[0], CTA_RECT[1]))
    recomposed.save(REVIEW_DIR / "02-dossier-overlay-recomposed-2x-v1.png")
    build_exploded_board(base, summary, metadata, risk, cta, recomposed).save(
        REVIEW_DIR / "01-dossier-overlay-exploded-v1.png"
    )

    # Godot 试装目录只放候选层，不登记进正式 manifest。
    for name, image in (
        ("rt-dossier-base-shell-probe-v1-2x.png", base),
        ("rt-dossier-summary-accent-probe-v1-2x.png", summary),
        ("rt-dossier-metadata-wash-probe-v1-2x.png", metadata),
        ("rt-dossier-risk-wash-probe-v1-2x.png", risk),
        ("rt-dossier-cta-probe-v1-2x.png", cta),
    ):
        image.save(GODOT_DIR / name)

    audit = {
        "probe_only": True,
        "source_size": list(raw.size),
        "normalized_size": list(normalized.size),
        "base_size": list(base.size),
        "cta_size": list(cta.size),
        "contract_rects_2x": {
            "summary": list(SUMMARY_RECT),
            "metadata": list(METADATA_RECT),
            "risk": list(RISK_RECT),
            "cta": list(CTA_RECT),
        },
        "art_rects_2x": {
            "risk_wash_with_top_bleed": list(RISK_ART_RECT),
        },
        "imagegen_sample_rects_2x": {
            "metadata": list(METADATA_SAMPLE_RECT),
            "risk": list(RISK_SAMPLE_RECT),
        },
        "nonzero_alpha_pixels": {
            "summary_accent": alpha_count(summary),
            "metadata_wash": alpha_count(metadata),
            "risk_wash": alpha_count(risk),
            "cta": alpha_count(cta),
        },
        "implementation_note": "程序仅裁切、遮罩、缩放与拼接；正式纹理来自同一张 imagegen 母件。",
    }
    (ART_ROOT / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
