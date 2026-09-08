# Angus 规范精简与实际入口迁移

2026-09-08，A366。用户明确要求“按照你的方式去精简优化”，本轮已实施 [组织提案](2026-09-08-angus-doc-organization-proposal.md)。目标是让规范保留责任、真源与可检索经验，设计方法由当前任务与证据决定。

## 已改变的使用方式

- [AGENTS](../../../AGENTS.md) 只保留目标、自主范围、真源路由、证据责任和记忆方式。通用协作说明成为兼容入口；不递归通读全部链接。
- [资产链](../../onboarding/assetized-ui-production-chain.md) 改为决策/风险/证据表。先从需求、原图与功能形成判断；在会导致昂贵返工的素材结构或批量决定前查相关经验，不等失败后补查，也不先套旧页面配方。
- [角色说明](../../onboarding/subagent-collaboration-improvement.md) 统一维护触发词、分工和冷备状态。UI/UX 技能取消固定对方复核前提，按当前问题提供独立判断；不规定两名角色和先后顺序。其他委派继续遵守当前会话权限。
- [截图首页](../../onboarding/功能改动截图指引.md) 缩为证据责任与使用入口，[采集方法](../../onboarding/references/screenshot-methods.md) 按需读取。去掉每个改动固定截入口/操作/结算、固定 HTML 汇总、固定标注流程。
- [验证说明](../angus-workflow-harness.md)、[条件目录](../workflow-gates.yml) 及两份 Godot 工具说明统一按受影响行为选择检查。组合脚本内部仍保持原有真实验证，只是不再由任意场景扩展名强制触发整套工具。
- UI 校验器改查实际角色权限、来源和本地链接；来源检查取消固定证据类型数量、固定 KB 版本及生产字段序列化顺序。必要产物身份兼容、运行证据与恢复要求保留。

## 经验怎样保存

[共享索引](../../experience/ui-assets/README.md) 目前只有两条已发生案例：

- [纸边与 alpha](../../experience/ui-assets/paper-contour-and-alpha.md)：记录小核柔化为何没修顺形状、不透明纸层色界为何需要另看、实际 GPU 像素尺寸及连续轮廓的适用限制。578×1078 左边专用实现没有被写成通用 Paper 组件。
- [内容与承载面](../../experience/ui-assets/content-and-surface.md)：记录固定槽位如何损坏常态排版，真实可写面与控件框的区别，以及长内容完整不能代替常态组合质量。

两张关键运行图以未修改副本放入案例的 evidence 目录；原完整批次仍位于原工作目录被忽略的过程截图目录，没有声称全部证据已跨端同步。案例图用于说明故障和改善，不替代当前美术标杆。未改现有游戏图片，也未生图。

## 实际使用面与保留内容

用户指定的 D:/angos 是现行规范起点，当前工作树为 C:/Users/gzfangyue/.codex/worktrees/4564/angos。开始时工作树仍有旧强制流程。本轮逐文件迁移，70 份共用规范、配套工具和案例文件在两处 SHA256 一致；各自采纳分册保留原内容，再补缺失的 A358 和新增 A366，没有整目录替换仓库或其他分支。

主目录修改/新增 27 个任务文件，工作树修改/新增 75 个任务文件（均不计本报告、原件归档与临时执行材料）。主目录已正确的 A358 支持文件保留原字节，只向工作树补齐。

各目录均保留自己的 `_obsolete/workflow-before-astra-2026-09-08/` 原件快照及失效说明，包含当时未提交原文；需要恢复时逐文件比较，不能用主目录快照覆盖工作树独有内容。为跨端审计，主目录另在 `_obsolete/workflow-before-astra-2026-09-08-worktree-4564/snapshot/` 保存该工作树的 66 份原字节副本，并已逐文件核验 66/66 SHA-256 一致；它不覆盖现有主目录快照或任何活动文件。四个冷备技能与注册壳、Git 提交技能、游戏代码、资源、GDD 和运行合同保持本轮开始时的内容；抽取范围的摘要核对分别为 245/166 个文件一致。

| 入口 | 主目录迁移前行数 | 工作树迁移前行数 | 当前行数 |
| --- | ---: | ---: | ---: |
| `AGENTS.md` | 48 | 76 | 30 |
| `docs/onboarding/ai-collaboration-guidance.md` | 34 | 1032 | 5 |
| `docs/onboarding/ui-interaction-guidelines.md` | 34 | 1024 | 30 |
| `docs/onboarding/assetized-ui-production-chain.md` | 54 | 612 | 35 |
| `docs/onboarding/subagent-collaboration-improvement.md` | 79 | 308 | 95 |
| `docs/onboarding/功能改动截图指引.md` | 257 | 257 | 20 |
| `docs/workflows/angus-workflow-harness.md` | 43 | 490 | 21 |
| `skills/ui-designer/SKILL.md` | 30 | 158 | 31 |
| `skills/ux-diagnosis/SKILL.md` | 50 | 161 | 52 |

行数仅说明入口版本变化，不作为规范质量或模型效果评分。角色表移入协作说明后该文件略长，但不再在其他入口重复。

## 验证

- 两个目录分别运行 `scripts/tests/test_astra_ui_workflow.py`，各 16 项通过。覆盖图像 helper 参数/调用保护、交付记录证据身份、角色只读与模型继承、KB 来源及产物 ID 兼容。
- 两处 `scripts/tests/check_astra_skill_sources.py` 和 `skills/ui-designer/scripts/validate_ui_designer_skill.py` 通过；13 份技能头、TOML/JSON、Python AST、当前 22 个产物 ID 的唯一性/引用、角色入口及活动链接有效。
- 对 UI 校验器另作内存负向验证：角色权限扩大和启动技能路径失效均被识别。没有为了测试修改活动配置。
- 两处本轮文件的 `git diff --check` 通过；新增文件另查 UTF-8、语法及链接。Git 仅提示原有 CRLF 转换策略；没有改全局 Git 配置。
- YAML 中授权、交接完整性与精确 GUI EXE 保护块，和开始时主目录现行版本一致。实际机器消费者仍是交付记录 lint；没有把声明目录变成自动执行引擎。
- 检索活动入口及迁移链，未发现残留的固定 UI/UX 双审前提、Godot 扩展名总触发或文档强制角色短语。历史案例保留事实，并明确失效适用范围。

系统 skill-creator 的 quick_validate.py 因本机缺 PyYAML 无法执行；未安装依赖或伪报通过，改用上述项目检查、标准库解析和手工 YAML 结构核对。项目来源检查只支持当前简单 YAML 字段，不是通用解析器。

## 范围推演与尚未证明的事

以下是父级对活动条款的静态核对，不是独立模型实验，也没有执行生成或游戏操作：

| 示例请求 | 当前条款导向 |
| --- | --- |
| 只谈下个界面方向，不改文件 | 围绕目标与参考提方案，不自动落地、写复盘或召集会审 |
| 保留构图做配色候选，不进 Godot | 真实生成与查看，保护指定构图；不要求几何冻结或运行检查 |
| 正式替换共享组件 | 查实际消费者，验证受影响常态/风险状态和运行路径；可见变化给真图，不按文件名固定跑全部流程 |
| 为下一批纸件决定拆层方式 | 先看原稿与功能，再查命中的轮廓案例，以代表件检验具体风险，不套 578×1078 的专用曲线 |

本轮没有运行 Godot、改变游戏功能、生成新美术、提交/推送，也没有启动下个界面。规范改动不会让当前会话或已启动代理卸载旧注入上下文；下个界面宜从已更新工作目录的新上下文开始，不能承诺热更新所有代理。

收益仍需在后续真实界面观察：首次可用成品是否保住风格、用户是否再次纠正同类缺陷、针对性经验是否减少返工。没有因为文档压短、离线通过或推演正确就宣称美术质量提升。

## 本次复盘

此前 A358 缩短了主目录，但当前工作树仍使用旧规则，截图/技能检查与顶层自主范围也未完全一致；新旧入口同时存在会让历史流程重新进入决策。本次修正实际文件和引用链，并把可迁移故障保存为有触发条件、证据与限制的共享案例。父级仍对是否真正看过成品、是否把功能通过夸大为视觉通过负责。

## 文件明细

以下为工作树实际写入的任务文件；两处均另追加本报告及各自归档说明。

- `AGENTS.md`（主目录同样修订）
- `scripts/check_delivery_manifest.py`（从主目录现行版本补入工作树）
- `skills/README.md`（主目录同样修订）
- `.codex/agents/angus-art-director.toml`（从主目录现行版本补入工作树）
- `.codex/agents/angus-character-pixel-director.toml`（从主目录现行版本补入工作树）
- `.codex/agents/steam-indie-appraiser.toml`（从主目录现行版本补入工作树）
- `.codex/agents/ui-designer.toml`（从主目录现行版本补入工作树）
- `.codex/agents/ux-laoge.toml`（从主目录现行版本补入工作树）
- `design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`（从主目录现行版本补入工作树）
- `design/art-direction/clean-lowpoly-weekly-paper-material-contract.md`（从主目录现行版本补入工作树）
- `docs/onboarding/ai-collaboration-guidance.md`（主目录同样修订）
- `docs/onboarding/assetized-ui-production-chain.md`（主目录同样修订）
- `docs/onboarding/imagegen-color-contract-gate.md`（从主目录现行版本补入工作树）
- `docs/onboarding/subagent-collaboration-improvement.md`（主目录同样修订）
- `docs/onboarding/ui-interaction-guidelines.md`（主目录同样修订）
- `docs/onboarding/功能改动截图指引.md`（主目录同样修订）
- `docs/tools/psd-ui-import.md`（从主目录现行版本补入工作树）
- `docs/workflows/angus-workflow-harness.md`（主目录同样修订）
- `docs/workflows/godot-agent-smoke.md`（主目录同样修订）
- `docs/workflows/godot-visual-feedback-smoke.md`（主目录同样修订）
- `docs/workflows/README.md`（主目录同样修订）
- `docs/workflows/ui-geometry-and-text-safety-gates.md`（主目录同样修订）
- `docs/workflows/workflow-gates.yml`（主目录同样修订）
- `docs/experience/ui-assets/content-and-surface.md`（主目录同样修订）
- `docs/experience/ui-assets/paper-contour-and-alpha.md`（主目录同样修订）
- `docs/experience/ui-assets/README.md`（主目录同样修订）
- `docs/experience/ui-assets/evidence/paper-left-edge-comparison.png`（主目录同样修订）
- `docs/experience/ui-assets/evidence/task-paper-live-default.png`（主目录同样修订）
- `docs/onboarding/references/screenshot-methods.md`（主目录同样修订）
- `docs/workflows/templates/delivery-manifest.md`（从主目录现行版本补入工作树）
- `docs/workflows/templates/loop-log.md`（从主目录现行版本补入工作树）
- `docs/workflows/templates/router-card.md`（从主目录现行版本补入工作树）
- `docs/workflows/templates/ui-assetization-canvas-sidecar.md`（从主目录现行版本补入工作树）
- `docs/workflows/templates/workflow-lab-checklist.md`（从主目录现行版本补入工作树）
- `scripts/tests/check_astra_skill_sources.py`（主目录同样修订）
- `scripts/tests/test_astra_ui_workflow.py`（从主目录现行版本补入工作树）
- `skills/angus-art-director/SKILL.md`（从主目录现行版本补入工作树）
- `skills/angus-character-pixel-director/SKILL.md`（从主目录现行版本补入工作树）
- `skills/art-reference-picker/SKILL.md`（从主目录现行版本补入工作树）
- `skills/openrouter-image-gen/SKILL.md`（从主目录现行版本补入工作树）
- `skills/psd-to-godot-ui/SKILL.md`（从主目录现行版本补入工作树）
- `skills/steam-indie-appraiser/SKILL.md`（从主目录现行版本补入工作树）
- `skills/ui-designer/SKILL.md`（主目录同样修订）
- `skills/ux-diagnosis/README.md`（从主目录现行版本补入工作树）
- `skills/ux-diagnosis/SKILL.md`（主目录同样修订）
- `skills/ux-diagnosis/system-prompt-v2.2.md`（从主目录现行版本补入工作树）
- `skills/ux-kb-cross-page/SKILL.md`（从主目录现行版本补入工作树）
- `skills/ux-kb-cross-page/skill_meta.json`（从主目录现行版本补入工作树）
- `skills/ux-kb-principles/SKILL.md`（从主目录现行版本补入工作树）
- `skills/ux-kb-principles/skill_meta.json`（从主目录现行版本补入工作树）
- `skills/ux-kb-risks/SKILL.md`（从主目录现行版本补入工作树）
- `skills/ux-kb-risks/skill_meta.json`（从主目录现行版本补入工作树）
- `skills/ux-kb-symptoms/SKILL.md`（从主目录现行版本补入工作树）
- `skills/ux-kb-symptoms/skill_meta.json`（从主目录现行版本补入工作树）
- `skills/ux-kb-templates/SKILL.md`（从主目录现行版本补入工作树）
- `skills/ux-kb-templates/skill_meta.json`（从主目录现行版本补入工作树）
- `skills/angus-art-director/references/casebook/README.md`（从主目录现行版本补入工作树）
- `skills/openrouter-image-gen/agents/openai.yaml`（从主目录现行版本补入工作树）
- `skills/openrouter-image-gen/references/model-routing.md`（从主目录现行版本补入工作树）
- `skills/openrouter-image-gen/references/prompt-planning.md`（从主目录现行版本补入工作树）
- `skills/openrouter-image-gen/scripts/openrouter_image_gen.py`（从主目录现行版本补入工作树）
- `skills/steam-indie-appraiser/references/casebook/README.md`（从主目录现行版本补入工作树）
- `skills/ui-designer/agents/openai.yaml`（从主目录现行版本补入工作树）
- `skills/ui-designer/references/playbook.md`（从主目录现行版本补入工作树）
- `skills/ui-designer/references/system-prompt-v1.0.md`（从主目录现行版本补入工作树）
- `skills/ui-designer/references/upstream-readme.md`（从主目录现行版本补入工作树）
- `skills/ui-designer/scripts/validate_ui_designer_skill.py`（主目录同样修订）
- `skills/ux-diagnosis/references/casebook/2026-07-09-wmw-left-card-six-round-tug.md`（从主目录现行版本补入工作树）
- `skills/ux-diagnosis/references/casebook/2026-07-17-wmw-short-state-oversized-container.md`（从主目录现行版本补入工作树）
- `skills/ux-diagnosis/references/casebook/README.md`（从主目录现行版本补入工作树）
- `docs/设计采纳记录.md`（主目录同样修订）
- `docs/design-decisions/process-and-research-decisions.md`（主目录同样修订）
- `docs/plans/world-map-benchmark-landing/STATUS.md`（主目录同样修订）
- `docs/workflows/reports/2026-09-08-angus-doc-organization-proposal.md`（主目录同样修订）
- `docs/workflows/reports/2026-09-07-astra-ui-workflow-audit.md`（从主目录现行版本补入工作树）
