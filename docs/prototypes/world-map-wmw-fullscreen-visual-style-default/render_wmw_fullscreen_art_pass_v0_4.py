from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "wmw-fullscreen-default-art-pass-imagegen-source-v0-4.png"
OUTPUT = ROOT / "wmw-fullscreen-default-art-pass-filled-v0-4.png"
AUDIT = ROOT / "wmw-fullscreen-default-art-pass-filled-v0-4-audit.json"

W, H = 1920, 1080
BOARD = (15, 22, 27)
INK = (31, 32, 29)
INK_SOFT = (72, 68, 59)
IVORY = (224, 216, 194)
PAPER_DARK = (178, 164, 137)
PAPER_TEXT_HIGH = (205, 195, 168)
OLIVE_TEXT = (235, 229, 207)
LOCK_FILL = (93, 86, 70)

FONT_CN = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_CN_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_LATIN = Path(r"C:\Windows\Fonts\bahnschrift.ttf")


def font(size: int, bold: bool = False, latin: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_LATIN if latin else (FONT_CN_BOLD if bold else FONT_CN)
    return ImageFont.truetype(str(path), size=size)


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
F30_LATIN = font(30, True, True)
F18_LATIN = font(18, False, True)

RECTS = {
    "left_card_north": [30, 36, 348, 240],
    "left_card_east": [30, 294, 348, 240],
    "left_card_pacific": [30, 552, 348, 240],
    "schedule": [30, 810, 348, 246],
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


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def contains(rect: list[int], bbox: tuple[int, int, int, int]) -> bool:
    x, y, w, h = rect
    return bbox[0] >= x and bbox[1] >= y and bbox[2] <= x + w and bbox[3] <= y + h


def paste_crop(canvas: Image.Image, source: Image.Image, crop: tuple[int, int, int, int], rect: list[int]) -> None:
    x, y, w, h = rect
    art = ImageOps.fit(source.crop(crop), (w, h), method=Image.Resampling.LANCZOS)
    canvas.paste(art, (x, y))


def fitted_crop(source: Image.Image, crop: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(source.crop(crop), size, method=Image.Resampling.LANCZOS)


def safe_text(draw: ImageDraw.ImageDraw, text: str, point, used_font, fill, anchor, safe_rect, records, key) -> None:
    bbox = draw.textbbox(point, text, font=used_font, anchor=anchor)
    passed = contains(safe_rect, bbox)
    records.append({
        "key": key,
        "text": text,
        "bbox_xyxy": list(bbox),
        "safe_rect_xywh": list(safe_rect),
        "passed": passed,
    })
    draw.text(point, text, font=used_font, fill=fill, anchor=anchor)


source = Image.open(SOURCE).convert("RGB")
assert source.size == (1672, 941)

canvas = Image.new("RGB", (W, H), BOARD)

# Full art-pass panels. All three cards share one generated shell master; only
# their photographs and semantic status color vary.
selected_shell = fitted_crop(source, (24, 20, 371, 251), (348, 240))
locked_shell = ImageEnhance.Brightness(ImageEnhance.Color(selected_shell).enhance(0.18)).enhance(0.88)
photo_crops = [
    (35, 30, 361, 183),
    (35, 276, 361, 417),
    (35, 506, 361, 636),
]
footer_art = fitted_crop(source, (35, 184, 361, 239), (324, 72))
selected_status = fitted_crop(source, (267, 184, 358, 235), (80, 48))
locked_status = ImageEnhance.Brightness(ImageEnhance.Color(selected_status).enhance(0.08)).enhance(0.72)
for index, key in enumerate(["left_card_north", "left_card_east", "left_card_pacific"]):
    x, y, _, _ = RECTS[key]
    canvas.paste(selected_shell if index == 0 else locked_shell, (x, y))
    canvas.paste(fitted_crop(source, photo_crops[index], (324, 144)), (42, y + 12))
    canvas.paste(footer_art, (42, y + 156))
    canvas.paste(selected_status if index == 0 else locked_status, (284, y + 166))
paste_crop(canvas, source, (20, 707, 371, 920), RECTS["schedule"])

# Central art stage.
paste_crop(canvas, source, (394, 25, 1192, 913), RECTS["center_column"])

# Right dossier uses one calm source-paper field plus the generated outer rim.
# The full generated panel is deliberately not pasted because it already contains
# a photo and rows, which would duplicate the exact functional layers below.
ImageDraw.Draw(canvas).rectangle((1404, 32, 1884, 1064), fill=(6, 9, 10))
paste_crop(canvas, source, (1225, 323, 1638, 457), RECTS["right_dossier"])

# Re-seat generated right-column art layers at the exact functional rects.
paste_crop(canvas, source, (1308, 53, 1637, 97), RECTS["right_title"])
# Replace the generated placeholder line inside the title carrier with calm
# same-source paper, while preserving the generated outer shell.
paste_crop(canvas, source, (1300, 350, 1600, 400), [1526, 92, 323, 41])
paste_crop(canvas, source, (1225, 114, 1638, 311), RECTS["right_photo"])
paste_crop(canvas, source, (1225, 323, 1638, 457), RECTS["right_body"])
paste_crop(canvas, source, (1224, 473, 1638, 532), RECTS["mission_header"])
row_crops = [
    (1225, 541, 1638, 599),
    (1225, 600, 1638, 659),
    (1225, 660, 1638, 727),
    (1225, 728, 1638, 790),
]
for crop, y in zip(row_crops, [681, 745, 809, 873]):
    paste_crop(canvas, source, crop, [1431, y, 414, 56])
paste_crop(canvas, source, (1223, 811, 1638, 899), RECTS["cta"])

draw = ImageDraw.Draw(canvas)
records: list[dict] = []

# Masthead.
safe_text(draw, "WORLD MYSTERIES WEEKLY", (426, 58), F30_LATIN, IVORY, "lm", [426, 24, 700, 72], records, "masthead")
safe_text(draw, "WEEK 01", (1350, 58), F18_LATIN, PAPER_DARK, "rm", [1160, 24, 190, 72], records, "week")

# Three region cards; generated shells and materials remain untouched.
card_copy = [
    (RECTS["left_card_north"], "北美禁区带", "选中", OLIVE_TEXT),
    (RECTS["left_card_east"], "东亚神秘地带", "锁定", IVORY),
    (RECTS["left_card_pacific"], "太平洋失航带", "锁定", IVORY),
]
for index, (rect, title, state, state_color) in enumerate(card_copy):
    x, y, _, _ = rect
    title_safe = [48, y + 166, 224, 48]
    state_safe = [284, y + 166, 80, 48]
    safe_text(draw, title, (58, y + 190), F17, INK, "lm", title_safe, records, f"left_title_{index}")
    safe_text(draw, state, (324, y + 190), F14, state_color, "mm", state_safe, records, f"left_state_{index}")

# Schedule content directly on the generated date/action/consequence materials.
safe_text(draw, "全局日程", (42, 819), F11, (240, 232, 210), "lm", [42, 812, 116, 14], records, "schedule_section")
safe_text(draw, "当前第 1 天", (58, 850), F18, INK, "lm", [58, 836, 132, 28], records, "schedule_current")
safe_text(draw, "剩余 7 天", (350, 850), F18, INK, "rm", [218, 836, 132, 28], records, "schedule_remaining")
safe_text(draw, "→", (91, 934), F28B, INK, "mm", [75, 918, 32, 32], records, "schedule_icon")
safe_text(draw, "推进到下一天", (144, 915), F23B, IVORY, "lm", [144, 898, 210, 34], records, "schedule_title")
safe_text(draw, "点击后查看推进影响", (144, 954), F12, PAPER_TEXT_HIGH, "lm", [144, 942, 210, 24], records, "schedule_subtitle")
safe_text(draw, "当前：无任务到期", (46, 1004), F12, (24, 25, 23), "lm", [46, 994, 316, 20], records, "schedule_info_1")
safe_text(draw, "日程归零：进入编辑部阶段", (46, 1032), F12, (24, 25, 23), "lm", [46, 1022, 316, 20], records, "schedule_info_2")

# Authoritative labels. Generated selected/locked rings are retained as art shells;
# small runtime lock carriers replace their generated center glyphs.
selected_center = (614, 352)
east_center = (1122, 363)
pacific_center = (1162, 711)
safe_text(draw, "北美禁区带", (646, 352), F18, IVORY, "lm", [646, 336, 190, 32], records, "map_label_0")
for index, (center, label) in enumerate([(east_center, "东亚神秘地带"), (pacific_center, "太平洋失航带")], start=1):
    cx, cy = center
    draw.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill=LOCK_FILL, outline=IVORY, width=1)
    safe_text(draw, "锁", center, F11, INK, "mm", [cx - 15, cy - 15, 30, 30], records, f"map_lock_{index}")
    safe_text(draw, label, (cx - 28, cy), F18, IVORY, "rm", [cx - 218, cy - 16, 190, 32], records, f"map_label_{index}")

# Right dossier real content.
safe_text(draw, "北美禁区带", (1687, 112), F28B, INK, "mm", RECTS["right_title"], records, "right_region_title")
safe_text(draw, "都市传说与军事封锁交叠。", (1450, 493), F20, INK, "lm", [1450, 475, 380, 36], records, "right_body_1")
safe_text(draw, "军方巡逻、档案残页与异常雷达同时露头。", (1450, 546), F15, INK_SOFT, "lm", [1450, 528, 380, 36], records, "right_body_2")
safe_text(draw, "任务情报", (1443, 642), F22B, INK, "lm", [1443, 620, 150, 44], records, "mission_header")
safe_text(draw, "常驻 2 · 限时 1 · 深链 1", (1832, 634), F13, INK_SOFT, "rm", [1620, 618, 212, 28], records, "mission_summary")
safe_text(draw, "已展开 4 / 4 ︿", (1832, 658), F12, INK_SOFT, "rm", [1690, 646, 142, 24], records, "mission_expanded")

rows = [
    (681, "01", "51 区外围公路", "科学纪实 · 耗时 2 天", "常驻"),
    (745, "02", "罗斯威尔档案残页", "科学纪实 · 耗时 1 天", "常驻"),
    (809, "03", "突发：雷达异常光点", "大众热度 · 耗时 2 天", "限时至第 4 天"),
    (873, "04", "M330 末班车空白段", "神秘玄学 · 耗时 2 天", "深链"),
]
for index, (y, num, title, meta, tag) in enumerate(rows):
    safe_text(draw, num, (1464, y + 28), F11, INK_SOFT, "lm", [1460, y + 12, 30, 32], records, f"mission_num_{index}")
    safe_text(draw, title, (1492, y + 18), F16, INK, "lm", [1492, y + 3, 208, 28], records, f"mission_title_{index}")
    safe_text(draw, meta, (1492, y + 42), F12, INK_SOFT, "lm", [1492, y + 30, 208, 22], records, f"mission_meta_{index}")
    tag_color = IVORY if index >= 2 else INK
    safe_text(draw, tag, (1773, y + 28), F12, tag_color, "mm", [1713, y + 10, 120, 36], records, f"mission_tag_{index}")

safe_text(draw, "进入地区任务台  →", (1638, 994), F24B, IVORY, "mm", [1450, 969, 376, 50], records, "primary_cta")

# One perimeter only; no top/bottom rails or inner double frame.
draw.rectangle((1398, 24, 1877, 1055), outline=(42, 40, 33), width=2)

violations = [record for record in records if not record["passed"]]
assert not violations, violations

canvas.save(OUTPUT, optimize=True)
stats = ImageStat.Stat(canvas.resize((240, 135), Image.Resampling.BILINEAR))

left_shells = [RECTS["left_card_north"], RECTS["left_card_east"], RECTS["left_card_pacific"], RECTS["schedule"]]
axis_values = {
    "x": [rect[0] for rect in left_shells],
    "width": [rect[2] for rect in left_shells],
    "right": [rect[0] + rect[2] for rect in left_shells],
    "center_x": [rect[0] + rect[2] // 2 for rect in left_shells],
}
assert axis_values == {"x": [30] * 4, "width": [348] * 4, "right": [378] * 4, "center_x": [204] * 4}

audit = {
    "artifact_type": "fullscreen_art_pass_filled_state_mock",
    "version": "wmw_fullscreen_default_art_pass_v0_4",
    "status": "rejected_by_user_art_identity_mismatch_layout_retained",
    "canvas": [W, H],
    "state": "default",
    "source": {
        "built_in_imagegen_used": True,
        "file": SOURCE.name,
        "size": list(source.size),
        "sha256": digest(SOURCE),
        "role": "complete no-text full-screen art-pass source",
    },
    "output": {
        "file": OUTPUT.name,
        "size": list(canvas.size),
        "mode": canvas.mode,
        "sha256": digest(OUTPUT),
    },
    "geometry": {
        "functional_input": "wmw-fullscreen-default-filled-style-v0-3.png",
        "rects_xywh": RECTS,
        "left_axis_values": axis_values,
        "left_vertical_gaps_px": [18, 18, 18],
        "route_lines_drawn": 0,
        "new_ui_modules_added": 0,
    },
    "art_program_boundary": {
        "art_pass_owns_shells_buttons_paper_shadows": True,
        "program_flat_surface_overlay_count": 0,
        "program_owns_text_semantics_and_exact_rects": True,
        "placeholder_text_bars_added": 0,
    },
    "content": {
        "selected_region_id": "north_america",
        "map_pin_count": 3,
        "mission_row_count": 4,
        "primary_cta_count": 1,
        "redline_status_badge_present": False,
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
        "imagegen_source_is_technical_input_not_separate_review": True,
        "confirming_not_generated_until_default_acceptance": True,
        "godot_unchanged": True,
        "formal_contracts_unchanged": True,
        "component_atlas_not_generated": True,
    },
    "review_status": {
        "original_ui_ux_pass": "withdrawn_after_user_benchmark_rejection",
        "ui_designer_reanalysis": {"verdict": "FAIL", "p0": 1, "p1": 4, "p2": 0},
        "ux_laoge_reanalysis": {"verdict": "FAIL", "p0": 1, "p1": 4, "p2": 0},
        "user_layout_decision": "accepted_for_next_art_pass",
        "user_art_direction_decision": "rejected_benchmark_identity_mismatch",
    },
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUTPUT)
print(AUDIT)
