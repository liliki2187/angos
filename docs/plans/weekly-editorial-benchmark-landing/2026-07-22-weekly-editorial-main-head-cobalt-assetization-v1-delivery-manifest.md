# 发刊编辑主头版钴蓝资产化预演 v1 交付清单

## 结论

主头版 `442×374` 已完成真实生图源、2× 分层资源、Godot 四态拼装和整屏合同坐标回填预览，机器几何审计通过；但 2026-07-22 用户视觉复核否决了该预演，原因是固定图形与文字叠化，且脚本重画的程序线框取代了风格稿的主要美术语言。当前产物降级为失败证据，不代表可继续生产。

## 分层资源

目录：`gd_project/Assets/ui/angus_packaging/weekly_editorial/assetization_preflight/main_head_cobalt_v1/`

- `base-paper.png`：2× 暖纸与深蓝照片凹槽。
- `fixed-decoration.png`：固定钴蓝角标、印务线和小型橄榄 / 芥末标记。
- `state-legal.png`：合法目标透明 overlay。
- `state-hover.png`：唯一悬停透明 overlay。
- `state-focused.png`：聚焦透明 overlay。
- `replace-action-skin.png`：`88×88` 源，运行时 `44×44` 的换稿按钮皮肤。
- `manifest.json`：源图、逻辑尺寸、2×尺寸、内容槽、命中和 alpha 统计。

## 真实拼装证据

- 四态：`docs/screenshots/2026-07-22-weekly-editorial-main-head-cobalt-assetization-v1/01-main-head-idle.png` 至 `04-main-head-focused.png`。
- 拆层与四态审阅板：`05-main-head-assetization-review-board.png`。
- 放回现行整屏合同布局：`06-fullscreen-placement-preview.png`。
- Godot 坐标审计：`audit.json`，`passed: true`。
- 整屏改动范围审计：`fullscreen-placement-audit.json`，合同矩形为 `[459,276,442,374]`，实际改动 bbox 为 `[469,286,891,642]`，未越界。

## 关键结果

- 根节点、报道图、标题、meta 在四态零漂移。
- 眉题区为 `[16,14,190,23]`，主标题区为 `[16,37,410,45]`；两者不重叠并完整落在冻结标题槽 `[16,14,410,68]` 内。
- 普通 / 合法 / 悬停三态不显示换稿按钮；聚焦态只有一个 `44×44` 换稿按钮。
- 斜角、角标和纸面装饰只存在于透明视觉层，视觉层全部忽略鼠标输入。
- 动态标题、报道图、meta 与按钮文字均由 Godot 生成，没有烘焙进美术图。
- 根据 UX 复核修正了两项问题：整屏普通态不叠加局部换稿按钮；纸面层改为半透明局部装饰，避免主头版读作独立白卡。

## 边界

本轮没有修改 `WeeklyRunEditorialPhase.gd`、正式 `weekly_editorial_asset_manifest.json`、组件合同或 GDD。整屏图是位置合成预览，不是正式 Godot 发刊界面截图。`candidate_card 288×92` 扩产已经暂停；下一步需先重做并确认主头版完整 `visual master`，再讨论反向拆层。
