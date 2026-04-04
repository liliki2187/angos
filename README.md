# Angus / 世界未解之谜周刊

This repository contains the Angus Godot MVP, historical HTML prototypes, design documentation, and project-local automation skills.

## Canonical Locations

- Runtime: `scenes/` and `Assets/`
- Gameplay design: `design/gdd/`
- Architecture decisions: `docs/architecture/`
- Execution state: `production/`
- Onboarding and collaboration rules: `docs/onboarding/`
- Feature packets: `specs/`

## Reference And Prototype Material

- Root HTML files and `design/htmls/` are reference or prototype layers, not the canonical runtime.
- `prototype/` is for distributable prototype packages. Generated package outputs are rebuildable and ignored by default.

## First Reads

- `docs/README.md`
- `docs/onboarding/repository-map.md`
- `docs/onboarding/git-collaboration.md`
- `docs/technical-preferences.md`
- `production/session-state/active.md`

## Notes

- The current MVP runtime is Godot 4.3.
- If you work on the HTML prototype sources, treat them as reference material unless a GDD or ADR explicitly promotes behavior into the game.
