# 周循环与状态

> **状态**：草案
> **作者**：Codex + 仓库综合整理
> **最后更新**：2026-04-08
> **对应支柱**：调查必须导向发刊；发刊必须是一种立场选择；四大势力必须改变你的发刊决定

## 概览

这个系统是 Angus 的顶层周状态机与周内容器真源。它定义一周如何从 `briefing` 进入 `explore`，再进入 `editorial` 与 `summary`，并明确哪些数据只活在本周、哪些数据属于长期系统。如果没有它，项目会重新塌回一堆彼此抢状态所有权的原型。

## 玩家幻想

玩家应感受到自己是在持续经营一份活着的刊物，而不是在几块互不相干的界面间跳来跳去。每一周都应该像一个完整且连续的编辑周期，并且每个阶段都知道自己为什么会到来、会留下什么后果。

## 详细设计

### 核心规则

1. 周循环只拥有四个顶层相位：`briefing -> explore -> editorial -> summary`。其他系统只能在所属父阶段内运行，不再自建并列顶层阶段。
2. 新开局与每个新周都必须先进入 `briefing`。`briefing` 负责生成周起始事件、本周任务和本周内容机会；玩家确认后才能进入 `explore`。
3. `explore` 只处理时间预算与行动推进。合法探索会消耗 `remaining_days`，并把结果写入素材库存真源；周循环最多记录“本周新增素材引用”，不重复持有素材本体。
4. `editorial` 是内容生产与排版的父阶段。认知构建、稿件生成、版位选择和发刊前校验都在这里完成。
5. `summary` 是发刊结算与世界反馈的父阶段。它冻结本期周刊，计算经济、势力与宏观后果，并写出 `next_week_hooks` 供下周 `briefing` 消费。
6. 周循环负责阶段切换和周内容器清空，不直接拥有长期系统真源。订阅、势力关系、宏观属性、素材库存和区域解锁仍分别由对应系统维护。
7. 当玩家主动结束探索、`remaining_days == 0`，或当前所有可见节点都不存在合法派遣组合时，周循环强制从 `explore` 进入 `editorial`。
8. 新周初始化只重置周内字段；所有长期字段继续保留，并在 `briefing` 阶段参与本周生成。

### 顶层阶段与切换

| 顶层阶段 | 进入条件 | 退出条件 | 子系统范围 | 本阶段主要写入 |
|----------|----------|----------|------------|----------------|
| `briefing` | 新开局或上一周 `summary` 确认后 | 玩家确认进入探索 | 回合起始事件、周期任务、势力压力快照 | `briefing_event_id`、`active_tasks`、`opportunity_ids` |
| `explore` | `briefing` 确认完成 | 玩家主动结束探索，或 `remaining_days == 0`，或 `legal_dispatch_count == 0` | 区域浏览、节点派遣、事件检定、素材入库 | `remaining_days`、`new_material_ids`、周内临时节点状态 |
| `editorial` | 探索结束 | 玩家确认发刊 | 内容生产、认知构建、稿件生成、排版与发刊前校验 | `article_candidates`、`slot_assignment`、`published_issue`、`settlement_preview` |
| `summary` | 发刊确认 | 玩家确认进入下一周 | 发刊结算、受众反馈、现实偏移展示 | `settlement_result`、`next_week_hooks` |

### 周状态真源

| 字段 | 持有方 | 生命周期 | 新周行为 | 说明 |
|------|--------|----------|----------|------|
| `week` | 周循环 | 跨周 | `+1` | 当前周序号 |
| `remaining_days` | 周循环 | 周内 | 设为 `week_days` | 本周剩余行动天数 |
| `current_phase` | 周循环 | 周内 | 设为 `briefing` | 四个顶层相位之一 |
| `briefing_event_id` | 周起始系统写入，周循环持有 | 周内 | 覆盖 | 本周开场事件引用 |
| `active_tasks` | 周起始 / 势力系统写入，周循环持有 | 周内 | 清空后重生 | 本周持续生效的任务与禁令 |
| `opportunity_ids` | 周起始 / 区域系统写入 | 周内 | 刷新 | 本周可见机会、临时节点与封锁结果 |
| `new_material_ids` | 素材库存系统写回引用 | 周内展示 | 清空 | 只记录本周新增素材引用，不保存素材正文 |
| `article_candidates` | 内容生产系统写入 | 周内 | 清空 | 本周可供排版的候选稿件 |
| `slot_assignment` | 排版系统写入 | 周内 | 清空 | 版位到稿件的映射 |
| `published_issue` | 排版系统冻结 | `editorial` 到 `summary` | 清空 | 供结算消费的本期周刊快照 |
| `settlement_preview` | 编辑系统写入 | 周内 | 清空 | 发刊前风险与收益预测 |
| `settlement_result` | 结算系统写入 | `summary` | 清空 | 发刊后的可展示结果 |
| `next_week_hooks` | 结算系统写入 | 跨周一跳 | 覆盖 | 下一周生成时要消费的钩子、禁令与偏置 |

### 长期状态边界

- `material_inventory` 的真源属于 **线索与内容素材库存**；周循环只读写本周新增引用。
- `macro_stats` 的真源属于 **宏观属性与现实偏移**；周循环只在 `briefing`、`explore` 和 `summary` 阶段读取或展示。
- `faction_reputation` 与任务模板真源属于 **四大势力任务、干预与声望**。
- `subscribers`、资源与运营基线属于长期运行状态，并由 **发刊结算与受众反馈** 在 `summary` 后更新。
- 区域解锁、永久标记与世界门槛属于区域系统和宏观系统，不在周循环里重复持有第二份真源。

### 与其他系统的交互

- **回合起始事件与周期任务** 只在 `briefing` 内运行，负责生成 `briefing_event_id`、`active_tasks` 和 `opportunity_ids`。
- **探索与节点派遣** 只在 `explore` 内运行，消费 `remaining_days`、任务约束和机会池；其结果先写入素材库存，再回写 `new_material_ids` 作为本周展示引用。
- **线索与内容素材库存** 保存素材正文与跨周保留规则，并向 `editorial` 提供当前可消费的库存。
- **内容生产链与稿件生成** 与 **编辑排版与发行策略** 只在 `editorial` 内运行，分别写入 `article_candidates`、`slot_assignment`、`published_issue` 与 `settlement_preview`。
- **发刊结算与受众反馈** 只在 `summary` 内运行，读取 `published_issue` 与长期状态，写回 `settlement_result` 与 `next_week_hooks`。
- **宏观属性与现实偏移** 提供 `briefing` / `explore` 的门槛输入，并在 `summary` 后接收结算增量。
- **菜单与场景导航** 可以创建新开局、返回菜单或恢复存档，但不拥有周玩法状态本身。

## 公式

### 周天数预算

```
remaining_days_next = max(0, remaining_days_current - node_days_cost)
```

| 变量 | 类型 | 范围 | 来源 | 说明 |
|------|------|------|------|------|
| `remaining_days_current` | int | 0-7 | 周状态 | 派遣前剩余天数 |
| `node_days_cost` | int | 1-3+ | 节点数据 | 一次远征消耗的时间 |
| `remaining_days_next` | int | 0-7 | 计算值 | 派遣后剩余天数 |

**预期输出范围**：0 到 7  
**边界情况**：如果 `node_days_cost > remaining_days_current`，则该次派遣无效。

### 强制进入编辑阶段

```
force_editorial =
  player_end_explore
  or remaining_days == 0
  or legal_dispatch_count == 0

legal_dispatch_count =
  count(dispatch_enabled(node, team) == true
        for each visible node
        for each available team combination of size 1..3)
```

| 变量 | 类型 | 范围 | 来源 | 说明 |
|------|------|------|------|------|
| `player_end_explore` | bool | true/false | 玩家输入 | 是否主动结束探索 |
| `remaining_days` | int | 0-7 | 周状态 | 当前剩余行动天数 |
| `legal_dispatch_count` | int | 0+ | 运行时检查 | 当前所有可见节点与合法队伍组合的可执行数量 |

**实现约束**：隐藏节点在被揭示前不计入 `legal_dispatch_count`。  
**UI 约束**：若因 `legal_dispatch_count == 0` 被迫收周，系统应先展示一次“本周已无合法派遣”的确认提示。

### 新周初始化契约

```
new_week.week = old_week.week + 1
new_week.remaining_days = week_days
new_week.current_phase = "briefing"
new_week.briefing_event_id = briefing_result.event_id
new_week.active_tasks = briefing_result.tasks
new_week.opportunity_ids = briefing_result.opportunities
new_week.new_material_ids = []
new_week.article_candidates = []
new_week.slot_assignment = {}
new_week.published_issue = {}
new_week.settlement_preview = {}
new_week.settlement_result = {}
new_week.next_week_hooks = summary_result.next_week_hooks
```

这是一条规则契约，而不是平衡公式。它的作用是把顶层周内容器与长期状态明确分离，并保证每个新周总是从 `briefing` 而不是 `explore` 开始。

## 边界情况

| 场景 | 预期行为 | 理由 |
|------|----------|------|
| 上一周 `summary` 确认后进入新周 | 必须先进入 `briefing`，不能直接落在 `explore` | 保证周起始事件、任务与压力总是可见 |
| 远征后 `remaining_days` 归零 | 强制切入 `editorial` | 防止出现死局周状态 |
| 玩家提前结束探索 | 允许带着较少素材进入编辑 | 弱势的一周也应可发刊 |
| 本周没有新增素材 | 仍可用跨周保留库存或低质量保底稿进入编辑 | 维持周闭环 |
| `next_week_hooks` 为空 | `briefing` 仍要生成基础事件、任务与机会 | 保持周结构完整 |
| 版面未填满时结算 | 允许，但给予经济惩罚 | 保持可读性并让后果可学习 |
| 亏损的一周后进入新周 | 继续游戏，只是长期值已被更新 | 支持带恢复空间的循环 |

## 依赖

| 系统 | 方向 | 依赖性质 |
|------|------|----------|
| 回合起始事件与周期任务 | 本系统支撑它 | 在 `briefing` 内生成本周起始输入 |
| 探索与节点派遣 | 本系统支撑它 | 在 `explore` 内消耗 `remaining_days` 并推进周进度 |
| 线索与内容素材库存 | 双向依赖 | 接收探索结果并回传本周新增素材引用 |
| 内容生产链与稿件生成 | 本系统支撑它 | 在 `editorial` 内生成 `article_candidates` |
| 编辑排版与发行策略 | 本系统支撑它 | 在 `editorial` 内冻结 `published_issue` |
| 发刊结算与受众反馈 | 本系统支撑它 | 在 `summary` 内写回结果与下周钩子 |
| 宏观属性与现实偏移 | 双向依赖 | 共享长期门槛并接收结算变化 |
| 菜单与场景导航 | 导航依赖本系统 | 创建或恢复到合法顶层阶段 |

## 调参旋钮

| 参数 | 当前值 | 安全范围 | 提高后的效果 | 降低后的效果 |
|------|--------|----------|--------------|--------------|
| `week_days` | 7 | 5-9 | 派遣更自由、压力更小 | 周节奏更紧、取舍更难 |
| `briefing_task_cap` | 3 | 2-4 | 外部干预更强 | 周起始更易读 |
| `minimum_weekly_opportunities` | 2 | 1-3 | 干周更少，起手更稳 | 更容易出现缺料周 |
| `empty_issue_penalty` | 中 | 低到高 | 发刊完整性更重要 | 玩家更容易硬凑过周 |

## 视觉 / 音频需求

| 事件 | 视觉反馈 | 音频反馈 | 优先级 |
|------|----------|----------|--------|
| 进入 `briefing` | 清晰的简报面板、任务摘要与周标签刷新 | 轻量过渡提示 | 高 |
| `briefing -> explore` | 明确的阶段切换与可行动内容高亮 | 鲜明的确认提示音 | 高 |
| `explore -> editorial` | 强调“本周已收尾”的界面切换与素材摘要 | 中强度切换提示音 | 高 |
| `summary -> briefing` | 标签重置、下周钩子提示与机会刷新 | 结算后回归提示音 | 中 |

## UI 需求

| 信息 | 显示位置 | 更新频率 | 条件 |
|------|----------|----------|------|
| 当前周次与顶层阶段 | 顶部 / 周状态栏 | 顶层阶段切换时 | 始终 |
| 剩余天数 | 顶部 / 周状态栏 | 每次合法派遣后 | `explore` |
| 本周起始事件与任务摘要 | 主内容面板 | `briefing` 生成后与任务状态变化时 | `briefing` / `explore` |
| 本周新增素材数、候选稿件数与已排版槽位数 | 阶段侧栏 | 数据变化时 | `editorial` |
| 结算结果与 `next_week_hooks` 摘要 | 结算面板 | 进入 `summary` 时 | `summary` |

## 验收标准

- [ ] 可以在 Godot 循环中完整游玩从 `briefing` 到下一周 `briefing` 的一周内容。
- [ ] 新周总是先进入 `briefing`，不会直接落在 `explore`。
- [ ] `explore` 阶段不能消耗非法天数，且在 `legal_dispatch_count == 0` 时能安全收周。
- [ ] 周循环不重复保存素材真源，只记录本周新增素材引用。
- [ ] `summary` 总能生成下一周所需的 `next_week_hooks` 或显式空结果。
- [ ] 顶层阶段切换明确、可读，并与下游系统文档一致。

## 开放问题

| 问题 | 负责人 | 截止时间 | 结论 |
|------|--------|----------|------|
| 未来是否支持在 `briefing` 与 `explore` 之间插入中断事件？ | 设计 | 后续 | 待定 |
| 存档 / 读档应优先挂在顶层阶段边界，还是允许深入子状态？ | 技术 | 垂直切片阶段 | 待定 |
| `next_week_hooks` 应该全部显式展示，还是允许部分只作为生成偏置存在？ | 设计 | 后续 | 待定 |
