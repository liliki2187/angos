# Godot 版本参考

最后核验：2026-04-09

| 字段 | 值 |
|------|------|
| 引擎 | Godot |
| 项目锁定版本 | 4.6.2 stable |
| 包类型 | Standard（非 .NET） |
| 主要脚本语言 | GDScript |
| 项目锁定日期 | 2026-04-09 |
| LLM 知识截止 | 2025-05 |
| 风险等级 | HIGH：版本已超出 LLM 截止，必须以官方文档与发布页为准 |
| 本地真源目录 | `tools/godot/4.6.2-stable/` |
| Windows 标准下载页 | `https://godotengine.org/download/windows/` |
| 版本归档页 | `https://godotengine.org/download/archive/4.6.2-stable/` |

## 当前结论

- 当前项目统一锁定 Godot `4.6.2 stable`。
- Angus 当前使用 GDScript，不需要 `.NET` 构建。
- 本地与 CI 都应围绕 `4.6.2 stable` 对齐，不再默认依赖外部全局 Godot 目录。

## 对当前项目最重要的版本事实

1. 官方 Windows 下载页当前给出的最新稳定版是 `4.6.2`。
2. 官方 Windows 下载说明明确写明：**解压即可运行，不需要安装**。
3. 官方稳定版文档仍明确写明：`Array[Array[float]]` 这类**嵌套 typed collections 仍不支持**。

## 对 Angus 的直接影响

- `Array[Array[String]]` 不能作为正式长期方案，升级到 4.6.2 也不会变合法。
- 周循环系统里的组合枚举、候选列表和多层结构，必须继续使用下列替代方案之一：
  - `Array[Array]` + 显式校验
  - typed dictionaries
  - `RefCounted` / `Resource` 状态类
- 如果未来要写更严格的深拷贝逻辑，应优先评估 4.5+ 的 `duplicate_deep()` 相关方案，而不是继续依赖模糊的 `duplicate(true)` 语义。

## 本地目录约定

```text
tools/
  godot/
    README.md
    4.6.2-stable/
      Godot_v4.6.2-stable_win64.exe
      Godot_v4.6.2-stable_win64_console.exe
      export_templates/
        templates/
```

## 关联文档

- `docs/engine-reference/godot/breaking-changes.md`
- `docs/engine-reference/godot/deprecated-apis.md`
- `docs/engine-reference/godot/current-best-practices.md`
- `docs/tools/godot-local-engine-workflow.md`
