---
description: "Update the campaign state after a new session: digest, date ledger, NPC roster, open threads."
agent: "agent"
argument-hint: "Session number (defaults to the newest log)"
---
A new session log has been added or updated. Use the `campaign-state`, `timeline` and `npcs` skills.

1. Read the session log (the given number, or the `log.md` of the highest-numbered folder in `sessions/`).
2. Update [session-digest.md](../skills/campaign-state/session-digest.md): add or revise the session entry, the "Current position" block and the open threads.
3. Update [date-ledger.md](../skills/timeline/date-ledger.md) with the in-world date span and mark it `inferred` unless the DM confirmed it. Check it against the calendar.
4. Update [roster-state.md](../skills/npcs/roster-state.md) with NPC status, new NPCs, relationships and what each now knows about the party.
5. Check the logged events against the campaign files and list divergences from the arc text. Do not edit the arc files.
6. List any `chosen` or `integrated` concepts and player plans that the divergences affect, and why.

Do not edit `sessions/` logs. Add only what the log states and label anything inferred. Finish with a short list of what changed and any question for the DM (especially the date).
