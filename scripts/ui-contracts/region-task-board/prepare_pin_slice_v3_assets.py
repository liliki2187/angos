from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "image_gen/2026-07-17/region-task-production-slice-v3"
OUT_DIR = SOURCE_DIR / "prepared"
GODOT_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/pin_slice"


def alpha_bbox(image: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("No opaque subject found")
    return bbox


def strip_key_fringe(image: Image.Image) -> Image.Image:
    """Remove small magenta remnants introduced by Lanczos resampling."""
    cleaned = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels: list[tuple[int, int, int, int]] = []
    for red, green, blue, alpha_value in image.getdata():
        if alpha_value == 0 or (red > 170 and blue > 170 and green < 125):
            pixels.append((0, 0, 0, 0))
        else:
            pixels.append((red, green, blue, alpha_value))
    cleaned.putdata(pixels)
    return cleaned


def fit_subject(
    source: Image.Image,
    canvas_size: tuple[int, int],
    inset: tuple[int, int, int, int],
    *,
    bottom_align: bool = False,
) -> tuple[Image.Image, dict[str, object]]:
    bbox = alpha_bbox(source)
    subject = source.crop(bbox)
    left, top, right, bottom = inset
    usable_w = canvas_size[0] - left - right
    usable_h = canvas_size[1] - top - bottom
    scale = min(usable_w / subject.width, usable_h / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    x = left + (usable_w - size[0]) // 2
    y = canvas_size[1] - bottom - size[1] if bottom_align else top + (usable_h - size[1]) // 2
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(subject, (x, y))
    canvas = strip_key_fringe(canvas)
    return canvas, {
        "source_bbox": list(bbox),
        "canvas_size": list(canvas_size),
        "inset": list(inset),
        "placed_bbox": [x, y, x + size[0], y + size[1]],
        "scale": scale,
    }


def fit_icon(source: Image.Image, frame_size: int = 84, inset: int = 12) -> tuple[Image.Image, dict[str, object]]:
    bbox = alpha_bbox(source)
    subject = source.crop(bbox)
    usable = frame_size - inset * 2
    scale = min(usable / subject.width, usable / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    x = (frame_size - size[0]) // 2
    y = (frame_size - size[1]) // 2
    frame = Image.new("RGBA", (frame_size, frame_size), (0, 0, 0, 0))
    frame.alpha_composite(subject, (x, y))
    frame = strip_key_fringe(frame)
    return frame, {
        "source_bbox": list(bbox),
        "placed_bbox": [x, y, x + size[0], y + size[1]],
        "scale": scale,
    }


def alpha_metrics(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    total = image.width * image.height
    transparent = histogram[0]
    opaque = histogram[255]
    partial = total - transparent - opaque
    magenta_like_visible = 0
    for red, green, blue, alpha_value in image.getdata():
        if alpha_value > 0 and red > 170 and blue > 170 and green < 125:
            magenta_like_visible += 1
    return {
        "size": [image.width, image.height],
        "bbox_alpha_gt_8": list(alpha_bbox(image)),
        "transparent_pixels": transparent,
        "partially_transparent_pixels": partial,
        "opaque_pixels": opaque,
        "transparent_ratio": round(transparent / total, 6),
        "partial_ratio": round(partial / total, 6),
        "visible_magenta_key_like_pixels": magenta_like_visible,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GODOT_DIR.mkdir(parents=True, exist_ok=True)

    pin_source = Image.open(SOURCE_DIR / "region-task-pin-shell-c-hybrid-v3-alpha.png").convert("RGBA")
    label_source = Image.open(SOURCE_DIR / "region-task-label-shell-c-hybrid-v3-alpha.png").convert("RGBA")
    icons_source = Image.open(SOURCE_DIR / "region-task-kind-icons-c-hybrid-v3-alpha.png").convert("RGBA")

    pin_3x, pin_fit = fit_subject(pin_source, (192, 240), (12, 12, 12, 12), bottom_align=True)
    label_2x, label_fit = fit_subject(label_source, (400, 144), (12, 16, 12, 16))
    pin_runtime = strip_key_fringe(pin_3x.resize((64, 80), Image.Resampling.LANCZOS))
    label_runtime = strip_key_fringe(label_2x.resize((200, 72), Image.Resampling.LANCZOS))

    icon_names = ["permanent", "chain", "hidden", "temp"]
    half_w = icons_source.width // 2
    half_h = icons_source.height // 2
    quadrants = [
        (0, 0, half_w, half_h),
        (half_w, 0, icons_source.width, half_h),
        (0, half_h, half_w, icons_source.height),
        (half_w, half_h, icons_source.width, icons_source.height),
    ]
    icon_frames: list[Image.Image] = []
    icon_fits: dict[str, object] = {}
    for name, rect in zip(icon_names, quadrants):
        frame, fit = fit_icon(icons_source.crop(rect))
        icon_frames.append(frame)
        icon_fits[name] = fit
        frame.save(OUT_DIR / f"rt-task-pin-icon-{name}-v3-3x.png")

    atlas = Image.new("RGBA", (84 * len(icon_frames), 84), (0, 0, 0, 0))
    for index, frame in enumerate(icon_frames):
        atlas.alpha_composite(frame, (index * 84, 0))
    atlas = strip_key_fringe(atlas)
    atlas_runtime = strip_key_fringe(atlas.resize((28 * len(icon_frames), 28), Image.Resampling.LANCZOS))

    prepared = {
        "rt-task-pin-shell-c-hybrid-v3-3x.png": pin_3x,
        "rt-task-pin-shell-c-hybrid-v3-runtime-64x80.png": pin_runtime,
        "rt-task-pin-label-c-hybrid-v3-2x.png": label_2x,
        "rt-task-pin-label-c-hybrid-v3-runtime-200x72.png": label_runtime,
        "rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png": atlas,
        "rt-task-pin-kind-icons-c-hybrid-v3-atlas-runtime.png": atlas_runtime,
    }
    for name, image in prepared.items():
        image.save(OUT_DIR / name)

    godot_names = [
        "rt-task-pin-shell-c-hybrid-v3-3x.png",
        "rt-task-pin-label-c-hybrid-v3-2x.png",
        "rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png",
    ]
    for name in godot_names:
        shutil.copy2(OUT_DIR / name, GODOT_DIR / name)

    metrics = {
        "artifact_type": "imagegen_assets_with_programmatic_chroma_removal_crop_resize_and_atlas_layout",
        "design_direction": "C cut-wedge primary + B quiet content face + A single side spine",
        "pin_source": alpha_metrics(pin_source),
        "pin_3x": alpha_metrics(pin_3x),
        "pin_fit": pin_fit,
        "pin_anchor_runtime": [32, 76],
        "label_source": alpha_metrics(label_source),
        "label_2x": alpha_metrics(label_2x),
        "label_fit": label_fit,
        "label_runtime_content_rect": [14, 8, 166, 56],
        "icon_source": alpha_metrics(icons_source),
        "icon_atlas_3x": alpha_metrics(atlas),
        "icon_frame_order": icon_names,
        "icon_fits": icon_fits,
        "status_and_selection_note": "State carrier, selection paper backplate, partial print arc and cluster remain runtime-owned Godot drawing.",
    }
    (OUT_DIR / "region-task-pin-slice-v3-alpha-metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
