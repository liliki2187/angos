# World Map B7 Branch Filled Content Contract

> Date: 2026-06-22  
> Scope: `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/15-variant-b7-strict-color-match-pass.png`  
> Stage: real-content preview preparation after color/style lock  
> Artifact status: B7 is a `color-locked style draft`, not a production benchmark, not a no-text asset master, and not a component split source.

## 1. Stage Gate

The next asset-UI-chain step is:

```text
lightweight content contract
-> safe-zone / capacity validation preview
-> filled-state text mock
-> UI / UX / pixel-art review
```

Do not jump from B7 to component grouping, atlas, manifest, or slicing. Those are later stages and require a reviewed `filled-state text mock` first.

## 2. Page Responsibility

The world map screen answers one player decision:

```text
Choose a reporting region, understand whether the selected region can be entered, then enter that selected region.
```

It does not select a concrete task, assign staff, show dice, show success rate, advance the day, or execute dispatch signoff.

## 3. Validation State

Use one concrete filled state:

```text
North America quarantine zone selected + red-line heating + enterable.
```

This state must prove that one selected region drives:

- left index selected card
- central map pin / selected route cue
- right dossier title and state
- fixed CTA state
- bottom ticker receipts

At least one locked region must remain visible, so availability distance is tested in the same screen.

## 4. Real Content Set

### Top / Global Status

| Field | Text |
| --- | --- |
| Week | `探索周 01` |
| Days left | `剩余 5天` |
| World state rail | `公信 42 / 诡名 18 / 声望 12 / 守序 34 / 狂性 16` |

If B7 does not have enough top-strip structure, this content may be temporarily placed as low-weight status text in existing small technical slots for capacity validation. The final filled-state mock should create a proper grouped status rail.

### Left Region Index

| Region | State | Difficulty | Recommendation | Reason / Gap |
| --- | --- | --- | --- | --- |
| 北美禁区 | 已选 | 高 | 推荐 ★★★★★ | 红线升温 |
| 欧洲裂隙 | 可进入 | 中 | 推荐 ★★★ | 线索稳定 |
| 东亚镜像城 | 锁定 | 异常 | 推荐 ★★ | 公信 42/60 |
| 南美遗迹 | 可进入 | 高 | 推荐 ★★★★ | 截稿临近 |
| 非洲夜航线 | 可进入 | 中 | 推荐 ★★ | 素材稀少 |
| 南极静默区 | 锁定 | 未明 | 推荐 ★ | 需诡名 25 |

The selected card should be visibly different from normal and locked cards. The locked card must not read as an active enter button.

### Right Selected-Region Dossier

| Slot | Text |
| --- | --- |
| Fixed label | `选定地区` |
| Title | `北美禁区` |
| Badges | `难度 高` / `推荐 ★★★★★` |
| State ribbon | `红线升温 · 3天内进入收益最高` |
| Task-intel ticket | `查看任务情报 · 3` |
| Intro paragraph | `废弃广播塔持续复述同一段不存在的晨间新闻。当地封锁线外出现同步采访记录，三名目击者描述了同一位尚未出生的播报员。` |
| Footer / consequence | `进入后消耗 1 天，解锁区域任务台。` |
| Primary CTA | `进入选定地区` |

The dossier body is one continuous selected-region introduction only. It must not contain task lists, region-intel tiles, file-update rows, material lists, staff, dice, success rate, or dispatch controls.

### Bottom Ticker

| Lane | Text |
| --- | --- |
| 地区情报 | `北美封锁线出现重复采访` |
| 档案更新 | `镜像城解锁缺口更新` |
| 地区预警 | `红线升温，失败将损失公信` |

Ticker lanes are clickable read-only detail entrances. They are not task cards and not a second task-summary row.

### Lower-Right Device

2026-06-22 user revision, revised 2026-06-23: the world map **may** include `下一天 / 推进一天`, but only if it follows the region task board's bottom global schedule contract. The current region page places `推进一天` in the bottom global schedule strip with a separate `确认推进？` state. For the B7 branch, the accepted direction is a **left-bottom independent global schedule dock** under the region index, while the right dossier extends downward into the former lower-right machine area.

Therefore the B7 lower-right mechanical console must not independently become a time-advance control. Next mock direction:

- if the world map includes day advance, move / redesign it as the same bottom global schedule component used by the region page; in the B7 branch, anchor it as a left-bottom independent global schedule dock;
- keep the right dossier CTA focused on `进入选定地区`;
- keep `推进一天` separated from the right CTA with its own atlas / hit rect / state matrix and first-click confirming state;
- if the lower-right device remains outside the bottom schedule strip, remove the strong `>>` actuator or make it clearly decorative / disabled so it does not read as the day-advance action.

It must not use `结束探索周`, `进入结算`, or any other global phase-change wording in this filled-state pass unless the content contract explicitly adds that state. If it uses `下一天 / 推进一天`, it must be in the bottom schedule strip and carry confirmation behavior.

## 5. Safety / Capacity Checks

Before calling a result `filled-state text mock`, it must pass:

- 5-second read: selected region, urgent state, enterability, and primary action are visible without interaction.
- Region responsibility: no full task list, no staff, no dice; day advance is allowed only as a bottom global schedule component consistent with the region page. In B7, the current target is left-bottom independent schedule dock + extended right dossier.
- Lower-right device: if it is not the bottom schedule strip, it must not read as `下一天 / 推进一天`; if ambiguous, mark the mock as failed for function-role clarity.
- CTA wording: fixed action only; no region name in the button.
- Left cards: show difficulty + recommendation, not task-pool counters.
- Right dossier: one intro paragraph only; `查看任务情报 · 3` is an independent secondary ticket.
- Locked state: at least one locked region has a visible blocker and lower action affordance.
- Bottom ticker: three low-weight detail entrances, not duplicate task summary.
- Text safety: no text over tabs, clips, screws, arrows, folded corners, paper edges, strong halftone, or heavy texture.
- Color safety: any AI-regenerated version must re-run the B7 Color Contract Gate before it can be called color-matched.

## 6. Current Preview Rule

If the next local image is made by drawing text onto B7, label it:

```text
safe-zone / capacity validation preview
```

It can validate text capacity and hierarchy, but it is not the final `filled-state text mock`, not a production art source, and not a slicing source. A true `filled-state text mock` must visually integrate text, fields, paper, cards, state tickets, and CTA in one refined art pass or equivalent polish pass.

## 7. Capacity Validation Preview

Preview file:

- `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/17-b7-filled-content-capacity-validation.png`

Artifact type:

```text
safe-zone / capacity validation preview
```

This preview was made by locally overlaying the contract text onto B7. It proves only basic capacity and hierarchy. It is not the final `filled-state text mock`.

### 7.1 What Works

- The selected-region chain can be made visible: left selected card, map label, right dossier, CTA, and ticker all point to `北美禁区`.
- The right dossier can carry the essential sequence `title -> state ribbon -> 查看任务情报 · 3 -> intro -> CTA`.
- The B7 color-locked palette still works after adding real content; the screen does not immediately collapse into old yellow paper or over-white UI.
- The left stack can carry compact region-level `难度 / 推荐 / lock gap` fields if the copy stays short.

### 7.2 Exposed Risks

- **Top status rail is under-structured.** B7 does not currently provide a proper world-state rail. The temporary `世界状态` block is too small. A true filled-state mock must create a deliberate top status structure instead of hiding macro values in technical marks.
- **Right prose capacity is tight.** The dossier can fit a 3-line intro plus one short footer. The earlier 70-110 character v7 target may require a taller prose body, shorter media viewport, or clearer footer slot.
- **Bottom ticker titles must be short.** The current bottom cards fit short labels such as `封锁线重复采访`; longer 10-14 character titles need wider text slots or smaller type.
- **Persistent map labels create clutter.** Six always-visible map labels are useful for capacity testing but should not become the final world-map behavior. Production should show only selected / hover / urgent short labels.
- **Left index count conflicts with prior v7 contract.** B7 visually supports six cards, while v7 production had moved toward four visible cards. The next filled-state mock must decide whether the B7 branch intentionally keeps six compact cards or conforms back to four larger, safer cards.

### 7.3 Required Change Before True Filled-State Mock

The actual `filled-state text mock` brief should not simply ask the image model to "add these labels." It must ask for structural refinement:

- Add a real top status rail for week / days and grouped five macro attributes.
- Keep the right dossier sequence but reserve a cleaner prose body and footer.
- Compress bottom ticker copy or widen ticker text slots.
- Use map labels sparingly: selected, hover, urgent, or locked only.
- Keep B7's strict color contract and re-run color sampling after any AI-regenerated result.
