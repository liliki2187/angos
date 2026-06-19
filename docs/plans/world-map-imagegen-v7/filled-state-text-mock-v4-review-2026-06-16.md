# World Map v7 Filled-State Text Mock v4 Review

> Draft: `docs/screenshots/2026-06-16-world-map-v7-functional-style-draft/05-world-map-v7-filled-state-text-mock-v4.png`  
> Prompt: `docs/plans/world-map-imagegen-v7/filled-state-text-mock-prompt.md`  
> Status: revised target screenshot / visual-density reference only. Not a production asset.

## User Feedback Addressed

The user pointed out that the five macro attributes should not use the same frame grammar as `探索周` / `剩余天数`.

UX diagnosis agreed: the issue is not that macro attributes are in the top strip, but that information with different time scales was using the same frame grammar. `探索周` and `剩余天数` are weekly operation context; the five macro attributes are long-term world state.

## v4 Fixes

- Left top strip keeps `探索周 01` and `剩余 7 天` as ivory weekly clock tickets.
- Right top strip now becomes a separate dark `世界状态` badge / meter rail.
- Macro attributes no longer share the full white paper-ticket frame with the weekly clock.
- The rail keeps all five values readable: `公信 42 / 诡名 18 / 声望 31 / 守序 26 / 狂性 11`.
- The top strip now reads as two semantic groups: weekly clock on the left, long-term world state on the right.

## Remaining Risks

- The generated image still colors `公信 42` red. In runtime, normal macro numbers should share one neutral token; red / cyan should only indicate threshold, change, warning, or other explicit state.
- The `世界状态` label is accepted for clarity in this iteration. `周刊回响` can be explored later if the UI needs more Angus flavor, but should not be introduced until terminology is confirmed.
- This is still a text mock. The final top strip must be rebuilt as no-text assets plus dynamic text / icon layers, not cropped from this screenshot.

## Updated Acceptance For Next Iteration

- A 100% top-strip crop must let a player read: left side is weekly clock, right side is long-term world state.
- Macro attributes must not look like task counters, current-week resources, clickable tabs, or the same paper-ticket fields as week / days.
- All five macro values must remain readable, with `狂性 11` fully visible and not pressed into right-side decoration.
- Macro rail visual weight must stay below the central map, selected-region dossier, and primary CTA.
