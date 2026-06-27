# 派遣签批台 V17.2 高保真生图交接稿

> 状态：handoff draft / not production truth  
> 输入基线：V17.1 正交真实内容方向稿与布局合同  
> 目标：把当前可判断结构稿推进到下一轮 `no-text asset master` 与 `filled-state text mock` 的高保真生成，不允许模型自由改版。

## 0. 使用边界

- 本文件只用于生成 / 精修下一轮高保真方向稿，不是 Godot 实装文件，也不是可直接切图母版。
- 若使用本地截图作为外部生图输入，会上传项目图片；执行前需要用户明确同意。
- 生成后若要称为生产标杆 / 资产标杆 / 真源候选，必须再交 `angus_art_director` 复审。
- 任何生成图若破坏正交功能面、底部基线、候选/器材归属或文字安全区，直接降级为偏差案例。

## 1. 参考输入

| 角色 | 文件 |
| --- | --- |
| 结构与内容参考 | `docs/screenshots/2026-06-22-dispatch-signoff-v17-orthogonal-real-content-style/01-dispatch-signoff-v17-filled-default.png` |
| hover 展开参考 | `docs/screenshots/2026-06-22-dispatch-signoff-v17-orthogonal-real-content-style/02-dispatch-signoff-v17-candidate-hover.png` |
| 安全区 / 切图合同参考 | `docs/screenshots/2026-06-22-dispatch-signoff-v17-orthogonal-real-content-style/04-dispatch-signoff-v17-1-contract-overlay.png` |
| 坐标合同 | `docs/plans/dispatch-signoff-imagegen/dispatch-signoff-v17-1-orthogonal-real-content-contract.json` |
| 视觉真源 | `design/art-direction/angus-visual-style-guide.md` |

## 2. 坐标锁

这些区域只能美术精修，不得重新布局：

| 区域 | rect | 锁定要求 |
| --- | --- | --- |
| 顶部状态条 | `[32, 28, 1888, 110]` | 只承载全局标题、周次、压力 / 可派状态；不得做成菜单栏。 |
| 左侧任务卷宗 | `[40, 132, 440, 978]` | 四色竖条是 `no_text` 装饰栏；任务身份、任务简报、本屏回答、本周状态必须在右侧独立内容面。 |
| 中央派遣板 | `[464, 132, 1532, 662]` | 队伍槽、随队器材、中央判断卡都必须正交；风险判断卡宽度保持约 760-820px。 |
| 右侧签批票据 | `[1560, 154, 1856, 654]` | 保持紧凑；只承载最终复核与 CTA，不要扩成宽侧栏。 |
| 底部资源抽屉 | `[464, 710, 1856, 952]` | 候选员工与器材共享父容器，底边固定在 `y=952`。 |

关键 `no_text`：

- 左栏四色竖条：`[54, 178, 104, 682]`
- 本屏回答右上小半调角标：`[376, 790, 400, 812]`
- 员工头像窗、右侧章印、票据半调等按 V17.1 合同执行。

## 3. Prompt A：No-Text Asset Master

用途：生成无动态文字的高保真资产母版，用于检查材质、分区、切图潜力和 Angus 视觉系统。

```text
Use case: ui-mockup
Asset type: 1920x1080 desktop 16:9 game UI no-text asset master draft
Primary request: Create a high-fidelity no-text asset master for the Angus dispatch signoff work surface / editorial approval control surface. Use the V17.1 layout as a strict reference: same panel positions, same bottom baseline, same compact right approval ticket, same central dispatch board, same left task dossier, same shared bottom resource drawer.

Scene/backdrop: modern midnight editorial field-dispatch approval control surface for the Angus supernatural weekly magazine. Fresh deep-sea navy UI work surface with restrained low-poly / pixel-print abstraction, not an old archive and not a cozy office desk.

Style/medium: polished game UI bitmap art, graphicized functional objects, fresh printed ivory paper, red-orange approval plates, restrained cyan signal accents, structured halftone dots, crop marks, subtle red-cyan print misregistration, high-definition micro-pixel material language. Pixels are used only as 2-4px clusters on edges, halftone, overprint, signal marks, and print material; the UI surfaces and text-safe zones remain modern, crisp, and readable, not 8-bit or low-resolution retro pixel art.

Composition/framing: full desktop 16:9 screen, square-on front view, all runtime content planes axis-aligned and rectangular. Keep the top bar, left task dossier, central dispatch board, right approval ticket, and bottom resource drawer in their V17.1 positions.

Text: no dynamic readable text. Do not bake task names, numbers, employee names, button labels, fake glyphs, lorem ipsum, or decorative text lines into the asset. Static logo plates may remain abstract or blank.

Content / no-text rule: obey the full V17.1 contract JSON. Dynamic `content_rects` must remain clean, flat, axis-aligned writable rectangles. Decorative color rails, halftone, stamps, avatar windows, crop marks, paper edges, clips, and strong print texture belong only in `no_text_rects` and must not intrude into writable content areas.

Must keep:
- top status bar rect [32,28,1888,110]
- left task dossier rect [40,132,440,978]
- central dispatch board rect [464,132,1532,662]
- right approval ticket rect [1560,154,1856,654]
- bottom shared resource drawer rect [464,710,1856,952]
- bottom drawer and left weekly status share baseline y=952
- central risk judgment is a compact card, about 760-820 px wide, not a full-width report strip
- candidate staff layer and equipment requisition layer are inside one shared bottom drawer
- selected staff cards and candidate staff cards use the same card family and similar dimensions
- one visible empty staff slot in the selected team row
- one carried-item receipt belongs to the current team area, not to a separate footer
- left colored rail and halftone marks are no-text decoration zones

Materials/textures: fresh printed ivory paper, not aged, not sepia, not stained, not torn, not archive parchment. Use fresh ink, controlled paper grain, small crop marks, crisp pixel-print edges, structured halftone only where it supports risk / signal / stamp language.

Avoid: old archive, yellowed dirty paper, torn parchment, coffee stains, warm wood desk, visible wooden furniture, cozy office props, nostalgic office, generic admin dashboard, SaaS panels, CAD grid, raw wireframe rectangles, 8-bit interface, low-resolution retro pixel art, tilted writable documents, skewed UI panels, perspective paper carrying body text or CTA, detached footer equipment tray, inventory bar at screen bottom, over-wide risk ruler strip, fake readable text, excessive clips, rivets, binder holes, busy office props, dark muddy blue, brown-orange palette, one-note purple palette.
```

## 4. Prompt B：Filled-State Text Mock

用途：生成带真实内容的高保真效果图，验证图文融合、头像/卡片融合、玩家第一眼读法。它仍不是可切图母版。

```text
Use case: ui-mockup
Asset type: 1920x1080 desktop 16:9 filled-state game UI style mock
Primary request: Create a high-fidelity filled-state text mock for the Angus dispatch signoff work surface / editorial approval control surface. Preserve the V17.1 layout and coordinate contract. Make the screen look like a usable in-game interface already filled with real mission, team, item, risk, and approval information.

Scene/backdrop: modern midnight editorial dispatch approval control surface for a supernatural weekly magazine. Fresh deep navy UI work surface, fresh printed ivory papers, red-orange approval stamp language, restrained cyan signal accents, pixel-print halftone structure. No visible wooden furniture, no cozy office props, no nostalgic archive desk.

Composition/framing: square-on front view, all runtime content planes orthogonal. Keep a compact right approval ticket, wide central team area, left task dossier, and shared bottom resource drawer. The candidate pool defaults to one row; hover variant may expand upward to two rows while keeping bottom y=952 fixed.

Text content target for runtime / local overlay. Render exact Chinese only if the model can keep it legible and verbatim; otherwise preserve clean text-safe rectangles and leave those areas ready for runtime text overlay. Do not invent fake Chinese, pseudo-glyphs, decorative unreadable text, or near-miss labels.
- Header: "WMW", "外勤签批台", "第 1 周 / 北美禁区 / M330 深度调查链", "可派 6/8 · 压力 22"
- Left task dossier: "任务卷宗", "只解释：为什么派人", "M330 未班车空白段", "北美禁区 / 深度调查", "当前环 1/4", "需求：洞察 2 / 人脉 2", "目标：潜在有效点 8", "风险：失败后压力 +2"
- Task brief: "任务简报", "一段车载录音缺了三秒。", "乘客口供互相矛盾，", "却都指向同一座夜间站台。", "签批后进入外勤队伍配置。"
- Screen answer: "本屏回答", "这 4 名员工 + 1 件随队器材", "能否承担当前任务？"
- Weekly status: "本周外勤状态", "已派 2/5 · 回报 1日"
- Central team: "本次队伍", "4/5 员工 + 1 件随队器材", "候选已移出 · 可继续补 1 人"
- Selected staff: "主编阿格斯 / 调查记者", "娜娜 / 街区线人", "末日钟表匠 / 档案写手", "伪人实习生 / 异常伪装", "空槽 / + 外勤成员"
- Current item: "随队器材", "匿名热线录音", "人脉覆盖 +1；不占人位", "撤回"
- Risk card: "签批前判断尺", "达标率", "78%", "有效点 13 / 目标 8", "洞察 2/2", "人脉 2/2", "缺口：无", "失败后果：压力 +2"
- Right ticket: "签批票据", "可签批", "达标率 78%", "消耗", "2 天", "本周", "7 -> 5", "队伍", "4/5 + 器材", "盖章派遣 · 2天"
- Bottom drawer: "可选资源抽屉", "候选员工优先 · 随队器材低权重", "已选者已移出 · 选中器材写回上方队伍槽", "更多候选", "悬停展开检索", "另有 4 名低适配员工"
- Candidate names: "印第安纳", "火鸡科长", "薛定鸭", "艾灵", "夜班校对", "摄影助理"
- Equipment names: "录音备份", "旧剪报", "照相机", "护身符", "线人费"

Must keep:
- selected characters do not also appear in the candidate pool
- selected staff cards and candidate cards share the same visual family and near-identical dimensions
- one selected empty slot remains visible
- carried item belongs to the team area
- bottom resource drawer contains both candidates and equipment, with baseline y=952
- right approval ticket stays compact and does not consume central width
- no button-state strip appears in the real functional screen
- all content and hit surfaces are axis-aligned rectangles
- obey the full V17.1 contract JSON: decoration, halftone, stamps, avatar windows, crop marks, paper edges, and strong print texture must stay out of `content_rects` and remain inside `no_text_rects`
- pixels are limited to 2-4px edge clusters, halftone, overprint, signal marks, and print material; do not turn the whole UI into 8-bit / low-res retro pixel art

Text rendering note: the preferred production path is no-text master plus local / runtime exact text overlay. If direct image generation cannot render exact Chinese, the result should still be acceptable as a visual-material target only when all text zones remain clean and usable. Fake glyphs or pasted-looking labels are a reject condition.

Materials/textures: fresh printed ivory paper, not aged, not sepia, not stained, not torn, not archive parchment. Deep navy must stay fresh and graphic, not muddy black, gray-blue, or cyber-terminal blue.

Avoid: old archive, yellowed dirty paper, torn parchment, coffee stains, warm wood desk, visible wooden furniture, cozy office props, nostalgic office, generic admin dashboard, SaaS panels, CAD grid, low-effort programmatic rectangles, 8-bit interface, low-resolution retro pixel art, tilted writable documents, skewed text slots, perspective CTA, detached footer equipment tray, inventory bar at screen bottom, over-wide risk ruler, candidate cards much smaller than selected cards, selected characters duplicated in candidate pool, fake Chinese, pseudo-glyphs, text pasted on top of art without integration.
```

## 5. Prompt C：Candidate Hover Variant

用途：在 Prompt B 通过后生成 hover 状态，只验证底部资源抽屉的展开规则。

```text
Image-to-image locked variant of the accepted Angus dispatch signoff filled-state mock. Preserve the accepted palette, material language, paper color, navy background, card family, content/no-text contract, and every panel position. No global restyle, no global retone, no new paper angle, no new perspective, no extra footer, no visible wooden furniture, no cozy office props.

Only change the bottom shared resource drawer: candidate staff expands upward to two rows, equipment layer stays visible at the bottom of the drawer, and the drawer bottom baseline remains fixed at y=952. Do not push the equipment layer downward. Do not cover the right approval ticket. Do not add a separate footer inventory bar. Preserve all V17.1 negative constraints: no tilted writable documents, no skewed text slots, no detached equipment tray, no over-wide risk ruler, no old archive / yellowed paper / fake Chinese / 8-bit low-resolution pixel UI.
```

## 6. 验收清单

生成后逐项检查：

- `1920x1080` 桌面 16:9。
- 第一眼是 Angus 外勤签批台，不是后台表格、旧档案、怀旧办公室或卡牌管理器。
- 任务卷宗、当前队伍、候选/器材资源抽屉、签批复核四区都能无说明读出。
- 所有动态文字 / 数值 / 头像 / CTA label 的承载面都是正交矩形。
- 左侧色条、半调、裁切线、印章、头像窗、纸边都没有压入动态内容安全区。
- 风险判断卡宽度约 760-820px，`达标率 78%` 是主结论。
- 底部资源抽屉底边与左侧本周状态底边一致，误差不超过 8px。
- 器材层在底部资源抽屉内部，默认可见但低权重。
- 上方队伍槽同时包含已选角色和随队器材。
- 候选池不包含已选角色。
- 右侧签批票据紧凑，不挤占中央队伍区。
- 真实功能界面中不出现 CTA 状态展示条。
- 纸张是干净象牙白，不泛黄、不脏旧、不破败。
- 深蓝背景清爽，有低多边形 / 像素概括感，不泥、不土、不全黑。

## 7. 失败样例判定

出现任一项，直接退回重生：

- 可写纸面或 CTA 文字槽被画成斜的、透视的、梯形的。
- 底部器材层像库存条或页脚，低于左侧状态基线。
- 判断尺重新横铺中央主板。
- 右侧签批区变成宽面板，中央角色区被压缩。
- 角色候选卡明显小于上方已选卡，无法形成同一资产家族。
- 已选角色还留在候选池。
- 图像整体回到旧档案、泛黄纸、暖木桌、破纸、脏噪点。
- 半调 / 颗粒只是随机噪声，没有成为风险、信号、印刷边界的结构语言。
- 真实文字像后贴 Label，和纸面、阴影、卡槽完全脱节。

## 8. 下一步执行顺序

1. 用 V17.1 默认图和 overlay 图作为参考，先生成 Prompt A 的 `no-text asset master`。
2. 通过安全区和美术复核后，再以 no-text master + V17.1 默认图生成 Prompt B 的 `filled-state text mock`。
3. Prompt B 通过后，再生成 Prompt C 的 hover 变体。
4. 三张图都通过后，进入组件拆分 / atlas 规划；仍不得直接从 filled-state mock 裁生产资产。
