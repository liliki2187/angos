# 发刊编辑正式视觉包装候选 v2｜Router Card

## 本轮任务

把用户已确认的报道图片两规格精确参数落实到正式视觉包装候选：除主头版外全部使用方形图片窗，主头版使用由方形母图左右扩展得到的 `15:8` 横图。

## 工作流

- 级别：`risky visible UI / formal visual packaging candidate`
- 复用已完成链路：`UX 诊断 → UI 设计 → 父级合并`
- 本轮执行：`用户参数冻结 → v2 独立 HTML 落地 → 1920×1080 浏览器回归 → 截图 / 动态 / 机器审计`
- 当前 Gate：候选 v2 已通过本地验收，等待用户审阅视觉排布。

## 冻结边界

- 不修改 Godot、组件合同、GDD 或正式报道图文件。
- 不改变 v4 已冻结的三栏、双页、筛选排序、定向换稿、重算、签发与唯一 CTA。
- 不把当前 A01–A06 旧素材的居中裁切称为正式方形母图生产完成。
- 不把 HTML 候选称为最终 UI 或 Godot 生产证据。

## 输入真值

- `weekly-editorial-formal-black-structure-v4`
- `weekly-editorial-formal-visual-packaging-v1`
- `weekly-editorial-two-spec-image-contract-review-v1`
- 设计采纳记录 A271 的 2026-07-21 精确参数修订

## 输出与证据

- 原型：`docs/prototypes/weekly-editorial-formal-visual-packaging-v2/`
- 截图与动态：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v2/`
- 机器审计：同目录 `audit.json`

## 放行条件

- 主头版、次版与普通版位的图片框体关系得到用户视觉确认。
- 用户确认次版右侧留白策略与普通位标题 / 图片 / meta 的纵向秩序。
- 通过后再单独裁决正式方形母图重制、组件合同与 Godot 接入，不自动联动。
