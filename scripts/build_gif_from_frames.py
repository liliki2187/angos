from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def _load_frame(path: Path, size: tuple[int, int]) -> Image.Image:
    source = Image.open(path).convert("RGB")
    resized = source.resize(size, Image.Resampling.LANCZOS)
    return resized


def build_animation(
    frames_dir: Path,
    output_path: Path,
    pattern: str,
    size: tuple[int, int],
    duration_ms: int,
) -> None:
    frame_paths = sorted(frames_dir.glob(pattern))
    if not frame_paths:
        raise SystemExit(f"No frames matched {pattern!r} in {frames_dir}")

    frames = [_load_frame(path, size) for path in frame_paths]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = output_path.suffix.lower()
    if suffix == ".gif":
        palette = frames[0].convert("P", palette=Image.Palette.ADAPTIVE, colors=160)
        indexed_frames = [frame.quantize(palette=palette) for frame in frames]
        indexed_frames[0].save(
            output_path,
            save_all=True,
            append_images=indexed_frames[1:],
            duration=duration_ms,
            loop=0,
            optimize=True,
            disposal=2,
        )
        return

    if suffix == ".webp":
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0,
            quality=78,
            method=6,
        )
        return

    raise SystemExit("Output must end with .gif or .webp")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_dir", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--pattern", default="frame_*.png")
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=540)
    parser.add_argument("--duration-ms", type=int, default=50)
    args = parser.parse_args()

    build_animation(
        frames_dir=args.frames_dir,
        output_path=args.output_path,
        pattern=args.pattern,
        size=(args.width, args.height),
        duration_ms=args.duration_ms,
    )


if __name__ == "__main__":
    main()
