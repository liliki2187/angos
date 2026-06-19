from __future__ import annotations

from pathlib import Path

from PIL import ImageDraw

from build_region_task_v3_structure_wireframe_v2 import (
    BLACK,
    BODY,
    CONTENT,
    CYAN,
    GOLD,
    H1,
    H2,
    INK,
    MUTED,
    PAPER,
    RED,
    ROOT,
    SMALL,
    TEAL,
    TINY,
    VIOLET,
    WHITE,
    _badge,
    _base,
    _box,
    _draw_day_advance_button,
    _task_card,
    _text,
)


OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-4-compact-status"


def _draw_non_chain_regions(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (112, 142, 430, 790), (10, 24, 38, 28), CYAN, "A 任务索引：候选 / 选中 / 执行中")
    _box(draw, (578, 102, 760, 790), (8, 21, 36, 0), GOLD, "B 地图：任务 pin / selected 短签")
    _box(draw, (1380, 112, 466, 820), (10, 24, 38, 28), CYAN, "C 任务详情 + 唯一主 CTA")
    _box(draw, (110, 962, 1236, 76), (10, 24, 38, 34), GOLD, "D 地区事件 / 回执 / 日程")


TASKS = {
    "normal": {
        "title": "51 区外围公路",
        "meta": "白色调查 · 耗时 2天 · 探索4 / 生存2",
        "pin": (820, 288),
        "tone": RED,
        "summary": "夜班货车司机称，公路尽头的警示牌每晚都会换字。",
        "need": "需求：探索4 / 生存2 · 对手骰2",
        "cta": "进入派遣签批",
        "footer": "探索周 余 4天 · 北美禁区 · 已选 51区",
    },
    "deadline": {
        "title": "突发：雷达异常光点",
        "meta": "红色截稿 · 剩 4天 · 探索5 / 生存3",
        "pin": (780, 430),
        "tone": RED,
        "right_slot": ("红色截稿 · 剩 4天", "过期关闭；成功或失败都会消耗本窗口。"),
        "summary": "城市雷达站刚记录到异常光点，热度正在快速升高。",
        "need": "需求：探索5 / 生存3 · 对手骰3",
        "cta": "抢占截稿窗口",
        "footer": "探索周 余 4天 · 北美禁区 · 已选 雷达异常",
    },
    "lead": {
        "title": "罗斯威尔档案残页",
        "meta": "线索调查 · 耗时 1天 · 探索3 / 洞察3",
        "pin": (840, 590),
        "tone": (26, 110, 184, 235),
        "right_slot": ("线索调查", "成功后生成新任务；本身不是深度链当前环。"),
        "summary": "一页编号残缺的档案被塞进周刊信箱，背面有半个坐标。",
        "need": "需求：探索3 / 洞察3 · 耗时1天",
        "cta": "派遣线索调查",
        "footer": "探索周 余 4天 · 北美禁区 · 已选 罗斯威尔",
    },
}


def _draw_common_left(draw: ImageDraw.ImageDraw, selected: str) -> None:
    _task_card(
        draw,
        150,
        188,
        "51 区外围公路",
        "白色调查 · 耗时 2天 · 探索4 / 生存2",
        tone=RED,
        selected=selected == "normal",
    )
    _task_card(
        draw,
        150,
        334,
        "罗斯威尔档案残页",
        "线索调查 · 耗时 1天 · 调查后生成任务",
        tone=(26, 110, 184, 235),
        selected=selected == "lead",
    )
    _task_card(
        draw,
        150,
        480,
        "突发：雷达异常光点",
        "红色截稿 · 剩 4天 · 对手骰3",
        tone=RED,
        urgent="截稿",
        selected=selected == "deadline",
    )
    _task_card(
        draw,
        150,
        626,
        "M330 未班车空白段",
        "深度调查链 · 地图点选当前环 1/4",
        tone=CYAN,
        chain="续 1/4",
    )
    _box(draw, (150, 780, 350, 76), (21, 34, 42, 188), (86, 105, 111, 220), None, width=2)
    _text(draw, (168, 795), "已派遣 · 执行中：2 项", SMALL, WHITE, 316)
    _text(draw, (168, 824), "明日到期：雷达异常 · 可展开查看", TINY, (214, 223, 221, 255), 316)


def _draw_non_chain_map(draw: ImageDraw.ImageDraw, selected: str) -> None:
    positions = {
        "normal": (820, 288, RED, "51区"),
        "deadline": (780, 430, RED, "截稿"),
        "lead": (840, 590, (26, 110, 184, 235), "线索"),
    }
    for key, (px, py, tone, label) in positions.items():
        draw.ellipse((px - 18, py - 18, px + 18, py + 18), fill=tone, outline=WHITE, width=2)
        if key == selected:
            draw.ellipse((px - 38, py - 38, px + 38, py + 38), outline=GOLD, width=3)
            _box(draw, (px + 28, py - 28, 150, 54), PAPER, GOLD, None, width=2)
            _badge(draw, (px + 40, py - 16, 52, 22), label, tone)
            _text(draw, (px + 100, py - 16), "可点任务", TINY, INK, 80)
    # Keep the deep chain visible but not selected.
    draw.line((1128, 524, 1016, 692), fill=(126, 92, 206, 96), width=3)
    draw.ellipse((1128 - 16, 524 - 16, 1128 + 16, 524 + 16), fill=CYAN, outline=WHITE, width=2)
    draw.ellipse((1016 - 16, 692 - 16, 1016 + 16, 692 + 16), fill=BLACK, outline=WHITE, width=2)
    _text(draw, (614, 800), "非深链任务：地图只显示选中 pin 与短任务签；不会出现当前环/下一环链卡。", SMALL, WHITE, 680)


def _draw_right(draw: ImageDraw.ImageDraw, data: dict[str, object], kind: str) -> None:
    _box(draw, (1426, 176, 372, 66), PAPER, (38, 50, 48, 220), None, width=2)
    _text(draw, (1444, 194), str(data["title"]), H2, INK, 332)
    if kind == "normal":
        _box(draw, (1426, 276, 372, 284), PAPER, (38, 50, 48, 220), None, width=2)
        _text(draw, (1444, 302), str(data["summary"]), SMALL, INK, 328)
        _text(draw, (1444, 406), "目标：沿外围公路追踪换字警示牌。", SMALL, INK, 328)
        _text(draw, (1444, 450), str(data["need"]), SMALL, (126, 94, 34, 255), 328)
        _text(draw, (1444, 500), "普通规则并入正文：失败不封死题材，可再次追踪。", TINY, MUTED, 328)
        risk_y = 604
    else:
        _box(draw, (1426, 276, 372, 240), PAPER, (38, 50, 48, 220), None, width=2)
        _text(draw, (1444, 302), str(data["summary"]), SMALL, INK, 328)
        _text(draw, (1444, 408), "目标：确认线索来源并决定是否抢占窗口。", SMALL, INK, 328)
        _text(draw, (1444, 452), str(data["need"]), SMALL, (126, 94, 34, 255), 328)
        slot_title, slot_desc = data["right_slot"]  # type: ignore[index]
        slot_outline = RED if "截稿" in str(slot_title) else (26, 110, 184, 235)
        _box(draw, (1426, 544, 372, 64), (246, 241, 230, 236), slot_outline, None, width=2)
        _text(draw, (1444, 555), str(slot_title), SMALL, slot_outline, 328)
        _text(draw, (1444, 583), str(slot_desc), TINY, INK, 328)
        risk_y = 630
    _box(draw, (1426, risk_y, 278, 76), PAPER, (38, 50, 48, 220), None, width=2)
    _text(draw, (1444, risk_y + 16), "可带回：照片 / 目击证词\n风险：凶险，可能引来封锁", TINY, INK, 246)
    _box(draw, (1426, 718, 372, 46), (245, 236, 203, 220), GOLD, None, width=2)
    _text(draw, (1440, 730), "阻断原因贴近 CTA；此处显示当前任务可行性。", TINY, INK, 340)
    _box(draw, (1426, 790, 356, 82), (198, 44, 28, 236), RED, None, width=2)
    _text(draw, (1462, 816), str(data["cta"]), H2, WHITE, 300)


def _draw_footer(draw: ImageDraw.ImageDraw, data: dict[str, object]) -> None:
    _box(draw, (180, 986, 430, 34), PAPER, (38, 50, 48, 210), None, width=2)
    _text(draw, (194, 994), str(data["footer"]), TINY, INK, 392)
    _box(draw, (634, 986, 350, 34), PAPER, (38, 50, 48, 210), None, width=2)
    _text(draw, (648, 994), "地区事件：军方封锁 · 本区对手骰+1", TINY, INK, 318)
    _box(draw, (1008, 986, 146, 34), PAPER, (38, 50, 48, 210), None, width=2)
    _text(draw, (1022, 994), "执行中 2 / 到期 1", TINY, INK, 120)
    _draw_day_advance_button(draw)


def build_variant(kind: str) -> None:
    data = TASKS[kind]
    img = _base()
    draw = ImageDraw.Draw(img, "RGBA")
    _text(draw, (70, 42), f"地区任务台 v3.4 · non-chain compat · {kind}", H1, WHITE)
    _text(draw, (70, 86), "兼容验证：非深链任务没有链卡；地图仍可点 pin；右侧替换为对应任务类型槽。", BODY, WHITE)
    _draw_non_chain_regions(draw)
    _draw_common_left(draw, kind)
    _draw_non_chain_map(draw, kind)
    _draw_right(draw, data, kind)
    _draw_footer(draw, data)
    img.save(OUT_DIR / f"{kind}-task-compat-fill.png")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for kind in ["normal", "deadline", "lead"]:
        build_variant(kind)
    print(OUT_DIR)
    print("normal-task-compat-fill.png")
    print("deadline-task-compat-fill.png")
    print("lead-task-compat-fill.png")


if __name__ == "__main__":
    main()
