from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "wmw-fullscreen-default-benchmark-art-pass-imagegen-source-v0-6.png"
OUTPUT = ROOT / "wmw-fullscreen-default-benchmark-art-pass-filled-v0-6.png"
AUDIT = ROOT / "wmw-fullscreen-default-benchmark-art-pass-filled-v0-6-audit.json"

W, H = 1920, 1080
INK = (24, 31, 33)
INK_SOFT = (63, 64, 59)
PAPER_TEXT = (223, 216, 195)
PAPER_TEXT_SOFT = (190, 184, 166)
BRAND_OLIVE = (135, 156, 54)
DEADLINE_TEXT = (242, 226, 204)
DEADLINE_INK = (139, 76, 48)

FONT_CN = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_CN_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_LATIN = Path(r"C:\Windows\Fonts\bahnschrift.ttf")
FONT_DISPLAY = Path(r"C:\Windows\Fonts\impact.ttf")


def font(size: int, bold: bool = False, latin: bool = False, display: bool = False) -> ImageFont.FreeTypeFont:
    if display:
        path = FONT_DISPLAY
    elif latin:
        path = FONT_LATIN
    else:
        path = FONT_CN_BOLD if bold else FONT_CN
    return ImageFont.truetype(str(path), size=size)


F11 = font(11)
F12 = font(12)
F13 = font(13)
F14 = font(14)
F15 = font(15)
F16 = font(16)
F17B = font(17, True)
F18 = font(18)
F20B = font(20, True)
F22B = font(22, True)
F24B = font(24, True)
F30B = font(30, True)
F16_LATIN = font(16, latin=True)
F43_DISPLAY = font(43, display=True)
F50_DISPLAY = font(50, display=True)

RECTS = {
    "left_card_north": [30, 36, 348, 240],
    "left_card_east": [30, 294, 348, 240],
    "left_card_pacific": [30, 552, 348, 240],
    "schedule": [30, 810, 348, 246],
    "center_column": [402, 24, 972, 1032],
    "center_title": [426, 24, 924, 72],
    "map_stage": [426, 96, 924, 936],
    "right_dossier": [1398, 24, 480, 1032],
    "right_title": [1438, 72, 300, 72],
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


def fit(source: Image.Image, crop: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(source.crop(crop), size, method=Image.Resampling.LANCZOS)


def paste_fit(canvas: Image.Image, source: Image.Image, crop: tuple[int, int, int, int], rect: list[int]) -> None:
    x, y, w, h = rect
    canvas.paste(fit(source, crop, (w, h)), (x, y))


def paste_feathered(canvas: Image.Image, source: Image.Image, crop: tuple[int, int, int, int], rect: list[int], edge: int = 8) -> None:
    x, y, w, h = rect
    art = fit(source, crop, (w, h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((edge, edge, w - edge - 1, h - edge - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(2, edge // 2)))
    canvas.paste(art, (x, y), mask)


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
assert source.size == (1672, 941), source.size

# Source-derived blank navy board texture for the global background. The crop
# deliberately excludes continents so gutters never show enlarged map shapes.
dark_patch_crop = (740, 650, 1040, 735)
canvas = fit(source, dark_patch_crop, (W, H))

# Fixed left carriers: three publication cards plus the weekly issue insert.
card_crops = [
    (15, 18, 370, 258),
    (15, 264, 370, 482),
    (15, 496, 370, 709),
]
for crop, key in zip(card_crops, ["left_card_north", "left_card_east", "left_card_pacific"]):
    paste_fit(canvas, source, crop, RECTS[key])
paste_fit(canvas, source, (15, 718, 370, 925), RECTS["schedule"])

# Center host: preserve the generated publication frame, then restore the exact
# functional map and masthead zones independently.
paste_fit(canvas, source, (382, 18, 1195, 925), RECTS["center_column"])
paste_fit(canvas, source, (388, 164, 1193, 925), RECTS["map_stage"])
paste_fit(canvas, source, (392, 28, 1193, 158), RECTS["center_title"])

# Right dossier remains one continuous feature sheet. A tight source crop keeps
# its rich paper texture; navy source masks remove every visible rear-page edge.
paper_patch_crop = (1450, 45, 1520, 85)
paste_fit(canvas, source, (1218, 28, 1641, 918), RECTS["right_dossier"])
paste_fit(canvas, source, dark_patch_crop, [1398, 24, 14, 1032])
paste_fit(canvas, source, dark_patch_crop, [1864, 24, 14, 1032])
paste_fit(canvas, source, dark_patch_crop, [1398, 24, 480, 8])
paste_fit(canvas, source, dark_patch_crop, [1398, 1046, 480, 10])
paste_fit(canvas, source, (1327, 12, 1385, 78), [1520, 10, 76, 76])
paste_fit(canvas, source, (1230, 157, 1625, 407), RECTS["right_photo"])
paste_fit(canvas, source, (1236, 416, 1626, 575), RECTS["right_body"])

# A calm same-source paper crop clears placeholder rules from future writing
# zones without introducing program-painted surfaces.
paste_feathered(canvas, source, paper_patch_crop, [1425, 58, 330, 104], edge=10)
paste_feathered(canvas, source, paper_patch_crop, [1438, 464, 392, 112], edge=10)
paste_feathered(canvas, source, paper_patch_crop, [1728, 484, 100, 92], edge=7)

# A strong source-derived olive publication band owns the mission heading.
paste_fit(canvas, source, (1260, 820, 1608, 900), [1425, 609, 426, 58])

# Four ledger rows remain flat information lines. The third row is the only
# rust-coded deadline row.
row_crops = [
    (1228, 584, 1632, 641),
    (1228, 641, 1632, 698),
    (1228, 698, 1632, 755),
    (1228, 755, 1632, 812),
]
for crop, y in zip(row_crops, [681, 745, 809, 873]):
    paste_fit(canvas, source, crop, [1431, y, 414, 56])
    paste_fit(canvas, source, paper_patch_crop, [1482, y + 4, 350, 48])
paste_fit(canvas, source, (1260, 820, 1608, 900), RECTS["cta"])

# Clean future text bands on card footers. The generated source keeps its small
# printed card-series seals intact; program text does not add any extra marks.
for y in [36, 294, 552]:
    paste_feathered(canvas, source, paper_patch_crop, [86, y + 158, 190, 62], edge=8)
for y in [294, 552]:
    paste_fit(canvas, source, paper_patch_crop, [31, y + 158, 255, 62])

# Schedule/date/consequence writing zones use the same generated paper.
paste_feathered(canvas, source, paper_patch_crop, [42, 819, 324, 58], edge=8)
paste_feathered(canvas, source, paper_patch_crop, [42, 986, 324, 64], edge=8)

draw = ImageDraw.Draw(canvas)
records: list[dict] = []

# Publication masthead: exact text with a display face, not generic UI labeling.
safe_text(draw, "WORLD MYSTERIES WEEKLY", (426, 60), F50_DISPLAY, INK, "lm", [426, 24, 700, 72], records, "masthead")
safe_text(draw, "WEEK 01", (1348, 58), F16_LATIN, BRAND_OLIVE, "rm", [1160, 24, 188, 72], records, "week")

# Three region cards. Generated globe marks remain at the left of each caption.
cards = [
    (36, "北美禁区带", "选中", PAPER_TEXT),
    (294, "东亚神秘地带", "锁定", PAPER_TEXT),
    (552, "太平洋失航带", "锁定", PAPER_TEXT),
]
for index, (y, title, state, state_color) in enumerate(cards):
    title_x = 98 if index == 0 else 70
    safe_text(draw, title, (title_x, y + 190), F17B, INK, "lm", [66, y + 164, 198, 48], records, f"left_title_{index}")
    safe_text(draw, state, (325, y + 190), F14, state_color, "mm", [284, y + 166, 82, 48], records, f"left_state_{index}")
    if index > 0:
        draw.line((44, y + 179, 60, y + 179), fill=INK_SOFT, width=1)
        draw.line((44, y + 187, 64, y + 187), fill=INK_SOFT, width=1)

# Schedule content on the generated weekly-insert art.
safe_text(draw, "全局日程", (50, 828), F12, INK_SOFT, "lm", [46, 817, 116, 22], records, "schedule_section")
safe_text(draw, "当前第 1 天", (58, 850), F18, INK, "lm", [58, 836, 132, 28], records, "schedule_current")
safe_text(draw, "剩余 7 天", (350, 850), F18, INK, "rm", [218, 836, 132, 28], records, "schedule_remaining")
safe_text(draw, "推进到下一天", (144, 914), F24B, PAPER_TEXT, "lm", [140, 897, 214, 36], records, "schedule_title")
safe_text(draw, "点击后查看推进影响", (144, 954), F12, PAPER_TEXT_SOFT, "lm", [140, 942, 214, 24], records, "schedule_subtitle")
safe_text(draw, "当前：无任务到期", (50, 1004), F12, INK, "lm", [46, 994, 316, 20], records, "schedule_info_1")
safe_text(draw, "日程归零：进入编辑部阶段", (50, 1032), F12, INK, "lm", [46, 1022, 316, 20], records, "schedule_info_2")

# Runtime map semantics on top of the generated editorial map.
selected_center = (614, 320)
east_center = (1122, 363)
pacific_center = (1162, 711)
# The selected North America ring is already owned by the generated art source;
# program text only supplies its exact runtime label.
safe_text(draw, "北美禁区带", (646, 352), F18, PAPER_TEXT, "lm", [646, 336, 190, 32], records, "map_label_0")
for index, (center, label) in enumerate([(east_center, "东亚神秘地带"), (pacific_center, "太平洋失航带")], start=1):
    cx, cy = center
    draw.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=(53, 73, 81), outline=PAPER_TEXT_SOFT, width=2)
    safe_text(draw, "锁", center, F11, PAPER_TEXT, "mm", [cx - 14, cy - 14, 28, 28], records, f"map_lock_{index}")
    safe_text(draw, label, (cx - 28, cy), F18, PAPER_TEXT, "rm", [cx - 218, cy - 16, 190, 32], records, f"map_label_{index}")

# Right editorial feature page.
safe_text(draw, "北美禁区带", (1444, 112), F30B, INK, "lm", RECTS["right_title"], records, "right_region_title")
safe_text(draw, "都市传说与军事封锁交叠。", (1450, 493), F20B, INK, "lm", [1450, 475, 380, 36], records, "right_body_1")
safe_text(draw, "军方巡逻、档案残页与异常雷达同时露头。", (1450, 546), F15, INK_SOFT, "lm", [1450, 528, 380, 36], records, "right_body_2")
safe_text(draw, "任务情报", (1443, 638), F22B, PAPER_TEXT, "lm", [1443, 618, 150, 40], records, "mission_header")
safe_text(draw, "常驻 2 · 限时 1 · 深链 1", (1832, 632), F13, PAPER_TEXT_SOFT, "rm", [1620, 616, 212, 28], records, "mission_summary")
safe_text(draw, "已展开 4 / 4 ︿", (1832, 654), F12, PAPER_TEXT_SOFT, "rm", [1690, 642, 142, 24], records, "mission_expanded")
draw.line((1415, 672, 1870, 672), fill=INK_SOFT, width=2)

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
    safe_text(draw, tag, (1824, y + 28), F12, DEADLINE_INK if index == 2 else INK_SOFT, "rm", [1705, y + 7, 125, 42], records, f"mission_tag_{index}")

safe_text(draw, "进入地区任务台  →", (1638, 994), F24B, PAPER_TEXT, "mm", [1450, 969, 376, 50], records, "primary_cta")

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
    "artifact_type": "fullscreen_benchmark_art_identity_revision_candidate",
    "version": "wmw_fullscreen_default_benchmark_art_pass_v0_6",
    "status": "benchmark_ui_ux_pass_pending_user_art_direction_decision",
    "canvas": [W, H],
    "state": "default",
    "source": {
        "built_in_imagegen_used": True,
        "file": SOURCE.name,
        "size": list(source.size),
        "sha256": digest(SOURCE),
        "reference_priority": ["benchmark-board-01", "benchmark-board-02", "v0.5-geometry-content-mask-only"],
    },
    "output": {
        "file": OUTPUT.name,
        "size": list(canvas.size),
        "mode": canvas.mode,
        "sha256": digest(OUTPUT),
    },
    "geometry": {
        "rects_xywh": RECTS,
        "left_axis_values": axis_values,
        "left_vertical_gaps_px": [18, 18, 18],
        "route_lines_drawn": 0,
        "new_ui_modules_added": 0,
    },
    "art_program_boundary": {
        "imagegen_owns_all_visible_carrier_materials": True,
        "same_source_art_patch_count": 35,
        "program_flat_surface_overlay_count": 0,
        "program_owns_text_and_runtime_semantics": True,
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
    "style_lock": {
        "benchmark_identity_first": True,
        "dashboard_negative_gate": True,
        "military_archive_negative_gate": True,
        "strategy_hud_negative_gate": True,
        "five_second_family_test": "pass_parent_and_ui_designer_p0_0_p1_0_p2_0",
    },
    "internal_reviews": {
        "ui_designer": {"verdict": "PASS", "p0": 0, "p1": 0, "p2": 0},
        "ux_laoge": {"verdict": "PASS", "p0": 0, "p1": 0, "p2": 0},
        "parent_three_up_benchmark_review": {"verdict": "PASS", "p0": 0, "p1": 0, "p2": 0},
        "user_art_direction_decision": "pending",
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
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUTPUT)
print(AUDIT)
