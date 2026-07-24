from __future__ import annotations

import colorsys
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v6-selected-type-frame"
OUTPUT_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-production-v7-b-type-frame"
FRAME_DIR = OUTPUT_DIR / "frames"
PRODUCTION_DIR = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task" / "v2" / "pin_compound_v7"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-compound-production-v7"
RUNTIME_FRAME_DIR = SCREENSHOT_DIR / "frames-runtime-v7"
RUNTIME_GIF = SCREENSHOT_DIR / "04-hover-selected-runtime-v7.gif"

DEFAULT_SOURCE = SOURCE_DIR / "rt-task-compound-permanent-default-right-v6-3x.png"
SELECTED_SOURCE = SOURCE_DIR / "rt-task-compound-permanent-selected-type-frame-right-v6-3x.png"
UNDERLAY_SOURCE = SOURCE_DIR / "rt-task-compound-permanent-selected-underlay-right-v6-3x.png"
PIN_SOURCE = SOURCE_DIR / "rt-task-pin-permanent-default-v6-3x.png"
ICON_ATLAS = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task" / "v2" / "pin_slice" / "rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png"
BADGE_SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v2" / "frames"

RIGHT_HOVER = "rt-task-compound-right-hover-b-type-v7-atlas-3x.png"
LEFT_HOVER = "rt-task-compound-left-hover-b-type-v7-atlas-3x.png"
RIGHT_SELECTED = "rt-task-compound-right-selected-front-b-type-v7-atlas-3x.png"
LEFT_SELECTED = "rt-task-compound-left-selected-front-b-type-v7-atlas-3x.png"
RIGHT_UNDERLAY = "rt-task-compound-right-selected-underlay-b-type-v7-atlas-3x.png"
LEFT_UNDERLAY = "rt-task-compound-left-selected-underlay-b-type-v7-atlas-3x.png"
RIGHT_FOCUS = "rt-task-compound-right-focus-b-type-v7-atlas-3x.png"
LEFT_FOCUS = "rt-task-compound-left-focus-b-type-v7-atlas-3x.png"
PIN_OUTPUT = "rt-task-pin-b-closed-v7-3x.png"
BADGE_ATLAS = "rt-task-state-badges-v7-atlas-3x.png"

QA_BOARD = SCREENSHOT_DIR / "00-four-kind-asset-matrix-v7.png"
METADATA = OUTPUT_DIR / "compound-production-v7.json"

FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")

KINDS = [
    {"id": "permanent", "name": "常驻", "color": "#7F8A47", "icon": 0, "title": "罗斯威尔档案残页", "meta": "常驻调查 · 1天"},
    {"id": "chain", "name": "连续", "color": "#34767A", "icon": 1, "title": "M330 末班车空白段", "meta": "连续追踪 · 2天"},
    {"id": "hidden", "name": "隐藏", "color": "#445967", "icon": 2, "title": "灵视：黑色方尖碑回声", "meta": "灵视异常 · 3天"},
    {"id": "temp", "name": "限时", "color": "#886A40", "icon": 3, "title": "突发：雷达异常光点", "meta": "限时截稿 · 2天"},
]

INK = (23, 37, 42)
BG = (5, 29, 43, 255)
PAPER_TEXT = (236, 226, 202, 255)
MUTED_TEXT = (174, 188, 154, 255)
GOOD = (99, 166, 125, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    source = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(source), size=size)


def build_runtime_gif() -> int:
    frame_paths = sorted(RUNTIME_FRAME_DIR.glob("frame_*.png"))
    if not frame_paths:
        return 0
    # Godot 4.6.3 SubViewport readback alternates its two render buffers on this
    # Windows runner. The even frames are the completed buffer; keeping them at
    # 33 ms preserves the real ~60 Hz timing without introducing blank frames.
    frame_paths = [path for path in frame_paths if int(path.stem.rsplit("_", 1)[-1]) % 2 == 0]
    frames = [
        Image.open(path).convert("RGBA").resize((780, 248), Image.Resampling.NEAREST)
        for path in frame_paths
    ]
    frames[0].save(
        RUNTIME_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=33,
        loop=0,
        disposal=2,
        optimize=False,
    )
    return len(frames)


def hex_rgb(value: str) -> np.ndarray:
    value = value.lstrip("#")
    return np.array([int(value[index:index + 2], 16) for index in (0, 2, 4)], dtype=np.float32)


def frame_coverage(default: Image.Image, selected: Image.Image) -> np.ndarray:
    a = np.asarray(default.convert("RGBA")).astype(np.float32)
    b = np.asarray(selected.convert("RGBA")).astype(np.float32)
    difference = np.max(np.abs(a[:, :, :3] - b[:, :, :3]), axis=2)
    coverage = np.clip((difference - 1.0) / 28.0, 0.0, 1.0)
    gate = np.zeros_like(coverage)
    gate[:, :240] = 1.0
    return coverage * gate * np.minimum(a[:, :, 3], b[:, :, 3]) / 255.0


def accent_coverage(image: Image.Image, gate: tuple[int, int, int, int] | None = None) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA")).astype(np.float32)
    rgb = rgba[:, :, :3] / 255.0
    maximum = np.max(rgb, axis=2)
    minimum = np.min(rgb, axis=2)
    saturation = np.zeros_like(maximum)
    np.divide(maximum - minimum, maximum, out=saturation, where=maximum > 0.001)
    blue = rgba[:, :, 2]
    coverage = np.clip((saturation - 0.16) / 0.22, 0.0, 1.0)
    coverage *= np.clip((205.0 - blue) / 55.0, 0.0, 1.0)
    coverage *= rgba[:, :, 3] / 255.0
    if gate is not None:
        x0, y0, x1, y1 = gate
        spatial = np.zeros_like(coverage)
        spatial[y0:y1, x0:x1] = 1.0
        coverage *= spatial
    return coverage


def recolor(image: Image.Image, coverage: np.ndarray, target_rgb: np.ndarray) -> tuple[Image.Image, list[float]]:
    rgba = np.asarray(image.convert("RGBA")).astype(np.float32)
    source = rgba[:, :, :3]
    core = coverage > 0.82
    if int(core.sum()) < 30:
        raise RuntimeError("Accent mask has too few core pixels")
    source_median = np.median(source[core], axis=0)
    material = target_rgb[None, None, :] + (source - source_median[None, None, :]) * 0.72
    result = source * (1.0 - coverage[:, :, None]) + material * coverage[:, :, None]
    for _index in range(3):
        result_median = np.median(result[core], axis=0)
        correction = target_rgb - result_median
        material += correction[None, None, :]
        result = source * (1.0 - coverage[:, :, None]) + material * coverage[:, :, None]
    output = rgba.copy()
    output[:, :, :3] = np.clip(np.rint(result), 0, 255)
    final_median = np.median(output[:, :, :3][core], axis=0)
    return Image.fromarray(output.astype(np.uint8), mode="RGBA"), [round(float(value), 2) for value in final_median]


def mirror_left(image: Image.Image) -> Image.Image:
    mirrored = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    result = Image.new("RGBA", (840, 240), (0, 0, 0, 0))
    result.alpha_composite(mirrored, (6, 0))
    return result


def atlas(frames: list[Image.Image]) -> Image.Image:
    result = Image.new("RGBA", (sum(frame.width for frame in frames), max(frame.height for frame in frames)), (0, 0, 0, 0))
    cursor = 0
    for frame in frames:
        result.alpha_composite(frame, (cursor, 0))
        cursor += frame.width
    return result


def save_asset(image: Image.Image, name: str) -> None:
    image.save(OUTPUT_DIR / name)
    image.save(PRODUCTION_DIR / name)


def icon_for(spec: dict) -> Image.Image:
    source = Image.open(ICON_ATLAS).convert("RGBA")
    index = int(spec["icon"])
    return source.crop((index * 84, 0, (index + 1) * 84, 84)).resize((28, 28), Image.Resampling.LANCZOS)


def compose_runtime(front: Image.Image, spec: dict, underlay: Image.Image | None = None, orientation: str = "right", badge: Image.Image | None = None) -> Image.Image:
    runtime_width = 278 if orientation == "right" else 280
    canvas = Image.new("RGBA", (runtime_width, 80), (0, 0, 0, 0))
    if underlay is not None:
        canvas.alpha_composite(underlay.resize((runtime_width, 80), Image.Resampling.LANCZOS))
    canvas.alpha_composite(front.resize((runtime_width, 80), Image.Resampling.LANCZOS))
    hit_x = 0 if orientation == "right" else 208
    label_x = 78 if orientation == "right" else 0
    canvas.alpha_composite(icon_for(spec), (hit_x + 22, 14))
    if badge is not None:
        canvas.alpha_composite(badge.resize((24, 24), Image.Resampling.LANCZOS), (hit_x + 48, 4))
    draw = ImageDraw.Draw(canvas)
    draw.text((label_x + 14, 9), spec["title"], font=font(15, True), fill=(23, 37, 42, 255))
    draw.text((label_x + 14, 38), spec["meta"], font=font(12), fill=(64, 81, 87, 255))
    return canvas


def checker(size: tuple[int, int], step: int = 14) -> Image.Image:
    image = Image.new("RGBA", size, (26, 51, 64, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2 == 0:
                draw.rectangle((x, y, min(size[0] - 1, x + step - 1), min(size[1] - 1, y + step - 1)), fill=(36, 67, 80, 255))
    return image


def build_qa(frames: dict, badges: list[Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1800, 1040), BG)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "区域任务 compound v7｜四类型正式资产矩阵", font=font(30, True), fill=PAPER_TEXT)
    draw.text((42, 72), "同一 B 闭合母结构；hover 中性框，selected 类型色框 + 外后纸，focus 深墨框", font=font(16), fill=MUTED_TEXT)
    row_specs = [("HOVER", "hover"), ("SELECTED", "selected"), ("FOCUS", "focus")]
    for column, spec in enumerate(KINDS):
        x = 42 + column * 430
        draw.text((x, 118), "%s｜%s" % (spec["name"], spec["color"]), font=font(18, True), fill=PAPER_TEXT)
        for row, (label, state) in enumerate(row_specs):
            y = 158 + row * 220
            stage = checker((390, 150))
            front = frames[(spec["id"], state, "right")]
            underlay = frames[(spec["id"], "underlay", "right")] if state == "selected" else None
            sample = compose_runtime(front, spec, underlay)
            stage.alpha_composite(sample, (42, 34))
            board.alpha_composite(stage, (x, y))
            draw.text((x, y + 164), label, font=font(15, True), fill=GOOD)

    draw.text((42, 822), "左挂 clamp + 美术状态徽签", font=font(19, True), fill=PAPER_TEXT)
    left_sample = compose_runtime(
        frames[("hidden", "selected", "left")],
        KINDS[2],
        frames[("hidden", "underlay", "left")],
        "left",
        badges[2],
    )
    stage = checker((420, 150))
    stage.alpha_composite(left_sample, (70, 34))
    board.alpha_composite(stage, (42, 862))
    draw.text((510, 850), "ASSIGNED", font=font(14, True), fill=PAPER_TEXT)
    draw.text((650, 850), "URGENT", font=font(14, True), fill=PAPER_TEXT)
    draw.text((790, 850), "LOCKED / DISABLED", font=font(14, True), fill=PAPER_TEXT)
    for index, badge in enumerate(badges):
        shown = badge.resize((96, 96), Image.Resampling.NEAREST)
        board.alpha_composite(shown, (510 + index * 140, 886))
    draw.text((1050, 870), "冻结项", font=font(18, True), fill=PAPER_TEXT)
    notes = [
        "✓ right 278×80 / left 280×80",
        "✓ anchor in hit = 36/76",
        "✓ default / selected / focus 前层 alpha 一致",
        "✓ 状态徽签为位图，不再由 Polygon2D / Line2D 绘制",
    ]
    for index, line in enumerate(notes):
        draw.text((1050, 910 + index * 28), line, font=font(14), fill=GOOD)
    return board


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    default = Image.open(DEFAULT_SOURCE).convert("RGBA")
    selected = Image.open(SELECTED_SOURCE).convert("RGBA")
    underlay = Image.open(UNDERLAY_SOURCE).convert("RGBA")
    pin = Image.open(PIN_SOURCE).convert("RGBA")
    frame_mask = frame_coverage(default, selected)
    default_cap_mask = accent_coverage(default, (760, 0, 834, 240))
    selected_cap_mask = accent_coverage(selected, (760, 0, 834, 240))
    underlay_accent_mask = accent_coverage(underlay)

    frames: dict[tuple[str, str, str], Image.Image] = {}
    medians: dict[str, dict] = {}
    for spec in KINDS:
        kind = str(spec["id"])
        target = hex_rgb(str(spec["color"]))
        hover_right, hover_cap_median = recolor(default, default_cap_mask, target)
        selected_right, selected_frame_median = recolor(selected, frame_mask, target)
        selected_right, selected_cap_median = recolor(selected_right, selected_cap_mask, target)
        underlay_right, underlay_median = recolor(underlay, underlay_accent_mask, target)
        focus_right, _focus_cap_median = recolor(default, default_cap_mask, target)
        focus_right, focus_frame_median = recolor(focus_right, frame_mask, np.array(INK, dtype=np.float32))

        for state, right in (
            ("hover", hover_right),
            ("selected", selected_right),
            ("underlay", underlay_right),
            ("focus", focus_right),
        ):
            left = mirror_left(right)
            frames[(kind, state, "right")] = right
            frames[(kind, state, "left")] = left
            right.save(FRAME_DIR / f"compound-right-{state}-{kind}-v7-3x.png")
            left.save(FRAME_DIR / f"compound-left-{state}-{kind}-v7-3x.png")

        medians[kind] = {
            "target": [int(value) for value in target],
            "hover_cap": hover_cap_median,
            "selected_frame": selected_frame_median,
            "selected_cap": selected_cap_median,
            "selected_underlay": underlay_median,
            "focus_frame": focus_frame_median,
        }

    state_files = {
        RIGHT_HOVER: [frames[(spec["id"], "hover", "right")] for spec in KINDS],
        LEFT_HOVER: [frames[(spec["id"], "hover", "left")] for spec in KINDS],
        RIGHT_SELECTED: [frames[(spec["id"], "selected", "right")] for spec in KINDS],
        LEFT_SELECTED: [frames[(spec["id"], "selected", "left")] for spec in KINDS],
        RIGHT_UNDERLAY: [frames[(spec["id"], "underlay", "right")] for spec in KINDS],
        LEFT_UNDERLAY: [frames[(spec["id"], "underlay", "left")] for spec in KINDS],
        RIGHT_FOCUS: [frames[(spec["id"], "focus", "right")] for spec in KINDS],
        LEFT_FOCUS: [frames[(spec["id"], "focus", "left")] for spec in KINDS],
    }
    for name, ordered in state_files.items():
        save_asset(atlas(ordered), name)
    save_asset(pin, PIN_OUTPUT)

    badges = [
        Image.open(BADGE_SOURCE_DIR / "state-badge-assigned-v2-3x.png").convert("RGBA"),
        Image.open(BADGE_SOURCE_DIR / "state-badge-urgent-v2-3x.png").convert("RGBA"),
        Image.open(BADGE_SOURCE_DIR / "state-badge-locked-v2-3x.png").convert("RGBA"),
    ]
    save_asset(atlas(badges), BADGE_ATLAS)
    build_qa(frames, badges).save(QA_BOARD)

    alpha_checks = {}
    for spec in KINDS:
        kind = str(spec["id"])
        for orientation in ("right", "left"):
            hover_alpha = np.asarray(frames[(kind, "hover", orientation)].getchannel("A"))
            selected_alpha = np.asarray(frames[(kind, "selected", orientation)].getchannel("A"))
            focus_alpha = np.asarray(frames[(kind, "focus", orientation)].getchannel("A"))
            alpha_checks[f"{kind}_{orientation}"] = bool(
                np.array_equal(hover_alpha, selected_alpha) and np.array_equal(hover_alpha, focus_alpha)
            )

    METADATA.write_text(
        json.dumps(
            {
                "id": "region_task_compound_b_type_frame_production_v7",
                "status": "production_candidate_pending_user_visual_review",
                "source_candidate": "runtime-preflight-v6-selected-type-frame",
                "kind_order": [spec["id"] for spec in KINDS],
                "type_colors": {spec["id"]: spec["color"] for spec in KINDS},
                "runtime_contract": {
                    "pin": [64, 80],
                    "hit": [72, 80],
                    "anchor_in_hit": [36, 76],
                    "compound_right": [278, 80],
                    "compound_left": [280, 80],
                    "caption_right": [78, 4, 200, 72],
                    "caption_left": [-208, 4, 200, 72],
                    "text_content": [14, 8, 166, 56],
                },
                "states": {
                    "idle": "shared B pin-only + runtime kind icon",
                    "hover": "neutral B compound with type cap",
                    "selected": "type selected underlay + type-color B frame compound",
                    "focus": "ink B frame compound with type cap",
                    "assigned_urgent_locked_disabled": "fixed art badge atlas",
                },
                "motion": {
                    "hover_to_selected_target_ms": 96,
                    "selected_to_hover_target_ms": 80,
                    "easing": "cubic_ease_out",
                    "crossfade": "hover=1-t; selected=t; underlay=t",
                },
                "alpha_equal_hover_selected_focus": alpha_checks,
                "color_medians": medians,
                "runtime_drawing_removed": [
                    "selected Polygon2D backplate",
                    "hover/selected/focus draw_arc",
                    "Polygon2D/Line2D state carrier",
                    "disabled Line2D slash",
                    "detached label background",
                ],
                "production_dir": str(PRODUCTION_DIR.relative_to(ROOT)).replace("\\", "/"),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    runtime_frame_count = build_runtime_gif()
    print(QA_BOARD)
    print(METADATA)
    print(PRODUCTION_DIR)
    if runtime_frame_count:
        print(f"{RUNTIME_GIF} ({runtime_frame_count} frames)")


if __name__ == "__main__":
    main()
