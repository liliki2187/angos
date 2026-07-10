from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_dice_glb_v0_12_assets as v012


REPO = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO / "design" / "art-direction" / "dice-style"
BASE_SHEET = SOURCE_DIR / "dice-face-simplified-v0-11-r1-ai-base-sheet.png"
TEXTURE_DIR = REPO / "gd_project" / "Assets" / "dice_textures" / "v0_11"
OUT_DIR = REPO / "gd_project" / "Assets" / "dice_models" / "v0_14"
STYLE_OUT_DIR = REPO / "design" / "art-direction" / "dice-style"
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")

TILE = 512
ATLAS_COLS = 3
ATLAS_ROWS = 2

TITLE_RECT = (70, 48, 442, 146)
VALUE_RECT = (148, 154, 364, 282)
WATERMARK_RECT = (184, 326, 328, 424)

FACES = [
    {
        "kind": "explore",
        "label": "探索",
        "value": "+2",
        "cell": [0, 0],
        "side": "dice_face_side_explore_watermark.png",
        "body": "#43552a",
        "text": "#f5e8bd",
        "stroke": "#10170f",
        "accent": "#d8ddb0",
    },
    {
        "kind": "reason",
        "label": "理性",
        "value": "+2",
        "cell": [1, 0],
        "side": "dice_face_side_reason_watermark.png",
        "body": "#1f7884",
        "text": "#f5e8bd",
        "stroke": "#071a1e",
        "accent": "#d9e5d7",
    },
    {
        "kind": "occult",
        "label": "诡思",
        "value": "+2",
        "cell": [0, 1],
        "side": "dice_face_side_occult_watermark.png",
        "body": "#463158",
        "text": "#f5e8bd",
        "stroke": "#100b16",
        "accent": "#bfa2c9",
    },
    {
        "kind": "ghost",
        "label": "鬼迹",
        "value": "!",
        "cell": [1, 1],
        "side": "dice_face_side_ghost_watermark.png",
        "body": "#171719",
        "text": "#ff6240",
        "stroke": "#0b0706",
        "accent": "#e85b36",
    },
]

TILE_LAYOUT = {
    "top": (0, 0),
    "front": (1, 0),
    "right": (2, 0),
    "back": (0, 1),
    "left": (1, 1),
    "bottom": (2, 1),
}


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def assert_square_grid(path: Path, cols: int, rows: int) -> int:
    with Image.open(path) as image:
        width, height = image.size
    if width != height:
        raise SystemExit(f"{path} must be square, got {width}x{height}")
    if width % cols != 0 or height % rows != 0:
        raise SystemExit(f"{path} must divide cleanly by {cols}x{rows}, got {width}x{height}")
    cell = width // cols
    if cell != height // rows:
        raise SystemExit(f"{path} grid cell must be square")
    return cell


def crop_base_tile(sheet: Image.Image, cell: list[int], cell_size: int) -> Image.Image:
    col, row = cell
    x0 = col * cell_size
    y0 = row * cell_size
    return sheet.crop((x0, y0, x0 + cell_size, y0 + cell_size)).resize((TILE, TILE), Image.Resampling.LANCZOS).convert("RGBA")


def hex_rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    raw = hex_color.lstrip("#")
    return (int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16), alpha)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    stroke: str,
    stroke_width: int,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = rect[0] + ((rect[2] - rect[0] - width) // 2) - bbox[0]
    y = rect[1] + ((rect[3] - rect[1] - height) // 2) - bbox[1]
    draw.text((x, y), text, font=font, fill=fill, stroke_fill=stroke, stroke_width=stroke_width)


def suppress_old_icon(tile: Image.Image, face: dict[str, object]) -> Image.Image:
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    body = str(face["body"])
    draw.rounded_rectangle((46, 38, 466, 292), radius=20, fill=hex_rgba(body, 34))
    draw_suppression_icon(draw, str(face["kind"]), 256, 370, 158, hex_rgba(body, 224))
    return Image.alpha_composite(tile, overlay)


def draw_compass(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color: tuple[int, int, int, int]) -> None:
    r = size // 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=4)
    for angle in (0, 90, 180, 270):
        rad = math.radians(angle)
        x = cx + int(math.cos(rad) * r * 0.9)
        y = cy + int(math.sin(rad) * r * 0.9)
        draw.line((cx, cy, x, y), fill=color, width=4)
    points = [(cx, cy - r), (cx + 12, cy), (cx, cy + r), (cx - 12, cy)]
    draw.polygon(points, outline=color)
    draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), outline=color, width=4)


def draw_head(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color: tuple[int, int, int, int]) -> None:
    r = size // 2
    draw.ellipse((cx - r * 0.55, cy - r, cx + r * 0.55, cy + r * 0.12), fill=color)
    draw.polygon([(cx - r * 0.52, cy - 4), (cx - r * 0.82, cy + 16), (cx - r * 0.42, cy + 20)], fill=color)
    draw.rectangle((cx - int(r * 0.28), cy + int(r * 0.10), cx + int(r * 0.32), cy + int(r * 0.62)), fill=color)
    draw.rectangle((cx - int(r * 0.50), cy + int(r * 0.50), cx + int(r * 0.54), cy + int(r * 0.74)), fill=color)


def draw_eye(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color: tuple[int, int, int, int]) -> None:
    w = size
    h = int(size * 0.52)
    draw.ellipse((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), outline=color, width=5)
    draw.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), outline=color, width=5)
    draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=color)


def draw_ghost(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color: tuple[int, int, int, int]) -> None:
    r = size // 2
    draw.ellipse((cx - r * 0.55, cy - r, cx + r * 0.55, cy + r * 0.10), fill=color)
    draw.rounded_rectangle((cx - int(r * 0.52), cy - int(r * 0.25), cx + int(r * 0.52), cy + int(r * 0.65)), radius=16, fill=color)
    draw.polygon(
        [
            (cx - int(r * 0.52), cy + int(r * 0.62)),
            (cx - int(r * 0.25), cy + int(r * 0.86)),
            (cx, cy + int(r * 0.62)),
            (cx + int(r * 0.25), cy + int(r * 0.86)),
            (cx + int(r * 0.52), cy + int(r * 0.62)),
        ],
        fill=color,
    )
    eye_cut = (0, 0, 0, 64)
    draw.ellipse((cx - 18, cy - 20, cx - 7, cy - 9), fill=eye_cut)
    draw.ellipse((cx + 7, cy - 20, cx + 18, cy - 9), fill=eye_cut)


def draw_suppression_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int, size: int, color: tuple[int, int, int, int]) -> None:
    if kind == "explore":
        draw_compass(draw, cx, cy, size, color)
    elif kind == "reason":
        draw_head(draw, cx, cy, size, color)
    elif kind == "occult":
        draw_eye(draw, cx, cy, size, color)
    else:
        draw_ghost(draw, cx, cy, size, color)


def draw_small_icon(tile: Image.Image, face: dict[str, object]) -> Image.Image:
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    kind = str(face["kind"])
    color = hex_rgba(str(face["accent"]), 54 if kind != "ghost" else 68)
    cx = (WATERMARK_RECT[0] + WATERMARK_RECT[2]) // 2
    cy = (WATERMARK_RECT[1] + WATERMARK_RECT[3]) // 2 + 2
    size = 62
    if kind == "explore":
        draw_compass(draw, cx, cy, size, color)
    elif kind == "reason":
        draw_head(draw, cx, cy, size, color)
    elif kind == "occult":
        draw_eye(draw, cx, cy, size, color)
    else:
        draw_ghost(draw, cx, cy, size, color)
    return Image.alpha_composite(tile, overlay)


def make_top_tile(base_tile: Image.Image, face: dict[str, object]) -> Image.Image:
    tile = suppress_old_icon(base_tile, face)
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    accent = str(face["accent"])
    body = str(face["body"])

    draw.rounded_rectangle((VALUE_RECT[0] - 12, VALUE_RECT[1] - 8, VALUE_RECT[2] + 12, VALUE_RECT[3] + 8), radius=18, fill=hex_rgba(body, 154))
    draw.rounded_rectangle((VALUE_RECT[0] - 12, VALUE_RECT[1] - 8, VALUE_RECT[2] + 12, VALUE_RECT[3] + 8), radius=18, outline=hex_rgba(accent, 210), width=4)
    draw.line((132, 150, 380, 150), fill=hex_rgba(accent, 122), width=3)
    tile = Image.alpha_composite(tile, overlay)
    tile = draw_small_icon(tile, face)

    draw = ImageDraw.Draw(tile)
    draw_centered_text(draw, TITLE_RECT, str(face["label"]), load_font(86), str(face["text"]), str(face["stroke"]), 4)
    draw_centered_text(draw, VALUE_RECT, str(face["value"]), load_font(94), str(face["text"]), str(face["stroke"]), 5)
    return tile


def make_atlas(top_tile: Image.Image, face: dict[str, object], atlas_path: Path) -> None:
    atlas = Image.new("RGBA", (ATLAS_COLS * TILE, ATLAS_ROWS * TILE), "#00000000")
    side = Image.open(TEXTURE_DIR / str(face["side"])).convert("RGBA").resize((TILE, TILE), Image.Resampling.LANCZOS)
    for tile_name, (col, row) in TILE_LAYOUT.items():
        source = top_tile if tile_name == "top" else side
        atlas.paste(source, (col * TILE, row * TILE))
    atlas.save(atlas_path)


def make_uv_proof(atlas_path: Path, proof_path: Path) -> None:
    atlas = Image.open(atlas_path).convert("RGB")
    draw = ImageDraw.Draw(atlas)
    for name, (col, row) in TILE_LAYOUT.items():
        x0 = col * TILE
        y0 = row * TILE
        draw.rectangle((x0, y0, x0 + TILE - 1, y0 + TILE - 1), outline="#f6e6ad", width=4)
        draw.text((x0 + 18, y0 + 18), name, fill="#f6e6ad")
    atlas.save(proof_path)


def save_contact_sheet(paths: list[Path], output_path: Path) -> None:
    thumb = 220
    gap = 22
    label_h = 28
    width = gap + 4 * (thumb + gap)
    height = gap + thumb + label_h + gap
    sheet = Image.new("RGB", (width, height), "#101719")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(paths):
        x = gap + index * (thumb + gap)
        y = gap
        with Image.open(path) as image:
            sheet.paste(image.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + thumb + 8), path.stem, fill="#d7c79a")
    sheet.save(output_path)


def save_text_safe_review(paths: list[Path], output_path: Path) -> None:
    tile_size = 420
    gap = 28
    sheet = Image.new("RGB", (gap + 2 * (tile_size + gap), gap + 2 * (tile_size + gap)), "#07101c")
    label_font = load_font(20, bold=False)
    for index, path in enumerate(paths):
        col = index % 2
        row = index // 2
        x = gap + col * (tile_size + gap)
        y = gap + row * (tile_size + gap)
        with Image.open(path) as image:
            tile = image.convert("RGB").resize((tile_size, tile_size), Image.Resampling.LANCZOS)
        sheet.paste(tile, (x, y))
        draw = ImageDraw.Draw(sheet)
        scale = tile_size / TILE
        for rect, color, label in [
            (TITLE_RECT, "#fff0a6", "title"),
            (VALUE_RECT, "#ffb45f", "number priority"),
            (WATERMARK_RECT, "#70e6ff", "small watermark"),
        ]:
            rx0 = x + int(rect[0] * scale)
            ry0 = y + int(rect[1] * scale)
            rx1 = x + int(rect[2] * scale)
            ry1 = y + int(rect[3] * scale)
            draw.rounded_rectangle((rx0, ry0, rx1, ry1), radius=10, outline=color, width=3)
            label_y = max(y + 4, ry0 - 24)
            draw.text((rx0 + 8, label_y), label, fill=color, font=label_font)
    sheet.save(output_path)


def main() -> None:
    cell_size = assert_square_grid(BASE_SHEET, 2, 2)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mesh = v012.build_beveled_dice_mesh()
    top_paths: list[Path] = []

    manifest: dict[str, object] = {
        "id": "angus_dice_glb_v0_14_number_priority_uv",
        "status": "glb_uv_runtime_preview_input",
        "extends": "v0.13 text-safe GLB/UV",
        "top_information_contract": {
            "title_rect": TITLE_RECT,
            "value_rect": VALUE_RECT,
            "watermark_rect": WATERMARK_RECT,
            "rule": "number/value is the second-priority read after the attribute title; icon is a smaller low-opacity watermark",
        },
        "mesh_contract": {
            "type": "closed beveled cube mesh",
            "central_faces": 6,
            "edge_chamfers": 12,
            "corner_chamfers": 8,
            "former_gap_fix": "same one-mesh beveled body as v0.12/v0.13",
        },
        "uv_contract": {
            "atlas_layout": "3x2",
            "tiles": TILE_LAYOUT,
            "note": "Top uses number-priority text-safe tile; side, bottom, bevels and corners use watermark/rim regions from the same atlas.",
        },
        "models": [],
    }

    with Image.open(BASE_SHEET) as base_sheet:
        base_sheet = base_sheet.convert("RGBA")
        for face in FACES:
            top_tile = make_top_tile(crop_base_tile(base_sheet, face["cell"], cell_size), face)
            top_path = OUT_DIR / f"dice_{face['kind']}_top_number_priority_v0_14.png"
            atlas_path = OUT_DIR / f"dice_{face['kind']}_uv_atlas_v0_14.png"
            proof_path = OUT_DIR / f"dice_{face['kind']}_uv_atlas_v0_14_proof.png"
            glb_path = OUT_DIR / f"dice_{face['kind']}_v0_14.glb"
            top_tile.save(top_path)
            make_atlas(top_tile, face, atlas_path)
            make_uv_proof(atlas_path, proof_path)
            v012.make_glb(mesh, atlas_path, glb_path)
            v012.validate_glb_header(glb_path)
            top_paths.append(top_path)
            manifest["models"].append(
                {
                    "kind": face["kind"],
                    "label": face["label"],
                    "value": face["value"],
                    "glb": str(glb_path.relative_to(REPO)).replace("\\", "/"),
                    "top_tile": str(top_path.relative_to(REPO)).replace("\\", "/"),
                    "atlas": str(atlas_path.relative_to(REPO)).replace("\\", "/"),
                    "uv_proof": str(proof_path.relative_to(REPO)).replace("\\", "/"),
                    "source_base": str(BASE_SHEET.relative_to(REPO)).replace("\\", "/"),
                    "source_side": str((TEXTURE_DIR / str(face["side"])).relative_to(REPO)).replace("\\", "/"),
                }
            )

    contact_sheet = STYLE_OUT_DIR / "dice-face-layout-v0-14-number-priority-sheet.png"
    review = STYLE_OUT_DIR / "dice-face-layout-v0-14-number-priority-review.png"
    save_contact_sheet(top_paths, contact_sheet)
    save_text_safe_review(top_paths, review)
    manifest["style_contact_sheet"] = str(contact_sheet.relative_to(REPO)).replace("\\", "/")
    manifest["text_safe_review"] = str(review.relative_to(REPO)).replace("\\", "/")
    (OUT_DIR / "dice_glb_v0_14_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(FACES)} v0.14 number-priority GLB dice models to {OUT_DIR}")


if __name__ == "__main__":
    main()
