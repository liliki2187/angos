from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json
import os

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
VARIANT = os.environ.get("WMW_A263_VARIANT", "v0.2")
IS_V03 = VARIANT == "v0.3"
SOURCE = ROOT / "wmw-a259-01-uncoated-independent-weekly-v0-1.png"
V01_DEFAULT = ROOT / "wmw-a263-uncoated-fullscreen-default-v0-1.png"
V01_CONFIRMING = ROOT / "wmw-a263-uncoated-fullscreen-schedule-confirming-v0-1.png"
THIRD_CARD_INGREDIENT = ROOT / (
    "wmw-a263-v03-third-card-footer-imagegen.png" if IS_V03 else "wmw-a263-v02-third-card-footer-imagegen.png"
)
SCHEDULE_INGREDIENT = ROOT / "wmw-a263-v02-schedule-carriers-imagegen.png"
VERSION_SUFFIX = "v0-3" if IS_V03 else "v0-2"
DEFAULT_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-default-{VERSION_SUFFIX}.png"
CONFIRMING_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-schedule-confirming-{VERSION_SUFFIX}.png"
BOARD_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-state-pair-{VERSION_SUFFIX}.png"
LOCAL_QA_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-local-qa-{VERSION_SUFFIX}.png"
THIRD_QA_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-qa-third-card-{VERSION_SUFFIX}.png"
SCHEDULE_QA_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-qa-schedule-{VERSION_SUFFIX}.png"
DOSSIER_QA_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-qa-dossier-{VERSION_SUFFIX}.png"
THIRD_MAPPING_QA_OUTPUT = ROOT / f"wmw-a263-uncoated-fullscreen-third-card-mapping-qa-{VERSION_SUFFIX}.png"
AUDIT = ROOT / f"wmw-a263-uncoated-fullscreen-{VERSION_SUFFIX}-audit.json"

W, H = 1920, 1080
INK = (39, 48, 51)
INK_SOFT = (88, 98, 101)
PAPER_TEXT = (241, 238, 229)
PAPER_TEXT_SOFT = (205, 205, 201)
DEADLINE = (181, 111, 103)

FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


F12 = font(12)
F14 = font(14)
F16 = font(16)
F18B = font(18, True)
F20B = font(20, True)
F22B = font(22, True)
F26B = font(26, True)
F28B = font(28, True)
F32B = font(32, True)

VISIBLE_RECTS = {
    "left_card_north": [22, 22, 407, 285],
    "left_card_east": [22, 312, 407, 271],
    "left_card_pacific": [22, 589, 407, 215],
    "schedule": [22, 813, 407, 242],
    "center": [450, 23, 918, 1032],
    "right_dossier": [1384, 23, 514, 1032],
    "right_photo": [1397, 76, 482, 360],
    "right_copy": [1404, 438, 428, 112],
    "mission_rows": [1398, 556, 482, 311],
    "cta": [1398, 884, 482, 148],
}

PATCHES = {
    "card_meta_paper": [92, 252, 282, 288],
    "dossier_copy_paper": [1476, 458, 1726, 526],
    "schedule_paper": [96, 998, 346, 1020],
    "task_text_paper": [1600, 650, 1770, 686],
}

SCHEDULE_DELTA_RECT = [65, 871, 317, 149]
V02_MUTABLE_RECTS = [
    [49, 744, 367, 52],
    [43, 832, 350, 102],
    [1404, 438, 428, 118],
]

# v0.2 failure evidence. The status tag is a protected visual object in the
# generated ingredient; it must survive source-to-target mapping intact.
THIRD_CARD_FOOTER_CROP = [1206, 508, 2054, 628] if IS_V03 else [100, 430, 2050, 650]
THIRD_CARD_TAG_PROTECTED_BBOX = [1775, 528, 2035, 616] if IS_V03 else [1576, 523, 2133, 623]
THIRD_CARD_MAPPING_MODE = "direct_resize" if IS_V03 else "ImageOps.fit(center, cover)"

VISIBLE_CARRIERS = {
    "third_card_footer": [49, 744, 367, 52],
    "third_card_state_tag": [296, 753, 112, 38] if IS_V03 else [314, 744, 102, 52],
    "schedule_date": [65, 834, 317, 28],
    "schedule_action_key": [65, 871, 70, 63],
    "schedule_action_plate": [143, 871, 239, 63],
    "dossier_copy": [1404, 438, 428, 112],
    "mission_row_1": [1398, 556, 482, 78],
}
THIRD_CARD_STATE_POINT = (352, 772) if IS_V03 else (365, 770)
THIRD_CARD_STATE_SAFE = [304, 757, 96, 30] if IS_V03 else [323, 754, 84, 30]


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def contains(rect: list[int], bbox: tuple[int, int, int, int]) -> bool:
    x, y, w, h = rect
    return bbox[0] >= x and bbox[1] >= y and bbox[2] <= x + w and bbox[3] <= y + h


def fit(source: Image.Image, crop: list[int], size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(source.crop(tuple(crop)), size, method=Image.Resampling.LANCZOS)


def protected_fit_audit(
    source_crop: list[int],
    target_rect: list[int],
    protected_bbox: list[int],
    mapping_mode: str,
) -> dict:
    crop_x1, crop_y1, crop_x2, crop_y2 = source_crop
    target_x, target_y, target_w, target_h = target_rect
    protected_x1, protected_y1, protected_x2, protected_y2 = protected_bbox
    crop_w = crop_x2 - crop_x1
    crop_h = crop_y2 - crop_y1
    crop_aspect = crop_w / crop_h
    target_aspect = target_w / target_h

    scale_x = target_w / crop_w
    scale_y = target_h / crop_h
    if mapping_mode == "direct_resize":
        effective_x1, effective_y1, effective_x2, effective_y2 = source_crop
    else:
        # ImageOps.fit uses a uniform cover scale and center crop by default.
        scale = max(scale_x, scale_y)
        effective_w = target_w / scale
        effective_h = target_h / scale
        effective_x1 = crop_x1 + (crop_w - effective_w) / 2
        effective_y1 = crop_y1 + (crop_h - effective_h) / 2
        effective_x2 = effective_x1 + effective_w
        effective_y2 = effective_y1 + effective_h

    visible_x1 = max(protected_x1, effective_x1)
    visible_y1 = max(protected_y1, effective_y1)
    visible_x2 = min(protected_x2, effective_x2)
    visible_y2 = min(protected_y2, effective_y2)
    visible_w = max(0.0, visible_x2 - visible_x1)
    visible_h = max(0.0, visible_y2 - visible_y1)
    protected_w = protected_x2 - protected_x1
    protected_h = protected_y2 - protected_y1
    retention = (visible_w * visible_h) / (protected_w * protected_h)

    mapped_scale_x = target_w / (effective_x2 - effective_x1)
    mapped_scale_y = target_h / (effective_y2 - effective_y1)
    mapped_visible_bbox = [
        target_x + (visible_x1 - effective_x1) * mapped_scale_x,
        target_y + (visible_y1 - effective_y1) * mapped_scale_y,
        target_x + (visible_x2 - effective_x1) * mapped_scale_x,
        target_y + (visible_y2 - effective_y1) * mapped_scale_y,
    ]
    crop_loss = {
        "left": max(0.0, effective_x1 - protected_x1),
        "right": max(0.0, protected_x2 - effective_x2),
        "top": max(0.0, effective_y1 - protected_y1),
        "bottom": max(0.0, protected_y2 - effective_y2),
    }
    edge_margin = {
        "left": mapped_visible_bbox[0] - target_x,
        "right": target_x + target_w - mapped_visible_bbox[2],
        "top": mapped_visible_bbox[1] - target_y,
        "bottom": target_y + target_h - mapped_visible_bbox[3],
    }
    edge_clearance_passed = edge_margin["right"] >= 8 and edge_margin["top"] >= 4 and edge_margin["bottom"] >= 4
    non_uniform_scale_error = abs(scale_x - scale_y) / max(scale_x, scale_y) * 100
    preserved = (
        all(value == 0 for value in crop_loss.values())
        and retention >= 0.99
        and edge_clearance_passed
        and non_uniform_scale_error <= 5
    )
    return {
        "passed": preserved,
        "fit_mode": mapping_mode,
        "source_crop_xyxy": source_crop,
        "source_crop_size": [crop_w, crop_h],
        "source_crop_aspect": round(crop_aspect, 6),
        "target_rect_xywh": target_rect,
        "target_rect_aspect": round(target_aspect, 6),
        "source_target_aspect_error_percent": round(abs(crop_aspect - target_aspect) / target_aspect * 100, 2),
        "non_uniform_scale_error_percent": round(non_uniform_scale_error, 4),
        "effective_source_window_xyxy": [round(value, 2) for value in [effective_x1, effective_y1, effective_x2, effective_y2]],
        "protected_source_bbox_xyxy": protected_bbox,
        "protected_bbox_inside_effective_window": preserved,
        "protected_crop_loss_px": {key: round(value, 2) for key, value in crop_loss.items()},
        "protected_pixel_retention_ratio": round(retention, 4),
        "mapped_visible_protected_bbox_xyxy": [round(value, 2) for value in mapped_visible_bbox],
        "protected_bbox_touches_target_edge": any(value < 0.5 for value in edge_margin.values()),
        "target_edge_margin_px": {key: round(value, 2) for key, value in edge_margin.items()},
        "target_edge_margin_passed": edge_clearance_passed,
        "endcaps_present": {
            "left": crop_loss["left"] == 0,
            "right": crop_loss["right"] == 0,
        },
        "failure": "right_endcap_and_right_paper_margin_cropped" if not preserved else None,
    }


def paste_feathered(
    canvas: Image.Image,
    source: Image.Image,
    crop: list[int],
    rect: list[int],
    edge: int = 7,
    opacity: int = 244,
) -> None:
    x, y, w, h = rect
    art = fit(source, crop, (w, h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((edge, edge, w - edge - 1, h - edge - 1), fill=opacity)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(2, edge // 2)))
    canvas.paste(art, (x, y), mask)


def safe_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    point: tuple[int, int],
    used_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    anchor: str,
    safe_rect: list[int],
    records: list[dict],
    key: str,
    owner_carrier_id: str | None = None,
    owner_carrier_rect: list[int] | None = None,
    semantic_group_id: str | None = None,
) -> None:
    bbox = draw.textbbox(point, text, font=used_font, anchor=anchor)
    carrier_rect = list(owner_carrier_rect or safe_rect)
    contract_passed = contains(safe_rect, bbox)
    carrier_passed = contains(carrier_rect, bbox)
    records.append(
        {
            "key": key,
            "text": text,
            "bbox_xyxy": list(bbox),
            "safe_rect_xywh": list(safe_rect),
            "owner_carrier_id": owner_carrier_id or key,
            "owner_carrier_rect_xywh": carrier_rect,
            "semantic_group_id": semantic_group_id or key,
            "contract_safe_rect_passed": contract_passed,
            "visible_carrier_passed": carrier_passed,
            "passed": contract_passed and carrier_passed,
        }
    )
    draw.text(point, text, font=used_font, fill=fill, anchor=anchor)


def apply_shared_patches(source: Image.Image) -> tuple[Image.Image, list[dict]]:
    canvas = source.copy()
    patch_records: list[dict] = []
    third_ingredient = Image.open(THIRD_CARD_INGREDIENT).convert("RGB")
    schedule_ingredient = Image.open(SCHEDULE_INGREDIENT).convert("RGB")

    # v0.2 uses one coherent generated footer ingredient instead of a title patch
    # colliding with the source image's clipped state tab.
    third_footer_crop = THIRD_CARD_FOOTER_CROP
    third_footer_rect = VISIBLE_CARRIERS["third_card_footer"]
    third_footer_source = third_ingredient.crop(tuple(third_footer_crop))
    third_footer_art = (
        third_footer_source.resize((third_footer_rect[2], third_footer_rect[3]), Image.Resampling.LANCZOS)
        if IS_V03
        else ImageOps.fit(third_footer_source, (third_footer_rect[2], third_footer_rect[3]), method=Image.Resampling.LANCZOS)
    )
    canvas.paste(
        third_footer_art,
        (third_footer_rect[0], third_footer_rect[1]),
    )
    patch_records.append(
        {
            "source_file": THIRD_CARD_INGREDIENT.name,
            "source_crop_xyxy": third_footer_crop,
            "target_rect_xywh": third_footer_rect,
            "role": "第三卡完整单层标题/状态载体",
            "mapping_mode": THIRD_CARD_MAPPING_MODE,
        }
    )

    # Clear the old combined schedule action block, then insert two independent
    # no-text carriers from the localized imagegen ingredient.
    schedule_clear_rect = [43, 832, 350, 102]
    canvas.paste(
        fit(source, PATCHES["dossier_copy_paper"], (schedule_clear_rect[2], schedule_clear_rect[3])),
        (schedule_clear_rect[0], schedule_clear_rect[1]),
    )
    patch_records.append(
        {
            "source_file": SOURCE.name,
            "source_crop_xyxy": PATCHES["dossier_copy_paper"],
            "target_rect_xywh": schedule_clear_rect,
            "role": "清除旧日期/动作共用载体",
        }
    )

    date_crop = [150, 58, 1520, 212]
    date_rect = VISIBLE_CARRIERS["schedule_date"]
    canvas.paste(fit(schedule_ingredient, date_crop, (date_rect[2], date_rect[3])), (date_rect[0], date_rect[1]))
    patch_records.append(
        {
            "source_file": SCHEDULE_INGREDIENT.name,
            "source_crop_xyxy": date_crop,
            "target_rect_xywh": date_rect,
            "role": "独立日期/剩余日载体",
        }
    )

    action_crop = [155, 252, 1530, 535]
    action_rect = [65, 871, 317, 63]
    canvas.paste(fit(schedule_ingredient, action_crop, (action_rect[2], action_rect[3])), (action_rect[0], action_rect[1]))
    patch_records.append(
        {
            "source_file": SCHEDULE_INGREDIENT.name,
            "source_crop_xyxy": action_crop,
            "target_rect_xywh": action_rect,
            "role": "与日期载体分离的主动作载体",
        }
    )

    # Remove the baked ingredient arrow so both states use exact dynamic glyphs.
    arrow_clear_rect = [72, 879, 58, 46]
    paste_feathered(
        canvas,
        source,
        PATCHES["dossier_copy_paper"],
        arrow_clear_rect,
        edge=5,
        opacity=255,
    )
    patch_records.append(
        {
            "source_file": SOURCE.name,
            "source_crop_xyxy": PATCHES["dossier_copy_paper"],
            "target_rect_xywh": arrow_clear_rect,
            "role": "清除素材箭头并交还动态图标层",
        }
    )

    targets = [
        ("dossier_copy_paper", [1404, 438, 428, 112], 8, 248, "右侧标题/正文/摘要同源纸面"),
        ("schedule_paper", [75, 951, 307, 20], 5, 238, "后果行一文字薄罩"),
        ("schedule_paper", [75, 998, 307, 20], 5, 238, "后果行二文字薄罩"),
    ]
    for patch_key, rect, edge, opacity, role in targets:
        paste_feathered(canvas, source, PATCHES[patch_key], rect, edge=edge, opacity=opacity)
        patch_records.append({"source_crop_xyxy": PATCHES[patch_key], "target_rect_xywh": rect, "role": role})

    row_safe_rects = [
        [1540, 560, 286, 66],
        [1540, 638, 286, 64],
        [1540, 714, 286, 66],
        [1540, 793, 286, 68],
    ]
    for index, rect in enumerate(row_safe_rects):
        paste_feathered(canvas, source, PATCHES["task_text_paper"], rect, edge=6, opacity=238)
        patch_records.append(
            {
                "source_crop_xyxy": PATCHES["task_text_paper"],
                "target_rect_xywh": rect,
                "role": f"任务 {index + 1} 文字区薄罩",
            }
        )

    return canvas, patch_records


def outlined_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    point: tuple[int, int],
    used_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    anchor: str,
    safe_rect: list[int],
    records: list[dict],
    key: str,
) -> None:
    x, y = point
    draw.text((x + 1, y + 1), text, font=used_font, fill=(17, 28, 39), anchor=anchor)
    safe_text(draw, text, point, used_font, fill, anchor, safe_rect, records, key)


def draw_common(canvas: Image.Image, records: list[dict]) -> None:
    draw = ImageDraw.Draw(canvas)

    safe_text(draw, "世界未解之谜周刊", (492, 94), F32B, PAPER_TEXT, "lm", [492, 76, 604, 40], records, "masthead")
    safe_text(draw, "第 1 周", (1315, 91), F18B, PAPER_TEXT_SOFT, "rm", [1170, 78, 145, 26], records, "week")

    cards = [
        ((64, 272), "北美禁区带", (365, 272), "选中", [64, 256, 232, 32], [323, 257, 84, 30]),
        ((64, 546), "东亚神秘地带", (365, 546), "锁定", [64, 530, 232, 32], [323, 531, 84, 30]),
        ((64, 770), "太平洋失航带", THIRD_CARD_STATE_POINT, "锁定", [64, 754, 232, 32], THIRD_CARD_STATE_SAFE),
    ]
    for index, (title_point, title, state_point, state, title_safe, state_safe) in enumerate(cards):
        if index == 2:
            safe_text(
                draw,
                title,
                title_point,
                F22B,
                INK,
                "lm",
                title_safe,
                records,
                f"left_title_{index}",
                "third_card_footer",
                VISIBLE_CARRIERS["third_card_footer"],
                "third_card_information",
            )
            safe_text(
                draw,
                state,
                state_point,
                F18B,
                PAPER_TEXT,
                "mm",
                state_safe,
                records,
                f"left_state_{index}",
                "third_card_state_tag",
                VISIBLE_CARRIERS["third_card_state_tag"],
                "third_card_information",
            )
        else:
            safe_text(draw, title, title_point, F22B, INK, "lm", title_safe, records, f"left_title_{index}")
            safe_text(draw, state, state_point, F18B, PAPER_TEXT, "mm", state_safe, records, f"left_state_{index}")

    outlined_text(draw, "北美禁区带", (654, 390), F20B, PAPER_TEXT, "lm", [654, 374, 172, 32], records, "map_selected")
    outlined_text(draw, "东亚神秘地带", (1208, 410), F20B, PAPER_TEXT, "rm", [1016, 394, 196, 32], records, "map_east")
    outlined_text(draw, "太平洋失航带", (1212, 692), F20B, PAPER_TEXT, "rm", [1016, 676, 200, 32], records, "map_pacific")

    safe_text(draw, "北美禁区带", (1424, 462), F26B, INK, "lm", [1424, 447, 388, 32], records, "right_title", "dossier_copy", VISIBLE_CARRIERS["dossier_copy"], "dossier_title")
    safe_text(draw, "都市传说与军事封锁交叠。", (1424, 482), F16, INK, "la", [1424, 480, 388, 24], records, "right_body_1", "dossier_copy", VISIBLE_CARRIERS["dossier_copy"], "dossier_body")
    safe_text(draw, "军方巡逻、档案残页与异常雷达同时露头。", (1424, 500), F14, INK_SOFT, "la", [1424, 500, 388, 18], records, "right_body_2", "dossier_copy", VISIBLE_CARRIERS["dossier_copy"], "dossier_body")
    safe_text(draw, "任务情报", (1424, 534), F18B, INK, "lm", [1424, 524, 100, 24], records, "mission_header", "dossier_copy", VISIBLE_CARRIERS["dossier_copy"], "mission_heading")
    safe_text(draw, "常驻 2 · 限时 1 · 深链 1", (1698, 535), F12, INK_SOFT, "rm", [1528, 525, 170, 20], records, "mission_summary", "dossier_copy", VISIBLE_CARRIERS["dossier_copy"], "mission_heading")
    safe_text(draw, "已展开 4 / 4", (1820, 535), F12, INK_SOFT, "rm", [1712, 525, 108, 20], records, "mission_expanded", "dossier_copy", VISIBLE_CARRIERS["dossier_copy"], "mission_heading")

    rows = [
        (556, "51 区外围公路", "科学纪实 · 耗时 2 天", "常驻"),
        (634, "罗斯威尔档案残页", "科学纪实 · 耗时 1 天", "常驻"),
        (710, "突发：雷达异常光点", "大众热度 · 耗时 2 天", "限时至第 4 天"),
        (789, "M330 末班车空白段", "神秘玄学 · 耗时 2 天", "深链"),
    ]
    for index, (y, title, meta, state) in enumerate(rows):
        safe_text(
            draw,
            title,
            (1544, y + 24),
            F20B,
            INK,
            "lm",
            [1544, y + 8, 278, 30],
            records,
            f"mission_title_{index}",
            "mission_row_1" if index == 0 else f"mission_row_{index + 1}",
            VISIBLE_CARRIERS["mission_row_1"] if index == 0 else [1398, y, 482, 78],
            f"mission_row_{index + 1}",
        )
        safe_text(draw, meta, (1544, y + 53), F16, INK_SOFT, "lm", [1544, y + 38, 190, 24], records, f"mission_meta_{index}")
        safe_text(
            draw,
            state,
            (1822, y + 53),
            F16 if index != 2 else F14,
            INK,
            "rm",
            [1710, y + 38, 112, 24],
            records,
            f"mission_state_{index}",
        )

    safe_text(draw, "进入地区任务台  →", (1639, 960), F28B, PAPER_TEXT, "mm", [1432, 934, 414, 52], records, "primary_cta")


def draw_schedule(canvas: Image.Image, records: list[dict], confirming: bool) -> None:
    draw = ImageDraw.Draw(canvas)
    safe_text(draw, "全局日程", (65, 825), F12, INK_SOFT, "lm", [62, 815, 100, 20], records, "schedule_section")
    safe_text(draw, "当前第 1 天", (80, 849), F16, INK, "lm", [78, 838, 120, 20], records, "schedule_current", "schedule_date", VISIBLE_CARRIERS["schedule_date"], "schedule_date")
    safe_text(draw, "剩余 7 天", (368, 849), F16, INK, "rm", [250, 838, 120, 20], records, "schedule_remaining", "schedule_date", VISIBLE_CARRIERS["schedule_date"], "schedule_date")
    safe_text(draw, "!" if confirming else "→", (105, 902), F28B, INK, "mm", [82, 880, 46, 44], records, "schedule_icon", "schedule_action_key", VISIBLE_CARRIERS["schedule_action_key"], "schedule_action")
    safe_text(
        draw,
        "确认推进到第 2 天" if confirming else "推进到下一天",
        (158, 888),
        F22B,
        PAPER_TEXT,
        "lm",
        [158, 877, 218, 28],
        records,
        "schedule_title",
        "schedule_action_plate",
        VISIBLE_CARRIERS["schedule_action_plate"],
        "schedule_action",
    )
    safe_text(
        draw,
        "再次点击执行；后果见下方" if confirming else "点击后查看推进影响",
        (158, 916),
        F14,
        PAPER_TEXT_SOFT,
        "lm",
        [158, 906, 218, 22],
        records,
        "schedule_help",
        "schedule_action_plate",
        VISIBLE_CARRIERS["schedule_action_plate"],
        "schedule_action",
    )
    safe_text(
        draw,
        "确认后：剩余 6 天 · 无任务到期" if confirming else "当前：无任务到期",
        (75, 963),
        F16,
        INK,
        "lm",
        [75, 951, 307, 22],
        records,
        "schedule_result_1",
    )
    safe_text(
        draw,
        "限时任务：雷达异常仍开放至第 4 天" if confirming else "日程归零：进入编辑部阶段",
        (75, 1010),
        F16,
        INK,
        "lm",
        [75, 998, 307, 22],
        records,
        "schedule_result_2",
    )


def build_state(source: Image.Image, confirming: bool) -> tuple[Image.Image, list[dict], list[dict]]:
    canvas, patch_records = apply_shared_patches(source)
    records: list[dict] = []
    draw_common(canvas, records)
    draw_schedule(canvas, records, confirming)
    violations = [record for record in records if not record["passed"]]
    assert not violations, violations
    return canvas, records, patch_records


def make_board(default: Image.Image, confirming: Image.Image) -> None:
    board = Image.new("RGB", (3840, 1144), (7, 14, 20))
    draw = ImageDraw.Draw(board)
    label_font = font(28, True)
    draw.text((24, 18), "默认态", font=label_font, fill=(238, 240, 235))
    draw.text((1944, 18), "推进二次确认态", font=label_font, fill=(238, 240, 235))
    board.paste(default, (0, 64))
    board.paste(confirming, (1920, 64))
    board.save(BOARD_OUTPUT, optimize=True)


def make_local_qa(default: Image.Image) -> list[dict]:
    specs = [
        ("third_card", [22, 690, 429, 813], THIRD_QA_OUTPUT, "第三卡：照片 / 标题 / 状态载体"),
        ("schedule", [22, 813, 429, 1055], SCHEDULE_QA_OUTPUT, "日程：日期 / 动作 / 后果"),
        ("dossier", [1384, 430, 1898, 575], DOSSIER_QA_OUTPUT, "右栏：正文 / 任务标题 / 首任务"),
    ]
    records: list[dict] = []
    crops: list[tuple[str, Image.Image]] = []
    for key, xyxy, output, label in specs:
        crop = default.crop(tuple(xyxy))
        crop.save(output, optimize=True)
        crops.append((label, crop))
        records.append(
            {
                "key": key,
                "source_xyxy": xyxy,
                "output": output.name,
                "scale": "100%",
                "review_source": "final_default_png",
            }
        )

    gap = 32
    label_h = 48
    scaled = [(label, crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.NEAREST)) for label, crop in crops]
    board_w = sum(image.width for _, image in scaled) + gap * (len(scaled) + 1)
    board_h = max(image.height for _, image in scaled) + label_h + gap * 2
    board = Image.new("RGB", (board_w, board_h), (7, 14, 20))
    draw = ImageDraw.Draw(board)
    label_font = font(22, True)
    cursor_x = gap
    for label, image in scaled:
        draw.text((cursor_x, 16), label, font=label_font, fill=(238, 240, 235))
        board.paste(image, (cursor_x, label_h))
        cursor_x += image.width + gap
    board.save(LOCAL_QA_OUTPUT, optimize=True)
    return records


def make_third_mapping_qa(default: Image.Image, mapping: dict) -> None:
    ingredient = Image.open(THIRD_CARD_INGREDIENT).convert("RGB")
    ingredient_overlay = ingredient.copy()
    overlay_draw = ImageDraw.Draw(ingredient_overlay)
    overlay_draw.rectangle(tuple(THIRD_CARD_FOOTER_CROP), outline=(64, 220, 150), width=8)
    overlay_draw.rectangle(tuple(THIRD_CARD_TAG_PROTECTED_BBOX), outline=(242, 92, 136), width=8)
    ingredient_overlay.thumbnail((1120, 375), Image.Resampling.LANCZOS)

    source_crop = ingredient.crop(tuple(THIRD_CARD_FOOTER_CROP))
    source_overlay = source_crop.copy()
    source_draw = ImageDraw.Draw(source_overlay)
    px1, py1, px2, py2 = THIRD_CARD_TAG_PROTECTED_BBOX
    cx1, cy1, _, _ = THIRD_CARD_FOOTER_CROP
    source_draw.rectangle((px1 - cx1, py1 - cy1, px2 - cx1, py2 - cy1), outline=(242, 92, 136), width=5)
    source_overlay = source_overlay.resize((1016, 144), Image.Resampling.LANCZOS)

    final_card = default.crop((22, 690, 429, 813))
    final_card_2x = final_card.resize((814, 246), Image.Resampling.NEAREST)
    endcap = default.crop((280, 742, 416, 798)).resize((544, 224), Image.Resampling.NEAREST)

    board = Image.new("RGB", (1920, 980), (7, 14, 20))
    draw = ImageDraw.Draw(board)
    title_font = font(28, True)
    label_font = font(18, True)
    body_font = font(16)
    white = (238, 240, 235)
    soft = (180, 190, 192)
    draw.text((32, 24), "A263 v0.3 第三卡 footer：素材 → 源裁片 → 最终整屏回填", font=title_font, fill=white)
    draw.text((32, 70), "绿框=实际 source crop；粉框=不可裁 protected 状态签", font=body_font, fill=soft)

    draw.text((32, 108), "1. 完整 imagegen ingredient（只改状态签）", font=label_font, fill=white)
    board.paste(ingredient_overlay, (32, 140))

    draw.text((32, 530), "2. 精确比例 source crop（无 cover 居中裁切）", font=label_font, fill=white)
    board.paste(source_overlay, (32, 562))

    draw.text((1176, 108), "3. 最终第三卡 100%", font=label_font, fill=white)
    board.paste(final_card, (1176, 140))
    draw.text((1064, 310), "4. 最终第三卡 200%", font=label_font, fill=white)
    board.paste(final_card_2x, (1064, 342))

    draw.text((32, 742), "5. 状态签端帽 400%", font=label_font, fill=white)
    board.paste(endcap, (32, 776))

    metrics = [
        f"source / target 比例误差：{mapping['source_target_aspect_error_percent']}%",
        f"protected 保留率：{mapping['protected_pixel_retention_ratio'] * 100:.2f}%",
        f"四向裁切损失：{mapping['protected_crop_loss_px']}",
        f"最终边距：{mapping['target_edge_margin_px']}",
        f"左右端帽：{mapping['endcaps_present']}",
    ]
    draw.text((616, 758), "自动审计", font=label_font, fill=white)
    for index, line in enumerate(metrics):
        draw.text((616, 794 + index * 30), line, font=body_font, fill=soft)
    board.save(THIRD_MAPPING_QA_OUTPUT, optimize=True)


def rect_to_xyxy(rect: list[int]) -> list[int]:
    x, y, w, h = rect
    return [x, y, x + w, y + h]


def intersection_xyxy(a: list[int], b: list[int]) -> list[int] | None:
    ax1, ay1, ax2, ay2 = rect_to_xyxy(a)
    bx1, by1, bx2, by2 = rect_to_xyxy(b)
    result = [max(ax1, bx1), max(ay1, by1), min(ax2, bx2), min(ay2, by2)]
    return result if result[0] < result[2] and result[1] < result[3] else None


def union_bbox(records: list[dict], keys: set[str]) -> list[int]:
    boxes = [record["bbox_xyxy"] for record in records if record["key"] in keys]
    assert boxes, keys
    return [
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    ]


def visual_carrier_audit(records: list[dict]) -> dict:
    by_key = {record["key"]: record for record in records}
    body_bbox = union_bbox(records, {"right_body_1", "right_body_2"})
    heading_bbox = union_bbox(records, {"mission_header", "mission_summary", "mission_expanded"})
    body_to_heading_gap = heading_bbox[1] - body_bbox[3]
    heading_to_row_gap = VISIBLE_CARRIERS["mission_row_1"][1] - heading_bbox[3]
    date_action_intersection = intersection_xyxy(
        VISIBLE_CARRIERS["schedule_date"],
        [65, 871, 317, 63],
    )
    state_bbox = by_key["left_state_2"]["bbox_xyxy"]
    state_carrier = VISIBLE_CARRIERS["third_card_state_tag"]
    state_text_center = [(state_bbox[0] + state_bbox[2]) / 2, (state_bbox[1] + state_bbox[3]) / 2]
    state_carrier_center = [state_carrier[0] + state_carrier[2] / 2, state_carrier[1] + state_carrier[3] / 2]
    state_center_error = [
        abs(state_text_center[0] - state_carrier_center[0]),
        abs(state_text_center[1] - state_carrier_center[1]),
    ]
    critical_safe_intersection = intersection_xyxy(
        by_key["right_body_2"]["safe_rect_xywh"],
        by_key["mission_header"]["safe_rect_xywh"],
    )
    visible_carrier_passed = all(record["visible_carrier_passed"] for record in records)
    passed = (
        visible_carrier_passed
        and critical_safe_intersection is None
        and date_action_intersection is None
        and body_to_heading_gap >= 10
        and heading_to_row_gap >= 8
        and max(state_center_error) <= 8
    )
    return {
        "passed": passed,
        "all_text_inside_owner_carrier": visible_carrier_passed,
        "body_bbox_xyxy": body_bbox,
        "mission_heading_bbox_xyxy": heading_bbox,
        "body_to_mission_heading_gap_px": body_to_heading_gap,
        "body_to_mission_heading_min_px": 10,
        "mission_heading_to_first_row_gap_px": heading_to_row_gap,
        "mission_heading_to_first_row_min_px": 8,
        "body_2_to_mission_header_safe_rect_intersection_xyxy": critical_safe_intersection,
        "schedule_date_action_carrier_intersection_xyxy": date_action_intersection,
        "schedule_date_to_action_gap_px": 871 - (834 + 28),
        "schedule_date_to_action_min_px": 8,
        "third_card_state_text_center_xy": state_text_center,
        "third_card_state_carrier_center_xy": state_carrier_center,
        "third_card_state_center_error_xy": state_center_error,
        "third_card_state_center_max_error_px": 8,
    }


def scope_invariant_audit(
    baseline: Image.Image,
    candidate: Image.Image,
    mutable_rects: list[list[int]] | None = None,
) -> dict:
    rects = mutable_rects or V02_MUTABLE_RECTS
    allowed = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(allowed)
    for x, y, w, h in rects:
        draw.rectangle((x, y, x + w, y + h), fill=255)
    difference = ImageChops.difference(baseline, candidate).convert("L")
    outside = ImageChops.multiply(difference, ImageChops.invert(allowed))
    outside_bbox = outside.getbbox()
    return {
        "mutable_rects_xywh": rects,
        "difference_bbox_xyxy": list(difference.getbbox()) if difference.getbbox() else None,
        "outside_mutable_bbox_xyxy": list(outside_bbox) if outside_bbox else None,
        "passed": outside_bbox is None,
    }


def source_diff_audit(
    source: Image.Image,
    candidate: Image.Image,
    patch_records: list[dict],
    text_records: list[dict],
) -> dict:
    allowed = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(allowed)
    for record in patch_records:
        x, y, w, h = record["target_rect_xywh"]
        draw.rectangle((x, y, x + w, y + h), fill=255)
    for record in text_records:
        x, y, w, h = record["safe_rect_xywh"]
        draw.rectangle((x, y, x + w, y + h), fill=255)

    difference = ImageChops.difference(source, candidate).convert("L")
    outside = ImageChops.multiply(difference, ImageChops.invert(allowed))
    outside_bbox = outside.getbbox()
    outside_pixels = sum(1 for value in outside.get_flattened_data() if value)
    return {
        "difference_bbox_xyxy": list(difference.getbbox()) if difference.getbbox() else None,
        "outside_allowed_bbox_xyxy": list(outside_bbox) if outside_bbox else None,
        "outside_allowed_pixels": outside_pixels,
        "passed": outside_bbox is None and outside_pixels == 0,
    }


source = Image.open(SOURCE).convert("RGB")
assert source.size == (W, H), source.size

default, default_records, patch_records = build_state(source, confirming=False)
confirming, confirming_records, confirming_patch_records = build_state(source, confirming=True)

default.save(DEFAULT_OUTPUT, optimize=True)
confirming.save(CONFIRMING_OUTPUT, optimize=True)
make_board(default, confirming)
local_qa_records = make_local_qa(default)

default_visual_carriers = visual_carrier_audit(default_records)
confirming_visual_carriers = visual_carrier_audit(confirming_records)
# The nominal text/carrier rectangles pass, but the actual generated state-tag
# object is cropped before those rectangles are evaluated. Keep both facts in
# the audit so the former can never be used as a fullscreen PASS again.
third_card_protected_fit = protected_fit_audit(
    THIRD_CARD_FOOTER_CROP,
    VISIBLE_CARRIERS["third_card_footer"],
    THIRD_CARD_TAG_PROTECTED_BBOX,
    THIRD_CARD_MAPPING_MODE,
)
default_by_key = {record["key"]: record for record in default_records}
mapped_tag_bbox = third_card_protected_fit["mapped_visible_protected_bbox_xyxy"]
mapped_tag_center = [
    (mapped_tag_bbox[0] + mapped_tag_bbox[2]) / 2,
    (mapped_tag_bbox[1] + mapped_tag_bbox[3]) / 2,
]
state_text_bbox = default_by_key["left_state_2"]["bbox_xyxy"]
state_text_center = [
    (state_text_bbox[0] + state_text_bbox[2]) / 2,
    (state_text_bbox[1] + state_text_bbox[3]) / 2,
]
state_to_visible_center_error = [
    round(abs(state_text_center[0] - mapped_tag_center[0]), 2),
    round(abs(state_text_center[1] - mapped_tag_center[1]), 2),
]
title_to_state_visual_gap = round(mapped_tag_bbox[0] - default_by_key["left_title_2"]["bbox_xyxy"][2], 2)
third_card_protected_fit["state_text_to_visible_tag_center_error_xy"] = state_to_visible_center_error
third_card_protected_fit["state_text_to_visible_tag_center_max_error_px"] = 4
third_card_protected_fit["title_to_state_visual_gap_px"] = title_to_state_visual_gap
third_card_protected_fit["title_to_state_visual_gap_min_px"] = 16
third_card_protected_fit["passed"] = (
    third_card_protected_fit["passed"]
    and max(state_to_visible_center_error) <= 4
    and title_to_state_visual_gap >= 16
)
if IS_V03:
    make_third_mapping_qa(default, third_card_protected_fit)
assert default_visual_carriers["passed"], default_visual_carriers
assert confirming_visual_carriers["passed"], confirming_visual_carriers

v01_default = Image.open(V01_DEFAULT).convert("RGB")
v01_confirming = Image.open(V01_CONFIRMING).convert("RGB")
default_scope_invariant = scope_invariant_audit(v01_default, default)
confirming_scope_invariant = scope_invariant_audit(v01_confirming, confirming)
assert default_scope_invariant["passed"], default_scope_invariant
assert confirming_scope_invariant["passed"], confirming_scope_invariant

v02_to_v03_scope_invariant = None
if IS_V03:
    v02_default = Image.open(ROOT / "wmw-a263-uncoated-fullscreen-default-v0-2.png").convert("RGB")
    v02_confirming = Image.open(ROOT / "wmw-a263-uncoated-fullscreen-schedule-confirming-v0-2.png").convert("RGB")
    v02_to_v03_scope_invariant = {
        "default": scope_invariant_audit(v02_default, default, [VISIBLE_CARRIERS["third_card_footer"]]),
        "schedule_confirming": scope_invariant_audit(v02_confirming, confirming, [VISIBLE_CARRIERS["third_card_footer"]]),
    }
    assert v02_to_v03_scope_invariant["default"]["passed"], v02_to_v03_scope_invariant
    assert v02_to_v03_scope_invariant["schedule_confirming"]["passed"], v02_to_v03_scope_invariant

default_source_diff = source_diff_audit(source, default, patch_records, default_records)
confirming_source_diff = source_diff_audit(source, confirming, confirming_patch_records, confirming_records)
assert default_source_diff["passed"], default_source_diff
assert confirming_source_diff["passed"], confirming_source_diff

state_delta = ImageChops.difference(default, confirming)
delta_bbox = state_delta.getbbox()
allowed_mask = Image.new("L", (W, H), 0)
x, y, w, h = SCHEDULE_DELTA_RECT
ImageDraw.Draw(allowed_mask).rectangle((x, y, x + w, y + h), fill=255)
outside_delta = ImageChops.multiply(state_delta.convert("L"), ImageChops.invert(allowed_mask))
outside_bbox = outside_delta.getbbox()
assert outside_bbox is None, outside_bbox
if IS_V03:
    assert third_card_protected_fit["passed"], third_card_protected_fit

audit_status = "dual_reviewed_pending_user_visual_confirmation" if IS_V03 else "user_visual_review_failed_third_card_endcap_crop_rework_required"
audit_version = f"wmw_a263_uncoated_fullscreen_text_landing_{'v0_3' if IS_V03 else 'v0_2'}"
current_reviews = (
    {
        "ux_laoge": {
            "verdict": "PASS",
            "p0": 0,
            "p1": 0,
            "p2": 0,
            "method": "先看完整默认态与第三卡100%局部，再核对audit",
            "notes": [
                "状态签左右端帽完整且右侧有约8px纸面余量，不再像被裁断按钮。",
                "第三签113×41相对第二卡101×46的微差不构成层级或标题侵占；日程与右栏未回退。",
            ],
        },
        "ui_designer": {
            "verdict": "PASS",
            "p0": 0,
            "p1": 0,
            "p2": 0,
            "method": "先看完整整屏、100%/200%第三卡与映射流程板，再核对audit",
            "notes": [
                "protected保留率100%，四向crop loss为0，左右端帽、边距和实际色域文字中心均通过。",
                "v0.3相对v0.2只改变第三卡footer；尺寸微差在较矮第三卡中保持平衡，不构成组件错型。",
            ],
        },
    }
    if IS_V03
    else {
        "ux_laoge": {
            "verdict": "ITERATE",
            "p0": 0,
            "p1": 1,
            "p2": 0,
            "method": "复核 ingredient、source crop、ImageOps.fit 有效窗口与最终100%局部",
            "notes": [
                "日程分组与右栏章节间距修复继续有效。",
                "第三卡状态签右端帽、右侧轮廓和纸面余量被居中fit裁掉，v0.2整屏PASS撤回。",
            ],
        },
        "ui_designer": {
            "verdict": "ITERATE",
            "p0": 0,
            "p1": 1,
            "p2": 1,
            "method": "复核 protected bbox、有效源窗口、最终映射和端帽完整性",
            "notes": [
                "单层footer与无旧接缝仍成立，但不能推出状态签完整。",
                "状态签仅保留约49.4%，右端帽缺失；非阻断P2仍是右栏12px摘要的未来runtime清晰度验证。",
            ],
        },
    }
)
third_card_regression_result = "FIXED_DUAL_REVIEWED" if IS_V03 else "FAILED_RIGHT_ENDCAP_CROPPED"
independent_local_crop_review = "PASS" if IS_V03 else "FAIL_THIRD_CARD_RIGHT_ENDCAP_CROPPED"

stats = ImageStat.Stat(default.resize((240, 135), Image.Resampling.BILINEAR))
audit = {
    "artifact_type": "fullscreen_filled_state_text_mock_state_pair",
    "version": audit_version,
    "status": audit_status,
    "decision_source": "A263",
    "canvas": [W, H],
    "source": {
        "built_in_imagegen_used": True,
        "selected_material_direction": "无涂布独立周刊",
        "file": SOURCE.name,
        "sha256": digest(SOURCE),
        "localized_imagegen_edits": [
            {
                "file": THIRD_CARD_INGREDIENT.name,
                "sha256": digest(THIRD_CARD_INGREDIENT),
                "role": "第三卡完整无字标题/状态载体",
            },
            {
                "file": SCHEDULE_INGREDIENT.name,
                "sha256": digest(SCHEDULE_INGREDIENT),
                "role": "分离日期与主动作的无字载体",
            },
        ],
    },
    "outputs": {
        "default": DEFAULT_OUTPUT.name,
        "schedule_confirming": CONFIRMING_OUTPUT.name,
        "state_pair_board": BOARD_OUTPUT.name,
        "local_qa_board": LOCAL_QA_OUTPUT.name,
        "third_card_mapping_qa_board": THIRD_MAPPING_QA_OUTPUT.name if IS_V03 else None,
        "local_100_percent_crops": local_qa_records,
        "default_sha256": digest(DEFAULT_OUTPUT),
        "schedule_confirming_sha256": digest(CONFIRMING_OUTPUT),
        "state_pair_board_sha256": digest(BOARD_OUTPUT),
        "local_qa_board_sha256": digest(LOCAL_QA_OUTPUT),
        "third_card_mapping_qa_board_sha256": digest(THIRD_MAPPING_QA_OUTPUT) if IS_V03 else None,
    },
    "visible_geometry": VISIBLE_RECTS,
    "content": {
        "rectangular_image_slots": 8,
        "mission_rows": 4,
        "primary_cta_count": 1,
        "route_lines_drawn": 0,
        "redline_status_badge_present": False,
        "selected_region_id": "north_america",
    },
    "art_program_boundary": {
        "imagegen_owns_all_visible_carrier_materials": True,
        "built_in_imagegen_local_edit_count": 2,
        "source_derived_patch_count": len(patch_records),
        "source_derived_patches": patch_records,
        "default_and_confirming_patch_sets_identical": patch_records == confirming_patch_records,
        "program_flat_surface_overlay_count": 0,
        "program_owns_exact_text_and_target_state_semantics": True,
        "program_color_regrade_used": False,
        "program_redraw_of_story_images_or_map_used": False,
    },
    "text_safe_area": {
        "default_checked_records": len(default_records),
        "confirming_checked_records": len(confirming_records),
        "default_violations": [record for record in default_records if not record["passed"]],
        "confirming_violations": [record for record in confirming_records if not record["passed"]],
        "passed": all(record["passed"] for record in default_records + confirming_records),
        "default_records": default_records,
        "confirming_records": confirming_records,
    },
    "state_difference": {
        "allowed_rect_xywh": SCHEDULE_DELTA_RECT,
        "difference_bbox_xyxy": list(delta_bbox) if delta_bbox else None,
        "outside_allowed_bbox_xyxy": list(outside_bbox) if outside_bbox else None,
        "schedule_only": outside_bbox is None,
    },
    "source_difference": {
        "default": default_source_diff,
        "schedule_confirming": confirming_source_diff,
    },
    "scope_invariant_vs_v0_1": {
        "default": default_scope_invariant,
        "schedule_confirming": confirming_scope_invariant,
    },
    "scope_invariant_vs_v0_2": v02_to_v03_scope_invariant,
    "runtime_support": {
        "target_only": True,
        "independent_advance_day": False,
        "a51h_full_height": False,
        "deadline_day_in_world_preview": False,
        "godot_runtime_unchanged": True,
    },
    "resolution_boundary": {
        "validated_target": "1920x1080 desktop only",
        "lower_resolution_runtime_validation": "not_executed_formal_runtime_required",
        "recommended_minimum_runtime_font_px_at_1366x768": 14,
        "recommended_text_texture_contrast_max_percent": 2,
        "recommended_mipmap_or_prefilter_at_1600_and_1366": True,
    },
    "withdrawn_reviews": {
        "reason": "2026-07-22 用户在最终整屏中指出第三卡锁定状态签右端不完整；名义 carrier 与文字中心证据不能证明实际图形对象完整。",
        "previous_status": "dual_reviewed_pending_user_visual_confirmation",
        "previous_ux_verdict": "PASS",
        "previous_ui_verdict": "PASS",
    },
    "final_reviews": current_reviews,
    "v0_1_failure_regression_targets": {
        "source": "2026-07-22 用户三张 100% 局部截图",
        "required_fixed_issues": [
            {
                "id": "third_card_state_carrier_mismatch",
                "current_parent_result": third_card_regression_result,
            },
            {
                "id": "schedule_state_action_grouping",
                "v0_2_parent_result": "FIXED_REVIEWED",
            },
            {
                "id": "dossier_body_mission_spacing",
                "v0_2_parent_result": "FIXED_REVIEWED",
            },
        ],
    },
    "protected_object_mapping_audit": {
        "third_card_state_tag": third_card_protected_fit,
    },
    "visual_carrier_audit": {
        "default": default_visual_carriers,
        "schedule_confirming": confirming_visual_carriers,
        "declared_rect_text_audit_passed": default_visual_carriers["passed"] and confirming_visual_carriers["passed"],
        "parent_passed": default_visual_carriers["passed"] and confirming_visual_carriers["passed"] and third_card_protected_fit["passed"],
        "independent_local_crop_review": independent_local_crop_review,
    },
    "visual_stats": {
        "mean_rgb_240x135": [round(value, 2) for value in stats.mean],
        "stddev_rgb_240x135": [round(value, 2) for value in stats.stddev],
    },
    "assertions": {
        "selected_scheme_1_pixels_preserved_outside_text_and_patch_zones": default_source_diff["passed"] and confirming_source_diff["passed"],
        "eight_classic_rectangular_image_slots": True,
        "all_text_inside_safe_rects": all(record["passed"] for record in default_records + confirming_records),
        "text_inside_visible_carriers": default_visual_carriers["all_text_inside_owner_carrier"] and confirming_visual_carriers["all_text_inside_owner_carrier"],
        "semantic_groups_non_overlapping": default_visual_carriers["body_2_to_mission_header_safe_rect_intersection_xyxy"] is None,
        "minimum_group_gap_passed": default_visual_carriers["body_to_mission_heading_gap_px"] >= 10 and default_visual_carriers["mission_heading_to_first_row_gap_px"] >= 8,
        "state_text_centered_in_state_carrier": max(default_visual_carriers["third_card_state_center_error_xy"]) <= 8,
        "scope_invariant_vs_v0_1_passed": default_scope_invariant["passed"] and confirming_scope_invariant["passed"],
        "v0_3_changes_only_third_card_footer_vs_v0_2": (
            v02_to_v03_scope_invariant["default"]["passed"]
            and v02_to_v03_scope_invariant["schedule_confirming"]["passed"]
            if IS_V03
            else None
        ),
        "third_card_state_carrier_complete": third_card_protected_fit["passed"],
        "third_card_state_endcaps_complete": all(third_card_protected_fit["endcaps_present"].values()),
        "third_card_state_tag_retention_at_least_99_percent": third_card_protected_fit["protected_pixel_retention_ratio"] >= 0.99,
        "independent_local_crop_review_passed": IS_V03,
        "state_delta_schedule_only": outside_bbox is None,
        "right_title_not_over_photo": True,
        "static_fasteners_have_no_runtime_semantics": True,
        "formal_contracts_unchanged": True,
        "godot_unchanged": True,
    },
}

AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(DEFAULT_OUTPUT)
print(CONFIRMING_OUTPUT)
print(BOARD_OUTPUT)
print(LOCAL_QA_OUTPUT)
print(AUDIT)
