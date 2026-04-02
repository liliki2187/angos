# Editorial Layout and Settlement

> **Status**: Draft
> **Author**: Codex + repository synthesis
> **Last Updated**: 2026-03-31
> **Implements Pillar**: Editorial Tradeoffs Must Stay Visible

## Overview

This system turns a week's investigatory output into a playable publication step. It generates a story pool, lets the player place stories into six issue slots, previews the consequences of composition choices, and settles the issue into profit, subscriptions, editorial profile, and macro-state change.

## Player Fantasy

The player should feel like an editor making a real front-page call: choosing what leads, what supports, what gets cut, and what kind of paper they are becoming.

## Detailed Design

### Core Rules

1. Weekly clues are converted into stories before the editorial phase begins.
2. The story pool is padded with filler stories so the player can always complete a valid issue.
3. The issue contains exactly six slots in the MVP, each with a different exposure weight.
4. Each slot can contain at most one story; placing a story in a new slot removes it from any previous slot.
5. Real-time stats update as the issue changes, exposing value, diversity, combo, penalty, balance, and bias signals.
6. Settlement transforms the current issue into demand, sales, revenue, cost, profit, next-week subscribers, editorial profile drift, and macro-stat deltas.

### States and Transitions

| State | Entry Condition | Exit Condition | Behavior |
|-------|----------------|----------------|----------|
| `story_pool_ready` | Editorial phase begins | Story selected | Weekly clues converted and filler generated |
| `layout_edit` | Story pool available | Settlement triggered | Player assigns stories to slots and sees live stats |
| `settled` | Settle action confirmed | Next week begins | Final stats applied and summary presented |

### Interactions with Other Systems

- **Clue Inventory and Story Conversion** supplies the initial exploration stories and their metadata.
- **Weekly Run Loop and State** supplies subscribers, editorial profile, and receives next-week values.
- **Macro Attributes and Unlock Pressure** reads the settled issue and mutates long-term paper identity.
- **Feedback and Forecast UI** reads live calculations before the player commits settlement.

## Formulas

### Weighted Story Value

```
total_base_value = sum(story.base_value * slot.weight for each filled slot)
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `story.base_value` | int | 100-500+ | story data | Baseline story worth |
| `slot.weight` | float | 0.2-1.0 | slot data | Exposure multiplier per slot |
| `total_base_value` | float | 0+ | calculated | Weighted issue value |

### Demand and Sales

```
demand =
  round((3200 + subscribers * 0.45 + total_base_value * 1.45)
  * m_quality * m_combo * m_diversity
  * m_layout * m_empty * m_penalty
  * m_link * m_balance * m_bias)

sold = clamp(demand, 0, print_capacity)
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `subscribers` | int | 0+ | long-term state | Existing subscriber base |
| `m_*` | float | ~0.35-1.55 | calculated | Composition multipliers |
| `print_capacity` | int | 1000+ | config/runtime | Hard cap on sales |
| `sold` | int | 0-print_capacity | calculated | Actual copies sold |

### Next-Week Subscribers

```
next_subscribers =
  max(600,
    round(
      subscribers
      + profit / 130
      + (m_balance - 1.0) * 180
      + (m_quality - 1.0) * 220
      - empty_slots * 45))
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `profit` | float | negative to positive | settlement result | Net issue profit |
| `m_balance`, `m_quality` | float | near 1.0 | calculated | Composition quality signals |
| `empty_slots` | int | 0-6 | layout state | Number of blank slots |

## Edge Cases

| Scenario | Expected Behavior | Rationale |
|----------|------------------|-----------|
| Player settles with empty slots | Allowed, with clear multiplier penalties | Preserve readable consequences |
| Story pool contains too few exploration stories | Filler stories pad the pool | Keep the weekly loop playable |
| Player reassigns a story to a new slot | Old slot is cleared automatically | Avoid duplicate placement |
| Highly imbalanced tag mix | Bias and balance multipliers can reward or punish, but must stay legible | Keeps editorial identity meaningful |

## Dependencies

| System | Direction | Nature of Dependency |
|--------|-----------|---------------------|
| Clue Inventory and Story Conversion | This system depends on it | Needs weekly stories to operate |
| Weekly Run Loop and State | Bidirectional | Reads long-term state and writes next-week state |
| Macro Attributes and Unlock Pressure | Soft dependency | Settlement can mutate macro stats and unlock direction |
| Feedback, Logging, and Forecast UI | It depends on this system | Presents live calculation feedback |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| Slot weights | 0.2-1.0 | per slot | Makes slot hierarchy sharper | Flattens layout choices |
| `m_combo` growth | +0.04 per combo | 0.02-0.06 | Stronger repeat-tag reward | Weaker synergy reward |
| `m_diversity` growth | +0.035 per unique tag | 0.02-0.05 | Stronger variety reward | Less incentive to diversify |
| Empty slot penalty | -0.12 each | 0.08-0.15 | Harsher underfilled issues | Softer punishment |
| Subscriber floor | 600 | 300-800 | More forgiving collapse state | More punishing downturn |

## Visual/Audio Requirements

| Event | Visual Feedback | Audio Feedback | Priority |
|-------|----------------|---------------|----------|
| Story selection | Clear selected state and disabled placed stories | Light UI confirm | Medium |
| Slot placement | Readable slot occupancy update | Placement cue | High |
| Live-stat change | Immediate stat refresh and emphasis on major swings | Soft tick or hover cue | High |
| Settlement | Summary panel, profit/sales highlight, next-week transition | Strong issue-published cue | High |

## UI Requirements

| Information | Display Location | Update Frequency | Condition |
|-------------|-----------------|-----------------|-----------|
| Story tags, quality, base value | Story list | Always | Editorial phase |
| Slot exposure and occupancy | Slot list | On every placement | Editorial phase |
| Live multipliers and forecast | Stats panel | On every placement or clear | Editorial phase |
| Summary outcome | Summary panel | On settlement | Post-settlement |

## Acceptance Criteria

- [ ] Weekly clues convert into stories without manual authoring work.
- [ ] The player can fill, replace, and clear all six slots.
- [ ] Live forecast updates correctly as layout changes.
- [ ] Settlement returns profit, demand, and next-subscriber values in one pass.
- [ ] Next-week state reflects settlement results immediately.

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| Should filler stories stay purely functional, or eventually inherit week mood and macro-state? | Design | Vertical Slice | Open |
| At what point should editorial profile influence unlock content, not just multipliers? | Design | Alpha | Open |
