# WMW 右 dossier 候选 A2 语义与全组件审计复审

> **日期**：2026-07-14
> **版本**：candidate A2 / v0.9.2
> **产物类型**：`runtime_state_preview`
> **裁决状态**：语义数据、照片比例与上半部证据可复用；用户已确认照片仅为构图图例，并判两条 action row 的“伪三控件 + 动作伪并列”未通过。A2 未冻结，动态状态与其它 class 未生产。

## 1. 触发与事故结论

用户追问候选 A1 状态章中的“推荐12是什么功能”，并要求以后由 AI 主动过一遍基本功能和组件。对照现行玩法真源后确认：世界地图只选择地区，具体任务与 1-3 人派遣发生在进入地区之后，因此不存在稳定的地区级推荐人数。

继续扫描同页后发现，A1 不只一个字段有问题：标题、泛化状态、两行正文、facts 与任务数也来自容量压力 / 演示 fixture。597 因此降级为 `visual_fail_fixture_semantic_leak_superseded_by_604`；A1 的无字美术、照片比例、页眉轴和正文安全内区仍可复用，但它不再是玩家视觉候选。事故复盘见 `2026-07-14-world-map-wmw-right-dossier-fixture-semantic-leak-loop-log.md`。

## 2. A2 正式运行字段

候选 A2 的 Python 与 Godot 不再各自手填字符串，而是共同读取 Godot 从 `WeeklyRunContent + WeeklyRunSystems + WeeklyRunState` 导出的 JSON：

| 槽位 | A2 可见值 | 正式来源 / 作用域 |
| --- | --- | --- |
| title | `北美禁区带` | `REGION_DATA[0].name`，地区身份 |
| status | `红线升温` | 可见节点中的限时状态派生，地区当前状态 |
| body | `都市传说与军事封锁交叠。` / `本周剩余 7 天，红线稿应优先处理。` | 地区 hint + 本周全局剩余时间 |
| facts | `任务构成 · 限时 1 · 线索 2 · 深链 1` | 当前地区可见节点分类明细 |
| mission | `查看任务情报 · 4项` | 当前地区可见节点总数，只读预览入口 |
| primary | `进入选定地区` | 当前地区解锁状态与进入动作 |

`推荐12 / 北美禁区警戒带 / 高危 / 限时2周 / 线索缺口3 / 12项` 等旧压力值均显式登记到 `removed_fixture_fields`，不得进入 A2 卡面。

## 3. 全组件必要性审计

598 覆盖 8 个功能组件与 2 组按钮图标配置，共 10 个审计条目。每项均登记玩家问题、存在理由、唯一数据源、交互性和 `keep / change`；没有只检查用户点名的状态章。

- 保留并绑定正式数据：标题、照片、主 CTA。
- 修正职责或内容：状态章、正文、facts、任务情报按钮、主按钮图标配置。
- 状态章从两层信息收敛为一个状态；主按钮从 `arrow + check` 改为 `globe + arrow`。
- A189 已采纳的任务情报预览入口与 v0.8.6 frozen 槽位继续保留。UX 老哥提出的结构删除方向已登记，但本轮未越权执行。

## 4. 证据与 Gate

- 598：全组件功能与必要性审计板。
- 599/600：Python production fixture 回填与真实 raster glyph bbox QA。
- 601/602：Godot 4.6.2 windowed OpenGL3 真实运行与 QA；截图脚本保留两次 `frame_post_draw`、全黑拒绝与相对基线完整性检查。
- 603：A1 / A2 同母版对照，单独放大 header、正文 / facts 与两条 action row。
- 604：A2 manifest。

关键结果：

| Gate | 结果 | 证据 |
| --- | --- | --- |
| production fixture provenance | PASS | `production_runtime_export=true`，Python / Godot 同读一份 JSON |
| visible field semantics | PASS | `validate_visible_field_semantics.py`；6/6 可见动态字段与 fixture 完全一致 |
| visible component audit | PASS | 10/10 审计条目，顺序与 expected ids 一致 |
| stress fixture not visible | PASS | 旧压力值与 A2 screenshot values 交集为 0 |
| raster glyph bbox | PASS | 7/7；独立字体重放 validator 通过 |
| header optical axis | PASS | 最大偏差 `0.5px@2x` |
| Godot content | PASS | 601/602 为 `1920x1080`，采样颜色 `3799/3905`，非黑有效 |
| frozen contracts | PASS | 三份 v0.8.6 frozen 字段未改；零 imagegen、零其它 class 生产 |

## 5. 双 Agent 终审

### UX 老哥增量确认原文

> 两项均已消费：facts 增加“任务构成”后不再冒充地区状态；“本周剩余 7 天”已明确全局周时间。更新后分级为 `P0 0｜P1 3｜P2 1`。P1 分别为北美标题与金字塔照片的地区身份关系、两条 action row 的三段式 / 分裂按钮观感、任务预览与主 CTA 视觉权重过近；P2 为 header globe 与 primary globe 同屏语义重复。A189 与 v0.8.6 frozen 下暂缓的结构建议不算本轮实现缺陷。A2 可按组件视觉候选交用户裁决，不能称完整 UX 终验通过。

### UI Designer 增量确认原文

> 两项语义问题均已消费：“本周剩余 7 天”不再与 facts 的“限时 1”混淆；“任务构成”明确 `1/2/1` 是分类明细，按钮“4项”可自然理解为明细总数与入口规模。`P0` 无；`P1` 为双按钮仍有三段式视觉可能被误读为分裂按钮，受 frozen 结构约束，不算本轮缺陷；状态章对比度、审计口径“8 个组件＋2 组图标配置”、双 globe 轻度重复为 `P2`。仍可交用户视觉裁决。

## 6. 用户需裁决的三个观感点

1. **地区身份**：用户是否接受“北美禁区带”使用雷达、金字塔与荒漠天线的异常场景；若不接受，下一轮只替换同规格 `69:44` 照片，不改槽位。
2. **按钮整体性**：左右圆框与中央米白板是否仍让一条 action row 看起来像三个独立控件。运行时必须保证整行只有一个 hit rect；未来若修视觉边界，需要先明确是否允许升合同 / 重做 child 母版。
3. **主次权重**：青色任务预览是否抢过橄榄绿主 CTA。A199 的色族不撤回，但可在后续状态皮肤轮降低 secondary 对比、强化 primary 整行反馈。

## 7. 当前结论

A2 已完成本轮数据目标：地区级推荐人数退役；全部可见字段绑定正式 region payload；Python / Godot 同源；旧压力值由硬 gate 阻断。用户复核后确认照片只承担构图图例，正式地区需按确定内容专门生图；同时确认任务情报与进入地区不是并列动作，当前两行却使用同模板、同方向且每行看似三个控件。A2 因此降级为 `visual_fail_action_scope_and_affordance`：parent 上半部、正文、状态、照片规格和 production fixture 可复用，两份 action child 默认态不得冻结或直接扩展状态。

## 8. 用户裁决后的功能解释与下一步

- 青色行：在当前 dossier 内打开只读摘要；不切页、不选择任务、不派遣、不扣天数。
- 橄榄绿行：离开世界地图并进入地区任务台；切页但不扣天数，后续派遣签批才消耗时间。
- 每行左图标、中标签、右符号共同组成一个命令，只有一个整行 `hit_rect`；三部分没有三种独立功能。
- 下一版先保持 A196 的 `284px` 同宽共轴与 v0.8.6 frozen 几何，重做内部视觉：secondary 使用薄纸披露语法与展开符号，primary 使用唯一橄榄绿实体压板与跨层箭头。若弱化圆槽后仍被误读，再请求显式升版。
- `4项` 是地区可见任务总数，但 popover 只承诺 2–3 条摘要，口径仍需收敛；不得未经裁决直接沿用到下一候选。
