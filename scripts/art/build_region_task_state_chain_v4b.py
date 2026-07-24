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


SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v4b-single-probe"
DEFAULT_CHROMA = SOURCE_DIR / "01-permanent-default-right-compound-source-v4b-chroma.png"
SELECTED_CHROMA = SOURCE_DIR / "02-permanent-selected-right-compound-source-v4b-chroma.png"
PIN_CHROMA = SOURCE_DIR / "03-permanent-default-pin-only-source-v4b-chroma.png"
DEFAULT_ALPHA = SOURCE_DIR / "01-permanent-default-right-compound-source-v4b-alpha.png"
SELECTED_ALPHA = SOURCE_DIR / "02-permanent-selected-right-compound-source-v4b-alpha.png"
PIN_ALPHA = SOURCE_DIR / "03-permanent-default-pin-only-source-v4b-alpha.png"

DEFAULT_3X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v4b-3x.png"
DEFAULT_1X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v4b-1x.png"
SELECTED_3X = SOURCE_DIR / "rt-task-compound-permanent-selected-right-v4b-3x.png"
SELECTED_1X = SOURCE_DIR / "rt-task-compound-permanent-selected-right-v4b-1x.png"
PIN_3X = SOURCE_DIR / "rt-task-pin-permanent-default-v4b-3x.png"
PIN_1X = SOURCE_DIR / "rt-task-pin-permanent-default-v4b-1x.png"

FIXTURE_DIR = ROOT / "gd_project" / "tests" / "fixtures" / "region_task_compound_probe_v4b"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-state-chain-v4b"
QA_BOARD = SCREENSHOT_DIR / "01-v4-v4b-selected-and-inner-line-qa.png"
STATE_FRAME_DIR = SCREENSHOT_DIR / "frames-state-chain-v4b"
STATE_GIF = SCREENSHOT_DIR / "03-hover-selected-runtime-demo-v4b.gif"
METADATA = SOURCE_DIR / "state-chain-v4b.json"

OLD_SELECTED_1X = (
    ROOT
    / "design"
    / "art-direction"
    / "region-task-board"
    / "runtime-preflight-v4-single-probe"
    / "rt-task-compound-permanent-selected-right-v4-1x.png"
)


def compound_left_pad(source: Image.Image) -> int:
    bbox = alpha_bbox(source)
    cropped = source.crop(bbox)
    scaled_width = round(cropped.width * 240 / cropped.height)
    scaled = cropped.resize((scaled_width, 240), Image.Resampling.LANCZOS)
    return round(108 - tip_center_x(scaled))


def build_qa(old_selected: Image.Image, default: Image.Image, selected: Image.Image, pin: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1600, 820), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "常驻右挂 v4b 定向修正｜selected 强度 + 内圈清理", font=font(30, True), fill=PAPER_TEXT)
    draw.text((48, 78), "同一结构，不是新方案：删除三态闭合黑线；selected 只增强左上/左/左下美术后衬", font=font(17), fill=MUTED_TEXT)

    for x, label, image in (
        (48, "旧 v4 SELECTED｜内圈断续、后衬偏弱", old_selected),
        (820, "新 v4b SELECTED｜无内圈、后衬增强", selected),
    ):
        cell = checker((700, 256), 24)
        cell.alpha_composite(image.resize((556, 160), Image.Resampling.NEAREST), (24, 48))
        board.alpha_composite(cell, (x, 132))
        draw.text((x, 408), label, font=font(18, True), fill=PAPER_TEXT)

    pin_cell = checker((320, 296), 24)
    pin_cell.alpha_composite(pin.resize((256, 320), Image.Resampling.NEAREST), (32, -12))
    board.alpha_composite(pin_cell, (48, 468))
    draw.text((48, 776), "IDLE pin-only｜内圈统一删除", font=font(18, True), fill=PAPER_TEXT)

    default_cell = checker((700, 296), 24)
    default_cell.alpha_composite(default.resize((556, 160), Image.Resampling.NEAREST), (24, 64))
    board.alpha_composite(default_cell, (430, 468))
    draw.text((430, 776), "HOVER default compound｜内圈统一删除", font=font(18, True), fill=PAPER_TEXT)
    draw.text((1160, 528), "冻结项", font=font(18, True), fill=PAPER_TEXT)
    notes = [
        "✓ compound / 共享肩不动",
        "✓ icon / 文字坐标不动",
        "✓ 右端类型帽不动",
        "✓ 程序不绘制选中框",
    ]
    for index, line in enumerate(notes):
        draw.text((1160, 574 + index * 40), line, font=font(15), fill=GOOD)
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

    default_pad = compound_left_pad(default_source)
    selected_pad = compound_left_pad(selected_source)
    default_3x, default_1x, default_metrics = build_runtime_frames(DEFAULT_ALPHA, default_pad)
    selected_3x, selected_1x, selected_metrics = build_runtime_frames(SELECTED_ALPHA, selected_pad)
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

    old_selected = Image.open(OLD_SELECTED_1X).convert("RGBA")
    build_qa(old_selected, default_1x, selected_1x, pin_1x).save(QA_BOARD)
    gif_source_frames = build_state_chain_gif()
    METADATA.write_text(
        json.dumps(
            {
                "id": "region_task_permanent_right_state_chain_v4b",
                "status": "runtime_candidate_pending_user_visual_review",
                "production_integration": False,
                "corrections": [
                    "remove the unstable closed inner keyline from idle, hover and selected",
                    "increase selected olive backing visibility around upper-left, left and lower-left head only",
                ],
                "runtime_contract": {
                    "pin": [64, 80],
                    "compound": [278, 80],
                    "hit": [72, 80],
                    "anchor": [36, 76],
                    "caption_rect": [78, 4, 200, 72],
                },
                "metrics": {
                    "default": default_metrics,
                    "selected": selected_metrics,
                    "pin_only": pin_metrics,
                    "key_removal": {
                        "default": default_key,
                        "selected": selected_key,
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
    print(DEFAULT_3X)
    print(SELECTED_3X)
    print(PIN_3X)
    print(QA_BOARD)
    if gif_source_frames:
        print(STATE_GIF)


if __name__ == "__main__":
    main()
