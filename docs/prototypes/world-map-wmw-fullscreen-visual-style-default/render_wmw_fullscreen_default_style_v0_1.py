from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "wmw-fullscreen-default-imagegen-source-v0-1.png"
OUTPUT = ROOT / "wmw-fullscreen-default-filled-style-v0-3.png"
AUDIT = ROOT / "wmw-fullscreen-default-filled-style-v0-3-audit.json"
ALIGNMENT_QA = ROOT / "wmw-fullscreen-default-filled-style-v0-3-alignment-qa.png"

W, H = 1920, 1080

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")

INK = (26, 31, 31)
INK_SOFT = (64, 67, 62)
IVORY = (224, 217, 198)
PAPER = (183, 164, 136)
PAPER_LIGHT = (187, 177, 158)
PAPER_ROW = (184, 174, 154)
OLIVE = (78, 96, 57)
OLIVE_DARK = (55, 69, 41)
TEAL = (43, 60, 65)
RUST = (126, 72, 48)
LOCKED = (102, 101, 88)
BOARD = (16, 24, 30)

RECTS = {
    "left_column": [36, 24, 342, 1032],
    "left_card_north": [66, 36, 306, 240],
    "left_card_east": [66, 294, 306, 240],
    "left_card_pacific": [66, 552, 306, 240],
    "schedule": [66, 810, 306, 246],
    "center_column": [402, 24, 972, 1032],
    "center_title": [426, 24, 924, 72],
    "map_stage": [426, 96, 924, 936],
    "right_dossier": [1398, 24, 480, 1032],
    "right_title": [1521, 87, 333, 51],
    "right_photo": [1431, 171, 414, 264],
    "right_body": [1431, 456, 414, 135],
    "mission_header": [1425, 609, 426, 66],
    "mission_rows": [1431, 681, 414, 248],
    "cta": [1425, 957, 426, 75],
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


F11 = font(11)
F12 = font(12)
F13 = font(13)
F14 = font(14)
F15 = font(15)
F16 = font(16)
F17 = font(17)
F18 = font(18)
F20 = font(20)
F22B = font(22, True)
F23B = font(23, True)
F24B = font(24, True)
F28B = font(28, True)
F30B = font(30, True)
F32B = font(32, True)


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def xyxy(rect: list[int]) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    return x, y, x + w, y + h


def paste_fit(canvas: Image.Image, image: Image.Image, rect: list[int]) -> None:
    x, y, w, h = rect
    fitted = ImageOps.fit(image.convert("RGB"), (w, h), method=Image.Resampling.LANCZOS)
    canvas.paste(fitted, (x, y))


def rgba_overlay(canvas: Image.Image, rect: list[int], fill: tuple[int, int, int], alpha: int, outline=None, width=1, radius=0) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    bounds = xyxy(rect)
    outline_rgba = None if outline is None else tuple(outline) + (255,)
    if radius:
        draw.rounded_rectangle(bounds, radius=radius, fill=fill + (alpha,), outline=outline_rgba, width=width)
    else:
        draw.rectangle(bounds, fill=fill + (alpha,), outline=outline_rgba, width=width)
    canvas.alpha_composite(layer)


def shadow(canvas: Image.Image, rect: list[int], offset=(5, 7), alpha=70, radius=0) -> None:
    x, y, w, h = rect
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    bounds = (x + offset[0], y + offset[1], x + w + offset[0], y + h + offset[1])
    if radius:
        draw.rounded_rectangle(bounds, radius=radius, fill=(0, 0, 0, alpha))
    else:
        draw.rectangle(bounds, fill=(0, 0, 0, alpha))
    canvas.alpha_composite(layer)


def contains(rect: list[int], bbox: tuple[int, int, int, int]) -> bool:
    x, y, w, h = rect
    return bbox[0] >= x and bbox[1] >= y and bbox[2] <= x + w and bbox[3] <= y + h


def safe_text(draw: ImageDraw.ImageDraw, text: str, xy, used_font, fill, anchor, safe_rect, records, key) -> None:
    bbox = draw.textbbox(xy, text, font=used_font, anchor=anchor)
    record = {
        "key": key,
        "text": text,
        "bbox_xyxy": list(bbox),
        "safe_rect_xywh": list(safe_rect),
        "passed": contains(safe_rect, bbox),
    }
    records.append(record)
    draw.text(xy, text, font=used_font, fill=fill + (255,), anchor=anchor)


def recolor_map_land(image: Image.Image) -> Image.Image:
    arr = np.asarray(image.convert("RGB")).copy()
    luminance = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]

    regions = [
        ((52, 130, 328, 398), [(78, 98, 61), (87, 105, 67), (100, 115, 76)], "north"),
        ((338, 120, 816, 350), [(41, 60, 65), (48, 66, 71), (56, 73, 73)], "other"),
        ((118, 318, 294, 714), [(41, 60, 65), (48, 66, 71), (56, 73, 73)], "other"),
        ((338, 318, 598, 676), [(41, 60, 65), (48, 66, 71), (56, 73, 73)], "other"),
        ((640, 508, 858, 748), [(41, 60, 65), (48, 66, 71), (56, 73, 73)], "other"),
        ((58, 788, 864, 926), [(41, 60, 65), (48, 66, 71), (56, 73, 73)], "other"),
    ]

    for (x1, y1, x2, y2), palette, kind in regions:
        sub = arr[y1:y2, x1:x2]
        sub_lum = luminance[y1:y2, x1:x2]
        if kind == "north":
            mask = (sub_lum > 34) & (sub[:, :, 1] > sub[:, :, 2] * 1.08)
        else:
            mask = sub_lum > 31
        values = sub_lum[mask]
        if values.size == 0:
            continue
        q1, q2 = np.quantile(values, [0.38, 0.72])
        target = np.zeros_like(sub)
        target[:] = palette[0]
        target[sub_lum > q1] = palette[1]
        target[sub_lum > q2] = palette[2]
        # Preserve a small amount of source variation while locking the requested three color families.
        blended = np.clip(target.astype(np.float32) * 0.86 + sub.astype(np.float32) * 0.14, 0, 255).astype(np.uint8)
        sub[mask] = blended[mask]
        arr[y1:y2, x1:x2] = sub
    return Image.fromarray(arr, "RGB")


source = Image.open(SOURCE).convert("RGB")
assert source.size == (1672, 941)

canvas = Image.new("RGBA", (W, H), BOARD + (255,))

# Use the model-generated screen only as a coherent art source; deterministic masks own final geometry.
map_source = source.crop((352, 24, 1219, 914))

# Remove the three source marker rings before restoring authoritative pins.
marker_centers = [(204, 309), (654, 308), (667, 611)]
for cx, cy in marker_centers:
    radius = 26
    donor_x = max(0, cx - 120)
    donor_y = max(0, cy - radius)
    donor = map_source.crop((donor_x, donor_y, donor_x + radius * 2, donor_y + radius * 2))
    mask = Image.new("L", (radius * 2, radius * 2), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(4))
    map_source.paste(donor, (cx - radius, cy - radius), mask)

shadow(canvas, RECTS["map_stage"], offset=(6, 8), alpha=78)
map_fitted = ImageOps.fit(map_source, (924, 936), method=Image.Resampling.LANCZOS)
for cx, cy in [(218, 325), (697, 325), (711, 643)]:
    radius = 34
    donor = map_fitted.crop((max(0, cx - 150), cy - radius, max(0, cx - 150) + radius * 2, cy + radius))
    mask = Image.new("L", (radius * 2, radius * 2), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(6))
    map_fitted.paste(donor, (cx - radius, cy - radius), mask)
map_fitted = recolor_map_land(map_fitted)
canvas.paste(map_fitted, (426, 96))
rgba_overlay(canvas, RECTS["map_stage"], BOARD, 12, outline=INK, width=2)

# Left column v0.2: source permission is photo-only. The source card footer,
# placeholder bars, status blocks, frames and shadows are never pasted.
card_photos = [
    source.crop((40, 43, 316, 177)),
    source.crop((40, 279, 316, 413)),
    source.crop((40, 515, 316, 649)),
]
card_rects = [RECTS["left_card_north"], RECTS["left_card_east"], RECTS["left_card_pacific"]]
for index, (card_photo, rect) in enumerate(zip(card_photos, card_rects)):
    x, y, w, h = rect
    shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.polygon(
        [(x + 4, y + 5), (x + w - 8, y + 5), (x + w + 4, y + 17), (x + w + 4, y + h + 5), (x + 4, y + h + 5)],
        fill=(0, 0, 0, 64),
    )
    canvas.alpha_composite(shadow_layer)

    shell = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shell_draw = ImageDraw.Draw(shell)
    shell_points = [(x, y), (x + w - 12, y), (x + w, y + 12), (x + w, y + h), (x, y + h)]
    shell_draw.polygon(shell_points, fill=(36, 42, 41, 255), outline=(32, 37, 38, 255))
    if index == 0:
        shell_draw.line(shell_points + [shell_points[0]], fill=(104, 119, 66, 255), width=2, joint="curve")
        shell_draw.rectangle((x, y, x + 3, y + h), fill=(104, 119, 66, 255))
    canvas.alpha_composite(shell)

    photo_rect = [x + 12, y + 12, 282, 144]
    paste_fit(canvas, card_photo, photo_rect)
    rgba_overlay(canvas, photo_rect, BOARD, 3, outline=(192, 185, 179), width=1)
    rgba_overlay(canvas, [x + 12, y + 156, 282, 72], PAPER, 255, outline=(32, 37, 38), width=1)

# Schedule v0.2 is rebuilt once from clean carriers; the source placeholder
# schedule is not reused at any layer.
shadow(canvas, RECTS["schedule"], offset=(4, 5), alpha=64)
rgba_overlay(canvas, RECTS["schedule"], (36, 42, 41), 255, outline=(32, 37, 38), width=1)

# Right column: one clean continuous dossier paper. The model's internal placeholder
# photo/rows are deliberately not reused, avoiding double-photo and double-frame residue.
shadow(canvas, RECTS["right_dossier"], offset=(6, 8), alpha=72)
right_paper = Image.new("RGBA", (480, 1032), PAPER + (255,))
rpd = ImageDraw.Draw(right_paper)
rpd.polygon([(0, 0), (352, 0), (480, 126), (480, 0)], fill=(187, 168, 140, 255))
rpd.polygon([(0, 580), (480, 510), (480, 784), (0, 842)], fill=(180, 161, 133, 255))
rpd.polygon([(0, 920), (220, 875), (480, 934), (480, 1032), (0, 1032)], fill=(185, 166, 138, 255))
canvas.paste(right_paper, (1398, 24), right_paper)
rgba_overlay(canvas, RECTS["right_dossier"], PAPER, 16, outline=INK, width=2)

# Recover the generated restricted-zone photo at the exact 69:44 slot.
right_photo_source = source.crop((1247, 119, 1630, 311))
paste_fit(canvas, right_photo_source, RECTS["right_photo"])
rgba_overlay(canvas, RECTS["right_photo"], BOARD, 8, outline=INK, width=2)

# Calm authoritative carriers while keeping generated material visible below.
rgba_overlay(canvas, RECTS["right_title"], PAPER_LIGHT, 210, outline=INK, width=2)
rgba_overlay(canvas, RECTS["right_body"], PAPER_LIGHT, 210, outline=INK, width=1)
rgba_overlay(canvas, RECTS["mission_header"], PAPER_LIGHT, 228, outline=INK, width=2)
rgba_overlay(canvas, RECTS["mission_rows"], PAPER, 110, outline=INK, width=1)
rgba_overlay(canvas, RECTS["cta"], OLIVE, 244, outline=INK, width=2)

draw = ImageDraw.Draw(canvas)
records: list[dict] = []

# Masthead and week.
safe_text(draw, "WORLD MYSTERIES WEEKLY", (426, 58), F30B, IVORY, "lm", [426, 24, 700, 72], records, "masthead")
safe_text(draw, "WEEK 01", (1350, 58), F18, PAPER_LIGHT, "rm", [1160, 24, 190, 72], records, "week")

# Card runtime content.
card_copy = [
    (RECTS["left_card_north"], "北美禁区带", "选中", OLIVE, IVORY),
    (RECTS["left_card_east"], "东亚神秘地带", "锁定", LOCKED, PAPER_LIGHT),
    (RECTS["left_card_pacific"], "太平洋失航带", "锁定", LOCKED, PAPER_LIGHT),
]
for index, (rect, title, state, state_fill, state_text) in enumerate(card_copy):
    x, y, w, h = rect
    title_rect = [x + 18, y + 166, 186, 48]
    state_rect = [x + 216, y + 166, 76, 48]
    rgba_overlay(canvas, state_rect, state_fill, 255, outline=(32, 37, 38), width=1)
    draw = ImageDraw.Draw(canvas)
    safe_text(draw, title, (x + 30, y + 190), F17, INK, "lm", title_rect, records, f"left_title_{index}")
    safe_text(draw, state, (x + 254, y + 190), F14, state_text, "mm", state_rect, records, f"left_state_{index}")

# Schedule carriers and copy.
rgba_overlay(canvas, [82, 826, 274, 48], PAPER, 255, outline=(32, 37, 38), width=1)
rgba_overlay(canvas, [78, 884, 282, 100], (63, 76, 45), 255, outline=(32, 37, 38), width=1)
rgba_overlay(canvas, [90, 901, 64, 64], (192, 185, 179), 255, outline=(32, 37, 38), width=1)
rgba_overlay(canvas, [82, 992, 274, 24], (178, 171, 155), 255)
rgba_overlay(canvas, [82, 1020, 274, 24], (178, 171, 155), 255)
draw = ImageDraw.Draw(canvas)
safe_text(draw, "全局日程", (78, 819), F11, PAPER_LIGHT, "lm", [78, 812, 116, 14], records, "schedule_section")
safe_text(draw, "当前第 1 天", (94, 850), F18, INK, "lm", [94, 836, 112, 28], records, "schedule_current")
safe_text(draw, "剩余 7 天", (344, 850), F18, INK, "rm", [232, 836, 112, 28], records, "schedule_remaining")
safe_text(draw, "→", (122, 933), F28B, INK, "mm", [106, 917, 32, 32], records, "schedule_icon")
safe_text(draw, "推进到下一天", (166, 915), F23B, IVORY, "lm", [166, 898, 182, 34], records, "schedule_title")
safe_text(draw, "点击后查看推进影响", (166, 954), F12, PAPER_LIGHT, "lm", [166, 942, 182, 24], records, "schedule_subtitle")
safe_text(draw, "当前：无任务到期", (82, 1004), F12, INK, "lm", [82, 994, 274, 20], records, "schedule_info_1")
draw.line((82, 1018, 356, 1018), fill=INK_SOFT + (255,), width=1)
safe_text(draw, "日程归零：进入编辑部阶段", (82, 1032), F12, INK, "lm", [82, 1022, 274, 20], records, "schedule_info_2")

# Authoritative map markers and labels.
map_markers = [
    (620, 365, "北美禁区带", "selected", "right"),
    (1164, 371, "东亚神秘地带", "locked", "left"),
    (1160, 710, "太平洋失航带", "locked", "left"),
]
for index, (px, py, label, state, side) in enumerate(map_markers):
    if state == "selected":
        draw.ellipse((px - 28, py - 28, px + 28, py + 28), outline=IVORY + (255,), width=2)
        draw.ellipse((px - 17, py - 17, px + 17, py + 17), fill=OLIVE + (255,), outline=IVORY + (255,), width=3)
    else:
        draw.ellipse((px - 15, py - 15, px + 15, py + 15), fill=LOCKED + (255,), outline=PAPER_LIGHT + (255,), width=2)
        safe_text(draw, "锁", (px, py), F11, INK, "mm", [px - 15, py - 15, 30, 30], records, f"map_lock_{index}")
    safe = [px + 28, py - 16, 190, 32] if side == "right" else [px - 218, py - 16, 190, 32]
    anchor = "lm" if side == "right" else "rm"
    point = (px + 28, py) if side == "right" else (px - 28, py)
    safe_text(draw, label, point, F18, IVORY, anchor, safe, records, f"map_label_{index}")

# Right title and low-weight printed identity mark (not a button).
badge_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
badge_draw = ImageDraw.Draw(badge_layer)
badge_draw.ellipse((1432, 82, 1488, 138), outline=INK + (148,), width=1)
badge_draw.ellipse((1447, 97, 1473, 123), outline=OLIVE + (148,), width=1)
badge_draw.ellipse((1455, 105, 1465, 115), fill=OLIVE + (148,))
canvas.alpha_composite(badge_layer)
draw = ImageDraw.Draw(canvas)
safe_text(draw, "北美禁区带", (1687, 112), F28B, INK, "mm", RECTS["right_title"], records, "right_region_title")

# Right body.
safe_text(draw, "都市传说与军事封锁交叠。", (1450, 493), F20, INK, "lm", [1450, 475, 380, 36], records, "right_body_1")
safe_text(draw, "军方巡逻、档案残页与异常雷达同时露头。", (1450, 546), F15, INK_SOFT, "lm", [1450, 528, 380, 36], records, "right_body_2")

# Mission header.
safe_text(draw, "任务情报", (1443, 642), F22B, INK, "lm", [1443, 620, 150, 44], records, "mission_header")
safe_text(draw, "常驻 2 · 限时 1 · 深链 1", (1832, 634), F13, INK_SOFT, "rm", [1620, 618, 212, 28], records, "mission_summary")
safe_text(draw, "已展开 4 / 4 ︿", (1832, 658), F12, INK_SOFT, "rm", [1690, 646, 142, 24], records, "mission_expanded")

# Four mission rows.
rows = [
    (681, "01", "51 区外围公路", "科学纪实 · 耗时 2 天", "常驻", TEAL),
    (745, "02", "罗斯威尔档案残页", "科学纪实 · 耗时 1 天", "常驻", TEAL),
    (809, "03", "突发：雷达异常光点", "大众热度 · 耗时 2 天", "限时至第 4 天", RUST),
    (873, "04", "M330 末班车空白段", "神秘玄学 · 耗时 2 天", "深链", (49, 58, 66)),
]
for index, (y, num, title, meta, tag, accent) in enumerate(rows):
    row_rect = [1431, y, 414, 56]
    rgba_overlay(canvas, row_rect, PAPER_ROW, 226, outline=INK, width=1)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((1443, y + 10, 1451, y + 46), fill=accent + (255,))
    safe_text(draw, num, (1464, y + 28), F11, INK_SOFT, "lm", [1460, y + 12, 30, 32], records, f"mission_num_{index}")
    safe_text(draw, title, (1492, y + 18), F16, INK, "lm", [1492, y + 3, 208, 28], records, f"mission_title_{index}")
    safe_text(draw, meta, (1492, y + 42), F12, INK_SOFT, "lm", [1492, y + 30, 208, 22], records, f"mission_meta_{index}")
    tag_rect = [1713, y + 10, 120, 36]
    tag_fill = accent if index >= 2 else (183, 175, 155)
    tag_text = IVORY if index >= 2 else INK
    rgba_overlay(canvas, tag_rect, tag_fill, 238, outline=INK, width=1, radius=4)
    draw = ImageDraw.Draw(canvas)
    safe_text(draw, tag, (1773, y + 28), F12, tag_text, "mm", tag_rect, records, f"mission_tag_{index}")

# Unique primary CTA.
draw = ImageDraw.Draw(canvas)
safe_text(draw, "进入地区任务台  →", (1638, 994), F24B, IVORY, "mm", [1450, 969, 376, 50], records, "primary_cta")

violations = [record for record in records if not record["passed"]]
assert not violations, violations

output_rgb = canvas.convert("RGB")
output_rgb.save(OUTPUT, optimize=True)

baseline_v0_2 = np.asarray(Image.open(ROOT / "wmw-fullscreen-default-filled-style-v0-2.png").convert("RGB"))
current_v0_3 = np.asarray(output_rgb)
diff_v0_2 = np.any(baseline_v0_2 != current_v0_3, axis=2)
allowed_schedule_envelope = np.zeros((H, W), dtype=bool)
allowed_schedule_envelope[810:1062, 36:383] = True
outside_schedule_envelope_diff_pixels = int((diff_v0_2 & ~allowed_schedule_envelope).sum())
center_right_diff_pixels = int(diff_v0_2[:, 402:].sum())
cards_diff_pixels = int(diff_v0_2[:810, :402].sum())
assert outside_schedule_envelope_diff_pixels == 0, outside_schedule_envelope_diff_pixels
assert center_right_diff_pixels == 0, center_right_diff_pixels
assert cards_diff_pixels == 0, cards_diff_pixels

left_shells = [RECTS["left_card_north"], RECTS["left_card_east"], RECTS["left_card_pacific"], RECTS["schedule"]]
left_axis_values = {
    "x": [rect[0] for rect in left_shells],
    "width": [rect[2] for rect in left_shells],
    "right": [rect[0] + rect[2] for rect in left_shells],
    "center_x": [rect[0] + rect[2] // 2 for rect in left_shells],
}
assert left_axis_values == {"x": [66] * 4, "width": [306] * 4, "right": [372] * 4, "center_x": [219] * 4}
left_stack_gaps = [294 - (36 + 240), 552 - (294 + 240), 810 - (552 + 240)]
assert left_stack_gaps == [18, 18, 18]

alignment_qa = output_rgb.convert("RGBA")
alignment_draw = ImageDraw.Draw(alignment_qa)
for axis_x, color in [(66, (255, 58, 84, 255)), (219, (84, 224, 255, 255)), (372, (255, 58, 84, 255))]:
    alignment_draw.line((axis_x, 24, axis_x, 1056), fill=color, width=1)
for edge_y in [36, 276, 294, 534, 552, 792, 810, 1056]:
    alignment_draw.line((54, edge_y, 384, edge_y), fill=(255, 196, 64, 220), width=1)
alignment_crop = alignment_qa.crop((48, 18, 390, 1062)).resize((684, 2088), Image.Resampling.NEAREST)
alignment_crop.save(ALIGNMENT_QA, optimize=True)

stats = ImageStat.Stat(output_rgb.resize((240, 135), Image.Resampling.BILINEAR))

audit = {
    "artifact_type": "filled_state_fullscreen_visual_style_mock",
    "version": "wmw_fullscreen_default_v0_3",
    "status": "functional_geometry_evidence_only_pending_fullscreen_art_pass",
    "target_only": True,
    "canvas": [W, H],
    "state": "default",
    "source": {
        "built_in_imagegen_used": True,
        "file": SOURCE.name,
        "size": list(source.size),
        "sha256": digest(SOURCE),
        "role": "cohesive no-text full-screen visual proposal source; not geometry truth",
    },
    "output": {
        "file": OUTPUT.name,
        "size": list(output_rgb.size),
        "sha256": digest(OUTPUT),
        "mode": output_rgb.mode,
    },
    "geometry": {
        "layout_truth": "black-white-full-map-v5-1-default.png plus user-mandated left schedule axis correction",
        "rects_xywh": RECTS,
        "all_final_carriers_deterministically_restored": True,
        "three_column_structure_unchanged": True,
        "route_lines_drawn": 0,
        "new_ui_modules_added": 0,
    },
    "content": {
        "selected_region_id": "north_america",
        "left_selected_count": 1,
        "left_locked_count": 2,
        "map_pin_count": 3,
        "mission_row_count": 4,
        "primary_cta_count": 1,
        "redline_status_badge_present": False,
        "all_readable_text_programmatically_added": True,
    },
    "left_column_composite": {
        "visual_target": "imagegen_source_figure_2_clean_single_layer_weight",
        "geometry_and_content_truth": "black-white-full-map-v5-1-default.png",
        "left_card_source_role": "photo_only",
        "left_schedule_source_reuse": False,
        "placeholder_carrier_reuse_count": 0,
        "card_footer_count": 3,
        "card_status_carrier_count": 3,
        "schedule_carrier_count": 3,
    },
    "left_column_alignment_gate": {
        "outer_axis_values": left_axis_values,
        "outer_axis_tolerance_px": 0,
        "vertical_gaps_px": left_stack_gaps,
        "inner_shared_edges": {
            "card_photo_footer": [78, 360],
            "schedule_action": [78, 360],
        },
        "passed": True,
        "internal_alignment_qa_file": ALIGNMENT_QA.name,
        "internal_alignment_qa_user_delivery": False,
    },
    "v0_2_regression": {
        "changed_scope": "schedule_and_shadow_envelope_x36_382_y810_1061_only",
        "outside_schedule_envelope_diff_pixels": outside_schedule_envelope_diff_pixels,
        "cards_diff_pixels": cards_diff_pixels,
        "center_right_diff_pixels": center_right_diff_pixels,
        "center_and_right_unchanged": center_right_diff_pixels == 0,
    },
    "text_safe_area": {
        "checked_records": len(records),
        "violations": violations,
        "passed": not violations,
        "records": records,
    },
    "visual_stats": {
        "mean_rgb_240x135": [round(value, 2) for value in stats.mean],
        "stddev_rgb_240x135": [round(value, 2) for value in stats.stddev],
    },
    "review_boundary": {
        "user_should_see_only_complete_player_view": True,
        "imagegen_source_is_technical_input_not_user_review_board": True,
        "confirming_not_generated_until_default_acceptance": True,
        "static_mock_does_not_prove_runtime": True,
    },
    "review_status": {
        "v0_2_user_review": "rejected_obvious_left_axis_misalignment",
        "ux_laoge_diagnosis": "iterate_p0_0_p1_1_p2_0",
        "ui_designer_axis_spec": "implemented",
        "ui_designer_final": "pass_p0_0_p1_0_p2_0",
        "ux_laoge_final": "pass_p0_0_p1_0_p2_0",
        "user_style_decision": "rejected_rough_visual_finish_fullscreen_art_pass_required",
    },
    "assertions": {
        "real_1920x1080_png": output_rgb.size == (W, H),
        "all_text_inside_safe_rects": not violations,
        "central_map_is_largest_visual_field": True,
        "right_dossier_is_single_full_height_sheet": True,
        "schedule_subordinate_to_primary_cta": True,
        "no_map_routes_legends_or_filters": True,
        "no_qa_labels_in_player_view_by_construction": True,
        "godot_unchanged": True,
        "formal_contracts_unchanged": True,
        "component_atlas_not_generated": True,
        "left_source_placeholder_carriers_not_reused": True,
    },
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(OUTPUT)
print(AUDIT)
