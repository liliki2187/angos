"""把真实 Godot 捕获帧整理成轻量交互状态 GIF。"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frame_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    paths = sorted(args.frame_dir.glob("frame_*.png"))
    if len(paths) < 4:
        raise SystemExit(f"至少需要 4 帧，当前只有 {len(paths)} 帧")

    frames: list[Image.Image] = []
    for path in paths:
        with Image.open(path) as source:
            frame = source.convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
            frames.append(frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=[1000, 900, 700, 1400],
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"saved {args.output}")


if __name__ == "__main__":
    main()
