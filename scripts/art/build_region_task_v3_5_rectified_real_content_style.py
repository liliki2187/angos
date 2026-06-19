from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/artboard_v3/rt-artboard-full.png"
OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-5-rectified-style"
OUT_FULL = OUT_DIR / "01-region-task-v3-5-rectified-real-content.png"
OUT_LEFT_CROP = OUT_DIR / "02-left-rectified-task-stack.png"
OUT_RIGHT_CROP = OUT_DIR / "03-right-rectified-approval-sheet.png"
OUT_BOTTOM_CROP = OUT_DIR / "04-bottom-advance-day-button.png"

CANVAS = (1920, 1080)

INK = (30, 37, 34, 255)
MUTED = (77, 86, 81, 255)
PAPER = (249, 242, 224, 248)
PAPER_SOFT = (252, 247, 233, 238)
NAVY = (8, 19, 31, 244)
NAVY_SOFT = (12, 29, 43, 232)
WHITE = (249, 243, 226, 255)
RED = (220, 56, 37, 238)
RED_DARK = (145, 32, 27, 240)
CYAN = (36, 169, 180, 236)
BLUE = (34, 118, 184, 235)
TEAL = (29, 142, 149, 236)
GOLD = (214, 158, 61, 240)
VIOLET = (126, 92, 206, 235)
BLACK = (20, 25, 32, 238)


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    names = ["msyhbd.ttc" if bold else "msyh.ttc", "simhei.ttf", "NotoSansCJK-Regular.ttc"]
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


H1 = _font(26, True)
H2 = _font(22, True)
BODY = _font(16)
BODY_BOLD = _font(16, True)
SMALL = _font(13)
SMALL_BOLD = _font(13, True)
TINY = _font(11)
MICRO = _font(9)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        candidate = current + ch
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def _text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill=INK,
    width: int | None = None,
    line_gap: int = 4,
) -> int:
    x, y = xy
    for raw in text.split("\n"):
        rows = _wrap(draw, raw, font, width) if width else [raw]
        for row in rows:
            draw.text((x, y), row, font=font, fill=fill)
            y += int(getattr(font, "size", 14) * 1.22) + line_gap
    return y


def _paste(base: Image.Image, layer: Image.Image, xy: tuple[int, int]) -> None:
    base.alpha_composite(layer.convert("RGBA"), xy)


def _noise(size: tuple[int, int], alpha: int = 20) -> Image.Image:
    noise = Image.effect_noise(size, 28).convert("L")
    overlay = Image.new("RGBA", size, (255, 255, 255, 0))
    overlay.putalpha(noise.point(lambda v: int(abs(v - 128) / 128 * alpha)))
    return overlay


def _paper_texture(size: tuple[int, int], tint=(247, 239, 218), alpha: int = 255) -> Image.Image:
    paper = Image.new("RGBA", size, (*tint, alpha))
    paper = Image.alpha_composite(paper, _noise(size, 16))
    draw = ImageDraw.Draw(paper, "RGBA")
    return paper


def _halftone(draw: ImageDraw.ImageDraw, origin: tuple[int, int], cols: int, rows: int, color) -> None:
    ox, oy = origin
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                x = ox + col * 5
                y = oy + row * 5
                draw.rectangle((x, y, x + 2, y + 2), fill=color)


def _crop_marks(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], color) -> None:
    x, y, w, h = rect
    marks = [
        (x, y, 20, 0), (x, y, 0, 20),
        (x + w, y, -20, 0), (x + w, y, 0, 20),
        (x, y + h, 20, 0), (x, y + h, 0, -20),
        (x + w, y + h, -20, 0), (x + w, y + h, 0, -20),
    ]
    for mx, my, dx, dy in marks:
        draw.line((mx, my, mx + dx, my + dy), fill=color, width=2)


def _shadowed_panel(
    base: Image.Image,
    xy: tuple[int, int],
    size: tuple[int, int],
    *,
    fill=(247, 239, 218),
    outline=(31, 43, 43, 150),
    accent=RED,
    shadow_alpha: int = 76,
) -> ImageDraw.ImageDraw:
    x, y = xy
    w, h = size
    shadow = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow, "RGBA")
    sd.rounded_rectangle((12, 12, w + 12, h + 12), radius=5, fill=(0, 0, 0, shadow_alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(2.0))
    _paste(base, shadow, (x - 2, y - 1))

    panel = _paper_texture(size, fill)
    draw = ImageDraw.Draw(panel, "RGBA")
    draw.rectangle((0, 0, w - 1, h - 1), outline=outline, width=2)
    draw.rectangle((22, 22, w - 23, h - 23), outline=(33, 44, 44, 85), width=1)
    _crop_marks(draw, (24, 24, w - 48, h - 48), (*accent[:3], 120))
    _halftone(draw, (w - 92, h - 82), 12, 8, (22, 31, 31, 70))
    _paste(base, panel, xy)
    return ImageDraw.Draw(base, "RGBA")


def _badge(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], label: str, color, font=MICRO) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=color, outline=(255, 246, 210, 145), width=1)
    _text(draw, (x + 9, y + 4), label, font, WHITE, w - 18, line_gap=1)


def _draw_rectified_left(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")

    # Hide the perspective document stack with a desk-colored sleeve, then rebuild straight paper slips on top.
    draw.rounded_rectangle((94, 116, 574, 900), radius=4, fill=(6, 16, 28, 218), outline=(27, 83, 96, 130), width=2)
    _halftone(draw, (112, 138), 18, 18, (35, 176, 188, 54))
    draw.rectangle((110, 150, 126, 862), fill=RED_DARK)
    draw.rectangle((126, 150, 139, 862), fill=(245, 238, 216, 188))
    draw.line((104, 884, 558, 884), fill=(14, 42, 55, 210), width=11)

    cards = [
        ("51 区外围公路", "白色调查 · 耗时 2天 · 探索4 / 生存2", RED, None),
        ("罗斯威尔档案残页", "线索调查 · 耗时 1天 · 调查后生成任务", BLUE, "线索"),
        ("突发：雷达异常光点", "红色截稿 · 剩 4天 · 对手骰3", RED, "截稿"),
        ("M330 未班车空白段", "深度调查链 · 地图点选当前环 1/4", CYAN, "链 1/4"),
    ]
    y = 164
    for i, (title, meta, accent, tag) in enumerate(cards):
        x = 152
        w, h = 382, 124
        if i > 0:
            # Visible rear-sheet lips, still axis-aligned.
            draw.rectangle((x + 12, y - 14, x + w + 24, y - 4), fill=(230, 222, 205, 220), outline=(36, 47, 45, 90), width=1)
        _shadowed_panel(base, (x, y), (w, h), fill=(248, 240, 219), accent=accent, shadow_alpha=48)
        draw = ImageDraw.Draw(base, "RGBA")
        draw.rectangle((x, y, x + 22, y + h), fill=accent)
        draw.rectangle((x + 12, y + 22, x + 26, y + 36), fill=(248, 242, 225, 230))
        draw.rectangle((x + 12, y + 52, x + 26, y + 66), fill=(248, 242, 225, 230))
        draw.rectangle((x + w - 44, y, x + w - 16, y + 44), fill=accent)
        draw.polygon((x + w - 44, y + 44, x + w - 30, y + 33, x + w - 16, y + 44), fill=(248, 240, 219, 255))
        if i == 3:
            draw.rounded_rectangle((x - 8, y - 8, x + w + 8, y + h + 8), radius=5, outline=GOLD, width=3)
            draw.rectangle((x + 32, y + 18, x + 39, y + h - 18), fill=VIOLET)
        _text(draw, (x + 62, y + 33), title, BODY_BOLD, INK, 230)
        _text(draw, (x + 62, y + 66), meta, SMALL, INK, 250)
        if tag:
            _badge(draw, (x + w - 104, y + 28, 76, 25), tag, VIOLET if "链" in tag else accent)
        y += 162

    draw.rounded_rectangle((148, 830, 502, 890), radius=5, fill=(17, 31, 42, 230), outline=(90, 110, 115, 205), width=1)
    _text(draw, (166, 842), "已派遣 · 执行中：51区、雷达异常", SMALL, WHITE, 318)
    _text(draw, (166, 868), "明日到期：雷达异常 · 可展开查看", MICRO, (218, 225, 218, 255), 318)


def _map_label(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], title: str, stage: str, tone, selected=False) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x + 3, y + 4, x + w + 3, y + h + 4), radius=4, fill=(0, 0, 0, 66))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=(249, 242, 224, 238), outline=GOLD if selected else (31, 42, 43, 150), width=2)
    if selected:
        draw.rounded_rectangle((x - 6, y - 6, x + w + 6, y + h + 6), radius=6, outline=GOLD, width=2)
    _badge(draw, (x + 10, y + 11, 48, 20), stage, tone)
    _text(draw, (x + 68, y + 10), title, TINY, INK, w - 78, line_gap=1)
    if selected:
        _text(draw, (x + 68, y + 29), "可点任务", MICRO, (91, 69, 28, 255), w - 78, line_gap=1)


def _draw_map_function_marks(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    draw.line((1128, 524, 1016, 692), fill=(126, 92, 206, 190), width=4)
    draw.ellipse((1088, 484, 1168, 564), outline=GOLD, width=3)
    draw.ellipse((982, 658, 1050, 726), outline=(214, 158, 61, 145), width=2)
    _map_label(draw, (900, 286, 124, 46), "雷达站", "截稿", RED)
    _map_label(draw, (744, 420, 130, 48), "51区公路", "调查", RED)
    _map_label(draw, (804, 592, 138, 48), "残页线索", "线索", BLUE)
    _map_label(draw, (642, 714, 136, 48), "异常光点", "截稿", RED)
    _map_label(draw, (1134, 502, 154, 48), "M330", "1/4", VIOLET, selected=True)
    _map_label(draw, (1004, 708, 154, 48), "下一环？", "2/4", BLACK)


def _draw_rectified_right(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")

    # Keep the metal clip from the source, but cover the slanted paper body with a straight rebuild.
    draw.rounded_rectangle((1356, 116, 1868, 1010), radius=4, fill=(8, 18, 29, 218), outline=(38, 54, 58, 125), width=2)
    for dx, dy, color in [(28, 18, (211, 200, 181, 230)), (16, 10, (229, 220, 202, 240)), (0, 0, (248, 240, 219, 255))]:
        _shadowed_panel(base, (1388 + dx, 142 + dy), (426, 804), fill=color[:3], accent=RED, shadow_alpha=42 if dx else 72)

    draw = ImageDraw.Draw(base, "RGBA")
    x, y, w, h = 1388, 142, 426, 804
    draw.rectangle((x + 24, y + 28, x + w - 24, y + 100), outline=(36, 48, 48, 150), width=2)
    _text(draw, (x + 44, y + 46), "M330 未班车空白段", H2, INK, 320)
    _text(draw, (x + 44, y + 76), "北美禁区 / 深度调查链", SMALL, MUTED, 300)

    body_rect = (x + 28, y + 118, w - 56, 224)
    draw.rectangle((body_rect[0], body_rect[1], body_rect[0] + body_rect[2], body_rect[1] + body_rect[3]), outline=(36, 48, 48, 135), width=2)
    _crop_marks(draw, (body_rect[0] + 8, body_rect[1] + 10, body_rect[2] - 16, body_rect[3] - 20), (50, 65, 63, 105))
    _halftone(draw, (x + 250, y + 126), 20, 3, (216, 58, 37, 80))
    body = "一段车载录音缺了三秒，乘客口供互相矛盾，但都指向同一站。\n目标：找出缺失三秒对应的站点记录。\n需求：察 / 诡 / 理 · 耗时 2天"
    _text(draw, (x + 52, y + 164), body, BODY, INK, 318, line_gap=7)

    _ticket(draw, (x + 36, y + 382, 310, 42), "深度调查 · 当前环 1/4", VIOLET, VIOLET)
    rows = [
        ("成功后提示下一环；失败保留线索。", VIOLET),
        ("可带回：录音 / 证词", CYAN),
        ("风险：凶险，可能触发误导线索", RED),
    ]
    row_y = y + 448
    for label, color in rows:
        draw.rectangle((x + 44, row_y + 5, x + 57, row_y + 18), fill=color)
        _text(draw, (x + 70, row_y), label, SMALL, INK, 300)
        row_y += 46

    _ticket(draw, (x + 36, y + 594, 300, 36), "签批不扣天数；派遣后预计占用 2 天。", GOLD, GOLD, font=TINY)

    # A straight, separable CTA tray. It intentionally covers the old slanted red tray.
    tray = (x + 20, y + 660, w - 40, 104)
    draw.rounded_rectangle((tray[0] + 4, tray[1] + 6, tray[0] + tray[2] + 4, tray[1] + tray[3] + 6), radius=8, fill=(0, 0, 0, 82))
    draw.rounded_rectangle((tray[0], tray[1], tray[0] + tray[2], tray[1] + tray[3]), radius=8, fill=RED, outline=(252, 217, 160, 180), width=2)
    draw.rectangle((tray[0] + 24, tray[1] + 22, tray[0] + tray[2] - 82, tray[1] + tray[3] - 22), fill=(246, 238, 216, 235), outline=(116, 38, 28, 160), width=2)
    _text(draw, (tray[0] + 74, tray[1] + 38), "进入派遣签批", H1, INK, 220)
    draw.polygon(
        [
            (tray[0] + tray[2] - 66, tray[1] + 30),
            (tray[0] + tray[2] - 38, tray[1] + tray[3] // 2),
            (tray[0] + tray[2] - 66, tray[1] + tray[3] - 30),
        ],
        fill=(248, 238, 210, 238),
    )


def _ticket(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    label: str,
    outline,
    accent,
    *,
    font=SMALL_BOLD,
) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x + 2, y + 3, x + w + 2, y + h + 3), radius=4, fill=(0, 0, 0, 50))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=(250, 243, 226, 238), outline=outline, width=2)
    draw.rectangle((x, y, x + 10, y + h), fill=accent)
    _text(draw, (x + 20, y + 11), label, font, (77, 49, 145, 255) if accent == VIOLET else INK, w - 40, line_gap=1)
    draw.line((x + 22, y + h - 11, x + w - 20, y + h - 11), fill=(47, 52, 45, 65), width=1)


def _draw_bottom_receipt(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    draw.rectangle((332, 922, 1330, 1044), fill=(247, 239, 218, 212), outline=(95, 67, 39, 90), width=1)
    draw.rectangle((338, 928, 458, 1038), outline=(216, 58, 37, 120), width=2)
    draw.ellipse((364, 946, 430, 1012), outline=(216, 58, 37, 145), width=3)
    _halftone(draw, (1140, 926), 28, 20, (216, 58, 37, 75))

    _text(draw, (482, 952), "探索周 余 4天 · 北美禁区 · 已选 M330", SMALL, INK, 320)
    _text(draw, (482, 986), "当前回执：签批不消耗天数，派遣后占用 2 天。", TINY, MUTED, 520)
    _text(draw, (804, 952), "地区事件：军方封锁 · 本区对手骰 +1", SMALL, INK, 360)
    _text(draw, (1000, 992), "执行中 2 / 到期 1", SMALL_BOLD, INK, 140)
    _draw_day_button(draw)


def _draw_day_button(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int] = (1126, 948, 188, 62)) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x + 4, y + 6, x + w + 4, y + h + 6), radius=8, fill=(0, 0, 0, 88))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=NAVY, outline=GOLD, width=3)
    draw.rectangle((x + 9, y + 9, x + 20, y + h - 9), fill=RED)
    draw.line((x + 32, y + h - 13, x + w - 58, y + h - 13), fill=(214, 158, 61, 190), width=2)
    draw.polygon(
        [(x + w - 47, y + 16), (x + w - 24, y + h // 2), (x + w - 47, y + h - 16)],
        fill=(214, 158, 61, 240),
    )
    _text(draw, (x + 34, y + 13), "推进一天", BODY_BOLD, WHITE)
    _text(draw, (x + 36, y + 40), "DAY +1", MICRO, (214, 158, 61, 255))


def build() -> Image.Image:
    image = Image.open(SOURCE).convert("RGBA").resize(CANVAS)
    _draw_rectified_left(image)
    _draw_map_function_marks(image)
    _draw_rectified_right(image)
    _draw_bottom_receipt(image)
    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = build()
    image.save(OUT_FULL)
    image.crop((80, 110, 590, 910)).save(OUT_LEFT_CROP)
    image.crop((1350, 110, 1876, 1018)).save(OUT_RIGHT_CROP)
    image.crop((1118, 918, 1348, 1040)).save(OUT_BOTTOM_CROP)
    print(OUT_DIR)
    print(OUT_FULL.name)
    print(OUT_LEFT_CROP.name)
    print(OUT_RIGHT_CROP.name)
    print(OUT_BOTTOM_CROP.name)


if __name__ == "__main__":
    main()
