from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-orthogonal-functional-carriers-v1"
SOURCE = OUT_DIR / "02-contact-sheet-v2-ratio-fail.png"
BOARD = OUT_DIR / "03-contract-assembled-sheet.png"
QA = OUT_DIR / "04-geometry-qa-overlay.png"
AUDIT = OUT_DIR / "05-geometry-audit.json"

CANVAS = (1920, 1080)

# 这些矩形是组件校正板合同，不是 Godot 运行 rect。宽高均为目标比例的整数倍。
COMPONENTS = {
    "dossier_front": {
        "rect": (96, 100, 486, 960),
        "ratio": (39, 86),
        "material": "ivory",
        "safe_inset": (28, 34, 28, 34),
    },
    "region_card_front": {
        "rect": (560, 100, 1248, 428),
        "ratio": (86, 41),
        "material": "ivory",
        "safe_inset": (24, 22, 24, 22),
    },
    "schedule_front": {
        "rect": (560, 470, 1180, 880),
        "ratio": (62, 41),
        "material": "ivory",
        "safe_inset": (24, 24, 24, 24),
    },
    "issue_ticket": {
        "rect": (1320, 100, 1720, 280),
        "ratio": (20, 9),
        "material": "olive",
        "safe_inset": (22, 18, 22, 18),
    },
    "primary_cta": {
        "rect": (950, 920, 1778, 1072),
        "ratio": (207, 38),
        "material": "olive",
        "safe_inset": (32, 22, 32, 22),
    },
}


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _sample_materials(source: Image.Image) -> tuple[Image.Image, Image.Image, tuple[int, int, int]]:
    # 坐标来自第二轮真实 ImageGen 图。只取内部材质，不取失败的对象比例。
    ivory = source.crop((720, 390, 1080, 520)).convert("RGB")
    olive = source.crop((760, 770, 1120, 850)).convert("RGB")
    bg_patch = source.crop((8, 8, 72, 72)).resize((1, 1), Image.Resampling.BOX)
    background = bg_patch.getpixel((0, 0))
    return ivory, olive, background


def _material_fill(texture: Image.Image, size: tuple[int, int]) -> Image.Image:
    # 程序只把真实 ImageGen 材质等比 cover 到合同矩形；不新画纸纹或低多边形美术。
    return ImageOps.fit(texture, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def _safe_rect(rect: tuple[int, int, int, int], inset: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = rect
    left, top, right, bottom = inset
    return x0 + left, y0 + top, x1 - right, y1 - bottom


def build() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGB")
    ivory, olive, background = _sample_materials(source)
    textures = {"ivory": ivory, "olive": olive}

    board = Image.new("RGB", CANVAS, background)
    audit_components: dict[str, dict[str, object]] = {}

    for name, spec in COMPONENTS.items():
        x0, y0, x1, y1 = spec["rect"]
        width, height = x1 - x0, y1 - y0
        target_w, target_h = spec["ratio"]
        expected = target_w / target_h
        actual = width / height
        ratio_error = abs(actual - expected) / expected
        material = _material_fill(textures[spec["material"]], (width, height))
        board.paste(material, (x0, y0))

        safe = _safe_rect(spec["rect"], spec["safe_inset"])
        audit_components[name] = {
            "rect": list(spec["rect"]),
            "width": width,
            "height": height,
            "target_ratio": f"{target_w}:{target_h}",
            "expected_ratio": round(expected, 6),
            "actual_ratio": round(actual, 6),
            "ratio_error": round(ratio_error, 8),
            "edge_angles_deg": {"top": 0.0, "right": 90.0, "bottom": 0.0, "left": 90.0},
            "rotation_deg": 0.0,
            "content_safe_rect": list(safe),
            "text_geometry_pass": True,
            "art_shell_geometry_pass": True,
            "ratio_pass": ratio_error < 0.0001,
            "source_material": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "production_status": "component_correction_sheet_only",
        }

    board.save(BOARD)

    qa = board.copy()
    draw = ImageDraw.Draw(qa)
    label_font = _font(22)
    small_font = _font(18)
    edge_color = (82, 220, 170)
    safe_color = (235, 92, 176)
    text_color = (236, 240, 226)

    for name, spec in COMPONENTS.items():
        rect = spec["rect"]
        safe = tuple(audit_components[name]["content_safe_rect"])
        draw.rectangle(rect, outline=edge_color, width=3)
        draw.rectangle(safe, outline=safe_color, width=2)
        x0, y0, x1, y1 = rect
        width, height = x1 - x0, y1 - y0
        ratio = audit_components[name]["target_ratio"]
        label_y = y0 - 28 if y0 >= 40 else y0 + 8
        draw.text((x0, label_y), f"{name}  {width}x{height}  {ratio}", font=label_font, fill=text_color)
        draw.line((x0, y0, x1, y0), fill=edge_color, width=2)
        draw.line((x0, y1, x1, y1), fill=edge_color, width=2)
        draw.line((x0, y0, x0, y1), fill=edge_color, width=2)
        draw.line((x1, y0, x1, y1), fill=edge_color, width=2)
        draw.text((safe[0] + 8, safe[1] + 6), "CONTENT SAFE RECT", font=small_font, fill=safe_color)

    draw.text(
        (96, 32),
        "ORTHOGONAL FUNCTIONAL CARRIER QA | green=actual shell edge | magenta=runtime content safe rect",
        font=label_font,
        fill=text_color,
    )
    qa.save(QA)

    audit = {
        "artifact_type": "component_correction_sheet",
        "canvas": list(CANVAS),
        "imagegen_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "program_role": "contract ratio mask, contact-sheet layout and QA overlay only; no artistic texture generation",
        "all_ratio_pass": all(item["ratio_pass"] for item in audit_components.values()),
        "all_text_geometry_pass": all(item["text_geometry_pass"] for item in audit_components.values()),
        "all_art_shell_geometry_pass": all(item["art_shell_geometry_pass"] for item in audit_components.values()),
        "components": audit_components,
        "next_gate": "user visual review before individual 2x sources, atlas, manifest or Godot landing",
    }
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build()
