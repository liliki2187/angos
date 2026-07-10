# WMW Clean Resource Request v0.6.6.1 Review

Date: 2026-07-07

## Artifact Type

`production resource request / bleed-safe coordinate contract / not final atlas`

This is a correction to v0.6.6 after the user pointed out that the warning-state clean export target looked clipped at the top.

## Output Files

- Bleed-safe clean resource request sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/325-world-map-wmw-v0-6-6-1-bleed-safe-clean-resource-request-sheet.png`
- Bleed-safe coordinate contract sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/326-world-map-wmw-v0-6-6-1-bleed-safe-coordinate-contract-sheet.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/327-world-map-wmw-v0-6-6-1-bleed-safe-clean-resource-request-manifest.json`
- Diagnosis crop: `docs/screenshots/2026-06-24-world-map-benchmark-landing/324-world-map-wmw-v0-6-6-warning-card-crop-diagnosis.png`
- Generator: `tmp/wmw_v06_6_clean_resource_request.py`

## Result

`PASS as bleed-safe production request; NOT atlas-ready.`

The correction separates two concepts:

- `inner_functional_rect`: the clickable/text/photo coordinate contract used by runtime UI.
- `export_size_with_bleed`: the sprite export bounds that include transparent padding for outer strokes, hand-drawn edges, and shadows.

## Loop Log

- Trigger source: User asked why the warning-state component top looked clipped in the v0.6.6 resource request sheet.
- Original problem: The clean export target used the inner functional card size as if it were the final sprite crop bounds.
- Failure cause: v0.6.6 conflated `functional card rect` with `sprite export bounds`. Functional rects can be tight, but final sprites need transparent bleed around the visible art.
- This-round handling: Added `export_bleed_pad_px = 12`, generated v0.6.6.1 sheets, and wrote `inner_functional_size`, `export_size_with_bleed`, and `runtime_export_rect_1920` into the manifest.
- Recurrence protection: Future atlas requests must distinguish inner rects from export rects. QA must reject any component whose outer stroke, shadow, tape, hand-drawn edge, or paper thickness touches the sprite boundary.
- Captured: Yes. The rule is captured in this review and in `327-world-map-wmw-v0-6-6-1-bleed-safe-clean-resource-request-manifest.json`.

## Production Rule

Do not crop final UI sprites exactly at the functional component bounds. Export sprites with transparent bleed, then place them in runtime using the export rect while using inner rects for text, photo, and hit zones.
