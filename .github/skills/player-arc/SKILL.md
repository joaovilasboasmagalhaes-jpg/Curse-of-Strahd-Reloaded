---
description: "Designs and evaluates a player character's story arc so that the player is satisfied - entertaining beats, agency, growth, spotlight balance and a satisfying resolution. Use when developing or reviewing a backstory, a character arc, a personal plot or its payoff, when checking whether a plan serves the player, or when a concept needs options and a test of how well it fits the player."
name: player-arc
---

# Player Arc

Knowledge for making a character's story work **for the player at the table**. Story logic still matters, but the main test is whether the player will enjoy it, feel it was theirs, and feel it paid off.

## Sources

| Need | Source |
|---|---|
| Who the character is | The player's Readme, then the fixed backstory and plot hook |
| What the player wants and enjoys | `players/<name>/player_profile.md` (see [player-profile-template.md](./player-profile-template.md)). If it does not exist, say so and ask the DM instead of guessing |
| Past decisions and rejected ideas | `players/<name>/design_notes.md`, if present |
| Current ideas | `players/<name>/concepts/*.md` (see [concept-template.md](./concept-template.md)) |
| Decided plans | `players/<name>/dm_plans.md`, `dm_campaign_integration.md` |
| What the player did and reacted to at the table | `sessions/Session N.md` (fixed) |
| The reusable integration method | `players/player_strategy.md` |
| Other players' arcs (for spotlight balance) | Their Readmes and plans |

## What makes an arc satisfying

Check each of these. Report which are strong, thin or missing.

- **Want and need.** The character wants something concrete. What they need is different and deeper. The arc resolves the tension between them.
- **Agency.** The player's choices change what happens. Avoid outcomes that come from an NPC's reveal or from the DM's plan alone.
- **Growth.** The character is different at the end because of choices they made. Name the starting and the ending state.
- **Escalation.** Stakes and costs grow. Each stage should ask for something harder than the last.
- **Setup and payoff.** Anything raised early (a hook, an item, a relationship) pays off later. Do not leave threads dangling.
- **Spotlight.** Beats are spread across sessions and balanced with the other four players. Include moments for the character's mechanics and the player's play style.
- **Distinct from the other players.** The arc must feel personal. If it copies another player's arc, the player feels interchangeable. Compare it with the other arcs on: central theme and emotional core, anchor (faction, NPC, place), kind of antagonist, plot shape (e.g. hunted, seeking, redeeming, inheriting), the central choice, type of scenes, and the ending. Flag any overlap and change the shared element so this arc owns something no one else has. A shared anchor is fine only if each player's angle on it is different.
- **Fun beats.** Include scenes the player will enjoy as play (their favorite kinds of scenes), not only lore delivery.
- **Resolution.** The ending fits the arc's promise. It can be bittersweet, but it should not be arbitrary or taken away from the player. It should also happen at a point in the campaign where the player is present for it.
- **Table reality.** The player can discover it through play. A secret that only the DM knows does not entertain anyone.

## Procedures

**Develop options**
1. Read the player's Readme, fixed backstory and profile. Name the character's core (what the backstory is emotionally about).
2. Read the other players' arcs and list what is already taken (themes, anchors, antagonists, plot shapes, endings). Offer two to four directions that differ from each other and from those. For each give the arc in a few beats, the want/need, the key choices the player gets, the payoff, and the likely risk.
3. Recommend one and say why it fits this player and what makes it theirs alone.

**Evaluate a concept**
Score it against the list above, including a comparison with every other player's arc for overlap, note what the player is likely to enjoy and what could disappoint them, and propose the smallest changes that improve it.

**Plan beats across the campaign**
Map the arc onto acts and arcs using `campaign-state`, `timeline` and `cartographer`. Space the beats across sessions, and note where the player's mechanics matter (`combat`) and which NPCs carry the story (`npcs`).

**Check satisfaction after play**
Compare what happened at the table with the plan. Note what the player responded to, and update the player's profile (with the DM's confirmation).

## Rules

- **The player's satisfaction is the DM's call.** Propose, and ask the DM what the player said or showed. Do not invent a player's preferences.
- **Fixed backstory does not change.** Develop around it.
- **Keep the story coherent.** A satisfying arc still has to make sense in the campaign. Use the specialist skills or the Continuity Reviewer for that.
- **Never decide the character's choices.** Offer situations, not outcomes.
- **Spoilers.** Planned reveals are DM-only until they happen at the table.
