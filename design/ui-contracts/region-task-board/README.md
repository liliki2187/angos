# 区域任务台 UI 合同

本目录约束桌面 16:9 区域任务台的几何、数据和交互边界。合同以 1920×1080 为参考画布；运行时只缩放参考画布，不改变三栏职责。

- `page_contract.json`：整页结构、数据真源和主操作链。
- `event_card_contract.json`：左侧任务卡及其与地图事件点的同源约束。
- `event_pin_contract.json`：0–N 个运行时事件图钉、标签和静态地标边界。
- `dossier_contract.json`：右侧摘要、元信息、风险和派遣入口。
- `schedule_contract.json`：底部日程条；本轮只冻结位置，时间推进逻辑尚未接入。
- `component_cutout_inventory_v1.json`：18 个正式组件 class 的生产路线、尺寸状态、倍率、alpha / padding、阴影所有权、允许 / 禁止烘焙内容与首个纵向切片。

本轮实现是 `runtime_skeleton` / `runtime_state_preview`，不是最终生产美术母版。地图底图可复用，纸面外壳、图钉和卡片仍由 Godot 原生节点承载，便于后续独立替换资源。

2026-07-16 起，任何新生图或裁切必须先命中 `component_cutout_inventory_v1.json` 中的唯一 `asset_id`。E2 等整屏效果稿只作视觉参考，不得直接挖成正式组件。
