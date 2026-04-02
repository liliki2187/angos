# Event Check Resolution

> **Status**: Draft
> **Author**: Codex + repository synthesis
> **Last Updated**: 2026-03-31
> **Implements Pillar**: Truth and Sensation Must Stay in Tension

## Overview

This system resolves dispatch risk. It converts staff attributes, node difficulty, and opponent pressure into result tiers through a split binomial check model. In Angus, it is the bridge between planning and consequence.

## Player Fantasy

The player should feel that preparation matters, risk is legible, and dangerous opportunities remain tempting because the system exposes odds without making outcomes trivial.

## Detailed Design

### Core Rules

1. Event checks use binomial success rolls rather than deterministic threshold comparison.
2. Difficulty maps to a base single-die success probability.
3. Split checks separate the expedition into two pools:
   - Investigation pool: exploration + insight + occult
   - Field pool: survival + reason
4. Opponent value reduces effective dice through random negation that preserves the underlying probability model.
5. Result tiers are:
   - major success: both pools clear their thresholds
   - minor success: exactly one pool clears its threshold
   - fail: neither pool clears
6. Result tier maps into clue quality and side effects rather than ending the game.

### States and Transitions

| State | Entry Condition | Exit Condition | Behavior |
|-------|----------------|----------------|----------|
| `preview` | Valid node and staff selection | Execute pressed | Show theoretical success distribution |
| `roll_generation` | Execute pressed | Dice and negation generated | Produce roll arrays and negated indices |
| `resolution` | Rolls generated | Result applied | Count surviving hits and assign tier |
| `post_result` | Result applied | Player returns to exploration | Emit clue and state changes |

### Interactions with Other Systems

- **Exploration and Node Dispatch** supplies staff totals, node difficulty, thresholds, and opponent value.
- **Clue Inventory and Story Conversion** consumes the result tier and clue metadata.
- **Feedback UI** reads roll arrays, negated indices, and probability summaries for presentation.
- **Macro Attributes and Unlock Pressure** may receive downstream deltas from failure or occult-heavy success.

## Formulas

### Difficulty to Single-Die Probability

```
p =
  0.60 if difficulty == "easy"
  0.50 if difficulty == "normal"
  0.3333333333 if difficulty == "hard"
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `difficulty` | enum | easy/normal/hard | node data | Difficulty label |
| `p` | float | 0.0-1.0 | lookup | Single-die success chance |

### Opponent Split Allocation

```
enemy_a = floor(enemy_attr * attr_a / max(1, attr_a + attr_b))
enemy_b = enemy_attr - enemy_a
n_a_eff = max(0, attr_a - enemy_a)
n_b_eff = max(0, attr_b - enemy_b)
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `enemy_attr` | int | 0+ | node data | Opponent pressure |
| `attr_a` | int | 0+ | aggregated staff | Investigation pool size |
| `attr_b` | int | 0+ | aggregated staff | Field pool size |
| `n_a_eff`, `n_b_eff` | int | 0+ | calculated | Effective dice after negation |

### Split Outcome Distribution

```
P_A = P(X_A >= k_A), where X_A ~ Binomial(n_a_eff, p)
P_B = P(X_B >= k_B), where X_B ~ Binomial(n_b_eff, p)
P_major = P_A * P_B
P_minor = P_A * (1 - P_B) + (1 - P_A) * P_B
P_fail = (1 - P_A) * (1 - P_B)
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `k_A`, `k_B` | int | 0+ | node data | Thresholds for each pool |
| `P_major` | float | 0.0-1.0 | calculated | Probability of major success |
| `P_minor` | float | 0.0-1.0 | calculated | Probability of minor success |
| `P_fail` | float | 0.0-1.0 | calculated | Probability of failure |

## Edge Cases

| Scenario | Expected Behavior | Rationale |
|----------|------------------|-----------|
| Effective dice count becomes 0 while threshold is above 0 | That pool fails automatically | Maintains probability integrity |
| Threshold is 0 | That pool succeeds automatically | Keeps formulas well-defined |
| Opponent pressure exceeds one pool heavily | Split allocation still conserves total negation | Preserves model consistency |
| UI uses numeric mode instead of dice mode | Same underlying random logic, different presentation only | Prevents desync between modes |

## Dependencies

| System | Direction | Nature of Dependency |
|--------|-----------|---------------------|
| Exploration and Node Dispatch | This system depends on it | Consumes input data for checks |
| Clue Inventory and Story Conversion | It depends on this system | Uses result tier to set clue quality |
| Feedback, Logging, and Forecast UI | It depends on this system | Displays probability and roll outcomes |
| Macro Attributes and Unlock Pressure | Soft dependency | Some results may mutate long-term state |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| `p_easy` | 0.60 | 0.55-0.70 | Easier expedition success | Less reliability |
| `p_normal` | 0.50 | 0.45-0.55 | More consistent mid-tier play | Sharper uncertainty |
| `p_hard` | 0.3333 | 0.25-0.40 | Hard nodes become less punishing | More punishing risk gating |
| Node thresholds `k_A`, `k_B` | per node | low-mid | Raises failure rate | Softens dispatch planning |
| Opponent value `enemy_attr` | per node | 0-5+ | More negation pressure | Cleaner success curve |

## Visual/Audio Requirements

| Event | Visual Feedback | Audio Feedback | Priority |
|-------|----------------|---------------|----------|
| Probability preview | Clear major/minor/fail percentages | None required | High |
| Dice resolution | Distinct roll reveal and negation pass | Dice or resolve cues | Medium |
| Result tier reveal | Large readable tier and consequence text | Strong confirm / fail cue | High |

## UI Requirements

| Information | Display Location | Update Frequency | Condition |
|-------------|-----------------|-----------------|-----------|
| Pool requirements | Mission panel | On node change | During dispatch planning |
| Team totals | Mission panel | On staff change | During dispatch planning |
| Major/minor/fail distribution | Mission panel | On every valid preview | Before execution |
| Roll detail and negation | Result area / log | On execution | Dice mode only |

## Acceptance Criteria

- [ ] Difficulty mapping remains identical between numeric preview and resolved check.
- [ ] Opponent negation preserves total-dice semantics instead of selectively deleting successes.
- [ ] Split major/minor/fail tiers match documented thresholds.
- [ ] Result output includes enough data for UI replay or logging.
- [ ] Clue quality mapping can be driven from result tier without extra hidden rules.

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| Should delta-p modifiers stay global or become per-node data only? | Design | Vertical Slice | Open |
| When should large-failure outcomes become a distinct tier in the Godot runtime? | Design | Later | Open |
