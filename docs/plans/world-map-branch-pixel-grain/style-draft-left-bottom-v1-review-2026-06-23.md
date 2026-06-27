# World Map B7 Left-Bottom Schedule Style Draft v1 Review

Date: 2026-06-23

## File

- Style draft: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/30-b7-left-bottom-advance-right-dossier-style-draft-v1.png`
- Structural source: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/29-b7-advance-day-left-bottom-right-dossier-structure-v3-clean.png`
- Visual benchmark: B7 strict color / pixel-grain reference from the same experiment folder.

## Intended Stage

`filled-state style draft candidate`

This is a visual style draft for discussion. It is not a production benchmark, not a no-text asset master, and not a component-splitting source.

## Layout Verdict

- Left-bottom `推进一天` is now a separate global schedule dock, not a region card.
- Right dossier extends downward into the former lower-right machine area and gains a larger prose body.
- The former lower-right machine / `>>` next-step affordance is removed.
- Right dossier keeps `进入选定地区` as the only primary CTA.
- Bottom receipts remain secondary world-detail entrances.

## Pixel / Material Verdict

Conditional pass for discussion:

- Pixel material uses medium print grain, small square clusters, halftone patches, red/cyan misregistration, and crisp paper edges.
- It does not slide into 8-bit / FC / voxel / retro-pixel game style.
- It does not slide into high-definition photographic noise.
- It remains close to the B7 reference's clean modern ivory paper and deep navy editorial board.

Risk:

- Some microtext remains image-generated and should be treated as visual placeholder, not final UI text.
- The style draft still bakes visible text and cannot be used as runtime background.

## Quick Color Spot Check

This is a lightweight mask check, not a full Color Contract Gate.

| Token | Reference median RGB | Candidate median RGB | Note |
| --- | --- | --- | --- |
| dark_navy | `(10, 24, 39)` | `(6, 21, 35)` | slightly colder / darker, acceptable for draft |
| ivory_paper | `(222, 210, 197)` | `(222, 210, 196)` | very close |
| alert_red | `(182, 61, 38)` | `(180, 49, 27)` | more saturated red-orange, still in family |
| signal_cyan | `(95, 154, 172)` | `(83, 146, 166)` | slightly darker, still restrained |

Before any production benchmark claim, rerun the formal `docs/onboarding/imagegen-color-contract-gate.md` workflow with fixed ROI sampling.

## Next Step

If accepted by the user, revise the B7 image-generation brief around:

1. left-bottom global schedule dock;
2. extended right dossier;
3. no lower-right machine function;
4. medium pixel-print grain;
5. dynamic UI text still separated from future production assets.
