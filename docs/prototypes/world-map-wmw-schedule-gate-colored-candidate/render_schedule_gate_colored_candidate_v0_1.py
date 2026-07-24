from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
SOURCE = ROOT / "wmw-schedule-gate-material-ingredients-imagegen-source-v0-1.png"
SPEC_PATH = ROOT.parent / "world-map-wmw-black-white-structure" / "schedule-gate-v0-1-candidate-spec.json"
ATLAS = REPO / "docs" / "screenshots" / "2026-07-01-wmw-component-correction" / "paper-material-atlas-clean-v3"

WORK_SIZE = (1368, 984)
MASTER_SIZE = (456, 328)
RUNTIME_SIZE = (342, 246)
BOARD_SIZE = (1920, 1080)

WORK_OUTPUT = ROOT / "wmw-schedule-gate-no-text-work-1368x984-v0-1.png"
MASTER_OUTPUT = ROOT / "wmw-schedule-gate-no-text-master-456x328-v0-1.png"
RUNTIME_OUTPUT = ROOT / "wmw-schedule-gate-no-text-runtime-342x246-v0-1.png"
MATERIAL_MANIFEST = ROOT / "wmw-schedule-gate-material-ingredients-v0-1-manifest.json"
AUDIT_OUTPUT = ROOT / "wmw-schedule-gate-colored-v0-1-audit.json"
BOARD_MATERIAL = ROOT / "wmw-schedule-gate-colored-v0-1-material-geometry-review-1920x1080.png"
BOARD_STATES = ROOT / "wmw-schedule-gate-colored-v0-1-runtime-states-review-1920x1080.png"
BOARD_PIPELINE = ROOT / "wmw-schedule-gate-colored-v0-1-full-pipeline-walkthrough-1920x1080.png"

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_SYMBOL = Path(r"C:\Windows\Fonts\seguisym.ttf")

INK = (31, 36, 37)
INK_MUTED = (67, 72, 70)
PAPER = (183, 164, 136)
PAPER_QUIET = (188, 172, 148)
IVORY = (192, 185, 179)
OLIVE = (83, 100, 61)
OLIVE_DARK = (63, 76, 45)
RUST = (126, 72, 48)
TEAL = (48, 67, 67)
DISABLED = (103, 101, 84)
WHITE = (241, 237, 226)


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def font(size: int, bold: bool = False, symbol: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_SYMBOL if symbol else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(str(path), size=size)


F10 = font(10)
F11 = font(11)
F12 = font(12)
F13 = font(13)
F14 = font(14)
F14B = font(14, bold=True)
F16 = font(16)
F18 = font(18)
F18B = font(18, bold=True)
F22B = font(22, bold=True)
F22S = font(22, symbol=True)
F26B = font(26, bold=True)
F32B = font(32, bold=True)
F34B = font(34, bold=True)


SOURCE_CROPS = {
    "warm": (30, 32, 712, 512),
    "olive": (760, 32, 1444, 512),
    "ivory": (30, 555, 712, 1032),
    "ink": (760, 555, 1444, 1032),
}

TARGETS = {
    "warm": PAPER,
    "olive": OLIVE,
    "ivory": IVORY,
    "ink": INK,
}

ATLAS_TILES = {
    "warm": ATLAS / "warm_paper_tile.png",
    "ivory": ATLAS / "ivory_edge_tile.png",
    "ink": ATLAS / "dark_board_tile.png",
}

WORK_RECTS = {
    "component": [0, 0, 1368, 984],
    "date": [64, 64, 1240, 192],
    "action": [48, 296, 1272, 400],
    "icon": [104, 352, 280, 280],
    "info_1": [64, 728, 1240, 96],
    "info_2": [64, 840, 1240, 96],
    "separator_1": [64, 728, 1240, 4],
    "separator_2": [64, 840, 1240, 4],
}

RUNTIME_RECTS = {
    "component": [0, 0, 342, 246],
    "input_capture": [0, 0, 342, 246],
    "activation_hit": [12, 74, 318, 100],
    "section_safe": [12, 2, 116, 14],
    "date": [16, 16, 310, 48],
    "current_safe": [28, 26, 132, 28],
    "remaining_safe": [190, 26, 124, 28],
    "action": [12, 74, 318, 100],
    "icon": [26, 88, 70, 70],
    "icon_safe": [42, 104, 38, 38],
    "title_safe": [114, 88, 202, 34],
    "subtitle_safe": [114, 132, 202, 24],
    "info_1_safe": [16, 184, 310, 20],
    "info_2_safe": [16, 212, 310, 20],
}


def xyxy(rect: list[int] | tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    return x, y, x + w, y + h


def target_rgb(name: str) -> np.ndarray:
    return np.asarray(TARGETS[name], dtype=np.float32)


def tile_luminance(path: Path, size: tuple[int, int]) -> np.ndarray:
    tile = Image.open(path).convert("RGB").resize(size, Image.Resampling.BICUBIC)
    arr = np.asarray(tile, dtype=np.float32)
    return 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]


def normalize_material(crop: Image.Image, name: str, out_size: tuple[int, int]) -> Image.Image:
    source = ImageOps.fit(crop.convert("RGB"), out_size, method=Image.Resampling.LANCZOS)
    arr = np.asarray(source, dtype=np.float32)
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    source_delta = np.clip(lum - np.median(lum), -24, 24)

    atlas_delta = np.zeros_like(source_delta)
    atlas_path = ATLAS_TILES.get(name)
    if atlas_path:
        atlas_lum = tile_luminance(atlas_path, out_size)
        atlas_delta = np.clip(atlas_lum - np.median(atlas_lum), -12, 12)

    # Imagegen owns the broad planes; the existing paper atlas quietly locks the branch token.
    delta = source_delta * 0.48 + atlas_delta * 0.25
    if name == "ink":
        delta *= 0.28
    if name == "ivory":
        delta *= 0.42

    out = target_rgb(name)[None, None, :] + delta[:, :, None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGB")


def calm_rect(image: Image.Image, rect: list[int], amount: float = 0.55) -> None:
    x, y, w, h = rect
    crop = np.asarray(image.crop((x, y, x + w, y + h)).convert("RGB"), dtype=np.float32)
    median = np.median(crop.reshape(-1, 3), axis=0)
    crop = crop * (1.0 - amount) + median[None, None, :] * amount
    image.paste(Image.fromarray(np.clip(crop, 0, 255).astype(np.uint8), "RGB"), (x, y))


def mask_rect(size: tuple[int, int], rect: list[int], radius: int = 0) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    bounds = xyxy(rect)
    if radius:
        draw.rounded_rectangle(bounds, radius=radius, fill=255)
    else:
        draw.rectangle(bounds, fill=255)
    return mask


def paste_material(canvas: Image.Image, material: Image.Image, rect: list[int], radius: int = 0) -> None:
    x, y, w, h = rect
    fitted = ImageOps.fit(material, (w, h), method=Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(fitted.convert("RGBA"), (x, y))
    mask = mask_rect(canvas.size, rect, radius)
    canvas.alpha_composite(Image.composite(layer, Image.new("RGBA", canvas.size), mask))


def outline(draw: ImageDraw.ImageDraw, rect: list[int], color: tuple[int, int, int], width: int, radius: int = 0) -> None:
    if radius:
        draw.rounded_rectangle(xyxy(rect), radius=radius, outline=color + (255,), width=width)
    else:
        draw.rectangle(xyxy(rect), outline=color + (255,), width=width)


def material_stats(image: Image.Image) -> dict:
    arr = np.asarray(image.convert("RGB"), dtype=np.float32)
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    med = np.median(arr.reshape(-1, 3), axis=0)
    return {
        "median_rgb": [int(round(v)) for v in med],
        "mean_rgb": [round(float(v), 2) for v in np.mean(arr, axis=(0, 1))],
        "std_luminance": round(float(np.std(lum)), 2),
        "min_luminance": round(float(np.min(lum)), 2),
        "max_luminance": round(float(np.max(lum)), 2),
    }


source = Image.open(SOURCE).convert("RGB")
assert source.size[0] >= 1444 and source.size[1] >= 1032
spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

ingredient_images: dict[str, Image.Image] = {}
ingredient_records: dict[str, dict] = {}
for name, bounds in SOURCE_CROPS.items():
    crop = source.crop(bounds)
    crop_path = ROOT / f"wmw-schedule-gate-ingredient-{name}-imagegen-v0-1.png"
    crop.save(crop_path, optimize=True)
    normalized = normalize_material(crop, name, WORK_SIZE)
    normalized_path = ROOT / f"wmw-schedule-gate-ingredient-{name}-normalized-v0-1.png"
    normalized.save(normalized_path, optimize=True)
    ingredient_images[name] = normalized
    ingredient_records[name] = {
        "source_crop_xyxy": list(bounds),
        "source_crop_file": crop_path.name,
        "normalized_file": normalized_path.name,
        "source_crop_stats": material_stats(crop),
        "normalized_stats": material_stats(normalized),
        "target_rgb": list(TARGETS[name]),
    }

# Assemble exactly at runtime geometry x4, then downsample once to the 456x328 mother.
work = Image.new("RGBA", WORK_SIZE, (0, 0, 0, 0))
paste_material(work, ingredient_images["warm"], WORK_RECTS["component"])
paste_material(work, ingredient_images["warm"], WORK_RECTS["date"])
paste_material(work, ingredient_images["olive"], WORK_RECTS["action"])
paste_material(work, ingredient_images["ivory"], WORK_RECTS["icon"], radius=24)
paste_material(work, ingredient_images["warm"], WORK_RECTS["info_1"])
paste_material(work, ingredient_images["warm"], WORK_RECTS["info_2"])

# Calm every copy-safe carrier without flattening the surrounding low-poly planes.
rgb_work = work.convert("RGB")
for rect, amount in [
    ([48, 8, 464, 56], 0.74),
    ([112, 104, 528, 112], 0.72),
    ([760, 104, 496, 112], 0.72),
    ([456, 352, 808, 136], 0.70),
    ([456, 528, 808, 96], 0.70),
    ([64, 736, 1240, 80], 0.78),
    ([64, 848, 1240, 80], 0.78),
]:
    calm_rect(rgb_work, rect, amount)
work = rgb_work.convert("RGBA")

work_draw = ImageDraw.Draw(work)
outline(work_draw, WORK_RECTS["component"], INK, 12)
outline(work_draw, WORK_RECTS["date"], INK, 8)
outline(work_draw, WORK_RECTS["action"], INK, 12)
outline(work_draw, WORK_RECTS["icon"], INK, 8, radius=24)
work_draw.rectangle(xyxy(WORK_RECTS["separator_1"]), fill=INK + (255,))
work_draw.rectangle(xyxy(WORK_RECTS["separator_2"]), fill=INK_MUTED + (255,))

work.save(WORK_OUTPUT, optimize=True)
master = work.resize(MASTER_SIZE, Image.Resampling.LANCZOS)
master_arr = np.asarray(master).copy()
master_arr[master_arr[:, :, 3] == 0, :3] = 0
master = Image.fromarray(master_arr, "RGBA")
master.save(MASTER_OUTPUT, optimize=True)
runtime_base = master.resize(RUNTIME_SIZE, Image.Resampling.LANCZOS)
runtime_base.save(RUNTIME_OUTPUT, optimize=True)


def rect_contains(outer: list[int], inner_xyxy: tuple[int, int, int, int]) -> bool:
    ox, oy, ow, oh = outer
    x1, y1, x2, y2 = inner_xyxy
    return x1 >= ox and y1 >= oy and x2 <= ox + ow and y2 <= oy + oh


def safe_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    used_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    anchor: str,
    safe_rect: list[int],
    records: list[dict],
    key: str,
) -> None:
    bbox = draw.textbbox(xy, text, font=used_font, anchor=anchor)
    record = {
        "key": key,
        "text": text,
        "bbox_xyxy": list(bbox),
        "safe_rect_xywh": safe_rect,
        "passed": rect_contains(safe_rect, bbox),
    }
    records.append(record)
    draw.text(xy, text, font=used_font, fill=fill + (255,), anchor=anchor)


@dataclass(frozen=True)
class State:
    id: str
    label: str
    mode: str
    date_current: str
    date_remaining: str
    icon: str
    title: str
    subtitle: str
    info_1: str
    info_2: str


STATES = [
    State("idle", "01 · idle_enabled", "idle", "当前第 1 天", "剩余 7 天", "→", "推进到下一天", "点击后查看推进影响", "当前：无任务到期", "日程归零：进入编辑部阶段"),
    State("confirming", "02 · confirming", "confirming", "当前第 1 天", "剩余 7 天", "!", "确认推进到第 2 天", "再次点击执行 · 后果见下方", "确认后：剩余 6 天 · 无任务到期", "限时任务：雷达异常仍开放至第 4 天"),
    State("executing", "03 · executing", "executing", "当前第 1 天", "剩余 7 天", "…", "正在推进到第 2 天", "命令已提交 · 请稍候", "预计：剩余 6 天 · 无任务到期", "限时任务：雷达异常仍开放至第 4 天"),
    State("runtime-unavailable", "04 · runtime_unavailable", "disabled", "当前第 1 天", "剩余 7 天", "—", "推进功能暂不可用", "独立日程命令尚未接入", "当前：无任务到期", "请继续处理地区任务"),
    State("idle-error", "05 · idle_error", "error", "当前第 1 天", "剩余 7 天", "!", "推进未完成", "失败：结算结果未返回", "未消耗天数 · 日程保持不变", "再次点击推进区可重试"),
    State("confirming-last-day", "06 · confirming_last_day", "confirming", "当前第 7 天", "剩余 1 天", "!", "确认结束本周日程", "再次点击执行 · 将进入编辑部", "确认后：剩余 0 天 · 进入编辑部阶段", "到期提示：本次推进无任务到期"),
    State("zero-days", "07 · disabled_zero_days", "disabled", "本周日程结束", "剩余 0 天", "✓", "本周日程已结束", "正在进入编辑部阶段", "剩余 0 天 · 不可继续推进", "下一阶段：编辑部"),
]


def render_state(state: State) -> tuple[Image.Image, list[dict]]:
    image = runtime_base.copy()
    draw = ImageDraw.Draw(image)
    records: list[dict] = []

    # Only runtime overlays may carry state color; the mother itself stays neutral olive/warm paper.
    action_box = xyxy(RUNTIME_RECTS["action"])
    if state.mode == "confirming":
        draw.rounded_rectangle(action_box, radius=2, outline=RUST + (255,), width=3)
        draw.rectangle((15, 77, 327, 81), fill=RUST + (150,))
    elif state.mode == "executing":
        draw.rounded_rectangle(action_box, radius=2, outline=TEAL + (255,), width=3)
        for x in range(14, 329, 13):
            draw.line((x, 76, min(x + 12, 328), 86), fill=TEAL + (115,), width=1)
    elif state.mode == "disabled":
        draw.rounded_rectangle(action_box, radius=2, fill=DISABLED + (218,), outline=INK_MUTED + (255,), width=3)
        draw.rounded_rectangle(xyxy(RUNTIME_RECTS["icon"]), radius=6, fill=(176, 173, 158, 255), outline=INK_MUTED + (255,), width=2)
    elif state.mode == "error":
        draw.rounded_rectangle(action_box, radius=2, outline=RUST + (255,), width=3)
        draw.rectangle((15, 169, 327, 173), fill=RUST + (220,))

    section_fill = INK_MUTED
    date_fill = INK
    action_fill = WHITE if state.mode != "disabled" else (231, 226, 214)
    action_minor = (222, 218, 205) if state.mode != "disabled" else (215, 211, 199)
    info_fill = INK

    safe_text(draw, "全局日程", (12, 9), F11, section_fill, "lm", RUNTIME_RECTS["section_safe"], records, "section")
    safe_text(draw, state.date_current, (28, 40), F16, date_fill, "lm", RUNTIME_RECTS["current_safe"], records, "date_current")
    safe_text(draw, state.date_remaining, (314, 40), F16, date_fill, "rm", RUNTIME_RECTS["remaining_safe"], records, "date_remaining")
    safe_text(draw, state.icon, (61, 123), F22S, INK, "mm", RUNTIME_RECTS["icon_safe"], records, "icon")
    safe_text(draw, state.title, (114, 105), F22B, action_fill, "lm", RUNTIME_RECTS["title_safe"], records, "title")
    safe_text(draw, state.subtitle, (114, 144), F12, action_minor, "lm", RUNTIME_RECTS["subtitle_safe"], records, "subtitle")
    safe_text(draw, state.info_1, (16, 194), F12, info_fill, "lm", RUNTIME_RECTS["info_1_safe"], records, "info_1")
    safe_text(draw, state.info_2, (16, 222), F12, info_fill, "lm", RUNTIME_RECTS["info_2_safe"], records, "info_2")
    return image, records


state_images: dict[str, Image.Image] = {}
text_records: list[dict] = []
state_paths: dict[str, str] = {}
for state in STATES:
    state_image, records = render_state(state)
    out = ROOT / f"wmw-schedule-gate-state-{state.id}-342x246-v0-1.png"
    state_image.save(out, optimize=True)
    state_images[state.id] = state_image
    state_paths[state.id] = out.name
    for record in records:
        record["state"] = state.id
    text_records.extend(records)


PRESSURE_LINES = [
    "确认后：剩余 99 天 · 无任务到期",
    "确认后：剩余 99 天 · 到期 北境深层雷达异常",
    "确认后：剩余 99 天 · 到期 99 项",
    "确认后：剩余 99 天 · 到期 99+ 项",
    "预计：剩余 99 天 · 无任务到期",
    "预计：剩余 99 天 · 到期 北境深层雷达异常",
    "预计：剩余 99 天 · 到期 99 项",
    "预计：剩余 99 天 · 到期 99+ 项",
    "到期提示：本次推进无任务到期",
    "到期：北境深层雷达异常",
    "到期：99 项",
    "到期：99+ 项",
    "限时任务：无",
    "限时任务：北境深层雷达异常仍开放至第 99 天",
    "限时任务：99 项 · 最早第 99 天",
    "限时任务：99+ 项 · 最早第 99 天",
    "失败：服务器未返回结算结果",
    "未消耗天数 · 日程保持不变",
    "再次点击推进区可重试",
    "确认后：剩余 0 天 · 进入编辑部阶段",
]

pressure_image = Image.new("RGBA", RUNTIME_SIZE, (255, 255, 255, 255))
pressure_draw = ImageDraw.Draw(pressure_image)
pressure_records: list[dict] = []
for index, line in enumerate(PRESSURE_LINES):
    if line.startswith("失败："):
        safe_text(pressure_draw, line, (114, 144), F12, INK, "lm", RUNTIME_RECTS["subtitle_safe"], pressure_records, f"pressure_{index}")
    else:
        safe = RUNTIME_RECTS["info_2_safe"] if (line.startswith("到期") or line.startswith("限时") or line.startswith("再次")) else RUNTIME_RECTS["info_1_safe"]
        anchor = (16, 222) if safe is RUNTIME_RECTS["info_2_safe"] else (16, 194)
        safe_text(pressure_draw, line, anchor, F12, INK, "lm", safe, pressure_records, f"pressure_{index}")


def board_box(draw: ImageDraw.ImageDraw, rect: list[int], fill: tuple[int, int, int], outline_color: tuple[int, int, int] = INK, width: int = 2) -> None:
    draw.rectangle(xyxy(rect), fill=fill, outline=outline_color, width=width)


def board_text(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], used_font: ImageFont.FreeTypeFont, fill: tuple[int, int, int] = INK, anchor: str = "la") -> None:
    draw.text(xy, text, font=used_font, fill=fill, anchor=anchor)


def contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    return copy


# Board 1: actual source, no-text mother at 1:1, runtime replay, and geometry evidence.
board1 = Image.new("RGB", BOARD_SIZE, (225, 220, 207))
b1 = ImageDraw.Draw(board1)
board_text(b1, "WMW · SCHEDULE GATE 0.1 · MATERIAL / GEOMETRY", (36, 32), F34B)
board_text(b1, "真实 imagegen 配料 → 确定性 456×328 无字母版 → 342×246 runtime 回放", (36, 80), F18, INK_MUTED)
board_text(b1, "技术 QA 附录 · 用户无需裁决几何 / alpha / hash", (1884, 38), F14B, RUST, "ra")
board_text(b1, "TARGET ONLY · 非 Godot / 非正式合同 / 非有色整屏", (1884, 72), F12, INK_MUTED, "ra")
b1.line((36, 108, 1884, 108), fill=INK, width=2)

board_box(b1, [24, 126, 936, 918], (239, 235, 225))
board_text(b1, "A · imagegen 原始材料配料板（无字、非完整 UI）", (48, 146), F18B)
src_thumb = contain(source, (864, 624))
sx = 48 + (864 - src_thumb.width) // 2
sy = 184
board1.paste(src_thumb, (sx, sy))
b1.rectangle((sx, sy, sx + src_thumb.width, sy + src_thumb.height), outline=INK, width=2)
board_text(b1, f"源尺寸 {source.width}×{source.height} · SHA256 {digest(SOURCE)[:16]}…", (48, 832), F12, INK_MUTED)
board_text(b1, "四角色：warm / olive / ivory / ink；无 warning rust 与 teal。", (48, 858), F12)
for i, name in enumerate(["warm", "olive", "ivory", "ink"]):
    crop = Image.open(ROOT / f"wmw-schedule-gate-ingredient-{name}-normalized-v0-1.png").convert("RGB")
    swatch = ImageOps.fit(crop, (200, 112), method=Image.Resampling.LANCZOS)
    px = 48 + i * 216
    board1.paste(swatch, (px, 892))
    b1.rectangle((px, 892, px + 200, 1004), outline=INK, width=1)
    board_text(b1, name, (px + 8, 900), F12, WHITE)

board_box(b1, [984, 126, 912, 918], (239, 235, 225))
board_text(b1, "B · 同一母版与 runtime-local 几何", (1008, 146), F18B)
board1.paste(master.convert("RGB"), (1008, 184), master)
b1.rectangle((1008, 184, 1464, 512), outline=INK, width=2)
board_text(b1, "456×328 MASTER · 1:1", (1008, 524), F12, INK_MUTED)

board1.paste(runtime_base.convert("RGB"), (1518, 184), runtime_base)
b1.rectangle((1518, 184, 1860, 430), outline=INK, width=2)
board_text(b1, "342×246 runtime · 1:1", (1518, 442), F12, INK_MUTED)

geo = runtime_base.copy()
gd = ImageDraw.Draw(geo)
colors = {"date": (71, 99, 116), "action": RUST, "icon": (155, 122, 55), "current_safe": (75, 52, 96), "remaining_safe": (75, 52, 96), "title_safe": WHITE, "subtitle_safe": WHITE, "info_1_safe": (75, 52, 96), "info_2_safe": (75, 52, 96)}
for key, color in colors.items():
    gd.rectangle(xyxy(RUNTIME_RECTS[key]), outline=color + (255,), width=2)
board1.paste(geo.convert("RGB"), (1008, 582), geo)
b1.rectangle((1008, 582, 1350, 828), outline=INK, width=2)
board_text(b1, "342×246 geometry overlay · 1:1", (1008, 840), F12, INK_MUTED)

geometry_lines = [
    "input capture  [0,0,342,246]",
    "activation     [12,74,318,100]",
    "date           [16,16,310,48]",
    "icon well      [26,88,70,70]",
    "title safe     [114,88,202,34]",
    "subtitle safe  [114,132,202,24]",
    "info safe 1    [16,184,310,20]",
    "info safe 2    [16,212,310,20]",
]
for i, line in enumerate(geometry_lines):
    board_text(b1, line, (1392, 584 + i * 28), F12)

board_box(b1, [1392, 824, 468, 180], (224, 217, 198), width=1)
board_text(b1, "母版边界", (1412, 842), F14B)
for i, line in enumerate([
    "外部阴影：0 px（runtime host 持有）",
    "烤字 / 图标：0",
    "基础 warning rust / teal：0",
    "全部状态共用同一 master hash",
    "runtime rect 相对权威值：≤1 px",
]):
    board_text(b1, line, (1412, 872 + i * 25), F11)
board1.save(BOARD_MATERIAL, optimize=True)


# Board 2: seven real 342x246 runtime outputs at 1:1.
board2 = Image.new("RGB", BOARD_SIZE, (225, 220, 207))
b2 = ImageDraw.Draw(board2)
state_board_title = "WMW • SCHEDULE GATE 0.1 • RUNTIME STATE REFILL"
state_board_title_bbox = b2.textbbox((36, 24), state_board_title, font=F32B, anchor="lt")
board_text(b2, state_board_title, (36, 24), F32B, anchor="lt")
board_text(b2, "7 个 342×246 运行时状态 · 全部复用同一 456×328 无字母版", (36, 90), F18, INK_MUTED, "lm")
board_text(b2, "当前真实构建未接入独立推进命令：unavailable 才是 runtime 真值", (1884, 52), F14, INK_MUTED, "rm")
b2.line((36, 108, 1884, 108), fill=INK, width=2)

context_columns = [
    (48, "技术证据用途", "展示同一母版如何回填成全部 7 个可见状态。"),
    (650, "为什么保留", "整屏风格通过后可复用其几何、分层与文字容量证据。"),
    (1252, "A242 降级声明", "不再用于判断 WMW 整屏纸材或正式美术风格。"),
]
for x, heading, body in context_columns:
    board_box(b2, [x, 122, 568, 70], (239, 235, 225), width=1)
    board_text(b2, heading, (x + 14, 134), F13, INK_MUTED, "lt")
    board_text(b2, body, (x + 14, 160), F12, INK, "lm")

top_x = [48, 414, 780, 1146]
bottom_x = [231, 597, 963]
positions = [(x, 244) for x in top_x] + [(x, 588) for x in bottom_x]
for state, (x, y) in zip(STATES, positions):
    board_text(b2, state.label, (x, y - 32), F14B)
    truth = "当前 runtime 真值" if state.id == "runtime-unavailable" else "目标状态示意"
    board_text(b2, truth, (x + 342, y - 30), F10, INK_MUTED, "ra")
    image = state_images[state.id]
    board2.paste(image.convert("RGB"), (x, y), image)
    b2.rectangle((x, y, x + 342, y + 246), outline=INK, width=2)

board_box(b2, [24, 870, 1872, 174], (239, 235, 225))
board_text(b2, "状态层边界（自动审计，用户无需逐像素判断）", (48, 890), F14B)
lines = [
    "confirming / idle_error：警示锈红只叠加动作区；executing：青灰只叠加动作区；disabled：禁用灰只叠加动作区。",
    "日期、剩余天数、箭头 / 叹号 / 进度符号、主副文案与两条结果行全部属于 runtime content；母版本身不含文字或状态。",
    "静态图不证明 committed 180–300ms、executing 全区输入锁，以及 Esc / 点外 / context change 退出。",
    "0 / 1 / 99 / 99+、双位截止日、最长 short_title 与 idle_error 另由文字 bbox 压力审计验证。",
]
for i, line in enumerate(lines):
    board_text(b2, line, (48, 922 + i * 27), F12)
board2.save(BOARD_STATES, optimize=True)


# Board 3: one continuous, user-facing walkthrough of the whole authorized slice.
pipeline = Image.new("RGB", BOARD_SIZE, (225, 220, 207))
pd = ImageDraw.Draw(pipeline)
board_text(pd, "WMW · SCHEDULE GATE 0.1 · 完整拆图流水线", (36, 24), F32B, anchor="lt")
board_text(pd, "A242：技术管线证据 · 不再用于 WMW 整屏美术审批或下一组件扩产", (36, 90), F18, RUST, "lm")
pd.line((36, 108, 1884, 108), fill=INK, width=2)

for x, heading, body in [
    (36, "保留用途", "记录真实 imagegen 配料到最终 7 状态的完整技术链。"),
    (656, "能证明什么", "几何、分层、回填与小尺寸文字容量技术上可复现。"),
    (1276, "不能证明什么", "不能证明三栏整屏属于同一套正式 WMW 美术语言。"),
]:
    board_box(pd, [x, 124, 596, 88], (239, 235, 225), width=1)
    board_text(pd, heading, (x + 14, 136), F14B, INK, "lt")
    board_text(pd, body, (x + 14, 178), F12, INK, "lm")


def stage_label(draw: ImageDraw.ImageDraw, number: str, title: str, x: int, y: int, note: str) -> None:
    board_text(draw, number, (x, y), F26B, RUST, "lt")
    board_text(draw, title, (x + 46, y + 3), F14B, INK, "lt")
    board_text(draw, note, (x + 46, y + 28), F10, INK_MUTED, "lt")


def paste_with_frame(canvas: Image.Image, image: Image.Image, rect: tuple[int, int, int, int]) -> None:
    x, y, w, h = rect
    fitted = ImageOps.contain(image.convert("RGB"), (w, h), method=Image.Resampling.LANCZOS)
    px = x + (w - fitted.width) // 2
    py = y + (h - fitted.height) // 2
    canvas.paste(fitted, (px, py))
    ImageDraw.Draw(canvas).rectangle((x, y, x + w, y + h), outline=INK, width=2)


top_stage_x = [36, 492, 948, 1404]
stage_label(pd, "01", "真实生成源", top_stage_x[0], 230, "四块无字配料，不是完整 UI")
paste_with_frame(pipeline, source, (36, 286, 400, 288))

stage_label(pd, "02", "按角色拆片", top_stage_x[1], 230, "warm / olive / ivory / ink")
for index, name in enumerate(["warm", "olive", "ivory", "ink"]):
    crop = Image.open(ROOT / f"wmw-schedule-gate-ingredient-{name}-imagegen-v0-1.png")
    x = 492 + (index % 2) * 196
    y = 286 + (index // 2) * 144
    paste_with_frame(pipeline, crop, (x, y, 180, 128))
    board_text(pd, name, (x + 8, y + 8), F10, WHITE, "lt")

stage_label(pd, "03", "归一化材质", top_stage_x[2], 230, "标杆 token 锁色，保留宽面纹理")
for index, name in enumerate(["warm", "olive", "ivory", "ink"]):
    normalized = Image.open(ROOT / f"wmw-schedule-gate-ingredient-{name}-normalized-v0-1.png")
    x = 948 + (index % 2) * 196
    y = 286 + (index // 2) * 144
    paste_with_frame(pipeline, normalized, (x, y, 180, 128))
    board_text(pd, name, (x + 8, y + 8), F10, WHITE, "lt")

stage_label(pd, "04", "1368×984 确定性装配", top_stage_x[3], 230, "runtime×4 mask 决定几何与 alpha")
paste_with_frame(pipeline, work, (1404, 286, 480, 288))

for x in [454, 910, 1366]:
    pd.line((x - 12, 426, x + 16, 426), fill=INK, width=2)
    pd.polygon(((x + 16, 421), (x + 24, 426), (x + 16, 431)), fill=INK)

stage_label(pd, "05", "456×328 无字母版", 36, 620, "一张母版服务所有状态")
pipeline.paste(master.convert("RGB"), (36, 682), master)
pd.rectangle((36, 682, 492, 1010), outline=INK, width=2)

stage_label(pd, "06", "342×246 runtime 回放", 528, 620, "0.75 显示，结构偏差 ≤1px")
pipeline.paste(runtime_base.convert("RGB"), (528, 724), runtime_base)
pd.rectangle((528, 724, 870, 970), outline=INK, width=2)

stage_label(pd, "07", "运行时状态叠加", 906, 620, "锈红 / 青灰 / 禁用灰只改动作区")
overlay_ids = ["idle", "confirming", "executing", "runtime-unavailable"]
for index, state_id in enumerate(overlay_ids):
    thumb = state_images[state_id].resize((164, 118), Image.Resampling.LANCZOS)
    x = 906 + (index % 2) * 178
    y = 704 + (index // 2) * 144
    pipeline.paste(thumb.convert("RGB"), (x, y), thumb)
    pd.rectangle((x, y, x + 164, y + 118), outline=INK, width=1)
    board_text(pd, state_id, (x, y + 122), F10, INK_MUTED, "lt")

stage_label(pd, "08", "最终 7 状态输出", 1298, 620, "完整 1:1 大图见状态复核板")
for index, state in enumerate(STATES):
    thumb = state_images[state.id].resize((160, 115), Image.Resampling.LANCZOS)
    x = 1298 + (index % 3) * 178
    y = 684 + (index // 3) * 112
    pipeline.paste(thumb.convert("RGB"), (x, y), thumb)
    pd.rectangle((x, y, x + 160, y + 115), outline=INK, width=1)
pipeline.save(BOARD_PIPELINE, optimize=True)


# Audit geometry by deterministic role maps using nearest-neighbor scaling.
role_work = Image.new("L", WORK_SIZE, 1)
role_draw = ImageDraw.Draw(role_work)
role_draw.rectangle(xyxy(WORK_RECTS["date"]), fill=2)
role_draw.rectangle(xyxy(WORK_RECTS["action"]), fill=3)
role_draw.rounded_rectangle(xyxy(WORK_RECTS["icon"]), radius=24, fill=4)
role_draw.rectangle(xyxy(WORK_RECTS["info_1"]), fill=5)
role_draw.rectangle(xyxy(WORK_RECTS["info_2"]), fill=6)
role_runtime = role_work.resize(MASTER_SIZE, Image.Resampling.NEAREST).resize(RUNTIME_SIZE, Image.Resampling.NEAREST)

geometry_records: list[dict] = []
expected_labels = {"date": 2, "action": 3, "icon": 4, "info_1": 5, "info_2": 6}
expected_rects = {
    "date": RUNTIME_RECTS["date"],
    "action": RUNTIME_RECTS["action"],
    "icon": RUNTIME_RECTS["icon"],
    "info_1": [16, 182, 310, 24],
    "info_2": [16, 210, 310, 24],
}
role_arr = np.asarray(role_runtime)
for key, label in expected_labels.items():
    ys, xs = np.where(role_arr == label)
    actual = [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]
    expected = expected_rects[key]
    delta = [actual[i] - expected[i] for i in range(4)]
    geometry_records.append({
        "key": key,
        "expected_xywh": expected,
        "actual_xywh": actual,
        "delta_px": delta,
        "passed_within_1px": all(abs(value) <= 1 for value in delta),
    })

alpha = np.asarray(master)[:, :, 3]
ys, xs = np.where(alpha > 0)
alpha_bbox = [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]
hidden_nonzero = int(np.count_nonzero(np.asarray(master)[:, :, :3][alpha == 0]))
text_violations = [record for record in text_records if not record["passed"]]
pressure_violations = [record for record in pressure_records if not record["passed"]]

base_arr = np.asarray(master.convert("RGB"))
rust_distance = np.linalg.norm(base_arr.astype(np.int16) - np.asarray(RUST, dtype=np.int16), axis=2)
teal_distance = np.linalg.norm(base_arr.astype(np.int16) - np.asarray(TEAL, dtype=np.int16), axis=2)
base_rust_near_pixels = int(np.count_nonzero(rust_distance < 10))
base_teal_near_pixels = int(np.count_nonzero(teal_distance < 10))

output_hashes = {
    "source": digest(SOURCE),
    "work": digest(WORK_OUTPUT),
    "master": digest(MASTER_OUTPUT),
    "runtime_no_text": digest(RUNTIME_OUTPUT),
    "material_review_board": digest(BOARD_MATERIAL),
    "state_review_board": digest(BOARD_STATES),
    "full_pipeline_walkthrough": digest(BOARD_PIPELINE),
}
for state_id, filename in state_paths.items():
    output_hashes[f"state_{state_id}"] = digest(ROOT / filename)

material_manifest = {
    "artifact_type": "imagegen_material_ingredient_manifest",
    "version": "schedule_gate_v0_1",
    "source": SOURCE.name,
    "source_size": list(source.size),
    "source_sha256": digest(SOURCE),
    "ingredients": ingredient_records,
    "normalization_policy": "imagegen broad value planes + branch token centering; deterministic masks own geometry",
    "assembled_no_text_master": MASTER_OUTPUT.name,
}
MATERIAL_MANIFEST.write_text(json.dumps(material_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

assert master.size == MASTER_SIZE
assert runtime_base.size == RUNTIME_SIZE
assert board1.size == BOARD_SIZE and board2.size == BOARD_SIZE
assert alpha_bbox == [0, 0, MASTER_SIZE[0], MASTER_SIZE[1]]
assert hidden_nonzero == 0
assert not text_violations, text_violations
assert not pressure_violations, pressure_violations
assert all(item["passed_within_1px"] for item in geometry_records), geometry_records
assert base_rust_near_pixels == 0
assert base_teal_near_pixels == 0
assert state_board_title_bbox[0] >= 36 and state_board_title_bbox[2] <= 936

audit = {
    "artifact_type": "derived_no_text_component_candidate_audit",
    "version": "schedule_gate_v0_1_colored",
    "status": "technical_pipeline_evidence_only_not_visual_candidate_a242",
    "target_only": True,
    "source_truth": {
        "built_in_imagegen_used": True,
        "imagegen_source": SOURCE.name,
        "material_manifest": MATERIAL_MANIFEST.name,
        "candidate_spec": str(SPEC_PATH),
        "benchmark_branch": "clean-lowpoly-weekly",
    },
    "review_status": {
        "ui_designer": "pass_p0_0_p1_0_p2_1",
        "ux_laoge": "pass_p0_0_p1_0_p2_1",
        "remaining_p2": "date module downsamples to 49px height versus 48px target; within approved <=1px tolerance",
        "user_visual_decision": "withdrawn_a242_missing_approved_fullscreen_style_mock",
    },
    "outputs": {
        "work_no_text": {"file": WORK_OUTPUT.name, "size": list(work.size)},
        "master_no_text": {"file": MASTER_OUTPUT.name, "size": list(master.size)},
        "runtime_no_text": {"file": RUNTIME_OUTPUT.name, "size": list(runtime_base.size)},
        "runtime_states": state_paths,
        "technical_evidence_boards": [BOARD_PIPELINE.name, BOARD_STATES.name, BOARD_MATERIAL.name],
        "user_review_boards": [],
    },
    "hashes_sha256": output_hashes,
    "geometry": {
        "runtime_local_integer_pixels_authoritative": True,
        "work_scale_from_runtime": 4,
        "work_to_master_scale": [1, 3],
        "master_to_runtime_scale": 0.75,
        "records": geometry_records,
        "all_within_1px": all(item["passed_within_1px"] for item in geometry_records),
        "input_capture_rect_xywh": RUNTIME_RECTS["input_capture"],
        "activation_hit_rect_xywh": RUNTIME_RECTS["activation_hit"],
    },
    "alpha": {
        "mode": "RGBA",
        "visible_bbox_xyxy": alpha_bbox,
        "full_456x328_bbox_no_padding": alpha_bbox == [0, 0, 456, 328],
        "alpha_zero_nonzero_rgb_values": hidden_nonzero,
        "external_shadow_pixels": 0,
    },
    "color_roles": {
        "mother_tokens": {key: list(value) for key, value in TARGETS.items()},
        "base_warning_rust_near_pixels": base_rust_near_pixels,
        "base_teal_near_pixels": base_teal_near_pixels,
        "warning_rust_owner": "runtime confirming / idle_error overlay",
        "teal_owner": "runtime executing overlay",
    },
    "text_safe_area": {
        "checked_state_text_records": len(text_records),
        "expected_state_text_records": len(STATES) * 8,
        "violations": text_violations,
        "passed": not text_violations,
    },
    "dynamic_copy_pressure": {
        "checked_records": len(pressure_records),
        "expected_records": 20,
        "records": pressure_records,
        "violations": pressure_violations,
        "passed": not pressure_violations,
    },
    "state_layering": {
        "one_master_hash_for_all_states": digest(MASTER_OUTPUT),
        "state_count": len(STATES),
        "baked_runtime_text_or_icons": False,
        "whole_component_swap_required": False,
        "static_snapshots_do_not_prove_runtime_timing_or_input": True,
        "runtime_overlay_metrics": {
            "confirming_rust": {"mask_xywh": RUNTIME_RECTS["action"], "color_rgb": list(RUST), "outline_width_px": 3, "top_accent_alpha": 150},
            "idle_error_rust": {"mask_xywh": RUNTIME_RECTS["action"], "color_rgb": list(RUST), "outline_width_px": 3, "bottom_accent_alpha": 220},
            "executing_teal": {"mask_xywh": RUNTIME_RECTS["action"], "color_rgb": list(TEAL), "outline_width_px": 3, "hatch_alpha": 115},
            "disabled_gray": {"mask_xywh": RUNTIME_RECTS["action"], "color_rgb": list(DISABLED), "fill_alpha": 218, "outline_width_px": 3},
        },
    },
    "review_board_layout": {
        "runtime_states_title_target_rect_xywh": [36, 24, 900, 48],
        "runtime_states_title_glyph_bbox_xyxy": list(state_board_title_bbox),
        "runtime_states_title_not_clipped": state_board_title_bbox[0] >= 36 and state_board_title_bbox[2] <= 936,
        "user_review_context_present": {
            "purpose": True,
            "why_now": True,
            "user_judgement": True,
        },
        "full_authorized_pipeline_present": [
            "imagegen_source",
            "role_crops",
            "normalized_materials",
            "1368x984_deterministic_assembly",
            "456x328_no_text_master",
            "342x246_runtime_replay",
            "runtime_state_overlays",
            "seven_final_visible_states",
        ],
    },
    "assertions": {
        "true_imagegen_source_preserved": True,
        "master_is_real_456x328_rgba_png": master.size == MASTER_SIZE and master.mode == "RGBA",
        "runtime_replay_is_real_342x246_png": runtime_base.size == RUNTIME_SIZE,
        "review_boards_are_real_1920x1080_png": board1.size == BOARD_SIZE and board2.size == BOARD_SIZE,
        "no_text_or_icon_baked_in_mother_by_construction": True,
        "all_text_inside_existing_safe_rects": not text_violations,
        "all_pressure_strings_inside_existing_safe_rects": not pressure_violations,
        "formal_ui_contract_unchanged": True,
        "godot_runtime_unchanged": True,
        "compact_a51_unchanged": True,
        "colored_full_screen_not_generated": True,
        "not_a_fullscreen_visual_style_candidate": True,
        "component_asset_expansion_paused_by_a242": True,
    },
}
AUDIT_OUTPUT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(WORK_OUTPUT)
print(MASTER_OUTPUT)
print(RUNTIME_OUTPUT)
print(BOARD_MATERIAL)
print(BOARD_STATES)
print(BOARD_PIPELINE)
print(AUDIT_OUTPUT)
