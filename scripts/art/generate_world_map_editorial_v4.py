from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map"

SCALE = 2
W, H = 750, 540

BLACK = (3, 8, 10, 255)
WALL = (7, 18, 21, 255)
WALL_DARK = (4, 12, 15, 255)
BOARD = (5, 18, 21, 238)
MAP_BG = (4, 28, 33, 228)
MAP_FILL = (9, 72, 78, 170)
MAP_FILL_DIM = (8, 48, 55, 150)
CYAN = (40, 205, 216, 210)
CYAN_DIM = (24, 125, 138, 125)
RED = (226, 48, 38, 220)
RED_DIM = (120, 28, 24, 130)
PAPER = (218, 203, 151, 238)
PAPER_DARK = (118, 106, 72, 220)
GOLD = (236, 185, 70, 220)


def rect(draw: ImageDraw.ImageDraw, box, fill, outline=None, width: int = 1) -> None:
    draw.rectangle(tuple(int(v) for v in box), fill=fill, outline=outline, width=width)


def poly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width: int = 1) -> None:
    pts = [(int(x), int(y)) for x, y in points]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width)


def add_shadow(img: Image.Image, points, alpha: int = 80, blur: int = 5, offset=(5, 6)) -> None:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon([(x + offset[0], y + offset[1]) for x, y in points], fill=(0, 0, 0, alpha))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def add_halftone(draw: ImageDraw.ImageDraw, box, color, step: int = 10, r: int = 1) -> None:
    x0, y0, x1, y1 = [int(v) for v in box]
    for y in range(y0, y1, step):
        shift = ((y // step) & 1) * (step // 2)
        for x in range(x0 + shift, x1, step):
            draw.rectangle((x - r, y - r, x + r, y + r), fill=color)


def fake_print(draw: ImageDraw.ImageDraw, x: int, y: int, width: int, rows: int, color=(14, 22, 20, 160)) -> None:
    for i in range(rows):
        line_width = int(width * random.uniform(0.38, 0.95))
        yy = y + i * 7
        rect(draw, (x, yy, x + line_width, yy + 2), color)


def paper(img: Image.Image, x: int, y: int, w: int, h: int, accent=RED, tilt: int = 0, tab: bool = True) -> None:
    layer = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = [(8, 10), (w + 8, 7), (w + 10, h + 9), (10, h + 12)]
    add_shadow(layer, pts, 60, 3, (3, 3))
    poly(d, pts, PAPER, (7, 12, 12, 190), 2)
    if tab:
        rect(d, (8, 10, 21, h + 9), accent)
    fake_print(d, 28 if tab else 18, 22, max(24, w - 42), max(2, h // 14))
    add_halftone(d, (8, 10, w + 10, h + 12), (0, 0, 0, 15), 9, 0)
    if tilt:
        layer = layer.rotate(tilt, resample=Image.Resampling.NEAREST, expand=True)
    img.alpha_composite(layer, (x, y))


def draw_world(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int) -> None:
    def p(x: float, y: float) -> tuple[int, int]:
        return int(x0 + (x1 - x0) * x), int(y0 + (y1 - y0) * y)

    shapes = [
        ([p(0.08, 0.25), p(0.17, 0.14), p(0.29, 0.18), p(0.35, 0.34), p(0.28, 0.50), p(0.15, 0.45)], MAP_FILL),
        ([p(0.27, 0.52), p(0.36, 0.60), p(0.34, 0.84), p(0.25, 0.72), p(0.23, 0.61)], MAP_FILL_DIM),
        ([p(0.43, 0.25), p(0.56, 0.14), p(0.76, 0.22), p(0.87, 0.36), p(0.79, 0.50), p(0.58, 0.44), p(0.49, 0.53)], MAP_FILL_DIM),
        ([p(0.51, 0.48), p(0.64, 0.52), p(0.67, 0.72), p(0.58, 0.86), p(0.48, 0.64)], MAP_FILL_DIM),
        ([p(0.73, 0.68), p(0.89, 0.68), p(0.86, 0.82), p(0.73, 0.79)], MAP_FILL_DIM),
        ([p(0.80, 0.46), p(0.86, 0.41), p(0.90, 0.49), p(0.85, 0.55)], (8, 58, 64, 135)),
    ]
    for pts, fill in shapes:
        poly(draw, pts, fill, CYAN_DIM, 2)
        add_halftone(draw, (*minmax(pts),), (39, 200, 214, 20), 7, 0)

    # Coast pixels and small print ticks.
    clusters = [p(0.18, 0.32), p(0.30, 0.44), p(0.56, 0.36), p(0.72, 0.35), p(0.58, 0.62), p(0.82, 0.74)]
    for cx, cy in clusters:
        for _ in range(24):
            dx = random.randint(-18, 18)
            dy = random.randint(-14, 14)
            rect(draw, (cx + dx, cy + dy, cx + dx + 2, cy + dy + 2), (36, 198, 212, 80))

    # Editorial routes, not radar arcs.
    routes = [
        [p(0.16, 0.36), p(0.34, 0.42), p(0.52, 0.34), p(0.73, 0.38)],
        [p(0.33, 0.62), p(0.50, 0.55), p(0.67, 0.67), p(0.82, 0.58)],
        [p(0.28, 0.48), p(0.46, 0.28), p(0.58, 0.20)],
    ]
    for pts in routes:
        draw.line(pts, fill=(226, 48, 38, 120), width=2)
        for x, y in pts:
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=RED)


def minmax(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def draw_asset() -> Image.Image:
    random.seed(260607)
    img = Image.new("RGBA", (W, H), WALL)
    draw = ImageDraw.Draw(img)

    for y in range(0, H, 5):
        rect(draw, (0, y, W, y + 4), WALL if y % 10 == 0 else WALL_DARK)
    for x in range(0, W, 40):
        draw.line((x, 0, x, H), fill=(18, 52, 58, 35), width=1)
    for y in range(0, H, 32):
        draw.line((0, y, W, y), fill=(18, 52, 58, 28), width=1)

    board = [(26, 38), (724, 30), (732, 506), (20, 514)]
    add_shadow(img, board, 120, 8, (8, 10))
    poly(draw, board, BOARD, (42, 196, 208, 100), 3)
    rect(draw, (78, 59, 672, 65), (236, 223, 172, 120))
    rect(draw, (82, 67, 668, 70), (3, 8, 10, 160))

    map_box = (70, 86, 680, 428)
    rect(draw, map_box, MAP_BG, (222, 207, 151, 95), 2)
    for x in range(map_box[0] + 28, map_box[2], 50):
        draw.line((x, map_box[1], x, map_box[3]), fill=(44, 155, 166, 42), width=1)
    for y in range(map_box[1] + 24, map_box[3], 38):
        draw.line((map_box[0], y, map_box[2], y), fill=(44, 155, 166, 42), width=1)
    add_halftone(draw, map_box, (34, 178, 190, 28), 8, 0)
    draw_world(draw, *map_box)

    # Clippings and tabs inside the frame fill deliberate empty zones.
    paper(img, 42, 86, 82, 54, RED, -5)
    paper(img, 610, 90, 78, 62, CYAN, 6)
    paper(img, 42, 408, 120, 48, CYAN, 4)
    paper(img, 538, 418, 138, 52, RED, -4)
    for x, y, color in [(92, 165, RED), (628, 196, CYAN), (350, 112, GOLD), (228, 404, RED), (483, 380, CYAN)]:
        rect(draw, (x, y, x + 36, y + 10), color)
        rect(draw, (x + 3, y + 13, x + 58, y + 16), (218, 203, 151, 100))

    # Bottom desk density, kept below pin safe zone.
    rect(draw, (0, 458, W, H), (12, 14, 13, 225))
    rect(draw, (84, 468, 326, 508), PAPER_DARK, (8, 10, 10, 200), 2)
    fake_print(draw, 100, 480, 194, 4, (20, 24, 22, 150))
    rect(draw, (348, 462, 468, 523), (4, 12, 14, 235), (38, 200, 214, 85), 2)
    rect(draw, (376, 452, 440, 474), PAPER, (5, 10, 10, 190), 2)
    fake_print(draw, 386, 462, 42, 2)
    rect(draw, (580, 462, 730, 526), (5, 12, 14, 235), (226, 48, 38, 70), 2)
    for x in range(598, 700, 18):
        rect(draw, (x, 494, x + 8, 500), random.choice([RED, CYAN, GOLD]))

    # Print texture and pixel noise.
    add_halftone(draw, (0, 0, W, H), (0, 0, 0, 24), 12, 0)
    for _ in range(1700):
        x = random.randrange(W)
        y = random.randrange(H)
        c = random.choice([(255, 245, 190, 18), (0, 0, 0, 46), (40, 205, 216, 18), (226, 48, 38, 16)])
        rect(draw, (x, y, x + random.choice([0, 0, 1]), y + random.choice([0, 0, 1])), c)

    out = img.resize((W * SCALE, H * SCALE), Image.Resampling.NEAREST)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "global-channel-editorial-pixel-v4.png"
    draw_asset().save(path)
    print(path)


if __name__ == "__main__":
    main()
