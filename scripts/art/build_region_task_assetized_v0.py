from __future__ import annotations

"""Deprecated local-cleanup experiment for the region task board.

This script may be useful for comparing extraction/inpaint ideas, but it must
not overwrite production assets. The production map base should come from the
approved image/reference workflow and keep the original map's visual density.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/region-task-board-clean-pixel-v2.png"
OUT = ROOT / "tmp/whitebox/region_task_assetized_v0"
CONTACT = ROOT / "docs/screenshots/2026-06-16-region-task-board-reference-v1/local-cleanup-whitebox-contact-sheet.png"

CANVAS = (1920, 1080)
MAP_RECT = (492, 126, 492 + 960, 126 + 742)
MAP_SOURCE_RECT = (560, 126, 1328, 868)
DETAIL_RECT = (1482, 128, 1482 + 386, 128 + 840)
CTA_RECT = (1530, 872, 1530 + 320, 872 + 64)


def paste_alpha(dst: Image.Image, src: Image.Image, xy: tuple[int, int]) -> None:
    dst.alpha_composite(src.convert("RGBA"), xy)


def safe_crop(img: Image.Image, rect: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    crop = img.crop(rect)
    if crop.size != size:
        crop = crop.resize(size, Image.Resampling.LANCZOS)
    return crop


def paper_texture(src: Image.Image, size: tuple[int, int]) -> Image.Image:
    sample = src.crop((160, 190, 520, 315)).resize(size, Image.Resampling.BICUBIC).convert("RGBA")
    overlay = Image.new("RGBA", size, (248, 239, 216, 205))
    return Image.alpha_composite(sample, overlay)


def draw_halftone(draw: ImageDraw.ImageDraw, origin: tuple[int, int], cols: int, rows: int, color: tuple[int, int, int, int]) -> None:
    ox, oy = origin
    for y in range(rows):
        for x in range(cols):
            if (x + y) % 2 == 0:
                draw.rectangle((ox + x * 5, oy + y * 5, ox + x * 5 + 2, oy + y * 5 + 2), fill=color)


def inpaint_from_edges(src: Image.Image, mask: Image.Image, max_iterations: int = 260) -> Image.Image:
    source = np.asarray(src.convert("RGB"), dtype=np.float32)
    missing = np.asarray(mask.convert("L")) > 0
    if not missing.any():
        return src.convert("RGB")

    filled = source.copy()
    known = ~missing
    if known.any():
        base = np.median(source[known], axis=0)
    else:
        base = np.array([12.0, 32.0, 48.0], dtype=np.float32)
    filled[missing] = base

    remaining = missing.copy()
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ]
    height, width = remaining.shape
    for _index in range(max_iterations):
        sums = np.zeros_like(filled)
        counts = np.zeros((height, width), dtype=np.float32)
        known_now = ~remaining

        for dy, dx in directions:
            src_y0 = max(0, -dy)
            src_y1 = min(height, height - dy)
            dst_y0 = max(0, dy)
            dst_y1 = min(height, height + dy)
            src_x0 = max(0, -dx)
            src_x1 = min(width, width - dx)
            dst_x0 = max(0, dx)
            dst_x1 = min(width, width + dx)

            neighbor_known = known_now[src_y0:src_y1, src_x0:src_x1]
            sums[dst_y0:dst_y1, dst_x0:dst_x1] += filled[src_y0:src_y1, src_x0:src_x1] * neighbor_known[..., None]
            counts[dst_y0:dst_y1, dst_x0:dst_x1] += neighbor_known.astype(np.float32)

        boundary = remaining & (counts > 0)
        if not boundary.any():
            break
        filled[boundary] = sums[boundary] / counts[boundary, None]
        remaining[boundary] = False

    result = np.clip(filled, 0, 255).astype(np.uint8)
    filled_img = Image.fromarray(result, "RGB")
    feather = mask.convert("L").filter(ImageFilter.GaussianBlur(2.2))
    return Image.composite(filled_img, src.convert("RGB"), feather)


def make_map_dynamic_mask(src: Image.Image, include_route_colors: bool = True) -> Image.Image:
    rgb = np.asarray(src.convert("RGB"))
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]
    paper = (r > 150) & (g > 132) & (b > 104)
    route_red = (r > 120) & (g < 118) & (b < 112) & ((r - g) > 34)
    route_cyan = (g > 112) & (b > 112) & (r < 112) & ((b - r) > 22)
    dynamic = paper | route_red | route_cyan if include_route_colors else paper
    mask_array = dynamic.astype(np.uint8) * 255
    mask = Image.fromarray(mask_array, "L")
    draw = ImageDraw.Draw(mask)
    cleanup_rects = [
        (360, 54, 676, 214),
        (172, 170, 486, 350),
        (32, 438, 328, 632),
        (254, 326, 542, 524),
        (618, 248, 940, 456),
        (508, 426, 826, 636),
    ]
    for rect in cleanup_rects:
        draw.rounded_rectangle(rect, radius=20, fill=255)
    return mask.filter(ImageFilter.MaxFilter(15))


def make_board_shell(full: Image.Image) -> Image.Image:
    shell = full.copy().convert("RGBA")
    draw = ImageDraw.Draw(shell)

    # Runtime-owned layers are cleared here so the shell cannot bake fake pins,
    # labels, route feedback, or button text underneath Godot controls.
    draw.rectangle(MAP_RECT, fill=(4, 13, 24, 255))
    for x in range(MAP_RECT[0], MAP_RECT[2] + 1, 48):
        draw.line((x, MAP_RECT[1], x, MAP_RECT[3]), fill=(36, 76, 92, 46), width=1)
    for y in range(MAP_RECT[1], MAP_RECT[3] + 1, 48):
        draw.line((MAP_RECT[0], y, MAP_RECT[2], y), fill=(36, 76, 92, 46), width=1)
    draw.rectangle(MAP_RECT, outline=(151, 129, 82, 118), width=2)
    draw.rectangle((MAP_RECT[0] + 10, MAP_RECT[1] + 10, MAP_RECT[2] - 10, MAP_RECT[3] - 10), outline=(24, 121, 134, 74), width=1)

    paper_fill = (238, 226, 202, 255)
    draw.rounded_rectangle(CTA_RECT, radius=5, fill=paper_fill)
    draw.line((CTA_RECT[0] + 16, CTA_RECT[1] + 18, CTA_RECT[2] - 62, CTA_RECT[1] + 18), fill=(37, 43, 40, 82), width=1)
    draw.line((CTA_RECT[0] + 16, CTA_RECT[1] + 40, CTA_RECT[2] - 82, CTA_RECT[1] + 40), fill=(37, 43, 40, 56), width=1)

    return shell.convert("RGB")


def make_clean_map(full: Image.Image) -> Image.Image:
    src = safe_crop(full, MAP_SOURCE_RECT, (960, 742)).convert("RGBA")
    mask = make_map_dynamic_mask(src, True)
    cleaned = inpaint_from_edges(src, mask)
    return cleaned.convert("RGB")


def make_route_layer(full: Image.Image) -> Image.Image:
    src = safe_crop(full, MAP_SOURCE_RECT, (960, 742)).convert("RGBA")
    layer = Image.new("RGBA", src.size, (0, 0, 0, 0))
    pixels = src.load()
    out = layer.load()
    remove_mask = make_map_dynamic_mask(src, False)
    remove_pixels = remove_mask.load()
    for y in range(src.height):
        for x in range(src.width):
            if remove_pixels[x, y] > 0:
                continue
            r, g, b, _a = pixels[x, y]
            is_red = r > 150 and g < 95 and b < 85
            is_cyan = g > 145 and b > 145 and r < 90
            if is_red or is_cyan:
                out[x, y] = (r, g, b, 130)
    return layer.filter(ImageFilter.GaussianBlur(0.35))


def draw_pin_frame(frame: Image.Image, tone: str, selected: bool = False, disabled: bool = False) -> None:
    draw = ImageDraw.Draw(frame)
    colors = {
        "red": ((232, 70, 45, 255), (96, 20, 18, 255)),
        "cyan": ((62, 194, 195, 255), (13, 81, 89, 255)),
        "gold": ((246, 181, 74, 255), (118, 67, 20, 255)),
        "gray": ((126, 127, 118, 220), (46, 50, 48, 220)),
        "black": ((38, 45, 48, 255), (8, 12, 14, 255)),
    }
    fill, edge = colors[tone]
    if disabled:
        fill, edge = colors["gray"]
    radius = 15 if selected else 13
    cx, cy = 32, 21
    draw.line((cx, cy + 13, cx, 58), fill=(14, 18, 19, 185), width=5)
    draw.polygon([(cx - 8, cy + 31), (cx + 8, cy + 31), (cx, 58)], fill=edge)
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=edge)
    draw.ellipse((cx - radius + 3, cy - radius + 3, cx + radius - 3, cy + radius - 3), fill=fill)
    draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=(255, 232, 190, 120))
    if selected:
        draw.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=(255, 214, 104, 180), width=3)


def make_pin_atlas() -> Image.Image:
    atlas = Image.new("RGBA", (384, 64), (0, 0, 0, 0))
    specs = [
        ("red", False, False),
        ("red", True, False),
        ("gold", True, False),
        ("gray", False, True),
        ("cyan", True, False),
        ("red", True, False),
    ]
    for i, spec in enumerate(specs):
        frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw_pin_frame(frame, spec[0], spec[1], spec[2])
        paste_alpha(atlas, frame, (i * 64, 0))
    return atlas


def make_pin_label_atlas(full: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", (600, 72), (0, 0, 0, 0))
    base = paper_texture(full, (200, 72))
    states = [
        ((13, 85, 91, 210), (0, 0, 0, 0)),
        ((194, 92, 28, 230), (255, 212, 98, 36)),
        ((80, 82, 72, 160), (0, 0, 0, 0)),
    ]
    for i, (edge, fill_overlay) in enumerate(states):
        frame = base.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle((5, 8, 190, 60), radius=3, outline=edge, width=2, fill=fill_overlay)
        draw.line((20, 47, 145, 47), fill=(21, 31, 32, 80), width=1)
        draw_halftone(draw, (154, 42), 7, 4, (16, 24, 25, 95))
        paste_alpha(atlas, frame, (i * 200, 0))
    return atlas


def make_task_card_atlas(full: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", (384, 720), (0, 0, 0, 0))
    accents = [
        (218, 45, 31, 235),
        (30, 169, 176, 235),
        (230, 160, 55, 245),
        (118, 118, 104, 205),
        (34, 140, 146, 235),
        (218, 45, 31, 245),
    ]
    overlays = [
        (0, 0, 0, 0),
        (255, 255, 255, 22),
        (255, 210, 80, 34),
        (54, 55, 48, 70),
        (31, 120, 130, 32),
        (205, 40, 24, 26),
    ]
    for i in range(6):
        frame = paper_texture(full, (384, 120))
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


def make_filter_tab_atlas(full: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", (480, 48), (0, 0, 0, 0))
    states = [
        ((242, 232, 208, 190), (27, 42, 45, 110)),
        ((246, 238, 215, 230), (30, 169, 176, 190)),
        ((249, 238, 206, 245), (205, 70, 34, 230)),
        ((116, 118, 108, 145), (49, 52, 47, 150)),
    ]
    for i, (fill, edge) in enumerate(states):
        frame = Image.new("RGBA", (120, 48), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle((4, 6, 116, 42), radius=3, fill=fill, outline=edge, width=2)
        draw.line((18, 30, 98, 30), fill=(31, 36, 34, 80), width=1)
        paste_alpha(atlas, frame, (i * 120, 0))
    return atlas


def make_detail_sheet(full: Image.Image) -> Image.Image:
    sheet = safe_crop(full, DETAIL_RECT, (386, 840)).convert("RGBA")
    # Remove the CTA mount area from this base so the independent CTA atlas owns button text and states.
    mask = Image.new("L", sheet.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((44, 710, 362, 792), radius=6, fill=255)
    transparent = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    sheet = Image.composite(transparent, sheet, mask)
    return sheet


def make_cta_atlas(full: Image.Image) -> Image.Image:
    base = safe_crop(full, CTA_RECT, (320, 64)).convert("RGBA")
    atlas = Image.new("RGBA", (1920, 64), (0, 0, 0, 0))
    variants = [
        base,
        ImageEnhance.Brightness(base).enhance(1.10),
        ImageChops.offset(ImageEnhance.Brightness(base).enhance(0.88), 0, 2),
        ImageEnhance.Color(ImageEnhance.Brightness(base).enhance(0.58)).enhance(0.45),
        ImageEnhance.Contrast(ImageEnhance.Brightness(base).enhance(1.12)).enhance(1.12),
        ImageEnhance.Brightness(base).enhance(0.96),
    ]
    for i, frame in enumerate(variants):
        paste_alpha(atlas, frame.crop((0, 0, 320, 64)), (i * 320, 0))
    return atlas


def make_hud_strip(full: Image.Image) -> Image.Image:
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
    src = Image.open(SRC).convert("RGB")
    full = src.resize(CANVAS, Image.Resampling.LANCZOS)
    outputs: list[tuple[str, Image.Image]] = [
        ("rt-board-shell.png", make_board_shell(full)),
        ("rt-map-base-clean.png", make_clean_map(full)),
        ("rt-map-route-layer.png", make_route_layer(full)),
        ("rt-pin-atlas.png", make_pin_atlas()),
        ("rt-pin-label-atlas.png", make_pin_label_atlas(full)),
        ("rt-task-card-atlas.png", make_task_card_atlas(full)),
        ("rt-filter-tab-atlas.png", make_filter_tab_atlas(full)),
        ("rt-detail-sheet-base.png", make_detail_sheet(full)),
        ("rt-cta-dispatch-atlas.png", make_cta_atlas(full)),
        ("rt-hud-strip.png", make_hud_strip(full)),
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
