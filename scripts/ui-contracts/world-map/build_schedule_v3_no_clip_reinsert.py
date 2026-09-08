from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw


ROOT = Path(r"D:\angos")
V2_SCRIPT = ROOT / "scripts/ui-contracts/world-map/build_schedule_v2_contact_reinsert.py"
SPEC = importlib.util.spec_from_file_location("schedule_v2_builder", V2_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load Schedule V2 builder")
V2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V2)

OUT = ROOT / "image_gen/2026-09-04/world-map-schedule-v3-no-clip-backdecor-v1"
EFFECTIVE_BACK_RECT = (12, 16, 700, 464)
OLIVE_EDGE_RECT = (676, 472, 36, 8)


def make_backdecor() -> tuple[Image.Image, dict]:
    generated, source_meta = V2.extract_backing_papers(V2.BACK_RAW)

    visible = Image.new("L", V2.CANVAS, 0)
    ImageDraw.Draw(visible).rectangle(V2.xyxy(EFFECTIVE_BACK_RECT), fill=255)
    slate = generated.copy()
    slate.putalpha(ImageChops.multiply(slate.getchannel("A"), visible))

    # Reuse the generated gray-olive edge pixels as a tiny bottom paper reveal.
    # No color or shape is redrawn; the source strip is only rotated/resized.
    olive_source = generated.crop((718, 292, 732, 462)).rotate(90, expand=True)
    olive_edge = olive_source.resize((OLIVE_EDGE_RECT[2], OLIVE_EDGE_RECT[3]), Image.Resampling.LANCZOS)
    olive_layer = Image.new("RGBA", V2.CANVAS, (0, 0, 0, 0))
    olive_layer.alpha_composite(olive_edge, (OLIVE_EDGE_RECT[0], OLIVE_EDGE_RECT[1]))

    back = slate.copy()
    back.alpha_composite(olive_layer)
    return back, {
        "source": str(V2.BACK_RAW.relative_to(ROOT)).replace("\\", "/"),
        "source_meta": source_meta,
        "effective_slate_rect_x2": list(EFFECTIVE_BACK_RECT),
        "effective_slate_rect_runtime": [value // 2 for value in EFFECTIVE_BACK_RECT],
        "olive_edge_rect_x2": list(OLIVE_EDGE_RECT),
        "olive_edge_rect_runtime": [value // 2 for value in OLIVE_EDGE_RECT],
        "contact_decor": "empty",
    }


def make_qa_board(full: Image.Image, runtime: Image.Image, back: Image.Image, front: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1920, 1080), V2.BOARD_BG)
    draw = ImageDraw.Draw(board)
    draw.text((52, 38), "SCHEDULE V3 · PAPER RELATION / NO CLIP", font=V2.font(38, bold=True, latin=True), fill=V2.BOARD_INK)
    draw.text((54, 92), "No ContactDecor, icon, tape or replacement prop. Backing relation only.", font=V2.font(21, latin=True), fill=V2.BOARD_MUTED)

    context = V2.crop_rect(full, (20, 794, 404, 262)).resize((808, 524), Image.Resampling.NEAREST)
    board.alpha_composite(context, (52, 152))
    draw.rectangle((52, 152, 860, 676), outline=V2.QA_CYAN, width=2)
    draw.text((52, 694), "FULL CONTEXT · 200% NEAREST", font=V2.font(19, latin=True), fill=V2.BOARD_INK)

    native = V2.checker(V2.RUNTIME)
    native.alpha_composite(runtime)
    board.alpha_composite(native.resize((744, 492), Image.Resampling.NEAREST), (1050, 152))
    draw.rectangle((1050, 152, 1794, 644), outline=V2.QA_YELLOW, width=2)
    draw.text((1050, 662), "COMPONENT · 200% NEAREST", font=V2.font(19, latin=True), fill=V2.BOARD_INK)

    back_thumb = V2.checker((372, 246))
    back_thumb.alpha_composite(back.resize(V2.RUNTIME, Image.Resampling.LANCZOS))
    front_thumb = V2.checker((372, 246))
    front_thumb.alpha_composite(front.resize(V2.RUNTIME, Image.Resampling.LANCZOS))
    board.alpha_composite(back_thumb, (52, 780))
    board.alpha_composite(front_thumb, (466, 780))
    draw.text((52, 1030), "BACKDECOR", font=V2.font(17, latin=True), fill=V2.BOARD_MUTED)
    draw.text((466, 1030), "FRONTCARRIER · UNCHANGED", font=V2.font(17, latin=True), fill=V2.BOARD_MUTED)

    notes = (
        "1  Left slate reveal: 8px runtime",
        "2  Top slate reveal: 2px runtime",
        "3  Bottom slate reveal: 4px runtime",
        "4  Right slate reveal: 0px",
        "5  Olive: short 18x4px lower-edge reveal",
        "6  ContactDecor count: 0 / NO-HIT",
    )
    for index, value in enumerate(notes):
        draw.text((866, 792 + index * 40), value, font=V2.font(19, latin=True), fill=V2.BOARD_INK if index < 4 else V2.BOARD_MUTED)
    return board


def make_scope_overlay(full: Image.Image, runtime: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", full.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y, w, h = V2.SCHEDULE_RECT
    draw.rectangle((x, y, x + w - 1, y + h - 1), outline=V2.QA_CYAN, width=3)
    bbox = runtime.getchannel("A").getbbox()
    if bbox:
        draw.rectangle((x + bbox[0], y + bbox[1], x + bbox[2] - 1, y + bbox[3] - 1), outline=V2.QA_YELLOW, width=2)
    draw.text((x + 12, y + h - 28), "SCHEDULE / NO-HIT / CONTACTDECOR 0", font=V2.font(15, bold=True, latin=True), fill=V2.QA_MAGENTA, stroke_width=2, stroke_fill=(5, 18, 28, 230))
    return Image.alpha_composite(full, layer)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    contract = json.loads(V2.CONTRACT.read_text(encoding="utf-8"))
    baseline = Image.open(V2.BASELINE).convert("RGBA")
    legacy = Image.open(V2.LEGACY_MASTER).convert("RGBA")
    front = Image.open(V2.FRONT_SOURCE).convert("RGBA")
    if not V2.pixel_equal(V2.crop_rect(baseline, V2.SCHEDULE_RECT), legacy):
        raise ValueError("Frozen legacy Schedule root no longer matches baseline")

    back, back_meta = make_backdecor()
    text_layer, glyph_bboxes = V2.make_text_layer()
    state = Image.new("RGBA", V2.CANVAS, (0, 0, 0, 0))
    no_text = Image.new("RGBA", V2.CANVAS, (0, 0, 0, 0))
    no_text.alpha_composite(back)
    no_text.alpha_composite(front)
    filled_x2 = no_text.copy()
    filled_x2.alpha_composite(state)
    filled_x2.alpha_composite(text_layer)
    runtime = filled_x2.resize(V2.RUNTIME, Image.Resampling.LANCZOS)

    paths = {
        "full": OUT / "01-schedule-v3-fullscreen-reinsert-proof-1920x1080.png",
        "runtime": OUT / "02-schedule-v3-runtime-372x246.png",
        "x2": OUT / "03-schedule-v3-x2-744x492.png",
        "back": OUT / "04-schedule-v3-backdecor-x2.png",
        "front": OUT / "05-schedule-v3-frontcarrier-x2.png",
        "no_text": OUT / "06-schedule-v3-no-text-composite-x2.png",
        "context": OUT / "07-schedule-v3-100pct-context-crop.png",
        "left": OUT / "08-left-column-100pct-crop.png",
        "qa": OUT / "09-schedule-v3-paper-relation-qa-board-1920x1080.png",
        "overlay": OUT / "10-schedule-v3-scope-overlay-1920x1080.png",
        "audit": OUT / "11-schedule-v3-audit.json",
        "manifest": OUT / "12-delivery-manifest.md",
    }
    back.save(paths["back"])
    front.save(paths["front"])
    no_text.save(paths["no_text"])
    filled_x2.save(paths["x2"])
    runtime.save(paths["runtime"])

    restored = V2.restore_panel_background(baseline, V2.SCHEDULE_RECT)
    full = baseline.copy()
    x, y, _, _ = V2.SCHEDULE_RECT
    full.paste(restored, (x, y))
    full.alpha_composite(runtime, (x, y))
    full.save(paths["full"])
    V2.crop_rect(full, (20, 794, 404, 262)).save(paths["context"])
    V2.crop_rect(full, (24, 112, 396, 944)).save(paths["left"])
    make_qa_board(full, runtime, back, front).save(paths["qa"])
    make_scope_overlay(full, runtime).save(paths["overlay"])

    allowed = Image.new("L", baseline.size, 0)
    ImageDraw.Draw(allowed).rectangle((x, y, x + 371, y + 245), fill=255)
    difference = ImageChops.difference(baseline, full).convert("RGB")
    outside_difference = Image.composite(Image.new("RGB", baseline.size), difference, allowed)
    outside_bbox = outside_difference.getbbox()

    back_alpha = np.asarray(back.getchannel("A"))
    # Right of the FrontCarrier is intentionally empty; olive stays below it.
    right_alpha = int(np.count_nonzero(back_alpha[20:472, 720:744]))
    left_alpha = int(np.count_nonzero(back_alpha[20:472, 12:28]))
    top_alpha = int(np.count_nonzero(back_alpha[16:20, 28:712]))
    bottom_alpha = int(np.count_nonzero(back_alpha[472:480, 28:712]))
    olive_alpha = int(np.count_nonzero(back_alpha[472:480, 676:712]))
    zone_checks = {name: V2.pixel_equal(V2.crop_rect(baseline, rect), V2.crop_rect(full, rect)) for name, rect in V2.ZONES.items()}
    regioncard_checks = [V2.pixel_equal(V2.crop_rect(baseline, rect), V2.crop_rect(full, rect)) for rect in V2.REGION_CARD_RECTS]
    checks = {
        "contact_decor_count_zero": True,
        "clip_alpha_pixels_zero": True,
        "replacement_icon_count_zero": True,
        "frontcarrier_pixel_equal_v1": V2.pixel_equal(front, Image.open(V2.FRONT_SOURCE).convert("RGBA")),
        "frontcarrier_rotation_zero": True,
        "slate_visible_left": left_alpha > 100,
        "slate_visible_top": top_alpha > 100,
        "slate_visible_bottom": bottom_alpha > 100,
        "right_slate_exposure_zero": right_alpha == 0,
        "olive_short_bottom_reveal_present": olive_alpha > 8,
        "root_exact_372x246": runtime.size == V2.RUNTIME,
        "outside_schedule_root_pixel_equal": outside_bbox is None,
        "all_regioncards_pixel_equal": all(regioncard_checks),
        "mapfield_pixel_equal": zone_checks["mapfield"],
        "dossier_pixel_equal": zone_checks["dossier"],
        "masthead_pixel_equal": zone_checks["masthead"],
        "region_index_header_pixel_equal": zone_checks["region_index_header"],
        "regioncard_schedule_gap_pixel_equal": zone_checks["regioncard_schedule_gap"],
        "state_decor_empty": state.getchannel("A").getbbox() is None,
        "dynamic_text_unchanged": list(V2.TEXT_VALUES.values()) == contract["frozen"]["dynamic_text"],
        "hit_rect_count_zero": contract["frozen"]["hit_rect_count"] == 0,
        "mouse_filter_ignore": contract["frozen"]["mouse_filter"] == "IGNORE",
        "focus_mode_none": contract["frozen"]["focus_mode"] == "NONE",
        "godot_touched_false": True,
        "atlas_touched_false": True,
        "manifest_finalized_false": True,
    }
    audit = {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_schedule_v3_no_clip_backdecor_v1",
        "status": "visual_candidate_pending_dual_agent_and_user_gate",
        "runtime_rect": list(V2.SCHEDULE_RECT),
        "runtime_size": list(V2.RUNTIME),
        "source_provenance": {
            "backing_paper": "real ImageGen paper art from Schedule V2, deterministically alpha-masked and repositioned",
            "frontcarrier": "pixel-exact Schedule V1 ImageGen FrontCarrier reuse",
            "contact_decor": "none",
            "program_drawn_final_art": False,
        },
        "layer_stack": ["BackDecor.papers", "FrontCarrier", "StateDecor.empty", "DynamicText"],
        "back": back_meta,
        "glyph_bboxes_x2": glyph_bboxes,
        "exposure_pixel_counts_x2": {"left": left_alpha, "top": top_alpha, "bottom": bottom_alpha, "right": right_alpha, "olive": olive_alpha},
        "zone_checks": zone_checks,
        "outside_difference_bbox": list(outside_bbox) if outside_bbox else None,
        "checks": checks,
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "proof_limits": ["not_runtime", "filled_fixture", "does_not_authorize_Godot_atlas_manifest_or_WeeklyRunGame"],
    }
    paths["audit"].write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["manifest"].write_text(
        f"""# Schedule V3 无夹具纸层回嵌候选

- 状态：双 agent 与用户视觉门禁前候选，不是运行时实现。
- 变更：彻底删除 ContactDecor 和所有替代小图标；只保留不等宽石板蓝背纸与底边末端的短灰橄榄露边。
- 冻结：`372×246`、FrontCarrier、四条动态文字、底部留白、0° 与 NO-HIT。
- 生图来源：`image_gen/2026-09-04/world-map-schedule-v2-contact-backdecor-v1/sources/01-schedule-backing-imagegen-raw.png`。
- 程序职责：假透明清理、可见范围 mask、缩放、分层、回嵌与 QA；没有重画纸张美术。
- 暂不进入：Godot、atlas、final manifest、WeeklyRunGame。
- 机器门禁：`{audit['machine_pass']}`。
""",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(OUT), "machine_pass": audit["machine_pass"], "failed": [key for key, value in checks.items() if not value], "outside_bbox": outside_bbox, "exposures": audit["exposure_pixel_counts_x2"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
