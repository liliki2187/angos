# Active Risk Register

## R1. Monolithic Runtime Script

- **Risk**: `gd_project/scenes/gameplay/full_chain/FullChainGame.gd` still owns too much state, content, and presentation logic.
- **Impact**: High
- **Mitigation**: Keep new work tied to ADR boundaries and plan extraction slices before adding more mechanics.

## R2. Source-Of-Truth Drift

- **Risk**: HTML prototypes, legacy docs, and Godot runtime can still diverge.
- **Impact**: High
- **Mitigation**: Treat `design/gdd/` plus Godot runtime as canonical and mark prototypes as reference-only.

## R3. Generated Output Noise

- **Risk**: Demo packaging and local cache outputs make the worktree noisy and harder to review.
- **Impact**: Medium
- **Mitigation**: Ignore generated package paths and keep rebuildable outputs script-owned.

## R4. Git Workflow Ambiguity

- **Risk**: Different docs previously gave incompatible push instructions.
- **Impact**: Medium
- **Mitigation**: Route all Git collaboration guidance through `docs/onboarding/git-collaboration.md`.
