# World Map v7 Filled-State Text Mock v2 Review

> Draft: `docs/screenshots/2026-06-16-world-map-v7-functional-style-draft/03-world-map-v7-filled-state-text-mock-v2.png`  
> Prompt: `docs/plans/world-map-imagegen-v7/filled-state-text-mock-prompt.md`  
> Status: revised target screenshot / visual-density reference only. Not a production asset.

## Why v1 Was Rejected

User feedback on the first filled-state mock found four information-contract problems:

- The right dossier did not reserve a stable region-intro space.
- The top strip omitted the full five macro attributes and instead showed weak / wrong fields such as `全球频道`, `素材`, and standalone `声望`.
- The primary CTA used a dynamic region name (`北美禁区带`) inside the button label; the button should use fixed copy such as `进入选定地区`.
- The bottom strip read like an odd functional bar / progress bar instead of a low-weight world-map receipt.

UX / UI diagnosis agreed that the root cause was not visual polish but a broken information contract: the world map layer had started mixing task-layer, dispatch-layer, resource-layer, and dynamic-region copy into a screen that should only choose a region and enter that selected region.

## v2 Fixes

- Top strip now carries week, remaining days, phase, and all five macro slots: `公信 / 诡名 / 声望 / 守序 / 狂性`.
- Right dossier now has a fixed slot label (`选定地区`), region title, and a visible two-line region intro before state and preview rows.
- Primary CTA now uses fixed copy: `进入选定地区`; the selected region name is kept in the dossier title.
- Bottom strip now reads as three low-weight receipts: recent change, region anomaly, and enter hint.
- The six-zone visual structure remains close to the approved v7 direction, so this is a field-contract correction rather than a visual reset.

## Remaining Risks

- Image-generated Chinese remains unreliable. In this draft, some text may still render as near-Chinese or slightly wrong glyphs. Treat all text as density / hierarchy reference only.
- The macro attribute values in the top strip are placeholder values; runtime must render exact names and numbers.
- Region pin, route, selected ring, side tabs, and CTA states must still become runtime layers or component atlases.
- The bottom receipt copy is better, but runtime should keep it low-weight and non-clickable unless a specific ticker interaction is later designed.

## Updated Acceptance For Next Iteration

- A 5-second static screenshot must communicate: selected region, whether it can be entered, main region status, and where to click next.
- The top strip must show all five macro attributes together, not a standalone resource row.
- The right dossier must keep a visible region intro before any state / preview rows.
- The CTA must use fixed copy (`进入选定地区` or equivalent) and must not include dynamic region, task, red-line, or dispatch names.
- The bottom strip must read as world-map receipts, not a function bar, filter bar, task progress bar, or duplicate current-region label.
- Filled-state mocks remain target screenshots only; production assets must still be no-text components plus Godot / HTML dynamic text.
