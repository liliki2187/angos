# WMW 功能密度结构稿 v2 Router Card

> **已被 A229 / v3 取代**：本稿保留紧凑双回执与扩大地图结论；182px 日程器、浅袋口和右下无框背景已被用户否决，不得继续作为生图真源。

## 目标

在不改变三栏、B2.12、A5.1、世界地图、推进日日程器和双回执语义的前提下，让组件体量与真实信息量匹配，产出一张 1920×1080 黑白功能结构稿。

## 用户硬约束

- 当前整体形式大致正确，不重新设计页面身份。
- 红线预警 / 深链动向功能简单，只需底部一小条。
- `进入地区任务台` 下方空白档案区过大，必须压缩。
- 以已确定组件形式为基础，不新增功能。

## 本轮调整

- 新建结构级 `bottom_receipt_strip` 变体，两条各 450×90；不拉扁旧 `bottom_receipt_card v0.8.5`。
- 中央地图扩大至约 924×822，回收空间全部归还地图。
- A5.1 与内部槽位保持 frozen；CTA 下只保留 480×62 浅袋口，之后是无框世界背景。
- 左下日程器压至 342×182，保持推进、确认、后果预览；本稿保留既有 `y=810` 锚点。

## 不在本轮

- 不修改 UI 合同 JSON、Godot、HTML runtime 或 gameplay command。
- 不调用 imagegen。
- 不生产正式材质、atlas、manifest 或生产候选。
- 不增加第三回执、图例、右下抽屉、第二 CTA 或填空功能。

## Gate

- `information_value_to_container_volume`：短只读状态不得读成二级任务卡。
- `frozen_vs_new_variant`：旧 frozen 卡不缩放，新职责新建紧凑变体。
- `noninteractive_closure`：浅袋口无文字、无命中、无全高外框。
- `action_scope_separation`：推进日与进入地区保持分离。
- `geometry`：1920×1080、关键矩形和间距由审计 JSON 记录。

## 状态

`structure_wireframe_pass_pending_user_review / runtime_unchanged`
