# Godot MVP Foundation

**Status**: Active
**Stage**: Early Production
**Primary Goal**: Stabilize the Godot weekly-loop MVP as the canonical runtime while reducing repository confusion.

## In Scope

- Keep Godot as the only canonical runtime target
- Preserve HTML and visual prototypes as reference material
- Strengthen directory ownership and onboarding clarity
- Reduce repository noise from generated packages and local outputs
- Prepare for config-pipeline and runtime modularization work

## Explicitly Out Of Scope

- Large gameplay redesigns
- Broad scene refactors without spec or ADR backing
- New major prototype branches
- Polishing release packaging as if it were a shipping build pipeline

## Exit Criteria

- A new contributor can identify the canonical runtime, design, architecture, and production layers in under 10 minutes
- Production workspace contains stage, sprint, backlog, risks, and handoff structure
- Generated package outputs no longer pollute normal `git status`
- Git collaboration guidance is no longer contradictory across docs
