# WMW Left Card Uniform Reinsert v0.8.2 Review

Date: 2026-07-07

## Artifact Type

`contract_reinsert_fit_proof / left_region_card / full-screen validation / not final art / not atlas`

This pass puts the unified left-side region card class back into the full world-map screen to answer whether a same-size card class can work in the real page layout.

## Output Files

- `204x150` full-screen proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/351-world-map-wmw-v0-8-2-left-card-uniform-reinsert-proof.png`
- `204x150` QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/352-world-map-wmw-v0-8-2-left-card-uniform-reinsert-qa.png`
- `204x150` 100% crops: `docs/screenshots/2026-06-24-world-map-benchmark-landing/353-world-map-wmw-v0-8-2-left-card-uniform-reinsert-crops.png`
- `204x150` manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/354-world-map-wmw-v0-8-2-left-card-uniform-reinsert-manifest.json`
- `204x160` full-screen proof: `docs/screenshots/2026-06-24-world-map-benchmark-landing/355-world-map-wmw-v0-8-2-left-card-uniform-160-reinsert-proof.png`
- `204x160` QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/356-world-map-wmw-v0-8-2-left-card-uniform-160-reinsert-qa.png`
- `204x150` vs `204x160` comparison: `docs/screenshots/2026-06-24-world-map-benchmark-landing/357-world-map-wmw-v0-8-2-left-card-150-vs-160-comparison.png`
- Size comparison manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/358-world-map-wmw-v0-8-2-left-card-size-comparison-manifest.json`
- Generator scripts:
  - `tmp/wmw_v082_left_region_card_reinsert.py`
  - `tmp/wmw_v082_left_region_card_size_compare.py`

## Result

The same-size left card class **does work in the full world-map layout**, but the earlier `204x150` candidate is not the best production choice.

Recommended next candidate:

| Field | Recommended value |
| --- | --- |
| `class_id` | `left_region_card` |
| `export_size` | `204 x 160` at 1280x720 reference scale |
| `positions` | `[44,24] / [44,196] / [44,368] / [44,540]` |
| `stack_gap` | `12 px` |
| `photo_slot` | `174 x 64` |
| `label_plate` | `114 x 32` |
| `action_badge` | `38 x 38` |
| `hit_rect` | full `204 x 160` card bounds |

## Comparison

| Candidate | Full-screen fit | Visual rhythm | Photo-slot pressure | Recommendation |
| --- | --- | --- | --- | --- |
| `204 x 150` | passes | slightly short / loose | higher, photo slot only `174 x 58` | do not freeze yet |
| `204 x 160` | passes | stronger left-list rhythm | lower, photo slot `174 x 64` | recommended next contract |

`204x160` keeps four cards inside the left column: last card bottom is `y=700`, still within the 720px reference screen. It also keeps the left list closer to the benchmark's card weight without returning to inconsistent per-state heights.

## What Is Validated

- Four `left_region_card` instances can be stacked in the full page as one uniform class.
- `selected / available / warning / locked` can share the same export size.
- `photo_slot`, `label_plate`, `action_badge`, and `hit_rect` can stay fixed across states.
- A uniform card class does not require changing the central map, right dossier, bottom receipts, or icon cluster.

## What Is Not Validated

- Final WMW art quality.
- Final low-poly material and color matching.
- Final typography tokens.
- Longest-string stress cases.
- Final no-text sprite slicing.
- Godot runtime assembly.

The proof images are contract / fit validation images. They deliberately should not be treated as final component art.

## Production Decision

Revise the previous `204x150` candidate to `204x160` before writing the clean-sprite brief.

Do not let the source art's unequal card heights return as state-specific production sizes. If art wants more selected-state presence, use glow, color, overlay, badge weight, or a separate explicitly named expanded class. Do not silently make selected taller inside `left_region_card`.

## Loop Log - Full-Screen Reinsert Before Freezing Class Size

- Trigger source: User asked to put the unified left components back into the whole interface to see whether the class works in context.
- Original issue: v0.8.1 produced a same-size contract candidate, but a component contract can still fail when returned to the full page: the stack might feel too sparse, crowd the bottom, crop images too much, or no longer match the benchmark rhythm.
- Failure attribution: Earlier iterations jumped from component sheets toward production before testing class geometry inside the full composition.
- Current handling: v0.8.2 compares `204x150` and `204x160` in the real world-map screen. Both fit, but `204x160` has better rhythm and less photo crop pressure.
- Recurrence protection: Every major component class must pass a full-screen reinsert proof before clean-sprite brief or atlas production. The class contract cannot be frozen from an isolated component sheet alone.
- Captured: Yes. This review records the gate; broader rules remain covered by `component_aspect_taxonomy`, `component_class_uniformity_gate`, and `image_slot_contract_pass`.

## Next Gate

If the user accepts the `204x160` direction:

1. Update the left-region-card class contract from `204x150` to `204x160`.
2. Produce v0.8.3 clean-sprite brief for `left_region_card`:
   - no baked runtime text;
   - four state skins;
   - fixed export size;
   - fixed photo slot;
   - fixed label plate;
   - fixed action badge;
   - fixed hit rect;
   - no non-uniform image scaling;
   - WMW low-poly block facets preserved only as material, not as text-slot wrinkles.
3. Then generate / request no-text art assets against that brief.
