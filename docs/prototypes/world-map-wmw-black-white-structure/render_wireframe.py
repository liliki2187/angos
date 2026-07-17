from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "black-white-function-structure-v1.png"
AUDIT = ROOT / "black-white-function-structure-v1-audit.json"

W, H = 1920, 1080
INK = "#171717"
DARK = "#303030"
MID = "#777777"
LIGHT = "#d9d9d9"
PAPER = "#f3f3f0"
WHITE = "#ffffff"

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_LATIN = Path(r"C:\Windows\Fonts\arialbd.ttf")


def font(size, bold=False, latin=False):
    path = FONT_LATIN if latin else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(str(path), size=size)


F12 = font(12)
F13 = font(13)
F14 = font(14)
F16 = font(16)
F18 = font(18)
F20 = font(20)
F22 = font(22, bold=True)
F24 = font(24, bold=True)
F26 = font(26, bold=True)
F28 = font(28, bold=True)
F30 = font(30, bold=True)
F34 = font(34, bold=True)
F38 = font(38, bold=True)
F24_LATIN = font(24, latin=True)


img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def box(x, y, w, h, fill=WHITE, outline=INK, width=2, radius=0):
    xy = (x, y, x + w, y + h)
    if radius:
        d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    else:
        d.rectangle(xy, fill=fill, outline=outline, width=width)


def label(text, x, y, f=F16, fill=INK, anchor="la"):
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)


def centered(text, rect, f=F16, fill=INK):
    x, y, w, h = rect
    label(text, x + w / 2, y + h / 2, f=f, fill=fill, anchor="mm")


def line(points, fill=INK, width=2, dash=None):
    if not dash:
        d.line(points, fill=fill, width=width, joint="curve")
        return
    for start, end in zip(points, points[1:]):
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        length = max((dx * dx + dy * dy) ** 0.5, 1)
        ux, uy = dx / length, dy / length
        cursor = 0.0
        draw_segment = True
        while cursor < length:
            step = dash[0] if draw_segment else dash[1]
            nxt = min(cursor + step, length)
            if draw_segment:
                d.line(
                    (
                        x1 + ux * cursor,
                        y1 + uy * cursor,
                        x1 + ux * nxt,
                        y1 + uy * nxt,
                    ),
                    fill=fill,
                    width=width,
                )
            cursor = nxt
            draw_segment = not draw_segment


def hatch(rect, spacing=18, fill="#b0b0b0", width=1):
    x, y, w, h = rect
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for offset in range(-h, w + h, spacing):
        md.line((offset, h, offset + h, 0), fill=255, width=width)
    pattern = Image.new("RGB", (w, h), fill)
    img.paste(pattern, (x, y), mask)


def dimension(text, x, y, w):
    line([(x, y + 10), (x + w, y + 10)], fill=MID, width=1)
    line([(x, y + 5), (x, y + 15)], fill=MID, width=1)
    line([(x + w, y + 5), (x + w, y + 15)], fill=MID, width=1)
    label(text, x + w / 2, y - 2, f=F12, fill=MID, anchor="ma")


# Canvas and exact three-column host.
d.rectangle((0, 0, W, H), fill=PAPER)
label("LOW-FIDELITY · FUNCTION / POSITION / SIZE ONLY · NOT ART", 16, 8, f=F12, fill=MID)

columns = {
    "left": (36, 24, 342, 1032),
    "center": (402, 24, 972, 1032),
    "right": (1398, 24, 480, 1032),
}
for x, y, w, h in columns.values():
    box(x, y, w, h, fill=WHITE, outline=DARK, width=2)

dimension("LEFT 342", 36, 1058, 342)
dimension("CENTER 972", 402, 1058, 972)
dimension("RIGHT 480", 1398, 1058, 480)


def draw_region_card(x, y, title, state, selected=False, locked=False):
    box(x, y, 306, 240, fill=WHITE, outline=INK, width=3)
    if selected:
        box(x + 5, y + 5, 296, 230, fill=None, outline=INK, width=2)
    photo = (x + 32, y + 36, 261, 96)
    box(*photo, fill=LIGHT, outline=INK, width=2)
    hatch(photo, spacing=24, fill="#a6a6a6")
    centered("地区照片", photo, F20, DARK)
    # Globe ownership marker.
    d.ellipse((x + 16, y + 14, x + 48, y + 46), outline=INK, width=2)
    line([(x + 24, y + 30), (x + 40, y + 30)], width=1)
    line([(x + 32, y + 16), (x + 32, y + 44)], width=1)
    # Frozen bottom title plate + state badge.
    box(x + 33, y + 156, 171, 48, fill=WHITE, outline=INK, width=2)
    centered(title, (x + 33, y + 156, 171, 48), F20)
    badge_fill = DARK if selected else (LIGHT if locked else WHITE)
    badge_text = WHITE if selected else INK
    box(x + 216, y + 152, 66, 66, fill=badge_fill, outline=INK, width=3, radius=10)
    centered(state, (x + 216, y + 152, 66, 66), F16, badge_text)


draw_region_card(66, 36, "北美禁区带", "选中", selected=True)
draw_region_card(66, 294, "东亚神秘地带", "可用")
draw_region_card(66, 552, "太平洋失航带", "锁定", locked=True)


# Left-bottom global time gate: independent from region selection.
box(36, 810, 342, 246, fill="#ededed", outline=INK, width=3)
box(52, 826, 310, 48, fill=WHITE, outline=INK, width=2)
label("全局日程", 64, 850, f=F18, fill=MID, anchor="lm")
label("当前第 1 天", 178, 850, f=F18, anchor="mm")
label("剩余 7 天", 342, 850, f=F18, anchor="rm")

box(48, 884, 318, 100, fill=DARK, outline=INK, width=3)
box(62, 898, 70, 70, fill=WHITE, outline=WHITE, width=2, radius=8)
label("01", 97, 924, f=F28, anchor="mm")
label("DAY", 97, 952, f=F12, fill=MID, anchor="mm")
label("推进到下一天", 150, 916, f=F24, fill=WHITE, anchor="la")
label("首次点击进入确认态", 150, 950, f=F14, fill="#d8d8d8", anchor="la")
label("推进后：剩余 6 天 · 红线截止推进 · 到期 0", 52, 1022, f=F14, fill=DARK, anchor="la")


# Center masthead and identity. Day count intentionally has one owner only: left time gate.
label("WORLD MYSTERIES WEEKLY", 426, 56, f=F30, anchor="lm")
label("ISSUE 001 / WEEK 01", 1350, 56, f=F18, fill=MID, anchor="rm")


# Map stage.
box(426, 96, 924, 696, fill=WHITE, outline=INK, width=3)
for gx in range(426 + 92, 1350, 92):
    line([(gx, 96), (gx, 792)], fill="#e1e1e1", width=1)
for gy in range(96 + 87, 792, 87):
    line([(426, gy), (1350, gy)], fill="#e1e1e1", width=1)

continents = [
    [(488, 294), (556, 210), (652, 201), (735, 250), (695, 321), (625, 353), (568, 412), (516, 355)],
    [(598, 392), (658, 382), (686, 436), (666, 505), (645, 588), (610, 650), (576, 573), (587, 492)],
    [(779, 238), (838, 182), (947, 172), (1012, 207), (1100, 194), (1190, 228), (1217, 284), (1164, 329), (1074, 332), (1007, 365), (935, 337), (853, 348)],
    [(877, 371), (960, 369), (995, 431), (975, 516), (928, 609), (875, 575), (850, 486), (827, 426)],
    [(1112, 564), (1180, 549), (1238, 590), (1220, 644), (1158, 658), (1096, 622)],
]
for poly in continents:
    d.polygon(poly, fill="#dddddd", outline=INK)

# Routes and pins.
line([(620, 313), (790, 245), (990, 244), (1164, 321)], fill=DARK, width=3, dash=(10, 8))
line([(620, 313), (808, 403), (958, 522), (1160, 614)], fill=DARK, width=3, dash=(10, 8))
line([(1164, 321), (1196, 430), (1182, 520), (1160, 614)], fill=DARK, width=3, dash=(10, 8))
pins = [(620, 313, "北美禁区带", True), (1164, 321, "东亚神秘地带", False), (1160, 614, "太平洋失航带", False)]
for px, py, name, active in pins:
    r = 18 if active else 15
    d.ellipse((px - r, py - r, px + r, py + r), fill=DARK if active else WHITE, outline=INK, width=3)
    if active:
        d.ellipse((px - 28, py - 28, px + 28, py + 28), outline=INK, width=2)
    label(name, px + 28 if name != "东亚神秘地带" else px - 28, py + 2, f=F18, anchor="lm" if name != "东亚神秘地带" else "rm")

label("点击卡片或地图针脚 → 同步右侧选区档案", 444, 768, f=F14, fill=MID, anchor="la")


def draw_receipt(x, y, title, value, symbol):
    box(x, y, 369, 207, fill=WHITE, outline=INK, width=3)
    # Top edge ownership tab.
    d.polygon([(x + 18, y), (x + 52, y - 12), (x + 90, y), (x + 146, y)], fill=WHITE, outline=INK)
    box(x + 28, y + 32, 64, 64, fill=LIGHT, outline=INK, width=2, radius=6)
    centered(symbol, (x + 28, y + 32, 64, 64), F30)
    label(title, x + 112, y + 48, f=F22, anchor="la")
    label(value, x + 112, y + 82, f=F16, fill=MID, anchor="la")
    for i in range(7):
        fill = DARK if i == 0 else WHITE
        box(x + 28 + i * 43, y + 126, 30, 30, fill=fill, outline=INK, width=2)
    label("只读世界回执 · 有真实载荷时才显示", x + 28, y + 182, f=F12, fill=MID, anchor="la")


draw_receipt(432, 837, "红线预警", "红线稿剩 7 天", "!")
draw_receipt(836, 837, "深链动向", "青线将推进缺口", "◎")
box(1220, 837, 130, 207, fill="#eeeeee", outline=MID, width=1)
centered("有意负空间\n不放第三张回执", (1220, 837, 130, 207), F14, MID)


# Right carrier. It owns the whole right column while A5.1 remains a frozen 480x780 module.
box(1398, 24, 480, 1032, fill="#eeeeee", outline=INK, width=3)
label("RIGHT CARRIER", 1414, 38, f=F12, fill=MID, anchor="la")

# Rear page and bottom folder remain quiet and non-interactive.
box(1408, 825, 460, 75, fill="#dddddd", outline=INK, width=2)
box(1398, 900, 480, 156, fill="#cfcfcf", outline=INK, width=3)
centered("NO TEXT / NO HIT\n纯承托，不是第二功能区", (1398, 900, 480, 156), F16, MID)

# Frozen A5.1 dossier shell.
box(1398, 45, 480, 780, fill=WHITE, outline=INK, width=4)
box(1434, 102, 54, 54, fill=WHITE, outline=INK, width=2, radius=27)
centered("◎", (1434, 102, 54, 54), F24)
box(1521, 108, 240, 51, fill=LIGHT, outline=INK, width=2)
centered("北美禁区带", (1521, 108, 240, 51), F22)
box(1767, 96, 87, 87, fill="#d0d0d0", outline=INK, width=2)
centered("红线\n升温", (1767, 96, 87, 87), F18)

box(1431, 192, 414, 264, fill=LIGHT, outline=INK, width=3)
hatch((1431, 192, 414, 264), spacing=36, fill="#aaaaaa")
centered("69:44 地区主照片", (1431, 192, 414, 264), F24, DARK)

box(1431, 477, 414, 135, fill=WHITE, outline=INK, width=2)
label("都市传说与军事封锁交叠。", 1450, 512, f=F20, anchor="la")
label("红线稿需在 7 天内处理。", 1450, 548, f=F20, anchor="la")
label("地区说明只负责‘为什么去’，不重复地图摘要。", 1450, 590, f=F13, fill=MID, anchor="la")

box(1425, 630, 426, 66, fill=WHITE, outline=INK, width=3)
label("任务情报", 1444, 663, f=F22, anchor="lm")
label("限时 1 · 线索 2 · 深链 1", 1792, 663, f=F16, fill=MID, anchor="rm")
label("＋", 1832, 663, f=F24, anchor="mm")
label("收起态", 1828, 642, f=F12, fill=MID, anchor="ra")

box(1425, 711, 426, 75, fill=DARK, outline=INK, width=3)
centered("进入地区任务台", (1425, 711, 426, 75), F28, WHITE)
label("当前选区主 CTA · 进入不耗天", 1425, 802, f=F12, fill=MID, anchor="la")


# Geometry labels are outside functional hit regions.
label("B2.12 × 3", 48, 804, f=F12, fill=MID, anchor="la")
label("MAP 924 × 696", 436, 102, f=F12, fill=MID, anchor="la")
label("A5.1 480 × 780", 1410, 54, f=F12, fill=MID, anchor="la")

img.save(OUTPUT, format="PNG", optimize=True)

audit = {
    "artifact_type": "structure_wireframe",
    "viewport": [W, H],
    "columns": columns,
    "region_cards": [
        [66, 36, 306, 240],
        [66, 294, 306, 240],
        [66, 552, 306, 240],
    ],
    "time_gate": [36, 810, 342, 246],
    "map_stage": [426, 96, 924, 696],
    "receipts": [[432, 837, 369, 207], [836, 837, 369, 207]],
    "right_carrier": [1398, 24, 480, 1032],
    "a51_dossier": [1398, 45, 480, 780],
    "a51_photo": [1431, 192, 414, 264],
    "a51_disclosure": [1425, 630, 426, 66],
    "a51_cta": [1425, 711, 426, 75],
    "states": {
        "time_gate": "default_to_confirming_on_first_click",
        "dossier": "collapsed",
    },
    "assertions": {
        "single_day_owner": True,
        "advance_day_present": True,
        "consequence_preview_present": True,
        "enter_region_present": True,
        "third_receipt_absent": True,
        "right_folder_noninteractive": True,
        "runtime_command_implemented": False,
    },
}
AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUTPUT)
print(AUDIT)
