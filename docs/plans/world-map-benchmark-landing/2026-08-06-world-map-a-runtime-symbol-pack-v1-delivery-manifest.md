# 世界地图 A 风格真实符号包 v1 交付清单

## 结论

用户指出的三类粗糙程序符号已由真实 ImageGen 位图替换。当前画面仍是 `runtime_state_preview`，但 A289 的资产来源问题已在资源、代码、测试和双审层关闭；等待用户依据新截图进行视觉 Gate。

## 资产来源矩阵

| 可见对象 | 美术来源 | 本地处理 | Runtime 继续负责 |
| --- | --- | --- | --- |
| 芥末 UFO 便签 | Codex 内置 ImageGen，参考 A 风格稿 | 色键去背、透明裁边、等比缩放为 `228×256` | 两行中文、位置、显隐 |
| 三窗共享海线事件牌 | Codex 内置 ImageGen，参考 A 风格稿 | 色键去背、等比缩放为 `224×84` | story payload、位置、显隐 |
| Eye default / selected / selected_warning / locked | 同一张 ImageGen 2×2 四态母版 | 色键去背、四象限拆分、统一 `144×144` 注册框 | 状态选图、编号、地区名、状态文字、Button、焦点与 hit rect |
| 机构连接线与 hover/focus/blocked 直线 | Godot runtime | 无 | 允许继续程序绘制；它们不是品牌贴纸美术 |

## 运行规格

- UFO：source `228×256`，display `[563,218,114,128]`，两行文字 safe rect 位于父节点 `[12,78,90,36]`。
- 三窗事件牌：source `224×84`，display `[718,266,112,42]`，无文字、无热区。
- Eye 四态：source 均为 `144×144`，display 均为 `72×72`，`STRETCH_KEEP_ASPECT_CENTERED`，`MOUSE_FILTER_IGNORE`。
- 程序品牌美术：`false`；`MapDecor` / `Beacon` 中已无 `draw_polygon / draw_polyline / draw_arc / draw_circle`。

## 自动 Gate

- Godot 4.6.2：`test_world_map_integrated_prototype.gd OK`。
- 交互节点仍恰好 8 个。
- Schedule 整树 pointer / focus 消费均为 0。
- locked 点击不替换 selected 或 dossier。
- disclosure 展开前后 CTA `global_rect` 不变。
- UFO、三窗与四态 eye 逐项断言资源路径、source / display、stretch、mouse-ignore 与 `programmatic_final_art=false`。
- alpha manifest：6 张派生纹理均有透明角、有效 alpha bbox，无纯色键背景残留。

## 真实证据

目录：`docs/screenshots/2026-08-06-world-map-a-runtime-symbol-pack-v1/`

- `01-selected-collapsed.png`
- `02-locked-feedback.png`
- `03-selected-expanded.png`
- `04-hit-rect-review.png`
- `05-interaction-state-sequence.gif`

## 双终审

- UI Designer：`PASS / P0=0 / P1=0`。两项非阻塞 P2：事件牌不得继续缩小或降低海线对比；UFO 文案维持两行与当前字量。
- UX 老哥：`PASS / P0=0 / P1=0`。初始 P2 为四态路径矩阵未逐态执行，已在终审后补齐并通过自动测试。
- 综合结论：资产 provenance Gate 关闭；仍须由用户决定新符号的最终观感是否通过。

## 阶段边界

- 不把本轮升级为 `production_frozen`。
- 用户确认前不扩产东亚 / 太平洋正式故事图，不接正式 `WeeklyRunGame`。
- 若用户仍不认可，只调整点名符号的生成美术，不重开 A282 布局、功能合同、地图板或北美新闻母图。
