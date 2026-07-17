from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-15-region-task-board-runtime-v2"
OUTPUT = SCREENSHOT_DIR / "05-region-event-selection-runtime-demo.gif"


def main() -> None:
    source_names = [
        "01-region-empty-selection.png",
        "02-region-m330-selected.png",
        "03-region-deadline-selected.png",
        "02-region-m330-selected.png",
    ]
    durations = [900, 1500, 1500, 900]
    frames: list[Image.Image] = []
    for name in source_names:
        with Image.open(SCREENSHOT_DIR / name) as image:
            frame = image.convert("RGB").resize((960, 540), Image.Resampling.LANCZOS)
            frames.append(frame.quantize(colors=192, method=Image.Quantize.MEDIANCUT))
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
