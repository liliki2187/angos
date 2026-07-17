# Loop Log：右 dossier 压力 fixture 泄漏到运行复审图

> **结论**：候选 A1 的文字容量通过不能证明字段语义成立；`推荐12` 只是最显眼的一处，同页标题、状态、正文、事实和任务数也混入了压力 / 演示值。
> **影响**：597 的视觉复审结论降级；A1 美术配料仍可复用，但 A1 的运行时文字不得作为正式默认态依据。
> **下一步**：候选 A2 只改运行时语义层，读取由正式 `WeeklyRunContent + WeeklyRunSystems` 导出的同一 fixture，并用 `visible_field_semantic_necessity` 阻断占位值。

## 错误结论

597 曾把“推荐12正式语义 / 单位未闭合”列为 P2，并仍判候选可交用户视觉裁决。这个判断把“文字能放进状态章”误当成“这个字段应该出现在世界地图且拥有正式数据源”。用户追问“推荐12是什么功能”后，继续要求逐项复核基础功能，才暴露同页并非只有一个错误值。

## 同页全量审计结果

| A1 可见内容 | 实际性质 | 现行正式来源 / 处理 |
| --- | --- | --- |
| `北美禁区警戒带` | 8 字标题压力串 | `WeeklyRunContent.REGION_DATA[0].name = 北美禁区带` |
| `高危` | 无地区级状态数据源 | 当前首周北美由 `region_counts.deadline` 派生为 `红线升温` |
| `推荐12` | 压力数字，且推荐人数属于具体任务 / 派遣签批 | 从世界地图彻底删除，不保留副行 |
| 两行天线 / 林线描述 | 为照片构图临时编写，不是当前 region payload | `region_brief + region_warning_text` |
| `限时2周 · 线索缺口3 · 深链1` | 混淆时间单位、locked 缺口和地区计数 | 当前首周北美为 `限时1 · 线索2 · 深链1` |
| `查看任务情报 · 12项` | 两位数容量压力串 | `region_counts.visible = 4`，显示 `4项` |
| `进入选定地区` | 正式主动作 | 保留，来自 `region_enter_text` |

## 事故链

1. A184 容量轮用最长标题、两位数任务数和最长事实串验证槽位。
2. 候选 A / A1 管线直接复用了这组字符串，没有建立“capacity fixture”和“runtime fixture”的产物边界。
3. manifest 只检查实际光栅 bbox、载体、图片比例、非黑和色彩多样性，没有要求字段登记玩家问题、页面归属与正式数据源。
4. UX / UI 复审把 `推荐12` 标为低优先级语义待办，却没有反向审计同页其余字段；父级也没有读取 `WeeklyRunGame._build_explore_payload()` 做数据对账。
5. 最终由用户在运行截图中发现一个表面词条，才触发整页组件必要性扫描。

## 为什么已有 gate 没拦住

- `text_capacity_stress` 只拥有“最长字符串能否装下”的证明权，不能拥有“字段是否必要、值是否真实”的证明权。
- `runtime_text_raster_alpha_containment` 只证明字形在框内；错误数字和错误页面归属同样可以完美居中。
- `dynamic_fields_can_bind` 没有要求绑定目标必须存在于正式 payload，也没有禁止手填演示值。
- 原复审只看视觉层级和可读性，没有做全页 `visible_component_audit`，构成 F1“验证等级冒充”与 F4“只修点名局部不扫同类”的复发。

## 修正律

1. 生产候选每个可见动态字段必须登记 `player_question / decision_value / owner_scope / data_source / source_kind / fixture_key / screenshot_value`。
2. 容量压力板与运行复审图使用不同 fixture；`stress / placeholder / fixture_only` 值不得进入用户复审截图。
3. 运行 fixture 由正式内容与状态代码导出；Python 与 Godot / HTML 必须读取同一文件，禁止各自手填。
4. 用户指出一个字段后，必须扫描该页全部可见基础组件，而不是只替换被圈出的词。
5. 新增 trial gate `visible_field_semantic_necessity` 与校验器 `scripts/ui-contracts/validate_visible_field_semantics.py`；没有稳定数据源、属于下游或与同页主承载位重复即失败。

## 停止条件

候选 A1 的无字 parent / child、照片和运行时图标可以复用；其运行文字结论不得继续引用。只有 A2 的正式数据 fixture、全组件审计、Python / Godot 同源截图、校验器与双 agent 复核齐全后，才可重新进入用户视觉裁决；仍不得据此宣称多状态生产完成。
