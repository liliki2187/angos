from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "image_gen/2026-08-07/world-map-backdecor-state-decor-v1/06-real-ui-backdecor-reinsert-preview.png"
OUT_DIR = ROOT / "image_gen/2026-08-07/world-map-visual-refinement-zone-map-v1"
VIZ_DIR = Path(r"C:\Users\gzfangyue\.codex\visualizations\2026\07\22\019f8963-8f75-7e91-92e0-515d05adc6c9")


COLORS = {
    "bg": (7, 24, 31),
    "panel": (12, 35, 43),
    "paper": (236, 229, 204),
    "muted": (157, 177, 176),
    "now": (205, 84, 66),
    "wait": (222, 166, 76),
    "freeze": (108, 145, 112),
    "ink": (11, 32, 38),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc") if bold else Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf") if bold else Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def rounded_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    number: str,
    label: str,
    color: tuple[int, int, int],
) -> None:
    x, y = xy
    draw.ellipse((x, y, x + 52, y + 52), fill=color, outline=COLORS["paper"], width=3)
    box = draw.textbbox((0, 0), number, font=font(25, True))
    draw.text((x + 26 - (box[2] - box[0]) / 2, y + 25 - (box[3] - box[1]) / 2 - 2), number, font=font(25, True), fill=COLORS["paper"])
    label_box = draw.textbbox((0, 0), label, font=font(24, True))
    w = label_box[2] - label_box[0]
    draw.rounded_rectangle((x + 62, y + 3, x + 82 + w, y + 49), radius=4, fill=(*COLORS["bg"], 232), outline=color, width=3)
    draw.text((x + 72, y + 10), label, font=font(24, True), fill=COLORS["paper"])


def draw_zone(
    overlay: Image.Image,
    rect: tuple[int, int, int, int],
    color: tuple[int, int, int],
    number: str,
    label: str,
    label_xy: tuple[int, int] | None = None,
    dash: bool = False,
) -> None:
    draw = ImageDraw.Draw(overlay, "RGBA")
    x, y, w, h = rect
    draw.rectangle((x, y, x + w, y + h), fill=(*color, 36))
    if dash:
        step = 26
        for xx in range(x, x + w, step):
            draw.line((xx, y, min(xx + 14, x + w), y), fill=(*color, 255), width=5)
            draw.line((xx, y + h, min(xx + 14, x + w), y + h), fill=(*color, 255), width=5)
        for yy in range(y, y + h, step):
            draw.line((x, yy, x, min(yy + 14, y + h)), fill=(*color, 255), width=5)
            draw.line((x + w, yy, x + w, min(yy + 14, y + h)), fill=(*color, 255), width=5)
    else:
        draw.rectangle((x, y, x + w, y + h), outline=(*color, 255), width=6)
    rounded_label(draw, label_xy or (x + 12, y + 12), number, label, color)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    line = ""
    for char in text:
        candidate = line + char
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = char
    if line:
        lines.append(line)
    return lines


def issue_card(
    draw: ImageDraw.ImageDraw,
    y: int,
    number: str,
    title: str,
    body: str,
    color: tuple[int, int, int],
    status: str,
) -> int:
    x0, x1 = 2000, 2518
    draw.rounded_rectangle((x0, y, x1, y + 144), radius=5, fill=COLORS["panel"], outline=color, width=3)
    draw.ellipse((x0 + 18, y + 18, x0 + 62, y + 62), fill=color)
    draw.text((x0 + 31, y + 21), number, font=font(22, True), fill=COLORS["paper"])
    draw.text((x0 + 78, y + 15), title, font=font(27, True), fill=COLORS["paper"])
    draw.text((x1 - 98, y + 20), status, font=font(20, True), fill=color)
    lines = wrap_text(draw, body, font(20), 400)
    for idx, line in enumerate(lines[:3]):
        draw.text((x0 + 78, y + 58 + idx * 27), line, font=font(20), fill=COLORS["muted"])
    return y + 158


def crop_cover(source: Image.Image, rect: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    x, y, w, h = rect
    crop = source.crop((x, y, x + w, y + h))
    scale = max(size[0] / crop.width, size[1] / crop.height)
    resized = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def crop_contain(source: Image.Image, rect: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    x, y, w, h = rect
    crop = source.crop((x, y, x + w, y + h))
    scale = min(size[0] / crop.width, size[1] / crop.height)
    resized = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    result = Image.new("RGB", size, COLORS["bg"])
    result.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return result


def paper_contact_composite(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    left = crop_cover(source, (0, 760, 430, 320), (size[0] // 2 - 5, size[1]))
    right = crop_cover(source, (1390, 0, 530, 1080), (size[0] // 2 - 5, size[1]))
    result = Image.new("RGB", size, COLORS["bg"])
    result.paste(left, (0, 0))
    result.paste(right, (size[0] // 2 + 5, 0))
    divider = ImageDraw.Draw(result)
    divider.rectangle((size[0] // 2 - 5, 0, size[0] // 2 + 5, size[1]), fill=COLORS["now"])
    return result


def detail_panel(
    canvas: Image.Image,
    source: Image.Image,
    origin: tuple[int, int],
    crop_rect: tuple[int, int, int, int],
    number: str,
    title: str,
    current: str,
    repair: str,
    color: tuple[int, int, int],
    fit_mode: str = "cover",
    image_override: Image.Image | None = None,
) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y = origin
    panel_w, panel_h = 880, 430
    draw.rounded_rectangle((x, y, x + panel_w, y + panel_h), radius=6, fill=COLORS["panel"], outline=color, width=3)
    image_rect = (x + 18, y + 18, 500, 394)
    if image_override is not None:
        crop = image_override.resize((image_rect[2], image_rect[3]), Image.Resampling.LANCZOS)
    elif fit_mode == "contain":
        crop = crop_contain(source, crop_rect, (image_rect[2], image_rect[3]))
    else:
        crop = crop_cover(source, crop_rect, (image_rect[2], image_rect[3]))
    canvas.paste(crop, (image_rect[0], image_rect[1]))
    draw.rectangle(
        (image_rect[0], image_rect[1], image_rect[0] + image_rect[2], image_rect[1] + image_rect[3]),
        outline=color,
        width=4,
    )
    tx = x + 544
    draw.ellipse((tx, y + 20, tx + 48, y + 68), fill=color)
    draw.text((tx + 14, y + 24), number, font=font(22, True), fill=COLORS["paper"])
    draw.text((tx + 62, y + 18), title, font=font(31, True), fill=COLORS["paper"])
    draw.text((tx, y + 92), "现在为什么粗", font=font(22, True), fill=color)
    yy = y + 128
    for line in wrap_text(draw, current, font(20), 306)[:4]:
        draw.text((tx, yy), line, font=font(20), fill=COLORS["muted"])
        yy += 28
    draw.line((tx, y + 250, x + panel_w - 24, y + 250), fill=COLORS["muted"], width=1)
    draw.text((tx, y + 270), "返修只做什么", font=font(22, True), fill=COLORS["paper"])
    yy = y + 306
    for line in wrap_text(draw, repair, font(20), 306)[:4]:
        draw.text((tx, yy), line, font=font(20), fill=COLORS["muted"])
        yy += 28


def build_detail_board(source: Image.Image) -> Image.Image:
    board = Image.new("RGB", (1920, 1080), COLORS["bg"])
    draw = ImageDraw.Draw(board)
    draw.text((58, 34), "视觉粗糙来源 · 四个局部拆解", font=font(46, True), fill=COLORS["paper"])
    draw.text((60, 96), "目标不是增加装饰，而是让每一层有明确职责和接触关系", font=font(25), fill=COLORS["muted"])

    detail_panel(
        board,
        source,
        (58, 150),
        (470, 170, 500, 310),
        "1",
        "选中证据簇",
        "照片白框、便签、Eye、红圈、标签和连接线几乎同权；互相贴边，主次不清。",
        "保留照片为主证据；Eye 与标签组成状态组；便签退后；红圈只做一次手批。",
        COLORS["now"],
    )
    detail_panel(
        board,
        source,
        (982, 150),
        (0, 0, 1400, 155),
        "2",
        "顶部刊头",
        "目前像软件页头：刊名、ISSUE 和提示文字只是横向排开，缺少杂志品牌锁定。",
        "用 WMW globe、刊名和 ISSUE 票签形成一组；保留留白，不把顶部做成贴纸展板。",
        COLORS["now"],
        fit_mode="contain",
    )
    detail_panel(
        board,
        source,
        (58, 620),
        (0, 770, 1920, 310),
        "3",
        "纸层与夹具",
        "Schedule 与 Dossier 都是平整白纸加均匀阴影，夹具与纸面没有压住、翘起或遮挡关系。",
        "各自只加 2–3 层背页和一处可信接触；Schedule 更像票据，Dossier 更像正式简报。",
        COLORS["now"],
        image_override=paper_contact_composite(source, (500, 394)),
    )
    detail_panel(
        board,
        source,
        (982, 620),
        (20, 140, 405, 670),
        "4",
        "地区卡",
        "三张卡像同一后台列表行换图，纸角、印章、编号和状态缺少可控的同族差异。",
        "先等比例合同关闭；之后只改前壳层次和状态偏移，不改图片、文字槽和热区。",
        COLORS["wait"],
    )

    return board


def build() -> Iterable[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    VIZ_DIR.mkdir(parents=True, exist_ok=True)

    source = Image.open(SOURCE).convert("RGB")
    if source.size != (1920, 1080):
        raise ValueError(f"unexpected source size: {source.size}")

    canvas = Image.new("RGB", (2560, 1440), COLORS["bg"])
    draw = ImageDraw.Draw(canvas)
    screenshot_origin = (40, 180)
    canvas.paste(source, screenshot_origin)

    draw.text((42, 30), "世界地图真实界面 · 视觉返修分区", font=font(48, True), fill=COLORS["paper"])
    draw.text((44, 96), "只修完成度，不重开功能合同，不进入 Godot", font=font(27), fill=COLORS["muted"])

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ox, oy = screenshot_origin

    draw_zone(overlay, (ox + 500, oy + 190, 380, 235), COLORS["now"], "1", "证据簇疏理")
    draw_zone(overlay, (ox + 20, oy + 8, 1372, 126), COLORS["now"], "2", "刊头锁定", (ox + 960, oy + 35))
    draw_zone(overlay, (ox + 22, oy + 798, 400, 268), COLORS["now"], "3", "纸层接触", (ox + 50, oy + 816))
    draw_zone(overlay, (ox + 1405, oy + 6, 492, 1058), COLORS["now"], "3", "纸层接触", (ox + 1422, oy + 985))
    draw_zone(overlay, (ox + 430, oy + 152, 964, 895), COLORS["now"], "4", "GIS 降噪", (ox + 1030, oy + 930), dash=True)
    draw_zone(overlay, (ox + 35, oy + 150, 374, 646), COLORS["wait"], "6", "地区卡待合同", (ox + 55, oy + 708), dash=True)

    od = ImageDraw.Draw(overlay, "RGBA")
    # One shared diagnostic line links the three repeated redline labels.
    red_points = [(ox + 258, oy + 319), (ox + 736, oy + 372), (ox + 1795, oy + 105)]
    od.line(red_points, fill=(*COLORS["now"], 220), width=5)
    for px, py in red_points:
        od.ellipse((px - 11, py - 11, px + 11, py + 11), fill=(*COLORS["now"], 255), outline=COLORS["paper"], width=3)
    rounded_label(od, (ox + 945, oy + 270), "5", "红线只留主位", COLORS["now"])

    # Freeze tags are deliberately small: these areas are evidence, not repair targets.
    freeze_tags = [
        (ox + 940, oy + 675, "大陆母图冻结"),
        (ox + 1455, oy + 430, "canonical 图冻结"),
        (ox + 1460, oy + 955, "CTA / HitRect 冻结"),
        (ox + 1110, oy + 425, "Eye 状态族冻结"),
    ]
    for x, y, text_value in freeze_tags:
        tw = od.textbbox((0, 0), text_value, font=font(21, True))[2]
        od.rounded_rectangle((x, y, x + tw + 30, y + 38), radius=3, fill=(*COLORS["bg"], 220), outline=(*COLORS["freeze"], 255), width=3)
        od.text((x + 14, y + 7), text_value, font=font(21, True), fill=COLORS["paper"])

    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    draw.text((2000, 34), "执行边界", font=font(40, True), fill=COLORS["paper"])
    draw.text((2002, 92), "红：现在修  黄：等合同  绿：冻结", font=font(22), fill=COLORS["muted"])

    y = 180
    y = issue_card(draw, y, "1", "选中证据簇", "把照片、便签、Eye、标签、红圈分成前中后三层，先恢复净距。", COLORS["now"], "现在修")
    y = issue_card(draw, y, "2", "顶部刊头", "补足 WMW globe、ISSUE 票签与刊名锁定，但不先裁生产资源。", COLORS["now"], "现在修")
    y = issue_card(draw, y, "3", "纸层接触", "Schedule 与 Dossier 分别建立背页、夹具、胶带和接触阴影，避免复制感。", COLORS["now"], "现在修")
    y = issue_card(draw, y, "4", "地图底板", "网格和长连线退后约一档，让地图重新像编辑证据板而非 GIS 软件。", COLORS["now"], "现在修")
    y = issue_card(draw, y, "5", "红线状态", "只设一个主承载位，其余两处降级为线索或删除，避免三处同权。", COLORS["now"], "现在修")
    y = issue_card(draw, y, "6", "左侧地区卡", "先关闭 2:1 与 86:41 比例冲突，再重做正式前壳；当前只诊断。", COLORS["wait"], "等待")

    draw.rounded_rectangle((2000, 1138, 2518, 1260), radius=5, fill=COLORS["panel"], outline=COLORS["freeze"], width=3)
    draw.text((2020, 1156), "冻结区", font=font(27, True), fill=COLORS["paper"])
    freeze_lines = ["大陆低多边形母图与三张新闻图", "Eye 状态族、CTA 五态与 hit rect", "现有综合色彩与 UFO 趣味剂量"]
    for idx, line in enumerate(freeze_lines):
        draw.text((2020, 1194 + idx * 25), f"· {line}", font=font(18), fill=COLORS["muted"])

    out = OUT_DIR / "01-visual-refinement-zone-map.png"
    canvas.save(out, optimize=True)

    detail_board = build_detail_board(source)
    detail_out = OUT_DIR / "02-visual-roughness-detail-board.png"
    detail_board.save(detail_out, optimize=True)

    viz_jpg = VIZ_DIR / "world-map-refinement-zones.jpg"
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(viz_jpg, quality=84, optimize=True)
    detail_viz_jpg = VIZ_DIR / "world-map-refinement-details.jpg"
    detail_board.resize((1280, 720), Image.Resampling.LANCZOS).save(detail_viz_jpg, quality=84, optimize=True)
    return [out, detail_out, viz_jpg, detail_viz_jpg]


if __name__ == "__main__":
    for path in build():
        print(path)
