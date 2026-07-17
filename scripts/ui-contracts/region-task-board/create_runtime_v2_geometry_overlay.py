from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-15-region-task-board-runtime-v2"
SOURCE = SCREENSHOT_DIR / "02-region-m330-selected.png"
OUTPUT = SCREENSHOT_DIR / "06-region-runtime-v2-geometry-overlay.png"

REGIONS = [
    ("HUD 1920×72", (0, 0, 1919, 71), "#58b4d4"),
    ("EVENT INDEX 380x804", (24, 96, 403, 899), "#f1b85b"),
    ("MAP STAGE 1040x804", (420, 96, 1459, 899), "#55d7c0"),
    ("DOSSIER 412x960", (1484, 96, 1895, 1055), "#e27ba9"),
    ("SCHEDULE 1436x140", (24, 916, 1459, 1055), "#e5d65b"),
    ("DISPATCH CTA 356x112", (1512, 916, 1867, 1027), "#9acb55"),
    ("SUMMARY SAFE ZONE", (1508, 244, 1871, 547), "#ff765e"),
]


def main() -> None:
    with Image.open(SOURCE) as source:
        image = source.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.load_default(size=18)
    for label, rect, color in REGIONS:
        draw.rectangle(rect, outline=color, width=4)
        left, top, _, _ = rect
        box = draw.textbbox((0, 0), label, font=font)
        label_width = box[2] - box[0] + 16
        label_height = box[3] - box[1] + 10
        draw.rectangle((left + 6, top + 6, left + 6 + label_width, top + 6 + label_height), fill=(7, 29, 46, 225))
        draw.text((left + 14, top + 10), label, fill=color, font=font)
    for x in (24, 404, 420, 1460, 1484, 1896):
        draw.line((x, 0, x, 1080), fill=(240, 240, 220, 90), width=1)
    for y in (72, 96, 900, 916, 1056):
        draw.line((0, y, 1920, y), fill=(240, 240, 220, 90), width=1)
    Image.alpha_composite(image, overlay).convert("RGB").save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
