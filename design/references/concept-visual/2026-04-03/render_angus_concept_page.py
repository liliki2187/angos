from __future__ import annotations

from pathlib import Path
from random import Random
from typing import Iterable

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "angus-concept-visual-page.png"
FONT_ROOT = ROOT.parents[2] / "skills" / "canvas-design" / "canvas-fonts"
W, H = 1800, 2400
RNG = Random(31)


def rgba(hex_value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b = ImageColor.getrgb(hex_value)
    return r, g, b, alpha


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_ROOT / name), size)


FONTS = {
    "masthead": font("BigShoulders-Bold.ttf", 48),
    "meta_label": font("IBMPlexMono-Regular.ttf", 23),
    "meta_value": font("BigShoulders-Regular.ttf", 48),
    "title": font("YoungSerif-Regular.ttf", 84),
    "hero_title": font("Gloock-Regular.ttf", 70),
    "section_title": font("CrimsonPro-Bold.ttf", 42),
    "body": font("InstrumentSans-Regular.ttf", 31),
    "body_small": font("InstrumentSans-Regular.ttf", 24),
    "body_bold": font("InstrumentSans-Bold.ttf", 26),
    "mono": font("IBMPlexMono-Regular.ttf", 22),
    "mono_bold": font("IBMPlexMono-Bold.ttf", 24),
    "numeric": font("BigShoulders-Bold.ttf", 76),
    "vertical": font("IBMPlexMono-Regular.ttf", 30),
}


PALETTE = {
    "bg_top": "#151114",
    "bg_bottom": "#2c1e22",
    "paper": "#efe5d3",
    "paper_shadow": "#0f0a0d",
    "paper_line": "#d9ccb9",
    "ink": "#1d1718",
    "ink_soft": "#423535",
    "hero": "#201c28",
    "hero_2": "#2f2c3b",
    "burgundy": "#9d3a3a",
    "red": "#c95a4f",
    "gold": "#d5c08c",
    "gold_soft": "#f4e7c8",
    "teal": "#3a7f88",
    "teal_soft": "#88b9b0",
    "olive": "#768168",
    "violet": "#8570b8",
    "orange": "#bf8558",
    "green": "#86b67a",
    "cream_text": "#f8f1e4",
}


def gradient_background(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
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


def draw_shadowed_round_rect(
    base: Image.Image,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
    radius: int = 10,
    shadow_alpha: int = 90,
    offset: tuple[int, int] = (0, 24),
    blur: int = 26,
) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    x0, y0, x1, y1 = box
    ox, oy = offset
    sdraw.rounded_rectangle((x0 + ox, y0 + oy, x1 + ox, y1 + oy), radius=radius, fill=(0, 0, 0, shadow_alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=fill)


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


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int] | tuple[int, int, int],
    max_width: int,
    line_gap: int,
) -> int:
    x, y = xy
    lines = wrap_text(draw, text, font_obj, max_width)
    bbox = draw.textbbox((0, 0), "Ag", font=font_obj)
    height = bbox[3] - bbox[1]
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += height + line_gap
    return y


def glow_circle(base: Image.Image, center: tuple[int, int], radius: int, color: str, alpha: int, blur: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=rgba(color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def draw_cross(base: Image.Image, center: tuple[int, int], size: int, color: tuple[int, int, int, int], width: int = 2) -> None:
    draw = ImageDraw.Draw(base)
    x, y = center
    draw.line((x - size, y, x + size, y), fill=color, width=width)
    draw.line((x, y - size, x, y + size), fill=color, width=width)


def draw_dotted_line(draw: ImageDraw.ImageDraw, points: Iterable[tuple[int, int]], color: tuple[int, int, int, int], width: int = 2) -> None:
    pts = list(points)
    for a, b in zip(pts, pts[1:]):
        x0, y0 = a
        x1, y1 = b
        steps = max(abs(x1 - x0), abs(y1 - y0)) // 14
        steps = max(steps, 1)
        for i in range(steps):
            if i % 2 == 0:
                t0 = i / steps
                t1 = min((i + 1) / steps, 1)
                p0 = (int(x0 + (x1 - x0) * t0), int(y0 + (y1 - y0) * t0))
                p1 = (int(x0 + (x1 - x0) * t1), int(y0 + (y1 - y0) * t1))
                draw.line((p0, p1), fill=color, width=width)


def make_paper_panel(width: int, height: int, color: str) -> Image.Image:
    panel = Image.new("RGBA", (width, height), rgba(color))
    panel = add_noise(panel, sigma=9.0, opacity=36)
    panel = add_noise(panel, sigma=24.0, opacity=15)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for _ in range(120):
        x0 = RNG.randint(0, width)
        y0 = RNG.randint(0, height)
        length = RNG.randint(20, 120)
        odraw.line((x0, y0, min(width, x0 + length), y0 + RNG.randint(-3, 3)), fill=(255, 255, 255, 12), width=1)
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(panel, overlay)


def paste_with_shadow(base: Image.Image, panel: Image.Image, xy: tuple[int, int], blur: int = 14, alpha: int = 70) -> None:
    x, y = xy
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow.paste(panel.split()[-1].point(lambda _: alpha), (x + 10, y + 10))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)
    base.alpha_composite(panel, xy)


def draw_meta_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, value: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=8, outline=rgba("#53494b", 255), fill=rgba("#1b171a", 255), width=2)
    draw.text((x0 + 22, y0 + 18), label.upper(), font=FONTS["meta_label"], fill=rgba("#b7ac9c"))
    draw.text((x0 + 22, y0 + 58), value, font=FONTS["meta_value"], fill=rgba("#f4ead6"))


def story_card(base: Image.Image, box: tuple[int, int, int, int], tag: str, title: str, text: str, accent: str) -> None:
    draw_shadowed_round_rect(base, box, rgba("#f0e4d0"), radius=6, shadow_alpha=38, offset=(0, 10), blur=12)
    draw = ImageDraw.Draw(base)
    x0, y0, x1, y1 = box
    thumb = (x0 + 18, y0 + 18, x0 + 120, y0 + 120)
    draw.rounded_rectangle(thumb, radius=4, fill=rgba("#4b5b67"))
    glow_circle(base, ((thumb[0] + thumb[2]) // 2 + 8, (thumb[1] + thumb[3]) // 2 - 2), 22, "#c8d7df", 120, 12)
    draw.rectangle((thumb[0] + 12, thumb[1] + 86, thumb[2] - 12, thumb[1] + 90), fill=rgba(accent, 255))
    draw.text((x0 + 145, y0 + 16), tag.upper(), font=FONTS["mono"], fill=rgba(accent))
    draw.text((x0 + 145, y0 + 50), title, font=FONTS["section_title"], fill=rgba(PALETTE["ink"]))
    draw_wrapped_text(draw, (x0 + 145, y0 + 98), text, FONTS["body_small"], rgba("#554747"), max_width=x1 - x0 - 170, line_gap=4)


def memo_card(base: Image.Image, box: tuple[int, int, int, int], label: str, title: str, text: str, accent: str) -> None:
    draw_shadowed_round_rect(base, box, rgba("#f3e8d8"), radius=6, shadow_alpha=34, offset=(0, 8), blur=10)
    draw = ImageDraw.Draw(base)
    x0, y0, x1, y1 = box
    draw.line((x0 + 24, y0 + 56, x1 - 24, y0 + 56), fill=rgba("#d8c7b5"), width=2)
    draw.text((x0 + 24, y0 + 18), label.upper(), font=FONTS["mono"], fill=rgba(accent))
    draw.text((x0 + 24, y0 + 70), title, font=FONTS["section_title"], fill=rgba(PALETTE["ink"]))
    draw_wrapped_text(draw, (x0 + 24, y0 + 122), text, FONTS["body"], rgba("#4d4140"), max_width=x1 - x0 - 48, line_gap=6)


def draw_stat_bar(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str, value: int, color: str) -> None:
    x, y = xy
    draw.text((x, y), label.upper(), font=FONTS["mono"], fill=rgba("#6c5f5c"))
    bar_x = x + 190
    draw.rounded_rectangle((bar_x, y + 7, bar_x + 260, y + 26), radius=9, fill=rgba("#d8cabb"))
    width = int(260 * max(0.15, min(1.0, value / 100)))
    draw.rounded_rectangle((bar_x, y + 7, bar_x + width, y + 26), radius=9, fill=rgba(color))
    draw.text((bar_x + 284, y - 2), f"{value:02d}", font=FONTS["mono_bold"], fill=rgba(color))


def vertical_label(text: str, font_obj: ImageFont.FreeTypeFont, fill: str, padding: int = 20) -> Image.Image:
    temp = Image.new("RGBA", (1000, 120), (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp)
    draw.text((padding, 18), text, font=font_obj, fill=rgba(fill))
    bbox = temp.getbbox()
    cropped = temp.crop(bbox)
    return cropped.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)


def build() -> None:
    base = gradient_background((W, H), PALETTE["bg_top"], PALETTE["bg_bottom"])
    base = add_noise(base, sigma=12, opacity=18)
    draw = ImageDraw.Draw(base)

    for y in range(180, H, 180):
        draw.line((0, y, W, y), fill=rgba("#ffffff", 10), width=1)
    for x in range(80, W, 120):
        draw.line((x, 0, x, H), fill=rgba("#ffffff", 7), width=1)

    thread_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(thread_layer)
    thread_sets = [
        [(40, 260), (520, 120), (1130, 430), (1680, 70)],
        [(1350, 0), (1100, 410), (965, 790), (1210, 1220), (1730, 1640)],
        [(120, 2130), (540, 1770), (930, 1510), (1370, 1460), (1760, 1240)],
    ]
    for points in thread_sets:
        draw_dotted_line(tdraw, points, rgba(PALETTE["burgundy"], 130), width=3)
    thread_layer = thread_layer.filter(ImageFilter.GaussianBlur(0.8))
    base.alpha_composite(thread_layer)

    glow_circle(base, (1560, 280), 180, "#7d1f2f", 55, 90)
    glow_circle(base, (280, 2060), 220, "#3e6270", 30, 110)

    paper = make_paper_panel(1560, 2180, PALETTE["paper"])
    paper_draw = ImageDraw.Draw(paper)
    paper_draw.rectangle((0, 0, 1559, 2179), outline=rgba(PALETTE["paper_line"]), width=3)

    header_box = (50, 48, 1510, 320)
    paper_draw.rounded_rectangle(header_box, radius=8, fill=rgba("#191519"), outline=rgba("#3a2e30"), width=2)
    paper_draw.text((88, 82), "ANGUS / WEEKLY MYSTERY GAZETTE", font=FONTS["masthead"], fill=rgba("#c7b893"))
    paper_draw.text((88, 138), "CONCEPT VISUAL / ISSUE 00 / ARCHIVE PROOF", font=FONTS["mono"], fill=rgba("#9e9387"))
    paper_draw.text((88, 180), "THE PAPER THAT", font=FONTS["title"], fill=rgba(PALETTE["gold_soft"]))
    paper_draw.text((88, 252), "HUNTS THE UNPROVEN", font=FONTS["title"], fill=rgba(PALETTE["gold_soft"]))

    meta_boxes = [
        (970, 86, 1135, 216, "Loop", "Week Arc"),
        (1155, 86, 1320, 216, "Bias", "Truth"),
        (1340, 86, 1505, 216, "Threat", "Occult"),
    ]
    for box in meta_boxes:
        draw_meta_box(paper_draw, box[:4], box[4], box[5])

    hero = Image.new("RGBA", (736, 980), rgba(PALETTE["hero"]))
    hero = Image.alpha_composite(hero, gradient_background(hero.size, PALETTE["hero"], PALETTE["hero_2"]))
    hero = add_noise(hero, sigma=8.0, opacity=18)
    hdraw = ImageDraw.Draw(hero)
    hdraw.rectangle((0, 0, 735, 979), outline=rgba("#4e4551"), width=2)
    hdraw.text((40, 38), "SIGNAL BOARD", font=FONTS["mono_bold"], fill=rgba("#e0d4c0"))

    ring_center = (366, 330)
    for radius in (120, 214, 308):
        hdraw.ellipse((ring_center[0] - radius, ring_center[1] - radius, ring_center[0] + radius, ring_center[1] + radius), outline=rgba("#766d7a", 85), width=2)
    for angle, node in zip(
        (10, 64, 123, 190, 255, 310),
        ((583, 367), (492, 556), (252, 586), (98, 365), (191, 149), (491, 112)),
    ):
        x, y = node
        glow_circle(hero, node, 22, "#f6e8bf", 160, 14)
        hdraw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=rgba("#fbe9b5"))
        draw_cross(hero, node, 16, rgba("#f4ddaa", 120))

    draw_dotted_line(hdraw, [(82, 649), (201, 540), (306, 390), (518, 304), (655, 206)], rgba("#d06659", 220), width=4)
    hdraw.line((140, 750, 644, 750), fill=rgba("#897e79", 80), width=2)
    hdraw.text((40, 676), "A WEEK BEGINS", font=FONTS["hero_title"], fill=rgba("#f7ead2"))
    hdraw.text((40, 742), "WITH A SIGNAL", font=FONTS["hero_title"], fill=rgba("#f7ead2"))
    draw_wrapped_text(hdraw, (44, 842), "Dispatch staff into rumor, ritual, debris, and static. Every recovered clue changes what the page can become.", FONTS["body"], rgba("#c9bbb2"), 640, 6)
    glow_circle(hero, (600, 90), 72, "#f5e5bc", 120, 30)
    glow_circle(hero, (120, 820), 58, "#4a8690", 45, 24)

    paper.alpha_composite(hero, (50, 364))

    diagram_layer = Image.new("RGBA", paper.size, (0, 0, 0, 0))
    ddraw = ImageDraw.Draw(diagram_layer)
    for radius in (170, 270, 360):
        ddraw.arc((850 - radius, 730 - radius, 850 + radius, 730 + radius), start=250, end=70, fill=rgba("#d9c8b3", 80), width=3)
    ddraw.line((888, 470, 1274, 612), fill=rgba("#c65f54", 190), width=4)
    ddraw.line((1280, 612, 1340, 776), fill=rgba("#c65f54", 150), width=3)
    ddraw.ellipse((1264, 596, 1296, 628), fill=rgba("#c65f54"))
    ddraw.ellipse((1328, 764, 1352, 788), fill=rgba("#c65f54"))
    ddraw.rectangle((880, 636, 1460, 651), fill=rgba("#e8dac6", 160))
    diagram_layer = diagram_layer.filter(ImageFilter.GaussianBlur(0.4))
    paper.alpha_composite(diagram_layer)

    memo_card(
        paper,
        (878, 400, 1460, 670),
        "Dispatch",
        "Field work exists to feed print.",
        "Investigation is not a side activity. The expedition, the clue, and the cover line are one continuous editorial instrument.",
        PALETTE["red"],
    )
    memo_card(
        paper,
        (878, 700, 1460, 970),
        "Layout",
        "Truth and spectacle refuse to align.",
        "The page must feel elegant and compromised at once: every placement pulls credibility, obsession, and profit in different directions.",
        PALETTE["violet"],
    )
    memo_card(
        paper,
        (878, 1000, 1460, 1270),
        "Settlement",
        "One issue is one readable wound.",
        "A finished week should leave behind money, drift, reputation, and a sharper appetite for the next impossible headline.",
        PALETTE["teal"],
    )

    story_card(
        paper,
        (50, 1396, 760, 1606),
        "Field Note 01",
        "Nightsignal in the wire room",
        "A relay station returns a voice nobody recorded, yet the print room keeps setting type for it.",
        PALETTE["teal"],
    )
    story_card(
        paper,
        (50, 1630, 760, 1840),
        "Field Note 02",
        "Salt map under the floorboards",
        "Editorial geometry mirrors an excavation grid; every measured square implies a buried paragraph.",
        PALETTE["orange"],
    )
    story_card(
        paper,
        (50, 1864, 760, 2074),
        "Field Note 03",
        "Issue six remembers the missing",
        "A perfect six-slot paper behaves like a ritual circle: stable from afar, slightly unstable the closer you read.",
        PALETTE["burgundy"],
    )

    paper_draw.text((878, 1396), "EDITORIAL PRESSURE", font=FONTS["section_title"], fill=rgba(PALETTE["ink"]))
    paper_draw.text((878, 1450), "Macro drift should feel measurable, but never safe.", font=FONTS["body_small"], fill=rgba("#5b4b4a"))
    stat_y = 1516
    stats = [
        ("credibility", 74, PALETTE["teal"]),
        ("notoriety", 58, PALETTE["violet"]),
        ("prestige", 67, PALETTE["orange"]),
        ("order", 49, PALETTE["olive"]),
        ("frenzy", 83, PALETTE["red"]),
    ]
    for label, value, color in stats:
        draw_stat_bar(paper_draw, (878, stat_y), label, value, color)
        stat_y += 72

    paper_draw.text((878, 1906), "ISSUE GRID", font=FONTS["section_title"], fill=rgba(PALETTE["ink"]))
    paper_draw.text((878, 1958), "Six placements. Six exposures. One identity drifting into next week.", font=FONTS["body_small"], fill=rgba("#5b4b4a"))

    slot_y = 2036
    for i in range(6):
        x = 878 + i * 94
        fill = "#1c1718" if i in (0, 2, 4) else "#efe3d3"
        text_fill = "#f6ead4" if i in (0, 2, 4) else "#1c1718"
        paper_draw.rounded_rectangle((x, slot_y, x + 76, slot_y + 76), radius=8, fill=rgba(fill), outline=rgba("#c9baa7"), width=2)
        value = f"{i + 1:02d}"
        bbox = paper_draw.textbbox((0, 0), value, font=FONTS["numeric"])
        tx = x + (76 - (bbox[2] - bbox[0])) / 2
        ty = slot_y + (76 - (bbox[3] - bbox[1])) / 2 - 6
        paper_draw.text((tx, ty), value, font=FONTS["numeric"], fill=rgba(text_fill))

    paper_draw.line((1230, 2030, 1498, 2126), fill=rgba("#d36457"), width=6)
    paper_draw.ellipse((1216, 2018, 1244, 2046), fill=rgba("#d36457"))
    paper_draw.ellipse((1484, 2112, 1512, 2140), fill=rgba("#d36457"))
    paper_draw.text((1188, 2142), "truth / spectacle / profit", font=FONTS["mono"], fill=rgba("#8e5f57"))

    side_label = vertical_label("ANGUS CONCEPT PAGE / ARCHIVE PROOF / APRIL 2026", FONTS["vertical"], "#7d716c")
    paper.alpha_composite(side_label, (1488, 660))

    for x, y, r, color, blur in [
        (1420, 1560, 58, "#f2e2b7", 28),
        (1100, 1820, 42, "#4c8994", 18),
        (620, 1500, 38, "#d4b36d", 18),
    ]:
        glow_circle(paper, (x, y), r, color, 110, blur)

    for _ in range(55):
        px = RNG.randint(90, 1460)
        py = RNG.randint(360, 2100)
        if RNG.random() < 0.45:
            paper_draw.ellipse((px, py, px + 3, py + 3), fill=rgba("#ffffff", RNG.randint(24, 70)))

    paper = paper.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))
    paste_with_shadow(base, paper, (120, 110))

    final = base.convert("RGB")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    final.save(OUTPUT, quality=95)


if __name__ == "__main__":
    build()
