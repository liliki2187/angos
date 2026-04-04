# Documentation Map

This is the unified entry point for repository documentation.

## Canonical Layers

- Gameplay design: `../design/gdd/`
- Supporting analysis: `../design/systems/`
- Architecture decisions: `architecture/`
- Technical defaults: `../docs/technical-preferences.md`
- Onboarding and collaboration rules: `onboarding/`
- Production execution state: `../production/`

## Status Guide

| Area | Current Home | Status |
|------|--------------|--------|
| Runtime gameplay rules | `../design/gdd/` | Canonical |
| System analysis and deeper breakdowns | `../design/systems/` | Reference, still useful |
| Git / repo onboarding | `onboarding/` | Canonical |
| Technical workflow and tooling | `../docs/`, `../scripts/` | Canonical |
| Active execution plans | `plans/` + `../production/` | Canonical if still active |
| Historical design docs from pre-GDD phase | `archive/legacy-design/` | Archived |
| Deferred systems outside current MVP | `archive/deferred-design/` | Archived reference |
| Development chronology | `dev-logs/` | Historical record |

## What Changed

The old root-level gameplay design docs under `docs/` were overlapping with the newer `design/gdd/` and `design/systems/` layers.
They are no longer treated as current source of truth.

The repository now uses this split:

1. `design/gdd/` for current gameplay rules
2. `design/systems/` for supporting analysis, templates, and deeper breakdowns
3. `docs/archive/` for legacy or deferred design material

## Recommended Read Order

1. `onboarding/repository-map.md`
2. `../docs/technical-preferences.md`
3. `../design/gdd/README.md`
4. `../production/session-state/active.md`
