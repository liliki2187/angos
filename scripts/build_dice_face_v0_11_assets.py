from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO / "design" / "art-direction" / "dice-style"
NO_TEXT_SHEET = SOURCE_DIR / "dice-face-simplified-v0-11-r1-ai-base-sheet.png"
OUT_DIR = REPO / "gd_project" / "Assets" / "dice_textures" / "v0_11"
TARGET_TILE = 512
FONT_PATH = Path("C:/Windows/Fonts/msyhbd.ttc")

FACES = [
    {
        "kind": "explore",
        "id": "dice_face_top_explore",
        "side_id": "dice_face_side_explore_watermark",
        "label": "\u63a2\u7d22",
        "value": "+2",
        "cell": [0, 0],
    },
    {
        "kind": "reason",
        "id": "dice_face_top_reason",
        "side_id": "dice_face_side_reason_watermark",
        "label": "\u7406\u6027",
        "value": "+2",
        "cell": [1, 0],
    },
    {
        "kind": "occult",
        "id": "dice_face_top_occult",
        "side_id": "dice_face_side_occult_watermark",
        "label": "\u8be1\u601d",
        "value": "+2",
        "cell": [0, 1],
    },
    {
        "kind": "ghost",
        "id": "dice_face_top_ghost",
        "side_id": "dice_face_side_ghost_watermark",
        "label": "\u9b3c\u8ff9",
        "value": "!",
        "cell": [1, 1],
    },
]


def assert_square_grid(path: Path, cols: int, rows: int) -> tuple[int, int]:
    with Image.open(path) as image:
        width, height = image.size
    if width != height:
        raise SystemExit(f"{path} must be square, got {width}x{height}")
    if width % cols != 0 or height % rows != 0:
        raise SystemExit(f"{path} must divide cleanly by {cols}x{rows}, got {width}x{height}")
    cell_w = width // cols
    cell_h = height // rows
    if cell_w != cell_h:
        raise SystemExit(f"{path} grid cell must be square, got {cell_w}x{cell_h}")
    return cell_w, cell_h


def crop_tile(sheet: Image.Image, cell: list[int], cell_size: int) -> Image.Image:
    col, row = cell
    x0 = col * cell_size
    y0 = row * cell_size
    tile = sheet.crop((x0, y0, x0 + cell_size, y0 + cell_size))
    return tile.resize((TARGET_TILE, TARGET_TILE), Image.Resampling.LANCZOS)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    return ImageFont.load_default()


def centered_text(draw: ImageDraw.ImageDraw, text: str, y: int, font: ImageFont.ImageFont, fill: str, stroke: str, stroke_width: int) -> None:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    width = bbox[2] - bbox[0]
    x = (TARGET_TILE - width) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_fill=stroke, stroke_width=stroke_width)


def add_runtime_text(tile: Image.Image, label: str, value: str, kind: str) -> Image.Image:
    out = tile.convert("RGBA")
    draw = ImageDraw.Draw(out)
    is_ghost = kind == "ghost"
    fill = "#ff6544" if is_ghost else "#f7e7bd"
    stroke = "#120d0d" if is_ghost else "#111719"
    centered_text(draw, label, 34, load_font(142), fill, stroke, 6)
    centered_text(draw, value, 158, load_font(98), fill, stroke, 5)
    return out


def save_contact_sheet(tile_paths: list[Path], output_path: Path) -> None:
    thumb = 180
    gap = 22
    label_h = 28
    width = gap + 4 * (thumb + gap)
    height = gap + 2 * (thumb + label_h + gap)
    sheet = Image.new("RGB", (width, height), "#101719")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(tile_paths):
        row = index // 4
        col = index % 4
        x = gap + col * (thumb + gap)
        y = gap + row * (thumb + label_h + gap)
        with Image.open(path) as image:
            sheet.paste(image.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + thumb + 8), path.stem, fill="#d7c79a")
    sheet.save(output_path)


def main() -> None:
    base_cell = assert_square_grid(NO_TEXT_SHEET, 2, 2)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cell_size = base_cell[0]
    top_paths: list[Path] = []
    side_paths: list[Path] = []
    tiles: list[dict[str, object]] = []

    with Image.open(NO_TEXT_SHEET) as top_sheet, Image.open(NO_TEXT_SHEET) as side_sheet:
        top_sheet = top_sheet.convert("RGBA")
        side_sheet = side_sheet.convert("RGBA")
        for face in FACES:
            top_path = OUT_DIR / f"{face['id']}.png"
            side_path = OUT_DIR / f"{face['side_id']}.png"
            top_tile = crop_tile(top_sheet, face["cell"], cell_size)
            add_runtime_text(top_tile, str(face["label"]), str(face["value"]), str(face["kind"])).save(top_path)
            crop_tile(side_sheet, face["cell"], cell_size).save(side_path)
            top_paths.append(top_path)
            side_paths.append(side_path)
            tiles.append(
                {
                    "kind": face["kind"],
                    "label": face["label"],
                    "value": face["value"],
                    "top_id": face["id"],
                    "top_path": str(top_path.relative_to(REPO)).replace("\\", "/"),
                    "side_id": face["side_id"],
                    "side_path": str(side_path.relative_to(REPO)).replace("\\", "/"),
                    "source_cell": face["cell"],
                    "source_cell_size": [cell_size, cell_size],
                    "export_size": [TARGET_TILE, TARGET_TILE],
                }
            )

    contact_sheet = OUT_DIR / "dice_face_tiles_v0_11_contact_sheet.png"
    save_contact_sheet(top_paths + side_paths, contact_sheet)

    manifest = {
        "id": "dice_face_textures_v0_11_simplified_square_cells",
        "status": "bitmap_face_runtime_preview_input",
        "geometry_contract": "source sheets are 1:1; each 2x2 cell is square before tile export",
        "target_tile_size": [TARGET_TILE, TARGET_TILE],
        "sources": {
            "no_text_base": {
                "path": str(NO_TEXT_SHEET.relative_to(REPO)).replace("\\", "/"),
                "grid": [2, 2],
                "cell_size": [cell_size, cell_size],
                "note": "No-text AI image layer. Top faces use program-rendered Chinese/value overlay after square crop; side/bottom faces keep the watermark-only base.",
            },
        },
        "tiles": tiles,
        "contact_sheet": str(contact_sheet.relative_to(REPO)).replace("\\", "/"),
    }
    (OUT_DIR / "dice_face_textures_v0_11_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(top_paths) + len(side_paths)} tiles to {OUT_DIR}")


if __name__ == "__main__":
    main()
