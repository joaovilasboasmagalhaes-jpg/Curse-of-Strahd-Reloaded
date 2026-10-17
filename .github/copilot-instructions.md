# Curse of Strahd: Reloaded (DM workspace)

This workspace is a DM's campaign guide for a running D&D 5e *Curse of Strahd* game, plus per-player backstory integration and session logs. The user is the DM.

## Canon model

- **Campaign files are one canon.** Intro, chapters, acts/arcs, and appendices began as the original campaign. Edits made while planning count as the campaign; do not distinguish "original" from "altered".
- **The original book is a referenced source.** *Reloaded* revises the original *Curse of Strahd*, and the full original text is in `assets/Curse of Strahd.md`. Use it only where the guide references it (citations like `E2. Blood of the Vine Tavern (p. 43)`), **except where the guide contradicts or overwrites it**. If the guide does not reference an original element (an encounter, a piece of lore), assume it does not exist. Page markers in the file look like `**[p. 43]**`, and areas are headed like `### E2.`. See `Introduction/Using This Guide.md`.
- **Sessions are history.** `sessions/Session N.md` records what already happened at the table. Treat it as fixed: never contradict or rewrite it. The DM may add forgotten details to a log later.
- **Ambiguous past events have room.** If a logged event is unclear, propose an interpretation that fits it. Do not override anything the log states explicitly.
- **Player files:** each `players/<name>/Readme.md` indexes that player's files and says which are fixed (backstory, plot hook, mechanics) and which are mutable DM plans (`dm_plans.md`, `dm_campaign_integration.md`, `clan_lore_dm.md`). Read the player's Readme first. Mutable plans become fixed only once revealed in play.
- **Concepts are not canon.** Ideas under development live in `players/<name>/concepts/*.md` with a status (`exploring`, `chosen`, `integrated`, `discarded`). Only `integrated` concepts have been applied to the campaign files. Testing a concept against the campaign (a dry run) must not edit campaign files.
- DM-only material is spoilers. Do not present planned revelations as something the characters already know.

## Working rules

- To learn where the party is or what has happened, use the `campaign-state` skill instead of guessing.
- Combat must not be a static HP race. For any significant fight, follow the design principles in the `combat` skill (objective beyond killing, something to react to, short and intense).
- Propose campaign changes as edits to the relevant campaign file and say which file. Do not edit session logs unless asked.
- Follow the existing Obsidian-style markdown (wikilinks, callouts) and the Barovian calendar (735 B.C., 12 months of 28 days).
