# WMW Clean Sprite Production Pack v0.6.8 Review

Date: 2026-07-07

## Artifact Type

`art handoff pack / imagegen-ready briefs / not final art / not atlas / not Godot capture`

This pass converts the accepted left-card contract into a clean sprite production package. It does not claim the proof carriers are final resources. Its purpose is to make the next art or image-generation step produce assets that still fit the validated UI runtime contract.

## Output Files

- Overview sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/333-world-map-wmw-v0-6-8-clean-sprite-production-pack.png`
- Per-state brief sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/334-world-map-wmw-v0-6-8-per-state-brief-sheet.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/335-world-map-wmw-v0-6-8-clean-sprite-production-pack-manifest.json`
- Brief directory: `docs/screenshots/2026-06-24-world-map-benchmark-landing/wmw-v0-6-8-clean-sprite-production-briefs/`
- Generator: `tmp/wmw_v06_8_clean_sprite_production_pack.py`

## Result

`SUPERSEDED FOR LEFT-REGION-CARD GEOMETRY by v0.6.9; retained as a process/error record.`

User review found that v0.6.8 incorrectly allowed same-class region card states to have different heights and local slot geometry. Do not use this pass as the left-region-card production geometry source. Use `2026-07-07-world-map-wmw-region-card-class-contract-v0-6-9-review.md` and `338-world-map-wmw-v0-6-9-region-card-class-contract-manifest.json` instead.

- Each state has its own brief instead of one universal card template.
- Each brief separates accepted visual target, proof-only carrier, required clean layer stack, export contract, and rejection rules.
- The export contract keeps the v0.6.6.1 / v0.6.7 distinction between transparent bleed bounds and inner functional card bounds.
- The hard rules explicitly reject baked runtime text, pseudo text, cropped edges, perspective slant on functional carriers, changed photo ratio, and fine-grunge detail replacing broad low-poly color planes.

## Why This Exists

The previous failures came from treating a generated visual mock as if it were already a usable UI resource. v0.6.8 reverses that: the accepted image is only the visual target, while the actual production request is a structured clean-sprite contract.

This is the bridge between style exploration and asset UI-ization:

- Art can preserve the benchmark look without baking unreadable text.
- UI can render real text in known safe zones.
- Runtime can place sprites by export rect while aligning functional content by inner rect.
- Future validation can fail a resource for measurable reasons instead of only by feel.

## Still Not Validated

- Final clean transparent PNG art.
- Whether image generation can obey these briefs without text hallucination.
- Godot import behavior and texture filtering.
- Godot `Label` font metrics on the clean sprites.
- Hover, pressed, focused, selected, disabled, and locked state frames.

## Next Gate

Generate or export the four clean state sprites from the v0.6.8 briefs. Then rerun the v0.6.7 bleed-safe runtime validation with those clean sprites instead of proof carriers. Only after that should the result enter a minimal Godot capture.
