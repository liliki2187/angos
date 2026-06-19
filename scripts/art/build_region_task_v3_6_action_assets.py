from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/assetized"
SCREENSHOT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-6-separated-advance"
STYLE_FULL = SCREENSHOT_DIR / "01-region-task-v3-6-separated-advance.png"
OUT_ATLAS = ASSET_DIR / "rt-advance-day-atlas.png"
OUT_OVERLAY = SCREENSHOT_DIR / "05-action-separation-contract-overlay.png"

FRAME = (236, 66)
FRAMES = ["default", "hover", "pressed", "disabled", "focus", "confirming"]

NAVY = (8, 19, 31, 242)
NAVY_HOVER = (13, 31, 43, 246)
NAVY_DISABLED = (24, 29, 32, 212)
GOLD = (214, 158, 61, 242)
GOLD_HOVER = (243, 188, 73, 252)
CYAN = (36, 169, 180, 226)
WHITE = (249, 243, 226, 255)
MUTED = (114, 113, 101, 210)
RED = (220, 56, 37, 235)


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for name in ("msyhbd.ttc" if bold else "msyh.ttc", "simhei.ttf"):
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT = _font(16, True)
TINY = _font(11)


def _calendar(draw: ImageDraw.ImageDraw, x: int, y: int, color) -> None:
    draw.rectangle((x, y + 5, x + 34, y + 38), outline=color, width=2)
    draw.rectangle((x, y + 5, x + 34, y + 14), fill=color)
    draw.line((x + 8, y, x + 8, y + 10), fill=color, width=3)
    draw.line((x + 26, y, x + 26, y + 10), fill=color, width=3)
    for gx in (x + 10, x + 20):
        draw.line((gx, y + 18, gx, y + 34), fill=(*color[:3], 120), width=1)
    for gy in (y + 23, y + 30):
        draw.line((x + 6, gy, x + 30, gy), fill=(*color[:3], 120), width=1)


def _draw_frame(draw: ImageDraw.ImageDraw, frame_index: int, state: str) -> None:
    x = frame_index * FRAME[0]
    y = 0
    fill = NAVY
    outline = GOLD
    alpha = 255
    offset_y = 0
    if state == "hover":
        fill = NAVY_HOVER
        outline = GOLD_HOVER
    elif state == "pressed":
        offset_y = 2
        fill = (7, 16, 26, 248)
    elif state == "disabled":
        fill = NAVY_DISABLED
        outline = MUTED
        alpha = 184
    elif state == "focus":
        fill = NAVY_HOVER
        outline = CYAN
    elif state == "confirming":
        fill = NAVY_HOVER
        outline = GOLD_HOVER

    rect = (x + 1, y + 1 + offset_y, x + FRAME[0] - 2, y + FRAME[1] - 2 + offset_y)
    draw.rounded_rectangle(rect, radius=9, fill=fill, outline=outline, width=3)
    if state == "focus":
        draw.rounded_rectangle((x + 4, y + 4, x + FRAME[0] - 5, y + FRAME[1] - 5), radius=7, outline=(*CYAN[:3], 130), width=1)
    _calendar(draw, x + 24, y + 16 + offset_y, outline)
    draw.line((x + 78, y + FRAME[1] - 16 + offset_y, x + FRAME[0] - 62, y + FRAME[1] - 16 + offset_y), fill=(*outline[:3], 184), width=2)
    draw.line((x + FRAME[0] - 70, y + 14 + offset_y, x + FRAME[0] - 70, y + FRAME[1] - 14 + offset_y), fill=(244, 210, 140, 76), width=1)
    draw.polygon(
        [
            (x + FRAME[0] - 48, y + 17 + offset_y),
            (x + FRAME[0] - 24, y + FRAME[1] // 2 + offset_y),
            (x + FRAME[0] - 48, y + FRAME[1] - 17 + offset_y),
        ],
        fill=outline,
    )
    if state == "disabled":
        draw.rectangle((x, y, x + FRAME[0], y + FRAME[1]), fill=(7, 8, 9, 82))
    if state == "confirming":
        draw.rectangle((x + 78, y + 13, x + 153, y + 34), outline=(*outline[:3], 145), width=1)
    if alpha < 255:
        draw.rectangle((x, y, x + FRAME[0], y + FRAME[1]), outline=(0, 0, 0, 0))


def build_atlas() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    atlas = Image.new("RGBA", (FRAME[0] * len(FRAMES), FRAME[1]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas, "RGBA")
    for index, state in enumerate(FRAMES):
        _draw_frame(draw, index, state)
    atlas.save(OUT_ATLAS)


def build_overlay() -> None:
    if not STYLE_FULL.exists():
        return
    image = Image.open(STYLE_FULL).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    task_cta = (1428, 804, 1796, 907)
    advance = (674, 944, 910, 1010)
    schedule = (648, 934, 930, 1024)

    draw.rounded_rectangle(task_cta, radius=8, outline=(255, 87, 60, 245), width=4)
    draw.rounded_rectangle(schedule, radius=8, outline=(214, 158, 61, 245), width=4)
    draw.rounded_rectangle(advance, radius=8, outline=(36, 169, 180, 245), width=3)
    draw.line((910, 977, 1428, 856), fill=(255, 243, 190, 160), width=3)
    draw.rectangle((948, 950, 1390, 1004), fill=(7, 18, 28, 220), outline=(214, 158, 61, 220), width=2)
    draw.text((966, 960), "动作分离：任务 CTA 与全局推进不共享热区", font=FONT, fill=WHITE)
    draw.text((966, 984), "advance_day_button 首击进入确认态", font=TINY, fill=(230, 208, 152, 255))
    draw.rectangle((1408, 760, 1816, 790), fill=(7, 18, 28, 210), outline=(255, 87, 60, 200), width=1)
    draw.text((1420, 765), "task_dispatch_cta：只进入派遣签批", font=TINY, fill=WHITE)
    out = Image.alpha_composite(image, overlay)
    out.save(OUT_OVERLAY)


def main() -> None:
    build_atlas()
    build_overlay()
    print(OUT_ATLAS)
    print(OUT_OVERLAY)


if __name__ == "__main__":
    main()
