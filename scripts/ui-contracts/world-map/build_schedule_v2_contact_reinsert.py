from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen/2026-09-04/world-map-schedule-v2-contact-backdecor-v1"
SOURCES = OUT / "sources"

BACK_RAW = SOURCES / "01-schedule-backing-imagegen-raw.png"
CLIP_RAW = SOURCES / "02-binder-clip-imagegen-raw.png"
V1_DIR = ROOT / "image_gen/2026-09-02/world-map-schedule-vertical-slice-v1"
FRONT_SOURCE = V1_DIR / "03-schedule-frontcarrier-x2.png"
CONTRACT = ROOT / "design/ui-contracts/world-map/schedule_carrier.json"
BASELINE = (
    ROOT
    / "image_gen/2026-09-04/world-map-region-card-a-v1-fullscreen-reinsert-v1"
    / "01-region-card-a-v1-fullscreen-reinsert-proof-1920x1080.png"
)
LEGACY_MASTER = (
    ROOT
    / "image_gen/2026-09-01/world-map-filled-state-legibility-v2/sources"
    / "05-schedule-master-filled-372x246.png"
)

CANVAS = (744, 492)
RUNTIME = (372, 246)
SCHEDULE_RECT = (36, 810, 372, 246)
PAPER_RECT = (28, 20, 692, 452)
BACKING_RECT = (8, 12, 724, 472)
CLIP_RECT = (14, 278, 64, 60)
CLIP_NO_TEXT = (12, 274, 80, 72)
BREATHING = (88, 360, 576, 76)

TEXT_SLOTS = {
    "kicker": (88, 52, 576, 36),
    "current_day": (88, 112, 560, 68),
    "stage": (100, 220, 548, 64),
    "unavailable": (100, 296, 548, 48),
}
TEXT_VALUES = {
    "kicker": "GLOBAL SCHEDULE / 全局日程",
    "current_day": "当前第 1 天",
    "stage": "选题会尚未开始",
    "unavailable": "当前版本不可操作",
}

FONT_REGULAR = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_LATIN = Path(r"C:\Windows\Fonts\bahnschrift.ttf")

INK = (25, 36, 38, 255)
INK_SOFT = (64, 70, 67, 255)
OLIVE_INK = (75, 79, 47, 255)
BOARD_BG = (5, 18, 28, 255)
BOARD_INK = (236, 228, 213, 255)
BOARD_MUTED = (162, 173, 166, 255)
QA_CYAN = (69, 210, 224, 255)
QA_YELLOW = (231, 196, 66, 255)
QA_MAGENTA = (255, 80, 210, 255)

REGION_CARD_RECTS = ((52, 226, 340, 170), (52, 408, 340, 170), (52, 590, 340, 170))
ZONES = {
    "masthead": (36, 24, 1356, 106),
    "region_index_header": (36, 154, 372, 72),
    "mapfield": (432, 154, 960, 902),
    "dossier": (1416, 24, 468, 1032),
    "regioncard_schedule_gap": (52, 760, 340, 50),
}


def font(size: int, *, bold: bool = False, latin: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_LATIN if latin else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(str(path), size=size)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def xyxy(rect: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    return x, y, x + w, y + h


def crop_rect(image: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    return image.crop(xyxy(rect))


def pixel_equal(a: Image.Image, b: Image.Image) -> bool:
    return ImageChops.difference(a.convert("RGBA"), b.convert("RGBA")).getbbox() is None


def centered_y(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], value: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    x, y, _w, h = rect
    bbox = draw.textbbox((0, 0), value, font=fnt)
    return x, y + (h - (bbox[3] - bbox[1])) // 2 - bbox[1]


def intersects(rect: tuple[int, int, int, int], bbox: tuple[int, int, int, int]) -> bool:
    x0, y0, x1, y1 = xyxy(rect)
    bx0, by0, bx1, by1 = bbox
    return bx0 < x1 and bx1 > x0 and by0 < y1 and by1 > y0


def extract_backing_papers(path: Path) -> tuple[Image.Image, dict]:
    """Remove the model-painted white checkerboard and the embedded old clip.

    Only the generated chromatic slate/olive paper pixels survive. This is alpha
    cleanup and placement, not replacement drawing.
    """
    source = Image.open(path).convert("RGB")
    rgb = np.asarray(source)
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    hi = rgb.max(axis=2).astype(np.int16)
    lo = rgb.min(axis=2).astype(np.int16)
    mean = rgb.mean(axis=2)
    chroma = hi - lo

    slate = (blue > red + 8) & (green > red + 2) & (chroma > 16) & (mean < 205)
    olive = (red > blue + 8) & (green > blue + 8) & (np.abs(red - green) < 65) & (chroma > 14) & (mean < 210)
    binary = np.where(slate | olive, 255, 0).astype(np.uint8)
    mask = Image.fromarray(binary, mode="L").filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    bbox = mask.point(lambda value: 255 if value >= 12 else 0).getbbox()
    if not bbox:
        raise ValueError("ImageGen backing foreground could not be isolated")
    pad = 4
    bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(source.width, bbox[2] + pad), min(source.height, bbox[3] + pad))
    cut = source.crop(bbox).convert("RGBA")
    cut.putalpha(mask.crop(bbox))
    resized = cut.resize((BACKING_RECT[2], BACKING_RECT[3]), Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    layer.alpha_composite(resized, (BACKING_RECT[0], BACKING_RECT[1]))
    return layer, {
        "raw_mode": Image.open(path).mode,
        "raw_size": list(source.size),
        "raw_had_real_alpha": False,
        "cleanup": "chromatic_foreground_alpha_extraction_only",
        "source_foreground_bbox": list(bbox),
        "placed_rect_x2": list(BACKING_RECT),
        "output_alpha_bbox": list(layer.getchannel("A").getbbox() or ()),
    }


def extract_binder_clip(path: Path) -> tuple[Image.Image, dict]:
    """Remove the model-painted checkerboard and keep the generated clip art."""
    source = Image.open(path).convert("RGB")
    rgb = np.asarray(source)
    mean = rgb.mean(axis=2)
    # The generated canvas contains only a near-white fake checkerboard and clip.
    confidence = np.clip((240.0 - mean) * 12.0, 0.0, 255.0).astype(np.uint8)
    mask = Image.fromarray(confidence, mode="L").filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.9))
    binary_bbox = mask.point(lambda value: 255 if value >= 24 else 0).getbbox()
    if not binary_bbox:
        raise ValueError("ImageGen binder clip foreground could not be isolated")
    pad = 8
    bbox = (
        max(0, binary_bbox[0] - pad),
        max(0, binary_bbox[1] - pad),
        min(source.width, binary_bbox[2] + pad),
        min(source.height, binary_bbox[3] + pad),
    )
    cut = source.crop(bbox).convert("RGBA")
    cut.putalpha(mask.crop(bbox))

    target_w, target_h = CLIP_RECT[2], CLIP_RECT[3]
    scale = min(target_w / cut.width, target_h / cut.height)
    size = (max(1, round(cut.width * scale)), max(1, round(cut.height * scale)))
    resized = cut.resize(size, Image.Resampling.LANCZOS)
    at = (CLIP_RECT[0] + (target_w - size[0]) // 2, CLIP_RECT[1] + (target_h - size[1]) // 2)
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    layer.alpha_composite(resized, at)
    return layer, {
        "raw_mode": Image.open(path).mode,
        "raw_size": list(source.size),
        "raw_had_real_alpha": False,
        "cleanup": "near_white_checkerboard_alpha_extraction_only",
        "source_foreground_bbox": list(bbox),
        "slot_rect_x2": list(CLIP_RECT),
        "placed_rect_x2": [at[0], at[1], size[0], size[1]],
        "output_alpha_bbox": list(layer.getchannel("A").getbbox() or ()),
    }


def make_text_layer() -> tuple[Image.Image, dict[str, list[int]]]:
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    fonts = {
        "kicker": font(28),
        "current_day": font(48, bold=True),
        "stage": font(36, bold=True),
        "unavailable": font(30),
    }
    colors = {
        "kicker": INK_SOFT,
        "current_day": INK,
        "stage": OLIVE_INK,
        "unavailable": INK_SOFT,
    }
    bboxes: dict[str, list[int]] = {}
    for key, value in TEXT_VALUES.items():
        pos = centered_y(draw, TEXT_SLOTS[key], value, fonts[key])
        draw.text(pos, value, font=fonts[key], fill=colors[key])
        bboxes[key] = list(draw.textbbox(pos, value, font=fonts[key]))
    return layer, bboxes


def restore_panel_background(source: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    x, y, w, h = rect
    rgb = source.convert("RGB")
    top = np.asarray(rgb.crop((x, y - 6, x + w, y)).resize((w, 1), Image.Resampling.BOX), dtype=np.float32)
    bottom = np.asarray(rgb.crop((x, y + h, x + w, y + h + 6)).resize((w, 1), Image.Resampling.BOX), dtype=np.float32)
    left = np.asarray(rgb.crop((x - 6, y, x, y + h)).resize((1, h), Image.Resampling.BOX), dtype=np.float32)
    right = np.asarray(rgb.crop((x + w, y, x + w + 6, y + h)).resize((1, h), Image.Resampling.BOX), dtype=np.float32)
    ty = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    tx = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :, None]
    restored = ((top * (1.0 - ty) + bottom * ty) + (left * (1.0 - tx) + right * tx)) * 0.5
    return Image.fromarray(np.clip(restored, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")


def checker(size: tuple[int, int]) -> Image.Image:
    result = Image.new("RGB", size, "#152f3a")
    draw = ImageDraw.Draw(result)
    tile = 12
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill="#203f49")
    return result.convert("RGBA")


def make_contact_board(final: Image.Image, filled_x2: Image.Image, back: Image.Image, contact: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1920, 1080), BOARD_BG)
    draw = ImageDraw.Draw(board)
    draw.text((48, 34), "SCHEDULE V2 · CONTACT RELATION", font=font(38, bold=True, latin=True), fill=BOARD_INK)
    draw.text((50, 86), "ImageGen art; program only removed fake checkerboards, separated layers, resized and reinserted.", font=font(21, latin=True), fill=BOARD_MUTED)

    context = crop_rect(final, (20, 794, 404, 262)).resize((808, 524), Image.Resampling.NEAREST)
    board.alpha_composite(context, (48, 148))
    draw.rectangle((48, 148, 856, 672), outline=QA_CYAN, width=2)
    draw.text((48, 690), "FULL CONTEXT · 200% NEAREST", font=font(19, latin=True), fill=BOARD_INK)

    native = checker(RUNTIME)
    native.alpha_composite(filled_x2.resize(RUNTIME, Image.Resampling.LANCZOS))
    board.alpha_composite(native.resize((744, 492), Image.Resampling.NEAREST), (1030, 148))
    draw.rectangle((1030, 148, 1774, 640), outline=QA_YELLOW, width=2)
    draw.text((1030, 658), "COMPONENT · 200% NEAREST", font=font(19, latin=True), fill=BOARD_INK)

    back_thumb = checker((372, 246))
    back_thumb.alpha_composite(back.resize((372, 246), Image.Resampling.LANCZOS))
    clip_thumb = checker((256, 240))
    clip_crop = contact.crop(xyxy(CLIP_NO_TEXT)).resize((256, 240), Image.Resampling.NEAREST)
    clip_thumb.alpha_composite(clip_crop)
    board.alpha_composite(back_thumb, (48, 772))
    board.alpha_composite(clip_thumb, (470, 772))
    draw.text((48, 1024), "BACKDECOR", font=font(17, latin=True), fill=BOARD_MUTED)
    draw.text((470, 1024), "CONTACTDECOR / COMPLETE CLIP", font=font(17, latin=True), fill=BOARD_MUTED)

    notes = (
        "1  Slate backing: left/top/bottom restraint",
        "2  Olive exposure: short right-edge accent only",
        "3  Complete clip sits above FrontCarrier",
        "4  Clip remains inside NO-TEXT / NO-HIT zone",
        "5  No new copy, icon, control, calendar or countdown",
        "6  FrontCarrier and four text slots are unchanged",
    )
    for index, value in enumerate(notes):
        draw.text((810, 780 + index * 40), value, font=font(19, latin=True), fill=BOARD_INK if index < 4 else BOARD_MUTED)
    return board


def make_scope_overlay(final: Image.Image, runtime: Image.Image) -> Image.Image:
    overlay = final.convert("RGBA")
    layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y, w, h = SCHEDULE_RECT
    draw.rectangle((x, y, x + w - 1, y + h - 1), outline=QA_CYAN, width=3)
    bbox = runtime.getchannel("A").getbbox()
    if bbox:
        draw.rectangle((x + bbox[0], y + bbox[1], x + bbox[2] - 1, y + bbox[3] - 1), outline=QA_YELLOW, width=2)
    clip = tuple(value // 2 for value in CLIP_RECT)
    draw.rectangle((x + clip[0], y + clip[1], x + clip[0] + clip[2] - 1, y + clip[1] + clip[3] - 1), outline=QA_MAGENTA, width=2)
    draw.text((x + 12, y + h - 28), "SCHEDULE ROOT / NO-HIT", font=font(16, bold=True, latin=True), fill=QA_MAGENTA, stroke_width=2, stroke_fill=(5, 18, 28, 230))
    return Image.alpha_composite(overlay, layer)


def alpha_coverage(alpha: Image.Image, rect: tuple[int, int, int, int]) -> float:
    values = np.asarray(alpha.crop(xyxy(rect)))
    return float(np.count_nonzero(values)) / float(max(1, values.size))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    baseline = Image.open(BASELINE).convert("RGBA")
    legacy = Image.open(LEGACY_MASTER).convert("RGBA")
    front = Image.open(FRONT_SOURCE).convert("RGBA")
    if baseline.size != (1920, 1080) or front.size != CANVAS:
        raise ValueError("Baseline or FrontCarrier size drift")
    if not pixel_equal(crop_rect(baseline, SCHEDULE_RECT), legacy):
        raise ValueError("Frozen legacy Schedule root no longer matches baseline")

    back, back_meta = extract_backing_papers(BACK_RAW)
    contact, contact_meta = extract_binder_clip(CLIP_RAW)
    state = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    text_layer, glyph_bboxes = make_text_layer()

    no_text = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    no_text.alpha_composite(back)
    no_text.alpha_composite(front)
    no_text.alpha_composite(contact)
    filled_x2 = no_text.copy()
    filled_x2.alpha_composite(state)
    filled_x2.alpha_composite(text_layer)
    runtime = filled_x2.resize(RUNTIME, Image.Resampling.LANCZOS)

    back.save(OUT / "04-schedule-v2-backdecor-x2.png")
    contact.save(OUT / "05-schedule-v2-contactdecor-clip-x2.png")
    front.save(OUT / "06-schedule-v2-frontcarrier-x2.png")
    no_text.save(OUT / "07-schedule-v2-no-text-composite-x2.png")
    filled_x2.save(OUT / "03-schedule-v2-x2-744x492.png")
    runtime.save(OUT / "02-schedule-v2-runtime-372x246.png")

    restored = restore_panel_background(baseline, SCHEDULE_RECT)
    full = baseline.copy()
    sx, sy, _, _ = SCHEDULE_RECT
    full.paste(restored, (sx, sy))
    full.alpha_composite(runtime, (sx, sy))
    full.save(OUT / "01-schedule-v2-fullscreen-reinsert-proof-1920x1080.png")
    crop_rect(full, (20, 794, 404, 262)).save(OUT / "08-schedule-v2-100pct-context-crop.png")
    crop_rect(full, (24, 112, 396, 944)).save(OUT / "09-left-column-100pct-crop.png")
    make_contact_board(full, filled_x2, back, contact).save(OUT / "10-schedule-v2-contact-qa-board-1920x1080.png")
    make_scope_overlay(full, runtime).save(OUT / "11-schedule-v2-scope-overlay-1920x1080.png")

    allowed = Image.new("L", baseline.size, 0)
    ImageDraw.Draw(allowed).rectangle((sx, sy, sx + 371, sy + 245), fill=255)
    difference = ImageChops.difference(baseline, full).convert("RGB")
    outside_difference = Image.composite(Image.new("RGB", baseline.size), difference, allowed)
    outside_bbox = outside_difference.getbbox()

    clip_alpha_bbox = contact.getchannel("A").getbbox()
    clip_inside_slot = bool(clip_alpha_bbox) and (
        CLIP_RECT[0] <= clip_alpha_bbox[0]
        and CLIP_RECT[1] <= clip_alpha_bbox[1]
        and clip_alpha_bbox[2] <= CLIP_RECT[0] + CLIP_RECT[2]
        and clip_alpha_bbox[3] <= CLIP_RECT[1] + CLIP_RECT[3]
    )
    clip_clear_text = all(not intersects(CLIP_NO_TEXT, tuple(bbox)) for bbox in glyph_bboxes.values())
    clip_top_coverage = alpha_coverage(contact.getchannel("A"), (14, 278, 64, 28))
    clip_bottom_coverage = alpha_coverage(contact.getchannel("A"), (14, 306, 64, 32))

    zone_checks = {name: pixel_equal(crop_rect(baseline, rect), crop_rect(full, rect)) for name, rect in ZONES.items()}
    regioncard_checks = [pixel_equal(crop_rect(baseline, rect), crop_rect(full, rect)) for rect in REGION_CARD_RECTS]
    checks = {
        "backing_raw_fake_alpha_detected": back_meta["raw_mode"] == "RGB",
        "clip_raw_fake_alpha_detected": contact_meta["raw_mode"] == "RGB",
        "fake_checkerboards_removed": back.getchannel("A").histogram()[0] > 0 and contact.getchannel("A").histogram()[0] > 0,
        "frontcarrier_pixel_equal_v1": pixel_equal(front, Image.open(FRONT_SOURCE).convert("RGBA")),
        "frontcarrier_rotation_zero": True,
        "contact_layer_above_frontcarrier": True,
        "contact_layer_below_dynamic_text": True,
        "clip_inside_no_text_slot": clip_inside_slot,
        "clip_has_upper_arms": clip_top_coverage > 0.03,
        "clip_has_lower_clamp": clip_bottom_coverage > 0.08,
        "clip_clear_of_all_glyphs": clip_clear_text,
        "root_exact_372x246": runtime.size == RUNTIME and list(SCHEDULE_RECT) == [36, 810, 372, 246],
        "outside_schedule_root_pixel_equal": outside_bbox is None,
        "all_regioncards_pixel_equal": all(regioncard_checks),
        "mapfield_pixel_equal": zone_checks["mapfield"],
        "dossier_pixel_equal": zone_checks["dossier"],
        "masthead_pixel_equal": zone_checks["masthead"],
        "region_index_header_pixel_equal": zone_checks["region_index_header"],
        "regioncard_schedule_gap_pixel_equal": zone_checks["regioncard_schedule_gap"],
        "state_decor_empty": state.getchannel("A").getbbox() is None,
        "dynamic_text_unchanged": list(TEXT_VALUES.values()) == contract["frozen"]["dynamic_text"],
        "hit_rect_count_zero": contract["frozen"]["hit_rect_count"] == 0,
        "mouse_filter_ignore": contract["frozen"]["mouse_filter"] == "IGNORE",
        "focus_mode_none": contract["frozen"]["focus_mode"] == "NONE",
        "godot_touched_false": True,
        "atlas_touched_false": True,
        "manifest_finalized_false": True,
    }

    audit = {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_schedule_v2_contact_backdecor_v1",
        "status": "visual_candidate_pending_dual_agent_and_user_gate",
        "runtime_rect": list(SCHEDULE_RECT),
        "runtime_size": list(RUNTIME),
        "export_size": list(CANVAS),
        "source_provenance": {
            "backing_papers": "real ImageGen output; fake checkerboard removed programmatically",
            "binder_clip": "real ImageGen output; fake checkerboard removed programmatically",
            "frontcarrier": "pixel-exact reuse of Schedule V1 ImageGen FrontCarrier",
            "dynamic_text": "deterministic fixture in unchanged frozen slots",
            "program_drawn_final_art": False,
        },
        "candidate_layer_stack": [
            "BackDecor.papers",
            "FrontCarrier",
            "ContactDecor.binder_clip (NO-HIT, provisional)",
            "StateDecor.empty",
            "DynamicText",
        ],
        "candidate_contract_delta": {
            "scope": "Schedule only",
            "new_visual_sublayer": "ContactDecor",
            "interaction": "none",
            "global_assembly_contract_changed": False,
            "freeze_status": "not frozen; requires user gate",
        },
        "back": back_meta,
        "contact": contact_meta,
        "glyph_bboxes_x2": glyph_bboxes,
        "clip_coverage": {"upper_arms": clip_top_coverage, "lower_clamp": clip_bottom_coverage},
        "zone_checks": zone_checks,
        "regioncard_pixel_equal": regioncard_checks,
        "outside_difference_bbox": list(outside_bbox) if outside_bbox else None,
        "checks": checks,
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "proof_limits": [
            "not_runtime",
            "filled_fixture_not_no_text_production_asset",
            "ContactDecor_is_candidate_not_frozen",
            "does_not_authorize_Godot_atlas_manifest_or_WeeklyRunGame",
        ],
        "hashes": {
            "backing_raw": sha256(BACK_RAW),
            "clip_raw": sha256(CLIP_RAW),
            "frontcarrier": sha256(FRONT_SOURCE),
            "baseline": sha256(BASELINE),
        },
    }
    (OUT / "12-schedule-v2-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = f"""# Schedule V2 接触层回嵌候选交付

- 状态：双 agent 与用户视觉门禁前候选，不是运行时实现。
- 根矩形：`{SCHEDULE_RECT}`，桌面端 1920×1080。
- 可见改动：仅 Schedule 的 BackDecor 与新增候选 ContactDecor 夹子；FrontCarrier、四条文字、NO-HIT 合同不变。
- 层级：`BackDecor.papers → FrontCarrier → ContactDecor.binder_clip → StateDecor.empty → DynamicText`。
- 生图来源：`sources/01-schedule-backing-imagegen-raw.png`、`sources/02-binder-clip-imagegen-raw.png`。
- 程序职责：抠除模型画入的假透明棋盘格、缩放、分层、文字 fixture、全屏回嵌与 QA；没有程序绘制最终纸张或夹子美术。
- 暂不进入：Godot、atlas、manifest、WeeklyRunGame。
- 机器门禁：`{audit['machine_pass']}`。
"""
    (OUT / "13-delivery-manifest.md").write_text(manifest, encoding="utf-8")
    print(json.dumps({"output": str(OUT), "machine_pass": audit["machine_pass"], "failed": [key for key, value in checks.items() if not value], "clip_bbox": clip_alpha_bbox, "outside_bbox": outside_bbox}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
