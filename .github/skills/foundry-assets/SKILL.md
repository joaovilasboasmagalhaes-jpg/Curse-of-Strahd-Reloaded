---
name: foundry-assets
description: 'Look up and manage player handouts and other campaign assets, their image text/transcriptions, source files, Foundry Player Handouts journals and pages, and player visibility/ownership. Use when finding a letter, invitation, journal, portrait, clue or handout; asking what an asset says or whether players can see it; adding asset notes/tags; or refreshing the asset catalog. Not for token/item/spell icon selection (use foundry-images).'
---

# Foundry assets

This skill owns the DM-only player-handout catalog, not campaign canon or the token/icon index.
The portable [catalog](./catalog.json) stores paths, hashes, cached text, notes/tags, journal references,
native journal text and the last observed permissions. Search it instead of repeatedly opening images.
Never load the entire catalog into context.

## Lookup

Run from the repository root:

```powershell
& .github\skills\foundry-assets\assets.ps1 search invitation
& .github\skills\foundry-assets\assets.ps1 search "lost and missing" Doru
& .github\skills\foundry-assets\assets.ps1 show --id "worlds/curse-of-strahd/assets/handouts/death-house/durst-invitation.png"
```

Search is case-insensitive, matches all supplied terms, and includes paths, journal/page names,
transcriptions, notes, tags and native journal text. Results are compact summaries with 240-character
text excerpts and their observation timestamp, not entire journal dumps.
For broad searches, use `rg` against the catalog to locate a name first, then a targeted lookup.
`show --id` requires the exact asset `id` returned by search. For a native text-page result, use
`show --journal "<journalId>" --page "<pageId>"` to read that page and its player permissions.
Paths in Foundry use forward slashes;
filesystem/tool paths on Windows use backslashes.

## Refresh and source locations

When local Foundry is available, refresh once at the start of asset work, especially before answering
visibility questions or transcribing new/changed images:

```powershell
& .github\skills\foundry-assets\assets.ps1 refresh
```

The [launcher](./assets.ps1) uses Foundry's bundled Electron as Node; no package installation or server
login is needed. The [reader](./assets.cjs) reads **temporary copies**, never opens the original
databases with LevelDB, and never modifies Foundry files or player permissions. Foundry may be closed.

- Data root: `%LOCALAPPDATA%\FoundryVTT\Data`.
- Main source: `worlds\curse-of-strahd\assets\handouts`, recursively (all file types).
- Journal documents: `worlds\curse-of-strahd\data\journal` (LevelDB, not a JSON file).
- Folder membership: `data\folders`; player roles: `data\users`.
- Includes the journal folder named **Player Handouts** and all its descendants.
- Includes assets referenced by those pages (`src` and HTML image sources), even outside `handouts`,
  including `handout-generator` and portraits in `assets\creatures`.
- Includes native text pages even when no image exists; preserves their HTML as the source.
- Only user ID, display name and role are read into the permission calculation; no authentication
  details are saved.

Optional overrides: `--data <Data-root> --app <resources-app-root> --catalog <catalog-file>
--folder <journal-folder-name>`. A compatible Node runtime can run `assets.cjs` directly instead of
the launcher; refresh still needs Foundry's compatible `classic-level` installation.

This is a **best-effort disk snapshot**, not an authenticated live browser query. Copies made while
Foundry writes are not transactional across databases. If copying/reading fails, the command fails
explicitly and leaves the previous catalog intact; retry when Foundry is idle or closed. Do not repair
or write its databases. A missing/ambiguous Player Handouts folder is an error, not an empty success.
If Foundry isn't installed/accessible, use the saved catalog and say that visibility is last-known,
including `checkedAt`. Never describe a failed refresh as current. Nothing polls in the background;
run refresh on demand after uploads or permission changes.

## Visibility: report permissions, not assumptions

Every journal and asset reference records effective permissions per non-GM, non-banned user:

| Level | Meaning |
|---|---|
| 0 | NONE |
| 1 | LIMITED; **not** full observer access |
| 2 | OBSERVER |
| 3 | OWNER |
| -1 | INHERIT; resolve to the parent journal |

An explicit player override, including NONE, beats default ownership. Page inheritance is resolved
independently for each player. Both journal and page levels are kept. `journalInSidebar` needs journal
OBSERVER or OWNER; `pageReadable` needs page OBSERVER or OWNER. A readable page does not itself imply
its parent appears in the sidebar. Assistant/Gamemaster roles are excluded from player reporting.
LIMITED is not promoted to readable image/full text access.

- Report all/some/no players with observer access **per reference**; mention limited-only access.
  An asset may be shared through one journal but private through another.
- A loose/unreferenced file has **unknown sharing outside this folder**, not confirmed private.
- Folder membership or a file existing under `handouts` does not grant permission.
- Modules and unsaved live changes may differ from the core disk permissions.
- "Show to Players" can display a page temporarily without persistent ownership. This catalog
  **does not track those events or prove that a player actually saw/read something**.
- A Foundry image URL is not an access-control boundary; journal permissions do not make a known
  static file URL secret.
- Asset text and DM annotations are not automatically player-known or campaign canon. Keep spoilers
  out of player-facing answers, and use campaign-state for what has actually happened at the table.

## Cache image text once

1. Read `transcription` first. `verified` is reusable for that SHA-256; `pending` needs work.
   `stale` retains old text for reference but **must not** be quoted as the current image.
2. Prefer an existing matching Foundry text page as a draft. Compare it to the image before calling
   it a verified transcription: text-only pages may be older, abridged or different.
3. If missing/stale, inspect the local image once with `view`. If a WebP or oversized image cannot
   be displayed, use an already-installed local decoder to create a temporary PNG preview in the
   session workspace. Do not upload assets to external OCR services, install tools without need,
   or alter the original image. Inspect higher-resolution crops if text is too small.
4. Transcribe visible text faithfully, including typos and dates. Use `[illegible]` / `[obscured]`
   for uncertainty, never guess or silently "correct" it to campaign lore. For an image with no
   readable text, explicitly cache `[No readable text: brief visual description.]`.
5. Save UTF-8 text in a temporary session file and associate it with the original asset:

```powershell
& .github\skills\foundry-assets\assets.ps1 set-text --id "worlds/curse-of-strahd/assets/handouts/death-house/durst-invitation.png" --file "C:\path\to\session\transcript.txt" --source "Visually checked original image"
```

The command requires the image still to match its catalog hash. It stores the text, provenance,
timestamp and original hash, and reuses it for byte-identical copies. Refresh preserves text and
notes/tags; changed/missing images make old text stale. Removed assets remain `unreferenced` with
no old permission claims. External URLs are cataloged but not fetched or hash-verified.

For a verified transcription, no image re-analysis is necessary until its hash changes. Never mark
automated OCR output verified without checking it. Native journal text is separate from image text.
Use `notes` and `tags` for DM metadata by surgically editing the matching catalog record; these
fields survive refresh. Do not put an interpretation or story correction in the transcription.
Remove temporary previews/transcription files when finished.

The initial catalog includes checked text for the invitation, letter, adventurer journal, torn
vampire page and missing-person records, plus portrait text checks. The eight handwritten
`cult-victims` tables are labeled by language with **pending** full transcriptions, not invented
OCR or verified empty text. Their notes flag graphic content; pages 3 and 7 describe sexual violence
and conflict with the Session 0 boundary. Preserve that warning when finding handouts for players.

## Validation

```powershell
$env:ELECTRON_RUN_AS_NODE = '1'
& 'C:\Program Files\Foundry Virtual Tabletop\Foundry Virtual Tabletop.exe' --test .github\skills\foundry-assets\assets.test.cjs | Out-Host
if ($LASTEXITCODE -ne 0) { throw "Asset tests failed" }
```

Tests use temporary fixtures, not the live world.
