# Sprint: Repository Governance Foundation

**Window**: 2026-04-04 to 2026-04-11
**Status**: Active
**Source Plan**: `docs/plans/project-structure-collaboration-governance-plan.md`

## Sprint Goals

1. Land the minimum production workspace needed for ongoing collaboration
2. Establish a single Git-collaboration authority entry point
3. Clarify which directories are canonical, reference-only, or generated
4. Reduce workspace noise from generated demo packages and caches

## Planned Deliverables

- `production/stage.txt`
- production skeleton with backlog, sprint, milestone, risk, and handoff docs
- onboarding docs for repository map and Git collaboration
- updated root README and AI handoff docs
- ignore rules for generated demo packages and Python cache output

## Done Definition

- Core governance docs exist and reference each other coherently
- `git status` is not polluted by `prototype/fullchain_demo` or `scripts/__pycache__`
- Onboarding materials point to canonical directories instead of scattered assumptions
