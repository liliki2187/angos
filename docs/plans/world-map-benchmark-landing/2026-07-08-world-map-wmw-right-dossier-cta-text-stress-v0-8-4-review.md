# WMW Right Dossier + CTA Text Stress v0.8.4 Review

Date: 2026-07-08

## Artifact Type

`text_capacity_stress / right_dossier_page / right_action_lane / not final typography / not final art / not atlas`

This pass tests whether the v0.8.3 right-side contract can hold real Chinese content and longer stress strings.

## Output Files

- Text stress board: `docs/screenshots/2026-06-24-world-map-benchmark-landing/364-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-board.png`
- Normal full-screen refill: `docs/screenshots/2026-06-24-world-map-benchmark-landing/365-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-full.png`
- Stress QA full-screen refill: `docs/screenshots/2026-06-24-world-map-benchmark-landing/366-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-qa.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/367-world-map-wmw-v0-8-4-right-dossier-cta-text-stress-manifest.json`
- Generator script: `tmp/wmw_v084_right_dossier_text_stress.py`

## Contract Under Test

| Class / Slot | Value |
| --- | --- |
| `right_dossier_page` | `320 x 520` |
| `right_action_lane` | `284 x 50` |
| CTA `label_plate` | `170 x 32` |
| `title_slot` | `160 x 34` |
| `status_stamp` | `58 x 58` |
| `meta_slot` | `196 x 22` |

## Result

The contract passes this text-capacity stress:

| Scenario | Result |
| --- | --- |
| normal | `8 / 8` fields fit |
| stress | `8 / 8` fields fit |

This validates capacity, not final visual taste.

## Font Stress Findings

| Field | Normal font | Stress font | Note |
| --- | ---: | ---: | --- |
| title | `26` | `21` | stress title fits, but slot is close to upper limit |
| risk stamp | `18` | `18` | stable |
| recommend stamp | `13` | `13` | stable |
| heat line | `13` | `13` | stable |
| meta line | `13` | `13` | stress width `183px` inside slot, close but pass |
| CTA 1 | `14` | `13` | most constrained CTA; needs quiet label plate |
| CTA 2 | `16` | `15` | pass |
| CTA 3 | `18` | `18` | pass |

## Production Implication

`right_action_lane = 284 x 50` can continue, but the label plate is not allowed to lose readable space in clean-sprite art.

The following must be protected in the no-text art brief:

- CTA label plate must stay visually quiet.
- No diagonal facet, fold, wrinkle, paper tear, badge edge, or shadow may cross CTA text.
- The right action badge must not shift left into the label plate.
- Stress title and meta text should remain on simple paper / muted color modules.
- If final typography uses a wider font than this test, rerun text stress before atlas.

## What Is Not Validated

- Final title art direction.
- Final UI font choice.
- Hover / pressed / disabled / locked state text.
- All possible localization strings.
- Godot runtime font rendering.
- Final WMW paper color and texture.

## Loop Log - Capacity Pass Is Not Typography Approval

- Trigger source: After v0.8.3 normalized the right-side page and CTA rows, the next risk was whether real Chinese UI strings actually fit inside those slots.
- Original issue: Previous iterations repeatedly treated blank-slot fit as enough, then real text later appeared too big, too small, too close to edges, or visually pasted on.
- Failure attribution: Geometry contracts are necessary but not sufficient. A `label_plate` can be correctly measured and still fail if the longest real CTA needs a tiny font or if the art makes the text surface noisy.
- Current handling: v0.8.4 tests normal and stress strings in the exact contract. All fields fit, but CTA 1 and title are tight and must be protected in the no-text art brief.
- Recurrence protection: Any clean-sprite brief for right-side components must carry these stress strings and font-size results as required QA input.
- Captured: Yes. This review records the capacity results and the caution that this is not final typography approval.

## Next Gate

If accepted:

1. Write v0.8.5 no-text clean-sprite brief for `right_dossier_page` and `right_action_lane`.
2. Include the v0.8.4 stress strings as non-negotiable QA examples.
3. Then move to bottom receipt class contracts before requesting full art assets.
