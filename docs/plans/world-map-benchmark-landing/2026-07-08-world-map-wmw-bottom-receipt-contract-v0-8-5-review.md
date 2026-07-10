# WMW Bottom Receipt Contract v0.8.5 Review

Date: 2026-07-08

## Artifact Type

`component_class_contract_candidate / bottom_receipt_card / full-screen QA / text_capacity_stress / not final typography / not final art / not atlas`

This pass locks the three bottom receipt cards as one repeated component class.

## Output Files

- Source measurement audit: `docs/screenshots/2026-06-24-world-map-benchmark-landing/368-world-map-wmw-v0-8-5-bottom-receipt-source-audit.png`
- Contract candidate board: `docs/screenshots/2026-06-24-world-map-benchmark-landing/369-world-map-wmw-v0-8-5-bottom-receipt-contract.png`
- Full-screen reinsert QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/370-world-map-wmw-v0-8-5-bottom-receipt-reinsert-qa.png`
- Text stress board: `docs/screenshots/2026-06-24-world-map-benchmark-landing/371-world-map-wmw-v0-8-5-bottom-receipt-text-stress.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/372-world-map-wmw-v0-8-5-bottom-receipt-manifest.json`
- Generator script: `tmp/wmw_v085_bottom_receipt_contract.py`

## Source Measurement Result

The source reference is nearly uniform:

| Source object | Measurement |
| --- | ---: |
| weekly action receipt | `246 x 137` |
| intel pool receipt | `245 x 137` |
| redline account receipt | `246 x 137` |

The source is close enough visually, but production should still normalize the three cards into a single exact class.

## Contract Candidate

Recommended class:

| Field | Value |
| --- | --- |
| `class_id` | `bottom_receipt_card` |
| `export_size` | `246 x 138` |
| `positions` | `[288,558] / [557,558] / [826,558]` |
| horizontal gap | `23 px` |
| `left_icon_zone` | `52 x 52` |
| `title_slot` | `120 x 28` |
| `value_slot` | `128 x 32` |
| `meter_slot` | `166 x 24` |
| `hit_rect` | full `246 x 138` |

## Text Capacity Result

| Scenario | Result |
| --- | --- |
| normal | `6 / 6` fields fit |
| stress | `6 / 6` fields fit |

Largest pressure point:

| Field | Stress text | Font size | Text width | Slot note |
| --- | --- | ---: | ---: | --- |
| redline value | `12天后升温` | `23` | `120px` | fits inside `128px` slot, but close |

## What Is Validated

- Three bottom receipts can share one `246 x 138` class.
- Weekly / intel / redline states can differ by color and icon only.
- Title, value, icon, meter, and hit rect can remain fixed.
- Full-screen reinsert does not overlap the central map.
- Text capacity passes normal and stress cases.

## What Is Not Validated

- Final typography hierarchy.
- Whether bottom receipt values should be visually quieter.
- Final WMW paper color / texture.
- Hover / selected / clicked receipt states.
- Godot runtime font rendering.
- No-text sprite quality.

## Production Notes

- `bottom_receipt_card = 246 x 138` can continue as the production contract candidate.
- The third receipt is close to the right-side icon cluster; keep this safety distance in future full-screen QA.
- The `value_slot` is capacity-safe but visually strong. Typography review may choose to reduce value font weight/size without changing the component size.
- The meter slot must not change width by resource count.

## One-Vote Fails

The bottom receipt class fails if:

- weekly / intel / redline cards use different export sizes;
- redline card becomes taller because warning text is longer;
- meter slot changes width by resource count;
- icon or perforation shifts title / value slot;
- tape, paper shadow, or color tab expands runtime bounds;
- bottom receipt overlaps the central map, right dossier, or icon cluster after reinsert.

## Loop Log - Nearly Uniform Source Still Needs Exact Class Lock

- Trigger source: Continuing the world-map assetization route after left-card and right-dossier contracts; bottom receipts are another repeated component family.
- Original issue: The source receipts look almost uniform, which can tempt us to use them directly. But the middle card is still `1px` narrower, and production UI should not inherit source drift.
- Failure attribution: Earlier work let tiny source differences, AI crop differences, or visual balance choices become production geometry.
- Current handling: v0.8.5 normalizes all three receipts to one `246 x 138` class, reinserts them into the full screen, and runs text-capacity stress.
- Recurrence protection: Repeated components with near-identical source measurements still need exact class locking before clean sprites or atlas.
- Captured: Yes. This review records the contract and stress result.

## Next Gate

After user review:

1. Accept or adjust `bottom_receipt_card = 246 x 138`.
2. Continue remaining contracts:
   - central map panel;
   - top status strip;
   - icon / sticker badge set.
3. Then write clean-sprite briefs for accepted classes.
