---
name: session-prep
description: The DM's step-by-step pipeline for preparing a session, and where prep files live. Use when prepping, planning or scoping an upcoming session, deciding what to prepare, checking whether prep is done, or creating a session's prep file.
---
# Session prep

The DM's pipeline is in [pipeline.md](./pipeline.md). Follow it in order and stop at the "lock" point (step 3) for redesign. Stop preparing when the final check is all ticked.

## Where things live

| Item | Path | Fixed? |
|---|---|---|
| Session log (what happened) | `sessions/Session N/log.md` | Yes, history |
| Session prep (the plan) | `sessions/Session N/prep.md` | No, mutable until played |

Prep files start at Session 8. Sessions 1-7 have logs only. Once a session is played, its prep is a historical plan. The log wins on any conflict.

## prep.md format

Create it from this skeleton and tick the pipeline steps as they finish:

```markdown
# Session N prep

**Status:** scoping | reading | locked | designed | table-ready | played
**Starts:** <where and in-world date> · **Length:** <hours>

## 1. Scope
## 2. Open questions and desired changes
## 3. Resolved and adapted (lock)
## 4. Session design
Scenes, NPCs, clues, branches. DM-only material is marked.
### Combats
Each significant fight: objective or what players react to, expected rounds.
### Urn glow warnings
Per scene, undead within 300 feet of Elga, or "none".
## 5. Table prep
Foundry, maps, tokens, props, music.
## 6. Study and practice
## Final check
- [ ] Story  - [ ] Players  - [ ] Play  - [ ] Combat  - [ ] Table  - [ ] Me
```

## Rules

- Every scene, fight, reward and NPC choice is checked against the `session-rules` skill.
- Steps 2-3 use `campaign-state`, `timeline`, `cartographer` and `npcs`; step 4 fights use `combat`.
- Do not prepare more than the session can reasonably reach.
- Do not edit campaign files or logs during prep. Propose arc changes as edits and say which file; apply them only when the DM agrees.
