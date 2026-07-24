from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "wmw-colorway-base-user-selected-v0-1.png"
BASE_NORMALIZED = ROOT / "wmw-colorway-base-user-selected-v0-1-1920x1080.png"
VARIANTS = [
    (
        "A",
        "核心橄榄周刊",
        ROOT / "wmw-colorway-01-core-olive-v0-1-imagegen.png",
        ROOT / "wmw-colorway-01-core-olive-v0-1.png",
    ),
    (
        "B",
        "芥末黄 × 钴蓝周刊",
        ROOT / "wmw-colorway-02-mustard-cobalt-v0-1-imagegen.png",
        ROOT / "wmw-colorway-02-mustard-cobalt-v0-1.png",
    ),
    (
        "C",
        "极地青档案",
        ROOT / "wmw-colorway-03-arctic-teal-v0-1-imagegen.png",
        ROOT / "wmw-colorway-03-arctic-teal-v0-1.png",
    ),
    (
        "D",
        "黑墨 × 酸绿印刷",
        ROOT / "wmw-colorway-04-ink-acid-v0-1-imagegen.png",
        ROOT / "wmw-colorway-04-ink-acid-v0-1.png",
    ),
]

TARGET_SIZE = (1920, 1080)
BOARD_SIZE = (3840, 2280)
LABEL_HEIGHT = 60
BOARD_BG = (9, 16, 22)

ROLE_RECTS = {
    "board": (450, 44, 1360, 125),
    "paper": (1410, 368, 1840, 500),
    "selected": (500, 205, 700, 390),
    "locked": (820, 205, 1150, 390),
    "cta": (1410, 940, 1840, 1040),
    "deadline": (1710, 760, 1840, 820),
}


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def normalize_image(source: Path, destination: Path) -> tuple[int, int]:
    image = Image.open(source).convert("RGB")
    source_size = image.size
    if image.size != TARGET_SIZE:
        image = image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
    image.save(destination, optimize=True)
    return source_size


def edge_array(image: Image.Image) -> np.ndarray:
    gray = image.convert("L").resize((960, 540), Image.Resampling.LANCZOS)
    gray = gray.filter(ImageFilter.GaussianBlur(radius=0.7))
    edges = np.asarray(gray.filter(ImageFilter.FIND_EDGES), dtype=np.float32)
    edges -= edges.mean()
    norm = float(np.linalg.norm(edges))
    return edges / norm if norm else edges


def shifted_similarity(base: np.ndarray, variant: np.ndarray) -> dict[str, object]:
    best = (-1.0, 0, 0)
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            y0b = max(0, dy)
            y1b = min(base.shape[0], base.shape[0] + dy)
            x0b = max(0, dx)
            x1b = min(base.shape[1], base.shape[1] + dx)
            y0v = max(0, -dy)
            y1v = y0v + (y1b - y0b)
            x0v = max(0, -dx)
            x1v = x0v + (x1b - x0b)
            score = float(np.sum(base[y0b:y1b, x0b:x1b] * variant[y0v:y1v, x0v:x1v]))
            if score > best[0]:
                best = (score, dx, dy)
    zero = float(np.sum(base * variant))
    return {
        "zero_shift_edge_cosine": round(zero, 4),
        "best_edge_cosine": round(best[0], 4),
        "best_shift_at_1920": [int(best[1] * 2), int(best[2] * 2)],
        "pass_canvas": True,
        "pass_global_alignment": abs(best[1]) <= 1 and abs(best[2]) <= 1,
    }


def mean_rgb(image: Image.Image, rect: tuple[int, int, int, int]) -> list[int]:
    data = np.asarray(image.crop(rect).convert("RGB"), dtype=np.float32)
    return [int(round(value)) for value in data.reshape(-1, 3).mean(axis=0)]


def role_vector(role_colors: dict[str, list[int]]) -> np.ndarray:
    return np.asarray([value for role in ROLE_RECTS for value in role_colors[role]], dtype=np.float32)


def main() -> None:
    base_source_size = normalize_image(BASE, BASE_NORMALIZED)

    normalized: list[tuple[str, str, Path, tuple[int, int]]] = []
    for code, title, source, destination in VARIANTS:
        source_size = normalize_image(source, destination)
        normalized.append((code, title, destination, source_size))

    board = Image.new("RGB", BOARD_SIZE, BOARD_BG)
    draw = ImageDraw.Draw(board)
    font = load_font(32)
    base_edges = edge_array(Image.open(BASE_NORMALIZED).convert("RGB"))
    audit_variants: dict[str, object] = {}
    role_vectors: dict[str, np.ndarray] = {}

    for index, (code, title, path, source_size) in enumerate(normalized):
        col = index % 2
        row = index // 2
        x = col * TARGET_SIZE[0]
        y = row * (TARGET_SIZE[1] + LABEL_HEIGHT)
        image = Image.open(path).convert("RGB")
        draw.text((x + 24, y + 11), f"{code}  {title}", fill=(235, 239, 235), font=font)
        board.paste(image, (x, y + LABEL_HEIGHT))

        role_colors = {name: mean_rgb(image, rect) for name, rect in ROLE_RECTS.items()}
        role_vectors[code] = role_vector(role_colors)
        audit_variants[code] = {
            "title": title,
            "source_file": str(VARIANTS[index][2]),
            "source_size": list(source_size),
            "final_file": str(path),
            "final_size": list(image.size),
            "role_mean_rgb": role_colors,
            **shifted_similarity(base_edges, edge_array(image)),
        }

    distances: dict[str, float] = {}
    codes = [item[0] for item in normalized]
    for i, left in enumerate(codes):
        for right in codes[i + 1 :]:
            distance = float(np.linalg.norm(role_vectors[left] - role_vectors[right]) / math.sqrt(role_vectors[left].size))
            distances[f"{left}-{right}"] = round(distance, 2)

    board_path = ROOT / "wmw-colorway-v0-1-comparison-board.png"
    board.save(board_path, optimize=True)

    audit = {
        "status": "review_candidate",
        "base_file": str(BASE),
        "base_source_size": list(base_source_size),
        "base_normalized_file": str(BASE_NORMALIZED),
        "base_size": list(TARGET_SIZE),
        "normalization": "真实 imagegen 输出仅做 LANCZOS 尺寸归一化；未做程序化重绘或调色。",
        "geometry_note": "边缘相关只用于发现整屏平移或明显结构漂移；最终视觉仍需人工复核。",
        "role_sample_rects": {key: list(value) for key, value in ROLE_RECTS.items()},
        "variants": audit_variants,
        "pairwise_role_rgb_rms": distances,
        "comparison_board": str(board_path),
        "comparison_board_size": list(BOARD_SIZE),
    }
    audit_path = ROOT / "wmw-colorway-v0-1-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print(board_path)
    print(audit_path)


if __name__ == "__main__":
    main()
