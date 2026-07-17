from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SCREENSHOTS = ROOT / "docs" / "screenshots"
FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


GROUPS = [
    {
        "output": "01-2026-05-27-to-06-07-functional-and-reorg.png",
        "title": "报刊组版功能原型与 report-reorg 起线（2026-05-27 ～ 06-07）",
        "items": [
            ("docs/screenshots/2026-05-27-full-chain-redundancy-audit/09-paper-editorial.png", "05-27 最早完整组版页"),
            ("docs/screenshots/2026-05-27-paper-editorial-cleanup/01-paper-editorial-cleanup.png", "05-27 组版清理版"),
            ("docs/screenshots/2026-06-06-report-board-concept/01-report-board-concept-v2.png", "06-06 报道板概念 v2"),
            ("docs/screenshots/2026-06-06-report-board-formal/01-report-board-formal-v1.png", "06-06 报道板正式 v1"),
            ("docs/screenshots/2026-06-06-report-board-formal/02-report-board-formal-v2.png", "06-06 报道板正式 v2"),
            ("docs/screenshots/2026-06-06-report-reorg-modern/01-headline-publication-desk.png", "06-06 头版送印桌"),
            ("docs/screenshots/2026-06-06-report-reorg-modern/02-headline-filled.png", "06-06 头版满稿态"),
            ("docs/screenshots/2026-06-06-report-reorg-workbench/01-report-workbench-empty.png", "06-06 工作台空版"),
            ("docs/screenshots/2026-06-06-report-reorg-workbench/02-report-workbench-filled.png", "06-06 工作台满版"),
            ("docs/screenshots/2026-06-07-report-reorg-american-style-pass/02-report-workbench-filled.png", "06-07 美式报刊分支"),
            ("docs/screenshots/2026-06-07-report-reorg-film-rail/02-report-workbench-filled.png", "06-07 胶片轨分支"),
            ("docs/screenshots/2026-06-07-report-reorg-magazine-appeal/02-report-workbench-filled.png", "06-07 杂志吸引力分支"),
            ("docs/screenshots/2026-06-07-report-reorg-magazine-spread/02-report-workbench-filled.png", "06-07 杂志跨页分支"),
        ],
    },
    {
        "output": "02-2026-06-07-to-06-08-style-and-assetization.png",
        "title": "报刊跨页风格与资产化分支（2026-06-07 ～ 06-08）",
        "items": [
            ("docs/screenshots/2026-06-07-report-reorg-paper-texture/01-report-workbench-empty.png", "纸张纹理：空版"),
            ("docs/screenshots/2026-06-07-report-reorg-paper-texture/02-report-workbench-filled.png", "纸张纹理：满版"),
            ("docs/screenshots/2026-06-07-report-reorg-ux-state-pass/01-report-workbench-empty.png", "UX 状态：空版"),
            ("docs/screenshots/2026-06-07-report-reorg-ux-state-pass/02-report-workbench-filled.png", "UX 状态：满版"),
            ("docs/screenshots/2026-06-07-report-reorg-interface-style-master/01-full-interface-abstract-pixel-anomaly-style.png", "整屏像素异常风格"),
            ("docs/screenshots/2026-06-07-report-reorg-style-master/01-style-master-board-balanced.png", "均衡风格母板"),
            ("docs/screenshots/2026-06-07-report-reorg-magazine-style-master/01-pure-magazine-q-black-humor.png", "杂志母板：Q 黑色幽默"),
            ("docs/screenshots/2026-06-07-report-reorg-magazine-style-master/02-simplified-pixel-magazine-style.png", "杂志母板：简化像素"),
            ("docs/screenshots/2026-06-07-report-reorg-magazine-style-master/03-abstract-pixel-anomaly-magazine.png", "杂志母板：抽象异常"),
            ("docs/screenshots/2026-06-08-report-reorg-assetized-p0/01-report-workbench-empty.png", "资产化 P0：空版"),
            ("docs/screenshots/2026-06-08-report-reorg-assetized-p0/02-report-workbench-filled.png", "资产化 P0：满版"),
            ("docs/screenshots/2026-06-08-report-reorg-assetized-p0-cleanup/01-report-workbench-empty.png", "资产化清理：空版"),
            ("docs/screenshots/2026-06-08-report-reorg-assetized-p0-cleanup/02-report-workbench-filled.png", "资产化清理：满版"),
            ("docs/screenshots/2026-06-08-report-reorg-global-channel-style-pass/02-report-workbench-filled.png", "全局频道风格回填"),
        ],
    },
    {
        "output": "03-2026-06-08-to-06-09-html-hardening.png",
        "title": "HTML 报刊工作台可读性与资产收束（2026-06-08 ～ 06-09）",
        "items": [
            ("docs/screenshots/2026-06-08-report-reorg-global-channel-style-pass/01-report-workbench-empty.png", "全局频道：空版"),
            ("docs/screenshots/2026-06-08-report-reorg-rollback-stable/01-report-workbench-empty.png", "稳定回滚：空版"),
            ("docs/screenshots/2026-06-08-report-reorg-rollback-stable/02-report-workbench-filled.png", "稳定回滚：满版"),
            ("docs/screenshots/2026-06-08-report-reorg-ux-p0-clean/01-report-workbench-empty.png", "UX P0 清理：空版"),
            ("docs/screenshots/2026-06-08-report-reorg-ux-p0-clean/02-report-workbench-filled.png", "UX P0 清理：满版"),
            ("docs/screenshots/2026-06-09-report-reorg-safe-zone-fix/2026-06-09-report-reorg-safe-zone-empty-1600.png", "安全区修复：空版"),
            ("docs/screenshots/2026-06-09-report-reorg-safe-zone-fix/2026-06-09-report-reorg-safe-zone-filled-1600.png", "安全区修复：满版"),
            ("docs/screenshots/2026-06-09-report-reorg-asset-pass-safe/2026-06-09-report-reorg-asset-pass-empty.png", "安全资产：空版"),
            ("docs/screenshots/2026-06-09-report-reorg-asset-pass-safe/2026-06-09-report-reorg-asset-pass-filled.png", "安全资产：满版"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/02-pixel-object-filled-1600.png", "像素物件 P0：初版"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/05-pixel-object-filled-1600-v2.png", "像素物件 P0：v2"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/08-pixel-object-filled-1600-final.png", "像素物件 P0：final"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/17-pixel-object-filled-1600-delivery.png", "像素物件 P0：交付版"),
            ("docs/screenshots/2026-06-09-report-reorg-editor-desk-style-pass/02-editor-desk-filled-1600.png", "编辑桌风格：满版"),
        ],
    },
    {
        "output": "04-2026-06-09-signoff-and-detail-states.png",
        "title": "HTML 报刊签批、多分辨率与局部状态（2026-06-09）",
        "items": [
            ("docs/screenshots/2026-06-09-report-reorg-approval-signoff-fix/02-approval-signoff-filled-1600.png", "签批修复：1600"),
            ("docs/screenshots/2026-06-09-report-reorg-approval-signoff-fix/03-approval-signoff-filled-1366.png", "签批修复：1366"),
            ("docs/screenshots/2026-06-09-report-reorg-approval-signoff-fix/04-approval-signoff-filled-1920.png", "签批修复：1920"),
            ("docs/screenshots/2026-06-09-report-reorg-signoff-readable-fields/01-signoff-readable-filled-1600.png", "签批字段：1600"),
            ("docs/screenshots/2026-06-09-report-reorg-signoff-readable-fields/02-signoff-readable-filled-1366.png", "签批字段：1366"),
            ("docs/screenshots/2026-06-09-report-reorg-signoff-readable-fields/03-signoff-readable-filled-1920.png", "签批字段：1920"),
            ("docs/screenshots/2026-06-09-report-reorg-editor-desk-style-pass/01-editor-desk-empty-1600.png", "编辑桌：空版"),
            ("docs/screenshots/2026-06-09-report-reorg-editor-desk-style-pass/04-editor-desk-filled-1920.png", "编辑桌：1920 满版"),
            ("docs/screenshots/2026-06-09-report-reorg-editor-desk-style-pass/03-editor-desk-filled-1366.png", "编辑桌：1366 满版"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/16-pixel-object-empty-1600-delivery.png", "交付版：空版"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/17-pixel-object-filled-1600-delivery.png", "交付版：1600 满版"),
            ("docs/screenshots/2026-06-09-report-reorg-pixel-object-p0/18-pixel-object-filled-1366-delivery.png", "交付版：1366 满版"),
            ("docs/screenshots/2026-06-09-report-reorg-editor-desk-style-board/01-editor-desk-ui-style-board.png", "编辑桌 UI 风格板"),
            ("docs/screenshots/2026-06-09-report-reorg-editor-desk-style-board/02-story-art-visual-formula-board.png", "报道图视觉公式板"),
        ],
    },
    {
        "output": "05-2026-07-14-mocks-html-and-godot-branches.png",
        "title": "整屏过程 Mock、HTML 骨架与 Godot 分支（2026-07-14）",
        "items": [
            ("image_gen/2026-07-14/20260714-110214_weekly_editorial_filled_style_01.png", "整屏填充风格稿 01"),
            ("image_gen/2026-07-14/20260714-114433_weekly_editorial_atmosphere_v2_01.png", "整屏氛围稿 v2"),
            ("docs/screenshots/2026-07-14-weekly-editorial-functional-skeleton/01-held-and-drop-target.png", "HTML 骨架：持稿"),
            ("docs/screenshots/2026-07-14-weekly-editorial-functional-skeleton/02-placed-full-review.png", "HTML 骨架：满版"),
            ("docs/screenshots/2026-07-14-weekly-editorial-functional-skeleton/03-signoff-confirmation.png", "HTML 骨架：确认"),
            ("docs/screenshots/2026-07-14-weekly-editorial-dual-page-focus-skeleton/01-dual-page-overview-held.png", "HTML 聚焦支线：总览"),
            ("docs/screenshots/2026-07-14-weekly-editorial-dual-page-focus-skeleton/02-single-page-focus-held.png", "HTML 聚焦支线：单版"),
            ("docs/screenshots/2026-07-14-weekly-editorial-dual-page-focus-skeleton/03-dual-page-signoff-confirmation.png", "HTML 聚焦支线：确认"),
            ("docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/01-godot-dual-page-overview-held.png", "Godot 切片：双版"),
            ("docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/02-godot-focus-left-held.png", "Godot 切片：左版"),
            ("docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/02-godot-focus-right-held.png", "Godot 切片：右版"),
            ("docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/03-godot-dual-page-confirmation.png", "Godot 切片：确认"),
            ("docs/screenshots/2026-07-14-weekly-editorial-dual-page-only/01-godot-dual-page-held.png", "Godot 双版常显：持稿"),
            ("docs/screenshots/2026-07-14-weekly-editorial-dual-page-only/02-godot-dual-page-full.png", "Godot 双版常显：满版"),
            ("docs/screenshots/2026-07-14-weekly-editorial-dual-page-only/03-godot-dual-page-confirmation.png", "Godot 双版常显：确认"),
            ("docs/screenshots/2026-07-14-weekly-editorial-benchmark-landing/01-editorial-current-runtime.png", "Godot 07-14 运行基线"),
        ],
    },
    {
        "output": "06-2026-07-15-godot-interaction-refinement.png",
        "title": "Godot 双版报刊交互与资产细化（2026-07-15）",
        "items": [
            ("docs/screenshots/2026-07-15-weekly-editorial-masthead/01-godot-masthead-held.png", "刊头：持稿"),
            ("docs/screenshots/2026-07-15-weekly-editorial-masthead/02-godot-masthead-full.png", "刊头：满版"),
            ("docs/screenshots/2026-07-15-weekly-editorial-masthead/03-godot-masthead-confirmation.png", "刊头：确认"),
            ("docs/screenshots/2026-07-15-weekly-editorial-headline-alignment/01-godot-headline-alignment-full.png", "标题对齐"),
            ("docs/screenshots/2026-07-15-weekly-editorial-headline-autofit/01-godot-headline-autofit-mixed-full.png", "标题自适应"),
            ("docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/01-godot-same-paper-default.png", "同纸色：默认"),
            ("docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/02-godot-single-local-replace.png", "同纸色：局部换稿"),
            ("docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/03-godot-drag-hover.png", "同纸色：拖拽目标"),
            ("docs/screenshots/2026-07-15-weekly-editorial-secondary-head-assetized/01-godot-secondary-head-occupied.png", "副头版：占用"),
            ("docs/screenshots/2026-07-15-weekly-editorial-secondary-head-assetized/02-godot-secondary-head-source.png", "副头版：来源"),
            ("docs/screenshots/2026-07-15-weekly-editorial-secondary-head-assetized/03-godot-secondary-head-targets.png", "副头版：目标"),
            ("docs/screenshots/2026-07-15-weekly-editorial-standard-story-b-slice/01-godot-standard-story-default.png", "普通报道：默认"),
            ("docs/screenshots/2026-07-15-weekly-editorial-standard-story-b-slice/02-godot-standard-story-local-replace.png", "普通报道：局部换稿"),
            ("docs/screenshots/2026-07-15-weekly-editorial-standard-story-b-slice/03-godot-standard-story-drag-hover.png", "普通报道：拖拽目标"),
            ("docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/dynamic-frames/frame_04_candidate_selected.png", "交互帧：候选已选"),
            ("docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/dynamic-frames/frame_08_candidate_replaced.png", "交互帧：完成替换"),
        ],
    },
    {
        "output": "07-2026-07-16-to-07-17-godot-capacity-and-new-structures.png",
        "title": "Godot 报道图、容量回归与后续结构提案（2026-07-16 ～ 07-17）",
        "items": [
            ("docs/screenshots/2026-07-16-weekly-editorial-story-art-restyle/01-godot-three-restyled-story-images-default.png", "报道图重绘基线"),
            ("docs/screenshots/2026-07-16-weekly-editorial-roswell-b-slice/01-godot-two-standard-story-images-default.png", "罗斯威尔图接入"),
            ("docs/screenshots/2026-07-16-weekly-editorial-shadow-department-b-slice/01-godot-three-standard-story-images-default.png", "影子部门图接入"),
            ("docs/screenshots/2026-07-16-weekly-editorial-blue-phone-booth-b-slice/01-godot-four-standard-story-images-default.png", "蓝色电话亭图接入"),
            ("docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/00-capacity-closeout-contact-sheet.png", "容量回归汇总"),
            ("docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/01-godot-capacity-0-of-6.png", "Godot 容量 0/6"),
            ("docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/02-godot-capacity-3-of-6.png", "Godot 容量 3/6"),
            ("docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/03-godot-capacity-5-of-6.png", "Godot 容量 5/6"),
            ("docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/04-godot-capacity-6-of-6.png", "Godot 容量 6/6"),
            ("docs/screenshots/2026-07-17-weekly-editorial-packaging-mock-v1/01-weekly-editorial-packaging-mock-v1.png", "包装 Mock v1（已否决）"),
            ("docs/screenshots/2026-07-17-weekly-editorial-functional-black-structure-v1/01-weekly-editorial-functional-black-structure-v1.png", "黑色结构 v1（已替代）"),
            ("docs/screenshots/2026-07-17-weekly-editorial-formal-black-structure-v2/01-weekly-editorial-formal-black-structure-v2.png", "黑白结构 v2（待确认）"),
        ],
    },
]


def crop_to_fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def build_sheet(group: dict) -> dict:
    width, height = 2400, 1660
    margin, header_h, gap = 32, 80, 20
    cols, rows = 4, 4
    tile_w = (width - margin * 2 - gap * (cols - 1)) // cols
    tile_h = (height - margin * 2 - header_h - gap * (rows - 1)) // rows
    label_h = 44
    image_h = tile_h - label_h
    canvas = Image.new("RGB", (width, height), "#080b0d")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 22), group["title"], font=font(34, True), fill="#f1f1ed")
    draw.text((width - margin, 31), f"既有真实截图 · {len(group['items'])} 张代表页", font=font(18), fill="#9ba3a6", anchor="ra")
    entries = []
    for index, (relative, label) in enumerate(group["items"]):
        source = ROOT / relative
        status = "included"
        if not source.exists() or source.stat().st_size <= 1:
            entries.append({"source": relative, "label": label, "status": "missing"})
            continue
        col, row = index % cols, index // cols
        x = margin + col * (tile_w + gap)
        y = margin + header_h + row * (tile_h + gap)
        with Image.open(source) as original:
            thumb = crop_to_fit(original, (tile_w, image_h))
        canvas.paste(thumb, (x, y))
        draw.rectangle((x, y, x + tile_w - 1, y + image_h - 1), outline="#6f777a", width=2)
        draw.rectangle((x, y + image_h, x + tile_w - 1, y + tile_h - 1), fill="#11171b", outline="#6f777a", width=1)
        draw.text((x + 12, y + image_h + 10), f"{index + 1:02d}  {label}", font=font(18, True), fill="#e8e4d8")
        entries.append({"source": relative, "label": label, "status": status})
    output = OUT / group["output"]
    canvas.save(output, optimize=True)
    return {"output": group["output"], "title": group["title"], "entries": entries}


def image_record(path: Path, classification: str, reason: str = "") -> dict:
    size = None
    try:
        with Image.open(path) as image:
            size = list(image.size)
    except Exception:
        pass
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "classification": classification,
        "reason": reason,
        "size": size,
        "bytes": path.stat().st_size,
    }


def add_directory(records: list[dict], directory: Path, classification: str) -> None:
    if not directory.exists():
        return
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES or path.stat().st_size <= 1:
            continue
        name = path.name.lower()
        current = classification
        reason = ""
        if "publication-echo" in name or "summary" in name:
            current = "excluded_or_adjacent"
            reason = "发刊后的回响/摘要，不是报刊组版主体"
        records.append(image_record(path, current, reason))


def build_inventory() -> list[dict]:
    records: list[dict] = []
    early = [
        SCREENSHOTS / "2026-05-27-full-chain-redundancy-audit" / "09-paper-editorial.png",
        SCREENSHOTS / "2026-05-27-paper-editorial-cleanup" / "01-paper-editorial-cleanup.png",
    ]
    for path in early:
        records.append(image_record(path, "html_runtime_or_functional_prototype"))
    for directory in sorted(SCREENSHOTS.iterdir()):
        name = directory.name
        if not directory.is_dir() or directory == OUT:
            continue
        if name.startswith(("2026-06-06-report-board", "2026-06-06-report-reorg", "2026-06-07-report-reorg", "2026-06-08-report-reorg", "2026-06-09-report-reorg")):
            classification = "process_mock" if ("style-master" in name or "style-board" in name) else "html_runtime_or_functional_prototype"
            add_directory(records, directory, classification)
        elif name.startswith(("2026-07-14-weekly-editorial", "2026-07-15-weekly-editorial", "2026-07-16-weekly-editorial", "2026-07-17-weekly-editorial")) and "history-index" not in name:
            if any(token in name for token in ("functional-skeleton", "dual-page-focus-skeleton", "packaging-mock", "black-structure")):
                classification = "process_mock_or_html_prototype"
            else:
                classification = "godot_runtime_evidence"
            add_directory(records, directory, classification)
    for relative in (
        "image_gen/2026-07-14/20260714-110214_weekly_editorial_filled_style_01.png",
        "image_gen/2026-07-14/20260714-114433_weekly_editorial_atmosphere_v2_01.png",
    ):
        records.append(image_record(ROOT / relative, "process_mock"))
    adjacent_paths = []
    adjacent_paths.extend(sorted((SCREENSHOTS / "2026-06-01-publication-echo").glob("*.*")))
    adjacent_paths.extend(sorted((ROOT / "design/art-direction/references/clean-lowpoly-weekly-branch").glob("benchmark-board-*.png")))
    adjacent_paths.extend(sorted((ROOT / "design/references/settlement-reference/2026-03-18/output").glob("*.*")))
    adjacent_paths.extend(sorted((SCREENSHOTS / "2026-07-07-ending-meme-special").glob("*newspaper*")))
    adjacent_paths.append(SCREENSHOTS / "2026-05-27-full-chain-redundancy-audit" / "10-paper-summary.png")
    for path in adjacent_paths:
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            records.append(image_record(path, "excluded_or_adjacent", "不是报刊组版/校样/签批主体"))
    unique = {record["path"]: record for record in records}
    return [unique[key] for key in sorted(unique)]


def main() -> None:
    sheets = [build_sheet(group) for group in GROUPS]
    inventory = build_inventory()
    source_endpoints = [
        "design/prototypes/html/full-chain-demo/world-mysteries-full-chain.html",
        "paperlab-demo/world-mysteries-full-chain.html",
        "paperlab-demo-test/world-mysteries-full-chain.html",
        "docs/prototypes/weekly-editorial-functional-skeleton/index.html",
        "gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunEditorialPhase.tscn",
        "gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunEditorialPhase.gd",
    ]
    counts: dict[str, int] = {}
    for record in inventory:
        counts[record["classification"]] = counts.get(record["classification"], 0) + 1
    manifest = {
        "scope": "newspaper_interface_history_corrected",
        "definition": "画面主体承担报纸组版、周刊校样、版位编辑、发刊签批或送印",
        "representative_sheets": sheets,
        "inventory_count": len(inventory),
        "classification_counts": counts,
        "source_endpoints": source_endpoints,
        "inventory": inventory,
    }
    (OUT / "inventory.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"sheets": [group["output"] for group in GROUPS], "inventory_count": len(inventory), "classification_counts": counts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
