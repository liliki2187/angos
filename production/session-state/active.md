# Session State

**Date**: 2026-04-05
**Task**: Split the Godot codebase so `gd_project/` becomes the formal runtime project root
**Status**: In Progress

## Completed In This Pass

- Moved the Godot runtime root into `gd_project/`
- Kept technical docs under `docs/` and import/export tooling under `scripts/`
- Updated repository onboarding docs to treat `gd_project/` as the formal development root
- Updated Codex skill guidance to read technical defaults from `docs/technical-preferences.md`
- Updated CI and export tooling to build from `gd_project/project.godot`
- Preserved the existing HTML prototype and design-document split outside the Godot runtime

## Current Source Of Truth

- Runtime behavior: `gd_project/scenes/` and `gd_project/Assets/`
- Godot project root: `gd_project/project.godot`
- Technical defaults and supporting tooling: `docs/` and `scripts/`
- Gameplay design: `design/gdd/`
- Architecture boundaries: `docs/architecture/`
- Execution state: `production/`
- Git collaboration authority: `docs/onboarding/git-collaboration.md`

## Immediate Next Work

1. Continue extracting state/content/UI boundaries from `gd_project/scenes/gameplay/full_chain/FullChainGame.gd`
2. Keep trimming stale docs and prototype remnants that still assume the pre-split root layout
3. Start the first real `specs/` packet when the next feature is selected

## Notes

- `prototype/fullchain_demo/` is treated as a generated distribution package, not source of truth.
- HTML reference sources remain under `design/prototypes/html/`.
- New Godot runtime work should happen under `gd_project/`; supporting scripts remain under `scripts/`.
