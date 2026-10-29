---
name: git
description: "Git workflow rules for this repository, including the large-file guard applied before any commit. Use when staging, committing, pushing, or when asked whether a file should be added to the repository."
---
# Git rules

## Large-file guard (mandatory before every commit)

Never let something too big into the repository without the user's explicit confirmation.

**Limits (per file, size on disk):**
- **Over 1 MB**: flag and ask.
- **Over 5 MB**: flag and strongly recommend against; ask twice if needed.
- **Over 100 MB**: refuse (GitHub rejects it). Offer alternatives only.
- **Binary or generated files** (epub, pdf, zip, images, videos, audio, map tiles, db dumps, `.venv`, caches): flag at **500 KB**.

Plain-text campaign notes are normally tiny; a large markdown/JSON file is a sign of a pasted book or an export.

**How to check** (before `git add` / `git commit`, and again on what is actually staged):

```powershell
git --no-pager status --porcelain
git --no-pager diff --cached --name-only -z | % { $_ -split "`0" } | ? { $_ } | % { Get-Item -LiteralPath $_ -ea 0 } | ? { $_.Length -gt 500KB } | % { "{0:N0} KB  {1}" -f ($_.Length/1KB), $_.FullName }
```
Also check untracked files that `git add -A` / `git add .` would pick up (`git ls-files --others --exclude-standard`).

**If anything is flagged**, do not commit it. For each flagged file tell the user the path, size and why it is flagged, then ask (with the ask tool) whether to commit it anyway, and offer an alternative:

- **Move it outside the repo**, e.g. next to the external books folder (`E:\Users\João Magalhães (HDD)\Documents\Books`) and reference it by path in the notes.
- **Ignore it**: add it to `.gitignore` (and `git rm --cached` if already tracked).
- **Shrink it**: split, trim, compress, or summarise it (as the `dm-craft/books/*.md` digests do for books).
- **Git LFS** for binaries that must be versioned.
- **Commit anyway**, only on the user's explicit yes for that specific file.

Unflagged files may be committed while flagged ones wait for the answer. Never override a "no".

Pre-existing large tracked files under `assets/` (source book text and epubs) are known; do not re-flag them unless modified in the change being committed. The Foundry example JSON in `.github/skills/foundry-statblock/examples/` is also large; flag it only if it grows.

## Other conventions

- Use `git --no-pager`; never force-push or rewrite history unless asked.
- Do not commit secrets or `.obsidian/*.json` (ignored).
- Commit messages: short imperative summary; end with the trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
