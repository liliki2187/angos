from __future__ import annotations

from pathlib import Path
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont


BASE = Path(r"D:\angos\docs\screenshots\2026-06-24-world-map-benchmark-landing")
REF = Path(r"D:\angos\.codex-remote-attachments\019ef3f7-be2f-70d3-ae57-7df7fa181048\285fb7d4-37f0-4a98-86f4-c1652013a1d1\1-Photo-1.jpg")

OUT_AUDIT = BASE / "348-world-map-wmw-v0-8-1-left-card-current-uniformity-audit.png"
OUT_CONTRACT = BASE / "349-world-map-wmw-v0-8-1-left-card-class-contract.png"
OUT_MANIFEST = BASE / "350-world-map-wmw-v0-8-1-left-card-class-contract-manifest.json"

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


SOURCE_CARDS = [
    {
        "state": "selected",
        "rect": [44, 24, 246, 192],
        "photo": [64, 73, 239, 146],
        "note": "tall source card; not production contract",
    },
    {
        "state": "available",
        "rect": [44, 207, 247, 377],
        "photo": [65, 253, 239, 328],
        "note": "tall source card; not production contract",
    },
    {
        "state": "warning",
        "rect": [44, 388, 247, 537],
        "photo": [65, 433, 239, 486],
        "note": "shorter card; source drift",
    },
    {
        "state": "locked",
        "rect": [44, 543, 248, 692],
        "photo": [65, 587, 239, 638],
        "note": "shorter card; source drift",
    },
]


CONTRACT = {
    "class_id": "left_region_card",
    "artifact_type": "component_class_contract_candidate / geometry lock / not final art / not atlas",
    "source_scale": "1280x720 reference scale",
    "export_size": [204, 150],
    "transparent_bleed": 6,
    "outer_shell_rect": [0, 0, 204, 150],
    "slots": {
        "icon_badge": [16, 15, 32, 32],
        "photo_slot": [21, 24, 174, 58],
        "label_plate": [22, 94, 114, 32],
        "meta_line": [22, 128, 96, 10],
        "action_badge": [158, 96, 38, 38],
        "hit_rect": [0, 0, 204, 150],
    },
    "state_policy": {
        "selected": "skin only; no size or slot change",
        "available": "skin only; no size or slot change",
        "warning": "skin only; no size or slot change",
        "locked": "skin only; no size or slot change",
    },
    "forbidden": [
        "selected state changes card height",
        "warning / locked state uses shorter photo slot",
        "photo is non-uniformly stretched",
        "status icon changes export bounds",
        "shadow / paper bleed changes runtime layout size",
    ],
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
FMB = font(FONT_BOLD, 18)
FR = font(FONT_REGULAR, 15)
FS = font(FONT_REGULAR, 12)


def size_of(rect: list[int]) -> tuple[int, int]:
    return rect[2] - rect[0], rect[3] - rect[1]


def ratio(rect: list[int]) -> float:
    w, h = size_of(rect)
    return w / h


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill=(235, 238, 218), font_obj=None) -> None:
    font_obj = font_obj or FR
    x, y = xy
    bbox = draw.textbbox((x, y), text, font=font_obj)
    draw.rectangle([bbox[0] - 6, bbox[1] - 4, bbox[2] + 6, bbox[3] + 4], fill=(8, 14, 16, 210))
    draw.text((x, y), text, font=font_obj, fill=fill)


def create_audit() -> None:
    src = Image.open(REF).convert("RGB")
    crop = src.crop((20, 0, 280, 720))
    canvas = Image.new("RGB", (1280, 720), (8, 18, 20))
    canvas.paste(crop, (24, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")

    title = "v0.8.1 Left Region Card Uniformity Audit"
    draw.text((330, 28), title, font=FB, fill=(240, 238, 215))
    draw.text(
        (330, 62),
        "结论：当前美术稿左侧地区卡不是同一生产几何；只能作为视觉参考，不能直接切成同一 class。",
        font=FR,
        fill=(210, 224, 205),
    )

    x_offset = 24 - 20
    for idx, card in enumerate(SOURCE_CARDS, 1):
        rect = [card["rect"][0] + x_offset, card["rect"][1], card["rect"][2] + x_offset, card["rect"][3]]
        photo = [card["photo"][0] + x_offset, card["photo"][1], card["photo"][2] + x_offset, card["photo"][3]]
        w, h = size_of(card["rect"])
        pw, ph = size_of(card["photo"])
        line_color = (255, 91, 91, 255) if h != 149 and h != 150 else (104, 232, 150, 255)
        draw.rectangle(rect, outline=line_color, width=3)
        draw.rectangle(photo, outline=(90, 220, 255, 255), width=3)
        draw_label(
            draw,
            (rect[0] + 6, rect[1] + 6),
            f"{idx} {card['state']}  card {w}x{h}  photo {pw}x{ph}",
            fill=(255, 230, 210) if line_color[0] > 200 else (190, 255, 210),
            font_obj=FS,
        )

    table_x = 330
    table_y = 116
    col = [0, 92, 210, 330, 470, 690]
    headers = ["state", "card size", "card ratio", "photo size", "photo ratio", "contract status"]
    row_h = 48
    draw.rectangle([table_x, table_y, table_x + 860, table_y + row_h], fill=(28, 54, 50))
    for i, h in enumerate(headers):
        draw.text((table_x + col[i] + 10, table_y + 15), h, font=FS, fill=(220, 232, 210))
    target_w, target_h = CONTRACT["export_size"]
    for r, card in enumerate(SOURCE_CARDS, 1):
        y = table_y + row_h * r
        cw, ch = size_of(card["rect"])
        pw, ph = size_of(card["photo"])
        card_pass = (cw, ch) == (target_w, target_h)
        fill = (38, 24, 27) if not card_pass else (22, 42, 32)
        draw.rectangle([table_x, y, table_x + 860, y + row_h], fill=fill)
        vals = [
            card["state"],
            f"{cw} x {ch}",
            f"{ratio(card['rect']):.2f}",
            f"{pw} x {ph}",
            f"{ratio(card['photo']):.2f}",
            "FAIL: geometry drift" if not card_pass else "PASS",
        ]
        colors = [(236, 232, 208)] * len(vals)
        colors[-1] = (255, 112, 112) if not card_pass else (114, 245, 153)
        for i, val in enumerate(vals):
            draw.text((table_x + col[i] + 10, y + 15), val, font=FR if i == 0 else FS, fill=colors[i])

    note_y = table_y + row_h * 6 + 10
    notes = [
        "Production rule: selected / available / warning / locked are skins of one left_region_card class.",
        "The status icon, color skin, lock / warning glyph, and paper facets may change; export size and slots may not.",
        "If art wants an expanded selected card, it must be a separate class and the left list layout must be redesigned.",
    ]
    for i, line in enumerate(notes):
        draw.text((table_x, note_y + i * 28), line, font=FR, fill=(230, 226, 190))

    OUT_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_AUDIT)


def draw_card_contract(draw: ImageDraw.ImageDraw, x: int, y: int, state: str, color: tuple[int, int, int]) -> None:
    w, h = CONTRACT["export_size"]
    bleed = CONTRACT["transparent_bleed"]
    draw.rectangle([x - bleed, y - bleed, x + w + bleed, y + h + bleed], outline=(96, 96, 96, 160), width=1)
    draw.rectangle([x, y, x + w, y + h], fill=(color[0], color[1], color[2], 210), outline=(236, 232, 200, 255), width=2)
    # Beveled corners remain inside the same shell bounds.
    cut = 16
    draw.line([(x, y + cut), (x + cut, y), (x + w - cut, y), (x + w, y + cut), (x + w, y + h - cut), (x + w - cut, y + h), (x + cut, y + h), (x, y + h - cut), (x, y + cut)], fill=(20, 28, 20, 180), width=3)

    sx, sy, sw, sh = CONTRACT["slots"]["photo_slot"]
    draw.rectangle([x + sx, y + sy, x + sx + sw, y + sy + sh], fill=(50, 91, 94, 220), outline=(95, 225, 242, 255), width=2)
    draw.text((x + sx + 42, y + sy + 7), "PHOTO SLOT 174x58", font=FS, fill=(214, 244, 236))

    lx, ly, lw, lh = CONTRACT["slots"]["label_plate"]
    draw.rectangle([x + lx, y + ly, x + lx + lw, y + ly + lh], fill=(220, 205, 168, 230), outline=(236, 229, 198, 255), width=2)
    draw.text((x + lx + 6, y + ly + 7), "LABEL PLATE", font=FS, fill=(54, 45, 35))

    ix, iy, iw, ih = CONTRACT["slots"]["icon_badge"]
    draw.ellipse([x + ix, y + iy, x + ix + iw, y + iy + ih], outline=(238, 230, 190, 255), width=2)
    draw.text((x + ix + 5, y + iy + 7), "G", font=FS, fill=(238, 230, 190))

    ax, ay, aw, ah = CONTRACT["slots"]["action_badge"]
    draw.rectangle([x + ax, y + ay, x + ax + aw, y + ay + ah], fill=(26, 34, 28, 180), outline=(242, 226, 185, 255), width=2)
    glyph = {"selected": "✓", "available": "◎", "warning": "!", "locked": "L"}.get(state, "*")
    draw.text((x + ax + 12, y + ay + 7), glyph, font=FMB, fill=(245, 232, 190))

    draw.text((x, y + h + 11), f"{state}: same {w}x{h}, same slots", font=FS, fill=(230, 232, 210))


def create_contract() -> None:
    canvas = Image.new("RGB", (1280, 1040), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.text((32, 26), "v0.8.1 Left Region Card Class Contract Candidate", font=FB, fill=(241, 238, 214))
    draw.text(
        (32, 62),
        "目标：把左侧地区列表从“美术自由高度”改成一个可落地的统一组件 class。",
        font=FR,
        fill=(210, 224, 205),
    )

    # Contract summary.
    x0, y0 = 40, 116
    draw.rectangle([x0, y0, x0 + 500, y0 + 284], fill=(14, 34, 34), outline=(106, 150, 130), width=1)
    summary = [
        ("class_id", CONTRACT["class_id"]),
        ("export_size", f"{CONTRACT['export_size'][0]} x {CONTRACT['export_size'][1]} @ 1280x720 ref"),
        ("transparent_bleed", f"{CONTRACT['transparent_bleed']} px fixed, not layout size"),
        ("photo_slot", "174 x 58, same in all states"),
        ("label_plate", "114 x 32, same in all states"),
        ("action_badge", "38 x 38, same in all states"),
        ("hit_rect", "full card bounds; visual states do not move it"),
    ]
    draw.text((x0 + 18, y0 + 18), "A. Fixed Geometry", font=FMB, fill=(240, 230, 190))
    for i, (k, v) in enumerate(summary):
        yy = y0 + 58 + i * 30
        draw.text((x0 + 18, yy), k, font=FS, fill=(122, 214, 188))
        draw.text((x0 + 158, yy), v, font=FS, fill=(232, 232, 210))

    # Uniform stack preview.
    stack_x, stack_y = 610, 106
    states = [
        ("selected", (86, 112, 48)),
        ("available", (45, 107, 118)),
        ("warning", (151, 112, 36)),
        ("locked", (72, 72, 66)),
    ]
    for i, (state, color) in enumerate(states):
        draw_card_contract(draw, stack_x, stack_y + i * 190, state, color)

    # Target positions at reference scale.
    x1, y1 = 40, 436
    draw.rectangle([x1, y1, x1 + 500, y1 + 250], fill=(20, 29, 30), outline=(110, 130, 118), width=1)
    draw.text((x1 + 18, y1 + 18), "B. Stack Layout Rule", font=FMB, fill=(240, 230, 190))
    lines = [
        "At 1280x720 reference scale, one possible stack:",
        "x = 44, width = 204",
        "y = 24 / 197 / 370 / 543",
        "height = 150, gap = 23",
        "",
        "The exact y can be adjusted by page layout,",
        "but every card in the class keeps the same size.",
    ]
    for i, line in enumerate(lines):
        draw.text((x1 + 18, y1 + 58 + i * 25), line, font=FR, fill=(226, 226, 204))

    x2, y2 = 40, 884
    draw.rectangle([x2, y2, x2 + 1160, y2 + 140], fill=(32, 18, 20), outline=(214, 92, 78), width=1)
    draw.text((x2 + 18, y2 + 18), "C. One-Vote Fails", font=FMB, fill=(255, 204, 190))
    fails = [
        "selected card becomes taller / wider than other region cards",
        "warning or locked state uses a shorter photo slot",
        "photo is squeezed to fit a new slot instead of re-authored / cropped with an approved slot contract",
        "paper shadow, badge, lock, or warning glyph expands the runtime export box",
    ]
    for i, line in enumerate(fails):
        draw.text((x2 + 18, y2 + 55 + i * 22), f"- {line}", font=FS, fill=(244, 224, 208))

    OUT_CONTRACT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_CONTRACT)


def write_manifest() -> None:
    data = {
        "artifact": "WMW v0.8.1 left region card class contract candidate",
        "date": "2026-07-07",
        "source_reference": str(REF),
        "outputs": {
            "audit": str(OUT_AUDIT),
            "contract": str(OUT_CONTRACT),
            "manifest": str(OUT_MANIFEST),
        },
        "source_measurements": [
            {
                "state": card["state"],
                "card_rect": card["rect"],
                "card_size": list(size_of(card["rect"])),
                "card_ratio": ratio(card["rect"]),
                "photo_rect": card["photo"],
                "photo_size": list(size_of(card["photo"])),
                "photo_ratio": ratio(card["photo"]),
                "note": card["note"],
            }
            for card in SOURCE_CARDS
        ],
        "contract": CONTRACT,
        "decision": "Left region cards should be one uniform component class. Source art may vary for composition, but production export size and functional slots must not vary by state.",
        "next_gate": "User review, then write full v0.8.1 class contract review and use this class in clean-sprite brief v0.8.2.",
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    create_audit()
    create_contract()
    write_manifest()
    print(OUT_AUDIT)
    print(OUT_CONTRACT)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
