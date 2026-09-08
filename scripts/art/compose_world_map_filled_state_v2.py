from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen" / "2026-08-03" / "world-map-a-filled-state-visual-target-v2"
SOURCE = OUT / "02-world-map-a-mother-art-base-v2.png"
FINAL = OUT / "03-world-map-a-real-content-v2.png"
QUARTER = OUT / "04-world-map-a-real-content-v2-25pct.png"
COMPARE = OUT / "05-world-map-a-v1-reference-vs-v2.png"
REFERENCE = ROOT / "image_gen" / "2026-07-28" / "world-map-colorways-v1" / "01-a-night-slate-blue.png"

FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

INK = "#25312e"
INK_SOFT = "#58615a"
PAPER = "#d9cfb9"
PAPER_LIGHT = "#e1d8c5"
RUST = "#93462f"
CREAM = "#eee5d1"
OLIVE = "#53613a"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int,
          fill: str = INK, bold: bool = False, anchor: str | None = None) -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def center(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str,
           size: int, fill: str = INK, bold: bool = True) -> None:
    x0, y0, x1, y1 = box
    draw.text(((x0 + x1) // 2, (y0 + y1) // 2), value,
              font=font(size, bold), fill=fill, anchor="mm")


def soft_patch(image: Image.Image, box: tuple[int, int, int, int], color: str,
               alpha: int = 236) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    patch = ImageDraw.Draw(overlay)
    patch.rectangle(box, fill=(*ImageColor.getrgb(color), alpha))
    image.paste(Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB"))


def main() -> None:
    # Resize the model-native 16:9 result to the project review canvas.
    image = Image.open(SOURCE).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)

    # Left staggered clippings: use the existing torn-paper text areas, not new UI fields.
    draw.rectangle((350, 235, 446, 299), fill=PAPER_LIGHT)
    center(draw, (350, 235, 446, 264), "北美禁区带", 14)
    center(draw, (350, 264, 446, 284), "已选中", 12, fill="#315f7b")
    center(draw, (350, 284, 446, 299), "红线升温", 10, fill=RUST)

    draw.rectangle((350, 505, 446, 566), fill=PAPER_LIGHT)
    center(draw, (350, 505, 446, 536), "东亚神秘地带", 12)
    center(draw, (350, 537, 446, 566), "锁定", 12, fill=OLIVE)

    draw.rectangle((350, 747, 446, 807), fill=PAPER_LIGHT)
    center(draw, (350, 747, 446, 778), "太平洋失航带", 11)
    center(draw, (350, 779, 446, 807), "锁定", 12, fill=OLIVE)

    # The dark map remains the visual subject; labels are confined to the generated torn tabs.
    center(draw, (621, 326, 731, 367), "北美禁区带", 14)
    center(draw, (1041, 428, 1162, 472), "东亚神秘地带", 13)
    center(draw, (1248, 602, 1371, 646), "太平洋失航带", 12)

    # Right continuous dossier: erase only placeholder print lines behind exact copy.
    draw.rectangle((1584, 129, 1788, 178), fill="#ddd4c1")
    label(draw, (1594, 138), "北美禁区带", 24, bold=True)
    draw.rectangle((1794, 154, 1864, 204), fill=RUST)
    center(draw, (1794, 154, 1864, 204), "红线\n升温", 13, fill=CREAM)

    draw.rectangle((1441, 543, 1842, 617), fill="#ddd4c1")
    label(draw, (1448, 550), "都市传说与军事封锁交叠。", 18, bold=True)
    label(draw, (1448, 584), "红线稿需在 7 天内处理。", 15, fill=RUST)

    draw.rectangle((1410, 699, 1852, 778), fill="#d7cfbc", outline="#86826f", width=1)
    label(draw, (1424, 716), "任务情报", 18, bold=True)
    label(draw, (1538, 719), "限时 1 · 线索 2 · 深链 1", 14, fill=INK_SOFT)
    label(draw, (1817, 708), "＋", 25, bold=True)
    label(draw, (1424, 749), "当前为折叠摘要；进入后再选择具体任务", 12, fill=INK_SOFT)

    # The only solid action remains attached inside the dossier.
    label(draw, (1624, 838), "进入地区任务台  →", 25, fill=CREAM, bold=True, anchor="mm")
    label(draw, (1624, 874), "本次进入：0 天", 12, fill="#d9d4bd", anchor="mm")

    # Passive time device receipt.
    draw.rectangle((119, 1001, 259, 1060), fill="#ddd5c2")
    center(draw, (119, 1001, 259, 1032), "本屏操作：0 天", 13)
    center(draw, (119, 1033, 259, 1060), "仅选择与进入", 10, fill=INK_SOFT, bold=False)

    image.save(FINAL, quality=96)
    image.resize((480, 270), Image.Resampling.LANCZOS).save(QUARTER, quality=94)

    reference = Image.open(REFERENCE).convert("RGB").resize((960, 540), Image.Resampling.LANCZOS)
    current = image.resize((960, 540), Image.Resampling.LANCZOS)
    compare = Image.new("RGB", (1920, 540), "#071722")
    compare.paste(reference, (0, 0))
    compare.paste(current, (960, 0))
    compare.save(COMPARE, quality=95)


if __name__ == "__main__":
    # Imported here so the file-level palette stays easy to audit.
    from PIL import ImageColor

    main()
