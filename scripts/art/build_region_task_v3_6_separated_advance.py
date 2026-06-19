from __future__ import annotations

from PIL import Image, ImageDraw

from build_region_task_v3_5_rectified_real_content_style import (
    BLACK,
    BODY_BOLD,
    CANVAS,
    CYAN,
    GOLD,
    H2,
    INK,
    MICRO,
    MUTED,
    NAVY,
    OUT_DIR as _V35_OUT_DIR,
    PAPER,
    RED,
    ROOT,
    SMALL,
    SMALL_BOLD,
    SOURCE,
    TINY,
    WHITE,
    _draw_map_function_marks,
    _draw_rectified_left,
    _draw_rectified_right,
    _halftone,
    _text,
)


OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-6-separated-advance"
OUT_FULL = OUT_DIR / "01-region-task-v3-6-separated-advance.png"
OUT_BOTTOM_CROP = OUT_DIR / "02-bottom-global-schedule-strip.png"
OUT_RIGHT_GAP_CROP = OUT_DIR / "03-right-task-cta-separated-from-advance.png"
OUT_CONFIRM_CROP = OUT_DIR / "04-advance-confirming-state-crop.png"

del _V35_OUT_DIR


def _draw_calendar_icon(draw: ImageDraw.ImageDraw, x: int, y: int, color) -> None:
    draw.rectangle((x, y + 5, x + 34, y + 38), outline=color, width=2)
    draw.rectangle((x, y + 5, x + 34, y + 14), fill=color)
    draw.line((x + 8, y, x + 8, y + 10), fill=color, width=3)
    draw.line((x + 26, y, x + 26, y + 10), fill=color, width=3)
    for gx in (x + 10, x + 20):
        draw.line((gx, y + 18, gx, y + 34), fill=(*color[:3], 120), width=1)
    for gy in (y + 23, y + 30):
        draw.line((x + 6, gy, x + 30, gy), fill=(*color[:3], 120), width=1)


def _draw_day_button(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int] = (674, 944, 236, 66),
    *,
    confirming: bool = False,
) -> None:
    x, y, w, h = rect
    outline = (243, 188, 73, 255) if confirming else GOLD
    fill = (13, 31, 43, 248) if confirming else NAVY
    draw.rounded_rectangle((x + 5, y + 7, x + w + 5, y + h + 7), radius=9, fill=(0, 0, 0, 92))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=9, fill=fill, outline=outline, width=3)
    _draw_calendar_icon(draw, x + 24, y + 16, outline)
    draw.line((x + 78, y + h - 16, x + w - 62, y + h - 16), fill=(*outline[:3], 190), width=2)
    draw.line((x + w - 70, y + 14, x + w - 70, y + h - 14), fill=(244, 210, 140, 76), width=1)
    draw.polygon(
        [(x + w - 48, y + 17), (x + w - 24, y + h // 2), (x + w - 48, y + h - 17)],
        fill=outline,
    )
    label = "确认推进？" if confirming else "推进一天"
    sub = "再次点击执行" if confirming else "DAY +1"
    _text(draw, (x + 78, y + 13), label, BODY_BOLD, WHITE, w - 150)
    _text(draw, (x + 80, y + 42), sub, MICRO, outline, w - 150)


def _draw_bottom_receipt(base: Image.Image, *, confirming: bool = False) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    strip = (332, 922, 1330, 1044)
    draw.rectangle(strip, fill=(247, 239, 218, 214), outline=(95, 67, 39, 96), width=1)
    draw.rectangle((338, 928, 458, 1038), outline=(216, 58, 37, 120), width=2)
    draw.ellipse((364, 946, 430, 1012), outline=(216, 58, 37, 145), width=3)
    draw.line((620, 940, 620, 1028), fill=(59, 54, 45, 88), width=1)
    draw.line((946, 940, 946, 1028), fill=(59, 54, 45, 88), width=1)
    _halftone(draw, (1168, 928), 24, 18, (216, 58, 37, 70))

    _text(draw, (482, 946), "本周区域事件", SMALL_BOLD, INK, 118)
    _text(draw, (482, 974), "军方封锁 · 本区对手骰 +1", SMALL, INK, 120, line_gap=2)
    _text(draw, (482, 1000), "探索周余 4天 · 已选 M330", TINY, MUTED, 128, line_gap=1)

    draw.rounded_rectangle((648, 934, 930, 1024), radius=8, fill=(10, 24, 34, 232), outline=(214, 158, 61, 120), width=1)
    _text(draw, (664, 930), "全局日程", MICRO, (227, 188, 104, 255), 80, line_gap=1)
    _draw_day_button(draw, confirming=confirming)

    _text(draw, (970, 946), "当前派遣", SMALL_BOLD, INK, 120)
    _text(draw, (970, 976), "2 / 5", H2, INK, 80, line_gap=1)
    draw.rectangle((1034, 990, 1160, 1000), outline=(32, 94, 94, 126), width=1)
    draw.rectangle((1036, 992, 1092, 998), fill=CYAN)
    _text(draw, (1184, 950), "预计返报", SMALL_BOLD, INK, 88)
    _text(draw, (1184, 980), "1 天后", H2, INK, 88, line_gap=1)
    _text(draw, (970, 1010), "推进日程前需再次确认；不与任务签批共享热区。", MICRO, MUTED, 324, line_gap=1)


def build(*, confirming: bool = False) -> Image.Image:
    image = Image.open(SOURCE).convert("RGBA").resize(CANVAS)
    _draw_rectified_left(image)
    _draw_map_function_marks(image)
    _draw_rectified_right(image)
    _draw_bottom_receipt(image, confirming=confirming)
    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = build()
    image.save(OUT_FULL)
    image.crop((300, 900, 1360, 1068)).save(OUT_BOTTOM_CROP)
    image.crop((1320, 646, 1888, 1048)).save(OUT_RIGHT_GAP_CROP)
    confirming = build(confirming=True)
    confirming.crop((620, 916, 960, 1042)).save(OUT_CONFIRM_CROP)
    print(OUT_DIR)
    print(OUT_FULL.name)
    print(OUT_BOTTOM_CROP.name)
    print(OUT_RIGHT_GAP_CROP.name)
    print(OUT_CONFIRM_CROP.name)


if __name__ == "__main__":
    main()
