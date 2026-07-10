# WMW World Map Left Cards / Bottom Receipts Geometry v0.5 Review

Date: 2026-07-06

## Artifact Type

`localized_geometry_gate / visible shell QA / not final art / not atlas`

This pass extends the v0.4.1 right dossier rule to the remaining repeated world-map components: left region cards and bottom receipt cards.

## Output Files

- Geometry QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/291-world-map-wmw-v0-5-1-left-bottom-geometry-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/292-world-map-wmw-v0-5-1-left-bottom-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/293-world-map-wmw-v0-5-1-left-bottom-geometry-manifest.json`
- Generator script: `tmp/wmw_v05_left_bottom_gate.py`

## Result

Scoped geometry gate candidate.

- Checked surfaces: 46
- Left region cards: visual shells, photo windows, label plates, title/meta lanes, action plates, and hit rects are readable as orthogonal functional carriers.
- Bottom receipts: text lanes, value lanes, icon slots, and progress strips are orthogonal enough for follow-up reconstruction.
- Important production risk: the bottom red receipt is partially overlapped by the right dossier stack in the full-screen composition. It must not be sliced directly from this screenshot as an independent atlas source.

## What This Proves

- The left-card grammar can proceed to no-text asset reconstruction without changing the world-map layout.
- The bottom receipt grammar can proceed, but only as separately rebuilt assets.
- The "visible shell first, text second" rule is applicable beyond the right dossier.

## What This Does Not Prove

- It does not produce final no-text left card or receipt atlas assets.
- It does not resolve color/material fidelity for the final WMW paper/token system.
- It does not test hover / selected / locked / disabled state variants.
- It does not validate runtime text fitting for future longest strings.

## Production Notes

- Left cards should be rebuilt as four state variants: selected, available, warning, locked.
- Bottom receipts should be rebuilt as three independent receipt components, not cropped from the full-screen mock.
- The red receipt needs a clean right edge in the source asset even if the final screen places the right dossier above it.
- Receipt progress strips should keep low-poly color blocks rectangular / horizontal. No triangular spikes, route arrows, or folds inside text/value lanes.

## Next Gate

1. Build a component correction sheet from independent no-text shells:
   - left region card: selected / available / warning / locked
   - bottom receipt: green / blue / red
   - right CTA: primary / secondary / warning using v0.4.1 clean CTA grammar
2. For each component, declare `visual_module_rect`, `photo_rect`, `text_plate_rect`, `value_rect`, `action_plate_rect`, `progress_rect`, and `hit_rect`.
3. Refill representative real text after the no-text shells pass.
4. Only then move toward atlas slicing / Godot manifest.
