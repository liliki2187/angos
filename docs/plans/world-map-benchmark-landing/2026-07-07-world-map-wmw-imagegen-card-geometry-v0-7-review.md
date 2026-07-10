# WMW Imagegen Card Geometry v0.7 Review

Date: 2026-07-07

## Artifact Type

`imagegen attempt geometry QA / visual reference only / not production atlas`

This pass tests whether prompt-only image generation can create four same-class `left_region_card` state sprites that satisfy the v0.6.9 geometry contract.

## Output Files

- First imagegen attempt: `docs/screenshots/2026-06-24-world-map-benchmark-landing/339-world-map-wmw-v0-7-0-imagegen-uniform-card-sheet-source.png`
- v0.7.0 candidate: `docs/screenshots/2026-06-24-world-map-benchmark-landing/340-world-map-wmw-v0-7-0-imagegen-uniform-card-sheet-candidate.png`
- v0.7.1 candidate: `docs/screenshots/2026-06-24-world-map-benchmark-landing/341-world-map-wmw-v0-7-1-imagegen-wide-card-sheet-candidate.png`
- Geometry QA sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/342-world-map-wmw-v0-7-1-imagegen-card-geometry-qa.png`
- Crop sheet: `docs/screenshots/2026-06-24-world-map-benchmark-landing/343-world-map-wmw-v0-7-1-imagegen-card-crops.png`
- Manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/344-world-map-wmw-v0-7-1-imagegen-card-geometry-manifest.json`
- Generator / QA script: `tmp/wmw_v07_imagegen_card_geometry_qa.py`

## Result

`FAIL as production sprite source; USEFUL as visual reference.`

v0.7.0 failed both uniform-size and target-ratio checks:

- Size range: width `39px`, height `8px`
- Ratio max error: `0.286`

v0.7.1 improved ratio but still failed same-class width consistency:

- Size range: width `22px`, height `0px`
- Ratio max error: `0.048`
- Ratio gate passes, but class uniformity gate fails.

## Interpretation

Prompt-only image generation is good enough to explore the WMW visual language and state skins. It is not reliable enough to define production geometry for reusable UI components. The generated sheets still need exact class-contract enforcement before they can become atlas resources.

## Loop Log

**Trigger Source**  
Parent self-check after generating clean sprite sheets from v0.6.9 briefs.

**Original Problem**  
The first generated sheet made same-state cards but drifted toward square cards. The second generated sheet was visually closer, but the cards still had inconsistent widths.

**Failure Attribution**  
The prompt described desired geometry, but the image model optimized for visual plausibility rather than pixel-exact component contracts. This is the same family of problem as earlier: treating a pretty image as if it can define UI geometry.

**This Round Handling**  
Generated candidates were copied into the workspace, measured, overlaid, and explicitly rejected as production sprite sources. They are kept only as art references.

**Recurrence Protection**  
All imagegen outputs for reusable UI components must pass `component_class_uniformity_gate` before being promoted. If the output is close visually but fails pixel geometry, the next step is exact-geometry redraw/export against the class contract, not direct cropping.

**Whether Deposited**  
Deposited in this review and the v0.7 manifest. The broader same-class hard gate was already added to `docs/onboarding/assetized-ui-production-chain.md` in v0.6.9.

## Next Gate

Use v0.7.1 as a visual reference only. Produce exact clean transparent sprites against the v0.6.9 `left_region_card` contract using one of these paths:

1. Artist redraw/export: preferred for production quality.
2. Imagegen only for texture/photo/state-skin inspiration, then rebuild the component on exact masks.
3. A temporary hybrid proof may be created for runtime validation, but must be labeled as `runtime_skeleton / visual_reference_mashup`, not final art.

