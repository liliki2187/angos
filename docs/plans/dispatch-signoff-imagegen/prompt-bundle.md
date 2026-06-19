# Dispatch Signoff Imagegen Prompt Bundle

> Date: 2026-06-15
> Scope: Angus dispatch signoff desk style draft for assetized UI production.
> Tool path: built-in `image_gen`.
> Status: v1 / v2 are review and iteration records only. After 2026-06-16 user feedback plus SIA / `@像素艺术` review, v2 must not be used as a production benchmark; next pass is v3 function-first clean ivory pixel-print artboard.

## Output Files

| id | path | role | status |
| --- | --- | --- | --- |
| v1 | `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/01-dispatch-signoff-style-draft-assetized.png` | first pass style draft | useful for structure, rejected as main candidate because it contains an outer dashed frame and more pseudo UI marks |
| v2-source | `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/02-dispatch-signoff-style-draft-cleaner-production-mother.png` | original v2 output | structure reference only; not a production benchmark |
| v2-1920 | `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/02-dispatch-signoff-style-draft-cleaner-production-mother-1920x1080.png` | scaled 16:9 review copy | review image only, 1920x1080 |
| v3b-artboard | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/01-dispatch-signoff-full-style-v3b-artboard-no-runtime-text.png` | function-first clean ivory pixel-print artboard | current split-asset discussion candidate; not final production benchmark |
| v3b-filled | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/02-dispatch-signoff-full-style-v3b-filled-preview.png` | local Chinese-filled interface preview | used to review actual screen readability and decision chain |
| v3b-safe-zone | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/03-dispatch-signoff-full-style-v3b-safe-zone-overlay.png` | safe-zone overlay | draft `content_rects / no_text_rects / hit_rects` guide |
| v3c-component-sheet | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/04-dispatch-signoff-component-sheet-v3c.png` | cohesive component sheet | current proof that function-split assets can preserve v3b style when generated together |
| cta-atlas-v1 | `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-cta-signoff-atlas.png` | transparent CTA atlas, 6 frames | first component asset candidate generated from the v3c component-sheet route |
| review-sheet-base-v1 | `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-review-sheet-base.png` | right review sheet base with empty CTA mount | engineering validation candidate only; bottom cleanup still needs art pass |
| review-sheet-base-v2-art | `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-review-sheet-base-v2-art-pass.png` | generated right review sheet art pass, no baked CTA | promising visual candidate; requires content rect remap before runtime |
| filled-content-preview-v1 | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/19-dispatch-signoff-filled-content-preview-v1.png` | local programmatic filled preview with real Chinese text and existing avatar assets | safe-zone / capacity validation only; not a visual target, production asset, or slicing source |
| filled-content-preview-v1-right | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/20-dispatch-signoff-filled-content-preview-v1-right-crop.png` | 100% right review sheet crop from the local filled preview | safe-zone / field fit check |
| ai-filled-effect-v1 | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/21-dispatch-signoff-ai-filled-effect-v1.png` | AI-redrawn filled-state effect mock with integrated Chinese text, avatars, cards and signoff sheet | current visual target screenshot for review; not a production asset or slicing source |
| ai-filled-effect-v1-left | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/22-dispatch-signoff-ai-filled-effect-v1-left-crop.png` | 100% left task brief crop | visual integration check |
| ai-filled-effect-v1-center | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/23-dispatch-signoff-ai-filled-effect-v1-center-crop.png` | 100% center dispatch tray crop | visual integration check |
| ai-filled-effect-v1-right | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/24-dispatch-signoff-ai-filled-effect-v1-right-crop.png` | 100% right signoff sheet crop | visual integration check |
| ai-operation-hover-v1 | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/25-dispatch-signoff-ai-operation-hover-v1.png` | AI-redrawn operation state: selected 2/3, support selected, candidate hover preview, right-side delta, active CTA | current operation-state target screenshot; not a production asset or slicing source |
| ai-blocked-full-v1 | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/26-dispatch-signoff-ai-blocked-full-v1.png` | AI-redrawn blocked state: selected 3/3, candidate blocked_full, right-side blocking reason, disabled CTA | current blocked-state target screenshot; not a production asset or slicing source |
| ai-operation-hover-v1-center | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/27-dispatch-signoff-ai-operation-hover-center-crop.png` | operation-state center crop | visual integration check |
| ai-operation-hover-v1-right | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/28-dispatch-signoff-ai-operation-hover-right-crop.png` | operation-state right crop | visual integration check |
| ai-blocked-full-v1-center | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/29-dispatch-signoff-ai-blocked-full-center-crop.png` | blocked-state center crop | visual integration check |
| ai-blocked-full-v1-right | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/30-dispatch-signoff-ai-blocked-full-right-crop.png` | blocked-state right crop | visual integration check |
| ai-p0-state-matrix-v1 | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/31-dispatch-signoff-ai-p0-state-matrix-v1.png` | AI-redrawn P0 state matrix: blocked-full screen plus CTA state strip | current P0 signoff-closure target screenshot; not a production asset or slicing source |
| ai-p0-state-matrix-v1-center | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/32-dispatch-signoff-ai-p0-state-matrix-center-crop.png` | P0 center tray crop | visual integration and capacity/remove check |
| ai-p0-state-matrix-v1-right | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/33-dispatch-signoff-ai-p0-state-matrix-right-crop.png` | P0 right review sheet crop | blocking reason and disabled CTA check |
| ai-p0-state-matrix-v1-cta | `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/34-dispatch-signoff-ai-p0-state-matrix-cta-states-crop.png` | P0 CTA state strip crop | state family check |

## Prompt V1

```text
Use case: ui-mockup
Asset type: 1920x1080 desktop 16:9 game UI style frame, production-oriented assetized UI mother draft for future slicing and manifest creation.
Primary request: Create one full-screen Angus dispatch signoff desk style draft that can guide future bitmap asset production and slicing. It must read as an editor-in-chief field dispatch approval desk, not as a generic data dashboard and not as a final baked UI screenshot.

Scene and layout: A modern anomalous weekly magazine editorial signoff desk viewed straight-on or near-orthographic, with a 48px outer safety margin. Use a low-weight top channel strip across the top, a left task dossier sheet zone, a central dice-pool tray zone, and a right approval review paper zone. Approximate layout proportions: left 500px wide, center 856px wide, right 420px wide, visible gutters between zones. The center zone is the visual focus.

Functional object zones:
- Left: a fresh warm off-white task dossier sheet and back-tab object, with large blank rectangular content areas for future dynamic task title, brief, time cost, and special constraint text.
- Center: a dice-pool tray with three stable selected staff ID card slots, a separate support/resource slot, and a grid of candidate staff card frames. Candidate staff cards should visibly reserve space for avatar, name, and preferably a full six-face dice net layout, but with no actual text or numbers.
- Right: a clean approval review sheet with blank content rectangles for summary, special constraint, probability/coverage strip, risk, gap, action scope, failure consequence, blocking reason, and a lower-right stamp-like signoff CTA plate. The CTA plate must look like a physical approval stamp/signoff action entrance, not a generic button.

Style: Angus visual language: deep naval blue editor workbench, flame red-orange approval accents, restrained cyan overprint marks, fresh warm off-white printed paper, modern graphic design, structured halftone blocks, slight red/cyan registration offset, high-definition micro-pixel grain as premium atmosphere material, crisp edges, strong hierarchy, black humor editorial workbench mood.

Production constraints: Every major object must feel separable as a future ds_* asset family: desk base, top strip, task brief sheet, back tab, selected staff slot frames, staff card frames, dice face tiles, sort tabs, support slots, review sheet, coverage strip, risk/status/approval stamps, signoff CTA plate. Use visible object boundaries, stable cut margins, clean gutters, rectangular writable content areas, and no-text zones for clips/folds/stamps/halftone corners. This should look like an assetized UI style sheet / production mother draft, not a fully populated in-game screenshot.

Text constraints: Absolutely no readable Chinese, English, numbers, percentages, names, task titles, fake labels, fake tooltip text, button copy, countdowns, probabilities, or glyph-like pseudo-text anywhere. Leave all future dynamic text areas blank or represented only by clean empty paper/card rectangles. Dice net cells may be empty icon cells or blank face tiles, but must not contain numbers, letters, or symbols.

Avoid: old newspaper, old archive, yellowed sepia paper, tea stains, parchment, warm wooden desk, cozy office lamp, detective corkboard, SaaS dashboard, glassmorphism, web cards, generic rectangular panels, cyber terminal, holographic sci-fi screen, casino terminal, low-res 8-bit pixel art, random photographic noise, baked UI text, fake Chinese characters, fake task cards, fake buttons, fake pins, fake tooltip, large perspective-tilted paper carrying body text or CTA, decorative clips/folds/stamps/halftone crossing writable text areas.
```

## Prompt V2

```text
Use case: ui-mockup
Asset type: 1920x1080 desktop 16:9 game UI production mother draft for asset slicing.
Primary request: Generate a cleaner second-pass Angus dispatch signoff desk style frame. It must be suitable as a production-oriented assetized UI mother draft for future slicing, not a final populated interface screenshot.

Composition: Full-screen near-orthographic editorial workbench with clear separable objects and no outer dashed border. Use a 48px visual safety margin. Layout: top low-weight blank channel strip; left task dossier sheet about 500px wide; center dice-pool tray about 856px wide as the dominant zone; right approval review sheet about 420px wide. Use clean gutters and layered paper/clipboard shadows rather than hard web panels.

Objects to show as blank production components:
- left warm off-white task dossier sheet with large empty orthogonal writable rectangles, back-tab shape, paper clip, folds only outside text zones;
- center dice-pool tray with exactly three selected staff ID-card slots on top, one distinct support/resource slot, sort-tab shapes, and six candidate staff card frames below;
- each candidate staff card has an avatar placeholder rectangle and a clean empty six-face dice-net grid area, with no lines pretending to be names or text;
- right approval review sheet with separate blank rectangles for summary, special constraint, probability/coverage strip, risk, gap, action scope, failure, blocking reason, and a lower-right stamp-like CTA plate;
- separate risk/status/approval stamp shapes, but blank and non-textual.

Style: Angus modern anomalous weekly magazine visual language: deep naval blue editor workbench, fresh warm off-white printed paper that is clean and not aged, flame red-orange approval accents, restrained cyan overprint marks, structured block halftone, subtle red/cyan registration offset, deliberate high-definition 2-4px micro-pixel grain, crisp modern graphic design. Professional game UI art direction, black humor editorial desk mood, not cozy.

Production constraints: All major objects should be separable as future ds_* assets with stable cut boundaries: desk base, top strip, task brief sheet, back tab, selected staff slot frames, staff card frames, dice face tiles, sort tabs, support slot, review sheet, coverage strip, risk/status/approval stamps, signoff CTA plate. Make writable areas blank, clean, near-rectangular, and measurable. Keep clips, folds, stamps, halftone corners, paper edges, and overprint marks outside writable rectangles.

Strict text and symbol constraints: No readable Chinese, no English, no letters, no numbers, no percentages, no names, no task titles, no fake labels, no fake tooltip, no button copy, no countdowns, no probabilities, no pictogram labels, no UI icons in the top strip, no placeholder text lines, no micro-glyphs. Use only blank paper/card rectangles and empty outlined cells. Dice-net cells must be empty boxes, with no pips, numbers, letters, icons, or symbols.

Avoid: old newspaper, old archive, yellowed sepia paper, tea stains, parchment, warm wooden desk, cozy office lamp, detective corkboard, SaaS dashboard, glassmorphism, web cards, generic rectangular panels, cyber terminal, holographic sci-fi screen, casino terminal, low-res 8-bit pixel art, random photographic noise, full-screen dashed border, baked UI text, fake Chinese characters, fake task cards with text, fake buttons with labels, fake pins, fake tooltip, large perspective-tilted paper carrying body text or CTA, decorative elements crossing writable text areas.
```

## Next Prompt Direction

V3 should not be a retouch of v2. Generate a new function-first no-runtime-text artboard from these fixed zones:

- Top: low-weight global status strip for week, days left, region, available staff, and pressure only.
- Left: clean ivory task briefing paper for title, tags, location / time cost, brief, requirements, and failure consequence.
- Center: dark navy dispatch configuration tray; top has three selected staff slots and one support slot, bottom has candidate staff cards. Candidate cards reserve avatar, name, contribution / dice net, and status slots.
- Right: clean ivory signoff review paper for success / coverage rate, effective points vs target, risk, day cost, after-action state, blocking reason, failure consequence, and the red-orange signoff CTA.

V3 positive prompt core:

```text
16:9 desktop game UI artboard, no readable text, no baked UI labels.
Modern supernatural weekly magazine dispatch signoff desk, four clear functional zones:
top minimal status strip, left clean ivory task briefing clipboard, center dark navy assignment tray with staff card slots and support slot, right clean ivory signoff sheet with a large red-orange stamp/approval button.
Angus visual style: bold modern editorial graphic design, deep navy #0F1A2E, vivid red-orange #E84B2C, clean warm ivory paper #F5EDD8 / #F8F2E4.
Printed matter materiality, crisp paper edges, subtle halftone fields, 2-4px pixel grain clusters, slight red-cyan misregistration, crop marks, clean graphic shadows.
Keep large blank orthogonal content rectangles for runtime text, flat readable surfaces, controlled texture outside text zones.
Show the gameplay cause chain visually: selected staff and support feed into right-side success/risk/cost review and final signoff action.
Cool, confident, urgent, black humor, fresh supernatural weekly magazine, not vintage archive.
```

V3 negative prompt must include:

```text
no yellowed old archive paper, no dirty stains, no broken torn paper, no coffee marks,
no dusty old newspaper, no decayed folder, no warm wooden desk, no cozy office,
no photorealistic scratches, no corroded metal, no chipped paint, no random paper noise,
no generic SaaS panels, no mobile game capsule buttons, no neon cyberpunk hologram,
no baked readable text, no fake paragraphs inside content areas.
```

## V3B Result Notes

V3B is the current best direction because it makes the dispatch decision chain visible: selected staff and support connect to the right-side review sheet, then down to the signoff CTA. It also moves the paper closer to clean ivory printed stock and reduces the old archive read.

Do not upgrade V3B directly to production benchmark. Before component generation, remove the remaining fake line bars from staff cards, reduce top-strip icon baking, and keep the paper corners clean rather than torn or dirty. Use `full-style-v3b-review-2026-06-16.md` and the safe-zone overlay as the next prompt / manifest input.

Component prompts after the art review must explicitly add:

```text
no baked text, no fake glyph bars, no placeholder micro text inside content_rects
empty clean content rectangles for runtime Chinese UI text
printed pictogram icon system, stamp-like HUD marks, not SaaS icons, not mobile resource bars
flat graphic stamp press CTA, printed approval plate, no glossy 3D knob, no generic mobile game button
minimal clean paper stacks, no archive scrapbook, no realistic rusty metal, no sepia paper
```

## V3C Component Sheet Notes

V3C exists to prevent the assetization chain from turning into programmatic UI. Use it as the shared visual reference for single-component prompts: paper color, shadow softness, red-orange stamp plates, cyan support slot, blank dice grids, status stamps and pixel-print density should stay close to this sheet.

Important: V3C is not a final atlas. Individual components still need exact sizes, transparent backgrounds, state frames, `content_rects`, `no_text_rects`, and immediate recomposition into the 1920x1080 dispatch screen. If a single generated component does not look like it belongs on the V3C sheet, reject it before Godot integration.

## CTA Atlas V1 Notes

`ds_cta_signoff_atlas` is the first component-level proof from this route. It was generated as a six-frame green-screen source, keyed to alpha, then normalized to the manifest size `1044x92` with `174x92` frames.

Use this prompt pattern for later atlas work:

```text
Generate a single horizontal six-frame atlas strip for <asset_id> on a perfectly flat solid #00ff00 chroma-key background.
Each frame must be isolated, equal-size, no labels, no text, no fake glyph bars.
Match the v3c component sheet: clean ivory paper, deep navy edges, red-orange/cyan print accents, 2-4px pixel clusters, blocky halftone, crisp graphic edges.
Keep all future runtime Chinese text areas blank and low-texture.
```

The CTA atlas has now been recomposed locally with `ds_review_sheet_base`; it still needs Godot state screenshots before it can be called runtime-ready.

## Review Sheet Base V1 Notes

`ds_review_sheet_base` exists because CTA recomposition exposed a P0 asset split bug: the v3b right review sheet baked a large red CTA, while `ds_cta_signoff_atlas` also supplies the real button. The base must therefore be an empty review paper stage, not a button.

Current engineering contract:

```text
component_rect: [1260, 130, 454, 860]
final_size: [454, 860]
cta_mount: [220, 646, 174, 92]
explicit facts: summary, special_constraint, probability, risk, coverage_checks, time_cost, action_scope, blocking_reason, failure
```

Prompt pattern for the next art pass:

```text
Generate / repair only the right-side dispatch review sheet base.
Keep warm clean ivory printed paper, red/cyan overprint, controlled halftone, micro-pixel printed texture, crop marks, layered paper edges and a modern supernatural weekly magazine feel.
Provide a blank lower-right CTA mounting zone as shallow paper deboss / registration plate only.
No filled red button, no knob, no button label, no real text, no fake Chinese, no pseudo text, no glyph bars.
The separate `ds_cta_signoff_atlas` will provide all red-orange button body, label, hover, pressed, disabled, focus and loading states.
Keep `time_cost`, `action_scope`, `blocking_reason` and `failure` as clean runtime text slots outside the CTA mount.
```

Reject if the output contains a red filled CTA base, any readable or fake text, or if the empty mount looks like a generic programmatic panel instead of a printed paper signoff mount.

The 2026-06-16 v2 art pass satisfies the visual direction better than the engineering crop, but its field layout is not the same as v1. Use it as the next visual target only after creating a new safe-zone overlay and re-running content/no-text intersection checks.

## Filled Content Preview V1 Notes

`19-dispatch-signoff-filled-content-preview-v1.png` is a local capacity and safe-zone validation mock. It uses:

- real dispatch text such as `线索调查：纽约市`, `天线井异常回声`, `有效点 11 / 目标 8`, `达标率 57%`, `消耗 2天 · 剩余 1天`;
- existing full-chain demo avatars from `design/prototypes/html/full-chain-demo/Assets/avatars`;
- `ds-review-sheet-base-v2-art-pass.png` plus `ds-cta-signoff-atlas.png`;
- local program-rendered Chinese text to preserve accuracy.

This preview is allowed to bake text and avatars because it is only a filled-state text mock, but it is not the desired visual result. It must not be used as `ds_desk_base`, `ds_review_sheet_base`, staff card art, CTA art, or any runtime texture. Use it to find layout failures, not to judge final polish.

## AI Filled Effect V1 Notes

`21-dispatch-signoff-ai-filled-effect-v1.png` is the current integrated completed-state effect mock. It should be judged like Image 2 in the user feedback: paper, text, avatars, staff cards, right-side review fields and CTA should look generated as one coherent interface rather than labels pasted on an artboard.

Prompt core:

```text
Generate a fully redrawn Angus dispatch signoff interface, not a composited overlay.
Make paper, buttons, avatars, text, icons, status marks and layout visually integrated.
Use Image 2 as the style reference for integrated Chinese UI text, modern pixel-print paper,
deep navy workbench, red-orange CTA, cyan accents, clean ivory paper and coherent UI density.
Use Image 1 as the negative example: avoid pasted labels, misaligned avatar chips,
unintegrated text and crowded debug dice chips.
```

The result improves the visual integration target: Chinese text is printed into paper fields, staff portraits sit inside cards, and the right CTA feels mounted into the signoff sheet. Known limitation: AI-rendered small Chinese and candidate names can still contain near-miss glyphs. Therefore `21-24` are review targets only; production still requires no-text components, state atlas and Godot-rendered exact text / avatars.

## AI Operation / Blocked State Notes

`25-dispatch-signoff-ai-operation-hover-v1.png` and `26-dispatch-signoff-ai-blocked-full-v1.png` were generated after UI Designer and UX review found that a single ready-state mock would miss core operation contracts.

Operation-state prompt intent:

```text
Selected 2/3 staff, one empty slot, selected support item, candidate hover / preview,
right-side delta line showing what changes if the hovered candidate is added,
active signoff CTA, integrated paper/card/button typography.
```

Blocked-state prompt intent:

```text
Selected 3/3 staff, clicked/hovered candidate gets local blocked_full feedback,
right-side signoff sheet explains the blocking reason and required action,
CTA is disabled / blocked but remains in the same component family.
```

Use these two images to guide `ds_selected_slot_atlas`, `ds_staff_card_atlas`, `ds_support_slot_atlas`, `ds_sort_tab_atlas`, `ds_review_sheet_base` content roles and `ds_cta_signoff_atlas` state expansion. Do not cut production assets from them.

## AI P0 State Matrix Notes

`31-dispatch-signoff-ai-p0-state-matrix-v1.png` was generated after the user accepted the P0-first scope. It is not a broader feature mock; it deliberately focuses on:

```text
blocking reason matrix, selected capacity and remove affordance,
CTA default / hover / pressed / loading / disabled / stamped states,
and text/avatar safe-zone readability.
```

Prompt intent:

```text
Show one integrated blocked-full dispatch signoff screen with selected 3/3 staff,
visible remove buttons, a candidate card with local 人数已满 feedback,
right-side review sheet explaining the blocking reason and next action,
a disabled CTA in the same component family,
and a compact bottom strip showing the six core CTA visual states.
Do not add P1/P2 features such as full detail drawers, permanent full dice nets,
temporary stringer store flow, or broad sorting controls.
```

Use `31-34` to guide P0 validation only. Production still requires no-text components, `content_rects / no_text_rects / hit_rects`, `ds_cta_signoff_atlas`, `ds_selected_slot_atlas`, `ds_staff_card_atlas`, and Godot-rendered exact text / avatars. Do not cut assets from the P0 state matrix image.
