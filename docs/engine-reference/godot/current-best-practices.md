# Godot 4.6.2 当前最佳实践

最后核验：2026-04-09

## 工具链

- 本地开发、smoke test、CI 应统一锁定 `Godot 4.6.2 stable`。
- Windows 开发环境使用 Standard 包即可；当前项目不需要 `.NET`。
- `scripts/run_weekly_run_smoke_tests.ps1` 默认优先查找 `tools/godot/` 下的仓库内引擎。

## GDScript / 状态建模

- 避免把“嵌套 typed collections”当作正式建模手段。
- 对系统状态，优先使用“顶层 typed array / typed dictionary + 显式转换函数”的组合。
- 对复杂长期状态，优先拆成 `RefCounted` / `Resource` 类，而不是在一个大字典里无限生长。

## UI / 调试

- Godot 4.6 的 `pivot_offset_ratio` 适合用在会缩放、旋转、居中锚定的 `Control` 节点上。
- 输出面板现在支持直接点开报错文件，日常调试优先走 Godot 4.6.2 本地编辑器，不要再回退到旧版环境。
- 4.5 的脚本回溯能力对定位运行时问题很有价值；排查疑难脚本问题时应开启对应调试设置。

## 资源与引用

- 资源目录稳定前，可以继续使用路径引用；但一旦开始做大规模重组，应优先转向 UID 友好的工作流。
- 不要再把资源移动后的手工改路径当作常规维护手段。

## 当前与 Angus 最相关的实践结论

1. 版本统一比追逐单个新 API 更重要。
2. 4.6.2 解决不了 `Array[Array[String]]` 语法问题，代码结构必须自己收紧。
3. 当前 sprint 最值得利用的 4.6 能力是更好的 UI 调试与更清晰的 `Control` pivot 工作流。
