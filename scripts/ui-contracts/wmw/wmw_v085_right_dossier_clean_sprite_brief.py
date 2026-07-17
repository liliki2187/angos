from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "docs" / "screenshots" / "2026-06-24-world-map-benchmark-landing"
CONTRACT_DIR = ROOT / "design" / "ui-contracts" / "world-map"
OUT_BOARD = BASE / "571-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-board.png"
OUT_MANIFEST = BASE / "572-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-manifest.json"

FONT_BOLD_PATHS = [
    Path(r"C:\Windows\Fonts\msyhbd.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
]
FONT_REGULAR_PATHS = [
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\arial.ttf"),
]

BG = (7, 19, 21)
PANEL = (13, 37, 38)
PANEL_EDGE = (55, 104, 102)
PAPER = (183, 164, 136)
PAPER_LIGHT = (194, 185, 179)
PAPER_DARK = (104, 101, 84)
INK = (25, 30, 30)
CREAM = (235, 227, 201)
MUTED = (182, 201, 191)
CYAN = (70, 171, 180)
TEAL = (56, 73, 70)
OLIVE = (78, 98, 61)
RUST = (122, 73, 47)
GOLD = (154, 119, 42)
LOCKED = (84, 87, 81)
GREEN = (103, 229, 148)
HOLD = (237, 191, 93)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


DOSSIER = load_json(CONTRACT_DIR / "right_dossier_page.json")
MISSION = load_json(CONTRACT_DIR / "right_mission_intel_button.json")
PRIMARY = load_json(CONTRACT_DIR / "right_action_lane.json")


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    paths = FONT_BOLD_PATHS if bold else FONT_REGULAR_PATHS
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and text_width(draw, candidate, font) > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int = 5,
) -> int:
    x, y = xy
    bbox = draw.textbbox((0, 0), "国Ag", font=font)
    line_height = bbox[3] - bbox[1]
    for line in wrap_text(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height + line_gap
    return y


def draw_panel(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], title: str) -> None:
    draw.rectangle(rect, fill=PANEL, outline=PANEL_EDGE, width=2)
    draw.text((rect[0] + 24, rect[1] + 18), title, font=load_font(25, True), fill=CREAM)


def scaled_rect(rect: list[int], origin: tuple[int, int], scale: float) -> tuple[int, int, int, int]:
    x, y, width, height = rect
    ox, oy = origin
    return (
        round(ox + x * scale),
        round(oy + y * scale),
        round(ox + (x + width) * scale),
        round(oy + (y + height) * scale),
    )


def draw_checker(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], cell: int = 14) -> None:
    for y in range(rect[1], rect[3], cell):
        for x in range(rect[0], rect[2], cell):
            even = ((x - rect[0]) // cell + (y - rect[1]) // cell) % 2 == 0
            color = (33, 57, 60) if even else (47, 78, 81)
            draw.rectangle((x, y, min(x + cell, rect[2]), min(y + cell, rect[3])), fill=color)


def draw_button(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    label: str,
    strong: bool,
) -> None:
    shadow = 6 if strong else 3
    draw.rectangle((rect[0] + shadow, rect[1] + shadow, rect[2] + shadow, rect[3] + shadow), fill=(4, 13, 14))
    draw.rectangle(rect, fill=fill, outline=CREAM, width=3 if strong else 2)
    icon_size = min(rect[3] - rect[1] - 12, 42)
    icon_rect = (rect[0] + 10, rect[1] + 6, rect[0] + 10 + icon_size, rect[1] + 6 + icon_size)
    draw.rectangle(icon_rect, outline=CREAM, width=2)
    badge_rect = (rect[2] - icon_size - 10, rect[1] + 6, rect[2] - 10, rect[1] + 6 + icon_size)
    draw.rectangle(badge_rect, outline=CREAM, width=2)
    plate = (icon_rect[2] + 12, rect[1] + 8, badge_rect[0] - 12, rect[3] - 8)
    draw.rectangle(plate, fill=PAPER_LIGHT, outline=(214, 205, 184), width=2)
    font = load_font(14, True)
    bbox = draw.textbbox((0, 0), label, font=font)
    tx = plate[0] + ((plate[2] - plate[0]) - (bbox[2] - bbox[0])) // 2
    ty = plate[1] + ((plate[3] - plate[1]) - (bbox[3] - bbox[1])) // 2 - bbox[1]
    draw.text((tx, ty), label, font=font, fill=INK)


def draw_assembly(draw: ImageDraw.ImageDraw) -> None:
    origin = (82, 178)
    scale = 1.34
    export = DOSSIER["frozen"]["export_size"]
    page = (origin[0], origin[1], origin[0] + round(export[0] * scale), origin[1] + round(export[1] * scale))
    draw.rectangle((page[0] - 14, page[1] + 12, page[2] + 15, page[3] + 15), fill=(52, 66, 48))
    draw.rectangle((page[0] - 6, page[1] + 5, page[2] + 7, page[3] + 8), fill=(143, 126, 103))
    draw.rectangle(page, fill=PAPER, outline=PAPER_LIGHT, width=3)

    slots = DOSSIER["frozen"]["slots"]
    title = scaled_rect(slots["title_slot"], origin, scale)
    stamp = scaled_rect(slots["status_stamp"], origin, scale)
    icon = scaled_rect(slots["header_icon"], origin, scale)
    photo = scaled_rect(slots["photo_slot"], origin, scale)
    body = scaled_rect(slots["region_body"], origin, scale)
    facts = scaled_rect(slots["decision_facts"], origin, scale)
    mission = scaled_rect(slots["mission_intel_button"], origin, scale)
    primary = scaled_rect(slots["primary_enter_cta"], origin, scale)

    draw.rectangle(title, fill=(169, 153, 126), outline=PAPER_LIGHT, width=2)
    draw.rectangle(stamp, fill=(137, 119, 97), outline=RUST, width=2)
    draw.ellipse(icon, outline=CREAM, width=3)
    draw_checker(draw, photo)
    draw.rectangle(photo, outline=PAPER_LIGHT, width=4)
    draw.text((photo[0] + 14, photo[1] + 12), "PHOTO CONTENT LAYER", font=load_font(17, True), fill=MUTED)
    draw.text((photo[0] + 14, photo[1] + 38), "ordinary rectangle / shell owns edges", font=load_font(13), fill=MUTED)

    draw.rectangle(body, fill=(181, 163, 135))
    draw.line((body[0], body[1] + 4, body[0], body[3] - 4), fill=TEAL, width=4)
    draw.text((body[0] + 12, body[1] + 9), "region_body · READ ONLY", font=load_font(15, True), fill=INK)
    draw.text((body[0] + 12, body[1] + 35), "open carrier / no closed frame", font=load_font(12), fill=(54, 58, 52))

    draw.rectangle(facts, fill=(157, 149, 119))
    draw.line((facts[0], facts[1], facts[2], facts[1]), fill=PAPER_LIGHT, width=2)
    draw.line((facts[0], facts[3], facts[2], facts[3]), fill=PAPER_LIGHT, width=2)
    draw.text((facts[0] + 12, facts[1] + 10), "decision_facts · READ ONLY", font=load_font(13, True), fill=INK)

    draw_button(draw, mission, TEAL, "SECONDARY CHILD", strong=False)
    draw_button(draw, primary, LOCKED, "PRIMARY COLOR HOLD", strong=True)

    draw.text((title[0] + 8, title[1] + 7), "TITLE CARRIER", font=load_font(12, True), fill=INK)
    draw.text((stamp[0] + 7, stamp[1] + 8), "STATUS", font=load_font(11, True), fill=CREAM)
    draw.text((stamp[0] + 7, stamp[1] + 28), "BASE", font=load_font(11, True), fill=CREAM)
    draw.text((page[0], page[3] + 20), "ASSEMBLY PREVIEW · annotations only · not production art", font=load_font(15, True), fill=GREEN)


def draw_ownership(draw: ImageDraw.ImageDraw) -> None:
    x = 590
    y = 160
    rows = [
        ("z60", "runtime feedback", GREEN, "focus / hover / pressed; hit rect does not move"),
        ("z50", "runtime content", CYAN, "all text, numbers, header/status/button icons"),
        ("z40", "two child sprites", TEAL, "each owns one frame, plate, badge base and shadow"),
        ("z30", "parent hollow shell", PAPER, "paper, photo bezel, title/body/facts carriers"),
        ("z20", "photo content", (47, 78, 81), "ordinary rectangle; never cropped to window shape"),
        ("z10", "back sheets / shadow", PAPER_DARK, "light paper depth; no slot intrusion"),
    ]
    for z_label, title, color, detail in rows:
        draw.rectangle((x, y, x + 76, y + 54), fill=color, outline=CREAM, width=2)
        draw.text((x + 17, y + 13), z_label, font=load_font(16, True), fill=INK if color in (PAPER, PAPER_DARK) else CREAM)
        draw.text((x + 96, y + 2), title, font=load_font(19, True), fill=CREAM)
        draw_wrapped(draw, (x + 96, y + 29), detail, load_font(13), MUTED, 430, 3)
        y += 84

    rule_y = 694
    draw.rectangle((580, rule_y, 1138, 955), fill=(9, 27, 29), outline=HOLD, width=2)
    draw.text((606, rule_y + 18), "PARENT / CHILD HARD RULE", font=load_font(22, True), fill=HOLD)
    rules = [
        "Parent child rect 下只有连续、无描边的底纸。",
        "Child 独占完整外框、内板、label、badge base 与局部阴影。",
        "合成后每个按钮只能出现一套边框和一套阴影。",
        "region_body / decision_facts 无 hit rect、无 hover、无按钮语法。",
    ]
    ry = rule_y + 62
    for index, rule in enumerate(rules, 1):
        draw.text((610, ry), f"{index}.", font=load_font(16, True), fill=GREEN)
        ry = draw_wrapped(draw, (640, ry), rule, load_font(15), CREAM, 465, 3) + 8


def draw_states_and_hold(draw: ImageDraw.ImageDraw) -> None:
    x = 1202
    draw.text((x, 156), "STATE DERIVATION", font=load_font(22, True), fill=CREAM)
    states = [
        ("DEFAULT", OLIVE, "paper readable · mission enabled · CTA enabled"),
        ("WARNING", RUST, "rust only on stamp / narrow tab · buttons stay enabled"),
        ("LOCKED", LOCKED, "mission locked_context_enabled · CTA locked_disabled"),
    ]
    y = 199
    for label, color, detail in states:
        draw.rectangle((x, y, x + 112, y + 56), fill=color, outline=CREAM, width=2)
        draw.text((x + 12, y + 14), label, font=load_font(15, True), fill=CREAM)
        draw_wrapped(draw, (x + 132, y + 2), detail, load_font(14), MUTED, 455, 3)
        y += 82

    draw.rectangle((1182, 452, 1858, 716), fill=(10, 29, 31), outline=HOLD, width=3)
    draw.text((1210, 472), "IMAGEGEN HOLD · PRIMARY CTA COLOR", font=load_font(22, True), fill=HOLD)
    candidates = [("OLIVE · recommended", OLIVE), ("RUST · v0.4", RUST), ("GOLD · 569 mock", GOLD)]
    cy = 525
    for label, color in candidates:
        draw.rectangle((1210, cy, 1310, cy + 38), fill=color, outline=CREAM, width=2)
        draw.text((1330, cy + 7), label, font=load_font(16, True), fill=CREAM)
        cy += 49
    hold_note_font = load_font(14)
    draw.text(
        (1210, 671),
        "Structure can land now. Do not start imagegen or state atlas",
        font=hold_note_font,
        fill=MUTED,
    )
    draw.text(
        (1210, 692),
        "until the user selects one stable semantic color family.",
        font=hold_note_font,
        fill=MUTED,
    )

    draw.text((1202, 754), "REQUIRED GATES", font=load_font(22, True), fill=CREAM)
    gates = [
        "single-master geometry identity",
        "parent button decoration absence",
        "photo window alpha clear",
        "readonly carrier affordance",
        "no baked text / digits / state glyphs",
        "composite cleanliness + 200% seams",
        "Godot raster glyph bbox + two hit rects",
    ]
    gy = 795
    for gate in gates:
        draw.rectangle((1206, gy + 6, 1218, gy + 18), fill=GREEN)
        draw.text((1232, gy), gate, font=load_font(15), fill=CREAM)
        gy += 31


def contract_assertions() -> dict[str, Any]:
    slots = DOSSIER["frozen"]["slots"]
    width, height = DOSSIER["frozen"]["export_size"]
    slot_inside = {}
    for name, rect in slots.items():
        x, y, rect_width, rect_height = rect
        slot_inside[name] = x >= 0 and y >= 0 and x + rect_width <= width and y + rect_height <= height

    parent_origin = DOSSIER["frozen"]["positions"][0]
    mission_local = slots["mission_intel_button"]
    primary_local = slots["primary_enter_cta"]
    mission_expected = [parent_origin[0] + mission_local[0], parent_origin[1] + mission_local[1]]
    primary_expected = [parent_origin[0] + primary_local[0], parent_origin[1] + primary_local[1]]
    checks = {
        "versions": {
            "right_dossier_page": DOSSIER["contract_version"],
            "right_mission_intel_button": MISSION["contract_version"],
            "right_action_lane": PRIMARY["contract_version"],
        },
        "export_scale_all_2x": all(contract["export_scale"] == 2 for contract in (DOSSIER, MISSION, PRIMARY)),
        "all_parent_slots_inside_export": slot_inside,
        "mission_child_absolute_position": {
            "expected": mission_expected,
            "actual": MISSION["frozen"]["positions"][0],
            "pass": mission_expected == MISSION["frozen"]["positions"][0],
        },
        "primary_child_absolute_position": {
            "expected": primary_expected,
            "actual": PRIMARY["frozen"]["positions"][0],
            "pass": primary_expected == PRIMARY["frozen"]["positions"][0],
        },
        "frozen_fields_modified": False,
    }
    checks["pass"] = (
        all(slot_inside.values())
        and checks["export_scale_all_2x"]
        and checks["mission_child_absolute_position"]["pass"]
        and checks["primary_child_absolute_position"]["pass"]
    )
    if not checks["pass"]:
        raise AssertionError(json.dumps(checks, ensure_ascii=False, indent=2))
    return checks


def image_metrics(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    colors = image.getcolors(maxcolors=image.width * image.height)
    non_black = sum(1 for pixel in image.get_flattened_data() if max(pixel) > 8)
    return {
        "size": [image.width, image.height],
        "unique_colors": len(colors) if colors is not None else "more_than_pixel_limit",
        "non_black_pixels": non_black,
    }


def create_board() -> None:
    image = Image.new("RGB", (1920, 1080), BG)
    draw = ImageDraw.Draw(image)
    draw.text((42, 30), "WMW 右侧 dossier v0.8.5 · 无字 clean-sprite 结构 brief", font=load_font(38, True), fill=CREAM)
    draw.text((44, 81), "571 · 三母版 / 父子像素所有权 / 状态派生 / CTA 色族阻断", font=load_font(19), fill=MUTED)
    draw.rectangle((1561, 27, 1878, 88), fill=(40, 33, 20), outline=HOLD, width=2)
    draw.text((1583, 39), "STRUCTURE ONLY", font=load_font(21, True), fill=HOLD)
    draw.text((1583, 67), "非生产美术 · 零 imagegen", font=load_font(13), fill=CREAM)

    draw_panel(draw, (38, 122, 548, 1012), "1 · CONTRACT ASSEMBLY")
    draw_panel(draw, (562, 122, 1160, 1012), "2 · PIXEL OWNERSHIP / Z ORDER")
    draw_panel(draw, (1174, 122, 1882, 1012), "3 · STATE + HOLD + GATES")
    draw_assembly(draw)
    draw_ownership(draw)
    draw_states_and_hold(draw)
    draw.text((42, 1032), "status: structure_gate PASS · brief conditional PASS · imagegen HOLD for primary CTA color decision", font=load_font(17, True), fill=GREEN)
    image.save(OUT_BOARD)


def create_manifest(assertions: dict[str, Any]) -> None:
    manifest = {
        "artifact": "WMW right dossier v0.8.5 clean-sprite structure brief",
        "date": "2026-07-14",
        "artifact_type": "production brief / structure board / not production art / not atlas / not Godot runtime",
        "status": {
            "structure_gate": "pass",
            "brief_landing": "conditional_pass",
            "imagegen_execution": "hold_for_primary_cta_color_decision",
        },
        "contracts": {
            "right_dossier_page": "design/ui-contracts/world-map/right_dossier_page.json",
            "right_mission_intel_button": "design/ui-contracts/world-map/right_mission_intel_button.json",
            "right_action_lane": "design/ui-contracts/world-map/right_action_lane.json",
        },
        "contract_assertions": assertions,
        "outputs": {
            "brief": "docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-clean-sprite-brief-v0-8-5.md",
            "board": "docs/screenshots/2026-06-24-world-map-benchmark-landing/571-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-board.png",
            "manifest": "docs/screenshots/2026-06-24-world-map-benchmark-landing/572-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-manifest.json",
        },
        "scope_guard": {
            "classes": ["right_dossier_page", "right_mission_intel_button", "right_action_lane"],
            "imagegen_called": False,
            "production_assets_created": False,
            "other_classes_started": False,
            "contract_frozen_fields_changed": False,
        },
        "master_strategy": {
            "master_count": 3,
            "masters": ["right_dossier_page_master", "right_mission_intel_button_master", "right_action_lane_master"],
            "independent_imagegen_per_state_forbidden": True,
            "same_class_alpha_silhouette_diff_required": 0,
            "same_class_slot_geometry_diff_required": 0,
        },
        "pixel_ownership": {
            "parent": ["paper shell", "photo window edge", "title/status/body/facts carriers", "continuous unframed paper below child rects"],
            "photo": ["ordinary rectangular region content"],
            "child_buttons": ["complete frame", "inner plate", "neutral icon/badge bases", "local shadow", "interaction skin"],
            "runtime": ["all text", "all digits", "all state semantic icons", "focus/hover/pressed feedback"],
            "duplicate_frame_or_shadow_allowed": False,
        },
        "baked_content_policy": {
            "text": False,
            "digits": False,
            "fake_text": False,
            "state_semantic_icons": False,
            "arrows": False,
        },
        "reviews": {
            "ui_designer": "PASS: use one parent hollow-shell master plus two independent child button masters; do not generate a complete page with baked buttons.",
            "ux_laoge": {
                "p0": 0,
                "p1": ["primary CTA color family unresolved", "two no-text buttons need stronger primary/secondary weight distance", "locked mission must be named locked_context_enabled"],
                "p2": ["parent-child seam gate", "hover/pressed runtime timing", "use unequal count fixtures"],
                "structure_gate": "conditional_pass",
            },
        },
        "open_decisions": {
            "blocking_before_imagegen": {
                "primary_cta_default_color": {
                    "options": ["olive_green", "warning_rust", "mustard_gold"],
                    "recommendation": "olive_green",
                    "reason": "Keep primary, secondary, warning and disabled semantic colors exclusive.",
                }
            },
            "non_blocking_for_structure": ["locked secondary action wording/callback", "warning enter confirmation", "entry cost terminology"],
        },
        "required_gates": [
            "parent_child_absolute_position_match",
            "parent_button_decoration_absence",
            "readonly_carrier_no_hit_rect",
            "single_master_geometry_identity",
            "alpha_silhouette_identity",
            "photo_window_alpha_clear",
            "no_baked_text_digits_or_state_glyphs",
            "paper_token_match",
            "composite_cleanliness",
            "card_body_opacity_probe",
            "runtime_glyph_bbox_inside_inner",
            "manual_200_percent_seam_review",
            "godot_windowed_capture",
        ],
        "image_content_checks": {"brief_board": image_metrics(OUT_BOARD)},
        "judgment": "Structure is ready to record. Asset generation remains blocked until the user chooses the primary CTA default color family.",
        "next_gate": "user_primary_cta_color_decision",
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    current_versions = {
        DOSSIER["contract_version"],
        MISSION["contract_version"],
        PRIMARY["contract_version"],
    }
    if current_versions != {"0.8.5"}:
        raise RuntimeError(
            "Historical v0.8.5 brief is version-locked. "
            "Use wmw_v086_right_dossier_alignment.py for the current contracts."
        )
    assertions = contract_assertions()
    create_board()
    create_manifest(assertions)
    print(OUT_BOARD)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
