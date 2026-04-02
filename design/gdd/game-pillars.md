# Game Pillars

> **Project**: Angus / 《世界未解之谜周刊》
> **Created**: 2026-03-31
> **Status**: Draft
> **Scope**: Godot single-player weekly loop

## Pillar 1: Investigation Must Feed Publication

The game's front half and back half are one system. Exploration exists to create, distort, or deny editorial material; publication exists to cash out the consequences of exploration.

**Design test**: If a feature does not materially change clue quality, issue composition, or next-week state, it should not delay MVP.

## Pillar 2: Truth and Sensation Must Stay in Tension

The player should never be able to maximize credibility, weirdness, and profit with the same obvious move. Good decisions come from visible compromise.

**Design test**: If a mechanic makes "best story" always equal to "most profitable story," rework it.

## Pillar 3: One Week Must Read as One Arc

Every week should open with context, present limited choices, end with a publishable issue, and produce a meaningful carryover into the next week.

**Design test**: If a system cannot produce value or consequence inside a single week, move it out of MVP unless it is a foundation dependency.

## Pillar 4: Occult Pressure Is Both Reward and Threat

Strange knowledge should unlock opportunities, not just flavor. But it must also destabilize long-term control through macro-attribute pressure, hidden content risk, or editorial drift.

**Design test**: If occult-facing choices only add content without adding instability, the pillar is not being served.

## Pillar 5: Readability Beats Feature Count

The project should prefer a small number of legible interconnected rules over parallel prototype branches or overloaded content layers.

**Design test**: If a new system makes the loop harder to read before it makes it deeper, defer it.

## Anti-Pillars

- **We will NOT build parallel canonical rulesets** because HTML reference prototypes and Godot runtime logic drifting apart will stall production.
- **We will NOT treat the editorial phase as cosmetic presentation only** because that would break the core identity of the project.
- **We will NOT chase broad faction, story synthesis, or content scale before the week loop is stable** because it would compromise readability and implementation speed.
- **We will NOT solve prototype weakness with UI polish first** because unclear rules hidden behind pretty surfaces are still unclear.

## Current MVP Implications

- Keep Godot as the single implementation source of truth.
- Keep the week loop narrow and replayable.
- Keep story synthesis outside current MVP, but preserve its future interface through clue and story data contracts.
- Prefer documentation and architecture cleanup over adding more isolated prototype screens.
