from __future__ import annotations

from typing import Any, Callable, Literal

from PIL import Image, ImageDraw, ImageFont


Rect = tuple[int, int, int, int]
Align = Literal["left", "center", "right"]
FontFactory = Callable[[int], ImageFont.ImageFont]


def raster_relative_bbox(text: str, font: ImageFont.ImageFont) -> dict[str, Any]:
    """返回相对 draw.text 原点的字体 metric bbox 与真实 alpha bbox。"""
    metric_probe = Image.new("L", (1, 1), 0)
    metric_draw = ImageDraw.Draw(metric_probe)
    metric_bbox = tuple(metric_draw.textbbox((0, 0), text, font=font))
    metric_w = max(1, metric_bbox[2] - metric_bbox[0])
    metric_h = max(1, metric_bbox[3] - metric_bbox[1])
    padding = 8
    probe = Image.new("L", (metric_w + padding * 2, metric_h + padding * 2), 0)
    probe_draw = ImageDraw.Draw(probe)
    probe_origin = (padding - metric_bbox[0], padding - metric_bbox[1])
    probe_draw.text(probe_origin, text, font=font, fill=255)
    alpha_bbox = probe.getbbox()
    if alpha_bbox is None:
        raise ValueError(f"文字未渲染出任何 alpha 像素: {text!r}")
    raster_bbox = (
        alpha_bbox[0] - probe_origin[0],
        alpha_bbox[1] - probe_origin[1],
        alpha_bbox[2] - probe_origin[0],
        alpha_bbox[3] - probe_origin[1],
    )
    font_source_value = getattr(font, "path", None)
    if isinstance(font_source_value, bytes):
        font_source_value = font_source_value.decode(errors="replace")
    font_source = str(font_source_value) if font_source_value else None
    try:
        font_name = list(font.getname())
    except (AttributeError, OSError):
        font_name = None
    return {
        "font_source": font_source,
        "font_name": font_name,
        "metric_bbox_relative_to_draw_origin": list(metric_bbox),
        "raster_bbox_relative_to_draw_origin": list(raster_bbox),
        "raster_size": [raster_bbox[2] - raster_bbox[0], raster_bbox[3] - raster_bbox[1]],
    }


def raster_text_size(text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    metrics = raster_relative_bbox(text, font)
    return tuple(metrics["raster_size"])


def fit_font_by_raster(
    text: str,
    font_factory: FontFactory,
    max_size: int,
    min_size: int,
    box: tuple[int, int],
) -> tuple[ImageFont.ImageFont, int, bool, dict[str, Any]]:
    for size in range(max_size, min_size - 1, -1):
        font = font_factory(size)
        metrics = raster_relative_bbox(text, font)
        width, height = metrics["raster_size"]
        if width <= box[0] and height <= box[1]:
            return font, size, True, metrics
    font = font_factory(min_size)
    return font, min_size, False, raster_relative_bbox(text, font)


def rect_contains(outer: Rect, inner: Rect) -> bool:
    return (
        inner[0] >= outer[0]
        and inner[1] >= outer[1]
        and inner[2] <= outer[2]
        and inner[3] <= outer[3]
    )


def draw_text_by_raster_bbox(
    draw: ImageDraw.ImageDraw,
    rect: Rect,
    text: str,
    font: ImageFont.ImageFont,
    fill: Any,
    *,
    align: Align = "left",
    pad_x: int = 0,
    pad_y: int = 0,
) -> dict[str, Any]:
    """按真实光栅字形 bbox 对齐，并返回同源 QA 证据。"""
    inner_rect = (
        rect[0] + pad_x,
        rect[1] + pad_y,
        rect[2] - pad_x,
        rect[3] - pad_y,
    )
    metrics = raster_relative_bbox(text, font)
    raster_relative = tuple(metrics["raster_bbox_relative_to_draw_origin"])
    glyph_w, glyph_h = metrics["raster_size"]
    inner_w = inner_rect[2] - inner_rect[0]
    inner_h = inner_rect[3] - inner_rect[1]

    if align == "center":
        glyph_left = inner_rect[0] + (inner_w - glyph_w) // 2
    elif align == "right":
        glyph_left = inner_rect[2] - glyph_w
    else:
        glyph_left = inner_rect[0]
    glyph_top = inner_rect[1] + (inner_h - glyph_h) // 2
    draw_origin = (
        glyph_left - raster_relative[0],
        glyph_top - raster_relative[1],
    )
    draw.text(draw_origin, text, font=font, fill=fill)

    raster_bbox = (
        draw_origin[0] + raster_relative[0],
        draw_origin[1] + raster_relative[1],
        draw_origin[0] + raster_relative[2],
        draw_origin[1] + raster_relative[3],
    )
    metric_relative = tuple(metrics["metric_bbox_relative_to_draw_origin"])
    metric_bbox = (
        draw_origin[0] + metric_relative[0],
        draw_origin[1] + metric_relative[1],
        draw_origin[0] + metric_relative[2],
        draw_origin[1] + metric_relative[3],
    )
    inside = rect_contains(inner_rect, raster_bbox)
    margins = {
        "left": raster_bbox[0] - inner_rect[0],
        "top": raster_bbox[1] - inner_rect[1],
        "right": inner_rect[2] - raster_bbox[2],
        "bottom": inner_rect[3] - raster_bbox[3],
    }
    return {
        "font_source": metrics["font_source"],
        "font_name": metrics["font_name"],
        "draw_origin": list(draw_origin),
        "inner_rect": list(inner_rect),
        "font_metric_bbox": list(metric_bbox),
        "font_metric_bbox_relative_to_draw_origin": list(metric_relative),
        "raster_glyph_bbox": list(raster_bbox),
        "raster_bbox_relative_to_draw_origin": list(raster_relative),
        "glyph_size": [glyph_w, glyph_h],
        "glyph_margins": margins,
        "glyph_bbox_inside_inner_rect": inside,
        "bbox_source": "raster_alpha_bbox",
        "manual_y_offset_px": 0,
    }
