# World Map B7 Branch · Local Filled-State Review

> Date: 2026-06-22  
> Scope: local no-upload continuation after OpenRouter generation was blocked by external-transfer policy.  
> Artifact type: `filled-state text mock candidate` / local polish candidate, not AI regeneration.

## 1. Files

- Closed state candidate: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/18-b7-local-filled-state-text-mock-candidate.png`
- Task-intel open candidate: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/19-b7-local-task-intel-popover-open-candidate.png`
- Lower-right passive v2 closed: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/20-b7-local-filled-state-v2-lower-right-passive.png`
- Lower-right passive v2 open: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/21-b7-local-task-intel-open-v2-lower-right-passive.png`
- Lower-right v2 crop: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/22-b7-v2-lower-right-passive-crop.png`
- Lower-right sealed v3 closed: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/23-b7-local-filled-state-v3-lower-right-sealed.png`
- Lower-right sealed v3 open: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/24-b7-local-task-intel-open-v3-lower-right-sealed.png`
- Lower-right v3 crop: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/25-b7-v3-lower-right-sealed-crop.png`
- Source style/color reference: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/15-variant-b7-strict-color-match-pass.png`
- Content contract: `docs/plans/world-map-branch-pixel-grain/filled-content-contract-b7-2026-06-22.md`
- Generation brief, still useful if a trusted image route becomes available: `docs/plans/world-map-branch-pixel-grain/filled-state-text-mock-brief-b7-2026-06-22.md`

## 2. External Generation Status

OpenRouter generation was attempted only after local dry-run validation, but the actual network request was rejected by policy because it would upload private project screenshots and prompt content to an external service.

No workaround was attempted. The safer continuation is a local-only mock that does not leave the workspace.

## 3. Local Color Check

The first local pass used an over-bright hardcoded paper fill. This was corrected before review: all added paper backplates now use the B7 contract paper colors:

- right / dossier paper: `#DFD4C7`
- left / bottom card paper: `#E0D5C7`
- alert red-orange: `#B53D27`
- signal cyan: `#5890A1`

Sampled local surfaces:

| Image | Surface | Hex | Note |
| --- | --- | --- | --- |
| Closed | `right_body_paper` | `#DFD4C7` | matches B7 contract |
| Closed | `left_selected_paper` | `#E0D5C7` | matches B7 contract |
| Closed | `bottom_ticker_paper` | `#E0D5C7` | matches B7 contract |
| Closed | `top_ticket_paper` | `#E0D5C7` | local added status ticket |
| Closed | `alert_ribbon` | `#B53D27` | matches B7 contract |
| Closed | `task_ticket_cyan` | `#5890A1` | matches B7 contract |
| Closed | `navy_status_bg` | `#081624` | close to B7 navy, slightly darker as UI backplate |

Global stats:

| Image | Mean luminance | Paper ratio | Dark ratio | Interpretation |
| --- | ---: | ---: | ---: | --- |
| B7 | 90.72 | 0.3106 | 0.5478 | baseline after local export sampling |
| Closed candidate | 93.12 | 0.3241 | 0.5382 | acceptable for local overlay; more text backplates increase paper area |
| Open candidate | 99.03 | 0.3560 | 0.5096 | expected because the task-intel popover adds a large paper sheet |

Because this is not a global image regeneration, global paper ratio is treated as a state-composition effect, not palette drift. If an AI-regenerated version is produced later, it must rerun the strict Color Contract Gate against the original reference.

## 4. Gate Review

| Gate | Closed candidate | Open candidate | Note |
| --- | --- | --- | --- |
| Current selected region visible in 5 seconds | Pass | Pass | `北美禁区` is dominant in left card, map short label, and right dossier |
| Urgent state visible | Pass | Pass | red ribbon `红线升温` is clear |
| Primary action clear | Pass | Pass | CTA uses fixed `进入选定地区` |
| CTA excludes region name | Pass | Pass | no `进入北美禁区` |
| Right body is one intro paragraph | Pass | Pass | no task list inside prose body |
| Task intel ticket independent | Pass | Pass | cyan ticket has its own raised plate and action cue |
| Task intel popover read-only | N/A | Pass | no dispatch, staff, dice, success rate, or selection CTA |
| Bottom ticker is low-weight detail entrance | Conditional pass | Conditional pass | works after shortening copy; longer titles need wider slots |
| Locked state distance visible | Pass | Pass | `东亚镜像城` / `南极静默区` are lower-affordance locked cards |
| Text not crossed by route / state decoration | Pass after correction | Pass after correction | first local pass failed this; diagonal state line was removed |
| Lower-right device role clarity | Fail | Fail | visually still reads like a strong `>>` actuator / possible next-step button; after the 2026-06-22 revision, day advance is allowed only in the bottom global schedule strip, not as this standalone lower-right console |

## 5. Remaining Risks

- This is still a local overlay / polish candidate, not a true single-pass art-integrated image. Some text backplates still read more engineered than generated paper ink.
- B7's right dossier can fit the necessary state sequence, but the prose area is tight. Longer paragraphs should be shortened or the actual mock should reserve a taller prose body.
- Bottom ticker accepts short two-part labels; 10-14 character titles will need wider text slots.
- Six left cards work visually in B7, but prior v7 production contracts favored four safer region cards. This branch needs an explicit choice before any asset pass.
- The task-intel popover open state is readable but visually more utilitarian than the base art. A true art pass should integrate the popover paper edge, shadow, and anchor more naturally.
- The lower-right mechanical console is currently unresolved. Its visual weight and `>>` actuator can be read as `下一天 / 推进一天`. The user has now revised the world-map rule: day advance may exist, but it must align with the region page's bottom global schedule strip. The next mock must therefore either move / rebuild `推进一天` into the bottom schedule strip, or remove / disable / visually downgrade the standalone lower-right console.

## 6. Status

The local closed and open candidates are acceptable for **next-step visual discussion and UI/UX/pixel-art review**, but they are not production assets, not a no-text asset master, and not component-splitting sources. After the lower-right device ambiguity was identified, they should be treated as **function-role clarity failed candidates** until the lower-right console is resolved.

Do not enter atlas / manifest / slicing until a reviewed `filled-state text mock` is accepted by the user and then converted into a separate `no-text asset master`.

## 7. Lower-Right Device Fix

User review raised the question whether the lower-right mechanical console was missing a function, possibly `下一天`. Initial contract check said:

- World map does not advance the day.
- `下一天 / 推进一天` belongs to the region task board or dispatch context.
- The lower-right console in this branch must not be a primary action.

2026-06-22 user revision supersedes the first bullet: world map can have `下一天 / 推进一天`, but it must use the same bottom global schedule strip location and confirmation behavior as the region task board. The current region reference is `docs/screenshots/2026-06-18-region-task-v3-6-separated-advance/02-bottom-global-schedule-strip.png`, with confirming crop `04-advance-confirming-state-crop.png`.

### v2 Result

`20` / `21` attempted to cover the gold `>>` actuator with a passive `只读` cap. This improved the issue but the small white-outlined cap still read like a miniature button. v2 is therefore kept as an intermediate failure / partial fix.

### v3 Result

`23` / `24` replace the actuator with a dark sealed instrument cover labeled `封存`, while the adjacent plate reads `频道监听 / 只读 · 不推进时间`.

Current v3 status:

| Check | Verdict | Note |
| --- | --- | --- |
| Reads as `下一天 / 推进一天` | Pass | no arrow, no gold push button, no next-step wording |
| Competes with primary CTA | Pass | visually lower than the red `进入选定地区` CTA |
| Still explains why the object exists | Conditional pass | reads as passive channel monitor / world-state instrument |
| Art integration | Partial | still local overlay; a true art pass should make the sealed cover more naturally part of the machine |

v3 is now a superseded detour rather than the current target. It solved the old "not next day" ambiguity, but the user clarified that a world-map next-day action is acceptable if placed consistently.

2026-06-23 update: after the left-bottom structure sketch, the current B7 target is **left-bottom global schedule dock + extended right dossier**. `推进一天 / 确认推进？` lives under the region index as an independent global schedule component, not as a region card. The right dossier extends downward into the former lower-right machine area to provide more selected-region prose and keeps `进入选定地区` as its only primary CTA.
