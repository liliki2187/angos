# WMW 完整整屏 benchmark Art Pass v0.6 Production Brief

## 状态

- `artifact_type = fullscreen_benchmark_art_identity_revision`
- `canvas = 1920x1080`
- `state = default`
- `status = executed_benchmark_ui_ux_pass_pending_user_art_direction_decision`
- `layout_truth = v0.5 fixed rects and functional hierarchy`
- `art_identity_truth = benchmark-board-01 / benchmark-board-02`
- `v0.5_permission = geometry_content_capacity_and_text_safe_areas_only`

本轮只修复三图同屏暴露的四项艺术身份差距：大字号出版图形、强色块节奏、受控非对称拼贴、统一品牌符号系统。功能 rect、文字安全区、命中区、三栏职责和真实内容全部不动。

## UX 生成前硬边界

- 中央北美选区第一、右侧档案第二、右下 CTA 唯一最强、左下日程次级。
- 每栏仅允许 1–2 个主要跨层关系；全屏仅允许 3–5 个统一品牌节点。
- gutter 越界最多 8–12px，并保留至少 8px 连续暗背景。
- 装饰与真实字段重叠为 0；不得新增按钮、标签、页签、路线、图例、工具栏、状态章或第二操作区。
- 锈红只属于第三条真实限时任务；任务状态必须是平面只读标签。

## 生成记录

- 模式：Codex 内置 `imagegen`，`ui-mockup`。
- 参考 1：`benchmark-board-01.png`，艺术身份第一真值。
- 参考 2：`benchmark-board-02.png`，艺术身份第一真值。
- 参考 3：`wmw-fullscreen-default-benchmark-art-pass-filled-v0-5.png`，仅 geometry / content mask。
- 原始生成位置：`C:\Users\gzfangyue\.codex\generated_images\019f7e73-ca4d-76a2-9cd3-ef38d3c490cc\exec-a8e92eaf-8006-40fa-ac82-596c9b316670.png`。
- 工作区生成源：`wmw-fullscreen-default-benchmark-art-pass-imagegen-source-v0-6.png`。
- 装配脚本：`render_wmw_fullscreen_benchmark_art_pass_v0_6.py`。
- 完整候选：`wmw-fullscreen-default-benchmark-art-pass-filled-v0-6.png`。

## 实际 Built-in imagegen Prompt

```text
Use case: ui-mockup
Asset type: complete no-text 1920x1080 desktop game UI art pass
Target version: WMW v0.6

REFERENCE ROLES — STRICT PRIORITY
Image 1 and Image 2 are the sole artistic-identity truth. Translate their large-scale publication graphics, vivid color-block rhythm, asymmetric editorial collage, matte paper and mounted-photo construction, restrained attachment hardware, low-poly anomaly imagery, and unified World Mystery Weekly globe-orbit brand language.
Image 3 is geometry, functional hierarchy, content capacity, and text-safe-area reference only. Preserve its fixed three-column structure and carrier positions. Do not inherit its cautious graphic scale, repetitive small globe marks, thin-line decoration, form-like task styling, heavy map extrusion, typography weight, or component skin.

CANVAS AND FIXED GEOMETRY
Create one complete front-facing landscape 16:9 player-facing desktop screen. Preserve these fixed outer carriers:
- left cards: x30 y36/294/552 w348 h240
- left schedule: x30 y810 w348 h246
- center host: x402 y24 w968 h1032
- central map stage: x426 y96 w924 h936
- right dossier: x1398 y24 w480 h1032
- bottom-right CTA: x1425 y957 w426 h75
Do not change any functional region, order, capacity, text-safe carrier, or interaction target. Central selected North America is first focus; right dossier second; bottom-right CTA only strongest action; bottom-left schedule secondary.

CORE STYLE TRANSLATION
Translate the benchmark identity at structural scale, not as stickers on an unchanged dashboard. The carriers themselves are editorial constructions: matte cardstock, mounted anomaly photos, large printed color fields, bold publication bars, controlled paper offsets, short crisp shadows, registration graphics, and one unified globe-orbit symbol system.
Use only one or two major cross-layer relationships per column. Any decorative overlap crosses a column edge by at most 8–12px and leaves at least 8px uninterrupted dark gutter. All future text carriers stay orthogonal, calm, high-contrast, and unobstructed.

COLOR RHYTHM
Deep navy-black editorial board dominates. Use vivid yellow-olive as primary brand color; cool teal and cobalt/slate blue as secondary structure; clean neutral cardstock and photo paper; very small mustard accents; rust only for the one real deadline row. Avoid muddy army green, gray-brown archive paper, uniform beige coverage, full-screen desaturation, and cold haze.

LEFT REGION CARDS
Three cards share one publication-card construction: dark cardstock base, mounted anomaly photo, orthogonal caption strip, flat printed state area. The selected North America card contains one large bright olive structural field covering about 18–24 percent of the card and one attachment crossing only the photo rim. Locked cards use cool slate and teal, never gray-brown. Do not repeat clips or globe marks on every card. Cards read as magazine region index cards, not game panels.

LEFT SCHEDULE
Treat it as a weekly issue insert: clean light date strip, one large dark-olive printed action field, calm light-paper consequence section, blank orthogonal icon well. The olive action field may offset up to 8px as the column’s second and last cross-layer relation. No bevel, metal, glow, embossed well, checkbox, or control-console styling. It stays weaker than the right CTA.

CENTER HOST AND MAP
Reserve the existing top safe area for a very large bold condensed publication masthead to be added later. Add one broad olive publication strip entering from the upper-right and overlapping the map edge by no more than 8px, with one abstract globe-orbit seal partially behind it. Build continents as printed cut-paper with short crisp shadows, not thick 3D slabs. North America is vivid olive; other continents are cool teal and slate. Keep broad readable low-poly planes. No route lines, legend, event network, GIS, radar, filter, toolbar, fake marker, or extra map function.

RIGHT EDITORIAL DOSSIER
Keep one continuous full-height editorial feature sheet, no rear page, folder, bag, or second frame. Use one bold asymmetric feature-heading zone, one unified globe-orbit seal, one mounted hero anomaly photo with one restrained clip, one calm article area, one strong dark-ink or olive mission-header band, four flat printed ledger rows, and one large bottom olive CTA field. Mission rows are information lines, never four buttons. Use bold issue numbers, short category bars, restrained rules, and flat status areas. Rust exists only in the third-row deadline. CTA is the brightest and most complete olive field, with no bevel, glow, raised shell, or duplicate frame.

BRAND SYMBOL SYSTEM
Exactly four major brand nodes across the screen: central masthead globe-orbit seal, existing selected North America ring-pin language, one publication seal on the selected left card, and one publication seal on the right feature page. All share circle, orbit line, registration dot, and print-weight language. Do not scatter small globe icons across every component or arrange icons as a toolbar.

MATERIALS
Matte uncoated cardstock, clean mounted photo paper, flat screen-printed fields, extremely restrained print registration variation, short crisp offset shadows. No stains, tears, dirt, yellowed paper, heavy grain, old newspaper, metal, glass, embossed frames, or luminous edges.

TYPOGRAPHY-SAFE OUTPUT
Render no readable text, letters, numbers, punctuation, fake words, fake serials, arrows, lock symbols, functional icons, or watermark. Leave every existing writing surface orthogonal and low-detail for later programmatic Chinese typography. Do not create fake labels or text-like scribbles.

HARD NEGATIVES
no generic dashboard; no military archive software; no strategy HUD; no muddy parchment dominance; no repeated chamfered panels; no beveled buttons; no metal frames; no inner glow; no sticker-only retrofit; no tiny decorative clutter replacing large graphics; no repeated globe icon on every card; no form-like mission list; no thick 3D map extrusion; no long black map shadows; no fake text; no fake label; no fake button; no toolbar; no route; no legend; no filter; no GIS; no radar; no extra module; no desk scene; no isometric environment; no object pile outside fixed carriers; no watermark.

OUTPUT INTENT
A polished shippable full-screen art-direction proposal, not an asset sheet or concept board. At 25 percent scale beside Images 1 and 2, it must immediately read as the same modern colorful low-poly mystery-weekly publication family while remaining a practical game screen.
```

## 生成后五秒三图同屏 Gate

1. 去字后是否立即属于同一个 WMW 出版物家族。
2. 是否先看到大刊头、北美 olive、日程动作带、任务头和 CTA，而不是小贴纸与细线。
3. 三栏是否各有 1–2 个清楚、受控的前后层关系。
4. 品牌节点是否统一且只有 3–5 个，不排成工具栏。
5. 是否仍保持地图第一、右档案第二、CTA 唯一最强、日程次级；无假功能与遮挡。

## 边界

- 本轮未改 Godot、正式合同、compact A5.1、B2.12 或三栏职责。
- 默认态获用户认可前，不生成 confirming、atlas 或拆件。
- 只向用户展示最终完整玩家视图；生成源、补片与 QA 不单独作为审阅项。
