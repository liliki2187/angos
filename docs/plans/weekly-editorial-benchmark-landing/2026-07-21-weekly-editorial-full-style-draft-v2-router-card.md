# 发刊编辑完整风格稿 v2｜Router Card

## 本轮任务

以发刊编辑 v6 的功能、规格和完整三栏布局为不可改动几何真值，把两张 clean low-poly weekly 标杆的风格和元素转译成一张完整 `1920×1080` 风格稿。

## 输入真值

- 布局与状态：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v6/01-targeting-guidance-plain-text.png`
- 美术标杆：`design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`、`benchmark-board-02.png`
- 风格规范：`design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`
- 纸张合同：`design/art-direction/clean-lowpoly-weekly-paper-material-contract.md`

## 工作流

- 级别：`visible UI art / full-screen style draft`
- 顺序：`真值读取 → UX 结构锁定 → UI 风格转译 → 内置 image_gen 首稿 → 生成后复审 → 几何定向修正 v2 → UI / UX 复审 → 父级合并`
- clean low-poly weekly 临时例外生效：不自动调用旧像素 / 半调坐标系的 `angus_art_director`，由两张原始标杆、支线规范、纸张合同、UI / UX 和父级直接对照放行。

## 硬边界

- 保持 `1920×1080`、`320 / 1040 / 360` 三栏、20px 栏间距、8 张候选、完整双页与六槽。
- 保持来源1、合法目标6、悬停1、局部换稿1、右栏连续证据链、硬阻断和唯一禁用 CTA。
- 不修改 Godot、正式组件合同、GDD 或正式报道资产。

## 输出

- 用户审阅稿：`image_gen/2026-07-21/20260721-174656_weekly-editorial-style-draft-v2.png`
- 元数据：同名 `.json`
- 首稿偏差证据：`image_gen/2026-07-21/20260721-173903_weekly-editorial-style-draft-v1.png`

## 放行条件

- 用户只裁决整屏美术方向是否成立；生成式小字不作为正式文字层验收。
- 用户确认前不拆件、不做状态 atlas、不接入 Godot。
