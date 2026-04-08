# 会话状态

**日期**：2026-04-05  
**任务**：拆分 Godot 代码库，使 `gd_project/` 成为正式运行时项目根目录  
**状态**：进行中

## 本轮已完成

- 将 Godot 运行时根目录迁移到 `gd_project/`
- 保留技术文档在 `docs/`，导入 / 导出工具在 `scripts/`
- 更新仓库入门文档，使其将 `gd_project/` 视为正式开发根目录
- 更新 Codex 技能指引，使其从 `docs/technical-preferences.md` 读取技术默认值
- 更新 CI 与导出工具，使其从 `gd_project/project.godot` 构建
- 保留 Godot 运行时之外的既有 HTML 原型与设计文档拆分

## 当前真实来源

- 运行时行为：`gd_project/scenes/` 与 `gd_project/Assets/`
- Godot 项目根：`gd_project/project.godot`
- 技术默认值与配套工具：`docs/` 与 `scripts/`
- 玩法设计：`design/gdd/`
- 架构边界：`docs/architecture/`
- 执行状态：`production/`
- Git 协作权威入口：`docs/onboarding/git-collaboration.md`

## 紧接着要做的事

1. 继续从 `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` 中抽离状态 / 内容 / UI 边界
2. 继续清理仍然假设旧根目录布局的陈旧文档和原型残留
3. 当下一个功能被选定后，启动第一份真正的 `specs/` 包

## 备注

- 历史分发包链路已归档到 `_obsolete/scripts/release/`，不再作为活跃目录。
- HTML 参考源码保留在 `design/prototypes/html/`。
- 新的 Godot 运行时工作应落在 `gd_project/` 下；配套脚本继续放在 `scripts/`。

