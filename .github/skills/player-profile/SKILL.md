---
name: player-profile
description: "Assess and update player profiles from session actions, reactions, choices and campaign history. Use when inferring a player's behavior, wishes, motivations, engagement or play style, reviewing patterns across sessions, or updating player_profile.md after recording a session. Separates observed character actions, stated player preferences and evidence-backed hypotheses."
---

# Player Profile

Build a useful, revisable understanding of what each player enjoys and wants from play. Make inductions from actual play, but never present them as established facts about the person.

## Sources and scope

- Read `players/Readme.md` for the player-to-character mapping, then each relevant `players/<name>/Readme.md` before their other files.
- Read the existing `players/<name>/player_profile.md`, if present. Preserve explicit preferences, their sources and any DM corrections.
- Use the `campaign-state` skill to locate or recall played events. Read the actual `sessions/Session N/log.md` for evidence; the digest is a finding aid, not a substitute.
- For a single-session update, use that session and earlier sources needed to check existing hypotheses. For a campaign-wide assessment, read the available logs in the requested range and state the coverage and gaps.
- Use player questionnaires, Session 0 answers and explicit DM reports as sources of stated preferences. Read backstory or mechanics only as needed to distinguish character motivation and available choices from player preference.
- Campaign plans, prep and unplayed concepts are not evidence of player behavior. Do not treat an NPC's reaction or a DM-designed scene as a player's reaction.
- Work directly. Do not launch subagents without the DM's permission.

## Procedure

1. **Set coverage.** Identify the session or campaign range and players being assessed. In post-session mode, review every player represented in the log; do not assume everyone attended or that every character action has an identifiable player behind it. If attribution is unclear, leave it unresolved.
2. **Extract observations.** Find concrete choices, initiated scenes, questions, follow-ups, risk-taking, problem-solving, resource use, social approaches and explicitly recorded reactions or feedback. Cite the source file with a heading or short identifying event. Distinguish:
   - what the character did or wanted;
   - what the player explicitly said they enjoyed, disliked or wanted;
   - what the DM reported about the player's engagement.
   Do not embellish a sparse log with imagined enthusiasm, frustration, tone or intent.
3. **Make inductions.** Look for patterns in preferred activities, decision-making, initiative, collaboration, spotlight, desired stakes, recurring interests and story wishes. A single revealing choice can support a tentative hypothesis; repeated voluntary choices across different situations support a stronger one. Explain the bridge from observation to hypothesis.
4. **Test alternatives.** Consider character duty, limited options, mechanics, party pressure and immediate necessity. Seeking a fight does not by itself establish a love of combat; a character's fear does not establish a player boundary. Silence, absence or missing log detail is not evidence of boredom or dislike. Keep a character-only observation when no player-level inference is warranted.
5. **Compare with the profile.** Add support or counterevidence to existing hypotheses rather than duplicating them. Preserve explicit statements even when behavior differs; record the tension and possible context instead of silently overruling the player. Revise or retire unsupported hypotheses. Never promote an inference to a stated preference without explicit player feedback or DM confirmation.
6. **Persist when requested.** An assessment-only request returns findings without editing files. An update request, including the post-session prompt, authorizes writing observations and clearly labeled hypotheses without waiting for confirmation of each one. Follow the storage rules below.
7. **Report.** Briefly list profiles changed, material new or revised hypotheses, evidence gaps and any questions worth checking with the DM. Say when there was no supported change.

## Evidence and confidence

Keep these categories separate:

| Category | Meaning |
|---|---|
| Stated preference | Explicit player feedback or a DM-confirmed preference; cite who reported it and where. |
| Observation | A sourced action or reaction, with no assumed motive. |
| Hypothesis - low | A plausible induction from a single or ambiguous example, with meaningful alternatives. |
| Hypothesis - medium | Repeated evidence, but narrow context or credible competing explanations remain. |
| Hypothesis - high | Consistent voluntary behavior across multiple sessions and contexts, with alternatives considered. Still not confirmed. |

Confidence describes support for an inference, not a score for the player. Do not use personality diagnoses, real-world psychological labels or sensitive personal inferences. Stay within table behavior and play preferences. Do not infer consent or content boundaries; use explicit feedback and the `session-rules` skill for the table's agreed limits.

## Storage and update rules

- Store DM-only findings in `players/<name>/player_profile.md`. Reuse the [profile template](../player-arc/player-profile-template.md) for missing profiles, leaving unknown fields as `Not established`. Create one only when there is attributable evidence, not just because a player has a folder.
- Preserve existing profile structure and confirmed material. Add the assessment sections from the template if missing; do not rewrite a questionnaire-derived profile as though it came from session observations.
- Record coverage so readers know which sessions were assessed. Keep concise observations with relative source links and enough event detail to verify them.
- For each hypothesis, include its claim, confidence, supporting observations, counterevidence or alternatives, and a modest preparation implication or question that could test it. Preparation implications are suggestions, not edits to campaign plans or predetermined character choices.
- Re-running the same session must not duplicate observations or inflate confidence. Update the existing evidence for that session. If the log was revised, correct or remove superseded observations and reassess dependent hypotheses; preserve unrelated evidence and flag conflicts with explicit DM confirmations.
- When creating a profile, add a relative link in that player's Readme under a DM-only section. Do not reclassify fixed backstory files.
- Do not edit session logs, fixed backstories, campaign files or player plans during profile maintenance. Hypotheses are DM aids, not character knowledge or campaign canon.

## Entry shape

Use the existing profile's prose or lists; a compact hypothesis can look like:

- **Hypothesis:** May enjoy investigating unresolved NPC motives.
  - **Confidence:** Low.
  - **Evidence:** Session N, named scene: initiated a follow-up question after the immediate task was resolved (link to the log).
  - **Alternatives / counterevidence:** Could be pursuing the character's specific obligation; no broader pattern yet.
  - **Preparation implication / check:** Offer an optional follow-up lead and observe whether they pursue it; do not assume they want a mystery-centered arc.
