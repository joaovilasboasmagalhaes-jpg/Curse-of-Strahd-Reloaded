---
name: post-session
description: Updates campaign state after a new or revised session log, including the session digest, date ledger, NPC roster, open threads, arc divergences, affected concepts and player profiles.
---

# Post-Session Update

Use this skill after a session log has been added or revised. It coordinates the existing `campaign-state`, `timeline`, `npcs` and `player-profile` skills.

## Scope

- Session number: use the number supplied by the DM. If none is supplied, use the highest-numbered `sessions/Session N/log.md`.
- Re-running the workflow after correcting a log is an update, not a new entry. Reconcile existing observations and do not duplicate or inflate evidence.
- Do not edit `sessions/Session N/log.md`.
- Do not edit campaign arcs, player backstories or mutable player plans. Report changes to concepts or plans without applying them.

## Procedure

1. Read the selected session log and the highest relevant campaign-state sources.
2. Update [session-digest.md](../campaign-state/session-digest.md):
   - add or revise the session entry;
   - update the "Current position" block;
   - reconcile open threads;
   - keep entries short and factual.
3. Update [date-ledger.md](../timeline/date-ledger.md):
   - record the in-world date span for the session;
   - mark it `confirmed` only when the DM confirmed it;
   - otherwise mark it `inferred`;
   - check month and day arithmetic against [calendar.md](../timeline/calendar.md).
4. Update [roster-state.md](../npcs/roster-state.md):
   - add new NPCs;
   - update statuses and locations;
   - record new relationships;
   - record what each NPC now knows about the party;
   - add only facts established by the log and supported channels of knowledge.
5. Read the relevant campaign files for context and cross-reference them with the log.
6. Check the events against the campaign arc text and identify divergences:
   - skipped content;
   - changed outcomes;
   - changed NPC status or relationships;
   - new locations or events;
   - do not edit the arc files.
7. Identify any `chosen` or `integrated` campaign concepts and player plans affected by those divergences, including why the connection matters. Leave them unchanged unless the DM separately requests an edit.
8. Use `player-profile` in update mode for every player represented in the session:
   - read the relevant player Readmes and existing profiles;
   - set session coverage and whether each player's attendance or attribution is clear;
   - create or update `players/<name>/player_profile.md` only when attributable evidence exists;
   - record observations separately from stated preferences and labeled hypotheses;
   - preserve explicit preferences and existing evidence;
   - use source links and confidence levels;
   - revise existing Session N evidence instead of duplicating or increasing confidence merely because the workflow ran again;
   - for players with insufficient evidence, report that no profile change was supported.

## Reporting

Finish with a concise list of:

- files updated;
- session entries, date changes and NPC changes;
- divergence findings;
- affected concepts or player plans;
- profile changes;
- significant uncertainties;
- questions for the DM, especially when an in-world date needs confirmation.

Do not present a log's inferences as facts, DM plans as revealed lore or player-profile hypotheses as established preferences.
