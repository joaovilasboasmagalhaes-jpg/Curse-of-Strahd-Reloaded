---
name: timeline
description: Keeps chronological consistency for the campaign. Owns the Barovian calendar, in-world dates for each session, the history timeline (3000 B.U. to 735 B.C.), and pre-campaign chronologies of player backstories. Use when a question or plan involves dates, durations, "how long ago", the order of events, moon phases, scheduled events, how many days a plan needs, or placing a backstory or NPC history on the timeline.
---

# Timeline

Holds time knowledge: what happened when, how long things take, and what is scheduled to happen. It does not decide where the party is (that is `campaign-state`) or how far places are (that is `cartographer`).

## Date ownership

- `campaign-state` **fills** the current in-world date after reading the session logs.
- This skill **keeps** the date: it holds the ledger in [date-ledger.md](./date-ledger.md), checks every new date against the calendar and the scheduled events, and flags contradictions.
- Dates the DM has not confirmed stay marked `inferred`. Only the DM can set `confirmed`.

## Sources

| Need | Source |
|---|---|
| Calendar, moon, sunrise and sunset | [calendar.md](./calendar.md), which summarizes `Chapter 2 - The Land of Barovia/Lore of Barovia.md` |
| History before the campaign | `Chapter 2 - The Land of Barovia/History of Barovia.md` and `assets/curse-of-strahd.timeline` |
| Dates of campaign events | The `# Timeline` section of each `Act * Summary.md`, then the arc files |
| Original book timing | `assets/Curse of Strahd.md`: "The Vampire's History" (Chapter 1), the "Special Events" sections of each area chapter, and the Epilogue. Use it where the arc files cite it. The Reloaded text wins on conflicts |
| What already happened | `sessions/Session N/log.md` (fixed) |
| Backstory chronology | The player's Readme, then their `backstory.md` (fixed) and mutable plans such as `players/ivan/clan_lore_dm.md` |
| Rules for backstory placement | `players/player_strategy.md`, section 3 |

`assets/curse-of-strahd.timeline` is a large JSON file for the Timelines app. It has year resolution only. Search it by `"title"` instead of reading it whole. Treat any entry you add as part of the campaign. Do not rewrite eras without the DM asking.

## Procedures

**Place an event or backstory on the timeline**
1. Find the start and end in the sources above. Prefer session logs, then act summaries, then history.
2. Check the Mists rule: anything transported into Barovia can only appear after Barovia entered the Mists (351 B.C.). A character can experience a loss as recent while Barovia counts it as centuries old.
3. Return the date, the source, and whether it is logged, from the module or planning, or inferred.

**Check a plan for date problems**
1. List the events and the dates or day counts each needs.
2. Add travel durations from `cartographer`, using Barovian day length (sunrise 7:00, sunset 17:00).
3. Check against scheduled events (moons, arc dates such as Tarokka on Neyavr 1 and arrival in Vallaki on Neyavr 2) and against anything already in the session logs.
4. Report conflicts with the smallest change that fixes them. A conflict with a logged event means the plan moves, not the log.

**Date arithmetic**
Every month has 28 days, so there are 336 days per year. Month order is in [calendar.md](./calendar.md). Day 28 is the last day of a month, so Octyavr 28 is followed by Neyavr 1. Compute with the table, not by memory of real calendars.

## Maintenance

After a session, update the ledger with the date range the session covered and its status. If the DM confirms a date, change its status to `confirmed`. If a log changes a date, update the ledger and recheck later entries.
