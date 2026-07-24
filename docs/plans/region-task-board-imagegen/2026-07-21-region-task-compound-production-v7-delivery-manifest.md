# 区域任务 B 类型色 compound v7 正式落地交付清单

## 本轮结论

用户已授权按常驻右挂 v6 推荐方向正式落地。v7 将 B 闭合框扩展到四种任务类型、左右挂、hover / selected / focus 与固定状态 badge，并替换生产 `WeeklyRunRegionEventPin.gd`。2026-07-22 用户在最终交付后回复“继续”，按约定正式冻结为 `production_frozen`；event card 继续冻结。

## 资源与实现

- 美术真源：`design/art-direction/region-task-board/runtime-production-v7-b-type-frame/`
- 生产资源：`gd_project/Assets/ui/angus_packaging/region_task/v2/pin_compound_v7/`
- 资源元数据：`compound-production-v7.json`
- 正式 manifest：`gd_project/Assets/ui/angus_packaging/region_task/region_task_asset_manifest_v2.json`，版本 `5`
- 正式组件：`WeeklyRunRegionEventPin.gd`
- 状态链承接：`WeeklyRunRegionTaskBoardV2.gd`
- payload 风险 / 建议：`WeeklyRunGame.gd`
- 正式合同：`event_pin_contract.json` 版本 `6`、`dossier_contract.json` 版本 `4`、`component_cutout_inventory_v1.json` 版本 `3`

四类型 selected 色：

| 类型 | 颜色 | 运行语义 |
| --- | --- | --- |
| 常驻 permanent | `#7F8A47` | selected 闭合框 + 后纸 |
| 连续 chain | `#34767A` | selected 闭合框 + 后纸 |
| 隐藏 hidden | `#445967` | selected 闭合框 + 后纸 |
| 限时 temp | `#886A40` | selected 闭合框 + 后纸 |

## 已移除的粗糙程序装饰

- selected `Polygon2D` 纸背板；
- hover / selected / focus `draw_arc`；
- assigned / urgent / locked `Polygon2D + Line2D` 状态签；
- disabled `Line2D` 斜线；
- 与图钉头分离的短签背景 TextureRect。

Godot 仍保留动态 icon、标题 / meta、task_id、左右向选择、disabled 明度与 alpha 过渡；不会把运行文字烘焙进位图。

## 真实运行证据

- `00-four-kind-asset-matrix-v7.png`：拆件、左右向、四类型颜色和固定 badge 美术 QA。
- `01-five-dense-selected-v7.png`：五点密集、selected 标签优先、8px 避让、右 dossier。
- `02-right-edge-dossier-v7.png`：右边缘左挂 clamp、一体接合、assigned badge、风险等级与建议。
- `03-runtime-state-and-kind-matrix-v7.png`：四类型 hover / selected，以及 assigned / urgent / locked / focus。
- `04-hover-selected-runtime-v7.gif`：真实生产 EventPin 的 idle → hover → selected → hover → idle。
- `05-cluster-collapsed-v7.png`：八任务密集组收拢为单一非圆形数量标记。
- `06-cluster-expanded-v7.png`：同一 cluster 展开后恢复全部动态 pin 与固定 badge。

证据目录：`docs/screenshots/2026-07-21-region-task-compound-production-v7/`。

## 验证

- `validate_component_cutout_inventory.py`：通过；18 class 与路线计数不变。
- `test_region_task_manifest_v2.gd`：Godot 4.6.3 可见 OpenGL 通过。
- `test_region_task_board_v2.gd`：通过；覆盖 0 / 1 / N、五点密集、cluster、label clearance、长摘要、风险等级与建议。
- `test_region_task_board_v2_integration.gd`：通过；选中 `m330` 后，标题、追踪类型、`2天`、连续追踪风险依据、风险等级与建议均由同一 task 刷新，且无旧截稿字段残留；进入签批台链路正常。
- Godot headless 在本机仍可能触发 `signal 11`；正式结论使用指定的 4.6.3 可见 OpenGL 结果。

## 用户最终只需判断

1. 四类型 selected 的“类型色闭合框 + 同色后纸”是否足够明显但不过重；
2. 图钉头和名称横条是否已读成一件完整纸品，而非两个底板硬拼；
3. assigned / urgent / locked 小 badge 在 1× 是否够精致、不会抢类型 icon；
4. 右 dossier 的风险等级、依据与建议是否达到继续推进所需的信息密度。

若四项均可接受，建议冻结 v7 并继续下一个资产组；若有问题，只做一次针对用户指出项的定向修正，不重开 A / B / C。

## 三方最终复核

- UI Designer：`P0=0 / P1=0 / P2=0 / GO`。四类型映射、状态层级、一体接合、动态文字区、五点密集、左挂 clamp 与 dossier 信息合同均通过，建议冻结。
- UX 老哥：首轮发现截图 fixture 的跨任务数据矛盾并判 P1；同源 fixture、production `m330` 断言及 cluster 收拢 / 展开证据补齐后，最终为 `P0=0 / P1=0 / P2=0 / GO`，建议冻结且不再追加视觉修饰。
- Angus 美术指导：`P0=0 / P1=0 / P2=0 / GO`。确认 B 闭合框、四类型色、共享肩、selected 后纸、fixed badge、1× 线重与透明边缘均达到生产冻结线；`96ms` 入场 / `80ms` 回退正确继承既有合同。

用户最终裁决：接受并继续。v7 已冻结；后续只有用户明确指出回归或视觉问题时才允许定向修正。
