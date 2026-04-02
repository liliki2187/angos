# Systems Index: Angus / 《世界未解之谜周刊》

> **Status**: Draft
> **Created**: 2026-03-31
> **Last Updated**: 2026-03-31
> **Source Concept**: design/gdd/game-concept.md

---

## Overview

Angus is a weekly management loop built around a narrow but tightly connected chain: maintain a persistent newspaper state, dispatch staff into mystery nodes, resolve expeditions through split event checks, convert results into publishable stories, assemble a six-slot issue, and settle the consequences into next week's conditions. The highest-value systems are the ones that keep this chain readable and maintainable in Godot. Anything that sits outside that loop is secondary until the MVP is stable.

---

## Systems Enumeration

| # | System Name | Category | Priority | Status | Design Doc | Depends On |
|---|-------------|----------|----------|--------|------------|------------|
| 1 | Weekly Run Loop and State | Core | MVP | Drafted | design/gdd/weekly-run-loop.md | -- |
| 2 | Region and Node Availability | Gameplay | MVP | Drafted | design/gdd/exploration-and-node-dispatch.md | Weekly Run Loop and State |
| 3 | Staff Dispatch and Attribute Aggregation | Gameplay | MVP | Drafted | design/gdd/exploration-and-node-dispatch.md | Weekly Run Loop and State |
| 4 | Event Check Resolution | Gameplay | MVP | Drafted | design/gdd/event-check-resolution.md | Staff Dispatch and Attribute Aggregation |
| 5 | Clue Inventory and Story Conversion (inferred) | Gameplay | MVP | Not Started | -- | Event Check Resolution, Weekly Run Loop and State |
| 6 | Editorial Layout and Slot Assignment | Gameplay | MVP | Drafted | design/gdd/editorial-layout-and-settlement.md | Clue Inventory and Story Conversion |
| 7 | Issue Settlement and Subscription Economy | Economy | MVP | Drafted | design/gdd/editorial-layout-and-settlement.md | Editorial Layout and Slot Assignment, Weekly Run Loop and State |
| 8 | Macro Attributes and Unlock Pressure (inferred) | Progression | MVP | Not Started | -- | Weekly Run Loop and State, Issue Settlement and Subscription Economy |
| 9 | Menus and Scene Navigation | UI | Vertical Slice | Implemented | -- | Weekly Run Loop and State |
| 10 | Feedback, Logging, and Forecast UI (inferred) | UI | Vertical Slice | Not Started | -- | Event Check Resolution, Editorial Layout and Slot Assignment |
| 11 | Content Data and Config Pipeline | Core | Vertical Slice | Not Started | -- | Weekly Run Loop and State |
| 12 | Narrative/Faction Event Layer | Narrative | Alpha | Not Started | -- | Macro Attributes and Unlock Pressure, Content Data and Config Pipeline |
| 13 | Save/Load and Profile Persistence | Persistence | Alpha | Not Started | -- | Weekly Run Loop and State |
| 14 | Onboarding and Tutorialization | Meta | Vertical Slice | Not Started | -- | Menus and Scene Navigation, Feedback, Logging, and Forecast UI |
| 15 | Story Synthesis Workbench | Gameplay | Full Vision | Deferred | -- | Clue Inventory and Story Conversion, Macro Attributes and Unlock Pressure |
| 16 | Accessibility and Presentation Polish | Meta | Full Vision | Not Started | -- | Feedback, Logging, and Forecast UI |

---

## Categories

| Category | Description | Typical Systems |
|----------|-------------|-----------------|
| **Core** | Foundation systems everything depends on | State loop, config pipeline |
| **Gameplay** | The systems that make the weekly loop interactive | Dispatch, checks, clue conversion, layout |
| **Progression** | How the paper changes over time | Macro attributes, unlock pressure, long-term drift |
| **Economy** | Resource creation and consumption | Settlement, subscriptions, profit |
| **Persistence** | Save state and continuity | Save/load, profile continuity |
| **UI** | Player-facing information displays | Menus, forecasts, result panels |
| **Narrative** | Story and event delivery | Factions, event chains, unlock text |
| **Meta** | Systems outside the core loop | Onboarding, accessibility, polish |

---

## Priority Tiers

| Tier | Definition | Target Milestone | Design Urgency |
|------|------------|------------------|----------------|
| **MVP** | Required for the core loop to function | First stable Godot week loop | Design first |
| **Vertical Slice** | Required for a clearer, pitchable, more maintainable demo | Internal vertical slice | Design second |
| **Alpha** | Expands long-term structure and content breadth | Alpha | Design third |
| **Full Vision** | High-scope additions and polish | Beta / Release | Design as needed |

---

## Dependency Map

### Foundation Layer (no dependencies)

1. **Weekly Run Loop and State** -- owns week boundaries, shared variables, phase transitions, and cross-week persistence rules.

### Core Layer (depends on foundation)

1. **Region and Node Availability** -- depends on: Weekly Run Loop and State
2. **Staff Dispatch and Attribute Aggregation** -- depends on: Weekly Run Loop and State
3. **Content Data and Config Pipeline** -- depends on: Weekly Run Loop and State
4. **Menus and Scene Navigation** -- depends on: Weekly Run Loop and State
5. **Macro Attributes and Unlock Pressure** -- depends on: Weekly Run Loop and State, Issue Settlement and Subscription Economy

### Feature Layer (depends on core)

1. **Event Check Resolution** -- depends on: Staff Dispatch and Attribute Aggregation
2. **Clue Inventory and Story Conversion** -- depends on: Event Check Resolution, Weekly Run Loop and State
3. **Editorial Layout and Slot Assignment** -- depends on: Clue Inventory and Story Conversion
4. **Issue Settlement and Subscription Economy** -- depends on: Editorial Layout and Slot Assignment, Weekly Run Loop and State
5. **Narrative/Faction Event Layer** -- depends on: Macro Attributes and Unlock Pressure, Content Data and Config Pipeline

### Presentation Layer (depends on features)

1. **Feedback, Logging, and Forecast UI** -- depends on: Event Check Resolution, Editorial Layout and Slot Assignment
2. **Onboarding and Tutorialization** -- depends on: Menus and Scene Navigation, Feedback, Logging, and Forecast UI

### Polish Layer (depends on everything)

1. **Save/Load and Profile Persistence** -- depends on: Weekly Run Loop and State, Content Data and Config Pipeline
2. **Story Synthesis Workbench** -- depends on: Clue Inventory and Story Conversion, Macro Attributes and Unlock Pressure
3. **Accessibility and Presentation Polish** -- depends on: Feedback, Logging, and Forecast UI

---

## Recommended Design Order

| Order | System | Priority | Layer | Agent(s) | Est. Effort |
|-------|--------|----------|-------|----------|-------------|
| 1 | Weekly Run Loop and State | MVP | Foundation | game-designer + gameplay-programmer | M |
| 2 | Region and Node Availability | MVP | Core | game-designer | M |
| 3 | Staff Dispatch and Attribute Aggregation | MVP | Core | game-designer | S |
| 4 | Event Check Resolution | MVP | Feature | game-designer + systems-designer | M |
| 5 | Clue Inventory and Story Conversion | MVP | Feature | game-designer | M |
| 6 | Editorial Layout and Slot Assignment | MVP | Feature | game-designer + ux-designer | M |
| 7 | Issue Settlement and Subscription Economy | MVP | Feature | economy-designer + systems-designer | L |
| 8 | Macro Attributes and Unlock Pressure | MVP | Core | game-designer | M |
| 9 | Content Data and Config Pipeline | Vertical Slice | Core | gameplay-programmer | L |
| 10 | Feedback, Logging, and Forecast UI | Vertical Slice | Presentation | ux-designer + ui-programmer | M |
| 11 | Menus and Scene Navigation | Vertical Slice | Core | ui-programmer | S |
| 12 | Onboarding and Tutorialization | Vertical Slice | Presentation | game-designer | S |
| 13 | Save/Load and Profile Persistence | Alpha | Polish | gameplay-programmer | M |
| 14 | Narrative/Faction Event Layer | Alpha | Feature | narrative-director + game-designer | L |
| 15 | Story Synthesis Workbench | Full Vision | Polish | game-designer | L |
| 16 | Accessibility and Presentation Polish | Full Vision | Polish | ux-designer | M |

---

## Circular Dependencies

- **Potential cycle: Macro Attributes and Unlock Pressure <-> Narrative/Faction Event Layer**. Resolve by making macro attributes the source state and letting the narrative layer only read and emit scripted mutations through explicit events.
- **Potential cycle: Content Data and Config Pipeline <-> Narrative/Faction Event Layer**. Resolve by defining the data schema first and keeping narrative content as consumers of the schema.

---

## High-Risk Systems

| System | Risk Type | Risk Description | Mitigation |
|--------|-----------|-----------------|------------|
| Weekly Run Loop and State | Technical | Current behavior is concentrated in a monolithic scene script | Extract state ownership and document interfaces before adding content |
| Issue Settlement and Subscription Economy | Design | Multipliers may produce opaque or dominant strategies | Prototype balance changes and document tuning ranges |
| Content Data and Config Pipeline | Scope | Hardcoded content will slow every future iteration | Move nodes, regions, and story templates toward data assets early |
| Story Synthesis Workbench | Scope | Design exists in docs but not in Godot MVP; easy to reintroduce too early | Keep deferred until the core loop is stable and documented |

---

## Progress Tracker

| Metric | Count |
|--------|-------|
| Total systems identified | 16 |
| Design docs started | 4 |
| Design docs reviewed | 0 |
| Design docs approved | 0 |
| MVP systems designed | 4/8 |
| Vertical Slice systems designed | 0/4 |

---

## Next Steps

- [ ] Review and approve this systems enumeration
- [ ] Draft or refine `Clue Inventory and Story Conversion`
- [ ] Draft `Macro Attributes and Unlock Pressure`
- [ ] Create the config-pipeline ADR-backed implementation plan
- [ ] Run focused design review on the drafted MVP GDDs
