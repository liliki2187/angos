# Angus 报刊界面历史索引（校正版）

本索引只收录画面主体明确承担“报纸组版、周刊校样、版位编辑、发刊签批或送印”的界面。它同时覆盖已经进入 HTML / Godot 的功能页，以及未落地的结构稿、整屏 Mock、风格分支和局部验收状态。

## 时间线汇总

1. `01-2026-05-27-to-06-07-functional-and-reorg.png`：最早的 HTML 报刊组版页，以及 6 月 6–7 日 `report-board / report-reorg` 功能与布局演进。
2. `02-2026-06-07-to-06-08-style-and-assetization.png`：报刊工作台风格分支、杂志跨页方向和第一轮资产化回填。
3. `03-2026-06-08-to-06-09-html-hardening.png`：安全区、空版/满版、像素物件和编辑桌版本收束。
4. `04-2026-06-09-signoff-and-detail-states.png`：签批纸、可读字段、多分辨率和局部细节验收。
5. `05-2026-07-14-mocks-html-and-godot-branches.png`：两张整屏过程 Mock、HTML 功能骨架、被撤回的单版聚焦分支，以及最早的 Godot 资产化切片。
6. `06-2026-07-15-godot-interaction-refinement.png`：Godot 刊头、标题、同纸色、局部换稿、副头版和普通报道图交互细化。
7. `07-2026-07-16-to-07-17-godot-capacity-and-new-structures.png`：报道图逐张接入、0/3/5/6 容量回归，以及后来提出的整屏包装与黑白结构稿。

## 落地口径

- 2026-05-27 至 06-09：`world-mysteries-full-chain.html` / `paperlab` 系 HTML 功能原型和实验分支。
- 2026-07-14 的 `functional-skeleton`、`dual-page-focus-skeleton`：HTML 可交互骨架，不是 Godot。
- 2026-07-14 的 `assetized-vertical-slice`、`dual-page-only`，以及 07-15 至 07-17 的运行截图：真实 Godot 页面。
- 2026-07-14 两张 `image_gen` 整屏图、2026-07-17 包装 Mock 与两版黑白结构稿：过程稿，不是运行时落地。

## 明确排除

以下内容仍记录在 `inventory.json` 的 `excluded_or_adjacent` 分类，但不进入主汇总：

- 编辑部大厅、编辑桌环境、NPC 弹层和世界回响：它们是上层工作空间，不是报刊组版界面。
- 发刊回响、普通周结算摘要：它们是组版之后的结果页。
- 单张报道插画、页面壳贴图、刊头或按钮资产：它们是组件，不是整页界面。
- `benchmark-board-01/02`、2026-03-18 settlement reference、结局报纸梗图：它们是视觉参考或内容图，不是这条界面的落地/过程版本。

`inventory.json` 保存主线全部截图、相邻排除项、可运行入口和实现来源。运行 `build_newspaper_history_index.py` 可重建汇总图与清单。
