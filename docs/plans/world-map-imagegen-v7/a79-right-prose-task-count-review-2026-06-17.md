# World Map v7 A79 Right Prose + Task Count Button Review

> Date: 2026-06-17  
> Scope: Image2 filled-state target iterations after the user's correction that the right prose paper should only contain region copy.

## Accepted Information Architecture

- Right dossier order is fixed: title / badges -> region image -> red state ticket -> cyan `任务情报 · N` ticket -> large region prose paper -> primary CTA.
- The large prose paper contains only `地区特征 / 本周异变 / 可带回素材 / 地区预警或编辑价值`.
- Task preview is opened from the `任务情报 · N` ticket as a read-only popover.
- The popover may show 2-3 compact preview rows, but it must not show dispatch, staff, dice, success rate, or selectable task cards.
- Left region cards keep difficulty / recommendation / short reason and must not show `目标 / 限时 / 线索 / 深链` task counters.

## Iteration QA

### Failed Structure

The first A79-style generation had good overall Angus styling, map quality, paper brightness, and pixel-print density, but it failed the user's core hierarchy:

- the cyan `任务情报` button remained below the large prose paper;
- the button did not include the visible count `· 3`;
- the popover title drifted toward a generic `任务情报预览` label;
- therefore the screen still implied that tasks are subordinate to the body prose area.

This output should be treated only as a failed structure reference.

### Corrected Direction

The corrected direction is:

- `任务情报 · 3` sits directly under the red state ticket;
- the prose paper begins below the task-count ticket;
- the prose paper only explains the region;
- the popover title is `本区可追踪任务 3`;
- the main CTA remains `进入选定地区` and stays visually primary.

## Prompt Guardrail

Future A79 prompts should explicitly state:

```text
The cyan 任务情报 · 3 ticket must never sit below the large prose paper.
The large prose paper must never sit directly under the red / state ticket when the task-intel ticket exists.
The 任务情报 ticket must show its count on the button face; do not render it as only 任务情报.
```

## Production Boundary

These Image2 outputs are filled-state target screenshots only. They are not production PNGs, cut-up sources, manifest sources, or runtime backgrounds. Production components must be no-text art assets; Godot renders region names, values, task counts, button states, popovers, and all dynamic labels.

## A80 Follow-Up: Button Affordance

The next UX issue is not placement but affordance. A full-width cyan `任务情报 · 3` strip directly above the prose paper reads as that paper's title bar, not as a clickable task-intel entrance.

Follow-up correction:

- Use `查看任务情报 · N` as the standard button label.
- Make the ticket narrower than the prose paper, inset from both sides, and visually raised.
- Keep a 12-16px air gap between the task-intel ticket and the first prose heading.
- Add a right-side action cue such as `>` / inspect icon / small `查看` chip.
- Ensure hover / pressed / open states affect the ticket itself.
- Treat any full-width cyan strip attached to the prose paper as failed, even if it is in the correct vertical order.
