# Sprint：周循环正式 Schema 迁移（切片 1）

- **周期**：2026-04-09 至 2026-04-16
- **状态**：已收尾（2026-04-10，遗留项转下一轮）
- **里程碑**：`production/milestones/godot-mvp-foundation.md`
- **约束来源**：`design/gdd/weekly-run-loop.md`、`docs/architecture/adr-0001-godot-week-loop-state-and-data-boundaries.md`、`docs/architecture/adr-0003-demo-weekly-schema-migration-boundary.md`

## Sprint 目标

在不打断当前 Godot 可玩周循环的前提下，以游戏系统所有权为单位重建正式周循环运行时骨架，把临时 `full_chain` 聚合实现迁到可管理的正式 weekly schema，并建立最小回归保护。

## 执行原则

- 本轮不以固定工时裁剪范围，质量、系统边界和后续管理优先。
- 当前 `gd_project/scenes/gameplay/full_chain/` 视为临时入口，不是必须保留的正式结构。
- 如果原地改造会继续固化单体脚本和临时目录命名，允许在新的 gameplay 系统目录中重写正式实现，再由旧入口过渡接线。
- 拆分粒度按游戏系统所有权，而不是按当前 UI 面板、演示页面或历史脚本名划分。
- 正式系统切片至少要能表达：周状态容器、`briefing`、派遣 / 外采结果、素材库存引用、认知 / 稿件候选、排版 / 发刊、结算。
- UI 场景和绑定脚本只负责展示与动作请求，不继续担任玩法状态聚合器。

## Tasks

> 说明：以下“预估”仅用于表达复杂度和依赖顺序，不作为砍项依据。

### Must Have（关键路径）

| ID | 任务 | Owner | 预估 | 依赖 | 验收标准 |
|----|------|-------|------|------|----------|
| WS-01 | 已完成：补齐 ADR-0003，冻结 demo 周字段到正式 weekly schema 的迁移边界，并确认允许在新系统目录中落地正式实现 | 架构 / 运行时 | 0.5 天 | 无 | ADR 已落盘，字段映射、阶段流、目录迁移立场和过渡规则明确 |
| WS-02 | 建立系统导向的正式周循环运行时骨架；如 `full_chain` 目录继续阻碍所有权表达，则在新的 gameplay 系统目录中承载正式入口 | 运行时 | 1.5 天 | WS-01 | 运行时入口不再被 demo 目录结构绑死，周循环主入口的职责边界清晰 |
| WS-03 | 在正式入口中引入真实 `briefing` 顶层阶段，并把新开局 / 下一周入口改到 `briefing` | 运行时 | 1.5 天 | WS-02 | 新开局与下一周都先进入 `briefing`，玩家确认后才进入 `explore` |
| WS-04 | 把周顶层 canonical 状态收口到正式 schema，至少完成 `remaining_days`、`article_candidates`、`published_issue`、`settlement_result` 的正式写路径，并集中到更可管理的状态容器 / 模块 | 运行时 | 2.0 天 | WS-02 | 关键状态不再以 `day`、`story_pool`、`last_summary` 对外暴露，也不再散落成难以管理的脚本成员变量集合 |
| WS-05 | 按正式系统链路重写 demo 主链 `weekly_clues -> story_pool -> settlement`，并保留受控过渡适配 | 运行时 | 1.5 天 | WS-03, WS-04 | 运行时主流程开始围绕正式系统链路工作，不再把 `story_pool` / `last_summary` 作为外显正式概念 |
| WS-06 | 为周阶段切换与结算公式补最小自动化覆盖 | 测试 | 1.0 天 | WS-02, WS-03, WS-04 | 至少具备阶段切换和结算结果各 1 条自动化用例 |

### Should Have

| ID | 任务 | Owner | 预估 | 依赖 | 验收标准 |
|----|------|-------|------|------|----------|
| WS-07 | 在不拆场景的前提下，为周顶层状态抽出更集中、更可读的容器结构 | 运行时 | 0.5 天 | WS-03 | 周状态访问点减少，字段初始化更集中 |
| WS-08 | 识别 `material_inventory`、`cognition` 与结算模块的下一轮拆分接口 | 架构 / 运行时 | 0.5 天 | WS-04 | 留下明确的下一轮拆分清单，而不是笼统 TODO |

### Nice to Have

| ID | 任务 | Owner | 预估 | 依赖 | 验收标准 |
|----|------|-------|------|------|----------|
| WS-09 | 为第一份真实功能包起草 `specs/` 使用样板 | 生产 / 架构 | 0.5 天 | WS-01 | 明确这条功能线之后如何使用 `specs/` 承接后续切片 |

## Carryover from Previous Sprint

| 任务 | 原因 | 新预估 |
|------|------|--------|
| 按 `design/gdd/weekly-run-loop.md` 迁移 `FullChainGame.gd` 到正式周状态 schema | 上一轮 sprint 聚焦仓库治理基础，功能迁移被顺延 | 4.5 天 |
| 为周阶段切换与结算公式建立最小自动化覆盖 | 治理 sprint 未进入测试主线 | 1.0 天 |
| 为第一份真实功能包明确 `specs/` 的使用方式 | 治理基础收口前没有合适的承载对象 | 0.5 天 |

## Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| `FullChainGame.gd` 单体脚本回归面过大 | 高 | 高 | 先锁字段边界，再按阶段切片迁移，并用最小自动化覆盖兜底 |
| 新旧字段并存时间过长，形成双真源 | 中 | 高 | 明确 canonical 写路径立即切到正式字段，旧字段只允许局部适配 |
| `briefing` 引入后，现有 UI 与流程衔接断裂 | 中 | 中 | 先保证 `briefing -> explore` 的最小闭环，再继续推进编辑链 |
| 测试框架与样例尚未落地，导致回归保护不足 | 高 | 中 | 优先覆盖阶段切换和结算公式，先求关键路径有保护 |

## Dependencies on External Factors

- `design/gdd/weekly-run-loop.md` 的正式字段命名在本 sprint 内保持稳定。
- 测试实现需要在 GdUnit4 或 GUT 中选择一条可立即落地的最小路径。
- 若 `briefing` 文案 / 任务 / 机会生成规则需要超出当前 GDD 的新设计，应先补文档再扩实现。

## Definition of Done for this Sprint

- [ ] `ADR-0003` 已存在并可作为运行时迁移边界引用
- [ ] 新开局和下一周都先进入 `briefing`
- [ ] 顶层周状态的 canonical 名称已向正式 weekly schema 收口
- [ ] demo 主链不再以 `weekly_clues -> story_pool -> settlement` 作为外显正式描述
- [ ] 周阶段切换与结算公式至少有最小自动化覆盖
- [ ] 若实现偏离 GDD，相关文档已同步更新

## 收尾说明

- 本轮 retrospective 已写入：
  - `production/sprints/2026-04-09-weekly-schema-migration-slice-1-retrospective.md`
- 当前可视为完成的目标：
  - 正式运行时骨架已收口到 `weekly_run`
  - 四阶段链路已成立
  - 最小 smoke test 已到位
- 转入下一轮的重点：
  - `ExplorePhase` 局部刷新
  - `cognition` / 结算模块下一轮拆分接口
  - 正式 GDD 同步 2026-04-09 原型规则
