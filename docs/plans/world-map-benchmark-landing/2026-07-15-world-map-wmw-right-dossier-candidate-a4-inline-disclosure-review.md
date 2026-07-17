# WMW 右 dossier 候选 A4 内联任务情报复审

> **后续状态（2026-07-15）**：用户采纳 A211，将独立任务事实条与本 disclosure 合并，并把释放高度回收给地区描述。A4 已由 A5 / v0.9.5 取代；本页仅保留“任务情报去实体按钮化、橄榄 CTA 为唯一跨层动作”的有效历史证据。当前复审见 `2026-07-15-world-map-wmw-right-dossier-candidate-a5-merged-summary-review.md`。

> **版本**：candidate A4 / v0.9.4
> **设计采纳**：A209
> **状态**：默认静态态证据就绪，等待用户视觉裁决；未冻结、未生产动态状态
> **范围**：只改 `mission_intel_button` 的可见语法与 production copy；不动 parent、照片、正文、事实条、橄榄主 CTA 与三份 v0.8.6 frozen

## 1. 用户裁决与问题

用户确认 A3 的青色 `展开任务情报` 仍像一个满宽次级按钮，与下方 `进入地区任务台` 的真实功能等级不匹配。A4 不再做“调浅一点”的配色修正，而是更换控件类型：

- `任务情报`：当前 dossier 内的只读 disclosure header，不导航、不耗时；
- `进入地区任务台`：唯一跨层导航，也是本区唯一实体按钮。

历史 A3 的 production fixture、上半部、`69:44` 照片图例与橄榄 CTA 继续复用；611 manifest 已降级为 `visual_fail_secondary_affordance_too_strong_superseded_by_618`。

## 2. A4 实现

`right_mission_intel_button` 的 `284×44` export rect、父页位置与整行单一 hit rect 保持冻结，但不再等同可见按钮边界：

| 项目 | A4 默认态 |
| --- | --- |
| 背景 | 完全透明，直接露出 parent dossier 纸面 |
| 文案 | 静态章节名 `任务情报`，12px reference / 18px runtime，Regular 400 |
| 文档图标 | frozen `left_icon_zone` 内的小型单色线图标 |
| Chevron | 10×8，紧随文案并保持在 frozen `label_plate` 内 |
| `right_action_badge` | 几何保留，默认可见像素 0 |
| 分隔线 | `[16,42,252,1]`，低饱和青绿 28% alpha，仅底线 |
| 动作实体 | 无实底、无封闭外框、无 bevel、无纸厚、无阴影、无整行 pressed 槽 |

UI Designer 原建议把整个披露簇收紧到 `x=16..106`，但会越过 frozen `label_plate=[58,6,170,32]`。父级采用合同内保守等价版：文档留在 `left_icon_zone`，文案与 chevron 留在 `label_plate`，旧右 badge 槽不绘制。双 agent 输出复审确认该适配没有造成新的控件分裂或视觉失衡。

## 3. 证据

- `612`：A3 实体底、A4 透明披露和复用橄榄 CTA 的结构 QA。
- `613/614`：Python production fixture 回填与真实光栅字形 QA。
- `615/616`：Godot 4.6.2 windowed OpenGL3 默认态与 QA 截图。
- `617`：A3 / A4 同尺度视觉对比板。
- `618`：本轮 manifest。

## 4. Gate 结果

| Gate | 结果 | 依据 |
| --- | --- | --- |
| frozen 合同 | PASS | 三份 v0.8.6 frozen 字段未改；全目录合同校验通过 |
| production fixture | PASS | `WeeklyRunContent.WORLD_MAP_UI_COPY` 导出静态章节名 `任务情报` |
| 去按钮化 | PASS | 满宽实底行 0；封闭轮廓 0；bevel / shadow 像素 0 |
| 色彩注意力 | PASS | 非纸面有色面积 5.23%，低于 8% 上限 |
| frozen 槽适配 | PASS | 文案 bbox 在 label plate 内；`right_action_badge_ink_pixels=0` |
| 视觉控制数量 | PASS | 交互热区 2；disclosure toggle 1；视觉实体按钮 1 |
| 主 CTA 不变量 | PASS | 直接复用 A3 橄榄资产与 SHA-256，不重绘、不调色、不移动 |
| 文字与正文安全区 | PASS | 7/7 光栅文字 bbox 通过；正文左缘与禁入区间距未回退 |
| 照片比例 | PASS | 继续为精确 `69:44` 构图图例，Godot 使用 `KEEP_ASPECT_COVERED` |
| Godot 截图 | PASS | 固定 4.6.2 windowed；非黑与颜色多样性通过；右侧基准保留率 1.00 |
| 可见字段语义 | PASS | `validate_visible_field_semantics.py` 通过 |

616 在一次全图查看器预览中右半区没有正确显示；独立像素探针确认 615/616 右侧亮像素均为 `2196`、保留率 `1.00`，右区裁片内容完整，因此判定为查看器预览问题，不改截图 gate，也不误报 Godot 丢层。

## 5. 双 Agent 输出复审

UX 老哥：`P0=0 / P1=0 / P2=1`。A3 的动作伪并列、契约语义滞后与命令语气均已修复；A4 默认态可以交用户。唯一 P2 是动态状态尚未验证，不能冻结完整状态矩阵。

UI Designer：`P0=0 / P1=0 / P2=1`。字号、字重、光学中心、左对齐、chevron、分隔线、有色面积和主次层级均通过；frozen 适配未造成新问题。橄榄 CTA 仍是唯一具有完整实底、边框、厚度、阴影和前进箭头的按钮。

## 6. 测试说明

- 周循环 `test_phase_flow.gd`、`test_settlement_result.gd`、`test_weekly_run_layout.gd` 均报告 `OK`，runner 退出码为 0。
- runner 收尾仍打印一组与本轮无关的 `EditorialPhase/.../StatsScroll` 旧路径错误；该噪音未由 A4 引入，也不作为 A4 通过依据，后续应在 editorial 测试线单独清理。

## 7. 待用户裁决

本轮只需要判断：A4 是否已让 `任务情报` 读成可展开的档案章节，而橄榄条仍是唯一进入下一层的实体按钮。

用户确认默认态后，下一轮才制作并录屏验收 `hover / focus / pressed / expanded / locked`。动态状态继续禁止满宽实底、封闭外框、纸厚、阴影和 `right_action_badge` 复活；expanded 必须让 chevron 与邻近内容同步，并保证橄榄 CTA 仍是稳定视觉终点。
