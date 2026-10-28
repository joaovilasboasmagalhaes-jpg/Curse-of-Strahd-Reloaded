---
name: player
description: "Work on a player's backstory. Without a name, shows where every player stands."
argument-hint: "Player name (agni, caspian, grim, ivan, sister_elga), or nothing for the overview"
disable-model-invocation: true
---
Work as the Backstory Developer (see [backstory-developer.agent.md](../../agents/backstory-developer.agent.md)).

Find out where the named player stands and do the next step. Do not ask the DM which step to run.

**No player named:** list every player with: whether `player_profile.md` exists, their concepts and statuses (`exploring`, `chosen`, `integrated`, `discarded`), and what is left to integrate. Stop there.

**Player named:** read their Readme, profile, design notes and concepts, then:
- **No concept yet:** offer distinct options with a recommendation, using the `player-arc` skill. If the profile is missing, say so and do not guess the player's preferences. Save the direction as `players/<name>/concepts/<short-title>.md` from `.github/skills/player-arc/concept-template.md`, status `exploring`.
- **A concept is `exploring`:** improve it from the DM's input. When the DM wants it tested, ask the DM for permission to have the Integrator do a dry run (no campaign edits) and the Continuity Reviewer check it. Record the result in the concept.
- **A concept is `chosen`:** list every edit with its file and section (the Integrator may do this only with the DM's permission), and show the list to the DM. Apply only after the DM approves, then check the result (the Continuity Reviewer only with the DM's permission) and set the concept to `integrated`.

Never edit campaign files without the DM's approval. Finish with what you did and the one decision you need from the DM.
