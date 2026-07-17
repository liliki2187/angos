# 新对话交接：区域任务台组件美术质量纠偏

请继续 Angus 的“区域任务选择界面 / 区域任务台”资产化工作。当前不是从零开始，先完整理解以下状态。

## 当前最重要的新反馈

我认为当前已经生成并接入 Godot 的 pin + label 组件美术资源，明显没有此前区域任务台美术效果稿好看。

上一轮只能证明它们容易裁切、alpha 干净、尺寸 / 锚点 / 命中区可落地，以及 0–N、密集避让、cluster、clamp 和状态交互可运行。这不代表组件美术已经达到效果稿。

请把此前的 `production vertical slice GO` 限定为技术 / 功能通过，重新打开美术质量 Gate。**先不要继续生成 event card，也不要批量生产其它组件。**

## 必须先看的视觉真值

1. 两张 clean-lowpoly-weekly 标杆：
   - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
   - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
2. 当前区域任务台综合色调 / 美术效果稿基底：
   - `image_gen/2026-07-16/20260716_region-task-color-mood-E2-local-calibration-v1.png`
3. 当前生成的独立组件：
   - `gd_project/Assets/ui/angus_packaging/region_task/v2/pin_slice/rt-task-pin-shell-v2-3x.png`
   - `gd_project/Assets/ui/angus_packaging/region_task/v2/pin_slice/rt-task-pin-label-v2-2x.png`
4. 当前真实运行效果：
   - `docs/screenshots/2026-07-16-region-task-pin-slice-v2/07-five-dense-selected-label-clearance.png`
   - `docs/screenshots/2026-07-16-region-task-pin-slice-v2/05-runtime-state-matrix.png`
   - `docs/screenshots/2026-07-16-region-task-pin-slice-v2/06-hover-select-runtime-demo.gif`
   - 汇总：`docs/screenshots/2026-07-16-region-task-pin-slice-v2/index.html`

## 已确认的美术方向

- 不是纯写实、严肃探案或专业复古杂志。
- 不是旧报纸、档案馆、泛黄脏旧和土味复古招贴。
- 也不是过度可爱、幼态或靠卡通怪物元素制造“卡通感”。
- 卡通感主要来自塑造：较大的多边形、概括轮廓、较少碎面、较低写实细节，而不是题材元素本身。
- 要有现代图形周刊拼贴感、有限但活跃的大色块、克制的纸张质感和清晰的形状经济。
- 要保留一点黑色幽默、符号化和新怪谈幻想，但它们是画面态度与余味，不是堆可爱怪物。
- 色调以 E 暖灰周刊拼贴版为基底：不能全局压暗；深海军蓝、暖纸、橄榄、青蓝 / 钴蓝是主要关系。
- 纸面色块是高级的结构性质感，不是年代污渍。
- 平面内容分三类，不能混用载体：草稿纸 / 便利贴使用手绘；文件夹 / 光盘 / 报刊等专业文书使用正体字和秩序化排版；符号化贴纸使用独立贴纸语言。

本支线继续执行临时例外：不要让旧像素 / 半调默认坐标系的 `angus_art_director` 自动指导或阻断。直接用两张标杆、E2、支线规范、UI / UX 和父级逐项对照。

## 当前组件合同：返工时不能丢失

### Pin

- 透明母版源尺寸：`192×240`（3x）。
- 运行时视觉尺寸：`64×80`；命中区：`72×80`。
- visual offset：`[4, 0]`；anchor：命中区坐标 `[36, 76]`。
- icon、文字、selected / hover ring、assigned / urgent / locked、禁用线全部由 Godot 叠加，不能烘焙。
- 外投影属于 Godot，alpha 里不能带外部阴影。

### Label

- 透明母版源尺寸：`400×144`（2x）。
- 运行时固定 `200×72`，不使用 NinePatch。
- 内容安全区：`[14, 8, 166, 56]`。
- 右挂点 `[78, 4]`，右边缘时左挂 `[-208, 4]`。
- `mouse_filter = IGNORE`。
- 标题、meta、状态色和外投影不能烘焙。

### 交互

- selected 标签持久，hover 标签临时。
- 五点密集时 selected label rect 以 8px 净距参加其它 pin 的 displacement，不能再遮挡相邻图钉。
- 8 个事件落入同一密集 cell 时用程序 cluster，可展开。
- 地图地标不可点击；事件来自 `payload.nodes[*].map_pos`，数量为 0–N；禁止恢复固定热点。

合同真源：

- `design/ui-contracts/region-task-board/event_pin_contract.json`
- `design/ui-contracts/region-task-board/component_cutout_inventory_v1.json`
- `gd_project/Assets/ui/angus_packaging/region_task/region_task_asset_manifest_v2.json`

## 当前实现位置

- Pin / label 运行时：`gd_project/scenes/gameplay/weekly_run/components/WeeklyRunRegionEventPin.gd`
- 区域任务台、避让与 cluster：`gd_project/scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskBoardV2.gd`
- Manifest loader：`gd_project/scenes/gameplay/weekly_run/components/WeeklyRunRegionTaskManifestV2.gd`
- 捕获脚本：`gd_project/tests/capture_region_task_pin_slice_v2.gd`
- 测试：`test_region_task_manifest_v2.gd`、`test_region_task_board_v2.gd`、`test_region_task_board_v2_integration.gd`

## 你接手后的第一项工作

先不要生图。先用文字做一次直接视觉复盘，把两张标杆、E2、当前 alpha 组件和真实运行截图放在同一分析框架里，回答：

1. 当前组件具体在哪些方面比美术效果稿普通、简陋或缺乏设计感？
2. 哪些是独立位图壳的问题，哪些是 Unicode icon、规则圆环、程序 cluster 等 runtime overlay 拉低了整体？
3. 此前为了易裁切、干净 alpha 和小尺寸可读，具体牺牲了哪些标杆特征？
4. 哪些现有优点必须保留，避免返工后重新出现浮雕、RPG 铭牌、写实细节、脏旧复古、碎多边形或难裁切？
5. 在不破坏尺寸与分层合同的前提下，如何恢复效果稿中的现代编辑拼贴感、活跃色块、块面塑造、纸面层次与新怪谈余味？

请先给出明确的文字修正方案和新的“美术验收合同”，不要直接说上一轮已通过，也不要直接进入 event card。我的确认之后，再决定是只重生 pin / label，还是先做一张小型“组件造型与材质母板”比较 2–3 种方案。

## 新的放行口径

技术通过、UI / UX 通过与美术标杆通过是三个独立 Gate。下一轮只有同时满足以下条件，才可恢复 event card：

- alpha、padding、尺寸、锚点、文字分层不退化；
- 100% 运行尺寸和 25% 缩略图都可读；
- 与 benchmark 01 / 02 和 E2 直接并排时，美术质量不再明显降级；
- 用户本人明确确认视觉方向；
- 真实 Godot 截图和动图中，位图壳与程序 overlay 属于同一套美术语言。

## 验证环境提醒

- Godot 4.6.2 在本机导入阶段会触发引擎级 `signal 11`。
- 使用 `D:/angos/tools/godot/4.6.3-stable/Godot_v4.6.3-stable_win64_console.exe` 已验证可运行。
- 现有功能测试之前均通过；美术返工只需按失效范围增量回归，不要无理由重跑其它系统。
- 当前工作树很脏，包含用户与其他任务的改动；不得重置或覆盖无关文件。

最新状态与复盘：

- `docs/plans/region-task-board-imagegen/STATUS.md`
- `docs/plans/region-task-board-imagegen/2026-07-17-region-task-component-functional-pass-aesthetic-gap-loop-log.md`
