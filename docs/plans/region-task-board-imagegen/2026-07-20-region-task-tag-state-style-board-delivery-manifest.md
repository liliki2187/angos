# 区域任务短签全类型 / 全状态美术母板 v1 交付清单

> 日期：2026-07-20  
> 产物类型：`visual_style_reference_candidate / component correction sheet`  
> 当前 Gate：`pending_user_visual_review`

**结论**：母板 v1 已明显解决当前 Godot 状态附件的程序拼块感，可进入用户方向审阅；由于 focus 权重和 disabled 语义仍有两项 P1，暂不冻结为最终美术参考。  
**影响**：本轮没有切 atlas、没有替换 Godot、没有修改既有尺寸与交互合同，event card 继续冻结。  
**下一步**：用户确认整体质感和三通道后，只做一轮定向母板修正，再拆成中性母版、类型 icon atlas 与状态 overlay kit。

## 实物证据

- 首选审核图（精确中文标注）：`design/art-direction/region-task-board/2026-07-20-region-task-tag-state-style-board-v1-annotated-cn-v3.png`
- 无字美术母板：`design/art-direction/region-task-board/2026-07-20-region-task-tag-state-style-board-v1.png`
- 像素尺寸：`1672 × 941`，16:9。
- 生成提示：`design/art-direction/region-task-board/2026-07-20-region-task-tag-state-style-board-v1-prompt.md`
- 标注版提示与文字映射：`design/art-direction/region-task-board/2026-07-20-region-task-tag-state-style-board-v1-annotated-cn-prompt.md`
- Router Card：`docs/plans/region-task-board-imagegen/2026-07-20-region-task-tag-state-style-board-router-card.md`

标注版先用真实生图在原母板外增加空标题栏、行签和逐格说明牌，再由程序只负责精确中文排版；程序没有重画 pin、短签或状态装饰。它是审核辅助图，不是生产 UI 资产。

## 16 格覆盖

1. 第一排：`permanent / temp / chain / hidden` 四类任务。
2. 第二排：`available / hover / selected / focus` 四种交互态。
3. 第三排：`assigned / urgent / locked / disabled` 四种流程态。
4. 第四排：`temp + urgent / chain + assigned / hidden + selected / mirrored edge` 四个组合压力样例。

这不是 16 个待切成品，也不是 32 个全排列状态。它只用同一纸壳家族证明每种类型与状态都已获得美术定义，并验证叠加后不会重新变成程序补丁。

## 通过项

- 四类任务始终由 pin 中心图标承载；状态变化没有改写类型语义。
- assigned / urgent / locked 获得固定右上流程签位置。
- hover / selected / focus 使用 pin 外缘反馈，与类型中心槽和动态文字分离。
- 纸背板、端帽、色脊与状态签已经表现为同一套美术纸件，不再依赖运行时现场画高可见多边形。
- 文字区保持空白，可继续服从 `200 × 72`、安全区、动态中文与左右翻签合同。

## 尚未关闭的问题

- **P1｜focus 反压 selected**：focus 同时使用多处弧线与底部笔触，扩散面积大于 selected；下一轮只保留一种深墨外缘语法。
- **P1｜disabled 语义错位**：人物加斜线更像“人员不可用”，不应代表任务整体禁用；下一轮改为整件降饱和、通用禁用斜线或无语义灰签。
- **P2｜图标偏软件化**：类型图标过于规整、等宽、对称；生产前应增加轻微剪纸偏心与印刷错位，但不加内部细节。
- **P2｜纸面略亮、略表单化**：可向灰米纸回收，并保留极低对比的 2–3 块平面明度差；禁止旧化、污渍和厚阴影。
- 右下翻签样例同时带 assigned 小签；它只证明右挂点 / 右缘镜像的构图空间，不作为最终组合语义。

## 运行时分工（待母板确认后执行）

- 美术资产：中性纸壳、类型 icon、selected 背板、hover / focus 印刷外缘、流程状态签、端帽 / 色脊与禁用洗色 mask。
- Godot：状态判断、层级组合、显隐、动画时序、文字、头像内容、锚点、左右镜像、密集避让、cluster 与 clamp。
- 禁止把每个状态生成成一张带字完整短签；生产结构应是“一枚中性母版 + 可组合 overlay kit”。

## 本轮需要用户判断

1. 新纸片、背板和状态签是否已经摆脱程序拼块感。
2. 中心看类型、右上看流程、外缘看交互的三通道是否自然。
3. 当前偏干净、偏亮、规整的现代纸品方向是否合适，还是希望纸色更灰、图标更有剪纸 / 印刷偏心感。

精确尺寸、alpha、锚点、文字容量、翻签、cluster、clamp 与能否直接进 Godot 不需要用户在本轮重判；这些合同未被修改，本图也不能证明它们。
