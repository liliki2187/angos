---
name: balance-check
description: "Analyzes game balance data files, formulas, and configuration to identify outliers, broken progressions, degenerate strategies, and economy imbalances. Use after modifying any balance-related data or design."
---

## Codex Notes

- Treat references like /balance-check or /other-skill as Codex skill names. For example, use $balance-check for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked:

1. **Identify the balance domain** from the argument.

2. **Read relevant data files** from `assets/data/` and `design/balance/`.

3. **Read the design document** for the system being checked from `design/gdd/`.

4. **Perform analysis**:

   For **combat balance**:
   - Calculate DPS for all weapons/abilities at each power tier
   - Check time-to-kill at each tier
   - Identify any options that dominate all others (strictly better)
   - Check if defensive options can create unkillable states
   - Verify damage type/resistance interactions are balanced

   For **economy balance**:
   - Map all resource faucets and sinks with flow rates
   - Project resource accumulation over time
   - Check for infinite resource loops
   - Verify gold sinks scale with gold generation
   - Check if any items are never worth purchasing

   For **progression balance**:
   - Plot the XP curve and power curve
   - Check for dead zones (no meaningful progression for too long)
   - Check for power spikes (sudden jumps in capability)
   - Verify content gates align with expected player power
   - Check if skip/grind strategies break intended pacing

   For **loot balance**:
   - Calculate expected time to acquire each rarity tier
   - Check pity timer math
   - Verify no loot is strictly useless at any stage
   - Check inventory pressure vs acquisition rate

5. **Output the analysis**:

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [HEALTHY / CONCERNS / CRITICAL ISSUES]

### Outliers Detected
| Item/Value | Expected Range | Actual | Issue |
|-----------|---------------|--------|-------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```
