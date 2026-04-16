# 文档总览

这是仓库文档的统一入口。

## 规范层级

- 游戏设计：`../design/gdd/`
- 补充分析：`../design/systems/`
- 架构决策：`architecture/`
- 技术默认约束：`../docs/technical-preferences.md`
- 入门与协作规则：`onboarding/`
- AI 协作偏好与避坑规则：`onboarding/ai-collaboration-guidance.md`
- 生产执行状态：`../production/`

## 状态说明

| 区域 | 当前位置 | 状态 |
|------|----------|------|
| 运行时游戏规则 | `../design/gdd/` | 规范来源 |
| 系统分析与更深层拆解 | `../design/systems/` | 参考层，仍有价值 |
| Git / 仓库入门 | `onboarding/` | 规范来源 |
| 技术工作流与工具 | `../docs/`、`../scripts/` | 规范来源 |
| 活跃执行计划 | `plans/` + `../production/` | 若仍在执行则视为规范来源 |
| GDD 之前阶段的历史设计文档 | `archive/legacy-design/` | 已归档 |
| 超出当前 MVP 范围的延期系统 | `archive/deferred-design/` | 归档参考 |
| 开发时间线记录 | `dev-logs/` | 历史记录 |
| 失效的跨层内容 | `../_obsolete/` | 默认忽略 |

## 发生过什么变化

旧的 `docs/` 根层玩法设计文档，与新的 `design/gdd/` 和 `design/systems/` 层发生了重叠。
它们已不再被视为当前的真实来源。

仓库现在使用以下拆分：

1. `design/gdd/` 保存当前正式玩法规则
2. `design/systems/` 保存补充分析、模板与深入拆解
3. `docs/archive/` 保存历史设计或延期设计材料
4. `_obsolete/` 保存“保留但失效”的内容，除非明确要求查历史，否则应忽略

## 建议阅读顺序

1. `onboarding/repository-map.md`
2. `../docs/technical-preferences.md`
3. `../design/gdd/README.md`
4. `../production/session-state/active.md`
