# WMW `schedule_gate` v0.1 派生候选复审

## 结论

`schedule_gate v0.1` 已完成 UI Designer → UX 老哥三轮回归，最终判定 **PASS（P0=0 / P1=0 / P2=0）**，可以提交用户裁决。

当前产物仍是 `derived_component_candidate_spec / TARGET_ONLY`：不是正式 UI 合同，不代表 `advance_day` 已在 Godot 实现，也不是无字有色母版或有色整屏。用户接受前不进入下一阶段。

## 候选范围

- runtime 外部位置：`[36,810,342,246]`。
- runtime-local 整数坐标为本候选权威；`[228,164]` 只记录 1280 reference，未来无字母版候选为 `[456,328] @ 0.75`。
- default / confirming 两格直接使用 v5.1 对应 342×246 真源 crop；其余状态只验证同壳几何、运行时文案与输入语义。
- 不修改三栏、B2.12、A5.1-H、地图、Godot 或 `design/ui-contracts/`。

## 关键闭环

### 输入职责

- `component_rect / input_capture_rect = [0,0,342,246]`：只负责组件归属、点外取消和 executing 全输入捕获。
- `activation_hit_rect = [12,74,318,100]`：唯一推进 / 确认推进激活区，与可见动作栏完全一致。
- 日期栏与两条信息栏为只读区域；idle / confirming 点击这些区域不得执行。
- confirming 仅在点击组件外、`Esc` 或关键 context change 时取消。
- executing 锁定完整输入捕获区，但任何位置都不得重复提交。

### 状态与边界

- 稳定可见态：`idle_enabled / confirming / executing / disabled_runtime_unavailable / disabled_zero_days`。
- `idle_error` 为 idle 的语义修饰态：保持提交前日期与剩余日，明确“未消耗天数 / 日程未变化 / 可重试”，不新增几何。
- `committed` 不是可停留皮肤；非最后一天提供 180–300ms 成功反馈，随后原子刷新；最后一天允许 0ms 直达编辑部。
- `remaining_days == 1` 使用“确认结束本周日程”，结果明确为“剩余 0 天 · 进入编辑部阶段”。
- `remaining_days == 0` 不得再次 confirming；计算统一钳制为 `max(remaining_days - 1, 0)`。
- runtime 当前没有独立 `advance_day`，真实构建只能显示 `disabled_runtime_unavailable`。

### 动态文案

- 动态摘要直接产出最终渲染整行，不再把带前缀摘要嵌入另一层“到期提示 / 限时任务”模板。
- confirming、executing、到期行、限时行均定义 0 / 1 / N 格式。
- 数量显示覆盖 `99 / 99+`；截止日覆盖两位数；`short_title` 最多 8 个全角单位。
- 缺失合法 `short_title` 视为内容合同失败；不得自由截断、缩字或换行。
- 具体任务名列表仍由右侧任务情报和具体任务行承载，日程器只显示决策所需聚合。

## 几何与文字审计

`black-white-schedule-gate-v0-1-audit.json` 当前结果：

- 真实画布：`1920×1080`。
- 六张主状态 / 边界卡：全部 `342×246`、100% 显示。
- default / confirming 对 v5.1 源 crop：逐像素一致。
- runtime 几何：全部落在组件内。
- 六格共 48 条状态文字 bbox：`0` 违规。
- 20 条最终装配压力文案：覆盖 0 / 1 / 99 / 99+、两位剩余日 / 截止日、8 全角短标题和 `idle_error`，`0` 违规。
- 中性色黑白结构板最大 RGB 通道差为 4；未生成有色资产。

## UI Designer 结论

- runtime-local 整数坐标应先于 reference 归一化；正式合同归一化留待用户接受后处理。
- 一张无字母版承担外纸、日期栏、动作栏、图标井与两条信息栏；文字、数字、箭头、叹号、progress、勾号和交互反馈全部留在 runtime。
- `committed` 只作瞬时语义节点，不占第七张主 crop。
- 旧 `region_task_schedule_v2` 只继承二次确认、无字母版 + runtime 内容和未接入前禁用；旧 1436×140 几何、asset id、atlas 切片与旧皮肤全部不复用。

## UX 回归记录

### 第一轮：FAIL，P0=0 / P1=3 / P2=1

1. 整组件命令热区会把日期与后果行变成幽灵触发面；已拆为 input capture 与 action activation。
2. `{due_summary} / {deadline_summary}` 缺 0/1/N、长任务名与数量容量规则；已补动态聚合合同与实际 bbox 压力。
3. `idle_enabled_with_real_error` 只在转移表孤立出现；已升为 `idle_error` 语义修饰态并补不扣天 / 可重试闭环。
4. committed 只有最大 300ms；已补非末日 180–300ms 最短反馈，末日仍允许立即离场。

### 第二轮：FAIL，剩余 P1=1 / P2=1

- 摘要片段仍可能被外层模板重复添加前缀，且压力测试尚未覆盖最终装配整行；已改成 `final_rendered_lines`，并补齐 0/1/99/99+ 全组合。
- `idle_error` 已可重试但未进入 hover；已同步纳入 hover / focus / pressed。

### 最终终审：PASS

UX 老哥确认此前问题全部闭合，未发现新增冲突；最终 `P0=0 / P1=0 / P2=0`，可以提交用户裁决。

## 标杆与旧资产边界

本轮是黑白结构 / 合同板，不进行有色材质放行。父级已直接对照 `clean low-poly weekly` 两张 benchmark board：当前正交纸面、单一强动作区和克制状态层不会迫使未来母版滑向旧像素、旧 atlas 或 GIS 化；真正的纸张、olive / rust / teal 权重仍需下一阶段无字有色母版单独复审。

旧 `rt-advance-day-atlas.png` 只参考日历 / 箭头语义和 ready / hover / pressed / focus 的覆盖思路；不得复用旧横向外框、颜色、强箭头、细描边、shadow 或整帧。

## 冷备审查提醒

高影响时间推进、失败恢复和 0 天阶段跳转已命中冷备 `game_logic_check` 的解冻价值窗口。建议在正式合同 / runtime 接线前由用户决定是否解冻做状态机防爆审查；不解冻时，替代方案是父级按本候选的转移表、输入语义与原子提交断言逐项验收。该提醒不阻塞当前黑白候选裁决。

## 下一 Gate

等待用户裁决：

- 接受：登记新的设计采纳项，再制作 `[456,328]` 单张无字有色母版与运行时填充回放；仍不直接生成有色整屏。
- 修订：只调整 `schedule_gate` 候选、合同板和 audit，不重开三栏或 frozen 组件。

