---
name: bug-report
description: "Creates a structured bug report from a description, or analyzes code to identify potential bugs. Ensures every bug report has full reproduction steps, severity assessment, and context."
---

## Codex Notes

- Treat references like /bug-report or /other-skill as Codex skill names. For example, use $bug-report for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When invoked with a description:

1. **Parse the description** for key information.

2. **Search the codebase** for related files using Grep/Glob to add context.

3. **Generate the bug report**:

```markdown
# Bug Report

## Summary
**Title**: [Concise, descriptive title]
**ID**: BUG-[NNNN]
**Severity**: [S1-Critical / S2-Major / S3-Minor / S4-Trivial]
**Priority**: [P1-Immediate / P2-Next Sprint / P3-Backlog / P4-Wishlist]
**Status**: Open
**Reported**: [Date]
**Reporter**: [Name]

## Classification
- **Category**: [Gameplay / UI / Audio / Visual / Performance / Crash / Network]
- **System**: [Which game system is affected]
- **Frequency**: [Always / Often (>50%) / Sometimes (10-50%) / Rare (<10%)]
- **Regression**: [Yes/No/Unknown -- was this working before?]

## Environment
- **Build**: [Version or commit hash]
- **Platform**: [OS, hardware if relevant]
- **Scene/Level**: [Where in the game]
- **Game State**: [Relevant state -- inventory, quest progress, etc.]

## Reproduction Steps
**Preconditions**: [Required state before starting]

1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

**Expected Result**: [What should happen]
**Actual Result**: [What actually happens]

## Technical Context
- **Likely affected files**: [List of files based on codebase search]
- **Related systems**: [What other systems might be involved]
- **Possible root cause**: [If identifiable from the description]

## Evidence
- **Logs**: [Relevant log output if available]
- **Visual**: [Description of visual evidence]

## Related Issues
- [Links to related bugs or design documents]

## Notes
[Any additional context or observations]
```

When invoked with `analyze`:

1. **Read the target file(s)**.
2. **Identify potential bugs**: null references, off-by-one errors, race
   conditions, unhandled edge cases, resource leaks, incorrect state
   transitions.
3. **For each potential bug**, generate a bug report with the likely trigger
   scenario and recommended fix.
