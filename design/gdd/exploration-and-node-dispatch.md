# Exploration and Node Dispatch

> **Status**: Draft
> **Author**: Codex + repository synthesis
> **Last Updated**: 2026-03-31
> **Implements Pillar**: Investigation Must Feed Publication

## Overview

This system covers the exploration half of the weekly loop: region availability, node selection, staff assignment, dispatch validation, and clue output preparation. Its job is to turn limited time and staff capability into publishable material.

## Player Fantasy

The player should feel like they are directing a fragile but capable investigative team into uncertain opportunities, reading risk, scarcity, and potential reward before committing the paper's limited week.

## Detailed Design

### Core Rules

1. The world is organized into regions, each containing permanent, temporary, or hidden nodes.
2. Regions unlock through explicit rules tied to macro attributes, flags, or prior evidence.
3. Each dispatch selects 1-3 staff members whose attributes are aggregated against node requirements.
4. A node is valid only if the player has enough remaining days and satisfies required attribute thresholds.
5. Successful or partial outcomes generate clues; failed outcomes may generate weak clues or pressure effects.
6. Exploration ends when the player chooses to stop or the week budget can no longer support useful action.

### States and Transitions

| State | Entry Condition | Exit Condition | Behavior |
|-------|----------------|----------------|----------|
| `region_browse` | Enter exploration phase | Region selected | Browse region list and unlock hints |
| `node_select` | Region selected | Staff and node prepared | Inspect nodes, filters, and availability |
| `dispatch_ready` | Valid node and staff combination exists | Execute pressed | Show probabilities and mission summary |
| `dispatch_resolved` | Event check returns a result | Player selects next action | Apply clue and state changes |

### Interactions with Other Systems

- **Weekly Run Loop and State** supplies remaining days, current week, flags, and macro attributes.
- **Event Check Resolution** consumes aggregated staff values, node difficulty, and opponent values, then returns a result tier.
- **Macro Attributes and Unlock Pressure** affects hidden nodes and region unlock rules.
- **Clue Inventory and Story Conversion** consumes the resulting clue objects.

## Formulas

### Staff Attribute Aggregation

```
team_total[attr] = sum(staff_i[attr] for each selected staff member)
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `staff_i[attr]` | int | 0-10+ | staff data | Attribute value for one staff member |
| `team_total[attr]` | int | 0-30+ | calculated | Aggregated team value for a requirement |

**Expected output range**: 0 to 30+
**Edge case**: Empty staff selection is invalid for dispatch.

### Node Availability Gate

```
dispatch_enabled =
  (remaining_days >= node.days)
  and staff_count in [1, 3]
  and all(team_total[attr] >= node.need[attr] for attr in node.need)
  and node_visibility == true
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `remaining_days` | int | 0-7 | week state | Available time budget |
| `staff_count` | int | 0-3 | selection state | Number of assigned staff |
| `node.need[attr]` | int | 0-10+ | node data | Requirement per attribute |
| `node_visibility` | bool | true/false | unlock logic | Whether player can see the node |

## Edge Cases

| Scenario | Expected Behavior | Rationale |
|----------|------------------|-----------|
| No staff selected | Node cannot execute | Prevent invalid dispatch state |
| Temporary node already resolved | Disable it for the current week | Preserve temporal pressure |
| Hidden node unlock condition met mid-run | Reveal it without rebuilding the loop | Makes macro pressure feel alive |
| Requirements missed by one point | Node stays unavailable, but UI explains why | Preserves legibility |

## Dependencies

| System | Direction | Nature of Dependency |
|--------|-----------|---------------------|
| Weekly Run Loop and State | This system depends on it | Reads phase, days, flags, and week state |
| Event Check Resolution | This system depends on it | Uses it to resolve dispatch outcome |
| Clue Inventory and Story Conversion | It depends on this system | Consumes clue output |
| Macro Attributes and Unlock Pressure | Bidirectional | Unlocks regions/nodes and may be mutated by results |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| Region count in MVP | 2 | 2-4 | More variety, more content load | Tighter onboarding |
| Staff cap per dispatch | 3 | 2-4 | More combinatorial depth | Harder requirement satisfaction |
| Node day cost | 1-3 | 1-4 | More week pressure | More dispatch volume per week |
| Node requirement thresholds | per node | low-mid | Requires stronger staff composition | Easier access, less tension |

## Visual/Audio Requirements

| Event | Visual Feedback | Audio Feedback | Priority |
|-------|----------------|---------------|----------|
| Region selection | Distinct selected state and hint panel update | Light UI confirm | Medium |
| Node availability change | Clear disabled reason text | None required | High |
| Dispatch execution | Mission panel emphasis and result reveal | Strong confirm and resolve cues | High |

## UI Requirements

| Information | Display Location | Update Frequency | Condition |
|-------------|-----------------|-----------------|-----------|
| Region hint and unlock status | Region panel | On selection or state change | During exploration |
| Node cost, risk, and reason text | Node list | On refresh | During exploration |
| Selected staff summary | Staff panel | On every selection change | During exploration |
| Probability preview | Mission panel | On staff or node change | When dispatch can be evaluated |

## Acceptance Criteria

- [ ] The player can complete a valid dispatch using 1-3 staff.
- [ ] Disabled nodes always explain why they are unavailable.
- [ ] Exploration outputs clue data that downstream systems can consume.
- [ ] Region unlock rules and hidden-node visibility respond to macro-state changes.
- [ ] A weak week with few clues remains valid and publishable.

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| Should node filters affect only UI highlighting or also spawn weight later? | Design | Vertical Slice | Open |
| How many node archetypes are enough before config extraction becomes mandatory? | Design/Tech | Vertical Slice | Open |
