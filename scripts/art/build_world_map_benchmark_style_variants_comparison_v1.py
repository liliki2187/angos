from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
SOURCE_DIR = ROOT / "image_gen/2026-08-18/world-map-benchmark-style-variants-v1"
OUTPUT = SOURCE_DIR / "07-three-benchmark-style-variants-comparison-1920x520.png"

SOURCES = (
    ("A  连续桌面 · 巨幅地图母版", "02-a-giant-map-master-1920x1080.png", "地图底稿统领三栏 / 功能最稳"),
    ("B  扁平纸雕 · 综合色周刊拼贴", "04-b-flat-cut-paper-collage-1920x1080.png", "最贴标杆图形语言 / 风格最大胆"),
    ("C  夜班桌景 · 综合色灯光静物", "06-c-night-desk-light-islands-1920x1080.png", "场景氛围最强 / 防止回流旧结构"),
)

FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def main() -> None:
    canvas = Image.new("RGB", (1920, 520), (10, 23, 31))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 16), "WORLD MAP / CLEAN LOW-POLY WEEKLY / 三方向并排", font=font(24, True), fill=(226, 220, 204))

    panel_width = 620
    image_width = 604
    image_height = 340
    for index, (title, filename, note) in enumerate(SOURCES):
        x = 16 + panel_width * index
        draw.text((x + 8, 58), title, font=font(19, True), fill=(224, 217, 198))
        source = Image.open(SOURCE_DIR / filename).convert("RGB")
        source = source.resize((image_width, image_height), Image.Resampling.LANCZOS)
        canvas.paste(source, (x + 8, 92))
        draw.rectangle((x + 7, 91, x + 8 + image_width, 92 + image_height), outline=(118, 128, 116), width=2)
        draw.text((x + 8, 447), note, font=font(15), fill=(159, 170, 158))

    draw.text((24, 488), "三张均为美术方向探索；功能合同继续冻结，暂不进入 Godot / atlas / manifest。", font=font(14), fill=(132, 144, 142))
    canvas.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
