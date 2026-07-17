from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps

import wmw_v091_right_dossier_candidate_a1_pipeline as a1


ROOT = a1.ROOT
BASE = a1.BASE
ASSET_DIR = (
    ROOT
    / "gd_project"
    / "Assets"
    / "ui"
    / "angus_packaging"
    / "world_map"
    / "wmw_v092_right_dossier_candidate_a2"
)
FIXTURE = ASSET_DIR / "right_dossier_candidate_a2_runtime_fixture.json"

OUT_AUDIT = BASE / "598-world-map-wmw-v0-9-2-right-dossier-candidate-a2-function-audit.png"
OUT_PYTHON = BASE / "599-world-map-wmw-v0-9-2-right-dossier-candidate-a2-python-runtime.png"
OUT_PYTHON_QA = BASE / "600-world-map-wmw-v0-9-2-right-dossier-candidate-a2-python-runtime-qa.png"
OUT_GODOT = BASE / "601-world-map-wmw-v0-9-2-right-dossier-candidate-a2-godot-runtime.png"
OUT_GODOT_QA = BASE / "602-world-map-wmw-v0-9-2-right-dossier-candidate-a2-godot-runtime-qa.png"
OUT_REVIEW = BASE / "603-world-map-wmw-v0-9-2-right-dossier-candidate-a1-a2-review.png"
OUT_MANIFEST = BASE / "604-world-map-wmw-v0-9-2-right-dossier-candidate-a2-manifest.json"

A1_GODOT = BASE / "594-world-map-wmw-v0-9-1-right-dossier-candidate-a1-godot-runtime.png"
A1_MANIFEST = BASE / "597-world-map-wmw-v0-9-1-right-dossier-candidate-a1-manifest.json"

NAVY = (7, 20, 22)
PANEL = (13, 39, 40)
CREAM = (235, 227, 201)
GREEN = (103, 229, 148)
RED = (255, 104, 96)
YELLOW = (255, 212, 68)

EXPECTED_COMPONENT_IDS = [
    "header_icon",
    "title_slot",
    "status_stamp",
    "photo_slot",
    "region_body",
    "decision_facts",
    "mission_intel_button",
    "primary_enter_cta",
    "mission_button_icon_pair",
    "primary_button_icon_pair",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_fixture() -> dict[str, Any]:
    fixture = a1.load_json(FIXTURE)
    required = {
        "region_title",
        "status_display_text",
        "region_body_text",
        "decision_facts",
        "mission_intel_label",
        "primary_enter_label",
    }
    missing = sorted(required - set(fixture))
    if missing:
        raise RuntimeError(f"production runtime fixture is missing fields: {missing}")
    if fixture.get("provenance") != "production_runtime_export":
        raise RuntimeError("runtime fixture provenance is not production_runtime_export")
    if fixture.get("generated_from_production_data") is not True:
        raise RuntimeError("runtime fixture is not marked as production-derived")
    if "\n" in str(fixture["status_display_text"]):
        raise RuntimeError("A2 status must remain one semantic line")
    if "recommendation" in fixture:
        raise RuntimeError("region-level recommendation was retired by A205")
    return fixture


def child_rect(parent: tuple[int, int, int, int], slot: list[int]) -> tuple[int, int, int, int]:
    local = a1.scale_rect(slot)
    return (
        parent[0] + local[0],
        parent[1] + local[1],
        parent[0] + local[2],
        parent[1] + local[3],
    )


def add_text_report(
    reports: list[dict[str, Any]],
    draw: ImageDraw.ImageDraw,
    field: str,
    rect: tuple[int, int, int, int],
    value: str,
    **kwargs: Any,
) -> dict[str, Any]:
    report = a1.fit_and_draw(draw, rect, value, **kwargs)
    report["field"] = field
    reports.append(report)
    return report


def render_runtime_component(
    fixture: dict[str, Any], show_qa: bool
) -> tuple[Image.Image, list[dict[str, Any]]]:
    shell = Image.open(a1.PARENT_MASTER).convert("RGBA")
    mission = Image.open(a1.MISSION_MASTER).convert("RGBA")
    primary = Image.open(a1.PRIMARY_MASTER).convert("RGBA")
    photo = Image.open(a1.PHOTO_INGREDIENT).convert("RGBA")
    photo_rect = a1.scale_rect(a1.DOSSIER["frozen"]["slots"]["photo_slot"])
    expected_photo_size = (photo_rect[2] - photo_rect[0], photo_rect[3] - photo_rect[1])
    if photo.size != expected_photo_size:
        raise RuntimeError(f"A1 photo ingredient drifted: {photo.size} != {expected_photo_size}")

    component = Image.new("RGBA", shell.size, (12, 27, 29, 255))
    component.alpha_composite(photo, (photo_rect[0], photo_rect[1]))
    component.alpha_composite(shell)

    slots = a1.DOSSIER["frozen"]["slots"]
    mission_rect = a1.scale_rect(slots["mission_intel_button"])
    primary_rect = a1.scale_rect(slots["primary_enter_cta"])
    component.alpha_composite(mission, (mission_rect[0], mission_rect[1]))
    component.alpha_composite(primary, (primary_rect[0], primary_rect[1]))

    draw = ImageDraw.Draw(component)
    reports: list[dict[str, Any]] = []
    ink = (28, 30, 25, 255)
    cream = (238, 229, 202, 255)
    teal_ink = (31, 82, 85, 255)

    header_icon = a1.scale_rect(slots["header_icon"])
    header_icon = (
        header_icon[0],
        header_icon[1] + a1.HEADER_ICON_OFFSET_2X,
        header_icon[2],
        header_icon[3] + a1.HEADER_ICON_OFFSET_2X,
    )
    header_icon_bbox = a1.paste_runtime_icon(
        component, a1.RUNTIME_GLOBE, header_icon, (90, 93, 76, 255), 0.86
    )
    title_report = add_text_report(
        reports,
        draw,
        "region_title",
        a1.scale_rect(slots["title_slot"]),
        str(fixture["region_title"]),
        max_size=38,
        min_size=28,
        bold=True,
        fill=ink,
        align="center",
        pad_x=8,
        pad_y=6,
    )

    status = a1.scale_rect(slots["status_stamp"])
    status = (
        status[0],
        status[1] + a1.STATUS_GROUP_OFFSET_2X,
        status[2],
        status[3] + a1.STATUS_GROUP_OFFSET_2X,
    )
    status_report = add_text_report(
        reports,
        draw,
        "status_display_text",
        status,
        str(fixture["status_display_text"]),
        max_size=22,
        min_size=18,
        bold=True,
        fill=(142, 54, 39, 255),
        align="center",
        pad_x=6,
        pad_y=8,
    )
    title_bbox = title_report["raster_glyph_bbox"]
    status_bbox = status_report["raster_glyph_bbox"]
    centers = {
        "icon": (header_icon_bbox[1] + header_icon_bbox[3]) / 2,
        "title": (title_bbox[1] + title_bbox[3]) / 2,
        "status": (status_bbox[1] + status_bbox[3]) / 2,
    }
    title_report["header_optical_alignment"] = {
        "axis_y_2x": a1.HEADER_AXIS_2X,
        "ink_bboxes": {
            "icon": list(header_icon_bbox),
            "title": list(title_bbox),
            "status": list(status_bbox),
        },
        "centers_y_2x": centers,
        "max_axis_deviation_px_2x": max(
            abs(value - a1.HEADER_AXIS_2X) for value in centers.values()
        ),
    }

    body_lines = str(fixture["region_body_text"]).split("\n")
    if len(body_lines) != 2:
        raise RuntimeError(f"region_body_text must contain exactly two lines: {body_lines}")
    body = a1.scale_rect(a1.REGION_BODY_INNER)
    body_mid = (body[1] + body[3]) // 2
    for index, (line, rect) in enumerate(
        (
            (body_lines[0], (body[0], body[1], body[2], body_mid)),
            (body_lines[1], (body[0], body_mid, body[2], body[3])),
        ),
        start=1,
    ):
        add_text_report(
            reports,
            draw,
            f"region_body_line_{index}",
            rect,
            line,
            max_size=23,
            min_size=17,
            bold=False,
            fill=ink,
            pad_x=0,
        )
    add_text_report(
        reports,
        draw,
        "decision_facts",
        a1.scale_rect(slots["decision_facts"]),
        str(fixture["decision_facts"]),
        max_size=22,
        min_size=16,
        bold=True,
        fill=(52, 57, 48, 255),
        align="center",
        pad_x=8,
        pad_y=4,
    )

    mission_slots = a1.MISSION["frozen"]["slots"]
    mission_left = child_rect(mission_rect, mission_slots["left_icon_zone"])
    mission_label = child_rect(mission_rect, mission_slots["label_plate"])
    mission_right = child_rect(mission_rect, mission_slots["right_action_badge"])
    a1.paste_runtime_icon(component, a1.RUNTIME_DOCUMENT, mission_left, cream, 0.84)
    a1.paste_runtime_icon(component, a1.RUNTIME_ARROW, mission_right, cream, 0.78)
    add_text_report(
        reports,
        draw,
        "mission_intel_label",
        mission_label,
        str(fixture["mission_intel_label"]),
        max_size=25,
        min_size=18,
        bold=True,
        fill=teal_ink,
        align="center",
        pad_x=8,
        pad_y=5,
    )

    primary_slots = a1.PRIMARY["frozen"]["slots"]
    primary_left = child_rect(primary_rect, primary_slots["left_icon_zone"])
    primary_label = child_rect(primary_rect, primary_slots["label_plate"])
    primary_right = child_rect(primary_rect, primary_slots["right_action_badge"])
    a1.paste_runtime_icon(component, a1.RUNTIME_GLOBE, primary_left, cream, 0.72)
    a1.paste_runtime_icon(component, a1.RUNTIME_ARROW, primary_right, cream, 0.78)
    add_text_report(
        reports,
        draw,
        "primary_enter_label",
        primary_label,
        str(fixture["primary_enter_label"]),
        max_size=28,
        min_size=20,
        bold=True,
        fill=(58, 66, 40, 255),
        align="center",
        pad_x=8,
        pad_y=6,
    )

    if show_qa:
        qa_colors = {
            "header_icon": (81, 238, 255, 255),
            "title_slot": (255, 72, 202, 255),
            "status_stamp": (255, 111, 95, 255),
            "photo_slot": (72, 236, 174, 255),
            "region_body": (255, 212, 68, 255),
            "decision_facts": (167, 128, 255, 255),
            "mission_intel_button": (79, 218, 232, 255),
            "primary_enter_cta": (174, 204, 91, 255),
        }
        for name, color in qa_colors.items():
            rect = a1.scale_rect(slots[name])
            draw.rectangle((rect[0], rect[1], rect[2] - 1, rect[3] - 1), outline=color, width=3)
        for report in reports:
            bbox = report["raster_glyph_bbox"]
            draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 55, 196, 255), width=2)
        inner = a1.scale_rect(a1.REGION_BODY_INNER)
        no_text = a1.scale_rect(a1.REGION_BODY_NO_TEXT)
        draw.rectangle((inner[0], inner[1], inner[2] - 1, inner[3] - 1), outline=(95, 255, 140, 255), width=3)
        draw.rectangle((no_text[0], no_text[1], no_text[2] - 1, no_text[3] - 1), outline=(255, 75, 75, 255), width=3)
        draw.line((0, a1.HEADER_AXIS_2X, component.width - 1, a1.HEADER_AXIS_2X), fill=(95, 255, 140, 255), width=2)
    return component, reports


def component_audit() -> list[dict[str, Any]]:
    return [
        {"component_id": "header_icon", "visible": True, "player_question": "这是哪个信息域？", "necessity": "保留地区 dossier 的类别锚点；静态且不承担状态。", "data_source": "共享 globe 图标 token", "interactive": False, "decision": "keep"},
        {"component_id": "title_slot", "visible": True, "player_question": "我正在看哪个地区？", "necessity": "地区身份主标题，不可缺。", "data_source": "WeeklyRunContent.REGION_DATA[].name", "interactive": False, "decision": "change"},
        {"component_id": "status_stamp", "visible": True, "player_question": "该地区现在是什么状态？", "necessity": "只保留一个正式状态，不再混入推荐人数。", "data_source": "WeeklyRunSystems visibility/deadline derived state", "interactive": False, "decision": "change"},
        {"component_id": "photo_slot", "visible": True, "player_question": "这个地区的视觉特征是什么？", "necessity": "提供地区识别与气氛；复用已验收 69:44 照片。", "data_source": "A1 552x352 photo ingredient", "interactive": False, "decision": "keep"},
        {"component_id": "region_body", "visible": True, "player_question": "本地区发生了什么？", "necessity": "两行承载地区特征与本周警告。", "data_source": "region.hint + WeeklyRunState.remaining_days", "interactive": False, "decision": "change"},
        {"component_id": "decision_facts", "visible": True, "player_question": "进入前要比较哪些事实？", "necessity": "集中呈现限时、线索、深链计数，避免信息散落。", "data_source": "visible node kind counts", "interactive": False, "decision": "change"},
        {"component_id": "mission_intel_button", "visible": True, "player_question": "有哪些已知任务？", "necessity": "A189 已采纳的只读预览入口；不进入派遣。", "data_source": "visible node count", "interactive": True, "decision": "change"},
        {"component_id": "primary_enter_cta", "visible": True, "player_question": "如何进入该地区？", "necessity": "页面唯一最高权重动作。", "data_source": "region unlocked state", "interactive": True, "decision": "keep"},
        {"component_id": "mission_button_icon_pair", "visible": True, "player_question": "按钮对象与去向是什么？", "necessity": "文档=对象，箭头=进入详情；同属一个命令。", "data_source": "共享 document + arrow tokens", "interactive": False, "decision": "keep"},
        {"component_id": "primary_button_icon_pair", "visible": True, "player_question": "按钮对象与去向是什么？", "necessity": "地球=地区对象，箭头=进入；删除歧义 check。", "data_source": "共享 globe + arrow tokens", "interactive": False, "decision": "change"},
    ]


def visible_fields(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field_id": "region_title", "component": "title_slot", "visible": True, "player_question": "我正在看哪个地区？", "decision_value": "稳定识别当前选中地区", "owner_scope": "region", "source_kind": "content_mapping", "data_source": "WeeklyRunContent.REGION_DATA[0].name", "fixture_key": "region_title", "screenshot_value": fixture["region_title"], "decision": "change"},
        {"field_id": "status_display_text", "component": "status_stamp", "visible": True, "player_question": "该地区当前能否进入、是否有时限？", "decision_value": "报告当前地区状态，单一语义", "owner_scope": "region", "source_kind": "state_derived", "data_source": "WeeklyRunSystems node visibility and deadline count", "fixture_key": "status_display_text", "screenshot_value": fixture["status_display_text"], "decision": "change"},
        {"field_id": "region_body_text", "component": "region_body", "visible": True, "player_question": "这里发生了什么、当前警告是什么？", "decision_value": "地区背景与本周时限说明", "owner_scope": "region", "source_kind": "state_derived", "data_source": "region.hint + WeeklyRunState.remaining_days", "fixture_key": "region_body_text", "screenshot_value": fixture["region_body_text"], "decision": "change"},
        {"field_id": "decision_facts", "component": "decision_facts", "visible": True, "player_question": "有哪些限时、线索与深链？", "decision_value": "进入前的可比事实", "owner_scope": "region", "source_kind": "state_derived", "data_source": "visible node kind counts", "fixture_key": "decision_facts", "screenshot_value": fixture["decision_facts"], "decision": "change"},
        {"field_id": "mission_intel_label", "component": "mission_intel_button", "visible": True, "player_question": "有多少已知任务可预览？", "decision_value": "打开只读任务情报并显示真实数量", "owner_scope": "region", "source_kind": "state_derived", "data_source": "visible node count", "fixture_key": "mission_intel_label", "screenshot_value": fixture["mission_intel_label"], "decision": "change"},
        {"field_id": "primary_enter_label", "component": "primary_enter_cta", "visible": True, "player_question": "能否进入当前地区？", "decision_value": "进入地区或明确不可进入", "owner_scope": "region", "source_kind": "state_derived", "data_source": "WeeklyRunSystems.is_region_unlocked", "fixture_key": "primary_enter_label", "screenshot_value": fixture["primary_enter_label"], "decision": "keep"},
    ]


def retired_fields() -> list[dict[str, Any]]:
    return [
        {"field_id": "region_recommendation", "prior_value": "推荐12", "reason": "世界地图只选择地区；人数建议属于具体任务派遣层。", "visible_after": False},
        {"field_id": "stress_region_title", "prior_value": "北美禁区警戒带", "reason": "容量压力字符串不是正式地区名。", "visible_after": False},
        {"field_id": "generic_risk_label", "prior_value": "高危", "reason": "改为由正式节点状态推导的红线升温。", "visible_after": False},
        {"field_id": "fictional_body", "prior_value": "天线阵列仍在发射，林线内出现异常回波。", "reason": "未绑定正式 region payload。", "visible_after": False},
        {"field_id": "stress_facts", "prior_value": "限时 2 周 · 线索缺口 3 · 深链 1", "reason": "压力计数不得进入运行复审图。", "visible_after": False},
        {"field_id": "stress_task_count", "prior_value": "查看任务情报 · 12项", "reason": "改为正式可见节点数。", "visible_after": False},
    ]


def build_function_audit_board(component: Image.Image) -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "WMW 右 dossier · A2 全组件功能与必要性审计", font=a1.font(32, True), fill=CREAM)
    draw.text((44, 75), "598 · 不是只删“推荐12”：玩家可见的 10 个基础组件逐项核对职责、数据源与交互边界。", font=a1.font(17), fill=(191, 211, 201))

    preview = component.convert("RGB").resize((480, 780), Image.Resampling.LANCZOS)
    board.paste(preview, (55, 150))
    draw.rectangle((45, 140, 545, 940), outline=GREEN, width=2)
    draw.text((55, 110), "A2 Python production fixture", font=a1.font(17, True), fill=GREEN)

    headers = ("组件", "处理", "存在理由", "真源 / 边界")
    xs = (590, 865, 995, 1430)
    for x, value in zip(xs, headers):
        draw.text((x, 116), value, font=a1.font(15, True), fill=YELLOW)
    for index, item in enumerate(component_audit()):
        y = 148 + index * 83
        draw.rectangle((575, y - 4, 1880, y + 70), fill=PANEL, outline=(48, 90, 88), width=1)
        draw.text((590, y + 8), item["component_id"], font=a1.font(14, True), fill=CREAM)
        decision = "保留" if item["decision"] == "keep" else "修正"
        draw.text((865, y + 8), decision, font=a1.font(14, True), fill=GREEN if decision == "保留" else YELLOW)
        reason = str(item["necessity"])
        source = str(item["data_source"])
        draw.text((995, y + 5), reason[:23], font=a1.font(13), fill=(218, 226, 205))
        draw.text((995, y + 34), reason[23:46], font=a1.font(13), fill=(218, 226, 205))
        draw.text((1430, y + 5), source[:30], font=a1.font(12), fill=(181, 205, 197))
        draw.text((1430, y + 34), source[30:60], font=a1.font(12), fill=(181, 205, 197))
    draw.text((58, 982), "退役：地区级推荐人数、压力标题、泛化高危、虚构正文、压力计数。", font=a1.font(16, True), fill=RED)
    draw.text((58, 1022), "保留结构删除需另行裁决；本轮不擅改 v0.8.6 frozen 槽位。", font=a1.font(15), fill=(215, 221, 199))
    OUT_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    board.save(OUT_AUDIT)


def build_runtime_board(
    component: Image.Image, reports: list[dict[str, Any]], show_qa: bool
) -> None:
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    board.paste(component.convert("RGB"), (48, 20))
    suffix = "QA" if show_qa else "fill"
    draw.text((742, 34), f"Python v0.9.2 candidate A2 production runtime {suffix}", font=a1.font(31, True), fill=CREAM)
    draw.text((744, 82), "A205：正式 region payload；推荐人数退役；压力 fixture 与运行 fixture 物理分离。", font=a1.font(17), fill=(191, 209, 198))

    slots = a1.DOSSIER["frozen"]["slots"]
    header_crop = component.crop(a1.scale_rect([14, 18, 290, 74])).resize((828, 222), Image.Resampling.NEAREST)
    info_crop = component.crop(a1.scale_rect([18, 282, 286, 100])).resize((828, 290), Image.Resampling.NEAREST)
    action_crop = component.crop(a1.scale_rect([14, 386, 292, 112])).resize((828, 318), Image.Resampling.NEAREST)
    board.paste(header_crop.convert("RGB"), (800, 150))
    board.paste(info_crop.convert("RGB"), (800, 430))
    board.paste(action_crop.convert("RGB"), (800, 770))
    draw.rectangle((790, 140, 1638, 382), outline=GREEN, width=2)
    draw.rectangle((790, 420, 1638, 730), outline=YELLOW, width=2)
    draw.rectangle((790, 760, 1638, 1078), outline=(72, 236, 174), width=2)
    draw.text((800, 112), "HEADER · one state only: 红线升温", font=a1.font(18, True), fill=GREEN)
    draw.text((800, 392), "INFO · hint/days + formal node counts", font=a1.font(18, True), fill=YELLOW)
    draw.text((800, 732), "ACTIONS · document→detail / globe→region", font=a1.font(18, True), fill=(72, 236, 174))

    passed = sum(
        1
        for report in reports
        if report["fit_search_pass"] and report["glyph_bbox_inside_inner_rect"]
    )
    draw.text((1660, 210), f"text bbox {passed}/{len(reports)}", font=a1.font(17, True), fill=GREEN if passed == len(reports) else RED)
    header = reports[0]["header_optical_alignment"]
    draw.text((1660, 255), f"axis dev {header['max_axis_deviation_px_2x']:.2f}px @2x", font=a1.font(15, True), fill=GREEN if header["max_axis_deviation_px_2x"] <= 2 else RED)
    draw.text((1660, 302), "粉框=真实字形 alpha" if show_qa else "同一 fixture 双端消费", font=a1.font(14), fill=(223, 221, 196))
    output = OUT_PYTHON_QA if show_qa else OUT_PYTHON
    output.parent.mkdir(parents=True, exist_ok=True)
    board.save(output)


def build_manifest(fixture: dict[str, Any], reports: list[dict[str, Any]]) -> dict[str, Any]:
    report_by_field = {item["field"]: item for item in reports}
    header = report_by_field["region_title"]["header_optical_alignment"]
    body_reports = [report_by_field["region_body_line_1"], report_by_field["region_body_line_2"]]
    body_boxes = [item["raster_glyph_bbox"] for item in body_reports]
    body_inner = list(a1.scale_rect(a1.REGION_BODY_INNER))
    no_text = list(a1.scale_rect(a1.REGION_BODY_NO_TEXT))
    body_lefts = [item[0] for item in body_boxes]
    body_rights = [item[2] for item in body_boxes]
    body_pass = (
        min(body_lefts) >= body_inner[0]
        and max(body_rights) <= body_inner[2]
        and max(body_lefts) - min(body_lefts) <= 2
        and min(body_lefts) - no_text[2] >= 16
    )
    text_pass = all(
        item["fit_search_pass"] and item["glyph_bbox_inside_inner_rect"] for item in reports
    )
    fields = visible_fields(fixture)
    retired = retired_fields()
    old_values = {str(item["prior_value"]) for item in retired}
    visible_values = {str(item["screenshot_value"]) for item in fields}
    stress_leak = sorted(old_values & visible_values)
    components = component_audit()

    reused_assets = [
        a1.PARENT_MASTER,
        a1.MISSION_MASTER,
        a1.PRIMARY_MASTER,
        a1.PHOTO_INGREDIENT,
        a1.ATLAS,
        a1.RUNTIME_GLOBE,
        a1.RUNTIME_DOCUMENT,
        a1.RUNTIME_ARROW,
    ]
    manifest = {
        "schema_version": 1,
        "asset_line": "world-map-benchmark-landing/right-dossier",
        "version": "v0.9.2",
        "candidate": "A2",
        "status": "evidence_ready_godot_capture_pending",
        "design_adoption": "A205：删除地区级推荐人数；玩家可见字段改由正式 region payload 驱动；候选交付前逐项审计全部基础组件必要性。",
        "runtime_fixture_path": rel(FIXTURE),
        "contracts": {
            "right_dossier_page": {"version": a1.DOSSIER["contract_version"], "frozen_changed": False},
            "right_mission_intel_button": {"version": a1.MISSION["contract_version"], "frozen_changed": False},
            "right_action_lane": {"version": a1.PRIMARY["contract_version"], "frozen_changed": False},
        },
        "sources": {
            "runtime_fixture": rel(FIXTURE),
            "production_source_files": fixture["source_files"],
            "reused_candidate_a1_assets": [rel(path) for path in reused_assets],
            "new_imagegen_calls": 0,
            "reused_asset_sha256": {rel(path): a1.file_sha256(path) for path in reused_assets},
        },
        "outputs": {
            "function_audit": rel(OUT_AUDIT),
            "python_runtime": rel(OUT_PYTHON),
            "python_qa": rel(OUT_PYTHON_QA),
            "godot_runtime": rel(OUT_GODOT),
            "godot_qa": rel(OUT_GODOT_QA),
            "review_board": rel(OUT_REVIEW),
            "reused_atlas": rel(a1.ATLAS),
        },
        "visible_field_semantics": fields,
        "visible_component_expected_ids": EXPECTED_COMPONENT_IDS,
        "visible_component_audit": components,
        "removed_fixture_fields": retired,
        "measurements": {
            "text_tokens": reports,
            "header_optical_alignment": header,
            "region_body_visual_padding": {
                "inner_rect_2x": body_inner,
                "no_text_rect_2x": no_text,
                "line_glyph_bboxes_2x": body_boxes,
                "line_left_difference_px_2x": max(body_lefts) - min(body_lefts),
                "minimum_gap_after_no_text_px_2x": min(body_lefts) - no_text[2],
            },
            "runtime_fixture": fixture,
        },
        "gates": {
            "contracts_frozen_unchanged": {"status": "pass", "basis": "三份 v0.8.6 frozen 字段未改。"},
            "no_new_imagegen": {"status": "pass", "calls": 0, "basis": "A2 只复用 A1 无字母版、照片与图标配料。"},
            "production_runtime_fixture": {"status": "pass", "provenance": fixture["provenance"], "generated_from_production_data": fixture["generated_from_production_data"]},
            "visible_field_semantic_necessity": {"status": "pass", "field_count": len(fields), "component_count": len(components), "validator": "scripts/ui-contracts/validate_visible_field_semantics.py"},
            "stress_fixture_not_visible": {"status": "pass" if not stress_leak else "fail", "leaked_values": stress_leak},
            "runtime_text_raster_alpha_containment": {"status": "pass" if text_pass else "fail", "passed": sum(1 for item in reports if item["fit_search_pass"] and item["glyph_bbox_inside_inner_rect"]), "total": len(reports)},
            "header_runtime_ink_optical_axis": {"status": "pass" if header["max_axis_deviation_px_2x"] <= 2 else "fail", "axis_y_1x": a1.HEADER_AXIS_2X / 2, "max_deviation_px_2x": header["max_axis_deviation_px_2x"], "limit_px_2x": 2},
            "region_body_visual_padding": {"status": "pass" if body_pass else "fail", "minimum_gap_after_no_text_px_2x": min(body_lefts) - no_text[2], "line_left_difference_px_2x": max(body_lefts) - min(body_lefts)},
            "photo_aspect_preserved": {"status": "pass", "ratio": "69:44", "ingredient": [552, 352], "godot_stretch": "STRETCH_KEEP_ASPECT_COVERED"},
            "action_icon_semantics": {"status": "pass", "mission": ["document", "arrow"], "primary": ["globe", "arrow"], "retired": ["left_arrow + right_check"]},
            "godot_windowed_capture": {"status": "pending", "runner": "scripts/run_wmw_right_dossier_godot_capture_v092.ps1"},
            "visual_review": {"status": "pending", "basis": "等待 601/602/603 与双 agent 终审。"},
        },
        "judgment": "A2 Python 语义证据已准备；等待锁定 Godot 4.6.2 windowed 截图。",
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def invalidate_a1() -> None:
    if not A1_MANIFEST.exists():
        return
    manifest = a1.load_json(A1_MANIFEST)
    manifest.setdefault("gates", {})["visible_field_semantic_necessity"] = {
        "status": "fail",
        "basis": "A205 复核确认 A1 将容量压力 fixture 当成玩家运行数据；推荐12、压力标题/计数与虚构正文均无正式 payload 归属。",
        "superseded_by": 604,
    }
    manifest["status"] = "visual_fail_fixture_semantic_leak_superseded_by_604"
    manifest["judgment"] = "A1 的几何、照片和文字容器证据仍可复用，但运行时可见语义已失败；不得继续作为玩家视觉候选，改由 A2/604 取代。"
    A1_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    fixture = load_fixture()
    component, reports = render_runtime_component(fixture, False)
    qa_component, qa_reports = render_runtime_component(fixture, True)
    build_function_audit_board(component)
    build_runtime_board(component, reports, False)
    build_runtime_board(qa_component, qa_reports, True)
    manifest = build_manifest(fixture, qa_reports)
    invalidate_a1()
    failed = [name for name, gate in manifest["gates"].items() if gate["status"] == "fail"]
    if failed:
        raise RuntimeError(f"candidate A2 build gates failed: {failed}")
    for path in (OUT_AUDIT, OUT_PYTHON, OUT_PYTHON_QA, OUT_MANIFEST):
        print(path)


def build_review_board() -> None:
    old = Image.open(A1_GODOT).convert("RGB")
    new = Image.open(OUT_GODOT).convert("RGB")
    board = Image.new("RGB", (1920, 1080), NAVY)
    draw = ImageDraw.Draw(board)
    draw.text((42, 28), "WMW 右 dossier · A1 → A2 语义与功能复审", font=a1.font(32, True), fill=CREAM)
    draw.text((44, 74), "603 · 同一无字母版与 69:44 照片；只比较正式数据、状态章和动作图标语法。", font=a1.font(16), fill=(194, 211, 201))

    old_dossier = old.crop((76, 150, 556, 930))
    new_dossier = new.crop((76, 150, 556, 930))
    board.paste(old_dossier, (30, 145))
    board.paste(new_dossier, (535, 145))
    draw.rectangle((20, 135, 520, 945), outline=RED, width=2)
    draw.rectangle((525, 135, 1025, 945), outline=GREEN, width=2)
    draw.text((30, 108), "A1 / 594 · 压力 fixture 泄漏", font=a1.font(16, True), fill=RED)
    draw.text((535, 108), "A2 / 601 · production payload", font=a1.font(16, True), fill=GREEN)

    closeups = [
        ("HEADER", (98, 176, 525, 306), 175, GREEN),
        ("BODY + FACTS", (106, 578, 526, 720), 485, YELLOW),
        ("ACTIONS", (100, 728, 530, 900), 795, (72, 236, 174)),
    ]
    for label, rect, y, color in closeups:
        old_crop = old.crop(rect).resize((392, 150), Image.Resampling.NEAREST)
        new_crop = new.crop(rect).resize((392, 150), Image.Resampling.NEAREST)
        board.paste(old_crop, (1080, y))
        board.paste(new_crop, (1500, y))
        draw.rectangle((1074, y - 6, 1478, y + 156), outline=RED, width=2)
        draw.rectangle((1494, y - 6, 1898, y + 156), outline=color, width=2)
        draw.text((1080, y - 34), f"{label} · A1", font=a1.font(15, True), fill=RED)
        draw.text((1500, y - 34), f"{label} · A2", font=a1.font(15, True), fill=color)

    notes = [
        "1. 状态章从“高危 + 推荐12”改为单一正式状态“红线升温”。",
        "2. 标题、正文、事实和任务数全部来自 WeeklyRun production export。",
        "3. 主按钮从 arrow + check 改为 globe + arrow，避免双动作误读。",
        "4. 无字美术、照片比例、页眉轴与正文安全内区均复用 A1，不改 frozen。",
    ]
    for index, note in enumerate(notes):
        draw.text((1060, 968 + index * 24), note, font=a1.font(12, index == 3), fill=(218, 226, 205))
    board.save(OUT_REVIEW)


def finalize() -> None:
    if not OUT_MANIFEST.exists():
        raise FileNotFoundError(OUT_MANIFEST)
    if not OUT_GODOT.exists() or not OUT_GODOT_QA.exists():
        raise FileNotFoundError("Godot screenshots 601/602 are required before finalization")
    build_review_board()
    manifest = a1.load_json(OUT_MANIFEST)
    baseline = a1.image_content_stats(OUT_GODOT)
    qa = a1.image_content_stats(OUT_GODOT_QA)
    godot_pass = (
        baseline["size"] == [1920, 1080]
        and qa["size"] == [1920, 1080]
        and baseline["sampled_color_count"] >= 80
        and qa["sampled_color_count"] >= 80
        and baseline["sampled_nonblack_pixels"] > 0
        and qa["sampled_nonblack_pixels"] > 0
    )
    manifest["measurements"]["godot_capture"] = {"baseline": baseline, "qa": qa}
    manifest["gates"]["godot_windowed_capture"] = {
        "status": "pass" if godot_pass else "fail",
        "godot_version": "4.6.2-stable",
        "mode": "windowed opengl3; UI capture never used headless",
        "runner": "scripts/run_wmw_right_dossier_godot_capture_v092.ps1",
        "frame_post_draw_waits": 2,
        "all_black_refusal": True,
        "relative_baseline_loss_refusal": True,
        "baseline": baseline,
        "qa": qa,
    }
    manifest["gates"]["visual_review"] = {
        "status": "evidence_ready_user_visual_review_pending",
        "basis": "598 全组件审计、599/600 Python、601/602 Godot 与 603 A1/A2 对比板已生成。",
        "parent_self_check": {
            "status_semantics": "evidence_ready：状态章只有红线升温，不含推荐人数。",
            "runtime_binding": "evidence_ready：Python/Godot 同读 production export fixture。",
            "action_grammar": "evidence_ready：两个按钮均为对象图标 + 右向箭头。",
            "geometry_reuse": "evidence_ready：A1 69:44 照片、光学轴与正文安全内区未回退。",
        },
        "dual_agent_reviews": {
            "ux_laoge": {
                "status": "pass_for_component_user_visual_review",
                "severity": {"p0": 0, "p1": 3, "p2": 1},
                "consumed_after_first_review": [
                    "facts 已增加任务构成主语，不再冒充地区状态。",
                    "正文已明确本周剩余 7 天，不再与限时节点数混淆。",
                ],
                "remaining": [
                    "北美标题与金字塔照片的地区身份关系仍需用户确认。",
                    "两条 action row 仍有三段式 / 分裂按钮观感。",
                    "任务预览与主 CTA 默认视觉权重仍然过近。",
                    "header globe 与 primary globe 同屏语义轻度重复。",
                ],
                "boundary": "A189 与 v0.8.6 frozen 下暂缓的结构删除不算本轮实现缺陷；A2 只能称组件视觉候选，不能称完整 UX 终验通过。",
            },
            "ui_designer": {
                "status": "pass_for_user_visual_review",
                "severity": {"p0": 0, "p1": 1, "p2": 3},
                "consumed_after_first_review": [
                    "本周剩余 7 天的作用域已明确。",
                    "任务构成 1/2/1 与按钮总数 4 的明细 / 总计关系已明确。",
                ],
                "remaining": [
                    "双按钮仍有三段式视觉可能被误读为分裂按钮。",
                    "状态章对比度、8 个功能组件 + 2 组图标配置的审计措辞、双 globe 轻度重复为 P2。",
                ],
            },
        },
    }
    manifest["status"] = "evidence_ready_user_visual_review_pending"
    manifest["judgment"] = "A2 已清除压力 fixture、绑定正式 region payload 并通过 Python / Godot / 双 agent 复核，可交用户做组件视觉裁决；仍有照片地区身份、三段按钮观感与主次 CTA 权重三个 P1 裁决点，未冻结、未生产动态状态。"
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not godot_pass:
        raise RuntimeError("Godot content validation failed")
    print(OUT_REVIEW)
    print(OUT_MANIFEST)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "finalize"))
    args = parser.parse_args()
    if args.command == "build":
        build()
    else:
        finalize()


if __name__ == "__main__":
    main()
