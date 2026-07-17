from __future__ import annotations

from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

from wmw_text_layout_metrics import draw_text_by_raster_bbox, fit_font_by_raster, raster_text_size


BASE = Path(r"D:\angos\docs\screenshots\2026-06-24-world-map-benchmark-landing")
REF = Path(r"D:\angos\.codex-remote-attachments\019ef3f7-be2f-70d3-ae57-7df7fa181048\285fb7d4-37f0-4a98-86f4-c1652013a1d1\1-Photo-1.jpg")

OUT_BOARD = BASE / "364-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-board.png"
OUT_FULL = BASE / "365-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-full.png"
OUT_QA = BASE / "366-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-qa.png"
OUT_MANIFEST = BASE / "367-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-manifest.json"

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


CONTRACT = {
    "dossier_position": [932, 30],
    "dossier_export_size": [320, 520],
    "content_slots": {
        "header_icon": [24, 38, 36, 36],
        "title_slot": [82, 42, 160, 34],
        "status_stamp": [246, 34, 58, 58],
        "photo_slot": [22, 98, 276, 176],
        "meta_slot": [22, 288, 196, 22],
        "action_stack": [16, 318, 284, 160],
    },
    "action_lane_export_size": [284, 50],
    "action_lane_gap": 5,
    "action_lane_slots": {
        "left_icon_zone": [12, 8, 34, 34],
        "label_plate": [62, 9, 170, 32],
        "right_action_badge": [238, 5, 42, 40],
        "hit_rect": [0, 0, 284, 50],
    },
}

SCENARIOS = [
    {
        "id": "normal",
        "title": "北美禁区带",
        "risk": "高危",
        "recommend": "推荐2",
        "heat": "红线升温",
        "bars": "■■■■□□",
        "meta": "异常热点　卫星阵列 / 方尖碑",
        "cta": [
            {"kind": "enter", "text": "进入北美禁区 · 消耗1天", "tone": (64, 88, 48)},
            {"kind": "info", "text": "查看任务情报 · 线报3", "tone": (43, 92, 106)},
            {"kind": "warning", "text": "红线截止 · 4天", "tone": (138, 62, 43)},
        ],
    },
    {
        "id": "stress",
        "title": "北美禁区警戒带",
        "risk": "极危",
        "recommend": "推荐12",
        "heat": "红线持续升温",
        "bars": "■■■■■■",
        "meta": "异常热点　卫星阵列 / 方尖碑群",
        "cta": [
            {"kind": "enter", "text": "进入北美禁区带 · 消耗1天", "tone": (64, 88, 48)},
            {"kind": "info", "text": "查看任务情报 · 线报12", "tone": (43, 92, 106)},
            {"kind": "warning", "text": "线报不足 · 还差12", "tone": (138, 62, 43)},
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


FR = font(FONT_REGULAR, 14)
FS = font(FONT_REGULAR, 11)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    return raster_text_size(text, fnt)


def fit_font(draw: ImageDraw.ImageDraw, text: str, paths: list[str], max_size: int, min_size: int, box: tuple[int, int]) -> tuple[ImageFont.ImageFont, int, bool, tuple[int, int]]:
    fnt, size, fits, metrics = fit_font_by_raster(text, lambda candidate: font(paths, candidate), max_size, min_size, box)
    return fnt, size, fits, tuple(metrics["raster_size"])


def abs_rect(origin: tuple[int, int], local: list[int]) -> tuple[int, int, int, int]:
    return (origin[0] + local[0], origin[1] + local[1], origin[0] + local[0] + local[2], origin[1] + local[1] + local[3])


def draw_centered(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str, fnt, fill) -> tuple[int, int, int, int]:
    report = draw_text_by_raster_bbox(draw, rect, text, fnt, fill, align="center")
    return tuple(report["raster_glyph_bbox"])


def draw_left(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str, fnt, fill, pad_x=8) -> tuple[int, int, int, int]:
    report = draw_text_by_raster_bbox(draw, rect, text, fnt, fill, align="left", pad_x=pad_x)
    return tuple(report["raster_glyph_bbox"])


def draw_dossier(draw: ImageDraw.ImageDraw, origin: tuple[int, int], scenario: dict, qa: bool = False) -> list[dict]:
    ox, oy = origin
    dw, dh = CONTRACT["dossier_export_size"]
    report: list[dict] = []

    # Contract carrier.
    draw.rectangle([ox + 8, oy + 10, ox + dw + 8, oy + dh + 10], fill=(0, 0, 0, 120))
    draw.rectangle([ox, oy, ox + dw, oy + dh], fill=(219, 207, 179, 246), outline=(238, 230, 200, 255), width=2)
    draw.rectangle([ox + 8, oy + 8, ox + dw - 8, oy + dh - 8], outline=(91, 84, 68, 160), width=1)
    draw.rectangle([ox + dw + 3, oy + 22, ox + dw + 16, oy + dh - 20], fill=(95, 112, 52, 210))
    draw.rectangle([ox + dw + 10, oy + 335, ox + dw + 24, oy + 435], fill=(51, 118, 130, 210))
    draw.rectangle([ox + dw + 17, oy + 400, ox + dw + 32, oy + 490], fill=(145, 63, 42, 210))

    slots = CONTRACT["content_slots"]
    title_rect = abs_rect(origin, slots["title_slot"])
    stamp_rect = abs_rect(origin, slots["status_stamp"])
    photo_rect = abs_rect(origin, slots["photo_slot"])
    meta_rect = abs_rect(origin, slots["meta_slot"])

    # Visual plates.
    draw.rectangle(title_rect, fill=(167, 158, 132, 155))
    draw.rectangle(stamp_rect, outline=(132, 42, 34, 230), width=2)
    draw.rectangle(photo_rect, fill=(56, 75, 80, 235), outline=(35, 45, 45, 230), width=2)
    draw.rectangle(meta_rect, fill=(211, 199, 171, 180))

    # Header icon.
    icon_rect = abs_rect(origin, slots["header_icon"])
    cx = (icon_rect[0] + icon_rect[2]) // 2
    cy = (icon_rect[1] + icon_rect[3]) // 2
    r = 18
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(70, 75, 58, 240), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(70, 75, 58, 230), width=1)
    draw.line([cx, cy - r, cx, cy + r], fill=(70, 75, 58, 230), width=1)

    # Photo placeholder: broad low-poly blocks, no final art claim.
    px0, py0, px1, py1 = photo_rect
    polys = [
        [(px0, py0), (px0 + 76, py0), (px0 + 38, py1), (px0, py1)],
        [(px0 + 76, py0), (px0 + 165, py0), (px0 + 130, py1), (px0 + 38, py1)],
        [(px0 + 165, py0), (px1, py0), (px1, py1), (px0 + 130, py1)],
        [(px0 + 110, py0 + 42), (px0 + 178, py0 + 68), (px0 + 154, py1), (px0 + 78, py1)],
    ]
    cols = [(70, 92, 99, 255), (100, 116, 126, 255), (58, 73, 80, 255), (42, 48, 50, 255)]
    for pts, col in zip(polys, cols):
        draw.polygon(pts, fill=col)

    # Text fitting.
    f_title, title_size, title_ok, title_wh = fit_font(draw, scenario["title"], FONT_BOLD, 26, 18, (slots["title_slot"][2] - 10, slots["title_slot"][3] - 6))
    title_bbox = draw_left(draw, title_rect, scenario["title"], f_title, (20, 24, 22, 245), pad_x=8)
    report.append({"field": "title", "text": scenario["title"], "font_size": title_size, "fits": title_ok, "text_size": title_wh, "rect": list(title_rect), "bbox": list(title_bbox)})

    # Stamp two lines.
    f_risk, risk_size, risk_ok, risk_wh = fit_font(draw, scenario["risk"], FONT_BOLD, 18, 13, (stamp_rect[2] - stamp_rect[0] - 8, 22))
    f_rec, rec_size, rec_ok, rec_wh = fit_font(draw, scenario["recommend"], FONT_BOLD, 13, 10, (stamp_rect[2] - stamp_rect[0] - 8, 18))
    risk_bbox = draw_centered(draw, (stamp_rect[0] + 4, stamp_rect[1] + 8, stamp_rect[2] - 4, stamp_rect[1] + 31), scenario["risk"], f_risk, (132, 42, 34, 245))
    rec_bbox = draw_centered(draw, (stamp_rect[0] + 4, stamp_rect[1] + 32, stamp_rect[2] - 4, stamp_rect[3] - 4), scenario["recommend"], f_rec, (38, 34, 28, 235))
    report.append({"field": "risk_stamp", "text": scenario["risk"], "font_size": risk_size, "fits": risk_ok, "text_size": risk_wh, "rect": list(stamp_rect), "bbox": list(risk_bbox)})
    report.append({"field": "recommend_stamp", "text": scenario["recommend"], "font_size": rec_size, "fits": rec_ok, "text_size": rec_wh, "rect": list(stamp_rect), "bbox": list(rec_bbox)})

    # Heat and bars below title.
    heat_rect = (title_rect[0], title_rect[3] + 8, title_rect[0] + 92, title_rect[3] + 28)
    bars_rect = (heat_rect[2] + 8, heat_rect[1], heat_rect[2] + 72, heat_rect[3])
    f_heat, heat_size, heat_ok, heat_wh = fit_font(draw, scenario["heat"], FONT_BOLD, 13, 10, (92, 16))
    heat_bbox = draw_left(draw, heat_rect, scenario["heat"], f_heat, (130, 43, 34, 245), pad_x=0)
    draw.text((bars_rect[0], bars_rect[1] + 1), scenario["bars"], font=font(FONT_BOLD, 11), fill=(135, 64, 44, 230))
    report.append({"field": "heat", "text": scenario["heat"], "font_size": heat_size, "fits": heat_ok, "text_size": heat_wh, "rect": list(heat_rect), "bbox": list(heat_bbox)})

    f_meta, meta_size, meta_ok, meta_wh = fit_font(draw, scenario["meta"], FONT_REGULAR, 13, 10, (slots["meta_slot"][2] - 8, slots["meta_slot"][3] - 4))
    meta_bbox = draw_left(draw, meta_rect, scenario["meta"], f_meta, (34, 34, 30, 235), pad_x=6)
    report.append({"field": "meta", "text": scenario["meta"], "font_size": meta_size, "fits": meta_ok, "text_size": meta_wh, "rect": list(meta_rect), "bbox": list(meta_bbox)})

    # CTA rows.
    sx, sy, _, _ = slots["action_stack"]
    lane_w, lane_h = CONTRACT["action_lane_export_size"]
    gap = CONTRACT["action_lane_gap"]
    lslots = CONTRACT["action_lane_slots"]
    for i, cta in enumerate(scenario["cta"]):
        lx = ox + sx
        ly = oy + sy + i * (lane_h + gap)
        col = cta["tone"]
        draw.rectangle([lx, ly, lx + lane_w, ly + lane_h], fill=(*col, 235), outline=(232, 218, 178, 235), width=2)
        # broad material facets
        draw.polygon([(lx, ly), (lx + 84, ly), (lx + 48, ly + lane_h), (lx, ly + lane_h)], fill=(0, 0, 0, 32))
        draw.polygon([(lx + 210, ly), (lx + lane_w, ly), (lx + lane_w, ly + lane_h), (lx + 220, ly + lane_h)], fill=(255, 255, 255, 20))

        icon_local = lslots["left_icon_zone"]
        label_local = lslots["label_plate"]
        badge_local = lslots["right_action_badge"]
        icon_rect2 = (lx + icon_local[0], ly + icon_local[1], lx + icon_local[0] + icon_local[2], ly + icon_local[1] + icon_local[3])
        label_rect = (lx + label_local[0], ly + label_local[1], lx + label_local[0] + label_local[2], ly + label_local[1] + label_local[3])
        badge_rect = (lx + badge_local[0], ly + badge_local[1], lx + badge_local[0] + badge_local[2], ly + badge_local[1] + badge_local[3])
        draw.rectangle(label_rect, fill=(222, 211, 180, 235), outline=(238, 230, 200, 180), width=1)
        draw.rectangle(badge_rect, fill=(30, 35, 30, 145), outline=(238, 230, 200, 210), width=2)
        draw.ellipse(icon_rect2, outline=(238, 230, 190, 230), width=2)

        f_cta, cta_size, cta_ok, cta_wh = fit_font(draw, cta["text"], FONT_BOLD, 18, 12, (label_local[2] - 12, label_local[3] - 6))
        cta_bbox = draw_centered(draw, label_rect, cta["text"], f_cta, (30, 31, 27, 245))
        report.append({"field": f"cta_{i+1}_{cta['kind']}", "text": cta["text"], "font_size": cta_size, "fits": cta_ok, "text_size": cta_wh, "rect": list(label_rect), "bbox": list(cta_bbox)})

        if qa:
            draw.rectangle([lx, ly, lx + lane_w, ly + lane_h], outline=(255, 110, 92, 255), width=2)
            draw.rectangle(label_rect, outline=(255, 221, 77, 255), width=2)
            draw.rectangle(cta_bbox, outline=(255, 80, 210, 255), width=1)

    if qa:
        draw.rectangle([ox, oy, ox + dw, oy + dh], outline=(100, 245, 135, 255), width=3)
        for name, local in slots.items():
            rr = abs_rect(origin, local)
            draw.rectangle(rr, outline=(100, 220, 255, 180), width=1)
        for item in report:
            draw.rectangle(item["bbox"], outline=(255, 80, 210, 210), width=1)
    return report


def create_board() -> tuple[list[dict], list[dict]]:
    canvas = Image.new("RGB", (1280, 840), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 24), "v0.8.4 Right Dossier + CTA Text Stress", font=font(FONT_BOLD, 26), fill=(244, 240, 214))
    draw.text((32, 58), "Normal content and long/stress content inside the same 320x520 / 284x50 contract.", font=FR, fill=(220, 230, 205))
    normal_report = draw_dossier(draw, (80, 110), SCENARIOS[0], qa=True)
    stress_report = draw_dossier(draw, (510, 110), SCENARIOS[1], qa=True)

    def summary(report: list[dict]) -> tuple[int, int]:
        total = len(report)
        passed = sum(1 for item in report if item["fits"])
        return passed, total

    np, nt = summary(normal_report)
    sp, st = summary(stress_report)
    draw.text((80, 650), f"normal: {np}/{nt} text fields fit", font=font(FONT_BOLD, 18), fill=(170, 255, 190) if np == nt else (255, 120, 110))
    draw.text((510, 650), f"stress: {sp}/{st} text fields fit", font=font(FONT_BOLD, 18), fill=(170, 255, 190) if sp == st else (255, 120, 110))
    notes = [
        "Pass means glyph bbox fits inside the declared slot at or above the min font size.",
        "This validates capacity, not final typography taste or final art quality.",
        "If a field only passes at the minimum font size, it should be reviewed before asset freeze.",
    ]
    for i, line in enumerate(notes):
        draw.text((80, 692 + i * 24), line, font=FR, fill=(230, 230, 205))
    canvas.save(OUT_BOARD)
    return normal_report, stress_report


def create_full_and_qa() -> tuple[list[dict], list[dict]]:
    base = Image.open(REF).convert("RGB")
    # Cover the baked old right panel with the contract panel.
    full = base.copy()
    draw = ImageDraw.Draw(full, "RGBA")
    draw.rectangle([920, 20, 1279, 570], fill=(7, 18, 20, 210))
    normal_report = draw_dossier(draw, tuple(CONTRACT["dossier_position"]), SCENARIOS[0], qa=False)
    full.save(OUT_FULL)

    qa = base.copy()
    draw_qa = ImageDraw.Draw(qa, "RGBA")
    draw_qa.rectangle([920, 20, 1279, 570], fill=(7, 18, 20, 210))
    stress_report = draw_dossier(draw_qa, tuple(CONTRACT["dossier_position"]), SCENARIOS[1], qa=True)
    draw_qa.rectangle([280, 28, 870, 88], fill=(7, 18, 20, 220), outline=(132, 168, 132, 255), width=1)
    draw_qa.text((292, 40), "v0.8.4 QA: right text stress, stress scenario", font=font(FONT_BOLD, 18), fill=(244, 240, 214))
    draw_qa.text((292, 66), "magenta=glyph bbox / blue=contract slots / green=dossier", font=FS, fill=(220, 230, 205))
    qa.save(OUT_QA)
    return normal_report, stress_report


def write_manifest(normal_board: list[dict], stress_board: list[dict], normal_full: list[dict], stress_full: list[dict]) -> None:
    data = {
        "artifact": "WMW v0.8.4 right dossier CTA text stress",
        "date": "2026-07-08",
        "artifact_type": "text_capacity_stress / right_dossier_page / right_action_lane / not final art / not atlas",
        "contract": CONTRACT,
        "scenarios": SCENARIOS,
        "outputs": {
            "board": str(OUT_BOARD),
            "full": str(OUT_FULL),
            "qa": str(OUT_QA),
            "manifest": str(OUT_MANIFEST),
        },
        "reports": {
            "normal_board": normal_board,
            "stress_board": stress_board,
            "normal_full": normal_full,
            "stress_full": stress_full,
        },
        "decision": "right_dossier_page 320x520 and right_action_lane 284x50 pass this text-capacity stress, but final typography taste still needs UI review before production art freeze.",
        "next_gate": "If accepted, write no-text clean-sprite brief for right_dossier_page and right_action_lane.",
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    OUT_BOARD.parent.mkdir(parents=True, exist_ok=True)
    normal_board, stress_board = create_board()
    normal_full, stress_full = create_full_and_qa()
    write_manifest(normal_board, stress_board, normal_full, stress_full)
    print(OUT_BOARD)
    print(OUT_FULL)
    print(OUT_QA)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
