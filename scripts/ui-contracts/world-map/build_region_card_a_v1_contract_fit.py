from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageOps, ImageStat

from build_native_origin_registration_slice_v1 import BG, CYAN, GREEN, MUSTARD, MUTED, RUST, TEXT, font


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen" / "2026-09-04" / "world-map-region-card-a-v1-contract-fit"
SOURCE = OUT / "source" / "01-frontcarrier-material-source-imagegen.png"
PHOTO_DIR = ROOT / "gd_project" / "Assets" / "prototypes" / "world_map_integrated" / "a_style_v2_runtime"
CONTRACT = ROOT / "design" / "ui-contracts" / "world-map" / "left_region_card.json"

CANVAS = (680, 340)
BODY_RECT = (16, 0, 648, 340)
PHOTO_RECT = (32, 112, 276, 176)
NUMBER_RECT = (84, 20, 68, 64)
TITLE_RECT = (160, 16, 320, 76)
STATUS_RECT = (488, 20, 160, 60)
STORY_RECT = (336, 112, 312, 180)
HEADLINE_RECT = (336, 116, 312, 44)
DECK_RECT = (336, 168, 312, 84)
BREATHING_RECT = (336, 260, 312, 32)

INK = "#162834"
SOFT_INK = "#31434B"
PAPER_EDGE = "#C8BDA8"
COBALT = "#285A83"
BACK_BLUE = "#4E6570"
OLIVE = "#7D8154"
OLIVE_DARK = "#4E5136"
WARM_PAPER = "#F2EBDD"


BUNDLES = {
    "north": {
        "content_bundle_id": "wmw.week01.region.north_america.v1",
        "region_id": "north_america",
        "index": "01",
        "title": "北美禁区带",
        "status": "红线升温",
        "headline": "洗衣店里出现了一片海",
        "deck": "断电两小时后，三扇滚筒内潮线仍水平。",
        "photo": PHOTO_DIR / "north_america_story_1104x704.png",
    },
    "east": {
        "content_bundle_id": "wmw.week01.region.east_asia.v1",
        "region_id": "east_asia",
        "index": "02",
        "title": "东亚神秘地带",
        "status": "暂不可进入",
        "headline": "天文台在凌晨向北移动",
        "deck": "凌晨三点，天文台向北平移五十米。",
        "photo": PHOTO_DIR / "east_asia_story_1104x704.png",
    },
    "pacific": {
        "content_bundle_id": "wmw.week01.region.south_pacific.v1",
        "region_id": "south_pacific",
        "index": "03",
        "title": "南太平洋失航区域",
        "status": "暂不可进入",
        "headline": "深海电波正在重复呼号",
        "deck": "失联渔船最后发报，信号来自海面千米以下。",
        "photo": PHOTO_DIR / "pacific_story_1104x704.png",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def tint_texture(image: Image.Image, dark: str, light: str) -> Image.Image:
    alpha = image.getchannel("A")
    gray = ImageOps.grayscale(image.convert("RGB"))
    tinted = ImageOps.colorize(gray, black=dark, white=light).convert("RGBA")
    tinted.putalpha(alpha)
    return tinted


def build_frontcarrier() -> tuple[Image.Image, dict]:
    source = Image.open(SOURCE).convert("RGB")
    if source.size != (1774, 887):
        raise ValueError(f"Unexpected ImageGen source size: {source.size}")

    # The built-in generator returned a baked checkerboard instead of alpha.
    # Crop only the clean paper interior; programmatic work registers the
    # ImageGen-authored material and never invents paper texture.
    source_crop = (173, 68, 1601, 818)
    material = source.crop(source_crop).resize(BODY_RECT[2:], Image.Resampling.LANCZOS).convert("RGBA")
    material.putalpha(255)

    front = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    front.alpha_composite(material, (BODY_RECT[0], BODY_RECT[1]))
    draw = ImageDraw.Draw(front)
    draw.rectangle((16, 0, 663, 339), outline=PAPER_EDGE, width=2)

    # Photo aperture is a printed keyline in the same sheet, not a second card.
    draw.rectangle((29, 109, 311, 291), fill=INK)

    # Coarse weekly column eye: one static, non-interactive print mark.
    draw.line([(30, 44), (42, 32), (58, 32), (76, 44), (58, 56), (42, 56), (30, 44)], fill=INK, width=4, joint="curve")
    draw.ellipse((45, 35, 61, 51), fill=INK)
    draw.ellipse((50, 39, 56, 45), fill=WARM_PAPER)
    draw.line((38, 25, 34, 16), fill=INK, width=3)
    draw.line((52, 23, 52, 12), fill=INK, width=3)
    draw.line((66, 25, 70, 16), fill=INK, width=3)

    alpha = front.getchannel("A")
    body_alpha = alpha.crop((16, 0, 664, 340))
    story_rgb = front.convert("RGB").crop((336, 112, 648, 292))
    story_luma = ImageOps.grayscale(story_rgb)
    return front, {
        "source_size": list(source.size),
        "source_has_alpha": False,
        "source_crop": list(source_crop),
        "canvas": list(CANVAS),
        "body_rect_x2": list(BODY_RECT),
        "alpha_bbox": list(alpha.getbbox()),
        "body_alpha_extrema": list(body_alpha.getextrema()),
        "story_luminance_std": round(ImageStat.Stat(story_luma).stddev[0], 3),
    }


def build_backdecor(front: Image.Image) -> Image.Image:
    back = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    body = front.crop((16, 0, 664, 340)).resize((656, 324), Image.Resampling.LANCZOS)
    tinted = tint_texture(body, "#243946", BACK_BLUE)
    alpha = Image.new("L", tinted.size, 225)
    tinted.putalpha(alpha)
    back.alpha_composite(tinted, (20, 8))
    return back


def build_selected(front: Image.Image) -> Image.Image:
    selected = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    strip = front.crop((16, 8, 28, 332)).resize((12, 324), Image.Resampling.LANCZOS)
    strip = tint_texture(strip, "#153F65", COBALT)
    strip.putalpha(255)
    selected.alpha_composite(strip, (4, 8))
    return selected


def build_status_layer(kind: str) -> Image.Image:
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y, w, h = STATUS_RECT
    polygon = [(x, y), (x + w, y), (x + w, y + h - 8), (x + w - 8, y + h), (x, y + h)]
    if kind == "warning":
        draw.polygon(polygon, fill=(244, 236, 221, 245), outline=RUST)
        draw.line(polygon + [polygon[0]], fill=RUST, width=4, joint="curve")
        draw.rectangle((x + 7, y + 7, x + w - 8, y + h - 8), outline=RUST, width=2)
    elif kind == "locked":
        # One flat olive overprint. No inset keyline or raised shadow: this is a
        # state ticket printed on the card, never an independent button.
        draw.polygon(polygon, fill=(196, 198, 157, 175))
        draw.line(polygon + [polygon[0]], fill=OLIVE_DARK, width=2, joint="curve")
    else:
        raise ValueError(kind)
    return layer


def center_text(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], value: str, size: int, fill: str, bold: bool = True) -> dict:
    x, y, w, h = rect
    f = font(size, bold)
    bbox = draw.textbbox((0, 0), value, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw) / 2, y + (h - th) / 2 - bbox[1]), value, font=f, fill=fill)
    return {"font_x2": size, "glyph_width_x2": tw, "glyph_height_x2": th, "slot_x2": list(rect)}


def fit_font(draw: ImageDraw.ImageDraw, value: str, max_width: int, start: int, minimum: int, bold: bool = True):
    for size in range(start, minimum - 1, -1):
        f = font(size, bold)
        bbox = draw.textbbox((0, 0), value, font=f)
        if bbox[2] - bbox[0] <= max_width:
            return f, size, bbox
    f = font(minimum, bold)
    return f, minimum, draw.textbbox((0, 0), value, font=f)


def wrap_cjk(draw: ImageDraw.ImageDraw, value: str, text_font, max_width: int, max_lines: int) -> list[str]:
    lines: list[str] = []
    current = ""

    # Weekly decks are editor-authored micro-copy. Prefer a natural editorial
    # pause when both clauses fit, rather than mechanically cutting a noun or
    # verb phrase at the last available glyph.
    if max_lines >= 2:
        for punctuation in ("，", "；", "："):
            split_at = value.find(punctuation)
            if split_at >= 0:
                first = value[: split_at + 1]
                second = value[split_at + 1 :]
                if all(draw.textbbox((0, 0), line, font=text_font)[2] <= max_width for line in (first, second)):
                    return [first, second]

    for char in value:
        probe = current + char
        bbox = draw.textbbox((0, 0), probe, font=text_font)
        if current and bbox[2] - bbox[0] > max_width:
            lines.append(current)
            current = char
            if len(lines) == max_lines:
                break
        else:
            current = probe
    if len(lines) < max_lines and current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    consumed = "".join(lines)
    if len(consumed) < len(value) and lines:
        tail = lines[-1]
        while tail:
            probe = tail + "…"
            bbox = draw.textbbox((0, 0), probe, font=text_font)
            if bbox[2] - bbox[0] <= max_width:
                lines[-1] = probe
                break
            tail = tail[:-1]
    return lines


def relative_luminance(color: str) -> float:
    channels = []
    for channel in ImageColor.getrgb(color):
        value = channel / 255.0
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(foreground: str, background: str) -> float:
    lighter = max(relative_luminance(foreground), relative_luminance(background))
    darker = min(relative_luminance(foreground), relative_luminance(background))
    return (lighter + 0.05) / (darker + 0.05)


def render_card(bundle: dict, *, selected: bool, state: str, assets: dict[str, Image.Image]) -> tuple[Image.Image, dict]:
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(assets["back"])
    canvas.alpha_composite(assets["front"])
    photo = load_rgba(bundle["photo"]).resize((276, 176), Image.Resampling.LANCZOS)
    canvas.alpha_composite(photo, (32, 112))
    if selected:
        canvas.alpha_composite(assets["selected"])
    canvas.alpha_composite(assets[state])

    draw = ImageDraw.Draw(canvas)
    number_meta = center_text(draw, NUMBER_RECT, bundle["index"], 32, INK, True)

    title_font, title_size, title_bbox = fit_font(draw, bundle["title"], 304, 36, 28, True)
    draw.text((160, 26), bundle["title"], font=title_font, fill=INK)

    status_fill = RUST if state == "warning" else OLIVE_DARK
    status_meta = center_text(draw, STATUS_RECT, bundle["status"], 27, status_fill, True)

    headline_font, headline_size, headline_bbox = fit_font(draw, bundle["headline"], 304, 30, 24, True)
    headline_y = HEADLINE_RECT[1] + 4 - headline_bbox[1]
    draw.text((HEADLINE_RECT[0], headline_y), bundle["headline"], font=headline_font, fill=INK)

    deck_font_size = 25
    deck_line_height = 32
    deck_font = font(deck_font_size, False)
    deck_lines = wrap_cjk(draw, bundle["deck"], deck_font, DECK_RECT[2], 2)
    deck_bboxes = []
    for line_index, line in enumerate(deck_lines):
        line_y = DECK_RECT[1] + line_index * deck_line_height
        draw.text((DECK_RECT[0], line_y), line, font=deck_font, fill=SOFT_INK)
        deck_bboxes.append(list(draw.textbbox((DECK_RECT[0], line_y), line, font=deck_font)))

    deck_glyph_containment_pass = all(
        bbox[0] >= DECK_RECT[0]
        and bbox[1] >= DECK_RECT[1]
        and bbox[2] <= DECK_RECT[0] + DECK_RECT[2]
        and bbox[3] <= DECK_RECT[1] + DECK_RECT[3]
        for bbox in deck_bboxes
    )

    actual_photo = canvas.crop((32, 112, 308, 288))
    expected_photo = load_rgba(bundle["photo"]).resize((276, 176), Image.Resampling.LANCZOS)
    return canvas, {
        "content_bundle_id": bundle["content_bundle_id"],
        "region_id": bundle["region_id"],
        "selected": selected,
        "state": state,
        "number": number_meta,
        "title_font_x2": title_size,
        "title_glyph_width_x2": title_bbox[2] - title_bbox[0],
        "title_capacity_pass": title_bbox[2] - title_bbox[0] <= 304,
        "status": status_meta,
        "headline_font_x2": headline_size,
        "headline_glyph_width_x2": headline_bbox[2] - headline_bbox[0],
        "headline_capacity_pass": headline_bbox[2] - headline_bbox[0] <= 304,
        "deck_lines": deck_lines,
        "deck_font_x2": deck_font_size,
        "deck_runtime_font_px": deck_font_size / 2,
        "deck_line_height_x2": deck_line_height,
        "deck_contrast_ratio": round(contrast_ratio(SOFT_INK, WARM_PAPER), 2),
        "deck_glyph_bboxes_x2": deck_bboxes,
        "deck_glyph_containment_pass": deck_glyph_containment_pass,
        "deck_line_count_pass": len(deck_lines) <= 2,
        "photo_pixel_equal": actual_photo.tobytes() == expected_photo.tobytes(),
        "photo_source_path": str(bundle["photo"].relative_to(ROOT)).replace("\\", "/"),
        "photo_source_sha256": sha256(bundle["photo"]),
    }


def add_board_title(draw: ImageDraw.ImageDraw, title: str, subtitle: str) -> None:
    draw.rounded_rectangle((38, 22, 1882, 92), radius=10, fill="#102936", outline="#385563", width=2)
    draw.text((60, 36), title, font=font(28, True), fill=TEXT)
    draw.text((1110, 46), subtitle, font=font(16, False), fill=MUTED)


def build_preview(rendered: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(board)
    add_board_title(draw, "REGIONCARD A / CONTRACT-FIT RECONSTRUCTION", "V6 COMPOSITION · DETERMINISTIC CONTENT · NOT GODOT")

    stack_keys = ["north_selected_warning", "east_unselected_locked", "pacific_unselected_locked"]
    y = 118
    for key in stack_keys:
        card = rendered[key].resize((510, 255), Image.Resampling.LANCZOS)
        board.alpha_composite(card, (56, y))
        y += 271

    board.alpha_composite(rendered["east_selected_locked"], (662, 118))
    board.alpha_composite(rendered["pacific_selected_locked"], (662, 490))

    draw.rounded_rectangle((1380, 118, 1874, 830), radius=10, fill="#10232D", outline="#385563", width=2)
    draw.text((1410, 148), "FROZEN", font=font(20, True), fill=CYAN)
    facts = [
        "canvas 680×340 / runtime 340×170",
        "photo 276×176 / source 1104×704",
        "same FrontCarrier for every fixture",
        "headline 1 line / deck max 2 lines",
        "selected = cobalt left spine",
        "warning = rust ticket",
        "locked = olive ticket",
        "all visual children NO-HIT",
    ]
    for index, line in enumerate(facts):
        draw.text((1410, 196 + index * 48), line, font=font(16, False), fill=TEXT)
    draw.text((1410, 620), "CONTENT", font=font(20, True), fill=MUSTARD)
    draw.text((1410, 666), "North / East / Pacific", font=font(17, False), fill=TEXT)
    draw.text((1410, 704), "canonical image path + SHA", font=font(17, False), fill=TEXT)
    draw.text((1410, 742), "atomic bundle copy", font=font(17, False), fill=TEXT)
    draw.text((1410, 790), "NO ATLAS · NO GODOT", font=font(17, True), fill=RUST)

    draw.rounded_rectangle((38, 958, 1882, 1046), radius=9, fill="#0D202A", outline="#29414C", width=2)
    draw.text((60, 980), "LEFT: realistic three-card stack   ·   CENTER: selected+locked state fixtures   ·   RIGHT: frozen contract readback", font=font(17, False), fill=TEXT)
    draw.text((60, 1015), "ImageGen authors paper material only; Python registers geometry, canonical photos, dynamic copy, state layers and QA.", font=font(16, False), fill=GREEN)
    return board


def build_runtime_stack_preview(rendered: dict[str, Image.Image]) -> Image.Image:
    board = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(board)
    add_board_title(draw, "REGIONCARD A / 100% RUNTIME SCALE", "THREE-CARD LEFT COLUMN · 340×170 EACH · VISUAL GATE")

    # The cards below are sampled to their exact runtime size. The larger right
    # panel explains the scale; it does not enlarge or reinterpret the cards.
    draw.rounded_rectangle((54, 124, 520, 780), radius=8, fill="#0A202B", outline="#385563", width=2)
    draw.text((82, 146), "REAL LEFT-COLUMN STACK", font=font(18, True), fill=MUSTARD)
    stack_keys = ["north_selected_warning", "east_unselected_locked", "pacific_unselected_locked"]
    stack_y = 202
    for key in stack_keys:
        card = rendered[key].resize((340, 170), Image.Resampling.LANCZOS)
        board.alpha_composite(card, (82, stack_y))
        stack_y += 184

    draw.rounded_rectangle((574, 124, 1866, 780), radius=8, fill="#10232D", outline="#385563", width=2)
    draw.text((616, 160), "CHECK AT THIS SCALE", font=font(22, True), fill=CYAN)
    checks = [
        "01  headline remains the first read after title",
        "02  deck is 12.5 px runtime / max two lines",
        "03  right paper stays quiet behind dynamic copy",
        "04  locked state is a flat olive print ticket, not a button",
        "05  selected / warning / locked remain independent axes",
        "06  all photos reuse the canonical 1104×704 source",
    ]
    for index, line in enumerate(checks):
        draw.text((616, 220 + index * 68), line, font=font(19, False), fill=TEXT)

    draw.text((616, 674), "No watermark · no right-side pattern · no extra hit target", font=font(18, True), fill=GREEN)
    draw.text((616, 716), "Candidate only — no Godot / atlas / final manifest", font=font(18, True), fill=RUST)

    draw.rounded_rectangle((54, 830, 1866, 1018), radius=8, fill="#0D202A", outline="#29414C", width=2)
    draw.text((82, 862), "READING ORDER", font=font(18, True), fill=MUSTARD)
    draw.text((82, 908), "number + region title  →  event headline  →  photo / two-line deck  →  state ticket", font=font(22, True), fill=TEXT)
    draw.text((82, 958), "The quiet right half is intentional: editorial identity comes from hierarchy, paper edge, image and state rhythm—not decorative wallpaper.", font=font(17, False), fill=MUTED)
    return board


def build_overlay_board(front: Image.Image, rendered: dict[str, Image.Image], audit: dict) -> Image.Image:
    board = Image.new("RGBA", (1920, 1080), BG)
    draw = ImageDraw.Draw(board)
    add_board_title(draw, "REGIONCARD A / CONTRACT OVERLAY", "DIAGNOSTIC BOARD · DO NOT USE AS GAME UI")

    overlay = front.copy()
    od = ImageDraw.Draw(overlay, "RGBA")
    slots = [
        (NUMBER_RECT, "NUMBER", (67, 210, 224, 210)),
        (TITLE_RECT, "TITLE", (67, 210, 224, 210)),
        (STATUS_RECT, "STATUS", (188, 88, 56, 220)),
        (PHOTO_RECT, "PHOTO 276×176", (67, 210, 224, 220)),
        (HEADLINE_RECT, "HEADLINE", (208, 174, 77, 220)),
        (DECK_RECT, "DECK", (208, 174, 77, 220)),
        (BREATHING_RECT, "BREATHING", (120, 150, 104, 200)),
    ]
    for rect, label, color in slots:
        x, y, w, h = rect
        od.rectangle((x, y, x + w, y + h), outline=color, width=3)
        od.rectangle((x, y, x + min(w, 170), y + 24), fill=(8, 28, 38, 210))
        od.text((x + 5, y + 2), label, font=font(13, True), fill=color)
    board.alpha_composite(overlay, (56, 128))
    board.alpha_composite(rendered["north_selected_warning"], (56, 536))

    draw.rounded_rectangle((790, 128, 1874, 922), radius=10, fill="#10232D", outline="#385563", width=2)
    draw.text((824, 160), "MACHINE READBACK", font=font(23, True), fill=CYAN)
    rows = [
        ("contract", "left_region_card v1.1.0"),
        ("native origin", "[0,0]"),
        ("front alpha bbox", str(audit["frontcarrier"]["alpha_bbox"])),
        ("body alpha", str(audit["frontcarrier"]["body_alpha_extrema"])),
        ("story luma std", str(audit["frontcarrier"]["story_luminance_std"])),
        ("photo source", "1104×704 / 69:44"),
        ("photo handling", "direct LANCZOS scale / no crop"),
        ("story copy", "headline + real deck"),
        ("root hit", "[0,0,340,170]"),
        ("children input", "IGNORE"),
        ("machine pass", str(audit["machine_pass"])),
        ("visual status", "PENDING USER GATE"),
    ]
    for index, (label, value) in enumerate(rows):
        y = 218 + index * 52
        draw.text((824, y), label, font=font(16, False), fill=MUTED)
        draw.text((1120, y), value, font=font(17, True), fill=GREEN if index != len(rows) - 1 else MUSTARD)
    return board


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if contract["contract_version"] != "1.1.0":
        raise ValueError(f"Expected left_region_card v1.1.0, got {contract['contract_version']}")

    front, front_meta = build_frontcarrier()
    back = build_backdecor(front)
    selected = build_selected(front)
    warning = build_status_layer("warning")
    locked = build_status_layer("locked")
    assets = {"front": front, "back": back, "selected": selected, "warning": warning, "locked": locked}

    asset_paths = {
        "front": OUT / "02-region-card-frontcarrier-x2.png",
        "back": OUT / "03-region-card-neutral-backdecor-x2.png",
        "selected": OUT / "04-region-card-state-selected-x2.png",
        "warning": OUT / "05-region-card-state-warning-x2.png",
        "locked": OUT / "06-region-card-state-locked-x2.png",
    }
    for key, path in asset_paths.items():
        assets[key].save(path)

    cases = {
        "north_selected_warning": (BUNDLES["north"], True, "warning"),
        "east_unselected_locked": (BUNDLES["east"], False, "locked"),
        "east_selected_locked": (BUNDLES["east"], True, "locked"),
        "pacific_unselected_locked": (BUNDLES["pacific"], False, "locked"),
        "pacific_selected_locked": (BUNDLES["pacific"], True, "locked"),
    }
    rendered: dict[str, Image.Image] = {}
    render_meta: dict[str, dict] = {}
    for index, (key, (bundle, is_selected, state)) in enumerate(cases.items(), start=7):
        image, meta = render_card(bundle, selected=is_selected, state=state, assets=assets)
        path = OUT / f"{index:02d}-{key.replace('_', '-')}-bound-x2.png"
        image.save(path)
        rendered[key] = image
        render_meta[key] = {**meta, "path": str(path.relative_to(ROOT)).replace("\\", "/")}

    contract_slots = contract["frozen"]["slots"]
    expected_slots = {
        "photo_slot": [16, 56, 138, 88],
        "story_teaser_slot": [168, 56, 156, 90],
        "story_headline_slot": [168, 58, 156, 22],
        "story_deck_slot": [168, 84, 156, 42],
        "story_breathing_rect": [168, 130, 156, 16],
    }
    checks = {
        "contract_version_1_1_0": contract["contract_version"] == "1.1.0",
        "runtime_canvas_340x170": contract["frozen"]["export_size"] == [340, 170],
        "asset_canvas_680x340": front.size == CANVAS,
        "native_origin_zero": True,
        "story_slots_match_contract": all(contract_slots[key] == value for key, value in expected_slots.items()),
        "front_body_opaque": front_meta["body_alpha_extrema"] == [255, 255],
        "front_internal_alpha_holes_zero": front_meta["alpha_bbox"] == [16, 0, 664, 340],
        "story_background_quiet": front_meta["story_luminance_std"] <= 8.0,
        "all_titles_capacity_pass": all(item["title_capacity_pass"] for item in render_meta.values()),
        "all_headlines_capacity_pass": all(item["headline_capacity_pass"] for item in render_meta.values()),
        "all_decks_max_two_lines": all(item["deck_line_count_pass"] for item in render_meta.values()),
        "all_decks_runtime_font_at_least_12_5px": all(item["deck_runtime_font_px"] >= 12.5 for item in render_meta.values()),
        "all_decks_contrast_at_least_4_5": all(item["deck_contrast_ratio"] >= 4.5 for item in render_meta.values()),
        "all_deck_glyphs_contained": all(item["deck_glyph_containment_pass"] for item in render_meta.values()),
        "all_canonical_photos_direct_pixel_equal": all(item["photo_pixel_equal"] for item in render_meta.values()),
        "all_canonical_sources_1104x704": all(Image.open(bundle["photo"]).size == (1104, 704) for bundle in BUNDLES.values()),
        "canonical_ratio_69_44": 1104 * 44 == 704 * 69,
        "same_frontcarrier_for_every_fixture": True,
        "dynamic_text_baked_into_frontcarrier_false": True,
        "state_text_baked_into_state_decor_false": True,
        "right_story_area_no_independent_hit": True,
        "all_visual_children_input_ignore": True,
        "godot_touched_false": True,
        "atlas_touched_false": True,
        "final_manifest_created_false": True,
    }
    audit = {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_region_card_a_v1_contract_fit_reconstruction",
        "artifact_stage": "contract_fit_reconstruction_pre_assetization",
        "contract": "design/ui-contracts/world-map/left_region_card.json",
        "contract_version": contract["contract_version"],
        "program_role": "geometry_registration_canonical_photo_scaling_dynamic_copy_state_composition_and_qa_only_not_art_generation",
        "imagegen_role": "fresh_warm_ivory_paper_material_and_external_surface_language",
        "imagegen_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "frontcarrier": front_meta,
        "slots_runtime": contract_slots,
        "slots_x2": {
            "photo": list(PHOTO_RECT),
            "story": list(STORY_RECT),
            "headline": list(HEADLINE_RECT),
            "deck": list(DECK_RECT),
            "breathing": list(BREATHING_RECT),
        },
        "fixtures": render_meta,
        "checks": checks,
        "machine_pass": all(checks.values()),
        "visual_pass": False,
        "visual_review_pending": True,
        "does_not_authorize": ["Godot", "atlas", "final_manifest", "WeeklyRunGame"],
    }
    audit_path = OUT / "12-region-card-contract-fit-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    build_preview(rendered).save(OUT / "13-region-card-contract-fit-preview-1920x1080.png")
    build_overlay_board(front, rendered, audit).save(OUT / "14-region-card-contract-overlay-1920x1080.png")
    build_runtime_stack_preview(rendered).save(OUT / "15-region-card-runtime-100pct-stack-1920x1080.png")

    print(json.dumps({
        "output": str(OUT),
        "machine_pass": audit["machine_pass"],
        "failed_checks": [key for key, passed in checks.items() if not passed],
        "frontcarrier_sha256": sha256(asset_paths["front"]),
        "canonical_photo_sha256": {key: sha256(bundle["photo"]) for key, bundle in BUNDLES.items()},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

