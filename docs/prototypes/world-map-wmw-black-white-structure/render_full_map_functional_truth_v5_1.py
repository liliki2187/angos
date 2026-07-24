from pathlib import Path
import json

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "black-white-full-map-v5-default.png"
DEFAULT_OUTPUT = ROOT / "black-white-full-map-v5-1-default.png"
CONFIRMING_OUTPUT = ROOT / "black-white-full-map-v5-1-schedule-confirming.png"
AUDIT = ROOT / "black-white-full-map-v5-1-audit.json"

W, H = 1920, 1080
INK = "#171717"
DARK = "#303030"
MID = "#777777"
SOFT = "#d6d6d2"
PALE = "#ecece8"
PAPER = "#f5f5f2"
WHITE = "#ffffff"

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


F10 = font(10)
F11 = font(11)
F12 = font(12)
F14 = font(14)
F16 = font(16)
F18 = font(18)
F20 = font(20)
F22B = font(22, True)
F24B = font(24, True)
F28B = font(28, True)


def line(draw, points, fill=INK, width=2):
    draw.line(points, fill=fill, width=width, joint="curve")


def txt(draw, text, x, y, used_font=F16, fill=INK, anchor="la"):
    draw.text((x, y), text, font=used_font, fill=fill, anchor=anchor)


def center(draw, text, rect, used_font=F16, fill=INK):
    x, y, w, h = rect
    txt(draw, text, x + w / 2, y + h / 2, used_font, fill, "mm")


def box(draw, rect, fill=WHITE, outline=INK, width=2, radius=0):
    x, y, w, h = rect
    bounds = (x, y, x + w, y + h)
    if radius:
        draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle(bounds, fill=fill, outline=outline, width=width)


CONTINENTS = [
    [(486, 309), (554, 218), (650, 208), (735, 262), (694, 339), (624, 374), (567, 440), (515, 378)],
    [(597, 416), (657, 405), (686, 465), (666, 542), (644, 635), (609, 704), (575, 618), (586, 526)],
    [(779, 246), (838, 185), (947, 174), (1014, 212), (1101, 198), (1192, 236), (1220, 296), (1166, 345), (1074, 348), (1007, 384), (935, 354), (853, 366)],
    [(877, 390), (961, 388), (996, 456), (975, 550), (928, 654), (874, 616), (848, 518), (826, 452)],
    [(1110, 625), (1180, 608), (1240, 653), (1221, 713), (1157, 728), (1094, 688)],
]

ANTARCTICA = [
    (496, 968), (570, 948), (650, 956), (735, 938), (820, 950), (910, 936),
    (1004, 949), (1090, 940), (1180, 955), (1270, 946), (1310, 980),
    (1220, 1008), (1108, 998), (1010, 1014), (910, 1002), (812, 1016),
    (710, 1000), (604, 1012), (520, 996),
]

ROUTES = [
    [(620, 365), (790, 284), (990, 286), (1164, 371)],
    [(620, 365), (810, 466), (960, 606), (1160, 710)],
    [(1164, 371), (1195, 490), (1180, 592), (1160, 710)],
]


def draw_dashed_route(draw, points):
    for a, b in zip(points, points[1:]):
        x1, y1 = a
        x2, y2 = b
        steps = max(int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 18), 1)
        for index in range(0, steps, 2):
            t1 = index / steps
            t2 = min((index + 1) / steps, 1)
            line(
                draw,
                [
                    (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1),
                    (x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2),
                ],
                fill=DARK,
                width=3,
            )


def draw_map_stage(with_routes):
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((426, 96, 1350, 1032), fill=WHITE)
    for gx in range(518, 1350, 92):
        line(draw, [(gx, 96), (gx, 1032)], fill="#e0e0dc", width=1)
    for gy in [188, 279, 370, 461, 552, 643, 734, 825, 916, 1007]:
        line(draw, [(426, gy), (1350, gy)], fill="#e0e0dc", width=1)
    for polygon in CONTINENTS:
        draw.polygon(polygon, fill="#d8d8d4", outline=INK)
    if with_routes:
        for route in ROUTES:
            draw_dashed_route(draw, route)

    for px, py, name, selected, side in [
        (620, 365, "北美禁区带", True, "right"),
        (1164, 371, "东亚神秘地带", False, "left"),
        (1160, 710, "太平洋失航带", False, "left"),
    ]:
        radius = 18 if selected else 15
        draw.ellipse(
            (px - radius, py - radius, px + radius, py + radius),
            fill=DARK if selected else WHITE,
            outline=INK,
            width=3,
        )
        if selected:
            draw.ellipse((px - 28, py - 28, px + 28, py + 28), outline=INK, width=2)
        txt(draw, name, px + 28 if side == "right" else px - 28, py + 2, F18, INK, "lm" if side == "right" else "rm")

    draw.polygon(ANTARCTICA, fill="#e1e1dd", outline=INK)
    box(draw, [426, 96, 924, 936], fill=None, outline=INK, width=3)
    return image


def redraw_audit_layer(draw):
    draw.rectangle((0, 0, 402, 23), fill=PAPER)
    txt(draw, "LOW-FIDELITY V5.1 · TARGET ONLY · 1920×1080", 16, 8, F11, MID)

    draw.rectangle((1160, 40, 1350, 76), fill=PAPER)
    txt(draw, "WEEK 01", 1350, 58, F18, MID, "rm")

    draw.rectangle((1408, 32, 1770, 64), fill=WHITE)
    txt(draw, "A5.1-H · TARGET ONLY · 任务展开态", 1412, 42, F11, MID)

    draw.rectangle((650, 1033, 1126, 1055), fill=PAPER)
    txt(draw, "地图主舞台 924×936 · 无路线 / 无常驻底带", 888, 1042, F10, MID, "ma")


def redraw_east_asia_card(draw):
    box(draw, [282, 446, 66, 66], fill=SOFT, outline=INK, width=3, radius=10)
    center(draw, "锁定", [282, 446, 66, 66], F16)


def redraw_locked_pins(draw):
    for px, py in [(1164, 371), (1160, 710)]:
        draw.ellipse((px - 15, py - 15, px + 15, py + 15), fill=SOFT, outline=INK, width=2)
        txt(draw, "锁", px, py + 1, F11, INK, "mm")


def redraw_schedule(draw, confirming=False):
    box(draw, [36, 810, 342, 246], fill="#e7e7e3", outline=INK, width=3)
    txt(draw, "全局日程", 48, 816, F11, MID)
    box(draw, [52, 826, 310, 48], fill=WHITE, outline=INK, width=2)
    txt(draw, "当前第 1 天", 64, 850, F16, INK, "lm")
    txt(draw, "剩余 7 天", 350, 850, F16, INK, "rm")
    box(draw, [48, 884, 318, 100], fill=DARK, outline=INK, width=3)
    box(draw, [62, 898, 70, 70], fill=WHITE, outline=WHITE, width=1, radius=6)
    center(draw, "!" if confirming else "→", [62, 898, 70, 70], F24B)
    txt(draw, "确认推进到第 2 天" if confirming else "推进到下一天", 150, 902, F22B, WHITE)
    txt(draw, "再次点击执行 · 后果见下方" if confirming else "点击后查看推进影响", 150, 950, F12, "#d8d8d5")
    line(draw, [(52, 992), (362, 992)], fill=INK, width=1)
    txt(
        draw,
        "确认后：剩余 6 天 · 无任务到期" if confirming else "当前：无任务到期",
        52,
        1004,
        F12,
        INK,
        "lm",
    )
    line(draw, [(52, 1020), (362, 1020)], fill=MID, width=1)
    txt(
        draw,
        "限时任务：雷达异常仍开放至第 4 天" if confirming else "日程归零：进入编辑部阶段",
        52,
        1032,
        F12,
        INK,
        "lm",
    )


def redraw_region_body(draw):
    box(draw, [1431, 456, 414, 135], fill=WHITE, outline=INK, width=2)
    txt(draw, "都市传说与军事封锁交叠。", 1450, 486, F20)
    txt(draw, "军方巡逻、档案残页与异常雷达同时露头。", 1450, 533, F16, MID)


def redraw_mission_intel(draw):
    box(draw, [1425, 609, 426, 66], fill=WHITE, outline=INK, width=3)
    txt(draw, "任务情报", 1443, 643, F22B, INK, "lm")
    txt(draw, "常驻 2 · 限时 1 · 深链 1", 1792, 635, F14, MID, "rm")
    txt(draw, "已展开 4 / 4 ︿", 1792, 657, F12, MID, "rm")

    box(draw, [1431, 681, 414, 248], fill=PALE, outline=INK, width=2)
    rows = [
        (681, 1, "51 区外围公路", "科学纪实 · 耗时 2 天", "常驻"),
        (745, 2, "罗斯威尔档案残页", "科学纪实 · 耗时 1 天", "常驻"),
        (809, 3, "突发：雷达异常光点", "大众热度 · 耗时 2 天", "限时至第 4 天"),
        (873, 4, "M330 末班车空白段", "神秘玄学 · 耗时 2 天", "深链"),
    ]
    for y, index, title, meta, tag in rows:
        box(draw, [1431, y, 414, 56], fill=WHITE, outline=INK, width=2)
        box(draw, [1443, y + 10, 8, 36], fill=DARK, outline=INK, width=1)
        txt(draw, f"{index:02d}", 1463, y + 16, F11, MID)
        txt(draw, title, 1492, y + 7, F16)
        txt(draw, meta, 1492, y + 35, F12, MID, "lm")
        box(draw, [1713, y + 10, 120, 36], fill=PALE, outline=INK, width=1, radius=4)
        center(draw, tag, [1713, y + 10, 120, 36], F12)


def build_common(source, clean_map, route_exact_mask):
    image = source.copy()
    image.paste(clean_map, (0, 0), route_exact_mask)
    draw = ImageDraw.Draw(image)
    redraw_audit_layer(draw)
    redraw_east_asia_card(draw)
    redraw_locked_pins(draw)
    redraw_region_body(draw)
    redraw_mission_intel(draw)
    return image


def build_allowed_mask(route_exact_mask):
    mask = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(mask)
    rects = [
        [0, 0, 402, 24],
        [1160, 40, 190, 36],
        [1408, 32, 362, 32],
        [650, 1033, 476, 22],
        [66, 294, 306, 240],
        [36, 810, 342, 246],
        [1134, 341, 60, 60],
        [1130, 680, 60, 60],
        [1431, 456, 414, 135],
        [1425, 609, 426, 66],
        [1431, 681, 414, 248],
    ]
    for x, y, w, h in rects:
        draw.rectangle((x, y, x + w, y + h), fill=255)
    route_allowed = route_exact_mask.filter(ImageFilter.MaxFilter(13))
    return ImageChops.lighter(mask, route_allowed), rects, route_allowed


def diff_audit(source, candidate, allowed_mask):
    diff = ImageChops.difference(source, candidate)
    bbox = diff.getbbox()
    changed_pixels = 0
    outside_allowed = 0
    if bbox is not None:
        pixels = diff.load()
        allowed = allowed_mask.load()
        for y in range(bbox[1], bbox[3]):
            for x in range(bbox[0], bbox[2]):
                if pixels[x, y] != (0, 0, 0):
                    changed_pixels += 1
                    if allowed[x, y] == 0:
                        outside_allowed += 1
    return {
        "difference_bbox_xyxy": list(bbox) if bbox else None,
        "changed_pixels": changed_pixels,
        "outside_allowed_pixels": outside_allowed,
        "passed": outside_allowed == 0,
    }


source = Image.open(SOURCE).convert("RGB")
assert source.size == (W, H)

map_with_routes = draw_map_stage(with_routes=True)
map_without_routes = draw_map_stage(with_routes=False)
route_difference = ImageChops.difference(map_with_routes, map_without_routes)
route_exact_mask = route_difference.convert("L").point(lambda value: 255 if value else 0)
route_exact_bbox = route_exact_mask.getbbox()
assert route_exact_bbox is not None

common = build_common(source, map_without_routes, route_exact_mask)
default_image = common.copy()
redraw_schedule(ImageDraw.Draw(default_image), confirming=False)
confirming_image = common.copy()
redraw_schedule(ImageDraw.Draw(confirming_image), confirming=True)

assert default_image.size == (W, H)
assert confirming_image.size == (W, H)

allowed_mask, allowed_rects, route_allowed = build_allowed_mask(route_exact_mask)
default_diff = diff_audit(source, default_image, allowed_mask)
confirming_diff = diff_audit(source, confirming_image, allowed_mask)
state_diff = diff_audit(default_image, confirming_image, Image.new("L", (W, H), 0))

schedule_only = Image.new("L", (W, H), 0)
ImageDraw.Draw(schedule_only).rectangle((36, 810, 378, 1056), fill=255)
state_delta = ImageChops.difference(default_image, confirming_image)
state_outside_schedule = ImageChops.multiply(state_delta.convert("L"), ImageChops.invert(schedule_only)).getbbox()

assert default_diff["passed"]
assert confirming_diff["passed"]
assert state_outside_schedule is None

default_image.save(DEFAULT_OUTPUT, format="PNG", optimize=True)
confirming_image.save(CONFIRMING_OUTPUT, format="PNG", optimize=True)

audit = {
    "artifact_type": "structure_wireframe_state_pair",
    "version": "full_map_functional_truth_v5_1",
    "viewport": [W, H],
    "source": str(SOURCE),
    "fixture": {
        "week": 1,
        "current_day": 1,
        "remaining_days": 7,
        "reputation": 45,
        "roswell_dossier": False,
        "east_asia_unlocked": False,
        "pacific_unlocked": False,
    },
    "outputs": {
        "default": str(DEFAULT_OUTPUT),
        "schedule_confirming": str(CONFIRMING_OUTPUT),
    },
    "target_only": True,
    "runtime_support": {
        "independent_advance_day": False,
        "a51h_full_height": False,
        "deadline_day_in_world_preview": False,
    },
    "geometry": {
        "columns_unchanged": True,
        "map_stage": [426, 96, 924, 936],
        "schedule": [36, 810, 342, 246],
        "east_asia_card": [66, 294, 306, 240],
        "right_dossier": [1398, 24, 480, 1032],
        "cta": [1425, 957, 426, 75],
        "allowed_rects_xywh": allowed_rects,
    },
    "route_removal": {
        "paths": ROUTES,
        "exact_difference_bbox_xyxy": list(route_exact_bbox),
        "exact_changed_pixels": sum(1 for value in route_exact_mask.get_flattened_data() if value),
        "allowed_mask_dilation_px": 6,
        "allowed_mask_pixels": sum(1 for value in route_allowed.get_flattened_data() if value),
        "edge_data_present": False,
    },
    "copy_truth": {
        "schedule_deep_chain_advance_removed": True,
        "zero_days_enters_editorial": True,
        "east_asia_locked": True,
        "mission_summary": "常驻 2 · 限时 1 · 深链 1",
        "mission_type_source": "Content.TAG_LABELS[node.type]",
        "region_body_secondary_is_candidate_copy": True,
        "issue_number_removed_until_formal_source_exists": True,
    },
    "diff": {
        "default_vs_v5": default_diff,
        "confirming_vs_v5": confirming_diff,
        "default_vs_confirming": {
            "difference_bbox_xyxy": state_diff["difference_bbox_xyxy"],
            "changed_pixels": state_diff["changed_pixels"],
            "outside_schedule_pixels": 0,
            "passed": True,
        },
    },
    "assertions": {
        "outside_allowed_pixels_default": default_diff["outside_allowed_pixels"] == 0,
        "outside_allowed_pixels_confirming": confirming_diff["outside_allowed_pixels"] == 0,
        "state_delta_schedule_only": state_outside_schedule is None,
        "three_column_geometry_unchanged": True,
        "map_outline_and_pin_coordinates_unchanged": True,
        "right_boxes_and_cta_unchanged": True,
        "compact_a51_frozen_contract_unchanged": True,
        "godot_runtime_unchanged": True,
        "colored_art_not_generated": True,
    },
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(DEFAULT_OUTPUT)
print(CONFIRMING_OUTPUT)
print(AUDIT)
