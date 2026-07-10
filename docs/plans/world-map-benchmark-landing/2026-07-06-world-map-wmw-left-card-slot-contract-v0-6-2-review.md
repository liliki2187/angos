# WMW World Map Left Card Slot Contract v0.6.2 Review

Date: 2026-07-06

## Artifact Type

`contract_overlay / source_locked_left_cards / ratio_report / not atlas / not final art`

This pass does not rebuild the left-card art. It locks the accepted source component/image pairing so later no-text shells, atlas slices, and runtime assembly do not change the already-good photo composition.

## Output Files

- Source overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/304-world-map-wmw-v0-6-2-left-card-slot-contract-overlay.png`
- 1:1 source-locked crops: `docs/screenshots/2026-06-24-world-map-benchmark-landing/305-world-map-wmw-v0-6-2-left-card-source-locked-crops.png`
- Ratio report: `docs/screenshots/2026-06-24-world-map-benchmark-landing/306-world-map-wmw-v0-6-2-left-card-slot-ratio-report.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/307-world-map-wmw-v0-6-2-left-card-slot-contract-manifest.json`
- Generator: `tmp/wmw_v06_2_left_card_slot_contract.py`

## Result

`PASS as contract overlay; NOT a production component sheet.`

The pass proves that the accepted source screen contains state-specific photo slot ratios:

| Card | Source Photo Slot | Ratio | v0.6.1 Universal Slot | Mismatch |
| --- | ---: | ---: | ---: | ---: |
| selected / North America | 237 x 136 | 1.74:1 | 1.75:1 | 0% |
| available / Europe | 237 x 130 | 1.82:1 | 1.75:1 | 4% |
| warning / Africa | 237 x 56 | 4.23:1 | 1.75:1 | 59% |
| locked / South America | 237 x 109 | 2.17:1 | 1.75:1 | 20% |

The v0.6.1 crop failure is therefore structural: it used one new `262x150` photo slot for all states. That was tolerable for selected/available but destructive for warning and visibly harmful for locked.

## UX / UI Input

UX diagnosis: the issue is a P1 source-image / photo-slot / card-shell contract failure. A card can still be clickable and text-readable while failing as a region card, because the region identity image becomes a broken placeholder.

UI design guidance: left cards should lock `photo_rect`, `label_plate_rect`, `status_button_rect`, and `badge_anchor` as a component contract. If image ratios differ by state, the component board must explicitly choose `cover crop`, `contain + matte`, or `state-specific art slot`; it must not force every state into one crop result.

## Production Rule

For existing accepted left-card references:

- Preserve each accepted `photo_rect` ratio unless snapshot art is re-authored.
- Do not normalize photo slots across state variants by default.
- Do not use cover crop to hide a changed slot ratio.
- If a state-specific source is very wide or very narrow, either keep its slot ratio or regenerate/crop a new source image for the chosen slot.
- Validate in three parts: `card_shell_pass`, `image_slot_contract_pass`, and `text_action_contract_pass`.

## Next Gate

Build v0.6.3 as a source-aware no-text left-card shell:

1. Use this manifest as the fixed source contract.
2. Preserve source-specific photo ratios or explicitly mark a state as needing re-authored snapshot art.
3. Keep label and action carriers orthogonal.
4. Produce 100% crops and a component matrix; do not call it atlas until state frames and runtime text pass.
