from __future__ import annotations

import argparse
from pathlib import Path

from psd_support import export_composite_png


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a PSD file to a flattened PNG."
    )
    parser.add_argument("input_psd", type=Path)
    parser.add_argument("output_png", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    export_composite_png(args.input_psd, args.output_png)
    print(f"Saved PNG to {args.output_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
