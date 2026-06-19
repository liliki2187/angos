# World Map v7 Filled-State Text Mock Prompt

> Status: 2026-06-17 historical P0/P1 functional parity visual target prompt. Superseded by A77 for the next world-map target.  
> Historical output: `docs/screenshots/2026-06-17-world-map-v7-p0p1-real-info-style-draft/01-world-map-v7-p0p1-real-info-text-mock.png`  
> Rule: this is a target screenshot / visual-density reference only. It must not be used as a production PNG or cut-up UI asset.
> Current prompt: `docs/plans/world-map-imagegen-v7/difficulty-rating-task-intel-popover-prompt.md`.

## Purpose

The filled-state text mock tests:

- whether the v7 functional layout can hold real Chinese copy;
- whether information density feels like a shipped game screenshot;
- whether text, cards, dossier, CTA, ticker, and map state read as one visual system;
- whether the P0 loop is visible: selected region -> dossier refresh -> enterable / blocked state -> enter selected region;
- whether P1 region-level summaries are restored without turning the world map into a task board;
- what Godot typography / color / hierarchy should attempt to reproduce dynamically.

It is intentionally allowed to include baked text because it is not a runtime asset.

## Supersession Note - A77

This prompt restored the older web prototype's task-pool counters as a compact world-map summary. After the 2026-06-17 UX / UI review, that direction was revised:

- left region cards now show region-level `难度` and `推荐`, not task-pool counters;
- the selected-region title area may repeat `难度` / `推荐` as confirmation;
- task-pool preview moves behind a right-side secondary `任务情报` ticket;
- the `任务情报` popover is read-only and must not include task selection, dispatch, staff, dice, success rate, or full task details.

Use `difficulty-rating-task-intel-popover-prompt.md` for new Image 2 target mocks.

## Filled State

```text
Selected region: 北美禁区带
State: 红线升温 + 可进入
Remaining days: 7 天
Counts: 线报 4 / 红线 1 / 青线 1
Region-level summary: 可见目标 2 / 限时机会 1 / 线索 2 / 深度链 1
Main action: 进入选定地区

Top status must show two distinct visual grammars: left weekly clock paper tickets, right world-state badge rail. It must show week, remaining days, and all five macro attributes together:
公信 / 诡名 / 声望 / 守序 / 狂性.

Do not use top-strip space for 全球频道, 素材, or 阶段：取材. Do not show 声望 alone; it is only valid as one of the five macro attributes. Reserve enough width so the last macro chip 狂性 11 is fully visible and not cropped.
The five macro attributes must NOT use the same white paper-ticket frame as 探索周 / 剩余天数. They should read as a low-weight 世界状态 badge rail / meter rail / signal-light strip, with weak backing, small badge marks, subtle ticks or lamps, and no full outer paper card frame.
```

P0/P1 requirements for this mock:

```text
The same selected region must be readable in five places:
1. selected left region card;
2. selected North America map pin / ring;
3. right selected-region dossier title and facts;
4. primary CTA state;
5. bottom ticker receipts.

The left index must visibly separate enterable regions from locked regions. At least one locked region should show a short blocker, such as 声望 31/40 or 缺青线 1. It should look informational, not clickable.

The right dossier for the selected enterable region must include compact region-level summary chips:
目标 2 / 限时 1 / 线索 2 / 深链 1

The right dossier preview rows must be real region intel, not legend or tutorial copy.

Do not restore low-priority items in this mock: no topic filter, no long action log, no full task list, no staff, no dice, no success rate, no next-day control.
```

## Prompt

```text
Create a P0/P1 functional-parity filled-text visual mock based on the v7 world-map functional style draft structure: deep navy editorial board, bright modern ivory printed paper, strong pixel-print texture, low-poly faceted paper world map, left region index, central map board, right selected-region dossier, separate red primary CTA plate, top status strip, bottom ticker.

Important purpose:
- This is NOT production asset art. It is a filled-state screenshot target to evaluate how real Chinese UI text, information density, hierarchy, and typography feel when integrated with the art.
- It must visibly repair P0/P1 issues from the previous v4 target: selected-state linkage, enterability, locked-region blocker, region-level summary, real region intel, and coherent bottom receipts.
- Render the text as clean modern Chinese UI typography that looks printed/inked onto the paper objects, not floating labels.
- Keep the same Angus style: modern supernatural weekly magazine, high-end pixel-print material, deep navy, bright ivory paper, red-orange urgency, restrained cyan signal marks.

Functional state:
- Current selected region: 北美禁区带
- Status: 红线升温, 可进入
- Remaining days: 7 天
- Region counts: 线报 4, 红线 1, 青线 1
- Region summary: 可见目标 2, 限时机会 1, 线索 2, 深度链 1
- Page only chooses a region and enters it. Do not show staff, dice, success rate, next-day controls, or full task list.
- Right dossier must include a region image / identity area, one compact task-overview ticket, and body sections for region understanding: 地区特征, 本周异变, 可带回素材, and optional 地区预警 / 编辑价值. Do not repeat task counters in the body.
- Primary CTA must use a fixed action label: 进入选定地区. Do not put 北美禁区带 or any dynamic region name in the CTA label.
- Bottom ticker is low-weight world-map feedback only. It must not look like a task progress bar, filter bar, tutorial prompt, duplicate current-region display, or second task-summary lane. Use feedback lane roles such as 最新记录, 档案更新, 地区预警.
- The whole screenshot must communicate that the current selection is 北美禁区带 across left card, map pin, right dossier, CTA, and bottom ticker.

Top status strip:
- 探索周 01
- 剩余 7 天
- Small low-weight label near the macro rail: 世界状态
- 公信 42
- 诡名 18
- 声望 31
- 守序 26
- 狂性 11

Top strip visual grammar:
- Left side: `探索周 01` and `剩余 7 天` are weekly clock paper tickets, matching the current ivory paper ticket style.
- Right side: the five macro attributes are a separate `世界状态` badge rail, not paper tickets. Use a darker navy backing, subtle etched line, tiny status lamps / small stamp marks / micro tick bars, lighter border, and lower visual weight.
- Keep a clear gap or thin rivet divider between weekly clock tickets and the world-state badge rail.
- Do not use strong vertical table lines between macro attributes. Avoid making them look like a resource bar, task counters, buttons, or the same kind of paper fields as week/day.
- Normal macro numbers should use unified dark ink. Do not color only `公信 42` red unless it has an explicit warning/change marker.

Left region index:
Card 1 selected, red emphasis:
- 北美禁区带
- 红线升温  剩 7 天
- 目标 2 / 限时 1
- 线索 2 / 深链 1

Card 2 locked / muted:
- 东亚神秘地带
- 锁定  声望 31/40
- 缺青线 1

Card 3 muted cyan:
- 太平洋失航带
- 可进入  普通线报
- 目标 1 / 线索 1

Card 4 locked / muted red-gray:
- 南美红线档
- 封存  许可不足
- 需要完成复核

Central map:
- Show North America selected using a red/cyan pin, selected ring, and route emphasis.
- Do not place long labels over the map. A tiny short tag near North America may say: 北美
- Other pins are muted and unlabeled.
- Locked pins should look ghosted or sealed, not equally clickable.

Right selected-region dossier:
Fixed slot label:
- 选定地区

Title:
- 北美禁区带

Region intro, two lines:
- 北美频道持续传回重复目击，城市边缘的同一新闻
- 在不同报纸上提前出现。

Badges:
- 红线升温
- 可进入

Compact task-overview ticket, one row only:
- 目标 2
- 限时 1
- 线索 2
- 深链 1

Current state / status ticket:
- 本周取材区已打开。

Region body sections:
- 地区特征：都市传说与军事封锁交叠。
- 本周异变：红线升温，异常信号增强。
- 可带回素材：目击证词 / 封锁传闻 / 异常广播。

Enter condition:
- 进入后选择具体线报。

Footer:
- 进入地区，本屏不消耗天数。

Primary CTA plate:
- 进入选定地区

Bottom ticker:
- 最新记录：北美禁区带红线升温
- 档案更新：该区新增目击材料
- 地区预警：进入暂无惩罚

Typography and readability:
- Use clear, high-quality Chinese UI lettering. Text should be sharp and legible at screenshot scale.
- Do not use tiny unreadable text. Avoid overly bold black text everywhere; use hierarchy: titles larger, body medium, meta smaller.
- Text must stay inside paper content areas, with comfortable padding from tabs, screws, crop marks, halftone dots, stripes, colored side tabs, and paper edges.
- Keep the CTA label centered vertically and horizontally in the clean label area; do not let it touch the bottom stripe or screws.
- The CTA label is fixed UI copy and must not include the selected region name.
- Bottom ticker labels should read as feedback receipts, not as selectable filters, task progress bars, tutorial prompts, a second current-region display, or repeated task-summary counters.
- The third bottom lane is a region warning / entry impact slot. It may show no penalty in this state (`进入暂无惩罚`), but in other states it may carry punishments or debuffs.
- Locked left cards must look less actionable than the selected enterable card: lower contrast, sealed/lock icon, no bright CTA affordance.
- Do not make the four summary chips look like concrete task cards. They are compact region-level counters only.

Avoid:
- old newspaper, yellowed archive, parchment, dirty paper, glass SaaS panels, cyberpunk holograms, generic mobile game UI.
- broken Chinese, random pseudo text, gibberish, extra fake labels, extra English headings, watermark, signature.
- putting full task cards, staff cards, dice, success rates, next-day button, or long logs on this screen.
```
