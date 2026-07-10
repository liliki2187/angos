# WMW Region Card Class Contract v0.6.9 Review

Date: 2026-07-07

## Artifact Type

`corrected component-class contract / imagegen-ready briefs / not final art / not Godot capture`

This pass fixes the v0.6.8 geometry error: the four left-region cards were treated as separate crop-derived components, even though they are one functional component class with multiple states.

## Output Files

- Class audit sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/336-world-map-wmw-v0-6-9-region-card-class-audit.png`
- Uniform brief sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/337-world-map-wmw-v0-6-9-region-card-uniform-brief-sheet.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/338-world-map-wmw-v0-6-9-region-card-class-contract-manifest.json`
- Brief directory: `docs/screenshots/2026-06-24-world-map-benchmark-landing/wmw-v0-6-9-left-region-card-class-briefs/`
- Generator: `tmp/wmw_v06_9_region_card_class_contract.py`

## Result

`READY as corrected geometry handoff; NOT visual pass candidate.`

- All four states now share `class_id = left_region_card`.
- All four states share `inner_functional_size = 352x228`.
- All four states share `export_size_with_bleed = 376x252`.
- All four states share the same `photo_slot`, `label_plate`, `action_button`, `title_text_box`, and `meta_text_box`.
- `v0.6.8` is superseded for left-region-card geometry.

## Corrected Class Contract

- `inner_functional_size`: `[352, 228]`
- `export_size_with_bleed`: `[376, 252]`
- `transparent_bleed_px`: `12`
- `photo_slot`: `[48, 25, 285, 161]`
- `label_plate`: `[35, 162, 203, 216]`
- `action_button`: `[271, 160, 331, 220]`
- `title_text_box`: `[43, 166, 195, 191]`
- `meta_text_box`: `[43, 193, 195, 212]`

## Loop Log

**Trigger Source**  
User pointed out that the four component targets in v0.6.8 had inconsistent height and aspect, especially the third component where the top edge was almost compressed away.

**Original Problem**  
The workflow treated source crop bounds as production component bounds. `region_warning` and `region_locked` inherited shorter crop heights, while `region_available` inherited local slot drift even though its overall size matched selected.

**Failure Attribution**  
The previous gates checked bleed, text fit, and no-text layering, but did not check component-class uniformity. The manifest had per-state contracts, but no higher-level `class_id` contract saying these states belong to the same reusable component. That allowed state skins to accidentally redefine base geometry.

**This Round Handling**  
v0.6.9 introduces a class-level contract. State differences are restricted to tint, icon/button treatment, paper wear, disabled/warning tone, and non-functional decoration. Functional geometry is fixed across all states.

**Recurrence Protection**  
Add `component_class_uniformity_gate`: before manifest or atlas handoff, every state under the same `class_id` must share base size, export size, content slots, hit rects, and core nine-slice / padding assumptions. If a compact or large version is needed, it must get a new `class_id`.

**Whether Deposited**  
Deposited in this review, in the v0.6.9 manifest, and in `docs/onboarding/assetized-ui-production-chain.md` as a 2026-07-07 hard gate.

## Next Gate

Generate or export clean sprites from the v0.6.9 briefs. Then rerun the bleed-safe runtime validation with these uniform state sprites. Do not use v0.6.8 geometry for left-region-card production.

