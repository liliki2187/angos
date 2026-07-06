# Angus Workflow Harness

This folder contains lightweight workflow guards for Angus AI collaboration.

Use these files when a task is more than a tiny typo or obvious bug fix:

- [`angus-workflow-harness.md`](./angus-workflow-harness.md): the main process, from light routing to hard gates.
- [`workflow-gates.yml`](./workflow-gates.yml): machine-readable stage, risk, and artifact rules for future scripts.
- [`godot-agent-smoke.md`](./godot-agent-smoke.md): the plain-language Godot health check for Codex changes, combining `gda script validate` with a real headless weekly-run smoke.
- [`godot-debug-skill-v0.md`](./godot-debug-skill-v0.md): the Angus Godot error notebook for Codex, with plain-language error cards, repair rules, and verification commands.
- `scripts/run_godot_gui_startup_check.ps1`: the separate Windows GUI / exact executable startup check for native Godot crashes.
- [`ai-radar-memory.md`](./ai-radar-memory.md): context sidecar for Angus-focused AI daily / next reports.
- [`ai-radar-loop-cases.md`](./ai-radar-loop-cases.md): loop cases and report-state objects for AI intelligence reports.
- [`templates/router-card.md`](./templates/router-card.md): quick task entry card.
- [`templates/delivery-manifest.md`](./templates/delivery-manifest.md): delivery and artifact classification note.
- [`templates/loop-log.md`](./templates/loop-log.md): post-feedback loop and sedimentation note.
- [`templates/workflow-lab-checklist.md`](./templates/workflow-lab-checklist.md): small experiments before hard automation.

The intent is not to call every agent for every task. The harness should first remind, then record, then block only high-risk mistakes.

Use the three-line `Decision Strip` only for workflow gates, loop logs, pass/fail judgments, blockers, or user decisions: conclusion, impact, and next step. Ordinary explanations, discussions, completion reports, and light Q&A should stay in natural prose.
