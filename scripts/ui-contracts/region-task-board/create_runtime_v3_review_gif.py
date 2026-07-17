from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
SCREENSHOT_DIR = ROOT / "docs/screenshots/2026-07-17-region-task-pin-slice-v3"
FRAME_DIR = SCREENSHOT_DIR / "frames"
OUTPUT = SCREENSHOT_DIR / "06-hover-select-runtime-demo.gif"


def main() -> None:
    source_paths = sorted(FRAME_DIR.glob("frame_*.png"))
    if len(source_paths) != 26:
        raise RuntimeError(f"Expected 26 runtime frames, found {len(source_paths)}")
    frames: list[Image.Image] = []
    for path in source_paths:
        with Image.open(path) as image:
            frame = image.convert("RGB").resize((960, 540), Image.Resampling.LANCZOS)
            frames.append(frame.quantize(colors=192, method=Image.Quantize.MEDIANCUT))
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=110,
        loop=0,
        optimize=False,
        disposal=2,
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
