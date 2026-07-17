from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
SCREENSHOTS = ROOT / "docs" / "screenshots"
OUT = Path(__file__).resolve().parent

FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


GROUPS = [
    {
        "output": "01-early-editorial-office-experiments.png",
        "title": "早期报刊工作空间 / 编辑部大厅实验（2026-05-27 ～ 06-04）",
        "items": [
            ("2026-05-27-paper-editorial-cleanup/01-paper-editorial-cleanup.png", "05-27 报刊编辑清理版"),
            ("2026-06-03-editorial-office-art-assets/01-editorial-office-assets-v1.png", "06-03 编辑部大厅资产 v1"),
            ("2026-06-03-editorial-office-art-assets/04-editorial-office-assets-1366-v3.png", "06-03 1366 布局 v3"),
            ("2026-06-03-editorial-office-pixel-variants/01-editorial-office-pixel-v2-1920.png", "06-03 像素变体 v2"),
            ("2026-06-03-editorial-office-pixel-variants/02-editorial-office-pixel-v3-1920.png", "06-03 像素变体 v3"),
            ("2026-06-03-editorial-office-v2-clean-prop/01-v2-prop-board-window-1920.png", "06-03 清洁物件版"),
            ("2026-06-03-editorial-office-world-echo/01-world-echo-astral-1920.png", "06-03 世界回响：星界"),
            ("2026-06-03-editorial-office-world-echo/02-world-echo-transit-1920.png", "06-03 世界回响：交通裂隙"),
            ("2026-06-03-editorial-office-world-echo/03-world-echo-signal-1920.png", "06-03 世界回响：信号中断"),
            ("2026-06-04-editorial-office-interactions/01-main-1920.png", "06-04 编辑部主界面"),
            ("2026-06-04-editorial-office-interactions/02-science-dialogue-1920.png", "06-04 科学联络人弹层"),
            ("2026-06-04-editorial-office-interactions/03-reader-letter-1920.png", "06-04 读者来信弹层"),
            ("2026-06-04-editorial-office-interactions/04-tv-broadcast-1920.png", "06-04 电视广播弹层"),
        ],
    },
    {
        "output": "02-july14-godot-structure-branches.png",
        "title": "Godot 发刊功能结构与分支收束（2026-07-14）",
        "items": [
            ("2026-07-14-weekly-editorial-functional-skeleton/01-held-and-drop-target.png", "功能骨架：持稿与目标"),
            ("2026-07-14-weekly-editorial-functional-skeleton/02-placed-full-review.png", "功能骨架：上版复核"),
            ("2026-07-14-weekly-editorial-functional-skeleton/03-signoff-confirmation.png", "功能骨架：签批确认"),
            ("2026-07-14-weekly-editorial-dual-page-focus-skeleton/01-dual-page-overview-held.png", "双版聚焦支线：总览"),
            ("2026-07-14-weekly-editorial-dual-page-focus-skeleton/02-single-page-focus-held.png", "双版聚焦支线：单版放大"),
            ("2026-07-14-weekly-editorial-dual-page-focus-skeleton/03-dual-page-signoff-confirmation.png", "双版聚焦支线：确认"),
            ("2026-07-14-weekly-editorial-assetized-vertical-slice/01-godot-dual-page-overview-held.png", "资产化切片：双版总览"),
            ("2026-07-14-weekly-editorial-assetized-vertical-slice/02-godot-focus-left-held.png", "资产化切片：左版聚焦"),
            ("2026-07-14-weekly-editorial-assetized-vertical-slice/02-godot-focus-right-held.png", "资产化切片：右版聚焦"),
            ("2026-07-14-weekly-editorial-assetized-vertical-slice/03-godot-dual-page-confirmation.png", "资产化切片：签批确认"),
            ("2026-07-14-weekly-editorial-dual-page-only/01-godot-dual-page-held.png", "双版常显：持稿"),
            ("2026-07-14-weekly-editorial-dual-page-only/02-godot-dual-page-full.png", "双版常显：全版"),
            ("2026-07-14-weekly-editorial-dual-page-only/03-godot-dual-page-confirmation.png", "双版常显：确认"),
            ("2026-07-14-weekly-editorial-benchmark-landing/01-editorial-current-runtime.png", "07-14 当时运行时基线"),
        ],
    },
    {
        "output": "03-july15-godot-mainline-refinement.png",
        "title": "Godot 发刊主线细化（2026-07-15）",
        "items": [
            ("2026-07-15-weekly-editorial-masthead/01-godot-masthead-held.png", "刊头接入：持稿"),
            ("2026-07-15-weekly-editorial-masthead/02-godot-masthead-full.png", "刊头接入：全版"),
            ("2026-07-15-weekly-editorial-masthead/03-godot-masthead-confirmation.png", "刊头接入：确认"),
            ("2026-07-15-weekly-editorial-headline-alignment/01-godot-headline-alignment-full.png", "标题对齐"),
            ("2026-07-15-weekly-editorial-headline-autofit/01-godot-headline-autofit-mixed-full.png", "标题自适应"),
            ("2026-07-15-weekly-editorial-same-paper-local-replace/01-godot-same-paper-default.png", "同纸色：默认"),
            ("2026-07-15-weekly-editorial-same-paper-local-replace/02-godot-single-local-replace.png", "同纸色：局部换稿"),
            ("2026-07-15-weekly-editorial-same-paper-local-replace/03-godot-drag-hover.png", "同纸色：拖拽目标"),
            ("2026-07-15-weekly-editorial-secondary-head-assetized/01-godot-secondary-head-occupied.png", "副头版资产：占用"),
            ("2026-07-15-weekly-editorial-secondary-head-assetized/02-godot-secondary-head-source.png", "副头版资产：来源"),
            ("2026-07-15-weekly-editorial-secondary-head-assetized/03-godot-secondary-head-targets.png", "副头版资产：目标"),
            ("2026-07-15-weekly-editorial-standard-story-b-slice/01-godot-standard-story-default.png", "普通报道图：默认"),
            ("2026-07-15-weekly-editorial-standard-story-b-slice/02-godot-standard-story-local-replace.png", "普通报道图：局部换稿"),
            ("2026-07-15-weekly-editorial-standard-story-b-slice/03-godot-standard-story-drag-hover.png", "普通报道图：拖拽目标"),
        ],
    },
    {
        "output": "04-july16-17-assets-capacity-and-wireframes.png",
        "title": "报道图接入、容量回归与整屏结构提案（2026-07-16 ～ 07-17）",
        "items": [
            ("2026-07-16-weekly-editorial-story-art-restyle/01-godot-three-restyled-story-images-default.png", "三张报道图重绘"),
            ("2026-07-16-weekly-editorial-roswell-b-slice/01-godot-two-standard-story-images-default.png", "罗斯威尔报道图接入"),
            ("2026-07-16-weekly-editorial-shadow-department-b-slice/01-godot-three-standard-story-images-default.png", "影子部门报道图接入"),
            ("2026-07-16-weekly-editorial-blue-phone-booth-b-slice/01-godot-four-standard-story-images-default.png", "蓝色电话亭报道图接入"),
            ("2026-07-17-weekly-editorial-ordinary-story-closeout/00-capacity-closeout-contact-sheet.png", "容量回归汇总"),
            ("2026-07-17-weekly-editorial-ordinary-story-closeout/01-godot-capacity-0-of-6.png", "Godot 容量 0/6"),
            ("2026-07-17-weekly-editorial-ordinary-story-closeout/02-godot-capacity-3-of-6.png", "Godot 容量 3/6"),
            ("2026-07-17-weekly-editorial-ordinary-story-closeout/03-godot-capacity-5-of-6.png", "Godot 容量 5/6"),
            ("2026-07-17-weekly-editorial-ordinary-story-closeout/04-godot-capacity-6-of-6.png", "Godot 容量 6/6"),
            ("2026-07-17-weekly-editorial-packaging-mock-v1/01-weekly-editorial-packaging-mock-v1.png", "整屏包装 Mock v1（已否决）"),
            ("2026-07-17-weekly-editorial-functional-black-structure-v1/01-weekly-editorial-functional-black-structure-v1.png", "功能黑色结构 v1（已替代）"),
            ("2026-07-17-weekly-editorial-formal-black-structure-v2/01-weekly-editorial-formal-black-structure-v2.png", "正式黑白结构 v2（待确认）"),
        ],
    },
]


def crop_to_fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def build_sheet(group: dict) -> dict:
    width, height = 2400, 1660
    margin = 32
    header_h = 80
    gap = 20
    cols = 4
    rows = 4
    tile_w = (width - margin * 2 - gap * (cols - 1)) // cols
    tile_h = (height - margin * 2 - header_h - gap * (rows - 1)) // rows
    label_h = 44
    image_h = tile_h - label_h

    canvas = Image.new("RGB", (width, height), "#080b0d")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 22), group["title"], font=font(34, True), fill="#f1f1ed")
    draw.text((width - margin, 31), f"真实历史截图 · {len(group['items'])} 张代表页", font=font(18), fill="#9ba3a6", anchor="ra")

    entries = []
    for index, (relative, label) in enumerate(group["items"]):
        source = SCREENSHOTS / relative
        if not source.exists() or source.stat().st_size <= 1:
            entries.append({"source": relative.replace("\\", "/"), "label": label, "status": "missing"})
            continue
        col = index % cols
        row = index // cols
        x = margin + col * (tile_w + gap)
        y = margin + header_h + row * (tile_h + gap)
        with Image.open(source) as original:
            thumb = crop_to_fit(original, (tile_w, image_h))
        canvas.paste(thumb, (x, y))
        draw.rectangle((x, y, x + tile_w - 1, y + image_h - 1), outline="#6f777a", width=2)
        draw.rectangle((x, y + image_h, x + tile_w - 1, y + tile_h - 1), fill="#11171b", outline="#6f777a", width=1)
        draw.text((x + 12, y + image_h + 10), f"{index + 1:02d}  {label}", font=font(18, True), fill="#e8e4d8")
        entries.append({"source": relative.replace("\\", "/"), "label": label, "status": "included"})

    output = OUT / group["output"]
    canvas.save(output, optimize=True)
    return {"output": group["output"], "title": group["title"], "entries": entries}


def full_inventory() -> list[dict]:
    prefixes = (
        "2026-05-27-paper-editorial-cleanup",
        "2026-06-03-editorial-office",
        "2026-06-04-editorial-office-interactions",
        "2026-07-14-weekly-editorial",
        "2026-07-15-weekly-editorial",
        "2026-07-16-weekly-editorial",
        "2026-07-17-weekly-editorial",
    )
    inventory: list[dict] = []
    for directory in sorted(path for path in SCREENSHOTS.iterdir() if path.is_dir() and path.name != OUT.name):
        if not directory.name.startswith(prefixes):
            continue
        for path in sorted(directory.iterdir()):
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"} or path.stat().st_size <= 1:
                continue
            try:
                with Image.open(path) as image:
                    size = list(image.size)
            except Exception:
                size = None
            inventory.append({
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "size": size,
                "bytes": path.stat().st_size,
            })
    return inventory


def main() -> None:
    sheets = [build_sheet(group) for group in GROUPS]
    inventory = full_inventory()
    manifest = {
        "scope": "weekly_editorial_history",
        "representative_sheets": sheets,
        "inventory_count": len(inventory),
        "inventory": inventory,
    }
    (OUT / "inventory.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"sheets": [item["output"] for item in sheets], "inventory_count": len(inventory)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
