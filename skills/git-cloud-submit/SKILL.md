---
name: git-cloud-submit
description: 审计、分批、验证、提交并推送 Git 工作区改动到远端，按 GPT-5.6 Luna、Terra、Sol 分配机械盘点、常规判断和高风险裁决。用户提出“提交未提交资源”“同步云端”“stage/commit/push 当前改动”“整理脏工作区后上传”等请求时使用；也用于只读评估当前改动是否适合提交。
---

# Git 云端提交

把一次云端提交拆成可审计的阶段。默认由 Terra 负责整单，Luna 只做确定性只读工作，Sol 只处理会改变风险结论的裁决。

## 先冻结权限边界

1. 读取仓库根 `AGENTS.md` 与更近层级规则。
2. 区分用户是在“评估 / 诊断”，还是已明确要求“暂存 / 提交 / 推送”。评估不授权写入 Git 索引或远端。
3. 保留所有既有用户改动。不得用 `reset --hard`、`checkout --`、清理未跟踪文件或历史改写来整理工作区。
4. 把 `stage`、`commit`、`push`、`force push / rebase / amend` 视为不同授权；前一项授权不自动包含后一项。
5. 模型档位不扩大权限。即使升级到 Sol，也不能替用户授权破坏性或外部状态变更。

## 使用固定模型路由

| 阶段 | 默认模型 | 职责 | 禁止事项 |
| --- | --- | --- | --- |
| A. 只读盘点 | GPT-5.6 Luna / low | 运行审计脚本，统计状态、体积、LFS、分支、上游、删除、冲突和疑似敏感文件名 | 不判断文件归属，不暂存，不提交，不推送 |
| B. 提交编排 | GPT-5.6 Terra / medium | 阅读 diff 与项目真源，划分提交批次，给出 include / exclude、验证项和提交说明 | 不默认 `git add -A`，不把模糊范围解释成“全部提交” |
| C. 风险裁决 | GPT-5.6 Sol / medium 起 | 只在升级条件命中时裁决范围、历史、真源、安全、许可或冲突方案 | 不重复机械盘点，不凭模型等级越权执行 |
| D. 写入与验证 | GPT-5.6 Terra / medium | 按已冻结清单精确暂存，复核 staged diff，运行验证，提交，并在明确授权后推送 | 不改变已批准范围，不静默 pull / rebase / force |
| E. 回执 | GPT-5.6 Luna / low 或当前模型 | 只读核对 commit、工作区状态、远端跟踪关系与 push 结果 | 不把“命令返回成功”扩写成未验证结论 |

详细升级条件与运行时回退见 [模型路由](references/model-routing.md)。不要凭 Sol / Terra / Luna 的名称直觉推断高低顺序。

## 阶段 A：生成只读审计

从仓库根执行：

```powershell
powershell -ExecutionPolicy Bypass -File skills/git-cloud-submit/scripts/audit_git_submit.ps1 -Format Text
```

需要机器可读结果时使用 `-Format Json`。脚本只读取 Git 和文件元数据，不读取或显示疑似密钥文件内容。

把以下任一结果视为停止信号：

- 合并冲突或未合并状态；
- 疑似密钥、证书、凭据或令牌文件；
- 单文件达到脚本阻断阈值；
- 上游落后且本地存在待提交改动；
- 远端、分支或上游关系不明确；
- 用户改动与本任务生成物无法区分。

脚本的 `review` 标记只表示进入 Terra 复核，不自动触发 Sol。`MANY_UNTRACKED`、`BINARY_WITHOUT_LFS`、`MIXED_TOP_LEVEL`、`DELETIONS` 或 `PRIMARY_BRANCH` 单独出现时仍由 Terra 处理；只有 Terra 复核后确认存在下节所列实际高风险取舍，才升级 Sol。脚本的 `block` 标记表示停止写操作，也不等于“换成 Sol 就可以继续”。

## 阶段 B：冻结提交清单

按 [提交清单模板](references/submission-manifest.md) 输出清单。至少写清：

- 目标 remote、branch 与 upstream；
- 每个批次的目的、精确 include / exclude 路径、验证命令和 commit message；
- 删除、重命名、生成物、归档、图片 / 音视频、代码、GDD / 设计决策是否混批；
- `stage / commit / push` 各自是否已获授权；
- 当前模型路由，以及是否命中 Sol 升级条件。

默认按“同一意图、可独立回滚、验证方式相同”分批。文件多不自动等于需要 Sol；只有判断复杂度或后果风险升级时才调用 Sol。

Angus 特有规则：

- `docs/screenshots/**` 的过程截图默认不入库；真源例外必须按截图指引显式 `git add -f` 并确认引用关系。
- 玩法 / 规则 / 常量改动必须检查 `design/gdd/` 与实现是否同步；不一致时显式提醒用户选择修正文档或实现。
- `_obsolete/` 只收明确废弃材料；每个新增归档目录要有说明废弃原因的 README。
- 不把本任务新建的提交技能与工作区内其它用户改动无条件混成一个 commit。

## 阶段 C：仅在需要时升级 Sol

先由 Terra 把审计标记转成具体问题。命中以下任一**已确认事实**时，停止写操作并交 Sol 裁决：

- 需要改写历史、强推、复杂 rebase，或处理跨多个提交的冲突；
- 疑似密钥已进入 Git 历史，问题从“排除文件”升级为“安全事件”；
- 用户决定引入 / 迁移 Git LFS，且方案会影响既有远端历史或协作者；仅“二进制很多且当前无 LFS”不足以升级；
- 改动跨代码、GDD、设计决策、生成资产，且 Terra 已发现实际归属争议或真源矛盾；仅跨目录或文件多不足以升级；
- 删除 / 重命名可能损失用户内容，且 Terra 无法从任务证据或用户确认判断是否有意；
- 第三方资源的许可证、来源或可公开上传性不确定；
- Terra 给出的两个方案会产生不同的不可逆后果。

Sol 只返回裁决与修订后的提交清单。仍由 Terra 在用户授权范围内执行。

## 阶段 D：精确写入

1. 使用清单中的精确 pathspec 暂存；只有用户明确要求全部提交且审计证明范围单一时，才允许 `git add -A`。
2. 执行 `git diff --cached --check`、`git diff --cached --stat` 与逐批 staged diff 复核。
3. 运行与该批次风险相称的测试。资源批至少验证 manifest / 引用 / 导入关系；代码批运行相关测试；文档批检查链接和真源同步。
4. staged diff 与清单不一致时取消该批次继续执行并上报；不得自行扩大 include。
5. 提交后再次读取 `git status --short` 和 `git log -1 --oneline`。
6. 只有用户明确要求推送时，核对 remote URL、目标 branch、upstream 与 ahead / behind，再执行非 force push。
7. push 后核对本地 HEAD 与对应远端跟踪引用。无法验证远端引用时，只报告“push 命令成功”，不得声称远端内容已完整验收。

## 运行时能力回退

若当前 Codex 运行时能把子任务绑定到具体模型，按表分派；若不能：

- 用 Terra 启动整单并运行 Luna 对应的确定性脚本；
- 命中 Sol 升级条件时明确暂停，请用户切换 Sol 或使用运行时已暴露的 Sol agent；
- 不得声称已经自动切换模型。

当前仓库 `.codex/agents/*.toml` 只证明已配置的 agent 壳和 reasoning effort，不足以证明本次运行时支持按 subtask 自动切换 GPT-5.6 型号。

## 交付回执

最终说明：

- 实际采用的模型路由与是否发生升级；
- 每个 commit 的哈希、主题和验证结果；
- push 的 remote / branch 与核验结果；
- 仍未提交、被排除或需要用户裁决的内容；
- 若只完成审计或暂存，明确停在哪一阶段。
