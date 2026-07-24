# 发刊报道图片两规格合同审阅板 v1｜Router Card

## 本轮任务

把用户已采纳的“方形母图 + 主头版扩图”原则转成可直接审阅的黑白结构板，解决副头版与普通版位仍使用非方形图片框的问题。

## 工作流

- 级别：`risky visual / structure contract candidate`
- 顺序：`UX 诊断 → UI 设计 → 父级合并 → 1920×1080 浏览器截图与机器审计`
- 产物类型：`structure_wireframe + safe_zone_capacity_validation`
- 当前 Gate：等待用户裁决精确比例与副头版方图尺寸。

## 冻结边界

- 不修改桌面 `1920×1080`、`320 / 1040 / 360` 三栏、双页常显、8 卡容量、12 卡左栏滚动、定向替换、重算、签发与唯一 CTA。
- 不修改 Godot、组件合同、GDD、正式报道图文件或现有视觉包装候选 v1。
- 本轮不把黑白结构板称为最终 UI。

## 输入真值

- `docs/prototypes/weekly-editorial-formal-visual-packaging-v1/`
- `docs/prototypes/weekly-editorial-formal-black-structure-v4/`
- `docs/design-decisions/ui-ux-decisions.md` 的报道图片两规格采纳条目
- 用户截图 `codex-clipboard-485319e2-778b-4e4c-bbf2-da5d21d2e2da.png`

## 输出

- 结构板：`docs/prototypes/weekly-editorial-two-spec-image-contract-review-v1/index.html`
- 截图：`docs/screenshots/2026-07-21-weekly-editorial-two-spec-image-contract-review-v1/01-two-spec-contract-overview.png`
- 审计：同目录 `audit.json`

## 放行条件

- 用户确认或调整主头版 `15:8`。
- 用户确认或调整副头版 `210×210` 方图。
- 用户确认无摘要字段时保留留白，不为版面虚构字段。
