from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"D:\angos")
SOURCE = ROOT / "image_gen/2026-08-18/world-map-rough-abstraction-filled-target-v1/07-geometry-guided-edit-1920x1080.png"
CARD_MASTER = ROOT / "image_gen/2026-08-18/world-map-rough-abstraction-filled-target-v1/09-region-card-simple-paper-master-imagegen.png"
OUTPUT = ROOT / "image_gen/2026-08-18/world-map-rough-abstraction-filled-target-v1/08-filled-state-rough-abstraction-contract-corrected-1920x1080.png"

FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

CARD_SIZE = (480, 244)
CARD_X = 28
CARD_YS = (132, 385, 638)
PHOTO_RECT = (22, 63, 229, 195)  # 207×132, exact 69:44

STORIES = (
    {
        "number": "01",
        "title": "北美禁区带",
        "state": "已选择",
        "warning": "红线升温",
        "summary": ("可进入", "声望 ≥ 55 或 线人许可"),
        "image": ROOT / "gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/north_america_story_1104x704.png",
    },
    {
        "number": "02",
        "title": "东亚神秘地带",
        "state": "锁定",
        "warning": "",
        "summary": ("暂不可进入", "声望 ≥ 55 或『罗斯威尔残页』"),
        "image": ROOT / "gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/east_asia_story_1104x704.png",
    },
    {
        "number": "03",
        "title": "太平洋失航带",
        "state": "锁定",
        "warning": "",
        "summary": ("暂不可进入", "北美追踪第 2 环 或 线人许可"),
        "image": ROOT / "gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/pacific_story_1104x704.png",
    },
)


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def remove_connected_light_background(image: Image.Image) -> Image.Image:
    """Remove only the baked checkerboard connected to the outer border."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_background(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return min(red, green, blue) >= 228 and max(red, green, blue) - min(red, green, blue) <= 8

    def seed(x: int, y: int) -> None:
        index = y * width + x
        if not visited[index] and is_background(x, y):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        seed(x, 0)
        seed(x, height - 1)
    for y in range(height):
        seed(0, y)
        seed(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for neighbor_x, neighbor_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                index = neighbor_y * width + neighbor_x
                if not visited[index] and is_background(neighbor_x, neighbor_y):
                    visited[index] = 1
                    queue.append((neighbor_x, neighbor_y))

    alpha = Image.new("L", (width, height), 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if visited[row + x]:
                alpha_pixels[x, y] = 0

    result = image.convert("RGBA")
    result.putalpha(alpha)
    bbox = alpha.getbbox()
    if bbox is None:
        raise RuntimeError("Card master background removal produced an empty asset")
    return result.crop(bbox)


def build_card(master: Image.Image, story: dict[str, object], selected: bool) -> Image.Image:
    card = master.resize(CARD_SIZE, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(card, "RGBA")

    ink = (26, 40, 43, 255)
    muted = (75, 85, 82, 255)
    cobalt = (47, 91, 126, 255)
    olive = (91, 96, 66, 255)
    rust = (154, 62, 45, 255)
    if selected:
        draw.rectangle((3, 8, 8, 236), fill=cobalt)

    draw.text((18, 12), str(story["number"]), font=font(34, bold=True), fill=cobalt if selected else olive)
    draw.text((72, 18), str(story["title"]), font=font(21, bold=True), fill=ink)

    state_box = (390, 13, 461, 43)
    if selected:
        draw.rectangle(state_box, fill=(220, 224, 216, 230), outline=cobalt, width=2)
        state_color = cobalt
    else:
        draw.rectangle(state_box, fill=(97, 101, 70, 235), outline=olive, width=2)
        state_color = (233, 229, 213, 255)
    state_text = str(story["state"])
    state_font = font(16, bold=True)
    state_bbox = draw.textbbox((0, 0), state_text, font=state_font)
    state_x = state_box[0] + (state_box[2] - state_box[0] - (state_bbox[2] - state_bbox[0])) // 2
    state_y = state_box[1] + 3
    draw.text((state_x, state_y), state_text, font=state_font, fill=state_color)

    photo = Image.open(Path(str(story["image"]))).convert("RGB")
    if photo.size != (1104, 704):
        raise ValueError(f"Canonical source must be 1104×704: {story['image']} = {photo.size}")
    photo = photo.resize((207, 132), Image.Resampling.LANCZOS)
    card.alpha_composite(photo.convert("RGBA"), (PHOTO_RECT[0], PHOTO_RECT[1]))
    draw.rectangle(PHOTO_RECT, outline=(31, 51, 58, 255), width=2)

    warning = str(story["warning"])
    if warning:
        draw.rectangle((258, 68, 263, 92), fill=rust)
        draw.text((272, 65), warning, font=font(16, bold=True), fill=rust)
        draw.line((272, 91, 322, 91), fill=(154, 62, 45, 150), width=2)

    summary = story["summary"]
    assert isinstance(summary, tuple)
    draw.text((258, 108), str(summary[0]), font=font(15, bold=True), fill=ink)
    draw.text((258, 138), str(summary[1]), font=font(11), fill=muted)
    draw.text((258, 166), "WMW 地区简报", font=font(11), fill=muted)

    draw.text((20, 216), f"档案 {story['number']} · 来源：夜班编辑台", font=font(13), fill=muted)

    if not selected:
        veil = Image.new("RGBA", CARD_SIZE, (82, 87, 69, 13))
        card = Image.alpha_composite(card, veil)

    return card


def main() -> None:
    canvas = Image.open(SOURCE).convert("RGBA")
    if canvas.size != (1920, 1080):
        raise ValueError(f"Source must be 1920×1080, got {canvas.size}")

    # Clear the unreliable generated card stack with a narrow strip sampled from the same ImageGen board.
    clear_box = (20, 126, 522, 914)
    strip = canvas.crop((0, clear_box[1], 24, clear_box[3]))
    replacement = Image.new("RGBA", (clear_box[2] - clear_box[0], clear_box[3] - clear_box[1]))
    for x in range(0, replacement.width, strip.width):
        tile = ImageOps.mirror(strip) if (x // strip.width) % 2 else strip
        replacement.alpha_composite(tile, (x, 0))
    canvas.paste(replacement, (clear_box[0], clear_box[1]))

    master = remove_connected_light_background(Image.open(CARD_MASTER))
    for index, (story, y) in enumerate(zip(STORIES, CARD_YS)):
        card = build_card(master, story, selected=index == 0)
        canvas.alpha_composite(card, (CARD_X, y))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, quality=96)
    print(OUTPUT)


if __name__ == "__main__":
    main()
