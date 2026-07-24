from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "wmw-fullscreen-default-art-pass-imagegen-source-v0-5.png"
OUTPUT = ROOT / "wmw-fullscreen-default-benchmark-art-pass-filled-v0-5.png"
AUDIT = ROOT / "wmw-fullscreen-default-benchmark-art-pass-filled-v0-5-audit.json"

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

# Use source-derived dark editorial board texture for the whole background.
canvas = fit(source, (820, 32, 1030, 142), (W, H))

# The generated source owns every visible carrier, material, photo mount and shadow.
card_crops = [
    (20, 17, 400, 264),
    (25, 268, 401, 480),
    (23, 490, 401, 687),
]
for crop, key in zip(card_crops, ["left_card_north", "left_card_east", "left_card_pacific"]):
    paste_fit(canvas, source, crop, RECTS[key])
paste_fit(canvas, source, (24, 694, 400, 920), RECTS["schedule"])

# Central board and map. Remove the generated bottom ticket-like decorations with
# a same-source board patch; Antarctica / editorial ice strip remains above it.
paste_fit(canvas, source, (402, 18, 1186, 920), RECTS["center_column"])
paste_fit(canvas, source, (650, 800, 1050, 846), [410, 946, 956, 110])

# Right page: one continuous generated feature sheet, then exact photo/body/rows/CTA.
paste_fit(canvas, source, (1188, 20, 1631, 920), RECTS["right_dossier"])
paste_fit(canvas, source, (1214, 151, 1608, 376), RECTS["right_photo"])
paste_fit(canvas, source, (1211, 417, 1608, 549), RECTS["right_body"])

# Same-source calm paper patches remove generated placeholder rules only inside
# future writing zones, preserving surrounding paper, clips, seals and color edges.
paper_patch_crop = (1360, 35, 1510, 72)
paste_feathered(canvas, source, paper_patch_crop, [1428, 68, 310, 94], edge=10)
paste_feathered(canvas, source, paper_patch_crop, [1438, 466, 392, 108], edge=10)
paste_feathered(canvas, source, paper_patch_crop, [1410, 650, 460, 25], edge=6)

# Four exact mission rows are constructed from the generated printed-row language.
row_teal = (1210, 579, 1607, 632)
row_rust = (1210, 685, 1607, 739)
for index, y in enumerate([681, 745, 809, 873]):
    paste_fit(canvas, source, row_rust if index == 2 else row_teal, [1431, y, 414, 56])
    # Statuses are read-only printed labels. Remove the generated raised tag
    # carrier so the CTA remains the only object with button-like volume.
    paste_fit(canvas, source, paper_patch_crop, [1694, y + 3, 147, 50])
paste_fit(canvas, source, (1210, 768, 1612, 904), RECTS["cta"])

# Clean future text bands in card footers but retain generated globe seals and
# printed status tags. Schedule/date/consequence faces use source paper too.
for y in [36, 294, 552]:
    paste_feathered(canvas, source, paper_patch_crop, [86, y + 156, 190, 68], edge=9)
paste_feathered(canvas, source, paper_patch_crop, [42, 823, 324, 54], edge=8)
paste_fit(canvas, source, (150, 748, 382, 816), [132, 884, 234, 100])
paste_fit(canvas, source, paper_patch_crop, [38, 954, 98, 34])
paste_feathered(canvas, source, paper_patch_crop, [42, 988, 324, 62], edge=8)

draw = ImageDraw.Draw(canvas)
records: list[dict] = []

# Publication masthead: exact text with a display face, not generic UI labeling.
safe_text(draw, "WORLD MYSTERIES WEEKLY", (426, 58), F43_DISPLAY, PAPER_TEXT, "lm", [426, 24, 650, 72], records, "masthead")
safe_text(draw, "WEEK 01", (1348, 58), F16_LATIN, BRAND_OLIVE, "rm", [1160, 24, 188, 72], records, "week")

# Three region cards. Generated globe marks remain at the left of each caption.
cards = [
    (36, "北美禁区带", "选中", PAPER_TEXT),
    (294, "东亚神秘地带", "锁定", PAPER_TEXT),
    (552, "太平洋失航带", "锁定", PAPER_TEXT),
]
for index, (y, title, state, state_color) in enumerate(cards):
    safe_text(draw, title, (98, y + 190), F17B, INK, "lm", [92, y + 164, 172, 48], records, f"left_title_{index}")
    safe_text(draw, state, (325, y + 190), F14, state_color, "mm", [284, y + 166, 82, 48], records, f"left_state_{index}")

# Schedule content on the generated weekly-insert art.
safe_text(draw, "全局日程", (50, 828), F12, INK_SOFT, "lm", [46, 817, 116, 22], records, "schedule_section")
safe_text(draw, "当前第 1 天", (58, 850), F18, INK, "lm", [58, 836, 132, 28], records, "schedule_current")
safe_text(draw, "剩余 7 天", (350, 850), F18, INK, "rm", [218, 836, 132, 28], records, "schedule_remaining")
safe_text(draw, "推进到下一天", (144, 914), F24B, PAPER_TEXT, "lm", [140, 897, 214, 36], records, "schedule_title")
safe_text(draw, "点击后查看推进影响", (144, 954), F12, PAPER_TEXT_SOFT, "lm", [140, 942, 214, 24], records, "schedule_subtitle")
safe_text(draw, "当前：无任务到期", (50, 1004), F12, INK, "lm", [46, 994, 316, 20], records, "schedule_info_1")
safe_text(draw, "日程归零：进入编辑部阶段", (50, 1032), F12, INK, "lm", [46, 1022, 316, 20], records, "schedule_info_2")

# Runtime map semantics on top of the generated editorial map.
selected_center = (614, 352)
east_center = (1122, 363)
pacific_center = (1162, 711)
draw.ellipse((590, 328, 638, 376), outline=PAPER_TEXT, width=3)
draw.ellipse((598, 336, 630, 368), outline=BRAND_OLIVE, width=3)
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
safe_text(draw, "任务情报", (1443, 642), F22B, INK, "lm", [1443, 620, 150, 44], records, "mission_header")
safe_text(draw, "常驻 2 · 限时 1 · 深链 1", (1832, 634), F13, INK_SOFT, "rm", [1620, 618, 212, 28], records, "mission_summary")
safe_text(draw, "已展开 4 / 4 ︿", (1832, 658), F12, INK_SOFT, "rm", [1690, 646, 142, 24], records, "mission_expanded")
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
    "artifact_type": "fullscreen_benchmark_art_identity_pass_candidate",
    "version": "wmw_fullscreen_default_benchmark_art_pass_v0_5",
    "status": "parent_three_up_benchmark_identity_iterate_pending_user_decision",
    "canvas": [W, H],
    "state": "default",
    "source": {
        "built_in_imagegen_used": True,
        "file": SOURCE.name,
        "size": list(source.size),
        "sha256": digest(SOURCE),
        "reference_priority": ["benchmark-board-01", "benchmark-board-02", "v0.4-geometry-content-mask-only"],
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
        "same_source_art_patch_count": 23,
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
        "five_second_family_test": "reopened_parent_three_up_comparison_iterate",
    },
    "internal_reviews": {
        "ui_designer": {"verdict": "PASS", "p0": 0, "p1": 0, "p2": 0},
        "ux_laoge": {"verdict": "PASS", "p0": 0, "p1": 0, "p2": 0},
        "parent_three_up_benchmark_review": {
            "verdict": "ITERATE",
            "p0": 1,
            "reason": "same-family cues exist, but benchmark-scale typography, color-block rhythm, collage asymmetry and graphic-symbol energy remain materially weaker",
        },
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
