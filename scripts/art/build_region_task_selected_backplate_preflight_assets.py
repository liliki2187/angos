from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board"
OUTPUT_DIR = SOURCE_DIR / "runtime-preflight-v1"

BACKPLATE_SOURCE = SOURCE_DIR / "2026-07-21-region-task-selected-backplate-source-v2-alpha.png"
PIN_SOURCE = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task" / "v2" / "pin_slice" / "rt-task-pin-shell-c-hybrid-v3-3x.png"
LABEL_SOURCE = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task" / "v2" / "pin_slice" / "rt-task-pin-label-c-hybrid-v3-2x.png"
ICON_SOURCE = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task" / "v2" / "pin_slice" / "rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png"
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-pin-runtime-preflight"
BOARD_OUTPUT = SOURCE_DIR / "2026-07-21-region-task-pin-runtime-content-preflight-v1.png"
EXPLODED_OUTPUT = SOURCE_DIR / "2026-07-21-region-task-pin-layer-exploded-sheet-v1.png"

TYPE_COLORS = {
    "permanent": (127, 138, 71),
    "temp": (136, 106, 64),
    "chain": (52, 118, 122),
    "hidden": (68, 89, 103),
}
FRAME_ORDER = ["permanent", "temp", "chain", "hidden"]
PAPER_MIX = (214, 194, 171)
IVORY_EDGE = (232, 223, 200)
INK = (23, 37, 42, 255)
MUTED_INK = (82, 99, 106, 255)
PAPER_TEXT = (232, 223, 200, 255)
BOARD_COLOR = (7, 29, 46, 255)
FONT_PATH = Path("C:/Windows/Fonts/msyh.ttc")

SPECS = [
    {"kind": "permanent", "row": "常驻任务", "title": "罗斯威尔档案残页", "meta": "常驻调查 · 1天"},
    {"kind": "temp", "row": "限时任务", "title": "突发：雷达异常光点", "meta": "限时截稿 · 2天"},
    {"kind": "chain", "row": "连续任务", "title": "M330 末班车空白段", "meta": "连续追踪 · 2天"},
    {"kind": "hidden", "row": "隐藏任务", "title": "灵视：黑色方尖碑的回声", "meta": "灵视异常 · 3天"},
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def distance(rgb: tuple[int, int, int], target: tuple[int, int, int]) -> float:
    return math.sqrt(sum((rgb[index] - target[index]) ** 2 for index in range(3)))


def mix_rgb(a: tuple[int, int, int], b: tuple[int, int, int], amount_b: float) -> tuple[int, int, int]:
    return tuple(round(a[index] * (1.0 - amount_b) + b[index] * amount_b) for index in range(3))


def recolor_backplate(source: Image.Image, target: tuple[int, int, int]) -> Image.Image:
    source = source.convert("RGBA")
    result = Image.new("RGBA", source.size, (0, 0, 0, 0))
    source_pixels = source.load()
    result_pixels = result.load()
    selected_base = mix_rgb(target, PAPER_MIX, 0.38)

    for y in range(source.height):
        for x in range(source.width):
            red, green, blue, alpha = source_pixels[x, y]
            if alpha == 0:
                continue
            luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
            if luminance >= 225:
                factor = clamp(0.92 + (luminance - 225.0) / 180.0, 0.92, 1.06)
                color = tuple(round(channel * factor) for channel in IVORY_EDGE)
            else:
                factor = clamp(0.86 + (luminance - 175.0) / 260.0, 0.78, 1.08)
                color = tuple(round(clamp(channel * factor, 0, 255)) for channel in selected_base)
            result_pixels[x, y] = (*color, alpha)
    return result


def accent_overlay(source: Image.Image, target: tuple[int, int, int], role: str) -> Image.Image:
    source = source.convert("RGBA")
    result = Image.new("RGBA", source.size, (0, 0, 0, 0))
    source_pixels = source.load()
    result_pixels = result.load()
    accent_reference = (154, 164, 166)
    paper_reference = (238, 218, 194)
    ink_reference = (28, 42, 45)

    for y in range(source.height):
        for x in range(source.width):
            if role == "pin" and y < 170:
                continue
            if role == "label" and x < 350:
                continue
            red, green, blue, alpha = source_pixels[x, y]
            if alpha == 0:
                continue
            rgb = (red, green, blue)
            accent_distance = distance(rgb, accent_reference)
            other_distance = min(distance(rgb, paper_reference), distance(rgb, ink_reference))
            confidence = clamp((other_distance - accent_distance) / 34.0, 0.0, 1.0)
            luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
            if luminance < 82:
                confidence = 0.0
            overlay_alpha = round(alpha * confidence)
            if overlay_alpha == 0:
                continue
            factor = clamp(0.84 + (luminance - 140.0) / 220.0, 0.74, 1.10)
            color = tuple(round(clamp(channel * factor, 0, 255)) for channel in target)
            result_pixels[x, y] = (*color, overlay_alpha)
    return result


def build_backplate_atlas() -> Image.Image:
    source = Image.open(BACKPLATE_SOURCE).convert("RGBA")
    bounds = source.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("背板源没有有效 alpha。")
    cropped = source.crop(bounds)
    resized = cropped.resize((210, 198), Image.Resampling.LANCZOS)
    atlas = Image.new("RGBA", (216 * len(FRAME_ORDER), 240), (0, 0, 0, 0))
    for index, kind in enumerate(FRAME_ORDER):
        frame = Image.new("RGBA", (216, 240), (0, 0, 0, 0))
        frame.alpha_composite(recolor_backplate(resized, TYPE_COLORS[kind]), (3, 6))
        atlas.alpha_composite(frame, (216 * index, 0))
    return atlas


def build_accent_atlas(source_path: Path, role: str) -> Image.Image:
    source = Image.open(source_path).convert("RGBA")
    atlas = Image.new("RGBA", (source.width * len(FRAME_ORDER), source.height), (0, 0, 0, 0))
    for index, kind in enumerate(FRAME_ORDER):
        atlas.alpha_composite(accent_overlay(source, TYPE_COLORS[kind], role), (source.width * index, 0))
    return atlas


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size)


def atlas_frame(atlas: Image.Image, index: int, frame_size: tuple[int, int]) -> Image.Image:
    width, height = frame_size
    return atlas.crop((index * width, 0, (index + 1) * width, height))


def kind_index(kind: str) -> int:
    return FRAME_ORDER.index(kind)


def icon_index(kind: str) -> int:
    return {"permanent": 0, "chain": 1, "hidden": 2, "temp": 3}[kind]


def ellipsize(value: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> str:
    if text_font.getlength(value) <= max_width:
        return value
    suffix = "…"
    shortened = value
    while shortened and text_font.getlength(shortened + suffix) > max_width:
        shortened = shortened[:-1]
    return shortened + suffix


def make_runtime_sample(
    kind: str,
    title: str,
    meta: str,
    selected: bool,
    label_left: bool,
    backplates: Image.Image,
    pin_accents: Image.Image,
    label_accents: Image.Image,
) -> Image.Image:
    pin_shell = Image.open(PIN_SOURCE).convert("RGBA").resize((64, 80), Image.Resampling.LANCZOS)
    label_base = Image.open(LABEL_SOURCE).convert("RGBA").resize((200, 72), Image.Resampling.LANCZOS)
    icons = Image.open(ICON_SOURCE).convert("RGBA")
    icon = atlas_frame(icons, icon_index(kind), (84, 84)).resize((28, 28), Image.Resampling.LANCZOS)
    type_index = kind_index(kind)
    pin_accent = atlas_frame(pin_accents, type_index, (192, 240)).resize((64, 80), Image.Resampling.LANCZOS)
    label_accent = atlas_frame(label_accents, type_index, (400, 144)).resize((200, 72), Image.Resampling.LANCZOS)
    backplate = atlas_frame(backplates, type_index, (216, 240)).resize((72, 80), Image.Resampling.LANCZOS)

    if label_left:
        root_x = 208
        label_x = 0
        width = 280
        label_base = ImageOps.mirror(label_base)
        label_accent = ImageOps.mirror(label_accent)
    else:
        root_x = 0
        label_x = 78
        width = 278

    sample = Image.new("RGBA", (width, 80), (0, 0, 0, 0))
    if selected:
        sample.alpha_composite(backplate, (root_x, 0))
    sample.alpha_composite(label_base, (label_x, 4))
    sample.alpha_composite(label_accent, (label_x, 4))
    sample.alpha_composite(pin_shell, (root_x + 4, 0))
    sample.alpha_composite(pin_accent, (root_x + 4, 0))
    sample.alpha_composite(icon, (root_x + 22, 14))

    draw = ImageDraw.Draw(sample)
    title_font = font(15)
    meta_font = font(12)
    draw.text((label_x + 14, 9), ellipsize(title, title_font, 166), font=title_font, fill=INK)
    draw.text((label_x + 14, 38), ellipsize(meta, meta_font, 166), font=meta_font, fill=MUTED_INK)
    return sample


def draw_centered(draw: ImageDraw.ImageDraw, value: str, box: tuple[int, int, int, int], text_font: ImageFont.FreeTypeFont, fill: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    bounds = draw.textbbox((0, 0), value, font=text_font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    x = left + (right - left - width) / 2 - bounds[0]
    y = top + (bottom - top - height) / 2 - bounds[1]
    draw.text((x, y), value, font=text_font, fill=fill)


def build_contract_boards(backplates: Image.Image, pin_accents: Image.Image, label_accents: Image.Image) -> tuple[Image.Image, Image.Image]:
    board = Image.new("RGBA", (2560, 1440), BOARD_COLOR)
    draw = ImageDraw.Draw(board)
    draw_centered(draw, "区域任务短签｜精确运行比例与真实中文回填", (80, 34, 2480, 92), font(34), PAPER_TEXT)
    draw_centered(draw, "所有组件先按 1× 合同组合，再以整数 2× 展示；左：默认　中：选中　右：边缘左置", (80, 92, 2480, 126), font(18), (174, 188, 154, 255))
    draw_centered(draw, "默认", (400, 150, 956, 190), font(24), PAPER_TEXT)
    draw_centered(draw, "选中", (1120, 150, 1676, 190), font(24), PAPER_TEXT)
    draw_centered(draw, "右边缘左置验证", (1884, 150, 2448, 190), font(24), PAPER_TEXT)

    row_y = [220, 450, 680, 910]
    for index, spec in enumerate(SPECS):
        y = row_y[index]
        draw_centered(draw, spec["row"], (90, y + 48, 340, y + 100), font(25), PAPER_TEXT)
        default_sample = make_runtime_sample(spec["kind"], spec["title"], spec["meta"], False, False, backplates, pin_accents, label_accents)
        selected_sample = make_runtime_sample(spec["kind"], spec["title"], spec["meta"], True, False, backplates, pin_accents, label_accents)
        board.alpha_composite(default_sample.resize((default_sample.width * 2, 160), Image.Resampling.NEAREST), (400, y))
        board.alpha_composite(selected_sample.resize((selected_sample.width * 2, 160), Image.Resampling.NEAREST), (1120, y))
        if index == 3:
            left_sample = make_runtime_sample(spec["kind"], spec["title"], spec["meta"], True, True, backplates, pin_accents, label_accents)
            board.alpha_composite(left_sample.resize((left_sample.width * 2, 160), Image.Resampling.NEAREST), (1884, y))

    draw.rectangle((2480, 196, 2481, 1116), fill=(136, 106, 64, 255))
    draw_centered(draw, "地图安全边界", (2360, 1118, 2560, 1148), font(15), (203, 191, 159, 255))
    draw.text((90, 1190), "1× 原生读回（不放大）", font=font(20), fill=PAPER_TEXT)
    native_sample = make_runtime_sample("hidden", SPECS[3]["title"], SPECS[3]["meta"], True, False, backplates, pin_accents, label_accents)
    board.alpha_composite(native_sample, (470, 1170))
    draw.text((850, 1188), "合同：pin 64×80｜hit 72×80｜anchor [36,76]｜label 200×72｜content [14,8,166,56]", font=font(17), fill=(174, 188, 154, 255))
    draw.text((850, 1234), "本图只验证缩小可读性、独立图层与左右挂签；不是生产 atlas，也不是 Godot 正式替换。", font=font(17), fill=(203, 191, 159, 255))

    native = Image.new("RGBA", (1280, 720), BOARD_COLOR)
    native_draw = ImageDraw.Draw(native)
    draw_centered(native_draw, "1× 原生尺寸读回｜四类选中背板", (48, 28, 1232, 74), font(28), PAPER_TEXT)
    origins = [(120, 126), (700, 126), (120, 382), (700, 382)]
    for spec, origin in zip(SPECS, origins):
        sample = make_runtime_sample(spec["kind"], spec["title"], spec["meta"], True, False, backplates, pin_accents, label_accents)
        native.alpha_composite(sample, origin)
    native_draw.text((48, 650), "程序仅负责严格尺寸、四色规范化和动态中文排版；纸件轮廓与材质来自生图源。", font=font(16), fill=(174, 188, 154, 255))
    return board, native


def checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    width, height = size
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    colors = [(30, 49, 62, 255), (43, 65, 78, 255)]
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            draw.rectangle((x, y, min(x + cell - 1, width - 1), min(y + cell - 1, height - 1)), fill=colors[((x // cell) + (y // cell)) % 2])
    return result


def contain(image: Image.Image, box: tuple[int, int], padding: int = 10) -> Image.Image:
    width, height = box
    available = (max(1, width - padding * 2), max(1, height - padding * 2))
    scale = min(available[0] / image.width, available[1] / image.height)
    resized = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), Image.Resampling.LANCZOS)
    result = Image.new("RGBA", box, (0, 0, 0, 0))
    result.alpha_composite(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    return result


def draw_layer_tile(
    sheet: Image.Image,
    position: tuple[int, int],
    size: tuple[int, int],
    title: str,
    subtitle: str,
    layer: Image.Image,
    badge: str,
) -> None:
    x, y = position
    width, height = size
    draw = ImageDraw.Draw(sheet)
    draw.rounded_rectangle((x, y, x + width, y + height), radius=10, fill=(12, 36, 52, 255), outline=(103, 125, 130, 255), width=2)
    draw.text((x + 14, y + 10), title, font=font(18), fill=PAPER_TEXT)
    draw.text((x + 14, y + 38), subtitle, font=font(12), fill=(174, 188, 154, 255))
    badge_color = (52, 118, 122, 255) if badge == "程序" else (127, 138, 71, 255)
    badge_bounds = draw.textbbox((0, 0), badge, font=font(12))
    badge_width = badge_bounds[2] - badge_bounds[0] + 20
    draw.rounded_rectangle((x + width - badge_width - 12, y + 10, x + width - 12, y + 34), radius=6, fill=badge_color)
    draw_centered(draw, badge, (x + width - badge_width - 12, y + 10, x + width - 12, y + 34), font(12), PAPER_TEXT)
    preview_box = (width - 28, height - 86)
    preview = checkerboard(preview_box)
    preview.alpha_composite(contain(layer, preview_box, 14))
    sheet.alpha_composite(preview, (x + 14, y + 70))


def build_exploded_sheet(backplates: Image.Image, pin_accents: Image.Image, label_accents: Image.Image) -> Image.Image:
    sheet = Image.new("RGBA", (1920, 1080), BOARD_COLOR)
    draw = ImageDraw.Draw(sheet)
    draw_centered(draw, "区域任务短签｜实际拆图与运行合成", (60, 28, 1860, 76), font(32), PAPER_TEXT)
    draw_centered(draw, "所有格子展示真实透明层；绿色标签＝美术位图，青色标签＝Godot 动态内容", (60, 76, 1860, 108), font(16), (174, 188, 154, 255))

    kind = "permanent"
    index = kind_index(kind)
    backplate = atlas_frame(backplates, index, (216, 240))
    pin_shell = Image.open(PIN_SOURCE).convert("RGBA")
    pin_accent = atlas_frame(pin_accents, index, (192, 240))
    icon = atlas_frame(Image.open(ICON_SOURCE).convert("RGBA"), icon_index(kind), (84, 84))
    label_base = Image.open(LABEL_SOURCE).convert("RGBA")
    label_accent = atlas_frame(label_accents, index, (400, 144))

    text_layer = Image.new("RGBA", (400, 144), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    text_draw.text((28, 18), "罗斯威尔档案残页", font=font(30), fill=INK)
    text_draw.text((28, 76), "常驻调查 · 1天", font=font(24), fill=MUTED_INK)

    selected_sample = make_runtime_sample(kind, "罗斯威尔档案残页", "常驻调查 · 1天", True, False, backplates, pin_accents, label_accents)
    final_preview = selected_sample.resize((556, 160), Image.Resampling.NEAREST)
    draw.rounded_rectangle((58, 132, 648, 360), radius=12, fill=(12, 36, 52, 255), outline=(214, 194, 171, 255), width=2)
    draw.text((78, 148), "最终运行组合｜常驻任务 · 选中", font=font(22), fill=PAPER_TEXT)
    draw.text((78, 180), "运行 278×80（此处整数 2× 展示）", font=font(13), fill=(174, 188, 154, 255))
    sheet.alpha_composite(final_preview, (76, 210))

    draw.text((700, 132), "A. 图钉子组件：四张透明层叠加", font=font(22), fill=PAPER_TEXT)
    pin_tiles = [
        ("01 selected_backplate", "源 216×240 → 运行 72×80｜z10", backplate, "美术"),
        ("02 neutral_pin_shell", "源 192×240 → 运行 64×80｜z21", pin_shell, "美术"),
        ("03 pin_type_accent", "源 192×240 → 运行 64×80｜z30", pin_accent, "美术"),
        ("04 kind_icon", "源 84×84 → 运行 28×28｜z40", icon, "美术"),
    ]
    for tile_index, tile in enumerate(pin_tiles):
        draw_layer_tile(sheet, (700 + tile_index * 298, 174), (276, 270), *tile)
        if tile_index < len(pin_tiles) - 1:
            draw.text((970 + tile_index * 298, 292), "+", font=font(30), fill=(203, 191, 159, 255))

    draw.text((58, 480), "B. 短签子组件：底纸、类型端帽与动态文字分离", font=font(22), fill=PAPER_TEXT)
    label_tiles = [
        ("05 neutral_label_base", "源 400×144 → 运行 200×72｜z20", label_base, "美术"),
        ("06 label_type_accent", "源 400×144 → 运行 200×72｜z30", label_accent, "美术"),
        ("07 dynamic_text", "运行 content_rect [14,8,166,56]｜z50", text_layer, "程序"),
    ]
    for tile_index, tile in enumerate(label_tiles):
        draw_layer_tile(sheet, (58 + tile_index * 488, 522), (454, 238), *tile)
        if tile_index < len(label_tiles) - 1:
            draw.text((518 + tile_index * 488, 620), "+", font=font(30), fill=(203, 191, 159, 255))

    final_label = Image.new("RGBA", (400, 144), (0, 0, 0, 0))
    final_label.alpha_composite(label_base)
    final_label.alpha_composite(label_accent)
    final_label.alpha_composite(text_layer)
    draw_layer_tile(sheet, (1522, 522), (340, 238), "08 final_label", "源 400×144 → 运行 200×72", final_label, "合成")

    draw.text((58, 798), "C. 同一背板 alpha，四种预着色 frame", font=font(22), fill=PAPER_TEXT)
    color_names = ["常驻 · 橄榄绿", "限时 · 赭黄", "连续 · 青绿", "隐藏 · 蓝灰"]
    for frame_index, color_name in enumerate(color_names):
        frame = atlas_frame(backplates, frame_index, (216, 240))
        tile_x = 58 + frame_index * 282
        draw.rounded_rectangle((tile_x, 842, tile_x + 252, 1026), radius=10, fill=(12, 36, 52, 255), outline=(103, 125, 130, 255), width=2)
        preview = checkerboard((132, 132), 10)
        preview.alpha_composite(contain(frame, (132, 132), 6))
        sheet.alpha_composite(preview, (tile_x + 12, 876))
        draw.text((tile_x + 154, 880), color_name, font=font(15), fill=PAPER_TEXT)
        draw.text((tile_x + 154, 910), "frame 216×240", font=font(12), fill=(174, 188, 154, 255))
        draw.text((tile_x + 154, 936), "运行 72×80", font=font(12), fill=(174, 188, 154, 255))
        draw.text((tile_x + 154, 970), "轮廓完全一致", font=font(12), fill=(203, 191, 159, 255))

    draw.rounded_rectangle((1206, 842, 1862, 1026), radius=10, fill=(12, 36, 52, 255), outline=(136, 106, 64, 255), width=2)
    draw.text((1230, 864), "合成规则", font=font(20), fill=PAPER_TEXT)
    rules = [
        "selected 才显示 01；default 从 02 开始",
        "类型色只在 01 / 03 / 06，流程状态另走 overlay",
        "标题与 meta 永远不进入 PNG",
        "外投影、锚点、避让、clamp 与 cluster 仍由 Godot 承担",
    ]
    for rule_index, rule in enumerate(rules):
        draw.text((1230, 906 + rule_index * 27), "• " + rule, font=font(13), fill=(174, 188, 154, 255))
    return sheet


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    backplate_path = OUTPUT_DIR / "rt-task-pin-selected-backplates-v1-atlas-3x.png"
    pin_accent_path = OUTPUT_DIR / "rt-task-pin-type-accents-v1-atlas-3x.png"
    label_accent_path = OUTPUT_DIR / "rt-task-label-type-accents-v1-atlas-2x.png"

    build_backplate_atlas().save(backplate_path)
    build_accent_atlas(PIN_SOURCE, "pin").save(pin_accent_path)
    build_accent_atlas(LABEL_SOURCE, "label").save(label_accent_path)

    backplates = Image.open(backplate_path).convert("RGBA")
    pin_accents = Image.open(pin_accent_path).convert("RGBA")
    label_accents = Image.open(label_accent_path).convert("RGBA")
    contract_board, native_readback = build_contract_boards(backplates, pin_accents, label_accents)
    exploded_sheet = build_exploded_sheet(backplates, pin_accents, label_accents)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    contract_board.save(BOARD_OUTPUT)
    contract_board.save(SCREENSHOT_DIR / "01-contract-scale-content-fill.png")
    native_readback.save(SCREENSHOT_DIR / "02-native-1x-selected-readback.png")
    exploded_sheet.save(EXPLODED_OUTPUT)
    exploded_sheet.save(SCREENSHOT_DIR / "03-layer-exploded-sheet.png")

    frames_dir = OUTPUT_DIR / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for frame_index, kind in enumerate(FRAME_ORDER):
        atlas_frame(backplates, frame_index, (216, 240)).save(frames_dir / ("selected-backplate-%s-v1-3x.png" % kind))
        atlas_frame(pin_accents, frame_index, (192, 240)).save(frames_dir / ("pin-type-accent-%s-v1-3x.png" % kind))
        atlas_frame(label_accents, frame_index, (400, 144)).save(frames_dir / ("label-type-accent-%s-v1-2x.png" % kind))

    manifest = {
        "id": "region_task_selected_backplate_runtime_preflight_v1",
        "status": "preflight_only_not_production_atlas",
        "frame_order": FRAME_ORDER,
        "type_colors": {kind: "#%02X%02X%02X" % TYPE_COLORS[kind] for kind in FRAME_ORDER},
        "assets": {
            "selected_backplates": {
                "path": str(backplate_path.relative_to(ROOT)).replace("\\", "/"),
                "frame_size": [216, 240],
                "runtime_size": [72, 80],
            },
            "pin_type_accents": {
                "path": str(pin_accent_path.relative_to(ROOT)).replace("\\", "/"),
                "frame_size": [192, 240],
                "runtime_size": [64, 80],
            },
            "label_type_accents": {
                "path": str(label_accent_path.relative_to(ROOT)).replace("\\", "/"),
                "frame_size": [400, 144],
                "runtime_size": [200, 72],
            },
        },
        "frozen_contract": {
            "pin_visual_size": [64, 80],
            "pin_hit_size": [72, 80],
            "anchor_in_hit_control": [36, 76],
            "label_size": [200, 72],
            "label_content_rect": [14, 8, 166, 56],
        },
    }
    (OUTPUT_DIR / "runtime-preflight-assets-v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(backplate_path)
    print(pin_accent_path)
    print(label_accent_path)


if __name__ == "__main__":
    main()
