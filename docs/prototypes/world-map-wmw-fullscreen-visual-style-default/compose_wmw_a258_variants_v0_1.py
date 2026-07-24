from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parent
FINAL_SIZE = (1920, 1080)

VARIANTS = [
    {
        "code": "1",
        "title": "浅靛鼠尾草 · 轻奇闻特刊",
        "source": ROOT / "wmw-a258-01-light-indigo-sage-v0-1-imagegen.png",
        "output": ROOT / "wmw-a258-01-light-indigo-sage-v0-1.png",
    },
    {
        "code": "2",
        "title": "暖纸柔珊瑚 · 怪新闻头版",
        "source": ROOT / "wmw-a258-02-warm-coral-frontpage-v0-1-imagegen.png",
        "output": ROOT / "wmw-a258-02-warm-coral-frontpage-v0-1.png",
    },
    {
        "code": "3",
        "title": "暮蓝陶土 · 午夜增刊",
        "source": ROOT / "wmw-a258-03-dusk-terracotta-midnight-v0-1-imagegen.png",
        "output": ROOT / "wmw-a258-03-dusk-terracotta-midnight-v0-1.png",
    },
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for font_path in (
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ):
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(variant: dict[str, object]) -> dict[str, object]:
    source = Path(variant["source"])
    output = Path(variant["output"])
    image = Image.open(source).convert("RGB")
    source_size = image.size
    source_aspect = source_size[0] / source_size[1]
    final_aspect = FINAL_SIZE[0] / FINAL_SIZE[1]
    aspect_delta = abs(source_aspect - final_aspect)
    if aspect_delta > 0.002:
        raise RuntimeError(
            f"{source.name} 不是 16:9：{source_size}，aspect_delta={aspect_delta:.6f}"
        )
    final = image.resize(FINAL_SIZE, Image.Resampling.LANCZOS)
    final.save(output, optimize=True)
    stat = ImageStat.Stat(final)
    return {
        "source": str(source),
        "source_size": list(source_size),
        "source_sha256": sha256(source),
        "output": str(output),
        "output_size": list(final.size),
        "output_sha256": sha256(output),
        "mean_rgb": [round(value, 2) for value in stat.mean],
        "aspect_delta_from_16_9": round(aspect_delta, 8),
    }


def make_board() -> Path:
    board = Image.new("RGB", (3840, 2312), (7, 14, 20))
    draw = ImageDraw.Draw(board)
    font = load_font(34)
    placements = [(0, 0), (1920, 0), (960, 1156)]
    label_height = 64
    for variant, (x, y) in zip(VARIANTS, placements):
        draw.text(
            (x + 24, y + 12),
            f"{variant['code']}  {variant['title']}",
            fill=(238, 240, 235),
            font=font,
        )
        image = Image.open(variant["output"]).convert("RGB")
        board.paste(image, (x, y + label_height))
    output = ROOT / "wmw-a258-v0-1-comparison-board.png"
    board.save(output, optimize=True)
    return output


def main() -> None:
    variants = {variant["code"]: normalize(variant) for variant in VARIANTS}
    board = make_board()
    audit = {
        "status": "dual_reviewed_pending_user_selection",
        "decision_source": "A258",
        "generation_mode": "built-in imagegen",
        "program_role": "只做 16:9 尺寸归一化、拼版、哈希和基础图像审计；不重绘、不调色、不增加 UI 内容。",
        "final_size": list(FINAL_SIZE),
        "shared_asset_contract": {
            "layout_source": "A 怪新闻头版 v0.2",
            "left_region_images": 3,
            "right_hero_images": 1,
            "mission_thumbnail_images": 4,
            "total_rectangular_image_slots": 8,
            "mission_rows": 4,
            "cta_count": 1,
            "forbidden": [
                "multi_photo_collage",
                "irregular_image_mask",
                "title_over_image",
                "pure_white_paper",
                "bright_yellow_cta",
                "fake_text",
                "fake_controls",
            ],
        },
        "variants": variants,
        "comparison_board": str(board),
        "comparison_board_size": [3840, 2312],
        "review": {
            "ux": {
                "ranking": ["1", "2", "3"],
                "verdict": {
                    "1": "PASS_DIRECTION_P0_0_P1_1",
                    "2": "PASS_DIRECTION_P0_0_P1_2",
                    "3": "ITERATE_BOUNDARY_SAMPLE_P0_0_P1_2",
                },
                "summary": "方案 1 最轻、最不像军情；方案 2 更像可信怪新闻；方案 3 只建议作为深色边界样本。",
            },
            "ui": {
                "ranking": ["2", "1", "3"],
                "verdict": {
                    "1": "PASS_DIRECTION_P0_0_P1_1",
                    "2": "PASS_RECOMMENDED_DIRECTION_P0_0_P1_2",
                    "3": "ITERATE_BOUNDARY_SAMPLE_P0_0_P1_3",
                },
                "summary": "方案 2 最完整实现 A 的生产骨架与 C 的轻快邀请感；方案 1 语义最稳；方案 3 偏暗。",
            },
            "parent_conclusion": "方案 1 和 2 可作为正式二选一，方案 3 作为更暗悬疑的边界对照；三套均不是 runtime filled-state。",
        },
    }
    audit_path = ROOT / "wmw-a258-v0-1-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(board)
    print(audit_path)


if __name__ == "__main__":
    main()
