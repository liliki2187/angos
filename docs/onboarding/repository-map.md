# Repository Map

This document is the quickest way to identify what is canonical, what is reference-only, and what is generated.

## Canonical Layers

- `scenes/`: Godot runtime scenes and scene-owned scripts
- `Assets/`: runtime assets and import inputs that belong to the game
- `design/gdd/`: canonical gameplay design
- `docs/architecture/`: architecture decisions and technical boundaries
- `production/`: execution state, sprint context, and handoff
- `scripts/`: automation, import, rendering, and packaging scripts
- `specs/`: future feature packets and acceptance-driven work

## Reference-Only Layers

- Root HTML prototype files such as `world-mysteries-full-chain.html`
- `design/htmls/`: HTML prototypes and UI experiments
- `design/systems/`: supporting system analysis and older design decomposition
- Most root-level `docs/*.md`: legacy design docs and historical reference material

## Generated Or Rebuildable Layers

- `prototype/fullchain_demo/`: generated distribution package output
- `prototype/*.zip`: generated packaged exports
- `scripts/__pycache__/`: Python bytecode cache

## Notes On Legacy Material

- Prototype HTML entry points live under `design/htmls/`; duplicate root-level `docs/` mirrors have been removed.
- `design/generated-settlement-reference/` remains a reference asset area; some outputs are still consumed by the current Godot UI preview flow.
- `design/original-art-reference/` remains the current art-reference archive because project skills already depend on that path.
