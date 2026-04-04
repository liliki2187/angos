---
name: localize
description: "Run the localization workflow: extract strings, validate localization readiness, check for hardcoded text, and generate translation-ready string tables."
---

## Codex Notes

- Treat references like /localize or /other-skill as Codex skill names. For example, use $localize for this workflow.
- Treat AGENTS.md as the project coordination doc and combine it with relevant repo docs under docs/.
- Ask concise follow-up questions directly in chat instead of relying on Claude-only question tools.
- Treat specialized role names from the source repo as conceptual guidance. Work locally by default, and only use generic Codex subagents if the user explicitly asks for delegation.
- Shared imported templates live under ../_game-studio-shared/templates/.
- Use docs/technical-preferences.md as the project-level technical preferences file. Seed it from ../_game-studio-shared/templates/technical-preferences.md if needed.

When this skill is invoked:

1. **Parse the subcommand** from the argument:
   - `scan` -- Scan for localization issues (hardcoded strings, missing keys)
   - `extract` -- Extract new strings and generate/update string tables
   - `validate` -- Validate existing translations for completeness and format
   - `status` -- Report overall localization status

2. **For `scan`**:
   - Search `gd_project/` for hardcoded user-facing strings:
     - String literals in UI code that are not wrapped in a localization function
     - Concatenated strings that should be parameterized
     - Strings with positional placeholders (`%s`, `%d`) instead of named ones (`{playerName}`)
   - Search for localization anti-patterns:
     - Date/time formatting not using locale-aware functions
     - Number formatting without locale awareness
     - Text embedded in images or textures (flag asset files)
     - Strings that assume left-to-right text direction
   - Report all findings with file paths and line numbers

3. **For `extract`**:
   - Scan all source files for localized string references
   - Compare against the existing string table (if any) in `gd_project/Assets/data/`
   - Generate new entries for strings that don't have keys yet
   - Suggest key names following the convention: `[category].[subcategory].[description]`
   - Output a diff of new strings to add to the string table

4. **For `validate`**:
   - Read all string table files in `assets/data/`
   - Check each entry for:
     - Missing translations (key exists but no translation for a locale)
     - Placeholder mismatches (source has `{name}` but translation is missing it)
     - String length violations (exceeds character limits for UI elements)
     - Orphaned keys (translation exists but nothing references the key in code)
   - Report validation results grouped by locale and severity

5. **For `status`**:
   - Count total localizable strings
   - Per locale: count translated, untranslated, and stale (source changed since translation)
   - Generate a coverage matrix:

   ```markdown
   ## Localization Status
   Generated: [Date]

   | Locale | Total | Translated | Missing | Stale | Coverage |
   |--------|-------|-----------|---------|-------|----------|
   | en (source) | [N] | [N] | 0 | 0 | 100% |
   | [locale] | [N] | [N] | [N] | [N] | [X]% |

   ### Issues
   - [N] hardcoded strings found in source code
   - [N] strings exceeding character limits
   - [N] placeholder mismatches
   - [N] orphaned keys (can be cleaned up)
   ```

### Rules
- English (en) is always the source locale
- Every string table entry must include a translator comment explaining context
- Never modify translation files directly -- generate diffs for review
- Character limits must be defined per-UI-element and enforced automatically
- Right-to-left (RTL) language support should be considered from the start, not bolted on later
