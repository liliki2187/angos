# Weekly Run Loop and State

> **Status**: Draft
> **Author**: Codex + repository synthesis
> **Last Updated**: 2026-03-31
> **Implements Pillar**: One Week Must Read as One Arc

## Overview

This system owns the weekly structure of Angus. It defines what state persists across weeks, what resets inside a week, how the player moves from briefing to exploration to publication, and how settlement feeds the next week. Without it, the project collapses back into disconnected prototypes.

## Player Fantasy

The player should feel like an editor managing a living publication over time, not a user hopping between unrelated screens. Every week should feel like one complete editorial cycle with continuity.

## Detailed Design

### Core Rules

1. Each week begins with a briefing, current macro state, and a refreshed set of available content opportunities.
2. The player starts each week with a fixed day budget of 7.
3. Exploration actions consume days and produce either usable clues, partial outcomes, or negative pressure.
4. The player transitions from exploration to editorial either by choice or because the week can no longer support useful dispatch.
5. Editorial settlement writes back to long-term state before the next week begins.
6. Week-local containers are cleared at the start of a new week; long-term state remains.

### States and Transitions

| State | Entry Condition | Exit Condition | Behavior |
|-------|----------------|----------------|----------|
| `briefing` | New run or post-settlement transition | Player enters exploration | Refresh week-facing text and available pressure |
| `explore` | Week begins | Player ends week or day budget exhausted | Node selection, staff assignment, expedition resolution |
| `editorial` | Exploration ends | Player settles the issue | Story pool generation, layout interaction, forecast updates |
| `summary` | Settlement completes | Player advances week | Present outcome summary and long-term deltas |

### Interactions with Other Systems

- **Exploration and Node Dispatch** reads week state, day budget, unlock flags, and writes clue results.
- **Editorial Layout and Settlement** reads weekly clues, story pool, subscriptions, and editorial profile, then writes profit and next-week values.
- **Macro Attributes and Unlock Pressure** reads and mutates long-term variables such as credibility, weirdness, reputation, order, and mania.
- **Menus and Scene Navigation** can create a new run or return to menu, but should not own weekly gameplay state.

## Formulas

### Week Day Budget

```
remaining_days_next = remaining_days_current - node_days_cost
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `remaining_days_current` | int | 0-7 | runtime state | Days left before dispatch |
| `node_days_cost` | int | 1-3+ | node data | Time consumed by an expedition |
| `remaining_days_next` | int | 0-7 | calculated | Days left after dispatch |

**Expected output range**: 0 to 7
**Edge case**: If `node_days_cost > remaining_days_current`, dispatch is invalid.

### Weekly Reset Contract

```
new_week.week = old_week.week + 1
new_week.day = 7
new_week.weekly_clues = []
new_week.story_pool = []
new_week.slot_assignment = {}
new_week.last_roll = {}
new_week.current_phase = "explore"
```

This is a rule contract rather than a balance formula. It exists to keep long-term and short-term state separate.

## Edge Cases

| Scenario | Expected Behavior | Rationale |
|----------|------------------|-----------|
| Day budget reaches 0 after expedition | Force transition to editorial | Prevent dead-end weekly state |
| Player ends exploration early | Allow transition with fewer clues | A weak week should still be publishable |
| Settlement occurs with underfilled issue | Allowed, but economically punished | Preserves readability and teaches consequences |
| New week starts after a losing issue | Continue play with updated long-term values | Supports recovery-oriented loop |

## Dependencies

| System | Direction | Nature of Dependency |
|--------|-----------|---------------------|
| Exploration and Node Dispatch | This system supports it | Supplies day budget, unlock state, and week-local containers |
| Editorial Layout and Settlement | This system supports it | Supplies weekly input and receives next-week outputs |
| Macro Attributes and Unlock Pressure | Bidirectional | Shared long-term state and unlock logic |
| Menus and Scene Navigation | Navigation depends on this | Creates or resumes the runtime path |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| `week_days` | 7 | 5-9 | More dispatch freedom, less pressure | Tighter weeks, harder tradeoffs |
| `starting_subscribers` | 1200 | 600-2000 | Smoother early economy | More punishing early game |
| `starting_macro_stats` | per prototype values | 30-55 | Easier early unlock pressure control | Harsher starting conditions |

## Visual/Audio Requirements

| Event | Visual Feedback | Audio Feedback | Priority |
|-------|----------------|---------------|----------|
| Week start | Clear briefing panel and week label refresh | Light transition cue | Medium |
| Phase transition | Screen state swap and summary emphasis | Distinct transition sting | High |
| Next week advance | Reset labels and refreshed opportunity list | Resolve-and-return cue | Medium |

## UI Requirements

| Information | Display Location | Update Frequency | Condition |
|-------------|-----------------|-----------------|-----------|
| Current week | Header / week bar | On phase refresh | Always |
| Remaining days | Header / week bar | After every expedition | During exploration |
| Subscribers and editorial profile | Header / week bar | On refresh and settlement | Always |
| Current phase context | Main content panel | On transition | Always |

## Acceptance Criteria

- [ ] A full week can be played from briefing to next-week transition without leaving the Godot loop.
- [ ] Week-local state clears correctly while long-term state persists.
- [ ] Exploration cannot consume invalid days.
- [ ] Settlement always produces a next-week state.
- [ ] Phase transitions are explicit and readable.

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| Should future weeks support interrupts between briefing and exploration? | Design | Later | Open |
| When should save/load hook into the weekly state machine? | Tech | Vertical Slice | Open |
