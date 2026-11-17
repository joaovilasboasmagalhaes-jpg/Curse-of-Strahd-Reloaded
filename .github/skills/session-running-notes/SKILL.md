---
name: session-running-notes
description: "Distill campaign sources into short DM running cues; organize vertical scene bands, parallel lanes, NPC cards, conditional branches, and prominent alerts. Use when creating or maintaining a session board or cue sheet, selecting what belongs on it, or reconciling its summaries with source notes."
---

# Session running notes

Own the content and information design of a running aid. For Canvas JSON and technical validation, use [obsidian-canvas](../obsidian-canvas/SKILL.md). Work directly; this skill does not authorize subagents.

## 1. Establish the source boundary

- Agree the session/arc portion and core versus stretch scope. Reuse choices already given.
- Read the existing board, scoped campaign sections, relevant logs, accepted prep decisions, and the necessary player references. Check the actual logs through `campaign-state`; do not replay completed conversations.
- Apply the workspace canon model, including protections for fixed backstories. Separate history, established facts, accepted plans, open questions, and optional additions.
- Prep is a reference here, not a workflow to advance. Do not change prep status, settle a question, mark an asset/rehearsal complete, or edit campaign sources while producing a board.
- Where a source conflict matters, use the established priority and expose any remaining ambiguity. A task assignment is not evidence that the work was done.

## 2. Extract actionable cues

- Choose what helps the DM at this moment: a sensory anchor, NPC attitude/question, available information, trigger, check, consequence, or transition.
- Write for a DM glancing up during play: the scene should be understandable across its lanes without reading paragraphs. These are memory cues, not prose summaries, read-aloud text, or instructions explaining how to DM.
- Default to a short title and 2-5 compact bullets per card. Prefer concrete keywords and fragments, usually 3-10 words per cue. These are guidelines, not caps: use longer sentences whenever a short cue would not be immediately understood. Clarity takes priority over brevity; do not make the DM decode shorthand or open a source just to understand the cue.
- Cut filler, repeated context, rationale, and delivery advice. Keep the observable detail or actionable trigger. Example: replace a paragraph about background camp company with `Low chatter; occasional laughter`, `Bowls passed; bread torn`, and `Hands warmed over coals`, under an `OPTIONAL ATMOSPHERE` label.
- Cover the scene, not every source detail: retain its sensory anchors, NPC attitudes/goals, and consequential triggers. Link explanation and secondary detail instead of reproducing them.
- Always order location and descriptive cues by first impression, then smaller details: lead with what would hit the characters first from their actual approach, then supporting sensations, nearby activity, and fine detail. Do not follow source-paragraph order or impose a fixed sight/sound/smell sequence; the strongest immediate impression may be any sense. Keep hidden or not-yet-perceptible details out of the initial description. Example for welcome and dinner: `Bright fire; warmth on the face` before `Smell of rabbit stew and bread`, then background Vistani activity and individual ingredients. Keep suggested additions labeled as optional atmosphere.
- Include a few fitting mundane actions to make inhabited places feel alive independently of the PCs: tending a fire, clearing bowls, fetching water, adjusting clothing, or briefly stepping away for personal needs. Usually put these under closer details, after the big picture; do not make every small action an event, clue, or invitation to interact. Use brief occasional cues, not a schedule or an exhaustive checklist. Source-backed or DM-requested details can be stated directly; label invented suggestions as optional atmosphere.
- Essential mechanics may need longer bullets; never shorten away a condition, exception, consequence, or required player warning. Split dense procedures into distinct beats/reference cards instead of shrinking the font or adding a wall of text.
- Keep essential DCs, ranges, counts, timing, action costs, limits, and consequences exact. Never invent them to fill a card.
- Link long tales, prophecies, manuscripts, and detailed procedures to their source headings. A summary is not a replacement script for clues whose wording matters.
- Put provenance on the card, or on an unambiguous scene source card. Distinguish an NPC's belief or legend from verified history and DM-only meanings.
- Mark unsettled decisions `UNRESOLVED`, incomplete execution `OPEN PREP`, conditional content `IF`, and optional invented description `OPTIONAL ATMOSPHERE`.
- Suggested atmosphere may enrich delivery, not add encounters, clues, clocks, supernatural powers, or mechanical penalties.
- Do not make decisions for PCs. Avoid NPC-to-NPC turn-taking unless the source moment needs it; keep the players involved.

## 3. Organize progression, not a timetable

Default for the Session 9 board is five aligned lanes inside variable-height scene/beat bands. This is a chosen layout, not a rule forbidding future changes.

| Lane | Include | Keep elsewhere |
|---|---|---|
| Time | Perceptible time cues, known appointments, relevant durations; label DM-only calendar knowledge | Do not invent a visible clock or assume an exact elapsed time from card spacing |
| Weather | General light, wind, precipitation, temperature, ambient fog | Local lamps, fire effects, landmarks, and terrain belong in Location |
| Location | Layout, landmarks, terrain, structures, local sounds/smells/light | Weather trends and NPC motives |
| NPCs | Named/grouped cards with distinct attitudes, goals, reactions, or information | Secret triggers and mechanical procedures can sit beside them in DM alerts |
| DM alerts | Checks, conditions, consequences, secrets, sensory-feature warnings, open decisions | Long explanatory source prose |

- Down means later; vertical distances are not elapsed-time measurements.
- Same-height cards belong to the same beat. Do not stack simultaneously available NPCs down the board merely to fit them: use side-by-side subcards in the NPC lane or a clearly labeled simultaneous roster.
- Use separate cards for speakers with distinct personalities or positions. Background participants can share a card. Recur an NPC at later beats when their role changes.
- Keep branches beside/within the triggering band, explicitly conditional; identify where they rejoin the main sequence.
- Omit empty cards. A lane can remain blank when nothing changes; label persistence on an earlier card if useful.
- Make alerts stand out using both text and color. The board remains DM-only even when a card says `TELL PLAYER`.
- Separate stretch material visually and retain source-triggered ordering rather than implying every optional event will happen.

## 4. Smaller-task routing

Load only the skills relevant to the task, and follow their actual references rather than copying their rules into this skill.

| Task | Existing skill |
|---|---|
| Starting position and played events | [campaign-state](../campaign-state/SKILL.md) |
| Interpret prep scope, accepted decisions, and open work, without advancing it | [session-prep](../session-prep/SKILL.md), reference only |
| Content boundaries, tone, PvP, rewards, house rules | [session-rules](../session-rules/SKILL.md) |
| Table usability, cue selection, pacing, sensory focus | [dm-craft](../dm-craft/SKILL.md), relevant digest only |
| Mechanical references and brief fitting-rule scan | [dnd-rules](../dnd-rules/SKILL.md); do not adopt new mechanics |
| NPC personality, knowledge, history | [npcs](../npcs/SKILL.md) |
| Dates, moon, time cues and durations | [timeline](../timeline/SKILL.md) |
| Routes, travel, physical layout and range context | [cartographer](../cartographer/SKILL.md) |
| Encounter triggers, statistics and tactical procedures | [combat](../combat/SKILL.md); do not redesign |
| Mists, souls, sunlight, other Barovian overrides | [barovia-rules-reference](../barovia-rules-reference/SKILL.md) |

For Elga and Agni, first read their player Readmes and then the actual feature references. Check every included beat for Urn and Blood Sense effects, including concealed creatures and range entry/exit. Use conditional warnings when activation or positions are unknown; never invent exact positions, suppress a clue, equate the sense with sight, or count PCs as undead. Flag any applicable Session 0 conflict rather than quietly changing a character feature.

## 5. Maintain without losing the DM's work

1. Read the current board and relevant changed sources.
2. Identify existing cards by stable ID and source/beat, not array position.
3. Make the smallest edits. Preserve custom text, coordinates, sizes, colors, unrelated cards, and source links unless the request requires changing them.
4. If source changes conflict with a manual summary, ask for a decision. If the task explicitly asks for a full rearrangement, preserve the content and IDs where possible.
5. Do not overwrite an existing board by regenerating it from scratch. Source summaries do not synchronize automatically.
6. Validate with `obsidian-canvas`, then check actual content: source fidelity, temporal alignment, branch conditions, character knowledge, open work, and core/stretch boundaries.
7. Apply a glance-test to every edited scene: can the DM scan across and immediately grasp the setting, who is doing what, and what needs attention? Compress any card that requires paragraph reading; preserve essential mechanics and source links. Do not rewrite unrelated or hand-edited cards without being asked.

Deliver the board and a brief account of validation and open items. Do not claim a session is ready merely because the board exists.
