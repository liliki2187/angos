# WMW 功能结构纠偏 Router Card

## 目标

保留用户认可的左 / 中 / 右三栏大模块组合，重新确定每个模块的真实功能、位置、尺寸和动作层级；先交付精确 1920×1080 黑白功能结构稿，再以结构稿作为唯一布局真源生成一张 `filled_state_text_mock`。

## 用户裁决

- 认可：三栏大模块组合方向成立。
- 否决：上一张概念图的内部功能、位置、尺寸与左右下角闭合方式。
- 明确补回：左下日期 / 周程组件必须提供“推进到下一天”。
- 交付顺序：总结问题 → 黑白结构稿 → 按结构稿真实生图。

## 本轮范围

- 冻结 1920×1080 三栏责任区与 B2.12 / A5.1 已确认几何。
- 左下建立独立全局日程器：当前日、剩余天数、推进到下一天、首次点击确认、后果预览。
- 中下只保留两张真实世界回执：红线预警、深链动向；删除当前选区摘要与“世界状态已同步”等同义填充。
- 右侧 A5.1 默认收起任务情报，保留唯一最强 CTA“进入地区任务台”；A5.1 下方只放无文字、无命中区的档案载体。
- 中央主舞台必须一眼可辨为世界地图，并让左卡、地图针脚与右档案同源。
- 记录 A227、Loop Log、双 Agent 原文、结构审计和资产线 STATUS。

## 不在本轮

- 不实现独立推进日 gameplay command。
- 不把生图当成 runtime 截图、生产底图、atlas 或 manifest 源。
- 不改 B2.12 / A5.1 frozen 内部比例。
- 不增加第四地区、第三张世界回执、symbol strip、外置 CTA、第二个进入地区按钮或右下伪功能区。
- 不恢复顶部重复的剩余天数；剩余天数只由左下全局日程器拥有。

## 风险与 Gate

- 风险等级：risky，主流程可见 UI + 生图。
- `accepted_decision_cross_read`：生图前必须交叉核对 A99 / A110 / A221 / A223 / A226 / A227。
- `functional_structure_before_filled_mock`：真实功能清单和精确结构稿先于风格生图。
- `single_fact_owner`：天数只在左下显示；右册只负责当前选区。
- `action_separation`：推进日与进入地区必须在位置、材质、色彩、命中区和后果语义上分离。
- `runtime_truthfulness`：独立推进日命令未实现，不得把目标交互图声称为 runtime 证据。
- `geometry`：画布、三栏、三卡、日程器、地图、双回执和 A5.1 坐标必须与审计 JSON 一致。

## 预期交付

- 1920×1080 黑白功能结构稿 PNG。
- 可编辑 HTML 与确定性渲染脚本。
- 结构几何审计 JSON。
- UX 老哥 / UI Designer 完整复核与父级冲突处理。
- 一张按结构稿生成的真实风格 mock，产物类型为 `filled_state_text_mock`。

## 状态

`structure_wireframe_pass / filled_state_text_mock_pending_generation / runtime_advance_day_command_pending`
