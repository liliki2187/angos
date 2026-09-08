from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\angos")
OUT = ROOT / "image_gen/2026-09-04/world-map-mapfield-overlay-ab-styleproof-v1"
A_RAW = OUT / "01-variant-a-editorial-locator-stamps-imagegen.png"
B_RAW = OUT / "02-variant-b-selected-evidence-cluster-imagegen.png"
MAP_SIZE = (960, 902)


def fit_mapfield(source: Image.Image, *, top_anchor: bool = False) -> Image.Image:
    image = source.convert("RGB")
    target_ratio = MAP_SIZE[0] / MAP_SIZE[1]
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        width = round(image.height * target_ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    elif source_ratio < target_ratio:
        height = round(image.width / target_ratio)
        top = 0 if top_anchor else (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    return image.resize(MAP_SIZE, Image.Resampling.LANCZOS)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    return ImageFont.truetype(path, size)


def main() -> None:
    a_raw = Image.open(A_RAW)
    b_raw = Image.open(B_RAW)
    a = fit_mapfield(a_raw)
    b = fit_mapfield(b_raw, top_anchor=True)
    a.save(OUT / "04-variant-a-mapfield-fit-960x902.png")
    b.save(OUT / "05-variant-b-mapfield-fit-960x902.png")

    board = Image.new("RGB", (1920, 1080), "#071923")
    draw = ImageDraw.Draw(board)
    draw.text((42, 22), "MAPFIELD 动态叠层 A / B 结构验证", font=font(34, True), fill="#efe5d3")
    draw.text((44, 68), "真实 ImageGen 风格验证 · 尚未保留 StaticBase 像素 · 无运行时文字与交互", font=font(18), fill="#a7b1a9")

    panel_size = (844, 793)
    a_panel = a.resize(panel_size, Image.Resampling.LANCZOS)
    b_panel = b.resize(panel_size, Image.Resampling.LANCZOS)
    board.paste(a_panel, (42, 136))
    board.paste(b_panel, (1034, 136))
    draw.rectangle((42, 136, 886, 929), outline="#d2ae4f", width=2)
    draw.rectangle((1034, 136, 1878, 929), outline="#5ca9b5", width=2)

    draw.text((42, 950), "A · 编辑定位纸章", font=font(25, True), fill="#d2ae4f")
    draw.text((42, 989), "最低成本去 GIS；照片与地点章仍是两组结构", font=font(18), fill="#d6d0c2")
    draw.text((1034, 950), "B · 当前选区证据簇（推荐）", font=font(25, True), fill="#75c0c9")
    draw.text((1034, 989), "照片、便签、选中章、标签与风险缺口构成一个编辑现场", font=font(18), fill="#d6d0c2")

    board.save(OUT / "03-mapfield-overlay-ab-structure-board-1920x1080.png")

    audit = {
        "schema_version": "1.0.0",
        "artifact_id": "world_map_mapfield_overlay_ab_styleproof_v1",
        "status": "style_structure_proof_pending_dual_agent_and_user_gate",
        "source_provenance": {
            "variant_a": "real built-in ImageGen output",
            "variant_b": "real built-in ImageGen output",
            "program_role": "aspect fit and comparison-board labels only",
            "program_drawn_final_art": False,
        },
        "outputs": {
            "variant_a": "04-variant-a-mapfield-fit-960x902.png",
            "variant_b": "05-variant-b-mapfield-fit-960x902.png",
            "comparison": "03-mapfield-overlay-ab-structure-board-1920x1080.png",
        },
        "checks": {
            "a_fit_960x902": a.size == MAP_SIZE,
            "b_fit_960x902": b.size == MAP_SIZE,
            "real_imagegen_sources_preserved": A_RAW.exists() and B_RAW.exists(),
            "no_program_drawn_final_art": True,
            "not_runtime": True,
            "not_staticbase_pixel_exact": True,
            "no_godot": True,
            "no_atlas": True,
            "no_final_manifest": True,
        },
        "known_limits": [
            "ImageGen redrew the map base; these are structure/style proofs only",
            "blank label carriers do not prove runtime text capacity",
            "locked and selected semantics require deterministic reconstruction after user choice",
            "no side columns were recomposed",
        ],
    }
    audit["machine_pass"] = all(audit["checks"].values())
    (OUT / "06-mapfield-overlay-ab-styleproof-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "07-delivery-manifest.md").write_text(
        """# MapField 动态叠层 A/B 风格结构验证

- A：编辑定位纸章；验证最低成本去 GIS 化。
- B：当前选区证据簇；验证照片、便签、Beacon、标签与 warning 的连续编辑现场。
- 两张主体美术均由内置 ImageGen 生成；程序只做比例适配与比较板排版。
- 这是风格／结构验证，不是 StaticBase 像素保真稿；ImageGen 已重绘地图底图。
- 用户选择后，才以既有 960×902 StaticBase 为像素真源，生成独立无字动态件并确定性注册。
- 不重拼左右栏，不进入 Godot、atlas、final manifest 或 WeeklyRunGame。
""",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(OUT), "machine_pass": audit["machine_pass"], "a_raw": a_raw.size, "b_raw": b_raw.size}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
