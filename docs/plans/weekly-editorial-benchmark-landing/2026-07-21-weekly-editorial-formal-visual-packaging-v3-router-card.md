# 发刊编辑正式视觉包装候选 v3｜Router Card

## 本轮任务

修复正式视觉包装候选 v2 中副头版方图造成的版位空心化：让副头版与主头版共同消费同源 `15:8` 横图，同时保留主副视觉等级。

## 工作流

- 级别：`risky visible UI / corrective visual packaging candidate`
- 顺序：`UX 复诊 → UI Designer 精确排布 → 父级合并 → v3 HTML 落地 → 1920×1080 三态 / 容量 / 文案压力 / 动态验收`
- UX：v2 `FAIL`；横图方向 `PASS WITH CHANGES`，P0 为 0。
- UI：撤回 v2 方图方案，唯一推荐副头版 `375×200`，不采用 `410×219`。
- 父级合并：采纳 `375×200`，无意见冲突。

## 冻结边界

- 不修改 Godot、正式组件合同、GDD 或正式报道图文件。
- 不改变三栏、双页、候选容量、筛选排序、定向换稿、重算、签发与唯一 CTA。
- 不新增摘要或伪数据填充副头版。
- 不把 A01–A06 旧素材的横向裁切称为正式扩图资产。

## 输出与证据

- 原型：`docs/prototypes/weekly-editorial-formal-visual-packaging-v3/`
- 截图与动态：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v3/`
- 机器审计：同目录 `audit.json`
- 纠偏记录：`2026-07-21-weekly-editorial-secondary-head-landscape-loop-log.md`

## 放行条件

- 用户确认副头版 `375×200` 横图的占用率与主副层级。
- 用户确认标题 / meta 置于横图下方。
- 用户确认局部换稿按钮位于右扩展翼，不影响主体判断。
- 通过后仍需另行授权正式资产、组件合同与 Godot 接入。
