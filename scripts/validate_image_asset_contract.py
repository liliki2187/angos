#!/usr/bin/env python3
"""Validate simple image-asset geometry contracts."""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def image_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        header = fh.read(24)
    if header.startswith(PNG_SIGNATURE) and header[12:16] == b"IHDR":
        return struct.unpack(">II", header[16:24])

    try:
        from PIL import Image  # type: ignore
    except Exception as exc:  # pragma: no cover - non-PNG fallback
        raise RuntimeError(f"{path} is not a PNG and Pillow is unavailable") from exc

    with Image.open(path) as image:
        return image.size


def assert_square(path: Path, tolerance: int) -> list[str]:
    width, height = image_size(path)
    if abs(width - height) <= tolerance:
        return []
    return [f"{path}: expected square image, got {width}x{height}"]


def assert_square_grid_cells(path: Path, cols: int, rows: int, tolerance: float) -> list[str]:
    width, height = image_size(path)
    cell_width = width / float(cols)
    cell_height = height / float(rows)
    if abs(cell_width - cell_height) <= tolerance:
        return []
    return [
        f"{path}: expected {cols}x{rows} grid cells to be square, "
        f"got cell {cell_width:.2f}x{cell_height:.2f} from source {width}x{height}"
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--square", action="append", default=[], help="Image path that must be square.")
    parser.add_argument(
        "--square-grid",
        nargs=3,
        action="append",
        metavar=("IMAGE", "COLS", "ROWS"),
        default=[],
        help="Atlas path and grid dimensions whose cells must be square.",
    )
    parser.add_argument("--pixel-tolerance", type=int, default=0)
    parser.add_argument("--cell-tolerance", type=float, default=0.5)
    args = parser.parse_args()

    errors: list[str] = []
    for image_path in args.square:
        errors.extend(assert_square(Path(image_path), args.pixel_tolerance))

    for image_path, cols, rows in args.square_grid:
        errors.extend(assert_square_grid_cells(Path(image_path), int(cols), int(rows), args.cell_tolerance))

    if errors:
        print("Image asset contract failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Image asset contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
