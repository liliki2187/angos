# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
B_GODOT = BASE / "389-world-map-wmw-v0-9-1-left-card-candidate-b-godot-single-component.png"
B1_GODOT = BASE / "403-world-map-wmw-v0-9-2-left-card-candidate-b1-godot-single-component.png"
OUT = BASE / "405-world-map-wmw-v0-9-2-left-card-b-vs-b1-comparison-board.png"


def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


FONT_BOLD = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]
FONT_REGULAR = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]
F_TITLE = font(FONT_BOLD, 32)
F_HEAD = font(FONT_BOLD, 22)
F_BODY = font(FONT_REGULAR, 18)
F_SMALL = font(FONT_REGULAR, 15)


def crop_stack(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return img.crop((32, 18, 430, 1064))


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, max_width: int, line_gap: int = 8) -> int:
    x, y = xy
    current = ""
    for ch in text:
        test = current + ch
        if draw.textbbox((0, 0), test, font=F_BODY)[2] <= max_width or not current:
            current = test
            continue
        draw.text((x, y), current, font=F_BODY, fill="#e6dec3")
        y += 25 + line_gap
        current = ch
    if current:
        draw.text((x, y), current, font=F_BODY, fill="#e6dec3")
        y += 25 + line_gap
    return y


def main() -> None:
    b = crop_stack(B_GODOT)
    b1 = crop_stack(B1_GODOT)
    board = Image.new("RGB", (1680, 1260), "#071315")
    draw = ImageDraw.Draw(board, "RGBA")
    draw.rectangle([0, 0, 1680, 1120], fill="#071315")
    draw.rectangle([32, 32, 1648, 1228], outline="#284246", width=2)
    draw.text((56, 48), "WMW left_region_card B -> B1 (v0.9.2) review board", font=F_TITLE, fill="#f3efd6")
    draw.text((56, 90), "Sources: 389 / 403 are Godot windowed runtime screenshots; B1 remains a candidate, not frozen production art.", font=F_SMALL, fill="#c9d4bf")

    board.paste(b, (70, 146))
    board.paste(b1, (535, 146))
    draw.text((70, 112), "B / v0.9.1", font=F_HEAD, fill="#f3efd6")
    draw.text((535, 112), "B1 / v0.9.2", font=F_HEAD, fill="#f3efd6")
    draw.rectangle([70, 146, 468, 1192], outline="#31565a", width=2)
    draw.rectangle([535, 146, 933, 1192], outline="#6a7f41", width=2)

    x = 990
    y = 150
    draw.text((x, y), "Diff checkpoints", font=F_HEAD, fill="#f3efd6")
    y += 42
    items = [
        ("photo_slot", "B 是通用低多边形风景；B1 加入金字塔、天线阵、遗迹和人影剪影，地区暗示更强。"),
        ("non-selected green", "available / warning / locked 的外缘绿色残边按 atlas 统计清理；选中态保留绿色状态语义。"),
        ("warning triangle", "warning 的三角提示从浅色线稿改为更红的运行时可读警示。"),
        ("frame weight", "外缘 glow 和暗绿底边被削薄；卡体厚度仍需用户按标杆观感裁决。"),
        ("text tokens", "label_title / meta_status 改为运行时 token；meta 墨色更深、字号提升到 Godot 14。"),
    ]
    for key, text in items:
        draw.text((x, y), key, font=F_HEAD, fill="#9ed0d6")
        y += 30
        y = draw_wrapped(draw, (x, y), text, 560)
        y += 18

    draw.text((x, 1016), "B1 acceptance question", font=F_HEAD, fill="#f3efd6")
    draw_wrapped(draw, (x, 1050), "请裁决：B1 的局部合成路线是否足够接近标杆，可进入后续 class 扩展；或继续只微调 left_region_card。", 560, line_gap=4)
    board.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
