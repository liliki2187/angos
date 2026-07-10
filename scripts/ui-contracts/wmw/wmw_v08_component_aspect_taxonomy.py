from __future__ import annotations

from pathlib import Path
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont


BASE = Path(r"D:\angos\docs\screenshots\2026-06-24-world-map-benchmark-landing")
REF = Path(r"D:\angos\.codex-remote-attachments\019ef3f7-be2f-70d3-ae57-7df7fa181048\285fb7d4-37f0-4a98-86f4-c1652013a1d1\1-Photo-1.jpg")

OUT_OVERLAY = BASE / "345-world-map-wmw-v0-8-component-aspect-taxonomy-overlay.png"
OUT_MATRIX = BASE / "346-world-map-wmw-v0-8-component-aspect-taxonomy-matrix.png"
OUT_MANIFEST = BASE / "347-world-map-wmw-v0-8-component-aspect-taxonomy-manifest.json"

FONT_BOLD = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]
FONT_REGULAR = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]


COMPONENTS = [
    {
        "id": "region_list_card",
        "label": "A 地区索引卡",
        "role": "left-side selectable region summary",
        "rects": [[44, 24, 246, 192], [44, 207, 247, 377], [44, 388, 247, 537], [44, 543, 248, 692]],
        "target_ratio_family": "compact landscape card, not square icon tile",
        "approx_ratio_range": "1.20-1.35",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": ["region_name", "status_meta"],
        "asset_status": "needs new class contract; previous v0.6.9 keeps uniform-state rule only, not final aspect",
        "notes": "Outer card is compact, but the photo slot and label plate are rectangular. Do not turn it into a square badge.",
        "color": (96, 232, 150),
    },
    {
        "id": "region_photo_slot",
        "label": "A1 地区缩略图槽",
        "role": "landscape snapshot inside region card",
        "rects": [[64, 73, 239, 146], [65, 253, 239, 328], [65, 433, 239, 486], [65, 587, 239, 638]],
        "target_ratio_family": "wide landscape image slot",
        "approx_ratio_range": "2.3-3.4, depends on final card class",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": [],
        "asset_status": "no formal final slot yet",
        "notes": "Must preserve image aspect by re-authoring or fixed slot design; no non-uniform squeeze.",
        "color": (94, 210, 255),
    },
    {
        "id": "map_panel",
        "label": "B 中央地图面板",
        "role": "main world map interaction surface",
        "rects": [[278, 34, 913, 536]],
        "target_ratio_family": "large landscape panel",
        "approx_ratio_range": "1.25-1.35",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": ["pins", "selection markers", "route line"],
        "asset_status": "reference only; not current focus asset",
        "notes": "Large square-on board. Pins may be icon-like, but map board is not a square card.",
        "color": (120, 178, 255),
    },
    {
        "id": "detail_dossier_page",
        "label": "C 右侧详情纸",
        "role": "selected region detail and action container",
        "rects": [[934, 35, 1251, 548]],
        "target_ratio_family": "vertical dossier page",
        "approx_ratio_range": "0.60-0.70",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": ["title", "status", "tags", "action labels"],
        "asset_status": "needs class contract after aspect taxonomy",
        "notes": "Page is vertical, but internal action lanes are horizontal strips.",
        "color": (246, 222, 150),
    },
    {
        "id": "right_action_lane",
        "label": "C1 右侧行动条",
        "role": "primary/secondary/warning CTA rows",
        "rects": [[950, 353, 1233, 401], [950, 408, 1232, 455], [950, 461, 1232, 510]],
        "target_ratio_family": "long horizontal button lane",
        "approx_ratio_range": "5.6-6.2",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": ["action_label", "cost", "countdown"],
        "asset_status": "no formal final asset; previous slant fixes were proofs only",
        "notes": "This is the clearest example that functional components must be long rectangles, not cards.",
        "color": (255, 122, 106),
    },
    {
        "id": "bottom_receipt_card",
        "label": "D 底部票据卡",
        "role": "weekly action / intel / redline receipt summaries",
        "rects": [[289, 558, 535, 695], [557, 558, 802, 695], [827, 558, 1073, 695]],
        "target_ratio_family": "wide receipt card",
        "approx_ratio_range": "1.75-1.90",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": ["receipt_title", "value", "meter"],
        "asset_status": "no final class contract; earlier ticket passes are proof only",
        "notes": "Longer than region card. Should not inherit left-card geometry.",
        "color": (255, 199, 91),
    },
    {
        "id": "icon_badge",
        "label": "E 图标 / 徽章 / 贴纸",
        "role": "symbol-only affordances and decoration",
        "rects": [[1088, 558, 1145, 617], [1146, 559, 1205, 617], [1089, 620, 1147, 676], [1149, 620, 1206, 676]],
        "target_ratio_family": "square/circle symbol asset",
        "approx_ratio_range": "0.9-1.15",
        "can_be_square": True,
        "can_slant": "decorative stickers may rotate; functional icons should remain centered in square bounds",
        "runtime_text": [],
        "asset_status": "square assets allowed here only",
        "notes": "This is where square components belong. Do not generalize this ratio to cards or lanes.",
        "color": (208, 155, 255),
    },
    {
        "id": "top_status_strip",
        "label": "F 顶部状态条",
        "role": "global status and decorative instrumentation",
        "rects": [[34, 22, 1238, 77]],
        "target_ratio_family": "very long horizontal strip",
        "approx_ratio_range": "20+",
        "can_be_square": False,
        "can_slant": False,
        "runtime_text": ["week_status", "resource_shortcuts"],
        "asset_status": "not started",
        "notes": "Mostly low-density HUD strip; separate from card and receipt classes.",
        "color": (174, 215, 120),
    },
]


ROUTE = [
    ("1 风格标杆理解", "有", "可继续", "WMW 低多边形纸质方向已能识别，但不能代替组件合同。"),
    ("2 页面结构 / 职责", "参考图有，正式结构稿未固化", "待补", "需要把左/中/右/底部职责写成 class。"),
    ("3 真实内容填充", "有失败迭代，无正式通过稿", "未通过", "字体、槽位、框体贴合需等 class 合同后重做。"),
    ("4 组件比例分类", "v0.8 本轮产出", "待用户确认", "当前关键环；确认后才能重写 brief。"),
    ("5 class 几何合同", "v0.6.9 需废弃比例，只保留同状态一致规则", "需重写", "先按 v0.8 重新定义长方形 class。"),
    ("6 无字 clean sprite brief", "v0.6.8/v0.6.9 不可继续用", "需重写", "上游比例错，brief 必须重开。"),
    ("7 生图候选", "v0.7.1", "仅视觉参考", "不能直接切图；宽度/比例仍不满足合同。"),
    ("8 atlas / manifest", "无正式稿", "未开始", "等待 clean sprites 和 class contracts。"),
    ("9 runtime 回填", "v0.6.5/v0.6.7 proof", "临时验证", "证明机制，不证明最终资源。"),
    ("10 Godot 截图", "无正式通过稿", "未完成", "需等 atlas / manifest。"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (FONT_BOLD if bold else FONT_REGULAR):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_grid(draw: ImageDraw.ImageDraw, w: int, h: int):
    for x in range(0, w, 24):
        draw.line((x, 0, x, h), fill=(22, 43, 45, 45), width=1)
    for y in range(0, h, 24):
        draw.line((0, y, w, y), fill=(22, 43, 45, 45), width=1)


def rect_size(rect: list[int]) -> tuple[int, int, float]:
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    return w, h, w / h


def draw_labeled_rect(draw: ImageDraw.ImageDraw, rect: list[int], color, label: str, sub: str = ""):
    fill = (*color, 38)
    line = (*color, 245)
    draw.rectangle(rect, fill=fill, outline=line, width=3)
    tx, ty = rect[0] + 6, max(0, rect[1] - 30)
    text_w = max(130, len(label) * 13)
    draw.rectangle((tx - 4, ty - 2, tx + text_w, ty + 27), fill=(0, 0, 0, 175))
    draw.text((tx, ty), label, fill=line, font=font(16, True))
    if sub:
        draw.text((tx, ty + 16), sub, fill=(238, 234, 204), font=font(10))


def create_overlay():
    src = Image.open(REF).convert("RGB")
    sheet = src.copy().convert("RGBA")
    marks = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(marks, "RGBA")
    for comp in COMPONENTS:
        for idx, rect in enumerate(comp["rects"]):
            w, h, ratio = rect_size(rect)
            label = comp["label"] if idx == 0 else comp["id"]
            sub = f"{w}x{h} r{ratio:.2f}"
            draw_labeled_rect(d, rect, comp["color"], label, sub)
    sheet = Image.alpha_composite(sheet, marks)
    d = ImageDraw.Draw(sheet, "RGBA")
    d.rectangle((10, 8, 660, 75), fill=(0, 0, 0, 185), outline=(238, 234, 204), width=1)
    d.text((22, 17), "v0.8 世界地图 UI 资产化：组件比例分类 overlay", fill=(238, 234, 204), font=font(22, True))
    d.text((22, 48), "结论：方形只属于 icon/sticker；主要承载组件是横向卡、横条、票据、竖向详情纸。", fill=(255, 220, 150), font=font(14, True))
    sheet.convert("RGB").save(OUT_OVERLAY, quality=95)


def create_matrix():
    sheet = Image.new("RGB", (1800, 1900), (5, 18, 22))
    d = ImageDraw.Draw(sheet, "RGBA")
    draw_grid(d, *sheet.size)
    d.text((28, 24), "v0.8 World Map Component Aspect Taxonomy", fill=(238, 234, 204), font=font(24, True))
    d.text((28, 58), "This is the missing upstream ring: classify UI asset classes before sprite briefs, imagegen, atlas, or runtime assembly.", fill=(198, 205, 178), font=font(14))
    d.line((28, 92, sheet.width - 28, 92), fill=(92, 110, 90), width=2)

    y = 126
    d.text((28, y), "A. Component Classes", fill=(238, 234, 204), font=font(20, True))
    y += 34
    headers = ["class_id", "role", "ratio family", "square?", "status", "notes"]
    widths = [220, 315, 250, 105, 280, 555]
    x = 28
    for h, w in zip(headers, widths):
        d.rectangle((x, y, x + w, y + 38), fill=(28, 48, 48, 230), outline=(88, 110, 96), width=1)
        d.text((x + 8, y + 10), h, fill=(238, 234, 204), font=font(12, True))
        x += w
    y += 38

    for comp in COMPONENTS:
        row_h = 92
        x = 28
        values = [
            comp["id"],
            comp["role"],
            f"{comp['target_ratio_family']}\nref: {comp['approx_ratio_range']}",
            "YES" if comp["can_be_square"] is True else "NO",
            comp["asset_status"],
            comp["notes"],
        ]
        for i, (value, w) in enumerate(zip(values, widths)):
            fill = (32, 26, 22, 230) if i == 3 and value == "YES" else (11, 28, 31, 205)
            d.rectangle((x, y, x + w, y + row_h), fill=fill, outline=(42, 64, 62), width=1)
            lines = []
            for para in str(value).split("\n"):
                lines.extend(textwrap.wrap(para, width=max(8, w // 12)))
            for li, line in enumerate(lines[:4]):
                color = (255, 210, 120) if i == 3 else ((156, 208, 222) if i == 0 else (206, 218, 194))
                d.text((x + 8, y + 8 + li * 18), line, fill=color, font=font(11, i in (0, 3)))
            x += w
        y += row_h

    y += 32
    d.text((28, y), "B. Assetization Route Status", fill=(238, 234, 204), font=font(20, True))
    y += 34
    headers2 = ["ring", "current formal artifact", "status", "blocking issue"]
    widths2 = [290, 410, 150, 850]
    x = 28
    for h, w in zip(headers2, widths2):
        d.rectangle((x, y, x + w, y + 38), fill=(28, 48, 48, 230), outline=(88, 110, 96), width=1)
        d.text((x + 8, y + 10), h, fill=(238, 234, 204), font=font(12, True))
        x += w
    y += 38
    for ring, artifact, status, issue in ROUTE:
        row_h = 62
        x = 28
        for value, w in zip([ring, artifact, status, issue], widths2):
            bad = status in {"未通过", "需重写", "未开始", "未完成"}
            warn = status in {"待补", "待用户确认", "临时验证", "仅视觉参考"}
            fill = (45, 22, 20, 210) if bad else ((45, 38, 18, 210) if warn else (11, 28, 31, 205))
            d.rectangle((x, y, x + w, y + row_h), fill=fill, outline=(42, 64, 62), width=1)
            lines = textwrap.wrap(str(value), width=max(8, w // 12))
            for li, line in enumerate(lines[:3]):
                d.text((x + 8, y + 8 + li * 17), line, fill=(206, 218, 194), font=font(10, value == status))
            x += w
        y += row_h

    d.rectangle((28, sheet.height - 122, sheet.width - 28, sheet.height - 28), outline=(168, 146, 74), width=2)
    rules = [
        "Decision: stop using square-card imagegen as production source. Square/circle assets are limited to icon_badge / sticker_symbol.",
        "Current stage: ring 4 component aspect taxonomy. Next valid work is rewriting class contracts for rectangular components.",
        "Do not proceed to clean sprite brief, atlas slicing, or Godot runtime until each class has target ratio, content rects, hit rects, and state matrix.",
    ]
    for i, line in enumerate(rules):
        d.text((48, sheet.height - 100 + i * 24), line, fill=(238, 210, 154), font=font(14, i == 0))

    sheet.save(OUT_MATRIX, quality=95)


def write_manifest():
    components = []
    for comp in COMPONENTS:
        rects = []
        for rect in comp["rects"]:
            w, h, ratio = rect_size(rect)
            rects.append({"rect": rect, "size": [w, h], "ratio": ratio})
        item = {k: v for k, v in comp.items() if k not in {"color", "rects"}}
        item["reference_rects"] = rects
        components.append(item)

    manifest = {
        "artifact": "WMW v0.8 world map component aspect taxonomy",
        "date": "2026-07-07",
        "artifact_type": "component_aspect_taxonomy / upstream_classification / not final class contract / not sprite atlas",
        "source_reference": str(REF),
        "outputs": {
            "overlay": str(OUT_OVERLAY),
            "matrix": str(OUT_MATRIX),
            "manifest": str(OUT_MANIFEST),
        },
        "current_ring": "4_component_aspect_taxonomy",
        "components": components,
        "route_status": [
            {
                "ring": ring,
                "current_formal_artifact": artifact,
                "status": status,
                "blocking_issue": issue,
            }
            for ring, artifact, status, issue in ROUTE
        ],
        "key_decision": "Do not use square-card components as the main world-map UI production source. Main UI carriers are rectangular classes; square assets are limited to badges/stickers/icons.",
        "supersedes_or_blocks": [
            "Blocks v0.6.9 left_region_card aspect from production use; keep only the same-class uniformity rule.",
            "Blocks v0.7.1 imagegen sheet from sprite slicing; use it only as a visual reference.",
            "Requires rewriting clean sprite briefs after class ratios are confirmed.",
        ],
        "next_gate": "User review of taxonomy, then produce v0.8.1 component class contracts with target ratios, content rects, hit rects, and state matrix.",
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    create_overlay()
    create_matrix()
    write_manifest()
    print(OUT_OVERLAY)
    print(OUT_MATRIX)
    print(OUT_MANIFEST)


if __name__ == "__main__":
    main()
