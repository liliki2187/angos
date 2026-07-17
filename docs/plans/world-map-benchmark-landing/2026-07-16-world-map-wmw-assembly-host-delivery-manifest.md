# WMW 独立整屏宿主 Delivery Manifest

## 交付结论

正确的桌面 16:9 WMW 独立整屏宿主已接入 `WeeklyRunGame`。三栏结构、B2.12 / A5.1 frozen 几何、collapsed / expanded / locked 状态、`selected_region_id` 四端同步与进入地区任务台 0 天行为均通过。中央地图仅为 `structure_only`，因此本轮不宣称正式地图美术通过。

## 产物

### 运行实现

- `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssembly.tscn`
- `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssembly.gd`
- `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapLeftRegionCardB212.gd`
- `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapStructureLayer.gd`
- `gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunExplorePhase.gd`
- `gd_project/scenes/gameplay/weekly_run/WeeklyRunGame.gd`

### 测试与证据脚本

- `gd_project/tests/test_world_map_right_dossier_a51_integration.gd`
- `gd_project/tests/capture_world_map_wmw_assembly_host.gd`
- `scripts/run_wmw_assembly_host_capture.ps1`
- `scripts/ui-contracts/wmw/wmw_assembly_host_evidence.py`

### 真实运行证据

- `644-world-map-wmw-assembly-host-dual-reference-board.png`
- `645-world-map-wmw-assembly-host-collapsed.png`
- `646-world-map-wmw-assembly-host-expanded.png`
- `647-world-map-wmw-assembly-host-locked.png`
- `648-world-map-wmw-assembly-host-geometry-qa.png`
- `649-world-map-wmw-assembly-host-state-cycle.gif`
- `650-world-map-wmw-assembly-host-integration-manifest.json`

## 运行合同

| 项目 | 结果 |
| --- | --- |
| 左栏责任区 | `[24,16,228,688]` |
| 中栏责任区 | `[268,16,648,688]` |
| 右栏责任区 | `[932,16,320,688]` |
| A5.1 frozen | `[932,30,320,520]` |
| 中栏最右界 | `x=916`，通过 |
| 地图分层 | `MapBaseLayer / RouteLayer / SelectedRegionLayer / PinLayer / LabelLayer` |
| 唯一选区真源 | `selected_region_id` |
| 四端同步 | 左卡 / 地图 pin / A5.1 / CTA 通过 |
| A5.1 交互数 | 2：任务情报 disclosure、进入地区任务台 |
| locked 任务泄漏 | 0 |
| 进入地区任务台耗时 | 0 天 |

## Gate

- `screen_identity_gate`：通过。没有旧 `GLOBAL CHANNEL`、旧 world shell、旧 A5.1 mount、底部跨栏票据、symbol strip 或 QA 顶栏。
- `dual_reference_gate`：通过。644 明确区分 30 的功能权限与 575 的视觉权限。
- `frozen_geometry_gate`：通过。B2.12 204×160、A5.1 320×520 与 frozen `[932,30]` 保持。
- `atomic_region_sync_gate`：通过。可用区与锁定区均为四端同 ID。
- `disclosure_locality_gate`：通过。collapsed / expanded 的像素变化只发生在右册范围。
- `locked_privacy_gate`：通过。锁定地区不泄漏任务名，披露与主 CTA 均禁用。
- `zero_day_entry_gate`：通过。
- `dynamic_evidence_gate`：通过，649 为真实运行帧循环 GIF。
- `map_visual_gate`：未通过也未宣称通过；当前 `map_artifact_type=structure_only`。

## 评审

- UX 老哥：`P0=0 / P1=0`，不阻断；4 项 P2。
- UI Designer：`P0=0 / P1=0`，不阻断；同意 UX，无需用户裁决的冲突。
- 位置修正附录：两位评审均确认 A5.1 恢复 `[932,30]` 后不新增问题。
- 完整原文：`2026-07-16-world-map-wmw-assembly-host-review.md`。

## 临时项与下一步

- 中央 `map_panel`：`structure_only` 运行时占位，需另行生产 clean map asset；替换后必须重跑标签碰撞、选中态、三栏平衡与截图证据。
- 左栏地区照片：按地区固定以避免状态漂移，但内容仍是构图图例，不是正式地区身份资产。
- A5.1 北美照片：仍为 composition placeholder。
- 其它地区照片：右册暂用深色 fallback。
- locked 文案与空照片槽：逻辑正确，最终视觉需强化“有意锁定”而不是“加载失败”。
- 折叠符号与 `2/4` 解释：P2 微调项，不阻断当前结构交付。
- A5.1 下方留白：应受保护，不以无功能模块填充。

## 复盘

首轮把右栏责任区起点 `[932,16]` 误当成 A5.1 frozen 起点。问题在交付前由父级合同复核发现，已恢复 `[932,30]`、新增断言并重跑 644-650；详见 `2026-07-16-world-map-wmw-a51-frozen-position-drift-loop-log.md`。

## 状态

`runtime_structure_and_state_integration_pass / production_map_visual_pending`
