# 生产工作区

本目录是 Angus 的执行层。

使用它快速回答四个问题：

1. 项目当前处于哪个阶段？
2. 当前 sprint 真实在推进什么？
3. 当前有什么阻塞或风险？
4. 下一次会话应该接着做什么？

## 目录说明

- `stage.txt`：用一行表示当前项目阶段
- `milestones/`：里程碑定义与退出标准
- `sprints/`：短期执行包
- `backlog/`：按优先级排列的待办工作
- `risk-register/`：当前交付与质量风险
- `handoff/`：会话或里程碑交接记录
- `roles/`：目录归属与协作边界
- `session-state/`：当前活跃会话摘要

## 权威规则

- 运行时真源位于 `gd_project/scenes/` 及相关 `gd_project/Assets/`。
- 设计真源位于 `design/gdd/`。
- 架构真源位于 `docs/architecture/`。
- 本目录只负责追踪执行状态，不负责承载深度设计正文。
