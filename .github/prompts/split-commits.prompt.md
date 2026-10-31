---
description: "Split pending changes into coherent commits, optionally limiting scope and consulting Copilot session history."
agent: "agent"
argument-hint: "Optional scope or exclusions, e.g. only Session 8; exclude assets; plan only. Defaults to all changes."
---
Split the repository's pending changes into relevant, coherent Git commits and create those commits. Additional text supplied with this prompt specifies scope, exclusions, grouping preferences, or other constraints. If the user requests a plan only, do not stage or commit anything.

## Scope

- With no additional text, include ALL pending changes: staged, unstaged, untracked, deletions, and renames. Do not limit the task to the open file, current conversation, or changes made by Copilot. Ignored files remain ignored.
- Apply explicit scope and exclusions before grouping. Leave excluded content untouched and preserve its original staged or unstaged state, including excluded hunks in otherwise included files.
- Safety rules override the default of including everything. Never silently omit something: report every exclusion, blocked file, or unresolved change and the reason.
- Work on the current branch. Do not push, create a branch, amend existing commits, rewrite history, or discard changes. Do not start subagents without explicit permission.

## Inspect And Group

1. Read the repository instructions and load its Git skill if present. Follow its staging rules, size limits, secret checks, and commit-message conventions.
2. Record the initial branch, HEAD, status, and index state. Inspect both staged and unstaged diffs, and inspect untracked content before adding it. Use path-safe commands, including NUL-delimited output where filenames are parsed. Check recent commit messages for local style.
3. Group changes by purpose, not merely by directory, extension, author, or editing session. Keep a change with the dependent notes, code, tests, configuration, or assets required to understand and use it. Separate independent concerns; do not manufacture tiny commits or create intermediate states with broken dependencies.
4. If the purpose or relationship of changes is unclear, you may inspect relevant Copilot session history. Load the chronicle skill and use the session-store tools to search this repository by changed paths, topics, and recent sessions, then read only relevant turns. Treat history as supporting evidence: the current diffs determine what is actually being committed. If history is unavailable, proceed from the diffs and disclose material uncertainty; never invent intent or reapply superseded plans.
5. Account for every in-scope change in an ordered commit plan. Briefly show each proposed summary, its purpose, and included paths or hunk boundaries. Proceed without an extra approval round unless a safety rule requires confirmation or a material ambiguity prevents a defensible grouping. Respect an explicit plan-only request.

## Stage, Verify, And Commit

- Run the repository's required pre-staging safety checks on all candidate files, including untracked files. Do not commit secrets. For oversized or other restricted files, follow the Git skill's confirmation requirements; eligible groups may proceed while blocked files remain pending.
- Stage only the exact paths or hunks belonging to the next group. Do not use blanket staging commands that could sweep in other groups or excluded changes. Existing staging is evidence of intent, not permission to include unrelated content.
- When a file spans multiple groups, split it using precise non-interactive index patches, without editing the working-tree content merely to manufacture commits. Preserve pre-existing excluded index content. If the available tools cannot isolate it safely, ask before combining groups or changing the requested scope.
- Before EVERY commit, inspect the complete staged diff, not just filenames. Ensure the index contains only that group's intended changes, recheck required size limits on what is actually staged, and run whitespace checks plus the cheapest relevant validation or required repository gates. For partial-file commits, validate the staged snapshot where practical; working-tree tests alone do not prove that the staged version works. Report unavailable checks honestly.
- If validation fails, investigate only enough to explain the blocker. Do not modify the user's changes or widen scope to fix unrelated issues. Pause the affected group and report the failure; independent validated groups may proceed.
- Use a short imperative summary that explains the actual change. Follow the repository's message format and required trailers, including its Copilot co-author trailer where required. Do not invent issue IDs or claim tests that were not run.
- Commit one group at a time in dependency order. Verify each resulting commit's contents before continuing. If hooks fail or alter files, inspect the outcome and revalidate before retrying; do not bypass hooks or automatically absorb unrelated hook changes.
- Recheck status between groups. Newly appearing changes that were not in the initial inventory must be reported and left untouched unless the user authorizes including them.

## Final Accounting

Compare the final status and created commits with the initial inventory. Confirm that every in-scope change was committed exactly once or explicitly accounted for, excluded content retains its original state, and no working-tree content was lost.

Report the created commit hashes and summaries, validation actually performed, and any remaining changes with reasons. If everything eligible was included, say so. If nothing is pending, report that without creating an empty commit.