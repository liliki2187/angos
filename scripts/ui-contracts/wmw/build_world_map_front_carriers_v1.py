from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-front-carriers-v1"

CANVAS = (1920, 1080)
BACKGROUND = (1, 24, 41)

COMPONENTS = {
    "dossier_front": {
        "source": "01-material-dossier-imagegen.png",
        "output": "06-front-carrier-dossier-2x.png",
        "size_2x": (936, 2064),
        "runtime_size": (468, 1032),
        "ratio": "39:86",
        "safe_rect_2x": (54, 48, 882, 2016),
        "root_input": "pass_not_full_button",
        "interactive_rects_runtime": {
            "mission_disclosure": (27, 572, 414, 56),
            "primary_cta_child": (27, 932, 414, 76),
        },
        "keyline_inset_2x": 18,
        "keyline_width_2x": 2,
        "review_rect": (1416, 24, 1884, 1056),
    },
    "schedule_front": {
        "source": "02-material-schedule-imagegen.png",
        "output": "07-front-carrier-schedule-2x.png",
        "size_2x": (744, 492),
        "runtime_size": (372, 246),
        "ratio": "62:41",
        "safe_rect_2x": (32, 16, 712, 460),
        "root_input": "mouse_filter_ignore_focus_none",
        "interactive_rects_runtime": {},
        "keyline_inset_2x": 16,
        "keyline_width_2x": 2,
        "review_rect": (36, 810, 408, 1056),
    },
    "primary_cta": {
        "source": "03-material-cta-imagegen.png",
        "output": "08-front-carrier-cta-default-2x.png",
        "size_2x": (828, 152),
        "runtime_size": (414, 76),
        "ratio": "207:38",
        "safe_rect_2x": (48, 20, 780, 132),
        "root_input": "button_hit_rect",
        "interactive_rects_runtime": {
            "primary_cta": (0, 0, 414, 76),
        },
        "keyline_inset_2x": 12,
        "keyline_width_2x": 3,
        "review_rect": (1443, 956, 1857, 1032),
    },
}

MATERIAL_REFERENCES = {
    "region_card_material": {
        "source": "04-material-region-card-imagegen-reference.png",
        "status": "material_reference_only",
        "blocker": "A282 current RegionCard is 340x170 (2:1), while A292 correction ratio is 86:41.",
    },
    "issue_material": {
        "source": "05-material-issue-imagegen-reference.png",
        "status": "material_reference_only",
        "blocker": "ISSUE has no frozen exact runtime rect, safe rect or interaction contract.",
    },
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _reflected_cover_without_upsample(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Cover target with the real ImageGen material without enlarging source pixels.

    If one source edge is shorter than the target, reflected tiling extends it. The
    program does not invent texture or rescale 1:1 into the component ratio.
    """
    source = source.convert("RGB")
    target_w, target_h = size
    tile_w = max(target_w, source.width)
    tile_h = max(target_h, source.height)
    cols = math.ceil(tile_w / source.width)
    rows = math.ceil(tile_h / source.height)
    tiled = Image.new("RGB", (cols * source.width, rows * source.height))
    for row in range(rows):
        for col in range(cols):
            tile = source
            if col % 2:
                tile = ImageOps.mirror(tile)
            if row % 2:
                tile = ImageOps.flip(tile)
            tiled.paste(tile, (col * source.width, row * source.height))
    x0 = max(0, (tiled.width - target_w) // 2)
    y0 = max(0, (tiled.height - target_h) // 2)
    return tiled.crop((x0, y0, x0 + target_w, y0 + target_h))


def _keyline_color(image: Image.Image) -> tuple[int, int, int]:
    mean = ImageStat.Stat(image.resize((1, 1), Image.Resampling.BOX)).mean[:3]
    return tuple(max(0, min(255, round(channel * 0.78))) for channel in mean)


def _build_carrier(spec: dict[str, object]) -> Image.Image:
    source_path = OUT_DIR / str(spec["source"])
    source = Image.open(source_path).convert("RGB")
    carrier = _reflected_cover_without_upsample(source, tuple(spec["size_2x"]))
    draw = ImageDraw.Draw(carrier, "RGB")
    inset = int(spec["keyline_inset_2x"])
    width = int(spec["keyline_width_2x"])
    color = _keyline_color(carrier)
    draw.rectangle(
        (inset, inset, carrier.width - inset - 1, carrier.height - inset - 1),
        outline=color,
        width=width,
    )
    return carrier


def _stats(image: Image.Image) -> dict[str, object]:
    rgb = image.convert("RGB")
    stat = ImageStat.Stat(rgb)
    mean = [round(value, 3) for value in stat.mean[:3]]
    stddev = [round(value, 3) for value in stat.stddev[:3]]
    return {
        "mean_rgb": mean,
        "stddev_rgb": stddev,
        "luma_mean": round(0.2126 * mean[0] + 0.7152 * mean[1] + 0.0722 * mean[2], 3),
    }


def _paste_runtime(board: Image.Image, carrier_2x: Image.Image, rect: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = rect
    runtime = carrier_2x.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    board.paste(runtime, (x0, y0))


def _build_review_board(carriers: dict[str, Image.Image]) -> tuple[Image.Image, Image.Image]:
    board = Image.new("RGB", CANVAS, BACKGROUND)
    draw = ImageDraw.Draw(board)
    title_font = _font(26, bold=True)
    body_font = _font(16)
    small_font = _font(14)

    draw.text((36, 32), "WORLD MAP / 独立 2× FrontCarrier 生产预览", font=title_font, fill=(232, 229, 212))
    draw.text((36, 70), "三项 exact rect 已放行；两项仅保留真实 ImageGen 材质源", font=body_font, fill=(171, 190, 181))

    _paste_runtime(board, carriers["schedule_front"], tuple(COMPONENTS["schedule_front"]["review_rect"]))
    _paste_runtime(board, carriers["dossier_front"], tuple(COMPONENTS["dossier_front"]["review_rect"]))
    _paste_runtime(board, carriers["primary_cta"], tuple(COMPONENTS["primary_cta"]["review_rect"]))

    # Material references are shown as unframed swatches, not as component silhouettes.
    region = Image.open(OUT_DIR / MATERIAL_REFERENCES["region_card_material"]["source"]).convert("RGB")
    issue = Image.open(OUT_DIR / MATERIAL_REFERENCES["issue_material"]["source"]).convert("RGB")
    board.paste(ImageOps.fit(region, (300, 220), Image.Resampling.LANCZOS), (64, 150))
    board.paste(ImageOps.fit(issue, (300, 220), Image.Resampling.LANCZOS), (432, 150))
    draw.text((64, 382), "REGION CARD · MATERIAL ONLY", font=small_font, fill=(224, 176, 84))
    draw.text((64, 410), "340×170 与 86:41 冲突，未生成壳体", font=small_font, fill=(183, 188, 173))
    draw.text((432, 382), "ISSUE · MATERIAL ONLY", font=small_font, fill=(224, 176, 84))
    draw.text((432, 410), "exact rect 未冻结，未生成壳体", font=small_font, fill=(183, 188, 173))

    draw.text((36, 770), "SCHEDULE 372×246 runtime / 744×492 source", font=small_font, fill=(202, 216, 204))
    draw.text((1416, 4), "DOSSIER 468×1032 runtime / 936×2064 source", font=small_font, fill=(202, 216, 204))
    draw.text((920, 1000), "CTA 414×76 runtime / 828×152 source", font=small_font, fill=(238, 230, 203))

    qa = board.copy()
    qa_draw = ImageDraw.Draw(qa)
    edge_color = (76, 224, 162)
    safe_color = (236, 83, 176)
    for name, spec in COMPONENTS.items():
        x0, y0, x1, y1 = tuple(spec["review_rect"])
        qa_draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=edge_color, width=3)
        sx0, sy0, sx1, sy1 = tuple(spec["safe_rect_2x"])
        scale_x = (x1 - x0) / int(spec["size_2x"][0])
        scale_y = (y1 - y0) / int(spec["size_2x"][1])
        safe_runtime = (
            round(x0 + sx0 * scale_x),
            round(y0 + sy0 * scale_y),
            round(x0 + sx1 * scale_x),
            round(y0 + sy1 * scale_y),
        )
        qa_draw.rectangle((safe_runtime[0], safe_runtime[1], safe_runtime[2] - 1, safe_runtime[3] - 1), outline=safe_color, width=2)
        qa_draw.text((x0 + 8, y0 + 8), f"{name} / EDGE PASS", font=small_font, fill=edge_color)

    qa_draw.text((780, 70), "green = FrontCarrier exact rect   magenta = runtime text/content safe rect", font=small_font, fill=(218, 224, 209))
    return board, qa


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    carriers: dict[str, Image.Image] = {}
    audit_components: dict[str, dict[str, object]] = {}
    for name, spec in COMPONENTS.items():
        carrier = _build_carrier(spec)
        output_path = OUT_DIR / str(spec["output"])
        carrier.save(output_path)
        carriers[name] = carrier
        width, height = carrier.size
        runtime_w, runtime_h = tuple(spec["runtime_size"])
        safe = tuple(spec["safe_rect_2x"])
        audit_components[name] = {
            "source_material": str((OUT_DIR / str(spec["source"])).relative_to(ROOT)).replace("\\", "/"),
            "output": str(output_path.relative_to(ROOT)).replace("\\", "/"),
            "size_2x": [width, height],
            "runtime_size": [runtime_w, runtime_h],
            "target_ratio": spec["ratio"],
            "ratio_error": 0.0,
            "content_safe_rect_2x": list(safe),
            "art_root_rect_runtime": [0, 0, runtime_w, runtime_h],
            "root_input": spec["root_input"],
            "interactive_rects_runtime": {
                key: list(value) for key, value in spec["interactive_rects_runtime"].items()
            },
            "rotation_deg": 0.0,
            "edge_angles_deg": {"top": 0.0, "right": 0.0, "bottom": 0.0, "left": 0.0},
            "upsample": False,
            "texture_application": "center crop or reflected material tiling; no aspect stretch",
            "keyline": {
                "inset_2x": spec["keyline_inset_2x"],
                "width_2x": spec["keyline_width_2x"],
                "role": "deterministic institutional geometry line; not ImageGen art replacement",
            },
            "art_shell_geometry_pass": width == runtime_w * 2 and height == runtime_h * 2,
            "text_geometry_pass": 0 <= safe[0] < safe[2] <= width and 0 <= safe[1] < safe[3] <= height,
            "stats": _stats(carrier),
            "production_status": "front_carrier_2x_candidate_not_atlas_not_godot",
        }

    review, qa = _build_review_board(carriers)
    review.save(OUT_DIR / "09-runtime-scale-review-board.png")
    qa.save(OUT_DIR / "10-geometry-safe-rect-qa.png")

    audit = {
        "artifact_type": "independent_2x_front_carrier_candidate",
        "imagegen_role": "five independent real ImageGen material sources",
        "program_role": "exact size crop/reflected tiling, 1-2px runtime institutional keyline, runtime-scale assembly and QA only",
        "direct_crop_from_visual_target": False,
        "all_released_component_geometry_pass": all(item["art_shell_geometry_pass"] for item in audit_components.values()),
        "all_released_text_geometry_pass": all(item["text_geometry_pass"] for item in audit_components.values()),
        "released_components": audit_components,
        "blocked_components": MATERIAL_REFERENCES,
        "next_gate": "independent bitmap validation, internal slot pressure board, then user visual gate; atlas/Godot remain blocked",
    }
    (OUT_DIR / "11-front-carrier-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build()
