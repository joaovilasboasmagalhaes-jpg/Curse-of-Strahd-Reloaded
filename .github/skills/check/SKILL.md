---
name: check
description: "Check a file, plan or selection for continuity problems."
argument-hint: "File or plan to check (defaults to the open file)"
disable-model-invocation: true
---
Work as the Continuity Reviewer (see [continuity-reviewer.agent.md](../../agents/continuity-reviewer.agent.md)).

Review the given file or plan, or the currently open file if none is given. Check it against the session logs, the calendar, travel, NPC facts and knowledge, and combat numbers. Report issues in order of severity with the source and the smallest fix.
