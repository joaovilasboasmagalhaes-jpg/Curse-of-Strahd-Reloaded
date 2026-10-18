# Copilot Cheat Sheet

In any chat, type `/` and pick one of these five. That is all you need to remember.

| Command | Use it to |
|---|---|
| `/story` | Understand the story, or find plot holes. Example: `/story plot holes in Arc K`, `/story explain Act III` |
| `/player` | Work on a player's backstory. Example: `/player grim`. With no name it shows where every player stands |
| `/prep-session` | Get a quick outline for the next session (for full prep, see below) |
| `/post-session` | Update the campaign notes after you write a session log |
| `/check` | Check a file or plan for mistakes against what already happened |

Everything else is automatic. You can also ask a normal question at any time ("what's the date?", "how far is Vallaki?", "what would Donavich do?"), and the right knowledge loads by itself.

## Backstories: you only make one decision

Working on one player for a while? Pick **Backstory Developer** in the chat's agent picker once, and keep talking in that chat. Use `/player <name>` to start or to see where everyone stands.

`/player <name>` looks at where that player is and does the next step. You answer its question.

- Exploring ideas: nothing in the campaign changes.
- When you like an idea, tell it: "choose this one".
- Next time you run `/player <name>`, it lists the exact edits and waits for your OK before touching any campaign file.

## Session prep

For full prep, pick **Session Prep** in the agent picker and say which session ("prep session 8"). It follows your pipeline (`.github/skills/session-prep/pipeline.md`) one step at a time and keeps the plan in `sessions/Session N/prep.md`. It tells you when the lock point is reached and when you can stop preparing.

Each session has a folder: `sessions/Session N/log.md` (history, fixed) and `prep.md` (the plan, from Session 8 on).

## Things only you can do

- Confirm the in-world date when asked. It is `Neyavr 1` (guessed) until then.
- After each session, write the log and run `/post-session`.
- Optional: fill in `players/<name>/player_profile.md` so ideas fit what the player enjoys. If it is missing, Copilot asks instead of guessing.

## Safety

- Session logs are never changed unless you ask.
- Nothing in the campaign files changes without your approval.
- Ideas stay in `players/<name>/concepts/` until you choose them.
- Plot holes are written down in `_other/plot_holes.md`.

## If something seems off

Say what was wrong in the chat. If it keeps happening, ask Copilot to fix the matching file in `.github/skills/`.
