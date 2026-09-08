# Astra UI 资产工作流审计与精简报告

日期：2026-09-07。对应用户授权：A358。产物身份：项目规则、技能与局部工具重构；不是 UI 美术批准或游戏生产候选。

## 结论

本轮已落实精简，不只是提供建议。核心问题不是项目把父级模型写死为旧型号，而是长指令链将历史页面处方、工程门槛和输出模板混成通用规则，容易让更认真遵循指令的模型反复停工或只做局部修补。

当前改为：按用户目标决定范围；风格探索允许整体创造；真实内容尽早验证；正式生产才承担完整的相关工程证据。必要质量边界保留，取消固定方法与重复审批。

九份核心入口由 **4870 行 → 545 行**，约减少 **89%**。这是文本行数，不是实测 token、费用或速度改善；不能据此声称生成的图已经更好。

## 官方依据与项目判断

- 官方 Astra 指南特别提醒审计 AGENTS/skills 的影响，并明确主动推进、简洁输出与适量验证等偏好。本轮据此删除冲突指令和重复流程，而非替模型添加另一层长提示词。[官方最新模型指南](https://developers.openai.com/api/docs/guides/latest-model)
- Codex 子代理可在未指定模型/推理档位时继承父级；独立、边界清楚的子任务才有协作收益。本轮移除五个 UI 配套壳固定的 high 档位，不全局强制昂贵模型。[官方子代理说明](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- 项目指令有加载层级和大小边界，应短而明确；磁盘修改不等于已运行角色的指令热替换。[官方 AGENTS 说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

上述资料是官方依据；“探索—代表性验证—扩产”的具体组织、角色调用条件及删改范围是结合本仓库证据的项目判断，不是声称官方规定了 Angus 的生产流程。OpenAI Docs 用于核实依据，Skill Creator 用于精简入口、按需参考与独立前向测试。

## 审计范围

- 62 个既有文件已修改，原文均已按当时工作区内容快照，不以 Git HEAD 替换用户未提交内容。
- 盘点九个注册壳；修改 UI Designer、UX 老哥、美术指导、角色美术指导、SIA 五个直接配套角色。制作人、系统架构、数值、逻辑审查四个冷备壳与技能未改、未解冻。
- 优化五个角色技能、五个 UX KB、生图/参考筛选/PSD 三个直接工具技能，以及实际活动入口、元数据、模板与检查器。
- 历史 casebook、两张原始标杆、原始图片和既有运行合同保留。普通案例不再是通用命令；冷备和未进入当前链的 game-studio 导入资料库没有扩写。
- 未改 GDD、玩法数值、世界地图 JSON 几何合同、Godot 场景/脚本、运行图片、外部密钥或全局模型配置；未提交或推送 Git。

## 主要冲突与处理

| 原问题 | 本轮处理 |
| --- | --- |
| 用户允许重构，通用入口仍要求最小局部修改和旧 exact rect | 区分“保护原稿的微调”与“已授权重设计”；旧合同只约束其运行消费者，新候选可以探索 |
| 所有生图被当作高风险生产任务，先冻结完整页合同才能看效果 | 风格探索按本轮视觉问题验证；代表区域尽早真实填入；生产再核对复用/状态/运行 |
| UI/UX 每轮全套串行、多份报告、所有分歧都上推用户 | 重要布局/交互和生产候选做独立交叉检查；小范围风格探索不重复会审；父级负责可逆取舍 |
| 固定字号、间距、字体占比、色差、面数成为通用门槛 | 移到适用合同/历史记录；实际比例、字形、可写区和功能安全继续验证 |
| UX 要凑问题数、按次数升 P0、旧问题不许降级 | 严重度以真实后果和恢复性决定；新证据允许修正判断，不凑数 |
| 旧上游核心和壳重复注入，五 KB 又强制连锁加载 | UI/UX 旧核心入口退役为短指针；当前方法只在 SKILL；KB 按需读取 |
| 像素/半调与 clean-low-poly 混用，纸材合同夹带旧版布局和下一步 | 分支隔离；纸材保留原样本和消费者范围；旧装配日志归入快照，不约束新探索 |
| 全局生图负面词禁止 UI、边框、阴影、贴纸，并给地图加人体禁词 | 修改真实 Python 提示词构造器：按角色选避坑；新增 --no-default-negatives；不改变 helper API/密钥 |
| 项目透明件默认外部 API 与当前内置 imagegen 技能冲突 | 普通生成、编辑、透明请求默认内置；明确选择外部路径才调用现有 OpenRouter helper |
| PSD 咨询默认运行有写入副作用的包装器 | 区分只读分析、隔离预览和复用导入；两种示例均显式跳过编辑器设置配置 |
| checker 用 STATUS、裁图词或艺术指导名字代替质量证据 | 检查器只负责记录字段，明确不证明视觉/运行；运行类记录仍需实际证据说明 |
| 复盘/画布模板继续恢复固定格式、两轮止损和旧阶段编号 | 模板改为可选便笺；不因“先别改文件”自动落盘或增加审批 |

### 仍保留的质量边界

实际查看参考与生成结果；同类图片按明确母图/适配策略复用；真实文字承载与可读性；选中/锁定/可进入语义；热区与可见物件对应；内容/装饰/运行文字层所有权；受影响状态与消费者验证；真实截图和动态证据；生产回退、文件归属与外部操作授权。

取消固定处方不代表取消这些检查。程序通过不等于符合标杆，生图也不等于运行实现。

## 独立复审与修正

UI 和 UX 的第一轮只读审计分别覆盖设计/生成入口、诊断核心及五 KB。重构后的独立复审实际发现并修正了：

- 所有阶段应核验用户明确要求的比例/透明等输出属性，不能仅限生产阶段。
- 材质合同自身仍混有旧布局规程，现已中文整理并保留原 token 数值。
- 活动案例仍有旧“两轮停工、每条问题入 manifest”命令，已标明历史失效范围。
- 证据目录缺 isolated_technical_probe，及 production 命名/回退不一致，已补齐。
- KB 元数据数量、显示名和版本陈旧，已同步并使用 2.0.0。
- PSD 的 reusable 命令遗漏跳过编辑器配置参数，第二次复核后已补齐。
- 冷备说明留下失效章节回指，已改为真实维护原则。

另以不继承本轮讨论、只读取活动文件的代理做三请求前向测试；不给它审计结论或预期答案：

| 请求 | 实际推演表现 |
| --- | --- |
| 保留布局，生成三个配色版本，不进 Godot | 直接真实生图，查看原图/结果，不要求几何冻结或逐轮双审 |
| 正式替换共享地区卡，长中文及锁定/已选正常 | 查实际合同/消费者，验证真实内容和状态，独立 UI/UX 复核，提供运行证据 |
| 先不改文件，询问 PSD 分层导入工作量 | 只读查层与导出器，不运行 preview，不把 TextureRect 说成动态 Label |

它还指出页面 JSON 的旧“禁止集成”阶段记录。**本轮没有删这些记录**：模拟请求中的集成授权不等于当前真实用户授权。以后真正收到集成要求时，应核对当前批准资产并迁移相应阶段状态，不机械停工，也不趁本轮审计放行 Godot。

## 验证结果与限制

已执行：

- [离线回归](../../../scripts/tests/test_astra_ui_workflow.py)：16 项通过，覆盖禁词、显式避坑、路由/参数保护、交付记录、继承与元数据。
- [来源字段检查](../../../scripts/tests/check_astra_skill_sources.py)：13 份技能头字段、项目 TOML、KB JSON、修改 Python AST、22 个证据身份及阶段引用通过。
- 现有 `skills/ui-designer/scripts/validate_ui_designer_skill.py` 通过，已不再要求固定 high 或完整旧核心。
- 本轮文件的 `git diff --check` 已通过（收尾模板/报告再次核对见交付时结果）。全工作树有本来就存在的 UI 决策分册尾空行，不借本轮修改无关内容。
- 冷备四个角色/技能的 Git diff 为空；未产生模型 API 调用。

明确未做：

- 没有重新生成 UI、接 Godot、跑完整游戏或对新旧工作流做美术质量 A/B；下次实际 UI 任务才可验证收益。
- Python 环境没有 PyYAML，官方 quick_validate.py 没有直接运行；使用现有 UI 校验器、标准库字段/配置检查及人工查看 YAML。新增检查器明确不是通用 YAML 解析器。
- 规则目录是声明和引用目录，不是已自动执行所有 gate 的完整引擎；目前实际消费者是交付记录检查脚本。
- 新启动的默认代理已读取新文件完成前向推演；五个专用注册壳已通过 TOML/继承检查，但已运行角色不会自动卸载旧启动指令。下一次新启动任务/角色还应确认读取新入口，不能承诺本会话热切换了所有底层配置。

## 文件压缩明细

| 核心文件 | 重构前行数 | 当前行数 |
| --- | ---: | ---: |
| `AGENTS.md` | 76 | 48 |
| `docs/onboarding/ai-collaboration-guidance.md` | 1038 | 34 |
| `docs/onboarding/ui-interaction-guidelines.md` | 1026 | 34 |
| `docs/onboarding/subagent-collaboration-improvement.md` | 308 | 79 |
| `docs/onboarding/assetized-ui-production-chain.md` | 643 | 54 |
| `docs/onboarding/imagegen-color-contract-gate.md` | 141 | 19 |
| `docs/workflows/angus-workflow-harness.md` | 491 | 43 |
| `docs/workflows/ui-geometry-and-text-safety-gates.md` | 130 | 23 |
| `docs/workflows/workflow-gates.yml` | 1017 | 211 |

统计基于本轮快照与写入文本，不含历史快照本身；不与 Git HEAD 混算。

## 恢复与下一次使用

原始文件快照：`_obsolete/workflow-before-astra-2026-09-07/`，共 62 份原文件及 README，包含开始前的未提交修改。需要恢复时按单文件比较现行内容与快照，不整目录覆盖后续工作；此目录只供明确的审计/恢复，不作为活动规范。

下一次世界地图工作读取当前 STATUS 的 A357 选稿和三栏候选、两张原始标杆及本轮精简入口。先把整屏视觉做好，再用代表性真实内容证明能落地；不重新带回旧硬框、固定纸色或无休止局部修补。

### 本轮修改的既有文件

- `AGENTS.md`
- `docs/onboarding/ai-collaboration-guidance.md`
- `docs/onboarding/ui-interaction-guidelines.md`
- `docs/onboarding/subagent-collaboration-improvement.md`
- `docs/onboarding/assetized-ui-production-chain.md`
- `docs/onboarding/imagegen-color-contract-gate.md`
- `docs/workflows/angus-workflow-harness.md`
- `docs/workflows/ui-geometry-and-text-safety-gates.md`
- `docs/workflows/workflow-gates.yml`
- `docs/workflows/templates/router-card.md`
- `docs/workflows/templates/delivery-manifest.md`
- `skills/ui-designer/SKILL.md`
- `skills/ui-designer/references/system-prompt-v1.0.md`
- `skills/ui-designer/references/playbook.md`
- `skills/ui-designer/references/upstream-readme.md`
- `skills/ui-designer/agents/openai.yaml`
- `skills/ui-designer/scripts/validate_ui_designer_skill.py`
- `skills/ux-diagnosis/SKILL.md`
- `skills/ux-diagnosis/system-prompt-v2.2.md`
- `skills/ux-diagnosis/README.md`
- `skills/angus-art-director/SKILL.md`
- `skills/angus-character-pixel-director/SKILL.md`
- `skills/steam-indie-appraiser/SKILL.md`
- `skills/openrouter-image-gen/SKILL.md`
- `skills/openrouter-image-gen/references/prompt-planning.md`
- `skills/openrouter-image-gen/references/model-routing.md`
- `skills/openrouter-image-gen/scripts/openrouter_image_gen.py`
- `skills/openrouter-image-gen/agents/openai.yaml`
- `skills/art-reference-picker/SKILL.md`
- `skills/psd-to-godot-ui/SKILL.md`
- `scripts/check_delivery_manifest.py`
- `skills/README.md`
- `docs/设计采纳记录.md`
- `docs/design-decisions/process-and-research-decisions.md`
- `docs/plans/world-map-benchmark-landing/STATUS.md`
- `design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`
- `design/art-direction/clean-lowpoly-weekly-paper-material-contract.md`
- `.codex/agents/ui-designer.toml`
- `.codex/agents/ux-laoge.toml`
- `.codex/agents/angus-art-director.toml`
- `.codex/agents/angus-character-pixel-director.toml`
- `.codex/agents/steam-indie-appraiser.toml`
- `skills/ux-kb-risks/SKILL.md`
- `skills/ux-kb-risks/skill_meta.json`
- `skills/ux-kb-cross-page/SKILL.md`
- `skills/ux-kb-cross-page/skill_meta.json`
- `skills/ux-kb-symptoms/SKILL.md`
- `skills/ux-kb-symptoms/skill_meta.json`
- `skills/ux-kb-principles/SKILL.md`
- `skills/ux-kb-principles/skill_meta.json`
- `skills/ux-kb-templates/SKILL.md`
- `skills/ux-kb-templates/skill_meta.json`
- `skills/ux-diagnosis/references/casebook/README.md`
- `skills/ux-diagnosis/references/casebook/2026-07-09-wmw-left-card-six-round-tug.md`
- `skills/ux-diagnosis/references/casebook/2026-07-17-wmw-short-state-oversized-container.md`
- `skills/angus-art-director/references/casebook/README.md`
- `skills/steam-indie-appraiser/references/casebook/README.md`
- `docs/tools/psd-ui-import.md`
- `docs/workflows/README.md`
- `docs/workflows/templates/loop-log.md`
- `docs/workflows/templates/workflow-lab-checklist.md`
- `docs/workflows/templates/ui-assetization-canvas-sidecar.md`
