from __future__ import annotations

from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


BASE = Path(r"D:\angos\docs\screenshots\2026-06-24-world-map-benchmark-landing")
REF = Path(r"D:\angos\.codex-remote-attachments\019ef3f7-be2f-70d3-ae57-7df7fa181048\285fb7d4-37f0-4a98-86f4-c1652013a1d1\1-Photo-1.jpg")

OUT_PROOF = BASE / "351-world-map-wmw-v0-8-2-left-card-uniform-reinsert-proof.png"
OUT_QA = BASE / "352-world-map-wmw-v0-8-2-left-card-uniform-reinsert-qa.png"
OUT_CROPS = BASE / "353-world-map-wmw-v0-8-2-left-card-uniform-reinsert-crops.png"
OUT_MANIFEST = BASE / "354-world-map-wmw-v0-8-2-left-card-uniform-reinsert-manifest.json"

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

CARD = {
    "class_id": "left_region_card",
    "export_size": [204, 150],
    "positions": [[44, 24], [44, 197], [44, 370], [44, 543]],
    "photo_slot": [21, 24, 174, 58],
    "label_plate": [22, 94, 114, 32],
    "meta_line": [22, 128, 104, 10],
    "icon_badge": [16, 15, 32, 32],
    "action_badge": [158, 96, 38, 38],
    "hit_rect": [0, 0, 204, 150],
    "stack_gap": 23,
}

SOURCE_PHOTOS = [
    [64, 73, 239, 146],
    [65, 253, 239, 328],
    [65, 433, 239, 486],
    [65, 587, 239, 638],
]

STATES = [
    {
        "id": "selected",
        "name": "北美禁区带",
        "meta": "红线升温  推荐2",
        "shell": (79, 102, 46),
        "accent": (170, 190, 94),
        "glyph": "✓",
    },
    {
        "id": "available",
        "name": "欧洲灰域",
        "meta": "可派遣  线报2",
        "shell": (45, 98, 108),
        "accent": (115, 184, 192),
        "glyph": "◎",
    },
    {
        "id": "warning",
        "name": "非洲禁区带",
        "meta": "异常升温  高危",
        "shell": (139, 100, 34),
        "accent": (214, 174, 70),
        "glyph": "!",
    },
    {
        "id": "locked",
        "name": "南美禁区带",
        "meta": "锁定  需3线报",
        "shell": (74, 76, 70),
        "accent": (146, 144, 128),
        "glyph": "L",
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


FB = font(FONT_BOLD, 22)
F_TITLE = font(FONT_BOLD, 20)
F_META = font(FONT_BOLD, 10)
F_LABEL = font(FONT_BOLD, 11)
F_SMALL = font(FONT_REGULAR, 11)


def polygon_card(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, fill, accent) -> None:
    cut = 17
    points = [
        (x + cut, y),
        (x + w - cut, y),
        (x + w, y + cut),
        (x + w, y + h - cut),
        (x + w - cut, y + h),
        (x + cut, y + h),
        (x, y + h - cut),
        (x, y + cut),
    ]
    shadow = [(px + 5, py + 5) for px, py in points]
    draw.polygon(shadow, fill=(0, 0, 0, 145))
    draw.polygon(points, fill=(*fill, 246), outline=(224, 218, 176, 235))
    draw.line(points + [points[0]], fill=(16, 26, 20, 180), width=3)

    # Low-poly-like block facets, deliberately broad and low contrast.
    facets = [
        [(x, y), (x + 70, y), (x + 36, y + 58), (x, y + 78)],
        [(x + 70, y), (x + w, y), (x + w - 38, y + 44), (x + 36, y + 58)],
        [(x + 122, y + 74), (x + w, y + 48), (x + w, y + h), (x + 126, y + h)],
        [(x, y + 106), (x + 70, y + 82), (x + 118, y + h), (x, y + h)],
    ]
    facet_cols = [
        (255, 255, 255, 18),
        (0, 0, 0, 20),
        (*accent, 38),
        (0, 0, 0, 28),
    ]
    for pts, col in zip(facets, facet_cols):
        draw.polygon(pts, fill=col)


def draw_globe(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color=(230, 222, 184, 230)) -> None:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 80, 280, fill=color, width=1)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], -100, 100, fill=color, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=1)
    draw.line([cx, cy - r, cx, cy + r], fill=color, width=1)


def draw_card(base: Image.Image, src: Image.Image, state: dict, photo_rect: list[int], position: list[int], qa: bool = False) -> dict:
    x, y = position
    w, h = CARD["export_size"]
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    polygon_card(draw, x, y, w, h, state["shell"], state["accent"])

    psx, psy, psw, psh = CARD["photo_slot"]
    photo = src.crop(photo_rect).convert("RGB")
    photo_fit = ImageOps.fit(photo, (psw, psh), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    photo_fit = Image.blend(photo_fit, Image.new("RGB", photo_fit.size, state["shell"]), 0.12)
    layer.paste(photo_fit.convert("RGBA"), (x + psx, y + psy))
    draw.rectangle([x + psx, y + psy, x + psx + psw, y + psy + psh], outline=(18, 26, 24, 210), width=2)

    ix, iy, iw, ih = CARD["icon_badge"]
    draw_globe(draw, x + ix + iw // 2, y + iy + ih // 2, 17)

    lx, ly, lw, lh = CARD["label_plate"]
    draw.rectangle([x + lx, y + ly, x + lx + lw, y + ly + lh], fill=(224, 211, 174, 242), outline=(236, 229, 200, 220), width=1)
    draw.text((x + lx + 8, y + ly + 4), state["name"], font=F_LABEL, fill=(20, 24, 22, 245))
    draw.text((x + lx + 8, y + ly + 21), state["meta"], font=F_META, fill=(112, 42, 34, 235))

    ax, ay, aw, ah = CARD["action_badge"]
    draw.rectangle([x + ax, y + ay, x + ax + aw, y + ay + ah], fill=(22, 32, 26, 185), outline=(232, 220, 176, 235), width=2)
    glyph = state["glyph"]
    if glyph == "✓":
        draw.line([x + ax + 10, y + ay + 21, x + ax + 18, y + ay + 29, x + ax + 31, y + ay + 10], fill=(238, 232, 190, 245), width=5)
    elif glyph == "◎":
        draw.ellipse([x + ax + 9, y + ay + 9, x + ax + 29, y + ay + 29], outline=(238, 232, 190, 240), width=3)
        draw.ellipse([x + ax + 15, y + ay + 15, x + ax + 23, y + ay + 23], fill=(238, 232, 190, 210))
    elif glyph == "!":
        draw.polygon([(x + ax + 19, y + ay + 8), (x + ax + 31, y + ay + 30), (x + ax + 7, y + ay + 30)], outline=(238, 232, 190, 240), fill=(0, 0, 0, 0))
        draw.text((x + ax + 16, y + ay + 13), "!", font=FB, fill=(238, 232, 190, 240))
    else:
        draw.text((x + ax + 13, y + ay + 9), "L", font=FB, fill=(238, 232, 190, 240))

    if qa:
        draw.rectangle([x, y, x + w, y + h], outline=(89, 244, 137, 255), width=2)
        draw.rectangle([x + psx, y + psy, x + psx + psw, y + psy + psh], outline=(83, 230, 255, 255), width=2)
        draw.rectangle([x + lx, y + ly, x + lx + lw, y + ly + lh], outline=(255, 221, 77, 255), width=2)
        draw.rectangle([x + ax, y + ay, x + ax + aw, y + ay + ah], outline=(255, 111, 111, 255), width=2)
        draw.text((x + 6, y + 6), f"{w}x{h}", font=F_SMALL, fill=(170, 255, 190, 255))

    base.alpha_composite(layer)
    return {
        "state": state["id"],
        "position": position,
        "export_rect": [x, y, x + w, y + h],
        "photo_rect": [x + psx, y + psy, x + psx + psw, y + psy + psh],
        "label_plate": [x + lx, y + ly, x + lx + lw, y + ly + lh],
        "action_badge": [x + ax, y + ay, x + ax + aw, y + ay + ah],
    }


def clear_left_stack(img: Image.Image) -> Image.Image:
    # Preserve the outer left arrows and surrounding board; only remove old card art.
    out = img.convert("RGBA")
    draw = ImageDraw.Draw(out, "RGBA")
    draw.rectangle([38, 18, 260, 702], fill=(7, 18, 19, 230))
    # Bring back a quiet left-rail feel.
    draw.rectangle([36, 18, 262, 702], outline=(24, 47, 50, 180), width=2)
    return out


def create_full(qa: bool = False) -> tuple[Image.Image, list[dict]]:
    src = Image.open(REF).convert("RGB")
    out = clear_left_stack(src)
    rects = []
    for state, photo, pos in zip(STATES, SOURCE_PHOTOS, CARD["positions"]):
        rects.append(draw_card(out, src, state, photo, pos, qa=qa))
    if qa:
        draw = ImageDraw.Draw(out, "RGBA")
        draw.text((285, 28), "v0.8.2 QA: left_region_card uniform reinsert", font=FB, fill=(244, 240, 212, 255))
        ew, eh = CARD["export_size"]
        psw, psh = CARD["photo_slot"][2], CARD["photo_slot"][3]
        draw.text((285, 58), f"green=export {ew}x{eh} / cyan=photo {psw}x{psh} / yellow=label plate / red=action badge", font=F_SMALL, fill=(222, 230, 204, 255))
    return out.convert("RGB"), rects


def create_crops(full: Image.Image) -> None:
    canvas = Image.new("RGB", (1280, 620), (7, 18, 20))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((30, 24), "v0.8.2 Left Card Reinsert 100% Crops", font=FB, fill=(244, 240, 212))
    for i, (state, pos) in enumerate(zip(STATES, CARD["positions"])):
        x, y = pos
        crop = full.crop((x - 10, y - 10, x + CARD["export_size"][0] + 14, y + CARD["export_size"][1] + 14))
        cx = 40 + (i % 2) * 610
        cy = 80 + (i // 2) * 250
        canvas.paste(crop, (cx, cy))
        draw.text((cx, cy + crop.height + 8), f"{state['id']}  export 204x150, same slots", font=F_SMALL, fill=(220, 230, 204))
    canvas.save(OUT_CROPS)


def write_manifest(rects: list[dict]) -> None:
    data = {
        "artifact": "WMW v0.8.2 left_region_card uniform reinsert proof",
        "date": "2026-07-07",
        "artifact_type": "runtime_fit_proof / contract reinsert / not final art / not atlas",
        "source_reference": str(REF),
        "outputs": {
            "proof": str(OUT_PROOF),
            "qa": str(OUT_QA),
            "crops": str(OUT_CROPS),
            "manifest": str(OUT_MANIFEST),
        },
        "contract": CARD,
        "rects": rects,
        "result": "Uniform 204x150 left_region_card stack fits within the left column at 1280x720 with four states and a 23px vertical gap.",
        "not_validated_yet": [
            "final art quality",
            "all long-text stress strings",
            "actual no-text sprite slicing",
            "Godot runtime assembly",
        ],
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    OUT_PROOF.parent.mkdir(parents=True, exist_ok=True)
    proof, rects = create_full(qa=False)
    proof.save(OUT_PROOF)
    qa, _ = create_full(qa=True)
    qa.save(OUT_QA)
    create_crops(qa)
    write_manifest(rects)
    print(OUT_PROOF)
    print(OUT_QA)
    print(OUT_CROPS)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
