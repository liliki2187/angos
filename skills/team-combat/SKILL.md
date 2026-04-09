---
name: team-combat
description: "Orchestrate the combat team: coordinates game-designer, gameplay-programmer, ai-programmer, technical-artist, sound-designer, and qa-tester to design, implement, and validate a combat feature end-to-end."
---

## Codex Notes

- Treat references like /team-combat or /other-skill as Codex skill names. For example, use $team-combat for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked, orchestrate the combat team through a structured pipeline.

**Decision Points:** At each phase transition, use `a concise direct user question` to present
the user with the draft proposals as selectable options. Write the
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **game-designer** -- Design the mechanic, define formulas and edge cases
- **gameplay-programmer** -- Implement the core gameplay code
- **ai-programmer** -- Implement NPC/enemy AI behavior for the feature
- **technical-artist** -- Create VFX, shader effects, and visual feedback
- **sound-designer** -- Define audio events, impact sounds, and ambient combat audio
- **qa-tester** -- Write test cases and validate the implementation

## How to Delegate

If the user explicitly wants delegation, map each team member below to a suitable generic Codex subagent:
- `role: game-designer` -- Design the mechanic, define formulas and edge cases
- `role: gameplay-programmer` -- Implement the core gameplay code
- `role: ai-programmer` -- Implement NPC/enemy AI behavior
- `role: technical-artist` -- Create VFX, shader effects, visual feedback
- `role: sound-designer` -- Define audio events, impact sounds, ambient audio
- `role: qa-tester` -- Write test cases and validate implementation

Always provide full context in each subagent prompt (design doc path, relevant code files, constraints). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Design
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **game-designer** pass:
- Create or update the design document in `design/gdd/` covering: mechanic overview, player fantasy, detailed rules, formulas with variable definitions, edge cases, dependencies, tuning knobs with safe ranges, and acceptance criteria
- Output: completed design document

### Phase 2: Architecture
Delegate to **gameplay-programmer** (with **ai-programmer** if AI is involved):
- Review the design document
- Design the code architecture: class structure, interfaces, data flow
- Identify integration points with existing systems
- Output: architecture sketch with file list and interface definitions

### Phase 3: Implementation (parallel where possible)
Delegate in parallel:
- **gameplay-programmer**: Implement core combat mechanic code
- **ai-programmer**: Implement AI behaviors (if the feature involves NPC reactions)
- **technical-artist**: Create VFX and shader effects
- **sound-designer**: Define audio event list and mixing notes

### Phase 4: Integration
- Wire together gameplay code, AI, VFX, and audio
- Ensure all tuning knobs are exposed and data-driven
- Verify the feature works with existing combat systems

### Phase 5: Validation
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **qa-tester** pass:
- Write test cases from the acceptance criteria
- Test all edge cases documented in the design
- Verify performance impact is within budget
- File bug reports for any issues found

### Phase 6: Sign-off
- Collect results from all team members
- Report feature status: COMPLETE / NEEDS WORK / BLOCKED
- List any outstanding issues and their assigned owners

## Output
A summary report covering: design completion status, implementation status per team member, test results, and any open issues.
