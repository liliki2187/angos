# ADR-0003：Demo 周状态字段向正式 Weekly Schema 的迁移边界

## 状态
已接受

## 日期
2026-04-09

## 背景

### 问题陈述

`design/gdd/weekly-run-loop.md` 已经把正式周循环定义为 `briefing -> explore -> editorial -> summary`，并明确了顶层周状态字段、长期状态边界和下游系统写入责任。但当前 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 仍保留明显的 demo 命名和流程：

- 新开局与新周直接落在 `explore`
- 顶层字段仍以 `day`、`week_briefing`、`weekly_clues`、`story_pool`、`last_summary` 为主
- `weekly_clues -> story_pool -> settlement` 仍是主链路

如果不先定义迁移边界，接下来的重构很容易退化成“边改边猜”，最终在代码里形成新旧字段并存、真源漂移和 UI 临时适配长期化的问题。

### 约束

- 当前可玩 Godot 场景必须持续可运行，不能为了 schema 迁移做一次性大重写。
- `ADR-0001` 已要求把内容数据、周状态 / 规则与场景表现分离；`ADR-0002` 已要求 UI 只做绑定，不拥有玩法真状态。
- `design/gdd/weekly-run-loop.md` 已经是周循环顶层状态真源，运行时命名必须向它收口。
- `tests/` 当前为空，迁移期的回归保护很弱。
- `FullChainGame.gd` 仍是单体脚本，短期内会存在过渡适配层。
- 当前 `gd_project/scenes/gameplay/full_chain/` 更接近 demo 聚合入口，而不是面向长期管理的正式系统目录。

### 要求

- 在继续拆脚本前，先把正式 weekly schema 设为唯一规范命名。
- 新开局与每个新周都必须先进入 `briefing`。
- 周内容器只保留本周字段和跨周一跳字段，不重复持有长期系统真源。
- 允许短期适配层，但不允许长期双写两套真源。
- 后续最小自动化覆盖必须围绕正式字段和正式阶段流建立，而不是围绕 demo 名称建立。
- 迁移不得被当前临时目录结构绑死；如果原目录妨碍系统所有权收口，应允许在新的运行时目录中落地正式实现。

## 决策

Angus 将采用“先统一正式 schema，再按切片重构代码”的迁移策略。自本 ADR 起，`design/gdd/weekly-run-loop.md` 中的字段名和阶段名是 `FullChainGame.gd` 后续重构的唯一规范命名。

### 核心迁移原则

1. 顶层阶段只允许 `briefing`、`explore`、`editorial`、`summary` 四个值。
2. 新开局和 `summary -> next week` 都必须先进入 `briefing`，不得再直接落入 `explore`。
3. 旧 demo 字段可以在单次重构切片内作为局部适配变量存在，但 canonical 写入点必须立即切到正式字段。
4. UI 允许读取正式字段生成展示文案，但展示文本不是周状态真源。
5. 当正式下游系统尚未抽离完成时，可用“过渡适配容器”承接数据，但容器命名必须体现正式链路，而不是继续扩张 demo 名称。
6. 如果 `full_chain` 这类临时目录阻碍系统边界表达，应优先新建按游戏系统组织的运行时根目录；旧入口最多保留为过渡壳层或兼容跳板。

### 字段迁移表

| 当前 demo 字段 / 概念 | 正式字段 / 概念 | 迁移策略 | 所有权结论 |
|------|------|------|------|
| `week` | `week` | 保留 | 周循环持有 |
| `day` | `remaining_days` | 直接改名，不保留为长期真名 | 周循环持有 |
| `current_phase = explore/editorial/summary` | `current_phase = briefing/explore/editorial/summary` | 扩展枚举并把新周入口改为 `briefing` | 周循环持有 |
| `week_briefing` | `briefing_event_id` + `active_tasks` + `opportunity_ids` | 拆分迁移；展示文本只允许作为 UI 派生数据 | 周起始系统写入，周循环持有引用 |
| `weekly_clues` | `dispatch_result -> material_inventory -> new_material_ids` | 不再把“线索数组”当正式顶层真源；外采结果先进入派遣结果，再映射到素材库存与本周新增引用 | 派遣 / 素材系统写入 |
| `story_pool` | `cognition -> article_candidates` | 旧“故事库”概念退位；正式对外字段统一为 `article_candidates` | 内容生产系统写入 |
| `slot_assignment` | `slot_assignment` | 保留，但只表达版位到稿件的映射 | 排版系统写入 |
| `last_summary` | `settlement_result` | 直接改名，并把展示刷新改为消费正式结算结果 | 结算系统写入 |
| “点击结算后直接更新长期值” | `published_issue -> settlement_preview -> settlement_result` | 在阶段边界上显式化；`published_issue` 成为结算输入 | 排版 / 结算系统协作 |
| `resolved_nodes` | `opportunity_ids` 或区域系统长期状态 | 从周顶层状态移出；是否跨周保留由区域系统决定 | 不再默认为周循环真源 |
| `subscribers`、`macro_stats`、`editorial_profile` | 长期运行状态 | 继续保留，但不得伪装成周内字段 | 长期系统持有 |

### 正式链路约束

迁移后的正式周内主链路定义为：

```text
briefing
  -> dispatch_result
  -> material_inventory
  -> cognition
  -> article_candidates
  -> published_issue
  -> settlement_result
  -> next_week_hooks
```

说明：

- `dispatch_result` 是探索 / 派遣的直接结果层，不等同于可长期持有的素材正文。
- `material_inventory` 是素材真源；周循环只记录 `new_material_ids` 这类本周引用。
- `cognition` 是从素材到稿件候选之间的处理中间层。即使第一版仍在同一脚本内，也应以正式名称出现。
- `published_issue` 是进入结算的冻结快照，不能再由 UI 临时拼读 `story_pool` 替代。

### 过渡适配规则

- 在第一轮迁移中，允许保留少量本地适配函数把旧数据结构翻译到正式字段。
- 这些适配只能存在于单一写路径中，不得形成“旧字段和新字段各自都可被业务写入”的双真源局面。
- 任何为了界面显示而保留的文本、副本或缓存，都必须明确标为派生视图数据，而不是 schema 字段。

### 架构示意

```text
周起始生成 / 派遣 / 内容生产 / 结算
               |
               v
        正式 Week Schema
  - week
  - remaining_days
  - current_phase
  - briefing_event_id
  - active_tasks
  - opportunity_ids
  - new_material_ids
  - article_candidates
  - slot_assignment
  - published_issue
  - settlement_preview
  - settlement_result
  - next_week_hooks
               |
               v
        UI 绑定与展示层
  - briefing 文案
  - 节点列表
  - 候选稿件列表
  - 结算面板
```

### 关键接口

- **周起始 -> 周循环**
  - 生成 `briefing_event_id`
  - 生成 `active_tasks`
  - 生成 `opportunity_ids`
- **探索 / 派遣 -> 周循环**
  - 写入 `dispatch_result`
  - 通过素材系统回写 `new_material_ids`
- **内容生产 / 排版 -> 周循环**
  - 写入 `article_candidates`
  - 写入 `slot_assignment`
  - 冻结 `published_issue`
- **结算 -> 周循环 / 长期状态**
  - 写入 `settlement_preview`
  - 写入 `settlement_result`
  - 写入 `next_week_hooks`
  - 更新长期状态

## 备选方案

### 方案 1：继续沿用 demo 命名，等模块拆完后再统一改名

- **描述**：先做代码拆分，把命名问题留到最后统一处理。
- **优点**：短期少改字段名，表面上更快。
- **缺点**：拆分时会把旧概念继续扩散到新模块，后续更难校正。
- **否决原因**：会把 schema 漂移变成结构化债务。

### 方案 2：先一次性重写完整周循环系统，再迁入正式字段

- **描述**：跳过渐进迁移，直接新写一套正式系统。
- **优点**：理论上最干净。
- **缺点**：风险高，且当前没有测试兜底，不适合单体脚本过渡期。
- **否决原因**：不符合当前迭代节奏和风险承受能力。

### 方案 3：旧字段与新字段长期并存，逐步替换读取方

- **描述**：同时保留两套状态字段，慢慢把调用方切到新名。
- **优点**：短期兼容成本低。
- **缺点**：最容易形成双写、漏改和真假源混淆。
- **否决原因**：与 `ADR-0001` 的真源收口方向冲突。

## 影响

### 正面

- 代码重构将围绕正式 schema 进行，而不是围绕 demo 词汇进行。
- `briefing` 会成为真实顶层阶段，而不是文档里存在、运行时缺失的占位概念。
- 后续自动化覆盖能直接锚定正式字段与阶段流。
- 未来抽离素材库存、内容生产和结算模块时，接口名称可直接复用。

### 负面

- 迁移初期会出现“结构还没完全拆开，但名字已经变了”的短期不适感。
- 需要额外处理一层过渡适配，避免 UI 与旧逻辑同时断裂。

### 风险

- **风险**：下游正式系统尚未抽离，导致正式名称只停留在表面。
  - **缓解**：要求所有适配都以正式字段为唯一写入点，并把旧概念局限在局部转换函数中。
- **风险**：字段重命名导致现有 UI 刷新逻辑大面积回归。
  - **缓解**：按阶段边界切片迁移，优先覆盖 `briefing` 入口、编辑链和结算链。
- **风险**：`briefing_event_id`、`active_tasks`、`opportunity_ids` 在第一版仍是占位数据。
  - **缓解**：允许占位，但必须是显式的正式字段，不得继续由 `week_briefing` 一把兜底。

## 性能影响

- **CPU**：中性；主要是命名和边界迁移，不引入新的热路径。
- **内存**：轻微增加；过渡期适配层会产生少量副本。
- **加载时间**：中性。
- **网络**：无。

## 迁移计划

1. 新增本 ADR，冻结 demo 字段到正式 schema 的映射规则。
2. 先建立按游戏系统组织的正式运行时骨架；如现有 `full_chain` 目录不适合作为正式根，允许在新的 gameplay 系统目录中落地实现。
3. 在正式入口中引入 `briefing` 作为真实顶层阶段，并把新周入口改到 `briefing`。
4. 把周顶层字段切到正式命名：至少完成 `remaining_days`、`article_candidates`、`settlement_result` 与 `published_issue` 的正式写路径。
5. 把 demo 主链从 `weekly_clues -> story_pool -> settlement` 改到正式链路命名，即使中间层暂时仍由同一脚本或过渡壳层托管。
6. 为阶段切换与结算公式补最小自动化覆盖，确保之后再做拆模块时有回归基线。

## 验证标准

- 新开局与每次进入下一周都先落在 `briefing`。
- 周顶层状态中不再把 `day`、`story_pool`、`last_summary` 作为 canonical 真名。
- 编辑链对外暴露 `article_candidates`、`published_issue` 和 `settlement_result`，而不是继续暴露 demo 名称。
- UI 展示文本能够从正式字段派生，但不反向拥有玩法真状态。
- 最小自动化覆盖至少验证阶段流和一条结算结果路径。

## 相关决策

- `ADR-0001`：Godot 周循环状态与数据边界
- `ADR-0002`：Godot UI 场景优先与绑定式脚本规范
- `design/gdd/weekly-run-loop.md`
- `gd_project/scenes/gameplay/full_chain/FullChainGame.gd`
