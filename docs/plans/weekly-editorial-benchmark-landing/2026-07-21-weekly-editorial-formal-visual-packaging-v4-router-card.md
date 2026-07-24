# 发刊编辑正式视觉包装候选 v4｜Router Card

## 本轮任务

在用户已冻结 v3 副头版横图结构的前提下，只增强主头版标题层级，不移动主图、meta、双页或三栏。

## 工作流

- 级别：`visible UI / focused typography correction`
- 顺序：`UX 聚焦诊断 → UI Designer 精确交接 → 父级合并 → v4 HTML 落地 → 1920×1080 主状态与最长标题压力验收`
- UX：当前 `19px` 与副头版 `18px` 感知近似同级，结论 `PASS WITH CHANGES`。
- UI：无需改 DOM；推荐真实字宽驱动的 `28px` 单行 / `24px` 双行，外框、主图和 meta 不动。
- 父级合并：采纳单一路线；真实字体压力使双行内容高出理论值 `2px`，标题盒增至 `54px`，仍与主图保留 `7px` 间隔，不缩字、不省略。

## 冻结边界

- v3 副头版横图结构继续冻结。
- 不修改 Godot、正式组件合同、GDD 或正式报道图。
- 不顺带处理其它 UI 问题。

## 输出与证据

- 原型：`docs/prototypes/weekly-editorial-formal-visual-packaging-v4/`
- 截图与审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v4/`

## 放行条件

- 用户确认主头版标题已经具有足够的头版权重。
- A01 与最长 A12 标题完整，无溢出，不侵入主图。
