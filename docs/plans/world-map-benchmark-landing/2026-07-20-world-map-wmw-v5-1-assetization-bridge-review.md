# WMW v5.1 资产化 Bridge 复审

## 结论

A237 冻结的 v5.1 黑白布局已被翻译为逐区资产映射、状态分层和生产顺序。UI Designer 初稿经 UX 老哥两轮回归后完成修订，当前判定为 **PASS（assetization bridge / no visual output）**，可作为下一阶段“全局日程器纵向切片”的输入。

本轮没有生成有色稿、没有修改 Godot、没有建立或修改正式合同，也没有重开三栏结构。

## UI Designer 结论

- B2.12、橄榄 CTA 与现有 69:44 照片资源存在局部复用价值。
- 日程器、A5.1-H 全高 parent、统一任务行、无路线地图底板和 clean-low-poly pin 需要新无字资产。
- 文字、日期、任务名、截止、锁定、选中、hover / focus / pressed 全部归运行时层。
- 默认 / confirming 使用同一张无字日程器，只切换文字、图标和局部状态层。
- 第一纵向切片选择日程器；它是 v5.1 新增、状态边界最清楚、且不触碰 compact A5.1 的最小高价值对象。

## UX 第一轮 FAIL 与修订

初审为 `P0=0 / P1=4 / P2=1`：

1. 日程器缺 `executing / committed / disabled / hover / focus / pressed`；已补齐，并规定确认撤回、执行锁热区与失败恢复。
2. 缺少最后一天和 0 天边界；已补 `remaining_days == 1` 的确认结果与 `remaining_days == 0` 禁用 / 转编辑部规则，禁止负数。
3. B2.12 不能整 atlas 直挂；已改为壳、底板、地球和 badge 配料条件复用，照片按 `region_id` 独立绑定。
4. A5.1-H 锁区 CTA 必须 `locked_disabled`；已补，并限制橄榄色只属于可进入态。
5. Z90 审计层需发行零像素 / 零节点；已加入独立资源、默认关闭、不入 atlas 的 Gate。

同时明确：现有北美 69:44 图只作构图占位，不能称正式地区身份资产。

## UX 第二轮冲突与父级裁决

第二轮只剩 1 个 P1：总表一处写“固定四任务展开”，任务情报头却保留 disclosure 回调。

父级没有删除 disclosure。原因是 A211 / A229 已定义 `collapsed_summary / expanded`，且收起态必须与展开态等高、不得移动 CTA；A237 只冻结当前默认截图为四任务展开，没有撤销这项既有状态能力。最终 brief 已统一为：

- 默认显示四任务 expanded；
- 任务情报头保持单一 disclosure 热区 / 回调；
- collapsed 用同高摘要替换四行区域；
- 档案高度、任务区高度和底部 CTA 坐标均不变。

该修订关闭了最后一处内部矛盾，不改变 A237 可见几何。UX 老哥最终确认：“内部矛盾已关闭，bridge PASS，可冻结为下一阶段输入。”

## 第一纵向切片 Gate

第一切片为 `schedule_gate [36,810,342,246]`，但在生产无字母版前先建立派生候选规格，至少覆盖：

- `idle_enabled → confirming → executing → committed`；
- `disabled_runtime_unavailable / disabled_zero_days`；
- `hover / focus / pressed`；
- default / confirming / executing / disabled 100% crop；
- 一张无字母版、运行时文字 / 图标、完整热区；
- 最后一天进入编辑部，不产生负天数；
- runtime 未接入时不得在真实构建中显示为可用。

## 边界

- 这是生产桥接 brief，不是设计采纳项；无需新增 A 编号。
- 下一步只允许制作日程器派生候选规格与单组件资产切片。
- 未通过单组件无字资产、文字安全、状态矩阵和 benchmark 对照前，不生成有色整屏，不进入 Godot 或正式合同。
- 本支线按 clean-low-poly weekly 临时例外不调用旧像素 / 半调 `angus_art_director`；父级必须直接对照两张 benchmark board、支线规范和纸张 / 色彩合同。
