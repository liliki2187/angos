# handsoff

> 日期：2026-04-08
> 范围：周循环真源收紧、相邻 GDD 对齐、系统索引同步

## 本轮已完成

1. 重写了 `design/gdd/weekly-run-loop.md`，把顶层阶段锁成 `briefing -> explore -> editorial -> summary`。
2. 在 `design/gdd/weekly-run-loop.md` 补了周状态 schema、长期状态边界、`remaining_days` 统一命名、`next_week_hooks` 交接，以及“无合法派遣时强制进入编辑阶段”的可实现规则。
3. 对齐了以下相邻设计文档的父子阶段与数据所有权：
   - `design/gdd/turn-start-events-and-cycle-tasks.md`
   - `design/gdd/exploration-and-node-dispatch.md`
   - `design/gdd/clue-and-content-inventory.md`
   - `design/gdd/content-production-and-article-generation.md`
   - `design/gdd/editorial-layout-and-publishing-strategy.md`
   - `design/gdd/issue-settlement-and-audience-feedback.md`
4. 更新了 `design/gdd/systems-index.md`，让系统索引反映新的周循环真源、父子阶段和当前进度。

## 已锁定的设计决定

- 周循环只有四个顶层父阶段：`briefing`、`explore`、`editorial`、`summary`。
- 新周必须先进入 `briefing`，不能直接落在 `explore`。
- 探索结果的真源是素材库存，不再允许周循环另存一份 `weekly_clues` 式正文副本。
- `editorial` 是内容生产和排版的父阶段，`summary` 是结算和世界反馈的父阶段。
- 下周生成偏置通过 `next_week_hooks` 传递，而不是散落在各系统的隐式字段里。

## 目前哪些 demo 内容不应继续当正式参考

当前 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 仍是 demo 状态。以下内容只应视为原型实现痕迹，不应继续当正式真源：

- `day`：正式设计已统一成 `remaining_days`。
- `weekly_clues`：正式设计已改成素材库存真源 + `new_material_ids` 引用。
- `story_pool`：它更像 demo 的候选稿缓存，后续应由 `article_candidates` 接管。
- `editorial_profile`：目前仍是 demo 性的聚合轴，正式版需重新定义它与宏观属性、稿件属性、发行策略的关系。
- `current_phase` 目前只有 `explore/editorial/summary`，缺 `briefing`，且仍是集中脚本驱动。
- 各类直接写 `macro_stats`、直接从探索结果跳成线索/稿件的逻辑，都不能再视为正式结构。

## 接手人下一步最该做什么

1. 先按 `design/gdd/weekly-run-loop.md` 重构 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 的顶层状态和字段命名。
2. 把 demo 里的 `weekly_clues -> story_pool -> settlement` 流程改成：
   `dispatch result -> material inventory -> cognition -> article_candidates -> published_issue -> settlement_result`。
3. 在代码层引入 `briefing`，让周起始事件、任务、机会池真的先生成再进入探索。
4. 在重构代码前，最好先写一份 ADR，明确“demo 字段迁移到正式周状态 schema”的技术决定。

## 本次提交建议包含

- `design/gdd/*.md` 中本轮修改过的 8 份设计文档
- 本文件 `tmp/handsoff.md`

## 未纳入本次提交的现有无关改动

以下文件在本轮开始前就处于未提交状态，且不属于这次周循环设计收紧：

- `docs/technical-preferences.md`
- `docs/architecture/adr-0002-godot-ui-scene-first-and-binding-driven.md`
- `tmp/2026-04-06-brainstorm-handoff.md`
- `tmp/designer_brainstorm`
