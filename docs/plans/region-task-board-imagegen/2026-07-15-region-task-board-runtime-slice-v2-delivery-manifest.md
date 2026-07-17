# 区域任务台 v2 运行纵向切片 Delivery Manifest

## 决策条 / Decision Strip

- **结论**：运行骨架与状态预览通过；生产候选不通过。
- **影响**：地图事件点—左侧任务卡—右侧摘要—派遣 CTA 已形成真实数据闭环，可以进入“一类一母版”的逐组件美术替换；不得据此批量生图或把当前原生控件称为最终 UI。
- **下一步**：优先制作任务卡、图钉 / 短签和 dossier 三类无字母版，逐类替换并复跑当前截图 / GIF / 0–N 测试；独立时间推进语义确认前继续禁用左下按钮。

## 详情 / Human Brief

- **一句话结论**：最危险的技术前提已经验证——区域任务不是固定热点，而是同一 `nodes[]` 动态生成 0–N 张卡与图钉；右侧可承载长摘要且 CTA 不被挤走。
- **我实际做了什么**：建立 manifest v2 与五份组件合同；复用已选地图；接入新的 Godot 区域任务台运行骨架；保留原世界地图和派遣页；新增静态、数据、密集点位、文本压力、主流程集成、截图与动态演示证据。
- **现在卡在哪里**：最终纸面 / 贴纸美术母版尚未制作；玩法层没有独立“推进一天”命令。
- **为什么不能跳过**：直接批量生图会在视觉未经过运行替换验证时重新制造难裁切资产；直接启用时间按钮则会造成无效果或错误消耗天数的假交互。
- **下一步怎么验证**：每替换一类母版，只比较对应组件裁切、运行整屏、hover / pressed / disabled 和 1600×900 回归，不牵动已冻结大区。
- **本轮不要做**：不把运行骨架升格为生产母版；不恢复固定热点；不启用假时间推进；不把静态地标变成任务按钮。

## 术语版 / Manifest

- **交付对象**：区域任务台 v2 最小运行纵向切片。
- **产物类型**：runtime_skeleton / runtime_state_preview
- **风险等级**：risky
- **它能证明**：
  - `payload.nodes` 可动态生成 0–N 张任务卡与地图图钉；卡 / 图钉共享 `task_id`。
  - 同一区域多任务与密集同坐标点位可得到不同命中目标，常驻标签只显示当前选中项。
  - 7 / 8 / 9 行摘要可保留完整文本并滚动，meta、风险和 CTA 仍在固定槽位。
  - 未选中 CTA 禁用；选中后可进入现有派遣流程；返回世界地图保持原路径。
  - 1920×1080 与 1600×900 下三栏、地图和左下日程条不换位。
- **它不能证明**：最终纸面质感、最终图钉 / 贴纸母版、最终 hover / pressed 动效、1366×768 极限、全键盘链、推进一天玩法可用性。
- **对照真源 / 标杆**：两张 clean-lowpoly 标杆、已选区域地图原图、A204、A208、A210、A212、区域任务台资产化生产规格。
- **截图 / 文件路径**：
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/01-region-empty-selection.png`
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/02-region-m330-selected.png`
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/03-region-deadline-selected.png`
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/04-region-m330-selected-1600x900.png`
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/05-region-event-selection-runtime-demo.gif`
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/06-region-runtime-v2-geometry-overlay.png`
  - `docs/screenshots/2026-07-15-region-task-board-runtime-v2/07-region-summary-nine-line-stress.png`
- **几何 / 正交检查**：自动触发-已画水平垂直参考线。
- **几何触发原因**：运行预览 / 宣称可继续。
- **已过 gate**：
  - manifest 与合同 JSON 可读取，地图纹理存在且声明无 baked task pins。
  - Godot `0 / 1 / N / 密集五点`、共享 ID、单常驻标签、7 / 8 / 9 行摘要测试通过。
  - 主流程集成通过：进入地区、选择 M330、CTA 启用、进入派遣、区域页隐藏。
  - `gda` 通过新 manifest / pin / board / test / capture 脚本；Godot agent smoke 通过。
  - 真实窗口化 Godot 捕获通过，独立视口与黑帧采样拒绝器工作正常。
- **未过 / 待确认 gate**：最终美术母版、1366×768、键盘全链、推进一天规则与确认态、完整 atlas / hit rect 资源化。
- **反向读法检查**：已覆盖未选中、连续追踪、限时截稿、同坐标密集五点、九行摘要与 1600×900；未把静态地标判为可点对象。
- **已调用 agent / 复审**：消费本轮前置环节的 `ui_designer` 与 `ux_laoge` 结构 / 交互结论；父级按直接标杆和合同执行。
- **未调用 agent 与原因**：clean-lowpoly 支线按 A180 不自动调用旧像素坐标系 `angus_art_director`；本轮不改玩法数值或系统规则，未解冻冷备玩法 agent。
- **文档 / 实现 drift 检查**：A204 动态事件点、A208 左下时间闸门、A210 长摘要和 A212 生产准入均一致；`推进一天` 因实现缺口保持禁用，没有伪造 GDD 规则。
- **下一步允许做**：任务卡、图钉 / 短签、dossier、CTA 的一类一母版；逐类运行替换与状态截图。
- **下一步禁止跳到**：整屏裁切、批量同类生图、全量 atlas、production candidate、启用假时间推进。

## 组件落地评估结果

| 组件 | 功能 / 交互 | 当前承载 | 裁切 / 生图判断 | 本轮结论 |
| --- | --- | --- | --- | --- |
| HUD | 返回、页名、周 / 天数 | Godot 原生 | 无需生图；后续只换无字条底 | 位置与返回回调通过 |
| 左侧事件索引 | 0–N 任务、选中、滚动 | Godot 原生按钮 | 禁止从整屏挖卡；后续一类一母版 | 共享 `task_id` 通过 |
| 地图 | 地理识别、静态地标 | 复用已选原图 | 不重生、不烘焙 pin / 文本 | 1920 / 1600 填满通过 |
| 事件图钉 / 短签 | 点位选择、hover、selected | Godot 自绘骨架 | 后续一类一母版；状态运行时派生 | 0–N / 密集避让 / 单标签通过 |
| dossier | 长摘要、meta、风险、CTA | Godot 原生纸面骨架 | 后续无字壳；文字永远运行时 | 9 行滚动与固定 CTA 通过 |
| 派遣 CTA | 唯一任务级主动作 | Godot Button | 后续独立状态母版 | disabled / ready / 主流程通过 |
| 日程条 | 周期摘要、后果预览 | Godot 原生 | 可保留原生；不需要整条生图 | 几何通过 |
| 推进一天 | 全局时间动作 | 禁用占位 | 缺玩法命令，禁止做可点击假按钮 | 本轮明确未放行 |
