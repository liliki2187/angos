# WMW `schedule_gate` v0.1 派生候选 Delivery Manifest

## 决策条

- **结论**：`schedule_gate v0.1` 派生候选已通过 UI / UX，当前为 `ui_ux_pass_user_decision_pending`。
- **影响**：342×246 几何、输入职责、状态矩阵、动态摘要、错误恢复与最后一天边界已有可重放证据。
- **下一步**：等待用户接受或修订；接受前不生成无字有色母版，不改正式合同或 runtime。

## Manifest

- **产物类型**：`derived_component_candidate_spec` + `black_white_contract_board`。
- **风险等级**：normal。
- **候选规格**：`docs/prototypes/world-map-wmw-black-white-structure/schedule-gate-v0-1-candidate-spec.json`。
- **真实图片**：`docs/prototypes/world-map-wmw-black-white-structure/black-white-schedule-gate-v0-1-contract-board.png`，1920×1080。
- **几何 / 文字审计**：`docs/prototypes/world-map-wmw-black-white-structure/black-white-schedule-gate-v0-1-audit.json`。
- **可复现脚本**：`docs/prototypes/world-map-wmw-black-white-structure/render_schedule_gate_candidate_v0_1.py`。
- **流程文件**：本 Manifest、同日 Router Card 与 Review。
- **上游真源**：A237、v5.1 default / confirming / audit、v5.1 assetization bridge。
- **当前状态**：`evidence_ready_user_visual_review_pending`。

## 证据

- default / confirming 两格与 v5.1 源 crop exact。
- 六张主 crop 均为 342×246、100% 展示。
- 48 条状态文字 bbox：`PASS / 0 violations`。
- 20 条最终装配压力文案 bbox：`PASS / 0 violations`。
- 输入语义：`input_capture_rect=[0,0,342,246]`；`activation_hit_rect=[12,74,318,100]`；日期与信息行只读。
- 状态边界：executing 全捕获锁、idle_error 不扣天可重试、committed 非末日 180–300ms、0 天进入编辑部、remaining days 不为负。
- runtime 真值：当前独立 `advance_day=false`，真实构建只允许 unavailable。
- UI Designer：PASS。
- UX 老哥：首轮 `P1=3/P2=1`，第二轮 `P1=1/P2=1`；全部修订后最终 `P0=0/P1=0/P2=0 PASS`。

## 能证明 / 不能证明

本交付能证明：日程器候选的静态几何、运行时分层、输入职责、状态语义、最后一天边界和文字容量已收敛，可以交用户裁决。

本交付不能证明：

- 无字有色母版已经生成或通过美术复审；
- `advance_day` 已在 Godot 实现；
- 状态切换的真实时序、动效或事务原子性已通过运行证据；
- 候选已成为正式 `design/ui-contracts/`；
- compact A5.1 或其他 WMW 组件发生任何改变。

## 未改范围

- `gd_project/`：未改。
- `design/ui-contracts/`：未改。
- compact A5.1：未改。
- 有色资产 / 有色整屏：未生成。
- Git stage / commit / push：未执行。

