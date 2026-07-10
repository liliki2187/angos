# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
B1_GODOT = BASE / "403-world-map-wmw-v0-9-2-left-card-candidate-b1-godot-single-component.png"
B11_GODOT = BASE / "412-world-map-wmw-v0-9-3-left-card-candidate-b1-1-godot-single-component.png"
B1_SOURCE = BASE / "397-world-map-wmw-v0-9-2-left-card-candidate-b1-composited-polish.png"
B11_SOURCE = BASE / "406-world-map-wmw-v0-9-3-left-card-candidate-b1-1-composite-clean.png"
OUT_COMPARE = BASE / "414-world-map-wmw-v0-9-3-left-card-b1-vs-b1-1-composite-fix-board.png"

FONT_BOLD = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
FONT_REGULAR = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\arial.ttf"]


def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


F_TITLE = font(FONT_BOLD, 36)
F_HEAD = font(FONT_BOLD, 24)
F_BODY = font(FONT_REGULAR, 18)
F_SMALL = font(FONT_REGULAR, 15)


def crop_runtime_left(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return img.crop((42, 26, 424, 1058))


def fit(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return img.resize(size, Image.Resampling.LANCZOS)


def add_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: tuple[int, int, int]) -> None:
    x, y = xy
    box = draw.textbbox((x, y), text, font=F_SMALL)
    draw.rectangle((box[0] - 6, box[1] - 4, box[2] + 6, box[3] + 4), fill=(9, 17, 18), outline=fill, width=1)
    draw.text((x, y), text, fill=fill, font=F_SMALL)


def draw_callout(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str, fill: tuple[int, int, int]) -> None:
    draw.rectangle(rect, outline=fill, width=4)
    add_label(draw, (rect[0], max(4, rect[1] - 24)), text, fill)


def main() -> None:
    board = Image.new("RGB", (2100, 1320), (12, 23, 24))
    draw = ImageDraw.Draw(board)
    draw.text((48, 32), "left_region_card B1 -> B1.1 composite repair board", fill=(245, 239, 209), font=F_TITLE)
    draw.text((48, 82), "B1.1 only repairs composition: no imagegen reroll, no contract resize, no runtime badge overlay.", fill=(213, 222, 199), font=F_BODY)

    left = fit(crop_runtime_left(B1_GODOT), (382, 1032))
    right = fit(crop_runtime_left(B11_GODOT), (382, 1032))
    lx, rx, y = 64, 514, 160
    board.paste(left, (lx, y))
    board.paste(right, (rx, y))
    draw.rectangle((lx, y, lx + 382, y + 1032), outline=(218, 93, 78), width=3)
    draw.rectangle((rx, y, rx + 382, y + 1032), outline=(116, 214, 151), width=3)
    draw.text((lx, y - 36), "B1 v0.9.2 rejected: visible compositing artifacts", fill=(255, 177, 158), font=F_HEAD)
    draw.text((rx, y - 36), "B1.1 v0.9.3 fixed", fill=(176, 240, 190), font=F_HEAD)

    draw_callout(draw, (lx + 52, y + 32, lx + 136, y + 126), "double globe", (255, 110, 91))
    draw_callout(draw, (lx + 264, y + 614, lx + 348, y + 704), "double warning", (255, 110, 91))
    draw_callout(draw, (lx + 58, y + 284, lx + 350, y + 410), "photo overflow / source edge", (255, 110, 91))
    draw_callout(draw, (lx + 334, y + 806, lx + 372, y + 956), "green strip", (255, 110, 91))

    draw_callout(draw, (rx + 52, y + 32, rx + 136, y + 126), "B globe only", (115, 235, 152))
    draw_callout(draw, (rx + 264, y + 614, rx + 348, y + 704), "baked badge only", (115, 235, 152))
    draw_callout(draw, (rx + 58, y + 284, rx + 350, y + 410), "inside photo_slot", (115, 235, 152))
    draw_callout(draw, (rx + 334, y + 806, rx + 372, y + 956), "full-frame greenish=0", (115, 235, 152))

    sx, sy = 1020, 210
    source_b1 = fit(Image.open(B1_SOURCE).convert("RGB"), (360, 288))
    source_b11 = fit(Image.open(B11_SOURCE).convert("RGB"), (360, 322))
    board.paste(source_b1, (sx, sy))
    board.paste(source_b11, (sx + 390, sy))
    draw.rectangle((sx, sy, sx + 360, sy + 288), outline=(218, 93, 78), width=3)
    draw.rectangle((sx + 390, sy, sx + 750, sy + 322), outline=(116, 214, 151), width=3)
    draw.text((sx, sy - 34), "397 B1 composite source", fill=(255, 177, 158), font=F_HEAD)
    draw.text((sx + 390, sy - 34), "406 B1.1 composite clean source", fill=(176, 240, 190), font=F_HEAD)

    notes = [
        "1. Double globe: crop starts after source badge; B shell globe is the only icon.",
        "2. Warning triangle: runtime overlay removed; baked badge pixels tinted only.",
        "3. Photo slot: every patch is pasted to [42,48,348,128] at 2x.",
        "4. Green residue: full-frame artifact scan; available/warning/locked = 0.",
        "5. New gate: composite_cleanliness records per-state manual checks in 411.",
    ]
    nx, ny = 980, 600
    draw.rounded_rectangle((nx - 20, ny - 20, 2040, ny + 230), radius=8, fill=(19, 35, 36), outline=(73, 114, 102), width=2)
    draw.text((nx, ny), "Fix checklist", fill=(245, 239, 209), font=F_HEAD)
    for i, text in enumerate(notes):
        draw.text((nx, ny + 42 + i * 34), text, fill=(218, 226, 206), font=F_BODY)

    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    board.save(OUT_COMPARE)
    print(OUT_COMPARE)


if __name__ == "__main__":
    main()
