# WMW World Map No-Text Orthogonal Imagegen Brief

Status: branch prompt brief for the next no-text component master. This is not a generated asset yet.

## Source

- Style candidate: `docs/screenshots/2026-06-24-world-map-benchmark-landing/95-world-map-imagegen-color-recorrected-v0-51.png`
- Component contract: `docs/plans/world-map-benchmark-landing/2026-06-30-world-map-wmw-single-state-component-contract.json`
- Color contract: `docs/plans/world-map-benchmark-landing/2026-06-30-world-map-selected-region-palette-token-contract.md`

## Primary Prompt

Use case: ui-mockup

Asset type: 16:9 no-text game UI component master for a desktop world-map screen.

Primary request: Generate a no-text World Mystery Weekly world-map UI component master for the selected-region screen. The design is a modern supernatural weekly magazine / editorial investigation board, using clean low-poly paper collage, large faceted color blocks, cut-paper UI objects, dark navy board background, muted ivory paper, low-chroma olive selected-region language, restrained teal information accents, and controlled red-orange deadline accents.

Composition: 1920x1080 desktop screen. Left side has four stacked region cards. Center has a large world map board. Right side has a selected-region dossier sheet with a header zone, media snapshot frame, and three stacked CTA/ticket plates. Bottom center has three small status receipt cards. Lower right has hand-cut sticker icons. All functional components face the camera square-on with no perspective.

Hard orthogonal rule: Every functional component must be perfectly square-on, axis-aligned, horizontal and vertical, 0 degree rotation. Any element that carries information, status, click, hover, pressed, disabled, selected, drag-over, or other player-facing operation semantics must be an orthographic rectangle parallel to the image edges. The left region cards, center map board frame, map pin/selected areas, right dossier paper front, media/photo frame, CTA plates, bottom status cards, title fields, ticket fields, status tickets, receipt cards, and all button label areas must stay square-on. No tilted, rotated, skewed, trapezoid, perspective, photographed, angled, leaning, diagonal, or slanted functional UI components. Decorative paper clips, back sheets, tabs, shadows, stickers, uneven cut-paper outer edges, and small tape pieces may be slightly irregular only when they do not carry information, state, or interaction.

Style retention rule: Orthogonal functional faces must not become flat software panels. Keep the functional geometry square-on, but preserve the benchmark's clean low-poly material language on the component skins: broad flat color-value planes, 4-8 large faceted value blocks per card/ticket/sheet, blocky cut-paper shadows, and subtle polygonal color shifts around quiet runtime text slots. Text slots may be calm in the center, and they must not contain visible wrinkle/crease lines; the surrounding plate, header, icon well, colored frame, and paper body must still show large low-poly color-block construction. Do not solve readability by erasing all internal color blocks and making plain blank rectangles.

No text: Do not generate readable words, letters, numbers, fake UI text, placeholder text, lorem ipsum, barcode numbers, or pseudo-Chinese. Leave clean blank text slots and quiet paper fields for runtime Godot text.

Style details: Use large simplified low-poly planes and color-value blocks to create texture, not heavy grunge. Keep shapes broad and graphic. Use slightly hand-drawn imperfect cut-paper edges only on outer silhouettes and stickers. The central world map should use fewer larger faceted land planes, not a dense triangulated mesh. Maintain clean negative space inside runtime text rectangles, but keep visible low-poly flat color blocks and large value planes in the surrounding component bodies. The selected North America region should use low-chroma moss olive, close to `#606548`, with darker `#5B5E3E` and light `#807E50` accents, not saturated yellow-green.

Required layout:

- Left: four orthogonal region cards with blank title/meta strips and small image windows.
- Center: large orthogonal dark navy map board with faceted gray world landmasses; selected North America in muted olive; runtime pin and selected halo space left unbaked.
- Right: orthogonal dossier sheet, blank title zone, blank risk stamp shell, orthogonal image frame, three horizontal CTA/ticket plates with blank label slots and icon wells.
- Bottom: three orthogonal receipt/status cards with blank title/value slots.
- Lower right: sticker/icon atlas area with globe, eye, check, warning, and hand icons as fixed decorative stickers.

Avoid: tilted functional panels, slanted CTA plates, skewed photo frames, diagonal text fields, perspective paper used as content, baked readable text, fake labels, route lines baked across the map, dense triangulation mesh, small holes, barcode clutter, many tiny UI marks, photographic paper grain, dirty archive speckles, old newspaper, parchment, grunge, cold legacy v6g runtime look, glass SaaS panels, cyberpunk holograms.
Also avoid: sterile flat UI cards, blank software rectangles, component shells with no low-poly color-value blocks, wrinkle or crease lines across text slots, high-contrast diagonal folded-corner or torn-paper marks inside functional cards / CTA plates / bottom receipts / dossier text bodies, map landmasses covered by fine triangular webbing, and any generation that fixes orthogonality by erasing the benchmark's broad polygonal paper/color-block language.

## Acceptance

Reject the generated image if any of these happen:

- Any functional component is visibly tilted.
- Any content-bearing panel is visibly tilted.
- Any CTA or ticket label slot is diagonal or trapezoid.
- The right dossier front face leans or has perspective.
- Text-like marks appear in content slots.
- The selected region becomes bright yellow-green.
- The image drifts darker than v0.51 or becomes old archive / muddy paper.
- Fine decorative marks cover areas intended for runtime text.
- The central world map reads as dense triangulation/GIS texture instead of broad low-poly cut-paper landmasses.
- Left cards, right dossier, CTA plates, or bottom receipts lose their broad low-poly color-value blocks and become flat empty rectangles.
- Geometry passes but the benchmark style DNA is erased by over-cleaning.
- Any right-side dossier, CTA stack, or bottom receipt face is visibly slanted after generation; geometry failure cannot be offset by better color blocks.
- Any bottom receipt, CTA plate, or text-bearing paper body has a bright diagonal fold, crease, wrinkle, torn-paper patch, or folded-corner mark.
- Any QA overlay uses an ideal horizontal box that does not hug the actual generated edge; the actual art edge is the source of truth.

## Required QA Crops

After generation, capture and inspect:

- left selected card
- central selected landmass
- right dossier header / media / CTA stack
- bottom receipt cards
- sticker atlas area

The pass is not accepted until the crops confirm square-on functional faces by tracing the actual visible generated edges, not by drawing ideal orthogonal boxes nearby.
The pass is also not accepted until the same crops confirm large low-poly flat component color blocks, broad color-value planes, no crease/wrinkle/fold/tear marks in text slots or functional paper bodies, and no dense triangulation drift.
