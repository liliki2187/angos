from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "design" / "art-direction" / "region-task-board" / "runtime-preflight-v4-single-probe"
SELECTED_SOURCE = SOURCE_DIR / "01-permanent-selected-right-compound-source-v4-alpha.png"
DEFAULT_SOURCE = SOURCE_DIR / "02-permanent-default-right-compound-source-v4-alpha.png"
SELECTED_FRAME_3X = SOURCE_DIR / "rt-task-compound-permanent-selected-right-v4-3x.png"
SELECTED_FRAME_1X = SOURCE_DIR / "rt-task-compound-permanent-selected-right-v4-1x.png"
DEFAULT_FRAME_3X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v4-3x.png"
DEFAULT_FRAME_1X = SOURCE_DIR / "rt-task-compound-permanent-default-right-v4-1x.png"
PIN_ONLY_CHROMA = SOURCE_DIR / "03-permanent-default-pin-only-source-v4-chroma.png"
PIN_ONLY_ALPHA = SOURCE_DIR / "03-permanent-default-pin-only-source-v4-alpha.png"
PIN_ONLY_FRAME_3X = SOURCE_DIR / "rt-task-pin-permanent-default-v4-3x.png"
PIN_ONLY_FRAME_1X = SOURCE_DIR / "rt-task-pin-permanent-default-v4-1x.png"
GODOT_FIXTURE_DIR = ROOT / "gd_project" / "tests" / "fixtures" / "region_task_compound_probe_v4"
SELECTED_GODOT_FIXTURE = GODOT_FIXTURE_DIR / SELECTED_FRAME_3X.name
DEFAULT_GODOT_FIXTURE = GODOT_FIXTURE_DIR / DEFAULT_FRAME_3X.name
PIN_ONLY_GODOT_FIXTURE = GODOT_FIXTURE_DIR / PIN_ONLY_FRAME_3X.name
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "2026-07-21-region-task-single-compound-probe-v4"
QA_BOARD = SCREENSHOT_DIR / "01-transparent-compound-and-joint-v4.png"
STATE_PAIR_QA = SCREENSHOT_DIR / "04-default-selected-transparent-qa-v4.png"
STATE_ASSET_QA = SCREENSHOT_DIR / "05-default-hover-selected-asset-qa-v4.png"
STATE_FRAME_DIR = SCREENSHOT_DIR / "frames-state-chain-v4"
STATE_GIF = SCREENSHOT_DIR / "07-hover-selected-runtime-demo-v4.gif"
GODOT_SCREENSHOT = SCREENSHOT_DIR / "02-godot-1x-map-placement-v4.png"
GODOT_DETAIL = SCREENSHOT_DIR / "03-godot-1x-pin-detail-v4.png"
METADATA = SOURCE_DIR / "single-compound-probe-v4.json"

FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")

BG = (5, 29, 43, 255)
PAPER_TEXT = (236, 226, 202, 255)
MUTED_TEXT = (174, 188, 154, 255)
GOOD = (99, 166, 125, 255)

TARGET_3X = (834, 240)
TARGET_1X = (278, 80)
PIN_TARGET_3X = (192, 240)
PIN_TARGET_1X = (64, 80)
LEFT_FIXED_3X = 240
RIGHT_FIXED_3X = 60
SELECTED_LEFT_PAD_3X = 2
DEFAULT_LEFT_PAD_3X = 12


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    source = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(source), size=size)


def alpha_bbox(image: Image.Image, threshold: int = 24) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise RuntimeError("compound source has no visible alpha")
    return bbox


def horizontal_three_slice(image: Image.Image, target_width: int, left_fixed: int, right_fixed: int) -> Image.Image:
    if image.width <= left_fixed + right_fixed:
        raise ValueError("source is too narrow for the fixed slices")
    if target_width <= left_fixed + right_fixed:
        raise ValueError("target is too narrow for the fixed slices")
    result = Image.new("RGBA", (target_width, image.height), (0, 0, 0, 0))
    left = image.crop((0, 0, left_fixed, image.height))
    center = image.crop((left_fixed, 0, image.width - right_fixed, image.height))
    right = image.crop((image.width - right_fixed, 0, image.width, image.height))
    center_width = target_width - left_fixed - right_fixed
    center = center.resize((center_width, image.height), Image.Resampling.LANCZOS)
    result.alpha_composite(left, (0, 0))
    result.alpha_composite(center, (left_fixed, 0))
    result.alpha_composite(right, (target_width - right_fixed, 0))
    return result


def tip_center_x(image: Image.Image, threshold: int = 24) -> float:
    alpha = image.getchannel("A")
    for y in range(image.height - 1, max(-1, image.height - 18), -1):
        xs = [x for x in range(image.width) if alpha.getpixel((x, y)) > threshold]
        if xs:
            return (min(xs) + max(xs)) / 2.0
    raise RuntimeError("unable to locate the bottom tip")


def connected_components(image: Image.Image, threshold: int = 24) -> list[int]:
    alpha = image.getchannel("A")
    width, height = image.size
    pixels = alpha.load()
    visited = bytearray(width * height)
    components: list[int] = []
    for y in range(height):
        for x in range(width):
            offset = y * width + x
            if visited[offset] or pixels[x, y] <= threshold:
                continue
            visited[offset] = 1
            queue = deque([(x, y)])
            count = 0
            while queue:
                current_x, current_y = queue.popleft()
                count += 1
                for next_x, next_y in (
                    (current_x - 1, current_y),
                    (current_x + 1, current_y),
                    (current_x, current_y - 1),
                    (current_x, current_y + 1),
                ):
                    if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
                        continue
                    next_offset = next_y * width + next_x
                    if visited[next_offset] or pixels[next_x, next_y] <= threshold:
                        continue
                    visited[next_offset] = 1
                    queue.append((next_x, next_y))
            if count > 16:
                components.append(count)
    return components


def remove_connected_chroma(image: Image.Image) -> tuple[Image.Image, dict]:
    source = image.convert("RGBA")
    width, height = source.size
    pixels = source.load()
    border_samples = []
    for x in range(width):
        border_samples.extend((pixels[x, 0][:3], pixels[x, height - 1][:3]))
    for y in range(height):
        border_samples.extend((pixels[0, y][:3], pixels[width - 1, y][:3]))
    key = tuple(sorted(sample[channel] for sample in border_samples)[len(border_samples) // 2] for channel in range(3))

    def is_key_candidate(rgb: tuple[int, int, int]) -> bool:
        red, green, blue = rgb
        distance = ((red - key[0]) ** 2 + (green - key[1]) ** 2 + (blue - key[2]) ** 2) ** 0.5
        return distance < 150 and red > green + 58 and blue > green + 48 and red > 170 and blue > 135

    background = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()
    for x in range(width):
        for y in (0, height - 1):
            if is_key_candidate(pixels[x, y][:3]):
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if is_key_candidate(pixels[x, y][:3]):
                queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        offset = y * width + x
        if background[offset] or not is_key_candidate(pixels[x, y][:3]):
            continue
        background[offset] = 1
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= next_x < width and 0 <= next_y < height and not background[next_y * width + next_x]:
                queue.append((next_x, next_y))

    result = source.copy()
    result_pixels = result.load()
    transparent = 0
    for y in range(height):
        for x in range(width):
            if background[y * width + x]:
                result_pixels[x, y] = (0, 0, 0, 0)
                transparent += 1
            else:
                red, green, blue, _alpha = result_pixels[x, y]
                if red > green + 36 and blue > green + 30:
                    neutral = max(green, min(red, 238))
                    result_pixels[x, y] = (neutral, green, min(neutral, blue), 255)
                else:
                    result_pixels[x, y] = (red, green, blue, 255)
    return result, {
        "sampled_key": "#%02x%02x%02x" % key,
        "transparent_pixels": transparent,
        "total_pixels": width * height,
        "method": "border-connected magenta flood; hard high-resolution matte before downscale",
    }


def build_pin_only_frame(source: Image.Image) -> tuple[Image.Image, Image.Image, dict]:
    source_bbox = alpha_bbox(source)
    cropped = source.crop(source_bbox)
    scaled_width = round(cropped.width * PIN_TARGET_3X[1] / cropped.height)
    scaled = cropped.resize((scaled_width, PIN_TARGET_3X[1]), Image.Resampling.LANCZOS)
    local_tip = tip_center_x(scaled)
    left_pad = round(PIN_TARGET_3X[0] / 2.0 - local_tip)
    if left_pad < 0 or left_pad + scaled.width > PIN_TARGET_3X[0]:
        raise RuntimeError(f"pin-only frame does not fit target: pad={left_pad}, width={scaled.width}")
    frame_3x = Image.new("RGBA", PIN_TARGET_3X, (0, 0, 0, 0))
    frame_3x.alpha_composite(scaled, (left_pad, 0))
    frame_1x = frame_3x.resize(PIN_TARGET_1X, Image.Resampling.LANCZOS)
    components_3x = connected_components(frame_3x)
    components_1x = connected_components(frame_1x)
    if len(components_3x) != 1 or len(components_1x) != 1:
        raise RuntimeError(f"pin-only alpha is not singular: 3x={components_3x}, 1x={components_1x}")
    return frame_3x, frame_1x, {
        "source_bbox": list(source_bbox),
        "source_crop_size": list(cropped.size),
        "scaled_size": list(scaled.size),
        "frame_3x": list(frame_3x.size),
        "frame_1x": list(frame_1x.size),
        "left_padding_3x": left_pad,
        "tip_center_x_3x": round(tip_center_x(frame_3x), 2),
        "tip_center_x_1x": round(tip_center_x(frame_1x), 2),
        "target_tip_center_x_3x": 96,
        "target_tip_center_x_1x": 32,
        "components_3x": len(components_3x),
        "components_1x": len(components_1x),
    }


def checker(size: tuple[int, int], step: int = 20) -> Image.Image:
    image = Image.new("RGBA", size, (26, 51, 64, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2 == 0:
                draw.rectangle((x, y, min(size[0] - 1, x + step - 1), min(size[1] - 1, y + step - 1)), fill=(38, 69, 82, 255))
    return image


def build_runtime_frames(source_path: Path, left_pad_3x: int) -> tuple[Image.Image, Image.Image, dict]:
    source = Image.open(source_path).convert("RGBA")
    source_bbox = alpha_bbox(source)
    cropped = source.crop(source_bbox)
    scaled_width = round(cropped.width * TARGET_3X[1] / cropped.height)
    scaled = cropped.resize((scaled_width, TARGET_3X[1]), Image.Resampling.LANCZOS)

    content_width = TARGET_3X[0] - left_pad_3x
    expanded = horizontal_three_slice(scaled, content_width, LEFT_FIXED_3X, RIGHT_FIXED_3X)
    frame_3x = Image.new("RGBA", TARGET_3X, (0, 0, 0, 0))
    frame_3x.alpha_composite(expanded, (left_pad_3x, 0))
    frame_1x = frame_3x.resize(TARGET_1X, Image.Resampling.LANCZOS)

    components_3x = connected_components(frame_3x)
    components_1x = connected_components(frame_1x)
    if len(components_3x) != 1 or len(components_1x) != 1:
        raise RuntimeError(f"compound alpha is not singular: 3x={components_3x}, 1x={components_1x}")

    metrics = {
        "source_bbox": list(source_bbox),
        "source_crop_size": list(cropped.size),
        "scaled_size_before_three_slice": list(scaled.size),
        "frame_3x": list(frame_3x.size),
        "frame_1x": list(frame_1x.size),
        "tip_center_x_3x": round(tip_center_x(frame_3x), 2),
        "tip_center_x_1x": round(tip_center_x(frame_1x), 2),
        "target_anchor_x_3x": 108,
        "target_anchor_x_1x": 36,
        "components_3x": len(components_3x),
        "components_1x": len(components_1x),
        "three_slice": {
            "left_fixed_3x": LEFT_FIXED_3X,
            "right_fixed_3x": RIGHT_FIXED_3X,
            "left_padding_3x": left_pad_3x,
            "rule": "only the calm central writable paper face is extended; the pin head, shared shoulder and far type cap remain fixed",
        },
    }
    return frame_3x, frame_1x, metrics


def build_qa_board(frame_1x: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1600, 760), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "单例真实美术资源｜常驻 selected 右挂", font=font(30, True), fill=PAPER_TEXT)
    draw.text((48, 78), "同一候选：透明 compound 全体 + 接合肩局部；不是多版方案", font=font(17), fill=MUTED_TEXT)

    full = frame_1x.resize((1112, 320), Image.Resampling.NEAREST)
    full_bg = checker((1160, 368), 32)
    full_bg.alpha_composite(full, (24, 24))
    board.alpha_composite(full_bg, (48, 132))

    joint = frame_1x.crop((0, 0, 128, 80)).resize((512, 320), Image.Resampling.NEAREST)
    joint_bg = checker((560, 368), 32)
    joint_bg.alpha_composite(joint, (24, 24))
    board.alpha_composite(joint_bg, (990, 132))

    draw.text((48, 530), "完整 compound｜4×", font=font(18, True), fill=PAPER_TEXT)
    draw.text((990, 530), "共享肩局部｜4×", font=font(18, True), fill=PAPER_TEXT)
    notes = [
        "✓ 前纸只有一圈连续模切外轮廓；pin 连接侧没有独立封边",
        "✓ selected 橄榄后衬只在头部外侧露出，回边藏在前纸下面",
        "✓ 中央延展只发生在无字纸面；pin 头、共享肩和远端类型帽不拉伸",
    ]
    for index, line in enumerate(notes):
        draw.text((48, 590 + index * 40), line, font=font(16), fill=GOOD)
    return board


def build_state_pair_qa(default_1x: Image.Image, selected_1x: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1600, 760), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "常驻右挂状态资源｜default / selected", font=font(30, True), fill=PAPER_TEXT)
    draw.text((48, 78), "同一母结构：前纸、共享肩、文字区与右端帽保持；selected 只增加后层橄榄背纸", font=font(17), fill=MUTED_TEXT)

    for x, label, image in (
        (48, "DEFAULT｜无 selected 后衬", default_1x),
        (820, "SELECTED｜增加橄榄后衬", selected_1x),
    ):
        full_bg = checker((700, 224), 24)
        full_bg.alpha_composite(image.resize((556, 160), Image.Resampling.NEAREST), (24, 32))
        board.alpha_composite(full_bg, (x, 132))
        draw.text((x, 374), label, font=font(18, True), fill=PAPER_TEXT)

        joint = image.crop((0, 0, 128, 80)).resize((512, 320), Image.Resampling.NEAREST)
        joint_bg = checker((560, 336), 32)
        joint_bg.alpha_composite(joint, (24, 8))
        board.alpha_composite(joint_bg, (x, 416))

    draw.text((48, 714), "共享肩 4×：两态位置不变；default 不含后衬，selected 后衬只位于前纸下方", font=font(16), fill=GOOD)
    return board


def build_state_asset_qa(pin_1x: Image.Image, default_1x: Image.Image, selected_1x: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1600, 660), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "常驻右挂三态资产｜idle / hover / selected", font=font(30, True), fill=PAPER_TEXT)
    draw.text((48, 78), "真实透明资源：idle 匹配 v4 头部；hover 无后衬；selected 增加美术后衬", font=font(17), fill=MUTED_TEXT)
    cells = (
        (48, "IDLE｜pin-only", pin_1x, (256, 320)),
        (430, "HOVER｜default compound", default_1x, (556, 160)),
        (1018, "SELECTED｜selected compound", selected_1x, (556, 160)),
    )
    for x, label, asset, asset_size in cells:
        width = 334 if x == 48 else 534
        cell = checker((width, 380), 24)
        scaled = asset.resize(asset_size, Image.Resampling.NEAREST)
        cell.alpha_composite(scaled, ((width - asset_size[0]) // 2, 30))
        board.alpha_composite(cell, (x, 132))
        draw.text((x, 534), label, font=font(18, True), fill=PAPER_TEXT)
    draw.text((48, 594), "运行时只切换 / 淡入这些美术帧；图标与文字保持同坐标，程序不绘制 selected 底板", font=font(16), fill=GOOD)
    return board


def build_godot_detail() -> Image.Image | None:
    if not GODOT_SCREENSHOT.exists():
        return None
    screenshot = Image.open(GODOT_SCREENSHOT).convert("RGBA")
    # 该区域来自 1920×1080 Godot 真实截图；这里只做整数倍放大与说明排版。
    crop = screenshot.crop((680, 374, 1012, 508))
    enlarged = crop.resize((996, 402), Image.Resampling.NEAREST)
    board = Image.new("RGBA", (1100, 560), BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 30), "Godot 真实 1× 组合｜放大检查", font=font(28, True), fill=PAPER_TEXT)
    draw.text((48, 72), "美术 compound + 现有类型图标 + 动态中文标题/时长；下图仅整数倍放大", font=font(16), fill=MUTED_TEXT)
    board.alpha_composite(enlarged, (52, 126))
    draw.rectangle((51, 125, 1048, 528), outline=(102, 143, 136, 255), width=1)
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
    GODOT_FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    selected_3x, selected_1x, selected_metrics = build_runtime_frames(SELECTED_SOURCE, SELECTED_LEFT_PAD_3X)
    default_3x, default_1x, default_metrics = build_runtime_frames(DEFAULT_SOURCE, DEFAULT_LEFT_PAD_3X)
    pin_source, pin_key_metrics = remove_connected_chroma(Image.open(PIN_ONLY_CHROMA))
    pin_source.save(PIN_ONLY_ALPHA)
    pin_3x, pin_1x, pin_metrics = build_pin_only_frame(pin_source)
    selected_3x.save(SELECTED_FRAME_3X)
    selected_3x.save(SELECTED_GODOT_FIXTURE)
    selected_1x.save(SELECTED_FRAME_1X)
    default_3x.save(DEFAULT_FRAME_3X)
    default_3x.save(DEFAULT_GODOT_FIXTURE)
    default_1x.save(DEFAULT_FRAME_1X)
    pin_3x.save(PIN_ONLY_FRAME_3X)
    pin_3x.save(PIN_ONLY_GODOT_FIXTURE)
    pin_1x.save(PIN_ONLY_FRAME_1X)
    build_qa_board(selected_1x).save(QA_BOARD)
    build_state_pair_qa(default_1x, selected_1x).save(STATE_PAIR_QA)
    build_state_asset_qa(pin_1x, default_1x, selected_1x).save(STATE_ASSET_QA)
    godot_detail = build_godot_detail()
    if godot_detail is not None:
        godot_detail.save(GODOT_DETAIL)
    gif_frame_count = build_state_chain_gif()
    METADATA.write_text(
        json.dumps(
            {
                "id": "region_task_permanent_selected_right_compound_probe_v4",
                "status": "single_art_probe_pending_user_review",
                "production_integration": False,
                "runtime_contract": {
                    "compound": [278, 80],
                    "pin_hit": [72, 80],
                    "anchor_in_hit": [36, 76],
                    "caption_rect": [78, 4, 200, 72],
                    "text_content": [14, 12, 158, 48],
                },
                "metrics": {
                    "selected": selected_metrics,
                    "default": default_metrics,
                    "pin_only": pin_metrics,
                    "pin_only_key_removal": pin_key_metrics,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(SELECTED_FRAME_3X)
    print(SELECTED_GODOT_FIXTURE)
    print(DEFAULT_FRAME_3X)
    print(DEFAULT_GODOT_FIXTURE)
    print(PIN_ONLY_FRAME_3X)
    print(PIN_ONLY_GODOT_FIXTURE)
    print(QA_BOARD)
    print(STATE_PAIR_QA)
    print(STATE_ASSET_QA)
    if godot_detail is not None:
        print(GODOT_DETAIL)
    if gif_frame_count:
        print(f"{STATE_GIF} ({gif_frame_count} Godot frames)")


if __name__ == "__main__":
    main()
