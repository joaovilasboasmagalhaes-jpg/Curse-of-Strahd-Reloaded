---
name: npcs
description: Knows the campaign's NPCs as both facts and personalities - who they are, where they are, status, relationships, factions, what they have done, what they know, and how they would react, speak or choose. Use when asked about an NPC's whereabouts, history, connections or knowledge, who could have done or known something, what an NPC would do or say, whether a planned NPC choice is in character, or when writing NPC dialogue, motives or reactions. For stat blocks and fighting, use the combat skill.
---

# NPCs

Covers an NPC's **facts** (identity, status, relationships, knowledge) and **behavior** (personality, likely choices). Stats, abilities and encounters belong to `combat`.

## Sources

| Need | Source |
|---|---|
| Base profile | `Appendices/Non-Player Characters.md`, organized by location (Death House, Village of Barovia, Tser Pool Encampment, Castle Ravenloft, Old Bonegrinder, Town of Vallaki, Village of Krezk, Abbey of St. Markovia, Wizard of Wines, Werewolf Den, Argynvostholt, Amber Temple, Berez). Each NPC is a `###` heading with **Resonance**, **Emotions**, **Motivations**, **Inspirations**, **Persona** (public vs private), **Morale** and **Relationships**. Search by name |
| Where they appear and what they do | Arc files (`Act * /Arc *.md`) |
| Strahd | `Chapter 2 - The Land of Barovia/Strahd von Zarovich.md`: his three modes (Gentleman, Tyrant, Monster), relationships and goals |
| Original book NPCs | `assets/Curse of Strahd.md`: the area chapters (3-15), Appendix D, Chapter 1 ("Roleplaying Strahd", "When Strahd Attacks"). Use an entry only where the guide references it. If the guide does not mention an original NPC, assume the NPC does not exist. The Reloaded text wins on conflicts |
| What happened to them at the table | `sessions/Session N/log.md` (fixed), summarized in [roster-state.md](./roster-state.md) |
| NPCs added or changed by planning | `players/*/dm_plans.md`, `dm_campaign_integration.md`, `clan_lore_dm.md`, and edits in the campaign files. Campaign-file edits count as canon |
| Backstory NPCs | The player's Readme and fixed backstory |
| Portraying villains and folklore-based NPCs (optional inspiration, never canon) | `dm-craft/books/villain-guide.md` (Strahd, his court), `vampires.md`, `werebeasts.md`, `vistani.md`. The guide wins on conflicts |

## Rules

- **Layers of truth.** Separate (1) what the logs fixed, (2) the campaign text, (3) mutable plans. When they conflict, logs win, then campaign files, then plans.
- **Knowledge is a fact too.** Record what an NPC could know. Example: Rahadin knew nothing about Grim's heart pouch, so he cannot act as if he did. Do not give an NPC knowledge unless a source or a plausible channel (spies, Strahd's network, a conversation) supplies it.
- **Strahd's spies** (bats, wolves, rats, ravens) mean Strahd may know what happened in the open, but not what was said in private. See "Strahd's Spies" in `Chapter 3 - Running the Game/Running the Adventure.md`.
- **Spoilers.** DM-only plans are not known to the characters. Label them when reporting.
- **Stay in range.** Surprise comes from a believable motive, not from out-of-character action. Barovians are scared and under siege, so fear, grief and distrust of outsiders are the baseline unless a source says otherwise. Strahd acts through his three modes and long-term goals, not as an enemy who attacks on sight.
- **Never decide the players' characters' reactions.** Describe only NPCs.
- **Voice.** Whenever NPCs speak in a written scene (dialogue, read-aloud, sample lines), read `dm-craft/books/strahd-voice.md` first and follow it: formal period diction, courtesy as menace, understatement, dry irony, and plain speech for common Barovians.

## Procedures

**Where is X, and what are they doing?**
1. Read their entry in [roster-state.md](./roster-state.md). If missing, read the appendix entry and the arc.
2. Combine with the current date from `timeline`. Check the NPC's scheduled actions against it.
3. Answer with status, location, source, and whether it is logged or planned.

**Who knows what / who could have done this?**
List each candidate with location, access and knowledge. Drop those that `cartographer` or `timeline` rule out.

**What would X do or say?**
1. **Profile:** read Persona (public and private), Motivations, Emotions and Morale.
2. **Knowledge:** check what they know and have seen of the party.
3. **Situation:** note what is done to them, who is present (public and private personas differ), and what is at stake for their Motivations.
4. **History:** check the session logs. A character who was threatened, helped or lied to remembers it.
5. **Answer** with the most likely reaction and a short reason, one or two plausible alternatives, a few lines of voice if wanted, and what would change the answer.
6. **Flag drift.** If a planned choice contradicts the profile or past behavior, say so and suggest what would make it believable (a new motive, a revealed fact, pressure).

**New NPC or relationship**
Check for an existing NPC with the same name or role. State faction, location, relationships, knowledge and a short personality profile in the appendix's format. Hand stats to `combat`.

## Maintenance

After each session, update [roster-state.md](./roster-state.md): status changes, new NPCs, new relationships, what each NPC now knows about the party. Add only what the logs establish.
