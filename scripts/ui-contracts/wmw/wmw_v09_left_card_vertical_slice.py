from __future__ import annotations

import json
import shutil
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"D:\angos")
BASE = ROOT / "docs/screenshots/2026-06-24-world-map-benchmark-landing"
REF = ROOT / ".codex-remote-attachments/019ef3f7-be2f-70d3-ae57-7df7fa181048/285fb7d4-37f0-4a98-86f4-c1652013a1d1/1-Photo-1.jpg"
CONTRACT_PATH = ROOT / "design/ui-contracts/world-map/left_region_card.json"

IMAGEGEN_SOURCE = Path(
    r"C:\Users\gzfangyue\.codex\generated_images\019ef3f7-be2f-70d3-ae57-7df7fa181048\ig_051b13bf76701c50016a4df1f06e248191a349c4386bc88525.png"
)

OUT_CANDIDATE = BASE / "374-world-map-wmw-v0-9-left-card-imagegen-candidate-a.png"
OUT_QA = BASE / "375-world-map-wmw-v0-9-left-card-imagegen-candidate-a-geometry-qa.png"
OUT_ATLAS = BASE / "376-world-map-wmw-v0-9-left-card-candidate-atlas-2x.png"
OUT_RUNTIME = BASE / "377-world-map-wmw-v0-9-left-card-vertical-slice-runtime-fill.png"
OUT_RUNTIME_QA = BASE / "378-world-map-wmw-v0-9-left-card-vertical-slice-runtime-fill-qa.png"
OUT_MANIFEST = BASE / "379-world-map-wmw-v0-9-left-card-vertical-slice-manifest.json"

GODOT_ASSET_DIR = ROOT / "gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice"
GODOT_ATLAS = GODOT_ASSET_DIR / "left_region_card_candidate_atlas_2x.png"
GODOT_MANIFEST = GODOT_ASSET_DIR / "left_region_card_candidate_manifest.json"

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

F_TITLE = font(FONT_BOLD, 19)
F_META = font(FONT_REGULAR, 10)
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


def crop_with_alpha(source: Image.Image, mask: Image.Image, box: tuple[int, int, int, int], pad: int = 8) -> Image.Image:
    x1, y1, x2, y2 = box
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(source.width, x2 + pad)
    y2 = min(source.height, y2 + pad)
    crop = source.crop((x1, y1, x2, y2)).convert("RGBA")
    alpha = mask.crop((x1, y1, x2, y2))
    crop.putalpha(alpha)
    return crop


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
    draw.text((32, 24), "WMW v0.9 left_region_card imagegen candidate geometry QA", font=F_HEAD, fill="#f1ead0")
    draw.text((32, 60), "Green boxes are detected card bboxes. Red result means imagegen art is not atlas-ready; do not resize it silently.", font=F_NOTE, fill="#d9dec7")

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
    draw.text((x0, y0 + 32), "States must share one class geometry.", font=F_SMALL, fill="#d9dec7")
    for i, row in enumerate(rows):
        y = y0 + 80 + i * 112
        color = "#88ff9d" if row["ratio_pass"] else "#ff6969"
        result = "PASS" if row["ratio_pass"] else "FAIL"
        draw.text((x0, y), f"{row['state']}: {result}", font=F_NOTE, fill=color)
        draw.text((x0, y + 30), f"bbox {row['detected_bbox'][2]}x{row['detected_bbox'][3]}  ratio {row['detected_ratio']}", font=F_SMALL, fill="#e2dfc8")
        draw.text((x0, y + 52), f"target ratio {row['target_ratio']}  delta {row['ratio_delta']}", font=F_SMALL, fill="#e2dfc8")

    if all(r["ratio_pass"] for r in rows):
        verdict = "atlas-ready geometry candidate"
        vcolor = "#88ff9d"
    else:
        verdict = "NOT atlas-ready: regenerate/edit art against wireframe; keep contract unchanged"
        vcolor = "#ff6969"
    draw.text((32, 842), f"Verdict: {verdict}", font=F_HEAD, fill=vcolor)
    draw.text((32, 884), "QA is intentionally strict: correcting this by squashing/cropping would recreate the earlier asset/UI mismatch problem.", font=F_NOTE, fill="#d9dec7")
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
        crop = crop_with_alpha(source, mask, box)
        frame, fit = fit_into_frame(crop, frame_size)
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
        lx, ly, lw, lh = slots["label_plate"]
        mx, my, mw, mh = slots["meta_line"]
        draw.text((x + lx + 8, y + ly + 5), title, font=F_TITLE, fill=(23, 26, 23, 245))
        draw.text((x + mx + 4, y + my - 1), meta, font=F_META, fill=(115, 42, 34, 230))
        if qa:
            draw.rectangle([x, y, x + w, y + h], outline=(100, 255, 136, 255), width=2)
            draw_box(draw, slots["photo_slot"], (x, y), 1, (91, 229, 255), "photo_slot")
            draw_box(draw, slots["label_plate"], (x, y), 1, (255, 227, 93), "label")
            draw_box(draw, slots["meta_line"], (x, y), 1, (255, 159, 82), "meta")
            draw_box(draw, slots["action_badge"], (x, y), 1, (255, 105, 105), "action")
    if qa:
        draw.text((288, 28), "v0.9 left_card vertical slice runtime fill QA", font=F_HEAD, fill=(245, 239, 210, 255))
        draw.text((288, 64), "This uses the generated no-text atlas with contract slots and real runtime text. Red/Yellow/Cyan boxes are contract slots.", font=F_NOTE, fill=(220, 226, 203, 255))
    return out.convert("RGB")


def write_manifest(contract: dict, rows: list[dict], atlas_meta: list[dict]) -> None:
    atlas_ready = all(row["ratio_pass"] for row in rows)
    data = {
        "artifact": "WMW v0.9 left_region_card vertical slice",
        "date": "2026-07-08",
        "status": "vertical_slice_candidate_needs_art_review",
        "source_reference": str(REF),
        "contract": str(CONTRACT_PATH),
        "imagegen_source": str(IMAGEGEN_SOURCE),
        "outputs": {
            "wireframe_prompt_anchor": str(BASE / "373-world-map-wmw-v0-9-left-card-wireframe-prompt-anchor.png"),
            "imagegen_candidate": str(OUT_CANDIDATE),
            "geometry_qa": str(OUT_QA),
            "candidate_atlas_2x": str(OUT_ATLAS),
            "runtime_fill": str(OUT_RUNTIME),
            "runtime_fill_qa": str(OUT_RUNTIME_QA),
            "manifest": str(OUT_MANIFEST),
            "godot_atlas": str(GODOT_ATLAS),
            "godot_manifest": str(GODOT_MANIFEST),
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
        "imagegen_geometry_rows": rows,
        "atlas_frames": atlas_meta,
        "gates": {
            "no_fake_text": "manual_check_pass_on_candidate_a",
            "functional_faces_orthogonal": "manual_check_pass_on_candidate_a",
            "same_state_layout": "manual_check_pass_on_candidate_a",
            "contract_aspect_ratio": "pass" if atlas_ready else "fail",
            "atlas_ready": atlas_ready,
            "runtime_text_fill_preview": "generated",
            "godot_single_component": "pending_until_capture_script_runs",
        },
        "decision": (
            "Generated art is suitable for workflow review, but not final atlas if contract_aspect_ratio is fail. "
            "Do not squash/crop to hide the failure; regenerate/edit from the wireframe anchor or hand-fix art while preserving left_region_card.json."
        ),
    }
    OUT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    GODOT_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if not IMAGEGEN_SOURCE.exists():
        raise FileNotFoundError(IMAGEGEN_SOURCE)
    BASE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(IMAGEGEN_SOURCE, OUT_CANDIDATE)
    contract = load_contract()
    source = Image.open(OUT_CANDIDATE).convert("RGB")
    mask = build_mask(source)
    boxes = find_components(mask)
    if len(boxes) != 4:
        raise RuntimeError(f"Expected 4 card components, found {len(boxes)}")
    rows = create_geometry_qa(source, boxes, contract)
    atlas_meta, frames = make_atlas(source, mask, boxes, contract)
    runtime_preview(frames, contract, qa=False).save(OUT_RUNTIME)
    runtime_preview(frames, contract, qa=True).save(OUT_RUNTIME_QA)
    write_manifest(contract, rows, atlas_meta)
    for path in [OUT_CANDIDATE, OUT_QA, OUT_ATLAS, OUT_RUNTIME, OUT_RUNTIME_QA, OUT_MANIFEST, GODOT_ATLAS, GODOT_MANIFEST]:
        print(path)


if __name__ == "__main__":
    main()
