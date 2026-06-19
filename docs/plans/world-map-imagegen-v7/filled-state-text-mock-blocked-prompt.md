# World Map v7 Blocked-State Text Mock Prompt

> Status: 2026-06-17 historical P0/P1 blocked-state companion prompt. Superseded by A77 for the next world-map target.  
> Output: `docs/screenshots/2026-06-17-world-map-v7-p0p1-real-info-style-draft/02-world-map-v7-p0p1-blocked-state-text-mock.png`  
> Rule: this is a target screenshot / visual-density reference only. It must not be used as a production PNG or cut-up UI asset.

## Supersession Note - A77

This blocked-state companion uses the earlier P0/P1 field contract where left cards and the right dossier could expose task-pool counters. After A77, the current target is:

- left cards show region-level `难度` and `推荐`, not `目标 / 限时 / 线索 / 深链`;
- task-pool preview moves behind a secondary `任务情报` ticket / popover;
- the popover is read-only and cannot contain task selection, dispatch, staff, dice, or success rate.

Use `difficulty-rating-task-intel-popover-prompt.md` and `functional-layout-contract.md` for new style targets.

## Purpose

The ready-state text mock proves the selected enterable-region loop. This companion mock proves the locked-region loop:

```text
select locked region -> show blocked dossier -> explain unlock gap -> disable CTA
```

It must keep the same visual language and component proportions as the ready-state target, so the two images can guide one state matrix rather than two separate layouts.

## Filled State

```text
Selected region: 东亚神秘地带
Availability: 锁定 / 暂不可进入
Unlock gap: 声望 31/40 / 缺青线 1
CTA: 暂不可进入
Bottom feedback lanes: 最新记录 / 档案更新 / 地区预警
```

## Prompt Summary

```text
Create the locked/blocked selected-state companion mock for the Angus world map v7 UI.

Keep the same full-screen 1920x1080 layout, deep navy editorial board, bright clean ivory paper, strong pixel-print texture, low-poly faceted paper world map, left region index, central map board, right selected-region dossier, red CTA plate, top status strip, and bottom ticker from the P0/P1 ready-state mock.

Top status strip remains:
- 探索周 01
- 剩余 7 天
- 世界状态
- 公信 42 / 诡名 18 / 声望 31 / 守序 26 / 狂性 11

Left region index:
- 北美禁区带: enterable but not selected, 红线升温, 目标 2 / 限时 1, 线索 2 / 深链 1
- 东亚神秘地带: selected locked, 锁定, 声望 31/40, 缺青线 1
- 太平洋失航带: enterable, 普通线报, 目标 1 / 线索 1
- 南美红线档: locked, 许可不足, 需要完成复核

Central map:
- East Asia selected with ghosted locked pin, sealed ring, and short tag 东亚.
- North America remains enterable but not selected.

Right blocked dossier:
- Slot label: 选定地区
- Title: 东亚神秘地带
- Intro: 东亚频道只回传残缺剪影，神秘地带仍被封存。 / 需要补足声望与青线证据后开放。
- Badges: 锁定 / 暂不可进入
- Summary: 声望 31/40 / 缺青线 1 / 目标 ? / 线索 ?
- Current state: 本周无法进入该地区。
- Blocked reason: 声望未达开放阈值。 / 需要完成 1 条青线追踪。
- Enter condition: 解锁后才能选择具体线报。
- Footer: 当前选择不会消耗天数。

CTA:
- 暂不可进入
- Must look disabled but readable.

Bottom ticker:
- 最新记录：东亚频道仍被封存
- 档案更新：缺少青线追踪证据
- 地区预警：暂不可进入

Do not show full task cards, staff, dice, success rate, next-day control, topic filters, or long action logs.
Use sharp modern Chinese UI typography. Keep all text inside clean paper content areas and away from tabs, screws, stripes, crop marks, halftone, and paper edges.
```
