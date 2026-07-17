from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "black-white-functional-density-v2.png"
AUDIT = ROOT / "black-white-functional-density-v2-audit.json"

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
    for o in range(-h, w + h, spacing):
        md.line((o, h, o + h, 0), fill=255, width=1)
    img.paste(Image.new("RGB", (w, h), "#a8a8a4"), (x, y), mask)


def dimension(text, x, y, w):
    line([(x, y + 8), (x + w, y + 8)], fill=MID, width=1)
    line([(x, y + 3), (x, y + 13)], fill=MID, width=1)
    line([(x + w, y + 3), (x + w, y + 13)], fill=MID, width=1)
    txt(text, x + w / 2, y - 2, f=F11, fill=MID, anchor="ma")


# Logical three-column grid: shown faintly because it is not a product frame.
d.rectangle((0, 0, W, H), fill=PAPER)
txt("LOW-FIDELITY V2 · DENSITY / FUNCTION / POSITION ONLY · NOT ART", 16, 8, f=F12, fill=MID)
columns = {
    "left": [36, 24, 342, 1032],
    "center": [402, 24, 972, 1032],
    "right": [1398, 24, 480, 1032],
}
for x, y, w, h in columns.values():
    dashed_rect(x, y, w, h)
dimension("LEFT LOGICAL 342", 36, 1058, 342)
dimension("CENTER LOGICAL 972", 402, 1058, 972)
dimension("RIGHT LOGICAL 480", 1398, 1058, 480)


def region_card(x, y, title, state, selected=False, locked=False):
    box(x, y, 306, 240, fill=WHITE, outline=INK, width=3)
    if selected:
        box(x + 5, y + 5, 296, 230, fill=None, outline=INK, width=2)
    # Frozen visual slots.
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


# Compact global time gate. UX anchor y=810 is retained; bottom 64px is unframed breath.
box(36, 810, 342, 182, fill="#e7e7e3", outline=INK, width=3)
box(52, 822, 310, 32, fill=WHITE, outline=INK, width=2)
txt("当前第 1 天", 64, 838, f=F16, anchor="lm")
txt("剩余 7 天", 350, 838, f=F16, anchor="rm")
box(48, 864, 318, 66, fill=DARK, outline=INK, width=3)
box(60, 874, 46, 46, fill=WHITE, outline=WHITE, width=1, radius=6)
txt("01", 83, 890, f=F22B, anchor="mm")
txt("DAY", 83, 910, f=F11, fill=MID, anchor="mm")
txt("推进到下一天", 122, 885, f=F22B, fill=WHITE, anchor="la")
txt("首次点击原位确认", 122, 914, f=F12, fill="#d8d8d5", anchor="la")
txt("推进后：剩余 6 天 · 红线截止推进 · 到期 0", 52, 952, f=F13, fill=DARK, anchor="la")
txt("CONFIRMING：同一 318×66 区域替换，不扩容", 52, 978, f=F11, fill=MID, anchor="la")
txt("UNFRAMED BREATH 64", 207, 1022, f=F11, fill=MID, anchor="ma")


# Center identity and enlarged world map.
txt("WORLD MYSTERIES WEEKLY", 426, 58, f=F30B, anchor="lm")
txt("ISSUE 001 / WEEK 01", 1350, 58, f=F18, fill=MID, anchor="rm")
box(426, 96, 924, 822, fill=WHITE, outline=INK, width=3)
for gx in range(518, 1350, 92):
    line([(gx, 96), (gx, 918)], fill="#e0e0dc", width=1)
for gy in range(188, 918, 91):
    line([(426, gy), (1350, gy)], fill="#e0e0dc", width=1)

# Continents stretched to the taller stage; map remains the primary spatial object.
continents = [
    [(486, 309), (554, 218), (650, 208), (735, 262), (694, 339), (624, 374), (567, 440), (515, 378)],
    [(597, 416), (657, 405), (686, 465), (666, 542), (644, 635), (609, 704), (575, 618), (586, 526)],
    [(779, 246), (838, 185), (947, 174), (1014, 212), (1101, 198), (1192, 236), (1220, 296), (1166, 345), (1074, 348), (1007, 384), (935, 354), (853, 366)],
    [(877, 390), (961, 388), (996, 456), (975, 550), (928, 654), (874, 616), (848, 518), (826, 452)],
    [(1110, 625), (1180, 608), (1240, 653), (1221, 713), (1157, 728), (1094, 688)],
]
for poly in continents:
    d.polygon(poly, fill="#d8d8d4", outline=INK)

# Routes.
route_color = DARK
for pts in [
    [(620, 338), (790, 264), (990, 265), (1164, 349)],
    [(620, 338), (810, 446), (960, 585), (1160, 683)],
    [(1164, 349), (1195, 470), (1180, 570), (1160, 683)],
]:
    for a, b in zip(pts, pts[1:]):
        x1, y1 = a
        x2, y2 = b
        steps = max(int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 18), 1)
        for i in range(0, steps, 2):
            t1, t2 = i / steps, min((i + 1) / steps, 1)
            line([(x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1), (x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2)], fill=route_color, width=3)

pins = [
    (620, 338, "北美禁区带", True, "right"),
    (1164, 349, "东亚神秘地带", False, "left"),
    (1160, 683, "太平洋失航带", False, "left"),
]
for px, py, name, selected, side in pins:
    r = 18 if selected else 15
    d.ellipse((px - r, py - r, px + r, py + r), fill=DARK if selected else WHITE, outline=INK, width=3)
    if selected:
        d.ellipse((px - 28, py - 28, px + 28, py + 28), outline=INK, width=2)
    txt(name, px + 28 if side == "right" else px - 28, py + 2, f=F18, anchor="lm" if side == "right" else "rm")

txt("地图主舞台 924×822 · 回收高度全部归还地图", 444, 896, f=F13, fill=MID)


def receipt_strip(x, y, title, value, symbol, active_count):
    box(x, y, 450, 90, fill=WHITE, outline=INK, width=3)
    # A small identity strip replaces the old large bookmark.
    box(x + 12, y + 12, 12, 66, fill=DARK, outline=INK, width=1)
    box(x + 36, y + 16, 48, 48, fill=SOFT, outline=INK, width=2, radius=5)
    center(symbol, (x + 36, y + 16, 48, 48), F22B)
    txt(title, x + 96, y + 14, f=F20, anchor="la")
    txt(value, x + 96, y + 45, f=F14, fill=MID, anchor="la")
    # Seven compact day cells; the whole strip has no hit rect.
    start = x + 264
    for i in range(7):
        fill = DARK if i < active_count else SOFT
        box(start + i * 26, y + 36, 18, 18, fill=fill, outline=INK, width=1)
    txt("READ ONLY", x + 438, y + 70, f=F11, fill=MID, anchor="ra")


receipt_strip(426, 942, "红线预警", "红线稿剩 7 天", "!", 2)
receipt_strip(900, 942, "深链动向", "青线将推进缺口", "◎", 1)
txt("NEW CLASS：bottom_receipt_strip 450×90 ×2", 888, 1048, f=F11, fill=MID, anchor="ma")


# Right column: no visible full-height carrier. A5.1 is frozen; only a shallow pocket closes it.
txt("RIGHT LOGICAL ONLY · NO FULL-HEIGHT PRODUCT FRAME", 1410, 36, f=F11, fill=MID)
box(1398, 825, 480, 62, fill=SOFT, outline=INK, width=3)
d.polygon([(1398, 825), (1582, 825), (1612, 845), (1664, 845), (1694, 825), (1878, 825)], fill=PALE, outline=INK)
center("SHALLOW POCKET · NO TEXT / NO HIT", (1398, 825, 480, 62), F13, MID)

# Frozen A5.1 dossier.
box(1398, 45, 480, 780, fill=WHITE, outline=INK, width=4)
box(1434, 102, 54, 54, fill=WHITE, outline=INK, width=2, radius=27)
center("◎", (1434, 102, 54, 54), F22B)
box(1521, 108, 240, 51, fill=SOFT, outline=INK, width=2)
center("北美禁区带", (1521, 108, 240, 51), F22B)
box(1767, 96, 87, 87, fill=SOFT, outline=INK, width=2)
center("红线\n升温", (1767, 96, 87, 87), F18)
box(1431, 192, 414, 264, fill=SOFT, outline=INK, width=3)
hatch(1431, 192, 414, 264, spacing=34)
center("69:44 地区主照片", (1431, 192, 414, 264), F24B, DARK)
box(1431, 477, 414, 135, fill=WHITE, outline=INK, width=2)
txt("都市传说与军事封锁交叠。", 1450, 512, f=F20)
txt("红线稿需在 7 天内处理。", 1450, 548, f=F20)
txt("地区说明只回答为什么去。", 1450, 590, f=F13, fill=MID)
box(1425, 630, 426, 66, fill=WHITE, outline=INK, width=3)
txt("任务情报", 1444, 663, f=F22B, anchor="lm")
txt("限时 1 · 线索 2 · 深链 1", 1790, 663, f=F16, fill=MID, anchor="rm")
txt("＋", 1832, 663, f=F24B, anchor="mm")
box(1425, 711, 426, 75, fill=DARK, outline=INK, width=3)
center("进入地区任务台", (1425, 711, 426, 75), F28B, WHITE)
txt("A5.1 FROZEN 480×780", 1410, 64, f=F11, fill=MID)
txt("UNFRAMED WORLD BACKGROUND 169 · NO TEXT / NO HIT / NO BORDER", 1638, 970, f=F12, fill=MID, anchor="ma")


img.save(OUTPUT, format="PNG", optimize=True)

audit = {
    "artifact_type": "structure_wireframe",
    "version": "functional_density_v2",
    "viewport": [W, H],
    "columns": columns,
    "region_cards_frozen": [
        [66, 36, 306, 240],
        [66, 294, 306, 240],
        [66, 552, 306, 240],
    ],
    "time_gate_compact": [36, 810, 342, 182],
    "time_gate_unframed_bottom_breath": [36, 992, 342, 64],
    "map_stage": [426, 96, 924, 822],
    "receipt_strips": [[426, 942, 450, 90], [900, 942, 450, 90]],
    "receipt_strip_gap": 24,
    "a51_frozen": [1398, 45, 480, 780],
    "a51_cta_frozen": [1425, 711, 426, 75],
    "shallow_pocket": [1398, 825, 480, 62],
    "right_unframed_background": [1398, 887, 480, 169],
    "assertions": {
        "b212_unchanged": True,
        "a51_unchanged": True,
        "bottom_receipt_card_not_scaled": True,
        "new_bottom_receipt_strip_class_required": True,
        "receipt_strips_readonly": True,
        "receipt_strip_has_no_footnote": True,
        "third_receipt_absent": True,
        "full_height_right_product_frame_absent": True,
        "right_pocket_noninteractive": True,
        "advance_day_and_enter_region_separated": True,
        "runtime_advance_day_command_implemented": False,
    },
}
AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUTPUT)
print(AUDIT)
