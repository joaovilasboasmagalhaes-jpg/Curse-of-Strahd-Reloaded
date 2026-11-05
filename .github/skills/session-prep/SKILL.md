---
name: session-prep
description: The DM's step-by-step pipeline for preparing a session, and where prep files live. Use when prepping, planning or scoping an upcoming session, deciding what to prepare, checking whether prep is done, or creating a session's prep file.
---
# Session prep

The DM's pipeline is in [pipeline.md](./pipeline.md). **When prepping a session, strictly follow the structure established there:** work through steps 1-6 in order, do exactly what each step says, meet its `Done when` criteria before moving on, and do not skip, merge, reorder or invent steps. Stop at the "lock" point (step 3) for redesign. Stop preparing when the final check is all ticked.

## Working Across Turns

Treat prep as one continuous, phased collaboration. Stay on the current pipeline step across turns, using its rules and `Done when` criteria without asking the DM to repeat them. Once those criteria are met, mark the step complete, announce the transition, and continue to the next step without requiring another command or permission to advance. Pause when the DM asks; campaign-edit approval is still required independently. If new information reopens a completed step, address it without restarting the whole pipeline.

## Step 2: DM-led Question and Task Register

Before assembling the list, read all potentially relevant material within the agreed session scope, including surrounding campaign sections, cited original passages, relevant logs, reminders, player files, and rules. This reading belongs to step 2, not a new step. Step 2 establishes the questions and tasks; answers and execution belong later in the pipeline.

The DM normally fills most of the list while reading the campaign sequentially. Organize it under the scoped campaign section headings in campaign order, with a separate general/before-session heading for cross-cutting items. The agent may seed entries from chat, previous sessions, reminders, or reading, but must wait for the DM to confirm the list is ready before completing step 2.

Give every question or task a stable, session-wide ID (`Q001`, `Q002`, etc.). New entries always get the next unused number, even under an earlier heading; never renumber or reuse IDs. Preserve DM-authored wording verbatim and append IDs, status, and tracking metadata without rewriting it.

In step 3, resolve decisions and route execution tasks to steps 4-6. Reference each ID in the later answer or output and record its location and status beside the original entry. Assigning a task is not completing it. Before lock, every ID must be resolved, routed, or explicitly deferred/declined by the DM with a reason, with no unresolved decision affecting the locked material. Before the final check, audit every ID for a completed outcome or an explicit DM-approved deferral/decline with a reason.

## Where things live

| Item | Path | Fixed? |
|---|---|---|
| Session log (what happened) | `sessions/Session N/log.md` | Yes, history |
| Session prep (the plan) | `sessions/Session N/prep.md` | No, mutable until played |

For prep technique and running advice, see `dm-craft/books/lazy-dm.md` and `gameplay-guide.md`. Where they conflict with the pipeline, the pipeline wins.

Prep files start at Session 8. Sessions 1-7 have logs only. Once a session is played, its prep is a historical plan. The log wins on any conflict.

## prep.md format

Create it from this skeleton and tick the pipeline steps as they finish:

```markdown
# Session N prep

**Status:** scoping | reading | locked | designed | table-ready | played
**Starts:** <where and in-world date> · **Length:** <hours>

## 1. Scope
## 2. Open questions and desired changes
### Reading coverage
Material read within scope, including relevant surrounding material.
### General / before-session
- **Q001** [open] <question or task, preserving the DM's exact wording>
  - Follow-through: <later step; outcome/reference; or DM-approved deferral/decline and reason>
### <Scoped campaign section heading, repeated in campaign order>
- **Q002** [open] <question or task, preserving the DM's exact wording>
  - Follow-through: <later step; outcome/reference; or DM-approved deferral/decline and reason>
## 3. Resolved and adapted (lock)
Decisions by Q-ID; route execution tasks to steps 4-6.
## 4. Session design
Scenes, NPCs, clues, branches, with originating Q-IDs where applicable. DM-only material is marked.
### Combats
Each significant fight: objective or what players react to, expected rounds.
### Urn glow warnings
Per scene, undead within 300 feet of Elga, or "none".
### Blood Sense warnings
Per scene involving Agni, especially ambushes or hidden creatures: living creatures within 30 feet (even behind total cover or invisible), distances and when they enter or leave range, or "none". Mark "DM: Agni's Blood Sense: check thirst stage/activation; tell the player if active".
## 5. Table prep
Foundry, maps, tokens, props, music, with originating Q-IDs where applicable.
## 6. Study and practice
Record practice outcomes by Q-ID; audit every step 2 entry before the final check.
## Final check
- [ ] Story  - [ ] Players  - [ ] Play  - [ ] Combat  - [ ] Table  - [ ] Me
```

## Rules

- Every scene, fight, reward and NPC choice is checked against the `session-rules` skill.
- Check Agni's Blood Sense against `players/agni/vampire_details.md`: always active and unsuppressible while Thirsty; Composed activates it with a bonus action for 1 minute, Sated with an action for 10 minutes. If stage or activation is unknown, keep scene warnings conditional. Active Blood Sense reveals living creatures' exact locations, bloodied status and which has the lowest current HP, not appearance or identity. Do not equate it with sight, detect nonliving creatures such as undead, or automatically rule surprise for the whole party.
- Steps 2-3 use `campaign-state`, `timeline`, `cartographer` and `npcs`; step 4 fights use `combat`.
- Use `dnd-rules` within the existing steps: scan for fitting published mechanics in steps 2-3, resolve adoption questions before lock, include approved procedures and book citations with step 4 scenes, and study them in step 6. Suggest useful lesser-known rules without adding steps or reopening locked design merely to add an option.
- Do not prepare more than the session can reasonably reach.
- During prep, do not edit session logs. Record desired campaign-source changes in step 2; in step 3, apply relevant edits to campaign files once the DM agrees, and note the files and outcome in `prep.md`.
