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
        "title": "无涂布独立周刊",
        "source": ROOT / "wmw-a259-01-uncoated-independent-weekly-v0-1-imagegen.png",
        "output": ROOT / "wmw-a259-01-uncoated-independent-weekly-v0-1.png",
    },
    {
        "code": "2",
        "title": "当代布脊专题册",
        "source": ROOT / "wmw-a259-02-cloth-spine-special-v0-1-imagegen.png",
        "output": ROOT / "wmw-a259-02-cloth-spine-special-v0-1.png",
    },
    {
        "code": "3",
        "title": "细网丝印增刊",
        "source": ROOT / "wmw-a259-03-fine-mesh-silkscreen-v0-1-imagegen.png",
        "output": ROOT / "wmw-a259-03-fine-mesh-silkscreen-v0-1.png",
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
    output = ROOT / "wmw-a259-v0-1-comparison-board.png"
    board.save(output, optimize=True)
    return output


def main() -> None:
    variants = {variant["code"]: normalize(variant) for variant in VARIANTS}
    board = make_board()
    audit = {
        "status": "dual_reviewed_pending_user_material_selection",
        "decision_source": "A261",
        "generation_mode": "built-in imagegen",
        "program_role": "只做 16:9 尺寸归一化、拼版、哈希和基础图像审计；不重绘、不调色、不增加 UI 内容。",
        "source_reference": str(ROOT / "wmw-a258-01-light-indigo-sage-v0-1.png"),
        "final_size": list(FINAL_SIZE),
        "locked_contract": {
            "desktop_aspect": "16:9",
            "layout": "A 方案三栏功能与尺寸关系",
            "palette": "A258 方案 1：浅暮靛背景、暖灰米纸、鼠尾草绿、灰靛、柔珊瑚、深鼠尾草 CTA",
            "rectangular_image_slots": 8,
            "mission_rows": 4,
            "cta_count": 1,
            "forbidden": [
                "multi_photo_collage",
                "irregular_image_mask",
                "title_over_image",
                "new_runtime_function",
                "fake_text",
                "fake_controls",
            ],
        },
        "controlled_experiment": [
            "既有静态装订与五金元素的材质转译",
            "纸张、底板、油墨和表面颗粒",
            "当代独立怪新闻周刊的情绪强弱",
            "允许故事插图题材在不增加资源位与复杂度的前提下形成概念级变化",
        ],
        "variants": variants,
        "comparison_board": str(board),
        "comparison_board_size": list(Image.open(board).size),
        "review": {
            "parent": {
                "verdict": "PASS",
                "ranking": ["1", "2", "3"],
                "summary": "三套整屏对齐稳定；首轮丝印草稿因地图和故事图漂移已在交付前淘汰，未进入最终文件。",
            },
            "ux": {
                "verdict": {
                    "1": "PASS_P0_0_P1_0_P2_1",
                    "2": "PASS_P0_0_P1_0_P2_2",
                    "3": "PASS_P0_0_P1_0_P2_2",
                },
                "ranking": ["1", "2", "3"],
                "summary": "三套均可交用户裁决；方案 1 最稳定地读成当代成人怪新闻周刊。",
            },
            "ui": {
                "verdict": {
                    "1": "PASS_P0_0_P1_0_P2_1",
                    "2": "ITERATE_P0_0_P1_1_P2_1",
                    "3": "ITERATE_P0_0_P1_2_P2_0",
                },
                "ranking": ["1", "2", "3"],
                "summary": "方案 1 最易按九宫格、纸材 atlas 与轻量 shader 落地；方案 2 需防布纹摩尔纹，方案 3 需恢复色彩采样并分区控制网点。",
            },
        },
    }
    audit_path = ROOT / "wmw-a259-v0-1-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(board)
    print(audit_path)


if __name__ == "__main__":
    main()
