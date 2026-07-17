#!/usr/bin/env python3
"""校验文字 QA manifest 是否使用真实光栅字形 bbox。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


REQUIRED = {
    "bbox",
    "raster_glyph_bbox",
    "inner_rect",
    "glyph_bbox_inside_inner_rect",
    "bbox_source",
    "manual_y_offset_px",
    "font_source",
    "draw_origin",
    "raster_bbox_relative_to_draw_origin",
}


def independent_raster_bbox(text: str, font_source: str, font_size: int) -> list[int]:
    """独立重放 Pillow 光栅化，不调用生产侧 bbox helper。"""
    font = ImageFont.truetype(font_source, font_size)
    metric_draw = ImageDraw.Draw(Image.new("L", (1, 1), 0))
    metric_bbox = tuple(metric_draw.textbbox((0, 0), text, font=font))
    width = max(1, metric_bbox[2] - metric_bbox[0])
    height = max(1, metric_bbox[3] - metric_bbox[1])
    padding = 8
    probe = Image.new("L", (width + padding * 2, height + padding * 2), 0)
    origin = (padding - metric_bbox[0], padding - metric_bbox[1])
    ImageDraw.Draw(probe).text(origin, text, font=font, fill=255)
    alpha_bbox = probe.getbbox()
    if alpha_bbox is None:
        raise ValueError(f"文字未渲染出 alpha 像素: {text!r}")
    return [
        alpha_bbox[0] - origin[0],
        alpha_bbox[1] - origin[1],
        alpha_bbox[2] - origin[0],
        alpha_bbox[3] - origin[1],
    ]


def collect_reports(value: Any, reports: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if {"field", "text", "font_size", "rect"}.issubset(value):
            reports.append(value)
        for child in value.values():
            collect_reports(child, reports)
    elif isinstance(value, list):
        for child in value:
            collect_reports(child, reports)


def validate(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    reports: list[dict[str, Any]] = []
    collect_reports(data.get("text_capacity", data), reports)
    errors: list[str] = []
    if not reports:
        return ["没有找到包含 field/text/font_size/rect 的原始文字报告"]
    for index, report in enumerate(reports):
        name = report.get("field", f"report_{index}")
        missing = sorted(REQUIRED - set(report))
        if missing:
            errors.append(f"{name}: 缺少字段 {missing}")
            continue
        if report["bbox_source"] != "raster_alpha_bbox":
            errors.append(f"{name}: bbox_source={report['bbox_source']!r}")
        if report["bbox"] != report["raster_glyph_bbox"]:
            errors.append(f"{name}: overlay bbox 与 raster_glyph_bbox 不一致")
        if report["glyph_bbox_inside_inner_rect"] is not True:
            errors.append(f"{name}: 实际光栅字形未完整落入 inner_rect")
        if report["manual_y_offset_px"] != 0:
            errors.append(f"{name}: 存在 manual_y_offset_px={report['manual_y_offset_px']}")
        font_source = report["font_source"]
        if not font_source or not Path(font_source).is_file():
            errors.append(f"{name}: font_source 不可重放: {font_source!r}")
            continue
        try:
            independent_relative = independent_raster_bbox(
                report["text"], font_source, report["font_size"]
            )
        except (OSError, ValueError) as error:
            errors.append(f"{name}: 独立光栅重放失败: {error}")
            continue
        if independent_relative != report["raster_bbox_relative_to_draw_origin"]:
            errors.append(f"{name}: manifest 相对 bbox 与独立光栅重放不一致")
        origin = report["draw_origin"]
        independent_absolute = [
            origin[0] + independent_relative[0],
            origin[1] + independent_relative[1],
            origin[0] + independent_relative[2],
            origin[1] + independent_relative[3],
        ]
        if independent_absolute != report["raster_glyph_bbox"]:
            errors.append(f"{name}: manifest 绝对 bbox 与独立光栅重放不一致")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("用法: python scripts/ui-contracts/validate_text_bbox_evidence.py <manifest.json> [...]")
        return 2
    failed = False
    for arg in argv[1:]:
        path = Path(arg)
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
