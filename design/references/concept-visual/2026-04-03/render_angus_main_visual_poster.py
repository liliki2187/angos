from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path
from random import Random
from typing import Iterable

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
FONT_ROOT = ROOT.parents[2] / "skills" / "canvas-design" / "canvas-fonts"
OUTPUT = ROOT / "output" / "angus-main-visual-poster.png"
W, H = 1800, 2600
RNG = Random(7)


def rgba(hex_value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b = ImageColor.getrgb(hex_value)
    return r, g, b, alpha


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_ROOT / name), size)


FONTS = {
    "title": font("BigShoulders-Bold.ttf", 182),
    "subtitle": font("BigShoulders-Regular.ttf", 60),
    "serif": font("Gloock-Regular.ttf", 96),
    "serif_large": font("YoungSerif-Regular.ttf", 122),
    "section": font("CrimsonPro-Bold.ttf", 38),
    "body": font("InstrumentSans-Regular.ttf", 34),
    "body_small": font("InstrumentSans-Regular.ttf", 26),
    "mono": font("IBMPlexMono-Regular.ttf", 24),
    "mono_bold": font("IBMPlexMono-Bold.ttf", 24),
    "numbers": font("BigShoulders-Bold.ttf", 64),
}


PALETTE = {
    "bg_top": "#140f13",
    "bg_mid": "#23161c",
    "bg_bottom": "#120d11",
    "paper": "#efe4d2",
    "paper_dark": "#e4d5bf",
    "ink": "#1f1819",
    "soft_ink": "#554949",
    "gold": "#e2d1a8",
    "gold_soft": "#f7ecd2",
    "red": "#c95c52",
    "red_dark": "#8d3d3b",
    "teal": "#3d7f86",
    "teal_soft": "#86b4b7",
    "violet": "#7968aa",
    "olive": "#788364",
    "cream": "#fbf4e8",
}


def gradient_vertical(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    top_rgb = ImageColor.getrgb(top)
    bottom_rgb = ImageColor.getrgb(bottom)
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        color = tuple(int(top_rgb[i] * (1 - t) + bottom_rgb[i] * t) for i in range(3))
        draw.line((0, y, size[0], y), fill=color + (255,))
    return image


def add_noise(base: Image.Image, sigma: float, opacity: int) -> Image.Image:
    noise = Image.effect_noise(base.size, sigma).convert("L")
    colored = ImageOps.colorize(noise, black="#000000", white="#ffffff").convert("RGBA")
    colored.putalpha(opacity)
    return Image.alpha_composite(base, colored)


def draw_shadowed_rect(base: Image.Image, box: tuple[int, int, int, int], fill: tuple[int, int, int, int], radius: int = 10, shadow_alpha: int = 95, blur: int = 24, offset: tuple[int, int] = (0, 24)) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    ox, oy = offset
    draw.rounded_rectangle((x0 + ox, y0 + oy, x1 + ox, y1 + oy), radius=radius, fill=(0, 0, 0, shadow_alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def glow(base: Image.Image, center: tuple[int, int], radius: int, color: str, alpha: int, blur: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=rgba(color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textlength(candidate, font=font_obj) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_wrapped_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font_obj: ImageFont.FreeTypeFont, fill: tuple[int, int, int, int] | tuple[int, int, int], max_width: int, line_gap: int) -> int:
    x, y = xy
    lines = wrap_text(draw, text, font_obj, max_width)
    bbox = draw.textbbox((0, 0), "Ag", font=font_obj)
    line_h = bbox[3] - bbox[1]
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_h + line_gap
    return y


def draw_dashed_line(draw: ImageDraw.ImageDraw, points: Iterable[tuple[int, int]], fill: tuple[int, int, int, int], width: int = 3, dash: int = 14, gap: int = 10) -> None:
    pts = list(points)
    for a, b in zip(pts, pts[1:]):
        x0, y0 = a
        x1, y1 = b
        dist = max(abs(x1 - x0), abs(y1 - y0))
        if dist == 0:
            continue
        steps = max(1, dist // (dash + gap))
        for i in range(steps + 1):
            start_t = i / max(1, steps)
            end_t = min(start_t + dash / max(1, dist), 1)
            sx = int(x0 + (x1 - x0) * start_t)
            sy = int(y0 + (y1 - y0) * start_t)
            ex = int(x0 + (x1 - x0) * end_t)
            ey = int(y0 + (y1 - y0) * end_t)
            draw.line((sx, sy, ex, ey), fill=fill, width=width)


def make_paper(size: tuple[int, int], color: str) -> Image.Image:
    panel = Image.new("RGBA", size, rgba(color))
    panel = add_noise(panel, 10, 34)
    panel = add_noise(panel, 22, 14)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for _ in range(160):
        x = RNG.randint(0, size[0])
        y = RNG.randint(0, size[1])
        length = RNG.randint(20, 110)
        odraw.line((x, y, min(size[0], x + length), y + RNG.randint(-4, 4)), fill=(255, 255, 255, 10), width=1)
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.8))
    return Image.alpha_composite(panel, overlay)


def paste_rotated(base: Image.Image, image: Image.Image, xy: tuple[int, int], angle: float, shadow_alpha: int = 80) -> None:
    rotated = image.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    shadow = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    shadow.putalpha(rotated.split()[-1].point(lambda a: shadow_alpha if a else 0))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    sx = xy[0] + 18
    sy = xy[1] + 22
    base.alpha_composite(shadow, (sx, sy))
    base.alpha_composite(rotated, xy)


def ticket(box_size: tuple[int, int], title: str, value: str, accent: str) -> Image.Image:
    w, h = box_size
    img = make_paper((w, h), PALETTE["paper"])
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=6, outline=rgba("#d7c7b4"), width=2)
    draw.text((18, 16), title.upper(), font=FONTS["mono"], fill=rgba(accent))
    if draw.textlength(value, font=FONTS["section"]) <= w - 36:
        draw.text((18, 56), value, font=FONTS["section"], fill=rgba(PALETTE["ink"]))
    else:
        draw_wrapped_text(draw, (18, 54), value, FONTS["body_small"], rgba(PALETTE["ink"]), w - 36, 2)
    return img


def make_main_sheet() -> Image.Image:
    sheet = make_paper((1080, 1520), PALETTE["paper"])
    draw = ImageDraw.Draw(sheet)
    draw.rounded_rectangle((0, 0, 1079, 1519), radius=8, outline=rgba("#dac9b3"), width=3)

    draw.rounded_rectangle((42, 34, 1038, 196), radius=6, fill=rgba("#191417"), outline=rgba("#3a3134"), width=2)
    draw.text((76, 70), "ANGUS / WEEKLY MYSTERY GAZETTE", font=FONTS["subtitle"], fill=rgba(PALETTE["gold"]))
    draw.text((78, 140), "A SINGLE-PLAYER OCCULT NEWSPAPER MANAGEMENT GAME", font=FONTS["mono"], fill=rgba("#b7ab9c"))

    draw.text((78, 264), "INVESTIGATE", font=FONTS["serif_large"], fill=rgba(PALETTE["ink"]))
    draw.text((78, 376), "PUBLISH", font=FONTS["serif_large"], fill=rgba(PALETTE["ink"]))
    draw.text((78, 488), "DRIFT", font=FONTS["serif_large"], fill=rgba(PALETTE["red_dark"]))

    draw.line((80, 610, 1000, 610), fill=rgba("#ccbda9"), width=3)
    draw.text((82, 628), "7 DAYS . 6 SLOTS . ONE DANGEROUS EDITORIAL CYCLE", font=FONTS["mono_bold"], fill=rgba("#7e706a"))

    chart = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(chart)
    cx, cy = 712, 982
    for r in (118, 204, 292):
        cdraw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba("#615a61", 92), width=2)
    for i in range(7):
        angle = -pi / 2 + i * (2 * pi / 7)
        x0 = int(cx + cos(angle) * 228)
        y0 = int(cy + sin(angle) * 228)
        x1 = int(cx + cos(angle) * 318)
        y1 = int(cy + sin(angle) * 318)
        cdraw.line((x0, y0, x1, y1), fill=rgba("#766a72", 96), width=2)
    for angle_deg in (12, 58, 129, 205, 276, 332):
        angle = angle_deg * pi / 180
        x = int(cx + cos(angle) * 218)
        y = int(cy + sin(angle) * 218)
        cdraw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=rgba(PALETTE["gold"], 255))
        glow(chart, (x, y), 34, PALETTE["gold_soft"], 100, 18)
    draw_dashed_line(cdraw, [(388, 1120), (528, 980), (690, 920), (850, 852), (972, 760)], rgba(PALETTE["red"], 230), width=4)
    cdraw.ellipse((688, 958, 736, 1006), fill=rgba(PALETTE["red"]))
    cdraw.ellipse((962, 750, 990, 778), fill=rgba(PALETTE["red"]))
    cdraw.text((400, 756), "WEEK ARC", font=FONTS["section"], fill=rgba(PALETTE["ink"]))
    cdraw.text((400, 798), "briefing / exploration / editorial / summary", font=FONTS["body_small"], fill=rgba(PALETTE["soft_ink"]))
    cdraw.text((392, 1188), "Investigation only matters if it can become a front page.", font=FONTS["body_small"], fill=rgba(PALETTE["soft_ink"]))
    chart = chart.filter(ImageFilter.GaussianBlur(0.2))
    sheet.alpha_composite(chart)

    info_boxes = [
        ((82, 1260, 328, 1404), "DISPATCH", "staff 1-3"),
        ((360, 1260, 606, 1404), "PRESSURE", "truth / sensation"),
        ((638, 1260, 884, 1404), "SETTLEMENT", "profit / drift"),
    ]
    for box, title, value in info_boxes:
        draw.rounded_rectangle(box, radius=6, fill=rgba("#f4e8d6"), outline=rgba("#d4c2ab"), width=2)
        draw.text((box[0] + 18, box[1] + 14), title, font=FONTS["mono"], fill=rgba(PALETTE["red"]))
        draw.text((box[0] + 18, box[1] + 54), value, font=FONTS["section"], fill=rgba(PALETTE["ink"]))

    draw.text((82, 1420), "EDITORIAL DRIFT", font=FONTS["section"], fill=rgba(PALETTE["ink"]))
    draw.text((82, 1466), "Credibility, notoriety, prestige, order, frenzy", font=FONTS["body_small"], fill=rgba(PALETTE["soft_ink"]))
    stat_specs = [
        ("credibility", 76, PALETTE["teal"]),
        ("notoriety", 58, PALETTE["violet"]),
        ("prestige", 69, "#bf8759"),
        ("order", 47, PALETTE["olive"]),
        ("frenzy", 84, PALETTE["red"]),
    ]
    sy = 1528
    for label, value, color in stat_specs:
        draw.text((82, sy), label.upper(), font=FONTS["mono"], fill=rgba("#6b605c"))
        draw.rounded_rectangle((292, sy + 7, 558, sy + 28), radius=10, fill=rgba("#ddd0c0"))
        draw.rounded_rectangle((292, sy + 7, 292 + int(266 * value / 100), sy + 28), radius=10, fill=rgba(color))
        draw.text((580, sy - 1), f"{value:02d}", font=FONTS["mono_bold"], fill=rgba(color))
        sy += 58

    draw.text((664, 1420), "ISSUE SLOTS", font=FONTS["section"], fill=rgba(PALETTE["ink"]))
    draw.text((664, 1466), "Every placement drags next week with it.", font=FONTS["body_small"], fill=rgba(PALETTE["soft_ink"]))
    slot_y = 1528
    for i in range(6):
        x = 666 + i * 66
        draw.rounded_rectangle((x, slot_y, x + 52, slot_y + 92), radius=8, fill=rgba("#1b1718" if i in (0, 3, 5) else "#f3e8d8"), outline=rgba("#ccb9a3"), width=2)
        fill = PALETTE["cream"] if i in (0, 3, 5) else PALETTE["ink"]
        draw.text((x + 10, slot_y + 18), f"{i + 1:02d}", font=FONTS["numbers"], fill=rgba(fill))
    draw.text((666, 1644), "truth / sensation / profit", font=FONTS["mono"], fill=rgba(PALETTE["red_dark"]))

    return sheet


def build() -> None:
    base = gradient_vertical((W, H), PALETTE["bg_top"], PALETTE["bg_mid"])
    base = Image.alpha_composite(base, gradient_vertical((W, H), "#00000000", PALETTE["bg_bottom"]))
    base = add_noise(base, 12, 16)
    draw = ImageDraw.Draw(base)

    for y in range(80, H, 130):
        draw.line((0, y, W, y), fill=rgba("#ffffff", 10), width=1)
    for x in range(50, W, 120):
        draw.line((x, 0, x, H), fill=rgba("#ffffff", 6), width=1)

    glow(base, (900, 1120), 320, PALETTE["gold"], 45, 120)
    glow(base, (900, 1320), 420, PALETTE["cream"], 18, 150)
    glow(base, (330, 1820), 280, PALETTE["teal"], 24, 140)
    glow(base, (1490, 520), 260, PALETTE["red"], 22, 120)

    back_orbit = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(back_orbit)
    cx, cy = 910, 1380
    for radius in (360, 520, 690):
        odraw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=rgba("#85746b", 34), width=2)
    for i in range(7):
        angle = -pi / 2 + i * (2 * pi / 7)
        x0 = int(cx + cos(angle) * 420)
        y0 = int(cy + sin(angle) * 420)
        x1 = int(cx + cos(angle) * 690)
        y1 = int(cy + sin(angle) * 690)
        odraw.line((x0, y0, x1, y1), fill=rgba("#7b6b6b", 28), width=2)
    odraw.arc((cx - 780, cy - 780, cx + 780, cy + 780), start=216, end=334, fill=rgba(PALETTE["red"], 110), width=4)
    back_orbit = back_orbit.filter(ImageFilter.GaussianBlur(0.6))
    base.alpha_composite(back_orbit)

    title = "ANGUS"
    bbox = draw.textbbox((0, 0), title, font=FONTS["title"])
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 96), title, font=FONTS["title"], fill=rgba(PALETTE["gold_soft"]))
    sub = "WEEKLY MYSTERY GAZETTE"
    sbbox = draw.textbbox((0, 0), sub, font=FONTS["subtitle"])
    sw = sbbox[2] - sbbox[0]
    draw.text(((W - sw) / 2, 272), sub, font=FONTS["subtitle"], fill=rgba(PALETTE["gold"], 220))
    micro = "THE PAPER THAT TURNS INVESTIGATION INTO PUBLIC REALITY"
    mbbox = draw.textbbox((0, 0), micro, font=FONTS["mono"])
    mw = mbbox[2] - mbbox[0]
    draw.text(((W - mw) / 2, 348), micro, font=FONTS["mono"], fill=rgba("#aa9d8e"))

    main_sheet = make_main_sheet()
    paste_rotated(base, main_sheet, (364, 520), -3.8, shadow_alpha=92)

    left_ticket = ticket((328, 152), "WEEK", "7 DAYS / LIMITED DISPATCH", PALETTE["red"])
    right_ticket = ticket((318, 152), "NODE LOGIC", "REGIONS / HIDDEN SIGNALS", PALETTE["teal"])
    lower_ticket = ticket((272, 138), "TENSION", "TRUTH / SENSATION / PROFIT", PALETTE["violet"])

    paste_rotated(base, left_ticket, (118, 898), -8.5, 72)
    paste_rotated(base, right_ticket, (1276, 944), 7.2, 72)
    paste_rotated(base, lower_ticket, (1222, 1878), 5.0, 72)

    thread = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(thread)
    draw_dashed_line(tdraw, [(270, 1052), (516, 980), (724, 1168)], rgba(PALETTE["red"], 210), width=4)
    draw_dashed_line(tdraw, [(1452, 1030), (1312, 1164), (1156, 1288)], rgba(PALETTE["red"], 210), width=4)
    draw_dashed_line(tdraw, [(1338, 1962), (1222, 1812), (1066, 1698)], rgba(PALETTE["red"], 210), width=4)
    for point in [(270, 1052), (724, 1168), (1452, 1030), (1156, 1288), (1338, 1962), (1066, 1698)]:
        x, y = point
        tdraw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=rgba(PALETTE["red"]))
    thread = thread.filter(ImageFilter.GaussianBlur(0.4))
    base.alpha_composite(thread)

    for x, y, r, color, alpha, blur in [
        (524, 974, 66, PALETTE["gold_soft"], 95, 26),
        (1288, 1240, 86, PALETTE["gold_soft"], 82, 32),
        (1110, 1810, 72, PALETTE["teal_soft"], 52, 26),
        (1362, 1660, 58, PALETTE["red"], 42, 22),
    ]:
        glow(base, (x, y), r, color, alpha, blur)

    verbs = "briefing      exploration      editorial      summary"
    vbbox = draw.textbbox((0, 0), verbs, font=FONTS["mono"])
    draw.text(((W - (vbbox[2] - vbbox[0])) / 2, 2360), verbs, font=FONTS["mono"], fill=rgba("#ae9f90"))
    draw.line((330, 2418, 1470, 2418), fill=rgba("#5c4f52"), width=2)
    footer = "INVESTIGATE THE UNKNOWN . PUBLISH THE ISSUE . LIVE WITH THE DRIFT"
    fbbox = draw.textbbox((0, 0), footer, font=FONTS["mono_bold"])
    draw.text(((W - (fbbox[2] - fbbox[0])) / 2, 2450), footer, font=FONTS["mono_bold"], fill=rgba(PALETTE["gold"], 220))

    specks = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(specks)
    for _ in range(140):
        x = RNG.randint(0, W)
        y = RNG.randint(0, H)
        r = RNG.randint(1, 3)
        sdraw.ellipse((x - r, y - r, x + r, y + r), fill=rgba("#ffffff", RNG.randint(18, 60)))
    specks = specks.filter(ImageFilter.GaussianBlur(0.4))
    base.alpha_composite(specks)

    base = base.filter(ImageFilter.UnsharpMask(radius=1.6, percent=135, threshold=3))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUTPUT, quality=95)


if __name__ == "__main__":
    build()
