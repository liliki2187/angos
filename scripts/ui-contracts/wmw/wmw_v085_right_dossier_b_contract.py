from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

import wmw_right_dossier_a184_capacity_review as preflight


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
DOSSIER_PATH = ROOT / "design" / "ui-contracts" / "world-map" / "right_dossier_page.json"
PRIMARY_PATH = ROOT / "design" / "ui-contracts" / "world-map" / "right_action_lane.json"
MISSION_PATH = ROOT / "design" / "ui-contracts" / "world-map" / "right_mission_intel_button.json"
FULLSCREEN_SOURCE = BASE / "365-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-full.png"

OUT_CONTRACT = BASE / "567-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-contract-board.png"
OUT_STRESS = BASE / "568-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-state-stress.png"
OUT_REINSERT = BASE / "569-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-reinsert.png"
OUT_MANIFEST = BASE / "570-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-manifest.json"

UPPER_SLOTS = {
    "title_slot": [82, 42, 160, 34],
    "status_stamp": [246, 34, 58, 58],
    "photo_slot": [22, 98, 276, 176],
}
LOWER_SLOTS = dict(preflight.PROPOSED_SLOTS)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


DOSSIER = load_json(DOSSIER_PATH)
PRIMARY = load_json(PRIMARY_PATH)
MISSION = load_json(MISSION_PATH)


def rects_intersect(a: list[int], b: list[int]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def contract_assertions() -> dict[str, Any]:
    slots = DOSSIER["frozen"]["slots"]
    origin = DOSSIER["frozen"]["positions"][0]
    upper_exact = {name: slots[name] == rect for name, rect in UPPER_SLOTS.items()}
    lower_exact = {name: slots[name] == rect for name, rect in LOWER_SLOTS.items()}
    primary_absolute = [
        origin[0] + LOWER_SLOTS["primary_enter_cta"][0],
        origin[1] + LOWER_SLOTS["primary_enter_cta"][1],
    ]
    mission_absolute = [
        origin[0] + LOWER_SLOTS["mission_intel_button"][0],
        origin[1] + LOWER_SLOTS["mission_intel_button"][1],
    ]
    lower_values = list(LOWER_SLOTS.values())
    overlap_pairs = []
    names = list(LOWER_SLOTS)
    for index, first in enumerate(lower_values):
        for second_index in range(index + 1, len(lower_values)):
            if rects_intersect(first, lower_values[second_index]):
                overlap_pairs.append([names[index], names[second_index]])
    checks = {
        "contract_versions": {
            "right_dossier_page": DOSSIER["contract_version"],
            "right_action_lane": PRIMARY["contract_version"],
            "right_mission_intel_button": MISSION["contract_version"],
        },
        "upper_slots_unchanged": upper_exact,
        "lower_slots_exact": lower_exact,
        "primary_child_position": {
            "expected": primary_absolute,
            "actual": PRIMARY["frozen"]["positions"][0],
            "pass": primary_absolute == PRIMARY["frozen"]["positions"][0],
        },
        "mission_child_position": {
            "expected": mission_absolute,
            "actual": MISSION["frozen"]["positions"][0],
            "pass": mission_absolute == MISSION["frozen"]["positions"][0],
        },
        "lower_slot_overlap_pairs": overlap_pairs,
        "interactive_components": ["right_mission_intel_button", "right_action_lane"],
        "read_only_carriers": ["region_body", "decision_facts"],
    }
    pass_flags = (
        all(upper_exact.values())
        and all(lower_exact.values())
        and checks["primary_child_position"]["pass"]
        and checks["mission_child_position"]["pass"]
        and not overlap_pairs
        and DOSSIER["frozen"]["export_size"] == [320, 520]
    )
    checks["pass"] = pass_flags
    if not pass_flags:
        raise AssertionError(json.dumps(checks, ensure_ascii=False, indent=2))
    return checks


def image_metrics(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    colors = image.getcolors(maxcolors=image.width * image.height)
    pixels = image.get_flattened_data()
    return {
        "size": [image.width, image.height],
        "unique_colors": len(colors) if colors is not None else "more_than_pixel_limit",
        "non_black_pixels": sum(1 for pixel in pixels if max(pixel) > 8),
    }


def normalize_reports(reports: list[dict[str, Any]], scale: float) -> list[dict[str, Any]]:
    normalized = []
    for report in reports:
        item = dict(report)
        item["font_size_reference"] = round(report["font_size"] / scale, 2)
        normalized.append(item)
    return normalized


def text_bbox_assertions(report_groups: list[list[dict[str, Any]]]) -> dict[str, Any]:
    items = []
    for reports in report_groups:
        for report in reports:
            origin = report["draw_origin"]
            relative = report["raster_bbox_relative_to_draw_origin"]
            reconstructed = [
                origin[0] + relative[0],
                origin[1] + relative[1],
                origin[0] + relative[2],
                origin[1] + relative[3],
            ]
            passed = (
                report["bbox_source"] == "raster_alpha_bbox"
                and report["bbox"] == report["raster_glyph_bbox"]
                and reconstructed == report["raster_glyph_bbox"]
                and report["glyph_bbox_inside_inner_rect"] is True
                and report["manual_y_offset_px"] == 0
            )
            items.append(
                {
                    "field": report["field"],
                    "text": report["text"],
                    "font_size": report["font_size"],
                    "font_metric_offset_relative_to_draw_origin": report["font_metric_bbox_relative_to_draw_origin"][:2],
                    "overlay_bbox": report["bbox"],
                    "raster_glyph_bbox": report["raster_glyph_bbox"],
                    "reconstructed_raster_bbox": reconstructed,
                    "inner_rect": report["inner_rect"],
                    "pass": passed,
                }
            )
    result = {
        "gate": "actual_raster_glyph_bbox_integrity",
        "layout_engine": "scripts/ui-contracts/wmw/wmw_text_layout_metrics.py",
        "validator": "scripts/ui-contracts/validate_text_bbox_evidence.py",
        "report_count": len(items),
        "all_overlay_boxes_use_raster_alpha_bbox": all(item["pass"] for item in items),
        "manual_y_offset_count": 0,
        "pass": bool(items) and all(item["pass"] for item in items),
        "items": items,
    }
    if not result["pass"]:
        raise AssertionError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def draw_slot_map(draw: ImageDraw.ImageDraw, origin: tuple[int, int], scale: float) -> None:
    x, y = origin
    w, h = DOSSIER["frozen"]["export_size"]
    outer = (x, y, x + round(w * scale), y + round(h * scale))
    draw.rectangle(outer, fill=(17, 37, 38, 255), outline=(*preflight.CREAM, 255), width=2)
    colors = {
        "region_body": (95, 198, 216),
        "decision_facts": (196, 177, 83),
        "mission_intel_button": (44, 153, 163),
        "primary_enter_cta": (184, 126, 31),
    }
    for name, rect in LOWER_SLOTS.items():
        box = preflight.rect_xyxy(rect, origin, scale)
        fill = colors[name]
        draw.rectangle(box, fill=(*fill, 190), outline=(*preflight.CREAM, 225), width=2)
        label = "只读" if name in ("region_body", "decision_facts") else "可点击"
        draw.text(
            (box[0] + 8, box[1] + 5),
            f"{name}  {label}",
            font=preflight.font(preflight.FONT_BOLD, 14),
            fill=preflight.CREAM,
        )


def build_contract_board(checks: dict[str, Any]) -> list[dict[str, Any]]:
    canvas = Image.new("RGB", (1920, 1080), preflight.BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    preflight.draw_heading(draw, (42, 28), "WMW 右侧 dossier v0.8.5：方案 B 光栅 bbox 修正版", 30)
    draw.text(
        (44, 70),
        "567 修正字体 bearing：洋红框直接读取实际 alpha 字形 bbox，不再用绘制原点拼框。",
        font=preflight.font(preflight.FONT_REGULAR, 16),
        fill=(203, 220, 203),
    )

    preflight.draw_heading(draw, (70, 118), "WARNING 合同回填", 20, preflight.GREEN)
    reports = preflight.draw_proposed(canvas, (70, 156), 1.55, preflight.PROPOSED_SCENARIOS[1], qa=True)
    draw.text((72, 982), "粉框=真实光栅字形；合同几何与 A189 方案 B 均不变", font=preflight.font(preflight.FONT_BOLD, 15), fill=preflight.GREEN)

    draw.rectangle((610, 116, 1280, 1012), fill=(12, 36, 37, 235), outline=(75, 129, 118, 220), width=2)
    preflight.draw_heading(draw, (642, 145), "冻结几何", 22)
    geometry_lines = [
        "dossier：320×520 @ (932,30)",
        "title_slot：[82,42,160,34]（不动）",
        "status_stamp：[246,34,58,58]（不动）",
        "photo_slot：[22,98,276,176]（不动）",
        "region_body：[22,288,276,54]",
        "decision_facts：[22,346,276,32]",
        "mission_intel_button：[22,390,276,44]",
        "primary_enter_cta：[16,444,284,50]",
    ]
    for index, line in enumerate(geometry_lines):
        color = (222, 235, 217) if index < 4 else (123, 222, 218)
        draw.text((646, 195 + index * 44), line, font=preflight.font(preflight.FONT_REGULAR, 16), fill=color)

    preflight.draw_heading(draw, (642, 590), "归属与硬边界", 20)
    ownership_lines = [
        "region_body / decision_facts：只读，不继承热区",
        "任务情报：唯一的次级按钮",
        "进入选定地区：最底部唯一主 CTA",
        "主 CTA 不拼地区名、不绑定天数",
        "locked / warning 的未决行为仍留 provisional",
    ]
    for index, line in enumerate(ownership_lines):
        draw.text((646, 634 + index * 48), line, font=preflight.font(preflight.FONT_REGULAR, 16), fill=(228, 226, 202))
    draw.text((646, 908), "几何断言：PASS" if checks["pass"] else "几何断言：FAIL", font=preflight.font(preflight.FONT_BOLD, 21), fill=preflight.GREEN if checks["pass"] else preflight.RED)
    draw.text((646, 950), "文字框来源：raster alpha bbox", font=preflight.font(preflight.FONT_BOLD, 17), fill=preflight.GREEN)

    preflight.draw_heading(draw, (1330, 118), "交互热区图", 20)
    draw.text((1332, 150), "灰蓝=只读 carrier；青 / 金=仅有的两个按钮", font=preflight.font(preflight.FONT_REGULAR, 14), fill=(203, 220, 203))
    draw_slot_map(draw, (1360, 210), 1.25)
    draw.text((1332, 895), "旧 3× action lane 已退役", font=preflight.font(preflight.FONT_BOLD, 17), fill=(255, 181, 132))
    draw.text((1332, 936), "下半部槽位互相交叠：0", font=preflight.font(preflight.FONT_BOLD, 17), fill=preflight.GREEN)
    draw.text((1332, 977), "下一 gate：无字 clean-sprite brief", font=preflight.font(preflight.FONT_REGULAR, 15), fill=(222, 229, 205))
    canvas.save(OUT_CONTRACT)
    return reports


def build_stress_board() -> dict[str, list[dict[str, Any]]]:
    canvas = Image.new("RGB", (1920, 1080), preflight.BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    preflight.draw_heading(draw, (40, 24), "v0.8.5 方案 B：实际光栅 bbox 三状态文字压力", 28)
    draw.text((42, 63), "1.5× 运行时尺度；彩框=合同 carrier，洋红框=渲染 alpha 的真实 glyph bbox。", font=preflight.font(preflight.FONT_REGULAR, 15), fill=(203, 220, 203))
    positions = [70, 650, 1230]
    state_names = {"default": "DEFAULT 可进入", "warning": "WARNING 高危", "locked": "LOCKED 锁定"}
    all_reports: dict[str, list[dict[str, Any]]] = {}
    for x, scenario in zip(positions, preflight.PROPOSED_SCENARIOS):
        preflight.draw_heading(draw, (x, 105), state_names[scenario["id"]], 19)
        reports = preflight.draw_proposed(canvas, (x, 145), 1.5, scenario, qa=True)
        all_reports[scenario["id"]] = reports
        passed = sum(1 for report in reports if report["fits"])
        minimum = min(report["font_size"] for report in reports)
        draw.text((x, 946), f"fit {passed}/{len(reports)} · 最小运行时字号 {minimum}px", font=preflight.font(preflight.FONT_BOLD, 15), fill=preflight.GREEN if passed == len(reports) else preflight.RED)
        draw.text((x, 979), "底部主 CTA 固定；锁定态仅禁用，不改几何。", font=preflight.font(preflight.FONT_REGULAR, 14), fill=(220, 220, 200))
    draw.text((42, 1041), "无 synthetic bbox / 无手工 y 偏移；容量通过仍不等于生产美术或 Godot 运行验收。", font=preflight.font(preflight.FONT_REGULAR, 14), fill=(255, 194, 145))
    canvas.save(OUT_STRESS)
    return all_reports


def build_reinsert() -> list[dict[str, Any]]:
    canvas = Image.open(FULLSCREEN_SOURCE).convert("RGB") if FULLSCREEN_SOURCE.exists() else Image.new("RGB", (1280, 720), preflight.BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((918, 18, 1279, 574), fill=(*preflight.BG, 248))
    reports = preflight.draw_proposed(canvas, tuple(DOSSIER["frozen"]["positions"][0]), 1.0, preflight.PROPOSED_SCENARIOS[1], qa=False)
    draw.rectangle((278, 24, 824, 84), fill=(*preflight.BG, 232), outline=(74, 130, 119, 220), width=1)
    draw.text((294, 36), "A189 / v0.8.5 方案 B：raster bbox 修正版整屏回填", font=preflight.font(preflight.FONT_BOLD, 17), fill=preflight.CREAM)
    draw.text((294, 62), "右侧文字已按实际字形居中；背景左卡为历史整屏证据。", font=preflight.font(preflight.FONT_REGULAR, 13), fill=(203, 220, 203))
    canvas.save(OUT_REINSERT)
    return reports


def write_manifest(
    checks: dict[str, Any],
    contract_reports: list[dict[str, Any]],
    stress_reports: dict[str, list[dict[str, Any]]],
    reinsert_reports: list[dict[str, Any]],
) -> None:
    all_state_fit = all(report["fits"] for reports in stress_reports.values() for report in reports)
    bbox_checks = text_bbox_assertions(
        [contract_reports, *stress_reports.values(), reinsert_reports]
    )
    data = {
        "artifact": "WMW right dossier option B raster glyph bbox correction",
        "date": "2026-07-14",
        "artifact_type": "component_contract / text_capacity_stress / full_screen_reinsert / not production art / not atlas / not Godot runtime",
        "status": "contract_v0_8_5_raster_bbox_pass_ready_for_clean_sprite_brief",
        "user_decision": "A189: option B adopted",
        "supersedes": {
            "manifest": "docs/screenshots/2026-06-24-world-map-benchmark-landing/566-world-map-wmw-v0-8-5-right-dossier-b-contract-manifest.json",
            "reason": "563-566 discarded font bearing offsets and drew synthetic overlay boxes from draw origin plus width/height.",
        },
        "contracts": {
            "right_dossier_page": str(DOSSIER_PATH.relative_to(ROOT)).replace("\\", "/"),
            "right_action_lane": str(PRIMARY_PATH.relative_to(ROOT)).replace("\\", "/"),
            "right_mission_intel_button": str(MISSION_PATH.relative_to(ROOT)).replace("\\", "/"),
            "versions": checks["contract_versions"],
        },
        "authorized_contract_mutation": {
            "performed": True,
            "authorization": "User explicitly adopted option B; recorded as A189.",
            "upper_geometry_changed": False,
            "lower_geometry_changed": True,
            "retired": ["right_dossier_page.frozen.slots.meta_slot", "right_dossier_page.frozen.slots.action_stack", "right_action_lane three-instance layout"],
            "added": list(LOWER_SLOTS),
        },
        "outputs": {
            "contract_board": str(OUT_CONTRACT.relative_to(ROOT)).replace("\\", "/"),
            "state_stress": str(OUT_STRESS.relative_to(ROOT)).replace("\\", "/"),
            "full_screen_reinsert": str(OUT_REINSERT.relative_to(ROOT)).replace("\\", "/"),
            "manifest": str(OUT_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        },
        "contract_assertions": checks,
        "text_capacity": {
            "all_states_pass": all_state_fit,
            "bbox_gate": bbox_checks,
            "reports_contract_board_warning_scale_1_55": normalize_reports(contract_reports, 1.55),
            "reports_state_stress_scale_1_5": {state: normalize_reports(reports, 1.5) for state, reports in stress_reports.items()},
            "reports_full_screen_warning_scale_1_0": normalize_reports(reinsert_reports, 1.0),
        },
        "interaction_ownership": {
            "read_only": ["region_body", "decision_facts"],
            "interactive": ["right_mission_intel_button", "right_action_lane as primary_enter_cta"],
            "interactive_hit_rect_count": 2,
            "legacy_three_lane_hot_regions_retired": True,
        },
        "provisional_semantics": {
            "locked_secondary_action": "查看解锁条件 vs 查看已知任务情报 remains pending",
            "warning_entry_confirmation": "pending runtime decision",
            "entry_cost_terminology": "A184 entry-cost wording conflicts with current GDD; fixture uses 地区任务耗时预览 and the enter CTA carries no day cost",
        },
        "image_content_checks": {
            "contract_board": image_metrics(OUT_CONTRACT),
            "state_stress": image_metrics(OUT_STRESS),
            "full_screen_reinsert": image_metrics(OUT_REINSERT),
        },
        "scope_guard": {
            "imagegen_called": False,
            "production_art_created": False,
            "atlas_created": False,
            "godot_runtime_capture_created": False,
            "other_classes_batch_produced": False,
        },
        "judgment": "Option B contract geometry and three-state text capacity pass after raster-alpha bbox correction. Overlay boxes, centering, manifest bbox, and containment gate now share one measured source. This is contract evidence only; visual asset production has not started.",
        "next_gate": "Author the right dossier v0.8.5 no-text clean-sprite brief, then run one vertical slice before any batch production.",
    }
    if not all_state_fit:
        raise AssertionError("Text capacity stress failed")
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    current_versions = {
        DOSSIER["contract_version"],
        PRIMARY["contract_version"],
        MISSION["contract_version"],
    }
    if current_versions != {"0.8.5"}:
        raise RuntimeError(
            "Historical v0.8.5 evidence is version-locked. "
            "Use wmw_v086_right_dossier_alignment.py for the current contracts."
        )
    BASE.mkdir(parents=True, exist_ok=True)
    checks = contract_assertions()
    contract_reports = build_contract_board(checks)
    stress_reports = build_stress_board()
    reinsert_reports = build_reinsert()
    write_manifest(checks, contract_reports, stress_reports, reinsert_reports)
    for path in (OUT_CONTRACT, OUT_STRESS, OUT_REINSERT, OUT_MANIFEST):
        print(path)


if __name__ == "__main__":
    main()
