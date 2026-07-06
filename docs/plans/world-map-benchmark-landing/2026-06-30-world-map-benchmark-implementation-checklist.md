# World Map Benchmark Implementation Checklist

Status: branch implementation checklist for the World Mystery Weekly benchmark landing experiment.

## Current Locks

Generated screen candidate:

- `95-world-map-imagegen-color-recorrected-v0-51.png`

Color guardrail:

- `92-world-map-first-version-color-reference.png`

Local selected-region proof:

- `103-world-map-v051-local-olive-grade-proof-v2.png`
- `104-world-map-v051-local-olive-proof-v2-color-check.png`

Runtime token contract:

- `2026-06-30-world-map-selected-region-palette-token-contract.md`

Branch source manifest:

- `2026-06-30-world-map-wmw-source-manifest.json`

Single-state component contract:

- `2026-06-30-world-map-wmw-single-state-component-contract.json`

No-text imagegen brief:

- `2026-06-30-world-map-wmw-no-text-orthogonal-imagegen-brief.md`

## Do Not Confuse These

- v0.51 is the generated style candidate.
- proof v2 is a local palette-token proof, not a new generated screen.
- the current Godot v6g preview is a runtime-token test bed, not the accepted new benchmark look.
- A geometry-correct orthogonal generation is not automatically a style candidate. If it removes broad low-poly color blocks, component value planes, or map large-plane construction, it is only an orthogonal constraint test.
- A style-rich generation is not automatically a geometry candidate. If the right dossier, CTA stack, bottom receipts, left cards, or any other functional component is visibly slanted, it fails even when the color blocks look closer to the benchmark.

## Replacement Layers

### 1. Runtime Tokens

Can be changed immediately in Godot:

- selected halo color
- selected brackets / corner marks
- selected overlay wash
- text colors
- route / trace colors if routes remain in a later structure
- badge border colors

Current selected-region token family:

- `#606548`
- `#5B5E3E`
- `#807E50`

### 2. Component Textures

Must be regenerated, re-cut, or locally graded as component assets:

- central map board, including the baked selected North America landmass
- left region card stack
- right dossier sheet body
- bottom folder/status cards
- CTA plate atlas
- sticker/icon atlas

Do not fix these by drawing flat programmatic shapes over the art unless the overlay is deliberately part of the design language.

### 3. Runtime Text

Should remain runtime-rendered:

- region names
- task counts
- remaining days
- risk/status summaries
- button labels
- mission preview text
- dynamic numbers and badges

Do not bake these into the generated texture.

### 4. Fixed Art Text / Stickers

Can become fixed PNG/SVG-like bitmap assets after separate generation and proofing:

- `WMW`
- globe sticker
- eye sticker
- warning sticker
- hand sticker
- short status stamps such as `高危`, `红线`, `锁定`, `已派遣`

Each fixed text asset still needs OCR / manual character QA.

## Next Practical Pass

1. Create or regenerate no-text component assets using v0.51 as the full-screen reference.
2. Apply selected-region olive token to the map-board selected landmass through local LUT or a newly cut map-board asset.
3. Keep runtime text from Godot, using established font tokens.
4. Capture 1920x1080 screenshots and compare against:
   - v0.51 for overall style
   - first_ref for brightness
   - proof v2 for selected-region hue
   - the clean low-poly branch benchmarks for large polygon scale and component flat paper/color-block planes
5. Reject the pass if it reintroduces:
   - full-screen dark drift
   - tilted information panels
   - tilted functional components, interactive surfaces, state surfaces, or skewed `content_rects / hit_rects`
   - cross-map route lines not required by the flow
   - blank placeholder text fields
   - over-detailed technical UI clutter
   - dense world-map triangulation that reads as GIS / mesh texture
   - flat component bodies where left cards, right dossier, CTA plates, or bottom receipts have lost broad low-poly color-value blocks
   - orthogonality achieved by making every functional piece a plain software rectangle
   - visible crease / wrinkle lines across text slots, which the benchmark does not use on text components
   - high-contrast diagonal folded-corner / torn-paper / crease marks inside CTA plates, bottom receipts, dossier text bodies, or any other functional component
   - any right-side dossier, CTA stack, or bottom receipt face that is still slanted after generation

## Dual Gate For Next Generation

Every WMW world-map candidate must pass both gates:

1. **Functional geometry gate**: all information-bearing, clickable, stateful, or dynamic-text surfaces are 0-degree orthogonal.
2. **Style retention gate**: those same orthogonal surfaces still inherit the benchmark's broad flat low-poly color blocks, large value planes, cut-paper shadows, and hand-drawn sticker/icon tension, without wrinkle / crease lines crossing text slots.

Do not promote a candidate if only one gate passes. A slanted but beautiful image fails; a square but flat image also fails.

## QA Failure Notes

- `110-world-map-wmw-flat-color-orthogonal-v0-56.png` is downgraded to a bias sample, not a candidate. It recovered flatter color blocks in some components, but the bottom receipt cards contain uncomfortable high-contrast diagonal fold / tear-like marks, and the right CTA stack still has actual generated edges that read as slanted.
- `111-world-map-wmw-flat-color-orthogonal-v0-56-qa.png` and `112-world-map-wmw-flat-color-orthogonal-v0-56-right-qa-crop.png` are not sufficient proof. The QA boxes were manually drawn as ideal orthogonal references instead of tracing the real generated component edges, so they produced a false pass.
- Future QA must inspect the actual visible edge of each right CTA strip, text slot, bottom receipt, dossier front, left card, and media frame. If the real edge is slanted, the candidate fails even when the reference box is straight.
- Future style QA must distinguish `flat low-poly color-value blocks` from `fold / crease / tear / wrinkle` marks. Text components and functional paper bodies may have low-contrast flat color blocks, but not bright diagonal fold scars.

## Current v0.57 Visual QA

- `113-world-map-wmw-foldless-orthogonal-v0-57.png` is the next generated no-text draft. It is a hard-failure repair candidate, not a production benchmark.
- `119-world-map-wmw-v0-57-right-cta-raw-crop.png` and `120-world-map-wmw-v0-57-bottom-receipt-raw-crop.png` are raw crops made after reading the generated image's real size (`1672x941`). Do not assume all imagegen outputs are `1920x1080`.
- `121-world-map-wmw-v0-57-right-cta-real-edge-qa.png` and `122-world-map-wmw-v0-57-bottom-receipt-real-edge-qa.png` are the current QA proof crops. They trace the actual CTA and receipt edges rather than drawing ideal reference boxes on the full screen.
- First-pass result: the v0.56 bright diagonal fold / tear scars on the bottom receipts are removed, and the right CTA stack no longer shows the obvious slant that caused the previous failure.
- Residual risks before promotion: bottom receipt perforation dots may still be too literal / detailed for the benchmark, map and thumbnails still need a broad-plane style pass, and the user must review whether the overall image keeps enough of the original benchmark's premium editorial feel.

## Open Questions

- Whether the final world-map structure should keep any route lines at all. The v0.51 generated candidate avoids cross-map route lines; older runtime previews still include them.
- Whether the selected landmass should be a baked texture state, runtime LUT, or separate selected overlay asset.
- Whether the current v6g assetization tooling should be reused for this branch. The v6g assets themselves are legacy test beds and are not the current visual source.
