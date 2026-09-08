# Angus 协作入口

## 目标、真源与权限

- 在系统、工具和授权边界内，以用户当前明确目标为准。历史流程是辅助，不得反过来缩小用户已授权的探索或重构范围；也不得把“自由设计”理解为擅自改玩法、正式运行资产或外部系统。
- 玩法真源：`design/gdd/core-experience.md`、`game-concept.md`、`game-pillars.md`、`gameplay-design-principles.md`、`systems-index.md`（均在同目录）。只读本任务相关内容。已落地的规则变更同步对应 GDD；发现文档与实现出入，明确提醒。旧总集 `docs/archive/legacy-design/系统功能设计总集.md` 只作历史对照，涉及其系统全貌章节时注明差异。
- UI / 玩法 / 原型任务先读 `docs/onboarding/ai-collaboration-guidance.md`；UI 再读 `docs/onboarding/ui-interaction-guidelines.md`。跨阶段资产任务按需读 `docs/onboarding/assetized-ui-production-chain.md`，不默认加载整个历史档案。
- 明确采纳、待定、撤回的用户意见，按 `docs/设计采纳记录.md` 的写入规则登记索引和主分册。AI 实现方案不得伪记为用户已确认。历史决定保留修订记录，不以旧条目覆盖新决定。
- 保留用户未提交修改；不擅自提交、推送、删除资产、覆盖主场景或改全局配置。任务说明、诊断与审计不自动授权实施，用户明确要求优化或修改则在所述范围内完成并验证。

## UI 与美术底线

- 默认仅桌面 16:9、1920×1080；不主动做移动版。用户当次明确要求移动端时可作一次例外，不改变项目平台。
- 看实际参考图再判断风格；区分原始标杆、用户选定稿、当前运行截图和历史样本。当前任务可重构的结构不继承旧页面 exact rect，仍在使用的运行合同未经迁移不能假称已兼容。
- `clean low-poly weekly` 以 `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`、`benchmark-board-02.png` 及当前用户裁决为视觉依据。不自动调用旧像素坐标系的 `angus_art_director`；不得强加半调、像素颗粒、泛黄档案材质。其他分支与角色真源按对应技能读取。
- 生图请求必须使用真实图像生成模型，不能以 SVG、Canvas、HTML/CSS 或脚本绘图冒充。用户明确要结构示意、程序绘图或可编辑模板时才采用相应方式。后期程序可负责文字、装配与检测，说明其实际作用。
- 风格稿不等于可拆资产；合成预览不等于运行截图；运行逻辑通过不等于美术通过。正式交付检查真实内容、图片复用、状态语义、视觉可写区与热区，不以“流程通过”替代观看成品。
- 游戏/原型有可见改动时给真实截图和简短说明，方法见 `docs/onboarding/功能改动截图指引.md`。判断节奏、动作或交互反馈时给真实动图/视频；无法导出就说明原因并提供可运行播放或逐帧临时替代，不以静帧声称动态通过。

## 子代理：为独立判断服务，不做固定流水线

- 明确点名 subagent 时调用。重要新布局、交互重构或生产候选，使用 `ui_designer` 与 `ux_laoge` 独立交叉检查；新方案可先设计，现有问题可先诊断。纯风格探索、配色变体、局部装饰或已通过方案的小修，不必每轮重复双审。
- 父级先定义具体任务、证据、权限、输出用途；有独立且有价值的子任务才委派。只读专家不直接改代码、生图或再召集整套委员会。能并行的独立阅读可以并行，评审实际产物必须等产物存在。
- 父级对总体效果负责，综合而非机械接受专家意见。可逆的设计取舍自主处理；功能语义冲突、授权外动作、不可逆影响或无法推断的关键偏好才请用户决定。
- 默认向用户给结论、关键证据和未解决分歧；完整专家正文按需保存/提供，不强制粘贴多份报告。详见 `docs/onboarding/subagent-collaboration-improvement.md`。
- 注册壳仅保留身份、边界和技能入口。UI 配套角色不固定模型或推理档位，默认继承父级；只有用户明确要求或独立任务有已说明的理由才覆盖。不把 API 专用参数写入 Codex 本地配置。
- 四个冷备角色继续冻结；显式调用可执行，维护解冻须用户确认。价值窗口与提醒义务见协作说明 §8。本次 UI 链优化不解冻它们。

| 角色 | 显式触发词 | 技能入口 |
| --- | --- | --- |
| `ui_designer` | @UI设计、@wireframe、@mock | `skills/ui-designer/SKILL.md` |
| `ux_laoge` | @UX老哥、@ux诊断、@UX诊断 | `skills/ux-diagnosis/SKILL.md` |
| `angus_art_director` | @像素艺术、@美术指导、ArtDirector | `skills/angus-art-director/SKILL.md` |
| `angus_character_pixel_director` | @像素美术、@角色美术、@角色风格守门 | `skills/angus-character-pixel-director/SKILL.md` |
| `steam_indie_appraiser` | @SIA、@独游鉴赏师 | `skills/steam-indie-appraiser/SKILL.md` |
| `game_producer`（冷备） | @制作人 | `skills/game-producer/SKILL.md` |
| `game_sys_architect`（冷备） | @系统架构 | `skills/game-sys-architect/SKILL.md` |
| `game_numerical`（冷备） | @数值策划 | `skills/game-numerical/SKILL.md` |
| `game_logic_check`（冷备） | @逻辑审查 | `skills/game-logic-check/SKILL.md` |

## 工作方式与维护

- 按 `docs/workflows/angus-workflow-harness.md` 依据后果而非文件类型选择验证强度。没有要求的表格、审批与固定轮数不应阻止在范围内继续工作。
- 重复失败、明显误判或用户要求复盘时记录原因、方法改变及验证结果；不要每次反馈都新增永久规则。可逆的替代方法先尝试，真正需要新增权限时停下询问。
- 项目本地技能优先，入口见 `skills/README.md`。工具不可用要说明，不能假称已调用或偷偷换付费供应商。未暴露被点名角色时，按对应技能在父级执行并说明。
- Git 盘点、提交、推送、跨端交接必须读取 `skills/git-cloud-submit/SKILL.md`；其提交与完整交接保护不因 UI 工作流简化而改变。
- `_obsolete/` 只作用户要求的历史查询、恢复、比对或审计，不自动检索为真源。新增归档写明失效原因。2026-09-07 之前的工作流快照不再是活动指令。
- 仓库说明文本默认简体中文；代码标识、路径、产品名、机器字段与许可证原文可保留原文。
