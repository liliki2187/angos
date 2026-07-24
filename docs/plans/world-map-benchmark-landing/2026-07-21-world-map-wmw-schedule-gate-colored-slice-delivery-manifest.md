# WMW `schedule_gate v0.1` 有色纵切 Delivery Manifest

## 身份与状态

- `artifact_type = derived_no_text_component_candidate`
- `version = schedule_gate_v0_1_colored`
- `status = technical_pipeline_evidence_only_not_visual_candidate_a242`
- `target_only = true`
- 用户授权：A240。
- 交付表达修订：A241。

## 历史审阅板（A242 后全部降级为技术证据）

| 文件 | 用途 | 用户判断 |
| --- | --- | --- |
| `wmw-schedule-gate-colored-v0-1-full-pipeline-walkthrough-1920x1080.png` | 完整展示 8 阶段拆图与装配链 | 仅证明技术流程，不审批整屏美术 |
| `wmw-schedule-gate-colored-v0-1-runtime-states-review-1920x1080.png` | 七个 342×246 状态的 1:1 复核 | 仅证明局部状态与文字容量 |

## 技术 QA 附录

| 文件 | 职责 |
| --- | --- |
| `wmw-schedule-gate-colored-v0-1-material-geometry-review-1920x1080.png` | imagegen 源、母版、runtime、几何 overlay 与边界；用户无需裁决 |
| `wmw-schedule-gate-colored-v0-1-audit.json` | 几何、alpha、颜色、文字、压力、hash 与 review status 真源 |
| `wmw-schedule-gate-material-ingredients-v0-1-manifest.json` | 四角色裁片、归一化统计与来源 hash |

## 真实生成与装配输入

| 文件 | 说明 |
| --- | --- |
| `wmw-schedule-gate-material-ingredients-imagegen-source-v0-1.png` | built-in imagegen 的真实四角色无字配料源，1477×1065 |
| `schedule-gate-v0-1-colored-production-brief.md` | 最终 imagegen prompt、工作坐标、材质角色与 Gate |
| `render_schedule_gate_colored_candidate_v0_1.py` | 确定性拆片、归一化、装配、状态回填、证据板和 audit 脚本 |

## 中间与母版资产

- 四张 imagegen 原始角色裁片：`ingredient-{warm|olive|ivory|ink}-imagegen-v0-1.png`。
- 四张角色归一化材料：`ingredient-{warm|olive|ivory|ink}-normalized-v0-1.png`。
- `wmw-schedule-gate-no-text-work-1368x984-v0-1.png`。
- `wmw-schedule-gate-no-text-master-456x328-v0-1.png`。
- `wmw-schedule-gate-no-text-runtime-342x246-v0-1.png`。

## Runtime 回填状态

- `wmw-schedule-gate-state-idle-342x246-v0-1.png`
- `wmw-schedule-gate-state-confirming-342x246-v0-1.png`
- `wmw-schedule-gate-state-executing-342x246-v0-1.png`
- `wmw-schedule-gate-state-runtime-unavailable-342x246-v0-1.png`
- `wmw-schedule-gate-state-idle-error-342x246-v0-1.png`
- `wmw-schedule-gate-state-confirming-last-day-342x246-v0-1.png`
- `wmw-schedule-gate-state-zero-days-342x246-v0-1.png`

## Gate 结果

- UI Designer：`PASS · P0=0 / P1=0 / P2=1`。
- UX 老哥：`PASS · P0=0 / P1=0 / P2=1`。
- 456×328 母版、342×246 runtime、两张用户板与一张技术附录尺寸通过。
- 56 条状态文字、20 条压力文案、alpha、基础状态色隔离与一母多态通过。
- 已知 P2：date carrier 下采样高度 +1px，处于 `≤1px` Gate 内。

## 未做 / 未授权

- Godot runtime 接入与真实 `advance_day`。
- `design/ui-contracts/` 升版。
- compact A5.1、B2.12、地图或三栏改动。
- 有色 1920×1080 整屏。
- 动态 committed / executing / 退出行为证据。
- Git stage、commit 或 push。

## A242 后的下一 Gate

停止下一单组件。先用 v5.1 默认态黑白布局、两张 clean-low-poly weekly benchmark board、真实默认态文案与既有 B2.12 / A5.1 局部语法制作一张完整 `1920×1080 filled-state full-screen visual style mock`，由用户判断整屏美术是否成立。通过前不进入 Godot、正式合同、atlas 或组件批量生产。
