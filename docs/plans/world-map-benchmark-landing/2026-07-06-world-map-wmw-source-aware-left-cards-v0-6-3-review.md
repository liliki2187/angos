# WMW Source-Aware Left Cards v0.6.3 Review

Date: 2026-07-06

## Artifact Type

`source-aware component sheet / no-text + filled preview / QA overlay / not atlas / not final art`

This pass tests the corrected workflow after the v0.6.1 crop failure: preserve the accepted card/photo pairing first, then clear and refill dynamic text. It does not repaint the card shell or normalize state ratios.

## Output Files

- No-text sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/308-world-map-wmw-v0-6-3-source-aware-left-cards-no-text.png`
- Filled text preview: `docs/screenshots/2026-06-24-world-map-benchmark-landing/309-world-map-wmw-v0-6-3-source-aware-left-cards-filled.png`
- QA overlay: `docs/screenshots/2026-06-24-world-map-benchmark-landing/310-world-map-wmw-v0-6-3-source-aware-left-cards-qa.png`
- Filled vs QA crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/311-world-map-wmw-v0-6-3-source-aware-left-cards-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/312-world-map-wmw-v0-6-3-source-aware-left-cards-manifest.json`
- Generator: `tmp/wmw_v06_3_source_aware_left_cards.py`

## Result

`PASS for source-slot preservation; READY for user visual review; NOT atlas-ready yet.`

- The four left cards use 1x source crops from the accepted v0.4.1 screen.
- Region snapshot content is not resized, stretched, compressed, or forced into a universal crop.
- Dynamic title/meta text is cleared from the paper label plate and refilled as a preview.
- QA overlay marks `card_shell_rect`, `photo_rect`, `label_rect`, and `action_rect`.

## What This Fixes

- Fixes the v0.6 non-uniform compression problem.
- Fixes the v0.6.1 cover-crop problem by preserving source-specific photo ratios.
- Prevents false pass where a component shell looks usable but image identity has been damaged.

## Remaining Limits

- This is still a source-aware proof, not a freshly authored no-text asset master.
- The blank label plate is a cleanup layer over the source card; final art should export a real no-text card shell with the same rects.
- State icons are still sourced from the accepted reference crop; final atlas will need state frames and hover/pressed/disabled variants.
- The annotation text on the right is QA-only and not part of game UI.

## Gate For Next Step

If accepted visually, the next step is an atlas planning pass:

1. Export or regenerate clean no-text left-card shells using the v0.6.3 rect contract.
2. Preserve per-state `photo_rect` ratios, or explicitly mark which states require re-authored snapshot art.
3. Split static shell, photo snapshot, label plate, state icon, and dynamic text layers.
4. Recompose one real world-map runtime screenshot and compare against this v0.6.3 proof.
