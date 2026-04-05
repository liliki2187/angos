# Sprint：仓库治理基础

**周期**：2026-04-04 至 2026-04-11  
**状态**：进行中  
**来源计划**：`docs/plans/project-structure-collaboration-governance-plan.md`

## Sprint 目标

1. 落地持续协作所需的最小生产工作区
2. 建立唯一的 Git 协作权威入口
3. 明确哪些目录是规范层、仅参考层或生成层
4. 降低生成 Demo 包与缓存带来的工作区噪音

## 计划交付物

- `production/stage.txt`
- 包含 backlog、sprint、milestone、risk 与 handoff 文档的生产骨架
- 仓库地图与 Git 协作入门文档
- 更新后的根 README 与 AI 交接文档
- 针对生成 Demo 包和 Python 缓存的忽略规则

## 完成定义

- 核心治理文档已经存在，并且互相引用一致
- `git status` 不再被 `prototype/fullchain_demo` 或 `scripts/__pycache__` 污染
- 入门材料指向明确的规范目录，而不是零散假设
