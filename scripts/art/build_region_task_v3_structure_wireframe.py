from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/artboard_v3/rt-artboard-full.png"
OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-structure-wireframe"


CANVAS = (1920, 1080)
INK = (32, 39, 35, 255)
PAPER = (247, 240, 224, 236)
PAPER_2 = (255, 251, 237, 228)
NAVY = (8, 21, 36, 230)
CYAN = (25, 166, 177, 235)
RED = (219, 58, 37, 238)
GOLD = (214, 158, 61, 238)
MUTED = (82, 91, 88, 255)
WHITE = (246, 242, 226, 255)
NO_TEXT = (219, 58, 37, 52)
CONTENT = (31, 161, 172, 88)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        "msyhbd.ttc" if bold else "msyh.ttc",
        "simhei.ttf",
        "NotoSansCJK-Regular.ttc",
    ]
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_H1 = _font(32, True)
FONT_H2 = _font(24, True)
FONT_BODY = _font(18, False)
FONT_SMALL = _font(15, False)
FONT_TINY = _font(13, False)


def _fit_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    rows: list[str] = []
    current = ""
    for ch in text:
        candidate = current + ch
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            if current:
                rows.append(current)
            current = ch
    if current:
        rows.append(current)
    return rows


def _text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill=INK, width: int | None = None, line_gap: int = 5) -> int:
    x, y = xy
    lines = text.split("\n")
    for raw in lines:
        wrapped = [raw]
        if width is not None:
            wrapped = _fit_text(draw, raw, font, width)
        for line in wrapped:
            draw.text((x, y), line, font=font, fill=fill)
            y += int(font.size * 1.25) + line_gap
    return y


def _box(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int],
    label: str | None = None,
    label_fill=WHITE,
    width: int = 3,
) -> None:
    x, y, w, h = rect
    fill_arg = None if len(fill) == 4 and fill[3] == 0 else fill
    draw.rounded_rectangle((x, y, x + w, y + h), radius=6, fill=fill_arg, outline=outline, width=width)
    if label:
        draw.rounded_rectangle((x + 10, y + 10, x + min(w - 10, 380), y + 40), radius=5, fill=outline)
        _text(draw, (x + 22, y + 13), label, FONT_SMALL, label_fill)


def _ghost_base() -> Image.Image:
    base = Image.open(SOURCE).convert("RGBA").resize(CANVAS)
    veil = Image.new("RGBA", CANVAS, (7, 13, 22, 38))
    return Image.alpha_composite(base, veil)


def _draw_card(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str, meta: str, color: tuple[int, int, int, int]) -> None:
    _box(draw, (x, y, w, h), PAPER_2, (35, 46, 42, 210), None, width=2)
    draw.rectangle((x, y, x + 18, y + h), fill=color)
    draw.rectangle((x + w - 42, y, x + w - 18, y + 44), fill=color)
    _text(draw, (x + 42, y + 20), title, FONT_BODY, INK, w - 94)
    _text(draw, (x + 42, y + 52), meta, FONT_SMALL, INK, w - 94)
    draw.line((x + 42, y + h - 26, x + w - 54, y + h - 26), fill=(120, 100, 70, 150), width=2)


def build_structure() -> Image.Image:
    img = _ghost_base()
    draw = ImageDraw.Draw(img, "RGBA")

    _text(draw, (70, 44), "地区任务台 v3 · structure_wireframe", FONT_H1, WHITE)
    _text(draw, (70, 88), "目标：保留当前整屏美术和中央地图，把左任务卡、右详情纸改成正交可写区；先验证信息容量，再重出美术资源。", FONT_BODY, WHITE)

    # Main zones
    _box(draw, (112, 142, 430, 704), (10, 24, 38, 28), CYAN, "A 左侧任务索引 / Candidate Tasks")
    _box(draw, (578, 102, 760, 742), (8, 21, 36, 0), GOLD, "B 中央地图 / 保留视觉主舞台")
    _box(draw, (1380, 112, 466, 836), (10, 24, 38, 28), CYAN, "C 右侧任务详情 / Task Dossier")
    _box(draw, (106, 902, 1240, 118), (10, 24, 38, 28), GOLD, "D 底部本周行动回条 / Low-priority Receipt")

    # Left cards, straight content.
    left_cards = [
        ("51 区外围公路", "常驻/科学纪实 · 2天 · 探/生 · 凶险", RED),
        ("罗斯威尔档案残页", "常驻/科学纪实 · 1天 · 察/理 · 凶险", (26, 110, 184, 235)),
        ("突发：雷达异常光点", "截稿/大众热度 · 2天 · 探/生/察 · 凶险", CYAN),
        ("M330 未班车空白段", "追踪/神秘玄学 · 2天 · 察/诡/理 · 凶险", RED),
    ]
    for i, item in enumerate(left_cards):
        _draw_card(draw, 150, 188 + i * 156, 350, 116, item[0], item[1], item[2])
    _text(draw, (150, 815), "验证：4 张首屏任务卡；每张只放 1 行标题 + 1-2 行 meta。\n色签/书签是状态，不压正文。", FONT_SMALL, WHITE, 360)

    # Center map annotations.
    for px, py, tone in [(820, 288, RED), (780, 430, RED), (1128, 524, CYAN), (1016, 692, (40, 44, 50, 235))]:
        draw.ellipse((px - 18, py - 18, px + 18, py + 18), fill=tone, outline=WHITE, width=2)
        draw.ellipse((px - 34, py - 34, px + 34, py + 34), outline=(255, 221, 96, 200), width=3)
    _text(draw, (608, 790), "地图不重画：保留底图、网格、路线质感。\npin 热区 / selected 圈 / hover 短签后续独立状态层。", FONT_SMALL, WHITE, 690)

    # Right detail straight fields.
    _box(draw, (1426, 176, 372, 66), CONTENT, (20, 150, 160, 240), "标题槽 content_rect")
    _box(draw, (1426, 302, 372, 206), CONTENT, (20, 150, 160, 240), "正文槽 2-5 行")
    _box(draw, (1426, 548, 278, 112), CONTENT, (20, 150, 160, 240), "meta / 状态槽")
    _box(draw, (1426, 780, 356, 82), CONTENT, RED, "主 CTA 独立动作")
    draw.rectangle((1728, 536, 1806, 720), fill=NO_TEXT, outline=RED, width=2)
    _text(draw, (1426, 888), "红色托盘保留为动作承载物；label/disabled/pressed 不烘焙。", FONT_TINY, WHITE, 360)

    # Bottom strip slots.
    _box(draw, (180, 942, 250, 52), CONTENT, (20, 150, 160, 240), None, width=2)
    _box(draw, (460, 942, 490, 52), CONTENT, (20, 150, 160, 240), None, width=2)
    _box(draw, (982, 942, 288, 52), CONTENT, (20, 150, 160, 240), None, width=2)
    draw.rectangle((1268, 902, 1346, 1020), fill=NO_TEXT, outline=RED, width=2)
    _text(draw, (194, 954), "剩余 4 天 / 北美禁区", FONT_TINY, INK, 224)
    _text(draw, (474, 954), "当前短回执：已选 M330，进入签批不消耗天数", FONT_TINY, INK, 454)
    _text(draw, (996, 954), "阻断/提醒：需先选任务", FONT_TINY, INK, 252)
    _text(draw, (178, 1004), "底部长条 = 低权重“本周行动回条”。不放完整详情，不放第二个 CTA，不抢右侧主操作。", FONT_SMALL, WHITE, 1060)

    # Straightening notes.
    _box(draw, (608, 846, 700, 48), (247, 240, 224, 208), (214, 158, 61, 238), None)
    _text(draw, (628, 860), "变正原则：外层纸叠、夹具、阴影可斜；动态文字所在的内框必须正交。下一步只校正左卡/右纸 content_rect，不重画地图。", FONT_TINY, INK, 660)
    return img


def build_filled_check() -> Image.Image:
    img = _ghost_base()
    draw = ImageDraw.Draw(img, "RGBA")

    _text(draw, (70, 44), "地区任务台 v3 · filled capacity check", FONT_H1, WHITE)
    _text(draw, (70, 88), "用接近真实字段填充，检查正交纸面是否装得下；这是结构验证稿，不是最终美术。", FONT_BODY, WHITE)

    _box(draw, (112, 142, 430, 704), (10, 24, 38, 28), CYAN, "任务索引填充效果")
    for i, item in enumerate([
        ("51 区外围公路", "线索 · 常驻 · 2天", "科学纪实 / 探索 / 生存", "凶险"),
        ("罗斯威尔档案残页", "线索 · 常驻 · 1天", "科学纪实 / 察理", "凶险"),
        ("雷达异常光点", "截稿 · 突发 · 2天", "大众热度 / 探索 / 监察", "4天"),
        ("M330 未班车空白段", "追踪 · 深链 · 2天", "神秘玄学 / 诡秘 / 理性", "已选"),
    ]):
        y = 188 + i * 156
        _box(draw, (150, y, 350, 116), PAPER_2, (45, 55, 50, 220), None, width=2)
        color = RED if i in [0, 2, 3] else (26, 110, 184, 235)
        draw.rectangle((150, y, 168, y + 116), fill=color)
        draw.rectangle((458, y, 482, y + 44), fill=color)
        _text(draw, (190, y + 16), item[0], FONT_BODY, INK, 250)
        _text(draw, (190, y + 48), item[1], FONT_SMALL, INK, 250)
        _text(draw, (190, y + 74), item[2], FONT_TINY, MUTED, 250)
        draw.rounded_rectangle((405, y + 72, 456, y + 98), radius=4, fill=(255, 245, 205, 220), outline=color)
        _text(draw, (413, y + 76), item[3], FONT_TINY, INK)

    _box(draw, (578, 102, 760, 742), (8, 21, 36, 0), GOLD, "地图保留 + 热区")
    _text(draw, (610, 778), "热区示例：点击 pin 或左卡都更新同一个 selected_task_id。", FONT_SMALL, WHITE, 700)

    _box(draw, (1380, 112, 466, 836), (10, 24, 38, 28), CYAN, "右侧详情填充效果")
    _box(draw, (1426, 176, 372, 66), PAPER, (30, 42, 38, 215), None, width=2)
    _text(draw, (1444, 194), "M330 未班车空白段", FONT_H2, INK, 330)
    _box(draw, (1426, 302, 372, 206), PAPER, (30, 42, 38, 215), None, width=2)
    _text(draw, (1444, 328), "一段车载录音缺了三秒，乘客口供互相矛盾，\n但都指向同一站。", FONT_SMALL, INK, 330)
    _text(draw, (1444, 392), "需求：察 / 诡 / 理  ·  耗时 2 天", FONT_SMALL, (126, 94, 34, 255), 330)
    _text(draw, (1444, 426), "连续追踪：成功后出现后续线索", FONT_SMALL, (2, 120, 130, 255), 330)
    _box(draw, (1426, 548, 278, 112), PAPER, (30, 42, 38, 215), None, width=2)
    _text(draw, (1444, 568), "预期素材：录音 / 证词\n风险：凶险，可能触发误导线索\n状态：可进入派遣", FONT_TINY, INK, 246)
    _box(draw, (1426, 780, 356, 82), (198, 44, 28, 236), RED, None, width=2)
    _text(draw, (1472, 806), "进入派遣签批", FONT_H2, WHITE)
    _text(draw, (1426, 884), "若未选任务：CTA disabled，label 改“先选择任务”。", FONT_TINY, WHITE, 360)

    _box(draw, (106, 902, 1240, 118), (10, 24, 38, 28), GOLD, "底部回条填充效果")
    for rect, text in [
        ((180, 942, 250, 52), "探索周 · 剩余 4 天\n当前：北美禁区"),
        ((460, 942, 490, 52), "短回执：M330 已选中，送至签批台不消耗天数"),
        ((982, 942, 288, 52), "提示：签批后再扣除 2 天"),
    ]:
        _box(draw, rect, PAPER, (30, 42, 38, 215), None, width=2)
        _text(draw, (rect[0] + 12, rect[1] + 9), text, FONT_TINY, INK, rect[2] - 24)
    _text(draw, (180, 1004), "结论：底部只做 1-2 行回执/周状态。完整任务描述、风险详情、员工、骰池都不能放这里。", FONT_SMALL, WHITE, 1040)
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_structure().save(OUT_DIR / "01-region-task-v3-structure-wireframe.png")
    build_filled_check().save(OUT_DIR / "02-region-task-v3-filled-capacity-check.png")
    print(OUT_DIR)
    print("01-region-task-v3-structure-wireframe.png")
    print("02-region-task-v3-filled-capacity-check.png")


if __name__ == "__main__":
    main()
