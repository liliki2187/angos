## 设计文档（正式真源）

- **顶层真源**：[`design/gdd/core-experience.md`](./design/gdd/core-experience.md)、[`design/gdd/game-concept.md`](./design/gdd/game-concept.md)、[`design/gdd/game-pillars.md`](./design/gdd/game-pillars.md)、[`design/gdd/gameplay-design-principles.md`](./design/gdd/gameplay-design-principles.md)、[`design/gdd/systems-index.md`](./design/gdd/systems-index.md)。
- **同步**：已确定并落地的玩法/规则/常量变更，应先同步对应 `design/gdd/` 文档；若影响产品定位、支柱或系统边界，再同步顶层三份文档。与系统全貌、全链原型对照相关的章节仍应同步 [`docs/archive/legacy-design/系统功能设计总集.md`](./docs/archive/legacy-design/系统功能设计总集.md)（或后续替代真源）中相应段落与 §13、§14。
- **归档提醒**：[`docs/archive/legacy-design/系统功能设计总集.md`](./docs/archive/legacy-design/系统功能设计总集.md) 为归档副本，与当前 `design/gdd/` 并行时以 `design/gdd/` 与代码为准，并在此总集注明差异。
- **出入提醒**：若代码/配置与上述文档不一致，助手在改完或评审时应**明确提醒**用户：择一修正文档或实现。
- **协作偏好**：后续 AI / 新对话在处理玩法、原型、UI 感知类任务前，先读 [`docs/onboarding/ai-collaboration-guidance.md`](./docs/onboarding/ai-collaboration-guidance.md)；若涉及 UI、交互、原型呈现或视觉实验页，还必须读取并执行 [`docs/onboarding/ui-interaction-guidelines.md`](./docs/onboarding/ui-interaction-guidelines.md)；收到新的强反馈后应按分工同步更新对应文档。
- **桌面 UI 顶层硬规则**：Angus 当前完全不做移动版。后续游戏 UI、HTML/Godot 原型、视觉实验页和截图验收默认只面向桌面 16:9；不得主动设计移动端、触屏版、窄屏版或移动端断点，也不得把移动端截图作为默认交付项。只有用户在当前任务里明确要求移动端时，才可作为一次性例外处理，并需说明不改变此顶层规则。
- **UI 设计双 agent 顶层规则**：后续每次做 UI 设计、布局方案、wireframe、mock 或可见原型落地前，默认让 `ui_designer` 与 `ux_laoge` 都参与并互相校验。新 UI / 从 brief 出稿先走 `ui_designer`，再交 `ux_laoge` 评审；改进现有 UI 先走 `ux_laoge` 诊断，再交 `ui_designer` 出改进稿；父级 Codex 负责合并意见、说明冲突，并在落地前把分歧交给用户裁决。
- **制作人子 agent 顶层规则**：`@制作人` 是 `game_producer` 调用触发词，用于立项评估、重大功能范围把关、greenlight / kill、里程碑复盘、熔断判断和制作人视角竞品分析。它不覆盖 `steam_indie_appraiser` 的 Steam 商店页 / 头图 / 宣传片 / 垂直切片诊断，也不插入每次 UI 设计默认链路；只有当 UI 或 Steam 诊断背后涉及项目方向、范围、人月或里程碑取舍时，才交给制作人做上游判断。
- **系统架构子 agent 顶层规则**：`@系统架构` 是 `game_sys_architect` 调用触发词，用于 Angus 玩法系统架构：核心循环到模块/系统/功能拆解、系统注册、依赖图、资源流转、边界接口、耦合审查和系统健康检查。它默认只读，不做技术架构、不写具体规则、不填数值、不替代制作人、SIA、数值策划、逻辑审查、UX/UI、design-review、code-review 或 `map-systems` 文档落盘；已确认架构若要写入 `design/gdd/systems-index.md`，由父级 Codex 或 `map-systems` 在用户确认后执行。
- **数值策划子 agent 顶层规则**：`@数值策划` 是 `game_numerical` 调用触发词，用于 Angus 主干数值设计：角色骰、达标率、任务目标值、概率校准、黑骰反噬、周压力、发刊结算、势力/宏观属性、资源消耗、配表和验证方案。它不替代系统设计、制作人、SIA、UX 或 UI；Roguelite、卡牌、塔防、回合 RPG、MMO/F2P、商业手游等与 Angus 无关的数值类型只作为按需资料库，不干扰 Angus 数值设计主干。商业/MMO/F2P 资料仅在用户明确触发对应领域时读取。
- **逻辑审查子 agent 顶层规则**：`@逻辑审查` 是 `game_logic_check` 调用触发词，用于已成形规则、GDD、配表、状态机、剧情时间线或实现片段的只读逻辑审查：exploit、因果闭环、边界条件、跨系统矛盾、MDA 体验逻辑和叙事一致性。它不做设计、不改文档、不改代码，不替代制作人、数值策划、design-review、UX/UI 或 code-review；不在早期头脑风暴阶段默认调用，除非用户提供了具体规则可审。
- **改动截图交付**：后续每次游戏/原型有可见改动，交付时必须附上改动部分的真实截图与文字说明；1-3 张截图可直接在对话里展示，超过 3 张再整理汇总页；截图方法优先按 [`docs/onboarding/功能改动截图指引.md`](./docs/onboarding/功能改动截图指引.md) 执行，避免让用户逐张翻找或自行对照。
- **动态效果交付硬规则**：后续凡涉及 UI 动效、2D/3D 角色动作、骰子 / 特效 / 转场、可交互美术小组件或任何需要判断时间节奏、物理感、停顿、反馈强弱的内容，交付时必须附真实动图或视频（GIF / animated WebP / MP4 / WebM 之一）供用户审核；静态截图只能作为关键帧和问题定位补充，不能替代动态演示。若技术环境暂时无法导出动图或视频，必须明确说明原因，并提供可运行的本地播放页或逐帧导出方案作为临时替代。
- **设计采纳沉淀**：用户在讨论中明确采纳 / 待定 / 进阶 / 撤回的设计意见，先登记到 [`docs/设计采纳记录.md`](./docs/设计采纳记录.md) 总索引，并按该索引的跨分类检索保护写入 [`docs/design-decisions/`](./docs/design-decisions/) 对应分册。每次讨论中只要出现新的明确表态，AI 必须在当次回复结束前更新总索引与主分册；不主动塞 AI 单方面设想；用户后续撤回/调整时保留原条目并标注修订时间，不要直接覆盖。若意见跨 UI / 机制 / 美术 / 流程，必须在索引补 cross-read tags，避免后续漏读。详细写入规则见总索引「写入规则」。
- **Workflow harness / loop 渐进规则**：后续 normal 以上复杂任务、可见 UI/美术/玩法任务、资产化 UI、生图、主流程改动或生产候选交付前，优先按 [`docs/workflows/angus-workflow-harness.md`](./docs/workflows/angus-workflow-harness.md) 使用 Router Card、Delivery Manifest 和分级 gate；只有在 workflow gate、Loop Log、是否通过判断、卡住/返工/需要裁决等场景，回馈第一屏才使用三行决策条：`结论 / 影响 / 下一步`。普通解释、讨论、完成汇报和轻量问答必须回到自然语言，不得把决策条、Human Brief、Router / gate / agent 术语泛化成所有回复的固定格式。用户说“这次错在 / 复盘 / 怎么避免 / 先别落地 / 不改文件 / 进错题本 / 转成 eval case”，或父级自检发现阶段、产物、证据、agent、可读性或实现范围误判时，必须自动触发 Loop Log，不能只道歉。tiny typo / 明显小 bug 可轻量跳过，但需在最终说明。不得用 checklist、agent/gate 名称或模板字段代替结论，不得把轻量 harness 误用成所有任务强制多 agent 会审；risky / production 任务才进入 hard gate。
- **像素艺术 / 美术指导子 agent 顶层规则**：`@像素艺术` 是 `angus_art_director` 的全局美术资源与界面视觉风格把关触发词；`@美术指导`、美术总监、ArtDirector、像素风美术、视觉风格、风格守门、美术鉴赏师等也调用同一 subagent。后续 Angus 的美术资源、UI 视觉包装、像素 / 半调 / 印刷材质、参考图转译、视觉 prompt 和风格跑偏诊断，默认先让 `@像素艺术` 做只读风格守门；它不直接生图、不直接改 UI / 代码、不替代 `ui_designer`、`ux_laoge`、`steam_indie_appraiser`、`game_producer`、`art-reference-picker` 或 `openrouter-image-gen`。当前正式美术风格以 [`design/art-direction/angus-visual-style-guide.md`](./design/art-direction/angus-visual-style-guide.md) 为准；角色高清微像素细则仍由 `angus_character_pixel_director` 与四人标杆图负责。
- **像素艺术生成后复审规则**：任何 UI 风格稿、美术资源包、界面元素风格稿或生图结果，若要被称为“生产标杆 / 资源标杆 / 真源候选”，必须在生成后再交 `@像素艺术` 复审。复审必须显式检查像素颗粒度、颗粒密度、半调 / 套印是否成为结构语言、是否继承当前标杆图，以及是否滑向旧报纸、旧档案、泛黄纸噪点或高清摄影噪声；未通过的图只能归档为偏差案例或灵感草稿。
- **像素美术子 agent 顶层规则**：`@像素美术` 是 `angus_character_pixel_director` 调用触发词，也适用于 `@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格`，以及眼镜记者、末日时钟、伪人、外星少女、新角色、角色头像、角色立绘、角色群像、角色表情、四人标杆图一致性、角色 prompt 审查等请求。当前角色 / 主编 / 编辑正式方向是高清微像素 Q 版角色；以 [`角色设计风格规范-AI包`](./角色设计风格规范-AI包) 及其四人标杆图 [`reference/01-原始基准图.png`](./角色设计风格规范-AI包/reference/01-原始基准图.png) 为角色美术真源。它默认只读，不直接生图、不直接改 UI / 代码、不替代 `angus_art_director` 的全局美术方向、`openrouter-image-gen` 的实际生图、`ui_designer` / `ux_laoge` 的 UI/UX、`steam_indie_appraiser` 的 Steam 吸引力或 `game_producer` 的资产范围判断。
- **Subagent 能力沉淀**：后续完善 `ux_laoge`、`ui_designer`、`angus_art_director`、`angus_character_pixel_director`、`game_producer`、`game_sys_architect`、`game_numerical`、`game_logic_check`、`steam_indie_appraiser` 等 subagent 时，按 [`docs/onboarding/subagent-collaboration-improvement.md`](./docs/onboarding/subagent-collaboration-improvement.md) 分层处理：项目级硬规则进 `AGENTS.md` / `docs/onboarding/`；subagent 自身流程进对应 `SKILL.md`；普通实战案例进 `skills/<skill>/references/casebook/`；`.codex/agents/*.toml` 保持短启动壳。

## Skills

Angus 的项目本地技能位于 `./skills`。
优先使用这些工作区内副本，而不是 `$CODEX_HOME/skills` 下的重复安装版本。

## Codex Subagents

- `ux_laoge`：项目级 Codex custom subagent，配置位于 `./.codex/agents/ux-laoge.toml`。当用户输入 `@UX老哥`、`@ux老哥`、`@UX诊断`、`@ux诊断`、`@cowork-ux-diagnosis`，或明确说“让 UX 老哥 / UX 子 agent 单独分析”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `ux_laoge`，把截图、问题描述、相关文件路径和必要上下文传入；该 subagent 默认只做只读 UX 诊断，不直接改代码。完整 UX 诊断主 spec 使用 `./skills/ux-diagnosis/system-prompt-v2.2.md`，这是从 portable 包 `core/system-prompt.md` 同步的上游核心；不要用 portable 包的 `adapters/codex/AGENTS.md` 覆盖本项目根 `AGENTS.md`。
- 父级 Codex 最终回复中必须保留 UX 老哥意见正文，不得只给结果或改写摘要。若篇幅较长，应使用 Markdown `<details><summary>UX 老哥诊断原文</summary>…</details>` 做成可折叠内容；折叠块外再单独写“我如何执行 / 已落地 / 未采纳或待确认”。用户明确要求极简摘要时，才可只给摘要，但仍应说明完整诊断可展开或可补发。
- 如果当前 Codex 运行环境暂未暴露 `ux_laoge` 这个 agent 类型，则父级 Codex 必须按 `./skills/ux-diagnosis/SKILL.md` 在当前线程执行同等诊断，不要把 `@UX老哥` 当普通文本忽略。
- `ui_designer`：项目级 Codex custom subagent，配置位于 `./.codex/agents/ui-designer.toml`。当用户输入 `@UI设计`、`@UI设计师`、`@ui-designer`、`@UI Designer`、`@UI出稿`、`@wireframe`、`@mock`，或明确说“让 UI 设计子 agent / UI Designer 单独出稿”“从 brief 出 UI 方案 / 布局稿 / mock / 控件清单”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `ui_designer`，把 brief、项目真源、目标载体、桌面 16:9 约束、相关页面路径和必要上下文传入；该 subagent 默认只做只读 UI 设计方案，不直接改代码、不直接替代 UX 诊断。完整工作流入口使用 `./skills/ui-designer/SKILL.md`，上游完整 prompt 保存在 `./skills/ui-designer/references/system-prompt-v1.0.md`。
- `ui_designer` 与 `ux_laoge` 必须按任务类型接力：新 UI / 新布局先由 `ui_designer` 产出元素对照表、桌面 16:9 mock 和交接摘要，再交 `ux_laoge` 做落地前评审；已有 UI / 截图 / 原型改进先由 `ux_laoge` 诊断，再交 `ui_designer` 出改进版 mock。父级 Codex 负责合并意见；若两者冲突，必须把分歧点、取舍成本和建议交给用户判断。
- 如果当前 Codex 运行环境暂未暴露 `ui_designer` 这个 agent 类型，则父级 Codex 必须按 `./skills/ui-designer/SKILL.md` 在当前线程执行同等 UI 设计流程，不要把 `@UI设计` 当普通文本忽略。
- `angus_art_director`：项目级 Codex custom subagent，配置位于 `./.codex/agents/angus-art-director.toml`。当用户输入 `@像素艺术`、`@美术指导`、`@美术总监`、`@ArtDirector`、`@art-director`、`@像素风美术`、`@视觉风格`、`@风格守门`、`@美术鉴赏师`，或明确说“让像素艺术 / 美术指导 / 美术总监 / 像素风游戏美术鉴赏师单独分析”“审一下这个图像不像 Angus”“把参考图转成 Angus 风格”“检查 prompt 是否跑偏”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `angus_art_director`，把截图、参考图、prompt、目标载体、当前美术真源、相关 GDD 和必要上下文传入；该 subagent 默认只做只读美术风格守门，不直接改代码、不直接生成图片、不直接替代 UI / UX / SIA / 制作人。
- `angus_art_director` 与其它 agent 的边界：Steam 第一眼、头图、宣传片和 demo 吸引力仍由 `steam_indie_appraiser` 判断；UI 布局仍由 `ui_designer` 出稿，UX 可读性仍由 `ux_laoge` 检查；实际生图仍用 `openrouter-image-gen`；参考图库存筛选仍可先用 `art-reference-picker`；若美术方向代表大量资产、人月、里程碑或范围风险，再交 `game_producer`。当前正式美术风格真源为 `./design/art-direction/angus-visual-style-guide.md`。
- 父级 Codex 最终回复中应保留美术指导的核心判断和证据链；若原文较长，可使用 Markdown `<details><summary>美术指导诊断原文</summary>…</details>` 折叠，并在折叠块外单独写“我如何执行 / 已落地 / 未采纳或待确认”。用户明确要求极简摘要时，才可只给摘要。
- 如果当前 Codex 运行环境暂未暴露 `angus_art_director` 这个 agent 类型，则父级 Codex 必须按 `./skills/angus-art-director/SKILL.md` 在当前线程执行同等美术指导流程，不要把 `@美术指导` 等触发词当普通文本忽略。
- `angus_character_pixel_director`：项目级 Codex custom subagent，配置位于 `./.codex/agents/angus-character-pixel-director.toml`。当用户输入 `@像素美术`、`@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格`，或明确说“让像素美术 / 角色美术 / 像素角色子 agent 单独分析”“审一下这个角色像不像四人标杆图”“检查伪人嘴型 / 末日时钟表情”“把新角色放进 Angus 角色高清微像素风格”“写角色图 prompt”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `angus_character_pixel_director`，把角色需求、参考图路径、`角色设计风格规范-AI包`、四人标杆图和必要上下文传入；该 subagent 默认只做只读像素美术 / 角色美术风格守门，不直接改代码、不直接生成图片、不直接替代全局美术指导 / UI / UX / SIA / 制作人。
- `angus_character_pixel_director` 与其它 agent 的边界：全局 Angus 视觉方向、UI 包装、像素 / 半调 / 印刷材质仍由 `angus_art_director` 判断；角色高清微像素、四人标杆图一致性、伪人嘴型、末日时钟表情、新角色 DNA、角色 prompt 与生成后验收由 `angus_character_pixel_director` 判断；实际生图仍用 `openrouter-image-gen`；如果角色资产方向代表大量立绘、头像、外包量、人月或里程碑风险，再交 `game_producer`。当前角色美术真源为 `./角色设计风格规范-AI包/` 及 `./角色设计风格规范-AI包/reference/01-原始基准图.png`。
- 父级 Codex 最终回复中应保留像素美术专科的核心判断和证据链；若原文较长，可使用 Markdown `<details><summary>像素美术诊断原文</summary>…</details>` 折叠，并在折叠块外单独写“我如何执行 / 已落地 / 未采纳或待确认”。用户明确要求极简摘要时，才可只给摘要。
- 如果当前 Codex 运行环境暂未暴露 `angus_character_pixel_director` 这个 agent 类型，则父级 Codex 必须按 `./skills/angus-character-pixel-director/SKILL.md` 在当前线程执行同等像素美术 / 角色美术流程，不要把 `@像素美术` 等触发词当普通文本忽略。
- `game_producer`：项目级 Codex custom subagent，配置位于 `./.codex/agents/game-producer.toml`。当用户输入 `@制作人`，或明确说“让制作人子 agent 单独评估 / 制作人视角 / 立项评估 / 范围把关 / 里程碑检查 / greenlight / kill / 熔断评估”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `game_producer`，把相关 GDD 真源、用户提案、已有 SIA/UX/UI 结论、竞品来源和必要上下文传入；该 subagent 默认只做只读制作人闸门判断，不直接改代码、不直接设计 UI/系统/数值/叙事。完整工作流入口使用 `./skills/game-producer/SKILL.md`，上游完整 prompt 保存在 `./skills/game-producer/references/system-prompt-v1.1.md`。
- `game_producer` 不覆盖 `steam_indie_appraiser`：Steam 首屏、头图、capsule、宣传片前 10 秒、当前 demo 吸引力、垂直切片产品相、内容包诊断和功能 ROI 的 Steam 证据链仍优先交给 SIA；制作人只在需要 go / no-go、砍范围、里程碑、pivot 或生产风险判断时接手。
- `game_producer` 不插入每次 UI 设计默认链路：新 UI 仍按 `ui_designer` -> `ux_laoge`，已有 UI 改进仍按 `ux_laoge` -> `ui_designer`。只有当 UI 背后代表重大功能扩张、项目方向变化或里程碑风险时，父级才调用制作人做范围把关。
- 如果当前 Codex 运行环境暂未暴露 `game_producer` 这个 agent 类型，则父级 Codex 必须按 `./skills/game-producer/SKILL.md` 在当前线程执行同等制作人闸门判断，不要把 `@制作人` 当普通文本忽略。
- `game_sys_architect`：项目级 Codex custom subagent，配置位于 `./.codex/agents/game-sys-architect.toml`。当用户输入 `@系统架构`、`@系统架构师`、`@系统拆解`、`@架构审查`、`@系统注册`、`@资源流转`、`@耦合审查`，或明确说“让系统架构子 agent 单独分析 / 玩法系统架构 / 系统蓝图 / 依赖图 / 资源流图 / 核心循环到系统树”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `game_sys_architect`，把相关 GDD 真源、`systems-index.md`、制作人或用户 greenlight、用户提案、已有 SIA/数值/逻辑/UX/UI 结论和必要上下文传入；该 subagent 默认只做只读玩法系统架构，不直接改代码、不直接写文档、不做技术架构。完整工作流入口使用 `./skills/game-sys-architect/SKILL.md`，上游完整 prompt 保存在 `./skills/game-sys-architect/references/system-prompt-v1.0.md`。
- `game_sys_architect` 位于 `game_producer` 下游、系统设计/数值/逻辑审查上游：制作人决定是否值得做和做多大；系统架构师决定如果做，应放在哪个模块、和哪些系统交换什么、资源如何流转、耦合风险在哪里；`game_numerical` 再填具体公式/概率/参数，`game_logic_check` 再检查已成形规则漏洞。
- `game_sys_architect` 不替代 `map-systems`：它输出只读架构判断、系统注册表、依赖图和资源流；已确认结构若要落到 `design/gdd/systems-index.md`，由父级 Codex 或 `map-systems` 执行。它也不替代技术架构、系统细则设计、SIA、UX/UI 或代码评审。
- 如果当前 Codex 运行环境暂未暴露 `game_sys_architect` 这个 agent 类型，则父级 Codex 必须按 `./skills/game-sys-architect/SKILL.md` 在当前线程执行同等系统架构流程，不要把 `@系统架构` 当普通文本忽略。
- `game_numerical`：项目级 Codex custom subagent，配置位于 `./.codex/agents/game-numerical.toml`。当用户输入 `@数值策划`，或明确说“让数值策划子 agent 单独分析 / 数值策划 / 达标率校准 / 概率校准 / 难度曲线 / 任务目标值 / 骰面数值 / 黑骰反噬 / 周压力 / 发刊结算 / 势力或宏观属性参数 / 配表 / 平衡验证”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `game_numerical`，把相关 GDD 真源、当前公式、原型数据、用户体验目标和必要上下文传入；该 subagent 默认只做只读数值策划，不直接改代码、不直接替代系统设计。完整工作流入口使用 `./skills/game-numerical/SKILL.md`，上游完整 prompt 保存在 `./skills/game-numerical/references/system-prompt-v1.0.md`。
- `game_numerical` 默认只服务 Angus 主干数值：角色骰、达标率、任务目标值、黑骰反噬、周压力、势力任务、发刊结算、宏观属性、资源消耗与验证方案。Roguelite、卡牌、塔防、回合 RPG、MMO/F2P、商业手游等无关数值类型只作为按需资料库；商业/MMO/F2P 资料独立保存在 `./skills/game-numerical/references/commercial-mmo-f2p.md`，不得默认加载或混入 Angus 主干。
- `game_numerical` 不替代 `game_producer` 判断是否值得做，不替代 `steam_indie_appraiser` 判断 Steam 吸引力，不替代 `ux_laoge` 判断玩家是否看懂数字，不替代 `ui_designer` 设计数字呈现。已有数据异常审计可用 `balance-check`；需要重定公式、曲线和目标区间时再交 `game_numerical`。
- 如果当前 Codex 运行环境暂未暴露 `game_numerical` 这个 agent 类型，则父级 Codex 必须按 `./skills/game-numerical/SKILL.md` 在当前线程执行同等数值策划流程，不要把 `@数值策划` 当普通文本忽略。
- `game_logic_check`：项目级 Codex custom subagent，配置位于 `./.codex/agents/game-logic-check.toml`。当用户输入 `@逻辑审查`，或明确说“让逻辑审查子 agent 单独检查 / 逻辑检查 / 规则体检 / 状态机审查 / 因果闭环 / 边界条件 / 跨系统矛盾 / exploit 检查 / 叙事一致性检查 / 上线前规则防爆”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `game_logic_check`，把相关规则、GDD、配表、状态机、剧情时间线、代码片段和必要上下文传入；该 subagent 默认只做只读逻辑审查，不直接改代码、不直接设计系统。完整工作流入口使用 `./skills/game-logic-check/SKILL.md`，上游完整 prompt 保存在 `./skills/game-logic-check/references/system-prompt-v1.0.md`。
- `game_logic_check` 只在规则或内容已经成形后接入：适合审周循环、派遣/角色骰、黑骰、深度链、发刊结算、势力任务、宏观属性、资源流和叙事时间线。早期创意验证交 `game_producer`；文档完整性先用 `design-review`；概率/阈值交 `game_numerical`；玩家是否看懂交 `ux_laoge`；代码质量交 `code-review`。
- `game_logic_check` 在 Angus 中的 FATAL 包括：无限资源或奖励、核心流程卡死无法恢复、状态机或存档损坏、主线/核心玩法永久锁死、关键系统不可达、重复结算导致经济或世界状态崩坏。大型网游/手游的后端并发、防刷和断线重连默认降级，但本地存档一致性、重复点击、时间推进、阶段切换、重复结算、状态卡死和叙事矛盾仍必须检查。
- 如果当前 Codex 运行环境暂未暴露 `game_logic_check` 这个 agent 类型，则父级 Codex 必须按 `./skills/game-logic-check/SKILL.md` 在当前线程执行同等逻辑审查流程，不要把 `@逻辑审查` 当普通文本忽略。
- `steam_indie_appraiser`：项目级 Codex custom subagent，配置位于 `./.codex/agents/steam-indie-appraiser.toml`。当用户输入 `@SIA`、`@sia`、`@steam-appraiser`、`@独游鉴赏师`、`@Steam独游鉴赏师`、`@独游诊断`、`@Steam商店页诊断`、`@头图诊断`、`@宣传片诊断`、`@steam-indie-appraiser`，或明确说“让独立游戏鉴赏师 / Steam 鉴赏师 / 独游子 agent 单独分析”“作为独立游戏鉴赏师评价某个游戏”“看看近期 / 当前 Steam 新游戏中有哪些可借鉴样本”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `steam_indie_appraiser`，把游戏文档、截图/头图、商店页链接、宣传片链接、竞品问题和必要上下文传入；该 subagent 默认只做只读商业与设计诊断，不直接改代码、不直接生成图片。完整工作流入口使用 `./skills/steam-indie-appraiser/SKILL.md` 及其 `references/` 样本库与方法论文档。它也承担垂直切片产品把关、内容包诊断、Steam 首屏诊断和功能 ROI 评审。若任务涉及当前 / 近期 / 新发售 Steam 游戏、评价数、销量报道、商店页或公开视频，父级必须先联网验证并把来源传给子 agent。
- `steam_indie_appraiser` 的 `.codex/agents/steam-indie-appraiser.toml` 必须保持短启动壳：只保留稳定注册所需的英文短描述、英文 nickname 和“读取 `skills/steam-indie-appraiser/SKILL.md`”指令。不要把完整中文规程、长 description、中文 nickname 或 references 清单塞回 TOML；实测会导致 Codex Desktop 报 `agent type is currently not available`。完整能力只能补到 `skills/steam-indie-appraiser/SKILL.md` 与 `skills/steam-indie-appraiser/references/`。
- 父级 Codex 最终回复中应保留独游鉴赏师的核心判断和证据链；若原文较长，可使用 Markdown `<details><summary>独游鉴赏师诊断原文</summary>…</details>` 折叠，并在折叠块外单独写“我如何执行 / 已落地 / 未采纳或待确认”。用户明确要求极简摘要时，才可只给摘要。
- 如果当前 Codex 运行环境暂未暴露 `steam_indie_appraiser` 这个 agent 类型，则父级 Codex 必须按 `./skills/steam-indie-appraiser/SKILL.md` 在当前线程执行同等诊断，不要把 `@独游鉴赏师` 等触发词当普通文本忽略。
- Codemaker / brainmaker 的 `C:/Users/gzfangyue/AppData/Roaming/com.brainmaker.client/codemaker/.opencode-config/agents/` 配置不作为 Codex 调用依据；Codex 使用本仓库 `.codex/agents/` 与 `./skills/`。

### Available skills

- `ux-diagnosis`：Codex 版 UX 老哥诊断技能。别名/触发词包括 `@UX老哥`、`@ux老哥`、`@UX诊断`、`@ux诊断`、`@cowork-ux-diagnosis`、`界面硬伤`、`交互硬伤`、`P0/P1/P2`。用于结合 Angus 系统功能分析 UI 截图/原型界面，输出决策链、冲突扫描、P0/P1/P2 和改进建议；除非用户明确要求摘要，否则最终交付不得把完整 subagent 报告压缩成几条建议。（文件：`./skills/ux-diagnosis/SKILL.md`）
- `ux-kb-risks`、`ux-kb-cross-page`、`ux-kb-symptoms`、`ux-kb-principles`、`ux-kb-templates`：`ux-diagnosis` 的长尾辅助知识库。仅在对应触发条件下读取，不要默认全量加载。
- `ui-designer`：Codex 版 UI 设计子 agent 技能。别名/触发词包括 `@UI设计`、`@UI设计师`、`@ui-designer`、`@UI Designer`、`@UI出稿`、`@wireframe`、`@mock`，以及“从 brief 出 UI 方案 / 布局稿 / mock / 控件清单”。用于把需求文字转成元素对照表、桌面 16:9 布局 mock、质量验证报告和给 UX 老哥的交接摘要；不用于现有界面评审、P0/P1/P2 或直接改代码。（文件：`./skills/ui-designer/SKILL.md`）
- `angus-art-director`：Codex 版 Angus 像素艺术 / 美术指导子 agent 技能。别名/触发词包括 `@像素艺术`、`@美术指导`、`@美术总监`、`@ArtDirector`、`@art-director`、`@像素风美术`、`@视觉风格`、`@风格守门`、`@美术鉴赏师`，以及“像素风游戏美术鉴赏师”“审一下图像不像 Angus”“参考图转译”“视觉 prompt 指导”“风格跑偏诊断”等美术风格守门请求。用于审查 Angus 美术方向、美术资源、界面视觉风格、像素 / 半调 / 印刷材质用法、视觉 prompt 和参考图转译；不替代 UI Designer、UX 老哥、SIA、制作人、art-reference-picker 或 openrouter-image-gen。（文件：`./skills/angus-art-director/SKILL.md`）
- `angus-character-pixel-director`：Codex 版 Angus 角色高清微像素 / 像素美术专科技能。别名/触发词包括 `@像素美术`、`@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格`，以及四人标杆图一致性、眼镜记者、末日时钟、伪人、外星少女、新角色、角色头像、角色立绘、角色群像、角色表情、角色 prompt 审查等请求。用于以 `./角色设计风格规范-AI包/` 和四人标杆图为真源，审查或规划角色高清微像素、Q 版比例、伪人嘴型、末日时钟表情、新角色 DNA、角色生图 prompt 和生成后验收；不替代 Angus Art Director 的全局美术方向、openrouter-image-gen 的实际生图、UI/UX、SIA 或制作人。（文件：`./skills/angus-character-pixel-director/SKILL.md`）
- `game-producer`：Codex 版制作人子 agent 技能。触发词为 `@制作人`，也适用于用户明确要求制作人视角做立项评估、重大功能范围把关、greenlight / kill、熔断判断、项目里程碑复盘或制作人竞品分析。用于判断是否继续投入、是否砍范围、下一里程碑验证什么；不用于 Steam 商店页 / 头图 / 宣传片 / 垂直切片吸引力诊断，也不插入每次 UI 设计链路。（文件：`./skills/game-producer/SKILL.md`）
- `game-sys-architect`：Codex 版系统架构子 agent 技能。触发词为 `@系统架构`，也适用于系统架构师、系统拆解、架构审查、系统注册、资源流转、依赖图、耦合审查、核心循环到系统树或重大新系统放置方案。用于只读输出系统蓝图、边界、依赖、资源流和健康检查；不用于技术架构、具体规则、数值、UI/UX、Steam 诊断或 `systems-index.md` 文档落盘。（文件：`./skills/game-sys-architect/SKILL.md`）
- `game-numerical`：Codex 版数值策划子 agent 技能。触发词为 `@数值策划`，也适用于达标率校准、概率校准、难度曲线、任务目标值、骰面数值、黑骰反噬、周压力、发刊结算、势力/宏观属性参数、资源消耗、配表和平衡验证。默认只服务 Angus 主干数值；Roguelite、卡牌、塔防、回合 RPG、MMO/F2P、商业手游等只作为按需资料库，不干扰 Angus 数值设计主干。（文件：`./skills/game-numerical/SKILL.md`）
- `game-logic-check`：Codex 版逻辑审查子 agent 技能。触发词为 `@逻辑审查`，也适用于逻辑检查、规则体检、状态机审查、因果闭环、边界条件、跨系统矛盾、exploit 检查、叙事一致性检查或上线前规则防爆。用于已成形规则、GDD、配表、状态机、剧情时间线或实现片段的只读审查；不用于早期创意设计、数值调优、UI/UX 评审或代码质量评审。（文件：`./skills/game-logic-check/SKILL.md`）
- `steam-indie-appraiser`：Steam 独立游戏鉴赏师技能。别名/触发词包括 `@SIA`、`@sia`、`@steam-appraiser`、`@独游鉴赏师`、`@Steam独游鉴赏师`、`@独游诊断`、`@Steam商店页诊断`、`@头图诊断`、`@宣传片诊断`、`@steam-indie-appraiser`、`Steam 小爆款标准`、`垂直切片诊断`、`内容包诊断`、`功能 ROI`、“作为独立游戏鉴赏师评价某个游戏”、“近期 / 当前 Steam 新游戏可借鉴样本”。用于评估独立游戏第一眼吸引力、小爆款潜力、系统性价比、Steam 头图 / capsule、截图顺序、宣传片前 10 秒、当前 demo 产品吸引力、任务内容包质量、功能阶段取舍和 Angus 竞品对照；需要最新商店页、销量、评价或公开视频时必须联网验证。（文件：`./skills/steam-indie-appraiser/SKILL.md`）
- `art-reference-picker`：审阅 Angus 项目的本地美术参考图，与项目文档对照后挑出最相关的图片，并给出具体适配原因。适用于分析已下载截图、为当前 UI 或美术需求挑选最佳参考、解释项目关联性、归档入选图片，或把选中的图片及理由发送到飞书群。（文件：`./skills/art-reference-picker/SKILL.md`）
- `claude-to-im`：把当前 Codex 或 Claude Code 会话桥接到 Telegram、Discord、飞书/Lark 或 QQ，让用户能从手机继续聊天，并可复用内置飞书发送脚本做一次性文本或图片发送。别名/触发词包括：`claude to im`、`claude_to_im`、`bridge`、`start bridge`、`restart bridge`、`bridge status`、`bridge logs`、`send to feishu`、`post to feishu`。用于桥接服务的配置、启动、停止、重启、状态检查、日志排障，以及从仓库文件做一次性飞书发送；不用于单独开发 IM Bot 或直接操作 IM 平台 SDK。（文件：`./skills/claude-to-im/SKILL.md`）
- `openrouter-image-gen`：通过 OpenRouter 图像模型生成、编辑或规划可直接用于游戏的图片资产，包括 GPT-5 Image 透明 PNG/WebP 工作流，以及 Nano Banana / Nano Banana 2 的不透明图工作流。别名/触发词包括：`openrouter image gen`、`openrouter 生图`、`nano banana`、`nano banana 2`、`gpt-5 image transparent`、`参考图生图`、`openrouter image`、`or image gen`。适用于基于 OpenRouter 的图像生成、透明背景素材切图、参考图编辑、图标、道具、贴图、精灵、海报、主视觉、UI 横幅、角色立绘、环境图等需求。（文件：`./skills/openrouter-image-gen/SKILL.md`）
- `psd-to-godot-ui`：把 Photoshop PSD 转成可复用的 Godot UI 资产包，包含复制后的 PSD 源文件、导出的图层 PNG、扁平预览图、manifest，以及一个以 `Control` 为根节点、可被后续场景实例化的 `.tscn` 场景。适用于导入 PSD 方案稿、验证 PSD 到 Godot UI 的导入链路、PSD 改动后重新生成 UI 场景，或提前整理后续会接入游戏的 UI 美术。（文件：`./skills/psd-to-godot-ui/SKILL.md`）
- 导入自 Claude Code Game Studios 的流程现在都以项目本地 Codex 技能形式存在于 `./skills/<skill-name>/SKILL.md`。当用户直接提到某个技能，或请求匹配的游戏制作工作流时，应使用对应技能。
- 评审与分析类：`asset-audit`、`balance-check`、`code-review`、`design-review`、`gate-check`、`perf-profile`、`project-stage-detect`、`scope-check`、`tech-debt`。
- 规划、文档与发布类：`architecture-decision`、`bug-report`、`changelog`、`estimate`、`hotfix`、`launch-checklist`、`milestone-review`、`onboard`、`patch-notes`、`release-checklist`、`retrospective`、`reverse-document`、`setup-engine`、`sprint-plan`、`start`。
- 设计与前期制作类：`brainstorm`、`design-system`、`localize`、`map-systems`、`playtest-report`、`prototype`。
- 团队协同类：`team-audio`、`team-combat`、`team-level`、`team-narrative`、`team-polish`、`team-release`、`team-ui`。
- 图像与资产辅助类：`openrouter-image-gen`、`reply-image-context`、`svg-to-png`。

### How to use skills

- 如果用户明确提到某个技能，打开对应 `SKILL.md` 并按其说明执行。
- 识别明显别名为直接点名技能。对 `ux-diagnosis`，包括 `@UX老哥`、`@ux老哥`、`@UX诊断`、`@ux诊断`、`@cowork-ux-diagnosis`、`界面硬伤`、`交互硬伤`、`P0/P1/P2` 等 UX 诊断请求。若用户使用 `@UX老哥` 等形式，优先按上方 `Codex Subagents` 规则调用 `ux_laoge`；调用不了时在当前线程按该技能执行。
- 识别明显别名为直接点名技能。对 `ui-designer`，包括 `@UI设计`、`@UI设计师`、`@ui-designer`、`@UI Designer`、`@UI出稿`、`@wireframe`、`@mock`，以及从 brief 出 UI 方案 / 布局稿 / mock / 控件清单等请求。若用户使用这些形式且语义是调用 UI 设计子 agent，优先按上方 `Codex Subagents` 规则调用 `ui_designer`；调用不了时在当前线程按该技能执行。任何 UI 设计落地前仍需按顶层规则让 `ux_laoge` 参与评审。
- 识别明显别名为直接点名技能。对 `angus-art-director`，包括 `@像素艺术`、`@美术指导`、`@美术总监`、`@ArtDirector`、`@art-director`、`@像素风美术`、`@视觉风格`、`@风格守门`、`@美术鉴赏师`、“像素风游戏美术鉴赏师”“美术资源把关”“界面视觉风格把关”“参考图转译”“视觉 prompt 指导”“风格跑偏诊断”等请求。若语义是调用像素艺术 / 美术指导子 agent，优先按上方 `Codex Subagents` 规则调用 `angus_art_director`；调用不了时在当前线程按该技能执行。不得用它替代 SIA 的 Steam 吸引力判断、UX 老哥的可读性诊断、UI Designer 的布局设计、制作人的范围判断或 openrouter-image-gen 的实际生图。
- 识别明显别名为直接点名技能。对 `angus-character-pixel-director`，包括 `@像素美术`、`@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格`、四人标杆图一致性、眼镜记者、末日时钟、伪人、外星少女、新角色、角色头像、角色立绘、角色群像、角色表情、角色 prompt 审查等请求。若语义是调用像素美术 / 角色高清微像素子 agent，优先按上方 `Codex Subagents` 规则调用 `angus_character_pixel_director`；调用不了时在当前线程按该技能执行。不得用它替代 `angus_art_director` 的全局美术风格判断、`openrouter-image-gen` 的实际生图、UI/UX、SIA 或制作人的范围判断。
- 识别明显别名为直接点名技能。对 `game-producer`，触发词为 `@制作人`；用户明确要求制作人视角、立项评估、范围把关、里程碑检查、greenlight / kill 或熔断评估时也可使用。若语义是调用制作人子 agent，优先按上方 `Codex Subagents` 规则调用 `game_producer`；调用不了时在当前线程按该技能执行。不得用它覆盖 SIA 的 Steam 诊断，也不得让它默认插入每次 UI 设计。
- 识别明显别名为直接点名技能。对 `game-sys-architect`，触发词为 `@系统架构`；用户明确要求系统架构师、系统拆解、架构审查、系统注册、资源流转、依赖图、耦合审查、核心循环到系统树或重大新系统放置方案时也可使用。若语义是调用系统架构子 agent，优先按上方 `Codex Subagents` 规则调用 `game_sys_architect`；调用不了时在当前线程按该技能执行。该 agent 只读，不替代制作人、数值、逻辑审查、UX/UI、技术架构或 `map-systems` 文档落盘。
- 识别明显别名为直接点名技能。对 `game-numerical`，触发词为 `@数值策划`；用户明确要求数值策划、达标率校准、概率校准、难度曲线、任务目标值、骰面数值、黑骰反噬、周压力、发刊结算、势力/宏观属性参数、配表或平衡验证时也可使用。若语义是调用数值策划子 agent，优先按上方 `Codex Subagents` 规则调用 `game_numerical`；调用不了时在当前线程按该技能执行。不得默认加载商业/MMO/F2P 资料，也不得把与 Angus 无关的数值类型混入 Angus 主干数值设计。
- 识别明显别名为直接点名技能。对 `game-logic-check`，触发词为 `@逻辑审查`；用户明确要求逻辑检查、规则体检、状态机审查、因果闭环、边界条件、跨系统矛盾、exploit 检查、叙事一致性检查或上线前规则防爆时也可使用。若语义是调用逻辑审查子 agent，优先按上方 `Codex Subagents` 规则调用 `game_logic_check`；调用不了时在当前线程按该技能执行。该 agent 只读，不替代设计、数值、UX/UI 或 code-review。
- 识别明显别名为直接点名技能。对 `steam-indie-appraiser`，包括 `@SIA`、`@sia`、`@steam-appraiser`、`@独游鉴赏师`、`@Steam独游鉴赏师`、`@独游诊断`、`@Steam商店页诊断`、`@头图诊断`、`@宣传片诊断`、`@steam-indie-appraiser`、`Steam 小爆款标准`、`垂直切片诊断`、`内容包诊断`、`功能 ROI`、“作为独立游戏鉴赏师评价某个游戏”、“近期 / 当前 Steam 新游戏可借鉴样本”等商业与竞品诊断请求。若用户使用这些形式且语义是调用独游子 agent，优先按上方 `Codex Subagents` 规则调用 `steam_indie_appraiser`；调用不了时在当前线程按该技能执行。
- 识别明显别名为直接点名技能。对 `claude-to-im`，包括 `claude to im`、`claude_to_im`、`bridge`、`start bridge`、`restart bridge`、`bridge status`、`bridge logs` 等桥接管理请求。
- 识别明显别名为直接点名技能。对 `openrouter-image-gen`，包括 `openrouter image gen`、`openrouter 生图`、`openrouter image`、`or image gen`、`nano banana`、`nano banana 2`、`gpt-5 image transparent`、`透明背景生图`、`参考图生图` 等相关图像生成请求。
- 识别明显别名为直接点名技能。对 `psd-to-godot-ui`，包括 `psd to godot ui`、`import psd`、`psd ui`、`photoshop ui import` 等 PSD 转 Godot UI 请求。
- 相对路径优先从技能目录解析。
- 导入的 game-studio 技能共用模板位于 `./skills/_game-studio-shared/templates`。
- 本工作区共享的桥接配置、日志和状态位于 `./skills/.claude-to-im`，除非 `CTI_HOME` 覆盖该位置。

## Obsolete Content

`./_obsolete/` 是仓库的过期材料墓地，用来存放已失效、被替代或仅供审计的内容。

适用于所有 AI 代理的规则：

- 浏览仓库时默认跳过 `./_obsolete/`。
- 不要把 `./_obsolete/` 当作代码、设计、资产、需求或流程的真实来源。
- 除非用户明确要求做历史查询、恢复或比对，否则不要引用、总结、迁移或更新 `./_obsolete/` 下的文件。
- 如果 `./_obsolete/` 中内容与现行文档或代码冲突，始终忽略 `_obsolete/` 版本。
- 当你新增归档内容时，在对应归档子目录补一个简短 README，说明其被废弃的原因。

## 文档与落盘语言规则

- 除非用户明确要求英文或双语，所有新建或更新后会落盘到仓库中的说明性文本，默认使用简体中文。
- 该规则覆盖 `README`、GDD、ADR、计划、规格、交接、报告、分析、清单、`*.md`、`*.txt` 等文档型文件。
- 代码、路径、文件名、命令、配置键、API 字段、类名、脚本名、外部产品官方名称、许可证原文和其他机器约定标记可保留英文；但正文说明应优先使用中文。
- 如果要修改现有英文文档，优先把原文整体翻译成中文，不要只在英文文件末尾追加一段中文。
- 如果技能或模板示例里给的是英文标题、英文段落或英文表头，真正写入仓库时必须先转成中文再落盘。
- 仅供机器读取的单值文件可保留既有约定，例如 `production/stage.txt` 这类阶段标记，除非用户明确要求本地化。
