# 发刊编辑正式视觉包装候选 v2 交付清单

## 结论

本轮已交付 `formal_visual_packaging_candidate_v2`。用户确认的报道图片两规格参数已落实到独立 HTML 候选，默认定向、真实换稿重算、确认送印和 12 条候选容量回归均通过。当前仍不是 Godot 生产界面，正式方形母图资产也尚未重制。

## 交付物

- 可运行页面：`docs/prototypes/weekly-editorial-formal-visual-packaging-v2/index.html`
- 视觉样式：`docs/prototypes/weekly-editorial-formal-visual-packaging-v2/visual.css`
- 视觉增强脚本：`docs/prototypes/weekly-editorial-formal-visual-packaging-v2/visual.js`
- 使用与边界说明：`docs/prototypes/weekly-editorial-formal-visual-packaging-v2/README.md`
- 主状态：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v2/01-targeting-default.png`
- 真实换稿后重算：同目录 `02-recalculating-after-replace.png`
- 确认送印：同目录 `03-confirmation.png`
- 换稿动态：同目录 `04-replace-to-recalculating.webp`
- 机器审计：同目录 `audit.json`

## 已落实的图片合同

- 方形母图生产目标：`1024×1024`。
- 候选缩略图：`64×64`。
- 普通版位：`189×189`。
- 副头版：`210×210` 方图 + `12px` 间隔 + `188×210` 文字栏；没有摘要字段时保留留白。
- 主头版：`15:8 / 1920×1024` 源，运行图片窗 `410×219`；方形核心左右各扩展 `448px`。

## 验证结果

- `1920×1080` 下两张 `490×800` 周刊在默认、重算、确认三态始终完整可见。
- 默认定向：候选 8、选中 1、合法目标 6、悬停目标 1、局部换稿按钮 1、主 CTA 1 且禁用。
- 真实点击换稿后：选中、合法目标、悬停目标、局部按钮均为 0；重算条为 1；主 CTA 继续禁用。
- 确认态：中央冻结，双页完整，唯一 CTA 改为“确认送印”，返回修改为 1。
- 12 条候选：左栏 viewport `820 / 1220` 可滚动；document 高度仍为 `1080 / 1080`，中右栏几何不变。
- 动态证据：`1920×1080` animated WebP；7 张真实浏览器源帧经编码后解码为 5 帧。
- 新鲜验收页控制台错误 / 警告：0。

## 资产与实现边界

A01–A06 仍使用现有旧规格报道图，只用于验证图片窗、裁切压力与版面秩序。它们不证明 `1024×1024 → 1920×1024` 正式生产管线已经执行；不得将当前居中裁切输出升格为生产资产。

本轮没有修改 Godot、`candidate_card`、`signoff_panel`、GDD、正式报道图文件或硬阻断规则。GDD 中“不完整版面是严重风险还是硬阻断”的歧义仍待单独裁决。

## 下一 Gate

等待用户审阅 v2 的三类版面视觉关系。若冻结，应先决定是否重制 A01–A06 方形母图并补 A07–A13，再单独进入组件合同与 Godot 接入；上述后续均不由本次确认自动授权。
