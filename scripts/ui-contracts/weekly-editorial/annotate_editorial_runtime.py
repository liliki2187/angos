#!/usr/bin/env python3
"""在真实 Godot 截图上按冻结合同坐标生成交付标注图。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/01-godot-dual-page-overview-held.png"
OUTPUT = ROOT / "docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/05-overview-annotated.png"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    items = [
        ("1 候选报道 320×920", (80, 96, 400, 1016), (72, 179, 190, 255)),
        ("2 双版工作区 1040×920", (420, 96, 1460, 1016), (126, 138, 72, 255)),
        ("3 发刊复核 360×920", (1480, 96, 1840, 1016), (211, 179, 124, 255)),
        ("4 固定持稿条 1010×56", (435, 112, 1445, 168), (232, 201, 111, 255)),
        ("5 首个资产化切片 442×374", (459, 276, 901, 650), (177, 96, 62, 255)),
    ]
    label_font = font(20)
    for label, rect, color in items:
        draw.rectangle(rect, outline=color, width=4)
        box = draw.textbbox((0, 0), label, font=label_font)
        width = box[2] - box[0] + 18
        height = box[3] - box[1] + 14
        x = rect[0] + 8
        y = rect[1] + 8
        draw.rectangle((x, y, x + width, y + height), fill=(4, 25, 37, 224), outline=color, width=2)
        draw.text((x + 9, y + 5), label, font=label_font, fill=(244, 239, 220, 255))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
