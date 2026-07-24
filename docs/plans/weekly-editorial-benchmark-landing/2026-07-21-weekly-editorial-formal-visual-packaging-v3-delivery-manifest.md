# 发刊编辑正式视觉包装候选 v3 交付清单

## 结论

本轮已交付 `formal_visual_packaging_candidate_v3`。v2 的副头版方图＋右文字栏已撤回，副头版改为 `375×200` 的同源 `15:8` 横图；主头版继续为 `410×219`。两者共用 `headliner_landscape` 资产规格，候选与普通位继续使用 `square`，因此报道图片体系仍只有两种规格。

## 交付物

- 可运行页面：`docs/prototypes/weekly-editorial-formal-visual-packaging-v3/index.html`
- 视觉样式：`docs/prototypes/weekly-editorial-formal-visual-packaging-v3/visual.css`
- 视觉增强脚本：`docs/prototypes/weekly-editorial-formal-visual-packaging-v3/visual.js`
- 使用与边界说明：`docs/prototypes/weekly-editorial-formal-visual-packaging-v3/README.md`
- 主状态：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v3/01-targeting-secondary-landscape.png`
- 真实换稿后重算：同目录 `02-recalculating-after-replace.png`
- 确认送印：同目录 `03-confirmation.png`
- 换稿动态：同目录 `04-secondary-replace-to-recalculating.webp`
- 机器审计：同目录 `audit.json`
- 纠偏 Loop Log：`2026-07-21-weekly-editorial-secondary-head-landscape-loop-log.md`

## 副头版最终候选几何

- 外槽：`442×342`，不变。
- 横图：`[33,14,375,200]`。
- 角色 / ID：`[15,226,72,14]` / `[95,226,48,14]`。
- 标题：`[15,248,411,48]`，最多两行。
- meta：`[15,306,411,18]`，强制单行。
- 换稿按钮：`[354,160,44,44]`，只位于右扩展翼 action-safe zone。
- 主头版横图仍为 `410×219`；副头版图片面积约为主头版的 `83.5%`。

## 验证结果

- `1920×1080` 下两张 `490×800` 周刊在默认、重算、确认三态均完整可见。
- 默认定向：来源 1、合法目标 6、悬停目标 1、局部换稿按钮 1。
- 主、副头版的 `data-image-format` 均为 `headliner_landscape_15_8`；普通位均为 `square`。
- A12 最长标题压力：`411×48` 标题槽的 `clientHeight / scrollHeight` 均为 48，meta 保持单行。
- 真实点击换稿后：A04 进入副头版，选中 / 合法 / 悬停 / 局部按钮全部归零，进入重算，送印禁用。
- 确认态：双页冻结，唯一 CTA 改为“确认送印”，保留返回修改。
- 12 条候选：左栏 viewport `820 / 1220` 可滚动，document 仍为 `1080 / 1080`，中右栏不移动。
- 清空双版：项目内确认通过；所有版位清空后右栏安全显示“尚未设置头版”，不再读取空对象标题。
- 动态证据：`1920×1080`、7 帧 animated WebP。
- 新鲜验收页控制台错误 / 警告：0。

## 资产与实现边界

A01–A06 仍是旧规格报道图，只用于布局与裁切压力预览。正式生产必须由 `1024×1024` 方形母图生成 `1920×1024` 同源横图，主、副头版读取同一横图文件；不得把当前 CSS `cover` 结果当作生产扩图。

本轮没有修改 Godot、`secondary_head_slot`、其他组件合同、GDD、正式报道图文件或硬阻断规则。若未来进入 Godot，必须先升 `secondary_head_slot` 合同并重跑整屏回填验证。

## 下一 Gate

等待用户审阅 v3。若冻结，再单独裁决正式方形母图 / 横图重制、A07–A13 补齐、组件合同与 Godot 接入；以上后续不由本次确认自动授权。
