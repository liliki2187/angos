# 设计采纳分册：流程、研究与 Subagent 协作

> 主索引：[`../设计采纳记录.md`](../设计采纳记录.md)。拆分前全文归档：[`archive-raw-adoption-log.md`](archive-raw-adoption-log.md)。
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

### A131. 动态效果交付必须提供动图或视频，截图只作关键帧补充

- **来源**：2026-07-06 骰子 v7.5 动态演示讨论。用户明确要求将“涉及动态效果的内容，一定要给出动图或视频展示，而不是只给截图审核”升格为核心硬规则。
- **机制 / 原则**：凡交付对象包含 UI 动效、2D/3D 角色动作、骰子 / 特效 / 转场、可交互美术小组件、物理反馈、进入 / 退出动画、hover / click / submit 反馈，或任何需要用户判断时间节奏、重量感、停顿、反馈强弱、是否抢主操作的内容，必须提供真实动图或视频。允许格式为 GIF、animated WebP、MP4、WebM，或等价的本地可播放 HTML / Godot capture 页面。
- **截图边界**：截图仍必须用于关键帧定位，尤其是静止、起势、主动作、冲击、回弹、落定和最终读数；但截图不能替代动态演示，也不能让用户仅凭静态图判断动效是否通过。
- **最低交付**：动效类中间版至少交付 1 个短动态图或视频 + 3-6 张关键帧截图。交付说明必须写明本轮能判断什么、不能判断什么；如果由于环境限制暂时无法导出动图 / 视频，必须说明原因，并提供可运行播放页、逐帧序列或明确的补导计划作为临时替代。
- **应用范围**：Angus 的 Godot / HTML 原型、UI 动效、2D 角色动作、3D 骰子、特效、转场、运行时反馈、资产化 UI 中的动态组件和后续所有需要动态审核的美术 / 交互任务。
- **状态**：已采纳为项目核心硬规则，并同步到 `AGENTS.md` 与 `docs/workflows/art-motion-asset-landing-workflow.md`。后续若只交截图却要求用户审核动态效果，应视为交付不完整。

### D3. Steam 独游小爆款研究以 10 万份作为成功样本门槛
- **来源**：2026-05-31 Steam 独立游戏鉴赏师 subagent 讨论。
- **机制**：后续构建 Steam 独立游戏鉴赏师 / 市场对照知识库时，不只研究年度级爆款，也要重点研究近三年发布、销量或估算销量达到 10 万份以上的小爆款；优先选择与《世界未解之谜周刊》在调查、未解之谜、异常事件、报刊 / 档案 / 桌面工作、卡牌叙事、周回合经营或轻策略取舍上有相似维度的样本。
- **应用范围**：市场研究、竞品样本筛选、Steam 鉴赏师 subagent 评价体系；不直接作为玩法规格或销量承诺。
- **状态**：作为研究口径留档；后续若落成正式技能，应同步写入对应 `skills/steam-indie-appraisal/` 说明。
- **已修订（2026-06-01）**：正式技能已落地到 `skills/steam-indie-appraiser/`；后续样本研究继续使用 10 万份 / 评价数推断的小爆款口径，但需标注证据等级，不能把估算当事实。
