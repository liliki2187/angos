# 区域任务 dossier v1 生图与源文件记录

## 目的

为区域任务台右侧 `412×960` dossier 生产三件独立但同源的美术资源：外壳、中性信息附页、空白主 CTA。组合预览不是生产切图源；文字、风险色、状态和外投影继续归 Godot。

## 参考图

- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- `image_gen/2026-07-16/20260716_region-task-color-mood-E2-local-calibration-v1.png`

两张 benchmark PNG 的原文件存在 CRC / deflate 严格解码问题，生图前只在 `tmp/region-task-dossier-imagegen-refs/` 做了像素内容不变的解码重封装。重封装不参与美术创作。

## 共同 prompt

```text
Create one isolated production UI art asset for Angus / World Mystery Weekly, clean low-poly weekly branch. Use the attached benchmark boards only for modern editorial color-block language, flat cut-paper construction, restrained print tooth, and material relationships. Use the E2 reference only for the olive backing plus warm ivory dossier relationship; do not copy its text, icons, stamps, red risk frame, CTA symbol, layout mistakes, or baked content.

Front-facing orthographic asset, perfectly axis-aligned, zero perspective, zero tilt. Modern graphic editorial collage, matte color-block UI, flat cut-paper low-poly poster language, broad low-contrast planar facets, thin crisp paper edges, restrained screen-print grain. Clean contemporary weekly design, not a realistic archive prop.

Render exactly one isolated asset on a perfectly flat solid chroma-magenta #FF00FF background, with generous clear separation around the silhouette. No cast shadow and no external drop shadow.

ABSOLUTELY NO readable text, pseudo-text, letters, numbers, labels, handwriting, stamps, question marks, approval marks, seals, barcodes, icons, pictograms, warning triangles, red risk borders, checkmarks, clips, tape, pins, holes, photographs, maps, dirt, stains, tears, scratches, yellowed paper, vintage archive grime, realistic paper thickness, bevel, embossing, glossy lighting, 3D rendering, perspective, or mobile-game styling.
```

## 外壳尾段

```text
Asset: right-side dossier shell master, target export 824 × 1920 px at 2×, corresponding to one 412 × 960 desktop runtime object.

Build one coherent two-layer dossier silhouette: a muted E2-family olive backing board behind one orthogonal warm-ivory front paper page. Depth must come only from visible layer overlap and color separation, never from a shadow. Keep the outer silhouette calm, tall, confident, and editorial, with a few restrained cut corners. The front page must remain one continuous paper object, not stacked software panels.

Preserve quiet writable zones for header, summary, metadata, risk_and_chain and primary_CTA_slot. Do not bake section plates or a CTA into the shell. Do not add internal frames that resemble five separate program rectangles.
```

## 中性附页尾段

```text
Use the accepted shell only to match its warm ivory paper texture, restrained screen-print tooth, thin dark olive-gray edge ink, and angular cut-corner vocabulary. Do not copy the shell's olive backing board.

Asset: one neutral dossier information section plate, target export 728 × 288 px at 2×, designed for NinePatch use. Single-layer warm gray-beige paper only; no olive backing, green frame or second sheet. Keep the central 75% calm, uniform and empty; facets may exist only near the outer edge.
```

## CTA 尾段

```text
Edit the referenced blank olive CTA asset while preserving its clean-lowpoly paper material, color palette, clipped-corner vocabulary, restrained print tooth and inner perimeter line. Make the visible silhouette width-to-height ratio about 3.18:1, matching a 712 × 224 production asset. Center one blank asset on solid chroma-magenta. No text, icon, state mark or shadow.
```

## 源文件与生产输出

采用源文件：

- `image_gen/2026-07-22/region-task-dossier-assetization-v1/source/rt-dossier-shell-source-v1.png`
- `image_gen/2026-07-22/region-task-dossier-assetization-v1/source/rt-dossier-section-source-v2-edge-clean.png`
- `image_gen/2026-07-22/region-task-dossier-assetization-v1/source/rt-dispatch-cta-source-v1.png`

生产候选：

- `gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1/rt-dossier-shell-v1-2x.png`
- `gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1/rt-dossier-section-plate-v1-2x.png`
- `gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1/rt-dispatch-cta-mother-v1-2x.png`

`scripts/art/prepare_region_task_dossier_assets_v1.py` 只做色键去除后的 alpha 边界裁切、等比缩放和透明画布居中，不重画美术。
