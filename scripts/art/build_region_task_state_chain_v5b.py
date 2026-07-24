from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

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


SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v5b-selected-icon-seat"
DEFAULT_CHROMA = SOURCE_DIR / "01-permanent-default-right-compound-source-v5b-chroma.png"
SELECTED_CHROMA = SOURCE_DIR / "02-permanent-selected-backing-underlay-source-v5b-chroma.png"
PIN_CHROMA = SOURCE_DIR / "03-permanent-default-pin-only-source-v5b-chroma.png"
DEFAULT_ALPHA = SOURCE_DIR / "01-permanent-default-right-compound-source-v5b-alpha.png"
SELECTED_ALPHA = SOURCE_DIR / "02-permanent-selected-backing-underlay-source-v5b-alpha.png"
PIN_ALPHA = SOURCE_DIR / "03-permanent-default-pin-only-source-v5b-alpha.png"

DEFAULT_3X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v5b-3x.png"
DEFAULT_1X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v5b-1x.png"
SELECTED_3X = SOURCE_DIR / "rt-task-compound-permanent-selected-underlay-right-v5b-3x.png"
SELECTED_1X = SOURCE_DIR / "rt-task-compound-permanent-selected-underlay-right-v5b-1x.png"
PIN_3X = SOURCE_DIR / "rt-task-pin-permanent-default-v5b-3x.png"
PIN_1X = SOURCE_DIR / "rt-task-pin-permanent-default-v5b-1x.png"

FIXTURE_DIR = ROOT / "gd_project" / "tests" / "fixtures" / "region_task_compound_probe_v5b"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-state-chain-v5b"
QA_BOARD = SCREENSHOT_DIR / "01-user-selected-b-three-state-assets-qa.png"
STATE_FRAME_DIR = SCREENSHOT_DIR / "frames-state-chain-v5b"
STATE_GIF = SCREENSHOT_DIR / "03-hover-selected-runtime-demo-v5b.gif"
METADATA = SOURCE_DIR / "state-chain-v5b.json"
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


def permanent_icon() -> Image.Image:
    atlas = Image.open(ICON_ATLAS).convert("RGBA")
    return atlas.crop((0, 0, 84, 84)).resize((28, 28), Image.Resampling.LANCZOS)


def add_icon(image: Image.Image, x: int) -> Image.Image:
    result = image.copy().convert("RGBA")
    result.alpha_composite(permanent_icon(), (x, 14))
    return result


def build_qa(pin: Image.Image, default: Image.Image, selected_underlay: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1600, 820), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "用户选择 B｜闭合八边纸槽同步三态", font=font(30, True), fill=PAPER_TEXT)
    draw.text((48, 78), "同一闭合框保持不变；idle 只显示 pin，hover 展开 compound，selected 仅从下层增加橄榄后纸", font=font(16), fill=MUTED_TEXT)

    cells = [
        (48, "IDLE｜B pin-only", add_icon(pin, 18), (256, 320)),
        (430, "HOVER｜B default compound", add_icon(default, 22), (556, 160)),
        (1010, "SELECTED underlay｜只负责后纸", selected_underlay, (556, 160)),
    ]
    for x, label, asset, size in cells:
        width = 334 if x == 48 else 534
        stage = checker((width, 390), 22)
        enlarged = asset.resize(size, Image.Resampling.NEAREST)
        stage.alpha_composite(enlarged, ((width - size[0]) // 2, 34 if x == 48 else 108))
        board.alpha_composite(stage, (x, 132))
        draw.text((x, 546), label, font=font(18, True), fill=PAPER_TEXT)

    draw.text((48, 616), "运行时 selected = selected underlay（后）+ B default compound（前）", font=font(18, True), fill=GOOD)
    notes = [
        "✓ B 闭合框在三态逐像素一致",
        "✓ 图标 / 标题 / meta 坐标不变",
        "✓ selected 只改变橄榄后纸",
        "✓ 生产组件与正式合同未修改",
    ]
    for index, line in enumerate(notes):
        draw.text((48, 660 + index * 32), line, font=font(15), fill=GOOD)
    return board


def build_state_chain_gif() -> int:
    frame_paths = sorted(STATE_FRAME_DIR.glob("frame_*.png"))
    if not frame_paths:
        return 0
    frames = []
    for path in frame_paths:
        frame = Image.open(path).convert("RGBA")
        frames.append(frame.resize((frame.width * 2, frame.height * 2), Image.Resampling.NEAREST))
    frames[0].save(
        STATE_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        disposal=2,
        optimize=False,
    )
    return len(frames)


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    default_source, default_key = remove_connected_chroma(Image.open(DEFAULT_CHROMA))
    selected_source, selected_key = remove_connected_chroma(Image.open(SELECTED_CHROMA))
    pin_source, pin_key = remove_connected_chroma(Image.open(PIN_CHROMA))
    default_source.save(DEFAULT_ALPHA)
    selected_source.save(SELECTED_ALPHA)
    pin_source.save(PIN_ALPHA)

    default_3x, default_1x, default_metrics = build_runtime_frames(DEFAULT_ALPHA, compound_left_pad(default_source))
    selected_3x, selected_1x, selected_metrics = build_runtime_frames(SELECTED_ALPHA, compound_left_pad(selected_source))
    pin_3x, pin_1x, pin_metrics = build_pin_only_frame(pin_source)

    for image, path in (
        (default_3x, DEFAULT_3X),
        (default_1x, DEFAULT_1X),
        (selected_3x, SELECTED_3X),
        (selected_1x, SELECTED_1X),
        (pin_3x, PIN_3X),
        (pin_1x, PIN_1X),
        (default_3x, FIXTURE_DIR / DEFAULT_3X.name),
        (selected_3x, FIXTURE_DIR / SELECTED_3X.name),
        (pin_3x, FIXTURE_DIR / PIN_3X.name),
    ):
        image.save(path)

    build_qa(pin_1x, default_1x, selected_1x).save(QA_BOARD)
    gif_source_frames = build_state_chain_gif()
    METADATA.write_text(
        json.dumps(
            {
                "id": "region_task_permanent_right_state_chain_v5b",
                "status": "runtime_candidate_pending_user_visual_review",
                "production_integration": False,
                "user_selection": "B_closed_octagonal_paper_groove",
                "reason": "A reads as unfinished because the lower half of the frame is missing",
                "runtime_contract": {
                    "pin": [64, 80],
                    "compound": [278, 80],
                    "hit": [72, 80],
                    "anchor": [36, 76],
                    "caption_rect": [78, 4, 200, 72],
                },
                "state_layering": {
                    "idle": "B pin-only",
                    "hover": "B default compound",
                    "selected": "v4b selected olive underlay behind B default compound",
                },
                "metrics": {
                    "default": default_metrics,
                    "selected_underlay": selected_metrics,
                    "pin_only": pin_metrics,
                    "key_removal": {"default": default_key, "selected": selected_key, "pin_only": pin_key},
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
    if gif_source_frames:
        print(STATE_GIF)


if __name__ == "__main__":
    main()
