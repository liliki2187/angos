# 区域地图界面风格板 v1 生图 Prompt 记录

## 生成方式

- 工具：Codex 内置 `imagegen`
- 模式：真实位图生成 + 一次定向真实位图编辑
- 首轮输出：`call_ShzX4dGaopRER2y2yc39VQKt.png`
- 最终修正版：`call_RIP5Ws39CosUlJMkAcNArppK.png`

## 输入图角色

1. 区域地图黑白功能稿：只提供事件索引、区域地图、任务详情、日程与派遣入口等功能家族，不作为直接上色目标。
2. 世界地图 A「夜班石板蓝」：只提供跨屏配色、WMW 品牌、纸张、墨色、低多边形与黑色幽默家族，不继承世界地图构图。
3. `benchmark-board-01.png`：直接风格真值。
4. `benchmark-board-02.png`：直接风格真值。

## 首次生成 Prompt

```text
Use case: ui-mockup
Asset type: desktop 16:9 game UI art-direction component style board, 1920×1080-style landscape

Primary request: Create the first REGION MAP interface component style board for World Mystery Weekly. This is not a finished gameplay screen and not a colorized version of Image 1. It is an editorial asset-language board proving that the regional map is a local field-reporting work surface, visibly different from the world map while belonging to exactly the same visual family.

Input images and roles:
- Image 1: black-and-white regional functional draft. Use only as the inventory of functional families: event index, dominant regional map, selected task dossier, schedule/consequence strip, dispatch entry. Do not trace its rigid software boxes or reproduce it as a full UI screenshot.
- Image 2: accepted sibling world-map A “night slate blue”. Use as the cross-screen palette, WMW brand, paper, ink, clip, low-poly and restrained black-humor family reference only. Do not reuse its globe, continents, global grid, world-atlas composition, large region shapes or world-map layout.
- Images 3 and 4: direct visual truth. Prioritize their modern graphic editorial collage, matte color blocks, clean thin paper layers, restrained asymmetry, varied media scale, flat cut-paper low-poly illustration, sophisticated adult weird-weekly mood.

Core prototype: a local field-reporting case-map already in active use by a newsroom. The player is comparing which specific strange local event to investigate, not choosing a destination. The dominant central object must be a large opened formal regional map sheet used as an active work surface.

Composition:
- Landscape 16:9 editorial style board on a deep night-slate newsroom surface, irregular but controlled collage rather than four rigid software columns.
- Central 50–55%: one dominant formal local coastal map sheet. It must still dominate at 25% thumbnail.
- Left: a small staggered family of four event-index tickets, with default, selected, deadline and continuing-chain variations; they are specimens, not a clickable software list.
- Right: one orthogonal selected-event dossier with calm blank writable bands, plus only one low-poly local newspaper clipping and one small witness note / transit ticket. Do not create a pile of generic evidence.
- Bottom: only two grouped families, not five equal blocks: (1) a restrained matte DAY 01 newsroom schedule device and time/cost receipts, (2) consequence preview plus a dispatch-approval paper CTA specimen.
- Make the same selected event visibly linked across one left ticket, one map anchor and the right dossier using a sparse night-slate blue state chain. No large blue corridor.

Regional map identity and event-centric grammar:
- Formal rectangular map paper with a clear map viewport and quiet margins.
- Readable coastline or estuary, water-land relationship, 4–6 secondary local zones, 3–5 large terrain / urban / industrial silhouettes, and only 2–3 main transport corridors.
- Use 6–12 varied large polygon planes across the whole geography, with 2–3 adjacent value/color planes inside major forms. Planes must correspond to terrain, city density, water or abnormal influence.
- Place 5–7 event anchors at believable local coordinates, not one anchor at each zone center; allow two nearby events in one zone. Short event tags appear only near selected or highlighted anchors.
- Selected event: a quiet coastal tide anomaly shown by one impossible inland tide contour and a simplified lighthouse snapshot whose shadow points subtly the wrong way. Treat the impossible fact seriously, not as a monster gag.
- Roads, railway and shoreline provide cartographic identity only; no highlighted route-planning interaction.

Eight asset families to visibly prove:
1. regional map base paper;
2. event anchor family: default, selected, deadline, continuing chain, locked / unavailable;
3. short event ticket/tag;
4. staggered candidate event index tickets;
5. one or two local field-evidence media pieces;
6. selected-event dossier with orthogonal writable areas;
7. DAY schedule / cost / consequence components;
8. dispatch approval CTA carrier.

Object-to-render-language contract:
- Map and local snapshots: first delete photographic information, then rebuild as strong silhouettes, 3–8 structural masses and 2–3 large matte color planes per mass. No photo with a polygon filter.
- Formal WMW map, dossier, issue number, barcode and state labels: stable orthogonal institutional print language with subtle printing deviation, never handwritten.
- Temporary notes and dry humor sticker: offset hand-drawn line weight, small breaks/redraws, 1–2 matte colors, uneven die-cut edge, slight misregistration.
- Clips, pencil, map paper, folders and DAY device: restrained tactile work objects, simplified front-facing construction, matte surfaces and one thin crisp offset shadow; no product rendering.

Dry black humor and brand point: include one small hand-made sticker attached near the selected event, showing a serious prohibited-sign diagram of someone feeding a radio antenna from a food bowl. No cute face, no mascot, no loud comedy. Add 2–3 secondary WMW marks with different silhouettes and roles, not a uniform icon toolbar.

Color palette and area hierarchy:
- 32% deep night navy #071923 / charcoal navy #16191C negative space.
- 22% desaturated slate blue around #40566A, only structural mats and folders.
- 27% warm gray-beige paper around #B7A488 with narrow ivory edges #C0B9B3.
- 10% dark clean olive around #4E623D.
- 5% muted mustard note paper around #B3A456.
- 2% selected-state blue around #426E96, sparse and local.
- 2% low-saturation rust around #7A4A32 for deadline / warning stamp only.
- The regional board must contain more warm paper and olive working objects than the world-map sibling, while clearly remaining in the same night-slate family.

Paper material: sophisticated muted gray-beige modern weekly paper, broad flat low-poly value planes, subtle print tooth, clean writable face, separate narrow ivory edge and thin hard offset shadow. No prominent wrinkles or folds across future text areas.

Text: use only a few correctly spelled decorative specimen labels in restrained condensed editorial typography: “REGION FIELD DESK”, “EVENT MAP”, “CASE FILE”, “DAY 01”. Keep all other content as blank orthogonal text carriers, short bars, event codes and tiny non-readable print texture. No Chinese baked into the art.

25% thumbnail goal: first read must be “local field-reporting map covered by specific events, case evidence and dispatch work”, not “a zoomed-in world map”, “travel desk”, “crime board”, “military command room” or “software dashboard”.

Constraints: central regional map remains the dominant active work surface at 25% thumbnail; the same selected event is visibly linked across event ticket, map anchor and dossier; keep 3 distinct media shapes and 3 scale tiers; functional writing faces are exactly orthogonal; light tactile depth only; adult, stylish, curious, immersive, dryly funny.

Avoid: globe or world continents; global latitude-longitude grid; world atlas composition; destination pins; compass/nautical travel souvenirs; tourism/travel agency mood; military, intelligence-agency, tactical HUD, radar rings, crosshairs, scanning UI, sector labels; route-planning highlight; GIS, satellite imagery, exact city streets, dense road grids; crime scene tape, police badge, red-string evidence wall, forensic dossier; realistic photography, cinematic night photo, volumetric light, AO, 3D/isometric diorama, glossy plastic, chrome, bevel; dense uniform triangulation, Delaunay/Voronoi texture, micro facets; flat retro WPA poster; sepia, yellowed archive, old-file grime, cardboard, heavy paper texture, stains, tears, deep wrinkles; large high-saturation cobalt or Klein blue areas; rigid SaaS panels, equal card grid, standard icon set, toolbar row, placeholder boxes; cute monsters, smiling moon, cartoon mascots, sticker overload; generic stock clip-art; watermark; extra text.
```

## 定向修正 Prompt

```text
Use case: precise-object-edit
Asset type: desktop 16:9 regional-map UI component style board revision

Image 1 is the edit target. Images 2 and 3 are the direct visual truth. Image 4 is the accepted sibling palette/brand reference only.

Primary request: Preserve the successful regional field-desk composition, all object positions, the dominant central map sheet, the left event-ticket family, right dossier, bottom two grouped families, overall night-slate palette, and the visible R-21 selected-event linkage. Make only the following targeted visual-language corrections so this becomes a stronger clean-low-poly weekly style reference.

1. Central map correction — keep its paper rectangle, coastline / estuary composition, five to seven existing event anchors and selected R-21 location. Simplify the geography into 4–6 macro zones and varied medium-coarse large polygon planes. Consolidate small facets: each major terrain/water/urban form should use 3–5 large structural planes, never a carpet of small triangles. Reduce the pale road network to only two main transport corridors plus one simplified railway. Preserve spatial map identity but remove local-atlas / GIS density. No new routes, no radar, no exact streets.

2. Hand-made dry-humor sticker correction — keep the small antenna-feeding prohibition joke near the lower-right corner of the map, but redraw it as a genuine WMW editor-made sticker: offset asymmetrical silhouette, varying black line weight, one small break/redraw, muted mustard paper, uneven die-cut edge, subtle misregistration. Remove the perfect red prohibition circle and stock safety-sign / vector clip-art appearance. No cute face, no mascot, no extra joke.

3. DAY 01 object correction — keep the DAY 01 device in exactly the same location and same functional identity, but simplify it into a restrained matte newsroom schedule gate: flatter front-facing housing, fewer shell details, no chrome, no product-photography highlight, no deep bevel and no thick 3D shadow. It must remain a real tactile time device, not become an icon or sticker.

4. Media and seriousness correction — preserve the right dossier and bottom functions, but let the small local newspaper / witness material use one clean teal or olive low-poly image field instead of gray documentary photography. Reduce repeated globe marks so only one WMW institutional globe remains on the entire board; replace other repeated globe marks with a restrained eye seal, regional code or barcode. Keep institutional order, but add the benchmark's varied media scale and adult weird-news curiosity. Do not add more objects or more text.

Invariants: unchanged 16:9 framing; unchanged layout and module count; central map remains dominant; selected R-21 chain remains linked across left ticket, map and right dossier; same A night-slate palette and warm paper family; all functional writing carriers remain exactly orthogonal; no changes to the main titles beyond replacing redundant globe marks; thin clean paper layers and subtle print tooth.

Quality target at 25%: first read is a local field-reporting event map with a clear selected anomaly, varied editorial media and restrained dry humor. It must not read as a zoomed world map, local atlas, GIS planning map, crime dossier, military command room, software dashboard or bureaucratic approvals office.

Avoid: photograph converted to low poly; dense uniform triangulation; micro facets; detailed road grid; perfect vector prohibition icon; regular equal-line sticker; industrial product render; glossy bevel; chrome; thick shadow; repeated globe logos; grayscale evidence photography; yellowed archive; sepia; military/radar/route-planning graphics; new UI panels; new evidence props; new text; watermark.
```
