from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map"

PALETTE = {
    "black": (3, 9, 11, 255),
    "wall": (8, 22, 25, 255),
    "wall2": (5, 16, 19, 255),
    "map": (10, 45, 49, 210),
    "map_dim": (7, 30, 34, 185),
    "cyan": (40, 196, 208, 210),
    "cyan_dim": (26, 118, 130, 120),
    "red": (222, 48, 38, 220),
    "red_dim": (110, 24, 22, 160),
    "paper": (222, 209, 158, 226),
    "paper_shadow": (0, 0, 0, 110),
    "cream": (244, 231, 178, 230),
}


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path)
    print(path)


def p(width: int, height: int, x: float, y: float) -> tuple[int, int]:
    return int(width * x), int(height * y)


def poly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width: int = 1) -> None:
    pts = [(int(x), int(y)) for x, y in points]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def rect(draw: ImageDraw.ImageDraw, xy, fill, outline=None, width: int = 1) -> None:
    draw.rectangle(tuple(int(v) for v in xy), fill=fill, outline=outline, width=width)


def add_noise(img: Image.Image, count: int, alpha: int = 26) -> None:
    draw = ImageDraw.Draw(img)
    width, height = img.size
    choices = [
        (255, 255, 255, max(4, alpha // 2)),
        (0, 0, 0, alpha + 18),
        (40, 196, 208, max(6, alpha // 2)),
        (222, 48, 38, max(6, alpha // 3)),
    ]
    for _ in range(count):
        x = random.randrange(width)
        y = random.randrange(height)
        size = random.choice([1, 1, 1, 2, 3])
        draw.rectangle((x, y, x + size, y + size), fill=random.choice(choices))


def add_halftone(img: Image.Image, box, color=(0, 0, 0, 42), step: int = 22, radius: int = 2) -> None:
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = [int(v) for v in box]
    for y in range(y0, y1, step):
        offset = ((y // step) % 2) * (step // 2)
        for x in range(x0 + offset, x1, step):
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def add_shadow(base: Image.Image, polygon_points, alpha: int = 115, blur: int = 14, offset=(8, 12)) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    pts = [(int(x + offset[0]), int(y + offset[1])) for x, y in polygon_points]
    draw.polygon(pts, fill=(0, 0, 0, alpha))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))


def draw_fake_print(draw: ImageDraw.ImageDraw, x: int, y: int, width: int, rows: int) -> None:
    for i in range(rows):
        line_width = int(width * random.uniform(0.35, 0.95))
        yy = y + i * 13
        draw.rectangle((x, yy, x + line_width, yy + 4), fill=(16, 24, 23, 150))


def draw_paper_clip(img: Image.Image, xy, angle: float = 0.0, accent: str = "red") -> None:
    width, height = img.size
    x, y, w, h = xy
    paper = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(paper)
    add_shadow(paper, [(20, 20), (w + 20, 18), (w + 22, h + 20), (22, h + 24)], 80, 8, (6, 7))
    poly(draw, [(20, 20), (w + 20, 18), (w + 22, h + 20), (22, h + 24)], PALETTE["paper"], (9, 16, 16, 185), 3)
    stripe = PALETTE["red"] if accent == "red" else PALETTE["cyan"]
    draw.rectangle((20, 20, 48, h + 20), fill=stripe)
    draw_fake_print(draw, 62, 42, max(30, w - 82), max(2, h // 22))
    add_halftone(paper, (20, 20, w + 24, h + 24), (0, 0, 0, 14), 18, 1)
    if angle:
        paper = paper.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    img.alpha_composite(paper, (int(x), int(y)))


def draw_world_map(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    land = PALETTE["map"]
    dim = PALETTE["map_dim"]
    cyan = PALETTE["cyan_dim"]
    shapes = [
        (
            [
                p(width, height, 0.18, 0.31),
                p(width, height, 0.25, 0.25),
                p(width, height, 0.34, 0.30),
                p(width, height, 0.37, 0.42),
                p(width, height, 0.30, 0.55),
                p(width, height, 0.20, 0.48),
            ],
            land,
        ),
        (
            [
                p(width, height, 0.33, 0.56),
                p(width, height, 0.39, 0.63),
                p(width, height, 0.38, 0.80),
                p(width, height, 0.31, 0.73),
            ],
            dim,
        ),
        (
            [
                p(width, height, 0.48, 0.31),
                p(width, height, 0.60, 0.25),
                p(width, height, 0.76, 0.29),
                p(width, height, 0.86, 0.42),
                p(width, height, 0.76, 0.54),
                p(width, height, 0.58, 0.48),
            ],
            dim,
        ),
        (
            [
                p(width, height, 0.55, 0.49),
                p(width, height, 0.66, 0.51),
                p(width, height, 0.68, 0.70),
                p(width, height, 0.59, 0.76),
                p(width, height, 0.51, 0.62),
            ],
            dim,
        ),
        (
            [
                p(width, height, 0.76, 0.67),
                p(width, height, 0.88, 0.69),
                p(width, height, 0.86, 0.78),
                p(width, height, 0.75, 0.77),
            ],
            dim,
        ),
    ]
    for points, color in shapes:
        poly(draw, points, color, cyan, 3)

    # Pixel city/noise clusters on coastlines, kept subtle so labels remain readable.
    for cx, cy in [(0.25, 0.39), (0.74, 0.44), (0.56, 0.60), (0.50, 0.36), (0.67, 0.43)]:
        px, py = p(width, height, cx, cy)
        for _ in range(18):
            dx = random.randint(-46, 46)
            dy = random.randint(-34, 34)
            draw.rectangle((px + dx, py + dy, px + dx + 5, py + dy + 5), fill=(35, 190, 204, 70))


def draw_grid_and_scanlines(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(120, width - 120, 80):
        draw.line((x, 120, x + random.randint(-8, 8), height - 140), fill=(36, 148, 158, 33), width=2)
    for y in range(110, height - 120, 60):
        draw.line((100, y, width - 100, y + random.randint(-6, 6)), fill=(36, 148, 158, 36), width=2)
    for y in range(0, height, 6):
        draw.line((0, y, width, y), fill=(0, 0, 0, 22), width=1)


def draw_edge_props(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Top rail and pin string, deliberately edge-heavy and central-clean.
    draw.rectangle((420, 74, 1510, 86), fill=(227, 218, 176, 175))
    draw.rectangle((424, 88, 1506, 94), fill=(4, 9, 10, 160))
    red = PALETTE["red"]
    strings = [
        [(170, 220), (430, 170), (710, 210), (920, 150), (1220, 210), (1510, 160), (1770, 230)],
        [(130, 700), (380, 620), (620, 680), (940, 610), (1280, 690), (1650, 610), (1870, 720)],
    ]
    for pts in strings:
        draw.line(pts, fill=(222, 48, 38, 128), width=4)
        for x, y in pts:
            draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=red)
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(3, 8, 9, 220))

    # Edge clippings and devices.
    draw_paper_clip(img, (70, 98, 210, 126), -7, "red")
    draw_paper_clip(img, (1360, 94, 290, 162), 8, "cyan")
    draw_paper_clip(img, (86, 690, 260, 144), 9, "cyan")
    draw_paper_clip(img, (1390, 750, 330, 155), -9, "red")

    # Lamp silhouette and small printer/ticker, both kept low and dark.
    draw.line((160, 878, 280, 720), fill=(8, 14, 15, 238), width=18)
    draw.line((255, 720, 430, 790), fill=(8, 14, 15, 238), width=14)
    draw.ellipse((402, 752, 560, 866), fill=(6, 12, 13, 238), outline=(205, 194, 146, 90), width=3)
    draw.pieslice((410, 754, 560, 874), 185, 345, fill=(221, 55, 44, 45))
    draw.rectangle((1460, 820, 1780, 986), fill=(5, 13, 15, 235), outline=(39, 190, 204, 80), width=3)
    draw.rectangle((1505, 780, 1735, 842), fill=(216, 203, 153, 180), outline=(4, 9, 10, 190), width=3)
    draw_fake_print(draw, 1524, 798, 190, 3)
    for x in [1496, 1550, 1720]:
        draw.rectangle((x, 940, x + 16, 954), fill=random.choice([PALETTE["red"], PALETTE["cyan"], (221, 178, 72, 180)]))


def make_global_channel_map() -> None:
    random.seed(260606)
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height), PALETTE["wall"])
    draw = ImageDraw.Draw(img)

    # Blocky dark wall with subtle magazine-print texture.
    for y in range(0, height, 10):
        color = PALETTE["wall"] if y % 20 == 0 else PALETTE["wall2"]
        draw.rectangle((0, y, width, y + 9), fill=color)
    for x in range(0, width, 120):
        draw.rectangle((x, 0, x + 2, height), fill=(10, 34, 38, 48))
    draw_grid_and_scanlines(draw, width, height)

    # Main map plate, strong but not a UI panel.
    plate = [(78, 72), (1848, 58), (1864, 1000), (72, 1014)]
    add_shadow(img, plate, 120, 20, (18, 20))
    poly(draw, plate, (3, 14, 17, 228), (39, 190, 204, 92), 5)
    inner = [(122, 110), (1808, 102), (1818, 962), (118, 974)]
    poly(draw, inner, (2, 12, 15, 215), (225, 211, 155, 58), 2)

    draw_world_map(draw, width, height)
    draw_edge_props(img)

    # Red anomaly wash only at far right, echoing the title screen without flooding the UI.
    wash = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for i in range(9):
        x0 = int(width * (0.82 + i * 0.02))
        wd.rectangle((x0, 0, x0 + 28, height), fill=(222, 48, 38, max(8, 42 - i * 4)))
    wash = wash.filter(ImageFilter.GaussianBlur(26))
    img.alpha_composite(wash)

    add_halftone(img, (0, 0, width, height), (0, 0, 0, 24), 28, 1)
    add_noise(img, 1200, 14)
    save(img, "global-channel-map-clean-v3.png")


def main() -> None:
    make_global_channel_map()


if __name__ == "__main__":
    main()
