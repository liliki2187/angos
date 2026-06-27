# World Map Branch Experiment · Color Contract v1

> Date: 2026-06-22  
> Purpose: Strict color gate for correcting the user-visible mismatch between the reference image and B5.  
> Gate source: `docs/onboarding/imagegen-color-contract-gate.md`  
> Status: B7 passes the strict color contract. B5 is reclassified as a broad-guardrail false pass.

## Files

- Reference image fixed by user comparison: `11-b6-reference-user-comparison.png`
- B5 before correction: `12-b6-before-b5-user-comparison.png`
- B6 strict color attempt: `13-variant-b6-strict-color-match.png`
- B6 comparison: `14-compare-reference-b5-b6-strict-color.png`
- B7 strict color pass: `15-variant-b7-strict-color-match-pass.png`
- B7 comparison: `16-compare-reference-b5-b7-strict-color-pass.png`

## Acceptance Thresholds

| Token group | Threshold |
| --- | --- |
| `navy_board`, `alert_red_orange`, `signal_cyan`, `ink_dark` | `DeltaE00 <= 3.0` and `|dL| <= 2.5` |
| `right_paper`, `left_card_paper`, `bottom_card`, `map_light` | `DeltaE00 <= 4.0` and `|dL| <= 2.5` |
| Global mean luminance | reference delta `<= 3.0` |
| Paper ratio / dark ratio | reference delta `<= 0.015` |

## Failure Boundaries

- B: yellow / old-paper boundary.
- B2: gray-white / over-white boundary.
- B5: broad-guardrail false pass; visually darker than reference, with muted red / cyan accents and heavier navy.
- B6: intermediate correction; improved color but failed strict dL on `left_card_paper`, `bottom_card`, and `map_light`.

## B5 vs Reference

| Token | Reference | B5 | DeltaE00 | dL | Verdict |
| --- | --- | --- | ---: | ---: | --- |
| `right_paper` | `#DED3C6` | `#DCCEBE` | 1.85 | -4.58 | Fail: luminance |
| `left_card_paper` | `#E1D6C8` | `#DCCDBD` | 2.61 | -8.29 | Fail: luminance |
| `bottom_card` | `#E1D6C8` | `#DCCDBD` | 2.61 | -8.29 | Fail: luminance |
| `map_light` | `#CFC2B0` | `#D0C0AC` | 1.36 | -1.51 | Pass |
| `navy_board` | `#0B1B2B` | `#051624` | 1.98 | -5.36 | Fail: luminance |
| `alert_red_orange` | `#B63E27` | `#A8351E` | 3.68 | -10.06 | Fail |
| `signal_cyan` | `#5D91A2` | `#42869A` | 5.07 | -14.19 | Fail |
| `ink_dark` | `#0B1927` | `#041420` | 2.16 | -5.57 | Fail: luminance |

Global:

| Image | Mean luminance | Paper ratio | Dark ratio |
| --- | ---: | ---: | ---: |
| Reference | 93.99 | 0.3201 | 0.5212 |
| B5 | 86.53 | 0.3070 | 0.5379 |

## B7 vs Reference

| Token | Reference | B7 | DeltaE00 | dL | Verdict |
| --- | --- | --- | ---: | ---: | --- |
| `right_paper` | `#DED3C6` | `#DFD4C7` | 0.23 | +1.00 | Pass |
| `left_card_paper` | `#E1D6C8` | `#E0D5C7` | 0.23 | -1.00 | Pass |
| `bottom_card` | `#E1D6C8` | `#E0D5C7` | 0.23 | -1.00 | Pass |
| `map_light` | `#CFC2B0` | `#D1C4B2` | 0.50 | +2.00 | Pass |
| `navy_board` | `#0B1B2B` | `#0B1B2A` | 0.67 | -0.07 | Pass |
| `alert_red_orange` | `#B63E27` | `#B53D27` | 0.38 | -0.93 | Pass |
| `signal_cyan` | `#5D91A2` | `#5890A1` | 0.91 | -1.85 | Pass |
| `ink_dark` | `#0B1927` | `#0A1826` | 0.32 | -1.00 | Pass |

Global:

| Image | Mean luminance | Paper ratio | Dark ratio | Verdict |
| --- | ---: | ---: | ---: | --- |
| Reference | 93.99 | 0.3201 | 0.5212 | Baseline |
| B7 | 91.37 | 0.3064 | 0.5310 | Pass |

## Notes

- B7 is a deterministic local color correction, not a new AI generation.
- B7 fixes the B5 over-darkening and muted accent issue without changing composition or pixel / halftone structure.
- Color pass does not automatically mean production benchmark. Pixel / halftone structure, paper nostalgia risk, safe writable areas, and UI assetization still require separate review.
- `@像素艺术`复核结论：B7 可以称为“严格颜色合同通过版本”，但不能称为生产标杆。修色没有明显引入旧纸、过白、偏黄、摄影噪声或颗粒破坏。`paper_ratio` delta 接近阈值，后续应冻结 B7 颜色，不再继续压暗、提亮或增加纸面纹理。
