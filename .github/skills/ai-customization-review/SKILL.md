---
name: ai-customization-review
description: "Use when the DM complains about AI behavior, suggests an AI workflow improvement, reports that an agent, skill, prompt, or instruction failed, or asks to audit or improve workspace AI customizations. Diagnose the cause and recommend or apply a durable, minimal fix."
---

# AI Customization Review

Improve the workspace's AI workflow when evidence points to a durable change. Treat user feedback as valuable diagnostic data, not as permission to add a rule for every isolated miss.

## Scope

Review workspace-level AI customizations that can affect the reported behavior:

- `.github/copilot-instructions.md` and other instruction files.
- `.github/agents/` agent definitions.
- `.github/skills/` skills and their references or templates.
- `.github/prompts/` prompt files.
- Other relevant, workspace-tracked AI configuration or customization artifacts.

Do not assume user-profile settings, hosted model behavior, unavailable tools, or product bugs can be changed from this workspace. Do not inspect or edit user-level configuration unless the DM asks and the files are available.

## Review Method

1. Identify the specific observed behavior or proposed improvement. Preserve the immediate user task and its constraints.
2. Locate the smallest set of customizations that control the behavior. Read their current content and any directly relevant workspace guidance before deciding.
3. Diagnose the likely cause: missing instruction, unclear trigger or description, conflicting rules, wrong agent/skill/prompt boundary, tool restriction, stale or duplicated guidance, missing reference, or behavior outside local configuration's control. Distinguish evidence from hypothesis.
4. Choose the smallest durable response. This may be to revise, clarify, combine, add, or remove a customization; add a focused reference or validation step; recommend a change without applying it; or make no change because the incident is isolated or not controllable here.
5. Consider tradeoffs and check that the proposed fix will not weaken canon, safety, privacy, user agency, or existing workflow boundaries. Avoid broad rules for narrow problems and avoid creating a new artifact when an existing one is the right home.
6. If the DM asks for a fix, implement and validate the scoped change. If they only report a problem or float an idea, inspect and provide the diagnosis and recommended change; apply it only when the intended change is clear and low-risk. Ask before changes with broad effects, especially user-level settings, tool permissions, subagent access, or core campaign/session rules.
7. State what was examined, the root cause or uncertainty, the recommended or applied change, and any behavior that cannot be controlled by workspace instructions.

## Guardrails

- Do not turn ordinary creative disagreement or a one-time content correction into an AI-customization review unless it signals a workflow problem.
- Do not change campaign canon, session logs, or player files as part of this review.
- Do not add instructions that force irrelevant skills, tools, or checks into every task.
- Do not duplicate an existing rule in multiple places unless a short routing instruction is needed to make it discoverable.
- Do not silently change the agent's autonomy, permitted tools, delegation rules, or user-level behavior.
- Follow the repository's existing Markdown, frontmatter, and Obsidian conventions.