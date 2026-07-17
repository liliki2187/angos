# WMW 右 dossier 候选 A3 动作层级复审

> **日期**：2026-07-14
> **版本**：candidate A3 / v0.9.3
> **后续裁决**：2026-07-15 用户否决满宽青色实底重量；A3 已由 A209 / A4 / 618 取代，611 manifest 降级为 `visual_fail_secondary_affordance_too_strong_superseded_by_618`。
> **产物类型**：`runtime_state_preview`
> **状态**：程序 gate 与双 agent 复核完成，等待用户视觉裁决；未冻结、未扩动态状态。

## 一、本轮目标

A3 只修 A2 的两条 action row，不改 parent 上半部、正文、状态、`69:44` 照片图例或三份 v0.8.6 frozen：

| 行 | 点击后果 | A3 语法 |
| --- | --- | --- |
| 青色任务情报 | dossier 内原地展开 / 收起，只读，不导航、不耗时 | 文档图标 + `展开任务情报` + 下向 chevron |
| 橄榄主 CTA | 进入地区任务台，跨层导航但不耗时 | `进入地区任务台` + 右向箭头；左侧地球删除 |

任务总数继续由 `decision_facts` 承载，不再拼进 disclosure 文案。两行仍各只有一个 frozen `hit_rect`。

## 二、资产与运行时

- 两份 child 空底从明确多边形一次构造，不复用 A2 圆托 / 中央纸签，也不做擦除、模糊补洞、inpaint 或局部覆盖。
- 空底尺寸保持 `568x88` / `568x100`；alpha 连通组件均为 `1`，核心透明洞均为 `0`。
- 三个 runtime 槽内部的旧奶油圆环 / 中央纸签像素均为 `0`。
- 文案统一来自 `WeeklyRunContent.WORLD_MAP_UI_COPY`；Godot 逻辑导出 production fixture，Python / Godot 共读同一 JSON。
- 当前照片继续只作精确 `69:44` 构图图例；正式地区内容冻结后再逐区专门生图。

## 三、证据

- 605：A2 / A3 空底与 A3 runtime action 结构 QA。
- 606/607：Python 正常回填与真实 glyph alpha bbox QA，`7/7` 文字通过。
- 608/609：Godot 4.6.2 windowed OpenGL3 正常 / QA 截图。
- 610：A2 / A3 同尺度 action hierarchy 对比板。
- 611：完整 manifest；`validate_visible_field_semantics.py` 与合同校验均 PASS。

## 四、Gate 结果

| Gate | 结果 | 证据 |
| --- | --- | --- |
| 单行单控件结构 | PASS | 每行 `hit_rect=1`、可见底面连通组件 `=1` |
| 旧分裂控件残留 | PASS | 两 child runtime 槽内旧圆环 / 纸签像素 `0/0` |
| 作用域与方向符号 | PASS | disclosure=`document + chevron_down`；navigation=`label + arrow_right` |
| 运行时文案 | PASS | `展开任务情报 / 收起任务情报 / 进入地区任务台` 来自 production token |
| 文字槽 containment | PASS | 7/7 实际 raster glyph bbox 在 inner rect 内 |
| Godot 截图 | PASS | 608/609 非黑、颜色多样性通过；UI 截图未用 headless |
| QA 基线内容保留 | PASS | 右侧说明区亮像素 `2349 -> 2349`，保留率 `1.00` |
| 合同 | PASS | `design/ui-contracts/world-map/` 五份合同与页面重叠检查通过；本轮只改 provisional |

## 五、截图假通过复盘

第一次 609 丢失右侧整块说明内容，但旧 runner 仍因全图非黑与颜色数量充足而 PASS；该图已作废。capture 已改为 baseline / QA 共用一个 SubViewport 场景，并新增右侧区域保留率 gate。完整 Loop Log：`2026-07-14-world-map-wmw-right-dossier-a3-qa-baseline-loss-loop-log.md`。

## 六、双 Agent 复核

### UX 老哥

`P0=0 / P1=0 / P2=1`，可立即提交用户视觉复审。A3 已用下向 chevron 与右向 arrow 拆清原地 disclosure / 跨层导航；连续底面不再稳定误读成三个按钮。唯一 P2 是青色 disclosure 仍为满宽实底，少数用户可能把它看作另一个次级按钮，但动作范围不含糊。

### UI Designer

同意 `P0=0 / P1=0 / P2=1`。旧圆托与中央纸签已明确退役，图标 / 文案 / 符号在 frozen 槽内的对齐和留白通过；橄榄 CTA 依靠底部流程终点、纸层厚度、动作文案与右向箭头形成主权重。青色满宽实底的视觉重量接近放行下限，留给用户做审美裁决。

## 七、当前裁决点

用户只需判断：是否接受青色 `展开任务情报` 当前的满宽实底重量。

- 接受：A3 default 成为后续状态制作基线，再做展开 / 收起、hover / pressed / locked 与动态录屏。
- 不接受：只降低青色 disclosure 的描边 / 阴影 / 实底重量；不改 v0.8.6 frozen，不动橄榄主 CTA 和上半部。
