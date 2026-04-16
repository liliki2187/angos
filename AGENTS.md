## 设计文档（系统总集）

- **母文档**：[`设计文档/系统功能设计总集.md`](./设计文档/系统功能设计总集.md) — 系统功能全貌、分册索引、全链原型落地对照。
- **同步**：已确定并落地的玩法/规则/常量变更，应同步更新该总集对应章节与 §13、§14。
- **出入提醒**：若代码/配置与总集描述不一致，助手在改完或评审时应**明确提醒**用户：择一修正文档或实现。
- **协作偏好**：后续 AI / 新对话在处理玩法、原型、UI 感知类任务前，先读 [`docs/onboarding/ai-collaboration-guidance.md`](./docs/onboarding/ai-collaboration-guidance.md)；收到新的强反馈后应同步更新该文档。

## Skills

Angus 的项目本地技能位于 `./skills`。
优先使用这些工作区内副本，而不是 `$CODEX_HOME/skills` 下的重复安装版本。

### Available skills

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
