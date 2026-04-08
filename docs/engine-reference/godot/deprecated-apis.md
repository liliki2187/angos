# Godot 4.6.2 下应停止采用的旧写法

最后核验：2026-04-09

> 说明：Godot 官方并没有提供一份专门面向 Angus 的“4.4-4.6 废弃 API 清单”。本页记录的是当前项目应视为停止采用的旧写法、错误预期或高风险模式。

| 旧写法 / 错误预期 | 当前结论 | 替代方案 |
|------|------|------|
| `Array[Array[String]]`、`Array[Array[T]]` 这类嵌套 typed collections | 官方稳定版文档仍明确不支持 | 使用 `Array[Array]` + 显式校验，或改成 typed dictionaries / `RefCounted` / `Resource` |
| 把 `duplicate(true)` 当作“所有嵌套资源都可靠深拷贝” | 4.5 发布页明确指出旧深拷贝语义并不总是可靠 | 对关键状态优先显式重建；确实需要时评估 `duplicate_deep()` |
| 默认依赖外部全局 Godot 安装 | 不可复现，且无法保证团队与 CI 使用同一版本 | 统一改用 `tools/godot/4.6.2-stable/` |
| 继续把路径写死为唯一长期资源寻址方式 | 4.4 / 4.5 强化 UID 工作流后，这种做法对大规模目录调整更脆弱 | 在资源目录稳定后，逐步转向 UID 友好的工作流 |

## 对当前周循环代码的直接建议

- 组合枚举、多层候选列表、临时队列这类结构，不要为了“看起来强类型”继续硬塞嵌套 typed arrays。
- 对真正需要强约束的运行时结构，优先考虑：
  - 顶层 `Array[Dictionary]`
  - 顶层 `Dictionary[String, Dictionary]`
  - 单独的状态类或资源对象
