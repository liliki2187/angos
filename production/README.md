# Production Workspace

This directory is the execution layer for Angus.

Use it to answer four questions quickly:

1. What stage is the project in?
2. What is the current sprint actually trying to finish?
3. What is blocked or risky right now?
4. What should the next session pick up?

Directory guide:

- `stage.txt`: current project stage in one line
- `milestones/`: milestone definitions and exit criteria
- `sprints/`: short-term execution packets
- `backlog/`: prioritized pending work
- `risk-register/`: active delivery and quality risks
- `handoff/`: session or milestone handoff notes
- `roles/`: directory ownership and collaboration boundaries
- `session-state/`: the currently active session summary

Authority rules:

- Runtime truth lives in `scenes/` and related Godot assets.
- Design truth lives in `design/gdd/`.
- Architecture truth lives in `docs/architecture/`.
- This directory tracks execution state, not deep design prose.
