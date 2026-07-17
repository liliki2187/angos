from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "image_gen/2026-07-16/region-task-pin-slice"
OUT_DIR = SOURCE_DIR / "prepared"
MAP_SOURCE = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/region_map_clean_lowpoly_selected_v1.png"


def alpha_bbox(image: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("No opaque subject found")
    return bbox


def fit_subject(
    source: Image.Image,
    canvas_size: tuple[int, int],
    inset: tuple[int, int, int, int],
) -> tuple[Image.Image, dict[str, object]]:
    bbox = alpha_bbox(source)
    subject = source.crop(bbox)
    left, top, right, bottom = inset
    usable_w = canvas_size[0] - left - right
    usable_h = canvas_size[1] - top - bottom
    scale = min(usable_w / subject.width, usable_h / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    x = left + (usable_w - size[0]) // 2
    y = top + (usable_h - size[1]) // 2
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(subject, (x, y))
    return canvas, {
        "source_bbox": bbox,
        "canvas_size": canvas_size,
        "inset": inset,
        "placed_bbox": [x, y, x + size[0], y + size[1]],
        "scale": scale,
    }


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    image = Image.new("RGB", size, (42, 50, 55))
    draw = ImageDraw.Draw(image)
    colors = ((44, 53, 58), (66, 75, 79))
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            draw.rectangle(
                (x, y, min(x + cell, size[0]), min(y + cell, size[1])),
                fill=colors[(x // cell + y // cell) % 2],
            )
    return image


def paste_center(base: Image.Image, sprite: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    x = x0 + (x1 - x0 - sprite.width) // 2
    y = y0 + (y1 - y0 - sprite.height) // 2
    base.paste(sprite, (x, y), sprite)


def alpha_metrics(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    total = image.width * image.height
    transparent = histogram[0]
    opaque = histogram[255]
    partial = total - transparent - opaque
    key_like_visible = 0
    for red, green, blue, alpha_value in image.getdata():
        if alpha_value > 0 and red > 180 and blue > 180 and green < 140:
            key_like_visible += 1
    return {
        "size": [image.width, image.height],
        "bbox_alpha_gt_8": list(alpha_bbox(image)),
        "transparent_pixels": transparent,
        "partially_transparent_pixels": partial,
        "opaque_pixels": opaque,
        "transparent_ratio": round(transparent / total, 6),
        "partial_ratio": round(partial / total, 6),
        "visible_magenta_key_like_pixels": key_like_visible,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pin_source = Image.open(SOURCE_DIR / "rt-task-pin-shell-v2-alpha.png").convert("RGBA")
    label_source = Image.open(SOURCE_DIR / "rt-task-pin-label-v2-alpha.png").convert("RGBA")

    pin_3x, pin_fit = fit_subject(pin_source, (192, 240), (18, 18, 18, 18))
    label_2x, label_fit = fit_subject(label_source, (400, 144), (16, 12, 16, 12))
    pin_runtime = pin_3x.resize((64, 80), Image.Resampling.LANCZOS)
    label_runtime = label_2x.resize((200, 72), Image.Resampling.LANCZOS)

    pin_3x.save(OUT_DIR / "rt-task-pin-shell-v2-3x.png")
    label_2x.save(OUT_DIR / "rt-task-pin-label-v2-2x.png")
    pin_runtime.save(OUT_DIR / "rt-task-pin-shell-v2-runtime-64x80.png")
    label_runtime.save(OUT_DIR / "rt-task-pin-label-v2-runtime-200x72.png")

    board = checker((1400, 800), 20).convert("RGBA")
    draw = ImageDraw.Draw(board)
    title_font = font(28)
    label_font = font(22)
    white = (232, 227, 211, 255)
    muted = (155, 169, 164, 255)
    draw.text((40, 28), "REGION TASK PIN SLICE V2 / ALPHA & RUNTIME QA", fill=white, font=title_font)
    draw.text((40, 72), "Generated art; programmatic layout is QA only", fill=muted, font=label_font)

    panels = [
        ((40, 120, 440, 700), "PIN 3x / 192x240", pin_3x.resize((384, 480), Image.Resampling.NEAREST)),
        ((480, 120, 1360, 360), "LABEL 2x / 400x144", label_2x.resize((800, 288), Image.Resampling.NEAREST)),
        ((480, 410, 1360, 700), "RUNTIME SIZE / 64x80 + 200x72", None),
    ]
    for panel, text_value, sprite in panels:
        draw.rounded_rectangle(panel, radius=10, fill=(10, 31, 42, 225), outline=(161, 156, 126, 255), width=2)
        draw.text((panel[0] + 18, panel[1] + 16), text_value, fill=white, font=label_font)
        if sprite is not None:
            paste_center(board, sprite, (panel[0] + 10, panel[1] + 55, panel[2] - 10, panel[3] - 10))

    runtime_box = panels[2][0]
    pin_4x = pin_runtime.resize((256, 320), Image.Resampling.NEAREST)
    label_4x = label_runtime.resize((800, 288), Image.Resampling.NEAREST)
    paste_center(board, pin_4x, (runtime_box[0] + 10, runtime_box[1] + 45, runtime_box[0] + 310, runtime_box[3] - 10))
    paste_center(board, label_4x, (runtime_box[0] + 300, runtime_box[1] + 55, runtime_box[2] - 15, runtime_box[3] - 10))
    board.save(OUT_DIR / "region-task-pin-slice-v2-alpha-runtime-qa.png")

    map_preview = Image.open(MAP_SOURCE).convert("RGB").resize((1040, 804), Image.Resampling.LANCZOS).convert("RGBA")
    map_draw = ImageDraw.Draw(map_preview)
    pin_xy = (606, 496)
    label_xy = (664, 488)
    # The ring, glyph and text below are runtime placeholders used only to verify carrier geometry.
    map_draw.ellipse((pin_xy[0] - 6, pin_xy[1] - 6, pin_xy[0] + 70, pin_xy[1] + 70), outline=(12, 35, 47, 255), width=5)
    map_draw.ellipse((pin_xy[0] - 2, pin_xy[1] - 2, pin_xy[0] + 66, pin_xy[1] + 66), outline=(169, 177, 92, 255), width=3)
    map_preview.alpha_composite(pin_runtime, pin_xy)
    map_preview.alpha_composite(label_runtime, label_xy)
    map_draw = ImageDraw.Draw(map_preview)
    glyph_center = (pin_xy[0] + 32, pin_xy[1] + 29)
    map_draw.ellipse(
        (glyph_center[0] - 10, glyph_center[1] - 6, glyph_center[0] + 10, glyph_center[1] + 6),
        outline=(25, 43, 48, 255),
        width=2,
    )
    map_draw.ellipse(
        (glyph_center[0] - 3, glyph_center[1] - 3, glyph_center[0] + 3, glyph_center[1] + 3),
        fill=(25, 43, 48, 255),
    )
    map_draw.text((label_xy[0] + 14, label_xy[1] + 7), "M330 末班车空白段", fill=(22, 38, 42, 255), font=font(17))
    map_draw.text((label_xy[0] + 14, label_xy[1] + 38), "追踪线索 · 2天", fill=(50, 72, 72, 255), font=font(14))
    map_preview.save(OUT_DIR / "region-task-pin-slice-v2-map-filled-preview.png")

    metrics = {
        "artifact_type": "generated_asset_with_programmatic_crop_resize_and_qa_layout",
        "pin_source": alpha_metrics(pin_source),
        "pin_3x": alpha_metrics(pin_3x),
        "pin_fit": pin_fit,
        "label_source": alpha_metrics(label_source),
        "label_2x": alpha_metrics(label_2x),
        "label_fit": label_fit,
        "map_preview_note": "The selected ring, eye placeholder and English text are programmatic QA overlays, not generated production art.",
    }
    (OUT_DIR / "region-task-pin-slice-v2-alpha-metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
