from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/artboard_v3/rt-artboard-full.png"
OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-4-compact-status"

CANVAS = (1920, 1080)
INK = (32, 39, 35, 255)
PAPER = (249, 243, 229, 236)
PAPER_SOFT = (255, 251, 238, 224)
DARK = (7, 18, 30, 212)
CYAN = (28, 168, 178, 232)
TEAL = (20, 124, 132, 230)
GOLD = (214, 158, 61, 238)
RED = (219, 58, 37, 236)
VIOLET = (126, 92, 206, 232)
BLACK = (20, 25, 32, 236)
WHITE = (246, 242, 226, 255)
MUTED = (82, 91, 88, 255)
CONTENT = (31, 161, 172, 78)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["msyhbd.ttc" if bold else "msyh.ttc", "simhei.ttf", "NotoSansCJK-Regular.ttc"]
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


H1 = _font(32, True)
H2 = _font(24, True)
BODY = _font(18)
SMALL = _font(15)
TINY = _font(13)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
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


def _text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill=INK,
    width: int | None = None,
    line_gap: int = 4,
) -> int:
    x, y = xy
    for raw in text.split("\n"):
        lines = _wrap(draw, raw, font, width) if width else [raw]
        for line in lines:
            draw.text((x, y), line, font=font, fill=fill)
            y += int(font.size * 1.25) + line_gap
    return y


def _box(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int],
    label: str | None = None,
    width: int = 3,
    radius: int = 6,
) -> None:
    x, y, w, h = rect
    fill_arg = None if len(fill) == 4 and fill[3] == 0 else fill
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill_arg, outline=outline, width=width)
    if label:
        label_w = min(w - 20, max(180, int(draw.textbbox((0, 0), label, font=SMALL)[2] + 28)))
        draw.rounded_rectangle((x + 10, y + 10, x + 10 + label_w, y + 42), radius=5, fill=outline)
        _text(draw, (x + 24, y + 15), label, SMALL, WHITE)


def _badge(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str, color, font=TINY) -> None:
    x, y, w, h = rect
    draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=color, outline=(255, 248, 220, 140), width=1)
    _text(draw, (x + 10, y + 5), text, font, WHITE, w - 20)


def _draw_day_advance_button(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int] = (1168, 970, 176, 58)) -> None:
    x, y, w, h = rect
    _box(draw, (x, y, w, h), (18, 31, 42, 242), GOLD, None, width=3, radius=8)
    draw.rectangle((x + 8, y + 8, x + 18, y + h - 8), fill=(219, 58, 37, 218))
    draw.line((x + 24, y + h - 10, x + w - 54, y + h - 10), fill=(214, 158, 61, 180), width=2)
    draw.polygon(
        [(x + w - 44, y + 16), (x + w - 24, y + h // 2), (x + w - 44, y + h - 16)],
        fill=(214, 158, 61, 236),
    )
    _text(draw, (x + 30, y + 11), "推进一天", BODY, WHITE)
    _text(draw, (x + 32, y + 35), "DAY +1", TINY, (214, 158, 61, 255), w - 78)


def _base() -> Image.Image:
    base = Image.open(SOURCE).convert("RGBA").resize(CANVAS)
    veil = Image.new("RGBA", CANVAS, (5, 11, 18, 30))
    return Image.alpha_composite(base, veil)


def _task_card(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    title: str,
    meta: str,
    *,
    tone=TEAL,
    selected: bool = False,
    chain: str | None = None,
    queued: str | None = None,
    urgent: str | None = None,
) -> None:
    w, h = 358, 118
    outline = GOLD if selected else (45, 55, 50, 220)
    fill = PAPER_SOFT if not queued else (224, 231, 218, 218)
    _box(draw, (x, y, w, h), fill, outline, width=3 if selected else 2)
    draw.rectangle((x, y, x + 18, y + h), fill=tone)
    if selected:
        draw.rounded_rectangle((x + 10, y + 8, x + w - 10, y + h - 8), radius=4, outline=(214, 158, 61, 176), width=2)
    if chain:
        draw.rectangle((x + 24, y + 18, x + 32, y + h - 18), fill=VIOLET)
        _badge(draw, (x + w - 92, y + 16, 68, 26), chain, VIOLET)
    elif urgent:
        _badge(draw, (x + w - 92, y + 16, 68, 26), urgent, RED)
    else:
        draw.rectangle((x + w - 40, y, x + w - 18, y + 42), fill=tone)
    _text(draw, (x + 48, y + 22), title, BODY, INK, w - 150)
    _text(draw, (x + 48, y + 54), meta, SMALL, INK, w - 112)
    if queued:
        _badge(draw, (x + w - 112, y + h - 34, 88, 24), queued, BLACK, TINY)
    draw.line((x + 48, y + h - 22, x + w - 54, y + h - 22), fill=(110, 93, 65, 136), width=2)


def _draw_regions(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (112, 142, 430, 790), (10, 24, 38, 28), CYAN, "A 任务索引：候选 / 深链 / 执行中")
    _box(draw, (578, 102, 760, 790), (8, 21, 36, 0), GOLD, "B 地图：深链具体任务在这里点选")
    _box(draw, (1380, 112, 466, 820), (10, 24, 38, 28), CYAN, "C 任务详情 + 唯一主 CTA")
    _box(draw, (110, 962, 1236, 76), (10, 24, 38, 34), GOLD, "D 地区事件 / 回执 / 日程")


def _map_chain_task(draw: ImageDraw.ImageDraw, x: int, y: int, title: str, stage: str, *, active: bool) -> None:
    fill = PAPER if active else (23, 30, 36, 225)
    outline = GOLD if active else (180, 180, 170, 190)
    text_fill = INK if active else WHITE
    _box(draw, (x, y, 178, 54), fill, outline, None, width=2)
    _badge(draw, (x + 10, y + 10, 52, 22), stage, VIOLET if active else BLACK)
    _text(draw, (x + 72, y + 11), title, TINY, text_fill, 94)
    _text(draw, (x + 72, y + 32), "可点任务" if active else "未揭示", TINY, (92, 72, 30, 255) if active else (220, 222, 218, 255), 94)


def _draw_map_chain(draw: ImageDraw.ImageDraw, filled: bool = False) -> None:
    # Common pins, then chain task cards. The current chain task itself is clickable on the map.
    for px, py, tone in [(820, 288, RED), (780, 430, RED)]:
        draw.ellipse((px - 18, py - 18, px + 18, py + 18), fill=tone, outline=WHITE, width=2)
    current_pin = (1128, 524)
    next_pin = (1016, 692)
    draw.line((current_pin[0], current_pin[1], next_pin[0], next_pin[1]), fill=(126, 92, 206, 170), width=3)
    draw.ellipse((current_pin[0] - 20, current_pin[1] - 20, current_pin[0] + 20, current_pin[1] + 20), fill=CYAN, outline=WHITE, width=2)
    draw.ellipse((current_pin[0] - 38, current_pin[1] - 38, current_pin[0] + 38, current_pin[1] + 38), outline=GOLD, width=3)
    draw.ellipse((next_pin[0] - 18, next_pin[1] - 18, next_pin[0] + 18, next_pin[1] + 18), fill=BLACK, outline=WHITE, width=2)
    draw.ellipse((next_pin[0] - 34, next_pin[1] - 34, next_pin[0] + 34, next_pin[1] + 34), outline=(214, 158, 61, 180), width=2)
    if filled:
        _map_chain_task(draw, 1112, 448, "M330 空白段", "1/4", active=True)
        _map_chain_task(draw, 950, 712, "下一环 ?", "2/4", active=False)
    else:
        _map_chain_task(draw, 1112, 448, "当前环任务", "1/4", active=True)
        _map_chain_task(draw, 950, 712, "下一环 ?", "2/4", active=False)


def build_structure() -> Image.Image:
    img = _base()
    draw = ImageDraw.Draw(img, "RGBA")
    _text(draw, (70, 42), "地区任务台 v3.4 · compact status structure", H1, WHITE)
    _text(draw, (70, 86), "修正：普通槽删除；红/紫特殊状态压缩；推进一天升级为独立日程按钮。", BODY, WHITE)
    _draw_regions(draw)

    _task_card(draw, 150, 188, "51 区外围公路", "常驻 / 科学纪实 · 耗时 2天 · 探/生", tone=RED)
    _task_card(draw, 150, 334, "罗斯威尔档案残页", "常驻 / 科学纪实 · 耗时 1天 · 察/理", tone=(26, 110, 184, 235))
    _task_card(draw, 150, 480, "突发：雷达异常光点", "截稿 / 大众热度 · 剩 4天 · 探/生/察", tone=RED, urgent="截稿")
    _task_card(
        draw,
        150,
        626,
        "M330 未班车空白段",
        "深度调查链 · 当前可点任务在地图",
        tone=CYAN,
        selected=True,
        chain="续 1/4",
    )
    _box(draw, (150, 780, 350, 76), (21, 34, 42, 188), (86, 105, 111, 220), None, width=2)
    _text(draw, (168, 795), "已派遣 · 执行中：2 项", SMALL, WHITE)
    _text(draw, (168, 824), "到期 1 项 · 可展开查看 / 撤回", TINY, (214, 223, 221, 255))

    _draw_map_chain(draw, filled=False)
    _text(draw, (608, 820), "深链下具体任务在地图卡片上点选；左卡只同步 selected / chain / queued 状态。", SMALL, WHITE, 680)

    # Right detail slots. No unlabelled red blocks.
    _box(draw, (1426, 176, 372, 66), CONTENT, (20, 150, 160, 240), "标题槽")
    _box(draw, (1426, 276, 372, 240), CONTENT, (20, 150, 160, 240), "摘要 / 目标 / 需求")
    _box(draw, (1426, 544, 372, 64), CONTENT, VIOLET, "深度短槽")
    _box(draw, (1426, 630, 278, 76), CONTENT, (20, 150, 160, 240), "可带回 / 风险")
    _box(draw, (1426, 718, 372, 46), (245, 236, 203, 220), GOLD, None, width=2)
    _text(draw, (1440, 730), "阻断原因贴近 CTA：未选 / 天数不足 / 已派遣", TINY, INK, 340)
    _box(draw, (1426, 790, 356, 82), (198, 44, 28, 236), RED, "主 CTA：进入派遣签批")
    _text(draw, (1430, 892), "红色只保留给 CTA、截稿、危险；不再出现孤立红块。", TINY, WHITE, 360)

    # Compressed receipt and day advance.
    _box(draw, (180, 986, 430, 34), (244, 238, 222, 230), (38, 50, 48, 210), None, width=2)
    _text(draw, (194, 994), "探索周 余 4天 · 北美禁区 · 已选 M330", TINY, INK, 392)
    _box(draw, (634, 986, 350, 34), (244, 238, 222, 230), (38, 50, 48, 210), None, width=2)
    _text(draw, (648, 994), "地区事件：军方封锁 · 本区对手骰+1", TINY, INK, 318)
    _box(draw, (1008, 986, 146, 34), (244, 238, 222, 230), (38, 50, 48, 210), None, width=2)
    _text(draw, (1022, 994), "执行中 2 / 到期 1", TINY, INK, 120)
    _draw_day_advance_button(draw)

    return img


def build_filled_check() -> Image.Image:
    img = _base()
    draw = ImageDraw.Draw(img, "RGBA")
    _text(draw, (70, 42), "地区任务台 v3.4 · compact status fill", H1, WHITE)
    _text(draw, (70, 86), "真实内容填充：右侧正文变大；深度链身份压成短槽；底部推进一天独立成日程动作。", BODY, WHITE)
    _draw_regions(draw)

    _task_card(draw, 150, 188, "51 区外围公路", "白色调查 · 耗时 2天 · 探索4 / 生存2", tone=RED)
    _task_card(draw, 150, 334, "罗斯威尔档案残页", "线索调查 · 耗时 1天 · 探索3 / 洞察3", tone=(26, 110, 184, 235))
    _task_card(draw, 150, 480, "突发：雷达异常光点", "红色截稿 · 剩 4天 · 对手骰3", tone=RED, urgent="截稿")
    _task_card(
        draw,
        150,
        626,
        "M330 未班车空白段",
        "深度调查链 · 地图点选当前环 1/4",
        tone=CYAN,
        selected=True,
        chain="续 1/4",
    )
    _box(draw, (150, 780, 350, 76), (21, 34, 42, 188), (86, 105, 111, 220), None, width=2)
    _text(draw, (168, 795), "已派遣 · 执行中：51区、雷达异常", SMALL, WHITE, 316)
    _text(draw, (168, 824), "明日到期：雷达异常 · 可展开查看", TINY, (214, 223, 221, 255), 316)

    _text(draw, (614, 800), "深度链：左卡确认链状态；真正可点击的当前环任务放在地图链卡上。", SMALL, WHITE, 690)

    _box(draw, (1426, 176, 372, 66), PAPER, (38, 50, 48, 220), None, width=2)
    _text(draw, (1444, 194), "M330 未班车空白段", H2, INK, 332)
    _box(draw, (1426, 276, 372, 240), PAPER, (38, 50, 48, 220), None, width=2)
    _text(
        draw,
        (1444, 302),
        "一段车载录音缺了三秒，乘客口供互相矛盾，\n但都指向同一站。",
        SMALL,
        INK,
        328,
    )
    _text(draw, (1444, 408), "目标：找出缺失三秒对应的站点记录。", SMALL, INK, 328)
    _text(draw, (1444, 452), "需求：察 / 诡 / 理 · 耗时 2天", SMALL, (126, 94, 34, 255), 328)
    _box(draw, (1426, 544, 372, 64), (246, 241, 230, 236), VIOLET, None, width=2)
    _text(draw, (1444, 555), "深度调查 · 当前环 1/4", SMALL, (78, 54, 145, 255), 328)
    _text(draw, (1444, 583), "成功后揭示下一环；失败保留线索。", TINY, INK, 328)
    _box(draw, (1426, 630, 278, 76), PAPER, (38, 50, 48, 220), None, width=2)
    _text(draw, (1444, 646), "可带回：录音 / 证词\n风险：凶险，可能触发误导线索", TINY, INK, 246)
    _box(draw, (1426, 718, 372, 46), (245, 236, 203, 220), GOLD, None, width=2)
    _text(draw, (1440, 730), "签批不扣天数；派遣后预计占用 2 天。", TINY, INK, 340)
    _box(draw, (1426, 790, 356, 82), (198, 44, 28, 236), RED, None, width=2)
    _text(draw, (1472, 816), "进入派遣签批", H2, WHITE)

    _draw_map_chain(draw, filled=True)

    _box(draw, (180, 986, 430, 34), PAPER, (38, 50, 48, 210), None, width=2)
    _text(draw, (194, 994), "探索周 余 4天 · 北美禁区 · 已选 M330", TINY, INK, 392)
    _box(draw, (634, 986, 350, 34), PAPER, (38, 50, 48, 210), None, width=2)
    _text(draw, (648, 994), "地区事件：军方封锁 · 本区对手骰+1", TINY, INK, 318)
    _box(draw, (1008, 986, 146, 34), PAPER, (38, 50, 48, 210), None, width=2)
    _text(draw, (1022, 994), "执行中 2 / 到期 1", TINY, INK, 120)
    _draw_day_advance_button(draw)
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_structure().save(OUT_DIR / "01-region-task-v3-real-content-structure.png")
    build_filled_check().save(OUT_DIR / "02-region-task-v3-real-content-fill.png")
    print(OUT_DIR)
    print("01-region-task-v3-real-content-structure.png")
    print("02-region-task-v3-real-content-fill.png")


if __name__ == "__main__":
    main()
