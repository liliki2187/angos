from __future__ import annotations

from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

import build_dice_glb_v0_14_assets as v014


REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "design" / "art-direction" / "dice-style" / "dice-external-reference-to-angus-v0-16-design-board.png"
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")

W, H = 2400, 1650


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    raw = hex_color.lstrip("#")
    return (int(raw[:2], 16), int(raw[2:4], 16), int(raw[4:6], 16), alpha)


def multiline(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fill: str,
    fnt: ImageFont.ImageFont,
    width: int,
    line_gap: int = 8,
) -> int:
    x, y = xy
    # Chinese text has no spaces; wrap by rough visual length.
    chars_per_line = max(8, width // max(16, int(getattr(fnt, "size", 20) * 0.9)))
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        lines.extend(textwrap.wrap(paragraph, chars_per_line, break_long_words=True, replace_whitespace=False))
    for line in lines:
        draw.text((x, y), line, fill=fill, font=fnt)
        y += int(getattr(fnt, "size", 20) * 1.2) + line_gap
    return y


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, subtitle: str = "") -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill="#111b22", outline="#2e4854", width=2)
    draw.text((x0 + 22, y0 + 18), title, fill="#f4d989", font=font(28, True))
    if subtitle:
        draw.text((x0 + 22, y0 + 56), subtitle, fill="#9eb5bf", font=font(17))


def draw_face(
    img: Image.Image,
    box: tuple[int, int, int, int],
    body: str,
    accent: str,
    text: str = "",
    icon: str = "",
    small: str = "",
    title: str = "",
    title_on_face: bool = False,
    bevel: bool = True,
    glow: bool = False,
) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    radius = 24
    draw.rounded_rectangle(box, radius=radius, fill=body, outline=rgba(accent, 190), width=4)
    if bevel:
        draw.line((x0 + 16, y0 + 8, x1 - 16, y0 + 8), fill=rgba("#ffffff", 80), width=3)
        draw.line((x0 + 8, y0 + 16, x0 + 8, y1 - 16), fill=rgba("#ffffff", 34), width=3)
        draw.line((x0 + 18, y1 - 9, x1 - 18, y1 - 9), fill=rgba("#000000", 86), width=4)
        draw.line((x1 - 9, y0 + 18, x1 - 9, y1 - 18), fill=rgba("#000000", 76), width=3)
        for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            cx = x1 - 28 if sx > 0 else x0 + 28
            cy = y1 - 28 if sy > 0 else y0 + 28
            draw.line((cx - sx * 20, cy, cx, cy - sy * 20), fill=rgba(accent, 148), width=3)
    draw.polygon(
        [(x0 + 20, y0 + int(h * 0.60)), (x1 - 24, y0 + int(h * 0.42)), (x1 - 20, y1 - 44), (x0 + 24, y1 - 24)],
        fill=rgba("#000000", 34),
    )
    draw.polygon(
        [(x0 + 24, y0 + int(h * 0.30)), (x1 - 28, y0 + int(h * 0.26)), (x1 - 28, y0 + int(h * 0.48)), (x0 + 28, y0 + int(h * 0.54))],
        fill=rgba("#ffffff", 16),
    )
    if glow:
        draw.rounded_rectangle((x0 + 24, y0 + 24, x1 - 24, y1 - 24), radius=20, outline=rgba(accent, 88), width=8)
    if title_on_face and title:
        v014.draw_centered_text(draw, (x0 + 22, y0 + 28, x1 - 22, y0 + 96), title, font(48, True), "#f8eab8", "#071014", 3)
    if text:
        v014.draw_centered_text(draw, (x0 + 28, y0 + 54, x1 - 28, y1 - 56), text, font(70, True), "#f8eab8", "#071014", 4)
    if small:
        v014.draw_centered_text(draw, (x0 + 18, y1 - 74, x1 - 18, y1 - 22), small, font(27, True), accent, "#071014", 2)
    if icon:
        draw_symbol(draw, icon, (x0 + x1) // 2, (y0 + y1) // 2 + 16, min(w, h) // 3, accent, 190)


def draw_symbol(
    draw: ImageDraw.ImageDraw,
    name: str,
    cx: int,
    cy: int,
    size: int,
    color: str,
    alpha: int = 210,
) -> None:
    col = rgba(color, alpha)
    if name == "claw":
        for i in [-1, 0, 1]:
            draw.ellipse((cx + i * 25 - 12, cy - 48, cx + i * 25 + 12, cy + 18), fill=col)
        draw.ellipse((cx - 52, cy - 2, cx + 52, cy + 64), fill=col)
    elif name == "heart":
        draw.ellipse((cx - 45, cy - 38, cx + 2, cy + 8), fill=col)
        draw.ellipse((cx - 2, cy - 38, cx + 45, cy + 8), fill=col)
        draw.polygon([(cx - 50, cy - 12), (cx + 50, cy - 12), (cx, cy + 64)], fill=col)
    elif name == "bolt":
        draw.polygon([(cx + 2, cy - 70), (cx - 44, cy + 4), (cx - 4, cy + 4), (cx - 22, cy + 70), (cx + 48, cy - 18), (cx + 6, cy - 18)], fill=col)
    elif name == "coin":
        draw.ellipse((cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), fill=rgba("#e1b443", alpha), outline=rgba("#fff2b7", alpha), width=5)
        v014.draw_centered_text(draw, (cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), "3", font(48, True), "#fff6c8", "#6d4110", 3)
    elif name == "head":
        v014.draw_head(draw, cx, cy, size, col)
    elif name == "ghost":
        v014.draw_ghost(draw, cx, cy, size, col)
    elif name == "die":
        draw.rounded_rectangle((cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), radius=18, fill=rgba("#f4f5e7", alpha), outline=rgba("#0e1216", alpha), width=4)
        for dx, dy in [(-26, -26), (0, 0), (26, 26)]:
            draw.ellipse((cx + dx - 7, cy + dy - 7, cx + dx + 7, cy + dy + 7), fill=rgba("#101820", 255))
    elif name == "sword":
        draw.polygon([(cx - 10, cy + 50), (cx + 10, cy + 50), (cx + 8, cy - 42), (cx, cy - 72), (cx - 8, cy - 42)], fill=col)
        draw.rectangle((cx - 38, cy + 30, cx + 38, cy + 42), fill=col)
    elif name == "corner_head":
        v014.draw_head(draw, cx, cy, size, col)
    else:
        draw.ellipse((cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), outline=col, width=5)


def draw_external_reference_card(
    img: Image.Image,
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    lesson: str,
    faces: list[dict[str, str]],
) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    panel(draw, (x, y, x + w, y + h), title)
    fx = x + 26
    fy = y + 80
    size = 96
    gap = 16
    for i, face in enumerate(faces):
        bx = fx + i * (size + gap)
        draw_face(
            img,
            (bx, fy, bx + size, fy + size),
            face.get("body", "#141414"),
            face.get("accent", "#8ff042"),
            text=face.get("text", ""),
            icon=face.get("icon", ""),
            small=face.get("small", ""),
            bevel=True,
        )
    multiline(draw, (x + 26, y + 204), lesson, "#c9d6db", font(19), w - 52, 6)


def draw_angus_option(
    img: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    subtitle: str,
    kind: str,
    face_style: str,
    recommended: bool = False,
) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    fill = "#111c22" if not recommended else "#142126"
    outline = "#345260" if not recommended else "#e6bd5f"
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=3 if recommended else 2)
    draw.text((x0 + 22, y0 + 18), title, fill="#f4d989" if recommended else "#d7c79a", font=font(25, True))
    draw.text((x0 + 22, y0 + 52), subtitle, fill="#aebec6", font=font(17))
    fx0 = x0 + 42
    fy0 = y0 + 96
    size = 190
    if kind == "reason":
        body = "#1d7883"
        accent = "#aee7e7"
        icon = "head"
        value = "+2"
    else:
        body = "#151519"
        accent = "#ff6240"
        icon = "ghost"
        value = "!"
    draw_face(img, (fx0, fy0, fx0 + size, fy0 + size), body, accent, text="" if face_style == "full" else value, bevel=True)
    if face_style == "corner":
        draw.rounded_rectangle((fx0 + 18, fy0 + size - 64, fx0 + 78, fy0 + size - 16), radius=12, fill=rgba(body, 180), outline=rgba(accent, 180), width=3)
        draw_symbol(draw, icon, fx0 + 48, fy0 + size - 40, 35, accent, 210)
    elif face_style == "edge":
        draw_symbol(draw, icon, fx0 + size - 44, fy0 + size - 56, 96, accent, 78)
    elif face_style == "external":
        draw.line((fx0 + 26, fy0 + size - 42, fx0 + size - 26, fy0 + size - 42), fill=rgba(accent, 96), width=3)
        draw.text((fx0 + 48, fy0 + size - 34), "图标移至侧面/槽位", fill=rgba(accent, 150), font=font(15))
    elif face_style == "full":
        v014.draw_centered_text(draw, (fx0 + 20, fy0 + 16, fx0 + size - 20, fy0 + 70), "理性", font(38, True), "#f8eab8", "#071014", 3)
        v014.draw_centered_text(draw, (fx0 + 28, fy0 + 74, fx0 + size - 28, fy0 + 145), "+2", font(48, True), "#f8eab8", "#071014", 4)
        draw_symbol(draw, icon, fx0 + size // 2, fy0 + 156, 50, accent, 130)
    multiline(draw, (fx0 + size + 28, fy0 + 8), option_text(face_style, kind), "#d0dde2", font(19), x1 - (fx0 + size + 48), 6)


def option_text(style: str, kind: str) -> str:
    if style == "corner":
        return "常态推荐：大数字居中，图标变成角落小章。属性名从骰面移到角色槽/骰槽标签。"
    if style == "edge":
        return "风格推荐：图标半露在边角，像材质刻印。运动中不压读数，但要控制透明度。"
    if style == "external":
        return "最清晰：顶面只读规则。图标放侧面、槽位、hover 或结算放大态。"
    if style == "full":
        return "只用于停住放大、hover、结算截图或教程。不要作为常态小尺寸骰面。"
    return ""


def draw_current_problem(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    panel(draw, (80, 690, 2320, 900), "Angus 当前问题：一个小面承担了三个主读数", "文字、数字、图标都想当主角，结果在斜俯视和运动中互相挤压")
    cx, cy = 190, 754
    draw_face(img, (cx, cy, cx + 150, cy + 150), "#1d7883", "#aee7e7", text="+2", bevel=True, title="理性", title_on_face=True)
    draw_symbol(draw, "head", cx + 78, cy + 124, 45, "#aee7e7", 110)
    draw.line((cx - 10, cy - 8, cx + 160, cy + 160), fill=rgba("#ff6240", 210), width=8)
    draw.line((cx + 160, cy - 8, cx - 10, cy + 160), fill=rgba("#ff6240", 210), width=8)
    text = (
        "外部案例的共同解法不是继续缩字，而是拆分职责：\n"
        "骰面只放“本次结果值 / 主要符号”；属性名、技能解释、任务语义交给角色框、槽位、卡牌或 hover。"
    )
    multiline(draw, (390, 748), text, "#d9e5e8", font(27, True), 1120, 8)
    contract = [
        ("顶面", "大 +2 / !"),
        ("颜色", "属性阵营"),
        ("角落/边缘", "小图标"),
        ("槽位标签", "理性 / 探索 / 诡思"),
        ("hover/结算", "完整解释"),
    ]
    x = 1590
    for i, (k, v) in enumerate(contract):
        y = 738 + i * 32
        draw.text((x, y), k, fill="#f0d385", font=font(21, True))
        draw.text((x + 118, y), v, fill="#c8d8dd", font=font(21))


def main() -> None:
    img = Image.new("RGB", (W, H), "#07101c")
    draw = ImageDraw.Draw(img, "RGBA")

    # Subtle grid.
    for x in range(0, W, 40):
        draw.line((x, 0, x, H), fill=rgba("#153040", 34), width=1)
    for y in range(0, H, 40):
        draw.line((0, y, W, y), fill=rgba("#153040", 34), width=1)

    draw.text((80, 44), "骰面设计大图：外部经验 → Angus 可落地方案", fill="#f6d982", font=font(48, True))
    draw.text(
        (80, 108),
        "抽象重绘外部骰面规律，不拼贴外部原图；用于决定信息层级和后续 GLB/Godot 动态验证方向。",
        fill="#b8c9d0",
        font=font(23),
    )

    refs = [
        (
            "King of Tokyo",
            "单面只放一个大符号或数字。优点是运动中极清楚；代价是所有语义必须由规则/玩家记忆承担。",
            [
                {"body": "#101112", "accent": "#58f141", "icon": "claw"},
                {"body": "#101112", "accent": "#58f141", "icon": "heart"},
                {"body": "#101112", "accent": "#58f141", "text": "3"},
            ],
        ),
        (
            "Dice Forge",
            "骰面像可替换 tile：有实体边框和资源图标，但每格信息仍很少。适合学“可替换资产单元”。",
            [
                {"body": "#ece2c6", "accent": "#d8472f", "icon": "coin"},
                {"body": "#ece2c6", "accent": "#577ee8", "text": "2"},
                {"body": "#ece2c6", "accent": "#e3ad3f", "text": "1"},
            ],
        ),
        (
            "Too Many Bones",
            "高信息骰面成立的前提是角色垫/技能表解释它。骰面可以有小数字和图标，但不承担完整说明。",
            [
                {"body": "#d83d31", "accent": "#f8dc62", "text": "2", "small": "x"},
                {"body": "#e8c23b", "accent": "#1b2025", "text": "3"},
                {"body": "#3285d6", "accent": "#e8f3ff", "icon": "sword"},
            ],
        ),
        (
            "Dice Throne",
            "英雄骰通常是数字 + 英雄符号；角色身份在角色板上，骰面不再写一行说明文字。",
            [
                {"body": "#214cab", "accent": "#f4f6ff", "text": "6"},
                {"body": "#214cab", "accent": "#f4f6ff", "text": "2"},
                {"body": "#214cab", "accent": "#f4f6ff", "icon": "sword"},
            ],
        ),
        (
            "Dicey Dungeons",
            "骰子是输入值；能力名、条件和效果写在卡槽上。极适合借鉴“规则语义外置”。",
            [
                {"body": "#f2f3e9", "accent": "#111820", "icon": "die"},
                {"body": "#f2f3e9", "accent": "#111820", "text": "4"},
                {"body": "#f2f3e9", "accent": "#111820", "text": "6"},
            ],
        ),
        (
            "Sleeper / Slice & Dice",
            "骰子数值被分配到行动槽/角色槽。骰面保持简单，系统意义由 UI 容器解释。",
            [
                {"body": "#f1d54a", "accent": "#111820", "text": "5"},
                {"body": "#111820", "accent": "#f1d54a", "text": "2"},
                {"body": "#242a35", "accent": "#79f3df", "icon": "die"},
            ],
        ),
    ]
    card_w = 360
    card_h = 320
    for i, ref in enumerate(refs):
        x = 80 + i * (card_w + 24)
        draw_external_reference_card(img, x, 170, card_w, card_h, ref[0], ref[1], ref[2])

    draw_current_problem(img)

    draw.text((80, 960), "我建议的 Angus 骰面方案", fill="#f6d982", font=font(40, True))
    draw.text((80, 1010), "核心变化：常态骰面不再写“理性/探索/诡思”，属性名交给角色框或骰槽；骰面只保证结果值、状态符号和材质身份。", fill="#b8c9d0", font=font(23))

    option_boxes = [
        (80, 1070, 650, 1356, "方案 A：常态生产版", "大数字 + 角落小章", "reason", "corner", True),
        (690, 1070, 1260, 1356, "方案 B：风格加强版", "大数字 + 边角半露图标", "reason", "edge", False),
        (1300, 1070, 1870, 1356, "方案 C：极清晰版", "顶面只留结果，图标外置", "reason", "external", False),
        (80, 1390, 650, 1620, "黑骰常态", "大 ! + 角落鬼迹小章", "ghost", "corner", True),
        (690, 1390, 1260, 1620, "黑骰风格版", "大 ! + 边角半露鬼影", "ghost", "edge", False),
        (1300, 1390, 1870, 1620, "放大/hover/结算态", "才显示完整 理性 +2 + 图标", "reason", "full", False),
    ]
    for box in option_boxes:
        draw_angus_option(img, box[:4], box[4], box[5], box[6], box[7], box[8])

    panel(draw, (1910, 1070, 2320, 1620), "落地合同", "给下一步 GLB/Godot 的硬规则")
    rules = [
        "1. 常态小尺寸顶面不写属性名。",
        "2. `+2 / !` 是第一视觉中心。",
        "3. 图标只能做角落小章、边角半露、侧面或 hover。",
        "4. 属性名写在角色框 / 骰槽标签。",
        "5. 运动 GIF 必须检查 52/72/96px 三档。",
        "6. 放大态可恢复完整图文，但不作为常态。",
    ]
    y = 1152
    for rule in rules:
        y = multiline(draw, (1936, y), rule, "#d5e0e4", font(21), 340, 5) + 8
    draw.text((1936, 1538), "推荐先落地：方案 A + 黑骰常态", fill="#f4d989", font=font(24, True))
    draw.text((1936, 1574), "备选做风格测试：方案 B", fill="#95dfe5", font=font(21, True))

    draw.text(
        (80, H - 34),
        "Sources used as reference patterns: King of Tokyo, Dice Forge, Too Many Bones, Dice Throne, Dicey Dungeons, Citizen Sleeper, Slice & Dice. See accompanying report for URLs.",
        fill="#728994",
        font=font(15),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
