from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen" / "2026-08-03" / "world-map-a-filled-state-visual-target-v1"
SOURCE = OUT / "01-world-map-a-filled-state-art-base-v1.png"
FINAL = OUT / "02-world-map-a-filled-state-real-content-v1.png"
QUARTER = OUT / "03-world-map-a-filled-state-real-content-v1-25pct.png"

FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

INK = "#27312c"
INK_SOFT = "#53605a"
PAPER = "#ddd7c5"
PAPER_LIGHT = "#e7e1d1"
COBALT = "#315d78"
RUST = "#934f34"
OLIVE = "#41492b"
CREAM = "#eee7d5"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int,
         fill: str = INK, bold: bool = False, anchor: str | None = None) -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str,
             size: int, fill: str, bold: bool = True) -> None:
    x0, y0, x1, y1 = box
    draw.text(((x0 + x1) // 2, (y0 + y1) // 2), value,
              font=font(size, bold), fill=fill, anchor="mm")


def paper_field(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
                fill: str = PAPER_LIGHT, outline: str = "#777564") -> None:
    draw.rectangle(box, fill=fill, outline=outline, width=1)


def main() -> None:
    image = Image.open(SOURCE).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)

    # Left region selectors: exact live state, kept within the generated card carriers.
    text(draw, (58, 280), "北美禁区带", 21, bold=True)
    text(draw, (58, 307), "红线升温 · 已选中", 13, fill=RUST, bold=True)

    text(draw, (58, 560), "东亚神秘地带", 20, bold=True)
    text(draw, (58, 586), "锁定 · 声望≥55 或「罗斯威尔残页」", 11, fill=INK_SOFT)

    text(draw, (58, 819), "太平洋失航带", 20, bold=True)
    text(draw, (58, 847), "锁定 · 北美追踪第2环 或 线人许可", 11, fill=INK_SOFT)

    # Passive DAY counter: correct the generated placeholder from 1 day to 0 days.
    paper_field(draw, (118, 972, 302, 1021), fill="#ded7c4", outline="#7e7765")
    centered(draw, (118, 972, 302, 1002), "本屏耗时 0 天", 16, INK, True)
    centered(draw, (118, 1000, 302, 1021), "选择与进入均不推进日期", 10, INK_SOFT, False)

    # Functional map labels: one consistent pin language, no decorative extra hit targets.
    centered(draw, (672, 313, 806, 355), "北美禁区带", 15, INK)
    centered(draw, (1206, 342, 1325, 382), "东亚神秘地带", 13, INK_SOFT)
    centered(draw, (1258, 524, 1340, 582), "太平洋\n失航带", 11, INK_SOFT)

    # Read-only selected-region receipt below the map.
    text(draw, (812, 781), "北美禁区带", 25, bold=True)
    text(draw, (812, 833), "红线稿 · 剩余 7 天", 16, fill=RUST, bold=True)
    text(draw, (812, 876), "进入地区任务台：0 天", 15, fill=INK_SOFT)
    text(draw, (812, 921), "都市传说与军事封锁交叠。", 15, fill=INK)
    text(draw, (812, 947), "红线稿需在 7 天内处理。", 15, fill=INK)

    draw.rectangle((1150, 766, 1307, 817), fill=COBALT)
    centered(draw, (1150, 766, 1307, 817), "已选择", 17, CREAM)
    draw.rectangle((1150, 824, 1307, 875), fill=RUST)
    centered(draw, (1150, 824, 1307, 875), "红线升温", 17, CREAM)

    # Right dossier: dynamic region identity and warning must be explicit and separate.
    text(draw, (1428, 174), "北美禁区带", 32, bold=True)
    text(draw, (1428, 216), "都市异闻 / 军事封锁", 14, fill=INK_SOFT)
    draw.rectangle((1764, 157, 1864, 239), fill=RUST)
    centered(draw, (1764, 157, 1864, 239), "红线\n升温", 18, CREAM)

    text(draw, (1428, 599), "都市传说与军事封锁交叠。", 19, bold=True)
    text(draw, (1428, 632), "红线稿需在 7 天内处理。", 16, fill=INK_SOFT)
    text(draw, (1428, 704), "当前地区可进入；选中本身不消耗时间。", 15, fill=INK)
    text(draw, (1428, 738), "风险不是封锁：它要求你尽快处理。", 14, fill=RUST)

    # Secondary disclosure remains a lightweight row; CTA is the only solid action.
    draw.rectangle((1423, 808, 1861, 862), fill="#d8d1be")
    draw.line((1423, 861, 1861, 861), fill="#928d7b", width=1)
    text(draw, (1430, 822), "任务情报", 18, bold=True)
    text(draw, (1544, 824), "限时 1 · 线索 2 · 深链 1", 15, fill=INK_SOFT)
    text(draw, (1826, 820), "＋", 25, fill=INK, bold=True)

    draw.rectangle((1392, 922, 1901, 1054), fill=OLIVE, outline="#b8b096", width=2)
    centered(draw, (1392, 922, 1901, 1054), "进入地区任务台  →", 28, CREAM)

    image.save(FINAL, quality=96)
    image.resize((480, 270), Image.Resampling.LANCZOS).save(QUARTER, quality=94)


if __name__ == "__main__":
    main()
