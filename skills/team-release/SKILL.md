---
name: team-release
description: "Orchestrate the release team: coordinates release-manager, qa-lead, devops-engineer, and producer to execute a release from candidate to deployment."
---

## Codex Notes

- Treat references like /team-release or /other-skill as Codex skill names. For example, use $team-release for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked, orchestrate the release team through a structured pipeline.

**Decision Points:** At each phase transition, use `a concise direct user question` to present
the user with the draft proposals as selectable options. Write the
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **release-manager** -- Release branch, versioning, changelog, deployment
- **qa-lead** -- Test sign-off, regression suite, release quality gate
- **devops-engineer** -- Build pipeline, artifacts, deployment automation
- **producer** -- Go/no-go decision, stakeholder communication, scheduling

## How to Delegate

If the user explicitly wants delegation, map each team member below to a suitable generic Codex subagent:
- `role: release-manager` -- Release branch, versioning, changelog, deployment
- `role: qa-lead` -- Test sign-off, regression suite, release quality gate
- `role: devops-engineer` -- Build pipeline, artifacts, deployment automation
- `role: producer` -- Go/no-go decision, stakeholder communication

Always provide full context in each subagent prompt (version number, milestone status, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Release Planning
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **producer** pass:
- Confirm all milestone acceptance criteria are met
- Identify any scope items deferred from this release
- Set the target release date and communicate to team
- Output: release authorization with scope confirmation

### Phase 2: Release Candidate
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **release-manager** pass:
- Cut release branch from the agreed commit
- Bump version numbers in all relevant files
- Generate the release checklist using `$release-checklist`
- Freeze the branch -- no feature changes, bug fixes only
- Output: release branch name and checklist

### Phase 3: Quality Gate (parallel)
Delegate in parallel:
- **qa-lead**: Execute full regression test suite. Test all critical paths. Verify no S1/S2 bugs. Sign off on quality.
- **devops-engineer**: Build release artifacts for all target platforms. Verify builds are clean and reproducible. Run automated tests in CI.

### Phase 4: Localization and Performance
Delegate (can run in parallel with Phase 3 if resources available):
- Verify all strings are translated (delegate to localization-lead if available)
- Run performance benchmarks against targets (delegate to performance-analyst if available)
- Output: localization and performance sign-off

### Phase 5: Go/No-Go
Handle this pass locally or, if delegation is explicitly requested, delegate a bounded subtask for the **producer** pass:
- Collect sign-off from: qa-lead, release-manager, devops-engineer, technical-director
- Evaluate any open issues -- are they blocking or can they ship?
- Make the go/no-go call
- Output: release decision with rationale

### Phase 6: Deployment (if GO)
Delegate to **release-manager** + **devops-engineer**:
- Tag the release in version control
- Generate changelog using `$changelog`
- Deploy to staging for final smoke test
- Deploy to production
- Monitor for 48 hours post-release

### Phase 7: Post-Release
- **release-manager**: Generate release report (what shipped, what was deferred, metrics)
- **producer**: Update milestone tracking, communicate to stakeholders
- **qa-lead**: Monitor incoming bug reports for regressions
- Schedule post-release retrospective if issues occurred

## Output
A summary report covering: release version, scope, quality gate results, go/no-go decision, deployment status, and monitoring plan.
