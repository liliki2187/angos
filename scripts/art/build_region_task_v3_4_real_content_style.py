from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/artboard_v3/rt-artboard-full.png"
OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-4-real-content-style"
OUT_FULL = OUT_DIR / "01-region-task-v3-4-real-content-style.png"
OUT_RIGHT_CROP = OUT_DIR / "02-right-detail-crop.png"
OUT_BOTTOM_CROP = OUT_DIR / "03-bottom-day-button-crop.png"
CANVAS = (1920, 1080)

INK = (31, 38, 35, 255)
MUTED = (73, 82, 78, 255)
PAPER = (250, 243, 226, 232)
PAPER_DENSE = (247, 239, 218, 244)
WHITE = (248, 242, 226, 255)
NAVY = (11, 23, 35, 244)
RED = (222, 58, 36, 238)
CYAN = (36, 168, 178, 235)
BLUE = (34, 118, 184, 235)
TEAL = (31, 141, 147, 235)
GOLD = (214, 158, 61, 238)
VIOLET = (126, 92, 206, 235)
BLACK = (22, 27, 32, 238)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
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


def _printed_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill=INK,
    width: int | None = None,
    line_gap: int = 5,
    overprint: bool = False,
) -> int:
    x, y = xy
    for raw in text.split("\n"):
        lines = _wrap(draw, raw, font, width) if width else [raw]
        for line in lines:
            if overprint:
                draw.text((x + 1, y), line, font=font, fill=(16, 151, 165, 12))
                draw.text((x - 1, y + 1), line, font=font, fill=(218, 54, 36, 10))
            draw.text((x, y), line, font=font, fill=fill)
            y += int(font.size * 1.22) + line_gap
    return y


def _ticket(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    *,
    outline=TEAL,
    fill=PAPER_DENSE,
    accent: tuple[int, int, int, int] | None = None,
    radius: int = 5,
    width: int = 2,
) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x + 2, y + 3, x + w + 2, y + h + 3), radius=radius, fill=(0, 0, 0, 55))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=outline, width=width)
    if accent:
        draw.rectangle((x, y, x + 10, y + h), fill=accent)
    draw.line((x + 18, y + h - 12, x + w - 22, y + h - 12), fill=(47, 52, 45, 65), width=1)


def _badge(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str, color, font=TINY) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=color, outline=(255, 246, 210, 150), width=1)
    _printed_text(draw, (x + 9, y + 4), text, font, WHITE, w - 18, overprint=False)


def _draw_left_cards(draw: ImageDraw.ImageDraw) -> None:
    cards = [
        {
            "rect": (184, 186, 324, 118),
            "title": "51 区外围公路",
            "meta": "白色调查 · 耗时 2天 · 探索4 / 生存2",
            "accent": RED,
            "badge": None,
        },
        {
            "rect": (184, 354, 324, 118),
            "title": "罗斯威尔档案残页",
            "meta": "线索调查 · 耗时 1天 · 调查后生成任务",
            "accent": BLUE,
            "badge": "线索",
        },
        {
            "rect": (184, 528, 324, 118),
            "title": "突发：雷达异常光点",
            "meta": "红色截稿 · 剩 4天 · 对手骰3",
            "accent": RED,
            "badge": "截稿",
        },
        {
            "rect": (184, 704, 324, 118),
            "title": "M330 未班车空白段",
            "meta": "深度调查链 · 地图点选当前环 1/4",
            "accent": CYAN,
            "badge": "续 1/4",
            "selected": True,
        },
    ]

    for card in cards:
        x, y, w, h = card["rect"]
        if card.get("selected"):
            draw.rounded_rectangle((x - 8, y - 8, x + w + 8, y + h + 8), radius=5, outline=GOLD, width=3)
            draw.rectangle((x - 3, y + 12, x + 4, y + h - 14), fill=VIOLET)
        _printed_text(draw, (x + 32, y + 30), str(card["title"]), BODY_BOLD, INK, 222)
        _printed_text(draw, (x + 32, y + 62), str(card["meta"]), SMALL, INK, 242)
        if card.get("badge"):
            _badge(draw, (x + w - 92, y + 26, 72, 25), str(card["badge"]), card["accent"], MICRO)

    _ticket(draw, (150, 842, 350, 58), outline=(102, 119, 116, 190), fill=(18, 31, 42, 218), radius=4, width=1)
    _printed_text(draw, (168, 854), "已派遣 · 执行中：51区、雷达异常", SMALL, WHITE, 310, overprint=False)
    _printed_text(draw, (168, 880), "明日到期：雷达异常 · 可展开查看", MICRO, (216, 223, 214, 255), 310, overprint=False)


def _draw_map_labels(draw: ImageDraw.ImageDraw) -> None:
    # Coordinates align with the blank paper labels in the approved v3 map.
    labels = [
        ((904, 286, 122, 46), "雷达站", "截稿", RED),
        ((744, 420, 130, 48), "51区公路", "调查", RED),
        ((804, 592, 132, 48), "残页线索", "线索", BLUE),
        ((642, 714, 132, 48), "异常光点", "截稿", RED),
        ((1134, 502, 154, 48), "M330 空白段", "1/4", VIOLET),
        ((1004, 708, 154, 48), "下一环？", "2/4", BLACK),
    ]

    draw.line((1128, 524, 1016, 692), fill=(126, 92, 206, 190), width=4)
    draw.ellipse((1090, 486, 1166, 562), outline=GOLD, width=3)
    draw.ellipse((982, 658, 1050, 726), outline=(214, 158, 61, 145), width=2)

    for rect, title, stage, color in labels:
        x, y, w, h = rect
        if title == "M330 空白段":
            draw.rounded_rectangle((x - 5, y - 5, x + w + 5, y + h + 5), radius=5, outline=GOLD, width=2)
        _badge(draw, (x + 8, y + 11, 42, 19), stage, color, MICRO)
        title_fill = INK if color != BLACK else WHITE
        _printed_text(draw, (x + 58, y + 10), title, TINY, title_fill, w - 64, line_gap=1)
        if title == "M330 空白段" or color == BLACK:
            _printed_text(
                draw,
                (x + 58, y + 28),
                "可派遣" if color != BLACK else "未揭示",
                MICRO,
                (92, 72, 30, 255) if color != BLACK else (221, 222, 214, 255),
                w - 64,
                line_gap=1,
            )


def _draw_right_detail(draw: ImageDraw.ImageDraw) -> None:
    _printed_text(draw, (1418, 220), "M330 未班车空白段", H2, INK, 350)
    _printed_text(draw, (1418, 250), "北美禁区 / 深度调查链", SMALL, MUTED, 320)

    body = (
        "一段车载录音缺了三秒，乘客口供互相矛盾，"
        "但都指向同一站。\n"
        "目标：找出缺失三秒对应的站点记录。\n"
        "需求：察 / 诡 / 理 · 耗时 2天"
    )
    _printed_text(draw, (1418, 338), body, BODY, INK, 350, line_gap=7)

    _ticket(draw, (1408, 568, 320, 42), outline=VIOLET, fill=(250, 243, 226, 238), accent=VIOLET, radius=4, width=2)
    _printed_text(draw, (1426, 579), "深度调查 · 当前环 1/4", SMALL_BOLD, (78, 54, 145, 255), 270)

    rows = [
        ((1410, 626), "成功后揭示下一环；失败保留线索。", VIOLET),
        ((1410, 674), "可带回：录音 / 证词", CYAN),
        ((1410, 722), "风险：凶险，可能触发误导线索", RED),
    ]
    for (x, y), text, color in rows:
        draw.rectangle((x, y + 5, x + 13, y + 18), fill=color)
        _printed_text(draw, (x + 24, y), text, SMALL, INK, 280)

    _ticket(draw, (1408, 760, 316, 36), outline=GOLD, fill=(246, 238, 211, 226), radius=4, width=2)
    _printed_text(draw, (1424, 769), "签批不扣天数；派遣后预计占用 2 天。", TINY, INK, 280)

    _printed_text(draw, (1488, 832), "进入派遣签批", H1, INK, 238, overprint=False)


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
    _printed_text(draw, (x + 34, y + 13), "推进一天", BODY_BOLD, WHITE, overprint=False)
    _printed_text(draw, (x + 36, y + 40), "DAY +1", MICRO, (214, 158, 61, 255), overprint=False)


def _draw_bottom_receipts(draw: ImageDraw.ImageDraw) -> None:
    _printed_text(draw, (352, 954), "探索周 余 4天 · 北美禁区 · 已选 M330", SMALL, INK, 300)
    _printed_text(draw, (680, 954), "地区事件：军方封锁 · 本区对手骰 +1", SMALL, INK, 320)
    _printed_text(draw, (1014, 954), "执行中 2 / 到期 1", SMALL_BOLD, INK, 130)
    _printed_text(draw, (352, 986), "当前回执：签批不消耗天数，派遣后占用 2 天。", TINY, MUTED, 610)
    _draw_day_button(draw)


def build() -> Image.Image:
    image = Image.open(SOURCE).convert("RGBA").resize(CANVAS)
    draw = ImageDraw.Draw(image, "RGBA")
    _draw_left_cards(draw)
    _draw_map_labels(draw)
    _draw_right_detail(draw)
    _draw_bottom_receipts(draw)
    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = build()
    image.save(OUT_FULL)
    image.crop((1338, 120, 1860, 930)).save(OUT_RIGHT_CROP)
    image.crop((1118, 918, 1348, 1040)).save(OUT_BOTTOM_CROP)
    print(OUT_DIR)
    print(OUT_FULL.name)
    print(OUT_RIGHT_CROP.name)
    print(OUT_BOTTOM_CROP.name)


if __name__ == "__main__":
    main()
