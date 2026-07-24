# 发刊编辑正式视觉包装候选 v1

## 产物定位

这是基于已冻结 `formal_ui_structure_wireframe_v4` 制作的桌面 `1920×1080` 有字视觉包装候选，产物类型为：

`filled_state_text_mock / formal_visual_packaging_candidate`

它用于审核视觉层级、材质语言、候选筛选/排序反馈、定向换稿、重算阻断和确认送印状态。它不是 Godot 正式界面，也不是已经完成资产合同与裁切安全区的生产候选。

## 已冻结并继承的结构

- 固定三栏：左 `320`、中 `1040`、右 `360`。
- 中央两张 `490×800` 周刊始终同时完整可见。
- 左栏 8 张 `288×92` 候选卡在 1080p 内完整可见；12 张时只滚动左栏。
- 不提供名称搜索；只保留报道类型筛选与等级/获得时间排序。
- 定向替换仍是“先选来源，再选择合法目标”；只有当前目标出现一枚局部“换稿”。
- 换稿后旧结果立即失效，进入重算并禁用送印。
- 右栏上部滚动证据链，下部固定阻断与唯一主 CTA。
- 确认送印时双页完整冻结，并保留“返回修改”。

## 本轮视觉包装

- 深海军蓝连续工作台作为外围负空间。
- 中央双版使用同纸暖灰材质，并复用 A01–A06 六张已存在的低多边形报道图。
- 锈红只保留给风险板与主行动；报道类型和顶部装饰不再借用锈红。
- 报道类型筛选为多选，排序支持等级高低与获得时间新旧。
- 排序按钮持续显示 `高 / 低 / 新 / 旧` 的当前状态角标。
- 候选卡元信息提升到 11px，并明确第三项为“基值”。
- 全部合法目标使用非按钮式四角定位线；当前目标才显示青绿色双框和局部按钮。
- “返回修改”升级为青灰描边次按钮。
- “清空双版”改为项目内确认层，不再依赖浏览器原生确认框。

## 资产边界

- A01–A06：复用现有正式报道图。
- A07–A13：当前只有确定性占位色块，并在缩略图内明确标记“占位”。这些图属于 `NEEDS_NEW_ASSETS`，不得称为正式报道图。
- 所有正式报道图仍需补 `focus_point / crop_safe_rect`，分别覆盖大图、窄版位与 64px 缩略图。
- 本轮没有修改 Godot 资源、组件合同、GDD 规则或设计采纳之外的正式真源。

## 预览参数

直接打开 `index.html` 即为定向换稿主状态。包装页会把查询参数继续传给 v4 结构宿主。

- `?candidateMenu=filter&filter=r2,r4`：打开类型筛选并选中深度/爆炸性新闻。
- `?candidateMenu=sort&sort=quality_desc`：打开排序并选中等级高到低。
- `?candidateCount=12`：12 张候选，仅左栏滚动。
- `?state=recalculating`：重算状态预览。真实换稿证据以截图 `04-recalculating-after-replace.png` 为准。
- `?state=ready`：结果有效、可进入确认。
- `?state=confirmation`：确认送印与双页冻结预览。

## 审阅证据

- 总览板：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v1/00-review-contact-sheet.png`
- 主状态：`01-targeting-default.png`
- 筛选：`02-filter-menu.png`
- 排序：`03-sort-menu.png`
- 真实换稿重算：`04-recalculating-after-replace.png`
- 确认送印：`05-confirmation.png`
- 动态：`06-filter-sort-interaction.webp`
- 自动审计：`audit.json`

## 尚未冻结

- A07–A13 正式报道图与全部裁切安全区。
- 键盘/手柄焦点图和非 hover 替换路径。
- “版面不完整是严重风险还是硬阻断”的 GDD 口径。
- Godot 落地与 `candidate_card / signoff_panel` 合同升版。
