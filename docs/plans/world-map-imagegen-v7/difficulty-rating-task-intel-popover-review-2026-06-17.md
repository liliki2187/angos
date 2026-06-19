# World Map v7 A77 Filled-State Review

> Screenshot: `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/03-world-map-v7-difficulty-rating-task-intel-popover.png`  
> Status: target mock accepted for direction review, not a production asset.

## What This Mock Proves

- The left region index can carry region-level `难度` and `推荐` without losing selection / lock readability.
- Removing `目标 / 限时 / 线索 / 深链` from the left cards makes the card role clearer: it is a region-choice card, not a task summary card.
- The right selected-region dossier can repeat `难度 / 推荐` near the title without breaking the region image / dossier hierarchy.
- A cyan `任务情报 · N` ticket can work as a secondary control while the main CTA remains `进入选定地区`.
- A read-only task preview popover can provide enough task-pool context without turning the world map into a task board.
- The large right body paper must stay as region prose only; task summaries belong to the task-intel ticket / popover, not the body sections.

## Production Implications

- Add or reserve a no-text `wm_task_intel_popover_v7` component with anchor / hit rects.
- Left region card atlas must expose content rects for title, availability, difficulty, recommendation, and one short reason / lock gap.
- Right dossier base must expose content rects for title, difficulty badge, recommendation badge, red / state ticket, task-intel label, task-intel count, region body sections, and footer.
- Godot / HTML dynamic layer owns all Chinese text, numbers, stars / marks, task preview rows, hover / open / disabled states, and click behavior.

## Risks / Corrections Before Component Production

- The generated screenshot still contains some target-mock text drift and should not be used as a crop source.
- The top title / ornamental labels are not final truth; production should follow `functional-layout-contract.md`.
- The task intel popover must remain visually secondary and read-only. If it gains row selection, dispatch buttons, staff, dice, or success-rate displays, it violates the world-map page contract.
- The right-side image and paper texture are useful as style direction, but the production split must still be no-text components plus dynamic runtime text.

## Acceptance Gate

Before v7 component production, a new no-text artboard / component sheet must pass:

- no baked Chinese, numbers, region names, task names, countdowns, button labels, or task preview text;
- left-card safe zones match difficulty / recommendation fields, not task counters;
- `任务情报 · N` ticket sits directly below the red / state ticket and has clear hit rects plus open / hover / disabled states;
- right body paper contains only region prose fields, not task counters or task preview rows;
- map pins, right dossier, primary CTA, and ticker remain driven by `selected_region_id`;
- safe-zone overlay crops include left cards, right title, task-intel ticket, open popover, CTA, and bottom ticker.

## A79 Supersession

The screenshot reviewed here remains useful for A77's main idea, but its right-dossier task placement must be corrected before the next target mock:

- the large right body paper must contain only region prose;
- the task-intel button must sit below the red / state ticket;
- the button face must include the count, preferably `任务情报 · N`;
- the popover stays read-only and concrete task selection stays in the downstream region task board.

Use `right-prose-task-count-button-prompt.md` for the next Image 2 filled-state target.
