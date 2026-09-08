# Angus 工作流护栏

本目录存放 Angus AI 协作使用的轻量工作流护栏。

按实际问题选用以下文件，不按复杂度标签要求逐个读取：

- [`angus-workflow-harness.md`](./angus-workflow-harness.md)：按目标、后果与证据组织任务，不固定模板、代理数量或阶段顺序。
- [`../../skills/git-cloud-submit/SKILL.md`](../../skills/git-cloud-submit/SKILL.md)：Git 工作区盘点、交接完整性分类、分批验证、多远端提交与推送的固定流程，按 Luna / Terra / Sol 分配模型职责。
- [`workflow-gates.yml`](./workflow-gates.yml)：条件式产物/证据目录；不是已自动执行所有规则的引擎。实际机器消费者目前为交付记录检查器，新增消费者需单独验证。
- [`ui-geometry-and-text-safety-gates.md`](./ui-geometry-and-text-safety-gates.md)：实际内容装配的几何/文字检查；阈值来自当前组件合同，不统一套历史参数。
- [`godot-agent-smoke.md`](./godot-agent-smoke.md)：覆盖 weekly-run 特定路径的可选健康检查，组合 `gda script validate` 与真实 headless weekly-run smoke。
- [`godot-visual-feedback-smoke.md`](./godot-visual-feedback-smoke.md)：覆盖探索/派遣特定路径的图像采集与有效性检查，产出真实窗口截图并挡住黑帧 / 空帧假阳性。
- [`godot-debug-skill-v0.md`](./godot-debug-skill-v0.md)：Angus Godot 错误笔记，提供白话错误卡、修复规则与验证命令。
- `scripts/run_godot_gui_startup_check.ps1`：Windows GUI / 精确 Godot 可执行文件的独立启动检查。
- [`ai-radar-memory.md`](./ai-radar-memory.md)：Angus AI 日报 / 下一期报告的上下文侧车。
- [`ai-radar-loop-cases.md`](./ai-radar-loop-cases.md)：AI 情报报告的 Loop case 与报告状态对象。
- [`templates/router-card.md`](./templates/router-card.md)：快速任务入口卡。
- [`templates/delivery-manifest.md`](./templates/delivery-manifest.md)：交付与产物分类记录。
- [`templates/loop-log.md`](./templates/loop-log.md)：反馈后复盘与沉淀记录。
- [`templates/workflow-lab-checklist.md`](./templates/workflow-lab-checklist.md)：进入硬自动化前的小型实验清单。

本套护栏不是要求每个任务调用所有 agent。流程应先提醒，再记录，只对高风险错误进行阻断。

默认自然语言交付；必要时说明决定和后果，不固定 Decision Strip 或 Human Brief。模板只在确实有用时采用。
