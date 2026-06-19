from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "dispatch"


PALETTE = {
    "ink": (8, 16, 18, 255),
    "desk": (20, 30, 30, 255),
    "desk2": (13, 24, 27, 255),
    "paper": (224, 212, 165, 242),
    "paper2": (198, 188, 143, 238),
    "folder": (47, 58, 53, 245),
    "folder_edge": (161, 149, 106, 255),
    "cyan": (39, 190, 204, 255),
    "cyan_dark": (11, 92, 106, 255),
    "red": (220, 55, 45, 255),
    "red_dark": (120, 26, 25, 255),
    "cream": (242, 228, 176, 255),
    "black": (2, 8, 10, 255),
    "shadow": (0, 0, 0, 110),
}


def jitter(color: tuple[int, int, int, int], amount: int = 10) -> tuple[int, int, int, int]:
    return (
        max(0, min(255, color[0] + random.randint(-amount, amount))),
        max(0, min(255, color[1] + random.randint(-amount, amount))),
        max(0, min(255, color[2] + random.randint(-amount, amount))),
        color[3],
    )


def rect(draw: ImageDraw.ImageDraw, xy, fill, outline=None, width: int = 1) -> None:
    x0, y0, x1, y1 = [int(v) for v in xy]
    draw.rectangle((x0, y0, x1, y1), fill=fill, outline=outline, width=width)


def poly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width: int = 1) -> None:
    pts = [(int(x), int(y)) for x, y in points]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def add_pixel_noise(img: Image.Image, density: int = 2800, alpha: int = 34) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(density):
        x = random.randrange(w)
        y = random.randrange(h)
        if img.getpixel((x, y))[3] == 0:
            continue
        size = random.choice([1, 1, 2, 3])
        c = random.choice([(255, 255, 255, alpha), (0, 0, 0, alpha + 16), (33, 213, 222, alpha // 2), (229, 54, 45, alpha // 2)])
        d.rectangle((x, y, x + size, y + size), fill=c)


def add_halftone(img: Image.Image, box, color=(0, 0, 0, 48), step: int = 18, radius: int = 2) -> None:
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = [int(v) for v in box]
    for y in range(y0, y1, step):
        for x in range(x0 + ((y // step) % 2) * (step // 2), x1, step):
            d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def add_shadow(base: Image.Image, mask_box, blur: int = 16, offset=(10, 14), alpha: int = 120) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    x0, y0, x1, y1 = mask_box
    d.rectangle((x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]), fill=(0, 0, 0, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)


def draw_fake_lines(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, count: int, color=(20, 31, 34, 190), gap: int = 16) -> None:
    for i in range(count):
        line_w = int(w * random.uniform(0.45, 0.96))
        yy = y + i * gap
        draw.rectangle((x, yy, x + line_w, yy + 4), fill=color)


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name)
    print(OUT / name)


def make_workbench() -> None:
    random.seed(240601)
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), PALETTE["desk"])
    d = ImageDraw.Draw(img)
    for y in range(0, h, 8):
        c = jitter(PALETTE["desk2"], 4)
        d.rectangle((0, y, w, y + 7), fill=c)
    for x in range(-80, w + 160, 160):
        d.line((x, 0, x + 280, h), fill=(20, 40, 42, 52), width=2)
    for y in range(96, h, 160):
        d.line((0, y, w, y + random.randint(-6, 6)), fill=(6, 14, 16, 88), width=2)
    add_halftone(img, (0, 0, w, h), (2, 8, 10, 18), 26, 1)

    # Keep props at the edges only; functional papers are separate UI containers.
    d.rectangle((0, 740, w, h), fill=(8, 14, 16, 150))
    for x in range(80, w, 160):
        d.line((x, 742, x + 30, h), fill=(31, 53, 55, 46), width=2)
    add_shadow(img, (70, 790, 430, 1010), blur=18, offset=(16, 18), alpha=80)
    poly(d, [(85, 830), (405, 795), (430, 964), (116, 1015)], fill=(27, 39, 37, 170), outline=(54, 78, 76, 120), width=2)
    rect(d, (112, 858, 220, 904), fill=(224, 212, 165, 118), outline=(10, 16, 18, 110), width=2)
    rect(d, (244, 846, 374, 880), fill=(39, 190, 204, 92), outline=(10, 16, 18, 110), width=2)
    d.line((138, 944, 350, 912), fill=(220, 55, 45, 110), width=5)

    add_shadow(img, (1450, 810, 1780, 1005), blur=18, offset=(14, 18), alpha=90)
    rect(d, (1480, 858, 1590, 918), fill=PALETTE["red_dark"], outline=PALETTE["red"], width=3)
    rect(d, (1545, 800, 1590, 864), fill=(20, 28, 29, 220), outline=PALETTE["red"], width=2)
    d.ellipse((1558, 776, 1578, 796), fill=PALETTE["red"])
    d.line((1640, 928, 1790, 850), fill=(39, 190, 204, 150), width=7)
    d.line((1644, 940, 1798, 862), fill=(2, 8, 10, 190), width=3)
    add_pixel_noise(img, 900, 12)
    save(img, "dispatch-workbench-pixel-v1.png")


def make_mission_folder() -> None:
    random.seed(240602)
    img = Image.new("RGBA", (980, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    add_shadow(img, (32, 40, 930, 260), 12, (12, 14), 72)
    poly(d, [(40, 78), (210, 56), (252, 92), (920, 58), (940, 246), (54, 268)], fill=(39, 51, 48, 236), outline=(162, 150, 105, 245), width=4)
    poly(d, [(70, 105), (910, 82), (920, 238), (82, 252)], fill=(18, 31, 32, 244), outline=(14, 20, 21, 250), width=3)
    rect(d, (74, 105, 154, 132), fill=(220, 55, 45, 170), outline=PALETTE["black"], width=2)
    rect(d, (760, 174, 880, 218), fill=(19, 44, 47, 95), outline=(37, 199, 212, 120), width=3)
    add_halftone(img, (70, 100, 920, 250), (0, 0, 0, 8), 34, 1)
    add_pixel_noise(img, 80, 10)
    save(img, "dispatch-mission-folder-v1.png")


def make_dice_tray() -> None:
    random.seed(240603)
    img = Image.new("RGBA", (1040, 380), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    add_shadow(img, (24, 56, 1000, 330), 16, (16, 18), 90)
    poly(d, [(45, 74), (986, 50), (1014, 310), (72, 346)], fill=(10, 26, 28, 226), outline=(41, 164, 174, 165), width=4)
    poly(d, [(80, 106), (970, 88), (988, 292), (102, 322)], fill=(8, 18, 20, 210), outline=(8, 13, 14, 220), width=2)
    for i, x in enumerate([140, 365, 590, 815]):
        rect(d, (x, 132, x + 155, 250), fill=(22, 33, 35, 92), outline=(74, 91, 87, 110), width=3)
        d.rectangle((x + 22, 152, x + 58, 188), fill=(226, 213, 164, 42), outline=(7, 12, 13, 90), width=2)
        d.rectangle((x + 74, 152, x + 110, 188), fill=(39, 190, 204, 42) if i % 2 == 0 else (220, 55, 45, 42), outline=(7, 12, 13, 90), width=2)
    rect(d, (68, 70, 236, 104), fill=PALETTE["red"], outline=PALETTE["black"], width=2)
    add_halftone(img, (88, 100, 998, 318), (0, 0, 0, 10), 34, 1)
    add_pixel_noise(img, 80, 10)
    save(img, "dispatch-dice-tray-v1.png")


def make_review_sheet() -> None:
    random.seed(240604)
    img = Image.new("RGBA", (600, 820), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    add_shadow(img, (54, 26, 542, 790), 18, (18, 20), 95)
    poly(d, [(78, 42), (520, 28), (546, 768), (66, 792)], fill=(224, 212, 165, 236), outline=(42, 50, 47, 255), width=4)
    d.line((108, 144, 504, 130), fill=(220, 55, 45, 115), width=6)
    rect(d, (334, 672, 492, 742), fill=(170, 31, 26, 16), outline=(220, 55, 45, 128), width=5)
    for angle in range(-20, 21, 10):
        x = 410 + angle
        d.line((x - 65, 716, x + 65, 660), fill=(220, 55, 45, 120), width=4)
    add_halftone(img, (74, 38, 544, 780), (0, 0, 0, 8), 34, 1)
    add_pixel_noise(img, 80, 10)
    save(img, "dispatch-review-sheet-v1.png")


def make_red_stamp() -> None:
    random.seed(240605)
    img = Image.new("RGBA", (360, 180), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 180, 88
    for r, width, alpha in [(74, 6, 220), (60, 3, 160), (42, 4, 170)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(220, 45, 38, alpha), width=width)
    for i in range(6):
        y = 52 + i * 16
        d.line((102, y, 260, y - 12), fill=(220, 45, 38, 140), width=6)
    d.rectangle((78, 122, 282, 148), outline=(220, 45, 38, 210), width=5)
    add_pixel_noise(img, 120, 26)
    img = img.rotate(-10, resample=Image.Resampling.BICUBIC, expand=False)
    save(img, "dispatch-red-stamp-blank-v1.png")


def make_staff_card() -> None:
    random.seed(240606)
    img = Image.new("RGBA", (560, 190), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    add_shadow(img, (24, 24, 528, 166), 10, (8, 10), 84)
    poly(d, [(34, 40), (520, 22), (538, 148), (46, 170)], fill=(18, 32, 34, 238), outline=(126, 130, 108, 225), width=4)
    rect(d, (56, 55, 128, 140), fill=(9, 18, 20, 230), outline=(39, 190, 204, 150), width=3)
    d.rectangle((68, 70, 116, 118), fill=(42, 61, 62, 120))
    rect(d, (154, 58, 516, 92), fill=(224, 212, 165, 34), outline=None)
    rect(d, (154, 111, 516, 142), fill=(224, 212, 165, 24), outline=None)
    rect(d, (486, 38, 526, 60), fill=(220, 55, 45, 180), outline=PALETTE["black"], width=2)
    add_halftone(img, (40, 38, 532, 166), (0, 0, 0, 8), 34, 1)
    add_pixel_noise(img, 50, 8)
    save(img, "dispatch-staff-card-frame-v1.png")


def main() -> None:
    make_workbench()
    make_mission_folder()
    make_dice_tray()
    make_review_sheet()
    make_red_stamp()
    make_staff_card()


if __name__ == "__main__":
    main()
