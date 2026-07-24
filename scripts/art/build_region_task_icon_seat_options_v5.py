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
    build_pin_only_frame,
    checker,
    font,
    remove_connected_chroma,
)


SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "icon-seat-options-v5"
FIXTURE_DIR = ROOT / "gd_project" / "tests" / "fixtures" / "region_task_icon_seat_options_v5"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-icon-seat-options-v5"
QA_BOARD = SCREENSHOT_DIR / "01-icon-seat-options-imagegen-1x-qa.png"
METADATA = SOURCE_DIR / "icon-seat-options-v5.json"
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


OPTIONS = [
    {
        "id": "a_open_bottom_frame",
        "title": "A｜下开口切角框",
        "subtitle": "推荐：有完整承托，但不形成闭合双框",
        "source": "01-option-a-open-bottom-frame-chroma.png",
        "stem": "rt-task-pin-permanent-icon-seat-a-open-bottom-v5",
    },
    {
        "id": "b_closed_octagon_groove",
        "title": "B｜闭合八边纸槽",
        "subtitle": "线框最完整；存在外框套内框的偏重风险",
        "source": "02-option-b-closed-octagon-groove-chroma.png",
        "stem": "rt-task-pin-permanent-icon-seat-b-closed-v5",
    },
    {
        "id": "c_tonal_paper_window",
        "title": "C｜微差色切角纸窗",
        "subtitle": "缩放最稳定；线框感比 A / B 更弱",
        "source": "03-option-c-tonal-paper-window-chroma.png",
        "stem": "rt-task-pin-permanent-icon-seat-c-window-v5",
    },
]


def add_runtime_icon(pin: Image.Image, scale: int = 1) -> Image.Image:
    result = pin.copy().convert("RGBA")
    atlas = Image.open(ICON_ATLAS).convert("RGBA")
    icon_3x = atlas.crop((0, 0, 84, 84))
    icon = icon_3x if scale == 3 else icon_3x.resize((28, 28), Image.Resampling.LANCZOS)
    result.alpha_composite(icon, (18 * scale, 14 * scale))
    return result


def build_qa(rows: list[dict]) -> Image.Image:
    board = Image.new("RGBA", (1600, 900), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "常驻任务 pin 图标座｜三种真实生图候选", font=font(30, True), fill=PAPER_TEXT)
    draw.text(
        (48, 78),
        "同一 64×80 pin、同一 28×28 动态图标；大图只做 4×最近邻放大，主判断仍看右下角原生 1×",
        font=font(16),
        fill=MUTED_TEXT,
    )

    card_width = 472
    for index, row in enumerate(rows):
        x = 48 + index * 508
        draw.rounded_rectangle((x, 130, x + card_width, 758), radius=10, fill=(15, 42, 54, 255), outline=(74, 105, 111, 255), width=2)
        draw.text((x + 24, 156), row["title"], font=font(22, True), fill=PAPER_TEXT)
        draw.text((x + 24, 194), row["subtitle"], font=font(14), fill=MUTED_TEXT)

        stage = checker((424, 404), 20)
        enlarged = row["with_icon"].resize((256, 320), Image.Resampling.NEAREST)
        stage.alpha_composite(enlarged, (84, 36))
        board.alpha_composite(stage, (x + 24, 236))

        draw.text((x + 24, 664), "原生 1×", font=font(14, True), fill=PAPER_TEXT)
        native_bg = Image.new("RGBA", (112, 96), (46, 66, 49, 255))
        native_bg.alpha_composite(row["with_icon"], (24, 8))
        board.alpha_composite(native_bg, (x + 112, 644))
        draw.rectangle((x + 111, 643, x + 224, 740), outline=(109, 137, 128, 255), width=1)

    draw.text((48, 804), "冻结项：外轮廓 / icon bbox / anchor / hit / compound / selected 背纸 / 动效均不变", font=font(17, True), fill=GOOD)
    draw.text((48, 844), "本板是方案比较，不是三种状态；用户选定后才把同一图标座同步到 idle / hover / selected 美术帧。", font=font(15), fill=MUTED_TEXT)
    return board


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    metadata = {
        "id": "region_task_permanent_icon_seat_options_v5",
        "status": "visual_options_pending_user_selection",
        "production_integration": False,
        "runtime_contract": {"pin": [64, 80], "icon": [18, 14, 28, 28]},
        "options": [],
    }
    for option in OPTIONS:
        chroma_path = SOURCE_DIR / option["source"]
        alpha_path = SOURCE_DIR / option["source"].replace("-chroma.png", "-alpha.png")
        alpha, key_metrics = remove_connected_chroma(Image.open(chroma_path))
        alpha.save(alpha_path)
        frame_3x, frame_1x, metrics = build_pin_only_frame(alpha)
        frame_3x_path = SOURCE_DIR / f"{option['stem']}-3x.png"
        frame_1x_path = SOURCE_DIR / f"{option['stem']}-1x.png"
        frame_3x.save(frame_3x_path)
        frame_1x.save(frame_1x_path)
        frame_3x.save(FIXTURE_DIR / frame_3x_path.name)
        with_icon = add_runtime_icon(frame_1x)
        with_icon.save(SOURCE_DIR / f"{option['stem']}-1x-with-runtime-icon.png")
        rows.append({**option, "with_icon": with_icon})
        metadata["options"].append(
            {
                "id": option["id"],
                "source": str(chroma_path.relative_to(ROOT)).replace("\\", "/"),
                "frame_3x": str(frame_3x_path.relative_to(ROOT)).replace("\\", "/"),
                "frame_1x": str(frame_1x_path.relative_to(ROOT)).replace("\\", "/"),
                "metrics": metrics,
                "key_removal": key_metrics,
            }
        )

    build_qa(rows).save(QA_BOARD)
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(QA_BOARD)
    print(METADATA)


if __name__ == "__main__":
    main()
