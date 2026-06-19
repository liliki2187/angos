# World Map v7 P0/P1 Filled-State Text Mock Review

> Date: 2026-06-17  
> Screenshots:  
> - Ready state: `docs/screenshots/2026-06-17-world-map-v7-p0p1-real-info-style-draft/01-world-map-v7-p0p1-real-info-text-mock.png`  
> - Blocked state: `docs/screenshots/2026-06-17-world-map-v7-p0p1-real-info-style-draft/02-world-map-v7-p0p1-blocked-state-text-mock.png`  
> Status: target screenshot / visual-density reference only. Not a production PNG, not a cut-up source, not a runtime background.

## Pass

- P0 selected-region loop is visible in one static read: the selected North America card, central North America pin, right dossier, CTA, and bottom receipts all point to `北美禁区带`.
- P0 enterability is clearer than v4: the selected card and CTA read as enterable, while locked regions use lower contrast and short blockers.
- P1 region-level summary is restored without showing a task list: the right dossier exposes `目标 / 限时 / 线索 / 深链` as compact counters.
- P1 right-side preview rows now read as region intel instead of UI legend copy.
- Bottom ticker lanes now support world-level receipts: `地区情报`, `任务小结`, `地区预警`.
- The top status strip keeps the week/day paper tickets visually separate from the `世界状态` rail, and the fifth macro attribute is fully visible.
- The blocked companion state demonstrates the P0 locked-region loop: selected locked East Asia card, locked map pin, right blocked dossier, disabled CTA `暂不可进入`, and ticker receipts all point to the same blocker.

## Remaining Risks

- This is still an Image 2 text mock. Exact Chinese glyph quality, line breaks, and typography must be rebuilt by Godot / HTML dynamic text, not copied from the bitmap.
- Both screenshots are still Image 2 text mocks. Exact chip typography, disabled label opacity, and Chinese line breaking must be rebuilt by Godot / HTML dynamic text.
- It demonstrates locked cards visually, but does not prove runtime interaction rules: hover, click selection, locked click ignored, CTA loading, or selected-region context transfer.
- The bottom ticker now has the right roles, but final runtime text should be tested with longest real values so `任务小结` does not crowd the lane.

## Production Implication

At the time of this review, these images were used as the P0/P1 visual target for field capacity, hierarchy, and art/text integration. After A77, use them only as historical evidence for the selected-region / locked-region loop. Component production must follow the current `functional-layout-contract.md`, return to no-text assets, state atlases, `content_rects / no_text_rects / hit_rects`, and a single `worldRegionViewModel`-style data source for left index, map pins, right dossier, CTA, and ticker.

## UX Redundancy Revision - 2026-06-17

Later UX review found that the right dossier body repeated the same task counters already present in the left card / compact task overview / bottom receipts. The revised direction keeps one compact task-overview ticket, but removes the body-level `任务小结`. The right dossier body should instead carry `地区特征`, `本周异变`, `可带回素材`, and optional `地区预警 / 编辑价值`.

The bottom ticker should also move away from a `任务小结` lane. Use low-weight feedback lanes such as `最新记录`, `档案更新`, and `地区预警`, so the ticker reports changes rather than duplicating task metrics.

Updated reference screenshot:

- `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/01-world-map-v7-fusion-b-ux-reduced-redundancy.png`

## A77 Supersession - 2026-06-17

User review restored the older web prototype's useful `难度 / 推荐` decision signal and moved task-pool information out of the left cards. The current v7 target is now:

- left region cards show title, availability, region-level difficulty, recommendation rating, and one short reason / lock gap;
- left region cards do not show `目标 / 限时 / 线索 / 深链`;
- selected-region title area may repeat difficulty / recommendation badges;
- the right cyan `任务情报` ticket opens a read-only popover with 2-3 task preview rows;
- the popover does not include task selection, dispatch, staff, dice, success rate, or full task detail.

The P0/P1 screenshots in this review remain useful as historical evidence for the selected-region loop and blocked-region loop, but they are no longer the current field contract for component production.

Current reference screenshot:

- `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/03-world-map-v7-difficulty-rating-task-intel-popover.png`

## Godot Runtime Follow-Up

Runtime P0/P1 landing screenshots:

- Ready: `docs/screenshots/2026-06-17-world-map-p0p1-godot/01-world-map-p0p1-ready.png`
- Locked: `docs/screenshots/2026-06-17-world-map-p0p1-godot/02-world-map-p0p1-locked.png`

Godot now owns the fixed CTA copy, selected-region state, locked preview, right dossier dynamic sections, and bottom ticker roles. These screenshots validate the interaction/data contract, not final v7 art replacement.
