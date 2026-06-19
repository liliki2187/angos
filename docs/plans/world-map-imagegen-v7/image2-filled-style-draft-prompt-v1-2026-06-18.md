# World Map v7 Image 2 Filled Style Draft Prompt V1

> Date: 2026-06-18  
> Status: generated in Codex Image 2 as a conversation preview; pending user review and project-file export.  
> Source contract: `docs/plans/world-map-imagegen-v7/filled-content-mock-v1-2026-06-18.md`

## Purpose

Generate one filled-state Image 2 style draft from the approved functional content mock. This image is only for visual direction review and text-density validation. It must not become a production no-text PNG, slicing source, or runtime background.

## Prompt

```text
Use case: ui-mockup
Asset type: desktop 16:9 game UI style draft, filled-state preview only, not a production no-text asset
Primary request: Create a polished pixel-print / editorial dossier world-map UI style draft for the Angus game, based on this exact functional layout and real content. It should look like a high-quality stylized game interface, not a web mockup.

Canvas and layout:
- 1920x1080 desktop landscape game UI.
- No annotation title row, no production notes, no red FAIL labels, no wireframe labels.
- Top strip only: left paper tickets for 探索周 01 and 剩余 7 天; right grouped five macro world-state metrics 公信 42, 诡名 18, 声望 31, 守序 26, 狂性 11 in a dark badge-rail / signal-meter style, visually different from the paper tickets.
- Three main columns below: left region index, central world map board, right selected-region dossier.
- Bottom ticker has exactly three clickable receipt-like lanes: 地区情报, 档案更新, 地区预警, each with a short title and an arrow cue.

Left region index content:
- Header: INDEX / 地区索引, with 已开放 1 / 4.
- Four stacked paper cards with strong pixel-print styling.
- Selected card: 01 北美禁区带, 可进入 · 红线升温, 难度 中等 / 推荐 ★★★★, 异常信号增强.
- Locked card: 02 东亚神秘地带, 锁定 · 声望 31/40, 难度 高 / 推荐 ★★, 缺青线 1 条.
- Available card: 03 太平洋失航带, 可进入 · 普通线报, 难度 低 / 推荐 ★★★, 适合补充素材.
- Sealed card: 04 南美红线档, 封存 · 许可不足, 难度 异常 / 推荐 ★, 需要完成复核.
- Footer: 本区 红 1 / 青 0 / 锁定 2.

Central map board:
- Retain the approved direction: deep navy editorial board, bright modern ivory / pale-blue low-poly paper world map, faceted paper continents, visible pixel-print edges, halftone dots, restrained cyan tracking arcs, red-orange anomaly route marks.
- Map should feel like a stylized paper cartography asset with moderate pixel granularity, not a flat placeholder and not photorealistic.
- Pins and route highlights are visual UI layers: selected red pin in North America with highlight, locked grey pins in East Asia and Australia, cyan pin in South America.
- No permanent region-name labels on the map.

Right selected-region dossier:
- Larger right dossier panel, straight orthographic paper, not tilted.
- Header: 区域档案 01, 选定地区, large title 北美禁区带, badges 中等 and 推荐 ★★★★.
- Region image viewport: dark city skyline / water tower / red anomaly eye in the sky, integrated in a framed media slot.
- Red status ticket directly below image: 红线升温 and 可进入 / 7天内提升狂性风险.
- Cyan secondary independent ticket below red status: 查看任务情报 · 3 with a clear arrow or inspect cue. It must look like a button/ticket, not the title bar of the prose body.
- Right prose body paper below the cyan ticket contains only one single intro section, not multiple tiles. Heading 地区简介. Body text: 北美禁区带由城市传说、军事封锁和异常广播交叠而成。编辑部把这里视作本周最值得进入的取材区域：危险清楚、线索密集，但进入后的具体线报必须在地区任务台选择。
- Footer note: 进入不消耗天数；具体线报在任务台选择。
- Large red primary CTA at the bottom: 进入选定地区. Fixed label, no region name in the button beyond this exact text.

Bottom ticker content:
- Lane 1 type chip 地区情报, title 城市传说与军事封锁交叠, arrow cue.
- Lane 2 type chip 档案更新, title 新增日志证词 / 封锁传闻, arrow cue.
- Lane 3 type chip 地区预警, title 进入后先到地区任务台, arrow cue.

Visual style:
- Strong pixel-print style, moderate pixelated edges and pixel halftone density, inspired by modern tactical editorial board UI.
- Bright modern ivory paper, not yellowed old parchment; deep navy workboard; red anomaly marks; restrained cyan signal marks; black ink text.
- Paper cards have crisp orthographic bounds, subtle shadows, screws/clips/folds/bookmark tabs outside text-safe areas.
- Typography should be readable and game-like, bold Chinese UI font feel. Text must stay inside content-safe areas, with comfortable padding, no overlaps, no out-of-frame elements.
- It should feel closer to a polished indie strategy game UI than to a browser wireframe.

Constraints:
- Must be a filled-state visual preview with readable text placement, but not a production asset sheet.
- Do not include wireframe labels, measurements, safe-zone overlays, debug text, English production notes, or the previous big title row.
- Do not bake fake task lists, staff, dice, success rate, dispatch controls, or long action logs into the world map.
- Do not put 地区情报 / 档案更新 / 地区预警 blocks inside the right prose body; those only appear in the bottom ticker.
- Avoid tilted text-bearing paper, excessive yellow/brown aging, blur, photorealistic noise, generic web dashboard styling, or one-note blue palette.
```

## Review Notes To Apply After User Sees The Draft

- Check whether the model preserves the single top status strip and does not recreate the removed annotation title row.
- Check whether the right prose body remains a single intro paragraph.
- Check whether bottom ticker entries read as clickable entrances.
- Check text legibility, Chinese corruption, and whether any generated labels drift from the contract.
- If the visual direction is accepted, run `angus_art_director` review before calling it a production candidate.
