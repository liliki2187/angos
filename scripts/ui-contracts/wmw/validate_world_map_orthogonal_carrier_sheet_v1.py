from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "image_gen" / "2026-08-07" / "world-map-orthogonal-functional-carriers-v1"
BOARD = OUT_DIR / "03-contract-assembled-sheet.png"
CONTRACT_AUDIT = OUT_DIR / "05-geometry-audit.json"
VALIDATION = OUT_DIR / "06-independent-geometry-validation.json"
DETECTED_QA = OUT_DIR / "07-detected-edge-qa.png"


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/arial.ttf")):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(sum((int(x) - int(y)) ** 2 for x, y in zip(a, b)))


def _fit_angle(points: list[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 999.0
    mean_x = sum(p[0] for p in points) / len(points)
    mean_y = sum(p[1] for p in points) / len(points)
    denom = sum((p[0] - mean_x) ** 2 for p in points)
    if denom == 0:
        return 90.0
    slope = sum((p[0] - mean_x) * (p[1] - mean_y) for p in points) / denom
    return math.degrees(math.atan(slope))


def _detect_bbox(
    image: Image.Image,
    expected: tuple[int, int, int, int],
    background: tuple[int, int, int],
    threshold: float = 55.0,
) -> tuple[int, int, int, int]:
    ex0, ey0, ex1, ey1 = expected
    sx0, sy0 = max(0, ex0 - 16), max(0, ey0 - 16)
    sx1, sy1 = min(image.width, ex1 + 16), min(image.height, ey1 + 16)
    xs: list[int] = []
    ys: list[int] = []
    px = image.load()
    for y in range(sy0, sy1):
        for x in range(sx0, sx1):
            if _distance(px[x, y], background) >= threshold:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise RuntimeError(f"No foreground detected around {expected}")
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def _edge_angles(
    image: Image.Image,
    bbox: tuple[int, int, int, int],
    background: tuple[int, int, int],
    threshold: float = 55.0,
) -> dict[str, float]:
    x0, y0, x1, y1 = bbox
    px = image.load()
    top: list[tuple[float, float]] = []
    bottom: list[tuple[float, float]] = []
    left_as_xy: list[tuple[float, float]] = []
    right_as_xy: list[tuple[float, float]] = []

    for x in range(x0, x1, max(1, (x1 - x0) // 120)):
        top_y = next((y for y in range(y0, y1) if _distance(px[x, y], background) >= threshold), None)
        bottom_y = next((y for y in range(y1 - 1, y0 - 1, -1) if _distance(px[x, y], background) >= threshold), None)
        if top_y is not None:
            top.append((x, top_y))
        if bottom_y is not None:
            bottom.append((x, bottom_y))

    # 对竖边以 y 为自变量、x 为因变量，得到相对竖直方向的偏角。
    for y in range(y0, y1, max(1, (y1 - y0) // 120)):
        left_x = next((x for x in range(x0, x1) if _distance(px[x, y], background) >= threshold), None)
        right_x = next((x for x in range(x1 - 1, x0 - 1, -1) if _distance(px[x, y], background) >= threshold), None)
        if left_x is not None:
            left_as_xy.append((y, left_x))
        if right_x is not None:
            right_as_xy.append((y, right_x))

    return {
        "top_from_horizontal": round(_fit_angle(top), 6),
        "bottom_from_horizontal": round(_fit_angle(bottom), 6),
        "left_from_vertical": round(_fit_angle(left_as_xy), 6),
        "right_from_vertical": round(_fit_angle(right_as_xy), 6),
    }


def validate() -> None:
    image = Image.open(BOARD).convert("RGB")
    contract = json.loads(CONTRACT_AUDIT.read_text(encoding="utf-8"))
    background = image.getpixel((0, 0))
    results: dict[str, dict[str, object]] = {}
    qa = image.copy()
    draw = ImageDraw.Draw(qa)
    font = _font(20)

    for name, item in contract["components"].items():
        expected = tuple(item["rect"])
        detected = _detect_bbox(image, expected, background)
        x0, y0, x1, y1 = detected
        width, height = x1 - x0, y1 - y0
        target_ratio = float(item["expected_ratio"])
        actual_ratio = width / height
        ratio_error = abs(actual_ratio - target_ratio) / target_ratio
        angles = _edge_angles(image, detected, background)
        max_abs_angle = max(abs(float(v)) for v in angles.values())
        bbox_delta = [detected[i] - expected[i] for i in range(4)]
        passed = max_abs_angle <= 1.0 and ratio_error <= 0.005 and max(abs(v) for v in bbox_delta) <= 1
        results[name] = {
            "expected_rect": list(expected),
            "detected_rect_from_bitmap": list(detected),
            "bbox_delta_px": bbox_delta,
            "detected_width": width,
            "detected_height": height,
            "actual_ratio_from_bitmap": round(actual_ratio, 6),
            "target_ratio": item["target_ratio"],
            "ratio_error": round(ratio_error, 8),
            "edge_angles_deg": angles,
            "max_abs_edge_angle_deg": round(max_abs_angle, 6),
            "pass": passed,
        }
        color = (255, 224, 74) if passed else (255, 75, 75)
        draw.rectangle(detected, outline=color, width=4)
        draw.text((x0 + 8, y0 + 8), f"{name}: {'PASS' if passed else 'FAIL'}", font=font, fill=color)

    payload = {
        "validator": "independent bitmap-edge scan",
        "background_rgb": list(background),
        "foreground_distance_threshold": 55,
        "angle_limit_deg": 1.0,
        "ratio_error_limit": 0.005,
        "bbox_delta_limit_px": 1,
        "all_pass": all(item["pass"] for item in results.values()),
        "components": results,
    }
    VALIDATION.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    qa.save(DETECTED_QA)


if __name__ == "__main__":
    validate()
