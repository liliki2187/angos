from pathlib import Path

from PIL import Image


ROOT = Path(r"D:\angos")
SOURCE = (
    ROOT
    / "design/art-direction/region-task-board/text-integrated-fullscreen-style-draft-v1/source/02-imagegen-camera-cleanup-source-v1.png"
)
RUNTIME = (
    ROOT
    / "docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/01-selected-ready-full-v1.png"
)
OUTPUT = (
    ROOT
    / "design/art-direction/region-task-board/text-integrated-fullscreen-style-draft-v1/review"
)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    # The model rendered all typography. Local processing only normalizes the 16:9 output
    # to the project review size and restores the immutable runtime map/pin rectangle.
    draft = Image.open(SOURCE).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    runtime = Image.open(RUNTIME).convert("RGB")
    map_rect = (420, 96, 1460, 900)
    draft.paste(runtime.crop(map_rect), (420, 96))

    draft.save(OUTPUT / "01-text-integrated-fullscreen-style-draft-v1.png", quality=95)
    draft.crop((0, 72, 420, 1080)).save(
        OUTPUT / "02-left-text-art-integration-v1.png", quality=95
    )
    draft.crop((1460, 72, 1920, 1080)).save(
        OUTPUT / "03-right-text-art-integration-v1.png", quality=95
    )
    draft.crop((420, 900, 1460, 1080)).save(
        OUTPUT / "04-bottom-text-art-integration-v1.png", quality=95
    )
    draft.resize((480, 270), Image.Resampling.LANCZOS).save(
        OUTPUT / "05-fullscreen-25-percent-v1.png", quality=95
    )


if __name__ == "__main__":
    main()
