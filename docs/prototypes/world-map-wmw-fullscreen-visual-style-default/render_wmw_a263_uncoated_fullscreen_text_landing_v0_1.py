from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "wmw-a259-01-uncoated-independent-weekly-v0-1.png"
DEFAULT_OUTPUT = ROOT / "wmw-a263-uncoated-fullscreen-default-v0-1.png"
CONFIRMING_OUTPUT = ROOT / "wmw-a263-uncoated-fullscreen-schedule-confirming-v0-1.png"
BOARD_OUTPUT = ROOT / "wmw-a263-uncoated-fullscreen-state-pair-v0-1.png"
AUDIT = ROOT / "wmw-a263-uncoated-fullscreen-v0-1-audit.json"

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

SCHEDULE_DELTA_RECT = [65, 839, 327, 189]


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
) -> None:
    bbox = draw.textbbox(point, text, font=used_font, anchor=anchor)
    passed = contains(safe_rect, bbox)
    records.append(
        {
            "key": key,
            "text": text,
            "bbox_xyxy": list(bbox),
            "safe_rect_xywh": list(safe_rect),
            "passed": passed,
        }
    )
    draw.text(point, text, font=used_font, fill=fill, anchor=anchor)


def apply_shared_patches(source: Image.Image) -> tuple[Image.Image, list[dict]]:
    canvas = source.copy()
    patch_records: list[dict] = []

    # The third story card lacks the same quiet title carrier as cards 1/2.
    # Restore only its title field; preserve the original gray-indigo state tag.
    title_patch_rect = [49, 744, 265, 52]
    canvas.paste(fit(source, PATCHES["card_meta_paper"], (265, 52)), (49, 744))
    patch_records.append(
        {
            "source_crop_xyxy": PATCHES["card_meta_paper"],
            "target_rect_xywh": title_patch_rect,
            "role": "恢复第三卡标题纸带并保留原状态色签",
        }
    )

    targets = [
        ("dossier_copy_paper", [1404, 438, 428, 112], 8, 248, "右侧标题/正文/摘要同源纸面"),
        ("schedule_paper", [151, 839, 238, 25], 5, 244, "日期/剩余日同源纸面"),
        ("schedule_paper", [75, 848, 58, 66], 4, 255, "清除底图箭头并承载动态确认图标"),
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
        ((64, 770), "太平洋失航带", (365, 770), "锁定", [64, 754, 232, 32], [323, 754, 84, 30]),
    ]
    for index, (title_point, title, state_point, state, title_safe, state_safe) in enumerate(cards):
        safe_text(draw, title, title_point, F22B, INK, "lm", title_safe, records, f"left_title_{index}")
        safe_text(draw, state, state_point, F18B, PAPER_TEXT, "mm", state_safe, records, f"left_state_{index}")

    outlined_text(draw, "北美禁区带", (654, 390), F20B, PAPER_TEXT, "lm", [654, 374, 172, 32], records, "map_selected")
    outlined_text(draw, "东亚神秘地带", (1208, 410), F20B, PAPER_TEXT, "rm", [1016, 394, 196, 32], records, "map_east")
    outlined_text(draw, "太平洋失航带", (1212, 692), F20B, PAPER_TEXT, "rm", [1016, 676, 200, 32], records, "map_pacific")

    safe_text(draw, "北美禁区带", (1424, 462), F26B, INK, "lm", [1424, 447, 388, 32], records, "right_title")
    safe_text(draw, "都市传说与军事封锁交叠。", (1424, 491), F16, INK, "la", [1424, 490, 388, 24], records, "right_body_1")
    safe_text(draw, "军方巡逻、档案残页与异常雷达同时露头。", (1424, 512), F14, INK_SOFT, "la", [1424, 512, 388, 22], records, "right_body_2")
    safe_text(draw, "任务情报", (1424, 540), F18B, INK, "lm", [1424, 527, 100, 28], records, "mission_header")
    safe_text(draw, "常驻 2 · 限时 1 · 深链 1", (1698, 540), F12, INK_SOFT, "rm", [1508, 532, 190, 20], records, "mission_summary")
    safe_text(draw, "已展开 4 / 4", (1820, 540), F12, INK_SOFT, "rm", [1712, 532, 108, 20], records, "mission_expanded")

    rows = [
        (556, "51 区外围公路", "科学纪实 · 耗时 2 天", "常驻"),
        (634, "罗斯威尔档案残页", "科学纪实 · 耗时 1 天", "常驻"),
        (710, "突发：雷达异常光点", "大众热度 · 耗时 2 天", "限时至第 4 天"),
        (789, "M330 末班车空白段", "神秘玄学 · 耗时 2 天", "深链"),
    ]
    for index, (y, title, meta, state) in enumerate(rows):
        safe_text(draw, title, (1544, y + 24), F20B, INK, "lm", [1544, y + 8, 278, 30], records, f"mission_title_{index}")
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
    safe_text(draw, "当前第 1 天", (158, 853), F16, INK, "lm", [158, 842, 112, 19], records, "schedule_current")
    safe_text(draw, "剩余 7 天", (382, 853), F16, INK, "rm", [270, 842, 112, 22], records, "schedule_remaining")
    safe_text(draw, "!" if confirming else "→", (104, 879), F28B, INK, "mm", [82, 855, 44, 48], records, "schedule_icon")
    safe_text(
        draw,
        "确认推进到第 2 天" if confirming else "推进到下一天",
        (158, 882),
        F22B,
        PAPER_TEXT,
        "lm",
        [158, 870, 224, 28],
        records,
        "schedule_title",
    )
    safe_text(
        draw,
        "再次点击执行；后果见下方" if confirming else "点击后查看推进影响",
        (158, 911),
        F14,
        PAPER_TEXT_SOFT,
        "lm",
        [158, 900, 224, 22],
        records,
        "schedule_help",
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

stats = ImageStat.Stat(default.resize((240, 135), Image.Resampling.BILINEAR))
audit = {
    "artifact_type": "fullscreen_filled_state_text_mock_state_pair",
    "version": "wmw_a263_uncoated_fullscreen_text_landing_v0_1",
    "status": "user_visual_review_failed_rework_required",
    "decision_source": "A263",
    "canvas": [W, H],
    "source": {
        "built_in_imagegen_used": True,
        "selected_material_direction": "无涂布独立周刊",
        "file": SOURCE.name,
        "sha256": digest(SOURCE),
    },
    "outputs": {
        "default": DEFAULT_OUTPUT.name,
        "schedule_confirming": CONFIRMING_OUTPUT.name,
        "state_pair_board": BOARD_OUTPUT.name,
        "default_sha256": digest(DEFAULT_OUTPUT),
        "schedule_confirming_sha256": digest(CONFIRMING_OUTPUT),
        "state_pair_board_sha256": digest(BOARD_OUTPUT),
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
    "final_reviews": {
        "ux_laoge": {
            "verdict": "RETRACTED_FALSE_PASS",
            "p0": 0,
            "p1": 3,
            "p2": 0,
            "notes": [
                "前次 PASS 已撤回：只检查 text bbox 位于作者定义的 safe rect，没有独立核对真实可见载体、语义间距与 100% 局部裁切。",
                "第三卡状态签错层、日程状态与动作粘连、右栏正文与任务章节拥挤均为 P1。",
            ],
        },
        "ui_designer": {
            "verdict": "RETRACTED_FALSE_PASS",
            "p0": 0,
            "p1": 3,
            "p2": 1,
            "notes": [
                "前次 PASS 已撤回：来源差分只能证明允许区外未变化，不能证明允许区内补纸、层级和接缝成立。",
                "右栏正文第二行 safe rect 与任务标题 safe rect 重叠 7px；任务标题实际 bbox 与首任务载体仅余 4px。",
            ],
        },
    },
    "user_visual_review": {
        "verdict": "FAIL",
        "p0": 0,
        "p1": 3,
        "issues": [
            {
                "id": "third_card_state_carrier_mismatch",
                "result": "FAIL",
                "evidence": "第三卡标题补纸、照片和原灰靛状态签错层；锁定文字未稳定落入真实状态签。",
            },
            {
                "id": "schedule_state_action_grouping",
                "result": "FAIL",
                "evidence": "当前日/剩余日与推进动作共用并贴近同一可见动作载体，状态事实与操作动词无法快速分组。",
            },
            {
                "id": "dossier_body_mission_spacing",
                "result": "FAIL",
                "evidence": "正文第二行 safe rect y512-534 与任务标题 safe rect y527-555 重叠；标题 bbox 底 y552 到首任务载体 y556 仅 4px。",
            },
        ],
    },
    "visual_carrier_audit": {
        "passed": False,
        "contract_safe_rect_containment_only": True,
        "visible_carrier_ownership_checked_before_user_review": False,
        "semantic_safe_rect_intersections": [
            {
                "a": "right_body_2",
                "b": "mission_header",
                "intersection_xyxy": [1424, 527, 1524, 534],
            }
        ],
        "minimum_group_gap_passed": False,
        "state_text_centered_in_visible_state_carrier": False,
        "independent_100_percent_local_crop_review_passed": False,
    },
    "visual_stats": {
        "mean_rgb_240x135": [round(value, 2) for value in stats.mean],
        "stddev_rgb_240x135": [round(value, 2) for value in stats.stddev],
    },
    "assertions": {
        "selected_scheme_1_pixels_preserved_outside_text_and_patch_zones": default_source_diff["passed"] and confirming_source_diff["passed"],
        "eight_classic_rectangular_image_slots": True,
        "all_text_inside_safe_rects": all(record["passed"] for record in default_records + confirming_records),
        "text_inside_visible_carriers": False,
        "semantic_groups_non_overlapping": False,
        "minimum_group_gap_passed": False,
        "state_text_centered_in_state_carrier": False,
        "independent_local_crop_review_passed": False,
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
print(AUDIT)
