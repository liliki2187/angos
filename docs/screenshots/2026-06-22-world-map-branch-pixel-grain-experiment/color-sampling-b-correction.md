# World Map Pixel Grain Experiment · Color Sampling

> Date: 2026-06-22  
> Purpose: Quantify why Variant B felt too yellow and the aborted B2 correction became too white.  
> Status: Sampling reference for the branch experiment only; not a production palette.

## Files

- Source branch reference: `00-source-branch-style.png`
- Variant B: `02-variant-b-medium-angus-pixel-halftone.png`
- Failed B2 boundary: `04-failed-b2-too-white.png`
- B3 color-locked correction: `05-variant-b3-color-locked.png`
- Source / B / B3 comparison: `06-compare-source-b-b3-color-lock.png`
- B4 AI regenerated with color contract: `07-variant-b4-ai-regenerated-color-contract.png`
- Source / B3 / B4 comparison: `08-compare-source-b3-b4-ai-regeneration.png`
- B5 local polish: `09-variant-b5-local-polish-accent-paper-noise.png`
- B4 / B5 comparison: `10-compare-b4-b5-local-polish.png`
- User comparison reference for strict color gate: `11-b6-reference-user-comparison.png`
- User comparison B5 input: `12-b6-before-b5-user-comparison.png`
- B6 strict color attempt: `13-variant-b6-strict-color-match.png`
- B7 strict color pass: `15-variant-b7-strict-color-match-pass.png`
- Strict color contract: `color-contract-v1-b7-strict-pass.md`

## Sampled Tokens

Samples are median sRGB values from fixed regions on the original 1672x941 images. They are used as a guardrail before any further color prompt.

| Image | Token | Hex | RGB |
| --- | --- | --- | --- |
| source | paper_safe | `#D8CCC0` | 216, 204, 192 |
| source | left_card_paper | `#DED4C6` | 222, 212, 198 |
| source | map_land_light | `#D1C4B3` | 209, 196, 179 |
| source | navy_board | `#0B1B2B` | 11, 27, 43 |
| source | red_orange | `#B74029` | 183, 64, 41 |
| source | signal_cyan | `#588295` | 88, 130, 149 |
| source | ink_dark | `#0B1928` | 11, 25, 40 |
| B | paper_safe | `#E0D1BE` | 224, 209, 190 |
| B | left_card_paper | `#E3D4C0` | 227, 212, 192 |
| B | map_land_light | `#DBC9B1` | 219, 201, 177 |
| B | navy_board | `#061929` | 6, 25, 41 |
| B | red_orange | `#AB3722` | 171, 55, 34 |
| B | signal_cyan | `#488899` | 72, 136, 153 |
| B | ink_dark | `#061726` | 6, 23, 38 |
| B2 failed | paper_safe | `#DFDEDE` | 223, 222, 222 |
| B2 failed | left_card_paper | `#E4E4E3` | 228, 228, 227 |
| B2 failed | map_land_light | `#D8D6D3` | 216, 214, 211 |
| B2 failed | navy_board | `#021323` | 2, 19, 35 |
| B2 failed | red_orange | `#B32A1B` | 179, 42, 27 |
| B2 failed | signal_cyan | `#3E7F9E` | 62, 127, 158 |
| B2 failed | ink_dark | `#02101F` | 2, 16, 31 |
| B3 locked | paper_safe | `#D8CEC1` | 216, 206, 193 |
| B3 locked | left_card_paper | `#DBD1C3` | 219, 209, 195 |
| B3 locked | map_land_light | `#D3C6B4` | 211, 198, 180 |
| B3 locked | navy_board | `#0B1B2B` | 11, 27, 43 |
| B3 locked | red_orange | `#B74029` | 183, 64, 41 |
| B3 locked | signal_cyan | `#588295` | 88, 130, 149 |
| B3 locked | ink_dark | `#0B1928` | 11, 25, 40 |
| B4 AI regen | paper_safe | `#DCCEBE` | 220, 206, 190 |
| B4 AI regen | left_card_paper | `#DCCDBD` | 220, 205, 189 |
| B4 AI regen | map_land_light | `#D0C0AC` | 208, 192, 172 |
| B4 AI regen | navy_board | `#051624` | 5, 22, 36 |
| B4 AI regen | red_orange | `#A8351E` | 168, 53, 30 |
| B4 AI regen | signal_cyan | `#41879A` | 65, 135, 154 |
| B4 AI regen | ink_dark | `#041420` | 4, 20, 32 |
| B5 local polish | paper_safe | `#DCCDBD` | 220, 205, 189 |
| B5 local polish | left_card_paper | `#DCCDBD` | 220, 205, 189 |
| B5 local polish | map_land_light | `#D0C0AC` | 208, 192, 172 |
| B5 local polish | navy_board | `#051624` | 5, 22, 36 |
| B5 local polish | red_orange | `#AE3A23` | 174, 58, 35 |
| B5 local polish | signal_cyan | `#498598` | 73, 133, 152 |
| B5 local polish | ink_dark | `#041420` | 4, 20, 32 |

## Readout

- Variant B shifted the paper and land tokens toward a lighter yellow-beige range compared with the source, especially `paper_safe` and `map_land_light`.
- Failed B2 removed the yellow cast too aggressively and collapsed paper / land into near-neutral gray-white, losing the source image's paper thickness.
- Future correction should target the source token range directly, not average B and B2.
- B3 is a deterministic color-locked correction made from Variant B, not a fresh AI generation. It preserves B's medium pixel / halftone grain while using the source branch image as the color contract.
- B3 pulls the major contract tokens back near the source: `paper_safe` lands at `#D8CEC1`, `map_land_light` at `#D3C6B4`, and `navy_board` at `#0B1B2B`. It should be treated as a color reference candidate for the next AI generation pass, not as a production style benchmark yet.
- B4 is the first AI regeneration after B3. It passes the broad color guardrail and does not repeat B's yellow shift or B2's gray-white wash. However, `red_orange` and `signal_cyan` are darker than the target, and the right dossier paper still needs art-direction review for old-file / paper-dirt risk.
- B5 is a local polish pass on top of B4, not a new AI redraw. It keeps paper, map, navy, and ink essentially unchanged while pulling the signal colors closer to contract: `red_orange` improves from `#A8351E` to `#AE3A23`, and `signal_cyan` from `#41879A` to `#498598`. It also lightly reduces fine paper fiber noise on the right dossier.
- Follow-up user comparison shows B5 still has a visible color difference from the source: it is darker overall, with heavier navy, lower paper luminance, and darker red / cyan accents. B5 is therefore reclassified as a broad-guardrail false pass / color mismatch case, not a color-approved branch candidate.
- B7 is the first correction to pass the strict `Color Contract Gate`: all tracked tokens satisfy the DeltaE00 and dL thresholds, and global mean luminance / paper ratio / dark ratio are inside the accepted range. See `color-contract-v1-b7-strict-pass.md`.

## Next Prompt Guardrail

Before generating a new correction:

- Lock `paper_safe` near `#D8CCC0`, `left_card_paper` near `#DED4C6`, and `map_land_light` near `#D1C4B3`.
- Keep `navy_board` near `#0B1B2B`.
- Treat B as the yellow upper-bound failure and B2 as the white upper-bound failure.
- Adjust only palette retention, local contrast, and organized pixel / halftone placement; do not globally retone the image.
- Use B3 as the color-locked reference when asking a model to regenerate details, and explicitly forbid moving toward B's yellow paper or B2's gray-white paper.
- After B4-style generations, resample before any qualitative review. Color pass alone is not enough to upgrade a candidate: pixel / halftone structure and paper nostalgia risk still require `@像素艺术` review.
- Do not use B5 as color-approved. Treat it as a failure boundary for over-darkening and muted red / cyan accents. The next correction must follow `docs/onboarding/imagegen-color-contract-gate.md` and create a strict `Color Contract v1` before producing B6.
