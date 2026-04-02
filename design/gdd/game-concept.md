# Game Concept: Angus / 《世界未解之谜周刊》

*Created: 2026-03-31*
*Status: Draft*

---

## Elevator Pitch

> It's a single-player weekly management strategy game where you run an occult newspaper, dispatch reporters into dangerous mystery sites, turn clues into publishable stories, lay out a six-slot issue, and steer the paper's credibility, reputation, and obsession with the unknown from week to week.

---

## Core Identity

| Aspect | Detail |
| ---- | ---- |
| **Genre** | Single-player management strategy + narrative investigation + newspaper simulation |
| **Platform** | PC first in Godot 4.3; HTML prototypes are reference-only |
| **Target Audience** | Mid-core players who enjoy occult themes, system-driven strategy, and readable session arcs |
| **Player Count** | Single-player |
| **Session Length** | 30-60 minutes for 1-3 in-game weeks |
| **Monetization** | None yet; internal prototype |
| **Estimated Scope** | Medium for MVP-to-vertical-slice, large for full vision |
| **Comparable Titles** | News Tower, Cultist Simulator, The Sultan's Game |

---

## Core Fantasy

You are not a field investigator or a heroic adventurer. You are the editor responsible for deciding which mysteries deserve resources, which truths should be amplified, and how much corruption, spectacle, or credibility the paper is willing to absorb in exchange for growth.

The fantasy is to feel like the mind behind a dangerous publication: making risky editorial bets, sensing that every expedition can reshape the paper's public identity, and watching one issue's choices ripple into the next week's opportunities and dangers.

---

## Unique Hook

This is a newspaper management game where the content pipeline starts with occult field dispatch, resolves through split binomial event checks, and only becomes publishable after surviving editorial tradeoffs. It is not just "run a newspaper" and not just "investigate mysteries"; the distinctive hook is that investigation quality and editorial positioning are part of the same weekly risk loop.

---

## Player Experience Analysis (MDA Framework)

### Target Aesthetics (What the player FEELS)

| Aesthetic | Priority | How We Deliver It |
| ---- | ---- | ---- |
| **Sensation** (sensory pleasure) | 6 | Moody UI, occult newspaper presentation, dice and result feedback |
| **Fantasy** (make-believe, role-playing) | 2 | Acting as editor-in-chief of a paranormal weekly |
| **Narrative** (drama, story arc) | 4 | Every week becomes a self-contained editorial story with consequences |
| **Challenge** (obstacle course, mastery) | 3 | Limited days, team composition, risk management, slot optimization |
| **Fellowship** (social connection) | N/A | Single-player prototype |
| **Discovery** (exploration, secrets) | 1 | Region unlocks, hidden nodes, occult pressure, clue quality variance |
| **Expression** (self-expression, creativity) | 5 | Editorial profile, issue composition, topic bias |
| **Submission** (relaxation, comfort zone) | 7 | Readable weekly loop and strong structure, but not a cozy game |

### Key Dynamics (Emergent player behaviors)

- Players compare short-term odds against long-term identity growth, choosing whether to chase safer credible stories or stranger high-risk ones.
- Players naturally optimize expedition staff compositions and region choices as they learn how clue quality converts into issue value.
- Players form an editorial style over time because layout, balance, and thematic bias all feed back into subscriptions and macro attributes.

### Core Mechanics (Systems we build)

1. Weekly state loop with cross-week persistence.
2. Region/node dispatch with staff selection and day consumption.
3. Split binomial event checks with opponent negation.
4. Clue-to-story conversion and six-slot editorial layout.
5. Economic settlement that updates subscriptions, editorial profile, and macro attributes.

---

## Player Motivation Profile

### Primary Psychological Needs Served

| Need | How This Game Satisfies It | Strength |
| ---- | ---- | ---- |
| **Autonomy** (freedom, meaningful choice) | Choose regions, staff, risk appetite, story mix, and issue bias every week | Core |
| **Competence** (mastery, skill growth) | Learn probabilities, optimize dispatch composition, and shape profitable balanced issues | Core |
| **Relatedness** (connection, belonging) | Build attachment to the paper, its staff roles, and the world reacting to editorial direction | Supporting |

### Player Type Appeal (Bartle Taxonomy)

- [x] **Achievers** (goal completion, collection, progression) -- How: unlock regions, improve subscriptions, stabilize profitable weekly issues
- [x] **Explorers** (discovery, understanding systems, finding secrets) -- How: hidden nodes, macro-attribute thresholds, occult progression
- [ ] **Socializers** (relationships, cooperation, community) -- How: not a current focus in the single-player MVP
- [ ] **Killers/Competitors** (domination, PvP, leaderboards) -- How: not a current focus

### Flow State Design

- **Onboarding curve**: Start with a small staff pool, one open region, and a fixed week loop that teaches dispatch, check, layout, and settlement in order.
- **Difficulty scaling**: Expand through harder nodes, stricter resource tradeoffs, stronger risk flags, and more punishing editorial imbalance.
- **Feedback clarity**: Show probabilities before dispatch, clue quality after checks, and real-time settlement forecasts during layout.
- **Recovery from failure**: A failed week should still produce readable output and allow fast transition into the next week rather than hard fail states.

---

## Core Loop

### Moment-to-Moment (30 seconds)

The player reads node requirements, picks staff, inspects success odds, commits a dispatch, then evaluates the resulting clue or failure outcome. In the editorial half, the player picks a story and places it into a slot while watching the issue forecast update.

### Short-Term (5-15 minutes)

The player spends a week budget by chaining 2-4 expeditions, converts clues into a usable story pool, fills six issue slots, and settles one complete paper. This is the "one more week" loop.

### Session-Level (30-120 minutes)

A session consists of several consecutive weekly issues. Each week creates a new editorial bet, new unlock pressure, and new macro-state consequences, giving the player natural stop points after settlement and natural return hooks at the next briefing.

### Long-Term Progression

Long-term growth comes from subscriptions, editorial profile drift, macro-attribute changes, unlocked regions/nodes, and future faction or occult event chains. The intended longer arc is to evolve the paper from a fringe publication into a powerful but unstable force.

### Retention Hooks

- **Curiosity**: Hidden nodes, unlock conditions, and unresolved world mysteries
- **Investment**: Cross-week subscriptions, macro attributes, and editorial identity
- **Social**: Not part of current MVP
- **Mastery**: Better staff assignment, cleaner layout composition, and more deliberate long-term profile shaping

---

## Game Pillars

### Pillar 1: Investigation Must Feed Publication

Every field action must either create publishable material, deny it, or distort it in a way the paper feels next.

*Design test*: If a feature is fun in isolation but does not affect the week's issue, it should not block MVP.

### Pillar 2: Editorial Tradeoffs Must Stay Visible

The player should always feel the tension between credibility, weirdness, profit, and long-term identity.

*Design test*: If a rule removes the need to choose between safer and stranger outcomes, it weakens the game.

### Pillar 3: One Week Should Form One Readable Arc

Each week must be understandable as a complete cycle: briefing, dispatch, issue assembly, settlement, next week.

*Design test*: If a system cannot express value within a week or feed into the next week, defer it.

### Anti-Pillars (What This Game Is NOT)

- **NOT an open-world adventure game**: Direct field movement and exploration scenes would dilute the editor fantasy and blow scope.
- **NOT a pure deckbuilder or card battler**: Cards can exist as content containers, but the core loop is editorial management, not combat or deck optimization.
- **NOT a content-bloat narrative sandbox for MVP**: Faction branches, broad story synthesis trees, and deep progression should not delay the weekly Godot loop.

---

## Inspiration and References

| Reference | What We Take From It | What We Do Differently | Why It Matters |
| ---- | ---- | ---- | ---- |
| **News Tower** | Newspaper production fantasy and publication framing | We attach issue quality to mystery investigation, not newsroom throughput alone | Validates the editorial-management appeal |
| **Cultist Simulator** | Occult pressure, dangerous knowledge, escalating instability | We structure it into readable weekly runs and explicit issue settlement | Validates the occult-management mood |
| **The Sultan's Game** | Binomial-style resolution feel and visible risk math | We use it as expedition resolution inside a broader newspaper loop | Validates the check model and tension |

**Non-game inspirations**: Paranormal tabloids, conspiracy newspapers, occult pulp magazines, Cold War mystery fiction, UFO folklore, and periodical front-page design.

---

## Target Player Profile

| Attribute | Detail |
| ---- | ---- |
| **Age range** | 18-40 |
| **Gaming experience** | Mid-core to hardcore systems players |
| **Time availability** | 30-60 minute focused sessions on weekdays; longer experimentation on weekends |
| **Platform preference** | PC |
| **Current games they play** | News Tower, Cultist Simulator, deckbuilders or management sims with strong thematic identity |
| **What they're looking for** | A compact strategic loop with strong theme, readable consequences, and meaningful medium-term planning |
| **What would turn them away** | Excessive randomness without agency, weak payoff from investigation, or a purely cosmetic newspaper phase |

---

## Technical Considerations

| Consideration | Assessment |
| ---- | ---- |
| **Recommended Engine** | Godot 4.3, because the team already has a live prototype and the project is UI-heavy rather than engine-technology heavy |
| **Key Technical Challenges** | Extracting monolithic weekly logic into maintainable systems, converging HTML reference rules into Godot, and building a content/config pipeline |
| **Art Style** | 2D stylized UI-forward prototype with occult newspaper presentation |
| **Art Pipeline Complexity** | Medium; interface-heavy with bespoke print presentation and reference-driven atmosphere |
| **Audio Needs** | Moderate; mood, feedback, and result emphasis matter more than reactive score complexity |
| **Networking** | None |
| **Content Volume** | MVP: 2 regions, a small node set, 1 full weekly loop; vertical slice: broader region variety, unlock chains, richer story pool |
| **Procedural Systems** | Light procedural or semi-random briefing, filler story generation, and weekly node refresh |

---

## Risks and Open Questions

### Design Risks

- The loop may feel too abstract if dispatch and issue outcomes do not create strong emotional contrast.
- The editorial phase may become a solved optimization puzzle if diversity and bias multipliers dominate too heavily.

### Technical Risks

- Current weekly logic is concentrated in a single Godot scene script, which will make iteration brittle.
- Data definitions for regions, nodes, and story generation remain embedded in code rather than stable content assets.

### Market Risks

- The concept is niche and relies heavily on strong thematic execution.
- Players may understand the newspaper fantasy faster than they understand why the occult layer matters unless onboarding is sharp.

### Scope Risks

- Reintroducing story synthesis, faction branches, or large content sets too early will split the prototype again.
- UI polish can absorb time before the content and state architecture are stable.

### Open Questions

- Does the current clue-to-story conversion have enough expressive depth, or will a later synthesis layer be required for retention?
- How aggressively should macro attributes unlock or distort weekly content before the game stops feeling readable?

---

## MVP Definition

**Core hypothesis**: Players will enjoy a weekly loop where risky occult investigation choices directly create editorial tradeoffs that affect profit, subscriptions, and long-term paper identity.

**Required for MVP**:
1. A playable Godot week loop with state persistence across weeks.
2. Region/node dispatch with 1-3 staff selection and split event checks.
3. Clue generation, automatic story conversion, six-slot layout, and settlement.
4. Cross-week updates to subscriptions, editorial profile, and macro attributes.

**Explicitly NOT in MVP** (defer to later):
- Story synthesis workbench as a separate Godot phase
- Deep faction mission chains
- Large-scale save/load or release-grade meta systems
- High-cost art polish or multiple alternate rule branches

### Scope Tiers (if budget/time shrinks)

| Tier | Content | Features | Timeline |
| ---- | ---- | ---- | ---- |
| **MVP** | 2 regions, limited node pool, 1 stable weekly loop | Dispatch, checks, clue conversion, six-slot settlement | 3-6 weeks of focused prototype cleanup and documentation-driven implementation |
| **Vertical Slice** | More region/node variety, clearer unlocks, improved UI feedback | Better onboarding, stronger progression, config-driven content | 6-10 additional weeks |
| **Alpha** | Most intended systems present in rough form | Factions, persistence, event layering, broader content | Dependent on team bandwidth |
| **Full Vision** | Content-complete and polished | Story synthesis, long-term growth layers, polish, balancing | Post-Alpha |

---

## Next Steps

- [ ] Approve this concept as the canonical Godot direction
- [ ] Use `design/gdd/game-pillars.md` as the decision filter for future scope calls
- [ ] Maintain `design/gdd/systems-index.md` as the source of truth for what gets designed next
- [ ] Design or revise the MVP system GDDs in dependency order
- [ ] Execute ADR-driven refactors before content expansion
- [ ] Prototype only the highest-risk unresolved system, not broad new branches
