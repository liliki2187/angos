## 设计文档（正式真源）

- **顶层真源**：[`design/gdd/core-experience.md`](./design/gdd/core-experience.md)、[`design/gdd/game-concept.md`](./design/gdd/game-concept.md)、[`design/gdd/game-pillars.md`](./design/gdd/game-pillars.md)、[`design/gdd/gameplay-design-principles.md`](./design/gdd/gameplay-design-principles.md)、[`design/gdd/systems-index.md`](./design/gdd/systems-index.md)。
- **同步**：已确定并落地的玩法/规则/常量变更，应先同步对应 `design/gdd/` 文档；若影响产品定位、支柱或系统边界，再同步顶层三份文档。与系统全貌、全链原型对照相关的章节仍应同步 [`docs/archive/legacy-design/系统功能设计总集.md`](./docs/archive/legacy-design/系统功能设计总集.md)（或后续替代真源）中相应段落与 §13、§14。
- **归档提醒**：[`docs/archive/legacy-design/系统功能设计总集.md`](./docs/archive/legacy-design/系统功能设计总集.md) 为归档副本，与当前 `design/gdd/` 并行时以 `design/gdd/` 与代码为准，并在此总集注明差异。
- **出入提醒**：若代码/配置与上述文档不一致，助手在改完或评审时应**明确提醒**用户：择一修正文档或实现。
- **协作偏好**：后续 AI / 新对话在处理玩法、原型、UI 感知类任务前，先读 [`docs/onboarding/ai-collaboration-guidance.md`](./docs/onboarding/ai-collaboration-guidance.md)；若涉及 UI、交互、原型呈现或视觉实验页，还必须读取并执行 [`docs/onboarding/ui-interaction-guidelines.md`](./docs/onboarding/ui-interaction-guidelines.md)；收到新的强反馈后应按分工同步更新对应文档。
- **桌面 UI 顶层硬规则**：Angus 当前完全不做移动版。后续游戏 UI、HTML/Godot 原型、视觉实验页和截图验收默认只面向桌面 16:9；不得主动设计移动端、触屏版、窄屏版或移动端断点，也不得把移动端截图作为默认交付项。只有用户在当前任务里明确要求移动端时，才可作为一次性例外处理，并需说明不改变此顶层规则。
- **UI 设计双 agent 顶层规则**：后续每次做 UI 设计、布局方案、wireframe、mock 或可见原型落地前，默认让 `ui_designer` 与 `ux_laoge` 都参与并互相校验。新 UI / 从 brief 出稿先走 `ui_designer`，再交 `ux_laoge` 评审；改进现有 UI 先走 `ux_laoge` 诊断，再交 `ui_designer` 出改进稿；父级 Codex 负责合并意见、说明冲突，并在落地前把分歧交给用户裁决。
- **制作人子 agent 顶层规则**：`@制作人` 调用 `game_producer`，做立项评估、范围把关、greenlight / kill、里程碑复盘和熔断判断；不覆盖 SIA 的 Steam 诊断，不默认插入 UI 设计链路。细则见 [`skills/game-producer/SKILL.md`](./skills/game-producer/SKILL.md)。
- **系统架构子 agent 顶层规则**：`@系统架构` 调用 `game_sys_architect`，只读输出玩法系统蓝图、依赖图、资源流和耦合审查；不做技术架构、不写规则、不填数值、不替代 `map-systems` 落盘。细则见 [`skills/game-sys-architect/SKILL.md`](./skills/game-sys-architect/SKILL.md)。
- **数值策划子 agent 顶层规则**：`@数值策划` 调用 `game_numerical`，服务 Angus 主干数值（角色骰、达标率、黑骰反噬、发刊结算、配表与验证方案）；Roguelite / 卡牌 / MMO / F2P 等外部数值类型只作按需资料库，商业资料仅显式触发时读取。细则见 [`skills/game-numerical/SKILL.md`](./skills/game-numerical/SKILL.md)。
- **逻辑审查子 agent 顶层规则**：`@逻辑审查` 调用 `game_logic_check`，对已成形规则、GDD、配表、状态机、剧情时间线做只读防爆审查（exploit、因果闭环、边界、跨系统矛盾）；不做设计、不改文件，不在早期头脑风暴默认调用。细则见 [`skills/game-logic-check/SKILL.md`](./skills/game-logic-check/SKILL.md)。
- **冷备 subagent 冻结与解冻提醒顶层规则**：自 2026-07-08 起，`game_producer`、`game_sys_architect`、`game_numerical`、`game_logic_check` 四个 subagent 处于冷备冻结状态：注册壳与技能保留，用户显式触发词调用时仍正常执行，但 AI 不再为它们新增规则、扩写 SKILL.md、补 references 或 casebook，也不主动 spawn 参与常规任务。用户无法自行判断解冻时机，因此 AI 负有解冻提醒义务：任务中一旦识别到某冷备 agent 的价值窗口（触发条件表见 [`docs/onboarding/subagent-collaboration-improvement.md`](./docs/onboarding/subagent-collaboration-improvement.md) §8），必须当场用一句话主动提醒用户“该场景命中冷备 agent X 的解冻条件，建议解冻”，说明理由并给出不解冻的替代方案；不得默默替代其职责而不提醒，也不得因时间久远忘记冻结状态。解冻需用户确认，确认后从本条冷备名单移除并同步 §8 冻结表。
- **改动截图交付**：后续每次游戏/原型有可见改动，交付时必须附上改动部分的真实截图与文字说明；1-3 张截图可直接在对话里展示，超过 3 张再整理汇总页；截图方法优先按 [`docs/onboarding/功能改动截图指引.md`](./docs/onboarding/功能改动截图指引.md) 执行，避免让用户逐张翻找或自行对照。
- **动态效果交付硬规则**：后续凡涉及 UI 动效、2D/3D 角色动作、骰子 / 特效 / 转场、可交互美术小组件或任何需要判断时间节奏、物理感、停顿、反馈强弱的内容，交付时必须附真实动图或视频（GIF / animated WebP / MP4 / WebM 之一）供用户审核；静态截图只能作为关键帧和问题定位补充，不能替代动态演示。若技术环境暂时无法导出动图或视频，必须明确说明原因，并提供可运行的本地播放页或逐帧导出方案作为临时替代。
- **生图请求硬规则**：后续用户说“生图 / 生成图片 / 再生一张 / 生张大图”等时，默认必须调用真实生图工具或图像生成模型（如 `openrouter-image-gen` / `$imagegen`），不得用 SVG、Canvas、HTML/CSS、PowerShell、C# `System.Drawing`、脚本绘图或程序化色卡冒充“生图”。只有用户明确要求“程序画 / 示意图 / 结构板 / 色卡表 / 可编辑模板 / 不用生图模型”时，才可改用程序生成；若需要精确文字层、拼版或 QA，可在生图后用程序合成与校验，但必须说明程序只负责排版 / 文字 / 检测，不替代图像生成。
- **设计采纳沉淀**：用户在讨论中明确采纳 / 待定 / 进阶 / 撤回的设计意见，先登记到 [`docs/设计采纳记录.md`](./docs/设计采纳记录.md) 总索引，并按该索引的跨分类检索保护写入 [`docs/design-decisions/`](./docs/design-decisions/) 对应分册。每次讨论中只要出现新的明确表态，AI 必须在当次回复结束前更新总索引与主分册；不主动塞 AI 单方面设想；用户后续撤回/调整时保留原条目并标注修订时间，不要直接覆盖。若意见跨 UI / 机制 / 美术 / 流程，必须在索引补 cross-read tags，避免后续漏读。详细写入规则见总索引「写入规则」。
- **Workflow harness / loop 渐进规则**：后续 normal 以上复杂任务、可见 UI/美术/玩法任务、资产化 UI、生图、主流程改动或生产候选交付前，优先按 [`docs/workflows/angus-workflow-harness.md`](./docs/workflows/angus-workflow-harness.md) 使用 Router Card、Delivery Manifest 和分级 gate；只有在 workflow gate、Loop Log、是否通过判断、卡住/返工/需要裁决等场景，回馈第一屏才使用三行决策条：`结论 / 影响 / 下一步`。普通解释、讨论、完成汇报和轻量问答必须回到自然语言，不得把决策条、Human Brief、Router / gate / agent 术语泛化成所有回复的固定格式。用户说“这次错在 / 复盘 / 怎么避免 / 先别落地 / 不改文件 / 进错题本 / 转成 eval case”，或父级自检发现阶段、产物、证据、agent、可读性或实现范围误判时，必须自动触发 Loop Log，不能只道歉。tiny typo / 明显小 bug 可轻量跳过，但需在最终说明。不得用 checklist、agent/gate 名称或模板字段代替结论，不得把轻量 harness 误用成所有任务强制多 agent 会审；risky / production 任务才进入 hard gate。
- **Git 云端提交固定工作流**：用户要求盘点、暂存、提交、推送、多远端同步或跨端无缝衔接时，必须读取并执行 [`skills/git-cloud-submit/SKILL.md`](./skills/git-cloud-submit/SKILL.md)。所有未入 Git 的相关内容必须完成 handoff 分类；“不提交”不等于“不同步”，存在 `UNKNOWN` 或仅存本机的必需内容时不得声称无缝交接。模型顺序固定为 Sol（最高能力）> Terra（默认协调）> Luna（最快、最低成本）；完整分工、Gate、授权边界和运行时回退只在该技能维护，不在顶层重复。
- **像素艺术 / 美术指导子 agent 顶层规则**：`@像素艺术` 是 `angus_art_director` 的全局美术资源与界面视觉风格把关触发词；`@美术指导`、美术总监、ArtDirector、像素风美术、视觉风格、风格守门、美术鉴赏师等也调用同一 subagent。后续 Angus 的美术资源、UI 视觉包装、像素 / 半调 / 印刷材质、参考图转译、视觉 prompt 和风格跑偏诊断，默认先让 `@像素艺术` 做只读风格守门；它不直接生图、不直接改 UI / 代码、不替代 `ui_designer`、`ux_laoge`、`steam_indie_appraiser`、`game_producer`、`art-reference-picker` 或 `openrouter-image-gen`。当前正式美术风格以 [`design/art-direction/angus-visual-style-guide.md`](./design/art-direction/angus-visual-style-guide.md) 为准；角色高清微像素细则仍由 `angus_character_pixel_director` 与四人标杆图负责。**临时例外（2026-07-13）**：以 `benchmark-board-01.png`、`benchmark-board-02.png` 为真值的 `clean low-poly weekly` 支线暂不自动调用 `angus_art_director`，避免其旧像素 / 半调默认坐标系反向牵引新标杆；细则见 [`docs/onboarding/subagent-collaboration-improvement.md`](./docs/onboarding/subagent-collaboration-improvement.md) §3。
- **像素艺术生成后复审规则**：除上述 `clean low-poly weekly` 临时例外外，任何 UI 风格稿、美术资源包、界面元素风格稿或生图结果，若要被称为“生产标杆 / 资源标杆 / 真源候选”，必须在生成后再交 `@像素艺术` 复审。复审必须显式检查像素颗粒度、颗粒密度、半调 / 套印是否成为结构语言、是否继承当前标杆图，以及是否滑向旧报纸、旧档案、泛黄纸噪点或高清摄影噪声；未通过的图只能归档为偏差案例或灵感草稿。`clean low-poly weekly` 支线改由标杆原图、支线风格规范、纸张 / 色彩合同、UI / UX 与父级逐项对照共同放行；未完成该直接标杆复审时同样不得升格。
- **像素美术子 agent 顶层规则**：`@像素美术` 是 `angus_character_pixel_director` 调用触发词，也适用于 `@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格`，以及眼镜记者、末日时钟、伪人、外星少女、新角色、角色头像、角色立绘、角色群像、角色表情、四人标杆图一致性、角色 prompt 审查等请求。当前角色 / 主编 / 编辑正式方向是高清微像素 Q 版角色；以 [`角色设计风格规范-AI包`](./角色设计风格规范-AI包) 及其四人标杆图 [`reference/01-原始基准图.png`](./角色设计风格规范-AI包/reference/01-原始基准图.png) 为角色美术真源。它默认只读，不直接生图、不直接改 UI / 代码、不替代 `angus_art_director` 的全局美术方向、`openrouter-image-gen` 的实际生图、`ui_designer` / `ux_laoge` 的 UI/UX、`steam_indie_appraiser` 的 Steam 吸引力或 `game_producer` 的资产范围判断。
- **Subagent 能力沉淀**：后续完善 `ux_laoge`、`ui_designer`、`angus_art_director`、`angus_character_pixel_director`、`game_producer`、`game_sys_architect`、`game_numerical`、`game_logic_check`、`steam_indie_appraiser` 等 subagent 时，按 [`docs/onboarding/subagent-collaboration-improvement.md`](./docs/onboarding/subagent-collaboration-improvement.md) 分层处理：项目级硬规则进 `AGENTS.md` / `docs/onboarding/`；subagent 自身流程进对应 `SKILL.md`；普通实战案例进 `skills/<skill>/references/casebook/`；`.codex/agents/*.toml` 保持短启动壳。

## Codex Subagents

注册壳位于 `./.codex/agents/*.toml`，必须保持短启动壳（完整规程在对应 `skills/<技能>/SKILL.md`；实测把完整规程塞回 TOML 会导致 Codex Desktop 报 `agent type is currently not available`）。协作顺序、分工边界、冷备冻结与能力沉淀细则统一见 [`docs/onboarding/subagent-collaboration-improvement.md`](./docs/onboarding/subagent-collaboration-improvement.md)。

| Subagent | 主触发词 | 一句话职责 | 技能入口 |
| --- | --- | --- | --- |
| `ux_laoge` | `@UX老哥` `@ux诊断` | 只读 UX 诊断：操作链、信息层级、遮挡、P0/P1/P2 | [`skills/ux-diagnosis/SKILL.md`](./skills/ux-diagnosis/SKILL.md)（主 spec `system-prompt-v2.2.md`） |
| `ui_designer` | `@UI设计` `@wireframe` `@mock` | 从 brief 出元素表、桌面 16:9 mock 和交接摘要 | [`skills/ui-designer/SKILL.md`](./skills/ui-designer/SKILL.md) |
| `angus_art_director` | `@像素艺术` `@美术指导` 等 | 全局美术风格守门、prompt 审查、生成后复审 | [`skills/angus-art-director/SKILL.md`](./skills/angus-art-director/SKILL.md) |
| `angus_character_pixel_director` | `@像素美术` `@角色美术` 等 | 角色高清微像素专科：四人标杆图一致性、角色 prompt 与验收 | [`skills/angus-character-pixel-director/SKILL.md`](./skills/angus-character-pixel-director/SKILL.md) |
| `steam_indie_appraiser` | `@SIA` `@独游鉴赏师` 等 | Steam 第一眼、垂直切片、内容包、功能 ROI、竞品样本 | [`skills/steam-indie-appraiser/SKILL.md`](./skills/steam-indie-appraiser/SKILL.md) |
| `game_producer`（冷备） | `@制作人` | 立项 / 砍范围 / 里程碑 / 熔断闸门 | [`skills/game-producer/SKILL.md`](./skills/game-producer/SKILL.md) |
| `game_sys_architect`（冷备） | `@系统架构` | 玩法系统蓝图、依赖图、资源流、耦合审查 | [`skills/game-sys-architect/SKILL.md`](./skills/game-sys-architect/SKILL.md) |
| `game_numerical`（冷备） | `@数值策划` | Angus 主干数值：公式、概率、配表、验证方案 | [`skills/game-numerical/SKILL.md`](./skills/game-numerical/SKILL.md) |
| `game_logic_check`（冷备） | `@逻辑审查` | 已成形规则只读防爆：exploit、边界、跨系统矛盾 | [`skills/game-logic-check/SKILL.md`](./skills/game-logic-check/SKILL.md) |

通用调用规则：

- 触发词、别名或等价语义（"让 XX 子 agent 单独分析"）视为显式调用；父级 Codex spawn 对应 subagent，并把截图、相关文件路径和必要上下文传入。subagent 默认只读，不直接改代码、不直接生图。
- 若当前环境未暴露对应 agent 类型，父级必须按对应 `SKILL.md` 在当前线程执行同等流程，不得把触发词当普通文本忽略。
- 最终回复必须保留 subagent 意见正文，不得只给结果或改写摘要；篇幅长时用 `<details><summary>XX 诊断原文</summary>…</details>` 折叠，折叠块外另写"我如何执行 / 已落地 / 未采纳或待确认"。仅用户明确要求极简摘要时可只给摘要，但需说明完整版可补发。
- 涉及当前 / 近期 Steam 游戏、评价数、销量报道、商店页或公开视频时，父级必须先联网验证并把来源传给 subagent；无法验证只能标注估算。
- Codemaker / brainmaker 的 opencode 配置不作为 Codex 调用依据；Codex 只使用本仓库 `.codex/agents/` 与 `./skills/`。

## Skills

Angus 的项目本地技能位于 `./skills`，优先使用工作区内副本而非 `$CODEX_HOME/skills` 下的重复安装版本。完整技能索引（触发词、别名、边界、按需资料库清单）见 [`skills/README.md`](./skills/README.md)。

- 常用独立技能：`openrouter-image-gen`（真实生图，含 `nano banana` 历史别名）、`claude-to-im`（IM 桥接 / 飞书发送）、`art-reference-picker`（参考图筛选）、`psd-to-godot-ui`（PSD 转 Godot UI）。
- game-studio 导入技能（`asset-audit`、`map-systems`、`team-*` 等约 40 个）：截至 2026-07-08 无真实使用记录，作为按需资料库保留；不默认加载、不主动推荐，用户点名或请求明确匹配时按其 `SKILL.md` 执行。

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
