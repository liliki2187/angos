# weekly_run

这个目录是 Angus 当前正式周循环运行时的系统入口，不再把 `full_chain/` 视为长期根目录。

## 目录职责

- `WeeklyRunGame.tscn`
  固定壳层，只承载顶部周信息与阶段宿主，不再直接混排四个阶段内容。
- `WeeklyRunGame.gd`
  UI 绑定脚本，负责状态绑定、阶段切换和 phase scene 之间的协调。
- `components/`
  正式切片的可复用 UI 组件场景，例如指标卡、动作项和信息卡。
- `content/WeeklyRunContent.gd`
  周循环当前使用的静态内容与平衡常量。
- `materials/WeeklyMaterialInventory.gd`
  素材库存真源，承接探索结果并向编辑阶段提供可消费素材。
- `phases/`
  `briefing`、`explore`、`editorial`、`summary` 四个阶段的独立场景与绑定脚本。
- `state/WeeklyRunState.gd`
  周循环正式状态容器，持有顶层阶段、周内字段和当前过渡期的长期运行值。
- `systems/WeeklyRunSystems.gd`
  周循环规则系统，处理简报生成、派遣结果、候选稿件生成、发刊与结算。

## 当前边界

- 正式顶层阶段：`briefing -> explore -> editorial -> summary`
- 正式关键字段：`remaining_days`、`article_candidates`、`published_issue`、`settlement_result`
- 素材真源由 `materials/WeeklyMaterialInventory.gd` 持有；`WeeklyRunState` 只保留 `new_material_ids` 这类周内引用。
- 正式 UI 边界：四个阶段各自拥有独立 phase scene，`briefing` 不再借住 `explore` 页面，整页布局不再沿用 demo 的混合工作台。

## 过渡说明

- `gd_project/scenes/gameplay/full_chain/` 现在只保留显式兼容 shim，用来承接旧场景路径。
- 菜单路径已经改到 `weekly_run/`，后续如需彻底清理旧入口，应先完成 shim 或归档策略。
