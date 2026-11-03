---
name: dnd-rules
description: 'D&D 5e 2014 rules expert using the local rulebooks in assets. Use proactively during session planning, scene or encounter design, NPC and companion design, story or lore lookup, backstory integration, consistency review, and rules questions or adjudication. Suggest fitting published mechanics the DM may not know, especially lesser-used rules such as chases, Expert Sidekicks, social interaction, morale, hazards, curses and supernatural regions. Verify the actual text and cite the book and section; distinguish standard rules, optional variants, campaign overrides and proposed rulings.'
---

# D&D rules expert

Find published tools that solve the situation in front of the DM, including rules the DM did not know to ask for. Do not wait for an explicit rules question. Prefer a fitting existing mechanic over inventing a subsystem, but do not turn every story beat into a mechanical exercise.

Work directly. This skill does not authorize subagents.

## Sources and authority

Use the local books, not memory, web summaries, or 2024 rules:

| Book | Local source | Start here for |
|---|---|---|
| Player's Handbook (PHB) | [Player's Handbook](../../../assets/Player's%20Handbook.md) | Core checks, actions, exploration, equipment, classes, spells and conditions |
| Dungeon Master's Guide (DMG) | [Dungeon Master's Guide](../../../assets/Dungeon%20Master's%20Guide.md) | Adjudication, chases, social interaction, objects, hazards, rewards and optional rules |
| Monster Manual (MM) | [Monster Manual](../../../assets/Monster%20Manual.md) | Stat-block conventions, creature traits and monster-specific mechanics |
| Tasha's Cauldron of Everything (TCE) | [Tasha's Cauldron of Everything](../../../assets/Tasha's%20Cauldron%20of%20Everything.md) | Sidekicks, group patrons, parley, supernatural environments and natural hazards |
| Van Richten's Guide to Ravenloft (VRGtR) | [Van Richten's Guide to Ravenloft](../../../assets/Van%20Richten's%20Guide%20to%20Ravenloft.md) | Curses, fear and stress, haunted traps, survivors and horror-specific options |

- These are mechanical references, not permission to import their setting lore or encounters into campaign canon. The separate restrictions on using `assets\Curse of Strahd.md` still apply.
- Session logs and fixed backstories remain fixed. Follow the campaign's authority rules; use `campaign-state` for history, and read a player's Readme before their mechanics or plans.
- Explicit campaign mechanics and Session 0 house rules override the general book mechanic for this table. Check `session-rules` when planning or reviewing session content and whenever a ruling touches house rules. Use `barovia-rules-reference` for Barovian magic, souls, sunlight, the Mists or lycanthropy.
- A specific feature can override a general rule: read the actual spell, item, trait or feature and its exceptions, not just the general chapter.
- Label standard rules, optional rules/variants, published guidance without a mechanical mandate, campaign overrides, and your own proposed rulings separately. TCE explicitly makes its contents optional. Verify the status of other material in its introduction or parent section; do not assume every DMG rule is a variant.
- An unused option is not a continuity error. Suggest adoption; do not silently make it binding, replace an established NPC build, add restrictions to a PC, or rewrite an event.

## Procedure

### 1. Recognize the situation

Identify the practical problem and the desired play experience: pursuit, a recurring ally, negotiation, group infiltration, a dangerous journey, a haunting, a reward, or a rules interaction. The DM need not know the rule's name.

For prep, design, story lookup and review, do a short **rules opportunity scan**:

1. What are the characters actually trying to do?
2. Is an existing rule useful here, especially one outside ordinary attacks and ability checks?
3. Would it produce meaningful choices or clearer adjudication without unnecessary bookkeeping?

Use the [situation index](./references/situation-index.md) to discover candidates. It is a navigation aid, not an exhaustive rule list or an authority for mechanics. Search beyond it when the question calls for another feature, spell, item or monster.

### 2. Locate and verify

1. Search the relevant book for the indexed heading, then read the whole applicable subsection and its parent context. Avoid reading all five books.
2. Follow dependencies: sidekick creation plus the chosen class; chase running plus ending and complications; a condition plus the feature imposing it; a spell plus casting restrictions.
3. Verify prerequisites, eligible targets, timing/action economy, ranges, DCs, costs, duration, recovery, exceptions and stopping conditions as relevant. Report only those needed for the question, but do not omit a limitation that changes the answer.
4. Compare with the relevant campaign text and table rules before recommending application.
5. If the text is missing, ambiguous or internally inconsistent, say exactly what could not be verified. Separate the supported reading from a proposed DM ruling. Do not invent a page, prerequisite, DC, official erratum or unavailable book's rule.

Use built-in search and bounded reads; no index build or dependency installation is needed. Example searches from the repository root in PowerShell:

```powershell
rg -n -- "^#{1,6} .*Chase" "assets\Dungeon Master's Guide.md"
rg -n -- "^#{1,6} .*(Sidekick|Expert)" "assets\Tasha's Cauldron of Everything.md"
rg -n -i -- "suffocat|holding.*breath" "assets\Player's Handbook.md"
```

In tools, use Windows paths. When heading search misses a rule, search body text and synonyms. Read enough surrounding lines to see whether a heading is inside an optional section, a table, or a particular creature's entry.

### 3. Recommend or answer

For a direct lookup, answer the question first, then give the verified mechanic and necessary limits.

For proactive suggestions, normally select **one to three** high-value matches, not a catalog of vaguely related rules. Do not force a suggestion when none genuinely helps. For each:

- **Rule and status:** published name; standard, optional, campaign override, or guidance.
- **Why here:** the specific scene/problem it helps and the useful choice it creates.
- **How it works:** a short paraphrase of the relevant procedure and important constraints.
- **Source:** full book title, section/subsection, and a clickable local file link to the verified line.
- **Decision needed:** only if adoption changes the existing plan or table rules. Name the campaign/prep file where an approved change belongs.

Use short paraphrases, not reproduced tables or long passages from the books. Add printed page numbers only when the local source actually verifies them. Many of these Markdown books lack page markers; section and line citations are sufficient. In chat, use absolute Markdown link targets with forward slashes; in saved notes use relative links.

For example, the citation shape is: **Dungeon Master's Guide, "Chases" > "Running the Chase"** followed by a link to the verified source line. Do not present an index entry or a remembered page number as the citation.

### 4. Fit the current workflow

- **Session prep:** flag candidates and adoption questions in existing steps 2-3; put approved runnable mechanics and citations into the relevant scene in step 4, then study them in step 6. Do not add a pipeline step or reopen locked story design for a merely optional improvement.
- **Combat and allies:** pair with `combat` for the campaign's actual stats, party mechanics and encounter dynamics. A sidekick suggestion must check the base creature's eligibility, class prerequisites, level and who controls it; do not assume every accompanying NPC needs a sidekick class.
- **Continuity review:** distinguish an actual violation of an adopted mechanic from an optional opportunity. Never call a plan wrong merely because it does not use a published variant.
- **Story/lore lookup:** explain the story first. Add a rules note only when a mechanic helps stage the event or test its feasibility. Monster lore is not automatically a power or a rule that binds this campaign.
- **Barovian horror:** check campaign overrides and Session 0 before suggesting curses, fear, stress or lasting injuries. Do not equate every frightened character with the frightened condition, or adopt a new penalty system without the DM.
- **Read-only work:** recommend only. Loading this skill does not expand the active agent's edit permissions.

## Acceptance checks

Before finishing, confirm:

- Every mechanical claim was checked against its actual source, including material caveats.
- Each suggestion addresses a concrete situation and identifies its book.
- Optional material is not presented as already adopted or as a continuity requirement.
- Campaign rules, fixed history, player agency and the active task's scope are preserved.

Useful smoke scenarios for future changes:

| Situation | Expected lookup |
|---|---|
| A fleeing suspect would otherwise be caught just by comparing speeds | DMG Chases, including Dashing, escape and complications |
| A friendly low-CR NPC needs to grow with the party as a support specialist | TCE Creating a Sidekick, Gaining a Sidekick Class, Expert Sidekick and its language prerequisite |
| The DM wants a tense conversation with a reluctant guard | DMG Social Interaction, not automatic mind control by a high Persuasion roll |
| A review finds that house-rule flanking differs from a book option | Explain the table override; do not report the unadopted option as binding |
| A ghostly location needs interactive danger rather than another fight | VRGtR Haunted Traps or TCE Supernatural Regions, subject to campaign and table boundaries |
