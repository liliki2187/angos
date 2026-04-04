# Angus / 世界未解之谜周刊

This repository contains the Angus Godot MVP, historical HTML prototypes, design documentation, and project-local automation skills.
The active Godot runtime now lives under `gd_project/`, while supporting docs and tooling remain under `docs/` and `scripts/`.

## Canonical Locations

- Runtime project root: `gd_project/`
- Gameplay runtime: `gd_project/scenes/` and `gd_project/Assets/`
- Runtime support docs and tools: `docs/` and `scripts/`
- Gameplay design: `design/gdd/`
- Architecture decisions: `docs/architecture/`
- Execution state: `production/`
- Onboarding and collaboration rules: `docs/onboarding/`
- Feature packets: `specs/`

## Reference And Prototype Material

- `design/prototypes/html/` is the reference / prototype layer for HTML experiments and legacy playable web demos.
- `prototype/` is for distributable prototype packages. Generated package outputs are rebuildable and ignored by default.

## First Reads

- `docs/README.md`
- `docs/onboarding/repository-map.md`
- `docs/onboarding/git-collaboration.md`
- `docs/technical-preferences.md`
- `gd_project/README.md`
- `production/session-state/active.md`

## Notes

- Open `gd_project/project.godot` in Godot 4.3.
- Treat `gd_project/` as the formal game-development directory for runtime work.
- If you work on the HTML prototype sources, treat them as reference material unless a GDD or ADR explicitly promotes behavior into the game.
