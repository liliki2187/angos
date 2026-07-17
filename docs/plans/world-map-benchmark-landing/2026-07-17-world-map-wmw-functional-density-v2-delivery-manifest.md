# WMW 功能密度结构稿 v2 Delivery Manifest

> **交付已作废**：用户指出左下 64px 与右下 169px 仍是明显职责空白。请改读 v3 `functional-closure` 交付。

## 交付结论

已交付一张严格 1920×1080 的黑白功能结构稿，解决双回执过大、地图被挤压、右下纯装饰过重和左下日程器偏厚四项密度问题。B2.12 与 A5.1 frozen 坐标未改；本轮没有修改 runtime 或正式合同。

## 产物

- 结构稿：`docs/prototypes/world-map-wmw-black-white-structure/black-white-functional-density-v2.png`
- 确定性渲染脚本：`docs/prototypes/world-map-wmw-black-white-structure/render_compact_structure_v2.py`
- 审计 JSON：`docs/prototypes/world-map-wmw-black-white-structure/black-white-functional-density-v2-audit.json`
- Router：`2026-07-17-world-map-wmw-functional-density-v2-router-card.md`
- 双 Agent 复核：`2026-07-17-world-map-wmw-functional-density-v2-review.md`
- Loop Log：`2026-07-17-world-map-wmw-functional-density-loop-log.md`

## 关键几何

| 元素 | Rect | 结果 |
| --- | --- | --- |
| B2.12 ×3 | 原 A227 坐标 | 未改 |
| 紧凑日程器 | `[36,810,342,182]` | 候选 |
| 世界地图 | `[426,96,924,822]` | 高度 +126px |
| 红线回执条 | `[426,942,450,90]` | 新结构类 |
| 深链回执条 | `[900,942,450,90]` | 新结构类 |
| A5.1 | `[1398,45,480,780]` | 未改 |
| A5.1 CTA | `[1425,711,426,75]` | 未改 |
| 浅袋口 | `[1398,825,480,62]` | 新非交互收口 |
| 右下无框背景 | `[1398,887,480,169]` | 无文字 / 无命中 / 无边框 |

## Gate

- 画布：1920×1080，通过。
- `bottom_receipt_card` 被直接拉扁：否，通过。
- 新 `bottom_receipt_strip`：结构候选存在，两条各 450×90。
- 第三回执 / 回执脚注：0，通过。
- 右栏全高产品框：0，通过。
- 浅袋口文字 / 命中：0，通过。
- B2.12 / A5.1 frozen 漂移：0，通过。
- 推进日 / 进入地区作用域分离：通过。
- runtime 变化：0。

## 能证明 / 不能证明

可以证明：功能密度、结构层级、空间回收去向、主要矩形、非交互收口读法。

不能证明：最终美术、正式合同可用、真实中文容量、状态动画、Godot 运行、推进日命令、生产资产可切图。

## 状态

`structure_wireframe_pass_pending_user_review / contract_and_runtime_unchanged`
