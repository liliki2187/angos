# 发刊编辑正式视觉包装候选 v4 交付清单

## 结论

v4 只增强主头版标题层级。主标题由接近副头版的 `19px` 改为真实字宽驱动的 `28px` 单行或 `24px` 双行，字重 `800`；副头版继续 `18px`。主图、meta、双页与三栏均未移动。

## 交付物

- 可运行页面：`docs/prototypes/weekly-editorial-formal-visual-packaging-v4/index.html`
- 视觉样式：`docs/prototypes/weekly-editorial-formal-visual-packaging-v4/visual.css`
- 使用与边界说明：`docs/prototypes/weekly-editorial-formal-visual-packaging-v4/README.md`
- 主状态：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v4/01-main-headline-hierarchy.png`
- 最长标题压力：同目录 `02-longest-headline-pressure.png`
- 主头版审阅裁切：同目录 `03-main-headline-detail.png`
- 机器审计：同目录 `audit.json`

## 验证结果

- A01 使用 `24px / 26px / 800` 双行档，实际无溢出。
- 最长 A12 使用同一双行档，`410×54` 标题盒的 `clientHeight / scrollHeight` 均为 `54`，无容量失败。
- 标题盒与主图保留 `7px` 间隔；主图起点、尺寸和 meta 均未改变。
- 新鲜页面控制台错误与警告为 0。

## 边界

本轮没有修改 Godot、正式组件合同、GDD、副头版冻结结构或正式报道图。v4 仍是正式视觉包装候选，不是生产界面。

## 用户确认

2026-07-21 用户查看完整三栏双版截图后确认标题大小，主头版标题层级已冻结。

## 下一 Gate

下一轮应单独审阅中栏顶部操作条的信息层级；该局部通过后，再进入正式报道图片资产补齐。不自动授权 Godot 或合同升版。
