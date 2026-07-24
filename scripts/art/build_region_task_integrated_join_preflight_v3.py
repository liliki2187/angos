from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
V2_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v2"
V2_FRAME_DIR = V2_DIR / "frames"
V3_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v3"
V3_FRAME_DIR = V3_DIR / "frames"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-pin-integrated-join-v3"
ICON_ATLAS = V2_DIR / "rt-task-pin-kind-icons-v4-candidate-atlas-3x.png"

FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")

BG = (5, 29, 43, 255)
PAPER_TEXT = (236, 226, 202, 255)
MUTED_TEXT = (174, 188, 154, 255)
INK = (23, 37, 42, 255)
META_INK = (64, 81, 87, 255)
GOOD = (99, 166, 125, 255)
BAD = (207, 92, 67, 255)

KINDS = [
    {"id": "permanent", "name": "常驻", "title": "罗斯威尔档案残页", "meta": "常驻调查 · 1天", "icon": 0},
    {"id": "temp", "name": "限时", "title": "突发：雷达异常光点", "meta": "限时截稿 · 2天", "icon": 3},
    {"id": "chain", "name": "连续", "title": "M330 末班车空白段", "meta": "连续追踪 · 2天", "icon": 1},
    {"id": "hidden", "name": "隐藏", "title": "灵视：黑色方尖碑的回声", "meta": "灵视异常 · 3天", "icon": 2},
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    source = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(source), size=size)


def horizontal_nine_slice(image: Image.Image, target_width: int, fixed_edge: int = 72) -> Image.Image:
    if target_width < fixed_edge * 2:
        raise ValueError("target width is too small for fixed edges")
    center_source_width = image.width - fixed_edge * 2
    center_target_width = target_width - fixed_edge * 2
    result = Image.new("RGBA", (target_width, image.height), (0, 0, 0, 0))
    left = image.crop((0, 0, fixed_edge, image.height))
    center = image.crop((fixed_edge, 0, fixed_edge + center_source_width, image.height))
    right = image.crop((image.width - fixed_edge, 0, image.width, image.height))
    center = center.resize((center_target_width, image.height), Image.Resampling.LANCZOS)
    result.alpha_composite(left, (0, 0))
    result.alpha_composite(center, (fixed_edge, 0))
    result.alpha_composite(right, (target_width - fixed_edge, 0))
    return result


def atlas(frames: list[Image.Image]) -> Image.Image:
    result = Image.new("RGBA", (sum(frame.width for frame in frames), max(frame.height for frame in frames)), (0, 0, 0, 0))
    cursor = 0
    for frame in frames:
        result.alpha_composite(frame, (cursor, 0))
        cursor += frame.width
    return result


def load_icon_frames() -> dict[str, Image.Image]:
    source = Image.open(ICON_ATLAS).convert("RGBA")
    frames = [source.crop((index * 84, 0, (index + 1) * 84, 84)) for index in range(4)]
    return {spec["id"]: frames[spec["icon"]] for spec in KINDS}


def load_badge(badge_id: str) -> Image.Image:
    return Image.open(V2_FRAME_DIR / f"state-badge-{badge_id}-v2-3x.png").convert("RGBA")


def build_compound_frame(kind: str, selected: bool, orientation: str) -> Image.Image:
    state = "selected" if selected else "default"
    pin = Image.open(V2_FRAME_DIR / f"pin-{state}-{kind}-v2-3x.png").convert("RGBA")
    label_2x = Image.open(V2_FRAME_DIR / f"label-{orientation}-{kind}-v2-2x.png").convert("RGBA")
    label_3x = label_2x.resize((600, 216), Image.Resampling.LANCZOS)
    label_joined = horizontal_nine_slice(label_3x, 666)

    if orientation == "right":
        # Runtime footprint remains x=0..278. The label's logical anchor is still x=78;
        # only the baked paper extends under the pin from x=56, producing a 12px underlap.
        result = Image.new("RGBA", (834, 240), (0, 0, 0, 0))
        label_position = (168, 12)
        pin_position = (12, 0)
    else:
        # Runtime footprint remains x=-208..72. The label rect is unchanged at -208;
        # its baked inner paper tongue reaches to x=14, underlapping the pin by 10px.
        result = Image.new("RGBA", (840, 240), (0, 0, 0, 0))
        label_position = (0, 12)
        pin_position = (636, 0)

    result.alpha_composite(label_joined, label_position)
    result.alpha_composite(pin, pin_position)
    return result


def ellipsize(value: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> str:
    if text_font.getlength(value) <= max_width:
        return value
    suffix = "…"
    shortened = value
    while shortened and text_font.getlength(shortened + suffix) > max_width:
        shortened = shortened[:-1]
    return shortened + suffix


def draw_in_rect(draw: ImageDraw.ImageDraw, value: str, rect: tuple[int, int, int, int], text_font: ImageFont.FreeTypeFont, fill: tuple[int, int, int, int]) -> None:
    x, y, width, height = rect
    bbox = draw.textbbox((0, 0), value, font=text_font)
    text_height = bbox[3] - bbox[1]
    draw.text((x, y + (height - text_height) / 2 - bbox[1]), value, font=text_font, fill=fill)


def compose_runtime_sample(frames: dict, icons: dict[str, Image.Image], spec: dict, selected: bool, orientation: str, badge: str | None = None) -> Image.Image:
    compound = frames[(spec["id"], selected, orientation)].resize(
        (278 if orientation == "right" else 280, 80), Image.Resampling.LANCZOS
    )
    canvas = compound.copy()
    hit_x = 0 if orientation == "right" else 208
    label_x = 78 if orientation == "right" else 0
    icon = icons[spec["id"]].resize((28, 28), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (hit_x + 22, 15))
    if badge is not None:
        canvas.alpha_composite(load_badge(badge).resize((24, 24), Image.Resampling.LANCZOS), (hit_x + 48, 4))

    draw = ImageDraw.Draw(canvas)
    title_font = font(15, True)
    meta_font = font(12)
    title = ellipsize(spec["title"], title_font, 158)
    meta = ellipsize(spec["meta"], meta_font, 158)
    draw_in_rect(draw, title, (label_x + 14, 12, 158, 25), title_font, INK)
    draw_in_rect(draw, meta, (label_x + 14, 39, 158, 20), meta_font, META_INK)
    return canvas


def checker(size: tuple[int, int], step: int = 10) -> Image.Image:
    image = Image.new("RGBA", size, (26, 51, 64, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2 == 0:
                draw.rectangle((x, y, min(size[0] - 1, x + step - 1), min(size[1] - 1, y + step - 1)), fill=(36, 67, 80, 255))
    return image


def paste_checker(board: Image.Image, asset: Image.Image, position: tuple[int, int], scale: int = 1, padding: int = 8) -> None:
    shown = asset.resize((asset.width * scale, asset.height * scale), Image.Resampling.NEAREST)
    tile = checker((shown.width + padding * 2, shown.height + padding * 2), max(8, 8 * scale))
    tile.alpha_composite(shown, (padding, padding))
    board.alpha_composite(tile, position)


def build_comparison(frames: dict, icons: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1500, 520), BG)
    draw = ImageDraw.Draw(board)
    draw.text((40, 28), "接合关系定向修正｜同一组件，非两版造型", font=font(28, True), fill=PAPER_TEXT)
    draw.text((40, 70), "逻辑 hit / anchor / caption rect 不变；只把纸质底图烘焙成连续压合件", font=font(17), fill=MUTED_TEXT)

    spec = KINDS[0]
    # Reconstruct the rejected v2 using the original separated placement.
    pin = Image.open(V2_FRAME_DIR / "pin-selected-permanent-v2-3x.png").convert("RGBA").resize((64, 80), Image.Resampling.LANCZOS)
    label = Image.open(V2_FRAME_DIR / "label-right-permanent-v2-2x.png").convert("RGBA").resize((200, 72), Image.Resampling.LANCZOS)
    rejected = Image.new("RGBA", (278, 80), (0, 0, 0, 0))
    rejected.alpha_composite(label, (78, 4))
    rejected.alpha_composite(pin, (4, 0))
    rejected.alpha_composite(icons["permanent"].resize((28, 28), Image.Resampling.LANCZOS), (22, 15))
    rejected_draw = ImageDraw.Draw(rejected)
    draw_in_rect(rejected_draw, spec["title"], (92, 12, 158, 25), font(15, True), INK)
    draw_in_rect(rejected_draw, spec["meta"], (92, 39, 158, 20), font(12), META_INK)

    corrected = compose_runtime_sample(frames, icons, spec, True, "right")
    draw.text((70, 130), "原 v2：暗缝分离", font=font(19, True), fill=BAD)
    paste_checker(board, rejected, (70, 170), scale=3, padding=10)
    draw.text((820, 130), "修正 v3：横条埋入，图钉压上", font=font(19, True), fill=GOOD)
    paste_checker(board, corrected, (650, 170), scale=3, padding=10)
    draw.text((70, 450), "× 右挂约 10px 地图底色穿透", font=font(16), fill=BAD)
    draw.text((820, 450), "✓ 12px 美术 underlap；无连接色块", font=font(16), fill=GOOD)
    return board


def build_truth_board(frames: dict, icons: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1560, 760), BG)
    draw = ImageDraw.Draw(board)
    draw.text((36, 24), "真实 1× 接合读回｜四类型 default / selected", font=font(27, True), fill=PAPER_TEXT)
    draw.text((36, 64), "所有动态文字仍使用原 [14,12,158,48] 安全区；远端类型帽、尖端类型色不变", font=font(16), fill=MUTED_TEXT)

    for index, spec in enumerate(KINDS):
        x = 36 + index * 380
        draw.text((x, 108), spec["name"], font=font(18, True), fill=PAPER_TEXT)
        draw.text((x, 144), "默认", font=font(13), fill=MUTED_TEXT)
        paste_checker(board, compose_runtime_sample(frames, icons, spec, False, "right"), (x, 170), padding=8)
        draw.text((x, 282), "选中", font=font(13), fill=MUTED_TEXT)
        paste_checker(board, compose_runtime_sample(frames, icons, spec, True, "right"), (x, 308), padding=8)

    draw.text((36, 430), "左右方向与状态压力样例", font=font(20, True), fill=PAPER_TEXT)
    hidden = KINDS[3]
    temp = KINDS[1]
    samples = [
        ("隐藏｜选中｜右挂", compose_runtime_sample(frames, icons, hidden, True, "right")),
        ("隐藏｜选中｜左挂", compose_runtime_sample(frames, icons, hidden, True, "left")),
        ("限时｜选中 + 紧急", compose_runtime_sample(frames, icons, temp, True, "right", "urgent")),
    ]
    for index, (caption, sample) in enumerate(samples):
        x = 36 + index * 500
        draw.text((x, 474), caption, font=font(15, True), fill=PAPER_TEXT)
        paste_checker(board, sample, (x, 510), padding=8)

    draw.text((36, 690), "接合判定：左右均无贯穿深蓝缝；pin 轮廓位于横条内肩上方；selected 背板保持连续。", font=font(16), fill=GOOD)
    return board


def main() -> None:
    V3_FRAME_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    icons = load_icon_frames()
    frames: dict[tuple[str, bool, str], Image.Image] = {}

    for spec in KINDS:
        kind = spec["id"]
        for selected in (False, True):
            state = "selected" if selected else "default"
            for orientation in ("right", "left"):
                frame = build_compound_frame(kind, selected, orientation)
                frames[(kind, selected, orientation)] = frame
                frame.save(V3_FRAME_DIR / f"compound-{orientation}-{state}-{kind}-v3-3x.png")

    for orientation in ("right", "left"):
        for selected in (False, True):
            state = "selected" if selected else "default"
            ordered = [frames[(spec["id"], selected, orientation)] for spec in KINDS]
            atlas(ordered).save(V3_DIR / f"rt-task-compound-{orientation}-{state}-v3-atlas-3x.png")

    comparison = build_comparison(frames, icons)
    comparison.save(SCREENSHOT_DIR / "01-v2-v3-integrated-join-comparison.png")
    truth = build_truth_board(frames, icons)
    truth.save(SCREENSHOT_DIR / "02-native-1x-integrated-join-evidence-v3.png")

    metadata = {
        "id": "region_task_pin_label_integrated_join_v3",
        "status": "visual_candidate_pending_user_review",
        "production_integration": False,
        "art_source": "01-integrated-pin-label-source-v3-alpha.png",
        "implementation": "baked_compound_background_with_dynamic_icon_and_text",
        "runtime_contract_preserved": {
            "hit": [72, 80],
            "anchor_in_hit": [36, 76],
            "pin": [64, 80],
            "caption_rect_right": [78, 4, 200, 72],
            "caption_rect_left": [-208, 4, 200, 72],
            "compound_right": [278, 80],
            "compound_left": [280, 80],
            "text_content": [14, 12, 158, 48],
        },
        "visual_join": {
            "right_underlap_px": 12,
            "left_underlap_px": 10,
            "layer_order": ["compound_paper", "kind_icon_and_dynamic_text", "state_badge"],
            "program_connector": False,
        },
        "notes": [
            "逻辑 caption anchor 不移动；接合关系烘焙在组合底图内。",
            "九宫格只延展横条中央空白纸面，左右端帽与 pin 不拉伸。",
            "当前只生成预检候选，未替换 Godot 生产资源。",
        ],
    }
    (V3_DIR / "runtime-preflight-assets-v3.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(SCREENSHOT_DIR / "01-v2-v3-integrated-join-comparison.png")
    print(SCREENSHOT_DIR / "02-native-1x-integrated-join-evidence-v3.png")


if __name__ == "__main__":
    main()
