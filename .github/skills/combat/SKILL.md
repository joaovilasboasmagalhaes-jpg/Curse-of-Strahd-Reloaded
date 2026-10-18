---
name: combat
description: Knows stat blocks, abilities and encounter design for the campaign and its party. Use when asked about a monster's or NPC's stats, attacks, abilities or CR, how dangerous a fight is for the party, how to build or adjust an encounter, what a player character can do in combat, or when writing a combat entry. Rules are D&D 5e 2014.
---

# Combat

Provides numbers and mechanics. The identity and behavior of an NPC belong to `npcs`. This skill answers "what can it do, and how hard is this fight?"

## Sources

| Need | Source |
|---|---|
| Custom stat blocks | `Appendices/Bestiary.md`. HTML `statblock` divs, each under a `###` heading (for example "Animated Major Object", "Castle Gargoyle", "Druid Assailant"). Search the heading |
| NPC stat blocks | `Appendices/Non-Player Characters.md`. Some NPCs have a block inline, others are defined by reference (for example Ireena: expert sidekick, Tasha's Cauldron p. 142, with the noble base). Follow the reference |
| Conditions | `Appendices/Glossary.md` |
| Encounters as the guide writes them | The arc files, in the sections where combat occurs |
| Original book stat blocks | `assets/Curse of Strahd.md`: Appendix D ("Monsters and NPCs") and the area chapters. Use only where the guide references them. Reloaded overrides on conflicts |
| Combat entry format | `_other/templates/combat.md`: Combat Level, Expected Character Level, Expected HP Consumption, Expected Allies, an enemies table by player count (3 to 6) and a Balancing table |
| Party capabilities | Each player's Readme, then their mechanics files (for example `players/agni/vampire_details.md`, Elga's `players/sister_elga/soul_gathering.md` and `potion_brewing.md`) and fixed backstory |
| Party level | The `Act * Summary.md` milestones: Act I starts at 2nd and ends at 4th, Act II 4th to 5th, Act III 5th to 8th |
| Past fights | `sessions/Session N/log.md` |

## Rules

- **Never invent numbers.** If the Reloaded files or the original book do not contain a stat, say so. Offer a nearby stat block as a labeled proxy and let the DM decide.
- **Rules edition is 2014.** The guide says it was not updated to the 2024 rules.
- **Reloaded wins.** Take stat blocks, modified abilities and encounter sizes from the Reloaded files, using the original only where cited. A Reloaded entry that modifies an original monster replaces it.
- **Fixed history.** The logs say what happened in earlier fights. Do not retcon outcomes.
- **Party, not average party.** There are five PCs (Agni, Caspian, Grim, Ivan, Sister Elga). Use their real mechanics, not a generic party.
- **Elga's Urn warns of undead.** Her Urn glows bright purple within 300 feet of any undead, so an ambush by undead near her is never a surprise to her player. When building or judging an encounter with undead, say when the Urn starts glowing and remind the DM to tell the player.
- **Intended difficulty (Session 0).** The table chose: few easy fights, most fights hard, and TPK is a frequent, accepted risk. Do not balance encounters to guarantee survival. When judging a fight, a result of "easy" or "comfortably winnable" is a mismatch with the table's intent: say so and propose a harder or more dangerous version (stronger enemies, a clock, worse terrain, reinforcements). Pair danger with foreshadowing and a way to retreat or escape, since the DM promised a fair chance to avoid bad situations. Combat is infrequent (about every two or three sessions), so each fight should matter.
- **Enemy behavior.** Enemies act like trained soldiers: they use cover, focus weak targets, retreat when losing and exploit weaknesses. Beasts and mindless creatures may be simpler, and commanders smarter.
- **Session 0 combat rules.** Flanking +2 to attack rolls, critical hits double the dice, default 5e conditions, potions are an action (full) or a bonus action (rolled), death saves are secret. See the `session-rules` skill.
- **Spoilers.** Hidden abilities and planned boss encounters in player plans are DM-only.

## Design principles

The table found combat boring: long fights drag, and static HP races (both sides trade blows until one side's HP runs out) are the main cause. Intense is better than long, and complex is better still. This does not apply to every fight. Minor encounters can stay simple and quick.

For each **significant** combat, require at least one of:

- **Something besides "kill everything"**: an objective, a clock, a rescue, an escape, a ritual to stop, an item to seize, a foe to protect or reach.
- **Something to react to**: terrain, hazards, a shifting battlefield, enemy behavior that changes (phases, retreats, reinforcements, targeting choices), or interactive environment features.

Tactics to draw on: timed events on initiative counts, moving or collapsing terrain, objectives with visible progress, enemies with distinct roles and counters (not several copies of one stat block), enemy tells that reward reacting, positioning that matters (cover, elevation, chokepoints, forced movement), a mid-fight twist, and ways to end the fight early (morale, objective success, retreat).

Pacing: prefer fewer, higher-impact enemies so rounds resolve quickly, and higher damage with smaller HP pools over big HP pools. Plan for roughly 4 to 6 rounds and give a way to wrap up if it drags. Hook into the PCs' custom combat mechanics (see the party's mechanics files) so those features matter in the scene.

When judging or building an encounter, state which of the two checks it passes and what the players will react to. If it passes neither, propose a change before giving numbers.

## Procedures

**Look up a stat block**
Find it in the Bestiary or NPC appendix, follow any reference, and report AC, HP, speed, abilities, actions, CR and notable traits, with the source and any note on what the guide changed.

**Judge an encounter**
1. Get the enemies' stats and the party's level for the current act.
2. List relevant party strengths and weaknesses from their mechanics files (healing, blood hunter abilities, turn undead, ranged damage, mobility).
3. Estimate the difficulty and the HP drain. Compare with the guide's own rating where it gives one, and say that the result is an estimate, not a calculation. Compare it with the table's intended difficulty (mostly hard, TPK possible) and say if the fight is too easy.
4. Run the combat check from the design principles (objective, or reactive battlefield/behavior) and note the expected length in rounds.
5. Suggest adjustments in the style of the template's Balancing table.

**Write a combat entry**
Fill in `_other/templates/combat.md`, including its Dynamics section. Keep monsters by player count for 3 to 6 players, and base the expected level on the act summary.

**NPC in a fight**
Ask `npcs` for Morale and personality (does the NPC flee, plead or fight to the death?) and combine it with the stats here.

## Maintenance

When a fight happens, `campaign-state` records it in the digest. Add lasting changes (a monster with a changed ability, a newly stat-blocked NPC) to the campaign files, not to this skill.
