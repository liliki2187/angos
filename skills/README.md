# Angus 项目技能索引

> 本索引承接原 `AGENTS.md`「Available skills / How to use skills」的完整清单（2026-07-08 治理迁入，A166）。AGENTS.md 只保留项目入口；角色路由统一见 docs/onboarding/subagent-collaboration-improvement.md；技能的触发词、别名、边界和工作流细节以各自 `SKILL.md` 为准。
> 优先使用本工作区内副本，而不是 `$CODEX_HOME/skills` 下的重复安装版本。

## 通用使用规则

- 用户明确提到某个技能，打开对应 `SKILL.md` 并按其说明执行。
- 识别明显别名视为直接点名技能；若别名对应注册 subagent（见 [角色路由](../docs/onboarding/subagent-collaboration-improvement.md)），优先 spawn subagent，环境未暴露时在当前线程按 SKILL.md 执行同等流程。
- 相对路径优先从技能目录解析。
- 导入的 game-studio 技能共用模板位于 `./_game-studio-shared/templates`。
- 本工作区共享的桥接配置、日志和状态位于 `./.claude-to-im`，除非 `CTI_HOME` 覆盖该位置。

## Subagent 配套技能（触发词见协作说明）

- `ux-diagnosis`：按当前问题诊断操作链、状态、可读性和实际风险；以 SKILL.md 为唯一核心，不强制完整报告。
- `ux-kb-risks`、`ux-kb-cross-page`、`ux-kb-symptoms`、`ux-kb-principles`、`ux-kb-templates`：`ux-diagnosis` 的长尾辅助知识库，仅在对应触发条件下读取，不默认全量加载。
- `ui-designer`：视觉概念、信息组织与可实现方案；输出随任务而变，默认只读。
- `angus-art-director`：按明确分支做标杆转译和风格评审；clean-low-poly 支线仍不自动调用。
- `angus-character-pixel-director`：角色高清微像素专科，以 `角色设计风格规范-AI包/` 与四人标杆图为真源：四角色一致性、伪人嘴型、末日时钟表情、新角色 DNA、角色 prompt 与生成后验收。
- `game-producer`：制作人闸门（立项 / 砍范围 / 里程碑 / 熔断 / 制作人竞品分析）。冷备冻结中。
- `game-sys-architect`：玩法系统架构（系统树 / 依赖图 / 资源流 / 耦合审查）。冷备冻结中。
- `game-numerical`：Angus 主干数值（达标率 / 概率 / 配表 / 验证方案）；商业/MMO/F2P 资料仅显式触发时读取。冷备冻结中。
- `game-logic-check`：已成形规则的只读防爆审查（exploit / 因果闭环 / 边界 / 跨系统矛盾 / 叙事一致性）。冷备冻结中。
- `steam-indie-appraiser`：Steam 第一眼吸引力、小爆款潜力、头图 / capsule / 宣传片、垂直切片、内容包、功能 ROI 与竞品样本；涉及最新商店页 / 销量 / 评价必须联网验证。

## 独立常用技能

- `openrouter-image-gen`：真实风格探索、参考编辑与资产生成。普通生成、编辑和透明请求默认内置 imagegen，明确选择外部路径才用项目 helper；限制按工具区分，用户指定型号时不静默替换。
- `claude-to-im`：会话桥接到 Telegram / Discord / 飞书 / QQ，及一次性飞书文本 / 图片发送。别名：`bridge`、`start bridge`、`bridge status`、`bridge logs`、`send to feishu` 等。
- `art-reference-picker`：按当前分支筛选实际参考，解释可转译内容；归档与发送需要相应授权。
- `psd-to-godot-ui`：区分只读可行性、隔离预览与可复用导入；栅格场景不等于交互已实现。
- `git-cloud-submit`：盘点、分批、验证、提交并推送当前 Git 工作区改动；固定采用 Luna 机械审计、Terra 默认编排与执行、Sol 高风险裁决的三级路由，并把 stage / commit / push / 历史改写分开授权。多远端或跨端续做时追加 handoff completeness Gate，区分 Git 真源、运行中、可复现、已外部同步、秘密渠道与可丢弃状态。
- `reply-image-context`、`svg-to-png`：图像与资产辅助小工具。

## game-studio 导入技能（按需查阅）

> 2026-04-09 从 Claude Code Game Studios 导入。截至 2026-07-08 治理评审，下列技能在项目工作文档中**均无真实使用记录**；保留为按需资料库，不默认加载、不主动推荐。用户直接点名或请求明确匹配时才使用；首次真实使用后可在本节标注。

- 评审与分析类：`asset-audit`、`balance-check`、`code-review`、`design-review`、`gate-check`、`perf-profile`、`project-stage-detect`、`scope-check`、`tech-debt`。
- 规划、文档与发布类：`architecture-decision`、`bug-report`、`changelog`、`estimate`、`hotfix`、`launch-checklist`、`milestone-review`、`onboard`、`patch-notes`、`release-checklist`、`retrospective`、`reverse-document`、`setup-engine`、`sprint-plan`、`start`。
- 设计与前期制作类：`brainstorm`、`design-system`、`localize`、`map-systems`、`playtest-report`、`prototype`。
- 团队协同类：`team-audio`、`team-combat`、`team-level`、`team-narrative`、`team-polish`、`team-release`、`team-ui`。
- 其它：`canvas-design`。

边界提醒：`map-systems` 负责 `design/gdd/systems-index.md` 落盘（`game_sys_architect` 只出蓝图不落盘）；`balance-check` 做已有数据异常审计（重定公式交 `game_numerical`）；`design-review` 查文档完整性（规则漏洞交 `game_logic_check`）。
