---
name: ux-diagnosis
description: Use when the user invokes @UX老哥, @ux老哥, @UX诊断, @ux诊断, @cowork-ux-diagnosis, asks for a game UI/UX hard-problem diagnosis, asks to analyze a screenshot together with Angus system/gameplay functions, or requests P0/P1/P2 interaction diagnosis.
---

# UX 老哥诊断

这是 Angus / 《世界未解之谜周刊》的 Codex 版 `@UX老哥` 入口。完整工作流真源是新版 portable 包的核心 spec：

- `./skills/ux-diagnosis/system-prompt-v2.2.md`

该文件由 portable 包的 `core/system-prompt.md` 同步而来，只保留平台无关核心，不包含 Cowork / Codemaker frontmatter。当前项目的 Codex Desktop 调用壳仍是：

- `./.codex/agents/ux-laoge.toml`

不要把新版 portable 包的 `adapters/codex/AGENTS.md` 直接覆盖到本项目根目录。那个文件适合独立 Codex CLI 项目；本项目根 `AGENTS.md` 还承载 Angus 的 GDD 真源、截图交付、文档落盘语言和本地技能优先级规则。

## 触发词

以下都视为直接点名本技能：

- `@UX老哥`
- `@ux老哥`
- `@UX诊断`
- `@ux诊断`
- `@cowork-ux-diagnosis`
- “UX老哥分析一下”
- “界面硬伤 / 交互硬伤 / P0 P1 P2”

在 Codex 中，如果用户使用这些触发词，且语义是“叫一个 UX 子 agent 单独分析”，父级 Codex 应优先 spawn 项目 subagent `ux_laoge`，并把截图、问题描述、相关文件路径和必要上下文传给它。

如果当前运行环境暂时没有暴露 `ux_laoge`，父级 Codex 必须在当前线程执行同等诊断，并且同样先读取完整 spec：

- `./skills/ux-diagnosis/system-prompt-v2.2.md`

## 强制读取顺序

执行诊断前，按这个顺序读取：

1. `./skills/ux-diagnosis/system-prompt-v2.2.md`
2. `./AGENTS.md`
3. `./docs/onboarding/ai-collaboration-guidance.md`
4. 涉及 UI、交互、原型呈现或视觉实验页时，读取 `./docs/onboarding/ui-interaction-guidelines.md`
5. 涉及 Angus 系统功能、玩法、全链 Demo、原型 UI 或截图时，按需读取相关 `design/gdd/` 真源和原型文件

项目级基础真源通常包括：

- `./design/gdd/core-experience.md`
- `./design/gdd/gameplay-design-principles.md`
- `./design/gdd/systems-index.md`

## 图片传递

如果父级 Codex 能把原始截图作为 `image` / `local_image` item 传给 `ux_laoge`，必须传原图；如果当前工具限制导致只能转写截图内容，父级必须在最终回答里说明“本次 UX 老哥基于截图转写而非原图像素”，不能假装做过逐像素视觉审计。

## 辅助 KB

这些项目本地技能是完整 spec 的长尾资料库，只在触发条件满足时读取，不要默认全量加载：

- `./skills/ux-kb-risks/SKILL.md`：商城、礼包、付费、充值、抽卡时必读
- `./skills/ux-kb-cross-page/SKILL.md`：多界面、跨流程诊断时读取
- `./skills/ux-kb-symptoms/SKILL.md`：症状命名卡住时读取
- `./skills/ux-kb-principles/SKILL.md`：需要更细原则论证时读取
- `./skills/ux-kb-templates/SKILL.md`：需要复杂 ASCII 布局、报告模板或方案表达时读取

如果使用了任何 KB，输出中要明确说明使用了哪个 KB；如果判断不触发，也要在必要时说明未触发原因。

## 输出边界

- 默认只做 UX 诊断，不直接改代码。
- 不要把 v2.2 工作流压缩成泛泛建议；除非用户明确要求“只给摘要”，否则要保留界面类型、目标对齐、操作链、冲突检测、P0/P1/P2、改进方案、Top 3 ROI 和待确认问题。
- 截图外的信息必须标注“需确认”，不要装作已经验证。
- 如果父级 Codex 需要最终回复，必须交付完整报告正文；可以额外补一个短结论，但不能用短结论替代 subagent 的完整诊断产物。
- 父级 Codex 若同时执行了修改，最终回复必须分成两层：一层说明“我如何执行 / 已落地 / 未采纳或待确认”，另一层用 Markdown `<details><summary>UX 老哥诊断原文</summary>…</details>` 保留 UX 老哥意见正文。除非用户明确要求极简摘要，不得直接省略 UX 老哥意见。
