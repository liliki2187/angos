# Angus / 世界未解之谜周刊

本仓库包含 Angus 的 Godot MVP、历史 HTML 原型、设计文档，以及项目本地自动化技能。
当前生效的 Godot 运行时位于 `gd_project/`，配套文档与工具位于 `docs/` 和 `scripts/`。

## 规范位置

- 运行时项目根目录：`gd_project/`
- 游戏运行时内容：`gd_project/scenes/` 与 `gd_project/Assets/`
- 运行时配套文档与工具：`docs/` 与 `scripts/`
- 游戏设计：`design/gdd/`
- 架构决策：`docs/architecture/`
- 执行状态：`production/`
- 入门与协作规则：`docs/onboarding/`
- 功能规格包：`specs/`

## 参考与原型材料

- `design/prototypes/html/` 是 HTML 实验和旧网页可玩 Demo 的参考层。
- `prototype/` 已移除；历史分发产物与打包流程归档在 `_obsolete/scripts/release/`。
- `_obsolete/` 是失效材料的归档区。除非明确在做历史查询或恢复，否则默认忽略。

## 建议先读

- `docs/README.md`
- `docs/onboarding/repository-map.md`
- `docs/onboarding/git-collaboration.md`
- `docs/technical-preferences.md`
- `gd_project/README.md`
- `production/session-state/active.md`

## 备注

- 请使用 Godot 4.3 打开 `gd_project/project.godot`。
- 运行时开发工作应把 `gd_project/` 视为正式游戏目录。
- 如果你在处理 HTML 原型源码，默认把它当作参考材料，除非某份 GDD 或 ADR 明确将对应行为提升为正式游戏规则。

