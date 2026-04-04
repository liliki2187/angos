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

- `design/prototypes/html/`: HTML prototypes, labs, and legacy web demos
- `design/systems/`: supporting system analysis and older design decomposition
- `docs/archive/`: legacy or deferred design material

## Generated Or Rebuildable Layers

- `prototype/fullchain_demo/`: generated distribution package output
- `prototype/*.zip`: generated packaged exports
- `scripts/__pycache__/`: Python bytecode cache

## Notes On Legacy Material

- Prototype HTML entry points now live under `design/prototypes/html/`; root-level HTML experiments have been removed from the repo root.
- The self-contained full-chain web demo source now lives under `design/prototypes/html/full-chain-demo/`.
- `design/generated-settlement-reference/` remains a reference asset area; some outputs are still consumed by the current Godot UI preview flow.
- `design/original-art-reference/` remains the current art-reference archive because project skills already depend on that path.
- Avatar-cropping rules now live at `docs/tools/avatar-cropping.md`.
