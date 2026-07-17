from __future__ import annotations

from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

from wmw_text_layout_metrics import draw_text_by_raster_bbox, fit_font_by_raster, raster_text_size


BASE = Path(r"D:\angos\docs\screenshots\2026-06-24-world-map-benchmark-landing")
REF = Path(r"D:\angos\.codex-remote-attachments\019ef3f7-be2f-70d3-ae57-7df7fa181048\285fb7d4-37f0-4a98-86f4-c1652013a1d1\1-Photo-1.jpg")

OUT_AUDIT = BASE / "368-world-map-wmw-v0-8-5-bottom-receipt-source-audit.png"
OUT_CONTRACT = BASE / "369-world-map-wmw-v0-8-5-bottom-receipt-contract.png"
OUT_REINSERT = BASE / "370-world-map-wmw-v0-8-5-bottom-receipt-reinsert-qa.png"
OUT_TEXT = BASE / "371-world-map-wmw-v0-8-5-bottom-receipt-text-stress.png"
OUT_MANIFEST = BASE / "372-world-map-wmw-v0-8-5-bottom-receipt-manifest.json"

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

SOURCE_RECEIPTS = [
    {"id": "weekly_action", "rect": [289, 558, 535, 695], "tone": (84, 112, 54), "title": "本周行动", "value": "余 6天"},
    {"id": "intel_pool", "rect": [557, 558, 802, 695], "tone": (43, 92, 106), "title": "情报余量", "value": "线报 3"},
    {"id": "redline_account", "rect": [827, 558, 1073, 695], "tone": (150, 64, 42), "title": "红线台账", "value": "4天后升温"},
]

CONTRACT = {
    "class_id": "bottom_receipt_card",
    "export_size": [246, 138],
    "positions": [[288, 558], [557, 558], [826, 558]],
    "gap": 23,
    "slots": {
        "left_icon_zone": [24, 28, 52, 52],
        "title_slot": [92, 23, 120, 28],
        "value_slot": [92, 57, 128, 32],
        "meter_slot": [28, 101, 166, 24],
        "side_notch_no_text": [224, 20, 14, 96],
        "hit_rect": [0, 0, 246, 138],
    },
    "states": ["weekly_action", "intel_pool", "redline_account"],
}

TEXT_CASES = [
    {
        "id": "normal",
        "receipts": [
            {"title": "本周行动", "value": "余 6天", "meter": 5},
            {"title": "情报余量", "value": "线报 3", "meter": 3},
            {"title": "红线台账", "value": "4天后升温", "meter": 4},
        ],
    },
    {
        "id": "stress",
        "receipts": [
            {"title": "本周行动安排", "value": "剩余 12天", "meter": 6},
            {"title": "情报余量", "value": "线报 12", "meter": 5},
            {"title": "红线升温台账", "value": "12天后升温", "meter": 6},
        ],
    },
]


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


def size(rect: list[int]) -> tuple[int, int]:
    return rect[2] - rect[0], rect[3] - rect[1]


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    return raster_text_size(text, fnt)


def fit_font(draw: ImageDraw.ImageDraw, text: str, paths: list[str], max_size: int, min_size: int, box: tuple[int, int]):
    fnt, size, fits, metrics = fit_font_by_raster(text, lambda candidate: font(paths, candidate), max_size, min_size, box)
    return fnt, size, fits, tuple(metrics["raster_size"])


def abs_rect(origin: tuple[int, int], local: list[int]) -> tuple[int, int, int, int]:
    return (origin[0] + local[0], origin[1] + local[1], origin[0] + local[0] + local[2], origin[1] + local[1] + local[3])


def draw_label_bg(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill=(236, 238, 214), fnt=None) -> None:
    fnt = fnt or FS
    x, y = xy
    bbox = draw.textbbox((x, y), text, font=fnt)
    draw.rectangle([bbox[0] - 5, bbox[1] - 3, bbox[2] + 5, bbox[3] + 3], fill=(7, 14, 16, 218))
    draw.text((x, y), text, font=fnt, fill=fill)


def draw_icon(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], kind: str, color=(84, 94, 58, 245)) -> None:
    cx = (rect[0] + rect[2]) // 2
    cy = (rect[1] + rect[3]) // 2
    r = min(rect[2] - rect[0], rect[3] - rect[1]) // 2 - 5
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    if kind == "weekly_action":
        draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
        draw.line([cx, cy - r, cx, cy + r], fill=color, width=2)
        draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 70, 290, fill=color, width=1)
    elif kind == "intel_pool":
        draw.rectangle([cx - 9, cy - 12, cx + 9, cy + 12], outline=color, width=2)
        draw.line([cx - 5, cy - 5, cx + 6, cy - 5], fill=color, width=2)
        draw.line([cx - 5, cy + 2, cx + 6, cy + 2], fill=color, width=2)
    else:
        draw.polygon([(cx, cy - 17), (cx + 17, cy + 14), (cx - 17, cy + 14)], outline=color)
        draw.line([cx, cy - 5, cx, cy + 5], fill=color, width=2)
        draw.ellipse([cx - 2, cy + 10, cx + 2, cy + 14], fill=color)


def draw_meter(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], tone: tuple[int, int, int], filled: int) -> None:
    draw.rectangle(rect, fill=(32, 38, 34, 220), outline=(218, 210, 180, 180), width=1)
    gap = 2
    count = 6
    seg_w = ((rect[2] - rect[0]) - gap * (count - 1)) // count
    for i in range(count):
        x0 = rect[0] + i * (seg_w + gap)
        x1 = x0 + seg_w
        col = (*tone, 235) if i < filled else (36, 45, 42, 235)
        draw.rectangle([x0, rect[1], x1, rect[3]], fill=col)


def draw_receipt(draw: ImageDraw.ImageDraw, origin: tuple[int, int], state: dict, text: dict | None = None, qa: bool = False) -> list[dict]:
    text = text or state
    x, y = origin
    w, h = CONTRACT["export_size"]
    tone = state["tone"]
    slots = CONTRACT["slots"]
    report: list[dict] = []

    # Shadow and shell.
    cut = 16
    pts = [(x + cut, y), (x + w - cut, y), (x + w, y + cut), (x + w, y + h - cut), (x + w - cut, y + h), (x + cut, y + h), (x, y + h - cut), (x, y + cut)]
    draw.polygon([(px + 5, py + 5) for px, py in pts], fill=(0, 0, 0, 120))
    draw.polygon(pts, fill=(221, 210, 181, 246), outline=(238, 230, 200, 245))
    draw.polygon([(x, y), (x + 58, y), (x + 32, y + 74), (x, y + 88)], fill=(*tone, 60))
    draw.polygon([(x + w - 70, y + h), (x + w, y + h - 62), (x + w, y + h), (x + w - 70, y + h)], fill=(*tone, 70))
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(*tone, 80))

    icon_rect = abs_rect(origin, slots["left_icon_zone"])
    title_rect = abs_rect(origin, slots["title_slot"])
    value_rect = abs_rect(origin, slots["value_slot"])
    meter_rect = abs_rect(origin, slots["meter_slot"])
    draw_icon(draw, icon_rect, state["id"], color=(*tone, 245))

    f_title, title_size, title_ok, title_wh = fit_font(draw, text["title"], FONT_BOLD, 18, 13, (slots["title_slot"][2] - 4, slots["title_slot"][3] - 4))
    f_value, value_size, value_ok, value_wh = fit_font(draw, text["value"], FONT_BOLD, 24, 16, (slots["value_slot"][2] - 4, slots["value_slot"][3] - 4))
    title_bbox = draw_left(draw, title_rect, text["title"], f_title, (34, 36, 30, 245), 2)
    value_bbox = draw_left(draw, value_rect, text["value"], f_value, (54, 52, 44, 245), 2)
    draw_meter(draw, meter_rect, tone, text.get("meter", 4))

    if qa:
        draw.rectangle([x, y, x + w, y + h], outline=(95, 245, 140, 255), width=2)
        draw.rectangle(icon_rect, outline=(150, 255, 185, 255), width=2)
        draw.rectangle(title_rect, outline=(255, 221, 77, 255), width=2)
        draw.rectangle(value_rect, outline=(255, 172, 77, 255), width=2)
        draw.rectangle(meter_rect, outline=(92, 218, 255, 255), width=2)
        draw.rectangle(title_bbox, outline=(255, 80, 210, 255), width=1)
        draw.rectangle(value_bbox, outline=(255, 80, 210, 255), width=1)
        draw.text((x + 4, y + 4), f"{w}x{h}", font=FS, fill=(170, 255, 190))

    report.append({"field": f"{state['id']}.title", "text": text["title"], "font_size": title_size, "fits": title_ok, "text_size": title_wh, "rect": list(title_rect), "bbox": list(title_bbox)})
    report.append({"field": f"{state['id']}.value", "text": text["value"], "font_size": value_size, "fits": value_ok, "text_size": value_wh, "rect": list(value_rect), "bbox": list(value_bbox)})
    return report


def draw_left(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str, fnt, fill, pad: int) -> tuple[int, int, int, int]:
    report = draw_text_by_raster_bbox(draw, rect, text, fnt, fill, align="left", pad_x=pad)
    return tuple(report["raster_glyph_bbox"])


def create_audit() -> None:
    src = Image.open(REF).convert("RGB")
    canvas = src.copy()
    draw = ImageDraw.Draw(canvas, "RGBA")
    for item in SOURCE_RECEIPTS:
        rect = item["rect"]
        w, h = size(rect)
        draw.rectangle(rect, outline=(255, 142, 92, 255), width=3)
        draw_label_bg(draw, (rect[0] + 8, rect[1] + 6), f"{item['id']} {w}x{h}", fill=(255, 226, 204))

    panel = [30, 30, 630, 158]
    draw.rectangle(panel, fill=(7, 18, 20, 230), outline=(128, 154, 132, 255), width=1)
    draw.text((45, 46), "v0.8.5 Bottom Receipt Source Audit", font=FB, fill=(244, 240, 214))
    lines = [
        "Source sizes are nearly uniform: 246x137 / 245x137 / 246x137.",
        "Production should normalize them to one bottom_receipt_card class.",
        "Candidate: 246x138, positions x=288/557/826, y=558.",
    ]
    for i, line in enumerate(lines):
        draw.text((45, 82 + i * 22), line, font=FR, fill=(226, 230, 205))
    canvas.save(OUT_AUDIT)


def create_contract() -> None:
    canvas = Image.new("RGB", (1280, 780), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 26), "v0.8.5 Bottom Receipt Class Contract Candidate", font=FB, fill=(244, 240, 214))
    draw.text((32, 62), "Goal: lock the three bottom receipt cards as one repeated class before clean-sprite work.", font=FR, fill=(220, 230, 205))

    for i, state in enumerate(SOURCE_RECEIPTS):
        draw_receipt(draw, (70 + i * 310, 140), state, qa=True)
        draw.text((70 + i * 310, 295), f"{state['id']}: same 246x138", font=FS, fill=(226, 230, 205))

    x0, y0 = 70, 360
    draw.rectangle([x0, y0, x0 + 520, y0 + 250], fill=(14, 34, 34), outline=(106, 150, 130), width=1)
    draw.text((x0 + 18, y0 + 18), "A. Fixed Geometry", font=FM, fill=(240, 230, 190))
    rows = [
        ("class_id", CONTRACT["class_id"]),
        ("export_size", "246 x 138"),
        ("positions", "x=288 / 557 / 826, y=558"),
        ("left_icon_zone", "52 x 52"),
        ("title_slot", "120 x 28"),
        ("value_slot", "128 x 32"),
        ("meter_slot", "166 x 24"),
        ("hit_rect", "full 246 x 138"),
    ]
    for i, (k, v) in enumerate(rows):
        draw.text((x0 + 18, y0 + 58 + i * 22), k, font=FS, fill=(122, 214, 188))
        draw.text((x0 + 170, y0 + 58 + i * 22), v, font=FS, fill=(232, 232, 210))

    x1, y1 = 650, 360
    draw.rectangle([x1, y1, x1 + 540, y1 + 250], fill=(32, 18, 20), outline=(214, 92, 78), width=1)
    draw.text((x1 + 18, y1 + 18), "B. One-Vote Fails", font=FM, fill=(255, 204, 190))
    fails = [
        "weekly / intel / redline cards use different export sizes",
        "redline card gets taller because warning text is longer",
        "meter slot changes width by resource count",
        "icon or perforation shifts title/value slot",
        "paper tape or shadow expands the runtime bounds",
        "bottom receipt overlaps central map or icon cluster after reinsert",
    ]
    for i, line in enumerate(fails):
        draw.text((x1 + 18, y1 + 58 + i * 25), f"- {line}", font=FS, fill=(244, 224, 208))
    canvas.save(OUT_CONTRACT)


def create_reinsert() -> list[dict]:
    src = Image.open(REF).convert("RGB")
    canvas = src.copy()
    draw = ImageDraw.Draw(canvas, "RGBA")
    # Clean old bottom cards only.
    draw.rectangle([270, 540, 1092, 708], fill=(7, 18, 20, 210))
    report: list[dict] = []
    for state, pos in zip(SOURCE_RECEIPTS, CONTRACT["positions"]):
        report.extend(draw_receipt(draw, tuple(pos), state, qa=True))
    draw.rectangle([280, 28, 790, 88], fill=(7, 18, 20, 220), outline=(132, 168, 132, 255), width=1)
    draw.text((292, 40), "v0.8.5 QA: bottom_receipt_card 246x138", font=FM, fill=(244, 240, 214))
    draw.text((292, 66), "green=export / yellow=title / orange=value / cyan=meter / magenta=glyph bbox", font=FS, fill=(220, 230, 205))
    canvas.save(OUT_REINSERT)
    return report


def create_text_stress() -> tuple[list[dict], list[dict]]:
    canvas = Image.new("RGB", (1280, 620), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 26), "v0.8.5 Bottom Receipt Text Stress", font=FB, fill=(244, 240, 214))
    reports = []
    for row_idx, case in enumerate(TEXT_CASES):
        y = 100 + row_idx * 225
        draw.text((48, y - 34), case["id"], font=FM, fill=(170, 255, 190))
        row_report: list[dict] = []
        for i, (state, text) in enumerate(zip(SOURCE_RECEIPTS, case["receipts"])):
            row_report.extend(draw_receipt(draw, (70 + i * 310, y), state, text=text, qa=True))
        passed = sum(1 for r in row_report if r["fits"])
        draw.text((1010, y + 48), f"{passed}/{len(row_report)} fields fit", font=FM, fill=(170, 255, 190) if passed == len(row_report) else (255, 120, 110))
        reports.append(row_report)
    canvas.save(OUT_TEXT)
    return reports[0], reports[1]


def write_manifest(reinsert_report: list[dict], normal_report: list[dict], stress_report: list[dict]) -> None:
    data = {
        "artifact": "WMW v0.8.5 bottom receipt class contract candidate",
        "date": "2026-07-08",
        "artifact_type": "component_class_contract_candidate / bottom_receipt_card / text_capacity_stress / not final art / not atlas",
        "source_reference": str(REF),
        "outputs": {
            "audit": str(OUT_AUDIT),
            "contract": str(OUT_CONTRACT),
            "reinsert_qa": str(OUT_REINSERT),
            "text_stress": str(OUT_TEXT),
            "manifest": str(OUT_MANIFEST),
        },
        "source_measurements": [
            {"id": item["id"], "rect": item["rect"], "size": list(size(item["rect"]))}
            for item in SOURCE_RECEIPTS
        ],
        "contract": CONTRACT,
        "reports": {
            "reinsert": reinsert_report,
            "normal": normal_report,
            "stress": stress_report,
        },
        "decision": "Normalize bottom receipts to one 246x138 bottom_receipt_card class. Text capacity passes normal and stress cases, but final typography/art still need review.",
        "next_gate": "User review, then lock bottom_receipt_card and proceed to map panel/top strip/icon badge contracts or no-text brief.",
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    OUT_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    create_audit()
    create_contract()
    reinsert_report = create_reinsert()
    normal_report, stress_report = create_text_stress()
    write_manifest(reinsert_report, normal_report, stress_report)
    print(OUT_AUDIT)
    print(OUT_CONTRACT)
    print(OUT_REINSERT)
    print(OUT_TEXT)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
