# World Map v7 Functional Layout Contract

> Status: 2026-06-16 pre-style functional contract.  
> Scope: world map / global channel screen before the next style draft.  
> Rule: keep the approved v6g visual direction, especially the central low-poly paper world map, but rebuild text-bearing components from function and capacity.

## 1. Page Contract

The world map page is responsible for one decision:

```text
Choose a reporting region, understand whether the selected region can be entered, then enter that selected region.
```

The page does not directly select tasks, configure staff, roll dice, advance the day, enter dispatch signoff, or show the full action log. Those responsibilities belong to the downstream region task board, dispatch signoff screen, and result/log surfaces.

The selected region name is owned by the region title / dossier. It must not be baked into the primary CTA label. The CTA label is a fixed action slot such as `进入选定地区`; disabled / loading states may change the state text, but still must not include a dynamic region name.

### 1.1 P0 / P1 Functional Recovery Scope

The v7/v4 visual target is not functionally complete until it restores the older web prototype's world-map decision loop. The loop must be visible in a filled-state mock before component production:

```text
select region -> refresh selected-region dossier -> understand enterable / blocked state -> enter selected region
```

P0 requirements:

- `selected_region_id` drives the left card selected state, map pin selected ring, right dossier content, CTA state, and bottom receipts.
- A selectable region and a locked region must have clearly different visual affordances. Locked regions are still visible as world information, but they do not behave like normal enter buttons.
- The CTA has at least `default`, `disabled`, and `loading` semantics. Disabled text stays fixed (`暂不可进入` or equivalent), while the blocker reason appears in the dossier footer, not inside the button.
- Entering a region passes the selected region context to the downstream region task board. The world map does not select a task directly.

P1 requirements:

- The older web prototype's useful region-level decision signals return as `难度` and `推荐` on the left region card and selected-region title area. Task-pool details move behind a secondary `任务情报` ticket located directly under the red / state ticket; the ticket label must include the available task count, and clicking it opens a read-only popover. Task-pool details must not occupy the left card or the dossier body paper.
- Locked regions expose a short left-card blocker and a full blocked-dossier variant with current value / required value or equivalent unlock gap.
- Right-dossier preview rows must be real region intel, not UI tutorial copy or legend text.
- Bottom ticker lanes carry low-weight clickable details only: `地区情报`, `档案更新`, `地区预警` or equivalent. They report region intel / file updates / entry impact and must not become a second task-summary lane.

Lower-priority items such as topic filters, long action logs, full hover preview behavior, and animated pressed polish are explicitly outside the current P0/P1 style draft unless the user reopens them.

## 2. Keep / Rework

| Category | Decision |
| --- | --- |
| Keep | Strong v6g pixel-print direction, bright ivory paper, deep navy editorial board, faceted low-poly paper world map, red-orange anomaly marks, restrained cyan tracking marks |
| Keep | Central map board as the primary visual object; it may be reused or cleaned without redesigning the map language |
| Rework | Left region cards, right dossier, CTA, ticker, pin labels, selected rings, lock/urgent/completed states |
| Remove from PNG | Region names, Chinese text, numbers, task names, button labels, countdowns, fake pins, fake tooltips, fake task states |
| Runtime owns | Text, values, hover, selected, disabled, pressed, locked, loading, hit areas, route highlights, tooltip / short label content |

## 3. Desktop 16:9 Layout

Target canvas: `1920x1080`.

```text
TopStatusStrip  [72, 36, 1776, 52]

LeftIndex       [72, 112, 424, 792]
MapBoard        [516, 112, 868, 792]
RightDossier    [1416, 112, 432, 636]
PrimaryCTA      [1416, 768, 432, 126]

BottomTicker    [72, 928, 1776, 100]
```

The existing v6g map board material is the anchor. If the final art keeps the current `856x812` map component, preserve its visual language and only adjust surrounding gutters / shell dimensions.

A83 update: the `RightDossier [1416,112,432,636]` / `PrimaryCTA [1416,768,432,126]` layout above is now a legacy v7/A80 draft and must not be used as the next production source. It failed the 2026-06-18 container compatibility review because the old right-side art cannot host the new media viewport, alert ribbon, task-intel ticket, prose body, and CTA. The pending replacement candidate is documented in §8.8 and tests a `560w` right dossier.

## 4. Functional Zones

| Zone | Player question | Dynamic content | Capacity limit | Art role |
| --- | --- | --- | --- | --- |
| Top status strip | What week / world-state am I in? | Left weekly clock tickets: week, days left; right world-state badge rail: 公信 / 诡名 / 声望 / 守序 / 狂性 | One compact row; no phase label; no material counters; two distinct visual grammars | Weekly paper tickets + low-weight world-state badge rail |
| Left region index | Which regions are available, locked, or worth entering first? | 4 visible region cards; name, availability, region-level difficulty, recommendation rating, one short reason / lock gap | 1 title + 2 meta lines per card; no task counters | Index folder / card stack |
| Central map | Where is the current region and what is active? | Pins, selected ring, route highlight, hover/selected short label | Persistent text: 0; pins <= 6 | Static map board, no gameplay labels |
| Right dossier | What is this selected region and what happens next? | Fixed slot label, region title, difficulty badge, recommendation badge, region image preview, red / state ticket, independent secondary `查看任务情报 · N` ticket directly below the red / state ticket, one single selected-region introduction paragraph, enter condition / consequence footer | Region intro 70-110 Chinese chars; dossier body paper is only a read-only region introduction; no task operation list, no region-intel tiles, no file-update rows, no warning detail cards; task-pool preview only appears through the task-intel ticket / popover; the task ticket must not read as the prose-paper title bar | Selected-region dossier paper |
| Task intel popover | What kind of tasks will I find after entering? | Read-only task-pool preview: 3 compact rows max, task type/name/cost/condition/risk tags, footer note | No selected task, no dispatch, no dice, no success rate; 3-4 rows max | Secondary paper popover anchored to the task-count ticket below the red / state ticket |
| Primary CTA | Can I enter the selected region? | Fixed CTA label, disabled/loading state | default `进入选定地区`; disabled `暂不可进入`; no region name | Independent action object / signoff plate |
| Bottom ticker | What changed recently and what details can I inspect? | 1-3 clickable detail entrances: `地区情报`, `档案更新`, `地区预警` or equivalent | type chip 4 chars + title 10-14 chars + action cue; each lane opens a read-only detail layer; no task progress bar or duplicate task summary | Printed receipt / channel ticker |

Do not use top-strip slots for `全球频道`, `素材`, `阶段：取材`, or a single standalone `声望` value. `声望` is one of the five macro attributes and must appear together with `公信 / 诡名 / 守序 / 狂性` when shown. Removing the phase label reserves enough width for the last macro chip (`狂性`) to render fully.

The weekly clock (`探索周`, `剩余天数`) and the five macro attributes must not share the same paper-ticket frame. They represent different time scales: weekly operation context vs long-term world state. The macro attributes should use a separate low-weight `世界状态` badge rail / meter rail / signal-light strip with lighter backing, smaller marks, and no full white paper card frame. The five metrics should read as a grouped long-term status display, not as task counters, resource currency, or clickable fields.

## 5. Field Capacity

| Field | Token | Max length | Lines | Overflow policy |
| --- | --- | ---: | ---: | --- |
| Region name | L3 26px | 8-10 Chinese chars | 1 | Use short name; ellipsis only after short-name review |
| Region state | L6 20px | 4-6 Chinese chars | 1 | State badge, not a body sentence |
| Region difficulty | L6 18-20px | 2-4 Chinese chars | 1 | Region-level entry pressure only: `低 / 中等 / 高 / 异常`; not a concrete task difficulty |
| Recommendation rating | L6 18-20px | label + 1-5 marks | 1 | `推荐 ★★★` / `取材优先 ★★★`; rating marks are dynamic and data-backed |
| Recommendation reason | L6 18px | 8-12 Chinese chars | 1 | One short reason only, e.g. `红线升温`, `首区主线`, `素材多` |
| Macro chip | L6 18-20px | 2 chars + 1-2 digit value | 1 | Show all five together inside the `世界状态` badge rail; do not promote one metric alone |
| Lock gap short | L6 20px | 14-18 Chinese chars | 1 | Longer gap moves to right dossier footer |
| Dossier fixed label | L6 18px | 4-6 Chinese chars | 1 | Fixed slot label such as `选定地区`; not a dynamic region name |
| Dossier title | L2 28px | 10 Chinese chars | 1 | Ellipsis + tooltip / detail |
| Region intro | L4 22px | 44-56 Chinese chars | 2 | Third line forbidden; move to region screen |
| Region intro paragraph | L5 18-20px | 70-110 Chinese chars | 4-5 compact lines | One continuous selected-region introduction; no `地区情报 / 档案更新 / 地区预警` submodules |
| Task intel ticket label | L6 20px | 7-11 Chinese chars incl. count | 1 | Standard secondary button label `查看任务情报 · 3`; shorter `任务情报 · 3` is allowed only if the ticket also has a clear right-side action zone. The total visible count is allowed here, but no `目标 / 限时 / 线索 / 深链` breakdown |
| Task intel popover row | L6 18px | title 14 chars + meta/tags | 2-3 | Read-only task preview; no selected state, no action button |
| Enter condition / consequence | L6 20px | 18-22 Chinese chars | 1 | Put blocker reason / entry consequence outside button |
| CTA label | L3/L4 24-26px | 4-6 Chinese chars | 1 | Fixed action: `进入选定地区`; do not include region name |
| CTA disabled reason | L6 20px | 18-22 Chinese chars | 1 | Put in dossier footer, not inside button |
| Ticker item | L6 18-20px | type 4 chars + title 10-14 chars + action cue | 1 | Clickable `地区情报 / 档案更新 / 地区预警` entry; detail opens separately; no long body text in ticker lane |

## 6. Component Contract

| Asset id | Size | Runtime rect | Dynamic text |
| --- | ---: | --- | --- |
| `wm_bg_editorial_shell_v7` | `1920x1080` | `[0,0,1920,1080]` | none |
| `wm_top_status_strip_v7` | `1776x52` | `[72,36,1776,52]` | weekly clock tickets, world-state badge rail |
| `wm_map_board_base_v7` | `868x792` | `[516,112,868,792]` | none |
| `wm_map_pin_atlas_v7` | `576x72`, 8 frames | by anchors | none inside PNG |
| `wm_map_short_label_v7` | `260x64` | by pin anchor | label + small status |
| `wm_left_region_card_atlas_v7` | `384x166`, 5 frames | 4 slots in LeftIndex | title, availability, difficulty, recommendation, short reason / lock gap |
| `wm_right_dossier_base_v7` | `432x636` | `[1416,112,432,636]` | fixed slot label, title, difficulty badge, recommendation badge, region image slot, state ticket, task-intel ticket label + count, region body sections only, footer |
| `wm_task_intel_popover_v7` | `560x500` | anchored left of right dossier task-intel ticket | title, subtitle, 3 read-only task rows, footer, close label |
| `wm_cta_enter_region_atlas_v7` | `1728x126`, 4 frames | `[1416,768,432,126]` | label only |
| `wm_bottom_ticker_v7` | `1776x100` | `[72,928,1776,100]` | three short feedback lanes |

The `wm_right_dossier_base_v7` and `wm_cta_enter_region_atlas_v7` rows above are retained only as the legacy draft record. If Right Dossier Structure Wireframe V1 is approved, replace them with:

| Candidate asset id | Size | Runtime rect | Dynamic text |
| --- | ---: | --- | --- |
| `wm_right_dossier_base_v7b_candidate` | `560x750` | `[1320,188,560,750]` | fixed label, region name, badges, single intro paragraph, footer |
| `wm_region_media_frame_v7b_candidate` | `470x170` | `[1348,292,470,170]` inside dossier | none; hosts clipped region preview image |
| `wm_alert_ribbon_v7b_candidate` | `470x44` | `[1348,478,470,44]` inside dossier | one alert line |
| `wm_task_intel_ticket_atlas_v7b_candidate` | `1544x52`, 4 frames | `[1390,536,386,52]` inside dossier | label + count + action cue |
| `wm_cta_enter_region_atlas_v7b_candidate` | `1880x60`, 4 frames | `[1348,842,470,60]` inside dossier | fixed CTA label |
| `wm_bottom_ticker_item_atlas_v7b_candidate` | `1770x68`, 3 lanes or atlas frames | bottom ticker lanes | type chip, short title, action cue |

## 7. Content Rects / No-Text Rects

| Asset id | Content rects | No-text / hit rects |
| --- | --- | --- |
| `wm_top_status_strip_v7` | `week:[32,10,170,32]`, `days:[230,10,150,32]`, `world_state_label:[440,12,96,28]`, `macro_badge_1:[560,10,104,32]`, `macro_badge_2:[690,10,104,32]`, `macro_badge_3:[820,10,104,32]`, `macro_badge_4:[950,10,104,32]`, `macro_badge_5:[1080,10,104,32]` | `left_trim:[0,0,24,52]`, `week_ticket_frame:[24,0,380,52]`, `macro_rail:[420,6,820,40]`, `right_marks:[1680,0,96,52]`; no phase slot; macro rail must not use the same full white paper-ticket frame as week/day |
| `wm_left_region_card_atlas_v7` | `title:[64,20,184,30]`, `difficulty:[64,56,112,28]`, `recommendation:[184,56,134,28]`, `availability_reason:[64,92,236,42]`, `status_badge:[284,20,72,30]` | `binding:[0,0,48,166]`, `bookmark:[330,0,54,166]`, `bottom_edge:[0,146,384,20]`, `hit:[0,0,384,166]`; no `目标 / 限时 / 线索 / 深链` counters on the card |
| `wm_map_board_base_v7` | none | whole map is no-baked-pins / no-baked-labels; anchors: North America `[205,335]`, South America `[265,545]`, Europe/Africa `[442,372]`, East Asia `[672,348]`, Oceania `[720,590]` |
| `wm_map_short_label_v7` | `label:[28,14,174,30]`, `status:[204,14,38,30]` | `tail:[110,46,42,18]`, `pin_overlap:[0,0,24,64]` |
| `wm_right_dossier_base_v7` | `slot_label:[54,42,118,24]`, `title:[54,70,210,36]`, `difficulty_badge:[272,74,74,28]`, `recommendation_badge:[54,106,150,28]`, `image_preview:[54,144,314,122]`, `state_ticket:[54,282,314,34]`, `task_intel_label:[88,338,172,28]`, `task_intel_action:[278,338,48,28]`, `body_feature:[54,418,314,42]`, `body_anomaly:[54,470,314,42]`, `body_materials:[54,522,314,42]`, `footer:[54,574,314,42]` | `top_clip:[118,0,196,36]`, `left_ribbon:[0,40,42,210]`, `right_tabs:[372,0,60,636]`, `corner_halftone:[330,500,86,112]`; `task_intel_ticket:[72,330,272,42]` sits directly below `state_ticket`, is inset from the prose paper, has 12-16px air gap before the body paper, and has visible hit / hover / pressed affordance; `body_top_safe:[54,390,314,20]` must stay empty so the ticket does not read as the prose-paper title bar |
| `wm_task_intel_popover_v7` | `title:[36,28,220,32]`, `subtitle:[36,64,350,26]`, `row_1:[42,112,470,82]`, `row_2:[42,210,470,82]`, `row_3:[42,308,470,82]`, `footer:[42,416,420,38]`, `close_label:[500,24,32,32]` | `anchor_tail:[500,188,60,60]`, `shadow:[0,0,560,500]`, `hit:[0,0,560,500]`; no action buttons, selected row, dispatch affordance, dice, or success-rate block |
| `wm_cta_enter_region_atlas_v7` | per frame `label:[64,34,250,42]` | per frame `left_screw:[8,32,44,56]`, `right_arrow:[330,26,70,68]`, `bottom_stripe:[0,100,432,26]`, `hit:[0,0,432,126]`, `hover:[-8,-8,448,142]` |
| `wm_bottom_ticker_v7` | `latest_record:[136,22,360,34]`, `dossier_update:[650,22,360,34]`, `region_warning:[1160,22,430,34]` | `color_tabs:[0,0,120,100]`, `[560,0,84,100]`, `[1070,0,84,100]`, `right_halftone:[1630,0,110,100]`; no large icon button |

## 8. State Matrix

| Component | Required states |
| --- | --- |
| Region card | normal, hover, selected, locked, completed |
| Map pin | normal, hover, selected, locked, urgent, completed |
| Map short label | hidden, hover, selected, locked |
| Right dossier | ready, blocked, empty |
| Task intel ticket | default, hover, pressed, open, disabled, new |
| Task intel popover | closed, open, blocked, empty |
| Primary CTA | default, hover, pressed, disabled, loading |
| Ticker lane | normal, alert, empty |
| Top status chip | normal, warning, changed |

All states must keep text in the same content rect. Pressed / disabled / loading cannot shift the label into stripes, screws, arrows, halftone, or card edges.

## 8.1 Runtime View Model Contract

The filled-state mock and the later Godot / HTML implementation must be backed by one conceptual `worldRegionViewModel`. The exact code name may change, but the data contract must exist before production replacement.

Minimum fields:

| Field | Purpose |
| --- | --- |
| `selected_region_id` | Single source for selected left card, map pin, right dossier, CTA, and ticker |
| `regions[].availability` | `enterable`, `locked`, `completed`, `urgent`, or equivalent state |
| `regions[].difficulty` | Region-level entry pressure: `low`, `medium`, `high`, `anomaly`, or equivalent localized label |
| `regions[].recommendation_rating` | 1-5 mark recommendation score for entry priority; data-backed or hand-authored, but not decorative |
| `regions[].recommendation_reason` | One short reason for the rating, such as red-line heat, tutorial priority, material value, or lock risk |
| `regions[].task_count` | Current known and previewable task count rendered on the task-intel ticket, e.g. `查看任务情报 · 3`; exclude hidden tasks, locked deep-chain tasks, and future generated tasks |
| `regions[].task_pool_summary` | Optional read-only task-pool preview data for the `任务情报` popover; not rendered on the left card or dossier body |
| `regions[].unlock_gap` | Short left-card blocker plus full blocked-dossier reason |
| `regions[].dossier_body` | Region feature, weekly anomaly, material leads, warning / editor value; not tutorial, legend text, or repeated task counters |
| `task_intel_popover_state` | `closed`, `open`, `blocked`, or `empty`; owned by the selected region and cyan secondary ticket |
| `cta_state` | `default`, `disabled`, `loading`, with label independent from region name |
| `ticker_receipts` | Three world-level feedback lanes: latest record, dossier update, region warning / entry impact |

The world map must not duplicate task-board data by rendering concrete playable task cards. It may preview task categories and entry risks only when the player opens `任务情报`, and that popover remains read-only.

### 8.2 Godot P0/P1 Runtime Landing - 2026-06-17

Current runtime landing screenshots:

- Ready: `docs/screenshots/2026-06-17-world-map-p0p1-godot/01-world-map-p0p1-ready.png`
- Locked: `docs/screenshots/2026-06-17-world-map-p0p1-godot/02-world-map-p0p1-locked.png`

Implemented dynamic fields:

- Fixed CTA label: `进入选定地区` / `暂不可进入`.
- Left region cards: status line plus compact region capacity line.
- Current runtime right dossier: `地区简介`, `任务小结`, `地区预警` rendered as dynamic Godot text. This is a smoke-test state; final v7 target is revised in A85 to keep only one selected-region introduction in the dossier body.
- Right state tickets: compact selected-region status and summary counters.
- Current runtime bottom ticker: `最近变化`, `地区异动`, `地区预警`. Final v7 target uses clickable detail lanes such as `地区情报`, `档案更新`, `地区预警`.
- Locked regions remain selectable for preview, but cannot enter through CTA.

This is a runtime information-contract landing over the current assetized world-map UI. It is not yet the final v7 no-text component replacement. Formal v7 PNG production must still create clean component backgrounds and state atlases matching the content rects in this document.

### 8.3 Right-Dossier Redundancy Reduction - 2026-06-17

The UX-reviewed fusion B revision removes the duplicated body-level `任务小结` from the right dossier. The right dossier may still show one compact secondary `任务情报` ticket near the image / status tickets. A85 further tightens the dossier body: it now contains one continuous selected-region introduction only, not separate `地区情报`, `档案更新`, `地区预警`, `本周异变`, or material submodules.

The bottom ticker should no longer use `任务小结` as a lane label in this world-map target. Use clickable detail lanes such as `地区情报`, `档案更新`, and `地区预警`. These lanes may react to the selected region, but must not repeat the same task-pool values already available from the `任务情报` ticket / popover.

Reference target screenshot:

- `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/01-world-map-v7-fusion-b-ux-reduced-redundancy.png`

### 8.4 Difficulty / Recommendation + Task Intel Popover - 2026-06-17

The older web prototype's useful `难度 / 推荐` decision signal is restored, but it is treated as region-level entry advice:

- Left cards answer: `这个地区能不能进？值不值得先进？为什么？`
- Left cards show region title, availability, region-level difficulty, recommendation rating, and one short reason or lock gap.
- Left cards must not show `目标 / 限时 / 线索 / 深链` counters. Those counters are task-pool details, not region-index priorities.
- The right dossier title area may repeat `难度` and `推荐` as selected-region confirmation, especially when the selected card is no longer fully visible in the player's scan path.
- The cyan secondary ticket is named `查看任务情报` and sits directly below the red / state ticket. Its face must include the task count, e.g. `查看任务情报 · 3`, so players know why the ticket is worth opening. If a shorter label is used, the ticket must still include a right-side action zone such as `查看 >`.
- The task preview popover may show at most 3 compact rows: task type / rough name, cost or condition tags, risk or material tags.
- The popover must not allow task selection, dispatch start, staff assignment, dice preview, success rate, or full task detail. Those remain downstream region-task-board responsibilities.
- The dossier body paper below the status / task-intel tickets is reserved for one continuous region-introduction paragraph only. Do not put task summaries, region-intel tiles, file-update rows, warning detail cards, or material lists inside this body paper.
- The production PNG may contain only the no-text ticket / popover shell, icons, dividers, empty chips, and paper texture. All labels, values, stars / marks, task names, and warnings are runtime text.

Reference target screenshot:

- `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/03-world-map-v7-difficulty-rating-task-intel-popover.png`

### 8.5 Right-Dossier Prose Boundary + Task Count Ticket - 2026-06-17

A79 further tightens the right-dossier hierarchy:

```text
region image
-> red / state ticket
-> cyan secondary task-count ticket
-> large region prose paper
-> primary CTA
```

Rules:

- The large right body paper is one continuous region-introduction paragraph only.
- The large body paper must not contain task count, task list, task name, task summary, task preview rows, dispatch controls, staff, dice, success rate, filters, sorting, or tutorial copy.
- The large body paper must not contain separate `地区情报`, `档案更新`, `地区预警`, `本周异变`, `可带回素材`, or other tiled submodules. Those details live in the bottom ticker detail layers.
- The task-intel ticket sits directly below the red / state ticket and displays the only task count on this screen. A80 standard wording is `查看任务情报 · N`; the older `任务情报 · N` form is allowed only when a separate action cue such as `查看 >` is visible.
- `N` means current known and previewable tasks only. Hidden tasks, locked deep-chain tasks, and future generated tasks are excluded.
- Empty / blocked states: `暂无任务情报`, `任务情报未解锁`, and `读取任务情报…` are allowed dynamic labels.
- Clicking the ticket opens only a read-only popover. Concrete task selection remains in the downstream region task board.

### 8.6 Task Intel Button Affordance - 2026-06-17

The A79 placement alone is not enough. The task-intel ticket must read as an independent clickable trigger, not as the title bar of the prose paper below it.

Rules:

- Use the standard label `查看任务情报 · N`. The verb `查看` is intentional; pure noun labels such as `任务情报 · N` are allowed only with a strong right-side action zone.
- The ticket is a narrow, independent paper / metal ticket inset from the prose paper: recommended rect `task_intel_ticket:[72,330,272,42]`, while the prose paper text starts no earlier than `y=418`.
- Keep a visible 12-16px air gap between the bottom of the task-intel ticket and the first prose heading.
- Add a right-side action cue: `>` arrow, inspect icon, folded corner, or a separate small `查看` chip. Hover / pressed / open states must change the ticket itself, not the prose paper.
- The ticket must have a slight raised layer, shadow, or offset. It must not share the exact width, top edge, or visual frame of the prose paper.
- The prose paper may not begin with a blue strip or module header. Its first visible text is the selected-region introduction, and it must sit inside the prose paper's own content-safe area.
- If the open popover is shown, anchor it to the task-intel ticket. The popover opening must not cause the right prose paper to reflow.

### 8.7 A80 Godot Functional Split Preview Rejection - 2026-06-18

The A80 hierarchy was tested as a Godot functional preview over the current v6g component candidates. User review on 2026-06-18 rejected it as a production direction because the old right-dossier artboard does not physically support the new information structure.

Preview screenshots:

- Default closed state: `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/01-world-map-a80-functional-preview.png`
- Task intel open state: `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/02-world-map-a80-task-popover-open.png`
- Safety overlay: `docs/screenshots/2026-06-17-world-map-v7-a80-godot-preview/03-world-map-a80-safe-zones.png`

The preview is now a failure sample / compatibility test only. It demonstrates several invalid assumptions:

- The old right dossier was treated as a generic background, but it has baked paper edges, tabs, clip, halftone, and side ornaments that are real no-text / no-control zones.
- The region image lacks a real media viewport / mask, so it visually spills out of the dossier and competes with side tabs.
- The red state strip and cyan task-intel ticket have no structural host; they read as floating overlays rather than physical UI objects.
- The new function set needs `selected region -> risk state -> task count -> enter CTA -> prose`, while the old artboard was not sized for those slots.
- A far-view screenshot and basic rect fit were not enough; 100% crop and visual-safe-zone QA would have failed the right panel immediately.

Required correction before the next style draft:

- Build a fresh right-dossier component contract first: header, media viewport, alert strip, task-intel ticket, prose body, footer / CTA must each have explicit dimensions and capacity.
- Run a `legacy_container_compatibility_gate` before reusing any v6g art. If a new slot depends on clipping into old decoration, floating over a baked image, or shrinking text to survive, the old component must be rejected.
- Produce a low-fidelity structure wireframe and a filled-state text mock before any no-text PNG component generation.
- Formal v7 component production needs a fresh manifest with updated `content_rects`, `no_text_rects`, `hit_rects`, state atlas frames, media masks, and no-text PNG paths. Do not reuse the legacy v6g safety overlay as the final A80 overlay.

### 8.8 Right Dossier Structure Wireframe V1 - 2026-06-18

A replacement structure wireframe has been drafted for review after the A80 compatibility failure:

- Spec: `docs/plans/world-map-imagegen-v7/right-dossier-structure-wireframe-v1-2026-06-18.md`
- Full screen: `docs/screenshots/2026-06-18-world-map-v7-right-dossier-structure/01-world-map-v7-right-dossier-structure-wireframe.png`
- Right dossier 100% crop: `docs/screenshots/2026-06-18-world-map-v7-right-dossier-structure/02-right-dossier-structure-100pct-crop.png`
- Source: `docs/prototypes/world-map-v7/right-dossier-structure-wireframe.html`

Status: user accepted the structural direction on 2026-06-18 after the prose body was revised to one single region introduction and `地区情报 / 档案更新 / 地区预警` were moved to clickable bottom ticker lanes. Do not use this wireframe as an approved art source yet. The old `432w` right dossier should be replaced by a fresh `560w` dossier component family with explicit `media_viewport`, `alert_ribbon`, `task_intel_ticket`, `prose_body`, `footer_hint`, `primary_cta`, and `bottom_ticker_item` rects.

### 8.9 Filled Content Mock V1 - 2026-06-18

A real-content validation mock has been drafted after the annotation row was removed from the structure wireframe. This is the field and capacity source for the next style draft, not an art source and not a no-text PNG component.

- Spec: `docs/plans/world-map-imagegen-v7/filled-content-mock-v1-2026-06-18.md`
- Full screen: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/01-world-map-v7-filled-content-mock.png`
- Right dossier 100% crop: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/02-right-dossier-filled-content-100pct.png`
- Bottom ticker warning detail open: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/03-bottom-ticker-warning-detail-open.png`
- Bottom ticker 100% crop: `docs/screenshots/2026-06-18-world-map-v7-filled-content-mock/04-bottom-ticker-100pct.png`
- Source: `docs/prototypes/world-map-v7/filled-content-mock-v1.html`

Validated content contract:

- Top strip is one game-facing strip only: week / days left + grouped five macro attributes. No production annotation title row.
- Right dossier body contains one selected-region intro paragraph only.
- Bottom ticker carries clickable `地区情报 / 档案更新 / 地区预警` detail entrances.
- The ticker detail popover opens as a read-only detail layer and does not cover the right-dossier primary CTA.
- The central map remains placeholder-level in this mock; the next style draft should retain or retranslate the approved v6g / fusion B low-poly paper map language.

## 9. Next Style Draft Brief

Generate one desktop 16:9 production style draft for a single real state:

```text
North America quarantine zone selected + red-line heating + enterable.
```

For the P0/P1 filled-state validation, the text mock should additionally demonstrate:

- North America selected consistently across left index, map pin, right dossier, CTA, and ticker.
- At least one locked region visible in the left index with a short unlock gap.
- Left region cards show `难度` and `推荐` as region-level entry advice. They must not show task-pool counters.
- Right dossier title area repeats selected-region `难度` and `推荐` in compact badges.
- Right dossier has one compact independent `查看任务情报 · N` secondary ticket directly below the red / state ticket, visibly separated from the prose paper, and the validation set should include one open-popover screenshot.
- The open `任务情报` popover shows 2-3 read-only task preview rows and no task operation controls.
- Right dossier body written only as one continuous selected-region introduction paragraph; no task summary, region-intel tiles, file-update rows, warning cards, or material lists are allowed in that body paper.
- Bottom ticker using clickable detail lanes such as `地区情报 / 档案更新 / 地区预警`, not a repeated `任务小结` lane.

The draft should validate structure and art language only. It must not bake readable UI text, Chinese, English labels, numbers, region names, task names, button labels, fake pin labels, fake status chips, fake tooltips, or fake task cards.

Keep the existing approved world-map direction: bright modern ivory paper, strong pixel-print texture, low-poly faceted paper world map, deep navy editorial board, red-orange anomaly marks, and restrained cyan signal marks. Do not redesign the central map base into a new visual theme.

All dynamic content areas must be clean, orthographic, low-noise `content_rects`. Tabs, clips, screws, folds, bookmarks, side color strips, arrows, halftone clusters, crop marks, paper edges, strong borders, decorative protrusions, icon plates, and warning stripes must remain outside text-safe zones.

Interactive elements must be separable assets or state atlases: map pins, selected rings, hover labels, CTA plate, ticker lanes, region cards, tabs, and status badges. The central map board may contain only map material, grid, paper facets, and low-weight decorative print marks.

## 10. Acceptance

- A 5-second static screenshot must communicate: current selected region, whether it can be entered, what urgent state exists, and where to click next.
- The top strip must show all five macro attributes together: 公信 / 诡名 / 声望 / 守序 / 狂性. It must not replace them with `全球频道`, `素材`, `阶段：取材`, or standalone `声望`; `狂性` must render fully. The macro group must use a visibly different `世界状态` badge-rail / meter-rail grammar from the week/day paper tickets.
- The left region card must show difficulty + recommendation as region-level entry advice, not task objective counters.
- The selected-region title area may show difficulty + recommendation badges, but those badges must not compete with the primary CTA.
- The right dossier must reserve a visible image / region-identity area and one single intro prose body before any footer note. That body paper must contain only the selected-region text introduction.
- The `查看任务情报 · N` ticket must sit directly below the red / state ticket, remain visually secondary, and open a read-only popover. It must have independent button affordance and must not read as the title bar of the prose paper below it. The popover must not contain task selection, dispatch, dice, success rate, or editable controls.
- The primary CTA must use the fixed label `进入选定地区` or an equivalent fixed action phrase. It must not include the selected region name, task name, red-line name, or dispatch target.
- The bottom ticker must read as low-weight clickable detail entrances: `地区情报`, `档案更新`, `地区预警` or equivalent. The third lane is the entry-impact / warning slot for possible punishment, debuff, lock, fatigue, reputation loss, or other region consequences. It must not become a tutorial prompt, task progress bar, filter bar, duplicate current-region display, or second task-summary lane.
- No full task list, staff cards, dice pool, success rate, next-day control, or long action log appears on this screen.
- Left index, map pin, right dossier, CTA, and ticker all point to the same selected region.
- Screenshots must include whole screen, safe-zone overlay, and 100% crops of left card, map pin, right dossier, CTA, and ticker.
- This contract must pass before any style draft becomes a component production source.
