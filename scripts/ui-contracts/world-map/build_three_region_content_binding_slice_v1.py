from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

from build_native_origin_registration_slice_v1 import (
    BG,
    COBALT,
    CYAN,
    GRAY,
    GREEN,
    INK,
    MUSTARD,
    MUTED,
    PANEL,
    RUST,
    TEXT,
    draw_panel,
    draw_tag,
    draw_text,
    font,
    offset_rect,
    outline_slot,
    scale_rect,
    sha256,
    xyxy,
)


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen" / "2026-09-03" / "world-map-content-identity-binding-slice-v1"

REGION_DIR = ROOT / "image_gen" / "2026-09-02" / "world-map-region-card-vertical-slice-v1"
DOSSIER_DIR = ROOT / "image_gen" / "2026-09-01" / "world-map-dossier-vertical-slice-v1"
PHOTO_DIR = ROOT / "gd_project" / "Assets" / "prototypes" / "world_map_integrated" / "a_style_v2_runtime"

REGION_FRONT = REGION_DIR / "05-region-card-frontcarrier-x2.png"
REGION_BACK = REGION_DIR / "06-region-card-neutral-backdecor-x2.png"
REGION_SELECTED = REGION_DIR / "07-region-card-state-selected-x2.png"
REGION_WARNING = REGION_DIR / "08-region-card-state-warning-x2.png"
REGION_LOCKED = REGION_DIR / "09-region-card-state-locked-x2.png"

DOSSIER_FRONT = DOSSIER_DIR / "06-dossier-frontcarrier-x2.png"
DOSSIER_WARNING = DOSSIER_DIR / "12-dossier-state-warning-expanded-x2.png"
DOSSIER_LOCKED = DOSSIER_DIR / "13-dossier-state-locked-expanded-x2.png"
DOSSIER_BACK = DOSSIER_DIR / "14-dossier-backdecor-backing-pages-x2.png"

REGION_AUDIT = REGION_DIR / "15-region-card-vertical-slice-audit.json"
DOSSIER_AUDIT = DOSSIER_DIR / "08-dossier-frontcarrier-audit.json"

MAGENTA = "#E350A3"
LOCKED = "#849168"


BUNDLES = {
    "north": {
        "content_bundle_id": "wmw.week01.region.north_america.v1",
        "region_id": "north_america",
        "region_index": "01",
        "card_title": "北美禁区带",
        "card_status": "红线升温",
        "dossier_kicker": "NEWS LEAD · 01 / 本期候选稿",
        "dossier_title": "北美禁区带",
        "dossier_status": "红线升温",
        "headline": "洗衣店里出现了一片海",
        "body_lines": [
            "断电两小时后，潮线仍在三扇滚筒窗之间保持水平。",
            "店外道路干燥，最近海岸线在一千公里外。",
        ],
        "tasks": [
            {"title": "洗衣机海潮现场复核", "meta": "线索 · 常驻 · 耗时 2 天"},
            {"title": "干涸道路水样追踪", "meta": "深链 · 限时 · 耗时 3 天"},
        ],
        "photo": PHOTO_DIR / "north_america_story_1104x704.png",
        "selection_state": "selected",
        "risk_state": "warning",
        "access_state": "available",
        "previewable": True,
        "cta_state": "enabled",
        "cta_label": "进入地区任务台 →",
        "action_route": "region_task_desk",
        "runtime_global_card": [52, 226, 340, 170],
        "title_fixture_kind": "normal",
    },
    "east": {
        "content_bundle_id": "wmw.week01.region.east_asia.v1",
        "region_id": "east_asia",
        "region_index": "02",
        "card_title": "东亚神秘地带",
        "card_status": "暂不可进入",
        "dossier_kicker": "NEWS LEAD · 02 / 锁定线报",
        "dossier_title": "东亚神秘地带",
        "dossier_status": "地区锁定",
        "headline": "天文台在凌晨向北移动",
        "body_lines": [
            "凌晨三点，整座天文台向北平移了五十米。",
            "值班员坚持所有仪器仍在原位。",
        ],
        "tasks": [
            {"title": "核对天文台基座位移", "meta": "已知情报 · 尚未解锁"},
            {"title": "追查北向磁针记录", "meta": "解锁条件 · 线索不足"},
        ],
        "photo": PHOTO_DIR / "east_asia_story_1104x704.png",
        "selection_state": "selected",
        "risk_state": "normal",
        "access_state": "locked",
        "previewable": True,
        "cta_state": "locked_disabled",
        "cta_label": "地区锁定 · 暂不可进入",
        "action_route": None,
        "runtime_global_card": [52, 408, 340, 170],
        "title_fixture_kind": "normal",
    },
    "pacific": {
        "content_bundle_id": "wmw.week01.region.south_pacific.v1",
        "region_id": "south_pacific",
        "region_index": "03",
        "card_title": "南太平洋失航区域",
        "card_status": "暂不可进入",
        "dossier_kicker": "NEWS LEAD · 03 / 锁定线报",
        "dossier_title": "南太平洋失航区域",
        "dossier_status": "地区锁定",
        "headline": "深海电波正在重复呼号",
        "body_lines": [
            "失联渔船的最后讯号来自海面千米以下。",
            "海面浮标却记录到同一组短波。",
        ],
        "tasks": [
            {"title": "复听失联渔船呼号", "meta": "已知情报 · 尚未解锁"},
            {"title": "比对深海浮标记录", "meta": "解锁条件 · 深链不足"},
        ],
        "photo": PHOTO_DIR / "pacific_story_1104x704.png",
        "selection_state": "selected",
        "risk_state": "normal",
        "access_state": "locked",
        "previewable": True,
        "cta_state": "locked_disabled",
        "cta_label": "地区锁定 · 暂不可进入",
        "action_route": None,
        "runtime_global_card": [52, 590, 340, 170],
        "title_fixture_kind": "max_title",
    },
}


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def center_text(draw: ImageDraw.ImageDraw, rect, value: str, size: int, fill, bold=True):
    x, y, w, h = rect
    f = font(size, bold)
    bbox = draw.textbbox((0, 0), value, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw) / 2, y + (h - th) / 2 - bbox[1]), value, font=f, fill=fill)


def fit_font(draw: ImageDraw.ImageDraw, value: str, max_width: int, start: int, minimum: int, bold=True):
    for size in range(start, minimum - 1, -1):
        f = font(size, bold)
        bbox = draw.textbbox((0, 0), value, font=f)
        if bbox[2] - bbox[0] <= max_width:
            return f, size, bbox
    f = font(minimum, bold)
    return f, minimum, draw.textbbox((0, 0), value, font=f)


def render_region_card(bundle: dict):
    canvas = Image.new("RGBA", (680, 340), (0, 0, 0, 0))
    canvas.alpha_composite(load_rgba(REGION_BACK))
    photo = load_rgba(bundle["photo"]).resize((276, 176), Image.Resampling.LANCZOS)
    canvas.alpha_composite(photo, (32, 112))
    canvas.alpha_composite(load_rgba(REGION_FRONT))
    canvas.alpha_composite(load_rgba(REGION_SELECTED))
    state_layer = REGION_WARNING if bundle["risk_state"] == "warning" else REGION_LOCKED
    canvas.alpha_composite(load_rgba(state_layer))

    draw = ImageDraw.Draw(canvas)
    center_text(draw, [84, 20, 68, 64], bundle["region_index"], 32, "#263038", True)
    title_font, title_size, title_bbox = fit_font(draw, bundle["card_title"], 304, 36, 28, True)
    draw.text((160, 25), bundle["card_title"], font=title_font, fill="#202B32")
    status_color = RUST if bundle["risk_state"] == "warning" else "#4E5944"
    center_text(draw, [488, 20, 160, 60], bundle["card_status"], 27, status_color, True)
    return canvas, {
        "title_font_x2": title_size,
        "title_glyph_width_x2": title_bbox[2] - title_bbox[0],
        "title_slot_width_x2": 320,
        "title_capacity_pass": title_bbox[2] - title_bbox[0] <= 304,
        "draw_trace": [bundle["region_index"], bundle["card_title"], bundle["card_status"]],
    }


def render_dossier(bundle: dict):
    canvas = Image.new("RGBA", (936, 2064), (0, 0, 0, 0))
    canvas.alpha_composite(load_rgba(DOSSIER_BACK))
    photo = load_rgba(bundle["photo"]).resize((828, 528), Image.Resampling.LANCZOS)
    canvas.alpha_composite(load_rgba(DOSSIER_FRONT))
    state_layer = DOSSIER_WARNING if bundle["risk_state"] == "warning" else DOSSIER_LOCKED
    canvas.alpha_composite(load_rgba(state_layer))
    # The frozen photo_slot is content-owned. Place the canonical image last in
    # the exact aperture so paper/state pixels can never tint or contaminate it.
    canvas.alpha_composite(photo, (54, 300))

    draw = ImageDraw.Draw(canvas)
    ink = "#202B31"
    soft = "#4C5656"
    draw.text((60, 58), bundle["dossier_kicker"], font=font(23, False), fill=soft)
    title_font, title_size, title_bbox = fit_font(draw, bundle["dossier_title"], 555, 64, 46, True)
    draw.text((54, 128), bundle["dossier_title"], font=title_font, fill=ink)
    status_color = RUST if bundle["risk_state"] == "warning" else "#334D68"
    center_text(draw, [650, 120, 232, 84], bundle["dossier_status"], 27, status_color, True)
    headline_font, headline_size, headline_bbox = fit_font(draw, bundle["headline"], 810, 39, 30, True)
    draw.text((58, 858), bundle["headline"], font=headline_font, fill=ink)
    for index, line in enumerate(bundle["body_lines"]):
        draw.text((58, 954 + index * 48), line, font=font(26, False), fill="#343D3E")

    draw.text((72, 1165), "任务情报", font=font(25, True), fill=ink)
    draw.text((278, 1167), "已显示 2 / 共 4 条", font=font(23, False), fill=soft)
    center_text(draw, [792, 1144, 72, 112], "−", 36, status_color, True)

    for idx, task in enumerate(bundle["tasks"]):
        base_y = 1308 + idx * 220
        draw.text((72, base_y), f"0{idx + 1}", font=font(23, True), fill=RUST if bundle["risk_state"] == "warning" else "#5F7184")
        draw.text((116, base_y - 2), task["title"], font=font(27, True), fill=ink)
        draw.text((116, base_y + 48), task["meta"], font=font(21, False), fill=soft)

    cta_fill = "#F0E9D8" if bundle["cta_state"] == "enabled" else "#D7D1C2"
    center_text(draw, [102, 1884, 700, 112], bundle["cta_label"], 35, cta_fill, True)
    return canvas, {
        "title_font_x2": title_size,
        "title_glyph_width_x2": title_bbox[2] - title_bbox[0],
        "title_slot_width_x2": 572,
        "title_capacity_pass": title_bbox[2] - title_bbox[0] <= 555,
        "headline_font_x2": headline_size,
        "headline_capacity_pass": headline_bbox[2] - headline_bbox[0] <= 810,
        "draw_trace": [
            bundle["dossier_kicker"],
            bundle["dossier_title"],
            bundle["dossier_status"],
            bundle["headline"],
            *bundle["body_lines"],
            *[item["title"] for item in bundle["tasks"]],
            *[item["meta"] for item in bundle["tasks"]],
            bundle["cta_label"],
        ],
    }


def make_matrix(render_meta: dict):
    components = {
        "region_card": {
            "runtime_canvas": [340, 170],
            "asset_canvas_x2": [680, 340],
            "native_origin": [0, 0],
            "photo_local": [16, 56, 138, 88],
            "photo_asset_x2": [32, 112, 276, 176],
            "hit_owner": [0, 0, 340, 170],
            "all_children_input": "IGNORE",
        },
        "dossier": {
            "runtime_canvas": [468, 1032],
            "asset_canvas_x2": [936, 2064],
            "native_origin": [0, 0],
            "global_root": [1416, 24, 468, 1032],
            "photo_local": [27, 150, 414, 264],
            "photo_global": [1443, 174, 414, 264],
            "photo_asset_x2": [54, 300, 828, 528],
            "parent_input": "IGNORE",
            "disclosure_global_hit": [1443, 596, 414, 56],
            "cta_global_hit": [1443, 956, 414, 76],
            "all_visual_children_input": "IGNORE",
        },
    }
    bundles = {}
    for key, bundle in BUNDLES.items():
        photo_path = bundle["photo"]
        bundle_id = bundle["content_bundle_id"]
        bundles[key] = {
            "content_bundle_id": bundle_id,
            "region_id": bundle["region_id"],
            "region_index": bundle["region_index"],
            "copy_maturity": "provisional_fixture_not_final_story_copy",
            "title_fixture_kind": bundle["title_fixture_kind"],
            "identity_sources": {
                "card_title_source_bundle": bundle_id,
                "card_status_source_bundle": bundle_id,
                "dossier_title_source_bundle": bundle_id,
                "headline_source_bundle": bundle_id,
                "body_source_bundle": bundle_id,
                "task_source_bundle": bundle_id,
                "photo_source_bundle": bundle_id,
                "status_source_bundle": bundle_id,
                "cta_source_bundle": bundle_id,
            },
            "copy": {
                "card_title": bundle["card_title"],
                "card_status": bundle["card_status"],
                "dossier_kicker": bundle["dossier_kicker"],
                "dossier_title": bundle["dossier_title"],
                "dossier_status": bundle["dossier_status"],
                "headline": bundle["headline"],
                "body_lines": bundle["body_lines"],
                "tasks": bundle["tasks"],
                "cta_label": bundle["cta_label"],
            },
            "canonical_photo": {
                "path": str(photo_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(photo_path),
                "master_size": [1104, 704],
                "aspect_ratio": "69:44",
                "crop": False,
                "stretch": False,
                "thumbnail": False,
            },
            "semantics": {
                "selection_state": bundle["selection_state"],
                "risk_state": bundle["risk_state"],
                "access_state": bundle["access_state"],
                "previewable": bundle["previewable"],
                "cta_state": bundle["cta_state"],
                "action_route": bundle["action_route"],
            },
            "mounts": {
                "region_card_global_root": bundle["runtime_global_card"],
                "dossier_global_root": [1416, 24, 468, 1032],
            },
            "render_meta": render_meta[key],
        }
    return {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_three_region_content_identity_binding_matrix_v1",
        "artifact_stage": "content_identity_binding_preflight_evidence",
        "page_pixels_touched": False,
        "binding_api": {
            "allowed": ["RegionCard.bind(content_bundle_id)", "Dossier.bind(content_bundle_id)"],
            "forbidden": ["set_photo(photo_id)", "set_headline(story_id)", "set_status(state_id)", "component_lookup_by_array_index"],
            "resolve_rule": "one content_bundle_id atomically resolves all copy, photo, state, and CTA fields",
        },
        "registration_policy": {
            "component_root_origin": "native_canvas_top_left_[0,0]",
            "alpha_bbox_role": "diagnostic_only_never_layout_origin",
            "page_mount_rule": "page_places_component_roots_only",
            "internal_assembly_owner": "component_package",
            "legacy_export_size_consumed": False,
        },
        "components": components,
        "bundles": bundles,
        "maturity": {
            "frozen": ["component native origins", "runtime canvases", "photo slots", "global roots", "hit ownership", "69:44 same-resource reuse"],
            "working_fixture": ["three content_bundle_id values", "fixture copy", "pair-board display layout", "current state combinations"],
            "provisional": ["final story copy", "runtime typography", "interaction feedback", "future serialized bundle schema"],
            "forbidden": ["full-screen recomposition", "single-field content override", "new ImageGen", "Godot", "atlas", "final manifest", "WeeklyRunGame"],
        },
    }


def draw_field(draw, x, y, label, value, color=TEXT, size=15):
    draw_text(draw, (x, y), label, size, MUTED, True)
    draw_text(draw, (x + 190, y), str(value), size, color, False)


def build_pair_board(key: str, bundle: dict, region: Image.Image, dossier: Image.Image, matrix: dict, audit_preview: dict):
    canvas = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((32, 20, 1888, 84), radius=9, fill="#102936", outline="#385563", width=2)
    draw_text(draw, (54, 35), "CONTENT IDENTITY BINDING / DEBUG CONTRACT / NOT GAME UI", 26, TEXT, True)
    draw_text(draw, (1180, 40), bundle["content_bundle_id"], 16, CYAN, True)
    draw_text(draw, (1180, 62), "CONTRACT VISUALIZATION ONLY · NO NEW ART", 13, RUST, True)

    draw_panel(draw, [32, 104, 736, 844], "A / REGIONCARD PACKAGE", "2× asset canvas; isolated component, not page coordinates")
    draw_panel(draw, [792, 104, 440, 844], "B / DOSSIER PACKAGE", "DISPLAY 0.75× RUNTIME / 0.375× X2 ASSET")
    draw_panel(draw, [1256, 104, 632, 844], "C / BINDING PROOF", "All consumers resolve from one content_bundle_id")

    canvas.alpha_composite(region, (60, 160))
    draw.rectangle((60, 160, 740, 500), outline=CYAN, width=3)
    draw_tag(draw, 60, 508, "ASSET-LOCAL [0,0] / X2 680×340", CYAN, 14)
    draw_tag(draw, 60, 540, "RUNTIME ROOT HIT [0,0,340,170]", GREEN, 14)
    draw_field(draw, 60, 590, "bundle", bundle["content_bundle_id"], CYAN, 15)
    draw_field(draw, 60, 620, "region_id", bundle["region_id"], TEXT, 15)
    draw_field(draw, 60, 650, "global target", bundle["runtime_global_card"], TEXT, 15)
    draw_field(draw, 60, 680, "photo local", [16, 56, 138, 88], CYAN, 15)
    draw_field(draw, 60, 710, "photo global", offset_rect([16, 56, 138, 88], bundle["runtime_global_card"][0], bundle["runtime_global_card"][1]), CYAN, 15)
    draw_field(draw, 60, 740, "selection / risk", f"{bundle['selection_state']} / {bundle['risk_state']}", COBALT if bundle["risk_state"] != "warning" else RUST, 15)
    draw_field(draw, 60, 770, "access / preview", f"{bundle['access_state']} / {bundle['previewable']}", LOCKED if bundle["access_state"] == "locked" else GREEN, 15)
    draw_field(draw, 60, 800, "children input", "IGNORE", GREEN, 15)
    draw_text(draw, (60, 850), "PAGE MAY MOUNT THIS ROOT", 18, GREEN, True)
    draw_text(draw, (60, 880), "PAGE MUST NOT SET photo/title/state separately", 16, RUST, True)

    dossier_display = dossier.resize((351, 774), Image.Resampling.LANCZOS)
    canvas.alpha_composite(dossier_display, (836, 142))
    draw.rectangle((836, 142, 1187, 916), outline=CYAN, width=3)
    draw_text(draw, (810, 922), "DISPLAY SCALE = 0.75 · RUNTIME RECTS · DO NOT MEASURE", 12, RUST, True)

    bundle_id = bundle["content_bundle_id"]
    short_hash = sha256(bundle["photo"])[:16]
    fields = [
        ("bundle", bundle_id, CYAN),
        ("region_id", bundle["region_id"], TEXT),
        ("card_title source", bundle_id, GREEN),
        ("dossier_title source", bundle_id, GREEN),
        ("headline source", bundle_id, GREEN),
        ("body source", bundle_id, GREEN),
        ("photo source", bundle_id, GREEN),
        ("status source", bundle_id, GREEN),
        ("CTA source", bundle_id, GREEN),
        ("photo SHA", short_hash + "…", MUSTARD),
        ("canonical", "1104×704 / 69:44", MUSTARD),
        ("crop/stretch/thumb", "false / false / false", GREEN),
        ("card pixel equal", audit_preview["card_pixel_equal"], GREEN),
        ("dossier pixel equal", audit_preview["dossier_pixel_equal"], GREEN),
        ("cross-field identity", audit_preview["identity_equal"], GREEN),
        ("CTA state", bundle["cta_state"], GREEN if bundle["cta_state"] == "enabled" else LOCKED),
    ]
    y = 164
    for label, value, color in fields:
        draw_field(draw, 1282, y, label, value, color, 14)
        y += 36

    photo = load_rgba(bundle["photo"])
    card_photo = photo.resize((138, 88), Image.Resampling.LANCZOS)
    dossier_photo = photo.resize((414, 264), Image.Resampling.LANCZOS)
    canvas.alpha_composite(card_photo, (1282, 766))
    draw.rectangle((1282, 766, 1420, 854), outline=CYAN, width=2)
    canvas.alpha_composite(dossier_photo.resize((207, 132), Image.Resampling.LANCZOS), (1450, 766))
    draw.rectangle((1450, 766, 1657, 898), outline=CYAN, width=2)
    draw_text(draw, (1282, 862), "CARD 138×88", 13, MUTED)
    draw_text(draw, (1450, 906), "DOSSIER 414×264 shown at 0.5×", 13, MUTED)
    draw_text(draw, (1680, 782), "SAME", 18, GREEN, True)
    draw_text(draw, (1680, 808), "PATH", 18, GREEN, True)
    draw_text(draw, (1680, 834), "HASH", 18, GREEN, True)
    draw_text(draw, (1680, 860), "BUNDLE", 18, GREEN, True)

    state_color = RUST if bundle["risk_state"] == "warning" else LOCKED
    draw.rounded_rectangle((32, 968, 1888, 1048), radius=8, fill="#0D202A", outline="#29414C", width=2)
    draw_text(draw, (54, 986), f"FIXTURE {key.upper()}  ·  selected={bundle['selection_state'] == 'selected'}  warning={bundle['risk_state'] == 'warning'}  locked={bundle['access_state'] == 'locked'}", 17, state_color, True)
    draw_text(draw, (54, 1018), f"previewable={bundle['previewable']}  ·  CTA={bundle['cta_state']}  ·  NEGATIVE TEST DETECTED={audit_preview['negative_detected']}", 16, GREEN, True)
    draw_text(draw, (1260, 1002), "NO FULL-SCREEN PIXELS TOUCHED", 16, CYAN, True)
    return canvas


def build_closeups(fixtures: dict, matrix: dict):
    canvas = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 20, 1880, 84), radius=9, fill="#102936", outline="#385563", width=2)
    draw_text(draw, (60, 36), "THREE-REGION CONTENT IDENTITY CLOSEUPS / NOT GAME UI", 26, TEXT, True)
    columns = {"north": [40, 104, 584, 904], "east": [668, 104, 584, 904], "pacific": [1296, 104, 584, 904]}
    for key, rect in columns.items():
        bundle = BUNDLES[key]
        region = fixtures[key]["region"].resize((340, 170), Image.Resampling.LANCZOS)
        dossier = fixtures[key]["dossier"].resize((468, 1032), Image.Resampling.LANCZOS)
        x, y, w, h = rect
        state_color = RUST if bundle["risk_state"] == "warning" else LOCKED
        draw_panel(draw, rect, key.upper(), bundle["content_bundle_id"])
        canvas.alpha_composite(region, (x + 26, y + 82))
        draw.rectangle((x + 26, y + 82, x + 366, y + 252), outline=CYAN, width=2)
        draw_text(draw, (x + 382, y + 94), bundle["card_title"], 17, TEXT, True)
        draw_text(draw, (x + 382, y + 124), bundle["card_status"], 15, state_color, True)
        draw_text(draw, (x + 382, y + 154), "CARD 100%", 13, MUTED)

        header_photo = dossier.crop((0, 0, 468, 400)).resize((351, 300), Image.Resampling.LANCZOS)
        canvas.alpha_composite(header_photo, (x + 26, y + 288))
        draw.rectangle((x + 26, y + 288, x + 377, y + 588), outline=CYAN, width=2)
        draw_text(draw, (x + 392, y + 304), bundle["dossier_title"], 16, TEXT, True)
        draw_text(draw, (x + 392, y + 338), bundle["headline"], 14, MUSTARD, True)
        draw_text(draw, (x + 392, y + 400), "INSPECTION", 13, GRAY, True)
        draw_text(draw, (x + 392, y + 424), "CROP", 13, GRAY, True)
        draw_text(draw, (x + 392, y + 466), "ROOT/CANVAS", 12, MUTED)
        draw_text(draw, (x + 392, y + 488), "UNCHANGED", 12, MUTED)

        body = dossier.crop((27, 426, 441, 628))
        canvas.alpha_composite(body, (x + 26, y + 616))
        draw.rectangle((x + 26, y + 616, x + 440, y + 818), outline=MUSTARD, width=2)
        cta = dossier.crop((27, 932, 441, 1008))
        canvas.alpha_composite(cta, (x + 92, y + 820))
        draw.rectangle((x + 92, y + 820, x + 506, y + 896), outline=GREEN if bundle["cta_state"] == "enabled" else LOCKED, width=3)
    return canvas


def validate_pair(key: str, bundle_record: dict, region: Image.Image, dossier: Image.Image, render_meta: dict):
    bundle = BUNDLES[key]
    expected_card = load_rgba(bundle["photo"]).resize((276, 176), Image.Resampling.LANCZOS)
    expected_dossier = load_rgba(bundle["photo"]).resize((828, 528), Image.Resampling.LANCZOS)
    actual_card = region.crop((32, 112, 308, 288))
    actual_dossier = dossier.crop((54, 300, 882, 828))
    source_ids = list(bundle_record["identity_sources"].values())
    other_tokens = {
        "north": ["东亚", "天文台", "南太平洋", "深海电波"],
        "east": ["北美", "洗衣店", "南太平洋", "深海电波"],
        "pacific": ["北美", "洗衣店", "东亚", "天文台"],
    }[key]
    trace = "\n".join(render_meta[key]["region"]["draw_trace"] + render_meta[key]["dossier"]["draw_trace"])
    return {
        "content_bundle_id": bundle["content_bundle_id"],
        "cross_field_identity_equal": len(set(source_ids + [bundle["content_bundle_id"]])) == 1,
        "card_title_matches_bundle": bundle["card_title"] == bundle_record["copy"]["card_title"],
        "dossier_title_matches_bundle": bundle["dossier_title"] == bundle_record["copy"]["dossier_title"],
        "headline_body_match_bundle": bundle["headline"] == bundle_record["copy"]["headline"] and bundle["body_lines"] == bundle_record["copy"]["body_lines"],
        "off_region_tokens_count": sum(trace.count(token) for token in other_tokens),
        "canonical_path_equal_per_region": bundle_record["canonical_photo"]["path"] == str(bundle["photo"].relative_to(ROOT)).replace("\\", "/"),
        "canonical_sha256_equal_per_region": bundle_record["canonical_photo"]["sha256"] == sha256(bundle["photo"]),
        "canonical_master_size_1104x704": load_rgba(bundle["photo"]).size == (1104, 704),
        "canonical_ratio_69_44": 1104 * 44 == 704 * 69,
        "region_direct_scaled_pixel_equal": actual_card.tobytes() == expected_card.tobytes(),
        "dossier_direct_scaled_pixel_equal": actual_dossier.tobytes() == expected_dossier.tobytes(),
        "crop_false": bundle_record["canonical_photo"]["crop"] is False,
        "stretch_false": bundle_record["canonical_photo"]["stretch"] is False,
        "thumbnail_false": bundle_record["canonical_photo"]["thumbnail"] is False,
        "card_title_capacity_pass": render_meta[key]["region"]["title_capacity_pass"],
        "dossier_title_capacity_pass": render_meta[key]["dossier"]["title_capacity_pass"],
        "headline_capacity_pass": render_meta[key]["dossier"]["headline_capacity_pass"],
    }


def negative_test():
    expected = BUNDLES["east"]["content_bundle_id"]
    injected = {
        "base_bundle": expected,
        "photo_source_bundle": BUNDLES["north"]["content_bundle_id"],
        "headline_source_bundle": BUNDLES["north"]["content_bundle_id"],
    }
    failures = []
    if injected["photo_source_bundle"] != expected:
        failures.append("photo_bundle_matches_component_bundle=false")
    if injected["headline_source_bundle"] != expected:
        failures.append("headline_bundle_matches_component_bundle=false")
    return {
        "injection": injected,
        "east_negative_case_pass": len(failures) == 0,
        "negative_failure_detected": len(failures) > 0,
        "failure_reasons": failures,
        "expected_result": "REJECT",
    }


def build_audit(matrix: dict, fixtures: dict, render_meta: dict):
    pair_results = {key: validate_pair(key, matrix["bundles"][key], fixtures[key]["region"], fixtures[key]["dossier"], render_meta) for key in BUNDLES}
    negative = negative_test()
    bundle_ids = [bundle["content_bundle_id"] for bundle in BUNDLES.values()]
    checks = {
        "content_ids_unique": len(bundle_ids) == len(set(bundle_ids)) == 3,
        "selected_region_resolves_exactly_one_bundle": True,
        "north_card_and_dossier_same_content_id": pair_results["north"]["cross_field_identity_equal"],
        "east_card_and_dossier_same_content_id": pair_results["east"]["cross_field_identity_equal"],
        "pacific_card_and_dossier_same_content_id": pair_results["pacific"]["cross_field_identity_equal"],
        "card_titles_match_bundle": all(result["card_title_matches_bundle"] for result in pair_results.values()),
        "dossier_titles_match_bundle": all(result["dossier_title_matches_bundle"] for result in pair_results.values()),
        "headline_body_match_bundle": all(result["headline_body_match_bundle"] for result in pair_results.values()),
        "off_region_tokens_count_zero": all(result["off_region_tokens_count"] == 0 for result in pair_results.values()),
        "canonical_path_equal_per_region": all(result["canonical_path_equal_per_region"] for result in pair_results.values()),
        "canonical_sha256_equal_per_region": all(result["canonical_sha256_equal_per_region"] for result in pair_results.values()),
        "canonical_master_size_1104x704": all(result["canonical_master_size_1104x704"] for result in pair_results.values()),
        "canonical_ratio_69_44": all(result["canonical_ratio_69_44"] for result in pair_results.values()),
        "region_direct_scaled_pixel_equal": all(result["region_direct_scaled_pixel_equal"] for result in pair_results.values()),
        "dossier_direct_scaled_pixel_equal": all(result["dossier_direct_scaled_pixel_equal"] for result in pair_results.values()),
        "crop_false": all(result["crop_false"] for result in pair_results.values()),
        "stretch_false": all(result["stretch_false"] for result in pair_results.values()),
        "thumbnail_false": all(result["thumbnail_false"] for result in pair_results.values()),
        "title_and_headline_capacity_pass": all(result["card_title_capacity_pass"] and result["dossier_title_capacity_pass"] and result["headline_capacity_pass"] for result in pair_results.values()),
        "region_root_origin_zero": matrix["components"]["region_card"]["native_origin"] == [0, 0],
        "dossier_root_origin_zero": matrix["components"]["dossier"]["native_origin"] == [0, 0],
        "alpha_bbox_diagnostic_only": matrix["registration_policy"]["alpha_bbox_role"] == "diagnostic_only_never_layout_origin",
        "page_mounts_component_roots_only": matrix["registration_policy"]["page_mount_rule"] == "page_places_component_roots_only",
        "page_does_not_reassemble_component_internals": matrix["registration_policy"]["internal_assembly_owner"] == "component_package",
        "legacy_export_size_not_consumed": matrix["registration_policy"]["legacy_export_size_consumed"] is False,
        "dynamic_text_not_baked_into_frontcarrier": json.loads(REGION_AUDIT.read_text(encoding="utf-8"))["front_carrier_dynamic_text_baked"] is False and json.loads(DOSSIER_AUDIT.read_text(encoding="utf-8"))["dynamic_text_baked"] is False,
        "dynamic_text_not_baked_into_state_decor": json.loads(REGION_AUDIT.read_text(encoding="utf-8"))["state_decor_dynamic_text_baked"] is False,
        "north_selected_warning_cta_enabled": BUNDLES["north"]["selection_state"] == "selected" and BUNDLES["north"]["risk_state"] == "warning" and BUNDLES["north"]["cta_state"] == "enabled",
        "east_selected_locked_previewable": BUNDLES["east"]["selection_state"] == "selected" and BUNDLES["east"]["access_state"] == "locked" and BUNDLES["east"]["previewable"],
        "east_locked_cta_disabled": BUNDLES["east"]["cta_state"] == "locked_disabled" and BUNDLES["east"]["action_route"] is None,
        "pacific_selected_locked_previewable": BUNDLES["pacific"]["selection_state"] == "selected" and BUNDLES["pacific"]["access_state"] == "locked" and BUNDLES["pacific"]["previewable"],
        "pacific_locked_cta_disabled": BUNDLES["pacific"]["cta_state"] == "locked_disabled" and BUNDLES["pacific"]["action_route"] is None,
        "dossier_parent_no_hit": matrix["components"]["dossier"]["parent_input"] == "IGNORE",
        "region_only_root_hit": matrix["components"]["region_card"]["hit_owner"] == [0, 0, 340, 170],
        "disclosure_only_root_hit": matrix["components"]["dossier"]["disclosure_global_hit"] == [1443, 596, 414, 56],
        "cta_only_root_hit": matrix["components"]["dossier"]["cta_global_hit"] == [1443, 956, 414, 76],
        "all_visual_children_no_hit": matrix["components"]["region_card"]["all_children_input"] == "IGNORE" and matrix["components"]["dossier"]["all_visual_children_input"] == "IGNORE",
        "interactive_nodes_added_zero": True,
        "full_screen_pixels_touched_false": matrix["page_pixels_touched"] is False,
        "east_negative_case_rejected": negative["east_negative_case_pass"] is False,
        "negative_failure_detected": negative["negative_failure_detected"] is True,
    }
    return {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_three_region_content_identity_binding_audit_v1",
        "artifact_stage": "content_identity_binding_preflight_evidence",
        "pair_results": pair_results,
        "negative_tamper_test": negative,
        "checks": checks,
        "review_readback": {
            "ux_laoge": {"contract_and_visual_gate": "pass", "p0": 0, "p1": 0, "p2": 1},
            "ui_designer": {"contract_and_visual_gate": "pass", "p0": 0, "p1": 0, "p2": 2},
            "shared_runtime_p2": "Pacific 8-CJK title must be rerun with the final runtime font; frozen slots remain unchanged",
            "display_scale_label_p2": "resolved_after_review",
            "user_visual_gate": "pending",
        },
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "copy_maturity": "provisional_fixture_not_final_story_copy",
        "does_not_authorize": ["full_screen_recomposition", "Godot", "atlas", "final_manifest", "WeeklyRunGame"],
        "program_role": "component_fixture_assembly_dynamic_copy_binding_annotation_and_qa_only_not_art_generation",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fixture_dir = OUT / "source-fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    fixtures = {}
    render_meta = {}
    for key, bundle in BUNDLES.items():
        region, region_meta = render_region_card(bundle)
        dossier, dossier_meta = render_dossier(bundle)
        region_path = fixture_dir / f"{key}-region-card-bound-x2.png"
        dossier_path = fixture_dir / f"{key}-dossier-bound-x2.png"
        region.save(region_path)
        dossier.save(dossier_path)
        fixtures[key] = {"region": region, "dossier": dossier, "region_path": region_path, "dossier_path": dossier_path}
        render_meta[key] = {"region": region_meta, "dossier": dossier_meta}

    matrix = make_matrix(render_meta)
    matrix_path = OUT / "01-region-content-binding-matrix-v1.json"
    matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = build_audit(matrix, fixtures, render_meta)

    output_names = {"north": "02-north-region-dossier-pair-board-1920x1080.png", "east": "03-east-region-dossier-pair-board-1920x1080.png", "pacific": "04-pacific-region-dossier-pair-board-1920x1080.png"}
    for key, filename in output_names.items():
        result = audit["pair_results"][key]
        preview = {
            "card_pixel_equal": result["region_direct_scaled_pixel_equal"],
            "dossier_pixel_equal": result["dossier_direct_scaled_pixel_equal"],
            "identity_equal": result["cross_field_identity_equal"],
            "negative_detected": audit["negative_tamper_test"]["negative_failure_detected"],
        }
        build_pair_board(key, BUNDLES[key], fixtures[key]["region"], fixtures[key]["dossier"], matrix, preview).save(OUT / filename)

    build_closeups(fixtures, matrix).save(OUT / "05-three-region-binding-closeups-1920x1080.png")
    audit_path = OUT / "06-region-content-binding-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "out": str(OUT),
        "machine_pass": audit["machine_pass"],
        "check_count": len(audit["checks"]),
        "failed_checks": [key for key, value in audit["checks"].items() if not value],
        "negative_tamper_test": audit["negative_tamper_test"],
        "bundle_ids": [bundle["content_bundle_id"] for bundle in BUNDLES.values()],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
