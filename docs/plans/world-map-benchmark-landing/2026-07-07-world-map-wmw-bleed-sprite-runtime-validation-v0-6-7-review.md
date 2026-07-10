# WMW Bleed Sprite Runtime Validation v0.6.7 Review

Date: 2026-07-07

## Artifact Type

`provisional bleed sprite validation / not final art / not Godot capture`

This pass validates the v0.6.6.1 export-bleed rule by wrapping the existing proof carriers in transparent bleed, placing them back by export rect, and confirming the inner functional card rect still lands on the accepted source position.

## Output Files

- Provisional sprite contact sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/328-world-map-wmw-v0-6-7-bleed-safe-provisional-sprite-contact.png`
- Runtime composition: `docs/screenshots/2026-06-24-world-map-benchmark-landing/329-world-map-wmw-v0-6-7-bleed-safe-runtime-composition.png`
- Runtime QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/330-world-map-wmw-v0-6-7-bleed-safe-runtime-composition-qa.png`
- 100% crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/331-world-map-wmw-v0-6-7-bleed-safe-runtime-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/332-world-map-wmw-v0-6-7-bleed-safe-runtime-validation-manifest.json`
- Provisional sprite directory: `docs/screenshots/2026-06-24-world-map-benchmark-landing/wmw-v0-6-7-bleed-safe-provisional-sprites/`
- Generator: `tmp/wmw_v06_7_bleed_sprite_runtime_validation.py`

## Result

`PASS as bleed-sprite contract validation; NOT final art; NOT runtime-ready.`

- All four provisional sprites have transparent edge clearance.
- All four sprites align their inner functional rect back to the accepted source card rect after applying the 12px bleed offset.
- No card or photo non-uniform resize is introduced.
- Runtime title/meta text still fits after switching from inner-rect placement to export-rect placement.

## Why It Matters

v0.6.6.1 corrected the conceptual rule: final sprite bounds need transparent bleed, while runtime layout still uses the inner functional rect. v0.6.7 proves the rule is mechanically usable. The export rect can be larger without shifting the card's functional layout.

## Still Not Validated

- Final clean transparent art. These provisional sprites wrap proof carriers from v0.6.4.
- Godot imported texture behavior.
- Godot `Label` font metrics.
- Hover, pressed, focused, selected, disabled, and locked state frames.

## Next Gate

Use the same export/inner rect contract to request or generate final clean sprites. The next production candidate must replace the provisional proof carriers with clean art, then rerun this validation plus a minimal Godot capture.
