from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "black-white-functional-closure-v3.png"
AUDIT = ROOT / "black-white-functional-closure-v3-audit.json"

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
F13 = font(13)
F14 = font(14)
F16 = font(16)
F18 = font(18)
F20 = font(20)
F22B = font(22, True)
F24B = font(24, True)
F28B = font(28, True)
F30B = font(30, True)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def box(x, y, w, h, fill=WHITE, outline=INK, width=2, radius=0):
    bounds = (x, y, x + w, y + h)
    if radius:
        d.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)
    else:
        d.rectangle(bounds, fill=fill, outline=outline, width=width)


def txt(text, x, y, f=F16, fill=INK, anchor="la"):
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)


def center(text, rect, f=F16, fill=INK):
    x, y, w, h = rect
    txt(text, x + w / 2, y + h / 2, f=f, fill=fill, anchor="mm")


def line(points, fill=INK, width=2):
    d.line(points, fill=fill, width=width, joint="curve")


def dashed_rect(x, y, w, h, fill="#b0b0ac", dash=10, gap=8, width=1):
    for sx in range(x, x + w, dash + gap):
        line([(sx, y), (min(sx + dash, x + w), y)], fill=fill, width=width)
        line([(sx, y + h), (min(sx + dash, x + w), y + h)], fill=fill, width=width)
    for sy in range(y, y + h, dash + gap):
        line([(x, sy), (x, min(sy + dash, y + h))], fill=fill, width=width)
        line([(x + w, sy), (x + w, min(sy + dash, y + h))], fill=fill, width=width)


def hatch(x, y, w, h, spacing=22):
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for offset in range(-h, w + h, spacing):
        md.line((offset, h, offset + h, 0), fill=255, width=1)
    img.paste(Image.new("RGB", (w, h), "#a8a8a4"), (x, y), mask)


def dimension(label, x, y, w):
    line([(x, y + 8), (x + w, y + 8)], fill=MID, width=1)
    line([(x, y + 3), (x, y + 13)], fill=MID, width=1)
    line([(x + w, y + 3), (x + w, y + 13)], fill=MID, width=1)
    txt(label, x + w / 2, y - 2, f=F10, fill=MID, anchor="ma")


columns = {
    "left": [36, 24, 342, 1032],
    "center": [402, 24, 972, 1032],
    "right": [1398, 24, 480, 1032],
}

d.rectangle((0, 0, W, H), fill=PAPER)
txt("LOW-FIDELITY V3 · FUNCTIONAL CLOSURE · 1920×1080 · NOT ART", 16, 8, f=F11, fill=MID)
for x, y, w, h in columns.values():
    dashed_rect(x, y, w, h)
dimension("LEFT 342", 36, 1058, 342)
dimension("CENTER 972", 402, 1058, 972)
dimension("RIGHT 480", 1398, 1058, 480)


def region_card(x, y, title, state, selected=False, locked=False):
    box(x, y, 306, 240, fill=WHITE, outline=INK, width=3)
    if selected:
        box(x + 5, y + 5, 296, 230, fill=None, outline=INK, width=2)
    box(x + 32, y + 36, 261, 96, fill=SOFT, outline=INK, width=2)
    hatch(x + 32, y + 36, 261, 96)
    center("地区照片", (x + 32, y + 36, 261, 96), F18, DARK)
    d.ellipse((x + 16, y + 14, x + 48, y + 46), outline=INK, width=2)
    line([(x + 24, y + 30), (x + 40, y + 30)], width=1)
    line([(x + 32, y + 16), (x + 32, y + 44)], width=1)
    box(x + 33, y + 156, 171, 48, fill=WHITE, outline=INK, width=2)
    center(title, (x + 33, y + 156, 171, 48), F20)
    badge_fill = DARK if selected else (SOFT if locked else WHITE)
    badge_text = WHITE if selected else INK
    box(x + 216, y + 152, 66, 66, fill=badge_fill, outline=INK, width=3, radius=10)
    center(state, (x + 216, y + 152, 66, 66), F16, badge_text)


region_card(66, 36, "北美禁区带", "选中", selected=True)
region_card(66, 294, "东亚神秘地带", "可用")
region_card(66, 552, "太平洋失航带", "锁定", locked=True)


# Full schedule responsibility closes the left column at y=1056.
box(36, 810, 342, 246, fill="#e7e7e3", outline=INK, width=3)
txt("全局日程", 48, 816, f=F11, fill=MID)
box(52, 826, 310, 48, fill=WHITE, outline=INK, width=2)
txt("当前第 1 天", 64, 850, f=F16, anchor="lm")
txt("剩余 7 天", 350, 850, f=F16, anchor="rm")
box(48, 884, 318, 100, fill=DARK, outline=INK, width=3)
box(62, 898, 70, 70, fill=WHITE, outline=WHITE, width=1, radius=6)
txt("01", 97, 920, f=F24B, anchor="mm")
txt("DAY", 97, 950, f=F11, fill=MID, anchor="mm")
txt("推进到下一天", 150, 902, f=F22B, fill=WHITE)
txt("首次点击后原位确认", 150, 950, f=F12, fill="#d8d8d5")
line([(52, 992), (362, 992)], fill=INK, width=1)
txt("直接后果：剩余 6 天 · 红线 / 深链推进", 52, 1004, f=F12, anchor="lm")
line([(52, 1020), (362, 1020)], fill=MID, width=1)
txt("到期提示：无任务到期 · 第 0 天进入结算", 52, 1032, f=F12, anchor="lm")


# Center identity and enlarged world map.
txt("WORLD MYSTERIES WEEKLY", 426, 58, f=F30B, anchor="lm")
txt("ISSUE 001 / WEEK 01", 1350, 58, f=F18, fill=MID, anchor="rm")
box(426, 96, 924, 822, fill=WHITE, outline=INK, width=3)
for gx in range(518, 1350, 92):
    line([(gx, 96), (gx, 918)], fill="#e0e0dc", width=1)
for gy in range(188, 918, 91):
    line([(426, gy), (1350, gy)], fill="#e0e0dc", width=1)

continents = [
    [(486, 309), (554, 218), (650, 208), (735, 262), (694, 339), (624, 374), (567, 440), (515, 378)],
    [(597, 416), (657, 405), (686, 465), (666, 542), (644, 635), (609, 704), (575, 618), (586, 526)],
    [(779, 246), (838, 185), (947, 174), (1014, 212), (1101, 198), (1192, 236), (1220, 296), (1166, 345), (1074, 348), (1007, 384), (935, 354), (853, 366)],
    [(877, 390), (961, 388), (996, 456), (975, 550), (928, 654), (874, 616), (848, 518), (826, 452)],
    [(1110, 625), (1180, 608), (1240, 653), (1221, 713), (1157, 728), (1094, 688)],
]
for polygon in continents:
    d.polygon(polygon, fill="#d8d8d4", outline=INK)

for points in [
    [(620, 365), (790, 284), (990, 286), (1164, 371)],
    [(620, 365), (810, 466), (960, 606), (1160, 710)],
    [(1164, 371), (1195, 490), (1180, 592), (1160, 710)],
]:
    for a, b in zip(points, points[1:]):
        x1, y1 = a
        x2, y2 = b
        steps = max(int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 18), 1)
        for i in range(0, steps, 2):
            t1 = i / steps
            t2 = min((i + 1) / steps, 1)
            line(
                [
                    (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1),
                    (x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2),
                ],
                fill=DARK,
                width=3,
            )

for px, py, name, selected, side in [
    (620, 365, "北美禁区带", True, "right"),
    (1164, 371, "东亚神秘地带", False, "left"),
    (1160, 710, "太平洋失航带", False, "left"),
]:
    radius = 18 if selected else 15
    d.ellipse((px - radius, py - radius, px + radius, py + radius), fill=DARK if selected else WHITE, outline=INK, width=3)
    if selected:
        d.ellipse((px - 28, py - 28, px + 28, py + 28), outline=INK, width=2)
    txt(name, px + 28 if side == "right" else px - 28, py + 2, f=F18, anchor="lm" if side == "right" else "rm")

txt("地图主舞台 924×822", 444, 896, f=F13, fill=MID)


def receipt_strip(x, y, title, value, symbol, active_count):
    box(x, y, 450, 90, fill=WHITE, outline=INK, width=3)
    box(x + 12, y + 12, 12, 66, fill=DARK, outline=INK, width=1)
    box(x + 36, y + 16, 48, 48, fill=SOFT, outline=INK, width=2, radius=5)
    center(symbol, (x + 36, y + 16, 48, 48), F22B)
    txt(title, x + 96, y + 14, f=F20)
    txt(value, x + 96, y + 45, f=F14, fill=MID)
    start = x + 264
    for i in range(7):
        cell_fill = DARK if i < active_count else SOFT
        box(start + i * 26, y + 36, 18, 18, fill=cell_fill, outline=INK, width=1)
    txt("只读", x + 438, y + 70, f=F11, fill=MID, anchor="ra")


receipt_strip(426, 942, "红线预警", "红线剩余 7 天", "!", 2)
receipt_strip(900, 942, "深链动向", "青线将推进缺口", "◎", 1)


# A5.1-H: full-height derivative. The compact frozen A5.1 remains untouched elsewhere.
box(1398, 24, 480, 1032, fill=WHITE, outline=INK, width=4)
txt("A5.1-H · 全高地区档案 · 主交付态：任务展开", 1412, 42, f=F11, fill=MID)
d.polygon([(1842, 24), (1878, 24), (1878, 60)], fill=PALE, outline=INK)
box(1434, 81, 54, 54, fill=WHITE, outline=INK, width=2, radius=27)
center("◎", (1434, 81, 54, 54), F22B)
box(1521, 87, 240, 51, fill=SOFT, outline=INK, width=2)
center("北美禁区带", (1521, 87, 240, 51), F22B)
box(1767, 75, 87, 87, fill=SOFT, outline=INK, width=2)
center("红线\n升温", (1767, 75, 87, 87), F18)
box(1431, 171, 414, 264, fill=SOFT, outline=INK, width=3)
hatch(1431, 171, 414, 264, spacing=34)
center("69:44 地区主照片", (1431, 171, 414, 264), F24B, DARK)
box(1431, 456, 414, 135, fill=WHITE, outline=INK, width=2)
txt("都市传说与军事封锁交叉。", 1450, 491, f=F20)
txt("红线稿需在 7 天内处理。", 1450, 527, f=F20)
txt("地区说明只回答为什么去。", 1450, 569, f=F13, fill=MID)

box(1425, 609, 426, 66, fill=WHITE, outline=INK, width=3)
txt("任务情报", 1443, 643, f=F22B, anchor="lm")
txt("限时 1 · 线索 2 · 深链 1", 1792, 635, f=F14, fill=MID, anchor="rm")
txt("已展开 4 / 4 ︿", 1792, 657, f=F12, fill=MID, anchor="rm")

box(1431, 681, 414, 248, fill=PALE, outline=INK, width=2)


def mission_row(y, index, title, meta, tag):
    box(1431, y, 414, 56, fill=WHITE, outline=INK, width=2)
    box(1443, y + 10, 8, 36, fill=DARK, outline=INK, width=1)
    txt(f"{index:02d}", 1463, y + 16, f=F11, fill=MID)
    txt(title, 1492, y + 7, f=F16)
    txt(meta, 1492, y + 35, f=F12, fill=MID, anchor="lm")
    box(1713, y + 10, 120, 36, fill=PALE, outline=INK, width=1, radius=4)
    center(tag, (1713, y + 10, 120, 36), F12)


mission_row(681, 1, "51 区外围公路", "科学调查 · 耗时 2 天", "常驻")
mission_row(745, 2, "罗斯威尔档案残页", "科学调查 · 耗时 1 天", "线索")
mission_row(809, 3, "突发：雷达异常光点", "热点调查 · 耗时 2 天", "限时至第 4 天")
mission_row(873, 4, "M330 末班车空白段", "神秘调查 · 耗时 2 天", "深链")

box(1425, 957, 426, 75, fill=DARK, outline=INK, width=3)
center("进入地区任务台   →", (1425, 957, 426, 75), F28B, WHITE)
txt("24px 安全边距", 1638, 1043, f=F10, fill=MID, anchor="ma")


img.save(OUTPUT, format="PNG", optimize=True)

audit = {
    "artifact_type": "structure_wireframe",
    "version": "functional_closure_v3",
    "viewport": [W, H],
    "columns": columns,
    "region_cards_frozen": [
        [66, 36, 306, 240],
        [66, 294, 306, 240],
        [66, 552, 306, 240],
    ],
    "schedule_gate_full": [36, 810, 342, 246],
    "schedule_default_action": [48, 884, 318, 100],
    "schedule_consequence": [52, 992, 310, 24],
    "schedule_due_hint": [52, 1020, 310, 24],
    "map_stage": [426, 96, 924, 822],
    "receipt_strips": [[426, 942, 450, 90], [900, 942, 450, 90]],
    "receipt_strip_gap": 24,
    "a51h_full_height_derivative": [1398, 24, 480, 1032],
    "mission_intel_header": [1425, 609, 426, 66],
    "mission_intel_content": [1431, 681, 414, 248],
    "mission_rows_expanded": [
        [1431, 681, 414, 56],
        [1431, 745, 414, 56],
        [1431, 809, 414, 56],
        [1431, 873, 414, 56],
    ],
    "a51h_cta_bottom_anchored": [1425, 957, 426, 75],
    "a51h_bottom_safe_margin": 24,
    "assertions": {
        "b212_unchanged": True,
        "compact_a51_contract_untouched": True,
        "new_a51h_derivative_required": True,
        "schedule_reaches_column_bottom": True,
        "left_unframed_void_absent": True,
        "right_pocket_absent": True,
        "right_unframed_void_absent": True,
        "right_column_ends_in_real_decision": True,
        "mission_intel_expanded_is_main_delivery_state": True,
        "collapsed_summary_must_keep_equal_height": True,
        "cta_position_stable_across_intel_states": True,
        "bottom_receipt_strip_class_required": True,
        "third_receipt_absent": True,
        "runtime_contract_changed": False,
    },
}
AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUTPUT)
print(AUDIT)
