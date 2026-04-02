# ADR-0001: Godot Week Loop State and Data Boundaries

## Status
Accepted

## Date
2026-03-31

## Context

### Problem Statement

Angus already has a playable Godot weekly prototype, but core behavior currently lives in a large scene script that owns content definitions, phase transitions, formulas, and UI refresh logic together. At the same time, HTML prototypes and legacy docs still exist as reference sources. Without a clear boundary, every new feature risks deepening prototype debt and reintroducing rule drift.

### Constraints

- The current live prototype is in Godot 4.3.
- The team needs to preserve momentum and avoid restarting the runtime.
- HTML reference assets still contain useful design information, but should not remain an equal implementation source.
- Team bandwidth favors incremental extraction over large rewrites.

### Requirements

- Must keep Godot as the only canonical runtime for the current MVP.
- Must separate weekly state ownership from scene presentation logic.
- Must support future migration of content definitions out of hardcoded arrays and dictionaries.
- Must preserve the existing playable loop while enabling safer iteration.

## Decision

Angus will treat the Godot weekly loop as the only implementation source of truth for the MVP. Weekly runtime state, content data, and scene presentation will be treated as separate concerns.

### Architecture Diagram

```text
Content Data (regions, nodes, staff, story templates)
        |
        v
Weekly State / Rules Layer
  - week/day
  - macro stats
  - subscribers
  - editorial profile
  - weekly clues
  - current phase
        |
        v
Scene/UI Layer
  - menu
  - exploration panels
  - editorial layout
  - summary presentation
```

### Key Interfaces

- **Content Data -> Weekly State**
  - Region definitions
  - Node definitions
  - Staff definitions
  - Story filler templates
- **Weekly State -> Scene/UI**
  - Current phase
  - Available regions/nodes
  - Probability previews
  - Story pool
  - Settlement summary
- **Scene/UI -> Weekly State**
  - Selected region/node
  - Selected staff
  - Slot assignment
  - Phase transition actions

### Additional Rules

- `Globals` should remain limited to bootstrapping, scene paths, theme helpers, and debug logging. It should not become the permanent home of gameplay state.
- HTML prototypes remain reference artifacts only. Any rule promoted from HTML must be re-documented in `design/gdd/` before being treated as canonical.
- Story synthesis is explicitly outside current MVP runtime scope.

## Alternatives Considered

### Alternative 1: Keep expanding the monolithic `FullChainGame.gd`

- **Description**: Continue building directly inside the existing scene script.
- **Pros**: Fastest short-term implementation speed.
- **Cons**: Harder to test, harder to document, harder to move to config-driven content, and more likely to create rule drift.
- **Rejection Reason**: Acceptable for proving the loop, not acceptable for sustained development.

### Alternative 2: Keep HTML and Godot as parallel canonical runtimes

- **Description**: Continue treating both the HTML full-chain reference and Godot prototype as equal sources of truth.
- **Pros**: Easier to compare old and new mechanics.
- **Cons**: Doubles documentation burden, invites divergence, and slows engineering focus.
- **Rejection Reason**: The project already suffers from parallel-branch ambiguity; this would worsen it.

### Alternative 3: Rebuild from scratch around a new architecture before documenting

- **Description**: Pause feature work and rewrite the runtime into a clean modular structure immediately.
- **Pros**: Best long-term purity.
- **Cons**: High interruption cost, risky loss of current behavior, and poor fit for team momentum.
- **Rejection Reason**: Too expensive relative to the value of incremental extraction.

## Consequences

### Positive

- One canonical runtime direction
- Cleaner separation between rules, content, and presentation
- Better support for upcoming config-pipeline work
- Documentation can now map to concrete system boundaries

### Negative

- Some existing code will need staged extraction and renaming.
- Team members must stop treating HTML prototypes as equal implementation targets.

### Risks

- **Risk**: Extraction work slows visible feature progress.
  - **Mitigation**: Tie refactors to specific GDD and ADR outputs, not open-ended cleanup.
- **Risk**: Documentation and runtime still diverge during transition.
  - **Mitigation**: Treat `design/gdd/` as the canonical design source for all new changes.
- **Risk**: Content remains hardcoded longer than planned.
  - **Mitigation**: Prioritize the content/config pipeline after the remaining MVP GDDs.

## Performance Implications

- **CPU**: Neutral to positive if update logic becomes more targeted.
- **Memory**: Neutral; structured state may add light overhead but reduce duplication.
- **Load Time**: Neutral for MVP, potentially better once content data is externalized.
- **Network**: None.

## Migration Plan

1. Keep the current playable scene operational.
2. Finish canonical MVP documentation in `design/gdd/`.
3. Identify state fields that belong to a weekly state layer versus presentation helpers.
4. Move region/node/staff/story definitions toward external content data or typed resources.
5. Refactor scene code in slices rather than rewriting all at once.

## Validation Criteria

- New gameplay changes can name which GDD and ADR they implement.
- Weekly state and content definitions are no longer mixed arbitrarily with UI refresh code.
- HTML reference features are only promoted after documentation updates.
- The team can add new nodes or story content without editing unrelated UI logic.

## Related Decisions

- `design/gdd/game-concept.md`
- `design/gdd/game-pillars.md`
- `design/gdd/systems-index.md`
