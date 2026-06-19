from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/artboard_v3/rt-artboard-full.png"
OUT_DIR = ROOT / "docs/screenshots/2026-06-18-region-task-v3-7-top-schedule-structure"
FULL_OUT = OUT_DIR / "01-region-task-v3-7-top-schedule-structure.png"
CROP_OUT = OUT_DIR / "02-right-top-schedule-detail-crop.png"
CLEAN_OUT = OUT_DIR / "03-clean-orthogonal-top-schedule-structure.png"

CANVAS = (1920, 1080)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/simhei.ttf" if bold else "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsunb.ttf" if bold else "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for item in candidates:
        p = Path(item)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


F_TITLE = font(28, True)
F_H1 = font(26, True)
F_H2 = font(22, True)
F_BODY = font(18)
F_SMALL = font(15)
F_TINY = font(13)


def rect_from_xywh(x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    return (x, y, x + w, y + h)


def draw_label(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fill: tuple[int, int, int, int] = (13, 31, 43, 226),
    outline: tuple[int, int, int, int] = (238, 187, 86, 235),
    color: tuple[int, int, int, int] = (245, 236, 208, 255),
    pad: tuple[int, int] = (12, 6),
    text_font: ImageFont.FreeTypeFont = F_SMALL,
) -> tuple[int, int, int, int]:
    x, y = xy
    bbox = d.textbbox((0, 0), text, font=text_font)
    w = bbox[2] - bbox[0] + pad[0] * 2
    h = bbox[3] - bbox[1] + pad[1] * 2
    r = rect_from_xywh(x, y, w, h)
    d.rounded_rectangle(r, radius=4, fill=fill, outline=outline, width=2)
    d.text((x + pad[0], y + pad[1] - 1), text, font=text_font, fill=color)
    return r


def draw_box(
    d: ImageDraw.ImageDraw,
    xywh: tuple[int, int, int, int],
    label: str,
    outline: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
    text_color: tuple[int, int, int, int] = (245, 245, 226, 255),
    label_bg: tuple[int, int, int, int] | None = None,
    label_font: ImageFont.FreeTypeFont = F_SMALL,
    width: int = 3,
) -> tuple[int, int, int, int]:
    x, y, w, h = xywh
    r = rect_from_xywh(x, y, w, h)
    d.rounded_rectangle(r, radius=4, fill=fill, outline=outline, width=width)
    if label:
        label_bg = label_bg or (13, 31, 43, 230)
        draw_label(d, (x + 8, y + 8), label, fill=label_bg, outline=outline, color=text_color, text_font=label_font)
    return r


def draw_wrapped(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    max_width: int,
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    line_gap: int = 6,
) -> int:
    x, y = xy
    lines: list[str] = []
    current = ""
    for ch in text:
        candidate = current + ch
        if d.textlength(candidate, font=text_font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)

    yy = y
    for line in lines:
        d.text((x, yy), line, font=text_font, fill=fill)
        bbox = d.textbbox((x, yy), line, font=text_font)
        yy += bbox[3] - bbox[1] + line_gap
    return yy


def arrow(d: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int, int]) -> None:
    d.line([start, end], fill=color, width=4)
    ex, ey = end
    sx, sy = start
    dx = ex - sx
    dy = ey - sy
    if abs(dx) > abs(dy):
        sign = 1 if dx > 0 else -1
        pts = [(ex, ey), (ex - sign * 16, ey - 8), (ex - sign * 16, ey + 8)]
    else:
        sign = 1 if dy > 0 else -1
        pts = [(ex, ey), (ex - 8, ey - sign * 16), (ex + 8, ey - sign * 16)]
    d.polygon(pts, fill=color)


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.open(SOURCE).convert("RGBA")
    if img.size != CANVAS:
        img = img.resize(CANVAS, Image.Resampling.LANCZOS)

    overlay = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Dim only enough to make contract boxes readable; this is a structure wireframe, not a style proof.
    d.rectangle((0, 0, 1920, 1080), fill=(4, 12, 18, 48))

    draw_label(
        d,
        (42, 34),
        "STRUCTURE_WIREFRAME v3.7 / 推进一天移入右侧顶部全局日程头",
        fill=(8, 19, 29, 238),
        outline=(238, 187, 86, 255),
        text_font=F_BODY,
    )

    # Left list and center map remain as functional anchors; they are intentionally low-detail here.
    draw_box(d, (48, 112, 482, 768), "左侧：任务档案索引 / 选择任务", (241, 78, 62, 220), (13, 31, 43, 54))
    draw_box(d, (554, 96, 742, 778), "中央：地区地图 / 深度链具体任务点在地图上点选", (41, 210, 222, 220), (13, 31, 43, 34))
    draw_box(d, (576, 136, 698, 700), "地图保持原视觉源，仅叠 pin / label / chain 状态层", (41, 210, 222, 110), (20, 115, 140, 28), width=2)

    # Bottom strip is no longer the action carrier; keep it as regional event/receipt only.
    draw_box(d, (82, 910, 1260, 112), "底部：地区特殊事件 / 派遣摘要 / 返报倒计时（只读，不放推进按钮）", (238, 187, 86, 220), (244, 235, 210, 86))
    for x in (468, 858):
        d.line((x, 924, x, 1008), fill=(35, 59, 66, 150), width=2)
    d.text((128, 948), "本周区域事件", font=F_H2, fill=(20, 35, 38, 235))
    d.text((128, 980), "探索周余 4天 · 北美禁区 · 选中 M330", font=F_SMALL, fill=(27, 45, 48, 225))
    d.text((512, 948), "当前派遣 2 / 5", font=F_H2, fill=(20, 35, 38, 235))
    d.text((512, 980), "签批后不消耗天数，派遣占用 2天", font=F_SMALL, fill=(27, 45, 48, 225))
    d.text((902, 948), "预计返报 1天后", font=F_H2, fill=(20, 35, 38, 235))
    d.text((902, 980), "最快返报时间 / 到期结算摘要", font=F_SMALL, fill=(27, 45, 48, 225))

    # Right sheet structure.
    right_shell = draw_box(d, (1340, 86, 520, 882), "右侧：当前任务详情 / 签批入口", (238, 187, 86, 210), (8, 19, 29, 70), width=3)
    d.rounded_rectangle((1366, 126, 1832, 936), radius=2, outline=(245, 236, 208, 210), width=2)

    # NEW global schedule header at the top of the right document.
    sched = draw_box(
        d,
        (1390, 144, 414, 78),
        "A 全局日程头（新位置）",
        (238, 187, 86, 255),
        (8, 27, 39, 210),
        label_bg=(36, 48, 50, 238),
        width=4,
    )
    d.text((1410, 182), "探索周 余 4天 · 当前派遣 2/5", font=F_SMALL, fill=(245, 236, 208, 255))
    d.rounded_rectangle((1638, 162, 1786, 206), radius=5, fill=(15, 31, 43, 245), outline=(247, 182, 65, 255), width=3)
    d.text((1650, 170), "推进一天", font=F_BODY, fill=(247, 182, 65, 255))
    d.polygon([(1762, 177), (1778, 184), (1762, 193)], fill=(247, 182, 65, 255))
    d.text((1650, 191), "DAY +1 / 二次确认", font=F_TINY, fill=(247, 182, 65, 220))

    # Semantic separator: schedule is global, task detail starts below.
    d.line((1392, 234, 1804, 234), fill=(238, 187, 86, 180), width=3)
    d.text((1398, 238), "以下才是当前选中任务，不和推进一天共享语义", font=F_TINY, fill=(238, 187, 86, 235))

    title = draw_box(d, (1390, 264, 414, 70), "B 任务标题 / meta", (235, 226, 202, 230), (245, 236, 208, 95), text_color=(20, 35, 38, 255), label_bg=(244, 235, 210, 235), width=2)
    d.text((1410, 300), "M330 未班车空白段", font=F_H2, fill=(20, 35, 38, 255))
    d.text((1410, 324), "北美禁区 / 深度调查链", font=F_TINY, fill=(49, 63, 59, 230))

    body = draw_box(d, (1390, 356, 414, 214), "C 正文：目标 / 需求 / 风险", (235, 226, 202, 230), (245, 236, 208, 86), text_color=(20, 35, 38, 255), label_bg=(244, 235, 210, 235), width=2)
    draw_wrapped(
        d,
        (1410, 394),
        "一段车载录音缺了三秒，乘客口供互相矛盾，但都指向同一站。目标：找出缺失三秒对应的站点记录。",
        362,
        F_SMALL,
        (20, 35, 38, 240),
    )
    d.text((1410, 506), "需求：察 / 诡 / 理 · 耗时 2天", font=F_SMALL, fill=(112, 83, 36, 245))

    chain = draw_box(d, (1390, 592, 414, 76), "D 特殊槽：深度链 / 截稿 / 黑骰等短状态", (145, 96, 220, 235), (97, 66, 150, 72), text_color=(245, 236, 208, 255), label_bg=(74, 48, 123, 238), width=3)
    d.text((1410, 630), "深度调查 · 当前环 1/4", font=F_BODY, fill=(245, 236, 208, 255))
    d.text((1638, 630), "1/4", font=F_BODY, fill=(245, 236, 208, 255))

    tickets = draw_box(d, (1390, 690, 414, 104), "E 结果摘要 / 可带回 / 风险票据", (41, 210, 222, 220), (244, 235, 210, 70), text_color=(20, 35, 38, 255), label_bg=(244, 235, 210, 235), width=2)
    for i, txt in enumerate(["成功后揭示下一环，失败保留线索。", "可带回：录音 / 证词", "风险：凶险，可能触发误导线索"]):
        y = 724 + i * 24
        d.rectangle((1410, y + 4, 1426, y + 20), fill=[(54, 145, 94, 235), (41, 164, 178, 235), (209, 53, 45, 235)][i])
        d.text((1436, y), txt, font=F_TINY, fill=(20, 35, 38, 235))

    cta = draw_box(d, (1390, 820, 414, 88), "F 主 CTA：进入派遣签批", (232, 54, 42, 255), (174, 38, 28, 210), label_bg=(78, 24, 22, 238), width=4)
    d.rounded_rectangle((1422, 842, 1732, 886), radius=4, fill=(245, 236, 208, 220), outline=(37, 29, 22, 255), width=2)
    d.text((1488, 850), "进入派遣签批", font=F_H1, fill=(18, 22, 22, 255))
    d.polygon([(1750, 842), (1790, 864), (1750, 886)], fill=(245, 236, 208, 245))

    # Mark right-bottom area as deliberate non-interactive visual breathing space, not a missing button.
    draw_box(
        d,
        (1390, 926, 414, 62),
        "G CTA 下方：非交互纸脚 / 阴影留白",
        (92, 125, 134, 175),
        (8, 19, 29, 90),
        label_bg=(8, 19, 29, 220),
        width=2,
    )

    # Safety arrows / rationale.
    arrow(d, (1704, 214), (1704, 816), (238, 187, 86, 220))
    draw_label(d, (1518, 706), "两个高风险动作垂直距离约 600px，避免连点误触", fill=(8, 19, 29, 238), outline=(238, 187, 86, 245), text_font=F_TINY)
    arrow(d, (1348, 924), (1320, 980), (92, 125, 134, 230))
    draw_label(d, (1276, 1000), "底部条只保留全局信息，不再承担主动作", fill=(8, 19, 29, 238), outline=(92, 125, 134, 245), text_font=F_TINY)

    result = Image.alpha_composite(img, overlay).convert("RGB")
    result.save(FULL_OUT, quality=96)

    crop = result.crop((1310, 72, 1870, 1008))
    crop.save(CROP_OUT, quality=96)

    clean = Image.new("RGBA", CANVAS, (6, 16, 25, 255))
    cd = ImageDraw.Draw(clean)
    # Functional blockout: all writable / clickable surfaces are orthogonal by construction.
    for x in range(0, 1920, 40):
        cd.line((x, 0, x, 1080), fill=(31, 62, 75, 65), width=1)
    for y in range(0, 1080, 40):
        cd.line((0, y, 1920, y), fill=(31, 62, 75, 65), width=1)
    cd.rectangle((0, 0, 1920, 1080), outline=(238, 187, 86, 180), width=3)

    draw_label(
        cd,
        (42, 32),
        "CLEAN STRUCTURE v3.7 / 所有动态文字承载面均为正交矩形",
        fill=(8, 19, 29, 240),
        outline=(238, 187, 86, 255),
        text_font=F_BODY,
    )

    draw_box(cd, (56, 104, 452, 764), "左：任务档案索引", (232, 54, 42, 230), (244, 235, 210, 56), width=3)
    for i, (name, meta, color) in enumerate(
        [
            ("51 区外围公路", "白色调查 · 耗时 2天", (232, 54, 42, 240)),
            ("罗斯威尔档案残页", "线索调查 · 成功后生成新任务", (32, 120, 202, 240)),
            ("突发：雷达异常光点", "红色截稿 · 剩 4天", (42, 164, 178, 240)),
            ("M330 未班车空白段", "深度链 · 当前环 1/4", (126, 80, 190, 240)),
        ]
    ):
        y = 160 + i * 166
        cd.rounded_rectangle((88, y, 470, y + 124), radius=4, fill=(244, 235, 210, 230), outline=(35, 50, 55, 245), width=2)
        cd.rectangle((88, y, 128, y + 124), fill=color)
        cd.text((150, y + 28), name, font=F_H2, fill=(18, 22, 22, 255))
        cd.text((150, y + 64), meta, font=F_SMALL, fill=(35, 49, 52, 240))
        if i == 3:
            cd.rounded_rectangle((82, y - 8, 478, y + 132), radius=5, outline=(238, 187, 86, 255), width=4)

    draw_box(cd, (540, 104, 770, 764), "中：地区地图主舞台", (41, 210, 222, 225), (12, 50, 66, 130), width=3)
    cd.text((604, 160), "保留原地图视觉源", font=F_H1, fill=(245, 236, 208, 240))
    cd.text((604, 200), "动态层：pin / label / chain / selected / locked", font=F_BODY, fill=(131, 225, 230, 240))
    # Rough node map only for structural reading.
    pts = [(790, 304), (910, 372), (1042, 520), (920, 630), (760, 566), (700, 438)]
    cd.line(pts + [pts[0]], fill=(232, 54, 42, 230), width=5)
    for idx, (x, y) in enumerate(pts):
        pin_color = (232, 54, 42, 255) if idx in (0, 2, 4) else (42, 210, 222, 255)
        cd.ellipse((x - 14, y - 14, x + 14, y + 14), fill=pin_color, outline=(245, 236, 208, 255), width=3)
        cd.rounded_rectangle((x - 58, y + 20, x + 96, y + 70), radius=4, fill=(244, 235, 210, 230), outline=(34, 52, 58, 240), width=2)
    cd.rounded_rectangle((1000, 472, 1196, 558), radius=5, fill=(244, 235, 210, 240), outline=(238, 187, 86, 255), width=4)
    cd.text((1022, 492), "M330", font=F_H2, fill=(18, 22, 22, 255))
    cd.text((1022, 524), "当前环 1/4", font=F_SMALL, fill=(126, 80, 190, 255))

    draw_box(cd, (1340, 84, 520, 884), "右：正交任务详情纸", (238, 187, 86, 230), (244, 235, 210, 230), text_color=(18, 22, 22, 255), label_bg=(244, 235, 210, 245), width=3)

    cd.rounded_rectangle((1376, 128, 1824, 214), radius=5, fill=(9, 25, 36, 245), outline=(238, 187, 86, 255), width=4)
    cd.text((1396, 144), "全局日程头", font=F_H2, fill=(245, 236, 208, 255))
    cd.text((1396, 176), "探索周余 4天 · 当前派遣 2/5 · 返报 1天后", font=F_SMALL, fill=(245, 236, 208, 235))
    cd.rounded_rectangle((1638, 144, 1804, 198), radius=5, fill=(16, 35, 48, 255), outline=(247, 182, 65, 255), width=3)
    cd.text((1660, 154), "推进一天", font=F_BODY, fill=(247, 182, 65, 255))
    cd.text((1660, 178), "DAY +1 / 确认", font=F_TINY, fill=(247, 182, 65, 230))
    cd.line((1376, 236, 1824, 236), fill=(238, 187, 86, 210), width=3)
    cd.text((1378, 244), "分隔线：上方是全局时间动作，下方才是当前任务", font=F_TINY, fill=(112, 83, 36, 235))

    cd.rectangle((1376, 278, 1824, 340), fill=(255, 249, 232, 245), outline=(35, 50, 55, 220), width=2)
    cd.text((1396, 292), "M330 未班车空白段", font=F_H1, fill=(18, 22, 22, 255))
    cd.text((1396, 320), "北美禁区 / 深度调查链", font=F_SMALL, fill=(49, 63, 59, 240))
    cd.rectangle((1376, 366, 1824, 570), fill=(255, 249, 232, 245), outline=(35, 50, 55, 220), width=2)
    draw_wrapped(
        cd,
        (1398, 392),
        "一段车载录音缺了三秒，乘客口供互相矛盾，但都指向同一站。目标：找出缺失三秒对应的站点记录。需求：察 / 诡 / 理，耗时 2天。",
        392,
        F_BODY,
        (18, 22, 22, 245),
    )
    cd.rectangle((1376, 596, 1824, 662), fill=(238, 230, 252, 245), outline=(126, 80, 190, 255), width=3)
    cd.text((1396, 616), "深度调查 · 当前环 1/4", font=F_BODY, fill=(126, 80, 190, 255))
    cd.rectangle((1376, 688, 1824, 778), fill=(255, 249, 232, 245), outline=(41, 210, 222, 220), width=2)
    cd.text((1396, 706), "成功后揭示下一环；失败保留线索。", font=F_SMALL, fill=(18, 22, 22, 240))
    cd.text((1396, 734), "可带回：录音 / 证词", font=F_SMALL, fill=(18, 22, 22, 240))
    cd.text((1396, 762), "风险：凶险，可能触发误导线索", font=F_SMALL, fill=(209, 53, 45, 245))
    cd.rounded_rectangle((1376, 812, 1824, 912), radius=8, fill=(184, 43, 32, 255), outline=(232, 54, 42, 255), width=4)
    cd.rectangle((1418, 836, 1730, 888), fill=(255, 249, 232, 245), outline=(25, 29, 28, 255), width=3)
    cd.text((1492, 846), "进入派遣签批", font=F_H1, fill=(18, 22, 22, 255))
    cd.polygon([(1752, 832), (1796, 862), (1752, 892)], fill=(255, 249, 232, 250))
    cd.text((1380, 926), "CTA 下方仅做纸脚/阴影/留白，不放第二个高风险按钮", font=F_TINY, fill=(112, 83, 36, 230))

    # Bottom status strip no longer hosts the day advance action.
    cd.rounded_rectangle((80, 908, 1298, 1028), radius=4, fill=(244, 235, 210, 235), outline=(238, 187, 86, 255), width=3)
    cd.text((126, 936), "地区特殊事件", font=F_H2, fill=(18, 22, 22, 255))
    cd.text((126, 970), "签批不消耗天数；推进动作已移到右侧顶部全局日程头。", font=F_SMALL, fill=(35, 50, 55, 245))
    cd.line((600, 926, 600, 1010), fill=(35, 50, 55, 160), width=2)
    cd.text((648, 936), "当前派遣 2 / 5", font=F_H2, fill=(18, 22, 22, 255))
    cd.text((648, 970), "执行中任务数 / 本周可用派遣位", font=F_SMALL, fill=(35, 50, 55, 245))
    cd.line((960, 926, 960, 1010), fill=(35, 50, 55, 160), width=2)
    cd.text((1000, 936), "预计返报 1天后", font=F_H2, fill=(18, 22, 22, 255))
    cd.text((1000, 970), "最近返报时间", font=F_SMALL, fill=(35, 50, 55, 245))

    clean.convert("RGB").save(CLEAN_OUT, quality=96)


if __name__ == "__main__":
    build()
    print(FULL_OUT)
    print(CROP_OUT)
    print(CLEAN_OUT)
