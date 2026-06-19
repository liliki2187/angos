# World Map v7 A80 Task Intel Button Affordance Review

> Date: 2026-06-17  
> Source: user feedback that the cyan task-intel button looks like the title bar of the prose content below it.

## Problem

The A79 hierarchy solved the wrong content boundary, but the visual affordance is still ambiguous:

- `任务情报 · 3` is full-width and sits directly above the prose paper;
- the strip shares the same horizontal rhythm as a section title bar;
- the first prose heading `地区特征` follows immediately below it;
- the control lacks an action verb, right-side action zone, and enough air gap.

Players can reasonably read it as “the title of the following content block” instead of “a clickable entrance that opens task preview.”

## UX Decision

Use an independent ticket-button pattern instead of a title-bar pattern.

Standard state:

```text
[red state ticket]

    [ 查看任务情报 · 3   > ]   <- inset, raised, clickable ticket

        12-16px air gap

[large prose paper]
  地区特征
  本周异变
  可带回素材
  地区预警
```

## Rules

- Standard label: `查看任务情报 · N`.
- The ticket is narrower than the prose paper and inset by 12-20px on both sides.
- The ticket has a visible raised layer: small shadow, offset, bevel, folded corner, or separated backing.
- Add one action cue on the right: `>` arrow, inspect icon, or a small `查看` chip.
- Keep 12-16px clear space between the ticket and the first prose heading.
- Hover / pressed / open states must change the ticket surface, not the prose paper.
- The prose paper starts with its own heading `地区特征`; it must not have a blue title strip.

## Rejection Criteria

- Cyan task-intel strip has the same width as the prose paper.
- Cyan task-intel strip touches the prose paper or shares its top edge.
- Label is only `任务情报` without count or action cue.
- The prose paper appears to be subordinate to the task-intel strip.
- The popover opens by shifting / reflowing the prose content instead of anchoring to the ticket.

## Production Boundary

This affects the no-text right-dossier component and task-intel ticket state atlas. The production PNG may include ticket shape, icon slot, arrow / inspect glyph, shadow, and state backgrounds, but all labels and counts remain runtime text.

## Godot Preview Rejection - 2026-06-18

Implemented as a functional split preview over the current v6g component candidates, then rejected by user review on 2026-06-18:

- Default closed state: `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/01-world-map-a80-functional-preview.png`
- Task-intel open state: `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/02-world-map-a80-task-popover-open.png`
- Safety overlay: `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/03-world-map-a80-safe-zones.png`

The preview solved only the narrow “task-intel strip should not read as a prose title bar” issue. It failed the larger container compatibility gate:

- the old right dossier does not have a valid region-image viewport;
- the region image visually spills out of the paper and clashes with side tabs;
- the red state strip and cyan task-intel ticket float on top of baked art instead of being hosted by dedicated components;
- buttons and text are being fitted by coordinates, not by a pre-approved visual-safe content area.

This preview is therefore a failure sample, not a production source. The next step is not to move the controls around. The next step is to redraw / regenerate the right-dossier component family from a fresh structure contract, with explicit `media_viewport`, `alert_ribbon`, `task_intel_ticket`, `prose_body`, `cta_plate`, `content_rects`, `no_text_rects`, and state atlas definitions.
