# weekly_run

这个目录是 Angus 当前正式周循环运行时的系统入口，不再把 `full_chain/` 视为长期根目录。

## 目录职责

- `WeeklyRunGame.tscn`
  场景壳层，负责承载正式周循环页面。
- `WeeklyRunGame.gd`
  UI 绑定脚本，只负责节点引用、输入响应、阶段刷新和展示更新。
- `content/WeeklyRunContent.gd`
  周循环当前使用的静态内容与平衡常量。
- `state/WeeklyRunState.gd`
  周循环正式状态容器，持有顶层阶段、周内字段和当前过渡期的长期运行值。
- `systems/WeeklyRunSystems.gd`
  周循环规则系统，处理简报生成、派遣结果、候选稿件生成、发刊与结算。

## 当前边界

- 正式顶层阶段：`briefing -> explore -> editorial -> summary`
- 正式关键字段：`remaining_days`、`article_candidates`、`published_issue`、`settlement_result`
- `material_inventory` 目前仍是过渡实现，后续应继续从 `WeeklyRunState` 中抽出为独立系统。

## 过渡说明

- `gd_project/scenes/gameplay/full_chain/` 仍保留旧 demo 实现，当前不再作为正式入口。
- 菜单路径已经改到 `weekly_run/`，后续如需彻底清理旧入口，应先完成 shim 或归档策略。
