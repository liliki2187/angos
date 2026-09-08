# Clean Low-Poly Weekly Paper Material Contract

> Status: branch-level material contract for the clean low-poly weekly direction. It is not the global Angus art truth unless the branch is later promoted.
> Created: 2026-07-01

## Purpose

The paper material in this branch must stop being re-invented by each image generation pass. The target is the benchmark paper: sophisticated muted gray-beige, clean modern weekly paper, broad low-poly value planes, and subtle print tooth. It is not cream form paper, yellowed archive paper, craft cardboard, or dirty old-file paper.

This contract exists so future world map, region screen, dispatch screen, and component atlas work can reuse one paper material definition instead of re-prompting from vague adjectives.

## Source Truth

Primary benchmark boards:

- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`

Current material truth board:

- `docs/screenshots/2026-07-01-wmw-component-correction/13-wmw-paper-material-truth-board-v0-3.png`
- `docs/screenshots/2026-07-01-wmw-component-correction/14-wmw-paper-material-truth-samples-v0-3.json`
- `docs/screenshots/2026-07-01-wmw-component-correction/paper-material-truth-crops-v0-3/`

Current clean material atlas for tests:

- `docs/screenshots/2026-07-01-wmw-component-correction/31-wmw-clean-paper-material-atlas-v3-recommended.png`
- `docs/screenshots/2026-07-01-wmw-component-correction/32-wmw-clean-paper-material-atlas-v3-manifest.json`
- `docs/screenshots/2026-07-01-wmw-component-correction/paper-material-atlas-clean-v3/`

Use the material truth board as the evidence source and the clean material atlas as the default test fill. The atlas is a branch-level test base, not final production art.

## Paper Token Family

Use these tokens as a starting contract. They are sampled from selected benchmark crops and should be refined only by replacing or adding benchmark crops, not by averaging failed generations.

| Token | Current Sample | Role |
| --- | --- | --- |
| `warm_paper` | `#B7A488` | Main warm gray-beige paper. |
| `case_paper` | `#967E5E` | Darker case-file paper family. |
| `ivory_edge` | `#C0B9B3` | Light paper/photo/sticker edge. |
| `gray_board` | `#686554` | Low-saturation gray-green backing board, not writable paper. |
| `note_paper` | `#B3A456` | Muted yellow note paper, not neon or cardboard. |
| `dark_board` | `#16191C` | Charcoal navy-gray background. |

## Layer Model

Every paper component should be thought of as five separate layers:

1. **Base paper color**: warm gray-beige, sampled from the token family.
2. **Flat low-poly value planes**: broad value patches, not folds or stains.
3. **Subtle print tooth**: fine, low-contrast surface grain.
4. **Paper edge / sticker rim**: separated from the writable face.
5. **Cast shadow / backing page**: separated from the paper face and content slot.

The writable paper face must stay calm. Depth should come from edge, shadow, backing pages, clips, tabs, and surrounding objects, not from grime inside the content area.

## Production Method

For future UI work, use this order:

1. **Lock the paper token first**  
   Declare which token a component uses: `warm_paper`, `case_paper`, `ivory_edge`, `gray_board`, or `note_paper`.

2. **Generate shape separately from material when possible**  
   Image generation may explore card shape, sticker geometry, icon style, low-poly thumbnails, and component composition, but it should not be trusted to invent the final paper color and texture.

3. **Apply or normalize paper material after generation**  
   For production candidates, prefer one of:
   - mask the paper face and apply a benchmark-derived texture tile / atlas;
   - Lab color-transfer the paper face toward the selected token crop;
   - use a component atlas whose paper faces are already built from the benchmark crops.

4. **Keep colored accents separate**  
   Do not globally retone the whole image. Paper correction must not wash out olive, teal, rust, icon ink, or dark board tokens.

5. **Run paper QA before style review**  
   If the paper face fails the material gate, do not continue to full-screen style review, text fitting, atlas slicing, or Godot integration.

6. **Prefer role-based atlas fill over prompt-only regeneration**  
   A generated image can propose component silhouette, composition, and broad mood, but exact paper material must be locked by role: main sheet, case body, input slot, receipt card, photo edge, sticker edge, backing board. Do not ask an image model to re-invent all paper faces in one prompt.

## Paper QA Gate

Each future candidate that contains paper UI must check:

- **Median paper color**: close to the declared token, not sampled from a failed generation.
- **Highlight ceiling**: no dominant cream / chalk paper above the token family unless it is a narrow paper edge.
- **Archive drift**: reject yellow-brown, sepia, old-file stains, or cardboard color.
- **Texture type**: accept broad flat low-poly value blocks and subtle print tooth; reject cloud stains, dirt blooms, wrinkles, folds, tears, scratches, and old-paper grime.
- **Content slot calmness**: text slots may have low-contrast value blocks, but no high-contrast marks crossing future text.
- **Layer separation**: edge / rim / shadow / clip can be expressive; writable face must remain clean.

The current valid method QA is:

- `docs/screenshots/2026-07-01-wmw-component-correction/23-wmw-paper-normalization-v0-6-before-after-qa-valid.png`
- `docs/screenshots/2026-07-01-wmw-component-correction/24-wmw-paper-normalization-v0-6-metrics-valid.json`

It shows that sampled mask/token correction can pull key writable paper slots toward `warm_paper`, but also that a single global `warm_paper` pass can darken or flatten some receipt cards. Therefore the production method must use a role-based paper atlas rather than one global paper recolor.

## Prompt Requirements

When image generation is used, prompts must include a paper material clause like:

```text
Paper material must match the attached WMW paper material truth tokens: warm gray-beige paper, broad flat low-poly value planes, subtle print tooth, clean writable face, separate ivory edge and shadow. Do not invent new cream, yellowed archive, dirty old-file, cardboard, or sepia paper.
```

Negative prompt must include:

```text
no cream form paper, no yellowed archive paper, no old-file grime, no cloud stains, no wrinkles, no folds, no tears, no paper damage across text slots, no global retone
```

## Current Decision

The v0.5 component sheet remains a color direction candidate, not a material truth. Its paper still drifts in highlight and saturation. The material truth must come from the benchmark crop board, then be applied to future generated components and UI screens.

As of 2026-07-01, `31-wmw-clean-paper-material-atlas-v3-recommended.png` is the default material base for the next world-map paper replacement test. `29-wmw-clean-paper-material-atlas-v2.png` remains a strict color calibration fallback, but it is visually too flat to be the preferred style base. The earlier prompt-only regeneration attempts are recorded as process failures: they changed scene/content instead of preserving component layout and cannot be used for exact material matching.

## World Map Application Test Log

As of 2026-07-02, the current world-map branch test should use:

- material-locked base candidate: `docs/screenshots/2026-06-24-world-map-benchmark-landing/140-world-map-wmw-paper-atlas-v3-refill-v0-66-info-gray.png`
- material mask QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/141-world-map-wmw-paper-atlas-v3-refill-mask-qa-v0-66.png`
- material metrics: `docs/screenshots/2026-06-24-world-map-benchmark-landing/142-world-map-wmw-paper-atlas-v3-refill-metrics-v0-66.json`
- rejected real text fill experiment: `docs/screenshots/2026-06-24-world-map-benchmark-landing/152-world-map-wmw-real-text-fill-v0-69-symbol-fixed.png`
- real text fill crops: `docs/screenshots/2026-06-24-world-map-benchmark-landing/153-world-map-wmw-real-text-fill-crops-v0-69.png`
- real text fill manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/155-world-map-wmw-real-text-fill-manifest-v0-69.json`
- rejected text-fit correction experiment: `docs/screenshots/2026-06-24-world-map-benchmark-landing/160-world-map-wmw-real-text-fill-v0-71-caption-safe.png`
- rejected text-fit crops: `docs/screenshots/2026-06-24-world-map-benchmark-landing/161-world-map-wmw-real-text-fill-crops-v0-71.png`
- rejected glyph QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/162-world-map-wmw-real-text-fill-glyph-qa-v0-71.png`

These files are **branch test outputs**, not production benchmarks. `140-world-map-wmw-paper-atlas-v3-refill-v0-66-info-gray.png` may be used as the current material-locked base for further text tests. `152-world-map-wmw-real-text-fill-v0-69-symbol-fixed.png` is now a rejected text-fit experiment: it fixed text encoding, but failed text/interface fusion.

Important notes from this pass:

- Do not regenerate the whole screen to fix paper color. Start from the same no-text world-map source and apply role-based paper masks.
- Do not globally recolor the image. Preserve map, thumbnail art, colored frames, icon ink, stickers, and dark board.
- Treat right-side photo caption bars as `info_gray`, not paper. The earlier cream-looking strip was a placeholder/info bar problem, not a reason to darken the whole dossier sheet.
- Keep the green CTA as the only primary action. Blue is secondary information, and red is warning/deadline state.
- Chinese runtime text must be generated through a UTF-8-safe path. `144-world-map-wmw-real-text-fill-v0-67.png` and `148-world-map-wmw-real-text-fill-v0-68-cn-fixed.png` are not review candidates because the PowerShell pipe corrupted some dynamic text/symbols.
- Functional text boxes remain orthogonal. Any future image generation pass that tilts title fields, CTA labels, status tickets, or bottom receipts fails before color/style review.

### 2026-07-02 Text Fill QA Failure: v0.69

`152-world-map-wmw-real-text-fill-v0-69-symbol-fixed.png` failed the real text fit gate. Do not use it as a positive typography reference.

Failure causes:

- Some text used the whole measured slot instead of a stricter inner safe zone. Bottom receipt values and labels became too tall for the ticket and read as crowded.
- Small meta text was too low contrast on warm paper, especially left-card secondary lines. It technically fit but did not read at screenshot scale.
- Header typography and graphic language were not fused. The right dossier title was too heavy and too close to the graphic strip/icon area, while the globe icon remained a thin generic glyph rather than a WMW-style hand-cut sign.
- The previous QA checked text boxes, not actual glyph comfort. Passing a green rectangle overlay is not enough.

Future real-text QA must check:

- Glyph height should stay below roughly 60-65% of the writable field height for small/medium fields, and below roughly 70% only for deliberate title fields.
- Every text field must use an inner safe zone, not the full detected paper patch. Reserve 8-14 px breathing room around labels and 12-18 px around CTA text at this canvas size.
- Small meta text must pass a legibility crop at 100% and at full-screen view. If it needs magnification to read, it fails.
- Decorative or state icons next to titles must be style-compatible: broad, hand-cut, low-poly paper/ink signs, not thin regular toolbar symbols.
- The QA overlay must include both layout boxes and rendered glyph bounding boxes; glyph comfort, contrast, and icon-title pairing must be reviewed together.

`160-world-map-wmw-real-text-fill-v0-71-caption-safe.png` is also rejected. It made small numeric adjustments after v0.69, but did not solve the user's three visible problems: bottom receipt typography still does not sit like a designed ticket, small meta text still lacks comfortable readability and hierarchy, and the right header/title/icon pairing still does not match the benchmark's mature hand-drawn graphic language. The failure was caused by checking local deltas against v0.69 instead of re-evaluating the final crop against the user's stated problem. Future passes must compare against the problem screenshots and the original benchmark feel, not merely against the previous failed iteration.

### 2026-07-02 Text Fit Correction: v0.72-v0.74

`165-world-map-wmw-text-component-rework-v0-72.png` is rejected. It attempted a structural rework, but used a Chinese font path that did not cover the required glyphs. The right header rendered as missing-glyph boxes and therefore failed before visual review.

`170-world-map-wmw-text-component-rework-v0-73.png` is rejected as a partial improvement only. It fixed the missing-glyph issue and moved the bottom receipt values back into the component, but bottom ticket text still felt too small/weak, and the right title/icon relationship was not yet strong enough to count as a final component pattern.

`175-world-map-wmw-text-component-fit-v0-74.png` is the current text-fit candidate for review, still not a production benchmark. It returns to `140-world-map-wmw-paper-atlas-v3-refill-v0-66-info-gray.png` as the material-locked base and only repaints scoped text/icon layers:

- bottom receipt content is now a two-line printed info block instead of a floating oversized value;
- left-card meta text uses stronger ink and supported Chinese fonts without horizontal compression;
- right header uses the WMW sticker-globe language and a shorter title string (`北美禁区`) to avoid title/icon crowding;
- CTA text is fitted by font size only, never by stretching or squeezing glyphs.

Current review files:

- candidate: `docs/screenshots/2026-06-24-world-map-benchmark-landing/175-world-map-wmw-text-component-fit-v0-74.png`
- issue crops: `docs/screenshots/2026-06-24-world-map-benchmark-landing/176-world-map-wmw-text-component-fit-crops-v0-74.png`
- glyph-fit QA: `docs/screenshots/2026-06-24-world-map-benchmark-landing/177-world-map-wmw-text-component-fit-qa-v0-74.png`
- before/after: `docs/screenshots/2026-06-24-world-map-benchmark-landing/178-world-map-wmw-text-component-fit-before-after-v0-74.png`
- manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/179-world-map-wmw-text-component-fit-manifest-v0-74.json`

Do not continue future text work from v0.71, v0.72, or v0.73. Continue from the material-locked v0.66 base plus the scoped v0.74 text layer method. If v0.74 is rejected, record the specific rejected crop and patch only that local text/icon layer.

### 2026-07-02 Text / Frame Fusion Failure

`175-world-map-wmw-text-component-fit-v0-74.png` remains a rejected/unfinished text integration candidate. It fixed several earlier visible problems, but still fails the user's text-frame fusion gate:

- text sizes still feel inconsistent across CTA rows, bottom receipts, left-card meta, and header fields;
- some text technically fits the glyph QA rectangle but visually touches or crowds colored frame edges, icon gutters, right action zones, or paper decoration;
- colored rows still mix different semantics: primary action, secondary information, and red-line warning look too similar as button-like strips;
- the current workflow still patches text after a full component exists, instead of producing the component from a declared text contract.

Root cause: the WMW branch currently has a **paper material contract**, but not yet a **text/component contract**. Future work must not continue by nudging individual glyphs. Before the next image or runtime refill, define each component's:

- `content_rects`: true writable areas after excluding edge, icon, action, fold, tab, paper rim, shadow, sticker, and colored accent zones;
- `no_text_rects`: icon gutter, right action button, paper edge, fold/cut corners, clip/tape, color tag body, barcode/detail garnish, and decorative low-poly accents;
- `hit_rects`: actual clickable area, separate from the text slot;
- typography tokens: `title`, `cta_label`, `meta_label`, `meta_value`, `warning`, `disabled_reason`, `resource_value`;
- state matrix: primary action, secondary/info action, warning non-action, warning action-entry, disabled/locked, selected, hover, pressed.

The next valid deliverable should be a `component_contract_sheet`, not another full-screen world-map revision. It should show CTA row, bottom receipt, left-card meta strip, right header, and HUD text slots with safe-area overlays, longest Chinese strings, and 100% crops. Only after this contract passes review should the world-map full screen be refilled again.

Current component-contract candidate for review:

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/196-world-map-wmw-component-contract-sheet-v3-v0-82.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/197-world-map-wmw-component-contract-sheet-v3-v0-82.json`

This sheet is a process/production contract, not a visual benchmark. If accepted, use it to produce the next clean no-text component atlas and then a filled-state mock. If rejected, revise the contract sheet first; do not return to full-screen image editing.

Note: v0.77 and v0.78 used text-filled crops for some overlays and could make the green safe-area frame look like it should coincide with the visible white text-field border. v0.79 corrects this by using the no-text material base and renaming the green frame to `INNER SAFE`: it marks the inset dynamic-text area inside the white field, not the visible field border itself.

### 2026-07-02 Contract Sheet QA Failure: v0.79

`189-world-map-wmw-component-contract-sheet-v0-79.png` is not sufficient as a final component contract. It clarified the meaning of `INNER SAFE`, but many overlay boxes still do not match the actual visible text plates, frame boundaries, and future rendered text. The failure is methodological: the boxes were estimated on screenshots instead of being derived from measured component geometry.

Future contract sheets must use a stricter three-layer matching method:

1. **Trace the real visible frame first**  
   For each text-bearing component, record `outer_frame_rect`, `visible_text_plate_rect`, `icon_gutter_rect`, `action_gutter_rect`, and decoration / edge / tab exclusion zones. Do not place `INNER SAFE` before the visible white text plate has been traced.

2. **Derive safe areas from frame geometry**  
   `INNER_SAFE` must be calculated from `visible_text_plate_rect` by role-based inset rules, not eyeballed. Example: meta strips need a smaller vertical text band centered on the plate; CTA rows need larger horizontal padding and a fixed action gutter; header titles need a baseline-safe band that avoids badges and status pips.

3. **Validate with real rendered glyphs**  
   Every `INNER_SAFE` area must be paired with a filled-state sample showing the actual longest Chinese string, rendered glyph bounding box, baseline, line height, and minimum distance to the visible plate border. A green frame without glyph proof is not enough.

4. **Separate overlay types clearly**  
   Show at least four different boxes when needed: visible frame / plate boundary, `INNER_SAFE`, `NO_TEXT`, and actual glyph bbox. Do not use one green frame to imply both the visual component boundary and text placement.

5. **Reject if relationship is visually ambiguous**  
   If the reviewer cannot tell whether the green box is describing the white plate, the future text area, or the current text, the contract sheet fails even if the numeric rectangle is plausible.

`194-world-map-wmw-component-contract-sheet-v2-v0-81.png` is the current measured v2 contract candidate. It separates:

- yellow `PLATE`: visible white / light text plate boundary;
- green `INNER`: safe text zone derived from `PLATE`;
- magenta `GLYPH`: actual rendered text bounding box;
- red `NO`: icon / action / edge / decoration no-text zones;
- blue `HIT`: clickable hot zone, which may be larger than text.

The next review should judge whether these relationships are visually convincing. If not, retrace plate geometry first; do not tune typography to compensate for a wrong plate.

### 2026-07-02 Contract Sheet QA Failure: v0.81

`194-world-map-wmw-component-contract-sheet-v2-v0-81.png` is clearer than v0.79 because it separates `PLATE`, `INNER`, `GLYPH`, `NO`, and `HIT`, but it still fails as a final contract candidate. The user correctly identified two problems:

- **Under-filled text plates**: several magenta glyph boxes occupy too little of the available plate. The result is mathematically safe but visually empty, making the text feel pasted into an oversized GUI resource.
- **Optical vertical misalignment**: some glyph boxes are not optically centered in the visible plate, especially left-card meta fields. The glyph bbox can be inside `INNER` while still reading as low or biased because Chinese glyph visual mass, font ascent/descent, and plate center are not being aligned.

Future contract generation must add a fifth gate: **visual occupancy and optical centering**.

Required metrics:

- `glyph_width / inner_width`: target roughly 0.55-0.85 for action labels and 0.45-0.75 for short meta labels. If lower, reduce plate width, split label/value, or increase font/token weight; do not leave a mostly empty field.
- `glyph_height / plate_height`: target roughly 0.42-0.62 for meta/secondary text, 0.48-0.68 for CTA labels, and 0.50-0.70 for key values. Below this reads too small; above this risks crowding.
- `optical_center_delta_y`: rendered glyph visual center should sit within about +/-2 px at source scale for small meta plates and +/-3 px for larger CTA/title plates. Do not rely on raw bbox centering alone.
- `baseline_rule`: align text by font baseline / optical center, not by rectangle center only. Chinese glyphs often need a slight upward optical correction compared with naive bbox centering.
- `plate_efficiency`: if the plate is much wider than the longest planned text, redesign the plate or split it into a small status chip plus value field. Do not use a giant text slot for a short status phrase.

Mature UI reference lesson: document and investigation games such as `Papers, Please`, `The Operator`, and `Strange Horticulture` use large paper/software surfaces, but their readable labels generally sit in intentional fields with stable baselines and visual fill. They do not treat empty field area as harmless if it makes text look like a debug label. WMW should follow this production principle while preserving its low-poly paper material.

The next contract version must show these metrics per component and should prefer resizing / redesigning plates before changing the font. If the plate/text scale relationship is wrong, the GUI resource is wrong, not merely the text.

`196-world-map-wmw-component-contract-sheet-v3-v0-82.png` is the current v3 contract candidate. It adds visual occupancy and optical-center metrics:

- width ratio: rendered glyph width / inner safe width;
- height ratio: rendered glyph height / visible plate height;
- center delta: glyph visual center relative to plate center.

This version intentionally reports failures instead of hiding them. Examples:

- bottom receipt values occupy too little horizontal field width, so the plate should be reduced or split into label/value fields;
- left-card meta strings are too long for the current short plate, so the text should be shortened, split, or the plate redesigned;
- CTA labels need role-specific plate widths rather than one repeated generic button slot.

Do not interpret v0.82 as an approved layout. Interpret it as a diagnostic contract: fix failed rows by resizing plates, splitting fields, changing component roles, or adjusting typography tokens, then produce the next contract revision before returning to full-screen refill.

### 2026-07-02 Contract Sheet QA Failure: text carrier misread

`196-world-map-wmw-component-contract-sheet-v3-v0-82.png` also fails a more basic semantic gate: some measured `PLATE` regions are not the intended text carriers. In the bottom receipt and right header examples, the dark horizontal bars are the actual text fields, while the contract sheet incorrectly treated nearby light paper areas as the text plates. This makes every later metric misleading: a glyph can pass width ratio, height ratio, and center delta while still being placed outside the designed GUI field.

Future contract sheets must run a **text-carrier identification pass** before any geometry, typography, or metric validation:

1. **Name the intended carrier by visual role, not brightness**  
   A text plate may be dark, light, colored, stamped, or inset. Do not assume white / beige paper equals writable text field. If the asset contains dark label bars, they must be considered candidate `text_carrier_rects`.

2. **Separate carrier discovery from text fitting**  
   First mark `text_carrier_rect`, `decorative_bar_rect`, `status_pips_rect`, `icon_rect`, and `action_rect`. Only after this semantic pass can `INNER`, `GLYPH`, occupancy, and baseline metrics be computed.

3. **Reject all metrics on wrong carriers**  
   If text is measured against the wrong plate, every PASS result is invalid. The failure reason should be `wrong text carrier`, not `font size`, `center`, or `plate efficiency`.

4. **Use component intent over image heuristics**  
   For designed GUI resources, carrier intent must be decided from the resource language: inset bars, printed label lanes, field strips, stamps, and ticket lanes. Color/luminance detection is only a helper and cannot override visible affordance.

5. **Add carrier labels to the next sheet**  
   The next contract sheet must explicitly label carriers such as `dark_label_bar`, `value_bar`, `status_stamp`, `signal_pips`, `icon_gutter`, and `action_gutter`, then place text only inside matching carriers.

This issue is more severe than occupancy or optical centering. The next revision must first answer: "Which exact drawn part of the asset was designed to hold this text?" If that answer is wrong, do not proceed to font or spacing review.

### 2026-07-02 Component Carrier Contract Candidate: v0.87

The current component-carrier contract candidate is:

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/215-world-map-wmw-component-carrier-contract-v8-v0-87.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/216-world-map-wmw-component-carrier-contract-v8-v0-87.json`
- 100% review crops:
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/217-contract-v0-87-cta-crop.png`
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/218-contract-v0-87-receipt-crop.png`
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/219-contract-v0-87-left-card-crop.png`
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/220-contract-v0-87-header-crop.png`

This sheet is still a **production contract candidate**, not a visual benchmark and not final UI art. It should be reviewed before the next full-screen world-map text refill.

What v0.87 fixes:

- It replaces the generic `field_lane` with role-specific carriers: `receipt_field_lane`, `header_title_lane`, `header_status_lane`, `button_label_plate`, `card_title_plate`, `grouped_meta_plate`, `stamp_primary_slot`, and `stamp_secondary_slot`.
- It treats `INNER` as a hard boundary. `glyph_inside_inner == true` is required before any field can pass; a 1px overflow is a failure.
- It records functional text carriers as orthogonal: `axis_aligned == true`, `angle_deg == 0`. Tilt is allowed only for `no_text` decoration such as clips, backing pages, shadows, or purely decorative paper layers.
- It fixes the bottom receipt carrier: text belongs to the two dark receipt lanes, not to the white paper face or color status blocks.
- It fixes the right header carrier: the title and red-line status belong to separate dark lanes; the status stamp is a container with two text slots, not one large text rectangle.
- It fixes the left-card semantic mistake found during local review: the lower `可派遣 线报2` field must sit on the actual visible meta plate below the thumbnail, not on the thumbnail image even if a metric pass could be forced.

Additional failure rule from this pass:

> A glyph metric pass is not enough. If the coordinate is not on the real visible text carrier, the result is a false pass and must be rejected as `wrong text carrier`.

Before returning to full-screen refill, use v0.87 as the minimum gate:

1. Identify the carrier role first.
2. Confirm the carrier is on the real visible text-bearing GUI surface.
3. Confirm functional carriers are axis-aligned.
4. Confirm glyph is fully inside `INNER`.
5. Confirm width ratio, height ratio, and optical center pass the role-specific rule.

If the real content cannot pass these gates, change the GUI resource or shorten the UI copy. Do not stretch, squeeze, tilt, or float text to rescue a mismatched asset.

### 2026-07-02 Contract Sheet QA Failure: color-module mismatch

`215-world-map-wmw-component-carrier-contract-v8-v0-87.png` is not approved. It fixed several geometry rules, but still fails visual carrier judgment in local crops:

- The left-card region title (`欧亚灰域`) sits visually low in its pale title plate.
- The right header title (`北美禁区`) sits visually high in its gray title lane.
- The bottom receipt text is still not fully bound to the dark gray field bars; it reads as sitting below / across the intended brown-gray module rather than inside it.

Root cause: v0.87 validated `glyph_inside_inner`, width ratio, height ratio, center delta, and `axis_aligned`, but did **not** validate that the selected carrier rectangle matched the actual colored module area. A glyph can pass the numeric `INNER` test while the whole `INNER` box is offset relative to the visible color block.

New hard rule:

> A text carrier must be segmented from the real visible color module first. Do not accept a manually drawn rectangle unless its top, bottom, left, and right edges visually coincide with the intended colored text-bearing module.

Future contract sheets must add a **module alignment gate** before typography:

1. Record `visible_color_module_rect` separately from `carrier_rect` and `inner_rect`.
2. Compare carrier edges to the real color module edges, not only to the glyph.
3. Reject if the carrier is vertically offset from the module, even if glyph metrics pass.
4. Review each crop at 100% with the raw source below or beside the overlay; do not rely on full-sheet view.
5. For dark or brown-gray field bars, inspect the actual filled color band boundaries. If text appears below, above, or straddling the band, mark `wrong color module`.

This failure supersedes v0.87 as a pass candidate. The next valid revision must start from color-module segmentation, then derive carrier, inner, and glyph from that segmentation.

### 2026-07-02 Component Carrier Contract Candidate: v0.89

The current post-color-module candidate is:

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/223-world-map-wmw-component-carrier-contract-v10-v0-89.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/224-world-map-wmw-component-carrier-contract-v10-v0-89.json`
- 100% review crops:
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/225-contract-v0-89-left-title-crop.png`
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/226-contract-v0-89-header-crop.png`
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/227-contract-v0-89-receipt-crop.png`
  - `docs/screenshots/2026-06-24-world-map-benchmark-landing/228-contract-v0-89-left-card-crop.png`

This version adds `visible_color_module` / `module_match` to each measured text field. It corrects the v0.87/v0.88 visual failures by placing:

- `欧亚灰域` inside the pale region title plate, not low against the lower border;
- `北美禁区带` inside the real gray header title lane, not above the lane;
- `本周行动` and `余 6 天` inside the real dark receipt lanes, not below the brown-gray bars.

The manifest check for v0.89 reports 12 measured fields, 0 failures, with:

- `module_match == true`;
- `glyph_inside_inner == true`;
- `axis_aligned == true`;
- role-specific width / height / optical center checks passing.

The user confirmed on 2026-07-02 that this version is the correct current effect. Treat v0.89 as the accepted component carrier contract for the next WMW world-map refill pass.

This acceptance is scoped: v0.89 proves the local component contract and text/carrier alignment rule. It is not the final full-screen world-map refill, not a final runtime screenshot, and not permission to change the already accepted WMW palette, paper texture, low-poly color blocks, orthogonal functional faces, or no-text/dynamic-text separation. The next pass must preserve the accepted color/material source and use this contract to refill real UI content.
