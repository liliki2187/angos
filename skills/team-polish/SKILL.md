---
name: team-polish
description: "Orchestrate the polish team: coordinates performance-analyst, technical-artist, sound-designer, and qa-tester to optimize, polish, and harden a feature or area for release quality."
---

## Codex Notes

- Treat references like /team-polish or /other-skill as Codex skill names. For example, use $team-polish for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked, orchestrate the polish team through a structured pipeline.

**Decision Points:** At each phase transition, use `a concise direct user question` to present
the user with the draft proposals as selectable options. Write the
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **performance-analyst** -- Profiling, optimization, memory analysis, frame budget
- **technical-artist** -- VFX polish, shader optimization, visual quality
- **sound-designer** -- Audio polish, mixing, ambient layers, feedback sounds
- **qa-tester** -- Edge case testing, regression testing, soak testing

## How to Delegate

If the user explicitly wants delegation, map each team member below to a suitable generic Codex subagent:
- `role: performance-analyst` -- Profiling, optimization, memory analysis
- `role: technical-artist` -- VFX polish, shader optimization, visual quality
- `role: sound-designer` -- Audio polish, mixing, ambient layers
- `role: qa-tester` -- Edge case testing, regression testing, soak testing

Always provide full context in each subagent prompt (target feature/area, performance budgets, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phases 3 and 4 can run simultaneously).

## Pipeline

### Phase 1: Assessment
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **performance-analyst** pass:
- Profile the target feature/area using `$perf-profile`
- Identify performance bottlenecks and frame budget violations
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Output: performance report with prioritized optimization list

### Phase 2: Optimization
Delegate to **performance-analyst** (with relevant programmers as needed):
- Fix performance hotspots identified in Phase 1
- Optimize draw calls, reduce overdraw
- Fix memory leaks and reduce allocation pressure
- Verify optimizations don't change gameplay behavior
- Output: optimized code with before/after metrics

### Phase 3: Visual Polish (parallel with Phase 2)
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **technical-artist** pass:
- Review VFX for quality and consistency with art bible
- Optimize particle systems and shader effects
- Add screen shake, camera effects, and visual juice where appropriate
- Ensure effects degrade gracefully on lower settings
- Output: polished visual effects

### Phase 4: Audio Polish (parallel with Phase 2)
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **sound-designer** pass:
- Review audio events for completeness (are any actions missing sound feedback?)
- Check audio mix levels -- nothing too loud or too quiet relative to the mix
- Add ambient audio layers for atmosphere
- Verify audio plays correctly with spatial positioning
- Output: audio polish list and mixing notes

### Phase 5: Hardening
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **qa-tester** pass:
- Test all edge cases: boundary conditions, rapid inputs, unusual sequences
- Soak test: run the feature for extended periods checking for degradation
- Stress test: maximum entities, worst-case scenarios
- Regression test: verify polish changes haven't broken existing functionality
- Test on minimum spec hardware (if available)
- Output: test results with any remaining issues

### Phase 6: Sign-off
- Collect results from all team members
- Compare performance metrics against budgets
- Report: READY FOR RELEASE / NEEDS MORE WORK
- List any remaining issues with severity and recommendations

## Output
A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, and release readiness assessment.
