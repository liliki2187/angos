from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v2"
FRAME_DIR = SOURCE_DIR / "frames"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-pin-runtime-preflight-v2"

PIN_SOURCE = SOURCE_DIR / "01-pin-macro-components-source-v2-alpha.png"
LABEL_SOURCE = SOURCE_DIR / "02-label-macro-components-source-v2e-alpha.png"
BADGE_SOURCE = SOURCE_DIR / "03-state-badges-source-v2-alpha.png"
TEMP_ICON_SOURCE = SOURCE_DIR / "04-temp-hourglass-icon-v2-alpha.png"
ICON_SOURCE = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task" / "v2" / "pin_slice" / "rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png"

BOARD_OUTPUT = ROOT / "design" / "art-direction" / "region-task-board" / "2026-07-21-region-task-macro-production-feasibility-v2.png"

FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")

BG = (5, 29, 43, 255)
PANEL = (10, 42, 57, 255)
PANEL_ALT = (12, 49, 64, 255)
EDGE = (116, 143, 145, 255)
PAPER_TEXT = (236, 226, 202, 255)
MUTED_TEXT = (174, 188, 154, 255)
INK = (23, 37, 42, 255)
META_INK = (64, 81, 87, 255)
TEAL = (52, 118, 122, 255)
OLIVE = (127, 138, 71, 255)
RUST = (173, 79, 54, 255)

KINDS = [
    {"id": "permanent", "name": "常驻", "title": "罗斯威尔档案残页", "meta": "常驻调查 · 1天", "icon": 0, "accent": (127, 138, 71)},
    {"id": "temp", "name": "限时", "title": "突发：雷达异常光点", "meta": "限时截稿 · 2天", "icon": 3, "accent": (136, 106, 64)},
    {"id": "chain", "name": "连续", "title": "M330 末班车空白段", "meta": "连续追踪 · 2天", "icon": 1, "accent": (52, 118, 122)},
    {"id": "hidden", "name": "隐藏", "title": "灵视：黑色方尖碑的回声", "meta": "灵视异常 · 3天", "icon": 2, "accent": (68, 89, 103)},
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(path), size=size)


def largest_connected_bbox(alpha: Image.Image, threshold: int = 24) -> tuple[int, int, int, int] | None:
    width, height = alpha.size
    pixels = alpha.load()
    visited = bytearray(width * height)
    best_count = 0
    best_bbox: tuple[int, int, int, int] | None = None
    for y in range(height):
        for x in range(width):
            offset = y * width + x
            if visited[offset] or pixels[x, y] <= threshold:
                continue
            visited[offset] = 1
            queue = deque([(x, y)])
            count = 0
            min_x = max_x = x
            min_y = max_y = y
            while queue:
                current_x, current_y = queue.popleft()
                count += 1
                min_x = min(min_x, current_x)
                max_x = max(max_x, current_x)
                min_y = min(min_y, current_y)
                max_y = max(max_y, current_y)
                for next_x, next_y in ((current_x - 1, current_y), (current_x + 1, current_y), (current_x, current_y - 1), (current_x, current_y + 1)):
                    if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
                        continue
                    next_offset = next_y * width + next_x
                    if visited[next_offset] or pixels[next_x, next_y] <= threshold:
                        continue
                    visited[next_offset] = 1
                    queue.append((next_x, next_y))
            if count > best_count:
                best_count = count
                best_bbox = (min_x, min_y, max_x + 1, max_y + 1)
    return best_bbox


def crop_grid_cell(image: Image.Image, columns: int, rows: int, column: int, row: int, padding: int = 2) -> tuple[Image.Image, tuple[int, int, int, int]]:
    left = round(column * image.width / columns)
    top = round(row * image.height / rows)
    right = round((column + 1) * image.width / columns)
    bottom = round((row + 1) * image.height / rows)
    cell = image.crop((left, top, right, bottom))
    bbox = largest_connected_bbox(cell.getchannel("A"))
    if bbox is None:
        raise RuntimeError(f"empty grid cell {column},{row}")
    bbox = (
        max(0, bbox[0] - padding),
        max(0, bbox[1] - padding),
        min(cell.width, bbox[2] + padding),
        min(cell.height, bbox[3] + padding),
    )
    return cell.crop(bbox), (left + bbox[0], top + bbox[1], left + bbox[2], top + bbox[3])


def exact_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)


def exact_resize_with_padding(image: Image.Image, size: tuple[int, int], padding: int) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    resized = image.resize((size[0] - padding * 2, size[1] - padding * 2), Image.Resampling.LANCZOS)
    canvas.alpha_composite(resized, (padding, padding))
    return canvas


def contain(image: Image.Image, size: tuple[int, int], padding: int = 0) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    available = (max(1, size[0] - padding * 2), max(1, size[1] - padding * 2))
    copy = image.copy()
    copy.thumbnail(available, Image.Resampling.LANCZOS)
    canvas.alpha_composite(copy, ((size[0] - copy.width) // 2, (size[1] - copy.height) // 2))
    return canvas


def atlas(frames: list[Image.Image]) -> Image.Image:
    result = Image.new("RGBA", (sum(frame.width for frame in frames), max(frame.height for frame in frames)), (0, 0, 0, 0))
    cursor = 0
    for frame in frames:
        result.alpha_composite(frame, (cursor, 0))
        cursor += frame.width
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


def checker(size: tuple[int, int], step: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (27, 53, 66, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2 == 0:
                draw.rectangle((x, y, min(size[0] - 1, x + step - 1), min(size[1] - 1, y + step - 1)), fill=(38, 69, 82, 255))
    return image


def rounded_panel(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], fill: tuple[int, int, int, int] = PANEL, outline: tuple[int, int, int, int] = EDGE, radius: int = 12, width: int = 2) -> None:
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)


def centered_text(draw: ImageDraw.ImageDraw, value: str, rect: tuple[int, int, int, int], text_font: ImageFont.FreeTypeFont, fill: tuple[int, int, int, int]) -> None:
    bbox = draw.textbbox((0, 0), value, font=text_font)
    x = rect[0] + (rect[2] - rect[0] - (bbox[2] - bbox[0])) / 2 - bbox[0]
    y = rect[1] + (rect[3] - rect[1] - (bbox[3] - bbox[1])) / 2 - bbox[1]
    draw.text((x, y), value, font=text_font, fill=fill)


def build_assets() -> dict:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    pin_source = Image.open(PIN_SOURCE).convert("RGBA")
    label_source = Image.open(LABEL_SOURCE).convert("RGBA")
    badge_source = Image.open(BADGE_SOURCE).convert("RGBA")
    temp_icon_source = Image.open(TEMP_ICON_SOURCE).convert("RGBA")
    icon_source = Image.open(ICON_SOURCE).convert("RGBA")

    default_frames: dict[str, Image.Image] = {}
    selected_frames: dict[str, Image.Image] = {}
    label_right_frames: dict[str, Image.Image] = {}
    label_left_frames: dict[str, Image.Image] = {}
    source_bboxes: dict[str, list[int]] = {}

    for row, spec in enumerate(KINDS):
        kind = spec["id"]
        default_crop, default_bbox = crop_grid_cell(pin_source, 2, 4, 0, row)
        selected_crop, selected_bbox = crop_grid_cell(pin_source, 2, 4, 1, row)
        right_crop, right_bbox = crop_grid_cell(label_source, 4, 2, row, 0)
        left_crop, left_bbox = crop_grid_cell(label_source, 4, 2, row, 1)

        default_frame = exact_resize_with_padding(default_crop, (192, 240), 3)
        selected_frame = exact_resize_with_padding(selected_crop, (192, 240), 3)
        right_frame = exact_resize_with_padding(right_crop, (400, 144), 2)
        left_frame = exact_resize_with_padding(left_crop, (400, 144), 2)

        default_frames[kind] = default_frame
        selected_frames[kind] = selected_frame
        label_right_frames[kind] = right_frame
        label_left_frames[kind] = left_frame

        default_frame.save(FRAME_DIR / f"pin-default-{kind}-v2-3x.png")
        selected_frame.save(FRAME_DIR / f"pin-selected-{kind}-v2-3x.png")
        right_frame.save(FRAME_DIR / f"label-right-{kind}-v2-2x.png")
        left_frame.save(FRAME_DIR / f"label-left-{kind}-v2-2x.png")
        source_bboxes[f"pin_default_{kind}"] = list(default_bbox)
        source_bboxes[f"pin_selected_{kind}"] = list(selected_bbox)
        source_bboxes[f"label_right_{kind}"] = list(right_bbox)
        source_bboxes[f"label_left_{kind}"] = list(left_bbox)

    badge_frames: dict[str, Image.Image] = {}
    for column, badge_id in enumerate(["assigned", "urgent", "locked"]):
        crop, bbox = crop_grid_cell(badge_source, 3, 1, column, 0)
        frame = contain(crop, (72, 72), 2)
        badge_frames[badge_id] = frame
        frame.save(FRAME_DIR / f"state-badge-{badge_id}-v2-3x.png")
        source_bboxes[f"badge_{badge_id}"] = list(bbox)

    atlas([default_frames[spec["id"]] for spec in KINDS]).save(SOURCE_DIR / "rt-task-pin-default-macro-v2-atlas-3x.png")
    atlas([selected_frames[spec["id"]] for spec in KINDS]).save(SOURCE_DIR / "rt-task-pin-selected-macro-v2-atlas-3x.png")
    atlas([label_right_frames[spec["id"]] for spec in KINDS]).save(SOURCE_DIR / "rt-task-label-right-macro-v2-atlas-2x.png")
    atlas([label_left_frames[spec["id"]] for spec in KINDS]).save(SOURCE_DIR / "rt-task-label-left-macro-v2-atlas-2x.png")
    atlas([badge_frames[key] for key in ["assigned", "urgent", "locked"]]).save(SOURCE_DIR / "rt-task-state-badges-macro-v2-atlas-3x.png")

    icon_frames: dict[str, Image.Image] = {}
    source_icon_frames = [icon_source.crop((index * 84, 0, (index + 1) * 84, 84)) for index in range(4)]
    temp_icon_bbox = largest_connected_bbox(temp_icon_source.getchannel("A"))
    if temp_icon_bbox is None:
        raise RuntimeError("empty generated temp hourglass icon")
    temp_icon_crop = temp_icon_source.crop(temp_icon_bbox)
    temp_icon_frame = contain(temp_icon_crop, (84, 84), 6)
    candidate_icon_atlas = atlas([source_icon_frames[0], source_icon_frames[1], source_icon_frames[2], temp_icon_frame])
    candidate_icon_atlas.save(SOURCE_DIR / "rt-task-pin-kind-icons-v4-candidate-atlas-3x.png")
    for spec in KINDS:
        source_icon = temp_icon_frame if spec["id"] == "temp" else source_icon_frames[spec["icon"]]
        icon_frames[spec["id"]] = source_icon.resize((28, 28), Image.Resampling.LANCZOS)

    return {
        "default": default_frames,
        "selected": selected_frames,
        "label_right": label_right_frames,
        "label_left": label_left_frames,
        "badges": badge_frames,
        "icons": icon_frames,
        "source_bboxes": source_bboxes,
    }


def runtime_frame(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    return source.resize(size, Image.Resampling.LANCZOS)


def compose_sample(assets: dict, spec: dict, selected: bool, orientation: str = "right", badge: str | None = None) -> Image.Image:
    pin = runtime_frame(assets["selected" if selected else "default"][spec["id"]], (64, 80))
    label = runtime_frame(assets[f"label_{orientation}"][spec["id"]], (200, 72))
    icon = assets["icons"][spec["id"]]

    if orientation == "right":
        canvas = Image.new("RGBA", (278, 80), (0, 0, 0, 0))
        hit_x = 0
        label_x = 78
    else:
        canvas = Image.new("RGBA", (280, 80), (0, 0, 0, 0))
        hit_x = 208
        label_x = 0

    canvas.alpha_composite(label, (label_x, 4))
    pin_x = hit_x + 4
    canvas.alpha_composite(pin, (pin_x, 0))
    canvas.alpha_composite(icon, (hit_x + 22, 15))
    if badge is not None:
        badge_frame = runtime_frame(assets["badges"][badge], (24, 24))
        canvas.alpha_composite(badge_frame, (hit_x + 48, 4))

    draw = ImageDraw.Draw(canvas)
    title_font = font(15, True)
    meta_font = font(12)
    title = ellipsize(spec["title"], title_font, 158)
    meta = ellipsize(spec["meta"], meta_font, 158)
    draw_in_rect(draw, title, (label_x + 14, 12, 158, 25), title_font, INK)
    draw_in_rect(draw, meta, (label_x + 14, 39, 158, 20), meta_font, META_INK)
    return canvas


def paste_on_checker(board: Image.Image, asset: Image.Image, position: tuple[int, int], scale: int = 1, padding: int = 12) -> None:
    resized = asset.resize((asset.width * scale, asset.height * scale), Image.Resampling.NEAREST)
    background = checker((resized.width + padding * 2, resized.height + padding * 2), max(8, 8 * scale))
    background.alpha_composite(resized, (padding, padding))
    board.alpha_composite(background, position)


def build_board(assets: dict) -> Image.Image:
    board = Image.new("RGBA", (2560, 1440), BG)
    draw = ImageDraw.Draw(board)
    centered_text(draw, "区域任务短签｜宏观组合件生产可行性 v2", (60, 28, 2500, 76), font(34, True), PAPER_TEXT)
    centered_text(draw, "真实 1× 中文回填 · 左右独立短签 · selected + urgent · 美术组合件而非程序微色片", (60, 76, 2500, 112), font(17), MUTED_TEXT)

    draw.text((60, 126), "A. 四类 default / selected：真实 1×", font=font(23, True), fill=PAPER_TEXT)
    card_width = 592
    for index, spec in enumerate(KINDS):
        x = 60 + index * 620
        rounded_panel(draw, (x, 166, x + card_width, 426), PANEL)
        draw.text((x + 20, 180), f"{spec['name']}任务", font=font(20, True), fill=PAPER_TEXT)
        draw.text((x + 20, 222), "默认", font=font(14), fill=MUTED_TEXT)
        draw.text((x + 20, 326), "选中", font=font(14), fill=MUTED_TEXT)
        default_sample = compose_sample(assets, spec, False)
        selected_sample = compose_sample(assets, spec, True)
        paste_on_checker(board, default_sample, (x + 90, 210), 1, 8)
        paste_on_checker(board, selected_sample, (x + 90, 314), 1, 8)

    draw.text((60, 464), "B. 现在如何拆：组合件保留纸沿与压合，文字 / 图标保持动态", font=font(23, True), fill=PAPER_TEXT)
    rounded_panel(draw, (60, 504, 1310, 1050), PANEL_ALT)

    permanent = KINDS[0]
    selected_pin = runtime_frame(assets["selected"]["permanent"], (64, 80))
    right_label = runtime_frame(assets["label_right"]["permanent"], (200, 72))
    icon = assets["icons"]["permanent"]
    sample = compose_sample(assets, permanent, True)

    component_tiles = [
        ("01 选中图钉组合件", "背板＋连接肩＋前壳＋类型尖端", selected_pin, 4),
        ("02 右挂短签组合件", "纸面＋外端帽；左右分别生产", right_label, 2),
        ("03 类型图标", "现有 28×28 atlas 可复用", icon, 4),
        ("04 最终动态合成", "标题 / meta 不进入 PNG", sample, 2),
    ]
    tile_positions = [(86, 560), (430, 560), (870, 560), (86, 820)]
    tile_sizes = [(310, 430), (410, 260), (230, 250), (1170, 190)]
    for (title, subtitle, asset, scale), position, size in zip(component_tiles, tile_positions, tile_sizes):
        x, y = position
        width, height = size
        rounded_panel(draw, (x, y, x + width, y + height), PANEL)
        draw.text((x + 14, y + 12), title, font=font(17, True), fill=PAPER_TEXT)
        draw.text((x + 14, y + 42), subtitle, font=font(12), fill=MUTED_TEXT)
        resized = asset.resize((asset.width * scale, asset.height * scale), Image.Resampling.NEAREST)
        background = checker((min(width - 28, resized.width + 16), min(height - 78, resized.height + 16)), max(8, 8 * min(scale, 2)))
        asset_fit = resized.copy()
        asset_fit.thumbnail((background.width - 16, background.height - 16), Image.Resampling.NEAREST)
        background.alpha_composite(asset_fit, ((background.width - asset_fit.width) // 2, (background.height - asset_fit.height) // 2))
        board.alpha_composite(background, (x + (width - background.width) // 2, y + 68))

    draw.text((1350, 464), "C. 关键压力样例", font=font(23, True), fill=PAPER_TEXT)
    rounded_panel(draw, (1350, 504, 2500, 1050), PANEL_ALT)
    hidden = KINDS[3]
    temp = KINDS[1]
    samples = [
        ("最长标题｜右挂", compose_sample(assets, hidden, True, "right")),
        ("最长标题｜左挂", compose_sample(assets, hidden, True, "left")),
        ("限时任务｜选中 + 紧急", compose_sample(assets, temp, True, "right", "urgent")),
    ]
    for index, (label, asset) in enumerate(samples):
        y = 548 + index * 160
        draw.text((1380, y), label, font=font(16, True), fill=PAPER_TEXT)
        paste_on_checker(board, asset, (1650, y - 8), 2, 10)

    rounded_panel(draw, (60, 1090, 2500, 1370), PANEL)
    draw.text((90, 1118), "本轮可审内容", font=font(21, True), fill=PAPER_TEXT)
    notes = [
        "• 默认与选中图钉已改为完整宏观组合件，不再拆背板、尖角和细纸沿。",
        "• 左挂 / 右挂短签各自成件；类型色端帽始终位于远端，不靠运行时镜像猜方向。",
        "• 文字安全区候选改为 [14,12,158,48]；真实长标题只在地图短签省略，完整信息留给右侧档案。",
        "• urgent / assigned / locked 为完整美术小纸签；外部投影、锚点、dense、cluster、clamp 仍由 Godot 承担。",
        "• 当前仍是 preflight，不替换生产资源；只有 1×可读性与小纸签辨识通过后才升合同。",
    ]
    for index, line in enumerate(notes):
        draw.text((90, 1164 + index * 38), line, font=font(15), fill=MUTED_TEXT)
    return board


def main() -> None:
    assets = build_assets()
    board = build_board(assets)
    board.save(BOARD_OUTPUT)
    board.save(SCREENSHOT_DIR / "01-macro-production-feasibility-v2.png")

    truth_strip = Image.new("RGBA", (1320, 440), BG)
    draw = ImageDraw.Draw(truth_strip)
    draw.text((30, 24), "真实 1× 读回｜四类默认 / 选中", font=font(25, True), fill=PAPER_TEXT)
    for index, spec in enumerate(KINDS):
        x = 30 + index * 320
        draw.text((x, 76), spec["name"], font=font(16, True), fill=PAPER_TEXT)
        truth_strip.alpha_composite(compose_sample(assets, spec, False), (x, 110))
        truth_strip.alpha_composite(compose_sample(assets, spec, True), (x, 230))
    truth_strip.save(SCREENSHOT_DIR / "02-native-1x-truth-strip-v2.png")

    metadata = {
        "id": "region_task_macro_production_preflight_v2",
        "status": "runtime_candidate_pending_user_visual_review",
        "production_integration": False,
        "runtime_contract_preserved": {
            "hit": [72, 80],
            "anchor_in_hit": [36, 76],
            "default_pin": [64, 80],
            "selected_pin": [64, 80],
            "label": [200, 72],
            "label_anchor_right": [78, 4],
            "label_anchor_left": [-208, 4],
        },
        "candidate_text_rects": {
            "content": [14, 12, 158, 48],
            "title": [14, 12, 158, 25],
            "meta": [14, 39, 158, 20],
        },
        "source_bboxes": assets["source_bboxes"],
        "notes": [
            "图钉 default / selected 为组合件，不再拆微型色片。",
            "短签 right / left 分别生产，端帽始终位于远端。",
            "状态小纸签运行候选尺寸为 24×24，需用户确认后才改正式合同。",
        ],
    }
    (SOURCE_DIR / "runtime-preflight-assets-v2.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(BOARD_OUTPUT)
    print(SCREENSHOT_DIR / "01-macro-production-feasibility-v2.png")


if __name__ == "__main__":
    main()
