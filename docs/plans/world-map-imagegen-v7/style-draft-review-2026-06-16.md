# World Map v7 Functional Style Draft Review

> Draft: `docs/screenshots/2026-06-16-world-map-v7-functional-style-draft/01-world-map-v7-functional-style-draft.png`  
> Prompt: `docs/plans/world-map-imagegen-v7/style-draft-prompt.md`  
> Status: style / functional-capacity candidate only; not a production component source yet.

## Passes

- Keeps the accepted world-map visual direction: deep navy editorial board, strong pixel-print texture, bright paper, and faceted low-poly paper continents.
- Removes baked readable UI text. No region names, countdowns, task names, CTA labels, or Chinese/English labels are present.
- Gives the top strip, left index, right dossier, CTA, and bottom ticker clear blank writing areas before Godot dynamic text.
- Makes the primary CTA a separate red action object instead of a label floating inside the right dossier.
- The selected North America state is visually readable through rings / route emphasis without relying on text.

## Risks Before Production

- The selected ring and route emphasis in this draft are visual-state placeholders. In production they must be separate runtime / atlas layers, not baked into the map base.
- The right dossier now has a stronger field structure, but its preview rows could still drift toward a task-list reading if Godot adds too much text. Keep it to 2-3 read-only previews.
- The left cards have enough broad writing space, but the right-side mini boxes should be reserved for short status / count only; do not put long state words there.
- The top strip is structurally clean, but the final Godot pass must keep it low weight so it does not compete with the map.
- The bottom ticker lanes should stay one-line receipts. Any longer explanation should move to the right dossier or a real log surface.

## Next Gate

Before using this draft for component production:

1. Ask the user to approve / reject the overall structure.
2. If approved, ask `angus_art_director` to review whether the draft still reads as Angus strong-pixel editorial UI.
3. Convert the v7 contract into manifest assets and generate components separately: map base, region card atlas, right dossier base, CTA atlas, ticker, pin / selected ring / route layers.
4. Run whole-screen, safe-zone, and 100% crop reviews before Godot replacement.
