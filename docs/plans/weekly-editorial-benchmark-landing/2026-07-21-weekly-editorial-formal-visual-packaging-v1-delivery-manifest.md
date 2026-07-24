# 发刊编辑正式视觉包装候选 v1 交付清单

## 结论

本轮交付 `formal_visual_packaging_candidate_v1`。v4 功能结构保持冻结，正式视觉包装方向已形成可审阅候选；UI 方案通过，UX 结论为 `PASS WITH CHANGES` 且 P0 为 0，能在本轮直接修复的 P1 已消费。当前仍不是 Godot 生产界面。

## 交付物

- 可运行页面：`docs/prototypes/weekly-editorial-formal-visual-packaging-v1/index.html`
- 视觉样式：`docs/prototypes/weekly-editorial-formal-visual-packaging-v1/visual.css`
- 使用与边界说明：`docs/prototypes/weekly-editorial-formal-visual-packaging-v1/README.md`
- 审阅总览：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v1/00-review-contact-sheet.png`
- 主状态：`01-targeting-default.png`
- 类型筛选：`02-filter-menu.png`
- 排序：`03-sort-menu.png`
- 真实换稿后重算：`04-recalculating-after-replace.png`
- 确认送印：`05-confirmation.png`
- 筛选/排序动态：`06-filter-sort-interaction.webp`
- 机器审计：`audit.json`
- 证据纠偏记录：`2026-07-21-weekly-editorial-formal-visual-packaging-v1-evidence-loop-log.md`

## 本轮证明范围

- 固定 `320 / 1040 / 360` 三栏和两张 `490×800` 周刊继续成立。
- 8 张候选卡在 1080p 内完整可见；筛选/排序不推动中栏和右栏。
- 无名称搜索；类型筛选可多选；排序支持等级和获得时间两个维度、四个方向。
- 排序菜单关闭后仍有 `高 / 低 / 新 / 旧` 状态角标。
- 候选元信息明确显示类型、等级与“基值”。
- 6 个合法目标使用非按钮式四角标；只有当前目标出现一枚青绿色“换稿”。
- 真实点击换稿后 A04 上副头版、A03 回候选；临时目标反馈清零，进入重算，CTA 禁用。
- 确认态双页完整冻结，唯一 CTA 改为“确认送印”，并保留明确的次级“返回修改”。
- 清空双版使用项目内确认层，不再调用浏览器原生确认框作为最终呈现。
- 锈红从报道类型和顶部装饰退出，只保留风险/破坏性确认与主行动语义。

## UX 必须修消费

- P1-1：已增加排序持续状态，候选元信息升至 11px 并标注“基值”。
- P1-2：已增加中央选稿提示与六目标四角定位线；仍只有一枚局部按钮。
- P1-3：已强化“返回修改”，并新增项目内清空确认层。
- P1-4：A07–A13 继续 `NEEDS_NEW_ASSETS`；当前占位缩略图已显式标“占位”，不冒充完成。
- P1-5：爆炸性新闻和顶部装饰改为芥末黄/橄榄体系，锈红语义收敛。

## 资产复用与缺口

已复用 A01–A06 六张正式报道图。A07–A13 尚缺七张语义报道图，同时全部报道图仍需建立大图、窄版位和 64px 缩略图的 `focus_point / crop_safe_rect`。

## 不能声称

- 不能称为最终 UI 或 Godot 已落地。
- 不能称 A07–A13 已完成正式美术。
- 不能据此提前升 `candidate_card` 或 `signoff_panel` 组件合同。
- 不能把当前“空位即硬阻断”写入 GDD；真源歧义仍待用户裁决。
- 不能声称键盘/手柄完整焦点链已验收。

## 验证

- `1920×1080` 主状态、筛选、排序、重算、确认五态截图完整。
- 主状态：8卡、2页、来源1、合法目标6、悬停目标1、局部按钮1、CTA1、搜索0。
- 换稿链：真实点击通过；A04/A03 交易事实与右栏一致。
- 确认链：从 ready 真实点击进入；双页2/2冻结、确认 CTA1、返回修改1、局部换稿0。
- 动态证据：`960×540`、6帧 animated WebP。
- 浏览器捕获时错误 / 警告：0。

## 下一 Gate

等待用户审核本轮正式视觉包装候选。若视觉方向冻结，下一轮应先补 A07–A13 报道资产与裁切合同，再决定是否升组件合同并进入 Godot；GDD 硬阻断歧义仍需单独裁决。
