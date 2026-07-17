from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

import wmw_right_dossier_a184_capacity_review as preflight
import wmw_v085_right_dossier_b_contract as raster_helper
import wmw_v085_right_dossier_clean_sprite_brief as brief_helper


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
CONTRACT_DIR = ROOT / "design" / "ui-contracts" / "world-map"
DOSSIER_PATH = CONTRACT_DIR / "right_dossier_page.json"
MISSION_PATH = CONTRACT_DIR / "right_mission_intel_button.json"
PRIMARY_PATH = CONTRACT_DIR / "right_action_lane.json"
FULLSCREEN_SOURCE = BASE / "569-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-reinsert.png"

OUT_ALIGNMENT = BASE / "573-world-map-wmw-v0-8-6-right-dossier-action-stack-alignment.png"
OUT_STRESS = BASE / "574-world-map-wmw-v0-8-6-right-dossier-raster-bbox-state-stress.png"
OUT_REINSERT = BASE / "575-world-map-wmw-v0-8-6-right-dossier-full-screen-reinsert.png"
OUT_BRIEF = BASE / "576-world-map-wmw-v0-8-6-right-dossier-clean-sprite-brief-board.png"
OUT_MANIFEST = BASE / "577-world-map-wmw-v0-8-6-right-dossier-alignment-manifest.json"

OLD_MISSION = [22, 390, 276, 44]
OLD_PRIMARY = [16, 444, 284, 50]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


DOSSIER = load_json(DOSSIER_PATH)
MISSION = load_json(MISSION_PATH)
PRIMARY = load_json(PRIMARY_PATH)
LOWER_SLOTS = {
    name: DOSSIER["frozen"]["slots"][name]
    for name in ("region_body", "decision_facts", "mission_intel_button", "primary_enter_cta")
}

# The existing raster text fixture is retained, but its geometry source is replaced
# by the current contract before any drawing occurs.
preflight.PROPOSED_SLOTS = dict(LOWER_SLOTS)


def rect_edges(rect: list[int]) -> dict[str, float]:
    x, _, width, _ = rect
    return {
        "left": x,
        "right": x + width,
        "width": width,
        "center_x": x + width / 2,
    }


def rects_intersect(a: list[int], b: list[int]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def contract_assertions() -> dict[str, Any]:
    mission = LOWER_SLOTS["mission_intel_button"]
    primary = LOWER_SLOTS["primary_enter_cta"]
    mission_edges = rect_edges(mission)
    primary_edges = rect_edges(primary)
    origin = DOSSIER["frozen"]["positions"][0]
    overlap_pairs: list[list[str]] = []
    names = list(LOWER_SLOTS)
    for index, first_name in enumerate(names):
        for second_name in names[index + 1 :]:
            if rects_intersect(LOWER_SLOTS[first_name], LOWER_SLOTS[second_name]):
                overlap_pairs.append([first_name, second_name])

    expected_mission_position = [origin[0] + mission[0], origin[1] + mission[1]]
    expected_primary_position = [origin[0] + primary[0], origin[1] + primary[1]]
    alignment = {
        "measurement_target": "contract slot / future visible_body_bbox excludes shadow_bbox",
        "mission": mission_edges,
        "primary": primary_edges,
        "left_edge_diff": abs(mission_edges["left"] - primary_edges["left"]),
        "right_edge_diff": abs(mission_edges["right"] - primary_edges["right"]),
        "center_x_diff": abs(mission_edges["center_x"] - primary_edges["center_x"]),
        "width_diff": abs(mission_edges["width"] - primary_edges["width"]),
    }
    alignment["pass"] = all(
        alignment[name] == 0
        for name in ("left_edge_diff", "right_edge_diff", "center_x_diff", "width_diff")
    )
    checks = {
        "contract_versions": {
            "right_dossier_page": DOSSIER["contract_version"],
            "right_mission_intel_button": MISSION["contract_version"],
            "right_action_lane": PRIMARY["contract_version"],
        },
        "expected_version": "0.8.6",
        "action_stack_alignment": alignment,
        "mission_child": {
            "slot": mission,
            "expected_position": expected_mission_position,
            "actual_position": MISSION["frozen"]["positions"][0],
            "export_size": MISSION["frozen"]["export_size"],
            "hit_rect": MISSION["frozen"]["hit_rect"],
        },
        "primary_child": {
            "slot": primary,
            "expected_position": expected_primary_position,
            "actual_position": PRIMARY["frozen"]["positions"][0],
            "export_size": PRIMARY["frozen"]["export_size"],
            "hit_rect": PRIMARY["frozen"]["hit_rect"],
        },
        "lower_slot_overlap_pairs": overlap_pairs,
        "upper_geometry_unchanged": all(
            DOSSIER["frozen"]["slots"][name] == value
            for name, value in {
                "header_icon": [24, 38, 36, 36],
                "title_slot": [82, 42, 160, 34],
                "status_stamp": [246, 34, 58, 58],
                "photo_slot": [22, 98, 276, 176],
                "region_body": [22, 288, 276, 54],
                "decision_facts": [22, 346, 276, 32],
            }.items()
        ),
        "child_internal_slots_unchanged": {
            "mission": MISSION["frozen"]["slots"]
            == {
                "left_icon_zone": [10, 5, 34, 34],
                "label_plate": [58, 6, 170, 32],
                "right_action_badge": [232, 4, 40, 36],
            },
            "primary": PRIMARY["frozen"]["slots"]
            == {
                "left_icon_zone": [12, 8, 34, 34],
                "label_plate": [62, 9, 170, 32],
                "right_action_badge": [238, 5, 42, 40],
            },
        },
        "visible_body_bbox_policy": {
            "locked": True,
            "shadow_excluded": True,
            "candidate_required_diffs": {
                "left_edge_diff": 0,
                "right_edge_diff": 0,
                "center_x_diff": 0,
            },
            "asset_measurement": "pending clean-sprite candidate; no production art in this round",
        },
    }
    checks["pass"] = (
        all(version == "0.8.6" for version in checks["contract_versions"].values())
        and alignment["pass"]
        and expected_mission_position == MISSION["frozen"]["positions"][0]
        and expected_primary_position == PRIMARY["frozen"]["positions"][0]
        and MISSION["frozen"]["export_size"] == [284, 44]
        and MISSION["frozen"]["hit_rect"] == [0, 0, 284, 44]
        and PRIMARY["frozen"]["export_size"] == [284, 50]
        and PRIMARY["frozen"]["hit_rect"] == [0, 0, 284, 50]
        and not overlap_pairs
        and checks["upper_geometry_unchanged"]
        and all(checks["child_internal_slots_unchanged"].values())
    )
    if not checks["pass"]:
        raise AssertionError(json.dumps(checks, ensure_ascii=False, indent=2))
    return checks


def panel(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], title: str) -> None:
    draw.rectangle(rect, fill=(12, 36, 37, 245), outline=(75, 129, 118, 220), width=2)
    preflight.draw_heading(draw, (rect[0] + 24, rect[1] + 18), title, 21)


def draw_action_pair(
    draw: ImageDraw.ImageDraw,
    origin: tuple[int, int],
    mission: list[int],
    primary: list[int],
    scale: float,
    color: tuple[int, int, int],
    label: str,
) -> None:
    ox, oy = origin
    center_x = round(ox + 160 * scale)
    draw.line((center_x, oy - 18, center_x, oy + 190), fill=(*preflight.CYAN, 170), width=2)
    for index, (name, rect) in enumerate((("MISSION", mission), ("PRIMARY", primary))):
        x, _, width, height = rect
        y = oy + index * 92
        box = (round(ox + x * scale), y, round(ox + (x + width) * scale), y + round(height * scale))
        draw.rectangle(box, fill=(*color, 75), outline=(*color, 255), width=4)
        draw.text((box[0] + 10, box[1] + 10), name, font=preflight.font(preflight.FONT_BOLD, 14), fill=preflight.CREAM)
        local_center = x + width / 2
        draw.text(
            (box[0] + 10, box[3] + 7),
            f"x={x}  w={width}  center={local_center:g}",
            font=preflight.font(preflight.FONT_REGULAR, 13),
            fill=color,
        )
    draw.text((ox, oy + 205), label, font=preflight.font(preflight.FONT_BOLD, 15), fill=color)


def build_alignment_board(checks: dict[str, Any]) -> list[dict[str, Any]]:
    canvas = Image.new("RGB", (1920, 1080), preflight.BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    preflight.draw_heading(draw, (42, 28), "WMW 右 dossier v0.8.6：A196 同宽动作栈", 30)
    draw.text(
        (44, 70),
        "573 · 合同几何 + raster glyph bbox；结构证据，不是生产美术。",
        font=preflight.font(preflight.FONT_REGULAR, 16),
        fill=(203, 220, 203),
    )

    panel(draw, (38, 116, 610, 1010), "1 · 旧误差 / 新规则")
    preflight.draw_heading(draw, (70, 170), "v0.8.5 近似居中：FAIL", 18, preflight.RED)
    draw_action_pair(draw, (84, 230), OLD_MISSION, OLD_PRIMARY, 1.42, preflight.RED, "中心差 2px · 左右边缘都不共线")
    preflight.draw_heading(draw, (70, 535), "v0.8.6 双边共线：PASS", 18, preflight.GREEN)
    draw_action_pair(
        draw,
        (84, 595),
        LOWER_SLOTS["mission_intel_button"],
        LOWER_SLOTS["primary_enter_cta"],
        1.42,
        preflight.GREEN,
        "width 284/284 · center 160/160 · edge diff 0",
    )
    draw.text((70, 900), "高度保留 44 / 50；主次不靠宽度差。", font=preflight.font(preflight.FONT_BOLD, 15), fill=preflight.CREAM)

    panel(draw, (628, 116, 1230, 1010), "2 · WARNING 真实文字回填")
    reports = preflight.draw_proposed(canvas, (690, 175), 1.48, preflight.PROPOSED_SCENARIOS[1], qa=True)
    passed = sum(1 for report in reports if report["fits"])
    draw.text((666, 952), f"raster alpha glyph bbox：{passed}/{len(reports)} fit", font=preflight.font(preflight.FONT_BOLD, 17), fill=preflight.GREEN if passed == len(reports) else preflight.RED)

    panel(draw, (1248, 116, 1882, 1010), "3 · 对齐判据冻结")
    lines = [
        "父页中心：x=160",
        "两条主体：x=18..302",
        "left_edge_diff = 0",
        "right_edge_diff = 0",
        "center_x_diff = 0",
        "width_diff = 0",
        "mission export：284x44 @ (950,420)",
        "primary export：284x50 @ (950,474)",
    ]
    for index, line in enumerate(lines):
        draw.text((1280, 176 + index * 43), line, font=preflight.font(preflight.FONT_REGULAR, 16), fill=preflight.GREEN if "diff" in line else preflight.CREAM)
    draw.rectangle((1280, 560, 1848, 812), fill=(9, 27, 29, 240), outline=preflight.GOLD, width=2)
    preflight.draw_heading(draw, (1306, 584), "VISIBLE BODY != SHADOW", 19, preflight.GOLD)
    draw.rectangle((1320, 650, 1770, 724), fill=(*preflight.CYAN, 85), outline=preflight.CREAM, width=3)
    draw.rectangle((1332, 661, 1790, 742), outline=(*preflight.GOLD, 210), width=3)
    draw.text((1320, 758), "奶油框=主体对齐 bbox；金框=独立 shadow bbox", font=preflight.font(preflight.FONT_REGULAR, 14), fill=preflight.CREAM)
    draw.text((1280, 852), "候选素材必须实测两种 bbox，禁止拿 export rect 代替肉眼轮廓。", font=preflight.font(preflight.FONT_BOLD, 14), fill=(255, 194, 145))
    draw.text((1280, 914), "CONTRACT ASSERTIONS PASS" if checks["pass"] else "CONTRACT ASSERTIONS FAIL", font=preflight.font(preflight.FONT_BOLD, 20), fill=preflight.GREEN if checks["pass"] else preflight.RED)
    canvas.save(OUT_ALIGNMENT)
    return reports


def build_stress_board() -> dict[str, list[dict[str, Any]]]:
    canvas = Image.new("RGB", (1920, 1080), preflight.BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    preflight.draw_heading(draw, (40, 24), "v0.8.6 同宽动作栈：实际光栅 bbox 三状态压力", 28)
    draw.text((42, 63), "574 · 1.5x 运行时尺度；彩框=合同 carrier，洋红框=实际 alpha glyph bbox。", font=preflight.font(preflight.FONT_REGULAR, 15), fill=(203, 220, 203))
    positions = [70, 650, 1230]
    names = {"default": "DEFAULT 可进入", "warning": "WARNING 高危", "locked": "LOCKED 锁定"}
    all_reports: dict[str, list[dict[str, Any]]] = {}
    for x, scenario in zip(positions, preflight.PROPOSED_SCENARIOS):
        preflight.draw_heading(draw, (x, 105), names[scenario["id"]], 19)
        reports = preflight.draw_proposed(canvas, (x, 145), 1.5, scenario, qa=True)
        all_reports[scenario["id"]] = reports
        passed = sum(1 for report in reports if report["fits"])
        minimum = min(report["font_size"] for report in reports)
        draw.text((x, 946), f"fit {passed}/{len(reports)} · 最小运行时字号 {minimum}px", font=preflight.font(preflight.FONT_BOLD, 15), fill=preflight.GREEN if passed == len(reports) else preflight.RED)
        draw.text((x, 979), "284px 共宽；高度与状态反馈继续区分主次。", font=preflight.font(preflight.FONT_REGULAR, 14), fill=(220, 220, 200))
    draw.text((42, 1041), "排版、粉框与 manifest 共用 raster alpha bbox；无 synthetic bbox / 无手工 y 偏移。", font=preflight.font(preflight.FONT_REGULAR, 14), fill=(255, 194, 145))
    canvas.save(OUT_STRESS)
    return all_reports


def build_reinsert() -> list[dict[str, Any]]:
    if FULLSCREEN_SOURCE.exists():
        canvas = Image.open(FULLSCREEN_SOURCE).convert("RGB")
    else:
        canvas = Image.new("RGB", (1280, 720), preflight.BG)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((918, 18, 1279, 574), fill=(*preflight.BG, 248))
    reports = preflight.draw_proposed(canvas, tuple(DOSSIER["frozen"]["positions"][0]), 1.0, preflight.PROPOSED_SCENARIOS[1], qa=False)
    draw.rectangle((278, 24, 866, 86), fill=(*preflight.BG, 235), outline=(74, 130, 119, 220), width=1)
    draw.text((294, 35), "A196 / v0.8.6：两条功能条 284px 同宽、中心 x=160", font=preflight.font(preflight.FONT_BOLD, 16), fill=preflight.CREAM)
    draw.text((294, 62), "右侧仅为结构与文字回填；未生产 clean sprite。", font=preflight.font(preflight.FONT_REGULAR, 13), fill=(203, 220, 203))
    canvas.save(OUT_REINSERT)
    return reports


def build_brief_board() -> None:
    brief_helper.OUT_BOARD = OUT_BRIEF
    brief_helper.create_board()
    canvas = Image.open(OUT_BRIEF).convert("RGB")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, 1920, 120), fill=(*brief_helper.BG, 255))
    draw.text((42, 30), "WMW 右侧 dossier v0.8.6 · 无字 clean-sprite 结构 brief", font=brief_helper.load_font(38, True), fill=brief_helper.CREAM)
    draw.text((44, 81), "576 · A196 同宽动作栈 / 父子像素所有权 / 状态派生 / CTA 色族仍阻塞", font=brief_helper.load_font(19), fill=brief_helper.MUTED)
    draw.rectangle((1561, 27, 1878, 88), fill=(40, 33, 20), outline=brief_helper.HOLD, width=2)
    draw.text((1583, 39), "STRUCTURE ONLY", font=brief_helper.load_font(21, True), fill=brief_helper.HOLD)
    draw.text((1583, 67), "非生产美术 · 零 imagegen", font=brief_helper.load_font(13), fill=brief_helper.CREAM)

    scale = 1.34
    origin = (82, 178)
    mission = LOWER_SLOTS["mission_intel_button"]
    primary = LOWER_SLOTS["primary_enter_cta"]
    left = round(origin[0] + mission[0] * scale)
    right = round(origin[0] + (mission[0] + mission[2]) * scale)
    top = round(origin[1] + mission[1] * scale) - 8
    bottom = round(origin[1] + (primary[1] + primary[3]) * scale) + 8
    draw.line((left, top, left, bottom), fill=(*brief_helper.GREEN, 235), width=2)
    draw.line((right, top, right, bottom), fill=(*brief_helper.GREEN, 235), width=2)
    draw.text((left + 8, top - 23), "visible body edges · shadow excluded", font=brief_helper.load_font(12, True), fill=brief_helper.GREEN)
    canvas.save(OUT_BRIEF)


def write_manifest(
    checks: dict[str, Any],
    alignment_reports: list[dict[str, Any]],
    stress_reports: dict[str, list[dict[str, Any]]],
    reinsert_reports: list[dict[str, Any]],
) -> None:
    all_state_fit = all(report["fits"] for reports in stress_reports.values() for report in reports)
    bbox_gate = raster_helper.text_bbox_assertions(
        [alignment_reports, *stress_reports.values(), reinsert_reports]
    )
    data = {
        "artifact": "WMW right dossier v0.8.6 A196 aligned action stack",
        "date": "2026-07-14",
        "artifact_type": "component_contract / text_capacity_stress / full_screen_reinsert / clean-sprite brief board / not production art / not atlas / not Godot runtime",
        "status": {
            "contract_v0_8_6": "pass",
            "text_capacity": "pass" if all_state_fit else "fail",
            "brief_landing": "conditional_pass",
            "imagegen_execution": "hold_for_primary_cta_color_decision",
        },
        "user_decision": "A196: mission and primary action bars use equal visible width, common center and double-edge alignment",
        "supersedes": {
            "contract_evidence": "docs/screenshots/2026-06-24-world-map-benchmark-landing/570-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-manifest.json",
            "brief_manifest": "docs/screenshots/2026-06-24-world-map-benchmark-landing/572-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-manifest.json",
            "reason": "A196 explicitly corrects the 276/284 width split and 160/158 center mismatch.",
        },
        "contracts": {
            "right_dossier_page": str(DOSSIER_PATH.relative_to(ROOT)).replace("\\", "/"),
            "right_mission_intel_button": str(MISSION_PATH.relative_to(ROOT)).replace("\\", "/"),
            "right_action_lane": str(PRIMARY_PATH.relative_to(ROOT)).replace("\\", "/"),
            "versions": checks["contract_versions"],
        },
        "authorized_contract_mutation": {
            "performed": True,
            "authorization": "User accepted the dual-agent recommendation; recorded as A196.",
            "changed_frozen_fields": {
                "right_dossier_page.frozen.slots.mission_intel_button": {"from": OLD_MISSION, "to": LOWER_SLOTS["mission_intel_button"]},
                "right_dossier_page.frozen.slots.primary_enter_cta": {"from": OLD_PRIMARY, "to": LOWER_SLOTS["primary_enter_cta"]},
                "right_mission_intel_button.frozen.export_size": {"from": [276, 44], "to": [284, 44]},
                "right_mission_intel_button.frozen.positions": {"from": [[954, 420]], "to": MISSION["frozen"]["positions"]},
                "right_mission_intel_button.frozen.hit_rect": {"from": [0, 0, 276, 44], "to": MISSION["frozen"]["hit_rect"]},
                "right_action_lane.frozen.positions": {"from": [[948, 474]], "to": PRIMARY["frozen"]["positions"]},
            },
            "upper_geometry_changed": False,
            "child_internal_slots_changed": False,
        },
        "outputs": {
            "alignment_board": str(OUT_ALIGNMENT.relative_to(ROOT)).replace("\\", "/"),
            "state_stress": str(OUT_STRESS.relative_to(ROOT)).replace("\\", "/"),
            "full_screen_reinsert": str(OUT_REINSERT.relative_to(ROOT)).replace("\\", "/"),
            "brief_board": str(OUT_BRIEF.relative_to(ROOT)).replace("\\", "/"),
            "manifest": str(OUT_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        },
        "contract_assertions": checks,
        "text_capacity": {
            "all_states_pass": all_state_fit,
            "bbox_gate": bbox_gate,
            "state_reports": {
                state: raster_helper.normalize_reports(reports, 1.5)
                for state, reports in stress_reports.items()
            },
        },
        "visual_alignment_gate": {
            "contract_slot_evidence": "pass",
            "visible_body_bbox_measurement": "required on first clean-sprite candidate",
            "shadow_bbox_measurement": "required separately on first clean-sprite candidate",
            "qa_rule_frozen": True,
        },
        "image_content_checks": {
            "alignment_board": raster_helper.image_metrics(OUT_ALIGNMENT),
            "state_stress": raster_helper.image_metrics(OUT_STRESS),
            "full_screen_reinsert": raster_helper.image_metrics(OUT_REINSERT),
            "brief_board": raster_helper.image_metrics(OUT_BRIEF),
        },
        "scope_guard": {
            "imagegen_called": False,
            "production_art_created": False,
            "atlas_created": False,
            "godot_runtime_capture_created": False,
            "other_classes_batch_produced": False,
        },
        "judgment": "A196 contract geometry, double-edge alignment and raster text capacity pass. Clean-sprite structure is updated, but production remains blocked on the primary CTA color decision.",
        "next_gate": "User selects olive, rust or mustard-gold primary CTA default color before imagegen.",
    }
    if not checks["pass"] or not all_state_fit or not bbox_gate["pass"]:
        raise AssertionError("v0.8.6 alignment or raster text gate failed")
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    checks = contract_assertions()
    alignment_reports = build_alignment_board(checks)
    stress_reports = build_stress_board()
    reinsert_reports = build_reinsert()
    build_brief_board()
    write_manifest(checks, alignment_reports, stress_reports, reinsert_reports)
    for path in (OUT_ALIGNMENT, OUT_STRESS, OUT_REINSERT, OUT_BRIEF, OUT_MANIFEST):
        print(path)


if __name__ == "__main__":
    main()
