---
name: team-level
description: "Orchestrate level design team: level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester for complete area/level creation."
---

## Codex Notes

- Treat references like /team-level or /other-skill as Codex skill names. For example, use $team-level for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked:

**Decision Points:** At each step transition, use `a concise direct user question` to present
the user with the draft proposals as selectable options. Write the
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next step.

1. **Read the argument** for the target level or area (e.g., `tutorial`,
   `forest dungeon`, `hub town`, `final boss arena`).

2. **Gather context**:
   - Read the game concept at `design/gdd/game-concept.md`
   - Read game pillars at `design/gdd/game-pillars.md`
   - Read existing level docs in `design/levels/`
   - Read relevant narrative docs in `design/narrative/`
   - Read world-building docs for the area's region/faction

## How to Delegate

If the user explicitly wants delegation, map each team member below to a suitable generic Codex subagent:
- `role: narrative-director` -- Narrative purpose, characters, emotional arc
- `role: world-builder` -- Lore context, environmental storytelling, world rules
- `role: level-designer` -- Spatial layout, pacing, encounters, navigation
- `role: systems-designer` -- Enemy compositions, loot tables, difficulty balance
- `role: art-director` -- Visual theme, color palette, lighting, asset requirements
- `role: qa-tester` -- Test cases, boundary testing, playtest checklist

Always provide full context in each subagent prompt (game concept, pillars, existing level docs, narrative docs).

3. **Orchestrate the level design team** in sequence:

### Step 1: Narrative Context (narrative-director + world-builder)
If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `narrative-director` pass to:
- Define the narrative purpose of this area (what story beats happen here?)
- Identify key characters, dialogue triggers, and lore elements
- Specify emotional arc (how should the player feel entering, during, leaving?)

If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `world-builder` pass to:
- Provide lore context for the area (history, faction presence, ecology)
- Define environmental storytelling opportunities
- Specify any world rules that affect gameplay in this area

### Step 2: Layout and Encounter Design (level-designer)
If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `level-designer` pass to:
- Design the spatial layout (critical path, optional paths, secrets)
- Define pacing curve (tension peaks, rest areas, exploration zones)
- Place encounters with difficulty progression
- Design environmental puzzles or navigation challenges
- Define points of interest and landmarks for wayfinding
- Specify entry/exit points and connections to adjacent areas

### Step 3: Systems Integration (systems-designer)
If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `systems-designer` pass to:
- Specify enemy compositions and encounter formulas
- Define loot tables and reward placement
- Balance difficulty relative to expected player level/gear
- Design any area-specific mechanics or environmental hazards
- Specify resource distribution (health pickups, save points, shops)

### Step 4: Visual Direction (art-director)
If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `art-director` pass to:
- Define the visual theme and color palette for the area
- Specify lighting mood and time-of-day settings
- List required art assets (environment props, unique assets)
- Define visual landmarks and sight lines
- Specify any special VFX needs (weather, particles, fog)

### Step 5: QA Planning (qa-tester)
If the user explicitly wants delegation, spawn a suitable generic Codex subagent for the `qa-tester` pass to:
- Write test cases for the critical path
- Identify boundary and edge cases (sequence breaks, softlocks)
- Create a playtest checklist for the area
- Define acceptance criteria for level completion

4. **Compile the level design document** combining all team outputs into the
   level design template format.

5. **Save to** `design/levels/[level-name].md`.

6. **Output a summary** with: area overview, encounter count, estimated asset
   list, narrative beats, and any cross-team dependencies or open questions.
