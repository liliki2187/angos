#!/usr/bin/env python3
"""校验主 / 副头版暖纸色接近度与副头版输出尺寸。"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageStat


def srgb_to_lab(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    values = []
    for value in rgb:
        value /= 255.0
        values.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    r, g, b = values
    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883

    def f(value: float) -> float:
        return value ** (1 / 3) if value > 0.008856 else 7.787 * value + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e_2000(lab1: tuple[float, float, float], lab2: tuple[float, float, float]) -> float:
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    c_bar = (c1 + c2) / 2
    g = 0.5 * (1 - math.sqrt(c_bar**7 / (c_bar**7 + 25**7)))
    ap1, ap2 = (1 + g) * a1, (1 + g) * a2
    cp1, cp2 = math.hypot(ap1, b1), math.hypot(ap2, b2)

    def hp(ap: float, b: float) -> float:
        angle = math.degrees(math.atan2(b, ap))
        return angle + 360 if angle < 0 else angle

    hp1, hp2 = hp(ap1, b1), hp(ap2, b2)
    dl = l2 - l1
    dc = cp2 - cp1
    dh_raw = hp2 - hp1
    if cp1 * cp2 == 0:
        dh = 0.0
    elif abs(dh_raw) <= 180:
        dh = dh_raw
    elif dh_raw > 180:
        dh = dh_raw - 360
    else:
        dh = dh_raw + 360
    dh_term = 2 * math.sqrt(cp1 * cp2) * math.sin(math.radians(dh / 2))
    l_bar = (l1 + l2) / 2
    cp_bar = (cp1 + cp2) / 2
    if cp1 * cp2 == 0:
        hp_bar = hp1 + hp2
    elif abs(hp1 - hp2) <= 180:
        hp_bar = (hp1 + hp2) / 2
    elif hp1 + hp2 < 360:
        hp_bar = (hp1 + hp2 + 360) / 2
    else:
        hp_bar = (hp1 + hp2 - 360) / 2
    t = (
        1
        - 0.17 * math.cos(math.radians(hp_bar - 30))
        + 0.24 * math.cos(math.radians(2 * hp_bar))
        + 0.32 * math.cos(math.radians(3 * hp_bar + 6))
        - 0.20 * math.cos(math.radians(4 * hp_bar - 63))
    )
    sl = 1 + 0.015 * (l_bar - 50) ** 2 / math.sqrt(20 + (l_bar - 50) ** 2)
    sc = 1 + 0.045 * cp_bar
    sh = 1 + 0.015 * cp_bar * t
    delta_theta = 30 * math.exp(-((hp_bar - 275) / 25) ** 2)
    rc = 2 * math.sqrt(cp_bar**7 / (cp_bar**7 + 25**7))
    rt = -rc * math.sin(math.radians(2 * delta_theta))
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dh_term / sh) ** 2 + rt * (dc / sc) * (dh_term / sh))


def paper_mean(path: Path) -> tuple[list[float], int]:
    image = Image.open(path).convert("RGB")
    warm_pixels = []
    for r, g, b in image.getdata():
        if r >= 135 and g >= 115 and b >= 78 and r >= b * 1.22 and g >= b * 1.12:
            warm_pixels.append((r, g, b))
    if not warm_pixels:
        raise RuntimeError(f"没有在 {path} 找到暖纸样本")
    sample = Image.new("RGB", (len(warm_pixels), 1))
    sample.putdata(warm_pixels)
    return list(ImageStat.Stat(sample).mean), len(warm_pixels)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    main_path = repo / "gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-main-head-slot-base-v1.png"
    secondary_path = repo / "gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-secondary-head-slot-base-v2.png"
    out_path = repo / "docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/asset-qa.json"
    main_rgb, main_count = paper_mean(main_path)
    secondary_rgb, secondary_count = paper_mean(secondary_path)
    main_lab = srgb_to_lab(tuple(main_rgb))
    secondary_lab = srgb_to_lab(tuple(secondary_rgb))
    delta_e = delta_e_2000(main_lab, secondary_lab)
    secondary_size = list(Image.open(secondary_path).size)
    checks = {
        "secondary_size_884x684": secondary_size == [884, 684],
        "paper_delta_e00_lte_3": delta_e <= 3.0,
        "paper_abs_delta_l_lte_2_5": abs(main_lab[0] - secondary_lab[0]) <= 2.5,
    }
    result = {
        "passed": all(checks.values()),
        "checks": checks,
        "main_paper_mean_rgb": [round(v, 3) for v in main_rgb],
        "secondary_paper_mean_rgb": [round(v, 3) for v in secondary_rgb],
        "main_paper_sample_count": main_count,
        "secondary_paper_sample_count": secondary_count,
        "delta_e00": round(delta_e, 4),
        "delta_l": round(secondary_lab[0] - main_lab[0], 4),
        "secondary_size": secondary_size,
        "method": "筛选暖纸像素后比较平均色；CIE Lab D65 与 CIEDE2000。",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
