# Angus 项目交接说明（给 AI）

> 更新时间：2026-04-04
> 目标：让接手者先找到权威层，再开始动手。

## 先读这些

1. `docs/onboarding/repository-map.md`
2. `docs/onboarding/git-collaboration.md`
3. `docs/technical-preferences.md`
4. `production/session-state/active.md`

## 当前权威层

- Runtime: Godot，目录以 `scenes/` 与 `Assets/` 为准
- Gameplay design: `design/gdd/`
- Architecture: `docs/architecture/`
- Production state: `production/`

## 参考层

- 根目录 HTML 原型
- `design/htmls/`
- 历史设计文档与分析文档

这些内容仍然有价值，但默认不作为运行时权威。

## 当前项目判断

- 项目阶段：Early Production
- 当前主线：稳定 Godot 周循环 MVP，并逐步把目录和协作边界收紧
- 当前高价值工作：配置管线、运行时边界拆分、最小自动化验证

## Git 规则

不要复述旧文档里的推送习惯。Git 协作规则只看：

- `docs/onboarding/git-collaboration.md`

## 给接手 AI 的一句话

先确认你改的是不是权威层；如果只是参考层，请先说明它和 Godot 主线或 `design/gdd/` 的关系，再决定是否继续改。

