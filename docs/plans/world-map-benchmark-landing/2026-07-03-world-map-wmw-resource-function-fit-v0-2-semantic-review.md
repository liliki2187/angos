# World Map WMW Resource-Function Fit Semantic QA v0.2 Review

Date: 2026-07-03

## Artifact Type

`semantic QA contract / dry-run / not production atlas`

This pass rebuilds the failed v0.1 fit QA. It separates visual resource regions from runtime text and interaction regions.

## Output Files

- Full semantic QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/272-world-map-wmw-resource-function-fit-v0-2-clean-semantic-qa.png`
- 100% crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/273-world-map-wmw-resource-function-fit-v0-2-clean-semantic-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/271-world-map-wmw-resource-function-fit-v0-2-semantic-manifest.json`

## Result

**v0.2 is a better QA contract candidate than v0.1, but it is still not a final atlas pass.**

The important repair is semantic separation:

- `visual_module_rect`: the actual colored / paper / bevel module in the benchmark art.
- `text_plate_rect`: the surface that is intended to carry runtime text.
- `ink_safe_rect`: the smaller box where glyph pixels may render.
- `hit_rect`: the clickable region; it may be bigger than the glyph but must not be confused with the glyph.
- `glyph_rect`: the visible check / arrow / target mark only.

## What Changed From v0.1

- The right CTA no longer uses one ambiguous `right_action_icon_hit`.
- CTA action areas are split into `action_visual_plate`, `action_glyph_rect`, and `action_hit_rect`.
- Green boxes are now explicitly "ink safe", not the full white text plate.
- Bottom receipts split title, value, progress, and hit areas.
- Left cards split card shell, thumbnail art, label plate, action glyph, and hit area.

## Automated Check

- Components: 11
- Layers: 90
- Axis-aligned rectangles: 90
- Nesting issues: 0
- Validation pass: true

## Human Visual Check Notes

- The user-problem warning CTA crop now shows the right arrow glyph as coral, the right clickable action area as magenta dashed, the row module as yellow, the text plate as cyan, and the glyph-safe area as green.
- The crop sheet should be used for review before any no-text atlas work.
- If a visible color module and its `visual_module_rect` still feel misaligned by eye, the manifest rect must be corrected before asset slicing.

## Known Limits

- The source is still a text-baked benchmark shell, so this does not prove final no-text art cleanup.
- Coordinates are manually authored from the benchmark image; final atlas assets need one more pass using the actual no-text components.
- This is a QA contract and fit proof, not a production screenshot.

## Next Gate

1. User / art review of v0.2 crops.
2. If approved, generate or paint no-text benchmark shells for each component.
3. Reapply the same v0.2 semantic manifest to those no-text shells.
4. Run multi-state long-text stress tests.
5. Only after those pass, slice atlas and integrate in Godot.
