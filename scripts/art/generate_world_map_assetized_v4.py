from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map" / "assetized"

INK = (4, 13, 17, 255)
INK_2 = (8, 24, 29, 255)
INK_SOFT = (14, 36, 42, 230)
CREAM = (232, 214, 166, 255)
PAPER = (224, 211, 178, 255)
PAPER_DIM = (194, 187, 166, 245)
RED = (226, 55, 42, 255)
RED_DARK = (118, 27, 25, 255)
CYAN = (39, 198, 211, 255)
CYAN_DARK = (14, 96, 108, 255)
GOLD = (221, 170, 74, 255)
GRAY = (112, 116, 111, 255)
BLACK = (2, 6, 8, 255)


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path)
    print(path)


def rect(draw: ImageDraw.ImageDraw, box, fill, outline=None, width: int = 1) -> None:
    draw.rectangle(tuple(int(v) for v in box), fill=fill, outline=outline, width=width)


def line(draw: ImageDraw.ImageDraw, xy, fill, width: int = 1) -> None:
    draw.line(tuple((int(x), int(y)) for x, y in xy), fill=fill, width=width)


def add_pixel_noise(img: Image.Image, count: int, alpha: int = 36) -> None:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    colors = [
        (255, 244, 206, max(7, alpha // 2)),
        (0, 0, 0, alpha),
        (39, 198, 211, max(7, alpha // 3)),
        (226, 55, 42, max(7, alpha // 3)),
    ]
    for _ in range(count):
        x = random.randrange(w)
        y = random.randrange(h)
        size = random.choice([1, 1, 1, 2])
        rect(draw, (x, y, x + size, y + size), random.choice(colors))


def add_halftone(draw: ImageDraw.ImageDraw, box, color, step: int = 8, radius: int = 1) -> None:
    x0, y0, x1, y1 = [int(v) for v in box]
    for y in range(y0, y1, step):
        offset = ((y // step) % 2) * (step // 2)
        for x in range(x0 + offset, x1, step):
            draw.rectangle((x - radius, y - radius, x + radius, y + radius), fill=color)


def draw_broken_frame(draw: ImageDraw.ImageDraw, w: int, h: int, color, accent) -> None:
    segments = [
        (0, 0, w // 3, 0),
        (w // 3 + 18, 0, w - 20, 0),
        (0, h - 1, w // 2, h - 1),
        (w // 2 + 26, h - 1, w - 1, h - 1),
        (0, 0, 0, h - 16),
        (w - 1, 18, w - 1, h - 1),
    ]
    for x0, y0, x1, y1 in segments:
        line(draw, [(x0, y0), (x1, y1)], color, 2)
    rect(draw, (8, 8, 20, 14), accent)
    rect(draw, (w - 26, h - 15, w - 12, h - 9), accent)


def make_panel_left() -> Image.Image:
    random.seed(61140)
    w, h = 320, 860
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect(draw, (0, 0, w - 1, h - 1), (3, 15, 17, 238), (25, 156, 170, 130), 2)
    rect(draw, (5, 6, w - 7, 64), (7, 26, 30, 220), (226, 55, 42, 120), 2)
    rect(draw, (7, 10, 76, 56), (98, 24, 25, 190))
    for i in range(8):
        y = 92 + i * 76
        rect(draw, (14, y, w - 16, y + 1), (226, 55, 42, 42) if i % 2 == 0 else (39, 198, 211, 42))
        rect(draw, (14, y + 54, w - 16, y + 55), (226, 55, 42, 24) if i % 2 == 0 else (39, 198, 211, 24))
    add_halftone(draw, (4, 84, w - 12, h - 80), (0, 0, 0, 42), 10, 1)
    add_pixel_noise(img, 220, 24)
    return img


def make_panel_right() -> Image.Image:
    random.seed(61141)
    w, h = 440, 860
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect(draw, (14, 0, w - 22, h - 16), PAPER, (9, 13, 12, 220), 3)
    rect(draw, (36, 18, w - 52, 224), (5, 20, 25, 255), (5, 9, 10, 255), 3)
    rect(draw, (38, 226, w - 56, 231), BLACK)
    rect(draw, (58, 252, w - 154, 294), (203, 190, 162, 170))
    rect(draw, (w - 138, 252, w - 58, 294), (206, 190, 164, 150))
    rect(draw, (58, 330, 82, 352), RED_DARK)
    rect(draw, (58, 368, 82, 390), RED)
    rect(draw, (110, 330, w - 160, 342), (120, 112, 96, 130))
    rect(draw, (110, 368, w - 120, 380), (120, 112, 96, 120))
    rect(draw, (w - 118, 330, w - 56, 438), (226, 55, 42, 42), RED, 2)
    add_halftone(draw, (w - 112, 336, w - 62, 432), (226, 55, 42, 85), 8, 1)
    for idx, color in enumerate([RED, CYAN, (20, 56, 63, 255), GOLD]):
        y = 54 + idx * 116
        points = [(w - 22, y), (w - 2, y + 12), (w - 2, y + 90), (w - 22, y + 104)]
        draw.polygon(points, fill=color)
        rect(draw, (w - 21, y + 44, w - 9, y + 58), (2, 8, 10, 210))
    rect(draw, (154, 0, 292, 22), RED, (7, 10, 10, 230), 2)
    draw_broken_frame(draw, w, h, (3, 8, 9, 185), CYAN)
    add_pixel_noise(img, 420, 25)
    return img


def make_bottom_strip() -> Image.Image:
    random.seed(61142)
    w, h = 1280, 92
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect(draw, (0, 0, w - 1, h - 1), (4, 17, 21, 235), (28, 112, 124, 145), 2)
    rect(draw, (14, 12, 128, h - 14), (8, 30, 36, 235), (32, 142, 154, 120), 1)
    for x in [158, 438, 718, 998]:
        rect(draw, (x, 12, x + 246, h - 14), (9, 25, 30, 230), (31, 62, 70, 130), 1)
        rect(draw, (x, 12, x + 10, h - 14), random.choice([RED, CYAN, GOLD]))
    for x in range(140, w - 60, 72):
        rect(draw, (x, h - 18, x + 18, h - 12), random.choice([RED, CYAN, (188, 182, 160, 170)]))
    add_halftone(draw, (0, 0, w, h), (0, 0, 0, 36), 10, 1)
    add_pixel_noise(img, 160, 22)
    return img


def make_region_strip(accent, locked: bool = False) -> Image.Image:
    random.seed(61143 + (1 if accent == CYAN else 0) + (3 if locked else 0))
    w, h = 320, 82
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    body = (5, 23, 28, 238) if not locked else (26, 29, 29, 190)
    edge = accent if not locked else GRAY
    rect(draw, (0, 8, w - 4, h - 7), body, (27, 66, 72, 145), 1)
    rect(draw, (0, 8, 46, h - 7), edge)
    rect(draw, (6, 16, 36, 46), (3, 11, 13, 230), (232, 214, 166, 140), 2)
    line(draw, [(12, 54), (38, 54)], (232, 214, 166, 130), 2)
    for j in range(5):
        color = edge if j < 3 else (150, 154, 148, 150)
        rect(draw, (216 + j * 16, 27, 226 + j * 16, 37), color)
    rect(draw, (w - 42, 23, w - 20, 45), (0, 0, 0, 0), (118, 128, 120, 120), 2)
    add_halftone(draw, (46, 12, w - 54, h - 12), (0, 0, 0, 34), 12, 1)
    add_pixel_noise(img, 44, 20)
    return img


def make_ticket(accent) -> Image.Image:
    random.seed(61144 + (1 if accent == CYAN else 0))
    w, h = 420, 62
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect(draw, (0, 5, w - 1, h - 6), PAPER_DIM, (9, 15, 14, 210), 2)
    rect(draw, (0, 5, 20, h - 6), accent)
    rect(draw, (38, 17, 72, 28), (135, 128, 110, 80))
    rect(draw, (82, 17, 170, 28), (135, 128, 110, 80))
    rect(draw, (38, 36, 246, 46), (135, 128, 110, 70))
    add_pixel_noise(img, 36, 18)
    return img


def make_log_chip(accent, dark: bool = True) -> Image.Image:
    random.seed(61145 + accent[0])
    w, h = 360, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    body = (6, 24, 29, 238) if dark else PAPER_DIM
    rect(draw, (0, 4, w - 1, h - 5), body, (33, 76, 82, 135), 1)
    rect(draw, (8, 12, 38, h - 13), accent)
    rect(draw, (54, 18, 118, 26), (232, 214, 166, 90) if dark else (110, 100, 84, 90))
    for j in range(4):
        rect(draw, (132 + j * 18, 18, 144 + j * 18, 26), (232, 214, 166, 65) if dark else (110, 100, 84, 80))
    add_halftone(draw, (42, 12, w - 16, h - 10), (0, 0, 0, 34), 10, 1)
    add_pixel_noise(img, 32, 18)
    return img


def make_cta() -> Image.Image:
    random.seed(61146)
    w, h = 420, 58
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect(draw, (0, 5, w - 1, h - 6), (21, 146, 154, 245), (232, 214, 166, 180), 2)
    rect(draw, (0, 5, 36, h - 6), CYAN_DARK)
    rect(draw, (w - 58, 5, w - 1, h - 6), RED)
    for x in [w - 48, w - 34, w - 20]:
        line(draw, [(x, 18), (x + 10, 29), (x, 40)], CREAM, 3)
    add_pixel_noise(img, 45, 18)
    return img


def make_pin(accent, symbol: str) -> Image.Image:
    scale = 2
    w, h = 56, 68
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    body = [(28, 3), (51, 24), (33, 41), (28, 63), (23, 41), (5, 24)]
    for dx, dy, color in [(2, 3, BLACK), (0, 0, CREAM), (0, 0, accent)]:
        pts = [(x + dx, y + dy) for x, y in body]
        draw.polygon(pts, fill=color)
        draw.line(pts + [pts[0]], fill=BLACK if color == accent else color, width=2)
    draw.polygon([(28, 10), (43, 24), (28, 38), (13, 24)], fill=(5, 18, 22, 245), outline=CREAM)
    if symbol == "lock":
        rect(draw, (22, 23, 34, 33), CREAM)
        draw.arc((21, 14, 35, 28), 180, 360, fill=CREAM, width=3)
        rect(draw, (27, 27, 29, 32), BLACK)
    elif symbol == "chain":
        draw.ellipse((20, 18, 31, 29), outline=CYAN, width=3)
        draw.ellipse((26, 22, 37, 33), outline=CREAM, width=3)
    elif symbol == "alert":
        rect(draw, (26, 16, 30, 29), CREAM)
        rect(draw, (26, 33, 30, 37), CREAM)
    else:
        draw.ellipse((18, 14, 38, 34), outline=CREAM, width=3)
        line(draw, [(28, 11), (28, 37)], accent, 2)
        line(draw, [(15, 24), (41, 24)], accent, 2)
        draw.ellipse((24, 20, 32, 28), fill=CREAM)
    add_pixel_noise(img, 22, 20)
    return img.resize((w * scale, h * scale), Image.Resampling.NEAREST)


def make_story_preview() -> Image.Image:
    random.seed(61147)
    w, h = 760, 290
    img = Image.new("RGBA", (w, h), (5, 21, 27, 255))
    draw = ImageDraw.Draw(img)
    for y in range(0, h, 6):
        line(draw, [(0, y), (w, y)], (0, 0, 0, 38), 1)
    for x in range(0, w, 18):
        building_h = random.randint(44, 128)
        rect(draw, (x, h - building_h, x + random.randint(8, 18), h - 20), (10, 29, 35, 245))
        if random.random() > 0.62:
            rect(draw, (x + 3, h - building_h + 12, x + 7, h - building_h + 17), RED)
    cx, cy = w // 2, 105
    for r, alpha in [(168, 46), (124, 80), (84, 140), (48, 220)]:
        draw.ellipse((cx - r, cy - r // 2, cx + r, cy + r // 2), outline=(226, 55, 42, alpha), width=8)
    draw.polygon([(cx - 164, cy), (cx - 70, cy - 44), (cx, cy - 54), (cx + 70, cy - 44), (cx + 164, cy), (cx + 70, cy + 44), (cx, cy + 54), (cx - 70, cy + 44)], fill=(226, 55, 42, 105))
    draw.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=(6, 20, 25, 255), outline=CREAM, width=4)
    draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=RED)
    add_halftone(draw, (0, 0, w, h), (0, 0, 0, 48), 9, 1)
    add_halftone(draw, (cx - 210, cy - 90, cx + 210, cy + 100), (226, 55, 42, 58), 10, 1)
    add_pixel_noise(img, 520, 24)
    return img


def make_contact_sheet(files: list[tuple[str, Image.Image]]) -> None:
    thumb_w, thumb_h = 320, 160
    cols = 3
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * thumb_w, rows * thumb_h), (12, 18, 22, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for idx, (name, img) in enumerate(files):
        col = idx % cols
        row = idx // cols
        x, y = col * thumb_w, row * thumb_h
        preview = img.copy()
        preview.thumbnail((thumb_w - 24, thumb_h - 42), Image.Resampling.NEAREST)
        sheet.alpha_composite(preview, (x + 12, y + 28))
        draw.text((x + 12, y + 8), name, fill=(232, 214, 166, 255), font=font)
        rect(draw, (x, y, x + thumb_w - 1, y + thumb_h - 1), (0, 0, 0, 0), (35, 80, 88, 140), 1)
    save(sheet, "wm-assetized-v4-contact-sheet.png")


def main() -> None:
    random.seed(61148)
    assets = [
        ("wm-panel-left-index-v4.png", make_panel_left()),
        ("wm-panel-right-detail-v4.png", make_panel_right()),
        ("wm-bottom-log-strip-v4.png", make_bottom_strip()),
        ("wm-region-strip-red-v4.png", make_region_strip(RED)),
        ("wm-region-strip-cyan-v4.png", make_region_strip(CYAN)),
        ("wm-region-strip-locked-v4.png", make_region_strip(GRAY, True)),
        ("wm-ticket-deadline-v4.png", make_ticket(RED)),
        ("wm-ticket-chain-v4.png", make_ticket(CYAN)),
        ("wm-log-chip-red-v4.png", make_log_chip(RED)),
        ("wm-log-chip-cyan-v4.png", make_log_chip(CYAN)),
        ("wm-log-chip-gold-v4.png", make_log_chip(GOLD)),
        ("wm-log-chip-next-v4.png", make_log_chip(CYAN)),
        ("wm-cta-enter-region-v4.png", make_cta()),
        ("wm-pin-symbol-red-v4.png", make_pin(RED, "alert")),
        ("wm-pin-symbol-cyan-v4.png", make_pin(CYAN, "chain")),
        ("wm-pin-symbol-gold-v4.png", make_pin(GOLD, "target")),
        ("wm-pin-symbol-normal-v4.png", make_pin(CREAM, "target")),
        ("wm-pin-symbol-locked-v4.png", make_pin(GRAY, "lock")),
        ("wm-story-preview-v4.png", make_story_preview()),
    ]
    for name, image in assets:
        save(image, name)
    make_contact_sheet(assets)


if __name__ == "__main__":
    main()
