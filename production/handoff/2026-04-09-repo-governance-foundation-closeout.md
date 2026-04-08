# 交接：仓库治理基础 Sprint 收口

- **日期**：2026-04-09
- **状态**：已收口
**对应 Sprint**：`production/sprints/2026-04-04-repo-governance-foundation.md`

## 当前目标

- 正式关闭“仓库治理基础” sprint，并把执行主线切换到周循环正式 schema 迁移与 `FullChainGame` 去原型化。

## 已完成工作

- `production/` 执行工作台已落地，具备 `stage.txt`、`milestones/`、`sprints/`、`backlog/`、`risk-register/`、`handoff/`、`roles/` 与 `session-state/` 的基础骨架。
- Git 协作权威入口已统一收口到 `docs/onboarding/git-collaboration.md`。
- 根 `README.md` 与 `docs/onboarding/repository-map.md` 已明确规范层、参考层与归档层位置。
- 历史原型 CI、发布脚本与相关工作流已归档到 `_obsolete/`，不再与正式主线混用。
- `.gitignore` 与目录治理规则已把历史分发产物、Python 缓存和本地桥接状态排除出常规工作区噪音。

## 未解决阻塞

- 治理 sprint 本身没有阻塞收口的问题。
- 以下事项仍未完成，但它们属于下一轮实现主线，而不是本 sprint 的关闭条件：
  - `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 仍然单体化，继续混合状态、内容与 UI 责任。
  - demo 周状态字段仍未迁移到 `design/gdd/weekly-run-loop.md` 定义的正式 schema。
  - 周阶段切换与结算公式仍缺最小自动化覆盖。

## 变更文件

- `production/README.md`
- `production/stage.txt`
- `production/milestones/godot-mvp-foundation.md`
- `production/backlog/current.md`
- `production/risk-register/current.md`
- `production/session-state/active.md`
- `production/sprints/2026-04-04-repo-governance-foundation.md`
- `docs/onboarding/repository-map.md`
- `docs/onboarding/git-collaboration.md`
- `README.md`
- `.gitignore`

## 建议下一步

1. 先写一份 ADR，明确 demo 周状态字段迁移到正式 weekly schema 的技术决定。
2. 依照 `design/gdd/weekly-run-loop.md` 重构 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 的顶层状态和字段命名。
3. 在代码层引入 `briefing`，并把 `weekly_clues -> story_pool -> settlement` 的 demo 流程替换为正式内容链路。
4. 重构稳定后，为周阶段切换、结算公式和关键状态迁移补最小自动化测试。
