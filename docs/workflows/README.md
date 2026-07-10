# Angus 工作流护栏

本目录存放 Angus AI 协作使用的轻量工作流护栏。

任务复杂度超过 tiny typo 或明显小 bug 时，按需使用以下文件：

- [`angus-workflow-harness.md`](./angus-workflow-harness.md)：主流程，从轻量路由到 hard gate。
- [`../../skills/git-cloud-submit/SKILL.md`](../../skills/git-cloud-submit/SKILL.md)：Git 工作区盘点、分批、验证、提交与推送的固定流程，按 Luna / Terra / Sol 分配模型职责。
- [`workflow-gates.yml`](./workflow-gates.yml)：机器可读的阶段、风险与产物规则；自 2026-07-08 起作为产物类型、阶段转换与 hard gate 真源，gate 变更必须同步写入此文件。
- [`ui-geometry-and-text-safety-gates.md`](./ui-geometry-and-text-safety-gates.md)：资产化 UI 链和美术动效链共用的几何、正交与文字安全 gate 真源。
- [`godot-agent-smoke.md`](./godot-agent-smoke.md)：Codex 改动后的 Godot 健康检查，组合 `gda script validate` 与真实 headless weekly-run smoke。
- [`godot-debug-skill-v0.md`](./godot-debug-skill-v0.md)：Angus Godot 错误笔记，提供白话错误卡、修复规则与验证命令。
- `scripts/run_godot_gui_startup_check.ps1`：Windows GUI / 精确 Godot 可执行文件的独立启动检查。
- [`ai-radar-memory.md`](./ai-radar-memory.md)：Angus AI 日报 / 下一期报告的上下文侧车。
- [`ai-radar-loop-cases.md`](./ai-radar-loop-cases.md)：AI 情报报告的 Loop case 与报告状态对象。
- [`templates/router-card.md`](./templates/router-card.md)：快速任务入口卡。
- [`templates/delivery-manifest.md`](./templates/delivery-manifest.md)：交付与产物分类记录。
- [`templates/loop-log.md`](./templates/loop-log.md)：反馈后复盘与沉淀记录。
- [`templates/workflow-lab-checklist.md`](./templates/workflow-lab-checklist.md)：进入硬自动化前的小型实验清单。

本套护栏不是要求每个任务调用所有 agent。流程应先提醒，再记录，只对高风险错误进行阻断。

三行 `Decision Strip` 只用于 workflow gate、Loop Log、通过 / 失败判断、阻塞或用户裁决：结论、影响、下一步。普通解释、讨论、完成汇报和轻量问答应使用自然语言。
