from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from wmw_text_layout_metrics import draw_text_by_raster_bbox


FONT_PATHS = [
    Path(r"C:\Windows\Fonts\msyhbd.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
]


def load_font(size: int) -> ImageFont.ImageFont:
    for path in FONT_PATHS:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def main() -> None:
    cases = [
        ("北美禁区警戒带", 32, "left"),
        ("高危", 26, "center"),
        ("推荐12", 19, "center"),
        ("ABCgj", 24, "right"),
    ]
    for text, size, align in cases:
        canvas = Image.new("RGBA", (360, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        report = draw_text_by_raster_bbox(
            draw,
            (20, 10, 340, 90),
            text,
            load_font(size),
            (255, 255, 255, 255),
            align=align,
            pad_x=8,
            pad_y=6,
        )
        actual_alpha_bbox = canvas.getchannel("A").getbbox()
        assert actual_alpha_bbox == tuple(report["raster_glyph_bbox"]), (text, actual_alpha_bbox, report)
        assert report["glyph_bbox_inside_inner_rect"] is True, (text, report)
        assert report["bbox_source"] == "raster_alpha_bbox"
        assert report["manual_y_offset_px"] == 0
    print(f"PASS raster glyph bbox cases={len(cases)}")


if __name__ == "__main__":
    main()
