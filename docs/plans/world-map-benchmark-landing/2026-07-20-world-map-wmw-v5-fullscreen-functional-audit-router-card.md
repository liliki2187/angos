# WMW v5 整页基础功能终审 Router Card

## 决策条

- **结论**：局部不通过；三栏几何与 A233 / B 通过，但 v5 可见语义尚有冻结阻断。
- **影响**：不得把 v5 原样冻结为整屏黑白布局真源，也不得进入有色稿；无需重做三栏。
- **下一步**：按 UI Designer 的 v5.1 最小修正规格生成 default / schedule-confirming 两张黑白图与差异审计，再做一次只读回归。

## 详情

- **一句话结论**：当前问题是时间后果、初始锁定、任务分类、无依据路线和审计注释混层，不是页面布局。
- **我实际做了什么**：读取 v5 原图、audit、review、A229/A232/A233、GDD、`WeeklyRunGame.gd`、内容与系统数据；依次完成 UX 老哥终审和 UI Designer 最小修正规格。
- **现在卡在哪里**：v5 尚有 2 个 P0 与主要 P1；本轮按约定只读，不生成 v5.1。
- **为什么不能跳过**：推进一天属于不可逆时间操作，错误后果会误导玩家；地区解锁状态错误会破坏左卡、地图针与 CTA 的同源状态。
- **下一步怎么验证**：两张 1920×1080 v5.1 实图，矩形差异区 + 路径 mask 审计，`outside_allowed_pixels = 0`，UX 回归 P0/P1 清零。
- **本轮不要做**：不重排三栏、不生有色稿、不改 Godot、不改 compact A5.1 frozen 合同。

## 术语版 / Routing

- **任务一句话**：审计 v5 每个玩家可见组件是否有独立用途和真实数据口径。
- **任务类型**：UI / UX / 代码与 GDD 只读核对
- **风险等级**：normal
- **当前阶段**：结构稿终审
- **目标载体**：评审文档
- **本轮交付物类型**：router_card / delivery_manifest / design_note
- **被路由对象类型**：structure_wireframe
- **本轮只验证**：功能职责、状态同步、时间口径、数据映射、玩家层 / 审计层边界。
- **本轮不做**：视觉包装、资产生产、runtime、正式合同。
- **本轮必读真源**：v5 default / audit / review、A229/A232/A233、`exploration-and-node-dispatch.md`、Weekly Run state / content / systems / game / map assembly。
- **必调 agent**：`ux_laoge` → `ui_designer`。
- **明确不调的 agent 与原因**：冷备 `game_logic_check` 未获解冻确认；本轮只做 UX 真值拦截，进入 runtime 前建议解冻。
- **被路由对象允许下一步**：v5.1 黑白局部修正与回归。
- **被路由对象禁止跳到**：有色整屏、Godot、compact 合同覆盖、生产候选。
- **停止条件**：双 agent 结论、P0/P1 清单与最小 rect 规格齐备；本轮完成。

