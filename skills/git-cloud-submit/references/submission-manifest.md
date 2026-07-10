# Git 云端提交清单模板

```md
# 提交清单

## 目标
- 仓库：
- 目标 remotes / URLs（凭据已遮罩）：
- branch：
- upstream：
- 每个目标远端当前 ahead / behind 与快进关系：

## 权限
- 只读审计：是
- stage：已授权 / 未授权
- commit：已授权 / 未授权
- push：已授权 / 未授权
- amend / rebase / force / 历史改写：已授权 / 未授权（默认未授权）

## 模型路由
- Luna 阶段：
- Terra 阶段：
- Sol 升级条件：未命中 / 命中（原因）
- 实际运行时能否切换模型：能 / 不能 / 未验证

## 风险
- 冲突：
- 删除 / 重命名：
- 疑似密钥或凭据：
- 大文件 / LFS：
- 第三方许可 / 来源：
- GDD / 代码 / 设计决策真源同步：
- 过程截图与真源例外：

## 交接完整性
- handoff manifest：
- `allow_active` 与用户授权证据：
- `ACTIVE`：
- `REPRODUCIBLE`（版本 / 输入 / 命令）：
- `EXTERNALIZED`（位置 / 校验指针）：
- `SECRET`（安全渠道，不记录秘密值）：
- `DISPOSABLE`（原因）：
- `LOCAL_ONLY_REQUIRED` / `UNKNOWN`：必须为 0
- `submission_ready`：
- `seamless_ready`：

## 批次

### Batch 1：<单一目的>
- include：精确路径或 pathspec
- exclude：明确排除项
- 删除 / 重命名意图：
- 验证命令：
- commit message：
- staged diff 复核：待执行 / 通过 / 失败
- 状态：待授权 / 待暂存 / 待提交 / 已提交

## 推送前冻结
- 计划推送的 commits：
- 每个 remote / branch 二次核对：
- 工作区剩余改动：
- 非 force push：是
- 用户 push 授权证据：

## 回执
- commits：
- 验证结果：
- push 结果：
- 各远端跟踪引用核对：
- 未提交 / 排除 / 待裁决及 handoff 分类：
- `submission_ready` / `seamless_ready`：
```

清单可以只在对话中呈现；仅当任务需要审计留痕或跨任务交接时才写入仓库。不要为了每次小提交制造常驻文档。
