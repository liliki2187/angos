# 当前交接状态

更新时间：2026-04-10

## 当前主线判断

- 项目当前仍在 **周循环正式 schema 迁移 / `weekly_run` 收口** 这条线上。
- 直接依据：
  - 阶段标记：`production/stage.txt` 当前为 `early-production`
  - 阶段报告：`production/project-stage-report.md` 当前写的是“早期制作”
  - 活跃会话：`production/session-state/active.md`
  - 当前 sprint：`production/sprints/2026-04-09-weekly-schema-migration-slice-1.md`
- 结论：
  - 这不是“已经离开周循环主线，开始做别的里程碑”的状态。
  - 当前更像是：`weekly_run` 运行时已经能玩，但性能、正式字段收口和设计文档同步还没彻底闭环。

## 现在真正需要记住的状态

- 正式运行时真源：
  - `gd_project/scenes/gameplay/weekly_run/`
- 周循环顶层阶段真源：
  - `design/gdd/weekly-run-loop.md`
- 当前正式阶段链路：
  - `briefing -> explore -> editorial -> summary`
- 旧 `full_chain/`：
  - 仅保留兼容入口，不再是正式实现真源

## 本轮新增结论

### 1. 目录标准已补正

以下内容原本落在不合适的位置，现已按当前仓库标准重新归位：

- 旧母文档：
  - `设计文档/系统功能设计总集.md`
  - 已移到：`docs/archive/legacy-design/系统功能设计总集.md`
- 待拍板头脑风暴：
  - `design/gdd/brainstorm-synthesis-cognition-2026-04-06.md`
  - 已移到：`docs/archive/deferred-design/brainstorm-synthesis-cognition-2026-04-06.md`
- HTML 实验页：
  - `design/htmls/synth-workbench-lab.html`
  - 已移到：`design/prototypes/html/labs/synth-workbench-lab.html`

并补了归档说明：

- `docs/archive/deferred-design/README.md`
- `docs/archive/legacy-design/README.md`
- `design/prototypes/html/labs/README.md`

### 2. 顶层设计文档冲突已拍板并完成同步

当前已按用户确认，以 **2026-04-09 全链原型** 作为这一组规则的正式来源，完成并回：

- `design/gdd/game-concept.md`
- `design/gdd/game-pillars.md`
- `design/gdd/systems-index.md`
- `design/gdd/content-production-and-article-generation.md`
- `design/gdd/editorial-layout-and-publishing-strategy.md`
- `design/gdd/issue-settlement-and-audience-feedback.md`
- `design/gdd/macro-attributes-and-reality-shift.md`

已正式写入的规则包括：

- 认知主要由 **内审定调** 生成
- **抢先快讯** 可以不经过认知直接发
- 正式稿件命名切到：
  - `抢先快讯 / 深度报道 / 个人专栏 / 爆炸性新闻`
- 引入 **主笔 / SAN / 心理干预 / 内审疲劳**
- 引入 **公开取向**
- 引入 **同题疲劳**
- 引入 **取向冲突惩罚**
- 异常内审成功会直接推动 **宏观狂性** 上升

### 3. 设计复核已继续完成，并补齐契约层缺口

在继续做 `design-review` 后，已把原本还不够落地的部分补进正式 GDD：

- `design/gdd/weekly-run-loop.md`
  - 已明确：异常题材内审成功带来的 `狂性` 增量可以在 `editorial` 直接入账
  - 已明确：`topic_stance_history` 属于长期状态，由结算系统更新
- `design/gdd/clue-and-content-inventory.md`
  - 已补素材字段契约：
    - `kind / domain / tier / topic_key / mystery_bias / evidence_value / consumable`
  - 已补公开合成时的默认消耗规则
- `design/gdd/content-production-and-article-generation.md`
  - 已补 `SAN` 风险区间
  - 已补 `心理干预包` 的默认供给规则
  - 已补 `article_candidates` 的字段契约
- `design/gdd/editorial-layout-and-publishing-strategy.md`
  - 已补 `published_issue / placed_articles` 的字段契约
  - 已补同题疲劳的当前原型常量基线
- `design/gdd/issue-settlement-and-audience-feedback.md`
  - 已补结算输入契约，明确结算读取哪些冻结字段

当前文档层面的结论：

- 这组规则现在已经不再是“仅原型成立、正式文档还没落稳”的状态
- 当前更适合把后续工作转回运行时实现与参数打磨，而不是继续大范围重写设计文档

## 已验证

- 本地 Windows 包已重新导出：
  - `gd_project/build/debug/Angus.exe`
  - `gd_project/build/debug/Angus.console.exe`
  - `gd_project/build/release/Angus.exe`
- 这次导出后 `git status` 仍可控，没有新的意外脏改动
- 退出时仍有旧告警：
  - `ObjectDB instances leaked at exit`
  - `resources still in use at exit`

## 当前还没闭环的点

1. 探索页切换节点仍是整页刷新
原因：
`WeeklyRunGame._on_node_pressed()` 现在仍直接走 `_refresh_all()`，还没做局部刷新。

2. `gd_project/project.godot` 里的 `config/features` 仍显示 `4.3`
原因：
还没做一次正式编辑器保存迁移。

3. Godot 退出泄漏告警仍在
原因：
当前没有继续追这条线，只确认了它不阻塞本地导出。

4. 内容生产链规则虽然已完成正式文档同步，但运行时还没有完整落到这套新契约
原因：
当前 `weekly_run` 运行时代码还没有完整对齐 `public_stance`、同题历史、成刊快照字段等新设计契约。

## 如果现在要 close 当前工作，用什么技能

最合适的是：

- `retrospective`

原因：

- 当前更像是“要给这条正在做的 sprint / 切片收尾、记录完成项与 carryover”，不是要切阶段。
- `project-stage-detect` 适合回答“项目现在在哪个阶段”
- `gate-check` 适合回答“是否可以进入下一开发阶段”
- `milestone-review` 适合做整个 milestone 的阶段性评估，范围更大，也更重

所以如果只是想：

- 关掉当前这轮 weekly schema 迁移切片
- 记录哪些完成了、哪些 carry over
- 再切到设计修改

优先用 `retrospective`，不要先用 `gate-check`。

## 下个会话最合理的顺序

1. 先用 `retrospective` 给当前这轮 weekly schema / weekly_run 切片做收尾
2. 回到运行时，开始把 `weekly_run` 对齐到新的内容生产链契约
3. 继续处理：
   - ExplorePhase 局部刷新
   - `project.godot` 版本戳迁移
   - 退出泄漏告警
4. 如果继续做设计侧工作，优先是参数与验收细化，而不是重新开一轮大规则改写
