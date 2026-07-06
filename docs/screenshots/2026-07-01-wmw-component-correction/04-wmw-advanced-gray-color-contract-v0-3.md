# WMW Advanced Gray Color Contract v0.3

> Date: 2026-07-01
> Scope: Clean low-poly weekly branch component correction. This contract responds to the feedback: "original has a sophisticated gray, but not earthy."

## Observed Problem

The current generated/world-map direction is close in structure, but the color relationship is still off:

- The dark board/base is too saturated blue in some drafts, so it reads like a terminal/naval UI instead of benchmark gray-navy editorial board.
- Paper and blank slots drift toward yellow-brown old archive paper, or become too pale in other drafts.
- Olive/mustard/rust accents drift toward muddy earth/craft-ticket colors.
- Teal can become either too blue-saturated or too gray-dead; benchmark teal is muted but still green-blue.

## Sampled Reference Tokens

Hand-sampled medians from the original benchmark boards:

| Token | Sample | H | S | L | Note |
| --- | --- | ---: | ---: | ---: | --- |
| benchmark_dark_board | `#16191C` | 210 | 0.120 | 0.098 | charcoal navy gray, not saturated blue |
| benchmark_pinboard_gray | `#686553` | 51 | 0.112 | 0.367 | warm gray-green board, low saturation |
| benchmark_paper_mid | `#B19E81` | 36 | 0.235 | 0.600 | warm gray beige, not chalk white |
| benchmark_olive_mid | `#616834` | 68 | 0.333 | 0.306 | muted olive, not khaki brown |
| benchmark_olive_light | `#7E8A47` | 71 | 0.321 | 0.410 | selected olive highlight |
| benchmark_blue_gray | `#445967` | 204 | 0.205 | 0.335 | muted blue-gray teal |
| benchmark_blue_dark | `#26384F` | 214 | 0.350 | 0.229 | deep cool blue accent |
| benchmark_rust | `#816240` | 31 | 0.337 | 0.378 | low-saturation rust/brown |

## Correction Targets

For the next component sheet:

- `dark_board`: target `#151A1D` to `#1A2022`; saturation low. Avoid `#0B1C2C` if it reads too blue.
- `paper_mid`: target `#AA9B84` to `#B8AA92`; keep warm gray beige. Avoid pale cream and old yellow-brown.
- `paper_shadow`: target `#8E8776` to `#9D927D`; low saturation.
- `olive`: target `#5F6938` to `#748046`; keep green-gray olive, not yellow-brown khaki.
- `teal_blue`: target `#344B52` to `#4A5F68`; muted blue-green gray, not bright cyan or dead gray.
- `rust`: target `#7A5138` to `#8A6042`; low-saturation rust, not red-orange and not dark blood red.
- `neutral_gray`: target `#5D5F59` to `#6B695E`; warm/cool balanced gray, not craft cardboard.

## Prompt Delta

Use phrase: "sophisticated muted gray palette, gray-navy editorial board, warm gray-beige paper, olive-gray green, blue-gray teal, low-saturation rust; preserve color separations but reduce earthiness."

Avoid phrase/visual outcome: "yellowed archive paper, craft cardboard, muddy khaki, sepia old file, saturated blue terminal, orange red ticket, chalk white paper."

## Candidate Notes

### v0.3

Path: `docs/screenshots/2026-07-01-wmw-component-correction/05-wmw-component-correction-sheet-v0-3-advanced-gray.png`

- Improved the gray relationship compared with v0.2.
- Residual issue: top paper highlight still too pale/cream (`#CDB9A3`-like), warning/rust still too saturated and earthy.

### v0.4

Path: `docs/screenshots/2026-07-01-wmw-component-correction/06-wmw-component-correction-sheet-v0-4-strict-advanced-gray.png`

- Closer hue discipline: paper and background moved toward benchmark gray.
- Residual issue: pushed too far into old-paper/archive feeling; central dossier paper became darker and dirtier than the benchmark should be.

### v0.5

Path: `docs/screenshots/2026-07-01-wmw-component-correction/07-wmw-component-correction-sheet-v0-5-balanced-advanced-gray.png`

- Current best direction for "advanced gray but not earthy": keeps v0.4's muted hue relationship while restoring some of v0.3's cleaner modern finish.
- Residual issue: warning ochre and rust still sample high in saturation; paper highlight still needs testing in the actual world-map single-state layout.
- Next prompt should not globally retone the sheet. Only adjust warning/rust saturation and paper highlight if the user still reads it as earthy.
