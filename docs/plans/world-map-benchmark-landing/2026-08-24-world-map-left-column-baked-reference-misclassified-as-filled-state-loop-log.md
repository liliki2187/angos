# 世界地图左栏烘焙参考被误判为 filled-state Loop Log

## 结论

2026-08-21 的 `08-fullscreen-filled-state-north-collapsed-1920x1080.png` 只完成了右侧 Dossier 回嵌，左侧 RegionIndex 与 Schedule 仍沿用 A291 烘焙参考像素，因此不能称为完整 `filled_state_visual_target`。该图立即降级为 `right_dossier_full_screen_reinsert_proof`。

## 影响

- 左栏没有证明独立 RegionCard 母壳、三卡同构状态层、动态文字槽、canonical 图片注册或 Schedule 无字壳。
- 若继续进入切片或 Godot，会从一张整屏参考图反向猜测组件，绕过 A305/A306 的 `340×170`、`138×88` 与统一状态几何合同。
- A320 中关于“完整 filled-state”与“RegionCard 比例冲突未解”的表述不再作为当前结论；A305 与 `left_region_card.json` v1.0.0 继续是尺寸真源。

## 触发证据

- 用户追问“目前做了右边组件，那左边呢”。
- UX 复核确认：A291 与清理版 09 均为 `1672×941`；08 虽为 `1920×1080`，但在共同左栏范围内与 09 逐像素差分为零。
- 这说明整屏截图的存在掩盖了必需组件类缺失，属于 F1“验证等级冒充”的再次复发，而不是新的错误家族。

## 根因

交付验收只检查了右侧 Dossier 的同壳、文字容量和回嵌位置，没有在宣称“整屏完成”前逐类盘点本屏必需可见组件。A291 的左栏因视觉上已有内容，被误当成了本轮完成的真实组件。

## 纠偏动作

1. 08 降级为右 Dossier 回嵌证明；A291/09 左栏明确标记 `reference-only`。
2. 下一产物先做左栏纵向切片：一套共享无字 RegionCard 母壳、三张同规格实例、独立状态层与 disabled Schedule。
3. 左卡只保留编号、地区名、状态与统一图片槽；解锁缺口、任务摘要和倒计时不回流。
4. Schedule 依 A296 仅显示“当前第 1 天 / 选题会尚未开始 / 当前版本不可操作”，不得恢复具体剩余天数。
5. 在 `workflow-gates.yml` 与 harness 新增试行 `screen_component_completion_integrity` Gate；完整整屏声明前逐类登记本轮证据。
6. 本轮仍不进入 atlas、manifest、Godot 或 `WeeklyRunGame`。

## 下一次放行条件

- 三张 RegionCard 同为 `340×170`，三图同为 `138×88`，且只从各自 `1104×704 / 69:44` canonical 母图完整等比缩放。
- FrontCarrier 和动态文字槽保持 `0°`，只有独立 BackDecor 允许轻微倾斜。
- 左栏纵切片与整屏回嵌同时提供；旧参考像素区域不计作当前轮次完成证据。
- UX 老哥与 UI Designer 对真实生成结果再次互审后，才可申请 `filled_state_visual_target / pending_user_confirmation`。
