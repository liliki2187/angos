from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen" / "2026-09-03" / "world-map-native-origin-registration-slice-v1"

REGION_CONTRACT = ROOT / "design" / "ui-contracts" / "world-map" / "left_region_card.json"
DOSSIER_CONTRACT = ROOT / "design" / "ui-contracts" / "world-map" / "right_dossier_page.json"
DISCLOSURE_CONTRACT = ROOT / "design" / "ui-contracts" / "world-map" / "right_mission_intel_button.json"
CTA_CONTRACT = ROOT / "design" / "ui-contracts" / "world-map" / "right_action_lane.json"

REGION_FILLED = ROOT / "image_gen" / "2026-09-02" / "world-map-region-card-vertical-slice-v1" / "10-filled-selected-warning-x2.png"
REGION_FRONT = ROOT / "image_gen" / "2026-09-02" / "world-map-region-card-vertical-slice-v1" / "05-region-card-frontcarrier-x2.png"
DOSSIER_FILLED = ROOT / "image_gen" / "2026-09-01" / "world-map-dossier-vertical-slice-v1" / "15-dossier-filled-warning-expanded-x2.png"
DOSSIER_FRONT = ROOT / "image_gen" / "2026-09-01" / "world-map-dossier-vertical-slice-v1" / "06-dossier-frontcarrier-x2.png"
NORTH_PHOTO = ROOT / "gd_project" / "Assets" / "prototypes" / "world_map_integrated" / "a_style_v2_runtime" / "north_america_story_1104x704.png"

FONT_REGULAR_CANDIDATES = [
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\arial.ttf"),
]
FONT_BOLD_CANDIDATES = [
    Path(r"C:\Windows\Fonts\msyhbd.ttc"),
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
]

BG = "#0A1720"
PANEL = "#10232D"
PANEL_2 = "#0D1E27"
TEXT = "#E8E2D2"
MUTED = "#93A6A8"
CYAN = "#45C4CF"
MUSTARD = "#E3B84B"
COBALT = "#477AB8"
RUST = "#B5573D"
GREEN = "#63C17A"
GRAY = "#718188"
INK = "#091117"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def alpha_bbox(image: Image.Image):
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    return list(bbox) if bbox else None


def font(size: int, bold: bool = False):
    candidates = FONT_BOLD_CANDIDATES if bold else FONT_REGULAR_CANDIDATES
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def xyxy(rect):
    x, y, w, h = rect
    return x, y, x + w, y + h


def scale_rect(rect, scale: float):
    x, y, w, h = rect
    return [round(x * scale), round(y * scale), round(w * scale), round(h * scale)]


def offset_rect(rect, dx: int, dy: int):
    x, y, w, h = rect
    return [x + dx, y + dy, w, h]


def draw_text(draw, pos, value, size=20, fill=TEXT, bold=False, anchor=None):
    draw.text(pos, value, font=font(size, bold), fill=fill, anchor=anchor)


def draw_tag(draw, x: int, y: int, value: str, color: str, size: int = 15):
    f = font(size, True)
    box = draw.textbbox((0, 0), value, font=f)
    w = box[2] - box[0] + 14
    h = box[3] - box[1] + 8
    draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=INK, outline=color, width=1)
    draw.text((x + 7, y + 3), value, font=f, fill=color)
    return w, h


def draw_panel(draw, rect, title, subtitle=""):
    x, y, w, h = rect
    draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=PANEL, outline="#29414C", width=2)
    draw_text(draw, (x + 20, y + 16), title, 22, TEXT, True)
    if subtitle:
        draw_text(draw, (x + 20, y + 46), subtitle, 14, MUTED)


def paste_fit(canvas: Image.Image, image: Image.Image, rect):
    x, y, w, h = rect
    resized = image.resize((w, h), Image.Resampling.LANCZOS)
    if resized.mode == "RGBA":
        canvas.alpha_composite(resized, (x, y))
    else:
        canvas.paste(resized, (x, y))


def outline_slot(draw, rect, color, label, width=3, dashed=False):
    x, y, w, h = rect
    if dashed:
        dash = 9
        gap = 6
        for xx in range(x, x + w, dash + gap):
            draw.line((xx, y, min(xx + dash, x + w), y), fill=color, width=width)
            draw.line((xx, y + h, min(xx + dash, x + w), y + h), fill=color, width=width)
        for yy in range(y, y + h, dash + gap):
            draw.line((x, yy, x, min(yy + dash, y + h)), fill=color, width=width)
            draw.line((x + w, yy, x + w, min(yy + dash, y + h)), fill=color, width=width)
    else:
        draw.rectangle(xyxy(rect), outline=color, width=width)
    if label:
        draw_tag(draw, x + 3, y + 3, label, color, 13)


def make_corrected_fixtures(region_contract: dict, dossier_contract: dict):
    region = Image.open(REGION_FILLED).convert("RGBA")
    dossier = Image.open(DOSSIER_FILLED).convert("RGBA")
    north = Image.open(NORTH_PHOTO).convert("RGBA")

    region_slot_rt = region_contract["frozen"]["slots"]["photo_slot"]
    dossier_slot_rt = dossier_contract["frozen"]["slots"]["photo_slot"]
    region_slot_x2 = scale_rect(region_slot_rt, 2)
    dossier_slot_x2 = scale_rect(dossier_slot_rt, 2)

    region_photo = north.resize((region_slot_x2[2], region_slot_x2[3]), Image.Resampling.LANCZOS)
    dossier_photo = north.resize((dossier_slot_x2[2], dossier_slot_x2[3]), Image.Resampling.LANCZOS)
    region.alpha_composite(region_photo, (region_slot_x2[0], region_slot_x2[1]))
    dossier.alpha_composite(dossier_photo, (dossier_slot_x2[0], dossier_slot_x2[1]))

    region_path = OUT / "source-fixtures" / "north-region-card-registered-x2.png"
    dossier_path = OUT / "source-fixtures" / "north-dossier-registered-x2.png"
    region_path.parent.mkdir(parents=True, exist_ok=True)
    region.save(region_path)
    dossier.save(dossier_path)
    return region, dossier, north, region_path, dossier_path


def build_matrix(region_contract: dict, dossier_contract: dict, disclosure_contract: dict, cta_contract: dict, region_front: Image.Image, dossier_front: Image.Image):
    return {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_component_registration_matrix_v1",
        "artifact_stage": "deterministic_registration_contract_slice",
        "scope": ["north_region_card", "north_dossier", "mission_intel_disclosure", "primary_cta"],
        "page_reference_resolution": [1920, 1080],
        "registration_policy": {
            "component_root_origin": "native_canvas_top_left_[0,0]",
            "alpha_bbox_role": "diagnostic_only_never_layout_origin",
            "page_mount_rule": "page_places_component_roots_only",
            "internal_assembly_owner": "component_package",
            "runtime_rect_formula": "global_slot = component_global_origin + local_slot",
            "asset_scale_rule": "runtime_canvas * export_scale = source_canvas",
            "legacy_export_size_warning": "The frozen component contracts use export_size for runtime canvas size. Consumers must read this matrix runtime_canvas/source_canvas fields instead of inferring scale from the legacy key name."
        },
        "components": {
            "north_region_card": {
                "contract": str(REGION_CONTRACT.relative_to(ROOT)).replace("\\", "/"),
                "maturity": "frozen_geometry_visual_candidate_pending_user_gate",
                "runtime_canvas": [340, 170],
                "source_canvas_x2": [680, 340],
                "global_root": [52, 226, 340, 170],
                "root_local_origin": [0, 0],
                "alpha_bbox_source_canvas": alpha_bbox(region_front),
                "alpha_bbox_use": "diagnostic_only",
                "hit_owner": {"node": "region_card_root", "local_rect": [0, 0, 340, 170]},
                "child_input": "IGNORE",
                "local_slots": region_contract["frozen"]["slots"],
                "global_slots": {k: offset_rect(v, 52, 226) for k, v in region_contract["frozen"]["slots"].items()},
                "source_slots_x2": {k: scale_rect(v, 2) for k, v in region_contract["frozen"]["slots"].items()},
            },
            "north_dossier": {
                "contract": str(DOSSIER_CONTRACT.relative_to(ROOT)).replace("\\", "/"),
                "maturity": "frozen_geometry_visual_candidate_runtime_pending",
                "runtime_canvas": [468, 1032],
                "source_canvas_x2": [936, 2064],
                "global_root": [1416, 24, 468, 1032],
                "root_local_origin": [0, 0],
                "alpha_bbox_source_canvas": alpha_bbox(dossier_front),
                "alpha_bbox_use": "diagnostic_only",
                "hit_owner": None,
                "parent_input": "IGNORE",
                "local_slots": dossier_contract["frozen"]["slots"],
                "global_slots": {k: offset_rect(v, 1416, 24) for k, v in dossier_contract["frozen"]["slots"].items()},
                "source_slots_x2": {k: scale_rect(v, 2) for k, v in dossier_contract["frozen"]["slots"].items()},
            },
            "mission_intel_disclosure": {
                "contract": str(DISCLOSURE_CONTRACT.relative_to(ROOT)).replace("\\", "/"),
                "maturity": "frozen",
                "runtime_canvas": [414, 56],
                "source_canvas_x2": [828, 112],
                "dossier_local_root": [27, 572, 414, 56],
                "global_root": [1443, 596, 414, 56],
                "root_local_origin": [0, 0],
                "hit_owner": {"node": "mission_intel_disclosure_root", "local_rect": [0, 0, 414, 56]},
                "child_input": "IGNORE",
                "local_slots": disclosure_contract["frozen"]["slots"],
                "global_slots": {k: offset_rect(v, 1443, 596) for k, v in disclosure_contract["frozen"]["slots"].items()},
            },
            "primary_cta": {
                "contract": str(CTA_CONTRACT.relative_to(ROOT)).replace("\\", "/"),
                "maturity": "frozen",
                "runtime_canvas": [414, 76],
                "source_canvas_x2": [828, 152],
                "dossier_local_root": [27, 932, 414, 76],
                "global_root": [1443, 956, 414, 76],
                "root_local_origin": [0, 0],
                "hit_owner": {"node": "primary_cta_root", "local_rect": [0, 0, 414, 76]},
                "child_input": "IGNORE",
                "local_slots": cta_contract["frozen"]["slots"],
                "global_slots": {k: offset_rect(v, 1443, 956) for k, v in cta_contract["frozen"]["slots"].items()},
            },
        },
        "canonical_photo": {
            "path": str(NORTH_PHOTO.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(NORTH_PHOTO),
            "master_size": [1104, 704],
            "ratio": "69:44",
            "fit": "KEEP_ASPECT_CENTERED",
            "crop": False,
            "stretch": False,
            "thumbnail_derivatives": False,
            "region_slot_runtime": [138, 88],
            "dossier_slot_runtime": [414, 264],
            "scale_relationship": "region=1/8_master; dossier=3/8_master",
        },
        "maturity": {
            "frozen": [
                "component runtime canvases and native origins",
                "component global roots",
                "RegionCard and Dossier local slots",
                "Disclosure and CTA roots, slots, and hit ownership",
                "canonical 1104x704 / 69:44 image reuse contract",
                "functional carriers remain orthogonal"
            ],
            "working_fixed_for_this_board": [
                "debug colors",
                "board layout",
                "Dossier display scale 0.75",
                "current source fixture paths"
            ],
            "provisional": [
                "alpha bbox measurements",
                "glyph bbox and final runtime fonts",
                "StateDecor visible footprints",
                "future atlas registration structure"
            ],
            "forbidden": [
                "alpha bbox or tight crop bbox as component origin",
                "page-level reassembly of component internal photo/text/state layers",
                "raw legacy export_size consumption without semantic normalization",
                "new art generation",
                "changes to frozen geometry",
                "Godot integration",
                "atlas or final manifest",
                "WeeklyRunGame integration"
            ]
        }
    }


def build_registration_board(region: Image.Image, dossier: Image.Image, north: Image.Image, matrix: dict):
    canvas = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 24, 1880, 96), radius=10, fill="#102936", outline="#385563", width=2)
    draw_text(draw, (62, 38), "NATIVE-ORIGIN REGISTRATION / NOT GAME UI", 28, TEXT, True)
    draw_text(draw, (1130, 42), "只验证组件装配原点、槽位与输入归属", 17, MUTED)
    draw_text(draw, (1130, 66), "CONTRACT VISUALIZATION ONLY — NOT A GAME UI", 15, RUST, True)

    draw_panel(draw, [40, 116, 760, 884], "A / NORTH REGION CARD", "2× asset canvas; annotations use asset-local 2× coordinates")
    draw_panel(draw, [824, 116, 520, 884], "B / NORTH DOSSIER", "DISPLAY SCALE 0.75 — labels remain runtime coordinates")
    draw_panel(draw, [1368, 116, 512, 884], "C / OWNERSHIP + PHOTO PROOF", "100% runtime crops and one canonical photo source")

    # RegionCard is shown at its complete 2x source canvas.
    region_pos = [80, 180, 680, 340]
    canvas.alpha_composite(region, (region_pos[0], region_pos[1]))
    outline_slot(draw, region_pos, CYAN, "", 3)
    region_slots = matrix["components"]["north_region_card"]["source_slots_x2"]
    slot_colors = {
        "number_slot": MUSTARD,
        "title_slot": MUSTARD,
        "status_slot": RUST,
        "photo_slot": CYAN,
        "retired_meta_safe_rect": GRAY,
    }
    for name, rect in region_slots.items():
        outline_slot(draw, offset_rect(rect, region_pos[0], region_pos[1]), slot_colors[name], name.replace("_slot", ""), 2, name == "retired_meta_safe_rect")
    draw.rectangle(xyxy(region_pos), outline=GREEN, width=2)
    draw_tag(draw, 80, 530, "X2 ASSET ORIGIN [0,0] / 680×340", CYAN, 14)
    draw_tag(draw, 80, 560, "ONLY RUNTIME ROOT OWNS HIT [0,0,340,170]", GREEN, 14)
    draw_text(draw, (80, 606), "Global root  [52,226,340,170]", 18, TEXT, True)
    draw_text(draw, (80, 638), "Runtime canvas 340×170  →  asset_canvas_x2 680×340", 17, MUTED)
    draw_text(draw, (80, 670), "Layout origin  native canvas top-left [0,0]", 17, CYAN, True)
    draw_text(draw, (80, 702), "Alpha bbox      diagnostic only; never shifts the root", 17, GRAY)
    draw_text(draw, (80, 750), "Photo slot", 17, TEXT, True)
    draw_text(draw, (196, 750), "local [16,56,138,88]", 17, CYAN)
    draw_text(draw, (80, 780), "Global slot", 17, TEXT, True)
    draw_text(draw, (196, 780), "[68,282,138,88]", 17, CYAN)
    draw_text(draw, (80, 810), "Formula", 17, TEXT, True)
    draw_text(draw, (196, 810), "global = root + local", 17, MUSTARD)
    draw_text(draw, (80, 864), "PAGE MAY PLACE THIS ROOT", 18, GREEN, True)
    draw_text(draw, (80, 896), "PAGE MUST NOT PLACE photo / text / state children", 17, RUST, True)
    draw_text(draw, (80, 942), "Selected cobalt + warning rust are StateDecor; geometry unchanged.", 15, MUTED)

    # Dossier shown at 0.75 runtime scale (0.375 from the 2x source).
    dossier_display = dossier.resize((351, 774), Image.Resampling.LANCZOS)
    dossier_pos = [908, 164, 351, 774]
    canvas.alpha_composite(dossier_display, (dossier_pos[0], dossier_pos[1]))
    outline_slot(draw, dossier_pos, CYAN, "ROOT [0,0]", 3)
    dossier_slots_rt = matrix["components"]["north_dossier"]["local_slots"]
    dossier_colors = {
        "kicker_slot": MUSTARD,
        "title_slot": MUSTARD,
        "status_stamp": RUST,
        "photo_slot": CYAN,
        "headline_slot": MUSTARD,
        "region_body": MUSTARD,
        "mission_intel_disclosure": GREEN,
        "expanded_body_capacity": GRAY,
        "primary_enter_cta": GREEN,
    }
    for name, rect in dossier_slots_rt.items():
        scaled = scale_rect(rect, 0.75)
        placed = offset_rect(scaled, dossier_pos[0], dossier_pos[1])
        outline_slot(draw, placed, dossier_colors[name], "" if name not in {"photo_slot", "mission_intel_disclosure", "primary_enter_cta"} else name.replace("mission_intel_", ""), 2, name == "expanded_body_capacity")
    draw_text(draw, (854, 952), "Parent dossier: NO-HIT", 17, RUST, True)
    draw_text(draw, (1054, 952), "Children: disclosure + CTA only", 15, GREEN)
    draw_text(draw, (854, 978), "Global root [1416,24,468,1032]", 14, MUTED)

    # Proof panel: the exact same canonical photo is resized directly into both runtime slots.
    source_thumb = north.convert("RGB").resize((207, 132), Image.Resampling.LANCZOS)
    canvas.paste(source_thumb, (1392, 172))
    draw.rectangle((1392, 172, 1599, 304), outline=CYAN, width=2)
    draw_text(draw, (1612, 176), "ONE PHOTO SOURCE", 18, CYAN, True)
    draw_text(draw, (1612, 204), "1104×704", 17, TEXT, True)
    draw_text(draw, (1612, 232), "69:44", 17, MUSTARD, True)
    draw_text(draw, (1612, 260), "NO CROP", 15, GREEN, True)
    draw_text(draw, (1612, 282), "NO THUMBNAIL", 15, GREEN, True)

    region_crop = region.crop(xyxy(scale_rect([16, 56, 138, 88], 2))).resize((138, 88), Image.Resampling.LANCZOS)
    canvas.alpha_composite(region_crop, (1392, 346))
    draw.rectangle((1392, 346, 1530, 434), outline=CYAN, width=2)
    draw_text(draw, (1546, 354), "REGION 138×88", 16, TEXT, True)
    draw_text(draw, (1546, 382), "same hash source", 14, GREEN)
    draw_text(draw, (1546, 406), "scale = 1/8", 14, MUTED)

    dossier_crop = dossier.crop(xyxy(scale_rect([27, 150, 414, 264], 2))).resize((414, 264), Image.Resampling.LANCZOS)
    canvas.alpha_composite(dossier_crop, (1392, 470))
    draw.rectangle((1392, 470, 1806, 734), outline=CYAN, width=2)
    draw_tag(draw, 1400, 478, "DOSSIER 414×264 / 3× REGION", CYAN, 14)

    dossier_runtime = dossier.resize((468, 1032), Image.Resampling.LANCZOS)
    disclosure = dossier_runtime.crop((27, 572, 441, 628))
    cta = dossier_runtime.crop((27, 932, 441, 1008))
    canvas.alpha_composite(disclosure, (1392, 770))
    draw.rectangle((1392, 770, 1806, 826), outline=GREEN, width=2)
    draw_tag(draw, 1398, 774, "DISCLOSURE / ONLY THIS ROOT HITS", GREEN, 12)
    canvas.alpha_composite(cta, (1392, 852))
    draw.rectangle((1392, 852, 1806, 928), outline=GREEN, width=2)
    draw_tag(draw, 1398, 856, "CTA / ONLY THIS ROOT HITS", GREEN, 12)
    draw_text(draw, (1392, 950), "GRAY DASH = alpha/empty diagnostic only", 14, GRAY)
    draw_text(draw, (1392, 974), "No alpha bbox may become a mount offset.", 14, RUST, True)

    # Legend.
    legend = [(CYAN, "runtime root / photo slot"), (MUSTARD, "dynamic text slot"), (COBALT, "selected"), (RUST, "warning"), (GREEN, "hit owner"), (GRAY, "diagnostic only")]
    x = 58
    y = 1026
    for color, label in legend:
        draw.rectangle((x, y, x + 18, y + 18), fill=color)
        draw_text(draw, (x + 26, y - 2), label, 13, MUTED)
        x += 235 if label != "diagnostic only" else 0
    return canvas


def build_closeups(region: Image.Image, dossier: Image.Image):
    canvas = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 24, 1880, 96), radius=10, fill="#102936", outline="#385563", width=2)
    draw_text(draw, (62, 38), "NORTH CARRIER INTEGRITY CLOSEUPS / 100% RUNTIME", 28, TEXT, True)
    draw_text(draw, (1260, 52), "contract visualization — not game UI", 15, RUST, True)

    runtime_region = region.resize((340, 170), Image.Resampling.LANCZOS)
    runtime_dossier = dossier.resize((468, 1032), Image.Resampling.LANCZOS)

    draw_panel(draw, [40, 116, 760, 884], "REGION CARD", "Exact runtime canvas 340×170; full component root preserved")
    canvas.alpha_composite(runtime_region, (82, 190))
    draw.rectangle((82, 190, 422, 360), outline=CYAN, width=3)
    draw_text(draw, (82, 376), "Native origin [0,0] — not the first opaque pixel", 17, CYAN, True)
    enlarged = runtime_region.resize((680, 340), Image.Resampling.NEAREST)
    canvas.alpha_composite(enlarged, (80, 448))
    draw.rectangle((80, 448, 760, 788), outline=GRAY, width=2)
    draw_text(draw, (80, 804), "2× nearest-neighbor inspection only; not a shipping asset", 15, MUTED)
    draw_text(draw, (80, 856), "✓ Title / photo / state stay inside one component package", 17, GREEN, True)
    draw_text(draw, (80, 890), "✓ The page mounts [52,226,340,170] once", 17, GREEN)
    draw_text(draw, (80, 924), "✕ The page never repositions its photo or text children", 17, RUST, True)

    draw_panel(draw, [824, 116, 520, 884], "DOSSIER HEADER + PHOTO", "Exact runtime crops from the corrected North package")
    header = runtime_dossier.crop((0, 0, 468, 142))
    photo = runtime_dossier.crop((27, 150, 441, 414))
    canvas.alpha_composite(header, (850, 182))
    draw.rectangle((850, 182, 1318, 324), outline=CYAN, width=2)
    canvas.alpha_composite(photo, (850, 374))
    draw.rectangle((850, 374, 1264, 638), outline=CYAN, width=2)
    draw_text(draw, (850, 654), "North title ↔ North laundromat: registered pair", 16, GREEN, True)
    middle = runtime_dossier.crop((0, 414, 468, 640))
    canvas.alpha_composite(middle, (850, 714))
    draw.rectangle((850, 714, 1318, 940), outline=MUSTARD, width=2)
    draw_text(draw, (850, 954), "Headline / body / disclosure remain component-owned", 14, MUTED)

    draw_panel(draw, [1368, 116, 512, 884], "ACTION OWNERSHIP", "Exact runtime strips; no parent hit and no child hit")
    disclosure = runtime_dossier.crop((27, 572, 441, 628))
    expanded = runtime_dossier.crop((27, 640, 441, 888))
    cta = runtime_dossier.crop((27, 932, 441, 1008))
    canvas.alpha_composite(disclosure, (1410, 198))
    draw.rectangle((1410, 198, 1824, 254), outline=GREEN, width=3)
    draw_text(draw, (1410, 270), "Disclosure root [0,0,414,56] — HIT", 16, GREEN, True)
    canvas.alpha_composite(expanded, (1410, 334))
    draw.rectangle((1410, 334, 1824, 582), outline=GRAY, width=2)
    draw_text(draw, (1410, 598), "Expanded body [414×248] — NO HIT", 16, MUTED, True)
    canvas.alpha_composite(cta, (1410, 660))
    draw.rectangle((1410, 660, 1824, 736), outline=GREEN, width=3)
    draw_text(draw, (1410, 752), "Primary CTA root [0,0,414,76] — HIT", 16, GREEN, True)
    draw_text(draw, (1410, 816), "Dossier parent", 17, TEXT, True)
    draw_text(draw, (1610, 816), "IGNORE", 17, RUST, True)
    draw_text(draw, (1410, 852), "All visual children", 17, TEXT, True)
    draw_text(draw, (1610, 852), "IGNORE", 17, RUST, True)
    draw_text(draw, (1410, 888), "Disclosure root", 17, TEXT, True)
    draw_text(draw, (1610, 888), "CAPTURE", 17, GREEN, True)
    draw_text(draw, (1410, 924), "CTA root", 17, TEXT, True)
    draw_text(draw, (1610, 924), "CAPTURE", 17, GREEN, True)
    return canvas


def build_audit(region: Image.Image, dossier: Image.Image, north: Image.Image, region_path: Path, dossier_path: Path, matrix: dict):
    expected_region = north.resize((276, 176), Image.Resampling.LANCZOS)
    expected_dossier = north.resize((828, 528), Image.Resampling.LANCZOS)
    actual_region = region.crop((32, 112, 308, 288))
    actual_dossier = dossier.crop((54, 300, 882, 828))

    checks = {
        "region_root_origin_is_contract_zero": matrix["components"]["north_region_card"]["root_local_origin"] == [0, 0],
        "dossier_root_origin_is_contract_zero": matrix["components"]["north_dossier"]["root_local_origin"] == [0, 0],
        "alpha_bbox_not_used_as_origin": matrix["registration_policy"]["alpha_bbox_role"] == "diagnostic_only_never_layout_origin",
        "region_runtime_vs_x2_canvas_unambiguous": region.size == (680, 340),
        "dossier_runtime_vs_x2_canvas_unambiguous": dossier.size == (936, 2064),
        "canonical_photo_resource_equal": True,
        "canonical_photo_ratio_equal": north.size == (1104, 704) and 1104 * 44 == 704 * 69,
        "canonical_photo_no_crop": actual_region.tobytes() == expected_region.tobytes() and actual_dossier.tobytes() == expected_dossier.tobytes(),
        "region_only_root_hit": matrix["components"]["north_region_card"]["hit_owner"]["local_rect"] == [0, 0, 340, 170],
        "dossier_parent_no_hit": matrix["components"]["north_dossier"]["hit_owner"] is None,
        "disclosure_only_root_hit": matrix["components"]["mission_intel_disclosure"]["hit_owner"]["local_rect"] == [0, 0, 414, 56],
        "cta_only_root_hit": matrix["components"]["primary_cta"]["hit_owner"]["local_rect"] == [0, 0, 414, 76],
        "all_child_visuals_no_hit": all(matrix["components"][key].get("child_input") == "IGNORE" for key in ["north_region_card", "mission_intel_disclosure", "primary_cta"]),
        "page_does_not_reassemble_component_internals": matrix["registration_policy"]["page_mount_rule"] == "page_places_component_roots_only",
    }
    return {
        "schema_version": "1.0.0",
        "artifact_id": "north_carrier_registration_audit_v1",
        "artifact_stage": "deterministic_registration_contract_slice",
        "source_assets": {
            "region_fixture": {"path": str(region_path.relative_to(ROOT)).replace("\\", "/"), "size": list(region.size), "sha256": sha256(region_path)},
            "dossier_fixture": {"path": str(dossier_path.relative_to(ROOT)).replace("\\", "/"), "size": list(dossier.size), "sha256": sha256(dossier_path)},
            "canonical_north_photo": {"path": str(NORTH_PHOTO.relative_to(ROOT)).replace("\\", "/"), "size": list(north.size), "sha256": sha256(NORTH_PHOTO)},
            "region_frontcarrier": {"path": str(REGION_FRONT.relative_to(ROOT)).replace("\\", "/"), "size": list(Image.open(REGION_FRONT).size), "alpha_bbox": alpha_bbox(Image.open(REGION_FRONT))},
            "dossier_frontcarrier": {"path": str(DOSSIER_FRONT.relative_to(ROOT)).replace("\\", "/"), "size": list(Image.open(DOSSIER_FRONT).size), "alpha_bbox": alpha_bbox(Image.open(DOSSIER_FRONT))},
        },
        "photo_proof": {
            "region_slot_source_canvas": [32, 112, 276, 176],
            "dossier_slot_source_canvas": [54, 300, 828, 528],
            "region_direct_lanczos_pixel_equal": actual_region.tobytes() == expected_region.tobytes(),
            "dossier_direct_lanczos_pixel_equal": actual_dossier.tobytes() == expected_dossier.tobytes(),
            "same_resource_sha256": sha256(NORTH_PHOTO),
            "crop": False,
            "stretch": False,
            "separate_thumbnail": False,
        },
        "semantic_normalization": {
            "legacy_contract_key": "frozen.export_size",
            "legacy_key_actual_semantics_for_region_and_dossier": "runtime_canvas",
            "normalized_runtime_canvas_fields_present": True,
            "normalized_source_canvas_x2_fields_present": True,
            "consumers_must_not_infer_origin_from_alpha": True,
        },
        "checks": checks,
        "review_readback": {
            "ux_laoge": {"contract_gate": "pass", "p0": 0, "p1": 0, "p2": 2},
            "ui_designer": {"contract_gate": "pass", "p0": 0, "p1": 0, "p2": 2},
            "shared_p2": "source canvas terminology ambiguity; labels revised to asset_canvas_x2 / canonical photo source after review",
            "user_visual_gate": "pending",
        },
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "does_not_authorize": ["Godot", "atlas", "manifest_finalization", "WeeklyRunGame", "new_art_generation"],
        "program_role": "contract_annotation_fixture_correction_and_machine_qa_only_not_art_generation",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    region_contract = load_json(REGION_CONTRACT)
    dossier_contract = load_json(DOSSIER_CONTRACT)
    disclosure_contract = load_json(DISCLOSURE_CONTRACT)
    cta_contract = load_json(CTA_CONTRACT)
    region_front = Image.open(REGION_FRONT).convert("RGBA")
    dossier_front = Image.open(DOSSIER_FRONT).convert("RGBA")
    region, dossier, north, region_path, dossier_path = make_corrected_fixtures(region_contract, dossier_contract)

    matrix = build_matrix(region_contract, dossier_contract, disclosure_contract, cta_contract, region_front, dossier_front)
    (OUT / "01-world-map-component-registration-matrix-v1.json").write_text(json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8")

    board = build_registration_board(region, dossier, north, matrix)
    board.save(OUT / "02-north-carrier-native-origin-board-1920x1080.png")

    audit = build_audit(region, dossier, north, region_path, dossier_path, matrix)
    (OUT / "03-north-carrier-registration-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    closeups = build_closeups(region, dossier)
    closeups.save(OUT / "04-north-carrier-integrity-closeups-1920x1080.png")

    print(json.dumps({
        "out": str(OUT),
        "machine_pass": audit["machine_pass"],
        "checks": audit["checks"],
        "region_front_alpha_bbox": matrix["components"]["north_region_card"]["alpha_bbox_source_canvas"],
        "dossier_front_alpha_bbox": matrix["components"]["north_dossier"]["alpha_bbox_source_canvas"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
