---
name: hotfix
description: "Emergency fix workflow that bypasses normal sprint processes with a full audit trail. Creates hotfix branch, tracks approvals, and ensures the fix is backported correctly."
---

## Codex Notes

- Treat references like /hotfix or /other-skill as Codex skill names. For example, use $hotfix for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked:

> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `$hotfix`. Do not auto-invoke based on context matching.

1. **Assess the emergency** -- Read the bug description or ID. Determine severity:
   - **S1 (Critical)**: Game unplayable, data loss, security vulnerability -- hotfix immediately
   - **S2 (Major)**: Significant feature broken, workaround exists -- hotfix within 24 hours
   - If severity is S3 or lower, recommend using the normal bug fix workflow instead

2. **Create the hotfix record** at `production/hotfixes/hotfix-[date]-[short-name].md`:

   ```markdown
   ## Hotfix: [Short Description]
   Date: [Date]
   Severity: [S1/S2]
   Reporter: [Who found it]
   Status: IN PROGRESS

   ### Problem
   [Clear description of what is broken and the player impact]

   ### Root Cause
   [To be filled during investigation]

   ### Fix
   [To be filled during implementation]

   ### Testing
   [What was tested and how]

   ### Approvals
   - [ ] Fix reviewed by lead-programmer
   - [ ] Regression test passed (qa-tester)
   - [ ] Release approved (producer)

   ### Rollback Plan
   [How to revert if the fix causes new issues]
   ```

3. **Create the hotfix branch** (if git is initialized):
   ```
   git checkout -b hotfix/[short-name] [release-tag-or-main]
   ```

4. **Investigate and implement the fix** -- Focus on the minimal change that resolves the issue. Do NOT refactor, clean up, or add features alongside the hotfix.

5. **Validate the fix** -- Run targeted tests for the affected system. Check for regressions in adjacent systems.

6. **Update the hotfix record** with root cause, fix details, and test results.

6b. **Collect approvals** -- If the user explicitly wants delegation, request sign-off with bounded generic Codex subagent tasks:
   - `role: lead-programmer` -- Review the fix for correctness and side effects
   - `role: qa-tester` -- Run targeted regression tests on the affected system
   - `role: producer` -- Approve deployment timing and communication plan

7. **Output a summary** with: severity, root cause, fix applied, testing status, and what approvals are still needed before deployment.

### Rules
- Hotfixes must be the MINIMUM change to fix the issue -- no cleanup, no refactoring, no "while we're here" changes
- Every hotfix must have a rollback plan documented before deployment
- Hotfix branches merge to BOTH the release branch AND the development branch
- All hotfixes require a post-incident review within 48 hours
- If the fix is complex enough to need more than 4 hours, escalate to technical-director for a scope decision
