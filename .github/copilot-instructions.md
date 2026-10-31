# Curse of Strahd: Reloaded (DM workspace)

This workspace is a DM's campaign guide for a running D&D 5e *Curse of Strahd* game, plus per-player backstory integration and session logs. The user is the DM.

## Canon model

- **Campaign files are one canon.** Intro, chapters, acts/arcs, and appendices began as the original campaign. Edits made while planning count as the campaign; do not distinguish "original" from "altered".
- **The original book is a referenced source.** *Reloaded* revises the original *Curse of Strahd*, and the full original text is in `assets/Curse of Strahd.md`. Use it only where the guide references it (citations like `E2. Blood of the Vine Tavern (p. 43)`), **except where the guide contradicts or overwrites it**. If the guide does not reference an original element (an encounter, a piece of lore), assume it does not exist. Page markers in the file look like `**[p. 43]**`, and areas are headed like `### E2.`. See `Introduction/Using This Guide.md`.
- **Sessions are history.** `sessions/Session N/log.md` records what already happened at the table. Treat it as fixed: never contradict or rewrite it. The DM may add forgotten details to a log later.
- **Ambiguous past events have room.** If a logged event is unclear, propose an interpretation that fits it. Do not override anything the log states explicitly.
- **Player files:** each `players/<name>/Readme.md` indexes that player's files and says which are fixed (backstory, plot hook, mechanics) and which are mutable DM plans (`dm_plans.md`, `dm_campaign_integration.md`, `clan_lore_dm.md`). Read the player's Readme first. Mutable plans become fixed only once revealed in play.
- **Fixed player backstories outrank source-derived details.** A backstory marked fixed in the player's Readme is campaign canon. If it conflicts with source/module material or source-derived campaign notes, adapt those notes to the backstory; never change the backstory to fit the source. Session logs remain fixed and must not be rewritten. Specifically, Ivan's Emil and Kiril are the brothers in his backstory; source-derived ages, pack roles, relationships, and histories apply only where compatible or explicitly adopted by the DM.
- **Concepts are not canon.** Ideas under development live in `players/<name>/concepts/*.md` with a status (`exploring`, `chosen`, `integrated`, `discarded`). Only `integrated` concepts have been applied to the campaign files. Testing a concept against the campaign (a dry run) must not edit campaign files.
- DM-only material is spoilers. Do not present planned revelations as something the characters already know.

## Working rules

- **No subagents without permission.** Agents and skills must not start a subagent on their own. Do the work directly, or ask the DM first and wait for a yes. A DM request to "delegate" or to run a named agent counts as permission for that agent only.
- To learn where the party is or what has happened, use the `campaign-state` skill instead of guessing.
- Combat must not be a static HP race. For any significant fight, follow the design principles in the `combat` skill (objective beyond killing, something to react to, short and intense).
- **Dialogue is a preference, not a rule:** Since the DM plays every NPC, avoid direct NPC-to-NPC turn-taking where possible; especially avoid one NPC speaking and then handing the conversation to another NPC. Multiple NPCs may speak in a conversation when a player character is also participating. An NPC-only exchange is fine when the scene genuinely needs it, such as a meaningful interaction between Strahd and Ireena.
- **Sister Elga's Urn glows near undead.** Her *Urn of Soulcatching* turns bright purple whenever it is within 300 feet of any undead (`players/sister_elga/soul_gathering.md`), and the player must be told when it happens. When planning anything involving Elga, or preparing a session, check every scene, location, NPC and monster for undead within 300 feet of her, and add a DM-only warning ("Elga's Urn glows: tell the player") where one is present. This includes undead that are hidden, disguised, in the next room, or only passing by, and undead NPCs such as Strahd's court. Player characters are never counted as undead, so Agni and the rest of the party never trigger the glow.
- **Session 0 rules apply to every session and its content.** The table agreed on content boundaries (no described sexual violence, PvP only with in-character consent), tone, difficulty, loot, resurrection and combat house rules. Use the `session-rules` skill when planning, writing or reviewing session content, and flag anything that breaks them. Sources are in `sessions/Session 0/`.
- Propose campaign changes as edits to the relevant campaign file and say which file. Do not edit session logs unless asked.
- Follow the existing Obsidian-style markdown (wikilinks, callouts) and the Barovian calendar (735 B.C., 12 months of 28 days).
