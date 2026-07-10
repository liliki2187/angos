# 跨端交接完整性规则

## 判断原则

`不进 Git` 不等于 `不做同步`。每个未纳入当前提交的相关路径必须只有一个分类；同一路径同时包含 staged 与 unstaged 改动时，分别记录 Git 层与工作区残留层。

| 分类 | 含义 | 最低证据 | 是否允许完成提交 | 是否允许声称无缝交接 |
| --- | --- | --- | --- | --- |
| `GIT_INCLUDED` | 已进入本次 staged diff | staged path | 是 | 是 |
| `ACTIVE` | 用户明确允许仍在运行或继续写入 | 原因、负责人或任务说明 | 是，仅当 `allow_active=true` | 否 |
| `REPRODUCIBLE` | 本地文件可由真源确定性重建 | 工具版本、输入、命令 | 是 | 是 |
| `EXTERNALIZED` | 不进 Git，但已放到双方可访问的位置 | 位置、校验值或索引 | 是 | 是 |
| `SECRET` | 必须走安全凭据渠道 | 凭据名称和交接渠道，不写秘密值 | 是 | 是 |
| `DISPOSABLE` | 明确不影响构建、判断或续做 | 可丢弃原因 | 是 | 是 |
| `LOCAL_ONLY_REQUIRED` | 另一端需要，但目前只存在本机 | 无 | 否 | 否 |
| `UNKNOWN` | 没有规则匹配或分类无效 | 无 | 否 | 否 |

生产代码、生产资产、manifest、GDD、设计决策和正式标杆不得归为 `DISPOSABLE`。非确定性生成结果不能只凭“有脚本”归为 `REPRODUCIBLE`；如果另一端需要精确结果，应入 Git 或标为 `EXTERNALIZED`。

## Manifest 格式

保存为 UTF-8 JSON。`pattern` 使用仓库相对路径和 PowerShell 通配符；规则按顺序匹配，先写窄规则。

```json
{
  "schema_version": "1.0",
  "allow_active": true,
  "active_authorization": "用户明确允许当前运行内容暂留本机",
  "target_remotes": [
    { "name": "origin", "branch": "main" },
    { "name": "daydreamer", "branch": "main" }
  ],
  "entries": [
    {
      "pattern": "path/to/active/**",
      "classification": "ACTIVE",
      "reason": "另一任务仍在写入",
      "evidence": "task name or status pointer"
    },
    {
      "pattern": "docs/screenshots/**",
      "classification": "DISPOSABLE",
      "reason": "过程验收证据，不是规则或资产真源",
      "evidence": "A166"
    }
  ]
}
```

不要把整个 `docs/screenshots/**` 永久视为可丢弃。正式标杆、校色尺、合同证据或另一端继续判断所必需的截图，应使用更窄规则改为 `EXTERNALIZED`，或按 A166 真源例外显式入库。

## 多远端 Gate

对每个目标远端依次执行：

1. 核对远端名称和脱敏 URL。
2. fetch 目标远端。
3. 核对 `HEAD...<remote>/<branch>` 的 ahead / behind。
4. 确认 `<remote>/<branch>` 是 `HEAD` 的祖先；否则停止，不做强推。
5. 普通 push。
6. 再次核对本地 HEAD 与远端跟踪引用。

所有远端逐个成功并不等于 `seamless_ready=true`；后者仍取决于未提交内容分类。
