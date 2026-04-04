# Cursor 新对话 · 研发无缝衔接指引

> 用途：在新对话里快速恢复正确上下文，而不是继续沿用旧假设。
> 工作区路径（当前）：`E:\angus\angus`
> 最后更新：2026-04-04

## 先读顺序

1. `docs/README.md`
2. `docs/onboarding/repository-map.md`
3. `docs/onboarding/git-collaboration.md`
4. `docs/technical-preferences.md`
5. `production/session-state/active.md`

## 当前项目判断

- 项目阶段：Early Production
- 当前主线：Godot 4.3 周循环 MVP
- 参考层仍保留：根目录 HTML 原型、`design/htmls/`、`design/systems/`、`docs/archive/`
- 当前重点：目录治理、配置管线、运行时边界拆分，而不是继续扩张原型分支

## 权威来源

- Runtime: `scenes/` 和 `Assets/`
- Gameplay design: `design/gdd/`
- Architecture: `docs/architecture/`
- Execution state: `production/`
- Git collaboration rule: `docs/onboarding/git-collaboration.md`

## 新对话常见误区

- 不要把根目录 HTML 当成 Godot 运行时权威
- 不要把旧 `docs/*.md` 默认当成当前设计主线
- 不要复述旧的 Git 推送说法，先看 `git remote -v` 再看 Git 协作文档
- 不要把生成包或缓存目录当源码

## 当前建议关注点

1. `scenes/FullChainGame.gd` 的边界拆分
2. 内容配置和数据入口
3. 公式与阶段切换的最小自动化验证
4. 继续清理 legacy/reference/generated 层的边界

## 给新对话 AI 的模板

```text
请接手 Angus 仓库，工作区是 E:\angus\angus。

先读：
1. docs/README.md
2. docs/onboarding/repository-map.md
3. docs/onboarding/git-collaboration.md
4. docs/technical-preferences.md
5. production/session-state/active.md

当前目标不是随意扩功能，而是沿着现有 GDD/ADR/production 状态继续推进。
如果你准备修改的是 HTML 原型或旧 docs，请先说明它和 Godot 主线的关系。
```
