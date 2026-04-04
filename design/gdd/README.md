# GDD Index

This directory is the canonical gameplay design layer for Angus.

## Current Canonical Docs

| Document | Purpose |
|----------|---------|
| `game-concept.md` | High-level product identity, fantasy, scope, and loop |
| `game-pillars.md` | Decision filter for scope and implementation tradeoffs |
| `systems-index.md` | Current system map and design priority |
| `weekly-run-loop.md` | Week structure, phase transitions, persistent vs weekly state |
| `exploration-and-node-dispatch.md` | Region/node browsing, staffing, dispatch validation |
| `event-check-resolution.md` | Split binomial checks, difficulty mapping, opponent negation |
| `editorial-layout-and-settlement.md` | Story pool, six-slot layout, settlement formulas |

## Supporting Docs That Still Matter

These are not the top authority layer, but they still carry useful analysis:

- `../systems/exploration.md`
- `../systems/editing.md`
- `../systems/event-check-design.md`
- `../systems/event-check-config-template.md`
- `../systems/event-check-scripts.md`
- `../systems/attributes.md`
- `../systems/factions.md`

## Archived Replacements

| Older Doc | Current Replacement |
|-----------|---------------------|
| `docs/archive/legacy-design/世界未解之谜周刊_全链条版设计文档汇总.md` | `game-concept.md` + `systems-index.md` |
| `docs/archive/legacy-design/世界未解之谜周刊_探索部分设计文档.md` | `weekly-run-loop.md` + `exploration-and-node-dispatch.md` |
| `docs/archive/legacy-design/事件检定系统设计文档.md` | `event-check-resolution.md` + supporting `../systems/event-check-*` docs |
| `docs/archive/legacy-design/骰子判定玩法_最终版.md` | `event-check-resolution.md` |
| `docs/archive/legacy-design/报刊结算出版玩法设计文档.md` | `editorial-layout-and-settlement.md` |
| `docs/archive/legacy-design/策划配置表模板_事件检定字段.md` | `../systems/event-check-config-template.md` |
| `docs/archive/legacy-design/事件脚本示例_3个事件配置与期望体验.md` | `../systems/event-check-scripts.md` |

## Deferred Design

- `docs/archive/deferred-design/故事合成与报道编写系统设计文档.md`

This system is not part of the current Godot MVP authority layer.
If it returns to active scope, promote it back into `design/gdd/` or `design/systems/` before treating it as live design.
