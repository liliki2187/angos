# Angus 项目结构与协作治理方案

**日期**: 2026-04-04
**适用阶段**: Early Production / Godot MVP 持续迭代期
**目标**: 在不打断当前开发的前提下，建立清晰的目录归属、文档权威层级、角色协作方式和反混乱机制，方便后续使用 OpenSpec 风格流程与仓库内 game-production skills。

## 1. 项目现状判断

当前仓库不是单一形态项目，而是 5 类内容叠加在一起：

1. **Godot 主工程**
   - `project.godot`
   - `scenes/`
   - `Assets/`
   - `addons/`
2. **HTML 历史参考与网页原型**
   - `design/prototypes/html/full-chain-demo/`
   - `design/prototypes/html/`
3. **设计文档体系**
   - `design/gdd/`
   - `design/systems/`
   - `docs/`
4. **AI / 自动化 / 导入工具体系**
   - `skills/`
   - `scripts/`
   - `.github/workflows/`
5. **分发与参考产物**
   - `prototype/`
   - `design/generated-*`
   - `artifacts/`
   - `design/generated-concept-visual/`

这说明仓库已经进入“**可玩原型存在，但治理边界还不稳**”的阶段。优势是素材和知识已经不少，风险是继续推进后会越来越难判断什么才是主线。

## 2. 当前结构的核心问题

### 2.1 权威来源不够单一

- Godot 已经被 ADR 明确为当前 MVP 的唯一运行时主线。
- 但仓库里仍同时存在 `design/prototypes/html/`、旧 `docs/` 设计文档、Godot 场景实现。
- 新同学和 AI 很容易误判“应该改哪里”。

### 2.2 生产协作层过薄

- `production/` 当前只有阶段报告和会话状态，缺少：
  - `stage.txt`
  - `milestones/`
  - `sprints/`
  - `backlog/`
  - `risk-register/`
  - `handoff/`
- 这会直接影响后续很多 skill 的发挥空间。

### 2.3 设计层和实现层还没完全对齐

- `design/gdd/` 已经建立为新的主设计层。
- 但 `docs/` 下仍保留大量旧的设计文档与交接信息，且部分内容与现在的 Godot 主线或 Git 规则并不完全一致。

### 2.4 运行时代码边界还偏原型化

- [`scenes/gameplay/full_chain/FullChainGame.gd`](E:\angus\angus\scenes\gameplay\full_chain\FullChainGame.gd) 同时承载了：
  - 内容定义
  - 周循环状态
  - 结算公式
  - UI 刷新
  - 探索/编辑/总结阶段控制
- 这对 MVP 验证有利，但对多人长期协作不利。

### 2.5 生成物和源文件边界不够清楚

- `prototype/fullchain_demo/` 是脚本生成的分发包，但当前不在忽略范围内，容易污染工作区。
- `scripts/__pycache__/` 这类派生产物也不应继续作为正式仓库内容扩散。
- `design/generated-*` 与 `Assets/ui/imported/` 已经出现“参考产物”和“运行时产物”同时存在的趋势，需要规则化。

## 3. 治理总原则

后续所有目录整理和协作规则，都以这 6 条为准：

1. **Godot 是唯一运行时主线**
   - 当前 MVP 的可实现规则，以 Godot 为准。
   - HTML 仅保留为参考、展示或回溯材料。

2. **一类信息只允许一个权威位置**
   - 玩法规则：`design/gdd/`
   - 技术决策：`docs/architecture/`
   - 团队执行状态：`production/`
   - 运行时资源：`Assets/`
   - 运行时场景/脚本：`scenes/`

3. **`design/` 不直接承担运行时主资源职责**
   - `design/` 用于设计、参考、视觉探索、HTML 原型和分析材料。
   - 真正进入游戏的资产必须进入 `Assets/` 或明确的导入链。

4. **所有生成物必须能追溯回源文件或脚本**
   - 任何导出包、预览图、打包目录都必须有来源说明。
   - 能忽略的生成物就忽略，不要让它们成为“看起来像源码”的东西。

5. **任何新功能都要有 spec / GDD / ADR 中至少一种前置说明**
   - 小改动至少要能指向已有 GDD。
   - 新机制要么有 spec，要么有 GDD，要么有 ADR，不允许只靠聊天记录驱动。

6. **主分支始终保持可读、可跑、可交接**
   - `main` 上不堆个人临时实验。
   - 任何临时产物要么进入 `design/` 的明确实验区，要么进入忽略目录。

## 4. 建议的目标目录职责

以下不是要求立刻大迁移，而是未来 2 到 4 周内逐步收敛到的目标。

### 4.1 运行时主线

```text
project.godot
addons/
scenes/
Assets/
scripts/
```

- `scenes/`: Godot 场景与直接挂接的 GDScript
- `Assets/`: 会被游戏加载或经过导入链进入游戏的资源
- `scripts/`: 构建、打包、导入、自动化脚本
- `addons/`: 引擎插件

### 4.2 设计与跨职能设计资产

```text
design/
  gdd/
  systems/
  diagrams/
  references/
  prototypes/
  ui/
  art-direction/
```

建议逐步把现有内容收敛为：

- `design/gdd/`: 当前生效的玩法设计文档
- `design/systems/`: 系统分析、推导、草稿、补充说明
- `design/references/`: 美术/视觉/题材参考
- `design/prototypes/`: HTML 或其他非运行时实验原型
- `design/ui/`: GUI 规范、高保真设计稿、组件说明
- `design/art-direction/`: 美术风格规范、视觉语言、主题方向

### 4.3 技术与项目说明

```text
docs/
  architecture/
  technical/
  onboarding/
  dev-logs/
  tools/
```

- `docs/architecture/`: ADR、架构边界、模块图
- `docs/technical/`: 工具链、CI、导入流程、工程说明
- `docs/onboarding/`: 新同学、新 AI 的上手文档
- `docs/dev-logs/`: 日期型开发日志
- `docs/tools/`: 特定工具使用说明

### 4.4 生产协作层

```text
production/
  stage.txt
  milestones/
  sprints/
  backlog/
  risk-register/
  handoff/
  roles/
  session-state/
```

这一层是以后 OpenSpec 风格流程和多数 production skills 的工作台。

### 4.5 规格驱动层

```text
specs/
  <feature-slug>/
    spec.md
    tasks.md
    handoff.md
```

这个目录建议新增在仓库根部，而不是塞进 `docs/`。

原因：

- 便于未来接 OpenSpec 或类似 spec-driven 工具
- 便于跨职能围绕单个功能协作
- 便于把“需求 -> 设计 -> 实现 -> 验收”放进同一个 feature packet

## 5. 当前仓库的“来源权威”划分

在大迁移前，先按下面的认知执行，能马上降低混乱。

| 领域 | 当前权威位置 | 非权威但可参考 |
|------|--------------|----------------|
| Godot 运行时行为 | `scenes/` | `design/prototypes/html/` |
| 核心玩法设计 | `design/gdd/` | `design/systems/`、`docs/*.md` |
| 技术架构决策 | `docs/architecture/` | 聊天记录、dev log |
| 团队执行状态 | `production/` | `docs/plans/` |
| UI 运行时资源 | `Assets/ui/` + `scenes/ui/` | `design/generated-*`、`design/prototypes/html/` |
| 美术参考 | `design/` | 飞书聊天记录、外部临时图片 |
| 分发体验包 | `prototype/` 或未来 release 目录 | 根目录源码 |

## 6. 四类同学的目录边界

### 6.1 策划

主责任目录：

- `design/gdd/`
- `design/systems/`
- `specs/`
- `production/backlog/`
- `production/milestones/`

规则：

- 新功能先写 `specs/<feature>/spec.md` 或补充到 `design/gdd/`
- 不直接把聊天内容当需求源
- 对程序的需求必须带验收条件

### 6.2 程序

主责任目录：

- `scenes/`
- `scripts/`
- `docs/architecture/`
- `docs/technical/`
- `.github/`

规则：

- 任何实现都必须能指向某个 GDD、spec 或 ADR
- 新技术边界先写 ADR，再重构
- 不把设计结论长期埋在脚本常量里不落文档

### 6.3 美术

主责任目录：

- `design/references/`
- `design/art-direction/`
- `Assets/art-source/` 或未来明确的 source 目录
- `Assets/characters/`
- `Assets/environments/`

规则：

- 参考图和正式资源分开
- 所有日期型参考归档都要有 README
- 进入游戏的资源必须有清晰命名与版本说明

### 6.4 GUI

主责任目录：

- `design/ui/`
- `Assets/ui/`
- `scenes/ui/`
- `docs/tools/psd-ui-import.md`

规则：

- 高保真稿、源 PSD、导出 PNG、Godot 场景要形成链路
- `design/ui/` 放规范与方案
- `Assets/ui/` 放导入源和运行时资源
- `scenes/ui/` 放实际游戏中的 UI 场景

## 7. 推荐的协作工作流

### 7.1 新功能标准流程

1. 策划在 `specs/<feature>/spec.md` 写目标、范围、验收条件
2. 若涉及玩法规则，补充或更新 `design/gdd/`
3. 若涉及技术边界变化，程序写 `docs/architecture/adr-xxxx-*.md`
4. GUI / 美术分别补 `design/ui/` 与 `design/references/`
5. 程序在 Godot 主线实现
6. 验收后把执行结果写回 `specs/<feature>/handoff.md`
7. 必要时再生成 `prototype/` 或 release 体验包

### 7.2 每周固定同步

每周至少维护 4 项内容：

1. `production/session-state/active.md`
2. 当前 sprint 文档
3. 当前 backlog
4. 相关 spec 的状态

### 7.3 适合这个项目的 skill 使用方式

- 策划起草新功能：`brainstorm` / `map-systems` / `sprint-plan`
- 程序落地前整理边界：`architecture-decision` / `reverse-document`
- GUI 落资源：`team-ui` / `psd-to-godot-ui`
- 美术与参考筛选：`art-reference-picker` / `asset-audit`
- 里程碑前统一检查：`milestone-review` / `gate-check`

## 8. 分阶段实施计划

## Phase 0：先立规矩，不先大迁移

目标：让团队从今天开始按统一规则协作。

本阶段应完成：

1. 建立本方案作为结构治理依据
2. 补齐 `docs/technical-preferences.md`
3. 补齐 `production/` 基本骨架
4. 统一 Git 协作规则，只保留一份权威说法
5. 明确 `prototype/` 是生成分发包还是正式版本目录

完成标准：

- 新同学能在 10 分钟内知道“应该看哪里、改哪里、不要碰哪里”

## Phase 1：让目录开始表达边界

目标：不重写项目，但让目录本身开始说人话。

本阶段建议动作：

1. 把 `design/prototypes/html/`、`design/generated-*`、`design/original-art-reference/` 收敛到更明确的子分类
2. 给 `Assets/` 区分 `ui`、`characters`、`environment`、`runtime-imports`
3. 给 `scenes/` 区分 `meta`、`gameplay`、`ui`、`dev`
4. 给 `scripts/` 区分 `git`、`import`、`prototypes`、`release`、`render`、`share`、`setup`

完成标准：

- 新文件不再继续无规则散落在顶层和现有大杂烩目录里

## Phase 2：让运行时代码脱离原型态

目标：减轻单文件负担，让多人能并行。

本阶段建议动作：

1. 从 [`scenes/gameplay/full_chain/FullChainGame.gd`](E:\angus\angus\scenes\gameplay\full_chain\FullChainGame.gd) 抽离：
   - 周状态
   - 内容定义
   - 结算公式
   - UI 渲染
2. 建立内容配置入口
3. 为事件检定与结算公式补最小自动化测试

完成标准：

- 程序、美术、GUI 不需要同时卡在同一个超大脚本上

## Phase 3：建立长期反混乱机制

目标：项目往前走时，不再靠记忆和聊天维持秩序。

本阶段建议动作：

1. 所有新功能进入 `specs/`
2. 每个 milestone 有清晰的 sprint、风险和验收记录
3. 每个大技术决策都有 ADR
4. 每月清一次历史参考和失效文档
5. 所有导出包、生成图、临时实验统一归档或忽略

完成标准：

- 仓库里的“正在用”“仅参考”“已归档”一眼能区分

## 9. 必须尽快补的三份基础文档

从“方便 skill 工作”和“方便协作”两个角度看，最值得优先补的是：

1. `docs/technical-preferences.md`
   - 统一 Godot 版本、命名规则、测试方式、禁用模式
2. `production/stage.txt`
   - 明确项目阶段，减少 skill 对当前阶段的误判
3. 第一个 `production/sprints/` sprint 文档
   - 把“当前真正在做什么”固定下来

## 10. 需要立即避免的坏习惯

1. 不要继续把新入口文件直接扔到仓库根目录
2. 不要让生成包和源码并列地位不清
3. 不要让旧 `docs/` 文档和新 `design/gdd/` 同时扮演主设计层
4. 不要把临时实验只留在聊天和飞书里
5. 不要再让 Git 规则在多个文档里互相冲突

## 11. 对当前项目的结论

这个项目**适合采用“轻量 spec 驱动 + GDD 主设计层 + ADR 技术边界 + production 执行层”**的治理方式，而不适合继续靠“原型文件 + 交接聊天 + 分散计划文档”向前推。

原因很直接：

- 你们已经不是 1 人纯实验，而是多职能协作
- 项目已经同时存在玩法、UI、美术、工具、分发、AI 技能体系
- 如果现在不先立边界，后面每多一个人、每多一个系统，混乱会成倍增长

因此，**最合适的不是马上大重构目录，而是先建立目录职责、权威层级、spec 流程和 production 工作台，再做分阶段收敛**。
