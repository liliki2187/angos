from pathlib import Path

from PIL import Image, ImageDraw

import build_region_task_surrounding_ui_visual_target_v1 as base


OUTPUT = (
    base.ROOT
    / "design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1-1-delayered/review"
)


def build_delayered_art_base(source: Image.Image) -> Image.Image:
    """Recompose generated art once per physical object; never paste a parent and its children."""
    background = source.crop((450, 108, 1232, 777)).resize(
        (1920, 1080), Image.Resampling.BICUBIC
    )
    canvas = background.convert("RGBA")

    # Top: three sibling carriers, each pasted once.
    base.paste_resized(canvas, source, (17, 16, 323, 97), (24, 14, 188, 58))
    base.paste_resized(canvas, source, (339, 17, 1297, 99), (204, 10, 1316, 62))
    base.paste_resized(canvas, source, (1310, 17, 1657, 97), (1574, 14, 1896, 58))

    # Left: the generated folder already contains its header, two sibling slips and footer.
    # Paste that coherent object once; do not paste any child paper a second time.
    base.paste_resized(canvas, source, (16, 109, 441, 780), (24, 96, 404, 900))

    # Right: exactly two structural layers (olive backing + one continuous warm page), then
    # one sibling CTA. Metadata and risk are typography on the page, not extra paper plates.
    # Use the native full-height dossier only as an outer backing. The continuous warm page
    # fully occludes its old internal plates, so no duplicate child edge remains visible.
    base.paste_resized(canvas, source, (1247, 109, 1659, 929), (1484, 96, 1896, 1056))
    base.paste_resized(canvas, source, (1273, 267, 1612, 487), (1508, 120, 1872, 892))
    base.paste_resized(canvas, source, (1277, 778, 1615, 896), (1512, 916, 1868, 1028))

    # Bottom: two sibling tickets on the navy stage. There is no parent band underneath.
    base.paste_resized(canvas, source, (1277, 778, 1615, 896), (52, 938, 370, 1038))
    base.paste_resized(canvas, source, (382, 790, 1236, 927), (396, 938, 1432, 1038))

    return canvas


def paste_delayered_kind_icons(canvas: Image.Image) -> None:
    atlas = Image.open(base.KIND_ATLAS).convert("RGBA")
    cell_width = atlas.width // 4
    for index, target in ((0, (68, 340, 110, 382)), (1, (68, 510, 110, 552))):
        icon = atlas.crop((index * cell_width, 0, (index + 1) * cell_width, atlas.height))
        icon.thumbnail((target[2] - target[0], target[3] - target[1]), Image.Resampling.LANCZOS)
        x = target[0] + (target[2] - target[0] - icon.width) // 2
        y = target[1] + (target[3] - target[1] - icon.height) // 2
        canvas.alpha_composite(icon, (x, y))


def draw_delayered_text(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)

    # Top.
    draw.text((40, 25), "← 返回世界地图", font=base.F_T3_B, fill=base.INK)
    draw.text((216, 23), "WORLD MYSTERY WEEKLY", font=base.F_T2, fill=base.LIGHT)
    draw.text((540, 17), "北岸调查区 · 区域任务台", font=base.F_T1, fill=base.LIGHT)
    draw.text((1600, 27), "第 002 期 · 第 02 周 · 剩余 5 天", font=base.F_T4_B, fill=base.LIGHT_META)

    # Left folder. Header and slips use the carriers already baked into the one folder image.
    draw.text((88, 142), "北岸调查区 · NORTH SHORE", font=base.F_T4_B, fill=base.TEAL)
    draw.text((88, 170), "事件索引", font=base.F_T1, fill=base.INK)
    draw.text((88, 214), "2 条可选 · 已选 1", font=base.F_T4, fill=base.META)

    draw.text((128, 330), "明日电台的停电预告", font=base.F_T3_B, fill=base.BODY)
    draw.text((128, 408), "连续追踪 · 2天 · 玄学", font=base.F_T4, fill=base.META)
    draw.text((326, 330), "已选", font=base.F_T4_B, fill=base.OLIVE)

    draw.text((128, 500), "变电站空白值班表", font=base.F_T3_B, fill=base.BODY)
    draw.text((128, 580), "限时截稿 · 1天 · 纪实", font=base.F_T4, fill=base.META)

    draw.text((60, 680), "ISSUE 002 / NORTH SHORE DESK", font=base.F_T4_B, fill="#2B6063")
    draw.text((60, 768), "本区取材回条", font=base.F_T4_B, fill=base.TEAL)
    draw.text((60, 808), "已选 1 · 可处理 2 · 执行中 0", font=base.F_T3_B, fill=base.BODY)
    draw.text((60, 846), "本周剩余 5 天", font=base.F_T4, fill=base.META)

    # Right dossier. All reading fields share one continuous warm page.
    draw.text((1532, 142), "当前任务 · CURRENT ASSIGNMENT", font=base.F_T4_B, fill=base.TEAL)
    draw.multiline_text(
        (1532, 168), "明日电台的\n停电预告", font=base.F_T1_DOSSIER, fill=base.INK, spacing=0
    )

    draw.text((1532, 250), "事件摘要", font=base.F_T4_B, fill=base.TEAL)
    summary = (
        "同一城区连续收到异常广播举报。\n"
        "停电后，旧电台会先播出明日新闻。\n"
        "三名听众记下了互相矛盾的时间。\n"
        "其中一段录音提到尚未发生的火灾。\n"
        "线路图显示信号绕过了主发射塔。\n"
        "编辑部需要确认预告是否能被改变。\n"
        "本次调查将决定后续连续追踪入口。"
    )
    draw.multiline_text((1532, 282), summary, font=base.F_T3, fill=base.BODY, spacing=10)

    draw.text((1532, 560), "地点 / 耗时 / 需求", font=base.F_T4_B, fill=base.TEAL)
    draw.text((1532, 590), "地点：北岸旧电台 / 变电站", font=base.F_T3_B, fill=base.BODY)
    draw.text((1532, 622), "耗时：2天　需求：洞察 / 推理", font=base.F_T3_B, fill=base.BODY)

    draw.text((1532, 684), "风险等级 / 依据 / 建议", font=base.F_T4_B, fill=base.RUST)
    draw.text((1532, 714), "风险等级：高", font=base.F_T3_B, fill=base.BODY)
    draw.text((1532, 742), "截稿：本周截稿前 2 天", font=base.F_T3, fill=base.BODY)
    draw.text((1532, 770), "连续追踪：成功后开启后续入口", font=base.F_T3, fill=base.BODY)
    draw.text((1532, 808), "建议：优先派洞察记者；", font=base.F_T3_B, fill=base.TEAL)
    draw.text((1532, 834), "签批时复核黑骰风险。", font=base.F_T3_B, fill=base.TEAL)

    base.draw_centered(draw, (1512, 936, 1868, 966), "任务已就绪", base.F_T4_B, base.LIGHT_META)
    base.draw_centered(draw, (1512, 962, 1868, 1014), "送至签批台", base.F_T2, base.LIGHT)

    # Bottom sibling tickets.
    draw.text((132, 954), "推进一天", font=base.F_T2, fill="#A6A78D")
    draw.text((132, 994), "完成本周调查后可用", font=base.F_T4, fill="#727969")
    draw.text((500, 954), "本周日程", font=base.F_T4_B, fill=base.TEAL)
    draw.text((500, 980), "已选 1 · 可处理 2 · 执行中 0", font=base.F_T3_B, fill=base.BODY)
    draw.text((500, 1012), "本周剩余 5 天", font=base.F_T4, fill=base.META)
    draw.text((920, 954), "推进后预览", font=base.F_T4_B, fill=base.RUST)
    draw.multiline_text(
        (920, 980),
        "明日电台截稿剩 2 天；\n连续追踪入口将在任务完成后开放。",
        font=base.F_T3,
        fill=base.BODY,
        spacing=7,
    )


def save_outputs(canvas: Image.Image) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT / "01-fullscreen-delayered-v1-1.png", quality=95)
    canvas.crop((24, 96, 404, 900)).convert("RGB").save(
        OUTPUT / "02-left-folder-delayered-v1-1.png", quality=95
    )
    canvas.crop((24, 916, 1460, 1056)).convert("RGB").save(
        OUTPUT / "03-bottom-tickets-delayered-v1-1.png", quality=95
    )
    canvas.crop((1484, 96, 1896, 1056)).convert("RGB").save(
        OUTPUT / "04-right-dossier-delayered-v1-1.png", quality=95
    )
    canvas.resize((480, 270), Image.Resampling.LANCZOS).convert("RGB").save(
        OUTPUT / "05-fullscreen-25-percent-delayered-v1-1.png", quality=95
    )


def main() -> None:
    source = Image.open(base.SOURCE).convert("RGBA")
    canvas = build_delayered_art_base(source)
    base.paste_frozen_runtime(canvas)
    paste_delayered_kind_icons(canvas)
    draw_delayered_text(canvas)
    save_outputs(canvas)


if __name__ == "__main__":
    main()
