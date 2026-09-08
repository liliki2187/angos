from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"D:\angos")
OUT_DIR = ROOT / "image_gen/2026-08-18/world-map-pasteup-abstraction-gap-board-v1"
CURRENT = ROOT / "image_gen/2026-08-18/world-map-pasteup-internal-variants-v1/02-color-separation-proof-1920x1080.png"
OUT = OUT_DIR / "01-benchmark-vs-current-abstraction-grayness-gap-board-1920x1080.png"

BG = "#071720"
PANEL = "#0d2530"
PANEL_2 = "#102d38"
INK = "#eee8d8"
MUTED = "#a9b2ad"
CYAN = "#6ba3aa"
MUSTARD = "#c2a052"
RUST = "#c35d47"
OLIVE = "#7f895b"
LINE = "#35505a"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


F_TITLE = font(34, True)
F_SUBTITLE = font(22, True)
F_BODY = font(18, False)
F_BODY_B = font(18, True)
F_SMALL = font(15, False)
F_NUM = font(19, True)


def rounded_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str = PANEL) -> None:
    draw.rounded_rectangle(box, radius=12, fill=fill, outline=LINE, width=2)


def contain(image: Image.Image, box: tuple[int, int, int, int], fill: str = "#08151b") -> tuple[Image.Image, tuple[int, int]]:
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    fitted = ImageOps.contain(image.convert("RGB"), (width, height), Image.Resampling.LANCZOS)
    plate = Image.new("RGB", (width, height), fill)
    offset = ((width - fitted.width) // 2, (height - fitted.height) // 2)
    plate.paste(fitted, offset)
    return plate, (x0, y0)


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        line = ""
        for char in paragraph:
            trial = line + char
            if draw.textbbox((0, 0), trial, font=face)[2] <= width or not line:
                line = trial
            else:
                lines.append(line)
                line = char
        if line:
            lines.append(line)
    return lines


def text_block(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    face: ImageFont.FreeTypeFont,
    fill: str,
    width: int,
    leading: int = 8,
) -> int:
    x, y = xy
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        bbox = draw.textbbox((x, y), line or "国", font=face)
        y += (bbox[3] - bbox[1]) + leading
    return y


def badge(draw: ImageDraw.ImageDraw, center: tuple[int, int], number: str) -> None:
    x, y = center
    draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=RUST, outline=INK, width=2)
    bbox = draw.textbbox((0, 0), number, font=F_NUM)
    draw.text((x - (bbox[2] - bbox[0]) / 2, y - (bbox[3] - bbox[1]) / 2 - 2), number, font=F_NUM, fill=INK)


def paste_reference(canvas: Image.Image, draw: ImageDraw.ImageDraw, filename: str, box: tuple[int, int, int, int], caption: str) -> None:
    image = Image.open(OUT_DIR / filename)
    plate, pos = contain(image, box)
    canvas.paste(plate, pos)
    draw.rectangle(box, outline="#62777c", width=2)
    draw.rectangle((box[0], box[3] - 28, box[2], box[3]), fill="#061116aa")
    draw.text((box[0] + 10, box[3] - 25), caption, font=F_SMALL, fill=INK)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rectangle((0, 0, 1920, 88), fill="#06121a")
    draw.text((34, 19), "世界地图组件差距板 01｜粗概括 vs 过度精制", font=F_TITLE, fill=INK)
    draw.text((1370, 33), "DIAGNOSTIC ONLY · 非生图目标", font=F_SMALL, fill=MUTED)

    rounded_panel(draw, (24, 104, 844, 1048), PANEL)
    rounded_panel(draw, (864, 104, 1896, 1048), PANEL_2)
    draw.text((46, 122), "BENCHMARK｜高完成度的粗概括", font=F_SUBTITLE, fill=MUSTARD)
    draw.text((886, 122), "CURRENT 02｜把微工艺全部做完", font=F_SUBTITLE, fill=RUST)

    paste_reference(canvas, draw, "reference-crop-01-masthead-folder.png", (46, 162, 427, 350), "① 一个主轮廓＋一处切角")
    paste_reference(canvas, draw, "reference-crop-02-folder-family.png", (442, 162, 822, 350), "② 色面区分，内部线稿很少")
    paste_reference(canvas, draw, "reference-crop-03-weekly-folder.png", (46, 366, 427, 620), "③ 纸层由一个主轮廓统领")
    paste_reference(canvas, draw, "reference-crop-04-documents.png", (442, 366, 822, 620), "④ 大形统一，小内容不抢轮廓")

    draw.line((46, 646, 822, 646), fill=LINE, width=2)
    draw.text((46, 664), "标杆把完成度放在哪里", font=F_BODY_B, fill=INK)
    left_notes = [
        "• 先完成大轮廓：宽、钝、略有手工裁切感",
        "• 每件只留 3–6 个宽明度/综合色块",
        "• 一张背纸或一件夹具就能说明接触关系",
        "• 蓝、青、橄榄、芥末和暖纸共享冷石板灰底",
    ]
    y = 704
    for note in left_notes:
        y = text_block(draw, (52, y), note, F_BODY, INK, 748, 8) + 4

    draw.rounded_rectangle((46, 890, 822, 1024), radius=8, fill="#0a1b23", outline="#5e6a58", width=2)
    draw.text((64, 907), "目标不是“画糙”", font=F_BODY_B, fill=OLIVE)
    text_block(
        draw,
        (64, 944),
        "把精度从边框、五金、微型版号和逐层阴影，转移到大形、综合色与压叠关系。",
        F_BODY,
        INK,
        728,
        7,
    )

    current = Image.open(CURRENT).convert("RGB")
    current_box = (886, 162, 1874, 718)
    plate, pos = contain(current, current_box)
    canvas.paste(plate, pos)
    draw.rectangle(current_box, outline="#6c7e82", width=2)

    scale = (current_box[2] - current_box[0]) / 1920.0
    ox, oy = current_box[0], current_box[1]

    def mark(src_box: tuple[int, int, int, int], number: str) -> None:
        x, y, w, h = src_box
        box = (ox + int(x * scale), oy + int(y * scale), ox + int((x + w) * scale), oy + int((y + h) * scale))
        draw.rectangle(box, outline=RUST, width=4)
        badge(draw, (box[0] + 18, box[1] + 18), number)

    mark((22, 154, 508, 720), "1")
    mark((542, 153, 855, 720), "2")
    mark((1410, 124, 472, 812), "3")
    mark((29, 875, 472, 174), "4")
    mark((1440, 36, 430, 85), "5")

    draw.text((886, 740), "超量位置", font=F_BODY_B, fill=INK)
    current_notes = [
        ("1", "左卡三次重复完整壳、双框、独立底栏、重复状态装饰和独立投影；保留一个显式状态位。"),
        ("2", "地图仍是密三角＋完整套印描边；应先读 3–6 个主质量块，同时保持轮廓与定位可辨。"),
        ("3", "右稿同时拥有纸堆、夹子、色样轨、准星、细框与版号；CTA、Disclosure 和动态槽冻结不减。"),
        ("4", "Schedule 的环装、铆钉、条码、内框都完成，读成可点击控件；它必须保持 passive。"),
        ("5", "品牌锁组后又接工具条、准星与条码，重新形成机构状态栏。"),
    ]
    y = 776
    for n, note in current_notes:
        badge(draw, (902, y + 10), n)
        y = text_block(draw, (930, y), note, F_SMALL, INK, 920, 5) + 10

    draw.rounded_rectangle((886, 958, 1874, 1032), radius=8, fill="#0a1b23", outline="#586c73", width=2)
    draw.text((902, 969), "冻结不减：三栏｜3 张等高卡｜69:44｜selected/locked｜地图定位｜右稿动态槽｜Disclosure｜CTA｜Schedule passive｜功能面 0°", font=font(13, False), fill=INK)
    draw.text((902, 1000), "主动降级：可见载体层级 ≤2｜每卡状态主承载位 1｜背纸 ≤1｜右稿夹具 1｜每洲 3–6 个主质量块且定位可辨", font=font(13, False), fill=CYAN)

    # 综合色灰度关系示意。这里只表达方向，不作为正式 token。
    draw.text((886, 927), "综合色：各色保留色相，仅降低色度并共享冷石板灰；不加 sepia / 泛黄 / 污损（方向示意，非正式色值）", font=font(14, False), fill=MUTED)
    swatches = [
        ("#235e8c", "#4a6472"),
        ("#4b9bab", "#637c7f"),
        ("#6f7c3d", "#74765f"),
        ("#c49327", "#a68d57"),
        ("#eadfc9", "#cbc7ba"),
    ]
    sx = 1442
    for current_color, target_color in swatches:
        draw.rectangle((sx, 930, sx + 30, 954), fill=current_color)
        draw.polygon([(sx + 35, 942), (sx + 43, 936), (sx + 43, 948)], fill=MUTED)
        draw.rectangle((sx + 49, 930, sx + 79, 954), fill=target_color)
        sx += 86

    canvas.save(OUT, "PNG")
    print(OUT)


if __name__ == "__main__":
    main()
