---
name: campaign-state
description: Determines the party's current position in the campaign (act, arc, section, in-world date) from the session logs, and recalls past events. Use when asked where we are, what comes next, what already happened, what is fixed vs. changeable, or before planning a session, checking continuity, or integrating a backstory.
---

# Campaign State

Answers "where are we?" and "what has already happened?" from the session logs. The logs are the source of truth. [session-digest.md](./session-digest.md) is only a cache of them.

## Sources and authority

| Source | Role | Changeable? |
|---|---|---|
| `sessions/Session N/log.md` | Events that already happened | No. Fixed history. The DM may add forgotten details, so re-check the logs when precision matters. |
| Act/arc files, chapters, appendices | The campaign, including our edits | Yes. Edited freely to integrate new events. |
| `assets/Curse of Strahd.md` | The original book, used only where the arc files cite it (citations like `(p. 43)`; find `**[p. 43]**` or the area heading such as `### E2.`) | Reference. The Reloaded text overrides it where they differ. |
| `players/*/Readme.md` | Says which player files are fixed and which are mutable | Follow it per player. |

If a logged event is vague, there is room to interpret it. If it is explicit, it cannot be changed. When a plan conflicts with a log, flag the conflict and offer a workaround that keeps the logged facts.

## Procedure: locate the current position

1. List `sessions/` and read the `log.md` in the highest-numbered folder. Skim earlier logs if the last one is short, since logs vary in length.
2. Check whether the digest's "last session covered" matches the newest log. If a newer log exists, read it and update the digest.
3. Find the matching sections in the campaign files. Arc files use headed sections such as `C2a. Strahd's Arrival`. Search headings with grep for the locations and NPCs named in the log.
4. Report:
   - **Act / Arc / section** where the last session ended.
   - **Next likely sections**, from the arc's own flow. Read the arc file to confirm.
   - **In-world date.** Fill it in from the act summary's Timeline section and the arc text, record it in the `timeline` skill's `date-ledger.md`, and label it `inferred` unless the DM has confirmed it. `timeline` validates the date against the calendar. Remember that every month has 28 days.
   - **Divergences**: where the table departed from the arc text (skipped content, changed outcomes).

The campaign files may have been edited, so read them rather than relying on memory of the published module. When an arc section cites the original book for its content, open that passage in `assets/Curse of Strahd.md` to know what the section covers and what comes next.

## Procedure: recall past events

1. Start with [session-digest.md](./session-digest.md) for a fast answer.
2. Verify any detail that will drive a decision against the session log itself, and cite `Session N`.
3. Separate what the logs state from what is inferred. Never invent events.

## Procedure: after a new session

Add or update the digest entry for that session (what happened, key NPC interactions, decisions, items, unresolved threads) and the "Current position" block. Also update the `timeline` ledger (date span) and `npcs`'s `roster-state.md` (NPC status and knowledge). Record any fight outcomes in the digest. Keep entries short and factual. Do not add planned content to the digest. Plans belong in campaign or player files.
