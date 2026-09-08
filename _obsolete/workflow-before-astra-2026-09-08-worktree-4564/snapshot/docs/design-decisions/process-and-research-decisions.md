# 设计采纳分册：流程、研究与 Subagent 协作

> 主索引：[`../设计采纳记录.md`](../设计采纳记录.md)。拆分前全文归档：`_obsolete/design-decisions-archive/archive-raw-adoption-log.md`（仅历史考证用）。
> 新增 / 修订时先更新主索引，再把完整条目写入本分册；跨领域内容必须在主索引补 cross-read tags。

## 收录范围

- SIA、subagent 能力沉淀、采纳记录维护、研究门槛与跨分类检索流程。
- 跨读提醒：流程条目只定义如何协作，执行具体 UI / 机制 / 美术任务时仍必须按总索引跨读对应分册。

## 条目

### A23. 独游鉴赏师升级为垂直切片产品把关人
- **来源**：2026-06-01 独游鉴赏师能力建设讨论；用户确认“推进吧”。
- **机制**：独游鉴赏师不只负责 Steam 头图 / 宣传片 / 商店页素材鉴赏，也应作为 Angus 的产品建议把关人，固定支持四类诊断：垂直切片诊断、内容包诊断、Steam 首屏诊断、功能 ROI 评审。每次建议必须回到 3 秒 fantasy、前 10 分钟闭环、周刊身份、发刊立场、玩家故事、截图价值、系统性价比和类型误读风险；输出按“立即做 / 先验证 / 后续做 / 暂缓或砍掉”帮助取舍。
- **应用范围**：`steam_indie_appraiser` subagent、`steam-indie-appraiser` 技能、demo / 内容 / 商业素材 / 功能提案评审。
- **状态**：已采纳并落地到 `skills/steam-indie-appraiser/` 与 `.codex/agents/steam-indie-appraiser.toml`。
- **已修订（2026-06-02 · Codex Desktop 启动壳限制）**：实测完整中文 TOML 会导致 Codex Desktop 报 `agent type is currently not available`；短启动壳可以注册成功。因此 `.codex/agents/steam-indie-appraiser.toml` 只保留稳定注册所需的短英文壳，完整能力沉淀到 `skills/steam-indie-appraiser/SKILL.md` 与 `references/`，后续不要把完整规程塞回 TOML。

### A26. Subagent 能力按分层案例库持续完善
- **来源**：2026-06-02 UX 老哥与独游鉴赏师协作机制讨论。
- **机制**：后续完善 `ux_laoge`、`steam_indie_appraiser` 等项目级 subagent 时，不把普通工作案例直接塞进核心 prompt。项目级硬规则写入 `AGENTS.md` / `docs/onboarding/`；subagent 自身流程写入对应 `SKILL.md`；普通实战案例写入 `skills/<skill>/references/casebook/`；重复出现的稳定模式再提炼到 references 方法论文档或项目级规范；`.codex/agents/*.toml` 继续保持短启动壳。
- **协作分工**：父级 Codex 作为“总编”负责判断该叫谁、限定任务范围、合并冲突和最终落地。SIA 优先处理独游吸引力、Steam 首屏、功能 ROI 与竞品借鉴；UX 老哥优先处理操作链、信息层级、遮挡、安全区和玩家误读。
- **应用范围**：项目级 subagent 使用、技能维护、案例沉淀、后续新对话交接。
- **状态**：已采纳并落地到 `docs/onboarding/subagent-collaboration-improvement.md`，同时为 UX 老哥和 SIA 新增实战案例库入口。

### A62. 设计采纳记录拆分为总索引与领域分册，但必须保留跨分类检索保护
- **来源**：2026-06-15 设计采纳记录瘦身与 UI 资产化链路讨论；用户同意把臃肿采纳记录拆成主索引与分册，同时强调不能因为分类导致任务进行时漏检相关领域，例如骰子界面设计仍可能需要检索整个游戏的艺术风格。
- **机制 / 原则**：`docs/设计采纳记录.md` 作为稳定总入口和路由表；完整条目按主影响域写入 `docs/design-decisions/` 分册。每条索引必须包含 cross-read tags；后续任务读取时先看总索引的跨分类检索保护，再按任务类型读取相关分册。分类只用于加速检索，不能替代整体上下文判断。
- **应用范围**：设计采纳沉淀、AI / subagent onboarding、UI / 机制 / 美术 / 流程相关任务的前置检索。
- **状态**：已采纳为设计采纳记录维护规则；已同步到 `docs/设计采纳记录.md`、`docs/design-decisions/README.md`、`docs/onboarding/ai-collaboration-guidance.md`、`AGENTS.md` 和相关 onboarding 文档。

### A90. 资产化 UI 交付前必须判定稿件类型，真实内容风格稿不得由贴片草图冒充
- **来源**：2026-06-18 地区任务台 v3.6 复盘；用户指出当前所谓“真实内容风格稿”仍存在右侧文档粗暴盖旧组件、左侧和底部多层贴片、旧边缘残留等半成品问题，要求解释为什么资产 UI 化链条已清晰仍会把半成品放到该环节。
- **机制 / 原则**：资产化 UI 每张可见图交付前，必须先声明稿件类型，例如 `structure_wireframe`、`interaction_fix_sketch`、`problem_overlay`、`contract_overlay`、`safe-zone / capacity validation`、`filled-state text mock`、`no-text asset master`、`runtime_skeleton`、`runtime_state_preview` 或 `production_candidate`。不同稿件只能回答对应问题，不能把只验证操作关系、热区或安全区的草图包装成高保真真实内容风格稿。
- **真实内容风格稿 Gate**：`filled-state text mock / 真实内容风格稿` 必须美术自洽，像下一步可以拆分落地的目标图。它不得出现粗暴盖图、普通面板贴片、旧组件残边、调试黑条、红框连线、合同说明文字、PIL / Canvas 临时纸片、旧底图与新 UI 断层或多套视觉系统叠在一起。若出现这些痕迹，必须降级为 `interaction_fix_sketch`、`contract_overlay` 或 `safe-zone / capacity validation`，不能进入无字资产母版、组件 atlas、manifest 生产或“下一步拆分落地”。
- **验收要求**：真实内容风格稿交付前必须做局部裁切自检，至少覆盖主容器边缘、左侧列表 / 任务卡、右侧详情纸、底部日程条 / ticker、主 CTA / 全局动作、地图节点 / 标签。任一裁切像贴片、露底、错层、默认 Label 或旧控件残留，就不能交付为真实内容风格稿。
- **应用范围**：资产化 UI 总链路、世界地图、地区任务台、派遣签批台、发刊前报道板、所有 AI 生图 / 本地脚本 / Godot / HTML UI 实验页交付。
- **状态**：已采纳为资产化 UI 流程硬门槛；已同步到 `docs/onboarding/assetized-ui-production-chain.md` 的 2026-06-18 新增硬门槛和 §2.2.1 `稿件类型 Gate 与降级规则`。

### A94. 生图调色必须先采样色号再写 prompt

- **来源**：2026-06-22 世界地图像素颗粒度分支实验；Variant B 颗粒度被认可但偏黄，父级 Codex 未先采样色号就用“去黄 / 冷白”描述继续修图，导致失败 B2 过白。用户明确要求：调整颜色时，父级和 `@像素艺术` 必须先确定老图色号，保证新图颜色不要出问题。
- **机制 / 原则**：任何涉及生图 / 修图的色彩调整，尤其是“更冷 / 更暖 / 少黄 / 更白 / 更高级 / 更现代 / 更接近参考图”，在写 prompt 前必须先建立色号合同。至少从用户认可的老图 / 标杆图中采样 `paper_safe`、`map_base_navy`、`land_mid / land_light`、`ink_dark`、`alert_red_orange`、`signal_cyan`、`pixel_grain` 等 token，并记录 `hex / RGB`、采样区域、允许浮动范围和失败边界。没有采样表，不得继续写调色 prompt，也不得让 `@像素艺术` 只用“感觉更暖 / 更冷”给修图建议。
- **执行流程**：第一步只锁色，不调颗粒；第二步复采样候选图并与老图 token 对比；第三步在色彩通过后，才继续调整像素颗粒、半调、套印和边缘锐度。每轮只改一个变量。若连续两轮在“偏黄”和“过白”等失败边界之间摆动，必须停止继续生成，回到采样表、局部 mask / 曲线修色方案或请用户确认色彩真源。
- **当前案例记录**：世界地图分支实验采样表位于 `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/color-sampling-b-correction.md`。B 是偏黄 / 旧纸失败边界，`04-failed-b2-too-white.png` 是过白失败边界；后续修正不得简单平均二者，应回到源图 token。
- **应用范围**：世界地图、地区任务台、派遣签批台、报道主板、所有资产化 UI 生图 / 修图、`@像素艺术` prompt 审查、生成后复审、图像实验页和生产候选评审。
- **状态**：已采纳为生图调色流程硬门槛。后续如果未采样就继续做颜色 prompt，应判定为流程违规；若输出无法说明相对老图的具体色号差异，不能称为通过复审。

### A96. 生图色彩必须通过 Color Contract Gate，不得用宽合同 PASS 替代同色

- **来源**：2026-06-22 世界地图像素颗粒度分支实验追加反馈；用户指出 B5 虽被父级称为“色彩合同通过”，但肉眼仍与参考图明显不同。复采样证明 B5 并非偏黄或过白，而是整体偏暗、纸面更沉、深蓝底更重、红橙和青色偏沉。`@像素艺术` 机制复盘判定：B5 只能称为“宽合同误判案例”，不能称为通过。
- **机制 / 原则**：A94 只解决“调色前必须采样”，A96 进一步规定“采样后如何判定通过”。任何要宣称“颜色接近参考图 / 同色 / 色彩通过”的候选图，必须先过 `Color Contract Gate`：唯一参考图、固定 ROI、`hex / RGB / Lab`、逐 token `DeltaE00 / dL`、整图均亮度、纸面占比、暗部占比、失败边界和复采样结果都必须并表记录。只有“没有明显偏黄 / 过白”不能算通过。
- **硬闸门**：核心品牌色和信号色（深蓝、红橙、青色）默认要求 `DeltaE00 <= 3.0` 且 `|dL| <= 2.5`；纸面和地图浅色默认要求 `DeltaE00 <= 4.0` 且 `|dL| <= 2.5`；整图均亮度差默认 `<= 3.0`；纸面占比和暗部占比差默认 `<= 0.01-0.015`。如果工具暂时只能给 RGB / luminance，只能标为“临时色彩检查”，不得给最终颜色通过。
- **像素艺术职责**：`@像素艺术` 复审必须先看颜色硬闸门是否通过；颜色未过时，不得继续给生产标杆、资源标杆或真源候选判断。颜色通过后，才审像素颗粒、块状半调、套印是否为结构语言，以及纸面是否滑向旧报纸、旧档案、泛黄纸噪点或高清摄影噪声。
- **熔断条件**：没有唯一参考图 / 固定 ROI / Lab 或等价色彩表 / 失败边界 / 候选复采样时，禁止继续生图；用户指出肉眼不同而父级只能回答“整体接近 / 风格通过”时，必须回到 Color Contract Gate，不能继续用 prompt 猜。
- **落地文档**：硬闸门入口为 `docs/onboarding/imagegen-color-contract-gate.md`。世界地图分支的案例记录继续写入 `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/color-sampling-b-correction.md`。
- **状态**：已采纳为生图色彩审核硬门槛。B5 记录为宽合同误判案例；B6 修色前必须先建立严格 `Color Contract v1`、失败边界表和验收阈值，再做局部色彩校正。

### A98. 风格锁定稿后必须先做真实内容填充预览，不得跳到资产拆分

- **来源**：2026-06-22 世界地图像素颗粒度分支实验；B7 通过严格颜色合同后，父级 Codex 误把“风格 / 色彩已可继续”理解为“下一步可以进入资产分组拆分”。用户纠正：按当前资产 UI 链，风格锁定后应先做真实内容填充版，验证图文融合和可读性，再谈拆资产。
- **机制 / 原则**：回答“接下来该哪一步”前，父级必须先判定当前稿件类型。若当前产物只是 `visual_style_reference`、`color-locked style draft` 或无字风格方向稿，且没有通过复审的 `filled-state text mock`，当前下一步只能是 `轻量内容合同 -> 真实内容填充预览稿 -> UI / UX / 像素艺术复审`。组件拆分、状态 atlas、manifest、切图和生产资产 brief 只能标为后续阶段，不能作为当前下一步。
- **执行检查**：每次资产化 UI 阶段跳转前，父级要明说三件事：当前图是什么稿件类型；是否已有通过复审的真实内容填充预览稿；若没有，下一步真实内容合同需要哪些地区名、状态、CTA、数值、列表密度、头像 / 图标样本和极端文案。只有 `filled-state text mock` 证明信息密度、可读性、CTA、状态表达、图文融合和桌面 16:9 构图成立后，才允许进入无字资产母版 brief 和组件拆分。
- **禁止表述**：在 `filled-state text mock` 通过前，不得把“组件分组 / atlas / manifest / 切图 / 资产拆分 / 可直接落地”描述为当前步骤；不得把色彩合同通过、像素颗粒通过或风格方向好看等同于生产链路通过。
- **应用范围**：世界地图、地区任务台、派遣签批台、报道主板、任何资产化 UI 风格实验、生图风格稿、色彩锁定稿、像素颗粒度实验和后续生产候选。
- **状态**：已采纳为资产化 UI 阶段判断硬门槛，并同步到 `docs/onboarding/assetized-ui-production-chain.md` 与 `docs/onboarding/subagent-collaboration-improvement.md`。后续若父级或子 agent 再把风格锁定稿之后的当前下一步说成资产拆分，应判定为流程违规并立即纠正。

### A122. Angus workflow harness 采用从轻到重的 Router / Manifest / Lab / Hard Gate 渐进链

- **来源**：2026-06-29 关于 AI 工作流从 harness 到 loop 的讨论。用户在检索近期错题本后确认：按“先轻量、再中间验证实验、最后高风险硬 gate”的方案开始完善，避免一步到位走得太远。
- **机制 / 原则**：Angus 不直接上重型自动 workflow。先用 `Router Card` 在开工前判断任务类型、风险等级、当前阶段、目标载体、必读真源、必调 agent、本轮只验证什么和本轮不做什么；再用 `Delivery Manifest` 在交付前声明产物类型、能证明什么、不能证明什么、已过 / 未过 gate、下一步允许做什么和禁止跳到什么。只有 risky / production 任务才进入 hard gate；tiny typo、明显小 bug 和低风险单点修复可轻量处理。
- **Loop 口径**：工作 loop 从“用户纠错后沉淀”前移到“交付前 Route -> Scope -> Build -> Inspect -> Classify -> Decide -> Sediment”。其中 `Classify` 是关键步骤：如果产物只是逻辑烟测、safe-zone 容量验证、无字风格稿或运行骨架图，父级必须主动降级，不得包装成视觉验收、真实内容风格稿、生产候选或真源候选。
- **中间验证实验**：在脚本化或 CI 化前，先做 3-5 次 Workflow Lab：产物类型判定、阶段跳转、agent 调用预算、截图验收和沉淀分层实验。只有证明某个 gate 能稳定减少误判，才考虑写成轻量检查脚本或自动阻断。
- **防僵化边界**：不得把 harness 误用成所有任务强制多 agent 会审；subagent 只提供证据链，父级 Codex 是 DRI，负责合并冲突、说明取舍成本并在必要时交给用户裁决。连续两轮同类失败时应熔断，回到上游定义或请用户裁决，而不是继续生成。
- **落地文档**：执行入口为 `docs/workflows/angus-workflow-harness.md`；机器可读 gate 草案为 `docs/workflows/workflow-gates.yml`；模板位于 `docs/workflows/templates/`。
- **应用范围**：AI / Codex 协作流程、复杂 UI / 资产化 UI / 生图 / 主流程玩法 / 数值 / 状态机 / GDD 真源变更 / 生产候选交付。具体任务仍需按总索引跨读 UI、机制、美术或其它分册。
- **状态**：已采纳为渐进 workflow 入口；已新增 `docs/workflows/` 文档和模板，并同步到 `AGENTS.md`。当前阶段先人工试用，不新增 CI 或硬脚本。
- **已修订（2026-06-29 · 回馈可读性）**：Router Card、Delivery Manifest 和 Loop Log 必须先给 `白话摘要 / Human Brief`，用 4-6 行说明“这句话到底是什么意思、做了什么、卡在哪里、为什么不能跳过、下一步怎么验证、本轮不要做什么”，再列详细清单。白话摘要必须用自然语言；`no_text_style_draft`、`filled_state_text_mock`、`production_candidate` 等标签只能放在括号或第二层术语清单里，不能用术语代替结论。Router Card 必须区分 `本轮交付物类型` 与 `被路由对象类型`，避免把“本轮只交 Router Card”误写成“被评估对象已进入 no-text / runtime / production 阶段”。本轮必读真源与进入下一步才需要读取的真源也应分开，避免填卡本身变成重流程。
- **已再修订（2026-06-29 · 决策条优先）**：`Human Brief` 仍有阅读门槛，因此第一屏改为三行 `Decision Strip / 决策条`：`结论 / 影响 / 下一步`。它必须让用户不读 Router、gate、agent 或 Loop Log 细节，也能立即知道是否通过、会挡住什么和下一轮具体做什么。Human Brief 降为第二层解释，术语清单降为第三层审计。
- **已再修订（2026-06-29 · 防模板泛化）**：决策条只用于 workflow gate、Loop Log、是否通过判断、卡住/返工/需要裁决等场景。普通解释、讨论、完成汇报、进度更新和轻量问答应回到自然语言；不得把 `结论 / 影响 / 下一步`、Human Brief 或 Router 字段泛化成所有回复的固定格式。
- **已再修订（2026-06-30 · 风格稿组件倾斜拦截）**：资产化 UI 的风格稿、生图稿、有字 mock、无字资产母版和生产候选必须显式触发 `ui_geometry_gate`。父级必须列出承载动态文字、按钮文案、头像状态、数值或点击热区的核心表面，并用局部裁切 + 水平 / 垂直参考线检查是否 0 度正交；只看整屏观感不得宣称几何通过。可写纸面、CTA、任务卡内框、右侧票据或按钮底板倾斜时，产物必须降级为灵感图 / 偏差案例，不得继续进入 `filled_state_text_mock`、`no_text_asset_master`、manifest 或 production candidate。
- **已再修订（2026-06-30 · 正交证据自动触发）**：用户不需要每次提醒“给裁切和参考线”。当任务对象是资产化 UI 风格稿、生图稿、有字 mock、无字资产母版、运行预览或生产候选，且画面里存在动态文字、按钮文案、CTA、hit rect、头像状态、数值、任务卡、票据、dossier、纸面或地图 pin 标签时，父级必须自动触发 `ui_geometry_gate`。凡要宣称“正交通过 / 可继续拆资产 / 可进 manifest / 可进 runtime / 可作为生产候选 / 视觉验收通过”，都必须至少给出 3 个核心信息面裁切、水平 / 垂直参考线或等价角度说明、逐项通过 / 未通过结论；没有证据只能写“几何未验证”，不得写“通过”。纯文字讨论、低保真结构线框且不声称视觉通过、无动态内容或 hit rect 的纯装饰图，不强制触发。
- **已再修订（2026-06-30 · Loop Log 自动触发）**：用户不需要说 `Loop Log`。当用户说“这次错在 / 哪里错了 / 为什么又 / 复盘 / 怎么避免 / 防复发 / 先别落地 / 不改文件 / 进错题本 / 转成 eval case / workflow 没跑完整 / 没触发 gate / 你误判了 / 你跳步了 / 漏调或乱调 agent”，或父级自检发现阶段、产物类型、证据、agent、可读性、实现范围或交付声明误判时，必须自动切到 `loop_log` 模式。触发后最低输出包括决策条、触发来源、原始问题、失败归因、本轮处理、复发保护和沉淀判断；只道歉或普通解释不算 Loop Log。

### A126. AI 日报 / 次报采用上下文对象化侧车，保护强反馈、错题本、eval case 和报告状态

- **来源**：2026-07-02 AI 日报 / 次报工作流讨论。用户认可将“用户强反馈 / 错题本 / eval case / 已采纳设计”明确对象化，用来解决日报规则、用户反馈、自动化复盘在上下文压缩后容易丢失的问题。
- **机制 / 原则**：AI 情报线程不只依赖聊天上下文，而应维护轻量 context sidecar。重要信息分为五类对象：用户强反馈、错题本 / Loop Case、可测试 eval case、已采纳规则、上次报告状态。每类对象都要记录来源、错误模式或规则、复发保护、适用范围和状态，避免下一次报告时凭印象复述。
- **日报规则**：发日报 / 次报前必须先读 `docs/workflows/ai-radar-memory.md` 和 `docs/workflows/ai-radar-loop-cases.md`。报告必须有覆盖窗口、人话标题、新在哪里、工具实际能力、典型例子、制作人判断、风险 / 不要误读和来源。Angus 判断必须位于事实解释之后，不能用项目推演替代工具能力说明。
- **错题保护**：TUA-Bench 这类 benchmark 不得被写成工具能力；LiveEdit 这类单项工具不得被误命名为“雷达”；图文页不得为了图形化降低信息密度；上次重点条目不得无新进展重复；Codex 自动化未真实触发时不得称为可用。
- **报告状态**：每次正式日报 / 次报后更新 last-report state，包括报告标题、覆盖窗口、重点条目、弱信号、下次禁止重复项和允许追踪条件。用户手动说“发次报”时，默认覆盖上次正式报告之后到当前时间。
- **落地文档**：执行入口为 `docs/workflows/ai-radar-memory.md`；当前错题本和报告状态为 `docs/workflows/ai-radar-loop-cases.md`。
- **应用范围**：Angus AI 日报、次报、周报交接、AI 工具筛选、图文页生成、日报自动化复盘和后续可脚本化 eval。
- **状态**：已采纳为 AI 情报线程的上下文保护规则。当前先人工维护 Markdown 对象；若重复稳定，可再升级为 JSONL、脚本化 checklist 或 Codex eval。

### A127. Godot 改动采用 gda 编译体检 + headless 场景烟测双层验收

- **来源**：2026-07-02 `gda/godot-agent` Windows headless 最小实验与 Angus 真实 `WeeklyRunGame` 故障实验。用户确认按方案落地 Godot 体检流程。
- **机制 / 原则**：后续 Codex 只要改动 Godot 脚本、`.tscn` 场景、节点层级、autoload、preload 路径、周循环阶段、世界地图、地区任务、派遣、排版或发刊流程，交付前必须跑双层体检：先用 `gda script validate` 检查 GDScript 语法 / 编译健康，再用 Godot `--headless` 跑真实 `WeeklyRunGame.tscn` 最小交互路径，检查场景能否加载、关键节点是否存在、阶段能否推进到探索和派遣。
- **关键经验**：`gda script validate` 能抓少冒号、缩进、解析失败等脚本错误，但不能单独抓 `.tscn` 节点被改名后的运行期错误；同时 `gda` 在脚本无效时仍可能以进程退出码 `0` 结束，因此必须解析 JSON 的 `valid` 字段。Godot headless smoke 用来抓 `Node not found`、null 调用、autoload / preload 运行期错误等“脚本看着没错，跑起来爆红”的问题。
- **落地文件**：执行脚本为 `scripts/run_godot_agent_smoke.ps1`；真实场景烟测为 `gd_project/tests/gda_angus_weekly_run_smoke.gd`；说明文档为 `docs/workflows/godot-agent-smoke.md`；工作流 gate 同步到 `docs/workflows/angus-workflow-harness.md` 与 `docs/workflows/workflow-gates.yml`。默认 `gda` 只校验入口脚本和 smoke runner；其它 `class_name` 脚本主要由 headless 场景运行覆盖，避免单文件校验触发 Godot 全局类误报。
- **边界**：这是运行体检，不是视觉验收、资产化 UI 验收、全状态覆盖或玩法平衡验证。它通过后只能说 Godot 周循环最小真实路径没有爆红；若任务涉及可见 UI、截图、资产化 UI 或生产候选，仍需额外跑对应截图 / UI / UX / 美术 gate。
- **状态**：已采纳并落地为 Angus Godot 改动的默认交付前体检。只改 Markdown、AI 日报、纯 HTML 原型或未落 Godot 的设计讨论时不强制跑。

### A129. Godot Debug Skill v0 作为 Angus Godot 报错错题本与修复入口

- **来源**：2026-07-03 AI 次报后的 Godot Debug Skill v0 方案讨论。用户确认“推进”，要求把“收集 5 个真实 Godot 报错，写成错误签名 / 原因 / 修复 / 验证命令”的方案落地，并保持足够简单易懂。
- **机制 / 原则**：Angus 维护一个轻量 Godot 报错错题本，用来把常见 Godot 失败从“看不懂的引擎红字”翻译成 Codex 可执行的修复卡。每张卡必须包含：报错长相、人话解释、常见原因、窄修法、验证命令和通过标准。Codex 遇到 Godot smoke 失败、用户报告 Godot 报错、或改动节点 / 场景 / GDScript 前后，应先按错题本归类，再做最小修复，最后跑 `gda + Godot headless smoke`。
- **首批错误卡**：GDScript 语法 / 编译错误、节点路径找不到、运行期 null 或方法缺失、`class_name` 单文件校验假阳性、Godot 版本 / PowerShell / `gda` 环境失败。首批卡片来自 2026-07-02 Windows headless 实验和 Angus `WeeklyRunGame` 真实故障演练。
- **落地文件**：错题本入口为 `docs/workflows/godot-debug-skill-v0.md`；Godot 体检入口仍为 `docs/workflows/godot-agent-smoke.md`、`scripts/run_godot_agent_smoke.ps1` 与 `gd_project/tests/gda_angus_weekly_run_smoke.gd`；workflow gate 已要求 Godot smoke 失败时查错题本。
- **边界**：Debug Skill 不是 Godot 教程，也不是自动修复器；它只定义“如何识别和修复高频错误”。它不能替代视觉截图、资产化 UI gate、玩法平衡、全状态覆盖或 GDD 真源同步。
- **状态**：已采纳并落地为 Angus Godot 报错处理入口。后续出现新的可复发 Godot 错误时，应追加新卡，而不是只在聊天里口头解释。
- **已修订（2026-07-03 · Godot GUI 原生崩溃）**：用户截图显示 `Godot_v4.6.2-stable_win64.exe - 应用程序错误 / 内存不能为 read`。复盘确认 `gda + headless smoke` 只能证明脚本与最小 headless 场景路径健康，不能证明 GUI / 编辑器 / 指定 Godot exe 不会原生崩溃。因此新增 `scripts/run_godot_gui_startup_check.ps1`，用于启动指定 GUI exe、加载项目、等待 `--quit-after` 自动退出并检查退出码 / 日志。后续遇到 Windows 应用程序错误、GUI / editor crash、版本 exe 差异时，必须单独跑 GUI startup check，不能用 headless smoke 通过冒充该层通过。

### A130. 美术资源 / 动效资产落地采用分阶段中间验收工作流

- **来源**：2026-07-03 3D 骰子动效讨论。用户确认可以试做，但明确要求这不是单纯调一个骰子效果，而是探索一套区别于成熟 UI 资产化链路的“美术资源 / 动效资源落地工作流”，并说明中间版本做到什么程度适合交给用户验收。
- **机制 / 原则**：美术资源与动效资产不直接套用静态 UI 的 `content_rects / no_text_rects / hit_rects` 链路。默认分为 `motion_blockout -> asset_read_proof -> atlas_or_rig_contract -> runtime_cell_preview -> production_candidate`。每次交付必须先标注产物类型，并说明本轮能判断什么、不能判断什么、禁止跳到什么阶段。
- **中间验收口径**：`motion_blockout` 阶段可以给用户看，但它只验证节奏、空间边界、触地 / 回弹 / 缓入缓出、镜头可读性和结果停顿，不验证最终材质、贴图、角色 UI 布局、面数 atlas 或生产可用性。它至少应包含 1 个短动态图（GIF / animated WebP / MP4）和 3-6 张关键帧截图，并在图面或交付说明中写清“这是 blockout，不是最终美术”。
- **3D 骰子试点**：当前试点目标是“2D 界面承载的俯视 / 斜俯视 3D 判定骰子”：每个角色的骰子保持在自己的 UI 槽位内，同时保留物理骰子落下、翻滚、碰撞、回弹和结果停住的信号。运行期可采用受约束的伪物理 / 烘焙物理，而不是让真实 Rigidbody 任意位移。框内位移优先控制在角色框宽度约 15%-25% 内，使用旋转、压缩、阴影、碰撞音效和微回弹来补足重量感。
- **落地文件**：流程文档为 `docs/workflows/art-motion-asset-landing-workflow.md`；3D 骰子 blockout 试点位于 `gd_project/scenes/dev/Dice3DV7Prototype.gd` 与 `gd_project/scenes/dev/Dice3DV7Prototype.tscn`；截图脚本为 `gd_project/tests/capture_dice_3d_v7_prototype.gd`。
- **执行保护**：未通过 `runtime_cell_preview` 和状态矩阵前，不得称为 `production_candidate`。如果交付物只有灰盒、临时数字、临时材质或孤立实验场景，只能要求用户判断“方向 / 节奏 / 空间 / 读感”，不能要求用户判断“可上线 / 可拆包 / 可直接替换正式界面”。
- **状态**：已采纳为试行流程。后续 UI 动效、2D 角色动作、3D 骰子、特效和其它非静态美术资源都应优先按此流程给出中间验收，而不是一口气跳到完整生产资产。
- **已修订（2026-07-03 · 2D UI 承载校正）**：用户指出实际游戏内更可能是 2D 界面下的俯视 3D 骰子效果，类似《苏丹的游戏》判定桌面，而不是独立 3D 场景。因此 v7.3 只能作为纯运动实验留档；v7.4 起改为 `ui_carrier_motion_blockout`，必须把骰子放回 2D 判定盘 / 角色槽承载中检查。
- **已修订（2026-07-03 · 局部判定槽预览）**：v7.5 起新增 `runtime_cell_preview_v0` 验收层，把 3D 骰子放进带任务目标、角色槽、结果预览和提交操作的局部判定弹窗中检查。该层只判断真实信息压力下的读感、槽内约束和主操作干扰，不验证最终美术材质、完整状态矩阵或生产可替换性。
- **已修订（2026-07-06 · 动态演示交付）**：动效类资源只交静态截图不足以验收节奏和重量感。后续动效 blockout / runtime preview 默认交付短动态图 + 关键帧截图；截图负责逐帧问题定位，动图负责判断节奏、物理感、停顿和是否抢主操作。
- **已修订（2026-07-06 · 程序 blockout 不等于美术资源落地）**：用户指出 v0.6 骰子虽然有 Godot 运动和大致配色，但没有走“Image 生成骰面美术资源 -> 切图 -> 拼接 / 贴图 -> Godot runtime 动态验收”的路线，因此观感仍像程序临时实现。后续凡用户要求美术资源、骰面、角色动作、UI 动效或其它可见资产“落地”，必须区分 `motion_blockout` 与 `bitmap_or_model_asset_runtime_preview`：前者只能证明运动，后者必须提供源 bitmap / atlas / GLB / 帧序列等资源文件、切分或绑定说明、引擎内真实运行截图 / GIF。只有程序色块、Label、临时材质或脚本绘图时，不得称为“美术资源已落地”。

### A131. 动态效果交付必须提供动图或视频，截图只作关键帧补充

- **来源**：2026-07-06 骰子 v7.5 动态演示讨论。用户明确要求将“涉及动态效果的内容，一定要给出动图或视频展示，而不是只给截图审核”升格为核心硬规则。
- **机制 / 原则**：凡交付对象包含 UI 动效、2D/3D 角色动作、骰子 / 特效 / 转场、可交互美术小组件、物理反馈、进入 / 退出动画、hover / click / submit 反馈，或任何需要用户判断时间节奏、重量感、停顿、反馈强弱、是否抢主操作的内容，必须提供真实动图或视频。允许格式为 GIF、animated WebP、MP4、WebM，或等价的本地可播放 HTML / Godot capture 页面。
- **截图边界**：截图仍必须用于关键帧定位，尤其是静止、起势、主动作、冲击、回弹、落定和最终读数；但截图不能替代动态演示，也不能让用户仅凭静态图判断动效是否通过。
- **最低交付**：动效类中间版至少交付 1 个短动态图或视频 + 3-6 张关键帧截图。交付说明必须写明本轮能判断什么、不能判断什么；如果由于环境限制暂时无法导出动图 / 视频，必须说明原因，并提供可运行播放页、逐帧序列或明确的补导计划作为临时替代。
- **应用范围**：Angus 的 Godot / HTML 原型、UI 动效、2D 角色动作、3D 骰子、特效、转场、运行时反馈、资产化 UI 中的动态组件和后续所有需要动态审核的美术 / 交互任务。
- **状态**：已采纳为项目核心硬规则，并同步到 `AGENTS.md` 与 `docs/workflows/art-motion-asset-landing-workflow.md`。后续若只交截图却要求用户审核动态效果，应视为交付不完整。

### A137. 美术资产必须先过几何不变量 Gate

- **来源**：2026-07-06 骰面贴图 v0.7 复盘。用户指出“方形的东西生成资源居然不是方形的”是低级错误，并明确这反映了很多工作流错误。复盘确认 v0.7 源 atlas 是 `1254x1254` 的正方形画布，却被当作 `4x3` 骰面图集切分，导致每格实际为约 `313.5x418` 的长方形；后续再压成 `512x512` tile 只是掩盖源头失败。
- **机制 / 原则**：任何美术资源在进入切图、贴图、manifest、runtime 或 GIF 验收前，必须先写出对象的几何不变量并验证。骰面必须是 1:1 方形；4x3 骰面 atlas 必须是 4:3 总画布；卡牌、票据、按钮、角色帧、头像、地图 pin、特效帧和 2D 动作帧也都必须先声明目标比例、pivot、裁切边界和是否允许透明留白。若源图比例错误，不得通过后处理缩放、裁切或运行时 plane 拉伸伪装为通过。
- **执行保护**：新增轻量脚本 `scripts/validate_image_asset_contract.py`，可检查单图方形和 atlas 网格单格方形。后续骰子、方形 icon、方形 UI tile、表情 / 头像、sprite sheet 或任何规则格子图集，切图前必须先跑对应几何检查；失败图只能作为偏差案例，不得进入 `runtime_cell_preview` 或 `production_candidate`。
- **当前案例状态**：`docs/screenshots/2026-07-06-dice-3d-v07-bitmap-godot/dice-v0-7-geometry-gate.md` 记录 v0.7 为 `failed source geometry gate`。v0.7 GIF 仅证明“bitmap 可加载进 Godot”，不证明骰面资产规格成立。

### A161. 已确认结局卡最终版归档与复盘规范

- **来源**：2026-07-08 结局卡社媒资产整理请求。用户要求把所有已确认过的好结局 / 坏结局卡牌最终版放入工作区新建的社媒目录，并总结生成规范、经验和此前所有错误复盘，避免后续重复犯错。
- **机制**：后续结局卡、meme 卡或同类社媒视觉资产，一旦用户明确确认最终版，应复制到 `社媒/好结局坏结局/` 或对应社媒资产包目录，而不是只留在 `docs/screenshots/` 的实验输出目录。资产包应区分成对长图、单卡、特殊结局或其它使用场景，并保留一份规范 / 复盘文档，记录尺寸、字体、颜色、真实生图要求、图像适配规则、QA 清单和错误案例。
- **执行约束**：社媒资产包只放已确认最终版，不混入 bbox QA、实验版、被用户否定的版本或中间源图。若需要裁出单卡，应从最终成对图中裁切，保证单卡与成对图完全同版。用户说“生图”仍必须使用真实图像生成工具；程序只负责复制、裁切、排版、检测和归档。
- **当前落地**：已创建 `社媒/好结局坏结局/`，内含 `成对长图/`、`单卡/`、`特殊结局/` 与 `README-生成规范与错误复盘.md`。
- **状态**：已采纳为结局卡社媒资产归档规范；后续同类资产确认后应按此目录或同构目录沉淀。

### A162. 资产化 UI 工作流 v2 改造：批处理合同板、纵向切片、倍率声明、合同真源与 gate 生命周期

- **来源**：2026-07-08 资产化 UI 工作流评审讨论。用户先要求审阅当前 UI 资产化工作流并结合世界地图 WMW 案例找问题，随后明确采纳改造方案：“按照你的想法改造完善工作流，保证后续 AI 进行相关工作时不要再出现类似问题”。
- **问题背景**：WMW 案例暴露两类问题。其一是流程自身拖慢：组件合同按组件逐轮开工、逐轮等用户裁决（v0.8.1→0.8.5 五轮），链路严格串行，风险最高的“生图能否服从合同”“引擎能否按 manifest 装配”被推到最后；其二是文档体系漂移：主链路文档退化为约 20 条日期补丁堆、三份真源（主链路 / harness / workflow-gates.yml）互相脱节、合同散在截图目录、证据脚本放在可清理的 `tmp/`、进度要考古 35 份评审、gate 只增不减、评审英文落盘违反语言规则。
- **核心机制**：
  1. **批处理原则**：同页同类工作合并成板；组件合同以“整页合同板”为单位一轮完成量测、归一、整屏回填、文案压力，用户裁决一次过整板；1px 级小归一并入板内说明，不单独立评审。
  2. **纵向切片原则**：首批 class 合同锁定后，先用 1 个代表性组件打通“无字素材 → gate → 切图 → Godot 单组件 → 运行截图”，验证生图服从性与引擎链路后再批量生产；剩余轻合同与素材生产并行。
  3. **倍率声明**：合同必含 `reference_resolution / runtime_resolution / export_scale`；非整数倍关系时素材按 ≥2x 制作，禁止位图放大上屏。
  4. **字段分级**：合同分 `frozen`（几何骨架，改动须显式升版本并重跑回填）与 `provisional`（贴上限文字槽、字体假设等弹性位，复审可回改不算破约）。
  5. **真源分工**：`workflow-gates.yml` 管产物类型 / 阶段跳转 / hard gate 的机器可读定义；主链路文档管操作细则；harness 管风险分级与回复格式；`ui-geometry-and-text-safety-gates.md` 作为两条资产链路共用的几何 / 正交 / 文字安全公共真源。gate 变更必须同时落 YAML 与文档。
  6. **Gate 生命周期**：新 gate 默认试行，存活一条资产线或两周后转正；每完成一条资产线做一次合并审查（合并重复、标注取代、收窄触发、退役失效），防止 gate 只增不减。
- **落地文件**：`docs/onboarding/assetized-ui-production-chain.md`（v2 重构：主链路并入比例分类 / 整页合同板 / 纵向切片，历史硬门槛归位到阶段章节并附 changelog）；`docs/workflows/ui-geometry-and-text-safety-gates.md`（新建公共 gate 真源）；`docs/workflows/workflow-gates.yml`（补齐 `component_aspect_taxonomy / component_class_contract / full_screen_reinsert_proof / text_capacity_stress / vertical_slice_proof` 等产物类型与新阶段跳转、gate_lifecycle）；`docs/workflows/angus-workflow-harness.md`（真源分工、Level 4 对齐、§6.1 gate 生命周期）；`design/ui-contracts/README.md` 与 `design/ui-contracts/world-map/`（四个已锁 class 合同 JSON 真源）；`scripts/ui-contracts/validate_class_contract.py`（合同校验器，含类一致 / 槽位包含 / 回填边界 / 倍率检查）；`scripts/ui-contracts/wmw/`（v0.8x 证据脚本自 `tmp/` 升格）；`docs/plans/world-map-benchmark-landing/STATUS.md`（资产线进度真源，每轮交付必须更新）。
- **执行约束**：评审与状态文档中文落盘；同一评审目录版本号单调递增，路线重启换新前缀；评审不得引用 `tmp/` 路径作为证据；素材不服从合同判素材失败，不得静默迁就；STATUS 未更新不得宣称本轮交付完成。
- **状态**：已采纳并落地。WMW 下一轮按新流程执行：剩余轻合同（map_panel / top_status_strip / icon set）一轮合并补完，与合并 clean-sprite brief、`left_region_card` 纵向切片并行推进。
- **已修订（2026-07-08 · UX 老哥与新工作流咬合小修）**：用户审阅 `ux_laoge` 能力评估后采纳小修方案。落地内容：`skills/ux-diagnosis/system-prompt-v2.2.md` 版本标识统一为 v2.2（原文头尾残留 v2.1）；`skills/ux-diagnosis/SKILL.md` 新增「Angus 项目校准」节——桌面 16:9 基线（不产出移动端方案、`ux-kb-risks` 默认不触发）、产物类型校准表（结构稿 / 合同板 / 有字 mock / runtime 骨架 / 多状态验收各阶段 UX 只判可判问题，禁止对合同板等工程产物做越阶段美术判断，UX 复审以阶段 gate 为单位批处理上场）、合同感知规则（改进建议触碰 `design/ui-contracts/` frozen 字段必须显式标注升版本，方案对比必须写明是否触碰合同）、案例回流规则（强纠偏 / P0 误判 / 越阶段判断必须按 casebook 短格式沉淀）；`.codex/agents/ux-laoge.toml` 增加一行产物类型路由指令，保持短壳。

### A163. 四个未实战 subagent 转入冷备冻结，AI 承担解冻提醒义务

- **来源**：2026-07-08 agent 体系评审讨论。AI 对 9 个 `.codex/agents/` subagent 按价值 / 完备度 / 必要性排序后发现：`game_producer`、`game_sys_architect`、`game_numerical`、`game_logic_check` 四个 2026-06-05 同批导入的 agent 规程完备但零实战记录（casebook 全为上游演示样本）。用户采纳“保留但冻结”方案，并补充关键要求：用户自己无法判断解冻时机、也可能忘记冻结过这件事，因此必须有顶层规则让 AI 在必要时主动提醒解冻。
- **机制**：四个 agent 转入冷备冻结——注册壳与技能保留、显式触发词调用仍可用，但冻结期间不再投入任何维护（不新增规则、不扩 SKILL.md / references / casebook），AI 也不主动 spawn 它们。对应地，AI 承担解冻提醒义务：任务中命中某冷备 agent 的价值窗口（制作人=范围 / 立项 / 里程碑决策；系统架构=新系统注册 / systems-index 更新 / 耦合冲突；数值策划=玩法数值调校启动；逻辑审查=规则成形准备实现或原型出现结算 / 卡死 / exploit 问题）时，必须当场一句话提醒用户并给出不解冻的替代方案，由用户裁决。
- **落地文件**：`AGENTS.md` 新增「冷备 subagent 冻结与解冻提醒顶层规则」；`docs/onboarding/subagent-collaboration-improvement.md` 新增 §8（冻结状态表、冻结含义、解冻触发条件表、解冻流程）。
- **执行约束**：提醒不得省略，也不得默默替代冷备 agent 职责；用户未回应时按替代方案（父级当前线程按 SKILL.md 执行同等流程）继续，不算解冻。解冻需用户确认，确认后同步更新 AGENTS.md 冷备名单与 §8 冻结表。
- **状态**：已采纳并落地。活跃 agent（`ux_laoge`、`ui_designer`、`angus_art_director`、`angus_character_pixel_director`、`steam_indie_appraiser`）不受影响。

### A164. 高频规则文档瘦身：沉淀去重律 + 补丁堆主题化归并 + 分册检索式读取

- **来源**：2026-07-08 高频规则文档与 harness 健康检查讨论。AI 复盘发现：harness/loop 本体运转良好（有真实使用痕迹与 A162 自愈记录），但沉淀层臃肿——`ai-collaboration-guidance.md` 158KB / 108 小节且 §7 为约 50 条无序日期补丁堆、`ui-interaction-guidelines.md` 尾部挂 17 条日期补充、同一经验三重落盘（guidance + guidelines + design-decisions 全文三连写）、`ui-ux-decisions.md` 229KB 使"读全文"规则名存实亡。用户采纳整套优化方案："按照这个方式优化"。
- **机制**：
  1. **沉淀去重律（harness §7.1，硬规则）**：同一条经验只允许一个主承载位（全文），其他位置只准短引用 + 链接；写入前先 `rg` 查重，命中就更新原条目；禁止在必读文档尾部追加日期补丁段落，禁止三连写全文。Loop 第 7 步 Sediment 写入前必须执行。
  2. **guidance §7 主题化重构**：原约 50 条日期补丁归并为 10 个主题小节（范围控制 / 截图交付 / UI 信息架构 / 地图空间 / 数值诚实 / 实验页 / 视觉方向 / 动效 3D / 生图放行 / 子 agent 协作），每条保留可执行判定与触发日期；已被规范文档全文承载的只留一行索引。文件从 158KB 降至约 77KB。
  3. **guidelines 尾部补充归位**：17 条日期补充归并为 §12（派遣签批台与中央主舞台专项）与 §13（跨页面控件与资产化几何）；功能面正交 / 几何 QA / 双通行证的阈值与证据要求收敛到 `docs/workflows/ui-geometry-and-text-safety-gates.md` 单一真源；附归并变更史对照表。
  4. **分册检索式读取**：`docs/设计采纳记录.md` 读取总规则由"读对应分册全文"改为"按 ID / tags 检索命中条目并完整读取条目及修订备注"；小分册或用户要求全面盘点时才通读。
  5. **归档挪位**：`archive-raw-adoption-log.md`（151KB）从 `docs/design-decisions/` 挪入 `_obsolete/design-decisions-archive/`，避免全文检索误命中；原 §7 补丁堆与 guidelines 尾部补充原文分别归档至 `_obsolete/ai-collaboration-guidance-legacy/` 与 `_obsolete/ui-interaction-guidelines-legacy/`，各附 README。
- **执行约束**：归并只重组不删规则，规则内容与触发日期必须保留；归档文件仅供历史查询，不作为现行规则来源；后续新增规则先查重再归并进主题章节，不再按日期在尾部追加。
- **状态**：已采纳并落地。剩余候选（未在本轮执行）：AGENTS.md agent 段落压缩、guidance §7A 跨分类读取表与总索引的重复收敛、其他资产线补 STATUS 页。

### A165. 错题本按错误家族治理：复发判定、二次复发升级律、交付前三问与 manifest 检查脚本

- **来源**：2026-07-08 错题本复盘讨论。AI 审阅全部错题（guidance 约 50+17 条、ai-radar 7 条、skill casebook）后发现：约 70 条错题可归并为 5 个反复发作的错误家族（F1 验证等级冒充 ≥9 次、F2 功能面倾斜 5 次、F3 范围失控 ≥5 次、F4 只修点名局部不扫同类 ≥4 次、F5 实验页入口同步 4 次），复发共同根因是修复写在文档规则层而错误发生在交付放行层；只有升级为 gate / 脚本的规则真正止血（F2、F5 已止血为证）。用户采纳整套治理方案："可以，落地"。
- **机制**：
  1. **错误家族索引**（guidance §7.0）：五族登记表含本质错误、典型化身、复发次数、当前防线层级、状态；Loop Log 失败归因先查表判断复发；出现 2 条本质相同错题即登记新家族。跨域家族（F1 同时出现在 UI 与 AI 日报域）的判断器属全项目层，域内错题本只记域内触发器。
  2. **二次复发升级律**（harness §5.2，硬规则）：同族第二次复发时禁止只补文档规则，必须沿 `文档规则 -> 交付前 checklist -> gate 自动触发 -> 校验脚本` 升一层防线；Loop Log 最低输出增加"复发判定"字段（同步 loop-log 模板）。
  3. **交付前三问**（harness Level 1，trial）：normal 以上任务交付前自问——产物诚实（F1）、范围一致（F3）、同类扫描（F4）；按家族频率反推可覆盖错题本约七成条目。
  4. **manifest 检查脚本**（`scripts/check_delivery_manifest.py`，trial）：检查产物类型声明（对照 workflow-gates.yml artifact_types）、几何声明配证据、交付完成配 STATUS、生产候选配复审；已在三份真实文档验证可运行并产出真实发现（v0.9 brief 缺产物类型声明）。
  5. **Workflow Lab 首跑挂账**：Level 3 五个实验与 §6.1 gate 合并审查从未实际运行，已挂入 WMW 资产线 STATUS 下一步（收尾时首跑产物类型判定实验 + gate 合并 + 评估脚本转正）。
- **执行约束**：家族表由 Loop Log 维护，复发必须更新次数与日期；升级出的新 gate / 脚本按 §6.1 标 trial 走转正；脚本只做文本存在性检查，不替代真实 QA。
- **状态**：已采纳并落地。
- **补充观察**：本次分析确认防线层级与复发率强相关——检查廉价二元（F5）或已脚本化（F2）的家族均已止血；靠自觉执行的高成本人工检查（肉眼裁切、同类扫描）复发率最高，这是后续所有新 gate 设计的优先级依据。

### A166. 仓库物理层治理：截图不入 git、AGENTS.md 压缩、资产线墓碑与状态页补全

- **来源**：2026-07-08 架构剩余问题评审。数据确认三个结构性问题：git 历史 2.9GB 且无 LFS（`docs/screenshots/` 1.84GB / 2394 文件，其中 1482 个已入历史；截图交付硬规则使增长制度性，git / 检索操作明显变慢）；AGENTS.md 45KB 每会话全量加载且近半为 agent / skills 路由细则（抽样 18 个 game-studio 导入技能在工作文档中零使用）；8 条资产线目录仅 1 条有状态页、死线无墓碑标注。用户采纳整套方案："按你的提议来执行"（历史重写明确不做）。
- **机制**：
  1. **截图入库策略**：`docs/screenshots/**` 加入 `.gitignore`（增量止血）；已跟踪的历史截图不动，不做 `git rm --cached`、不做历史重写；被规则 / 合同引用为真源、标杆、校色尺的关键图必须 `git add -f` 显式入库并在引用处注明；交付硬规则不变（截图照常产出与展示，只是不进版本历史）；资产线收尾时可把过程截图整体外部归档。细则落 `docs/onboarding/功能改动截图指引.md` §10。
  2. **AGENTS.md 压缩**：45KB / 129 行 → 16.9KB / 75 行。四个冷备 agent 顶层规则压为一行式（细则指向 SKILL.md）；「Codex Subagents」37 行长段落改为路由表 + 5 条通用调用规则（意见正文折叠保留、环境未暴露时按 SKILL.md 当前线程执行、Steam 数据先联网验证等共性规则合并为单条）；「Available skills / How to use skills」41 行清单迁出为 [`skills/README.md`](../../skills/README.md) 索引，AGENTS.md 只留常用技能一句话与 game-studio 技能"按需资料库、不默认加载"声明。
  3. **skills/README.md 索引**：承接完整技能清单，标注 game-studio 导入技能（约 40 个）截至 2026-07-08 零使用记录、按需查阅；保留 map-systems / balance-check / design-review 与对应 subagent 的边界提醒。
  4. **资产线墓碑与状态页**：`world-map-imagegen-v5/v6/v7`、`world-map-branch-pixel-grain` 各补"已废弃 / 已封存"README（指向 WMW 支线，依据 A123）；`dispatch-signoff-imagegen` 补回溯式 STATUS.md（暂停中，最后活动 2026-06-23 V17.2，恢复时按工作流 v2 重新路由）；`region-task-board-imagegen`、`ui-structure-latest` 补状态 README。
  5. **ai-radar 状态标注**：`ai-radar-memory.md` 头部注明纯手动触发模式、无自动调度、长期无更新属正常。
- **执行约束**：AGENTS.md 压缩只迁移不删规则（触发词、边界、真源指针全部保留在路由表、skills/README 或对应 SKILL.md）；墓碑 README 为回溯整理，恢复对应线工作时先核对最新评审再更新；git 历史重写需用户单独批准。
- **状态**：已采纳并落地。剩余候选：git 历史瘦身（filter-repo，破坏性，待用户单独决策）、`ui-ux-decisions.md` 二次拆分（检索式读取已缓解，降级）。

### A167. 资产化 UI 转向配料化拼装：生图管风格，几何由构造保证

- **来源**：2026-07-08 WMW `left_region_card` B1.1 / B1.2 / B1.3 右缘连续失败复盘后，用户采纳“配料化拼装管线”试点方向："可以的，按照这个方向去试一下"。
- **问题背景**：WMW 左卡线暴露出同一类根因：生图模型擅长风格、材质和局部内容，但不擅长精确几何；把整张生成图当资产源再下游裁切、对齐、掩膜、擦除或填色，会把几何误差转化成双地球、源框残留、照片残带、透明洞和程序色带等事故。B 壳可见照片窗口与合同 `photo_slot` 相差约 18px 后，连续三轮像素手术都没有解决语义冲突。
- **核心机制**：资产化 UI 的生产主链从“生图出成品 -> 切资产”转为“生图 / 标杆出配料 -> 程序按合同拼装成品”。配料包括 frame / bevel / badge 底座、plate 纹理、photo 内容层、icon 小图、运行时文字 token 等；程序只负责按合同几何、九宫格或固定件位置构造 atlas、掩膜、状态同构和 QA，不用程序绘制纸纹 / 边框冒充美术资源。生图继续负责低多边形照片、纸媒质感、半调 / 套印和风格材料。
- **执行边界**：
  1. 左卡试点命名为 B2（v0.9.6），不是 B1.4 像素补丁；第一版按现有 `left_region_card.json` v0.8.2 构造，不改 frozen 字段。
  2. 几何必须由构造保证：`export_size`、`photo_slot`、`label_plate`、`meta_line`、`icon_badge`、`action_badge` 来自合同；比例 gate 退化为自检。
  3. 配料从已认可 / 已生成 bitmap 提取，程序可做裁切、九宫格重组、tint、噪纹叠加、投影、掩膜和 QA，但不得用纯色带、普通面板或脚本纸纹替代美术质感。
  4. 素材与合同出现冲突时必须停下来登记 `*_conflict = needs_decision` 并让用户裁决，不得连续打补丁。
  5. 若拼装稿观感偏呆，可在几何正确后做独立“抛光轮”，但必须用结构 diff gate 证明抛光没有移动任何 frozen 几何。
- **验收路径**：左卡 B2 先做配料提取表与拼装脚本，再输出 2x atlas、manifest、几何自检、alpha / 接缝 / `art_shell_texture_integrity` gate、Python 回填、Godot windowed 单组件截图和 B1.3 vs B2 对比板。若 B2 观感可接受，再把配料化拼装写入 `docs/onboarding/assetized-ui-production-chain.md` 正式主链；若不可接受，配料库仍可作为下一轮美术/抛光输入。
  - **状态**：已采纳为 WMW 左卡试点路线；B2（v0.9.6）纵向切片已跑通机器 gate 与 Godot windowed 截图，但 2026-07-09 用户视觉拒收，原因是照片层缺少 shaped mask 与独立 frame overlay，未写入正式生产主链、未冻结为生产资源。下一轮若继续左卡，必须先补 `photo clipped by shaped mask -> frame overlay / globe / badge` 的分层模型。
- **已修订（2026-07-09 · B2.1 结构裁决）**：用户进一步裁决含图片槽资产不再把照片裁成窗口形状，而是采用 `矩形照片底层 -> 镂空框体上层 -> 运行时文字` 的 z 序结构。照片只盖满窗口外接矩形，边界全部归上层框体 alpha / 状态皮肤定义；未来 Godot 也按照片内容节点、框体状态皮肤节点、运行时文字节点理解。完整 UI 规则见 A168。
- **已修订（2026-07-09 · B2.3 单母版裁决）**：用户撤销 B2.2 的“逐帧窗口真源”路线，明确改为 `available` 帧单母版：只对母版实测窗口与地球圆盘、纯几何挖窗一次；selected / warning / locked 由母版程序派生状态色、badge 图标和 selected 绿光晕。四状态窗口几何必须全等，GateE 由派生断言保证。完整流程规则见 A169。

### A169. 含图片槽同类组件采用“一类一母版”，状态与实例变体由母版程序派生

- **来源**：2026-07-09 WMW `left_region_card` B2.2 v1.1 量测失败后的用户裁决。B2.2 已证明候选 B 原始四帧虽然视觉同类，但照片窗口纵向实测存在差异，继续把四帧都当生产真源会让 gate 反复围绕量测口径打转。用户明确撤销“逐帧窗口真源”，改为“单母版派生四状态”。
- **核心规则**：含图片槽同类组件采用“一类一母版”。生产链只选一个几何最干净、色彩分离最好的状态帧作为母版，本例为 `available` 帧；只对母版实测窗口、地球圆盘和镂空框体，随后所有状态与实例变体都从该母版程序派生。不得把同类多张生图 / 多状态风格稿同时作为生产几何输入。
- **状态派生口径**：状态色通过只作用于框色家族像素的色相 / 明度映射派生；奶油色纸签、地球、badge 底盘等中性结构保持母版；badge 图标从各状态原帧裁取小图替换；selected 绿光晕从原 selected 帧外缘提取为叠加层，只给 selected 使用；非 selected 帧继续执行绿残留清理和 GateD。
- **几何口径**：风格稿允许同类尺寸和窗口存在差异，但生产链第一步必须重建母版到合同几何；此后母版是唯一几何真源。GateE 不再比较四张源图的窗口差异，而是断言派生后的四状态窗口几何全等（diff = 0）。若母版量测或派生色彩质感明显失败，必须停下上报并贴对比图，不得改 gate 或靠局部补丁绕过。
- **应用范围**：WMW `left_region_card` B2.3 立即执行；后续 `right_dossier_page`、地区证据图槽、任务照片槽、地图 pin 预览、含状态皮肤的图片窗口组件都应优先按“一类一母版”生产，除非用户明确批准该 class 有多个真实几何变体。
- **状态**：已采纳为含图片槽组件正式产线规则，并已同步写入 `docs/workflows/wmw-hollow-shell-photo-pipeline.md` 与 `docs/onboarding/assetized-ui-production-chain.md`。B2.3（v0.9.9）已跑通完整纵向切片并生成 459-468 证据，但仍是等待用户观感裁决的候选，不得直接冻结为生产资源，也不得批量生产其它 class。

### A171. UI 资产链五层制度补全：止损规则、实测优先与 brief 双栏、缺陷→gate 闭环、gate 三级制、UX 回归清单与消费义务

- **来源**：2026-07-09 WMW 左卡六轮拉锯全程复盘。用户提问"整个 UI 资产链和 UX 老哥 agent 是否有不完善的地方，为什么运转起来没有解决这个并不难的问题"，AI 给出五层失效模型与成体系补全方案，用户裁决："可以，完全按照你的意思推进"。
- **五层失效诊断**：①资产生产方法层——生图被当成品机而它只能当风格机；②测量判定层——假设冒充事实（传闻几何值、单帧调参判定式、拍脑袋容差）；③gate 验收层——gate 量好量的不量重要的，色带 / 透明洞都是 gate 满分废品；④流程控制层——五轮补丁每轮合规走完流程，没人问方法对不对；⑤角色知识层——没人拥有"资产工程 / 像素所有权"视角，UX 诊断（B 轮绿边 P1）悬空五轮不进 gate。
- **落盘清单**（主承载位，遵守沉淀去重律）：
  1. `assetized-ui-production-chain.md` §5.3：分层 z 序结构、一类一母版、风格稿与生产分离、gate 三级制（构造性断言 > 测量容差 > 人工目检）；§7.5：缺陷→gate 闭环、宣称口径。
  2. `angus-workflow-harness.md` §6.2：止损规则（同类缺陷 2 轮触发，禁止继续修补，固定四段产出）与判据冻结；§6.3：brief / 对白双栏制（已实测事实 vs 待验证假设）。
  3. `ui-geometry-and-text-safety-gates.md` §5.1：合成与分层资产完整性 gate 组（state_geometry_identity / card_body_opacity_probe / chroma_residue_scan / old_content_leftover_scan / border_ring_integrity / screenshot_content_validity / composite_cleanliness，各附来源案例）；§5.2：人工目检清单。
  4. `ai-collaboration-guidance.md` §7.9：实测优先、止损、分层结构三条判断器（短索引 + 链接）。
  5. `skills/ux-diagnosis/SKILL.md`：资产生产完整性检查项（重复元素 / 接缝残留 / 叠化泄漏 / 透明洞 / 状态色独占）、复诊回归清单前置（上轮 P0/P1 状态第一节核对）、P0/P1 消费义务（父级必须在下轮 manifest 记录：进 gate / 进清单 / 接受风险，三选一）。
- **防官僚化边界**：以上制度只绑定资产化 UI 产线与 risky / production 级任务，不扩散到日常轻量任务；gate 按 §6.1 生命周期定期合并瘦身。
- **状态**：已采纳并全部落地（2026-07-09）。

### A173. 社媒冷启动研究采用三级定时流水线

- **来源**：2026-07-10 社媒冷启动持续研究讨论。用户先采纳四周试运行方案，随后明确要求按GPT-5.6不同档位配置性价比最优的定时任务。
- **核心机制**：把持续研究拆成三个共享资料目录的独立阶段。每周五上午由 GPT-5.6 Luna / low 执行平台内检索、固定账号巡检、互动数据摘录、去重和七日复查；每周五傍晚由 GPT-5.6 Terra / medium 读取原始扫描和历史案例，选择代表性样本并输出周报；每月第二个周六由 GPT-5.6 Sol / medium 合并近期周报，修订冷启动手册、检索词池和下一周期实验方向。
- **研究口径**：小红书为主要内容样本，Steam作为转化真源，B站、抖音 / TikTok、TapTap、YouTube、Reddit作为扩散与相邻趋势补充。每轮必须同时保留高互动、中位、低表现和低赞高评论异常样本；点赞不能代替参与和转化证据。平台内搜索与通用网页搜索分级标注，无法阅读全文时进入待人工补看队列，不能写成“平台没有案例”。
- **成本边界**：固定采集和结构化劳动不使用 Sol；关键全文深挖按需使用 Terra / high；Sol / high 或 xhigh 仅用于Demo、Steam商店页、账号定位等重大节点，试运行期间不使用 max / pro。
- **落地位置**：持续研究真源位于 docs/research/social-cold-start/，包含检索词池、历史案例库、监测状态、待人工补看、原始扫描、周报和冷启动手册。自动任务只允许更新该目录中的研究文件，不改游戏代码、GDD或社媒美术资产。
- **验证约束**：遵守 AIR-CASE-006。定时任务创建成功只能称为“已配置、未验证”；必须在 Scheduled 中出现真实运行记录，并按约定生成落盘文件后，才能标记为调度已验证。首四周为试运行，连续结果不足时不得为了按期复盘强行制造趋势。
- **状态**：已采纳，资料基线已落盘；定时任务配置与首次真实触发验证分别记录在监测状态文件中。
- **2026-07-10 一次性 A/B 验证**：用户要求立即并行产出默认组合与全 Sol / xhigh 对照。首次自主运行评分为 62 对 84，但发现默认组一次并发 12 条 RedNote 查询并提前结束等待、全 Sol 组采用 3 批持续等待，两组存在工具编排混杂；补做固定 `3 批 x 4 条、每批最多等待 240 秒` 的 Luna / low 受控复跑后，默认组合评分为 80，全 Sol 为 84。受控默认组召回 120 条、保留 24 条，全 Sol 召回 110 条、保留 24 条，未出现必须依靠 Sol 才能获得足够召回的证据。全 Sol 的稳定增量主要是全文成功率、反模式筛选和转化链分节点洞察，不足以支持每周全链路升级。
- **试运行后的协议修订**：常规三级组合保持不变。原始扫描必须冻结批次、等待、并发和终止阈值；开始 / 结束时间实时读取；不得由笔记 ID 推定发布日期；日期不可见的帖子不得满足严格近期配额；搜索返回、去重候选、正式样本和历史参照分开计数。Sol / xhigh 只用于重大节点或可能改变策略的 3—5 条重点全文深挖。单次 A/B 不具统计显著性，至少再做 2 次同协议盲评后才重新裁决常规档位。

### A175. Git 云端提交采用三级模型固定工作流

- **来源**：2026-07-10 Git 未提交资源上传讨论。用户明确要求把提交任务固化为工作流，并按 GPT-5.6 Sol / Terra / Luna 的能力与成本把子任务分级；随后指出父级首次把 Sol 与 Luna 的能力顺序写反，要求核实后继续。
- **核心机制**：固定采用 `Luna / low 只读盘点 -> Terra / medium 提交编排与授权内执行 -> Sol / medium 起高风险裁决 -> Terra 执行 -> Luna 或当前模型只读回执`。Luna 负责状态、文件数、体积、LFS、分支、上游、删除、冲突和疑似敏感文件名等确定性检查；Terra 负责阅读 diff、冻结 include / exclude、划分 commit、选测试、暂存、提交和在明确授权后普通推送；Sol 只处理历史改写、复杂冲突、密钥进入历史、LFS 迁移、第三方许可、跨 GDD / 代码 / 设计真源矛盾或不可逆方案取舍。
- **权限边界**：模型档位不扩大权限；`stage`、`commit`、`push`、`amend / rebase / force / 历史改写` 分开授权。没有精确清单时不默认 `git add -A`；不静默 pull、rebase、强推、清理未跟踪文件或回滚用户改动。过程截图继续遵守 A166，默认不入 git，真源例外显式加入并核对引用。
- **成本边界**：文件数量多本身不触发 Sol。范围单一、验证确定、用户已给精确清单的批量资源提交仍由 Terra 处理，机械盘点交 Luna；Sol / high 或 xhigh 只在复杂度和后果风险同时上升、或需要对照验证时使用。
- **运行时真实性**：固定工作流定义路由政策，不等于当前 Codex 运行时已经支持同一任务内按 subtask 自动切换型号。运行时未暴露模型绑定时，由 Terra 执行全链路，Luna 阶段用确定性脚本限制自由度；命中 Sol 升级条件时暂停并请用户切换或使用已暴露的 Sol agent，不得伪称已自动切换。
- **落地位置**：主执行真源为 [`skills/git-cloud-submit/SKILL.md`](../../skills/git-cloud-submit/SKILL.md)，包含模型路由、提交清单模板、只读审计脚本和本次型号顺序误判的 Loop Log casebook；AGENTS.md 与索引只保留触发入口。
- **状态**：已采纳并落地（2026-07-10）。


### A177. Git 提交增加交接完整性 Gate 与多远端逐一核验

- **来源**：2026-07-10 跨端续做讨论。用户明确指出关注点不是某一次未提交清单，而是当前“不提交”规则是否会妨碍另一端无缝衔接；在确认风险后采纳完善方案，并要求按新工作流同时提交 `origin` 与 daydream 远端。
- **核心机制**：`不进 Git` 不再等同于 `不做同步`。每个未纳入当前提交、但与续做有关的路径必须归为 `ACTIVE / REPRODUCIBLE / EXTERNALIZED / SECRET / DISPOSABLE / LOCAL_ONLY_REQUIRED`；没有规则匹配时记为 `UNKNOWN`。生产代码、生产资产、manifest、GDD、设计决策和正式标杆不得标为可丢弃。
- **放行口径**：`submission_ready` 与 `seamless_ready` 分开。用户明确允许当前仍在运行的任务暂留本机时，`ACTIVE` 可以不阻断本次普通提交，但必须在回执列出，且 `seamless_ready` 仍为否；`UNKNOWN`、`LOCAL_ONLY_REQUIRED`、缺失复现或外部位置证据一律阻断无缝交接声明。
- **多远端规则**：逐个核对远端名称、脱敏 URL、目标分支和授权；逐个 fetch、确认远端分支是当前 HEAD 的祖先、执行非强制 push，再逐个核对远端跟踪引用。一个远端成功不代表其他远端成功；分叉时停止，不静默 merge / rebase / force。
- **截图与大产物**：A166 继续有效。过程截图默认不进 Git，但如果另一端继续判断必须看到，就要外部同步并在 handoff manifest 记录位置，或提升为真源例外显式入库；不能只留当前机器又声称无缝交接。
- **落地位置**：执行真源为 [`skills/git-cloud-submit/SKILL.md`](../../skills/git-cloud-submit/SKILL.md) 与其 [`handoff-completeness.md`](../../skills/git-cloud-submit/references/handoff-completeness.md)；机器可读 gate 为 [`docs/workflows/workflow-gates.yml`](../workflows/workflow-gates.yml) 的 `hard_gates.handoff_completeness`；只读审计脚本支持 handoff manifest 与多远端快进检查。
- **状态**：已采纳并落地（2026-07-10，trial；按一条完整提交线或两周后复核转正 / 收窄）。

### A180. clean low-poly weekly 支线暂时剔除旧像素坐标系的美术指导自动路由

- **来源**：2026-07-13 区域任务台新风格稿讨论。用户确认本次两张标杆为 `benchmark-board-01.png`、`benchmark-board-02.png`，随后指出 `angus_art_director` 由此前像素风图片训练，要求判断其是否适合指导以新标杆为主的生产；若不适合，暂时从工作流剔除。
- **判断**：当前不适合担任该支线的主风格指导或阻断式复审者。启动壳将它定义为 Pixel Art / Art Director，技能默认把像素颗粒、半调和套印是否成为结构语言列为硬检查；而 clean low-poly weekly 支线明确以大块低多边形明度面、干净现代周刊、轻纸品、低微细节为主，且特意与旧像素 / 重半调方向分离。两套坐标系存在稳定的反向牵引风险。
- **机制**：仅对以两张新标杆为真值的 `clean low-poly weekly` 支线暂停 `angus_art_director` 自动路由，包括生成前 prompt 指导和生成后放行。父级直接读取两张标杆、支线风格规范、纸张材质合同与 Color Contract；`ui_designer` 与 `ux_laoge` 继续负责布局、容量、交互和可读性；父级按原图做逐项视觉对照。其他 Angus 像素 / 半调方向与用户显式点名 `@像素艺术` 的调用不受影响，显式调用在本支线只作非阻断对照。
- **恢复条件**：不得静默恢复。只有在 `angus_art_director` 完成 clean low-poly 支线专用真值源、失败样本和评审坐标校准，并经用户明确确认后，才能重新加入该支线自动工作流。
- **落地位置**：`AGENTS.md`、`docs/onboarding/subagent-collaboration-improvement.md`、`docs/onboarding/assetized-ui-production-chain.md` 与 `design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`；本次路由误判另记 Loop Log。
- **状态**：已采纳并落地（2026-07-13）。


### A212. 区域任务台完整风格稿先过全组件生产可行性评估

- **来源**：2026-07-15 区域任务台完整风格稿进入落地前。用户明确要求新增一环评估，吸取世界地图组件难挖图、难裁切以及本可用更简单方式实现却错误资产化的经验，先整理所有功能组件并检查功能、位置、交互、裁切与生图可行性。
- **核心规则**：完整风格稿只证明视觉组合，不自动取得生产母版资格。进入区域任务台资产生产前，必须逐组件登记功能、位置、状态、文字安全区、命中区、锚点、裁切污染和推荐实现方式；每项明确归入“复用原图 / Godot 原生构造 / 生图无字母版 / 退役旧资产”。带动态文字、数字、路线、图标状态或相邻遮挡的整屏内容禁止直接挖图。
- **生产路线**：复用已选地图原图；HUD、文本、路线、分隔结构与大部分状态反馈由 Godot 构造；任务卡、图钉、短签、dossier、CTA 和日程板只生产无字母版，并执行 A169“一类一母版”。先做“地图 + 0–N 事件图钉 + dossier + CTA”纵向切片，通过后才可批量生产。
- **阻断条件**：manifest v2 与 `design/ui-contracts/region-task-board/` 未建立、旧五热点未改为共享 `task_id` 的动态 0–N 事件坐标、7 / 8 / 9 行摘要未实测、CTA 未按冻结底边锚定、运行时仍由 `rt_artboard_full` 提前返回时，批量生产一律 NO-GO。
- **跨读保护**：继续执行 A162、A167、A169 的资产化链路；交互与几何读取 A204、A208、A210；clean low-poly 支线复审仍执行 A180，不恢复旧像素 `angus_art_director` 自动路由。
- **落地位置**：[`2026-07-15-region-task-board-prelanding-component-evaluation.md`](../plans/region-task-board-imagegen/2026-07-15-region-task-board-prelanding-component-evaluation.md) 与 [`region-task-board-assetized-production-spec.md`](../plans/region-task-board-assetized-production-spec.md) Step 0 / §14。
- **状态**：已采纳并落地为本页正式生产准入规则（2026-07-15）。同日后续已完成 manifest v2、区域任务台组件合同、共享 `task_id` 的 0 / 1 / N 与密集点位测试、7 / 8 / 9 行摘要压力、CTA 底边锚定及真实派遣回调；旧 `rt_artboard_full` 不再遮蔽新区域切片。当前放行按组件制作无字母版并逐类替换运行骨架，仍不放行整屏裁切、同类批量生图、全量 atlas 或 production candidate。`推进一天` 因缺少独立玩法命令保持禁用，不得以假交互跨过该阻断。
- **2026-07-16 裁切准入修订**：用户进一步要求所有需要裁切的功能组件必须在生图前逐项确定，不能只写“约 8 类外壳”或事后从整屏补抠。页面现冻结 18 个唯一 class；首条切片实测后路线修订为 10 类独立透明母版、5 类矩形 NinePatch、2 类不透明底图 / tile、1 类程序组件，短签固定 200×72，不使用未经拉伸证明的 NinePatch；E2 直接裁切正式资产的允许数量为 0。每个 class 必须在 `component_cutout_inventory_v1.json` 中登记尺寸状态、倍率、alpha padding、阴影所有权、允许 / 禁止烘焙内容、状态派生和生产授权；未登记或 `production_authorized=false` 的资产不得进入 prompt。第一条生产纵向切片收窄为 pin + 短签，未通过透明边缘、3x 缩小、anchor、0 / 1 / N、状态矩阵和真实 Godot 回插前不扩产。
- **2026-07-16 首条切片放行**：pin + 固定尺寸短签已完成真实 Godot 接入，覆盖 0 / 1 / N、五点密集、8 点 cluster、右边缘 clamp、八态矩阵、中文容量与 hover → selected 动态证据。首轮双复核发现 selected 短签遮挡相邻 pin，修订为 selected label rect 以 8px 净距参与其它 pin displacement；`07-five-dense-selected-label-clearance.png` 复核后 `ui_designer` 与 `ux_laoge` 均最终 GO，P0 / P1 清零。现只解锁下一类 `rt_event_card_mother` 单类验证，整屏挖图、其它组件和批量生成仍不放行。
- **2026-07-17 美术 Gate 重开**：用户明确指出当前生成的组件美术资源没有此前美术效果稿美观。2026-07-16 的 GO 现限定为技术、裁切、运行时和 UI / UX 功能通过，不再代表 benchmark 视觉通过；`rt_event_card_mother` 解锁撤回。新对话必须先直接对照 benchmark 01 / 02、E2、alpha master 与真实运行态，关闭 pin / label 的美术落差并取得用户视觉确认，才能恢复下一组件。
- **2026-07-16 落地位置**：[`2026-07-16-region-task-board-component-cutout-preflight-v2.md`](../plans/region-task-board-imagegen/2026-07-16-region-task-board-component-cutout-preflight-v2.md)、[`component_cutout_inventory_v1.json`](../../design/ui-contracts/region-task-board/component_cutout_inventory_v1.json) 与 [`STATUS.md`](../plans/region-task-board-imagegen/STATUS.md)。

### A216. normal 以上任务开工先说明隐含补全与同批必要性；可见预览和生产升格分阶段，验证按失效范围增量执行

- **来源**：2026-07-15 A214 耗时复盘。用户确认完整拖拽、跨版交换、候选池退稿、点击路径、取消与确认冻结大部分都有必要，但明确指出：这些隐含功能应在任务开始前或刚开始时被告知，并说明是否有必要一次做完；验证和生成不应每轮全量执行。
- **前置说明**：normal 以上任务的第一条进度更新必须用自然语言区分“用户明示需求 / 为闭环或正确性必须补完 / 可延期生产化 / 本轮推荐范围”，并给出首次可见结果的大致时间级别。它不是审批表；只有新增语义、额外延迟超过约 30 分钟、批量正式生图 / 生产升格或存在重大方案分歧时才停下请用户裁决。
- **两阶段执行**：连续看图、UI 纠偏和局部交互默认先交 `runtime_state_preview`，目标是在 30–45 分钟内给第一个真实可见检查点；方向确认后才做完整边界状态、正式资产、manifest、合同、全量 QA 与文档升格。会造成数据丢失、重复状态、确认分叉或核心流程卡死的正确性保护不能延期。
- **增量验证**：视觉改动只验证受影响状态和直接消费者；交互预览先跑 6–12 项核心断言、短动态和基础 smoke；单资产只重生并检查该 class；未被改动且依赖未失效的证据直接引用最近一次通过结果。全量状态矩阵、长文案、定量美术 QA、全量回归和长期文档同步只在生产升格、跨系统外溢、真源冻结或发布前触发。
- **落地位置**：执行真源为 [`docs/workflows/angus-workflow-harness.md`](../workflows/angus-workflow-harness.md) §2.1；本条只记录用户采纳，不复制详细矩阵。该规则属于人类可读范围与节奏控制，不新增 `workflow-gates.yml` hard gate。
- **状态**：已采纳并落地（2026-07-15）；先在后续 3–5 个可见 UI / 交互任务中试行，再评估是否需要机器检查。

### A231. 无字候选图必须附带可理解的选型说明

- **来源**：2026-07-17 区域任务组件 A/B/C 母版 v3 首次交付。助手只展示了图片，用户随即询问“这是几版让我选吗”，并明确要求“下次不要只贴图，要给必要的介绍和文本”。
- **机制**：无字母版、透明 clean master 和不烘焙文字的资产合同只约束图像内容，不约束对话交付。后续交付任何候选图、组件母版、风格稿或 A/B/C 选型板时，必须用简短文字写明：产物用途与方案数量、方位到方案的映射、当前推荐与核心理由、用户需要确认的事项，以及确认前仍冻结的生产动作。只有用户在当前回合明确要求“只发图”时才可省略。
- **禁止误用**：不得把图片 alt、文件名、无字画面或先前进度消息当作最终交付说明；不得要求用户从视觉差异自行猜测哪一列对应哪一方案，也不得在只贴图后等待用户追问当前 Gate。
- **落地位置**：`docs/onboarding/assetized-ui-production-chain.md` §9、区域任务生图线 STATUS 与 `2026-07-17-region-task-motherboard-image-only-handoff-loop-log.md`。
- **状态**：已采纳并立即生效。


### D3. Steam 独游小爆款研究以 10 万份作为成功样本门槛
- **来源**：2026-05-31 Steam 独立游戏鉴赏师 subagent 讨论。
- **机制**：后续构建 Steam 独立游戏鉴赏师 / 市场对照知识库时，不只研究年度级爆款，也要重点研究近三年发布、销量或估算销量达到 10 万份以上的小爆款；优先选择与《世界未解之谜周刊》在调查、未解之谜、异常事件、报刊 / 档案 / 桌面工作、卡牌叙事、周回合经营或轻策略取舍上有相似维度的样本。
- **应用范围**：市场研究、竞品样本筛选、Steam 鉴赏师 subagent 评价体系；不直接作为玩法规格或销量承诺。
- **状态**：作为研究口径留档；后续若落成正式技能，应同步写入对应 `skills/steam-indie-appraisal/` 说明。
- **已修订（2026-06-01）**：正式技能已落地到 `skills/steam-indie-appraiser/`；后续样本研究继续使用 10 万份 / 评价数推断的小爆款口径，但需标注证据等级，不能把估算当事实。

### A241. 可见资产交付必须给出完整拆图流水线与明确裁决任务

- **来源**：2026-07-21 用户在 WMW `schedule_gate v0.1` 有色纵切制作中明确指出：“不要只给我几张图让我看，我看不出啥”；若需要用户审阅，至少必须说明图片用途、为什么现在出示、需要确认和判断什么。
- **交付裁决**：后续生图、组件资产化、拆图、atlas、运行时回填与可见原型交付，不得把孤立母版、裁片、技术 QA 板或若干无说明截图直接当作用户裁决材料。必须按真实生产顺序展示“参考 / 原始生成源 → 角色裁片 → 材质或色彩归一化 → 几何装配 → 无字母版 → runtime 尺寸回放 → 状态叠加 → 最终可见状态”；没有发生的阶段必须明确标为未做，不得用示意冒充完成。
- **逐图上下文**：每一张要求用户观看的图，必须同时给出三项自然语言说明：`这张图是干嘛的`、`为什么现在要看`、`用户需要确认 / 判断什么`。图片内部优先放置简明的用途 / 当前 Gate / 判断点，最终回复再以玩家可理解的语言复述；不得只提供路径、hash、尺寸或技术 Gate。
- **裁决颗粒度**：父级必须把技术证据与用户裁决拆开。几何、alpha、文字 bbox、hash、色值等尽量自动审计；只把观感、层级、状态辨识、风格一致性与是否继续下一阶段交给用户。不得要求用户凭肉眼替代脚本判断像素级事项，也不得让用户自己从多图中猜比较关系。
- **阶段完整性**：纵向切片可以不进入 Godot 或整屏，但交付必须走完本轮授权范围内的最后可见结果。若本轮授权是“母版 + runtime 回填”，不能停在 imagegen 原图、材料裁片或无字母版阶段；必须展示最终 runtime 回填状态，并说明尚未覆盖的动态 / 接线边界。
- **本轮应用**：`schedule_gate v0.1` 将新增完整流水线讲解板，把真实 imagegen 配料、四角色拆分、1368×984 装配、456×328 母版、342×246 回放与 7 个 runtime 状态串成连续证据；状态板顶部补“用途 / 为什么现在看 / 你要判断什么”。
- **状态**：已采纳，立即用于本轮及后续可见资产交付。
- **cross-read tags**：`A216/A231/A240`、accepted、assetized-ui、communication、delivery、evidence、imagegen、pipeline、process、review-context、ui、ux、workflow、`docs/onboarding/功能改动截图指引.md`、`docs/workflows/angus-workflow-harness.md`。

### A242. WMW 必须先确认完整整屏美术风格稿，再继续组件资产化

- **来源**：2026-07-21 用户查看孤立 `schedule_gate` 有色纵切后明确指出：单看一个小组件无法判断其是否符合美术标杆；当前框体直觉上与标杆样式不同；更根本的问题是 WMW 尚无一张经过用户认可的正式完整美术风格稿，必须回到整个界面判断。
- **事实裁决**：当前 WMW 已确认的是 v5.1 的 1920×1080 黑白功能结构，以及 clean-low-poly weekly 的两张支线美术标杆。B2.12、A5.1 与 `schedule_gate` 等局部组件只能分别证明局部几何、信息承载、分层或生产技术，不能证明三栏整屏的色彩比例、材质节奏、地图主次、左右栏统一性和整体周刊身份已经成立。
- **阶段纠偏**：`schedule_gate v0.1` 有色纵切降级为 `technical_pipeline_evidence_only_not_visual_candidate`。它的 456×328 母版、七态回填、geometry / alpha / bbox 审计仍保留技术价值，但不再请求用户判断“是否符合 WMW 美术”，也不能作为下一组件的风格母本或批量扩产依据。
- **新前置 Gate**：下一项可见美术产物必须是一张完整 `1920×1080 filled-state full-screen visual style mock`，使用 A237 的 v5.1 黑白布局、真实默认态文案和 clean-low-poly weekly 两张标杆图，完整呈现左侧 B2.12 卡栈与日程器、中央地图、右侧 A5.1-H 档案的同屏色彩、材质、层级和构图。该稿是整屏风格裁决稿，不是可拆资产、Godot 截图或正式合同。
- **用户裁决范围**：整屏稿只让用户判断整体是否像同一个 WMW 界面、地图是否仍为视觉主场、左右栏与日程器是否属于同一材料语言、强调色比例与信息层级是否接近标杆。像素切图、alpha、hash、safe rect 和 atlas 不进入这次裁决。
- **扩产冻结**：完整整屏风格稿获用户确认前，暂停新的组件生图、atlas、状态资产与 Godot 接入；不得再用“局部 UI/UX 通过”替代整屏美术通过。既有正式合同、compact A5.1、B2.12 与 runtime 继续不动。
- **状态**：已采纳并立即生效；WMW 当前路线退回整屏风格稿缺失环节。
- **cross-read tags**：`A98/A216/A223/A237/A240/A241`、accepted、art-direction、assetized-ui、filled-state-mock、full-screen、imagegen、process、schedule、style-approval、ui、ux、world-map、workflow、`design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`。

### A246. 增量界面审阅只向用户展示必要裁决信息，完整技术证据默认隐藏

- **来源**：2026-07-21 用户审阅发刊编辑副头版横图 v3 交付时明确指出，当前回复信息过多；后续只需依次给出改动例图和本次改动内容。需要选择时，给两个明确方案或基础示意并列出需拍板事项；可补充仍存在的问题与建议，但不应把全部内部过程推到用户层。
- **初版默认审阅面**：一句话结论；1–2 张改动例图或必要动态；2–4 条本次改动；如有分歧则给最多两个方案、推荐与明确拍板问题；最后列最多 3 条仍需关注的问题。
- **2026-07-21 二次修订**：撤销上述机械条数限制。当前口径是只展示足以支撑用户判断的有效信息：例图数量由差异是否看清决定，改动项按真实影响列出，遗留问题与建议只有在会影响视觉判断、方案选择、风险或后续成本时才展示；高价值问题可以多列，低价值小问题不得上推。方案分歧优先收敛为清楚的 A/B，并明确推荐与拍板事项。
- **默认隐藏**：subagent 完整原文、像素坐标、审计 JSON 细项、控制台统计、完整状态矩阵、manifest、Router / Gate、验证命令、未变化截图和内部复盘。它们继续落盘并可追溯，但只在阻断、失败、方案冲突、会改变用户判断或用户主动要求时展开。
- **方案边界**：只有一个明显可行方向时不制造虚假 A/B，直接落地并展示；确有两个方向时，每个方案只说明可感知差异与核心代价，并明确写出“需要用户拍板的内容”。
- **agent 输出例外**：用户已明确要求精简，因此父级可只在对话中给 agent 结论摘要，并说明完整诊断已保存、需要时可补发；不得再把完整原文作为默认正文。
- **状态**：已采纳并立即用于后续 Angus UI / 美术增量审阅。
- **cross-read tags**：`A216/A231/A241`、accepted、communication、delivery、evidence、process、review-surface、subagent、ui、ux、workflow、`docs/onboarding/ai-collaboration-guidance.md`。

### A262. 发刊资产化审阅禁止以混杂程序皮肤的整屏批准单组件

- **来源**：2026-07-22 用户复核主头版 v3 整屏图后指出：其余内容仍由程序生成时，很难判断一个局部是否合适；即使整屏风格稿已经通过，也需要同时保证每个组件本身成立和组件组合后成立，并要求建立更好的审阅方法。
- **已确认要求**：旧程序皮肤不得继续作为美术审阅背景。单组件局部通过不能自动升格为可拆层、可生产或整屏冻结；必须同时提供能判断局部质量、相邻组合和未来整屏关系的证据。
- **当前证据修订**：主头版 visual master v3 降级为 `component_language_probe_local_provisional`。`01-local` 证明局部图文与风格语言可继续；`02-fullscreen` 只证明尺寸 / 位置兼容，不再请求用户据此批准美术。
- **已采纳机制**：用户于 2026-07-22 要求继续按该方向落地。状态采用 `局部暂准 → 区域通过 → 整屏冻结 → 运行态生产冻结`，禁止越级。区域审阅固定提供无字母件、真实内容区域组合、未来态整屏三种证据；未完成区域使用已批准风格稿裁片或目标风格代理，禁止裸露旧程序皮肤。组件从已批准区域母件反向拆层并做重组差分。
- **发刊区域顺序**：中央双版周刊 → 左侧候选报道抽屉 → 右侧发刊复核单 → 全局编辑台框架。当前下一审阅单位应为“主页面纸壳＋主头版＋主页面内页”的中央区域母件，不继续孤立扩产候选卡。
- **首个落地证据**：中央双版区域母件 v1 已完成无字母件、六篇真实报道回填和未来态整屏，UI Designer 与 UX 均 PASS；当前只待用户裁决“中央区域是否通过”，未通过前不得反向拆层。
- **边界**：该机制已同步 `docs/onboarding/assetized-ui-production-chain.md`；正式 Godot、组件合同和 GDD 继续不动。
- **cross-read tags**：`A216/A231/A241/A242/A246/A259`、accepted、art、assetized-ui、component-family、editorial、evidence-level、future-state-proxy、mixed-context、process、region-master、review-surface、ui、ux、workflow。
