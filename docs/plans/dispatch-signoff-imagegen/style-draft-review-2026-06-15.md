# 派遣签批台风格稿复审

> 日期：2026-06-15
> 对象：`02-dispatch-signoff-style-draft-cleaner-production-mother-1920x1080.png`、`05-dispatch-signoff-style-draft-filled-readable.png`
> 状态：`02` 有条件通过，作为资产母版方向候选；`05` 作为完成填充态观感评审图。二者均不得直接作为 Godot 生产底图接入。

## 结论

第二版比第一版更适合作为资产化 UI 生产母稿。它满足三项关键要求：

- 第一眼读作“主编外勤签批台”，而不是后台面板。
- 左任务档案、中骰池托盘、右复核纸、CTA 盖章区、员工卡和已选槽都有清楚边界，后续可以拆为 `ds_*` 资产族。
- 没有真实任务名、按钮文案、概率、倒计时或可读假中文；大部分动态信息区保持为空白矩形。

补充的 `05-dispatch-signoff-style-draft-filled-readable.png` 不是拆图母版，而是为解决“空母稿不容易看懂最终界面”而生成的完成态风格稿。它采用同一条三栏链路：左侧任务档案、中间本次骰池与候选员卡、右侧签批复核与主 CTA，并填入红色截稿任务、三名已选队员、道具支援、达标率、风险与签批后果。

`05` 的使用边界：

- 可作为：评审整屏观感、信息层级、默认填充密度、右侧复核事实承载、员工卡是否需要完整 dice net 的参考。
- 不可作为：最终 UI 截图、组件 atlas、可直接裁切的生产母版。后续正式资产仍应回到 `content_rects / no_text_rects / hit_rect / states / feedback_spec` 链路。
- 需要继承：标题与主要数值清晰、CTA 像签批动作、三栏各自承担不同决策事实。
- 需要继续避免：旧报纸泛黄化、SaaS KPI 卡片化、把生产说明文字放进游戏画面、候选区过度拥挤。

当前不能称为生产标杆，原因：

- 纸面仍略偏旧化，后续进入组件生产前应校正为更干净的新鲜暖白印刷纸。
- 右侧复核纸的 `action_scope / blocking_reason / failure` 虽有槽位，但视觉权重仍需在低保真和 manifest 阶段重新确认。
- 中央候选卡区域右侧有较大深色空区，需要明确用途：候选滚动区、hover 完整 dice net、详情区，或更多候选位。不能在实现时变成无意义空洞。
- 画面是整屏母稿，不包含 hover / selected / disabled / pressed / loading 等状态帧；后续不能直接切整图接入。

## 推荐拆图方向

优先拆出：

| asset_id | 来源区域 | 用途 |
| --- | --- | --- |
| `ds_desk_base` | 全屏深海军蓝工作台，不含功能纸面 | 场景底图 |
| `ds_top_channel_strip` | 顶部横条 | 低权重周状态 / 世界状态徽记底材 |
| `ds_task_brief_sheet` | 左侧大纸面 | 任务档案纸，需另标 `content_rects / no_text_rects` |
| `ds_dice_tray_base` | 中央上下托盘 | 本次骰池主物件 |
| `ds_selected_slot_atlas` | 中央上方 3 张竖卡 | 已选员工槽状态族 |
| `ds_support_slot_atlas` | 中央上方青色窄卡 | 支援 / 道具槽 |
| `ds_staff_card_atlas` | 中央下方 6 张候选卡 | 候选员工卡状态族 |
| `ds_review_sheet_base` | 右侧复核纸 | 签批复核字段底材 |
| `ds_cta_signoff_atlas` | 右下红色盖章按钮物件 | 主 CTA 状态族 |
| `ds_risk_stamp_atlas` / `ds_approval_stamp_atlas` | 右下印章、纸面章位 | 风险 / 盖章反馈 |

## 后续验收要求

进入下一步前必须补：

- `content_rects / no_text_rects / hit_rect / hover_rect / states / feedback_spec` 草案。
- 100% 局部裁切：任务纸、已选槽、候选员工卡、复核纸、CTA。
- 美术复审：重点检查是否滑向旧档案 / 旧报纸 / 泛黄纸噪点。
- UX 复审：重点检查 `action_scope`、`blocking_reason`、达标率、dice net 是否有主承载位。

## 资产化状态

- 可作为：风格方向候选、组件拆分参考、prompt 迭代基准。
- 不可作为：生产标杆、最终 UI 底图、可直接接入 Godot 的 P0 资源。
