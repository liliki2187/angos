from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parent
SOURCE_SIZE = (1672, 941)
FINAL_SIZE = (1920, 1080)

TARGETS = {
    "left_cards": (22, 20, 373, 694),
    "schedule": (22, 707, 373, 920),
    "map": (393, 20, 1191, 920),
    "dossier": (1208, 20, 1649, 920),
}

VARIANTS = [
    {
        "code": "A",
        "title": "怪新闻头版",
        "source": ROOT / "wmw-adult-weird-weekly-01-news-frontpage-v0-2-imagegen.png",
        "output": ROOT / "wmw-adult-weird-weekly-01-news-frontpage-v0-2.png",
        "crops": {
            "left_cards": (15, 18, 411, 758),
            "schedule": (28, 760, 411, 922),
            "map": (430, 14, 1172, 923),
            "dossier": (1190, 16, 1652, 923),
        },
    },
    {
        "code": "B",
        "title": "编辑部选题桌",
        "source": ROOT / "wmw-adult-weird-weekly-02-editorial-pitch-desk-v0-2-imagegen.png",
        "output": ROOT / "wmw-adult-weird-weekly-02-editorial-pitch-desk-v0-2.png",
        "crops": {
            "left_cards": (24, 20, 500, 682),
            "schedule": (18, 690, 500, 922),
            "map": (509, 20, 1212, 923),
            "dossier": (1223, 20, 1652, 923),
        },
    },
    {
        "code": "C",
        "title": "世界奇闻特刊",
        "source": ROOT / "wmw-adult-weird-weekly-03-world-oddities-special-v0-2-imagegen.png",
        "output": ROOT / "wmw-adult-weird-weekly-03-world-oddities-special-v0-2.png",
        "crops": {
            "left_cards": (13, 14, 470, 641),
            "schedule": (13, 649, 470, 920),
            "map": (481, 15, 1165, 920),
            "dossier": (1176, 14, 1655, 920),
        },
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


def scale_box(box: tuple[int, int, int, int]) -> list[int]:
    sx = FINAL_SIZE[0] / SOURCE_SIZE[0]
    sy = FINAL_SIZE[1] / SOURCE_SIZE[1]
    return [
        round(box[0] * sx),
        round(box[1] * sy),
        round(box[2] * sx),
        round(box[3] * sy),
    ]


def dark_background(source: Image.Image) -> tuple[int, int, int]:
    sample = source.crop((760, 50, 900, 130)).convert("RGB")
    mean = ImageStat.Stat(sample).mean
    return tuple(max(4, min(28, round(channel))) for channel in mean)


def reassemble(variant: dict[str, object]) -> dict[str, object]:
    source_path = Path(variant["source"])
    output_path = Path(variant["output"])
    source = Image.open(source_path).convert("RGB")
    if source.size != SOURCE_SIZE:
        raise RuntimeError(f"{source_path.name} 尺寸应为 {SOURCE_SIZE}，实际 {source.size}")

    canvas = Image.new("RGB", SOURCE_SIZE, dark_background(source))
    crop_audit: dict[str, object] = {}
    for name, target in TARGETS.items():
        crop = variant["crops"][name]
        patch = source.crop(crop)
        target_size = (target[2] - target[0], target[3] - target[1])
        patch = patch.resize(target_size, Image.Resampling.LANCZOS)
        canvas.paste(patch, (target[0], target[1]))
        crop_audit[name] = {
            "source_crop": list(crop),
            "target_box_1672x941": list(target),
            "target_box_1920x1080": scale_box(target),
        }

    final = canvas.resize(FINAL_SIZE, Image.Resampling.LANCZOS)
    final.save(output_path, optimize=True)
    return {
        "source": str(source_path),
        "source_size": list(source.size),
        "output": str(output_path),
        "output_size": list(final.size),
        "background_rgb": list(dark_background(source)),
        "regions": crop_audit,
    }


def make_board() -> Path:
    cell_w, cell_h, label_h = 1920, 1080, 60
    board = Image.new("RGB", (3840, 2280), (7, 14, 20))
    draw = ImageDraw.Draw(board)
    font = load_font(32)
    placements = [(0, 0), (1920, 0), (960, 1140)]
    for variant, (x, y) in zip(VARIANTS, placements):
        image = Image.open(variant["output"]).convert("RGB")
        draw.text((x + 24, y + 11), f"{variant['code']}  {variant['title']}", fill=(236, 239, 233), font=font)
        board.paste(image, (x, y + label_h))
    path = ROOT / "wmw-adult-weird-weekly-v0-2-comparison-board.png"
    board.save(path, optimize=True)
    return path


def main() -> None:
    variants = {variant["code"]: reassemble(variant) for variant in VARIANTS}
    board = make_board()
    audit = {
        "status": "art_direction_candidates_dual_reviewed_pending_user_choice",
        "source_generation": "built-in imagegen",
        "program_role": "只做已生成整屏的分区裁切、尺寸归一化、宏观三栏回位、拼版与审计；不重绘、不调色、不新增 UI 内容。",
        "source_size": list(SOURCE_SIZE),
        "final_size": list(FINAL_SIZE),
        "target_boxes_1672x941": {name: list(box) for name, box in TARGETS.items()},
        "target_boxes_1920x1080": {name: scale_box(box) for name, box in TARGETS.items()},
        "variants": variants,
        "comparison_board": str(board),
        "comparison_board_size": [3840, 2280],
        "review": {
            "ux": {
                "ranking": ["B", "C", "A"],
                "verdict": {
                    "A": "ITERATE_P0_0_P1_1",
                    "B": "PASS_P0_0_P1_0",
                    "C": "ITERATE_P0_0_P1_1",
                },
                "summary": "B 的故事比较、选中连续性与锁定语义最完整；C 的情绪承诺最强；A 仍略近国际态势新闻。",
            },
            "ui": {
                "ranking": ["B", "C", "A"],
                "verdict": {
                    "A": "ITERATE_DIRECTION_ONLY",
                    "B": "ITERATE_BUT_VISUAL_DIRECTION_APPROVED",
                    "C": "ITERATE_DIRECTION_ONLY",
                },
                "summary": "三套均无明显裁切拉伸，但只有风格方向可供裁决；B 最接近标杆，仍需统一内部子槽后才能成为正式母本。",
            },
            "parent_conclusion": "本轮只请用户裁决 A/B/C 的玩家身份感；推荐 B 编辑部选题桌。不得把任一方案称为正式整屏母本。",
        },
    }
    audit_path = ROOT / "wmw-adult-weird-weekly-v0-2-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(board)
    print(audit_path)


if __name__ == "__main__":
    main()
