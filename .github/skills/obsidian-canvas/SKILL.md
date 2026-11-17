---
name: obsidian-canvas
description: "Create, inspect, edit, and validate local Obsidian .canvas files in the open JSON Canvas format. Use for card/group geometry, Markdown source links, lane layouts, preserving manual edits, and checking structural validity versus native Obsidian rendering."
---

# Obsidian Canvas

Own the file representation and visual-editing workflow. For campaign cue selection and authority checks, use [session-running-notes](../session-running-notes/SKILL.md).

References: [JSON Canvas 1.0 specification](https://jsoncanvas.org/spec/1.0/) and [Obsidian Canvas help](https://help.obsidian.md/plugins/canvas). No plugin, dependency, service, or hosted board is required. Do not send campaign content to online converters.

## Format

- Root object: `nodes` and `edges` arrays. Nodes are in back-to-front stacking order; put scene groups before their cards.
- Every node needs a unique string `id`, supported `type`, integer `x`/`y`, and positive integer `width`/`height`.
- `text` nodes require `text` containing Markdown. Use these for independent summaries; editing them does not edit campaign source files.
- `file` nodes require `file` and can use a `subpath` starting with `#` to embed a heading/block. Editing an embedded source note may change that note: prefer text cards with links when sources must stay untouched.
- `link` nodes require `url`. `group` nodes may use `label`, `background`, and `backgroundStyle`.
- Optional `color`: preset strings `"1"` through `"6"` or a hex color. Always pair status color with explicit text.
- Edges need unique string `id`, `fromNode`, and `toNode` referencing existing nodes. Optional side values: `top`, `right`, `bottom`, `left`; end values: `none`, `arrow`. Avoid connectors that add no useful relationship.
- Use stable, descriptive IDs. Do not infer identity or progression from array order: native selection can reorder nodes to change stacking. Validate lane headers by coordinates, not serialization order.
- Preserve unfamiliar fields when updating an existing file; do not strip metadata or normalize the entire document unnecessarily.

## Layout

- Use full-width scene groups as the primary containers and aligned card coordinates for lanes. Avoid intersecting giant column groups with scene groups.
- Repeat short lane headers at major scene transitions. Native Canvas has no sticky headers, enforced lanes, or automatic reflow.
- Size lanes for the content: Time can be narrow; NPCs and alerts generally need more room. Same-beat NPC subcards can share a row inside the NPC lane.
- Leave space between cards and a group margin. Never stack simultaneous NPCs vertically without a clear same-beat label.
- Keep short cue cards readable at scene-level zoom. Link long prose instead of hiding it in tiny or heavily scrolled cards.
- Vertical spacing is ordinal unless the DM explicitly requests a measured timeline.

## Create or update

1. Read an existing board before editing. For a new one, agree path, scope, lanes, reading direction, and core/stretch distinction.
2. Write ordinary JSON with apply_patch. Store Markdown newlines as `\n` inside JSON strings.
3. Use vault-relative wikilinks for source notes, including headings: `[[Act I - Into the Mists/Arc C - Into the Valley#C4d. The Dancing Fire|Full scene]]`. The `/` separators inside these links are Obsidian link syntax, not shell paths.
4. Keep source links on cards or an explicit scene source card. Check actual file and heading spelling, including apostrophes.
5. For updates, retain IDs, manual coordinates, dimensions, text, and unrelated cards unless the requested change requires modifying them. Do not blindly regenerate the whole board.
6. Save the `.canvas` file in the vault. Local storage is the file itself, not browser storage. Git can track it like other text files.

## Focused validation

Use the tools already available; no package installation or standalone generator framework is needed.

1. Parse JSON, check root arrays and node/edge required attributes, integer geometry, positive sizes, supported types, unique IDs, enum values, and edge endpoints.
2. Check scene containment with the intended layout: every card should fit its scene group, and non-group card rectangles should not overlap unintentionally. Groups deliberately contain cards; that is not an overlap bug.
3. Check header positions and lane bounds, main progression, labels, and core/stretch separation. Geometry alone cannot validate chronology.
4. Resolve all local source links and their headings. Validate aliases separately from targets; links inside Markdown text are not JSON file-node paths.
5. Pair with the running-notes skill to audit cue meaning, conditions, provenance, and knowledge boundaries.
6. If authorized native-app access is available, open in Obsidian. Check clipping, readable scene-level zoom, navigation, and a reversible drag/edit/save/reopen round trip. Restore test edits and revalidate the saved JSON.
7. If native access is unavailable, state that clearly. Give the DM a short smoke test rather than claiming that a JSON parser or schematic preview proves the native rendering works.
8. Inspect the final diff and preserve unrelated local edits. Do not stage or commit unless requested.

## First-use handoff

Open the `.canvas` file inside the Obsidian vault. Double-click a text card to edit, drag to move, and drag an edge to resize. Cards save with the local Canvas file. Panning/zooming replaces ordinary document scrolling. Select a scene group and press `Shift+2` to frame it; `Shift+1` fits the whole board. For distant scenes, use the command palette's `Canvas: Jump to group`.

Summaries and source notes do not synchronize automatically. Manual lane alignment is intentional; ask for an update when source decisions change.
