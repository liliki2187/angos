# 派遣签批台资产化生产规格

> **状态**：2026-06-16 规格草案；P0 manifest 草案与安全区 overlay 已落地，等待正式资产生产与 Godot 接入。
> **目标**：把“选定任务后，派遣队员执行”的页面从暗色三栏数据面板，改成可资产化落地的“主编外勤签批台”。保留三段式流程与三栏职责，不重做探索流程。
> **读取前置**：`docs/设计采纳记录.md`、`docs/design-decisions/core-mechanics.md`、`docs/design-decisions/ui-ux-decisions.md`、`docs/design-decisions/art-direction-decisions.md`、`docs/onboarding/assetized-ui-production-chain.md`、`design/gdd/exploration-and-node-dispatch.md`。

---

## 0. 一句话合约

```text
派遣签批台：为当前已选任务配置本次骰池，确认是否消耗 X 天开始调查。
```

本页不是世界地图，不重新选择地区；不是区域任务台，不比较所有任务；不是判定页，不展示掷骰结果。玩家只做一件事：读当前任务，挑 1-3 名合法队员与可用支援，复核达标率 / 风险 / 阻断原因，然后签批外勤。

---

## 1. 当前问题定性

现有 Godot 派遣页已经有正确流程骨架：

- `world -> region -> dispatch` 三段式职责成立。
- `DispatchView` 下有左任务档案、中本次骰池、右签批复核。
- `DispatchDeskArt` 已经提供暗色工作台氛围，现有素材目录为 `gd_project/Assets/ui/angus_packaging/dispatch/`。

当前主要问题不是流程，而是资产化断层：

1. **背景图仍只是氛围底图**：`dispatch-signoff-desk-v2.png` 被整屏铺底，真正的任务纸、候选卡、槽位、复核纸和 CTA 仍靠普通控件硬贴。
2. **可交互对象没有状态资产**：候选队员、已选槽、CTA、返回按钮、支援槽没有完整 default / hover / selected / pressed / disabled / loading 契约。
3. **动态文字没有可写区契约**：任务名、brief、风险、达标率、候选姓名、dice net 摘要、阻断原因仍依赖控件矩形，不等于视觉安全区。
4. **职业幻想没有进入功能物件**：玩家看到的是“页面上有编辑部背景”，而不是“我在签批一份外勤单，把记者证放进本次骰池托盘”。
5. **复核信息仍偏调试读数**：右侧需要只做最终签批复核，避免把候选 hover 拆解、公式解释和调试指标常驻。

结论：不重做流程；重建派遣签批台资产包、manifest 和验收状态。

---

## 2. 跨分类约束

本规格必须同时继承机制、UI 和美术三类采纳记录：

- 机制侧：1-3 名员工合法派遣、相关骰面有效点、`need_target`、实际达标率、剩余天数、潜在有效点不足、节点可见性。
- UI 侧：A7 派遣配置围绕“本次骰池”；A29 三段式；A30/A31 派遣签批台物件化；A50/A56/A61 资产化安全区、状态和闭环。
- 美术侧：现代异常周刊、深海军蓝工作台、暖白新印刷纸、红 / 青套印、高清微像素、半调；不得滑向旧档案、旧报纸、泛黄 sepia 或普通 SaaS 面板。

如果后续只改骰池、达标率或候选排序，也必须至少回读 `core-mechanics.md` + `ui-ux-decisions.md`；如果涉及 PNG、生图、像素、纸张、印章、签批台，则必须补读 `art-direction-decisions.md`。

### 2.1 子 agent 合并结论

- `ui_designer`：三栏结构成立，但页面应读成“左任务档案 / 中本次骰池 / 右签批复核”的签批工作台，而不是后台数据面板；P0 资产必须覆盖顶部频道条、任务纸、员工卡、已选槽、骰面 tile、排序签、复核纸、风险章和签批 CTA。
- `ux_laoge`：不能只按组件验收，必须按“玩家签批前要知道什么”验收。右栏必须承载不可逆范围、特殊约束、阻断原因和失败后果；规格必须增加 `DecisionFactMatrix`，防止资产拆分后漏掉跨栏决策事实。
- `angus_art_director`：P0 资产不能是整屏桌面图加旧控件贴片，必须是一组可装配的签批物件。动态中文、数字、概率、状态、真实任务名、按钮文案全部由 Godot 渲染；图片只承载桌面、纸边、夹具、低权重半调、无文字装饰和交互状态底材。

### 2.2 DecisionFactMatrix

每个派遣任务不只按“左 / 中 / 右组件”验收，还必须按下表逐项验收。每条事实只能有一个主承载位，其它位置只能引用或呼应，避免同一信息重复三次，也避免某个分类被遗漏。

| 决策事实 | 玩家问题 | 主承载位 | 引用 / 呼应位 | 代码字段 / 数据源 | 截图验收 |
| --- | --- | --- | --- | --- | --- |
| 当前任务身份 | 我现在签的是哪一件事？ | 左 `ds_task_brief_sheet.title` | 右复核纸 `summary` | selected task id / title / type | 长任务名不出框，右侧只摘要不重复长文 |
| 任务需求 / 目标 | 这事需要什么能力、多少点？ | 右 `summary` + `probability` | 中候选卡相关骰面高亮 | `need_tags` / `need_target` | 有效点 / 目标只在右栏主表达 |
| 特殊约束 | 这是普通、截稿、深度链还是黑骰任务？ | 右 `special_constraint` | 左任务纸状态条、风险章颜色 | task flags / deadline / chain id | deadline / chain / none 三态都有截图 |
| 耗时与剩余天数 | 这次会消耗几天，消耗后还剩几天？ | 右 `action_scope` | CTA 状态只作呼应，不承载天数 | cost_days / week_days_left | 剩余两位数、天数不足、消耗后 0 天都不出框 |
| 已选人数 | 本次骰池有几个人，还能加谁？ | 中 `ds_selected_slot_atlas` | 容量徽记 / 候选卡 blocked_full | selected_staff_ids | 0/3、1/3、2/3、3/3 与满员点击都有截图 |
| 员工贡献 | 为什么这个人适合？ | 中 `ds_staff_card_atlas.dice_net` | 已选槽 contribution 摘要 | staff dice net / contribution | 首屏优先展示完整 6 面；若布局不足，常驻紧凑摘要并在 hover / 详情展示完整 6 面 |
| 有效点 / 达标率 | 这组人能不能过？ | 右 `probability` + `coverage_strip` | 风险章 | effective_points / target / success_rate | 低概率、高概率、刚好达标、缺口态都有截图 |
| 缺口 / 阻断原因 | 为什么不能签？差在哪里？ | 右 `blocking_reason` | 被点候选卡的局部反馈 | validation result / block code | 未选人、天数不足、潜在点不足、满员、已处理节点 |
| 失败后果 | 失败会发生什么？ | 右 `failure` | 左任务纸只保留短标记 | failure consequence config | 最长失败后果不压装饰 |
| 不可逆范围 | 点 CTA 后到底发生什么？ | 右 `action_scope` + CTA confirm state | CTA pressed / stamped | dispatch execution pipeline | pressed / confirm_pending / loading / stamped 都可见 |
| 支援 / 临时线人 | 额外资源怎么进入骰池？ | 中 `ds_support_slot_atlas` | 右 action_scope 只汇总 | support items / temporary staff | 道具槽和员工槽职责不同，不混用 |
| 返回状态 | 签批或返回后回到哪里？ | 左 `ds_back_tab_atlas` | 页面状态机 | selected region / selected task | 返回区域后保留地区与任务选中态 |

---

## 3. 页面功能边界

本页显示：

- 当前任务 brief：任务标题、任务性质、故事钩子、耗时、特殊约束、失败后果。
- 本次骰池：固定 1-3 个员工槽位、道具 / 支援槽、临时线人作为候选员工加入。
- 候选队员：按任务贡献排序，位置稳定，点击加入 / 移出，不因选中而跳位。
- 复核结果：有效点、目标、达标率、风险、缺口、阻断原因、主 CTA。
- 返回区域任务台：保留当前地区与当前任务选中态。

本页不显示：

- 世界地图 / 区域地图主体。
- 区域内其它任务的完整比较。
- 全局宏观五维大仪表盘。
- 完整结算结果或骰子判定动画。
- 全局“下一天”或“进入编辑部”跨阶段主按钮。
- 常驻调试拆解，例如每个候选加入后的完整来源变化表。

---

## 4. 桌面 16:9 布局合约

默认以 `1920x1080` 设计和验收，只做桌面 16:9。

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  64-72 顶部低权重频道条：刊名 / 当前周 / 剩余天数 / 返回主菜单              │
├───────────────┬───────────────────────────────────────┬──────────────────────┤
│ 左 470-520    │ 中 860-960                             │ 右 380-430           │
│ 任务档案夹    │ 本次骰池签批台                         │ 签批复核纸           │
│               │                                       │                      │
│ 返回区域任务台│ 1. 员工槽位 1-3                         │ 有效点 / 目标        │
│ 任务标题      │ 2. 道具 / 支援槽                        │ 达标率 / 风险        │
│ brief         │ 3. 候选队员卡网格                       │ 缺口 / 阻断原因      │
│ 耗时 / 截稿   │ 4. hover 轻提示                         │ 主 CTA               │
└───────────────┴───────────────────────────────────────┴──────────────────────┘
```

硬规则：

- 顶部 HUD 不得超过 72px；派遣页的视觉重心在签批台，不在全局指标。
- 左栏只保留当前任务的一份档案，不铺其它任务。
- 中栏是主舞台，候选队员卡不被复核信息挤出首屏。
- 候选队员卡首屏优先展示完整 dice net；如果 1920x1080 下为了保证 1-3 已选槽、候选卡网格和右侧复核纸稳定而确实放不下，才退为摘要常驻 + hover / 详情完整 6 面。
- 右栏是签批复核，不承担候选详细拆解的常驻展示。
- 主 CTA 固定在右下，文案只保留动作 `签批外勤`；耗时、消耗后剩余天数和 disabled 阻断原因必须放在右侧复核纸 `action_scope` / `blocking_reason`。

---

## 5. 元素归属表

| 元素 | 玩家问题 | 动态 | 交互 | 归属 | 生产要求 |
| --- | --- | --- | --- | --- | --- |
| 签批台底图 | 我在什么工作台上派遣？ | 否 | 否 | 烘焙底图 | 暗色编辑桌、印刷机、灯、纸堆、记者证氛围；中央和三栏承载区不得烘焙真实文字或按钮 |
| 顶部频道条 | 当前周、剩余天数和全局状态是什么？ | 是 | 少量 | 独立低权重 strip + 动态文字 | 高度 64-72px；只做世界状态徽记，不抢本次骰池 |
| 任务档案纸 | 当前任务是什么？ | 是 | 少量 | 独立组件 + 动态文字 | 标题、brief、耗时、特殊约束有 `content_rects`；红/青状态只给槽位 |
| 返回区域任务台 | 回到上一层 | 是 | 是 | 独立按钮 atlas | default / hover / pressed / disabled；低于主 CTA 但点击面积稳定 |
| 已选员工槽 | 本次骰池有哪些人？ | 是 | 是 | 独立槽位 atlas + 动态文字/头像 | empty / hover / occupied / remove-hover / invalid；不能自动替换 |
| 候选员工卡 | 谁适合这个任务？ | 是 | 是 | 独立卡 atlas + 动态文字/头像/dice net | normal / hover / selected / unavailable / assigned；位置稳定 |
| dice net 区 | 这个人为什么适合？ | 是 | 否/弱交互 | Godot 动态渲染 + 卡片安全区 | 首屏优先完整 6 面；布局不足时用摘要常驻 + hover / 详情完整 6 面；横向 chip 只做极小摘要或道具 |
| 候选排序签 | 当前为什么这样排序？ | 是 | 是 | 独立 tab atlas + 动态文字 | contribution / risk / time 等模式；selected 不改变卡片稳定位置 |
| 道具 / 支援槽 | 有没有额外骰池资源？ | 是 | 是 | 独立组件 | empty / available / selected / disabled；与员工槽职责分离 |
| 复核纸 | 当前组合能不能签批？ | 是 | 否 | 独立纸面 + 动态文字 | 有效点、目标、达标率、风险、缺口、失败后果、阻断原因各有槽位 |
| 风险印章 | 这次风险多高？ | 是 | 否 | 独立 stamp atlas | stable / risky / blocked / deadline；只辅助，不替代文字 |
| 签批确认章 | 本次是否进入盖章确认？ | 是 | 否 | 独立 approval stamp atlas | confirm_pending / stamped / cancelled；只做动作反馈，不烘焙结论文案 |
| 主 CTA | 下一步做什么？ | 是 | 是 | 独立 CTA atlas | default / hover / pressed / disabled / focus / loading；pressed 必须像盖章，必要时进入 confirm_pending |

---

## 6. P0 资产包

目标目录：

```text
gd_project/Assets/ui/angus_packaging/dispatch_signoff/
```

### 6.1 必需资产

| asset_id | 文件建议 | 类型 | 说明 |
| --- | --- | --- | --- |
| `ds_desk_base` | `ds-desk-base.png` | 不透明底图 | 深色主编签批桌；只承载环境、夹具、低权重装饰，不含动态 UI 文字 |
| `ds_top_channel_strip` | `ds-top-channel-strip.png` | 九宫格 / 透明组件 | 顶部低权重频道条，承载刊名、周数、剩余天数、世界状态徽记安全区 |
| `ds_task_brief_sheet` | `ds-task-brief-sheet.png` | 九宫格 / 透明组件 | 左栏任务档案纸，含标题、brief、meta、特殊约束安全区 |
| `ds_back_tab_atlas` | `ds-back-tab-atlas.png` | atlas | 返回区域任务台按钮：default / hover / pressed / disabled |
| `ds_selected_slot_atlas` | `ds-selected-slot-atlas.png` | atlas | 已选员工槽：empty / hover / occupied / remove-hover / invalid |
| `ds_staff_card_atlas` | `ds-staff-card-atlas.png` | atlas | 候选员工卡：normal / hover / selected / unavailable / assigned / blocked_full |
| `ds_dice_tray_base` | `ds-dice-tray-base.png` | 九宫格 / 透明组件 | 中央本次骰池托盘，容纳 1-3 员工槽、道具槽、临时线人提示 |
| `ds_dice_face_tile_atlas` | `ds-dice-face-tile-atlas.png` | atlas | 卡片内简骰面 tile：normal / highlighted / counted / ignored / risky |
| `ds_sort_tab_atlas` | `ds-sort-tab-atlas.png` | atlas | 候选排序 / 视图切换签：default / hover / selected / disabled |
| `ds_support_slot_atlas` | `ds-support-slot-atlas.png` | atlas | 一次性道具 / 支援资源槽：empty / available / selected / disabled |
| `ds_review_sheet_base` | `ds-review-sheet-base.png` | 九宫格 / 透明组件 | 右栏签批复核纸，含达标率、风险、缺口、阻断原因、后果说明槽 |
| `ds_coverage_strip_atlas` | `ds-coverage-strip-atlas.png` | atlas | 需求覆盖条 / 达标进度底材：empty / low / enough / strong / blocked，只做解释层，不冒充成功结论 |
| `ds_risk_stamp_atlas` | `ds-risk-stamp-atlas.png` | atlas | 风险印章：stable / risky / deadline / blocked |
| `ds_status_stamp_atlas` | `ds-status-stamp-atlas.png` | atlas | 任务状态章：normal / deadline / chain / black_dice / resolved / expired |
| `ds_approval_stamp_atlas` | `ds-approval-stamp-atlas.png` | atlas | 盖章反馈章：confirm_pending / stamped / cancelled |
| `ds_cta_signoff_atlas` | `ds-cta-signoff-atlas.png` | atlas | 主 CTA：default / hover / pressed / disabled / focus / loading |

### 6.2 P1 可选资产

| asset_id | 说明 |
| --- | --- |
| `ds_capacity_badge_atlas` | `0/3`、`1/3`、`2/3`、`3/3` 的小容量徽记底 |
| `ds_deadline_note_atlas` | 截稿 / 突发任务专属红色 note |
| `ds_chain_note_atlas` | 深度链 / 连续追踪青色 note |
| `ds_hover_hint_sheet` | 候选卡 hover 时的轻提示纸 |
| `ds_loading_stamp_fx` | 签批 loading / 盖章短动效帧 |

---

## 7. 交互状态矩阵

| 组件 | default / normal | hover | pressed | selected / occupied | disabled / invalid | loading |
| --- | --- | --- | --- | --- | --- | --- |
| 返回区域任务台 | 可返回 | 边缘提亮 | 下沉或暗化 | 不适用 | 不可用时灰化 | 不适用 |
| 候选员工卡 | 可选候选 | 轻抬 + 显示加入预览 | 轻压 | 已选高亮但原位不跳 | 已占用 / 不可用明确灰化 | 不适用 |
| 已选员工槽 | 空槽 | 可放入提示 | 不适用 | 显示头像、姓名、核心贡献、移出 affordance | 人数上限 / 非法组合提示 | 不适用 |
| 支援槽 | 可用道具 | 高亮 | 轻压 | 已选择 | 不可用 / 耗尽 | 不适用 |
| 风险印章 | 根据复核结果显示 | 不适用 | 不适用 | stable / risky / deadline | blocked | 不适用 |
| 主 CTA | 可签批 | 边缘提亮 | 盖章下压 | 不适用 | 显示阻断原因，不像可点击 | 短暂签批中 |

### 7.1 页面 / 任务 / 复核状态

| 对象 | 必需状态 | 说明 |
| --- | --- | --- |
| 页面 | no_task / task_selected / no_staff / partial_staff / full_staff / executable / blocked / executing / resolved_return | 页面状态驱动左中右的空态、可签、阻断和返回 |
| 任务 | normal / deadline_active / deadline_expired / chain_current / black_dice_risk / resolved / hidden | 特殊任务必须进入固定 `SpecialConstraintSlot`，不能只散在 brief 里 |
| 候选队员卡 | normal / hover / selected / disabled / blocked_full / unavailable_future / assigned_elsewhere | 满员点击必须就地反馈，不得沉默 |
| 已选槽 | empty / filled / hover_remove / remove_pressed / invalid | 移出 affordance 要贴近槽位，不做全局 toast |
| 签批纸 | empty / blocked / risky_ready / ready / confirm_pending / stamped / loading | `confirm_pending` 用于二次盖章或短 hold，避免不可逆动作黑箱 |
| CTA | default / hover / pressed / disabled / focus / loading | CTA 本体只负责动作入口；真实后果由复核纸 `action_scope` 承载 |

### 7.2 阻断清单

阻断原因必须同时写入代码、manifest QA 和截图验收：

- 未选任务。
- 未选队员。
- 已满 3 人后继续点击新候选。
- 剩余天数不足。
- 节点已处理或派遣已锁定。
- 截稿已过期。
- 缺少可计入相关骰面 / 潜在有效点不足。
- 道具不可用或已耗尽。
- 执行中 `dispatch_locked`。
- 资产安全区失败：动态文字进入 `no_text_rects`，或 `hit_rect` / `hover_rect` 与视觉对象不一致。

状态验收要求：

- pressed 不能只触发代码，必须有视觉变化。
- disabled 必须一眼不像可点击对象，并在复核纸给出简短原因。
- 候选卡 selected 不能改变候选列表位置。
- 人数满时点击新候选不能自动替换，必须提示先移出某人。
- CTA 文案只归 `ds_cta_signoff_atlas` 的 label 槽；复核纸只能提供 `cta_mount` 和 `blocking_reason`。

---

## 8. Manifest 最低规格

建议文件：

```text
gd_project/Assets/ui/angus_packaging/dispatch_signoff/dispatch_signoff_asset_manifest.json
```

每个资产至少声明：

```json
{
  "id": "ds_cta_signoff_atlas",
  "role": "primary_cta",
  "asset_paths_by_state": {
    "default": "assetized/ds-cta-signoff-default.png",
    "hover": "assetized/ds-cta-signoff-hover.png",
    "pressed": "assetized/ds-cta-signoff-pressed.png",
    "disabled": "assetized/ds-cta-signoff-disabled.png",
    "focus": "assetized/ds-cta-signoff-focus.png",
    "loading": "assetized/ds-cta-signoff-loading.png"
  },
  "final_size": [1044, 92],
  "frame_size": [174, 92],
  "visual_rect": [0, 0, 174, 92],
  "component_rect": [0, 0, 174, 92],
  "content_rects": {
    "label": [20, 22, 134, 40]
  },
  "no_text_rects": {
    "stamp_edge": [0, 0, 36, 64],
    "bottom_pressure": [0, 52, 360, 12]
  },
  "hit_rect": [0, 0, 174, 92],
  "hover_rect": [-6, -6, 186, 104],
  "anchor_points": {
    "tooltip": [180, -8]
  },
  "states": ["default", "hover", "pressed", "disabled", "focus", "loading"],
  "feedback_spec": {
    "pressed_offset": [0, 2],
    "pressed_duration_ms": 90,
    "sound": "stamp_soft"
  },
  "overflow_policy": {
    "label": "trim_ellipsis"
  },
  "qa_cases": ["long_label", "disabled_reason", "pressed_frame", "loading_frame"]
}
```

候选员工卡还必须声明：

```json
{
  "id": "ds_staff_card_atlas",
  "display_modes": ["full_inline", "compact_with_hover_full"],
  "content_rects": {
    "avatar": [18, 18, 56, 56],
    "name": [86, 16, 160, 28],
    "fit_badge": [252, 16, 72, 28],
    "dice_net_full": [86, 52, 232, 70],
    "dice_summary": [86, 52, 232, 30],
    "hover_full_dice_net": [18, 124, 306, 96]
  },
  "no_text_rects": {
    "clip": [0, 0, 22, 110],
    "halftone_corner": [286, 72, 58, 34]
  },
  "hit_rect": [0, 0, 344, 120],
  "hover_rect": [-4, -4, 352, 128],
  "states": ["normal", "hover", "selected", "unavailable", "assigned", "blocked_full"],
  "overflow_policy": {
    "name": "ellipsis",
    "fit_badge": "fixed",
    "dice_net": "prefer_full_inline_then_hover_full"
  }
}
```

已选槽还必须声明：

```json
{
  "id": "ds_selected_slot_atlas",
  "content_rects": {
    "avatar": [14, 12, 48, 48],
    "name": [72, 12, 150, 28],
    "contribution": [72, 42, 190, 24],
    "remove_hint": [254, 16, 54, 34]
  },
  "states": ["empty", "hover", "occupied", "remove-hover", "remove-pressed", "invalid"],
  "qa_cases": ["empty_slot", "occupied_long_name", "remove_hover", "remove_pressed", "invalid_full_team"]
}
```

复核纸还必须声明：

```json
{
  "id": "ds_review_sheet_base",
  "content_rects": {
    "summary": [34, 34, 310, 42],
    "special_constraint": [34, 82, 310, 34],
    "probability": [34, 124, 310, 34],
    "risk": [34, 166, 220, 34],
    "gap": [34, 208, 310, 58],
    "action_scope": [34, 274, 310, 54],
    "failure": [34, 336, 310, 54],
    "blocking_reason": [34, 398, 310, 42],
    "cta_mount": [20, 446, 340, 74]
  },
  "no_text_rects": {
    "red_stamp": [236, 126, 96, 96],
    "paper_clip": [0, 0, 72, 40]
  },
  "states": ["empty", "blocked", "risky_ready", "ready", "confirm_pending", "stamped", "loading"],
  "qa_cases": ["no_staff", "deadline", "chain", "days_insufficient", "confirm_pending", "loading"]
}
```

---

## 9. 生图 / 美术约束

P0 定义必须收紧为“可装配组件”，不是“好看的整屏 PNG”。现有 `dispatch-signoff-desk-v2.png` 可作为氛围母版 / 背景参考，`dispatch-workbench-pixel-v1.png` 更接近早期占位；`dispatch-mission-folder-v1.png`、`dispatch-review-sheet-v1.png`、`dispatch-staff-card-frame-v1.png`、`dispatch-dice-tray-v1.png` 只能算组件方向草稿，不能直接升为生产 P0。

必须：

- 使用深海军蓝工作台、暖白新印刷纸、红 / 青套印、半调、高清微像素颗粒。
- 物件读法是“外勤签批台 / 主编桌 / 记者证 / 任务档案 / 盖章”，不是后台配置页。
- 中央舞台留出干净、近正交、可测量的 1-3 员工槽和候选卡区域。
- 所有动态中文、任务名、姓名、数字、概率、按钮文案由 Godot 渲染。
- 纸张装饰、半调、折角、夹子、红青错位只允许进入 `no_text_rects`。
- 像素颗粒必须是结构化 2-4px 方块、块状半调、红青轻微套印错位和像素边缘，不是摄影噪声或随机纸脏。

禁止：

- 把任务标题、员工姓名、按钮文案、概率、倒计时、假中文烘焙进 PNG。
- 大角度斜透视纸面承载正文或 CTA。
- 用普通矩形面板贴片补救没有安全区的底图。
- 旧报纸、旧档案、泛黄纸噪点、茶渍、羊皮纸、sepia。
- 写实摄影噪声、低清 8-bit 像素、通用网页按钮、SaaS 卡片。
- 暖木桌、台灯、温馨办公室、纯赛博终端、玻璃拟态卡片、假 tooltip、假 pin、假中文 UI。

---

## 10. Godot 接入要求

当前代码状态：

- `WeeklyRunExplorePhase.tscn` 使用 `DispatchDeskArt` 加载 `dispatch-signoff-desk-v2.png` 作为整屏背景。
- `DispatchMissionPanel`、`DispatchDicePoolPanel`、`DispatchReviewPanel` 仍是 `PanelContainer`。
- `_render_dispatch()` 更新任务标题、brief、选中槽、达标率、骰池文本、结果和 CTA。
- `_style_dispatch_slot()` 仍用 `StyleBoxFlat` 绘制槽位。
- `execute_btn` 仍走 `UiStyle.apply_primary_channel_button()`，不是独立签批 CTA atlas。

资产化后应改为：

1. 新增 `dispatch_signoff_asset_manifest.json`。
2. 新增 `WeeklyRunDispatchSignoffAssetManifest.gd`，职责类似 `WeeklyRunRegionTaskAssetManifest.gd`。
3. `WeeklyRunUiStyle.gd` 增加 dispatch signoff assetized 读取入口：
   - `load_dispatch_signoff_texture(asset_id)`
   - `load_dispatch_signoff_atlas_frame(asset_id, frame_id)`
   - `has_dispatch_signoff_assetized_contract()`
   - `has_dispatch_signoff_assetized_runtime_assets()`
4. `DispatchDeskArt` 只保留 `ds_desk_base`，不可再承载功能面板。
5. 左任务档案、中骰池托盘、候选员工卡、右复核纸、主 CTA 改为 manifest 驱动的 Texture / NinePatch / Button 组合。
6. 动态文字只能落在 manifest `content_rects`。
7. 可点击对象使用 manifest `hit_rect` / `hover_rect`；不可用状态必须禁用手型光标。
8. 旧 StyleBoxFlat 只做 fallback，不作为生产路径。

---

## 11. 自动校验

至少新增或扩展测试，检查：

- `DecisionFactMatrix` 中每条事实都有主承载位、引用位、代码字段和至少一个截图 case。
- manifest JSON 有效。
- 所有 P0 `asset_id` 存在。
- 所有必需状态帧存在。
- atlas prompt 的 `target_size`、`frame_size`、`frame_order` 与 manifest 一致。
- `content_rects` 不与 `no_text_rects` 相交。
- `hit_rect` 覆盖视觉主体，不覆盖相邻组件。
- CTA label 只存在于 `ds_cta_signoff_atlas`，复核纸无 `cta_label`。
- 员工卡 `name`、`fit_badge`、`dice_net` 安全区在所有状态帧一致。
- 员工卡在 1920x1080 首屏优先使用 `full_inline` 完整 6 面；如果切到 `compact_with_hover_full`，必须有 hover / 详情完整 6 面截图作为替代证据。
- 复核纸 `blocking_reason` 能容纳“天数不足 / 未选员工 / 潜在点不足 / 人数已满 / 道具不可用”。
- 页面、任务、候选卡、已选槽、签批纸、CTA 的状态枚举与代码枚举一致。
- 满员点击新候选必须进入 `blocked_full` 局部反馈；不得沉默，也不得自动替换。
- `confirm_pending` / pressed / loading / stamped 只影响签批动作反馈，不提前写入结算结果。
- 旧 fallback 可运行，但当 P0 资产缺失时必须输出明确检查失败。

---

## 12. 截图验收

必须覆盖桌面 16:9：

- `1920x1080` 主验收。
- `1600x900` 回归。
- `1366x768` 回归。

状态截图：

1. 未选员工：空槽、候选卡、CTA disabled、阻断原因。
2. 选 1 人：达标率低 / 风险高时，复核纸能说明缺口。
3. 选 2 人：达标率变化可见，候选区位置不跳。
4. 选 3 人：人数满，继续点候选不会自动替换。
5. 天数不足：CTA disabled，按钮不像可点击，复核纸写明剩余天数问题。
6. 潜在点不足：说明缺少可计入相关骰面。
7. 临时线人：雇佣后作为候选员工出现，占员工槽。
8. 道具启用：道具槽与员工槽职责不同，状态不同。
9. hover 候选卡：若首屏已展示完整 dice net，hover 只做轻量预览；若首屏为紧凑摘要，hover / 详情必须展示完整 6 面，不把调试拆解常驻。
10. CTA pressed / confirm_pending：盖章下压、二次盖章或短 hold 状态可见，右侧 `action_scope` 清楚写明不可逆范围。
11. CTA loading / stamped：签批中和已盖章反馈可见，不提前展示完整结算页。
12. 返回区域任务台：返回后保留当前地区和当前任务选中态。

交付截图必须包含整屏和关键 100% 局部裁切：候选员工卡、已选槽、复核纸、CTA、阻断原因。

---

## 13. 落地顺序

1. 本规格确认。
2. `DecisionFactMatrix` 和阻断清单确认，确保每条签批事实都有主承载位。
3. 低保真布局和元素归属表，不生图。
4. P0 manifest 草案与安全区表。
5. prompt bundle：逐项覆盖 P0 资产和 atlas 状态，明确禁止真实文字 / 假按钮 / 假 tooltip。
6. 生成 / 裁切 / 登记资产；本地脚本只做裁切、缩放、透明留白、校验和 overlay。
7. Godot 接入 manifest loader 与 fallback。
8. 截图验收：空队、1 人、2 人、3 人、人数满、天数不足、潜在点不足、道具启用、临时线人、pressed / confirm_pending / disabled / loading / stamped。
9. `ui_designer`、`ux_laoge`、`angus_art_director` 复审后再称为生产候选。

---

## 14. 当前风格稿候选

2026-06-15 已生成首轮派遣签批台整屏风格稿，并补充一张“完成填充态”观感评审图。二者用途不同：`02` 用于资产拆分母版方向，`05` 用于看真实界面完成态；均不得直接作为 Godot 生产底图。

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/01-dispatch-signoff-style-draft-assetized.png` | 第一版结构探索 | 仅参考；存在外圈虚线和较多伪 UI 痕迹 |
| `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/02-dispatch-signoff-style-draft-cleaner-production-mother.png` | 第二版原始输出 | 资产母版候选源图，1672x941 |
| `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/02-dispatch-signoff-style-draft-cleaner-production-mother-1920x1080.png` | 第二版 1920x1080 评审图 | 资产母版候选，有条件通过 |
| `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/05-dispatch-signoff-style-draft-filled-readable.png` | 完成填充态界面预览 | 当前给人评审的主图；用于判断界面观感、信息层级和三栏承载，不用于直接拆图 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v2/01-dispatch-signoff-full-style-v2-artboard-no-runtime-text.png` | 整屏风格稿 v2 无运行时文字底稿 | 二次复审后降级为构图参考 / 偏差案例；不可作为生产标杆或直接切图母版 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v2/02-dispatch-signoff-full-style-v2-filled-preview.png` | 整屏风格稿 v2 填充态预览 | 二次复审用填充态；用于说明功能链和风格问题，不作为下一版视觉目标 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/01-dispatch-signoff-full-style-v3b-artboard-no-runtime-text.png` | v3b 功能分区优先无文字底稿 | 当前拆资产讨论基准候选；纸面更干净、因果链更清楚，但仍需移除假字横条后才可生产 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/02-dispatch-signoff-full-style-v3b-filled-preview.png` | v3b 完整填充态预览 | 用于评审真实界面观感、信息层级和签批因果链 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/03-dispatch-signoff-full-style-v3b-safe-zone-overlay.png` | v3b 安全区 overlay | 用于下一步 P0 manifest 坐标和组件拆分讨论 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/04-dispatch-signoff-component-sheet-v3c.png` | v3c 同屏组件板 | 用于验证拆功能后仍能继承 v3b 风格；不是最终 atlas |

配套文档：

- `docs/plans/dispatch-signoff-imagegen/prompt-bundle.md`
- `docs/plans/dispatch-signoff-imagegen/style-draft-review-2026-06-15.md`
- `docs/plans/dispatch-signoff-imagegen/full-style-v2-review-2026-06-16.md`
- `docs/plans/dispatch-signoff-imagegen/full-style-v3b-review-2026-06-16.md`
- `docs/plans/dispatch-signoff-imagegen/component-sheet-v3c-review-2026-06-16.md`
- `docs/plans/dispatch-signoff-imagegen/cta-atlas-v1-review-2026-06-16.md`
- `tmp/ui-screens/render-dispatch-filled-style.ps1`
- `tmp/ui-screens/render-dispatch-v2-filled-overlay.ps1`
- `tmp/ui-screens/render-dispatch-v3b-filled-overlay.ps1`
- `tmp/ui-screens/render-dispatch-v3b-safe-zone-overlay.ps1`
- `tmp/ui-screens/build-dispatch-cta-atlas.py`

当前候选只能作为风格方向、组件拆分参考、填充态观感评审和 prompt 迭代基准。进入生产前必须补齐 P0 manifest、安全区 overlay、组件裁切、状态 atlas 和 100% 局部截图复审。

2026-06-16 二次复审后新增硬约束：

- v2 构图可留，但整体不能作为生产标杆；下一版必须基于功能分区重新生成无运行时文字底图，不继续润色当前整屏图。
- 纸张必须从偏黄旧档案改为干净象牙白 / 暖白新印刷纸，禁止脏污、破败、撕裂、茶渍、黄褐灰土、旧报纸、羊皮纸和 sepia。
- 质感必须从写实旧物件改为 Angus 像素印刷语言：2-4px 方块颗粒、块状半调、红青套印错位、裁切线、清晰图形边缘和低权重印刷压痕。
- 功能分区优先于生图：顶部全局状态条、左任务简报纸、中派遣配置台、右签批复核纸必须先定义职责、`content_rects`、`no_text_rects` 和主要决策事实。
- Steam 截图读法必须保留“派人 + 投入支援 + 达标率 / 风险 + 消耗 + 签批执行”的因果链，不能变成三组漂亮旧物件并排，也不能清爽化成 SaaS 后台。

2026-06-16 v3b 像素艺术复审结论：v3b 有条件通过为“组件化拆资产方向候选”，不能称为生产标杆。进入 P0 组件化生图前必须清零假字横条，顶部 HUD 改为周刊印刷短条 / 压章 / 信号条，右侧 CTA 从写实 3D 旧机器改为扁平红橙印章压板，纸叠 / 折角 / 金属夹全部退到 `no_text_rects`，并通过 100% 中文局部裁切验收。

---

## 15. P0 manifest 草案与安全区 overlay

2026-06-16 已补首版 P0 manifest 草案与安全区 overlay：

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/dispatch_signoff_asset_manifest.json` | P0 资产、状态、文字安全区、热区、反馈和决策事实契约 | `draft_contract`，JSON 已通过解析；尚未绑定真实生产 PNG |
| `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/06-dispatch-signoff-manifest-safety-overlay.png` | 在完成填充态图上检查 `content_rects / no_text_rects / hit_rect / hover_rect / child_mounts` | 当前 overlay 评审图，可用于发现安全区冲突 |
| `tmp/ui-screens/render-dispatch-manifest-overlay.ps1` | 从 manifest 生成 overlay 的本地复查脚本 | 工具脚本，不是运行时资源 |

本轮 manifest 额外吸收了 UI / UX 复核意见：

- 将 `dispatch_eligibility` 作为一等事实：`can_signoff / block_code / block_reason_text / cta_state` 必须同源驱动。
- 拆分 `time_anchors`：当前剩余天数、行动耗时、签批后剩余天数、截稿剩余天数不得混成同一倒计时。
- 拆分 `staff_pool_availability` 与 `selected_staff_capacity`：顶部是本周员工池，中栏才是本次骰池上限。
- 拆分 `support_item_contract` 与 `temporary_staff_contract`：道具不占人位；临时线人作为候选员工并占员工槽。
- 把绿色 / 红色签批状态章标为非交互对象；真实动作只归 `ds_cta_signoff_atlas`。
- 候选区从一个抽象 grid 改为 6 个显式 `candidate_slot_*` mount，后续截图能逐卡验收。

当前仍有 4 个产品 / 系统待确认项，已写入 manifest `open_questions`：

- 顶部 `可派 3/6` 的正式含义是否为本周可派员工池。
- 红色截稿与深度链是否允许同一任务并存。
- `confirm_pending` 是二次点击确认，还是短暂盖章 hold。
- 临时线人获取入口是否在本页出现，还是只展示已雇佣后的候选卡。

## 16. 首个组件 atlas 候选

2026-06-16 已按 v3c 组件板路线生成第一批组件资产：`ds_cta_signoff_atlas`。

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-cta-signoff-atlas.png` | 签批 CTA 六状态透明 atlas，`1044x92`，每帧 `174x92` | 候选资产，已完成本地回拼验证，待 Godot 状态截图验证 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/07-ds-cta-signoff-atlas-preview.png` | CTA atlas 深蓝底预览 | 用于人工检查状态差异和风格继承 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/07-ds-cta-signoff-atlas-report.json` | 自动分帧报告 | 记录每帧源 bbox、crop 和 atlas 放置 rect |

该资产验证了“拆功能后仍可保持 v3c 风格”的第一步，但不能单独证明整套派遣签批台已可落地。CTA 回拼后暴露出 v3b 右侧复核纸烘焙红色按钮的问题，因此真实生产链路必须先清理 / 重生 `ds_review_sheet_base`，再进入 Godot。

## 17. 右侧复核纸 base 工程候选

2026-06-16 已生成 `ds_review_sheet_base` 的工程验证候选，用于校正裁切、文字槽、`time_cost` 显式事实位和 CTA mount。

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-review-sheet-base.png` | 右侧复核纸 base，`454x860` | 工程验证候选，不是美术最终标杆 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/11-ds-review-sheet-base-preview.png` | 空 base 预览 | 验证无烘焙 CTA / 无真实文字 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/12-ds-review-sheet-base-safe-zone-overlay.png` | 安全区 overlay | 验证 `time_cost / action_scope / blocking_reason / cta_mount` |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/13-ds-review-sheet-recompose-with-cta.png` | 真实装配回拼 | 先清掉旧 v3b 右栏，再挂 base + CTA atlas |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/14-ds-review-sheet-filled-text-fit-test.png` | 中文填字测试 | 验证耗时、不可逆范围和阻断原因不进入 CTA |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-review-sheet-base-v2-art-pass.png` | v2 美术生成候选 | 视觉更自然，但需重新映射 content rect 后才能替换 final path |

结论：

- 旧 manifest 裁切框 `[1368, 166, 454, 790]` 只截到复核纸中右部，导致拆分后仍露出旧烘焙 CTA；已改为 `[1260, 130, 454, 860]`。
- `time_cost` 已从 `action_scope` 中拆出为显式槽，避免后续按 UI / 机制 / 美术分册检索时漏掉耗时事实。
- 该版本底部清理区仍偏程序化，只能用于工程验证；正式美术生产必须重生 / 修图成自然纸面压痕式空挂载区。
- v2 美术生成候选已验证“自然纸面 + 空挂载位”方向可行，但当前 manifest 安全区不能直接套用，下一步应对 v2 重新标定 `content_rects`。

## 18. 已填充完成态预览

2026-06-16 已按用户确认的“图 + 文 + 头像填充”口径制作派遣签批台完成态预览，用真实任务文案、角色头像、候选池、右侧签批字段和 CTA 文案检查界面观感。该产物必须区分两类：

- **本地合成安全区验证**：可用程序把文字 / 头像贴到既有图上，专门暴露 `content_rects`、裁切、字段容量和头像槽问题；不评价最终视觉融合，不得称为“真实效果图”。
- **AI 重绘有字效果稿**：由图像模型把纸面、字体、头像、字段、按钮和状态一起重绘成完整界面，用来判断图文融合与商业截图观感；仍不得作为生产切图母版。

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/19-dispatch-signoff-filled-content-preview-v1.png` | 本地合成整屏验证，包含真实中文、头像、候选卡、已选槽、右侧复核纸和 CTA | 安全区 / 容量验证，不是视觉目标图 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/20-dispatch-signoff-filled-content-preview-v1-right-crop.png` | 本地合成右侧复核纸 100% 裁切 | 检查 `time_cost / action_scope / cta_mount` 容量和裁切 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/19-dispatch-signoff-filled-content-preview-v1-report.json` | 预览来源记录 | 记录 artboard、review sheet、CTA atlas 和头像来源 |
| `tmp/ui-screens/render-dispatch-filled-content-preview.py` | 本地预览合成脚本 | 只用于验证填充态，不进入 runtime |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/21-dispatch-signoff-ai-filled-effect-v1.png` | AI 重绘整屏有字效果稿，图、文、头像、字段和 CTA 融合生成 | 当前视觉目标图 / 评审图，不是生产资产 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/22-dispatch-signoff-ai-filled-effect-v1-left-crop.png` | 左侧任务简报 100% 裁切 | 检查纸面文字是否像印刷字段 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/23-dispatch-signoff-ai-filled-effect-v1-center-crop.png` | 中央派遣池 100% 裁切 | 检查头像、卡片、骰面摘要是否融为一体 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/24-dispatch-signoff-ai-filled-effect-v1-right-crop.png` | 右侧签批复核 100% 裁切 | 检查签批字段、风险、CTA 和纸面融合 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/25-dispatch-signoff-ai-operation-hover-v1.png` | AI 重绘操作态：`本次骰池 2/3`、候选 hover、支援已投入、右侧 delta、CTA ready | 当前操作态目标图 / 评审图，不是生产资产 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/26-dispatch-signoff-ai-blocked-full-v1.png` | AI 重绘阻断态：`本次骰池 3/3`、候选 blocked_full、右侧阻断原因、CTA disabled | 当前阻断态目标图 / 评审图，不是生产资产 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/27-dispatch-signoff-ai-operation-hover-center-crop.png` | 操作态中央派遣池 100% 裁切 | 检查容量、移出、排序、支援和 hover 预览 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/28-dispatch-signoff-ai-operation-hover-right-crop.png` | 操作态右侧复核纸 100% 裁切 | 检查判定句、hover delta、签后本周 / 截稿余量和 CTA ready |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/29-dispatch-signoff-ai-blocked-full-center-crop.png` | 阻断态中央派遣池 100% 裁切 | 检查满员、移出入口和候选就地阻断 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/30-dispatch-signoff-ai-blocked-full-right-crop.png` | 阻断态右侧复核纸 100% 裁切 | 检查阻断原因、处理建议和 CTA disabled |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/31-dispatch-signoff-ai-p0-state-matrix-v1.png` | AI 重绘 P0 状态矩阵：`本次骰池 3/3`、三张已选卡 `移出`、候选就地 `人数已满`、右侧阻断原因、disabled CTA、底部 CTA 六态 | 当前 P0 签批闭环目标图 / 评审图，不是生产资产 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/32-dispatch-signoff-ai-p0-state-matrix-center-crop.png` | P0 状态矩阵中央派遣池 100% 裁切 | 检查容量、移出、支援已投入和候选就地阻断 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/33-dispatch-signoff-ai-p0-state-matrix-right-crop.png` | P0 状态矩阵右侧复核纸 100% 裁切 | 检查阻断原因、处理建议、签批后时间变化和 disabled CTA |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/34-dispatch-signoff-ai-p0-state-matrix-cta-states-crop.png` | P0 CTA 六态 100% 裁切 | 检查 default / hover / pressed / loading / disabled / stamped 的同族差异 |

本地合成验证暴露并修正了两个生产风险：

1. 右侧复核纸若按 1920 位置直接回拼到当前 16:9 缩略画布，会被裁切；当前预览已把 review sheet 放回画布安全区。
2. 左侧失败后果和中心候选池一旦填入真实头像 / dice chip，信息密度明显上升；后续候选卡正式资产必须优先保证头像槽、姓名槽、dice net 或摘要槽有独立安全区，不能只靠空卡外观判断。

AI 重绘效果稿修正了本地合成的主要问题：文字、头像、员工卡和签批字段不再像漂浮贴片，而是进入纸面 / 卡片 / 签批牌的视觉系统。当前 `21` 可作为“真实完成态效果目标图”继续评审，但仍有模型生图常见风险：小字号姓名、候选卡细字和个别中文可能出现近似字，正式落地必须回到无字资产与 Godot 精确渲染。

`ui_designer` 与 `ux_laoge` 复审后，判断单张 ready 图仍会漏掉操作态与阻断态。已补 `25` 与 `26` 两张关键状态效果稿：

- `25` 解决“图好看但看不出怎么选人”的问题：明确 `本次骰池 2/3`、已选卡 `移出`、支援 `已投入 / 不占人位 / 可撤回`、候选排序签、`末日时钟` hover 预览、右侧 `加入末日时钟` 的达标率变化和 `本周 7->5 / 截稿 3->1`。
- `26` 解决“强 CTA 但不知道为什么不能点”的问题：明确 `本次骰池 3/3`、已选三人可移出、候选 `伪人` 就地 `人数已满`、右侧 `不可加入 · 本次骰池已满`、阻断原因、处理建议和灰化 `先调整队伍` CTA。
- `31` 按用户确认的“先做 P0”收束首轮目标：只验证阻断原因矩阵、容量 / 移出、CTA 状态矩阵和图文安全区，不把候选详情、完整 6 面常驻、排序页签、临时线人入口等 P1 / P2 项塞入首轮生产。底部 CTA 六态只是目标读法参考；正式生产仍需要独立 `ds_cta_signoff_atlas`、manifest 状态和 Godot 截图验收。

结论：填充态预览应继续作为派遣签批台的中间验收件，用来验证真实文字、头像和角色骰是否贴合美术组件。但所有真实任务名、员工姓名、头像、dice net、达标率、耗时、阻断原因和 CTA 文案仍由 Godot 动态渲染；不得从 `19`、`20` 或 `21-34` 中切生产组件。

## 19. Godot P0 动态层接入记录

2026-06-17 已按 A74 的 P0 范围把首批签批闭环接入 Godot `weekly_run` 派遣页，目标是先恢复可玩状态矩阵，而不是替换整套美术资源。

| 文件 | 本轮接入 | 状态 |
| --- | --- | --- |
| `gd_project/scenes/gameplay/weekly_run/WeeklyRunGame.gd` | 新增 `DISPATCH_MAX_STAFF`、`dispatch_notice_text`、`dispatch_signoff_state`；生成 `selected_staff_slots`、签批检查清单、满员阻断反馈、loading / stamped 签批态 | 已实现，Godot 截图复验通过 |
| `gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunExplorePhase.gd` | 已选 3 槽从只读 Label 改为可点击移出按钮；右侧复核区读取 `execute_state` 和检查清单；CTA 在 loading / stamped 时保持签批视觉但禁用重复点击 | 已实现，Godot 截图复验通过 |
| `gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunExplorePhase.tscn` | `SelectedSlot1-3` 改为 Button，槽位高度调整为 `58px` | 已实现，Godot 截图复验通过 |
| `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunUiStyle.gd` | 接入 `ds_cta_signoff_atlas` 的 default / hover / pressed / disabled / focus / loading 帧；stamped 临时复用 pressed 盖章读法 | 已实现，Godot 截图复验通过 |
| `gd_project/tests/capture_world_map_dispatch_ui.gd` | 截图脚本新增未选人、天数不足、有效点不足、loading、stamped、回区域任务台等 P0 状态截图 | 已实现，Godot 截图复验通过 |

已覆盖的 P0 行为：

- `本次骰池 0/3 -> 3/3` 明确展示。
- 已选席位直接显示“点击移出”，点击席位可移出该职员。
- 满员后继续点击候选不会自动替换；候选卡就地显示“席位已满 · 点上方席位移出一人”，右侧复核区同步显示阻断反馈。
- 耗时核对改为“本周 N -> 签后 M（耗 X）”，与左侧截稿剩余时间分开。
- 右侧 `DiceText` 改为 `签批检查`：队员席位、耗时核对、需求覆盖、任务状态、主编复核和操作反馈同屏展示，并按阻断 / 注意 / 通过排序，避免 OK 项抢占阻断原因。
- 主 CTA 接入 `idle / loading / stamped` 动态状态，签批后先短暂显示 `签批中...` 与 `已盖章`，再结算回区域任务台。

当前未完成 / 待复验：

- `ds_cta_signoff_atlas` 已替换 Godot 现有 CTA 样式；pressed / stamped 仍复用当前 atlas 帧，后续若生成独立 stamped 帧再替换。
- P1 的支援三态、候选 hover delta、角色详情入口、周内派遣队列提醒尚未进入 runtime。
- 右侧复核仍偏开发期清单；P0 可用，后续资产化复核纸应把阻断 / 警告 / 通过分层，而不是让所有 OK 同权重铺满。

截图复验记录：

- 最初在 Codex 沙箱内运行 Godot 时，Godot 无法写入用户目录下的 `AppData/Roaming/Godot` 与 shader cache，表现为超时 / `signal 11`；提权到沙箱外运行后，最小退出脚本、两个 `--check-only` 脚本检查和 `capture_world_map_dispatch_ui.gd` 均通过。
- 真实截图已刷新到 `docs/screenshots/2026-06-08-world-map-action-log-safe-pass-godot/03-dispatch-desk-chain.png` 与 `docs/screenshots/2026-06-08-world-map-action-log-safe-pass-godot/04-dispatch-desk-deadline.png`。截图中可见 2/3、3/3、席位已满、点击移出、右侧签批检查清单和主 CTA。
- 2026-06-17 续补 P0 阻断矩阵截图：`03-dispatch-no-staff.png` 验证 0/3 未选人；`04-dispatch-days-insufficient.png` 验证剩余天数不足；`04b-dispatch-potential-insufficient.png` 验证有效点不足 / 缺相关骰面。
- 2026-06-17 续补 CTA 连续状态截图：`05-dispatch-cta-loading.png` 验证签批中禁用与防重复提交，`06-dispatch-cta-stamped.png` 验证已盖章反馈，`07-region-return-after-signoff.png` 验证结算后回到区域任务台。

## 20. 2026-06-17 纠偏：逻辑烟测不等于目标界面落地

用户指出本轮 Godot 截图与此前确认的图文填充目标稿差距过大，甚至功能分区也不像同一界面。复核后结论如下：

- `docs/screenshots/2026-06-08-world-map-action-log-safe-pass-godot/*.png` 只能归类为 **逻辑烟测截图**：用于证明 P0 阻断、容量、移出、loading、stamped 和返回区域任务台等状态机可以触发。
- `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/31-dispatch-signoff-ai-p0-state-matrix-v1.png` 及其 `32-34` 局部裁切仍是 **P0 图文融合目标稿**：用于判断“左任务签批文件 / 中本次骰池工作台 / 右签批复核纸 / 底部 CTA 状态矩阵”这套资产化界面读法是否成立。
- Godot P0 接入不再表述为“派遣签批台 UI 已落地”，只能表述为“P0 逻辑状态已跑通，等待按目标稿重建视觉承载页”。

### 20.1 产物标签

| 产物类型 | 当前文件例子 | 可用于验收什么 | 不可用于验收什么 |
| --- | --- | --- | --- |
| 目标效果稿 / filled-state mock | `31-dispatch-signoff-ai-p0-state-matrix-v1.png` | 视觉读法、功能分区、图文融合、P0 状态是否一眼可懂 | 不能切生产资产，不能证明 Godot runtime 已实现 |
| 目标局部裁切 | `32`、`33`、`34` | 中央骰池、右侧复核纸、CTA 六态的 100% 局部读法 | 不能证明整页动线和真实点击 |
| 组件验证稿 | `ds-review-sheet-base-*`、`ds-cta-signoff-atlas-*` | 单组件安全区、状态 atlas、回拼契约 | 不能证明整页 UI 成立 |
| 逻辑烟测截图 | `03-dispatch-no-staff.png`、`04-dispatch-days-insufficient.png`、`04b-dispatch-potential-insufficient.png`、`05-06-07` | P0 状态机、阻断、loading、stamped、返回路径 | 不能作为视觉 / 风格 / 功能分区验收 |
| 承载合同验证 / 运行骨架图 | `2026-06-17-dispatch-signoff-runtime-reframe-godot/*.png` | 目标分区是否能接入真实任务、队员池、已选槽、阻断原因、CTA 和底部回条 | 不能作为美术效果、图文融合、最终布局或商业截图验收 |

### 20.2 下一轮真实落地顺序

1. 以 `31` 为视觉目标锚点，冻结桌面 16:9 分区：左 `任务签批文件`，中 `本次骰池工作台`，右 `签批复核纸`，底部 `CTA 状态矩阵 / 回条`。
2. 先改 Godot 派遣承载页的结构与命名，让 runtime 输出不再读成旧三栏开发面板；此步仍可用现有基础控件，但必须匹配目标分区。
3. 再接入 `ds_task_brief_sheet / ds_staff_card_atlas / ds_selected_slot_atlas / ds_review_sheet_base / ds_cta_signoff_atlas` 等资产化组件。
4. 每次交付截图必须先标注 `目标效果稿 / 组件验证稿 / 运行截图 / 逻辑烟测截图`；只有与目标分区一致的 runtime 图才能称为 UI 落地截图。
5. 验收时必须同时展示：目标效果稿、同状态 runtime 截图、中央骰池局部、右侧复核纸局部、CTA 局部；不能再只展示旧逻辑烟测图。

### 20.3 2026-06-17 运行骨架图的真实用途

用户反馈新一轮 Godot 截图“意义不大、过于抽象”。该反馈成立：这类截图不是资产化 UI 链条里的视觉效果交付，而是位于 `manifest / Godot 动态层` 之间的 **承载合同验证**。

它只应回答以下问题：

- 真实任务文案、耗时、剩余天数、队员池、已选 0/3-3/3、有效点、风险、阻断原因和 CTA 状态是否都有明确挂载位。
- 分区职责是否已从旧地图 / 后台三栏，转向左 `任务签批文件`、中 `本次骰池工作台`、右 `签批复核纸`、底部 `派遣回条`。
- 空态、中间态、满态、禁用、loading、stamped 和返回区域任务台是否能被真实状态驱动。

它不能回答以下问题：

- 是否已经接近 `31` 目标效果稿的美术观感。
- 文字、头像、纸面、按钮和状态章是否已经图文融合。
- 当前截图是否可以作为玩家展示、Steam 截图或最终 UI 观感评审。

因此后续交付顺序调整为：若用户要“看效果”，优先生成 / 展示 `filled-state text mock` 或资产回拼高保真图；若用户要“确认落地风险”，才展示运行骨架图，并必须在图名前和说明里标注 `承载合同验证`。

### 20.4 2026-06-17 高保真图文效果稿 v4

按用户反馈，已停止把运行骨架图作为视觉效果评审材料，改为生成新的派遣签批台高保真图文填充效果稿：

| 文件 | 产物标签 | 用途 | 禁止用途 |
| --- | --- | --- | --- |
| `docs/screenshots/2026-06-17-dispatch-signoff-effect-mock-v4/01-dispatch-signoff-filled-effect-mock-v4.png` | 目标效果稿 / filled-state text mock | 评审派遣签批台四分区、干净象牙纸面、微像素角色头像、图文融合、阻断态和 CTA 状态矩阵是否像最终游戏截图 | 不得切图、不得进入 manifest、不得作为 runtime 底图、不得替代 Godot 动态文字 / 动态头像层 |

本图生成时未使用 OpenRouter 路径：OpenRouter 调用因会上传本地项目参考图到第三方服务而被安全策略拦截。当前 v4 使用内置图像生成工具按文字约束生成，并已归档到本仓库截图目录。后续若要称为生产标杆或资源标杆，仍需再经过 `@像素艺术` 生成后复审；当前只作为效果评审图和下一轮无字组件 prompt / 资产回拼的视觉参考。
