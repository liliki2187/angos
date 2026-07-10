# Angus Workflow Harness 与 Loop 渐进方案

> 状态：2026-06-29 起作为轻量执行入口。先人工使用模板和 gate 表，经过数次真实任务验证后，再决定是否脚本化。
> 目的：把错题本从“事后提醒”推进为“交付前自检”，同时避免小任务被重流程拖慢。
> 真源分工（2026-07-08 起）：本文件负责风险分级、回复格式与 loop 生命周期；产物类型与阶段跳转的机器可读真源是 [`workflow-gates.yml`](./workflow-gates.yml)；资产化 UI 操作细则是 `docs/onboarding/assetized-ui-production-chain.md`；几何 / 正交 / 文字安全统一阈值是 [`ui-geometry-and-text-safety-gates.md`](./ui-geometry-and-text-safety-gates.md)。新增或修改 gate 必须同时落 YAML 与对应文档，只落一处视为未生效。

## 1. 核心原则

- **先提醒，再记录，再拦截**：初期只用 Router Card 和 Delivery Manifest；不要一开始就上 CI、强制脚本或全 agent 大会审。
- **轻任务轻过，风险任务硬过**：tiny / normal 任务只做最小自检；risky / production 任务才进入硬 gate。
- **产物先分类，再交付**：任何截图、风格稿、运行图、逻辑烟测都必须说明它能证明什么、不能证明什么。
- **loop 前移**：把“用户指出后复盘”提前到“交付前自我降级 / 返工 / 熔断”。
- **父级 Codex 做 DRI**：subagent 提供证据链，父级负责合并冲突、限定范围、决定采纳或交给用户裁决。
- **先选语气，再给结构**：普通解释、讨论、完成汇报和轻量问答用自然语言；只有 Router、Manifest、Loop Log、hard gate、是否通过判断、卡住/返工/需要裁决时，第一屏才给三行决策条：`结论 / 影响 / 下一步`。决策条是降低判断成本的急救牌，不是所有回复的模板。

## 1.1 回复模式选择

先判断本轮回复属于哪种模式，再选择格式：

| 模式 | 适用场景 | 第一屏 |
| --- | --- | --- |
| `direct_answer` | 普通解释、讨论、回答“怎么看” | 自然段落，不用决策条 |
| `completion_report` | 已完成小改、跑完测试、交付结果 | 自然语言说明改了什么，必要时补验证 |
| `progress_update` | 工作中短更新 | 1-2 句自然语言 |
| `workflow_gate` | Router / Manifest / 是否通过 / 交付验收 | 三行决策条 |
| `loop_log` | 用户纠错、复盘、返工、防复发 | 三行决策条 + 详情 |
| `blocked_or裁决` | 卡住、需要用户判断、不能继续 | 三行决策条 |

禁止把 `workflow_gate` 的格式泛化到所有回复。可读性第一原则是：用户当前只需要聊天，就像人一样说；用户需要判断，就给决策条。

## 1.2 决策条契约

在 `workflow_gate`、`loop_log`、`blocked_or裁决` 模式下，必须先给 `决策条 / Decision Strip`。它不是摘要，也不是 Router Card 的字段转写，而是给用户扫一眼做判断的第一屏。除非用户明确要求只要原始表格，否则按“三层输出”：

### 第一层：决策条

固定三行，不能扩成 checklist。每行只回答一个决策问题，主句必须用自然语言；`no_text_style_draft`、`filled_state_text_mock`、`production_candidate` 之类标签只能放在后面的详情或术语层。

1. **结论**：通过 / 部分通过 / 不通过 / 需要你裁决。
2. **影响**：这意味着可以继续什么、会挡住什么，或者对用户有什么风险。
3. **下一步**：下一轮具体做什么；不是原则，不是长期规范。

推荐格式：

```md
**结论**：……
**影响**：……
**下一步**：……
```

### 第二层：详情 / Human Brief

决策条之后，如任务需要，再用 4-6 行解释“做了什么、卡在哪里、为什么、怎么验证、本轮不要做什么”。这层仍然要用人话，但它已经不是第一屏。

推荐格式：

```md
**做了什么**：……
**问题在哪**：……
**为什么**：……
**验证方式**：……
**本轮不做**：……
```

### 第三层：术语清单

详情之后，再列 Router Card / Delivery Manifest / Loop Log / gate checklist。术语清单用于审计、复盘和下一轮执行，不能代替结论。至少把以下几组关系拆清：

- **本轮交付物类型**：这次回复本身交付了什么，例如 router_card / manifest / design_note / implementation。
- **被路由对象类型**：被判断的图、稿、代码或文档实际处在哪个阶段。
- **允许下一步**：从当前阶段合法进入什么。
- **禁止跳到**：哪些动作现在还不能做。
- **证据路径**：关键文档、截图、测试或复审来源。

禁止做法：

- 普通解释或完成汇报也套三行决策条。
- 用 20 行 checklist 代替结论。
- 用 6 行 Human Brief 代替 3 行决策条。
- 把“应做”写成“已做”。
- 只说“按流程不通过”，但不解释卡在哪一层。
- 只给 agent / gate 名字，不告诉用户下一步该怎么推进。
- 在第一屏堆 `no_text_style_draft -> filled_state_text_mock -> atlas`，但不解释这些标签对用户意味着什么。
- 在 Router Card 里混淆“本轮交付物”和“被路由对象”。

示例：

```md
**结论**：部分通过，能继续做带真实文字的效果验证，但不能直接进 Godot 切图。
**影响**：现在直接切图会得到好看的空底图，真实 UI 一放字可能挤、乱或不融合。
**下一步**：先选一个真实游戏状态，做一张带地区名、任务、按钮和状态的有字 mock。

详情：我只判断了下一步路线，没有实现、切图或生成运行截图；本轮不要进 atlas、manifest、Godot runtime 或 production candidate。

术语版：被路由对象=`no_text_style_draft`；允许下一步=`lightweight_content_contract -> filled_state_text_mock`；禁止=`atlas / manifest / runtime_background / production_candidate`。
```

## 2. 从轻到重的四层流程

### Level 0: Tiny Task

适用：

- typo、路径修正、明显 bug、单行文案、非可见重排。
- 不涉及设计真源、UI 结构、截图验收、数值公式或生图。

执行：

- 不强制 Router Card。
- 完成后说明改了什么，必要时跑最小测试。
- 若出现用户纠错，再补 Loop Log。

### Level 1: Router Card

适用：

- normal 以上任务。
- 任何可能跨 UI / 玩法 / 美术 / 文档 / 代码边界的任务。

必须回答：

- 本轮交付物是什么，被路由对象是什么。
- 任务类型、风险等级、当前阶段、目标载体。
- 本轮必读真源、若进入下一步再读的真源、必调 agent。
- 本轮只验证什么，本轮明确不做什么。

模板见 [`templates/router-card.md`](./templates/router-card.md)。

**交付前三问（2026-07-08 起，normal 以上任务交付前必过）**：即使本轮不需要完整 Delivery Manifest，交付前也必须自问三个问题——它们按错题家族频率反推，能覆盖错题本约七成条目：

1. **产物诚实**：我声称的产物类型 / 完成度和实际一致吗？工程验证（能跑、没越界、有截图文件）有没有被我说成体验 / 视觉验证？（对应家族 F1）
2. **范围一致**：我的改动范围和用户要求的范围一致吗？有没有把局部修正顺手扩成整体重做？（对应家族 F3）
3. **同类扫描**：如果本轮在修用户指出的问题，同页同语法的同类组件 / 位置我扫过了吗？（对应家族 F4）

任一答案含糊，先补检查再交付；tiny 任务可跳过，但出现用户纠错时按 Loop Log 补。

### Level 2: Delivery Manifest

适用：

- 交付任何可见图、运行截图、设计稿、风格稿、测试截图、逻辑烟测截图。
- 交付任何“下一步可以进入生产”的判断。

必须回答：

- 决策条：结论、影响、下一步。
- 详情 / Human Brief：做了什么、卡在哪里、为什么不能跳过、下一步怎么验证、本轮不要做什么。
- 产物类型。
- 它能证明什么、不能证明什么。
- 已过 gate、未过 gate、允许的下一步、禁止跳到的下一步。

模板见 [`templates/delivery-manifest.md`](./templates/delivery-manifest.md)。

试行检查脚本（2026-07-08 起，trial）：交付 manifest / 评审文档前可运行

```powershell
python scripts/check_delivery_manifest.py <manifest或评审文档路径>
```

它检查：产物类型标签是否声明（对照 `workflow-gates.yml` artifact_types）；声称"几何 / 正交通过"时是否附裁切与参考线证据；声称"本轮交付完成"时是否更新资产线 STATUS；声称"生产候选 / 标杆 / 真源候选"时是否提及复审。脚本只做文本存在性检查，不替代真实 QA。

### Level 3: Workflow Lab

适用：

- 新流程、新 gate、新自动检查脚本上线前。
- 重复错题需要从文档规则升级为检查器之前。

建议实验：

1. **产物类型判定实验**：抽 10 张近期图，判定它们是 `logic_smoke`、`safe_zone_capacity_validation`、`filled_state_text_mock`、`runtime_state_preview` 还是 `production_candidate`。
2. **阶段跳转实验**：给定当前阶段，要求输出合法下一步；重点检查是否从无字风格稿跳到 `atlas / manifest / 切图`。
3. **agent 调用预算实验**：同一任务按 tiny / normal / risky / production 跑路由，确认没有小题大做。
4. **截图验收实验**：用整屏、局部裁切、反向读法检查旧图，确认 gate 能发现旧错。
5. **沉淀分层实验**：用户纠错后判断进 casebook、design-decisions、onboarding hard rule 还是暂不沉淀。

模板见 [`templates/workflow-lab-checklist.md`](./templates/workflow-lab-checklist.md)。

### Level 4: Hard Gate

仅用于 risky / production 任务：

- 资产化 UI。
- 生图 / 风格稿 / 生产标杆候选。
- 世界地图、地区界面、派遣签批台、报道主板等主流程 UI。
- 数值公式、概率、结算、状态机。
- GDD 真源修改。
- 影响多个系统的玩法或架构变化。

通用 hard gate：

- 决策条 / Decision Strip 已先给出，且结论不是藏在清单里。
- Router Card 已填。
- 必读真源已读，或说明为什么不需要。
- 必调 agent 已调用，或说明例外。
- 当前产物类型已声明。
- 截图 / 测试 / 审查对象与目标阶段一致。
- 关键局部已裁切或等价检查。
- 至少写出一个反向读法，并检查是否仍成立。
- 文档 / 实现 drift 已判断。
- 用户采纳项是否需要沉淀已判断。

资产化 UI 追加 gate（完整清单以 `workflow-gates.yml` 的 `hard_gates.assetized_ui` 为准）：

- 功能分区表、信息容量表、最长文案 / 极端状态。
- `component_aspect_taxonomy`：先按功能角色分类形状家族，方形默认只属于 icon / badge。
- **整页合同板**：同页全部主 class 一轮完成量测、归一、整屏回填、文案压力，一次用户裁决；合同必含 `reference_resolution / runtime_resolution / export_scale`，字段分级 frozen / provisional。
- **纵向切片**：首批合同锁定后，先用 1 个 class 打通 素材 → gate → 切图 → Godot → 截图，再批量生产素材。
- `content_rects / no_text_rects / hit_rects`。
- `ui_geometry_gate`：几何正交证据，阈值与触发条件见 [`ui-geometry-and-text-safety-gates.md`](./ui-geometry-and-text-safety-gates.md)。
- 真实内容整屏预览（filled mock 或分层回填预览）+ UI / UX / 像素艺术复审。
- runtime screenshot 与目标稿对照。
- 资产线 `STATUS.md` 每轮更新；评审中文落盘；证据脚本不得引用 `tmp/`。
- 未通过前不得进入 `atlas / manifest / production_candidate`。

Git 多远端 / 跨端交接使用专用 gate：只要用户要求“同步另一端”“无缝衔接”或推送多个远端，就按 [`../../skills/git-cloud-submit/SKILL.md`](../../skills/git-cloud-submit/SKILL.md) 执行 handoff completeness 检查。每个未入 Git 的相关路径必须归为 `ACTIVE / REPRODUCIBLE / EXTERNALIZED / SECRET / DISPOSABLE / LOCAL_ONLY_REQUIRED`；存在未分类或仅存本机的必需内容时阻断“无缝交接完成”声明。机器可读清单见 `workflow-gates.yml` 的 `hard_gates.handoff_completeness`。

几何正交一票否决：自动触发条件、1 度阈值、双通行证（`text_geometry_pass` + `art_shell_geometry_pass`）、最低证据（3 个核心面裁切 + 参考线 + 逐项判定）统一见 [`ui-geometry-and-text-safety-gates.md`](./ui-geometry-and-text-safety-gates.md)，本文件不再维护副本。核心口径：没有几何证据只能写“几何未验证”，不能写“通过”；任一核心信息面倾斜即降级为灵感图 / 偏差案例。

## 3. 风险等级

| 等级 | 典型任务 | 默认动作 | agent 策略 |
| --- | --- | --- | --- |
| `tiny` | typo、单点 bug、非可见小修 | 最小测试 | 不默认调用 |
| `normal` | 普通 UI 文案、局部布局、文档补充、代码小改 | Router Card + 必要验证 | 只调直接相关 agent |
| `risky` | 资产化 UI、生图、主流程 UI、数值 / 状态机、跨系统玩法 | Router Card + Delivery Manifest + hard gate | 按任务链调用，父级合并冲突 |
| `production` | 生产候选、真源候选、主干落地、GDD / 配表正式同步 | 完整 hard gate + 截图 / 测试 / 文档同步 | 必调相关 agent，保留判断证据 |
| `experimental` | 明确隔离的探索页、候选图、方法实验 | 明确停止条件和不进入真源 | 只调能验证窄问题的 agent |

## 4. 产物类型表

| 产物类型 | 可以证明 | 不能声称 |
| --- | --- | --- |
| `structure_wireframe` | 功能分区和容量是否大致成立 | 美术通过、可切图、生产候选 |
| `problem_overlay` | 当前问题层和目标层是否对齐 | 真实界面效果 |
| `interaction_fix_sketch` | 操作关系、热区、局部纠偏 | 高保真真实内容风格稿 |
| `safe_zone_capacity_validation` | 文字容量、矩形、边界压力 | 图文融合、正式 UI 通过 |
| `logic_smoke` | P0 条件、状态机、阻断是否触发 | 视觉验收、目标界面落地 |
| `visual_style_reference` | 风格、材质、色彩方向潜力 | 功能承载、动态文字可落地 |
| `color_locked_style_draft` | 色彩合同阶段通过 | 资产拆分、生产候选 |
| `no_text_style_draft` | 无字构图、材质、可写区方向 | 真实内容截图、runtime 底图 |
| `filled_state_text_mock` | 图文融合、信息密度、字体气质、商业截图感 | 生产底图、manifest 源 |
| `no_text_asset_master` | 可拆组件、动态文字空位 | 最终玩家截图 |
| `runtime_skeleton` | 动态字段和状态能挂到分区上 | 最终视觉效果 |
| `runtime_state_preview` | 少数真实运行状态 | 全状态生产通过 |
| `production_candidate` | 无字资产、动态层、状态矩阵、截图验收基本齐备 | 未经复审的生产真源 |

### 4.1 Godot Agent Smoke Gate

当任务改动 Godot 脚本、场景、节点层级、autoload、preload 路径、周循环阶段、世界地图、地区任务、派遣、排版或发刊流程时，交付前必须跑 Godot 体检。

执行入口：

```powershell
.\scripts\run_godot_agent_smoke.ps1
```

失败处理入口：若体检失败，先查 [`godot-debug-skill-v0.md`](./godot-debug-skill-v0.md)，按“报错长相 -> 人话解释 -> 常见原因 -> 修法 -> 验证命令”归类，不要直接凭直觉大改。

如果用户看到的是 Windows `Godot_*.exe - 应用程序错误`、编辑器 / GUI 崩溃、或需要验证某个具体 Godot exe 能否启动，不要用 headless smoke 冒充覆盖。此时追加运行 GUI / 指定 exe 检查：

```powershell
.\scripts\run_godot_gui_startup_check.ps1 -GodotPath "D:\angos\tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64.exe"
```

体检分两层：

1. `gda script validate`：抓 GDScript 语法 / 编译错误。必须解析 JSON 里的 `valid` 字段，不能只看进程退出码。
2. Godot headless smoke：后台加载真实 `WeeklyRunGame.tscn`，推进到探索、区域、派遣的最小真实路径，用来抓节点路径丢失、场景层级改坏、autoload / preload 运行期错误和 null 调用。

通过条件：

- 所有被检查的 `.gd` 文件返回 `valid: true`。
- `res://tests/gda_angus_weekly_run_smoke.gd` 以退出码 `0` 结束。

边界：

- 这是运行体检，不是视觉验收。它不能证明 UI 好看、资产化 UI 通过、所有状态都覆盖或玩法平衡正确。
- 只改 Markdown、AI 日报、纯 HTML 原型或未落 Godot 的设计讨论时，不强制跑。

## 5. Loop 生命周期

每轮按 7 步走：

1. **Route**：判断任务类型、风险等级、当前阶段。
2. **Scope**：声明本轮只验证什么。
3. **Build**：做最小产物，不扩大到未确认范围。
4. **Inspect**：截图、测试、subagent 复审或人工检查。
5. **Classify**：判定产物类型和通过等级。
6. **Decide**：继续、降级、返工、停止、或交给用户裁决。
7. **Sediment**：只在必要时沉淀错题、采纳记录或规则；写入前必须先执行沉淀去重律（见 §7）。

Loop 回馈必须先回答：

- **这次纠错暴露的本质问题是什么？**
- **当前产物要降级、返工、继续，还是停止？**
- **下一次怎样避免复发？**

### 5.1 Loop Log 自动触发

用户不需要说 `Loop Log` 这个词。只要出现以下任一情况，父级 Codex 必须把回复模式切到 `loop_log`，不能只道歉或普通解释：

- 用户明确指出错误：例如“这次错在……”“哪里错了”“你误判了”“你跳步了”“你漏调 / 乱调 agent”。
- 用户要求复盘或防复发：例如“复盘一下”“以后怎么避免”“防复发”“这个要进错题本”。
- 用户要求停止落地：例如“先别落地”“不要继续”“不改文件”“只复盘”。
- 用户指出 workflow 失效：例如“没触发 gate”“workflow 没跑完整”“没有按流程”。
- 父级自检发现上一轮交付声明要撤回：例如产物类型冒名、阶段跳转错误、缺必需证据、缺必调 agent、普通解释误套模板、用户要求不实现但已经实现。

触发后最低输出：

```md
结论：本轮哪里错、当前继续 / 降级 / 返工 / 停止。
影响：这个错会挡住什么，或为什么不能继续按原结果推进。
下一步：本轮只复盘 / 降级 / 补证据 / 转 eval case / 更新 gate。

触发来源：用户反馈 / 自检失败 / agent 冲突 / 测试失败 / 截图验收失败。
原始问题：用户指出或自检发现的具体错误。
失败归因：路由、阶段、产物类型、证据、agent、可读性、实现或文档 drift 中哪一类。
复发判定：新错误 / 某家族第 N 次复发（先查 `docs/onboarding/ai-collaboration-guidance.md` §7.0 错误家族索引）。
本轮处理：继续 / 降级 / 返工 / 停止 / 交给用户裁决。
复发保护：下次同类任务开工前和交付前必须检查什么。
沉淀判断：不沉淀 / casebook / design-decisions / onboarding hard rule / eval case / gate 更新；复发时受 §5.2 升级律约束。
```

禁止做法：

- 只说“你说得对，我错了”，但不写失败归因和本轮处理。
- 只写未来规则，不处理当前产物应该降级、返工还是停止。
- 用户说“不改文件 / 只复盘”时还去改文件。
- 可迁移错误不判断是否进错题本、eval case 或 gate。
- 不做复发判定，把老家族的换皮化身当成全新错误单独立规。

### 5.2 二次复发升级律（2026-07-08 起，硬规则）

2026-07-08 错题本复盘发现：约 70 条错题可归并为 5 个反复发作的错误家族，复发的共同根因是**修复写在文档规则层，而错误发生在交付放行层**——文档规则的实际约束半衰期只有几周，只有升级成 checklist、gate 自动触发或校验脚本的规则才真正止血（正交家族五轮才走完这个楼梯，实验页家族因检查廉价一次就停）。因此：

- Loop Log 的失败归因必须先做**复发判定**：查 `ai-collaboration-guidance.md` §7.0 错误家族索引，判断本次是新错误还是已知家族的换皮化身；是复发则更新该家族的次数与日期。
- **同族错误第二次复发时，沉淀判断禁止再补一条文档规则了事**，必须把防线升级一层，升级阶梯为：`文档规则 -> 交付前 checklist 项 -> workflow-gates.yml gate（自动触发）-> 校验脚本`。已在脚本层仍复发的，说明检查本身有漏洞，修检查而不是加规则。
- 升级出的新 gate / 脚本按 §6.1 gate 生命周期标 trial，走正常转正与合并审查。
- 新家族登记门槛：出现 2 条本质相同的错题即在 §7.0 登记为新家族，不等第 3 次。

## 6. 熔断与防僵化

- 小任务不得自动升级成多 agent 大会审。
- 同时最多比较 2-3 个方案。
- 一轮只验证一个核心问题，但**同页同类工作必须合并成板**：同一页面的组件合同、同类裁决、同类小归一必须合并成一次板级交付和一次用户裁决，不得逐组件开轮（见 `assetized-ui-production-chain.md` §0.1 批处理原则）。
- 连续两轮同类失败，停止继续生成，回到上游定义或请用户裁决（细则见 §6.2 止损规则）。
- subagent 冲突时，父级不能把建议全部堆进方案；必须说明冲突、成本和推荐取舍。
- checklist 通过不等于体验通过；交付前必须检查反向读法。
- 未经用户明确采纳，不写入顶层 GDD 真源。

### 6.1 Gate 生命周期（2026-07-08 起）

防止 gate 只增不减、每轮固定成本单调上涨：

- 新 gate 默认标 **trial（试行）**，写明触发范围；存活满一条完整资产线或两周后转正。
- 每完成一条资产线（或每两周），在 Workflow Lab 做一次 **gate 合并审查**：合并重复项、标注被取代项、收窄过宽触发条件、退役长期没有拦到问题的 gate。
- gate 的新增 / 修改 / 退役必须同时落 `workflow-gates.yml` 与所属文档，只落一处视为未生效。
- Loop Log 的沉淀判断中，“新增 gate”不是默认选项：能并入既有 gate 的并入，能用轻规则覆盖的不升级为 hard gate。

### 6.2 止损规则（2026-07-09 起，硬规则）

来源：WMW 左卡资产线复盘——同一条 18px 窗口错位缺陷，被"残带→透明洞→程序色带"连续三轮补丁掩盖，每轮都合规走完流程，没人问方法对不对。

- **触发判定**：同类缺陷按交付 manifest 中的 gate / 缺陷类别判定；同类缺陷连续 **2 轮**未真正修复（含"换一种补丁掩盖"），即触发止损。复发计数记入资产线 `STATUS.md`。
- **触发后禁止**：继续做任何修补式尝试（盖、擦、填、调参数再试一次）。
- **触发后必须产出**（固定四段）：
  1. 根因：缺陷的结构性来源，而不是表层症状；
  2. 已试方案：列出各轮补丁与失败方式；
  3. 结构性替代：至少 1 个改变问题分解方式的方案（如换分层结构、换母版策略），说明代价；
  4. 待裁决问题：交用户决定走哪条。
- **判据冻结**（同源硬规则）：一轮执行内 gate 判据不得放宽或改口径；发现判据本身有问题（阈值无依据、判定式跨样本失效）→ 停下上报，判据修订必须记录在 manifest 与规程文档，禁止"改到能过为止"。执行中发现素材与合同 / 规程矛盾同样停下上报，禁止打补丁绕过。
- 已验证有效案例：左卡 v1.0/v1.1 规程执行中，执行方两次在 gate E 正确停止并交回裁决，单轮止损，未再制造下游假修复。

### 6.3 Brief / 对白双栏制（2026-07-09 起，硬规则）

给执行方（人或 AI）的 brief、对白、规程，凡包含几何值、判定式、阈值、容差，必须区分两栏：

- **已实测事实**：附证据指针（探针输出、QA 图、manifest 字段）；
- **待验证假设**：附验证步骤，执行方开工第一步就是跑探针验证，验证不过立即停下上报，不得带着坏假设往下游制造错误。

背景教训：v1.0 规程把"单帧调参的判定式"当事实冻结下发，执行方忠实执行撞墙；传闻几何值（"18px 残带到 x408"）层层转述五轮，一次实测即推翻。**判定式和容差本身也是假设**，写 brief 的人（包括父级 Codex 自己）必须声明校准范围。

## 7. 何时更新哪些文档

| 情况 | 写入位置 |
| --- | --- |
| 单次可迁移经验 | 对应 `skills/<skill>/references/casebook/` |
| 重复出现并可操作的模式 | 对应 skill `references/patterns.md` 或 onboarding 方法文档 |
| 用户明确采纳 / 待定 / 撤回 | `docs/设计采纳记录.md` + `docs/design-decisions/` 对应分册 |
| 影响所有任务安全或截图交付 | `AGENTS.md` 或 `docs/onboarding/*` |
| 正式玩法 / 规则 / 常量 | `design/gdd/` 对应真源 |

### 7.1 沉淀去重律（2026-07-08 起，硬规则）

同一条经验 / 规则只允许一个**主承载位**（全文），其他位置只准短引用 + 链接。这是为了掐断"guidance + guidelines + design-decisions 三连写"惯性——同一规则全文落三处，改一处漏两处，漂移只是时间问题（A162 返工的直接起因就是文档漂移）。

写入前必须执行：

1. **先查重**：用 `rg` 搜索关键词，确认该经验是否已有承载位。
2. **命中就更新原条目**：在原条目末尾追加修订时间与新表述，不新开日期补丁、不在别处重写全文。
3. **未命中才选主承载位**：按上表选一处写全文；采纳记录条目负责记录"用户决策"，规则细则归 onboarding / skill / gate 文档，两者互相链接而不是互相复制。
4. **顶层文档只留判断器**：`AGENTS.md` 和 guidance 类文档里只写"什么情况该警觉 + 详情在哪"，不复制执行细则。

禁止做法：

- 收到强纠偏后在 guidance、guidelines、design-decisions 各写一遍全文。
- 在必读文档尾部追加日期补丁段落（`## YYYY-MM-DD 补充：…`）；应归并进对应主题章节，变更史进 changelog 附录。
- 用"多写几处保险"替代"更新主承载位"。

## 8. 当前落地建议

1. 先在 3-5 个真实任务中人工使用 Router Card 和 Delivery Manifest。
2. 记录它是否减少“产物类型混淆”和“阶段跳跃”。
3. 只把高频且可判定的错点写入 `workflow-gates.yml`。
4. 轻量检查脚本第一版已落地（`scripts/check_delivery_manifest.py`，trial）：检查 manifest 产物类型标签、几何声明配套证据、STATUS 更新与复审声明。按 §6.1 生命周期在一条资产线后评估转正或收窄。
5. Workflow Lab（Level 3）与 §6.1 gate 合并审查尚未实际运行过；已挂入 WMW 资产线收尾动作（见该线 `STATUS.md` 下一步），首跑优先做产物类型判定实验（10 张近期图）+ gate 合并。
6. 最后才接入 CI 或自动阻断。
