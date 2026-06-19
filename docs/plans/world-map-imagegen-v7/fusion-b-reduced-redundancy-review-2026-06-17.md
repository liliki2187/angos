# World Map v7 Fusion B Reduced-Redundancy Review

> Date: 2026-06-17  
> Screenshot: `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/01-world-map-v7-fusion-b-ux-reduced-redundancy.png`  
> Status: filled-state visual target / UX information-architecture reference only. Not a production PNG, not a cut-up source, not a runtime background.

## UX Decision

The right selected-region dossier must stop repeating task counters in the main body. The page may keep one compact task-overview ticket for `目标 / 限时 / 线索 / 深链`, but the body should explain the region itself:

- `地区特征`: what kind of region this is.
- `本周异变`: what changed this week.
- `可带回素材`: what kind of editorial material the player can expect.
- `地区预警 / 编辑价值`: why entering matters, or what risk it carries.

## Pass

- The red-boxed redundant body-level `任务小结` is removed.
- The right dossier has more room for region identity, anomaly context, and material value.
- The bottom strip reads more like low-weight feedback lanes (`最新记录 / 档案更新 / 地区预警`) instead of a second task-summary area.
- The compact right-side structure still preserves the benefit of the earlier style draft: region image, status ticket, task overview, dossier body, and CTA are all visible in one column.

## Remaining Risks

- The `可带回素材` line can become too dense if all real material categories are shown at once. Runtime should cap it to 2-3 items or wrap into a controlled two-line field.
- The compact task-overview ticket is useful, but it must stay a single source of task counts. Do not also repeat those values in the body or ticker.
- The screenshot is still a filled-state Image 2 target. Production must return to no-text assets, state atlases, `content_rects / no_text_rects / hit_rects`, and Godot dynamic text.

## Production Implication

For component production, keep the right dossier art as an empty, orthographic paper object with clear safe zones:

- `image_preview`
- `state_ticket`
- `task_overview_ticket`
- `body_feature`
- `body_anomaly`
- `body_materials`
- `body_warning_or_value`
- `cta_label`

The final Godot / HTML implementation should drive left card, map pin, right dossier, CTA, and ticker from the same selected-region view model, while keeping all player-facing text dynamic.

## A77 Supersession - 2026-06-17

This review is now a historical stepping stone. A later UX / UI pass restored `难度 / 推荐` as the useful region-level choice signal and moved task-pool data behind the right-side `任务情报` ticket / popover.

Current component production should therefore treat `task_overview_ticket` as superseded by `task_intel_ticket`:

- left cards use difficulty, recommendation, and short reason / lock gap;
- left cards do not show `目标 / 限时 / 线索 / 深链`;
- the right cyan `任务情报` ticket opens a read-only popover;
- the popover must not include task selection, dispatch, staff, dice, or success rate.

Current reference:

- `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/03-world-map-v7-difficulty-rating-task-intel-popover.png`
