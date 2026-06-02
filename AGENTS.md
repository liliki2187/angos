## 设计文档（正式真源）

- **顶层真源**：[`design/gdd/core-experience.md`](./design/gdd/core-experience.md)、[`design/gdd/game-concept.md`](./design/gdd/game-concept.md)、[`design/gdd/game-pillars.md`](./design/gdd/game-pillars.md)、[`design/gdd/gameplay-design-principles.md`](./design/gdd/gameplay-design-principles.md)、[`design/gdd/systems-index.md`](./design/gdd/systems-index.md)。
- **同步**：已确定并落地的玩法/规则/常量变更，应先同步对应 `design/gdd/` 文档；若影响产品定位、支柱或系统边界，再同步顶层三份文档。与系统全貌、全链原型对照相关的章节仍应同步 [`docs/archive/legacy-design/系统功能设计总集.md`](./docs/archive/legacy-design/系统功能设计总集.md)（或后续替代真源）中相应段落与 §13、§14。
- **归档提醒**：[`docs/archive/legacy-design/系统功能设计总集.md`](./docs/archive/legacy-design/系统功能设计总集.md) 为归档副本，与当前 `design/gdd/` 并行时以 `design/gdd/` 与代码为准，并在此总集注明差异。
- **出入提醒**：若代码/配置与上述文档不一致，助手在改完或评审时应**明确提醒**用户：择一修正文档或实现。
- **协作偏好**：后续 AI / 新对话在处理玩法、原型、UI 感知类任务前，先读 [`docs/onboarding/ai-collaboration-guidance.md`](./docs/onboarding/ai-collaboration-guidance.md)；若涉及 UI、交互、原型呈现或视觉实验页，还必须读取并执行 [`docs/onboarding/ui-interaction-guidelines.md`](./docs/onboarding/ui-interaction-guidelines.md)；收到新的强反馈后应按分工同步更新对应文档。
- **桌面 UI 顶层硬规则**：Angus 当前完全不做移动版。后续游戏 UI、HTML/Godot 原型、视觉实验页和截图验收默认只面向桌面 16:9；不得主动设计移动端、触屏版、窄屏版或移动端断点，也不得把移动端截图作为默认交付项。只有用户在当前任务里明确要求移动端时，才可作为一次性例外处理，并需说明不改变此顶层规则。
- **改动截图交付**：后续每次游戏/原型有可见改动，交付时必须附上改动部分的真实截图与文字说明；1-3 张截图可直接在对话里展示，超过 3 张再整理汇总页；截图方法优先按 [`docs/onboarding/功能改动截图指引.md`](./docs/onboarding/功能改动截图指引.md) 执行，避免让用户逐张翻找或自行对照。
- **设计采纳沉淀**：用户在讨论中明确采纳 / 待定 / 进阶 / 撤回的设计意见，统一沉淀到 [`docs/设计采纳记录.md`](./docs/设计采纳记录.md)。每次讨论中只要出现新的明确表态，AI 必须在当次回复结束前把对应条目追加进该文档；不主动塞 AI 单方面设想；用户后续撤回/调整时保留原条目并标注修订时间，不要直接覆盖。详细写入规则见该文件头部「附录 · 用法说明」。
- **Subagent 能力沉淀**：后续完善 `ux_laoge`、`steam_indie_appraiser` 等 subagent 时，按 [`docs/onboarding/subagent-collaboration-improvement.md`](./docs/onboarding/subagent-collaboration-improvement.md) 分层处理：项目级硬规则进 `AGENTS.md` / `docs/onboarding/`；subagent 自身流程进对应 `SKILL.md`；普通实战案例进 `skills/<skill>/references/casebook/`；`.codex/agents/*.toml` 保持短启动壳。

## Skills

Angus 的项目本地技能位于 `./skills`。
优先使用这些工作区内副本，而不是 `$CODEX_HOME/skills` 下的重复安装版本。

## Codex Subagents

- `ux_laoge`：项目级 Codex custom subagent，配置位于 `./.codex/agents/ux-laoge.toml`。当用户输入 `@UX老哥`、`@ux老哥`、`@UX诊断`、`@ux诊断`、`@cowork-ux-diagnosis`，或明确说“让 UX 老哥 / UX 子 agent 单独分析”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `ux_laoge`，把截图、问题描述、相关文件路径和必要上下文传入；该 subagent 默认只做只读 UX 诊断，不直接改代码。完整 UX 诊断主 spec 使用 `./skills/ux-diagnosis/system-prompt-v2.2.md`，这是从 portable 包 `core/system-prompt.md` 同步的上游核心；不要用 portable 包的 `adapters/codex/AGENTS.md` 覆盖本项目根 `AGENTS.md`。
- 父级 Codex 最终回复中必须保留 UX 老哥意见正文，不得只给结果或改写摘要。若篇幅较长，应使用 Markdown `<details><summary>UX 老哥诊断原文</summary>…</details>` 做成可折叠内容；折叠块外再单独写“我如何执行 / 已落地 / 未采纳或待确认”。用户明确要求极简摘要时，才可只给摘要，但仍应说明完整诊断可展开或可补发。
- 如果当前 Codex 运行环境暂未暴露 `ux_laoge` 这个 agent 类型，则父级 Codex 必须按 `./skills/ux-diagnosis/SKILL.md` 在当前线程执行同等诊断，不要把 `@UX老哥` 当普通文本忽略。
- `steam_indie_appraiser`：项目级 Codex custom subagent，配置位于 `./.codex/agents/steam-indie-appraiser.toml`。当用户输入 `@SIA`、`@sia`、`@steam-appraiser`、`@独游鉴赏师`、`@Steam独游鉴赏师`、`@独游诊断`、`@Steam商店页诊断`、`@头图诊断`、`@宣传片诊断`、`@steam-indie-appraiser`，或明确说“让独立游戏鉴赏师 / Steam 鉴赏师 / 独游子 agent 单独分析”“作为独立游戏鉴赏师评价某个游戏”“看看近期 / 当前 Steam 新游戏中有哪些可借鉴样本”时，视为用户显式要求调用该 subagent。父级 Codex 应 spawn `steam_indie_appraiser`，把游戏文档、截图/头图、商店页链接、宣传片链接、竞品问题和必要上下文传入；该 subagent 默认只做只读商业与设计诊断，不直接改代码、不直接生成图片。完整工作流入口使用 `./skills/steam-indie-appraiser/SKILL.md` 及其 `references/` 样本库与方法论文档。它也承担垂直切片产品把关、内容包诊断、Steam 首屏诊断和功能 ROI 评审。若任务涉及当前 / 近期 / 新发售 Steam 游戏、评价数、销量报道、商店页或公开视频，父级必须先联网验证并把来源传给子 agent。
- `steam_indie_appraiser` 的 `.codex/agents/steam-indie-appraiser.toml` 必须保持短启动壳：只保留稳定注册所需的英文短描述、英文 nickname 和“读取 `skills/steam-indie-appraiser/SKILL.md`”指令。不要把完整中文规程、长 description、中文 nickname 或 references 清单塞回 TOML；实测会导致 Codex Desktop 报 `agent type is currently not available`。完整能力只能补到 `skills/steam-indie-appraiser/SKILL.md` 与 `skills/steam-indie-appraiser/references/`。
- 父级 Codex 最终回复中应保留独游鉴赏师的核心判断和证据链；若原文较长，可使用 Markdown `<details><summary>独游鉴赏师诊断原文</summary>…</details>` 折叠，并在折叠块外单独写“我如何执行 / 已落地 / 未采纳或待确认”。用户明确要求极简摘要时，才可只给摘要。
- 如果当前 Codex 运行环境暂未暴露 `steam_indie_appraiser` 这个 agent 类型，则父级 Codex 必须按 `./skills/steam-indie-appraiser/SKILL.md` 在当前线程执行同等诊断，不要把 `@独游鉴赏师` 等触发词当普通文本忽略。
- Codemaker / brainmaker 的 `C:/Users/gzfangyue/AppData/Roaming/com.brainmaker.client/codemaker/.opencode-config/agents/` 配置不作为 Codex 调用依据；Codex 使用本仓库 `.codex/agents/` 与 `./skills/`。

### Available skills

- `ux-diagnosis`：Codex 版 UX 老哥诊断技能。别名/触发词包括 `@UX老哥`、`@ux老哥`、`@UX诊断`、`@ux诊断`、`@cowork-ux-diagnosis`、`界面硬伤`、`交互硬伤`、`P0/P1/P2`。用于结合 Angus 系统功能分析 UI 截图/原型界面，输出决策链、冲突扫描、P0/P1/P2 和改进建议；除非用户明确要求摘要，否则最终交付不得把完整 subagent 报告压缩成几条建议。（文件：`./skills/ux-diagnosis/SKILL.md`）
- `ux-kb-risks`、`ux-kb-cross-page`、`ux-kb-symptoms`、`ux-kb-principles`、`ux-kb-templates`：`ux-diagnosis` 的长尾辅助知识库。仅在对应触发条件下读取，不要默认全量加载。
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
