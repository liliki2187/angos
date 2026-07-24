from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
SOURCE = ROOT / "design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/source/region-task-surrounding-ui-imagegen-source-v1.png"
RUNTIME = ROOT / "docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/01-selected-ready-full-v1.png"
KIND_ATLAS = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/v2/pin_slice/rt-task-pin-kind-icons-c-hybrid-v3-atlas-3x.png"
OUTPUT = ROOT / "design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/review"

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")

INK = "#10232B"
BODY = "#172A30"
META = "#526166"
TEAL = "#34767A"
OLIVE = "#6C773F"
RUST = "#A84E38"
LIGHT = "#F2E7D2"
LIGHT_META = "#D7D7AC"
DISABLED = "#70736B"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


F_T1 = font(28, True)
F_T1_DOSSIER = font(26, True)
F_T2 = font(20, True)
F_T3 = font(16)
F_T3_B = font(16, True)
F_T4 = font(13)
F_T4_B = font(13, True)
F_WATERMARK = font(112, True)


def paste_resized(canvas: Image.Image, source: Image.Image, source_box, target_box) -> None:
    x0, y0, x1, y1 = target_box
    patch = source.crop(source_box).resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    if patch.mode == "RGBA":
        canvas.alpha_composite(patch, (x0, y0))
    else:
        canvas.paste(patch, (x0, y0))


def draw_centered(draw: ImageDraw.ImageDraw, rect, text: str, face, fill: str) -> None:
    x0, y0, x1, y1 = rect
    box = draw.textbbox((0, 0), text, font=face)
    width = box[2] - box[0]
    height = box[3] - box[1]
    draw.text(
        (x0 + (x1 - x0 - width) / 2, y0 + (y1 - y0 - height) / 2 - box[1]),
        text,
        font=face,
        fill=fill,
    )


def build_art_base(source: Image.Image) -> Image.Image:
    # The model honored the art language but not the requested coordinates. Recompose only
    # whole generated regions; do not procedurally draw any carrier, edge, or decoration.
    background = source.crop((450, 108, 1232, 777)).resize((1920, 1080), Image.Resampling.BICUBIC)
    canvas = background.convert("RGBA")

    # Top editorial carriers.
    paste_resized(canvas, source, (17, 16, 323, 97), (24, 14, 188, 58))
    paste_resized(canvas, source, (339, 17, 1297, 99), (204, 10, 1316, 62))
    paste_resized(canvas, source, (1310, 17, 1657, 97), (1574, 14, 1896, 58))

    # Left index: generated backing first, then role-specific paper carriers.
    paste_resized(canvas, source, (16, 109, 441, 780), (24, 96, 404, 900))
    paste_resized(canvas, source, (34, 135, 411, 260), (40, 112, 388, 204))
    paste_resized(canvas, source, (43, 287, 405, 415), (46, 222, 382, 326))
    paste_resized(canvas, source, (43, 428, 405, 557), (46, 336, 382, 440))
    # Remove the model's unintended third blank task slip with a generated teal track patch.
    paste_resized(canvas, source, (42, 566, 405, 648), (40, 448, 388, 730))
    paste_resized(canvas, source, (40, 649, 410, 766), (44, 748, 384, 876))

    # Right dossier: preserve its continuous backing while normalizing each content carrier.
    paste_resized(canvas, source, (1247, 109, 1659, 929), (1484, 96, 1896, 1056))
    paste_resized(canvas, source, (1273, 132, 1612, 247), (1508, 120, 1872, 224))
    paste_resized(canvas, source, (1273, 267, 1612, 487), (1508, 244, 1872, 548))
    paste_resized(canvas, source, (1272, 498, 1612, 595), (1508, 568, 1872, 708))
    paste_resized(canvas, source, (1272, 604, 1615, 757), (1504, 718, 1876, 892))
    paste_resized(canvas, source, (1277, 778, 1615, 896), (1512, 916, 1868, 1028))

    # Bottom: one generated connected ticket composition, normalized to the fixed contract.
    paste_resized(canvas, source, (31, 788, 1237, 927), (24, 916, 1460, 1056))
    # Reuse the generated muted-olive action plate so the disabled time action stays below
    # the right dossier CTA in the decision hierarchy.
    paste_resized(canvas, source, (1277, 778, 1615, 896), (52, 938, 370, 1038))
    paste_resized(canvas, source, (382, 790, 1236, 927), (396, 938, 1432, 1038))

    return canvas


def paste_frozen_runtime(canvas: Image.Image) -> None:
    runtime = Image.open(RUNTIME).convert("RGBA")
    map_rect = (420, 96, 1460, 900)
    canvas.alpha_composite(runtime.crop(map_rect), (420, 96))


def paste_kind_icons(canvas: Image.Image) -> None:
    atlas = Image.open(KIND_ATLAS).convert("RGBA")
    cell_width = atlas.width // 4
    for index, target in ((0, (67, 238, 109, 280)), (1, (67, 352, 109, 394))):
        icon = atlas.crop((index * cell_width, 0, (index + 1) * cell_width, atlas.height))
        icon.thumbnail((target[2] - target[0], target[3] - target[1]), Image.Resampling.LANCZOS)
        x = target[0] + (target[2] - target[0] - icon.width) // 2
        y = target[1] + (target[3] - target[1] - icon.height) // 2
        canvas.alpha_composite(icon, (x, y))


def draw_text_layer(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)

    # Top: masthead has highest naming weight; issue data remains annotation scale.
    draw.text((40, 25), "← 返回世界地图", font=F_T3_B, fill=INK)
    draw.text((216, 23), "WORLD MYSTERY WEEKLY", font=F_T2, fill=LIGHT)
    draw.text((540, 17), "北岸调查区 · 区域任务台", font=F_T1, fill=LIGHT)
    draw.text((1600, 27), "第 002 期 · 第 02 周 · 剩余 5 天", font=F_T4_B, fill=LIGHT_META)

    # Left index: one selected task and one available task inside the same editorial object.
    draw.text((90, 113), "北岸调查区 · NORTH SHORE", font=F_T4_B, fill=TEAL)
    draw.text((90, 134), "事件索引", font=F_T1, fill=INK)
    draw.text((90, 174), "2 条可选 · 已选 1", font=F_T4, fill=META)

    draw.text((128, 232), "明日电台的停电预告", font=F_T3_B, fill=BODY)
    draw.text((128, 286), "连续追踪 · 2天 · 玄学", font=F_T4, fill=META)
    draw.text((328, 235), "已选", font=F_T4_B, fill=OLIVE)

    draw.text((128, 346), "变电站空白值班表", font=F_T3_B, fill=BODY)
    draw.text((128, 400), "限时截稿 · 1天 · 纪实", font=F_T4, fill=META)

    # Actual issue metadata turns the unused folder field into intentional editorial
    # breathing room without inventing a third task or gameplay responsibility.
    draw.text((62, 492), "ISSUE INDEX", font=F_T4_B, fill="#2B6063")
    draw.text((58, 510), "02", font=F_WATERMARK, fill="#1D5055")
    draw.text((66, 635), "NORTH SHORE DESK / ISSUE 002", font=F_T4_B, fill="#2B6063")

    draw.text((60, 768), "本区取材回条", font=F_T4_B, fill=TEAL)
    draw.text((60, 801), "已选 1 · 可处理 2 · 执行中 0", font=F_T3_B, fill=BODY)
    draw.text((60, 837), "本周剩余 5 天", font=F_T4, fill=META)

    # Right dossier: risk, evidence, recommendation, then one dominant task CTA.
    draw.text((1580, 128), "当前任务 · CURRENT ASSIGNMENT", font=F_T4_B, fill=TEAL)
    draw.multiline_text((1580, 148), "明日电台的\n停电预告", font=F_T1_DOSSIER, fill=INK, spacing=0)

    draw.text((1522, 260), "事件摘要", font=F_T4_B, fill=TEAL)
    summary = (
        "同一城区连续收到异常广播举报。\n"
        "停电后，旧电台会先播出明日新闻。\n"
        "三名听众记下了互相矛盾的时间。\n"
        "其中一段录音提到尚未发生的火灾。\n"
        "线路图显示信号绕过了主发射塔。\n"
        "编辑部需要确认预告是否能被改变。\n"
        "本次调查将决定后续连续追踪入口。"
    )
    draw.multiline_text((1522, 292), summary, font=F_T3, fill=BODY, spacing=10)

    draw.text((1566, 584), "地点 / 耗时 / 需求", font=F_T4_B, fill=TEAL)
    draw.text((1566, 616), "地点：北岸旧电台 / 变电站", font=F_T3_B, fill=BODY)
    draw.text((1566, 650), "耗时：2天　需求：洞察 / 推理", font=F_T3_B, fill=BODY)

    draw.text((1572, 734), "风险等级 / 依据 / 建议", font=F_T4_B, fill=RUST)
    draw.text((1572, 762), "风险等级：高", font=F_T3_B, fill=BODY)
    draw.text((1572, 788), "截稿：本周截稿前 2 天", font=F_T3, fill=BODY)
    draw.text((1572, 814), "连续追踪：成功后开启后续入口", font=F_T3, fill=BODY)
    draw.text((1572, 840), "建议：优先派洞察记者；", font=F_T3_B, fill=TEAL)
    draw.text((1572, 864), "签批时复核黑骰风险。", font=F_T3_B, fill=TEAL)

    draw_centered(draw, (1512, 936, 1868, 966), "任务已就绪", F_T4_B, LIGHT_META)
    draw_centered(draw, (1512, 962, 1868, 1014), "送至签批台", F_T2, LIGHT)

    # Bottom: deliberately lower interaction weight than the dossier CTA.
    draw.text((132, 954), "推进一天", font=F_T2, fill="#A6A78D")
    draw.text((132, 994), "完成本周调查后可用", font=F_T4, fill="#727969")
    draw.text((500, 954), "本周日程", font=F_T4_B, fill=TEAL)
    draw.text((500, 980), "已选 1 · 可处理 2 · 执行中 0", font=F_T3_B, fill=BODY)
    draw.text((500, 1012), "本周剩余 5 天", font=F_T4, fill=META)
    draw.text((920, 954), "推进后预览", font=F_T4_B, fill=RUST)
    draw.multiline_text(
        (920, 980),
        "明日电台截稿剩 2 天；\n连续追踪入口将在任务完成后开放。",
        font=F_T3,
        fill=BODY,
        spacing=7,
    )


def save_review_outputs(canvas: Image.Image) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    final_path = OUTPUT / "01-region-task-surrounding-ui-fullscreen-visual-target-v1.png"
    canvas.convert("RGB").save(final_path, quality=95)

    canvas.crop((24, 96, 404, 1056)).convert("RGB").save(
        OUTPUT / "02-left-index-and-bottom-action-detail-v1.png", quality=95
    )
    canvas.crop((1484, 96, 1896, 1056)).convert("RGB").save(
        OUTPUT / "03-right-dossier-risk-advice-detail-v1.png", quality=95
    )
    canvas.resize((480, 270), Image.Resampling.LANCZOS).convert("RGB").save(
        OUTPUT / "04-fullscreen-25-percent-readability-v1.png", quality=95
    )

    qa = canvas.copy()
    qa_draw = ImageDraw.Draw(qa)
    for rect, label in (
        ((420, 96, 1460, 900), "FROZEN MAP"),
        ((24, 96, 404, 900), "LEFT INDEX"),
        ((1484, 96, 1896, 1056), "RIGHT DOSSIER"),
        ((24, 916, 1460, 1056), "BOTTOM ACTION"),
    ):
        qa_draw.rectangle(rect, outline="#FF40A8", width=2)
        qa_draw.text((rect[0] + 6, rect[1] + 4), label, font=F_T4_B, fill="#FF40A8")
    qa.convert("RGB").save(OUTPUT / "05-geometry-qa-overlay-v1.png", quality=95)


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    canvas = build_art_base(source)
    paste_frozen_runtime(canvas)
    paste_kind_icons(canvas)
    draw_text_layer(canvas)
    save_review_outputs(canvas)


if __name__ == "__main__":
    main()
