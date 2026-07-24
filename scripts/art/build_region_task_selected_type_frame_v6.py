from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from build_region_task_single_compound_probe_v4 import (
    BG,
    GOOD,
    MUTED_TEXT,
    PAPER_TEXT,
    ROOT,
    alpha_bbox,
    build_pin_only_frame,
    build_runtime_frames,
    checker,
    font,
    remove_connected_chroma,
    tip_center_x,
)


V5B_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v5b-selected-icon-seat"
SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v6-selected-type-frame"

DEFAULT_CHROMA = V5B_DIR / "01-permanent-default-right-compound-source-v5b-chroma.png"
UNDERLAY_CHROMA = V5B_DIR / "02-permanent-selected-backing-underlay-source-v5b-chroma.png"
PIN_CHROMA = V5B_DIR / "03-permanent-default-pin-only-source-v5b-chroma.png"
IMAGEGEN_RAW = SOURCE_DIR / "02-permanent-selected-type-frame-source-v6-imagegen-raw.png"

SELECTED_CHROMA = SOURCE_DIR / "02-permanent-selected-type-frame-source-v6-chroma.png"
SELECTED_MASK = SOURCE_DIR / "02-permanent-selected-type-frame-source-v6-mask.png"
DEFAULT_ALPHA = SOURCE_DIR / "01-permanent-default-right-compound-source-v6-alpha.png"
SELECTED_ALPHA = SOURCE_DIR / "02-permanent-selected-type-frame-source-v6-alpha.png"
UNDERLAY_ALPHA = SOURCE_DIR / "03-permanent-selected-backing-underlay-source-v6-alpha.png"
PIN_ALPHA = SOURCE_DIR / "04-permanent-default-pin-only-source-v6-alpha.png"

DEFAULT_3X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v6-3x.png"
DEFAULT_1X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v6-1x.png"
SELECTED_3X = SOURCE_DIR / "rt-task-compound-permanent-selected-type-frame-right-v6-3x.png"
SELECTED_1X = SOURCE_DIR / "rt-task-compound-permanent-selected-type-frame-right-v6-1x.png"
UNDERLAY_3X = SOURCE_DIR / "rt-task-compound-permanent-selected-underlay-right-v6-3x.png"
UNDERLAY_1X = SOURCE_DIR / "rt-task-compound-permanent-selected-underlay-right-v6-1x.png"
PIN_3X = SOURCE_DIR / "rt-task-pin-permanent-default-v6-3x.png"
PIN_1X = SOURCE_DIR / "rt-task-pin-permanent-default-v6-1x.png"

FIXTURE_DIR = ROOT / "gd_project" / "tests" / "fixtures" / "region_task_selected_type_frame_v6"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-selected-type-frame-v6"
QA_BOARD = SCREENSHOT_DIR / "01-selected-type-frame-asset-layer-qa-v6.png"
STATE_FRAME_DIR = SCREENSHOT_DIR / "frames-selected-type-frame-v6"
STATE_GIF = SCREENSHOT_DIR / "03-hover-selected-type-frame-runtime-v6.gif"
METADATA = SOURCE_DIR / "selected-type-frame-v6.json"

ICON_ATLAS = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "region_task"
    / "v2"
    / "pin_slice"
    / "rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png"
)


def compound_left_pad(source: Image.Image) -> int:
    bbox = alpha_bbox(source)
    cropped = source.crop(bbox)
    scaled_width = round(cropped.width * 240 / cropped.height)
    scaled = cropped.resize((scaled_width, 240), Image.Resampling.LANCZOS)
    return round(108 - tip_center_x(scaled))


def _connected_component(mask: np.ndarray, seed: tuple[int, int]) -> np.ndarray:
    height, width = mask.shape
    sx, sy = seed
    if not mask[sy, sx]:
        raise RuntimeError(f"Frame seed {seed} is outside the neutral B-frame candidate mask")
    result = np.zeros_like(mask, dtype=bool)
    queue: deque[tuple[int, int]] = deque([(sx, sy)])
    result[sy, sx] = True
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height and mask[ny, nx] and not result[ny, nx]:
                result[ny, nx] = True
                queue.append((nx, ny))
    return result


def constrain_imagegen_frame(default_chroma: Image.Image, generated_raw: Image.Image) -> tuple[Image.Image, Image.Image, dict]:
    """Transfer generated olive ink only through the already-approved B-frame coverage."""
    default_rgb = default_chroma.convert("RGB")
    generated_rgb = generated_raw.convert("RGB").resize(default_rgb.size, Image.Resampling.LANCZOS)
    source = np.asarray(default_rgb).astype(np.float32)
    generated = np.asarray(generated_rgb).astype(np.float32)

    red, green, blue = source[:, :, 0], source[:, :, 1], source[:, :, 2]
    candidate = (
        (red < 220)
        & (green < 210)
        & (blue < 185)
        & ((red - blue) > 24)
        & ((green - blue) > 20)
    )
    spatial_gate = np.zeros(candidate.shape, dtype=bool)
    spatial_gate[190:600, 185:610] = True
    component = _connected_component(candidate & spatial_gate, (400, 220))
    if int(component.sum()) < 20_000:
        raise RuntimeError(f"B-frame component unexpectedly small: {int(component.sum())} px")

    dilated = np.asarray(
        Image.fromarray((component.astype(np.uint8) * 255), mode="L").filter(ImageFilter.MaxFilter(7))
    ).astype(np.float32) / 255.0
    paper_reference = np.array([244.0, 229.0, 204.0], dtype=np.float32)
    frame_reference = np.median(source[component], axis=0)
    ink_axis = paper_reference - frame_reference
    denominator = float(np.dot(ink_axis, ink_axis))
    coverage = np.sum((paper_reference - source) * ink_axis, axis=2) / denominator
    coverage = np.clip((coverage - 0.04) / 0.92, 0.0, 1.0) * dilated
    coverage[component] = np.maximum(coverage[component], 0.96)

    # Keep the generated material variation, but calibrate its representative ink
    # to the approved permanent-task color before it enters the original B mask.
    target_frame = np.array([127.0, 138.0, 71.0], dtype=np.float32)  # #7F8A47
    raw_target_median = np.median(generated[component], axis=0)
    calibrated = generated + (target_frame - raw_target_median)[None, None, :]
    calibration_delta = target_frame - raw_target_median
    for _index in range(3):
        trial = source * (1.0 - coverage[:, :, None]) + calibrated * coverage[:, :, None]
        trial_median = np.median(trial[component], axis=0)
        correction = target_frame - trial_median
        calibrated += correction[None, None, :]
        calibration_delta += correction

    # The original B frame owns exact coverage; imagegen owns only the constrained
    # olive ink texture inside it.
    result = source * (1.0 - coverage[:, :, None]) + calibrated * coverage[:, :, None]
    result = np.clip(np.rint(result), 0, 255).astype(np.uint8)
    mask_image = Image.fromarray(np.clip(np.rint(coverage * 255), 0, 255).astype(np.uint8), mode="L")
    metrics = {
        "default_canvas": list(default_rgb.size),
        "imagegen_raw_canvas": list(generated_raw.size),
        "constrained_canvas": list(default_rgb.size),
        "frame_component_pixels": int(component.sum()),
        "frame_coverage_pixels_gt_50pct": int((coverage > 0.5).sum()),
        "frame_reference_rgb": [round(float(value), 2) for value in frame_reference],
        "imagegen_raw_frame_rgb_median": [round(float(value), 2) for value in raw_target_median],
        "approved_target_rgb": [127, 138, 71],
        "calibration_delta_rgb": [round(float(value), 2) for value in calibration_delta],
        "constrained_frame_rgb_median": [round(float(value), 2) for value in np.median(result[component], axis=0)],
    }
    return Image.fromarray(result, mode="RGB"), mask_image, metrics


def permanent_icon() -> Image.Image:
    atlas = Image.open(ICON_ATLAS).convert("RGBA")
    return atlas.crop((0, 0, 84, 84)).resize((28, 28), Image.Resampling.LANCZOS)


def runtime_copy(front: Image.Image, underlay: Image.Image | None = None) -> Image.Image:
    result = Image.new("RGBA", (278, 80), (0, 0, 0, 0))
    if underlay is not None:
        result.alpha_composite(underlay)
    result.alpha_composite(front)
    result.alpha_composite(permanent_icon(), (22, 14))
    draw = ImageDraw.Draw(result)
    draw.text((92, 12), "罗斯威尔档案残页", font=font(15, True), fill=(23, 37, 42, 255))
    draw.text((92, 40), "常驻调查 · 1天", font=font(12), fill=(64, 81, 87, 255))
    return result


def build_qa(default: Image.Image, selected: Image.Image, underlay: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1500, 760), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "选中态局部实验 v6｜永久任务 · B 闭合框", font=font(30, True), fill=PAPER_TEXT)
    draw.text(
        (48, 78),
        "同一短签、同一拼接：selected 保留橄榄后纸，并将闭合内框切换为永久任务类型色",
        font=font(16),
        fill=MUTED_TEXT,
    )

    hover = runtime_copy(default)
    chosen = runtime_copy(selected, underlay)
    for x, label, asset in (
        (48, "HOVER｜中性闭合框", hover),
        (760, "SELECTED｜橄榄后纸 + 类型色闭合框", chosen),
    ):
        stage = checker((660, 248), 20)
        stage.alpha_composite(asset.resize((556, 160), Image.Resampling.NEAREST), (52, 44))
        board.alpha_composite(stage, (x, 132))
        draw.text((x, 398), label, font=font(18, True), fill=PAPER_TEXT)

    for x, label, asset in (
        (48, "1× HOVER", hover),
        (430, "1× SELECTED", chosen),
    ):
        stage = checker((334, 160), 16)
        stage.alpha_composite(asset, (28, 40))
        board.alpha_composite(stage, (x, 470))
        draw.text((x, 648), label, font=font(16, True), fill=PAPER_TEXT)

    draw.text((820, 486), "运行时图层", font=font(18, True), fill=PAPER_TEXT)
    notes = [
        "前：selected 类型色框短签",
        "后：既有橄榄 selected 后纸",
        "不动：图标、文字、右端帽、尺寸、锚点",
        "过渡：中性框 ↔ 类型色框互补淡变",
    ]
    for index, line in enumerate(notes):
        draw.text((820, 530 + index * 34), line, font=font(15), fill=GOOD)
    return board


def build_runtime_gif() -> int:
    frame_paths = sorted(STATE_FRAME_DIR.glob("frame_*.png"))
    if not frame_paths:
        return 0
    frames = [
        Image.open(path).convert("RGBA").resize((740, 344), Image.Resampling.NEAREST)
        for path in frame_paths
    ]
    frames[0].save(
        STATE_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=20,
        loop=0,
        disposal=2,
        optimize=False,
    )
    return len(frames)


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    default_chroma = Image.open(DEFAULT_CHROMA)
    imagegen_raw = Image.open(IMAGEGEN_RAW)
    selected_chroma, selected_mask, constrain_metrics = constrain_imagegen_frame(default_chroma, imagegen_raw)
    selected_chroma.save(SELECTED_CHROMA)
    selected_mask.save(SELECTED_MASK)

    default_source, default_key = remove_connected_chroma(default_chroma)
    selected_source, selected_key = remove_connected_chroma(selected_chroma)
    underlay_source, underlay_key = remove_connected_chroma(Image.open(UNDERLAY_CHROMA))
    pin_source, pin_key = remove_connected_chroma(Image.open(PIN_CHROMA))
    default_source.save(DEFAULT_ALPHA)
    selected_source.save(SELECTED_ALPHA)
    underlay_source.save(UNDERLAY_ALPHA)
    pin_source.save(PIN_ALPHA)

    left_pad = compound_left_pad(default_source)
    default_3x, default_1x, default_metrics = build_runtime_frames(DEFAULT_ALPHA, left_pad)
    selected_3x, selected_1x, selected_metrics = build_runtime_frames(SELECTED_ALPHA, left_pad)
    underlay_3x, underlay_1x, underlay_metrics = build_runtime_frames(
        UNDERLAY_ALPHA, compound_left_pad(underlay_source)
    )
    pin_3x, pin_1x, pin_metrics = build_pin_only_frame(pin_source)

    for image, path in (
        (default_3x, DEFAULT_3X),
        (default_1x, DEFAULT_1X),
        (selected_3x, SELECTED_3X),
        (selected_1x, SELECTED_1X),
        (underlay_3x, UNDERLAY_3X),
        (underlay_1x, UNDERLAY_1X),
        (pin_3x, PIN_3X),
        (pin_1x, PIN_1X),
        (default_3x, FIXTURE_DIR / DEFAULT_3X.name),
        (selected_3x, FIXTURE_DIR / SELECTED_3X.name),
        (underlay_3x, FIXTURE_DIR / UNDERLAY_3X.name),
        (pin_3x, FIXTURE_DIR / PIN_3X.name),
    ):
        image.save(path)

    build_qa(default_1x, selected_1x, underlay_1x).save(QA_BOARD)
    gif_source_frames = build_runtime_gif()
    alpha_equal = np.array_equal(np.asarray(default_source.getchannel("A")), np.asarray(selected_source.getchannel("A")))
    METADATA.write_text(
        json.dumps(
            {
                "id": "region_task_permanent_selected_type_frame_v6",
                "status": "runtime_candidate_pending_user_visual_review",
                "production_integration": False,
                "scope": "permanent singleton local experiment only",
                "selected_contract": {
                    "idle": "B pin-only",
                    "hover": "B neutral closed frame compound",
                    "selected": "existing olive underlay + B permanent olive closed frame compound",
                    "frame_color": "#7F8A47",
                    "hover_to_selected_target_ms": 96,
                    "hover_to_selected_gif_quantized_ms": 100,
                    "selected_to_hover_target_ms": 80,
                    "easing": "cubic_ease_out",
                    "alpha_crossfade": "neutral=1-t; selected=t; underlay=t",
                },
                "runtime_contract": {
                    "pin": [64, 80],
                    "compound": [278, 80],
                    "hit": [72, 80],
                    "anchor": [36, 76],
                    "caption_rect": [78, 4, 200, 72],
                },
                "imagegen": {
                    "mode": "built-in precise-object-edit",
                    "raw_source": str(IMAGEGEN_RAW.relative_to(ROOT)).replace("\\", "/"),
                    "constraint_method": "generated olive material transferred through original B-frame coverage",
                    "prompt_summary": "change only B closed frame to permanent olive #7F8A47",
                },
                "metrics": {
                    "constrain": constrain_metrics,
                    "default": default_metrics,
                    "selected_front": selected_metrics,
                    "selected_underlay": underlay_metrics,
                    "pin_only": pin_metrics,
                    "alpha_masks_identical_default_vs_selected": alpha_equal,
                    "key_removal": {
                        "default": default_key,
                        "selected_front": selected_key,
                        "selected_underlay": underlay_key,
                        "pin_only": pin_key,
                    },
                    "runtime_gif_source_frames": gif_source_frames,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(QA_BOARD)
    print(METADATA)
    if gif_source_frames:
        print(STATE_GIF)


if __name__ == "__main__":
    main()
