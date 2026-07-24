# 三屏共同风格证明板 v1 生图 Brief

> 状态：`ui_ux_reviewed_ready_for_single_imagegen`  
> 产物：一张桌面 16:9 联合美术证明板；不是三张完整界面，不替代黑白功能稿。  
> UI Designer：通过非对称联合板结构。  
> UX 老哥：`P0=0`，有条件放行；已补操作证据、非连续拖拽、品牌 / 状态分层和非换皮约束。

## 输入图角色

1. `benchmark-board-01.png`：美术风格真值。
2. `benchmark-board-02.png`：美术风格真值。
3. 世界地图黑白功能稿：只提供世界地图、地区夹、快照和 pin 的功能语义。
4. 区域地图黑白功能稿：只提供陆水、路线、事件票、pin 和任务详情的功能语义。
5. 报刊填入黑白功能稿：只提供候选报道、双版版位、空位阻断和复核回条的功能语义。

失败批次不得作为参考输入。

## 最终 Prompt

```text
Use case: ui-mockup
Asset type: one high-fidelity shared art-language proof board for a desktop 16:9 PC game

Input images:
Image 1 and Image 2 are the only visual-style truth.
Image 3 is world-map functional vocabulary only.
Image 4 is region-map functional vocabulary only.
Image 5 is newspaper-assembly functional vocabulary only.
Do not reproduce the three wireframes as finished screens and do not redesign their frozen layouts.

Primary request:
Create one cohesive 16:9 WMW art-direction proof board, designed as a real modern weird-news editorial workbench. It must prove that world map, region map, and newspaper assembly can share one visual language while keeping three unmistakably different object identities. This is a proof board, not three finished game screens.

Composition:
Use a non-symmetrical editorial board similar in spirit to the benchmark boards.
Top: one restrained institutional WMW anchor.
Main field: three unequal hero specimen zones, not equal columns and not repeated cards.
- WORLD specimen is the widest and most open: broad continental cut-paper silhouettes, long cross-region routes, one selected region folder slightly lifted forward, one matching pin, and one matching editorial snapshot.
- REGION specimen is denser and closer to square: clear land-water relationship, four to six large terrain/area masses, two or three main roads or river lines, one selected event ticket, and one matching event pin/location.
- NEWSPAPER specimen is vertically editorial: an unmistakable orthogonal two-page spread with a clear center gutter, one main story slot, two smaller report slots, one candidate article visibly seated inside a real slot, one clean empty paper slot, and a small blocked-print receipt.
Footer: a low-weight material and brand proof strip with WMW, globe, eye, question, abnormal seal, paper swatches, color blocks, and tiny 25-percent thumbnails of all three hero specimens.

Editorial immersion and skeuomorphism:
Make this feel like a real newsroom workbench in active use through object identity and physical relationships: thin map sheets, region folders, event tickets, clipped snapshots, loose story copy, an open issue proof, edition slots, approval receipts, paper tabs, a few clips and tape pieces. Selection is shown by slight forward lift, a short hard offset shadow, and a quiet matching mark. Paper overlap, insertion, occupancy and blocking must read clearly. The physical object logic should feel believable and tactile, but the entire rendering remains stylized graphic illustration, not photorealism and not 3D.

Action-to-result evidence:
WORLD: selected region folder matches the continent/pin and the updated region snapshot.
REGION: selected event ticket matches the event pin and route/location.
NEWSPAPER: candidate article is already inserted into an occupied editorial slot and the review receipt reflects it; one empty slot clearly blocks print approval.
The footer progression is a cross-screen state-translation display, not a drag-and-drop tutorial. Use four separated still-life states with paper spacing. No hand cursors, no drag handles, no motion trails, no continuous arrows, no conveyor belt. Only the newspaper article may visibly meet a drop slot.

Style and modeling:
Modern graphic weekly collage; matte color-block design; flat cut-paper low-poly poster; simplified colored silhouettes; front-facing orthographic printed-object composition; medium-coarse faceted color modeling; varied large polygon planes; active adjacent-color shifts; thin crisp paper edges; one short hard offset shadow direction; subtle print tooth.
Every subject begins as a strong complete silhouette organized into three to eight structural masses. Inside those masses use only a few large uneven neighboring color/value planes. No uniform triangle mesh. At 25-percent scale the first read must be colorful large shapes and silhouettes, never micro-facets or realistic scene detail.

Color and value:
Deep charcoal navy is negative space only, not a full-screen dark wash.
Each hero specimen needs clearly visible large matte mid-tone areas.
Use clean warm gray-beige paper and cold ivory edges; clean olive, cobalt blue and teal as broad structured color families; mustard or low-saturation rust only as small emphasis or true blocking state.
Use three to five discrete flat value levels, not continuous photographic shading.
The three hero specimens must have comparable palette area hierarchy and must not become olive-black world, beige-gray region, and blue-black newspaper.

Black humor and fashion-forward WMW branding:
Use one primary WMW institutional anchor for the entire board. Show WMW, globe, eye, question and abnormal seal mainly in the footer symbol library as one custom branded family: bold silhouettes, one to three internal marks, slightly off-center printing, controlled off-register color, asymmetrical cut edges, modern editorial confidence.
Inside each hero specimen use only one or two quiet secondary brand marks.
Use at most one deadpan joke per map specimen: a simplified UFO silhouette with an editorial no-parking ticket in one map specimen; a self-returning route with a dry ordinary-delay approval stamp in the other. Humor stays second-read and never covers pins, selected marks, action areas, empty-slot blockers or writable surfaces. No cute faces and no cartoon mascots.

Cross-screen unity test:
At thumbnail scale all three must clearly come from the same publication because they share paper, matte color-block modeling, coarse low-poly planes, shadow direction, symbol drawing language and print behavior.
They must not look like reskins:
world first reads as open continents and long routes;
region first reads as denser land-water adjacency with roads and event pins;
newspaper first reads as a vertical two-page editorial spread with slot hierarchy.
Unity must remain even if all text, logos and footer symbol samples are visually ignored.

Typography and writable surfaces:
Text-bearing faces are orthogonal, front-facing and calm.
Clips, tape, tabs, paper edges, photo borders, folds, stamps, shadows and decorative symbols are no-text zones.
Use blank editorial bars, short abstract marks and clean empty writable zones rather than paragraphs or fake interface copy.
Text (verbatim): “WMW” only. Do not invent other readable words, labels, numbers or gibberish.

Avoid:
three finished UI screenshots; equal three-column template; same-shaped repeated dashboard cards; generic SaaS interface; military command center; political strategy game; GIS; satellite map; aerial city model; photorealistic scene; cinematic night scene; low-poly 3D render; ambient occlusion; volumetric light; depth of field; material reflections; dense uniform triangulation; micro facets; fragmented glass texture; all-dark monochrome palette; desaturated gray-blue wash; yellowed archive; vintage dossier; old newspaper grime; thick cardboard; folds or stains across writable areas; heavy soft shadows; bevel; glow; glassmorphism; generic same-line-width software icons; retro badge collection; childish stickers; cute monsters; tilted functional text faces; invented workflow; extra CTA; drag handles; fake dashboard metrics; watermark.
```

## 验收限制

- 本图只用于用户评审共同画法、代入感、氛围、低多边形颗粒、颜色面积和品牌黑色幽默。
- 未经用户确认，不生成三张完整界面，不升级为生产标杆，不进入拆件 / atlas / Godot。
