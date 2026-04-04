# Session State

**Date**: 2026-04-04
**Task**: Execute repository governance foundation work from `docs/plans/project-structure-collaboration-governance-plan.md`
**Status**: In Progress

## Completed In This Pass

- Confirmed the governance plan and `docs/technical-preferences.md` as current structural guidance
- Added the missing `production/` workspace skeleton:
  - `stage.txt`
  - `milestones/`
  - `sprints/`
  - `backlog/`
  - `risk-register/`
  - `handoff/`
  - `roles/`
- Added onboarding docs for repository map and Git collaboration
- Updated root and AI-facing docs to point at canonical directories
- Added ignore rules for generated demo packages and Python cache output
- Added `.gdignore` markers for non-runtime prototype/reference directories
- Removed tracked Python cache output from `scripts/__pycache__/`
- Removed duplicate prototype HTML mirrors from the root `docs/` directory
- Moved the generated demo packaging workflow under `scripts/release/`
- Archived superseded root-level gameplay design docs under `docs/archive/`
- Added unified documentation indexes in `docs/` and `design/gdd/`
- Updated the documentation map so legacy and deferred docs no longer masquerade as current authority
- Consolidated all HTML prototype sources under `design/prototypes/html/`
- Moved prototype-only web assets out of `Assets/` into `design/prototypes/html/full-chain-demo/Assets/`
- Split scripts into `git/`, `import/`, `prototypes/`, `release/`, `render/`, `setup/`, and `share/`
- Split runtime scenes into `autoload/`, `gameplay/`, and `ui/`
- Removed obsolete Unity-era leftovers from `Assets/Editor/` and `Packages/`
- Cleared generated prototype outputs from `prototype/`

## Current Source Of Truth

- Runtime behavior: Godot scenes and assets
- Gameplay design: `design/gdd/`
- Architecture boundaries: `docs/architecture/`
- Execution state: `production/`
- Git collaboration authority: `docs/onboarding/git-collaboration.md`

## Immediate Next Work

1. Continue low-risk cleanup of legacy and duplicated reference entry points
2. Start the next runtime-boundary extraction pass from `FullChainGame.gd`
3. Start the first real `specs/` packet when the next feature is selected

## Notes

- `prototype/fullchain_demo/` is treated as a generated distribution package, not source of truth.
- HTML reference sources now live under `design/prototypes/html/`, not the repo root.
- The next high-value technical move remains config-pipeline work plus runtime boundary extraction.
