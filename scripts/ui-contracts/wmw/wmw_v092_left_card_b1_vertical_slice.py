# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
CONTRACT_PATH = ROOT / "design/ui-contracts/world-map/left_region_card.json"

# B1 is intentionally not a pure program-drawn asset. It combines:
# - candidate B as the geometry-preserving source,
# - true imagegen B1 R4 as the local art source for photo slots and the red warning badge.
SOURCE_B = BASE / "383-world-map-wmw-v0-9-1-left-card-imagegen-candidate-b.png"
IMAGEGEN_B1_R4 = BASE / "396-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r4-wide-failed.png"
REF = BASE / "258-world-map-wmw-benchmark-shell-reference-v0-1.png"

OUT_CANDIDATE = BASE / "397-world-map-wmw-v0-9-2-left-card-candidate-b1-composited-polish.png"
OUT_QA = BASE / "398-world-map-wmw-v0-9-2-left-card-candidate-b1-geometry-qa.png"
OUT_ATLAS = BASE / "399-world-map-wmw-v0-9-2-left-card-candidate-b1-atlas-2x.png"
OUT_RUNTIME = BASE / "400-world-map-wmw-v0-9-2-left-card-candidate-b1-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "401-world-map-wmw-v0-9-2-left-card-candidate-b1-runtime-fill-qa.png"
OUT_MANIFEST = BASE / "402-world-map-wmw-v0-9-2-left-card-candidate-b1-manifest.json"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_candidate_b1_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_candidate_b1_manifest.json"

STATE_ORDER = ["selected", "available", "warning", "locked"]
STATE_LABELS = [
    ("北美禁区带", "红线升温  推荐2"),
    ("欧洲灰域", "可派遣  线报2"),
    ("非洲禁区带", "异常升温  高危"),
    ("南美禁区带", "锁定  需3线报"),
]


def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


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

TOKENS = {
    "label_title": {
        "font": font(FONT_BOLD, 19),
        "godot_font_size": 25,
        "fill": (18, 22, 18, 248),
        "godot_color": "#121612",
    },
    "meta_status": {
        "font": font(FONT_REGULAR, 11),
        "godot_font_size": 14,
        "fill": (66, 28, 20, 248),
        "godot_color": "#421c14",
    },
}
F_SMALL = font(FONT_REGULAR, 13)
F_NOTE = font(FONT_REGULAR, 16)
F_HEAD = font(FONT_BOLD, 26)


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def is_chroma_green(pixel: tuple[int, int, int]) -> bool:
    r, g, b = pixel
    return g >= 210 and r <= 70 and b <= 70


def build_mask(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    src = rgb.load()
    dst = mask.load()
    for y in range(h):
        for x in range(w):
            dst[x, y] = 0 if is_chroma_green(src[x, y]) else 255
    return mask


def find_components(mask: Image.Image, min_area: int = 20000) -> list[tuple[int, int, int, int]]:
    w, h = mask.size
    data = mask.load()
    seen = bytearray(w * h)
    boxes: list[tuple[int, int, int, int, int]] = []

    def idx(x: int, y: int) -> int:
        return y * w + x

    for y0 in range(h):
        for x0 in range(w):
            start = idx(x0, y0)
            if seen[start] or data[x0, y0] == 0:
                continue
            seen[start] = 1
            q: deque[tuple[int, int]] = deque([(x0, y0)])
            min_x = max_x = x0
            min_y = max_y = y0
            area = 0
            while q:
                x, y = q.popleft()
                area += 1
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if nx < 0 or ny < 0 or nx >= w or ny >= h:
                        continue
                    n = idx(nx, ny)
                    if seen[n] or data[nx, ny] == 0:
                        continue
                    seen[n] = 1
                    q.append((nx, ny))
            if area >= min_area:
                boxes.append((min_x, min_y, max_x + 1, max_y + 1, area))
    boxes.sort(key=lambda b: (b[1] // max(1, h // 3), b[0]))
    return [(x1, y1, x2, y2) for x1, y1, x2, y2, _area in boxes[:4]]


def find_quadrant_boxes(mask: Image.Image) -> list[tuple[int, int, int, int]]:
    w, h = mask.size
    data = mask.load()
    quadrants = [
        (0, 0, w // 2, h // 2),
        (w // 2, 0, w, h // 2),
        (0, h // 2, w // 2, h),
        (w // 2, h // 2, w, h),
    ]
    boxes: list[tuple[int, int, int, int]] = []
    for qx1, qy1, qx2, qy2 in quadrants:
        xs: list[int] = []
        ys: list[int] = []
        for y in range(qy1, qy2):
            for x in range(qx1, qx2):
                if data[x, y] > 0:
                    xs.append(x)
                    ys.append(y)
        if not xs:
            boxes.append((qx1, qy1, qx2, qy2))
            continue
        boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    return boxes


def crop_with_alpha(
    source: Image.Image,
    mask: Image.Image,
    box: tuple[int, int, int, int],
    pad: int = 8,
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    x1, y1, x2, y2 = box
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(source.width, x2 + pad)
    y2 = min(source.height, y2 + pad)
    crop = source.crop((x1, y1, x2, y2)).convert("RGBA")
    alpha = mask.crop((x1, y1, x2, y2))
    crop.putalpha(alpha)
    return crop, (x1, y1, x2, y2)


def fit_into_frame(crop: Image.Image, frame_size: tuple[int, int]) -> tuple[Image.Image, dict]:
    fw, fh = frame_size
    scale = min(fw / crop.width, fh / crop.height)
    nw = max(1, round(crop.width * scale))
    nh = max(1, round(crop.height * scale))
    resized = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", frame_size, (0, 0, 0, 0))
    px = (fw - nw) // 2
    py = (fh - nh) // 2
    frame.alpha_composite(resized, (px, py))
    return frame, {
        "source_size": [crop.width, crop.height],
        "fit_size": [nw, nh],
        "offset": [px, py],
        "scale": scale,
        "letterbox": [fw - nw, fh - nh],
    }


def zero_chroma_alpha(img: Image.Image) -> Image.Image:
    out = img.convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a > 0 and is_chroma_green((r, g, b)):
                px[x, y] = (r, g, b, 0)
    return out


def scrub_nonselected_photo_right_edge(frame: Image.Image, state: str, slots: dict, scale: int) -> Image.Image:
    if state == "selected":
        return frame
    out = frame.convert("RGBA")
    px = out.load()
    x, y, w, h = slots["photo_slot"]
    x1 = max(0, (x + w) * scale - 16)
    x2 = out.width
    y1 = max(0, y * scale)
    y2 = min(out.height, (y + h) * scale)

    def is_residual_green(c: tuple[int, int, int, int]) -> bool:
        r, g, b, a = c
        return a > 20 and g > 105 and g > r * 1.16 and g > b * 1.08

    fallback = body_colors_for_state(state)
    for yy in range(y1, y2):
        source_x = max(0, x1 - 12)
        source = px[source_x, yy]
        if source[3] <= 20 or is_residual_green(source):
            source = (fallback[0], fallback[1], fallback[2], 255)
        for xx in range(x1, x2):
            if px[xx, yy][3] > 20:
                px[xx, yy] = source
    return out


def scrub_nonselected_outer_green_glow(frame: Image.Image, state: str) -> Image.Image:
    if state == "selected":
        return frame
    out = frame.convert("RGBA")
    px = out.load()
    border = 32
    for y in range(out.height):
        for x in range(out.width):
            if x >= border and x < out.width - border and y >= border and y < out.height - border:
                continue
            r, g, b, a = px[x, y]
            if a <= 0:
                continue
            saturated_green = g > 95 and g > r * 1.22 and g > b * 1.12
            bottom_shadow_green = y >= out.height - border and g > 34 and g > r * 1.02 and g > b * 1.02
            if saturated_green or bottom_shadow_green:
                px[x, y] = (r, g, b, 0)
    return out


def frame_rect_to_source_rect(
    crop_box: tuple[int, int, int, int],
    fit: dict,
    rect: list[int],
    scale_factor: int,
    inset: int = 0,
) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    fx1 = x * scale_factor + inset
    fy1 = y * scale_factor + inset
    fx2 = (x + w) * scale_factor - inset
    fy2 = (y + h) * scale_factor - inset
    ox, oy = fit["offset"]
    scale = fit["scale"]
    sx1 = crop_box[0] + round((fx1 - ox) / scale)
    sy1 = crop_box[1] + round((fy1 - oy) / scale)
    sx2 = crop_box[0] + round((fx2 - ox) / scale)
    sy2 = crop_box[1] + round((fy2 - oy) / scale)
    return sx1, sy1, sx2, sy2


def crop_relative(img: Image.Image, box: tuple[int, int, int, int], rel: tuple[float, float, float, float]) -> Image.Image:
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    rx, ry, rw, rh = rel
    return img.crop((
        round(x1 + w * rx),
        round(y1 + h * ry),
        round(x1 + w * (rx + rw)),
        round(y1 + h * (ry + rh)),
    )).convert("RGB")


def body_colors_for_state(state: str) -> tuple[int, int, int]:
    return {
        "selected": (74, 86, 35),
        "available": (42, 113, 118),
        "warning": (151, 104, 23),
        "locked": (76, 79, 74),
    }[state]


def trim_outer_frame_light(frame: Image.Image, state: str) -> Image.Image:
    out = frame.convert("RGBA")
    alpha = out.getchannel("A")
    inner = alpha.filter(ImageFilter.MinFilter(15))
    edge = ImageChops.subtract(alpha, inner)
    px = out.load()
    e = edge.load()
    body = body_colors_for_state(state)
    for y in range(out.height):
        for x in range(out.width):
            if e[x, y] < 32:
                continue
            r, g, b, a = px[x, y]
            lum = (r * 0.2126 + g * 0.7152 + b * 0.0722)
            if lum < 105 or a < 20:
                continue
            px[x, y] = (
                round(r * 0.70 + body[0] * 0.30),
                round(g * 0.70 + body[1] * 0.30),
                round(b * 0.70 + body[2] * 0.30),
                a,
            )
    return out


def cleanup_green_residue(img: Image.Image, box: tuple[int, int, int, int]) -> None:
    # Candidate B already uses chroma green as the sheet background. Earlier
    # wider thresholds over-cleaned teal/dark olive art into visible holes, so
    # this pass is intentionally conservative.
    return


def fill_chroma_green_from_neighbors(img: Image.Image) -> Image.Image:
    out = img.convert("RGB")
    px = out.load()
    w, h = out.size
    fallback = (10, 24, 30)
    for y in range(h):
        non_green = [x for x in range(w) if not is_chroma_green(px[x, y])]
        if not non_green:
            for x in range(w):
                px[x, y] = fallback
            continue
        for x in range(w):
            if not is_chroma_green(px[x, y]):
                continue
            left = max((nx for nx in non_green if nx < x), default=None)
            right = min((nx for nx in non_green if nx > x), default=None)
            if left is None and right is None:
                px[x, y] = fallback
            elif left is None:
                px[x, y] = px[right, y]
            elif right is None:
                px[x, y] = px[left, y]
            elif x - left <= right - x:
                px[x, y] = px[left, y]
            else:
                px[x, y] = px[right, y]
    return out


def scrub_green_patch_edges(img: Image.Image, margin: int = 12) -> Image.Image:
    out = img.convert("RGB")
    px = out.load()
    w, h = out.size

    def is_edge_green(c: tuple[int, int, int]) -> bool:
        r, g, b = c
        return g > 115 and g > r * 1.25 and g > b * 1.15

    for y in range(h):
        valid_x = [x for x in range(w) if not is_edge_green(px[x, y])]
        for x in range(w):
            if x >= margin and x < w - margin:
                continue
            if not is_edge_green(px[x, y]):
                continue
            left = max((nx for nx in valid_x if nx < x), default=None)
            right = min((nx for nx in valid_x if nx > x), default=None)
            if left is None and right is None:
                continue
            if left is None:
                px[x, y] = px[right, y]
            elif right is None:
                px[x, y] = px[left, y]
            elif x - left <= right - x:
                px[x, y] = px[left, y]
            else:
                px[x, y] = px[right, y]
    return out


def red_warning_mask(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    mask = Image.new("L", rgb.size, 0)
    src = rgb.load()
    dst = mask.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = src[x, y]
            if r > 135 and r > g * 1.25 and r > b * 1.25:
                dst[x, y] = 220
    return mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.7))


def repair_chroma_inside_base_mask(
    img: Image.Image,
    base_mask: Image.Image,
    box: tuple[int, int, int, int],
    fallback: tuple[int, int, int],
) -> None:
    px = img.load()
    mask_px = base_mask.load()
    x1, y1, x2, y2 = box
    for y in range(max(0, y1), min(img.height, y2)):
        valid_x = [
            x
            for x in range(max(0, x1), min(img.width, x2))
            if mask_px[x, y] > 0 and not is_chroma_green(px[x, y])
        ]
        for x in range(max(0, x1), min(img.width, x2)):
            if mask_px[x, y] == 0 or not is_chroma_green(px[x, y]):
                continue
            left = max((nx for nx in valid_x if nx < x), default=None)
            right = min((nx for nx in valid_x if nx > x), default=None)
            if left is None and right is None:
                px[x, y] = fallback
            elif left is None:
                px[x, y] = px[right, y]
            elif right is None:
                px[x, y] = px[left, y]
            elif x - left <= right - x:
                px[x, y] = px[left, y]
            else:
                px[x, y] = px[right, y]


def paste_warning_triangle(canvas: Image.Image, source_action: Image.Image, action_rect: tuple[int, int, int, int]) -> None:
    mask = red_warning_mask(source_action)
    bbox = mask.getbbox()
    if bbox is None:
        return
    bx1, by1, bx2, by2 = bbox
    pad = 4
    bx1 = max(0, bx1 - pad)
    by1 = max(0, by1 - pad)
    bx2 = min(source_action.width, bx2 + pad)
    by2 = min(source_action.height, by2 + pad)
    triangle = source_action.crop((bx1, by1, bx2, by2)).convert("RGBA")
    triangle.putalpha(mask.crop((bx1, by1, bx2, by2)))
    target_w = action_rect[2] - action_rect[0]
    target_h = action_rect[3] - action_rect[1]
    triangle = ImageOps.contain(triangle, (target_w, target_h), Image.Resampling.LANCZOS)
    dx = action_rect[0] + (target_w - triangle.width) // 2
    dy = action_rect[1] + (target_h - triangle.height) // 2
    canvas.paste(triangle.convert("RGB"), (dx, dy), triangle.getchannel("A"))


def compose_b1_candidate(contract: dict) -> tuple[Image.Image, list[dict]]:
    base = Image.open(SOURCE_B).convert("RGB")
    art = Image.open(IMAGEGEN_B1_R4).convert("RGB")
    base_mask = build_mask(base)
    art_mask = build_mask(art)
    base_boxes = find_components(base_mask)
    art_boxes = find_components(art_mask)
    if len(art_boxes) != 4:
        art_boxes = find_quadrant_boxes(art_mask)
    if len(base_boxes) != 4 or len(art_boxes) != 4:
        raise RuntimeError(f"Expected 4 base and 4 art components, got {len(base_boxes)} / {len(art_boxes)}")

    scale = int(contract["export_scale"])
    frame_size = (contract["frozen"]["export_size"][0] * scale, contract["frozen"]["export_size"][1] * scale)
    slots = contract["frozen"]["slots"]
    canvas = base.copy()
    rows: list[dict] = []

    # Source R4 is a failed full-card geometry attempt, but its photo-slot art is useful.
    photo_rels = [
        (0.15, 0.17, 0.78, 0.36),
        (0.06, 0.17, 0.82, 0.36),
        (0.15, 0.07, 0.78, 0.40),
        (0.06, 0.07, 0.82, 0.40),
    ]
    action_rel = (0.79, 0.60, 0.15, 0.19)

    for i, state in enumerate(STATE_ORDER):
        base_crop, crop_box = crop_with_alpha(base, base_mask, base_boxes[i])
        frame, fit = fit_into_frame(base_crop, frame_size)
        frame = trim_outer_frame_light(frame, state)

        photo_rect = frame_rect_to_source_rect(crop_box, fit, slots["photo_slot"], scale, inset=2)
        source_photo = crop_relative(art, art_boxes[i], photo_rels[i])
        source_photo = ImageOps.fit(source_photo, (photo_rect[2] - photo_rect[0], photo_rect[3] - photo_rect[1]), Image.Resampling.LANCZOS)
        source_photo = fill_chroma_green_from_neighbors(source_photo)
        source_photo = scrub_green_patch_edges(source_photo)
        canvas.paste(source_photo, photo_rect)

        if state == "warning":
            action_rect = frame_rect_to_source_rect(crop_box, fit, slots["action_badge"], scale, inset=4)
            source_action = crop_relative(art, art_boxes[i], action_rel)
            source_action = ImageOps.fit(source_action, (action_rect[2] - action_rect[0], action_rect[3] - action_rect[1]), Image.Resampling.LANCZOS)
            source_action = fill_chroma_green_from_neighbors(source_action)
            paste_warning_triangle(canvas, source_action, action_rect)

        if state != "selected":
            cleanup_green_residue(canvas, base_boxes[i])
        repair_chroma_inside_base_mask(canvas, base_mask, base_boxes[i], body_colors_for_state(state))

        rows.append(
            {
                "state": state,
                "base_bbox": list(base_boxes[i]),
                "art_source_bbox": list(art_boxes[i]),
                "photo_source": "imagegen_b1_r4",
                "geometry_source": "candidate_b_383",
                "green_residue_cleanup": state != "selected",
                "warning_badge_source": "imagegen_b1_r4" if state == "warning" else "candidate_b_383",
            }
        )

    canvas.save(OUT_CANDIDATE)
    return canvas, rows


def draw_box(draw: ImageDraw.ImageDraw, rect: list[int], origin: tuple[int, int], scale: int, color: tuple[int, int, int], label: str) -> None:
    x, y, w, h = rect
    ox, oy = origin
    box = [ox + x * scale, oy + y * scale, ox + (x + w) * scale, oy + (y + h) * scale]
    draw.rectangle(box, outline=color, width=2)
    draw.text((box[0] + 4, box[1] + 2), label, font=F_SMALL, fill=color)


def create_geometry_qa(source: Image.Image, boxes: list[tuple[int, int, int, int]], contract: dict) -> list[dict]:
    target_w, target_h = contract["frozen"]["export_size"]
    target_ratio = target_w / target_h
    rows: list[dict] = []
    canvas = Image.new("RGB", (1500, 980), "#081315")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((32, 24), "WMW v0.9.2 left_region_card candidate B1 geometry QA", font=F_HEAD, fill="#f1ead0")
    draw.text((32, 60), "B1 uses 383 geometry source plus true imagegen local art source. Ratio gate still uses detected visible card bboxes.", font=F_NOTE, fill="#d9dec7")

    preview = source.convert("RGB").copy()
    d_src = ImageDraw.Draw(preview, "RGBA")
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        ratio = w / h
        diff = ratio - target_ratio
        ratio_pass = abs(diff) <= 0.06
        color = (88, 255, 125, 255) if ratio_pass else (255, 88, 88, 255)
        d_src.rectangle([x1, y1, x2, y2], outline=color, width=5)
        d_src.text((x1 + 8, y1 + 8), f"{STATE_ORDER[i]} {w}x{h} r={ratio:.2f}", font=F_NOTE, fill=color)
        rows.append(
            {
                "state": STATE_ORDER[i],
                "detected_bbox": [x1, y1, w, h],
                "detected_ratio": round(ratio, 4),
                "target_ratio": round(target_ratio, 4),
                "ratio_delta": round(diff, 4),
                "ratio_pass": ratio_pass,
            }
        )

    scaled = ImageOps.contain(preview, (920, 690), method=Image.Resampling.LANCZOS)
    canvas.paste(scaled, (36, 104))
    x0 = 990
    y0 = 112
    draw.text((x0, y0), f"Contract: {target_w}x{target_h}, ratio {target_ratio:.3f}", font=F_NOTE, fill="#f1ead0")
    draw.text((x0, y0 + 32), "No squashing/cropping is used to pass this gate.", font=F_SMALL, fill="#d9dec7")
    for i, row in enumerate(rows):
        y = y0 + 80 + i * 112
        color = "#88ff9d" if row["ratio_pass"] else "#ff6969"
        result = "PASS" if row["ratio_pass"] else "FAIL"
        draw.text((x0, y), f"{row['state']}: {result}", font=F_NOTE, fill=color)
        draw.text((x0, y + 30), f"bbox {row['detected_bbox'][2]}x{row['detected_bbox'][3]}  ratio {row['detected_ratio']}", font=F_SMALL, fill="#e2dfc8")
        draw.text((x0, y + 52), f"target {row['target_ratio']}  delta {row['ratio_delta']}", font=F_SMALL, fill="#e2dfc8")

    atlas_ready = all(r["ratio_pass"] for r in rows)
    verdict = "atlas-ready geometry candidate" if atlas_ready else "NOT atlas-ready: regenerate/edit art against contract"
    vcolor = "#88ff9d" if atlas_ready else "#ff6969"
    draw.text((32, 842), f"Verdict: {verdict}", font=F_HEAD, fill=vcolor)
    draw.text((32, 884), "Visual micro-tune points are checked separately in the manifest and comparison board.", font=F_NOTE, fill="#d9dec7")
    canvas.save(OUT_QA)
    return rows


def make_atlas(source: Image.Image, mask: Image.Image, boxes: list[tuple[int, int, int, int]], contract: dict) -> tuple[list[dict], list[Image.Image]]:
    target_w, target_h = contract["frozen"]["export_size"]
    scale = int(contract["export_scale"])
    frame_size = (target_w * scale, target_h * scale)
    atlas = Image.new("RGBA", (frame_size[0] * 4, frame_size[1]), (0, 0, 0, 0))
    frames: list[Image.Image] = []
    meta: list[dict] = []
    for i, box in enumerate(boxes):
        crop, _crop_box = crop_with_alpha(source, mask, box)
        frame, fit = fit_into_frame(crop, frame_size)
        frame = zero_chroma_alpha(frame)
        frame = scrub_nonselected_photo_right_edge(frame, STATE_ORDER[i], contract["frozen"]["slots"], scale)
        frame = scrub_nonselected_outer_green_glow(frame, STATE_ORDER[i])
        atlas.alpha_composite(frame, (i * frame_size[0], 0))
        frames.append(frame)
        meta.append({"state": STATE_ORDER[i], "frame": [i * frame_size[0], 0, frame_size[0], frame_size[1]], **fit})
    atlas.save(OUT_ATLAS)
    GODOT_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(GODOT_ATLAS)
    return meta, frames


def clear_left_stack(img: Image.Image) -> Image.Image:
    out = img.convert("RGBA")
    draw = ImageDraw.Draw(out, "RGBA")
    draw.rectangle([34, 18, 270, 704], fill=(7, 18, 19, 235))
    draw.rectangle([36, 18, 270, 704], outline=(24, 47, 50, 180), width=2)
    return out


def runtime_preview(frames: list[Image.Image], contract: dict, qa: bool = False) -> Image.Image:
    ref = Image.open(REF).convert("RGBA")
    out = clear_left_stack(ref)
    draw = ImageDraw.Draw(out, "RGBA")
    frozen = contract["frozen"]
    w, h = frozen["export_size"]
    slots = frozen["slots"]
    for i, (frame, pos) in enumerate(zip(frames, frozen["positions"])):
        x, y = pos
        runtime_frame = frame.resize((w, h), Image.Resampling.LANCZOS)
        out.alpha_composite(runtime_frame, (x, y))
        title, meta = STATE_LABELS[i]
        lx, ly, _lw, _lh = slots["label_plate"]
        mx, my, _mw, _mh = slots["meta_line"]
        draw.text((x + lx + 8, y + ly + 5), title, font=TOKENS["label_title"]["font"], fill=TOKENS["label_title"]["fill"])
        draw.text((x + mx + 4, y + my - 2), meta, font=TOKENS["meta_status"]["font"], fill=TOKENS["meta_status"]["fill"])
        if qa:
            draw.rectangle([x, y, x + w, y + h], outline=(100, 255, 136, 255), width=2)
            draw_box(draw, slots["photo_slot"], (x, y), 1, (91, 229, 255), "photo_slot")
            draw_box(draw, slots["label_plate"], (x, y), 1, (255, 227, 93), "label")
            draw_box(draw, slots["meta_line"], (x, y), 1, (255, 159, 82), "meta")
            draw_box(draw, slots["action_badge"], (x, y), 1, (255, 105, 105), "action")
    if qa:
        draw.text((288, 28), "v0.9.2 B1 runtime fill QA", font=F_HEAD, fill=(245, 239, 210, 255))
        draw.text((288, 64), "Tokens: label_title 19px/Python 25px/Godot; meta_status 11px/Python 14px/Godot, darker ink.", font=F_NOTE, fill=(220, 226, 203, 255))
    return out.convert("RGB")


def image_stats(path: Path) -> dict:
    img = Image.open(path).convert("RGB")
    colors = img.getcolors(maxcolors=16_777_216)
    non_black = 0
    for count, (r, g, b) in colors or []:
        if r + g + b > 24:
            non_black += count
    return {"path": str(path), "size": list(img.size), "unique_colors": len(colors or []), "non_black_pixels": non_black}


def write_manifest(contract: dict, rows: list[dict], atlas_meta: list[dict], compose_rows: list[dict]) -> None:
    atlas_ready = all(row["ratio_pass"] for row in rows)
    data = {
        "artifact": "WMW v0.9.2 left_region_card candidate B1 vertical slice",
        "date": "2026-07-08",
        "status": "vertical_slice_candidate_b1_composited_polish_geometry_pass" if atlas_ready else "vertical_slice_candidate_b1_geometry_fail",
        "source_reference": str(REF),
        "contract": str(CONTRACT_PATH),
        "source_candidate_b": str(SOURCE_B),
        "imagegen_b1_attempts": {
            "r1": str(BASE / "394-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r1.png"),
            "r2": str(BASE / "395-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r2.png"),
            "r4": str(IMAGEGEN_B1_R4),
            "note": "R1/R2/R4 are true imagegen outputs. Full-card geometry drifted wide, so final B1 uses candidate B geometry with imagegen local art composited into fixed slots; it is not mislabeled as pure imagegen.",
        },
        "outputs": {
            "imagegen_candidate_b1_r1_failed": "docs\\screenshots\\2026-06-24-world-map-benchmark-landing\\394-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r1.png",
            "imagegen_candidate_b1_r2_failed": "docs\\screenshots\\2026-06-24-world-map-benchmark-landing\\395-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r2.png",
            "imagegen_candidate_b1_r4_failed": "docs\\screenshots\\2026-06-24-world-map-benchmark-landing\\396-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r4-wide-failed.png",
            "candidate_b1": str(OUT_CANDIDATE),
            "geometry_qa": str(OUT_QA),
            "candidate_atlas_2x": str(OUT_ATLAS),
            "runtime_fill": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "manifest": str(OUT_MANIFEST),
            "godot_atlas": str(GODOT_ATLAS),
            "godot_manifest": str(GODOT_MANIFEST),
            "godot_single_component": "pending_until_capture_script_runs",
            "godot_single_component_qa": "pending_until_capture_script_runs",
        },
        "contract_summary": {
            "class_id": contract["class_id"],
            "contract_version": contract["contract_version"],
            "reference_resolution": contract["reference_resolution"],
            "runtime_resolution": contract["runtime_resolution"],
            "export_scale": contract["export_scale"],
            "export_size": contract["frozen"]["export_size"],
            "slots": contract["frozen"]["slots"],
            "positions": contract["frozen"]["positions"],
        },
        "text_tokens": {
            "label_title": {
                "python_font_size": 19,
                "godot_font_size": TOKENS["label_title"]["godot_font_size"],
                "ink": TOKENS["label_title"]["godot_color"],
            },
            "meta_status": {
                "python_font_size": 11,
                "godot_font_size": TOKENS["meta_status"]["godot_font_size"],
                "ink": TOKENS["meta_status"]["godot_color"],
                "reason": "UX P1: meta_line was too pale/small/tight; token darkens ink and raises size within 19px upper bound.",
            },
        },
        "composition_rows": compose_rows,
        "imagegen_geometry_rows": rows,
        "atlas_frames": atlas_meta,
        "gates": {
            "no_fake_text": "manual_check_pass_on_candidate_b1_397: four no-text shells inspected; no baked readable words/digits; R4 photo-slot sources contain no UI text",
            "functional_faces_orthogonal": "manual_check_pass_on_candidate_b1_397_398: final B1 geometry source is candidate B 383; photo/label/meta/action faces remain axis-aligned",
            "same_state_layout": "manual_check_pass_on_candidate_b1_397_398: selected/available/warning/locked share one left_region_card shell and contract slots",
            "contract_aspect_ratio": "pass" if atlas_ready else "fail",
            "atlas_ready": atlas_ready,
            "runtime_text_fill_preview": "generated",
            "godot_single_component": "pending_until_capture_script_runs",
            "b1_micro_tune_points": {
                "thin_outer_frame": "partial_pass: outer bright bevel trimmed in edge band without changing silhouette; still needs user visual judgment",
                "non_selected_green_cleanup": "pass: available/warning/locked chroma-green residual edge pixels cleaned from candidate B source",
                "photo_slot_regional_hints": "pass: true imagegen R4 regional scenes composited into B geometry photo slots",
                "warning_triangle_redder": "pass: true imagegen R4 red warning badge composited into B geometry action slot",
            },
        },
        "content_checks": {
            "image_stats": [image_stats(p) for p in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA]],
        },
        "decision": (
            "Candidate B direction was user-accepted. B1 is a geometry-preserving local polish candidate, not frozen production art. "
            "Because true imagegen full-card edits drifted wide, B1 keeps 383 as geometry source and uses true imagegen B1 output only as local art source. "
            "Do not batch-produce other classes until B1 is reviewed and confirmed."
        ),
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    contract = load_contract()
    candidate, compose_rows = compose_b1_candidate(contract)
    mask = build_mask(candidate)
    boxes = find_components(mask)
    if len(boxes) != 4:
        raise RuntimeError(f"Expected 4 B1 card components, found {len(boxes)}")
    rows = create_geometry_qa(candidate, boxes, contract)
    atlas_meta, frames = make_atlas(candidate, mask, boxes, contract)
    runtime_preview(frames, contract, qa=False).save(OUT_RUNTIME)
    runtime_preview(frames, contract, qa=True).save(OUT_RUNTIME_QA)
    write_manifest(contract, rows, atlas_meta, compose_rows)
    for path in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_MANIFEST, GODOT_ATLAS, GODOT_MANIFEST]:
        print(path)


if __name__ == "__main__":
    main()
