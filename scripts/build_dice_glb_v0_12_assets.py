from __future__ import annotations

import json
import math
import struct
from pathlib import Path

from PIL import Image, ImageDraw


REPO = Path(__file__).resolve().parents[1]
TEXTURE_DIR = REPO / "gd_project" / "Assets" / "dice_textures" / "v0_11"
OUT_DIR = REPO / "gd_project" / "Assets" / "dice_models" / "v0_12"
TILE = 512
ATLAS_COLS = 3
ATLAS_ROWS = 2

FACES = [
    {
        "kind": "explore",
        "label": "\u63a2\u7d22",
        "top": "dice_face_top_explore.png",
        "side": "dice_face_side_explore_watermark.png",
        "body": "#43552a",
    },
    {
        "kind": "reason",
        "label": "\u7406\u6027",
        "top": "dice_face_top_reason.png",
        "side": "dice_face_side_reason_watermark.png",
        "body": "#1f7884",
    },
    {
        "kind": "occult",
        "label": "\u8be1\u601d",
        "top": "dice_face_top_occult.png",
        "side": "dice_face_side_occult_watermark.png",
        "body": "#463158",
    },
    {
        "kind": "ghost",
        "label": "\u9b3c\u8ff9",
        "top": "dice_face_top_ghost.png",
        "side": "dice_face_side_ghost_watermark.png",
        "body": "#171719",
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


def make_atlas(face: dict[str, str], atlas_path: Path) -> None:
    atlas = Image.new("RGBA", (ATLAS_COLS * TILE, ATLAS_ROWS * TILE), "#00000000")
    top = Image.open(TEXTURE_DIR / face["top"]).convert("RGBA")
    side = Image.open(TEXTURE_DIR / face["side"]).convert("RGBA")
    for tile_name, (col, row) in TILE_LAYOUT.items():
        source = top if tile_name == "top" else side
        atlas.paste(source.resize((TILE, TILE), Image.Resampling.LANCZOS), (col * TILE, row * TILE))
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


def normalize(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(sum(value * value for value in vector))
    return tuple(value / length for value in vector)


def cross(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def subtract(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def uv_rect(tile: str, inset: float = 0.035) -> list[tuple[float, float]]:
    col, row = TILE_LAYOUT[tile]
    u0 = (col + inset) / ATLAS_COLS
    u1 = (col + 1.0 - inset) / ATLAS_COLS
    v0 = (row + inset) / ATLAS_ROWS
    v1 = (row + 1.0 - inset) / ATLAS_ROWS
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def uv_strip(tile: str) -> list[tuple[float, float]]:
    col, row = TILE_LAYOUT[tile]
    u0 = (col + 0.10) / ATLAS_COLS
    u1 = (col + 0.90) / ATLAS_COLS
    v0 = (row + 0.08) / ATLAS_ROWS
    v1 = (row + 0.18) / ATLAS_ROWS
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


class MeshBuilder:
    def __init__(self) -> None:
        self.positions: list[tuple[float, float, float]] = []
        self.normals: list[tuple[float, float, float]] = []
        self.uvs: list[tuple[float, float]] = []
        self.indices: list[int] = []

    def add_vertex(self, position: tuple[float, float, float], normal: tuple[float, float, float], uv: tuple[float, float]) -> int:
        self.positions.append(position)
        self.normals.append(normal)
        self.uvs.append(uv)
        return len(self.positions) - 1

    def add_triangle(self, points: list[tuple[float, float, float]], uvs: list[tuple[float, float]], normal: tuple[float, float, float]) -> None:
        a = self.add_vertex(points[0], normal, uvs[0])
        b = self.add_vertex(points[1], normal, uvs[1])
        c = self.add_vertex(points[2], normal, uvs[2])
        self.indices.extend([a, b, c])

    def add_quad(self, points: list[tuple[float, float, float]], uvs: list[tuple[float, float]], normal: tuple[float, float, float]) -> None:
        tri_normal = cross(subtract(points[1], points[0]), subtract(points[2], points[0]))
        if dot(tri_normal, normal) >= 0.0:
            triangles = [(0, 1, 2), (0, 2, 3)]
        else:
            triangles = [(0, 2, 1), (0, 3, 2)]
        for ia, ib, ic in triangles:
            self.add_triangle([points[ia], points[ib], points[ic]], [uvs[ia], uvs[ib], uvs[ic]], normal)


def build_beveled_dice_mesh() -> MeshBuilder:
    h = 0.5
    bevel = 0.075
    c = h - bevel
    mesh = MeshBuilder()

    # Central square faces.
    mesh.add_quad([(-c, h, -c), (c, h, -c), (c, h, c), (-c, h, c)], uv_rect("top"), (0, 1, 0))
    mesh.add_quad([(-c, c, h), (c, c, h), (c, -c, h), (-c, -c, h)], uv_rect("front"), (0, 0, 1))
    mesh.add_quad([(h, c, c), (h, c, -c), (h, -c, -c), (h, -c, c)], uv_rect("right"), (1, 0, 0))
    mesh.add_quad([(c, c, -h), (-c, c, -h), (-c, -c, -h), (c, -c, -h)], uv_rect("back"), (0, 0, -1))
    mesh.add_quad([(-h, c, -c), (-h, c, c), (-h, -c, c), (-h, -c, -c)], uv_rect("left"), (-1, 0, 0))
    mesh.add_quad([(-c, -h, c), (c, -h, c), (c, -h, -c), (-c, -h, -c)], uv_rect("bottom"), (0, -1, 0))

    # Edge chamfers. These close the former decal gaps as real geometry.
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            normal = normalize((sx, sy, 0.0))
            points = [(sx * h, sy * c, -c), (sx * c, sy * h, -c), (sx * c, sy * h, c), (sx * h, sy * c, c)]
            mesh.add_quad(points, uv_strip("front"), normal)
    for sx in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            normal = normalize((sx, 0.0, sz))
            points = [(sx * h, -c, sz * c), (sx * c, -c, sz * h), (sx * c, c, sz * h), (sx * h, c, sz * c)]
            mesh.add_quad(points, uv_strip("right"), normal)
    for sy in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            normal = normalize((0.0, sy, sz))
            points = [(-c, sy * h, sz * c), (-c, sy * c, sz * h), (c, sy * c, sz * h), (c, sy * h, sz * c)]
            mesh.add_quad(points, uv_strip("top" if sy > 0 else "bottom"), normal)

    # Corner chamfers.
    corner_uvs = [
        uv_rect("bottom", 0.42)[0],
        uv_rect("bottom", 0.42)[1],
        uv_rect("bottom", 0.42)[2],
    ]
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                normal = normalize((sx, sy, sz))
                points = [(sx * h, sy * c, sz * c), (sx * c, sy * h, sz * c), (sx * c, sy * c, sz * h)]
                tri_normal = cross(subtract(points[1], points[0]), subtract(points[2], points[0]))
                if dot(tri_normal, normal) < 0.0:
                    points = [points[0], points[2], points[1]]
                    uvs = [corner_uvs[0], corner_uvs[2], corner_uvs[1]]
                else:
                    uvs = corner_uvs
                mesh.add_triangle(points, uvs, normal)

    return mesh


def pad4(data: bytes) -> bytes:
    return data + (b"\x00" * ((4 - len(data) % 4) % 4))


def append_view(buffer: bytearray, data: bytes) -> tuple[int, int]:
    while len(buffer) % 4:
        buffer.append(0)
    offset = len(buffer)
    buffer.extend(data)
    while len(buffer) % 4:
        buffer.append(0)
    return offset, len(data)


def make_glb(mesh: MeshBuilder, image_path: Path, glb_path: Path) -> None:
    binary = bytearray()

    index_data = struct.pack("<" + "H" * len(mesh.indices), *mesh.indices)
    pos_data = struct.pack("<" + "f" * (len(mesh.positions) * 3), *(value for point in mesh.positions for value in point))
    norm_data = struct.pack("<" + "f" * (len(mesh.normals) * 3), *(value for point in mesh.normals for value in point))
    uv_data = struct.pack("<" + "f" * (len(mesh.uvs) * 2), *(value for uv in mesh.uvs for value in uv))
    png_data = image_path.read_bytes()

    index_offset, index_len = append_view(binary, index_data)
    pos_offset, pos_len = append_view(binary, pos_data)
    norm_offset, norm_len = append_view(binary, norm_data)
    uv_offset, uv_len = append_view(binary, uv_data)
    image_offset, image_len = append_view(binary, png_data)

    mins = [min(point[i] for point in mesh.positions) for i in range(3)]
    maxs = [max(point[i] for point in mesh.positions) for i in range(3)]

    gltf = {
        "asset": {"version": "2.0", "generator": "Angus dice GLB v0.12 script"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "AngusDiceV012"}],
        "meshes": [
            {
                "name": "beveled_closed_dice_uv_mesh",
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "NORMAL": 1, "TEXCOORD_0": 2},
                        "indices": 3,
                        "material": 0,
                    }
                ],
            }
        ],
        "materials": [
            {
                "name": "dice_uv_atlas_material",
                "pbrMetallicRoughness": {
                    "baseColorTexture": {"index": 0},
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.84,
                },
            }
        ],
        "textures": [{"sampler": 0, "source": 0}],
        "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
        "images": [{"bufferView": 4, "mimeType": "image/png", "name": image_path.name}],
        "buffers": [{"byteLength": len(binary)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": index_offset, "byteLength": index_len, "target": 34963},
            {"buffer": 0, "byteOffset": pos_offset, "byteLength": pos_len, "target": 34962},
            {"buffer": 0, "byteOffset": norm_offset, "byteLength": norm_len, "target": 34962},
            {"buffer": 0, "byteOffset": uv_offset, "byteLength": uv_len, "target": 34962},
            {"buffer": 0, "byteOffset": image_offset, "byteLength": image_len},
        ],
        "accessors": [
            {"bufferView": 1, "byteOffset": 0, "componentType": 5126, "count": len(mesh.positions), "type": "VEC3", "min": mins, "max": maxs},
            {"bufferView": 2, "byteOffset": 0, "componentType": 5126, "count": len(mesh.normals), "type": "VEC3"},
            {"bufferView": 3, "byteOffset": 0, "componentType": 5126, "count": len(mesh.uvs), "type": "VEC2"},
            {"bufferView": 0, "byteOffset": 0, "componentType": 5123, "count": len(mesh.indices), "type": "SCALAR"},
        ],
    }

    json_chunk = pad4(json.dumps(gltf, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    bin_chunk = pad4(bytes(binary))
    total_len = 12 + 8 + len(json_chunk) + 8 + len(bin_chunk)
    header = struct.pack("<III", 0x46546C67, 2, total_len)
    json_header = struct.pack("<I4s", len(json_chunk), b"JSON")
    bin_header = struct.pack("<I4s", len(bin_chunk), b"BIN\x00")
    glb_path.write_bytes(header + json_header + json_chunk + bin_header + bin_chunk)


def validate_glb_header(path: Path) -> None:
    data = path.read_bytes()
    magic, version, total_len = struct.unpack("<III", data[:12])
    if magic != 0x46546C67 or version != 2 or total_len != len(data):
        raise SystemExit(f"Invalid GLB header for {path}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mesh = build_beveled_dice_mesh()
    manifest: dict[str, object] = {
        "id": "angus_dice_glb_v0_12_closed_beveled_uv",
        "status": "glb_uv_runtime_preview_input",
        "mesh_contract": {
            "type": "closed beveled cube mesh",
            "central_faces": 6,
            "edge_chamfers": 12,
            "corner_chamfers": 8,
            "former_gap_fix": "faces are part of one indexed mesh; bevel strips close top-side and side-side transitions",
        },
        "uv_contract": {
            "atlas_layout": "3x2",
            "tiles": TILE_LAYOUT,
            "note": "Top uses true Chinese/value tile; side, bottom, bevels and corners use watermark/rim regions from the same atlas.",
        },
        "models": [],
    }
    for face in FACES:
        atlas_path = OUT_DIR / f"dice_{face['kind']}_uv_atlas_v0_12.png"
        proof_path = OUT_DIR / f"dice_{face['kind']}_uv_atlas_v0_12_proof.png"
        glb_path = OUT_DIR / f"dice_{face['kind']}_v0_12.glb"
        make_atlas(face, atlas_path)
        make_uv_proof(atlas_path, proof_path)
        make_glb(mesh, atlas_path, glb_path)
        validate_glb_header(glb_path)
        manifest["models"].append(
            {
                "kind": face["kind"],
                "label": face["label"],
                "glb": str(glb_path.relative_to(REPO)).replace("\\", "/"),
                "atlas": str(atlas_path.relative_to(REPO)).replace("\\", "/"),
                "uv_proof": str(proof_path.relative_to(REPO)).replace("\\", "/"),
                "source_top": str((TEXTURE_DIR / face["top"]).relative_to(REPO)).replace("\\", "/"),
                "source_side": str((TEXTURE_DIR / face["side"]).relative_to(REPO)).replace("\\", "/"),
            }
        )
    (OUT_DIR / "dice_glb_v0_12_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(FACES)} GLB dice models to {OUT_DIR}")


if __name__ == "__main__":
    main()
