# 派遣签批台 V15/V16 真实内容风格稿生产规格

> 状态：生产规格底稿 / asset contract draft  
> 稿件类型：`contract_overlay` + `no-text asset master draft` + `filled-state capacity preview`  
> 重要边界：V15/V16 本地稿仍不是生产真源，也不是最终真实内容风格稿。它用于冻结结构、文字安全区、点击区和下一轮高保真无字 / 有字稿的生产合同。

## 0. V16 正交纠偏

用户明确指出：功能页面一定要方正，斜的界面资源很不好用。该反馈作为 V16 的一票否决 Gate：

- 承载动态文字、数值、头像状态、按钮文案、hit rect 的功能正面必须为 0 度正交矩形。
- 斜切、外侧标签、纸层阴影、半调、折角、票据舌片可以保留，但只能进入 `no_text_rects` 或背景装饰层。
- 右侧签批票据、中央派遣板、候选抽屉、器材托盘和 CTA plate 都必须可九宫格 / atlas 拆分；不得用梯形、透视、旋转纸面承载正文或主 CTA。
- 如果高保真生图出现“整体好看但可写纸面倾斜”，必须降级为灵感图 / 偏差案例，不进入 `filled-state text mock`、`no-text asset master` 或生产候选。

V16 正交合同稿用于替代 V15 中右侧斜票据的生产约束；V15 仍保留为历史结构容量参考。

## 1. 当前输入

| 类型 | 文件 | 用途 |
| --- | --- | --- |
| filled-state capacity preview | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v15-editorial-object/01-dispatch-signoff-editorial-object-v15-default.png` | 检查真实任务名、5 人队伍、1 道具、达标率、消耗和 CTA 信息容量 |
| role-pool hover preview | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v15-editorial-object/02-dispatch-signoff-editorial-object-v15-role-hover.png` | 检查候选员工抽屉 hover 向上展开，不推动右侧签批票据 |
| no-text asset master draft | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v15-editorial-object/03-dispatch-signoff-editorial-object-v15-no-text-base.png` | 检查动态文字被移除后，底图是否仍像派遣签批台 |
| contract overlay | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v15-editorial-object/04-dispatch-signoff-editorial-object-v15-asset-contract-overlay.png` | 标注 `content_rects / no_text_rects / hit_rects` |
| V16 orthogonal preview | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v16-orthogonal-contract/01-dispatch-signoff-editorial-object-v16-orthogonal-default.png` | 检查右侧签批票据、中央功能面、候选抽屉和 CTA 是否全部方正 |
| V16 orthogonal no-text draft | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v16-orthogonal-contract/03-dispatch-signoff-editorial-object-v16-orthogonal-no-text-base.png` | 检查无动态文字时的正交可写区 |
| V16 orthogonal contract overlay | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v16-orthogonal-contract/04-dispatch-signoff-editorial-object-v16-orthogonal-contract-overlay.png` | 绿色标注正交功能承载面，红色标注禁写装饰 |
| V16 right-ticket crop | `docs/screenshots/2026-06-18-dispatch-signoff-packaging-v16-orthogonal-contract/05-dispatch-signoff-editorial-object-v16-right-ticket-crop.png` | 100% 局部检查右侧签批票据是否可拆、可写、可点 |

## 2. 页面职责

派遣签批台只回答一句话：

```text
这 5 名员工 + 这 1 件随队道具，派去当前任务是否够用，签批后会消耗什么？
```

保留四个核心功能区：

| 功能区 | 玩家问题 | 当前 V15 承载物 | 下一轮高保真要求 |
| --- | --- | --- | --- |
| 任务档案 | 我为什么要派人？ | 左侧任务档案 / 摘要纸 | 只解释任务背景和需求，不承担选人 |
| 已选队伍槽 | 当前谁出发？ | 中央签批板上 5 张员工证 + 1 条随队道具 | 员工卡与候选卡同尺寸家族；道具在队伍下方，权重低于员工 |
| 候选 / 器材池 | 我还能换谁 / 带什么？ | 下方员工抽屉 + 底部器材托盘 | 员工池默认一行完整卡，hover 向上展开；器材池默认可见但低权重 |
| 签批复核 | 签下去发生什么？ | 右侧签批票据 + 盖章 CTA | 主结论是达标率和消耗后果，CTA 必须写清 `消耗 2 天` |

## 3. 视觉方向

- 深海军蓝是主场，约 70% 画面面积；不得回到黑灰后台、蓝绿泥色或全屏 CAD 网格。
- 象牙白纸件约 20%，只作为真实工作物件出现；纸面要干净、现代、新鲜印刷，不得脏旧破败。
- 红橙约 7%，只用于异常、签批、CTA、危险和高能印刷点。
- 青色约 3%，只用于信号、追踪和低频信息，不得成为全屏分区描边。
- 拟物只保留有功能职责的物件边缘：签批板、票据、员工证、道具票根、抽屉 / 托盘。夹子、圆孔、铆钉、叠纸、抽屉机械细节必须图形化，不做写实办公用品堆叠。
- 像素 / 半调必须进入结构：风险区域用红橙半调，信号用青色点阵，纸边用轻套印错位，角色头像按高清微像素 Q 版方向。
- 功能承载面必须方正：可写纸面、卡片内框、右侧票据、CTA 文本槽、候选抽屉和器材托盘都必须水平 / 垂直对齐；斜切只允许在外轮廓或装饰 no-text 层出现。

## 4. 动态字段合同

| 字段组 | 主承载 | 当前示例 | 生产规则 |
| --- | --- | --- | --- |
| 任务标题 | 左侧任务档案纸 | `M330 未班车空白段` | 1 行，最长 12 汉字，不能压纸角 / 裁切线 |
| 任务链状态 | 左侧任务档案纸 | `深度调查 · 当前环 1/4` | 次级色，不得抢任务标题 |
| 已选队伍标题 | 中央签批板顶条 | `已选队伍 5/5` | 主标题，不能烘焙在生产底图 |
| 已选员工卡 | 中央员工证 | 姓名、职能、dice net、移出 | 姓名 / 职能 / 移出由动态层或独立状态层承载 |
| 随队道具 | 中央道具票根 | `匿名热线录音` | 道具名、说明、撤回按钮都在正交安全区 |
| 风险判断 | 中央核验尺 | `达标率 78%` | 达标率最大；`13/8` 只能作为相关点上限 / 目标解释 |
| 签批票据 | 右侧票据 | `可签批 · 达标率 78%` | 只放最终复核摘要，不复读整页细节 |
| CTA | 右侧盖章板 | `盖章派遣 · 2天` | 文案必须含动作和消耗；不同状态拆 atlas；文本槽必须方正 |
| 候选员工 | 员工抽屉卡 | 姓名、适配、dice net、`+` | 默认露出 6 张完整卡；已选员工从候选池移出 |
| 器材托盘 | 底部器材票签 | 道具名、可带 / 耗尽、`+` | 默认可见但低权重，hover / focus 可展开 |

## 5. 资产拆分清单

P0 资产必须先做：

| asset_id | 类型 | 说明 |
| --- | --- | --- |
| `dispatch_desk_backdrop` | base bitmap | 深海军蓝工作台、弱网格、信号半调、背景负空间 |
| `task_dossier_base` | component bitmap | 左侧任务档案纸和摘录区，无动态文字 |
| `dispatch_board_base` | component bitmap | 中央签批板 / 队伍牌桌，无员工文字 |
| `selected_staff_card_frame` | atlas | 已选员工证卡，`default / hover / selected / disabled` |
| `staff_remove_badge` | atlas | 已选员工移出按钮，`default / hover / pressed` |
| `current_item_receipt` | component bitmap | 本次随队道具票根，含撤回按钮挂点 |
| `risk_ruler_base` | component bitmap | 盖章前风险判断 / 需求覆盖底板 |
| `approval_ticket_base` | component bitmap | 右侧签批票据，无动态文字 |
| `approval_cta_plate` | atlas | `default / hover / pressed / loading / disabled / stamped` |
| `candidate_staff_card_frame` | atlas | 候选员工证卡，`default / hover / disabled / full_blocked` |
| `candidate_drawer_base` | component bitmap | 员工抽屉底板，默认一行与 hover 两行态 |
| `equipment_tray_base` | component bitmap | 器材托盘底板 |
| `equipment_ticket` | atlas | 道具票签，`available / hover / selected / exhausted / disabled` |

P1 资产后续再做：

- `approval_stamp_mark`：盖章成功反馈。
- `dispatch_route_signal_layer`：中央路线 / 信号装饰层，可弱动画。
- `drawer_handle_hint`：候选抽屉 hover 提示。
- `tooltip_plate`：角色 / 道具详情短浮层。

## 6. 状态矩阵

| 对象 | 必需状态 | 备注 |
| --- | --- | --- |
| 主 CTA | `default / hover / pressed / loading / disabled / stamped` | 真实界面只显示一个当前状态；状态矩阵只进规格页 |
| 已选员工卡 | `default / hover / remove_hover / removing / disabled` | 上方已选区是权威状态，不缩略 |
| 候选员工卡 | `default / hover / selected-preview / full_blocked / disabled` | 满员只在候选卡局部阻断，不让全局签批不可用 |
| 员工抽屉 | `default_one_row / hover_two_rows` | hover 向上展开，不推动右侧票据 |
| 本次道具槽 | `empty / occupied / hover / revoke_hover / disabled` | 道具不占员工位，只能 0-1 个 |
| 器材托盘 | `default_compact / hover_expanded` | 默认比员工池低权重 |
| 签批票据 | `valid / invalid / warning / stamped` | 只承载最终复核摘要 |

## 7. 高保真生成 brief

下一轮生成 / 精修必须产出两张图：

1. `no-text asset master`：无动态文字、无真实姓名、无动态数值，但保留物件、卡槽、票据、按钮底板、头像占位和安全区。
2. `filled-state text mock`：使用 `M330 未班车空白段`、5 名员工头像 / 姓名、`匿名热线录音`、`达标率 78%`、`盖章派遣 · 2天` 等真实内容，检查图文融合与截图感。

正向关键词：

```text
modern midnight editorial dispatch approval desk, Angus supernatural weekly magazine, deep-sea navy dominant field, clean ivory printed paper, vivid red-orange approval stamp, restrained cyan signal accents, high-definition micro-pixel character portraits, structured halftone dots, crop marks, red-cyan print misregistration, graphicized physical objects, central dispatch board, compact right approval receipt, square-on axis-aligned writable document faces, orthogonal functional panels, candidate employee badge drawer, equipment requisition tray, polished in-game UI screenshot
```

负向关键词：

```text
old archive, yellowed dirty paper, torn parchment, coffee stains, warm wood desk, nostalgic office, Sultan palace ornament, ornate gold filigree, SaaS dashboard, generic admin panel, programmer wireframe, simple PIL rectangles, CAD grid, full-screen cyan outlines, tilted writable documents, skewed UI panels, perspective paper carrying body text or CTA, overly literal office props, excessive clips, rivets, binder holes, stacked paper mechanics, default UI labels pasted on art
```

## 8. 通过标准

- 缩小图第一眼读成 Angus 派遣签批工作台，不是后台表单、旧办公室或卡牌管理器。
- 四个核心功能区都能在无说明下读出。
- `达标率 78%` 是风险判断主结论，`13/8` 不再被读成确定通关。
- CTA 明确表达 `盖章派遣` 与 `消耗 2 天`，不需要玩家从字段里拼后果。
- 无字底图里没有动态文字、任务名、数值、员工姓名和按钮文案烘焙。
- 有字效果图的文字、头像和按钮像同一轮美术系统，不像贴在底图上的 Label。
- `content_rects` 不压装饰、纸边、半调、章、头像和裁切线。
- 所有承载动态内容的功能面均为正交矩形；斜边、透视和折角不得进入正文、数值、头像状态或 CTA label。
- `hit_rects` 与可点击物件一致，不靠隐藏大热区。
- 通过后必须再交 `@像素艺术` 生成后复审；复审通过前只能叫目标稿 / 合同稿，不能叫生产真源。

## 9. 当前阻塞

如果要用用户参考图或本地 V15 图作为外部生图输入，会上传本地参考图 / 项目截图到外部服务。需要用户明确同意后才能执行。未获同意前，只能继续本地规格、无字底图草稿和合同图推进。
