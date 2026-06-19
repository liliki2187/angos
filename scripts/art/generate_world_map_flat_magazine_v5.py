from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map"

SCALE = 2
W, H = 750, 540

INK = (3, 9, 12, 255)
PANEL = (5, 24, 29, 245)
GRID = (31, 111, 122, 16)
CREAM = (243, 240, 232, 238)
PAPER = (236, 232, 222, 248)
PAPER_DIM = (224, 226, 220, 255)
PAPER_INK = (13, 25, 30, 230)
LAND = (148, 184, 181, 210)
LAND_DARK = (101, 145, 148, 190)
RED = (205, 42, 32, 230)
RED_DIM = (158, 32, 28, 130)
CYAN = (31, 174, 190, 220)
CYAN_DIM = (32, 144, 156, 132)
GOLD = (222, 168, 59, 230)


def load_font(size: int, bold: bool = False, cn: bool = False) -> ImageFont.ImageFont:
    candidates = []
    if cn:
        candidates.extend([
            Path("C:/Windows/Fonts/NotoSansSC-VF.ttf"),
            Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
            Path("C:/Windows/Fonts/simhei.ttf"),
        ])
    candidates.extend([
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/NotoSans-Bold.ttf" if bold else "C:/Windows/Fonts/NotoSans-Regular.ttf"),
    ])
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def rect(draw: ImageDraw.ImageDraw, box, fill, outline=None, width: int = 1) -> None:
    draw.rectangle(tuple(int(v) for v in box), fill=fill, outline=outline, width=width)


def poly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width: int = 1) -> None:
    pts = [(int(x), int(y)) for x, y in points]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width)


def p(box: tuple[int, int, int, int], x: float, y: float) -> tuple[int, int]:
    x0, y0, x1, y1 = box
    return int(x0 + (x1 - x0) * x), int(y0 + (y1 - y0) * y)


def bars(draw: ImageDraw.ImageDraw, x: int, y: int, widths: list[int], color, h: int = 4) -> None:
    xx = x
    for width in widths:
        rect(draw, (xx, y, xx + width, y + h), color)
        xx += width + 6


def label_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color, size: int = 14, bold: bool = False, cn: bool = False) -> None:
    draw.text(xy, text, fill=color, font=load_font(size, bold, cn))


def draw_tag(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill, accent, cn: bool = True, icon: str = "") -> None:
    x, y = xy
    w = 110 if len(text) <= 5 else 130
    h = 30
    rect(draw, (x + 4, y + 4, x + w + 4, y + h + 4), (1, 5, 7, 110))
    rect(draw, (x, y, x + w, y + h), fill, INK, 2)
    rect(draw, (x, y, x + 12, y + h), accent)
    if icon:
        label_text(draw, (x + 17, y + 7), icon, INK, 15, True, False)
        label_text(draw, (x + 36, y + 8), text, INK, 13, True, cn)
    else:
        label_text(draw, (x + 18, y + 8), text, INK, 13, True, cn)


def halftone(draw: ImageDraw.ImageDraw, box, color, step: int = 10, max_size: int = 3, fade_x: bool = True) -> None:
    x0, y0, x1, y1 = [int(v) for v in box]
    span = max(1, x1 - x0)
    for y in range(y0, y1, step):
        shift = ((y // step) & 1) * (step // 2)
        for x in range(x0 + shift, x1, step):
            t = (x - x0) / span if fade_x else 0.75
            r = max(1, int(1 + t * max_size))
            rect(draw, (x - r, y - r, x + r, y + r), color)


def draw_land(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    shapes = [
        ([p(box, 0.10, 0.24), p(box, 0.19, 0.16), p(box, 0.31, 0.16), p(box, 0.39, 0.27), p(box, 0.36, 0.42), p(box, 0.27, 0.50), p(box, 0.16, 0.46)], LAND),
        ([p(box, 0.30, 0.51), p(box, 0.38, 0.59), p(box, 0.36, 0.78), p(box, 0.31, 0.90), p(box, 0.24, 0.70)], LAND_DARK),
        ([p(box, 0.44, 0.27), p(box, 0.53, 0.19), p(box, 0.69, 0.17), p(box, 0.84, 0.25), p(box, 0.93, 0.38), p(box, 0.84, 0.51), p(box, 0.65, 0.48), p(box, 0.53, 0.55), p(box, 0.47, 0.44)], LAND),
        ([p(box, 0.54, 0.49), p(box, 0.66, 0.51), p(box, 0.70, 0.66), p(box, 0.64, 0.80), p(box, 0.55, 0.75), p(box, 0.49, 0.62)], LAND_DARK),
        ([p(box, 0.76, 0.71), p(box, 0.90, 0.72), p(box, 0.88, 0.83), p(box, 0.75, 0.82)], LAND),
        ([p(box, 0.80, 0.42), p(box, 0.89, 0.42), p(box, 0.91, 0.53), p(box, 0.84, 0.58)], LAND_DARK),
        ([p(box, 0.34, 0.10), p(box, 0.42, 0.08), p(box, 0.45, 0.16), p(box, 0.36, 0.18)], LAND_DARK),
    ]
    for pts, fill in shapes:
        poly(draw, pts, fill, (226, 238, 226, 106), 2)
        for x, y in pts:
            rect(draw, (x - 1, y - 1, x + 1, y + 1), (221, 236, 224, 70))

    random.seed(60705)
    for _ in range(240):
        x = random.randint(box[0] + 36, box[2] - 36)
        y = random.randint(box[1] + 34, box[3] - 40)
        if random.random() < 0.45:
            rect(draw, (x, y, x + 2, y + 2), (10, 26, 28, 46))


def draw_signal(draw: ImageDraw.ImageDraw, center: tuple[int, int]) -> None:
    cx, cy = center
    for x, y in [(cx - 58, cy - 34), (cx + 50, cy - 28), (cx - 44, cy + 42), (cx + 34, cy + 50)]:
        rect(draw, (x, y, x + 18, y + 4), (243, 240, 232, 34))
    draw.ellipse((cx - 23, cy - 23, cx + 23, cy + 23), fill=(4, 10, 12, 244), outline=CREAM, width=2)
    draw.ellipse((cx - 8, cy - 4, cx - 3, cy + 4), fill=(232, 221, 180, 230))
    draw.ellipse((cx + 5, cy - 4, cx + 10, cy + 4), fill=(232, 221, 180, 230))


def draw_route(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color, width: int = 2) -> None:
    for a, b in zip(points, points[1:]):
        draw.line((a, b), fill=color, width=width)
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        length = max(1, int(math.hypot(dx, dy)))
        for step in range(12, length, 28):
            t = step / length
            x = int(a[0] + dx * t)
            y = int(a[1] + dy * t)
            rect(draw, (x - 2, y - 2, x + 2, y + 2), color)


def draw_pin_safe_marks(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    pins = [
        (0.18, 0.37, RED),
        (0.45, 0.31, RED),
        (0.72, 0.38, RED),
        (0.31, 0.60, CYAN),
        (0.53, 0.65, CYAN),
        (0.80, 0.57, CYAN),
        (0.62, 0.77, GOLD),
    ]
    for x, y, color in pins:
        cx, cy = p(box, x, y)
        faint = (color[0], color[1], color[2], 64)
        paper_edge = (243, 240, 232, 82)
        rect(draw, (cx - 11, cy - 6, cx + 11, cy + 6), (color[0], color[1], color[2], 34), paper_edge, 1)
        draw.line((cx - 14, cy, cx - 5, cy), fill=faint, width=2)
        draw.line((cx + 5, cy, cx + 14, cy), fill=faint, width=2)
        rect(draw, (cx - 2, cy - 2, cx + 2, cy + 2), paper_edge)


def draw_asset() -> Image.Image:
    random.seed(260707)
    img = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(img)

    rect(draw, (0, 0, W, H), (4, 12, 14, 255))
    for y in range(0, H, 8):
        rect(draw, (0, y, W, y + 1), (12, 30, 34, 42))

    rect(draw, (22, 26, W - 22, H - 28), (7, 21, 24, 246), (37, 126, 134, 82), 2)
    rect(draw, (34, 38, W - 34, 78), (9, 17, 18, 218), (205, 42, 32, 102), 1)
    rect(draw, (34, 38, 312, 78), RED, None)
    label_text(draw, (54, 50), "WORLD MAP / EDITORIAL WORK WALL", CREAM, 14, True)
    bars(draw, 332, 52, [42, 18, 62, 18, 38], (33, 166, 180, 150), 5)
    label_text(draw, (W - 168, 47), "WMW  ISSUE_001", (243, 240, 232, 145), 12, True)

    map_box = (52, 94, W - 52, H - 64)
    rect(draw, (map_box[0] - 16, map_box[1] - 18, map_box[2] + 16, map_box[3] + 18), (1, 6, 7, 148), None)
    rect(draw, (map_box[0] - 8, map_box[1] - 10, map_box[2] + 10, map_box[3] + 12), (226, 224, 214, 178), (12, 19, 18, 130), 1)
    rect(draw, map_box, (242, 239, 229, 252), (20, 34, 35, 168), 2)
    rect(draw, (map_box[0] + 10, map_box[1] + 10, map_box[2] - 10, map_box[3] - 10), (255, 250, 234, 26), (20, 92, 100, 46), 1)
    rect(draw, (map_box[0] + 18, map_box[1] - 8, map_box[0] + 118, map_box[1] + 12), (243, 240, 232, 150), None)
    rect(draw, (map_box[2] - 138, map_box[3] - 10, map_box[2] - 36, map_box[3] + 10), (243, 240, 232, 136), None)
    rect(draw, (map_box[0] + 218, map_box[1] - 7, map_box[0] + 288, map_box[1] + 10), (243, 240, 232, 92), None)
    rect(draw, (map_box[2] - 190, map_box[1] + 8, map_box[2] - 130, map_box[1] + 24), (243, 240, 232, 84), None)
    draw.line((map_box[0] + 4, map_box[1] + 124, map_box[2] - 10, map_box[1] + 120), fill=(5, 18, 20, 26), width=1)
    draw.line((map_box[0] + 286, map_box[1] + 2, map_box[0] + 294, map_box[3] - 4), fill=(5, 18, 20, 30), width=1)
    for x in range(map_box[0] + 36, map_box[2], 54):
        draw.line((x, map_box[1], x, map_box[3]), fill=(31, 111, 122, 28), width=1)
    for y in range(map_box[1] + 28, map_box[3], 48):
        draw.line((map_box[0], y, map_box[2], y), fill=(31, 111, 122, 24), width=1)

    poly(draw, [p(map_box, 0.00, 0.70), p(map_box, 0.26, 0.55), p(map_box, 0.18, 1.00), p(map_box, 0.00, 1.00)], (205, 42, 32, 168))
    poly(draw, [p(map_box, 0.76, 0.00), p(map_box, 1.00, 0.00), p(map_box, 1.00, 0.36), p(map_box, 0.88, 0.30)], (31, 174, 190, 150))
    halftone(draw, (map_box[0], map_box[3] - 132, map_box[0] + 180, map_box[3]), (220, 36, 32, 100), 8, 4)
    halftone(draw, (map_box[2] - 190, map_box[1], map_box[2], map_box[1] + 158), (31, 174, 190, 90), 8, 4)

    draw_land(draw, map_box)
    center = p(map_box, 0.50, 0.55)
    draw_signal(draw, center)
    draw_route(draw, [p(map_box, 0.18, 0.37), p(map_box, 0.45, 0.31), p(map_box, 0.72, 0.38)], (205, 42, 32, 118), 3)
    draw_route(draw, [p(map_box, 0.31, 0.60), p(map_box, 0.53, 0.65), p(map_box, 0.80, 0.57)], (31, 174, 190, 118), 2)
    draw_route(draw, [p(map_box, 0.50, 0.55), p(map_box, 0.62, 0.77)], (222, 168, 59, 118), 2)
    draw_pin_safe_marks(draw, map_box)

    draw_tag(draw, p(map_box, 0.04, 0.20), "红条截稿", RED, (118, 18, 14, 255), True, "!")
    draw_tag(draw, p(map_box, 0.78, 0.34), "青条追踪", CYAN, (14, 106, 116, 255), True, "?")
    label_text(draw, p(map_box, 0.07, 0.28), "剩 7 天", (118, 18, 14, 198), 12, True, True)
    label_text(draw, p(map_box, 0.81, 0.42), "线索钉住", (14, 106, 116, 198), 12, True, True)

    # Crop marks and editorial proof bars.
    for x, y in [(40, 88), (W - 40, 88), (40, H - 46), (W - 40, H - 46)]:
        draw.line((x - 9, y, x + 9, y), fill=(232, 224, 204, 112), width=1)
        draw.line((x, y - 9, x, y + 9), fill=(232, 224, 204, 112), width=1)
    bars(draw, 62, H - 46, [36, 18, 18, 70, 12], (232, 224, 204, 120), 3)
    bars(draw, W - 214, H - 46, [22, 52, 12, 12, 44], (31, 174, 190, 140), 3)

    # Light pixel print noise, kept clean.
    for _ in range(620):
        x = random.randrange(W)
        y = random.randrange(H)
        color = random.choice([(255, 248, 226, 14), (0, 0, 0, 24), (31, 174, 190, 16), (205, 42, 32, 16)])
        rect(draw, (x, y, x + random.choice([0, 1]), y + random.choice([0, 1])), color)

    return img.resize((W * SCALE, H * SCALE), Image.Resampling.NEAREST)


def draw_story_preview() -> Image.Image:
    w, h = 520, 190
    random.seed(260708)
    img = Image.new("RGBA", (w, h), (5, 24, 30, 255))
    draw = ImageDraw.Draw(img)
    rect(draw, (0, 0, w, h), (7, 32, 39, 255), (232, 224, 204, 115), 2)
    for y in range(0, h, 10):
        rect(draw, (0, y, w, y + 1), (15, 52, 58, 44))

    poly(draw, [(w * 0.72, 0), (w, 0), (w, h), (w * 0.86, h)], (165, 34, 28, 205))
    halftone(draw, (int(w * 0.72), 0, w, h), (3, 9, 12, 85), 8, 4)
    poly(draw, [(0, h * 0.74), (w * 0.33, h * 0.48), (w * 0.52, h), (0, h)], (22, 120, 134, 150))
    rect(draw, (16, 14, 174, 42), (5, 16, 20, 210), (232, 224, 204, 95), 1)
    label_text(draw, (26, 21), "北美禁区带", CREAM, 15, True, True)
    rect(draw, (392, 16, 486, 48), RED, INK, 2)
    label_text(draw, (416, 24), "?!", INK, 20, True)
    rect(draw, (360, 134, 488, 160), CYAN, INK, 2)
    label_text(draw, (378, 141), "青条追踪", INK, 13, True, True)

    horizon = int(h * 0.74)
    for i in range(20):
        x = int(i * w / 19)
        bw = random.randint(10, 28)
        bh = random.randint(34, 106)
        rect(draw, (x - bw // 2, horizon - bh, x + bw // 2, horizon), (2, 9, 12, 230))
        for yy in range(horizon - bh + 8, horizon - 5, 13):
            for xx in range(x - bw // 2 + 3, x + bw // 2 - 2, 8):
                if random.random() < 0.45:
                    rect(draw, (xx, yy, xx + 2, yy + 3), random.choice([RED, CYAN, CREAM]))

    cx, cy = int(w * 0.54), int(h * 0.38)
    for x, y in [(cx - 42, cy - 24), (cx + 34, cy - 20), (cx - 32, cy + 30), (cx + 24, cy + 34)]:
        rect(draw, (x, y, x + 14, y + 3), (243, 240, 232, 34))
    draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(3, 8, 10, 246), outline=CREAM, width=2)
    draw.ellipse((cx - 7, cy - 3, cx - 3, cy + 3), fill=CREAM)
    draw.ellipse((cx + 4, cy - 3, cx + 8, cy + 3), fill=CREAM)

    bars(draw, 16, h - 24, [42, 18, 82, 26, 46], (232, 224, 204, 120), 4)
    for _ in range(420):
        x = random.randrange(w)
        y = random.randrange(h)
        c = random.choice([(255, 248, 226, 16), (0, 0, 0, 24), (31, 174, 190, 16), (205, 42, 32, 16)])
        rect(draw, (x, y, x + random.choice([0, 1]), y + random.choice([0, 1])), c)
    return img.resize((w * 2, h * 2), Image.Resampling.NEAREST)


def draw_world_ui_shell() -> Image.Image:
    w, h = 1920, 1080
    random.seed(260709)
    img = Image.new("RGBA", (w, h), (5, 12, 16, 255))
    draw = ImageDraw.Draw(img)

    for y in range(0, h, 6):
        rect(draw, (0, y, w, y + 1), (13, 32, 37, 80))
    for x in range(0, w, 80):
        draw.line((x, 0, x, h), fill=(26, 88, 96, 34), width=1)

    # Top masthead.
    rect(draw, (24, 20, 1896, 108), (5, 13, 16, 245), (34, 126, 136, 130), 2)
    rect(draw, (38, 30, 124, 98), RED, (235, 190, 96, 95), 1)
    draw.ellipse((66, 54, 94, 82), outline=CREAM, width=2)
    draw.ellipse((74, 62, 86, 74), outline=CREAM, width=2)
    rect(draw, (1228, 28, 1762, 100), (6, 18, 21, 245), (68, 164, 170, 115), 1)
    bars(draw, 1284, 56, [54, 12, 12, 40, 12, 12], RED, 5)
    bars(draw, 1476, 56, [30, 18, 18, 66, 24, 12], CYAN, 5)
    bars(draw, 1650, 56, [24, 12, 12, 12, 12], GOLD, 5)

    # Left index shell.
    rect(draw, (24, 116, 332, 942), (5, 13, 15, 242), (34, 126, 136, 130), 2)
    rect(draw, (40, 138, 250, 168), (8, 24, 28, 250), (34, 126, 136, 115), 1)
    for i in range(4):
        y = 188 + i * 118
        tab_color = RED if i % 2 == 0 else CYAN
        rect(draw, (42, y - 10, 94, y + 8), tab_color)
        rect(draw, (52, y, 318, y + 80), CREAM, (22, 22, 18, 200), 2)
        rect(draw, (52, y, 65, y + 80), tab_color)
        draw.ellipse((248, y + 22, 292, y + 66), outline=tab_color, width=4)
        bars(draw, 86, y + 27, [30, 42, 18], (16, 24, 22, 185), 4)
        bars(draw, 86, y + 52, [18, 18, 18, 18, 18], tab_color, 4)
    rect(draw, (42, 694, 318, 734), (10, 16, 18, 245), (68, 58, 42, 160), 1)

    # Center map frame.
    rect(draw, (344, 116, 1468, 942), (4, 16, 20, 248), (28, 119, 128, 150), 3)
    rect(draw, (368, 136, 724, 174), RED, None)
    bars(draw, 750, 150, [64, 22, 112, 30, 64], CYAN, 5)
    halftone(draw, (352, 666, 520, 858), (205, 42, 32, 70), 8, 4)
    halftone(draw, (1280, 138, 1440, 312), (31, 174, 190, 60), 8, 4)

    # Right story shell.
    rect(draw, (1482, 116, 1896, 942), PAPER, (12, 15, 13, 230), 2)
    rect(draw, (1498, 136, 1646, 166), RED, None)
    rect(draw, (1500, 206, 1876, 344), (5, 26, 32, 255), (12, 15, 13, 190), 1)
    rect(draw, (1500, 374, 1876, 450), PAPER_DIM, (12, 15, 13, 180), 1)
    rect(draw, (1500, 466, 1876, 540), PAPER_DIM, (12, 15, 13, 180), 1)
    bars(draw, 1538, 404, [80, 22, 22, 22, 22, 22, 22], RED, 6)
    bars(draw, 1538, 496, [120, 22, 22, 22, 22, 22], CYAN, 6)
    rect(draw, (1500, 878, 1876, 924), (16, 132, 145, 255), (232, 224, 204, 150), 1)

    # Bottom action/proof shell.
    rect(draw, (24, 950, 1896, 1058), (5, 15, 18, 248), (28, 119, 128, 130), 2)
    rect(draw, (38, 990, 142, 1020), (6, 26, 30, 255), (31, 174, 190, 130), 1)
    for i in range(3):
        x = 152 + i * 436
        rect(draw, (x, 980, x + 424, 1028), PAPER, (20, 22, 18, 195), 1)
        rect(draw, (x + 10, 990, x + 44, 1020), RED if i == 0 else CYAN if i == 1 else GOLD)
        bars(draw, x + 58, 996, [74, 20, 20, 20], PAPER_INK, 4)
    for i in range(3):
        x = 1460 + i * 132
        rect(draw, (x, 976, x + 112, 1028), (7, 28, 33, 255), (232, 224, 204, 100), 1)
        bars(draw, x + 10, 986, [22, 18, 42], CYAN if i == 0 else RED if i == 1 else CREAM, 3)

    for _ in range(1120):
        x = random.randrange(w)
        y = random.randrange(h)
        c = random.choice([(255, 248, 226, 10), (0, 0, 0, 22), (31, 174, 190, 12), (205, 42, 32, 12)])
        rect(draw, (x, y, x + random.choice([0, 1]), y + random.choice([0, 1])), c)
    return img


def crop_editor_sticker() -> Image.Image | None:
    source = ROOT / "docs" / "screenshots" / "2026-06-07-global-channel-style-board" / "07-global-channel-full-interface-style-draft-flat-magazine-ui.png"
    if not source.exists():
        return None
    image = Image.open(source).convert("RGBA")
    return image.crop((1000, 524, 1196, 724))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "global-channel-flat-magazine-map-v5.png"
    draw_asset().save(path)
    story_path = OUT / "global-channel-story-preview-v1.png"
    draw_story_preview().save(story_path)
    shell_path = OUT / "global-channel-world-ui-shell-v1.png"
    draw_world_ui_shell().save(shell_path)
    sticker = crop_editor_sticker()
    if sticker is not None:
        sticker_path = OUT / "global-channel-editor-sticker-v1.png"
        sticker.save(sticker_path)
    print(path)
    print(story_path)
    print(shell_path)


if __name__ == "__main__":
    main()
