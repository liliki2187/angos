# WMW 地区档案“红线升温”状态章 v5 Delivery Manifest

## 决策条

- **结论**：通过；用户已采纳 B，并升为 v5 默认黑白结构候选。
- **影响**：本交付证明 B 去重后的局部结构成立；不代表 runtime、正式合同或有色稿获授权。
- **下一步**：本轮停止；待后续明确授权再进入 runtime 或有色资产阶段。

## 详情

- **一句话结论**：两张 1920×1080 黑白候选已生成，差异严格限制在右栏顶部与地区说明文字区；B 已采纳为默认，A 为条件参考。
- **我实际做了什么**：按 UX → UI Designer 顺序完成诊断与规格；从 v4 默认图派生 A / B；生成 JSON 像素差异审计与复核文档。
- **现在卡在哪里**：无本轮阻断；A 仍缺 `earliest_deadline_day` 同源数据，因此不进入默认态。
- **为什么不能跳过**：当前代码把 `remaining_days` 当任务时间窗口，会与 `deadline_day=4` 冲突。
- **下一步怎么验证**：B 已通过实图与像素差异审计；后续若获 runtime 授权，再验证 warning / locked / chain 状态切换。
- **本轮不要做**：不改 Godot、不改正式合同、不生有色稿、不重排三栏。

## 术语版 / Manifest

- **交付对象**：WMW A5.1-H 右栏 warning 顶部状态章 A / B 对照
- **产物类型**：structure_wireframe
- **风险等级**：normal
- **它能证明**：状态章职责比较、A / B 容量、正文去除错误时间句、局部几何没有范围漂移。
- **它不能证明**：A 的 runtime 聚合、切换 / 推进日刷新、locked / chain 动态切换、最终美术质量。
- **对照真源 / 标杆**：`black-white-full-map-v4-default.png`、v4 audit / review / manifest、`WeeklyRunGame.gd` 与 `WeeklyRunContent.gd`。
- **截图 / 文件路径**：
  - `docs/prototypes/world-map-wmw-black-white-structure/black-white-redline-status-v5-a-earliest-deadline.png`
  - `docs/prototypes/world-map-wmw-black-white-structure/black-white-redline-status-v5-b-remove-stamp.png`
  - `docs/prototypes/world-map-wmw-black-white-structure/black-white-redline-status-v5-audit.json`
- **几何 / 正交检查**：自动触发—1920×1080 全图与像素差异边界通过。
- **几何触发原因**：结构稿 / 有字 mock / 宣称可继续。
- **已过 gate**：UI / UX 顺序复核；图像尺寸；允许差异区；范围外变化 0；正文时间冲突止血。
- **未过 / 待确认 gate**：runtime 动态状态；A 同源数据（仅未来条件参考）。
- **反向读法检查**：不得把 A 图中的“第4天”读成已实现 runtime；不得把 B 读成退役 locked / chain 状态槽。
- **已调用 agent / 复审**：`ux_laoge`、`ui_designer`。
- **未调用 agent 与原因**：冷备 `game_logic_check` 未获用户确认解冻；本轮不扩成规则防爆审查。
- **文档 / 实现 drift 检查**：发现 `remaining_days` 与 `deadline_day` 时间口径 drift；本轮仅从结构稿撤下错误表达，未改实现。
- **下一步允许做**：A233 与路线状态已同步；当前停止。后续只有用户另行授权，B 才进入派生 runtime 规格；A 仍须先进入数据规格。
- **下一步禁止跳到**：Godot、compact frozen 合同、有色整屏、生产候选。

## 文件清单

| 文件 | 状态 |
| --- | --- |
| `black-white-redline-status-v5-a-earliest-deadline.png` | `CONDITIONAL` |
| `black-white-redline-status-v5-b-remove-stamp.png` | `SELECTED_B_REFERENCE` |
| `black-white-full-map-v5-default.png` | `SELECTED_DEFAULT` |
| `black-white-redline-status-v5-audit.json` | `PASS` |
| `render_redline_status_decision_v5.py` | 可复现 |
| 本 manifest / router / review | 已落盘 |
