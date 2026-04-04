# Technical Preferences

<!-- Project-specific technical defaults for Angus. -->
<!-- Update this file when the team intentionally changes coding standards, test strategy, or engine-level constraints. -->

## Engine & Language

- **Engine**: Godot 4.3
- **Primary Runtime Language**: GDScript
- **Supporting Tool Languages**: PowerShell, Python, small amounts of C# or Node.js for tooling only
- **Rendering**: 2D / UI-heavy Godot project using the `mobile` rendering method from project settings
- **Physics**: Minimal. This project is primarily driven by UI, state transitions, and formulas rather than physics simulation.

## Naming Conventions

- **Classes / Scene Scripts**: PascalCase when a script is paired to a scene or feature, for example `MainMenu.gd`, `EventCheck.gd`, `FullChainGame.gd`
- **Variables**: snake_case, for example `selected_region_id`, `editorial_profile`
- **Functions**: snake_case, for example `_refresh_all()`, `_calculate_node_probabilities()`
- **Signals / Events**: snake_case action or past-tense names, for example `closed`
- **Scenes**: PascalCase `.tscn` matching the scene purpose, for example `MainMenu.tscn`, `MysteryBroadsheetModal.tscn`
- **Constants**: UPPER_SNAKE_CASE, for example `DIFFICULTY_P`, `MACRO_LABELS`, `PSD_UI_PREVIEW_SIZE`
- **Script files**:
  - Runtime scene scripts follow the existing PascalCase pairing pattern
  - Utility and pipeline scripts under `scripts/` may use snake_case or verb-oriented names

## Directory Conventions

- **Runtime scenes**: `scenes/`
- **Runtime assets**: `Assets/`
- **Editor plugins / addons**: `addons/`
- **Automation / import / packaging scripts**: `scripts/`
- **Canonical gameplay design docs**: `design/gdd/`
- **System analysis and supporting design notes**: `design/systems/`
- **Architecture decisions**: `docs/architecture/`
- **Production tracking and coordination**: `production/`
- **HTML prototypes and reference experiments**: reference only, not runtime source of truth

## Source Of Truth Rules

- **Godot is the only canonical runtime** for the current MVP and weekly loop.
- **`design/gdd/` is the canonical design layer** for current gameplay behavior.
- **HTML prototypes are reference artifacts only**. If a rule from HTML is promoted into the game, it must be reflected in `design/gdd/` before being treated as canonical.
- **`Globals` must stay lightweight** and limited to bootstrapping, scene paths, debug logging, and small shared helpers. It must not become the permanent home of gameplay state.

## Architecture Preferences

- Prefer separating **content data**, **weekly state / rules**, and **scene presentation**.
- Avoid expanding monolithic scene scripts when a new slice can be extracted cleanly.
- New gameplay changes should be traceable to a GDD, spec, or ADR.
- When introducing a new technical boundary or workflow with long-term impact, document it in `docs/architecture/`.

## Performance Budgets

- **Target Framerate**: 60 FPS
- **Frame Budget**: 16.6 ms
- **Primary Risk Area**: UI refresh churn and monolithic full-loop scene logic
- **Draw Calls**: [TO BE CONFIGURED]
- **Memory Ceiling**: [TO BE CONFIGURED]
- **Load Time Budget**: [TO BE CONFIGURED]

## Testing

- **Recommended Framework**: GdUnit4 or GUT
- **Minimum Coverage Strategy**: prioritize critical formulas and phase/state transitions before broad coverage targets
- **Required Regression Coverage Areas**:
  - Event-check probability and tier resolution
  - Weekly phase transitions
  - Settlement formulas and subscriber updates
  - Unlock rules and hidden-node visibility
  - Content/config parsing once the config pipeline lands

## Forbidden Patterns

- Do not treat HTML prototypes as equal runtime implementation targets.
- Do not put new long-lived gameplay state into `Globals`.
- Do not mix content data, state ownership, formulas, and UI refresh into new monolithic scripts without a clear reason.
- Do not hardcode new core gameplay rules without updating the relevant GDD or ADR.
- Do not introduce new root-level entry files for experiments when they belong under `design/`, `prototype/`, or `scripts/`.

## Allowed Libraries / Addons

- `nklbdev.importality` for PSD and import workflow
- Project-local scripts under `scripts/`
- GitHub Actions workflows under `.github/workflows/`
- Additional third-party addons only after they are explicitly accepted and documented

## Build / Export Defaults

- Keep Godot export presets in `export_presets.cfg`
- Treat CI builds and export automation as repository-owned tooling
- Prefer reproducible packaging scripts over manual copy-paste release steps

## Architecture Decisions Log

- `ADR-0001`: Godot Week Loop State and Data Boundaries
