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

### D3. Steam 独游小爆款研究以 10 万份作为成功样本门槛
- **来源**：2026-05-31 Steam 独立游戏鉴赏师 subagent 讨论。
- **机制**：后续构建 Steam 独立游戏鉴赏师 / 市场对照知识库时，不只研究年度级爆款，也要重点研究近三年发布、销量或估算销量达到 10 万份以上的小爆款；优先选择与《世界未解之谜周刊》在调查、未解之谜、异常事件、报刊 / 档案 / 桌面工作、卡牌叙事、周回合经营或轻策略取舍上有相似维度的样本。
- **应用范围**：市场研究、竞品样本筛选、Steam 鉴赏师 subagent 评价体系；不直接作为玩法规格或销量承诺。
- **状态**：作为研究口径留档；后续若落成正式技能，应同步写入对应 `skills/steam-indie-appraisal/` 说明。
- **已修订（2026-06-01）**：正式技能已落地到 `skills/steam-indie-appraiser/`；后续样本研究继续使用 10 万份 / 评价数推断的小爆款口径，但需标注证据等级，不能把估算当事实。
