from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_dice_glb_v0_14_assets as v014


REPO = Path(__file__).resolve().parents[1]
STYLE_DIR = REPO / "design" / "art-direction" / "dice-style"
BASE_SHEET = STYLE_DIR / "dice-face-simplified-v0-11-r1-ai-base-sheet.png"
OUT_DIR = STYLE_DIR / "generated-assets" / "dice-icon-placement-v0-15"
BOARD_PATH = STYLE_DIR / "dice-face-icon-placement-options-v0-15-style-board.png"

TILE = 512

FACES = [
    {
        "kind": "reason",
        "label": "理性",
        "value": "+2",
        "cell": [1, 0],
        "body": "#1f7884",
        "text": "#f5e8bd",
        "stroke": "#071a1e",
        "accent": "#d9e5d7",
    },
    {
        "kind": "ghost",
        "label": "鬼迹",
        "value": "!",
        "cell": [1, 1],
        "body": "#171719",
        "text": "#ff6240",
        "stroke": "#0b0706",
        "accent": "#e85b36",
    },
]

STRATEGIES = [
    {
        "id": "a_bottom_watermark",
        "title": "A 下方小水印",
        "note": "v0.14 基准，安全但略居中",
        "score": "可读 4 / 风格 3",
    },
    {
        "id": "b_corner_badge",
        "title": "B 角落小章",
        "note": "图标离开读数区，像实体印记",
        "score": "可读 5 / 风格 4",
    },
    {
        "id": "c_corner_bleed",
        "title": "C 边角半露",
        "note": "更像材质图案，运动中不抢字",
        "score": "可读 5 / 风格 4",
    },
    {
        "id": "d_background_underlay",
        "title": "D 背景底层",
        "note": "图标最大，但必须极低对比",
        "score": "可读 3 / 风格 5",
    },
    {
        "id": "e_top_clean_side_icon",
        "title": "E 顶面无图标",
        "note": "顶面只读规则，图标交给侧面",
        "score": "可读 5 / 风格 2",
    },
]

TITLE_RECT = v014.TITLE_RECT
VALUE_RECT = v014.VALUE_RECT


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return v014.load_font(size, bold=bold)


def rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    return v014.hex_rgba(hex_color, alpha)


def draw_icon(
    draw: ImageDraw.ImageDraw,
    kind: str,
    cx: int,
    cy: int,
    size: int,
    color: tuple[int, int, int, int],
) -> None:
    if kind == "reason":
        v014.draw_head(draw, cx, cy, size, color)
    elif kind == "ghost":
        v014.draw_ghost(draw, cx, cy, size, color)
    elif kind == "explore":
        v014.draw_compass(draw, cx, cy, size, color)
    else:
        v014.draw_eye(draw, cx, cy, size, color)


def draw_value_plate(tile: Image.Image, face: dict[str, object]) -> Image.Image:
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    body = str(face["body"])
    accent = str(face["accent"])
    draw.rounded_rectangle(
        (VALUE_RECT[0] - 12, VALUE_RECT[1] - 8, VALUE_RECT[2] + 12, VALUE_RECT[3] + 8),
        radius=18,
        fill=rgba(body, 154),
    )
    draw.rounded_rectangle(
        (VALUE_RECT[0] - 12, VALUE_RECT[1] - 8, VALUE_RECT[2] + 12, VALUE_RECT[3] + 8),
        radius=18,
        outline=rgba(accent, 210),
        width=4,
    )
    draw.line((132, 150, 380, 150), fill=rgba(accent, 122), width=3)
    return Image.alpha_composite(tile, overlay)


def clean_source_icon_zone(tile: Image.Image, face: dict[str, object]) -> Image.Image:
    """Remove the original large baked icon so placement variants are comparable."""
    body = str(face["body"])
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    if face["kind"] == "ghost":
        dark = "#101012"
        mid = "#191317"
        light = "#241719"
        line = "#8f3527"
    else:
        dark = "#145963"
        mid = "#1d6f78"
        light = "#2a828b"
        line = "#9bd7d7"

    # Opaque fill first; this is a layout exploration board, not the final material tile.
    draw.rounded_rectangle((80, 238, 432, 456), radius=30, fill=rgba(body, 255))
    draw.polygon([(80, 238), (432, 238), (432, 304), (80, 366)], fill=rgba(light, 255))
    draw.polygon([(80, 320), (432, 270), (432, 384), (80, 438)], fill=rgba(mid, 255))
    draw.polygon([(80, 384), (244, 350), (432, 404), (432, 456), (80, 456)], fill=rgba(dark, 255))
    draw.line((122, 424, 390, 424), fill=rgba(line, 96), width=2)
    return Image.alpha_composite(tile, overlay)


def draw_label_text(tile: Image.Image, face: dict[str, object]) -> None:
    draw = ImageDraw.Draw(tile)
    v014.draw_centered_text(
        draw,
        TITLE_RECT,
        str(face["label"]),
        load_font(86),
        str(face["text"]),
        str(face["stroke"]),
        4,
    )
    v014.draw_centered_text(
        draw,
        VALUE_RECT,
        str(face["value"]),
        load_font(100),
        str(face["text"]),
        str(face["stroke"]),
        5,
    )


def apply_strategy(tile: Image.Image, face: dict[str, object], strategy_id: str) -> Image.Image:
    kind = str(face["kind"])
    accent = str(face["accent"])
    body = str(face["body"])
    result = tile.copy()

    if strategy_id == "a_bottom_watermark":
        result = draw_value_plate(result, face)
        overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        alpha = 54 if kind != "ghost" else 68
        draw_icon(draw, kind, 256, 378, 62, rgba(accent, alpha))
        result = Image.alpha_composite(result, overlay)

    elif strategy_id == "b_corner_badge":
        result = draw_value_plate(result, face)
        overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        badge = (58, 334, 156, 432)
        draw.rounded_rectangle(badge, radius=16, fill=rgba(body, 132), outline=rgba(accent, 170), width=3)
        draw_icon(draw, kind, 107, 383, 54, rgba(accent, 172 if kind != "ghost" else 190))
        result = Image.alpha_composite(result, overlay)

    elif strategy_id == "c_corner_bleed":
        overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        draw_icon(draw, kind, 414, 390, 184, rgba(accent, 58 if kind != "ghost" else 72))
        result = Image.alpha_composite(result, overlay)
        result = draw_value_plate(result, face)

    elif strategy_id == "d_background_underlay":
        overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        draw_icon(draw, kind, 256, 298, 286, rgba(accent, 28 if kind != "ghost" else 36))
        result = Image.alpha_composite(result, overlay)
        result = draw_value_plate(result, face)

    elif strategy_id == "e_top_clean_side_icon":
        result = draw_value_plate(result, face)
        overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        draw.line((86, 424, 426, 424), fill=rgba(accent, 86), width=3)
        draw.text((188, 438), "图标移至侧面", fill=rgba(accent, 128), font=load_font(18, bold=False))
        result = Image.alpha_composite(result, overlay)

    draw_label_text(result, face)
    return result


def make_board(generated: dict[tuple[str, str], Path]) -> None:
    thumb = 224
    col_gap = 24
    row_gap = 32
    left = 44
    top = 128
    header_h = 104
    face_label_w = 126
    width = left + face_label_w + len(STRATEGIES) * (thumb + col_gap) + 20
    height = top + len(FACES) * (thumb + row_gap + 86) + 44
    board = Image.new("RGB", (width, height), "#08111d")
    draw = ImageDraw.Draw(board)

    title_font = load_font(36)
    sub_font = load_font(20, bold=False)
    head_font = load_font(19)
    small_font = load_font(15, bold=False)
    label_font = load_font(26)

    draw.text((44, 32), "骰面图标放置方案 v0.15", fill="#f7dc91", font=title_font)
    draw.text(
        (44, 78),
        "控制变量：同一套骰面底材，同一套“属性 + 数字”读数；只比较图标层级与位置。先选方案，再进入 GLB / Godot 动态落地。",
        fill="#bfd0d7",
        font=sub_font,
    )

    x0 = left + face_label_w
    for i, strategy in enumerate(STRATEGIES):
        x = x0 + i * (thumb + col_gap)
        draw.text((x, header_h), str(strategy["title"]), fill="#f1dc99", font=head_font)
        draw.text((x, header_h + 26), str(strategy["score"]), fill="#8fd8df", font=small_font)

    for row, face in enumerate(FACES):
        y = top + row * (thumb + row_gap + 86)
        draw.text((left, y + 74), str(face["label"]), fill=str(face["text"]), font=label_font)
        draw.text((left, y + 110), "普通骰" if face["kind"] == "reason" else "黑骰", fill="#9fb3bd", font=sub_font)
        for col, strategy in enumerate(STRATEGIES):
            x = x0 + col * (thumb + col_gap)
            tile = Image.open(generated[(str(face["kind"]), str(strategy["id"]))]).convert("RGB")
            tile = tile.resize((thumb, thumb), Image.Resampling.LANCZOS)
            board.paste(tile, (x, y))
            draw.rounded_rectangle((x, y, x + thumb, y + thumb), radius=8, outline="#2e4653", width=2)
            draw.text((x, y + thumb + 10), str(strategy["note"]), fill="#c9d4d9", font=small_font)

    footer_y = height - 42
    draw.text(
        (44, footer_y),
        "初步判断：B/C 更适合继续落地；D 更有风格但风险是运动中抢字；E 最清楚但会削弱骰面身份。等待你确认后再做 UV/GLB/Godot GIF。",
        fill="#e2c57f",
        font=sub_font,
    )
    board.save(BOARD_PATH)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cell_size = v014.assert_square_grid(BASE_SHEET, 2, 2)
    generated: dict[tuple[str, str], Path] = {}
    with Image.open(BASE_SHEET) as sheet:
        sheet = sheet.convert("RGBA")
        for face in FACES:
            base = v014.crop_base_tile(sheet, list(face["cell"]), cell_size)
            clean = clean_source_icon_zone(base, face)
            for strategy in STRATEGIES:
                tile = apply_strategy(clean, face, str(strategy["id"]))
                path = OUT_DIR / f"dice_{face['kind']}_{strategy['id']}_v0_15.png"
                tile.save(path)
                generated[(str(face["kind"]), str(strategy["id"]))] = path
    make_board(generated)
    print(BOARD_PATH)


if __name__ == "__main__":
    main()
