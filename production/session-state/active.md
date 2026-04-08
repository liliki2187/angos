# 会话状态

- **日期**：2026-04-09
- **任务**：周循环正式 schema 迁移与 `FullChainGame` 重构准备
- **状态**：进行中

## 本轮已完成

- `仓库治理基础` sprint 已正式收口，生产工作台、仓库地图、Git 协作入口与忽略规则已达到最低治理目标。
- `docs/technical-preferences.md` 与 `docs/architecture/adr-0002-godot-ui-scene-first-and-binding-driven.md` 已明确正式 UI 的场景优先与绑定式脚本规范。
- `design/gdd/weekly-run-loop.md` 及相邻周循环 GDD 已对齐为 `briefing -> explore -> editorial -> summary` 的顶层阶段结构。

## 当前真实来源

- 运行时行为：`gd_project/scenes/` 与 `gd_project/Assets/`
- Godot 项目根：`gd_project/project.godot`
- 周循环顶层状态真源：`design/gdd/weekly-run-loop.md`
- 技术边界与 ADR：`docs/architecture/`
- 技术默认值与 UI 实现硬约束：`docs/technical-preferences.md`
- 执行状态：`production/`
- Git 协作权威入口：`docs/onboarding/git-collaboration.md`

## 紧接着要做的事

1. 先补一份 ADR，明确 demo 周状态字段如何迁移到正式 weekly schema。
2. 重构 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 的顶层状态和字段命名，并在代码层引入 `briefing`。
3. 把 demo 流程 `weekly_clues -> story_pool -> settlement` 改成 `dispatch result -> material inventory -> cognition -> article_candidates -> published_issue -> settlement_result`。
4. 在结构稳定后，为周阶段切换与结算公式补最小自动化覆盖。

## 备注

- 仓库治理相关目录与规则已进入维护态，不再作为当前 sprint 主线。
- 历史分发包链路已归档到 `_obsolete/scripts/release/`，HTML 参考源码保留在 `design/prototypes/html/`。
- 当前工作区仍有本地 `tmp/` 草稿，默认不纳入正式提交。
