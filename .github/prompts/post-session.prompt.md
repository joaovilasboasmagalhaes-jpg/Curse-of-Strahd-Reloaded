---
description: "Update the campaign state after a new session: digest, date ledger, NPC roster, open threads and evidence-based player profiles."
agent: "agent"
argument-hint: "Session number (defaults to the newest log)"
---
A new session log has been added or updated. Use the `campaign-state`, `timeline`, `npcs` and [player-profile](../skills/player-profile/SKILL.md) skills.

1. Read the session log (the given number, or the `log.md` of the highest-numbered folder in `sessions/` with a `log.md` file).
2. Update [session-digest.md](../skills/campaign-state/session-digest.md): add or revise the session entry, the "Current position" block and the open threads.
3. Update [date-ledger.md](../skills/timeline/date-ledger.md) with the in-world date span and mark it `inferred` unless the DM confirmed it. Check it against the calendar.
4. Update [roster-state.md](../skills/npcs/roster-state.md) with NPC status, new NPCs, relationships and what each now knows about the party.
5. Read campaign files for context and cross-reference with the session log.
6. Check the logged events against the campaign files and list divergences from the arc text. Do not edit the arc files.
7. List any `chosen` or `integrated` concepts and player plans that the divergences affect, and why.
8. Use `player-profile` in update mode for the session being recorded. Read the relevant player Readmes and existing profiles, then update `players/<name>/player_profile.md` for each player with attributable evidence in this log. Create missing profiles and index them in their Readmes when supported. Record sourced observations and labeled hypotheses about behavior, wishes and play style; compare with earlier evidence, preserve stated preferences, and leave unsupported fields unknown. Revise existing entries when re-recording a session rather than duplicating evidence or increasing confidence merely because the prompt ran again. Report players for whom there was insufficient evidence without inventing preferences.

Do not edit `sessions/` logs. Keep the digest, ledger and roster factual, with any necessary inference labeled. Player-profile inductions must remain separate from observed facts and explicitly stated preferences, with sources, confidence and alternative explanations. This profile-maintenance step does not authorize edits to campaign arcs or player plans. Finish with a short list of what changed, including profile changes and significant uncertainties, and any question for the DM (especially the date).
