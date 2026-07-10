from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_dice_glb_v0_12_assets as v012


REPO = Path(__file__).resolve().parents[1]
TEXTURE_DIR = REPO / "gd_project" / "Assets" / "dice_textures" / "v0_11"
OUT_DIR = REPO / "gd_project" / "Assets" / "dice_models" / "v0_19"
STYLE_OUT_DIR = REPO / "design" / "art-direction" / "dice-style"
GLB_OUT_DIR = STYLE_OUT_DIR / "glb-v0-19-disabled"
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")

TILE = 512
ATLAS_COLS = 3
ATLAS_ROWS = 2

# v0.19D: large attribute title, large rule number, no icon, no title plate.
TITLE_RECT = (58, 54, 454, 192)
VALUE_RECT = (102, 194, 410, 396)
CLEAR_ICON_RECT = (46, 46, 466, 466)

FACES = [
    {
        "kind": "explore",
        "label": "探索",
        "value": "+2",
        "source": "dice_face_side_explore_watermark.png",
        "body": "#43552a",
        "text": "#f5e8bd",
        "stroke": "#10170f",
        "accent": "#d8ddb0",
    },
    {
        "kind": "reason",
        "label": "理性",
        "value": "+2",
        "source": "dice_face_side_reason_watermark.png",
        "body": "#1f7884",
        "text": "#f5e8bd",
        "stroke": "#071a1e",
        "accent": "#d9e5d7",
    },
    {
        "kind": "occult",
        "label": "诡思",
        "value": "+2",
        "source": "dice_face_side_occult_watermark.png",
        "body": "#463158",
        "text": "#f5e8bd",
        "stroke": "#100b16",
        "accent": "#bfa2c9",
    },
    {
        "kind": "ghost",
        "label": "鬼迹",
        "value": "!",
        "source": "dice_face_side_ghost_watermark.png",
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


def make_plain_base(face: dict[str, object]) -> Image.Image:
    source = Image.open(TEXTURE_DIR / str(face["source"])).convert("RGBA").resize((TILE, TILE), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(source)
    body = str(face["body"])
    accent = str(face["accent"])

    # Remove the old icon/watermark while keeping the AI-generated low-poly material and beveled border.
    x0, y0, x1, y1 = CLEAR_ICON_RECT
    draw.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=hex_rgba(body, 255))
    facets = Image.new("RGBA", source.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(facets, "RGBA")
    # Rebuild the whole writable face as quiet low-poly material, not as an icon/panel layer.
    draw.polygon([(48, 52), (258, 52), (162, 252), (48, 236)], fill=hex_rgba("#ffffff", 14))
    draw.polygon([(258, 52), (466, 48), (466, 226), (162, 252)], fill=hex_rgba("#000000", 22))
    draw.polygon([(48, 236), (162, 252), (248, 466), (48, 466)], fill=hex_rgba("#000000", 18))
    draw.polygon([(162, 252), (466, 226), (466, 466), (248, 466)], fill=hex_rgba("#ffffff", 11))
    draw.polygon([(88, 420), (252, 284), (420, 420)], fill=hex_rgba(accent, 14))
    return Image.alpha_composite(source, facets)


def add_print_dust(tile: Image.Image, face: dict[str, object]) -> Image.Image:
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    accent = str(face["accent"])
    body = str(face["body"])

    for i in range(10):
        x = 82 + i * 10
        draw.rectangle((x, 67, x + 3, 70), fill=hex_rgba(accent, 52))
    for i in range(11):
        x = 366 + i * 8
        y = 398 + i * 5
        draw.rectangle((x, y, x + 3, y + 3), fill=hex_rgba(accent, 42))
    draw.rounded_rectangle((34, 34, 478, 478), radius=12, outline=hex_rgba(body, 42), width=2)
    return Image.alpha_composite(tile, overlay)


def make_top_tile(face: dict[str, object]) -> Image.Image:
    tile = add_print_dust(make_plain_base(face), face)
    draw = ImageDraw.Draw(tile)
    draw_centered_text(draw, TITLE_RECT, str(face["label"]), load_font(116), str(face["text"]), str(face["stroke"]), 7)
    value_font_size = 154 if str(face["value"]) != "!" else 176
    draw_centered_text(draw, VALUE_RECT, str(face["value"]), load_font(value_font_size), str(face["text"]), str(face["stroke"]), 8)
    return tile


def make_side_tile(face: dict[str, object]) -> Image.Image:
    tile = make_plain_base(face)
    overlay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    accent = str(face["accent"])
    draw.line((98, 412, 414, 412), fill=hex_rgba(accent, 54), width=2)
    for i in range(9):
        x = 362 + i * 9
        draw.rectangle((x, 366 + i * 4, x + 3, 369 + i * 4), fill=hex_rgba(accent, 36))
    return Image.alpha_composite(tile, overlay)


def make_atlas(top_tile: Image.Image, side_tile: Image.Image, atlas_path: Path) -> None:
    atlas = Image.new("RGBA", (ATLAS_COLS * TILE, ATLAS_ROWS * TILE), "#00000000")
    for tile_name, (col, row) in TILE_LAYOUT.items():
        source = top_tile if tile_name == "top" else side_tile
        atlas.paste(source, (col * TILE, row * TILE))
    atlas.save(atlas_path)


def make_uv_proof(atlas_path: Path, proof_path: Path) -> None:
    atlas = Image.open(atlas_path).convert("RGB")
    draw = ImageDraw.Draw(atlas)
    font = load_font(24, bold=False)
    for name, (col, row) in TILE_LAYOUT.items():
        x0 = col * TILE
        y0 = row * TILE
        draw.rectangle((x0, y0, x0 + TILE - 1, y0 + TILE - 1), outline="#f6e6ad", width=4)
        draw.text((x0 + 18, y0 + 18), name, fill="#f6e6ad", font=font)
    atlas.save(proof_path)


def save_contact_sheet(paths: list[Path], output_path: Path) -> None:
    thumb = 240
    gap = 28
    label_h = 30
    width = gap + 4 * (thumb + gap)
    height = gap + thumb + label_h + gap
    sheet = Image.new("RGB", (width, height), "#101719")
    draw = ImageDraw.Draw(sheet)
    font = load_font(18, bold=False)
    for index, path in enumerate(paths):
        x = gap + index * (thumb + gap)
        y = gap
        with Image.open(path) as image:
            sheet.paste(image.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + thumb + 8), path.stem, fill="#d7c79a", font=font)
    sheet.save(output_path)


def save_readability_review(paths: list[Path], output_path: Path) -> None:
    samples = [180, 96, 72, 52]
    gap = 24
    row_h = 232
    width = 1320
    height = gap + len(paths) * row_h
    sheet = Image.new("RGB", (width, height), "#07101c")
    draw = ImageDraw.Draw(sheet)
    label_font = load_font(22, bold=False)
    small_font = load_font(16, bold=False)
    for row, path in enumerate(paths):
        y = gap + row * row_h
        draw.text((gap, y), path.stem, fill="#f6e6ad", font=label_font)
        x = 280
        with Image.open(path) as image:
            tile = image.convert("RGB")
            for size in samples:
                sheet.paste(tile.resize((size, size), Image.Resampling.LANCZOS), (x, y + 34))
                draw.rectangle((x, y + 34, x + size - 1, y + 34 + size - 1), outline="#2b6f77", width=1)
                draw.text((x, y + 42 + size), f"{size}px", fill="#89d4dd", font=small_font)
                x += size + 42
    sheet.save(output_path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GLB_OUT_DIR.mkdir(parents=True, exist_ok=True)
    mesh = v012.build_beveled_dice_mesh()
    top_paths: list[Path] = []

    manifest: dict[str, object] = {
        "id": "angus_dice_glb_v0_19_text_only_d_layout_uv",
        "status": "runtime_texture_input_glb_generated_outside_godot_scan",
        "extends": "v0.14 number-priority GLB/UV",
        "source_style_reference": "design/art-direction/dice-style/dice-face-text-only-no-frame-layouts-imagegen-v0-19.png",
        "selected_reference_variant": "D",
        "top_information_contract": {
            "title_rect": TITLE_RECT,
            "value_rect": VALUE_RECT,
            "rule": "v0.19D: large attribute title, large value, no icon, no watermark, no title frame",
        },
        "mesh_contract": {
            "type": "closed beveled cube mesh",
            "central_faces": 6,
            "edge_chamfers": 12,
            "corner_chamfers": 8,
            "former_gap_fix": "same one-mesh beveled body as v0.12-v0.14; no floating top decal plane",
        },
        "uv_contract": {
            "atlas_layout": "3x2",
            "tiles": TILE_LAYOUT,
            "note": "Top tile carries the readable text; side, back, left, right and bottom use icon-free material tiles.",
        },
        "models": [],
    }

    for face in FACES:
        top_tile = make_top_tile(face)
        side_tile = make_side_tile(face)
        top_path = OUT_DIR / f"dice_{face['kind']}_top_text_only_d_v0_19.png"
        side_path = OUT_DIR / f"dice_{face['kind']}_side_plain_v0_19.png"
        atlas_path = OUT_DIR / f"dice_{face['kind']}_uv_atlas_v0_19.png"
        proof_path = OUT_DIR / f"dice_{face['kind']}_uv_atlas_v0_19_proof.png"
        glb_path = GLB_OUT_DIR / f"dice_{face['kind']}_v0_19.glb"
        top_tile.save(top_path)
        side_tile.save(side_path)
        make_atlas(top_tile, side_tile, atlas_path)
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
                "side_tile": str(side_path.relative_to(REPO)).replace("\\", "/"),
                "atlas": str(atlas_path.relative_to(REPO)).replace("\\", "/"),
                "uv_proof": str(proof_path.relative_to(REPO)).replace("\\", "/"),
                "source_material": str((TEXTURE_DIR / str(face["source"])).relative_to(REPO)).replace("\\", "/"),
            }
        )

    contact_sheet = STYLE_OUT_DIR / "dice-face-layout-v0-19-d-text-only-sheet.png"
    readability = STYLE_OUT_DIR / "dice-face-layout-v0-19-d-readability-review.png"
    save_contact_sheet(top_paths, contact_sheet)
    save_readability_review(top_paths, readability)
    manifest["style_contact_sheet"] = str(contact_sheet.relative_to(REPO)).replace("\\", "/")
    manifest["readability_review"] = str(readability.relative_to(REPO)).replace("\\", "/")
    (OUT_DIR / "dice_glb_v0_19_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(FACES)} v0.19D text-only texture sets to {OUT_DIR}")
    print(f"Wrote disabled GLB reference models to {GLB_OUT_DIR}")


if __name__ == "__main__":
    main()
