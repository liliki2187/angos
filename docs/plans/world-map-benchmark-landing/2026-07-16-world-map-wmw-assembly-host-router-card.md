# WMW 正确整屏宿主 Router Card

## 目标

把已确认的 B2.12 左卡与 A5.1 右 dossier 接入独立 WMW 三栏宿主，隔离旧 `GLOBAL CHANNEL` 错挂载，并以单一 `selected_region_id` 同步左卡、地图、右册与 CTA。

## 本轮范围

- 登记 A223 双参考图分工；30 管结构，575 管美术映射。
- 新建独立 `WeeklyRunWorldMapAssembly` scene / host。
- 挂载真实 B2.12 与 A5.1，不修改任何 world-map 合同 frozen 字段。
- 中央建立 `MapBaseLayer / RouteLayer / SelectedRegionLayer / PinLayer / LabelLayer`；由于缺少合规 clean `map_panel`，底图只作 `structure_only` 占位。
- 定向移除 A5.1 在旧 `WorldDetailPanel` 的挂载，不回退同文件内地区任务台等无关修改。
- 补四端原子同步测试、collapsed / expanded / locked / QA 运行截图与 GIF。

## 不在本轮

- 不调用 imagegen，不生产正式 `map_panel`。
- 不恢复底部三票据，不新建 compact 票据合同。
- 不挂载 globe / eye / check / hand symbol strip。
- 不修改 B2.12 / A5.1 的 frozen 几何、状态槽或 CTA 结构。

## 风险与 Gate

- 风险等级：risky，可见主流程宿主重建。
- `screen_identity`：运行图必须无 `GLOBAL CHANNEL`、旧装订索引、旧频道回条、跨栏票据与 symbol strip。
- `atomic_region_sync`：左卡、地图选中、A5.1 payload、CTA 目标必须同源。
- `right_column_exclusivity`：所有中央可见层与投影止于 `x=916`。
- `artifact_type`：中央底图为 `structure_only`，只允许宣称结构宿主通过，不允许宣称正式地图视觉通过。
- 截图：锁定 Godot 4.6.2 windowed + OpenGL3 + Dummy audio，保留 `frame_post_draw` 与全黑帧拒绝。

## 预期交付

- assembly scene、B2.12 运行组件与分层地图节点。
- 正确宿主集成测试与截图 runner。
- 644 起连续编号的双参考对照、三态、QA、GIF、manifest。
- UX 老哥原文、UI Designer 原文、父级处理结论、STATUS 与交付 manifest。

## 交付状态

- 独立宿主、B2.12 运行卡、五层地图结构与 A5.1 已接入生产 `WeeklyRunGame`。
- 旧 `GLOBAL CHANNEL`、旧 A5.1 背景挂载、旧 world shell 和外部顶栏在世界地图视图中均隐藏 / 移除。
- 644-650 已由 Godot 4.6.2 windowed OpenGL3 重跑；collapsed / expanded / locked / QA / GIF / manifest 齐备。
- 集成测试证明 `selected_region_id` 四端同源、locked 不泄漏任务、进入地区任务台为 0 天。
- 首轮曾误把右栏起点当作 A5.1 起点；现已恢复 frozen `[932,30,320,520]`，详见 `2026-07-16-world-map-wmw-a51-frozen-position-drift-loop-log.md`。
- UX 与 UI Designer 最终均为 `P0=0 / P1=0`，不阻断结构交付；地图继续是 `structure_only`，正式地图美术未通过也未宣称通过。
