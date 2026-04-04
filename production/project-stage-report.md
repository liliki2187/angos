# Project Stage Analysis

**Date**: 2026-04-04
**Stage**: Production (early)

## Completeness Overview

- **Design**: ~75% complete. Canonical `design/gdd/` documents now exist, though some older `docs/` design material still needs clearer legacy/reference labeling.
- **Code**: ~55% complete for MVP. Godot has a playable weekly vertical prototype with menu flow, exploration, event checks, editorial layout, and settlement, but architecture is still monolithic.
- **Architecture**: ~35% complete. Engine choice is locked and ADR work has started, but runtime boundaries are not yet enforced in code.
- **Production**: ~55% complete. A durable `production/` workspace now exists with stage, sprint, backlog, risk, handoff, and session-state artifacts, but it still needs regular operational use.
- **Tests**: ~0-5% complete. No project-owned automated gameplay test structure was found.

## Scope Check: Godot MVP

### Original Scope

Source of truth: `docs/plans/godot-full-chain-implementation-plan.md`

1. Global week state and loop skeleton
2. Exploration map and node execution
3. Event check integration into exploration
4. Clue-to-story conversion and editorial scene
5. Economic settlement and cross-week persistence
6. Content configuration pipeline

### Current Scope

Implemented or partially implemented in Godot:

1. Main menu entry into the current full-chain prototype
2. Unified weekly prototype in `gd_project/scenes/gameplay/full_chain/FullChainGame.gd`
3. Region and node selection with unlock rules
4. Staff dispatch and split event checks
5. Weekly clue generation
6. Automatic story generation and filler padding
7. Six-slot editorial layout
8. Settlement with subscriptions, profile drift, and macro-stat updates
9. Next-week transition

### Scope Additions (not in original plan as core deliverables)

| Addition | Justified? | Effort |
|----------|------------|--------|
| Responsive layout and presentation polish inside the Godot prototype | Yes | S |
| Main menu settlement preview and extra showcase entry points | Yes, but secondary | S |
| Continued HTML reference branch with story synthesis docs | Yes as reference, not as MVP runtime | M |

### Scope Removals / Not Yet Landed

| Removed or Missing Item | Reason | Impact |
|-------------------------|--------|--------|
| Config-driven content pipeline | Not implemented yet | Slows future iteration and content scaling |
| Formal save/load | Deferred | Acceptable for MVP, risky for longer sessions |
| Story synthesis as a separate Godot phase | Intentionally deferred | Keeps MVP narrow, but leaves one future design branch unresolved |

### Bloat Score

- Original items: 6
- Current implemented core items: 9
- Items added beyond original plan: 3 (+50% at repo level, but only +2 meaningful runtime additions)
- Items removed or deferred: 3
- **Verdict**: Minor creep at repository level, but the Godot MVP itself remains on track because most additions are presentation or reference-layer work rather than new mandatory gameplay branches.

### Risk Assessment

- **Schedule Risk**: Medium. The project already has a playable loop, but config work and architecture cleanup still need attention.
- **Quality Risk**: High. Core behavior is concentrated in a large scene script, which makes balancing and iteration fragile.
- **Integration Risk**: Medium. HTML reference logic and Godot runtime are close enough to cross-pollinate, but still need clearer source-of-truth rules.

## Gaps Identified

1. There was no canonical game-concept, pillars, or systems index. This is now being corrected, but those documents must become the default planning layer.
2. The project has a playable runtime but no formal architecture boundary between state, content, and UI.
3. Content is still too hardcoded for rapid iteration.
4. There is no owned test strategy for formulas or phase transitions.
5. The repo now has a durable production-state workspace, but it still needs the first real spec-driven feature packet and consistent weekly upkeep.

## Recommended Next Steps

1. Use the new `design/gdd/` documents as the canonical design layer.
2. Extract `Clue Inventory and Story Conversion` and `Macro Attributes and Unlock Pressure` into dedicated GDDs next.
3. Follow the ADR to separate weekly state ownership from scene presentation.
4. Build the content/config pipeline before broadening content volume.
5. Use the new `production/` workspace as the default execution layer and start the first real `specs/` packet on the next cross-functional feature.
