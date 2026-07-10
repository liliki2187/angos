from __future__ import annotations

from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont


BASE = Path(r"D:\angos\docs\screenshots\2026-06-24-world-map-benchmark-landing")
REF = Path(r"D:\angos\.codex-remote-attachments\019ef3f7-be2f-70d3-ae57-7df7fa181048\285fb7d4-37f0-4a98-86f4-c1652013a1d1\1-Photo-1.jpg")

OUT_AUDIT = BASE / "359-world-map-wmw-v0-8-3-right-dossier-cta-source-audit.png"
OUT_CONTRACT = BASE / "360-world-map-wmw-v0-8-3-right-dossier-cta-contract.png"
OUT_REINSERT_QA = BASE / "361-world-map-wmw-v0-8-3-right-dossier-cta-reinsert-qa.png"
OUT_CROPS = BASE / "362-world-map-wmw-v0-8-3-right-dossier-cta-crops.png"
OUT_MANIFEST = BASE / "363-world-map-wmw-v0-8-3-right-dossier-cta-manifest.json"

FONT_BOLD = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]
FONT_REGULAR = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]


SOURCE = {
    "dossier_page": [934, 35, 1251, 548],
    "photo_slot": [956, 133, 1225, 307],
    "header_title_slot": [1006, 65, 1165, 88],
    "status_stamp": [1182, 65, 1236, 118],
    "meta_slot": [956, 319, 1115, 339],
    "cta_rows": [
        [950, 353, 1233, 401],
        [950, 408, 1232, 455],
        [950, 461, 1232, 510],
    ],
}

CONTRACT = {
    "dossier_class_id": "right_dossier_page",
    "dossier_export_size": [320, 520],
    "dossier_position": [932, 30],
    "content_slots": {
        "header_icon": [24, 38, 36, 36],
        "title_slot": [82, 42, 160, 34],
        "status_stamp": [246, 34, 58, 58],
        "photo_slot": [22, 98, 276, 176],
        "meta_slot": [22, 288, 196, 22],
        "action_stack": [16, 318, 284, 160],
    },
    "action_lane_class_id": "right_action_lane",
    "action_lane_export_size": [284, 50],
    "action_lane_gap": 5,
    "action_lane_slots": {
        "left_icon_zone": [12, 8, 34, 34],
        "label_plate": [62, 9, 170, 32],
        "right_action_badge": [238, 5, 42, 40],
        "hit_rect": [0, 0, 284, 50],
    },
    "states": ["enter", "info", "warning"],
}


def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


FB = font(FONT_BOLD, 24)
FM = font(FONT_BOLD, 18)
FR = font(FONT_REGULAR, 14)
FS = font(FONT_REGULAR, 11)
FCN = font(FONT_BOLD, 18)


def size(rect: list[int]) -> tuple[int, int]:
    return rect[2] - rect[0], rect[3] - rect[1]


def draw_text_bg(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill=(236, 238, 214), font_obj=None) -> None:
    font_obj = font_obj or FS
    x, y = xy
    bbox = draw.textbbox((x, y), text, font=font_obj)
    draw.rectangle([bbox[0] - 5, bbox[1] - 3, bbox[2] + 5, bbox[3] + 3], fill=(7, 14, 16, 218))
    draw.text((x, y), text, font=font_obj, fill=fill)


def rect_abs(local: list[int], origin: list[int]) -> list[int]:
    x, y = origin
    return [x + local[0], y + local[1], x + local[0] + local[2], y + local[1] + local[3]]


def create_audit() -> None:
    src = Image.open(REF).convert("RGB")
    canvas = src.copy()
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rectangle(SOURCE["dossier_page"], outline=(112, 238, 142, 255), width=3)
    draw_text_bg(draw, (SOURCE["dossier_page"][0] + 8, SOURCE["dossier_page"][1] + 8), "right_dossier_page source 317x513")
    draw.rectangle(SOURCE["photo_slot"], outline=(92, 218, 255, 255), width=2)
    draw.rectangle(SOURCE["header_title_slot"], outline=(255, 219, 92, 255), width=2)
    draw.rectangle(SOURCE["status_stamp"], outline=(255, 110, 110, 255), width=2)
    draw.rectangle(SOURCE["meta_slot"], outline=(180, 255, 180, 255), width=2)

    for i, rect in enumerate(SOURCE["cta_rows"], 1):
        w, h = size(rect)
        draw.rectangle(rect, outline=(255, 124, 100, 255), width=3)
        draw_text_bg(draw, (rect[0] + 8, rect[1] + 4), f"CTA {i}: {w}x{h}", fill=(255, 216, 204))

    panel = [30, 560, 850, 705]
    draw.rectangle(panel, fill=(7, 18, 20, 235), outline=(128, 154, 132, 255), width=1)
    draw.text((45, 576), "v0.8.3 Right Dossier / CTA Source Audit", font=FB, fill=(244, 240, 214))
    lines = [
        "Source is visually close, but not production-exact:",
        "dossier page approx 317x513; normalize to a class contract before clean sprites.",
        "CTA rows measure 283x48 / 282x47 / 282x49; normalize to one 284x50 action lane.",
        "Decoration tabs, clips, paper shadow can vary outside the functional contract; content planes cannot.",
    ]
    for idx, line in enumerate(lines):
        draw.text((45, 610 + idx * 22), line, font=FR, fill=(226, 230, 205))

    canvas.save(OUT_AUDIT)


def draw_dossier_contract(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    w, h = CONTRACT["dossier_export_size"]
    draw.rectangle([x + 8, y + 10, x + w + 8, y + h + 10], fill=(0, 0, 0, 120))
    draw.rectangle([x, y, x + w, y + h], fill=(218, 206, 178, 245), outline=(240, 232, 202, 255), width=2)
    draw.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], outline=(96, 88, 72, 150), width=1)

    # Decorative back pages and tabs: allowed to sit behind, not functional.
    draw.rectangle([x + w + 3, y + 22, x + w + 16, y + h - 20], fill=(94, 112, 52, 210))
    draw.rectangle([x + w + 10, y + 335, x + w + 24, y + 435], fill=(51, 118, 130, 210))
    draw.rectangle([x + w + 17, y + 400, x + w + 32, y + 490], fill=(145, 63, 42, 210))

    slots = CONTRACT["content_slots"]
    colors = {
        "header_icon": (148, 234, 180, 255),
        "title_slot": (255, 219, 92, 255),
        "status_stamp": (255, 110, 110, 255),
        "photo_slot": (92, 218, 255, 255),
        "meta_slot": (180, 255, 180, 255),
        "action_stack": (255, 175, 88, 255),
    }
    labels = {
        "header_icon": "icon",
        "title_slot": "title",
        "status_stamp": "stamp",
        "photo_slot": "photo slot 276x176",
        "meta_slot": "meta",
        "action_stack": "action stack",
    }
    for key, local in slots.items():
        rx = [x + local[0], y + local[1], x + local[0] + local[2], y + local[1] + local[3]]
        fill = (*colors[key][:3], 26)
        draw.rectangle(rx, fill=fill, outline=colors[key], width=2)
        draw.text((rx[0] + 5, rx[1] + 4), labels[key], font=FS, fill=colors[key])

    # Action lanes inside stack.
    sx, sy, _, _ = slots["action_stack"]
    lane_w, lane_h = CONTRACT["action_lane_export_size"]
    gap = CONTRACT["action_lane_gap"]
    lane_cols = [(75, 95, 48), (42, 96, 108), (144, 65, 42)]
    lane_labels = ["enter", "info", "warning"]
    for i, (col, lab) in enumerate(zip(lane_cols, lane_labels)):
        ly = y + sy + i * (lane_h + gap)
        lx = x + sx
        draw.rectangle([lx, ly, lx + lane_w, ly + lane_h], fill=(*col, 230), outline=(238, 228, 190, 255), width=2)
        lslots = CONTRACT["action_lane_slots"]
        for slot_name, rect in lslots.items():
            if slot_name == "hit_rect":
                continue
            rr = [lx + rect[0], ly + rect[1], lx + rect[0] + rect[2], ly + rect[1] + rect[3]]
            outline = {
                "left_icon_zone": (150, 255, 185, 255),
                "label_plate": (255, 225, 98, 255),
                "right_action_badge": (255, 116, 116, 255),
            }[slot_name]
            draw.rectangle(rr, outline=outline, width=2)
        draw.text((lx + 70, ly + 15), lab, font=FR, fill=(238, 230, 200))


def create_contract() -> None:
    canvas = Image.new("RGB", (1280, 840), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 26), "v0.8.3 Right Dossier + CTA Class Contract Candidate", font=FB, fill=(244, 240, 214))
    draw.text((32, 62), "Goal: lock right-side detail paper and three CTA rows before clean-sprite work.", font=FR, fill=(220, 230, 205))

    draw_dossier_contract(draw, 80, 115)

    x0, y0 = 520, 130
    draw.rectangle([x0, y0, x0 + 680, y0 + 250], fill=(14, 34, 34), outline=(106, 150, 130), width=1)
    draw.text((x0 + 18, y0 + 18), "A. Fixed Classes", font=FM, fill=(240, 230, 190))
    rows = [
        ("right_dossier_page", "320 x 520"),
        ("photo_slot", "276 x 176, fixed"),
        ("title_slot", "160 x 34, fixed"),
        ("status_stamp", "58 x 58, fixed"),
        ("right_action_lane", "284 x 50, three states"),
        ("lane label_plate", "170 x 32, fixed"),
        ("lane hit_rect", "full 284 x 50"),
    ]
    for i, (k, v) in enumerate(rows):
        yy = y0 + 58 + i * 26
        draw.text((x0 + 18, yy), k, font=FS, fill=(122, 214, 188))
        draw.text((x0 + 190, yy), v, font=FS, fill=(232, 232, 210))

    x1, y1 = 520, 420
    draw.rectangle([x1, y1, x1 + 680, y1 + 260], fill=(32, 18, 20), outline=(214, 92, 78), width=1)
    draw.text((x1 + 18, y1 + 18), "B. One-Vote Fails", font=FM, fill=(255, 204, 190))
    fails = [
        "CTA rows use different heights by state",
        "right action badge shifts between green / blue / red rows",
        "label plate becomes narrower for warning text",
        "paper page tilts while runtime text remains horizontal",
        "decorative tabs or clip force content rects to move",
        "photo slot changes ratio without re-authoring image content",
    ]
    for i, line in enumerate(fails):
        draw.text((x1 + 18, y1 + 58 + i * 26), f"- {line}", font=FS, fill=(244, 224, 208))

    canvas.save(OUT_CONTRACT)


def create_reinsert_qa() -> None:
    src = Image.open(REF).convert("RGB")
    canvas = src.copy()
    draw = ImageDraw.Draw(canvas, "RGBA")
    origin = CONTRACT["dossier_position"]
    dw, dh = CONTRACT["dossier_export_size"]
    drect = [origin[0], origin[1], origin[0] + dw, origin[1] + dh]
    draw.rectangle(drect, outline=(102, 246, 142, 255), width=3)
    draw.text((origin[0] + 6, origin[1] + 5), "right_dossier_page 320x520", font=FS, fill=(170, 255, 190))

    for key, rect in CONTRACT["content_slots"].items():
        rr = rect_abs(rect, origin)
        color = {
            "header_icon": (148, 234, 180, 255),
            "title_slot": (255, 219, 92, 255),
            "status_stamp": (255, 110, 110, 255),
            "photo_slot": (92, 218, 255, 255),
            "meta_slot": (180, 255, 180, 255),
            "action_stack": (255, 175, 88, 255),
        }[key]
        draw.rectangle(rr, outline=color, width=2)
        draw.text((rr[0] + 4, rr[1] + 3), key, font=FS, fill=color)

    sx, sy, _, _ = CONTRACT["content_slots"]["action_stack"]
    lane_w, lane_h = CONTRACT["action_lane_export_size"]
    gap = CONTRACT["action_lane_gap"]
    lslots = CONTRACT["action_lane_slots"]
    for i in range(3):
        lx = origin[0] + sx
        ly = origin[1] + sy + i * (lane_h + gap)
        draw.rectangle([lx, ly, lx + lane_w, ly + lane_h], outline=(255, 124, 100, 255), width=3)
        for slot_name, rect in lslots.items():
            if slot_name == "hit_rect":
                continue
            rr = [lx + rect[0], ly + rect[1], lx + rect[0] + rect[2], ly + rect[1] + rect[3]]
            color = {
                "left_icon_zone": (150, 255, 185, 255),
                "label_plate": (255, 225, 98, 255),
                "right_action_badge": (255, 116, 116, 255),
            }[slot_name]
            draw.rectangle(rr, outline=color, width=2)
    draw.rectangle([280, 28, 820, 88], fill=(7, 18, 20, 220), outline=(132, 168, 132, 255), width=1)
    draw.text((292, 40), "v0.8.3 QA: right dossier 320x520 + CTA 284x50", font=FM, fill=(244, 240, 214))
    draw.text((292, 66), "green=dossier / orange=CTA rows / yellow=label / red=button badge", font=FS, fill=(220, 230, 205))
    canvas.save(OUT_REINSERT_QA)


def create_crops() -> None:
    qa = Image.open(OUT_REINSERT_QA).convert("RGB")
    canvas = Image.new("RGB", (1280, 760), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 24), "v0.8.3 Right Dossier / CTA 100% Crops", font=FB, fill=(244, 240, 214))
    crops = [
        ("right page", (920, 20, 1278, 570), (32, 72)),
        ("cta stack", (930, 330, 1260, 525), (470, 72)),
        ("header", (930, 40, 1260, 132), (470, 320)),
    ]
    for label, box, pos in crops:
        crop = qa.crop(box)
        canvas.paste(crop, pos)
        draw.text((pos[0], pos[1] + crop.height + 8), label, font=FR, fill=(226, 230, 205))
    canvas.save(OUT_CROPS)


def write_manifest() -> None:
    source_measurements = {
        "dossier_page": {
            "rect": SOURCE["dossier_page"],
            "size": list(size(SOURCE["dossier_page"])),
        },
        "cta_rows": [
            {
                "rect": rect,
                "size": list(size(rect)),
            }
            for rect in SOURCE["cta_rows"]
        ],
    }
    data = {
        "artifact": "WMW v0.8.3 right dossier CTA class contract candidate",
        "date": "2026-07-08",
        "artifact_type": "component_class_contract_candidate / right_dossier_page / right_action_lane / not final art / not atlas",
        "source_reference": str(REF),
        "outputs": {
            "audit": str(OUT_AUDIT),
            "contract": str(OUT_CONTRACT),
            "reinsert_qa": str(OUT_REINSERT_QA),
            "crops": str(OUT_CROPS),
            "manifest": str(OUT_MANIFEST),
        },
        "source_measurements": source_measurements,
        "contract": CONTRACT,
        "decision": "Normalize the right dossier to 320x520 and the three CTA rows to one 284x50 right_action_lane class before clean-sprite work.",
        "next_gate": "User review, then produce no-text clean-sprite brief for right_dossier_page and right_action_lane.",
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    OUT_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    create_audit()
    create_contract()
    create_reinsert_qa()
    create_crops()
    write_manifest()
    print(OUT_AUDIT)
    print(OUT_CONTRACT)
    print(OUT_REINSERT_QA)
    print(OUT_CROPS)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
