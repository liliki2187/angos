# Sprint：仓库治理基础

- **周期**：2026-04-04 至 2026-04-11
- **状态**：已完成（2026-04-09 收口）
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
- `git status` 不再被 历史分发包目录或 `scripts/__pycache__` 污染
- 入门材料指向明确的规范目录，而不是零散假设

## 实际完成

- 已建立 `production/` 执行工作台，并补齐 `stage.txt`、`milestones/`、`sprints/`、`backlog/`、`risk-register/`、`handoff/`、`roles/` 与 `session-state/` 基础骨架。
- 已补仓库治理所需的核心说明文件，包括 `production/README.md`、`production/milestones/godot-mvp-foundation.md`、`production/backlog/current.md`、`production/risk-register/current.md` 与 `production/session-state/active.md`。
- 已把 Git 协作规则统一收口到 `docs/onboarding/git-collaboration.md`，并让根 `README.md` 与 `docs/onboarding/repository-map.md` 指向规范目录和协作入口。
- 已下线历史原型 CI 与分发脚本，并把相关工作流和打包链路归档到 `_obsolete/`，避免继续与正式工作流混用。
- 已通过 `.gitignore`、目录整理和归档规则，降低历史分发包、缓存和生成产物对工作区的干扰。

## 转入下一轮

- 按 `design/gdd/weekly-run-loop.md` 把 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 从 demo 状态迁移到正式周状态 schema。
- 在代码重构前补一份 ADR，明确 demo 字段向正式周状态字段的迁移边界。
- 继续抽离 `FullChainGame.gd` 中的状态、内容和 UI 责任，并补最小自动化覆盖。
- 为第一份真正的功能包明确 `specs/` 的使用方式，作为治理基础后的常态流程。

## 收口判断

- [x] `production/` 已具备阶段、冲刺、待办、风险和交接的最低执行能力。
- [x] Git 协作权威入口已经单点收口，不再依赖多份互相冲突的旧说明。
- [x] 根 `README`、仓库地图和技术偏好已能把新接手者快速导向规范目录。
- [x] 当前 `git status` 不再被历史分发产物或 Python 缓存污染，治理目标已从“补基础设施”转为“按规则持续维护”。

以上说明本 sprint 的完成定义已经满足，可以正式关闭，并把主线切换到周循环 schema 迁移与运行时代码去原型化。

