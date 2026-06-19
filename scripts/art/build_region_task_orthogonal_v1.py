from __future__ import annotations

"""Deprecated whitebox generator for early layout tests.

Do not write its simplified map/paper assets into the production assetized
folder. The approved region-task-board direction keeps the original deep-blue
low-poly paper map style and only separates runtime UI pieces from it.
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tmp/whitebox/region_task_orthogonal_v1"
CONTACT = ROOT / "docs/screenshots/2026-06-15-region-task-board-orthogonal-v1/whitebox-contact-sheet.png"

CANVAS = (1920, 1080)
MAP_SIZE = (960, 742)
DETAIL_SIZE = (386, 840)


def paste_alpha(dst: Image.Image, src: Image.Image, xy: tuple[int, int]) -> None:
    dst.alpha_composite(src.convert("RGBA"), xy)


def noise_overlay(size: tuple[int, int], alpha: int = 22) -> Image.Image:
    noise = Image.effect_noise(size, 28).convert("L")
    overlay = Image.new("RGBA", size, (255, 255, 255, 0))
    overlay.putalpha(noise.point(lambda v: int(abs(v - 128) / 128 * alpha)))
    return overlay


def paper_texture(size: tuple[int, int], tint: tuple[int, int, int] = (241, 232, 209)) -> Image.Image:
    paper = Image.new("RGBA", size, (*tint, 255))
    paper = Image.alpha_composite(paper, noise_overlay(size, 18))
    draw = ImageDraw.Draw(paper)
    for y in range(18, size[1], 38):
        draw.line((18, y, size[0] - 18, y), fill=(55, 58, 50, 26), width=1)
    return paper


def draw_halftone(draw: ImageDraw.ImageDraw, origin: tuple[int, int], cols: int, rows: int, color: tuple[int, int, int, int]) -> None:
    ox, oy = origin
    for y in range(rows):
        for x in range(cols):
            if (x + y) % 2 == 0:
                draw.rectangle((ox + x * 5, oy + y * 5, ox + x * 5 + 2, oy + y * 5 + 2), fill=color)


def draw_crop_marks(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
    x, y, w, h = rect
    marks = [
        (x, y, 22, 0), (x, y, 0, 22),
        (x + w, y, -22, 0), (x + w, y, 0, 22),
        (x, y + h, 22, 0), (x, y + h, 0, -22),
        (x + w, y + h, -22, 0), (x + w, y + h, 0, -22),
    ]
    for mx, my, dx, dy in marks:
        draw.line((mx, my, mx + dx, my + dy), fill=color, width=2)


def draw_paper_panel(
    base: Image.Image,
    xy: tuple[int, int],
    size: tuple[int, int],
    accent: tuple[int, int, int] = (213, 49, 35),
) -> None:
    panel = paper_texture(size)
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rectangle((7, 7, size[0] - 1, size[1] - 1), fill=(0, 0, 0, 60))
    paste_alpha(base, shadow, (xy[0] + 8, xy[1] + 8))
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline=(33, 44, 44, 160), width=2)
    draw.rectangle((14, 14, size[0] - 15, size[1] - 15), outline=(33, 44, 44, 105), width=1)
    draw_halftone(draw, (size[0] - 94, 34), 13, 8, (*accent, 70))
    draw_crop_marks(draw, (18, 18, size[0] - 36, size[1] - 36), (*accent, 150))
    paste_alpha(base, panel, xy)


def make_board_shell() -> Image.Image:
    shell = Image.new("RGBA", CANVAS, (4, 13, 24, 255))
    shell = Image.alpha_composite(shell, noise_overlay(CANVAS, 16))
    draw = ImageDraw.Draw(shell)

    for x in range(0, CANVAS[0], 48):
        draw.line((x, 0, x, CANVAS[1]), fill=(37, 76, 92, 34), width=1)
    for y in range(0, CANVAS[1], 48):
        draw.line((0, y, CANVAS[0], y), fill=(37, 76, 92, 34), width=1)

    draw.rectangle((16, 18, 1904, 1064), outline=(142, 118, 73, 115), width=2)
    draw.rectangle((48, 118, 468, 972), outline=(25, 132, 143, 85), width=2)
    draw_paper_panel(shell, (52, 128), (410, 840), (213, 49, 35))
    draw.rectangle((492, 126, 1452, 868), fill=(3, 12, 22, 210), outline=(132, 118, 83, 135), width=2)
    draw.rectangle((506, 140, 1438, 854), outline=(23, 117, 133, 70), width=1)
    draw_paper_panel(shell, (1482, 128), DETAIL_SIZE, (213, 49, 35))

    draw.line((82, 224, 430, 224), fill=(213, 49, 35, 82), width=2)
    draw_halftone(draw, (1648, 42), 42, 4, (32, 180, 190, 92))
    draw_halftone(draw, (1290, 34), 34, 5, (214, 44, 29, 82))
    return shell.convert("RGB")


def make_clean_map() -> Image.Image:
    img = Image.new("RGBA", MAP_SIZE, (4, 14, 27, 255))
    img = Image.alpha_composite(img, noise_overlay(MAP_SIZE, 18))
    draw = ImageDraw.Draw(img)
    for x in range(0, MAP_SIZE[0], 40):
        draw.line((x, 0, x, MAP_SIZE[1]), fill=(38, 87, 104, 46), width=1)
    for y in range(0, MAP_SIZE[1], 40):
        draw.line((0, y, MAP_SIZE[0], y), fill=(38, 87, 104, 46), width=1)

    land = [
        [(78, 164), (172, 76), (344, 52), (520, 94), (650, 188), (752, 286), (708, 394), (560, 426), (476, 520), (354, 622), (210, 582), (158, 452), (70, 332)],
        [(610, 72), (734, 40), (902, 90), (944, 184), (862, 226), (738, 198), (638, 146)],
        [(352, 540), (430, 612), (400, 718), (304, 694), (272, 610)],
        [(702, 406), (856, 410), (922, 500), (862, 612), (716, 594), (642, 498)],
    ]
    tones = [(37, 86, 126, 218), (28, 75, 110, 205), (45, 98, 138, 212), (31, 83, 122, 205)]
    for poly, tone in zip(land, tones):
        draw.polygon(poly, fill=tone, outline=(76, 132, 162, 130))

    triangles = [
        (88, 164, 172, 76, 270, 206), (172, 76, 344, 52, 270, 206),
        (270, 206, 344, 52, 520, 94), (270, 206, 520, 94, 432, 296),
        (432, 296, 520, 94, 650, 188), (432, 296, 650, 188, 560, 426),
        (158, 452, 270, 206, 432, 296), (158, 452, 432, 296, 354, 622),
        (560, 426, 708, 394, 642, 498), (642, 498, 862, 612, 716, 594),
    ]
    for tri in triangles:
        draw.line(tri + (tri[0], tri[1]), fill=(114, 157, 181, 62), width=2)

    for cx, cy, rx, ry, color in [
        (270, 360, 146, 90, (36, 194, 205, 95)),
        (610, 428, 182, 108, (36, 194, 205, 75)),
        (772, 558, 124, 74, (214, 45, 31, 65)),
    ]:
        for i in range(0, 360, 16):
            if i % 32 == 0:
                continue
            draw.arc((cx - rx, cy - ry, cx + rx, cy + ry), i, i + 8, fill=color, width=2)

    draw_halftone(draw, (80, 250), 18, 16, (31, 187, 199, 118))
    draw_halftone(draw, (760, 80), 24, 18, (31, 187, 199, 104))
    draw_halftone(draw, (742, 562), 24, 18, (214, 45, 31, 105))
    draw.rectangle((0, 0, MAP_SIZE[0] - 1, MAP_SIZE[1] - 1), outline=(126, 116, 82, 145), width=2)
    draw_crop_marks(draw, (22, 22, MAP_SIZE[0] - 44, MAP_SIZE[1] - 44), (224, 212, 166, 150))
    return img.convert("RGB")


def make_route_layer() -> Image.Image:
    layer = Image.new("RGBA", MAP_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    nodes = [(150, 540), (300, 420), (440, 478), (560, 342), (420, 218), (650, 208), (720, 440), (820, 520)]
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (2, 6)]:
        draw.line((nodes[a], nodes[b]), fill=(220, 52, 35, 165), width=4)
        draw.line((nodes[a], nodes[b]), fill=(250, 151, 95, 95), width=1)
    for x, y in nodes:
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(220, 52, 35, 205), outline=(252, 184, 124, 150), width=1)
    return layer.filter(ImageFilter.GaussianBlur(0.25))


def draw_pin_frame(frame: Image.Image, tone: str, selected: bool = False, disabled: bool = False) -> None:
    draw = ImageDraw.Draw(frame)
    colors = {
        "red": ((232, 70, 45, 255), (96, 20, 18, 255)),
        "cyan": ((62, 194, 195, 255), (13, 81, 89, 255)),
        "gold": ((246, 181, 74, 255), (118, 67, 20, 255)),
        "gray": ((126, 127, 118, 220), (46, 50, 48, 220)),
    }
    fill, edge = colors["gray"] if disabled else colors[tone]
    cx, cy = 32, 21
    radius = 15 if selected else 13
    draw.line((cx, cy + 13, cx, 58), fill=(14, 18, 19, 185), width=5)
    draw.polygon([(cx - 8, cy + 31), (cx + 8, cy + 31), (cx, 58)], fill=edge)
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=edge)
    draw.ellipse((cx - radius + 3, cy - radius + 3, cx + radius - 3, cy + radius - 3), fill=fill)
    draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=(255, 232, 190, 120))
    if selected:
        draw.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=(255, 214, 104, 180), width=3)


def make_pin_atlas() -> Image.Image:
    atlas = Image.new("RGBA", (384, 64), (0, 0, 0, 0))
    specs = [("red", False, False), ("red", True, False), ("gold", True, False), ("gray", False, True), ("cyan", True, False), ("red", True, False)]
    for i, spec in enumerate(specs):
        frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw_pin_frame(frame, spec[0], spec[1], spec[2])
        paste_alpha(atlas, frame, (i * 64, 0))
    return atlas


def make_pin_label_atlas() -> Image.Image:
    atlas = Image.new("RGBA", (600, 72), (0, 0, 0, 0))
    states = [((13, 85, 91, 210), (0, 0, 0, 0)), ((194, 92, 28, 230), (255, 212, 98, 36)), ((80, 82, 72, 160), (0, 0, 0, 0))]
    for i, (edge, fill_overlay) in enumerate(states):
        frame = paper_texture((200, 72))
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle((5, 8, 190, 60), radius=3, outline=edge, width=2, fill=fill_overlay)
        draw.line((20, 47, 145, 47), fill=(21, 31, 32, 80), width=1)
        draw_halftone(draw, (154, 42), 7, 4, (16, 24, 25, 95))
        paste_alpha(atlas, frame, (i * 200, 0))
    return atlas


def make_task_card_atlas() -> Image.Image:
    atlas = Image.new("RGBA", (384, 720), (0, 0, 0, 0))
    accents = [(218, 45, 31, 235), (30, 169, 176, 235), (230, 160, 55, 245), (118, 118, 104, 205), (34, 140, 146, 235), (218, 45, 31, 245)]
    overlays = [(0, 0, 0, 0), (255, 255, 255, 22), (255, 210, 80, 34), (54, 55, 48, 70), (31, 120, 130, 32), (205, 40, 24, 26)]
    for i in range(6):
        frame = paper_texture((384, 120))
        draw = ImageDraw.Draw(frame)
        draw.rectangle((0, 0, 56, 120), fill=accents[i])
        draw.rectangle((10, 16, 24, 30), fill=(245, 238, 213, 230))
        draw.rectangle((10, 44, 24, 58), fill=(245, 238, 213, 230))
        draw.rectangle((332, 0, 365, 44), fill=accents[i])
        draw.polygon((332, 44, 348, 34, 365, 44), fill=(245, 238, 213, 230))
        draw.line((72, 23, 302, 23), fill=accents[i], width=2)
        draw.line((72, 53, 322, 53), fill=(31, 36, 34, 130), width=1)
        draw.line((72, 76, 300, 76), fill=(31, 36, 34, 95), width=1)
        draw_halftone(draw, (292, 78), 12, 6, (23, 30, 29, 84))
        frame = Image.alpha_composite(frame, Image.new("RGBA", frame.size, overlays[i]))
        paste_alpha(atlas, frame, (0, i * 120))
    return atlas


def make_filter_tab_atlas() -> Image.Image:
    atlas = Image.new("RGBA", (480, 48), (0, 0, 0, 0))
    states = [((242, 232, 208, 220), (27, 42, 45, 130)), ((246, 238, 215, 245), (30, 169, 176, 210)), ((249, 238, 206, 255), (205, 70, 34, 230)), ((116, 118, 108, 165), (49, 52, 47, 150))]
    for i, (fill, edge) in enumerate(states):
        frame = Image.new("RGBA", (120, 48), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle((4, 6, 116, 42), radius=3, fill=fill, outline=edge, width=2)
        draw.line((18, 30, 98, 30), fill=(31, 36, 34, 80), width=1)
        paste_alpha(atlas, frame, (i * 120, 0))
    return atlas


def make_detail_sheet() -> Image.Image:
    sheet = paper_texture(DETAIL_SIZE)
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, DETAIL_SIZE[0] - 1, DETAIL_SIZE[1] - 1), outline=(33, 44, 44, 160), width=2)
    draw.rectangle((28, 42, 340, 310), outline=(33, 44, 44, 120), width=2)
    draw.line((36, 92, 324, 92), fill=(213, 49, 35, 95), width=2)
    for y in [430, 466, 502, 538]:
        draw.line((36, y, 320, y), fill=(55, 58, 50, 76), width=2)
    draw.ellipse((214, 586, 326, 698), outline=(210, 43, 32, 160), width=4)
    draw.ellipse((230, 602, 310, 682), outline=(210, 43, 32, 120), width=3)
    draw_halftone(draw, (286, 70), 8, 6, (20, 28, 27, 95))
    return sheet


def make_cta_atlas() -> Image.Image:
    atlas = Image.new("RGBA", (1920, 64), (0, 0, 0, 0))
    specs = [
        ((196, 38, 26, 245), (250, 222, 170, 210), 0),
        ((218, 52, 34, 255), (255, 236, 196, 230), 0),
        ((150, 28, 22, 245), (236, 204, 156, 200), 2),
        ((88, 70, 62, 210), (150, 142, 128, 160), 0),
        ((220, 60, 38, 255), (255, 235, 188, 240), 0),
        ((170, 42, 31, 235), (235, 211, 168, 200), 0),
    ]
    for i, (fill, edge, offset_y) in enumerate(specs):
        frame = Image.new("RGBA", (320, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        y = offset_y
        draw.rounded_rectangle((4, 5 + y, 316, 58 + y), radius=5, fill=fill, outline=edge, width=2)
        draw.rectangle((24, 51 + y, 246, 55 + y), fill=(250, 220, 170, 80))
        draw.polygon((268, 18 + y, 294, 32 + y, 268, 46 + y, 276, 32 + y), fill=edge)
        paste_alpha(atlas, frame, (i * 320, 0))
    return atlas


def make_hud_strip() -> Image.Image:
    frame = Image.new("RGBA", (1856, 72), (5, 13, 22, 222))
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, 1855, 71), outline=(154, 136, 91, 150), width=2)
    draw.rectangle((16, 12, 420, 44), outline=(37, 99, 105, 120), width=1)
    draw.line((472, 45, 1440, 45), fill=(206, 52, 32, 80), width=2)
    draw.rounded_rectangle((1580, 9, 1818, 54), radius=5, outline=(210, 202, 166, 130), fill=(16, 25, 42, 155), width=1)
    draw_halftone(draw, (1660, 22), 14, 4, (42, 184, 190, 80))
    draw_halftone(draw, (1120, 13), 20, 3, (210, 46, 28, 80))
    return frame


def make_contact_sheet(paths: list[Path]) -> None:
    thumbs = []
    for path in paths:
        img = Image.open(path).convert("RGBA")
        img.thumbnail((360, 220), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (390, 260), (9, 16, 24, 255))
        paste_alpha(tile, img, ((390 - img.width) // 2, 18))
        draw = ImageDraw.Draw(tile)
        draw.text((14, 232), path.name, fill=(230, 222, 194, 255))
        thumbs.append(tile)
    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 390, rows * 260), (4, 9, 15, 255))
    for i, tile in enumerate(thumbs):
        paste_alpha(sheet, tile, ((i % cols) * 390, (i // cols) * 260))
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(CONTACT)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: list[tuple[str, Image.Image]] = [
        ("rt-board-shell.png", make_board_shell()),
        ("rt-map-base-clean.png", make_clean_map()),
        ("rt-map-route-layer.png", make_route_layer()),
        ("rt-pin-atlas.png", make_pin_atlas()),
        ("rt-pin-label-atlas.png", make_pin_label_atlas()),
        ("rt-task-card-atlas.png", make_task_card_atlas()),
        ("rt-filter-tab-atlas.png", make_filter_tab_atlas()),
        ("rt-detail-sheet-base.png", make_detail_sheet()),
        ("rt-cta-dispatch-atlas.png", make_cta_atlas()),
        ("rt-hud-strip.png", make_hud_strip()),
    ]
    saved: list[Path] = []
    for name, image in outputs:
        path = OUT / name
        image.save(path)
        saved.append(path)
        print(f"wrote {path.relative_to(ROOT)} {image.size} {image.mode}")
    make_contact_sheet(saved)
    print(f"wrote {CONTACT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
