---
name: team-narrative
description: "Orchestrate the narrative team: coordinates narrative-director, writer, world-builder, and level-designer to create cohesive story content, world lore, and narrative-driven level design."
---

## Codex Notes

- Treat references like /team-narrative or /other-skill as Codex skill names. For example, use $team-narrative for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked, orchestrate the narrative team through a structured pipeline.

**Decision Points:** At each phase transition, use `a concise direct user question` to present
the user with the draft proposals as selectable options. Write the
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **narrative-director** -- Story arcs, character design, dialogue strategy, narrative vision
- **writer** -- Dialogue writing, lore entries, item descriptions, in-game text
- **world-builder** -- World rules, faction design, history, geography, environmental storytelling
- **level-designer** -- Level layouts that serve the narrative, pacing, environmental storytelling beats

## How to Delegate

If the user explicitly wants delegation, map each team member below to a suitable generic Codex subagent:
- `role: narrative-director` -- Story arcs, character design, narrative vision
- `role: writer` -- Dialogue writing, lore entries, in-game text
- `role: world-builder` -- World rules, faction design, history, geography
- `role: level-designer` -- Level layouts that serve the narrative, pacing

Always provide full context in each subagent prompt (narrative brief, lore dependencies, character profiles). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 2 agents can run simultaneously).

## Pipeline

### Phase 1: Narrative Direction
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **narrative-director** pass:
- Define the narrative purpose of this content: what story beat does it serve?
- Identify characters involved, their motivations, and how this fits the overall arc
- Set the emotional tone and pacing targets
- Specify any lore dependencies or new lore this introduces
- Output: narrative brief with story requirements

### Phase 2: World Foundation (parallel)
Delegate in parallel:
- **world-builder**: Create or update lore entries for factions, locations, and history relevant to this content. Cross-reference against existing lore for contradictions. Set canon level for new entries.
- **writer**: Draft character dialogue using voice profiles. Ensure all lines are under 120 characters, use named placeholders for variables, and are localization-ready.

### Phase 3: Level Narrative Integration
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **level-designer** pass:
- Review the narrative brief and lore foundation
- Design environmental storytelling elements in the level
- Place narrative triggers, dialogue zones, and discovery points
- Ensure pacing serves both gameplay and story

### Phase 4: Review and Consistency
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **narrative-director** pass:
- Review all dialogue against character voice profiles
- Verify lore consistency across new and existing entries
- Confirm narrative pacing aligns with level design
- Check that all mysteries have documented "true answers"

### Phase 5: Polish
- Writer reviews all text for localization readiness
- Verify no line exceeds dialogue box constraints
- Confirm all text uses string keys (localization pipeline ready)
- World-builder finalizes canon levels for all new lore

## Output
A summary report covering: narrative brief status, lore entries created/updated, dialogue lines written, level narrative integration points, consistency review results, and any unresolved contradictions.
