---
name: foundry-rolltable
description: Creates importable Foundry VTT RollTable JSON from rollable tables, weighted lists, or dice-range tables. Use when asked to create, convert, export, or fix a random table for Foundry.
---

# Foundry rollable tables

Use [build_table.py](build_table.py) to turn a compact JSON spec into a Foundry v14 RollTable. Python standard library only; no live Foundry connection required.

## References and scope

- Format references: the DM's [exported tables](../../../assets/rollable_tables/), exported from Foundry 14.368 / dnd5e 6.0.3. These are examples, not templates to mutate.
- Uses the exported v14 result fields: `type: "text"`, `name`, `description`, `range`, `weight`, `drawn`, and `documentUuid: null`.
- Generates fresh 16-character result IDs; omits export provenance, timestamps, world folder IDs and module flags. Tables default to GM-only ownership, replacement enabled and roll display enabled.
- Text results only. Native `@UUID[...]{label}` links and `[[/r 1d6]]` inline rolls can be written in descriptions; the builder preserves text/HTML verbatim. It does not resolve or verify linked documents. Plutonium `@creature[...]` tags require that module; prefer plain names or verified native UUID links.
- This creates import files, not campaign canon. Get table content from the requested source; do not silently change its outcomes or probabilities.

## Procedure

1. Read the source table and preserve its wording, ranges and formula. For campaign design or rules changes, use the relevant campaign/rules skills separately.
2. Write a spec under this skill's `output/<name>.spec.json`. Use the example below or [example.spec.json](examples/example.spec.json).
3. Use weights for relative frequencies, or explicit ranges for an existing dice table. Never mix the two modes. Ask about ambiguous gaps, overlaps, or natural-roll versus modified-total rules rather than inventing a correction.
4. The default table/result icon is the indexed core `icons/svg/d20-grey.svg`, also present in the DM's urn export. Use `foundry-images` for custom art and set `img` explicitly.
5. From the workspace root, run:

   ```powershell
   python .github\skills\foundry-rolltable\build_table.py .github\skills\foundry-rolltable\output\<name>.spec.json
   ```

   Output defaults to `assets/rollable_tables/fvtt-RollTable-<name>.json`. An optional second positional path selects another output. Existing files are refused unless `--force` is supplied; never overwrite the DM's reference exports.
6. Compare the output against the source: formula, every outcome/range, replacement and visibility. Report the generated file and any limitations.
7. In Foundry's **Roll Tables** directory, create a new table, right-click it, choose **Import Data**, select the generated JSON, then import. Check the formula and perform a test draw. Actual in-app import remains unverified until the DM tests it; do not claim otherwise.

## Keep the sheet compact

- The table-level `description` is a header, not a prep document. Default to one short paragraph of 1-3 sentences: purpose/source and essential draw timing only.
- Do not put rules primers, design explanations, full encounter instructions or repeated source details in the header. Leave those in the campaign/prep sources.
- Keep outcome-specific flavor and runnable mechanics in that result's `description`. Preserve necessary DCs, damage, durations and choices; do not shorten by dropping rules.
- Essential DM-only warnings may use one additional compact paragraph, or stay in the relevant result. Preserve conditional triggers without copying entire player features.
- Check the generated header's length before delivery; do not truncate text automatically in the builder.

## Spec format

### Weighted list

```json
{
  "name": "Example discoveries",
  "description": "<p>A demonstration table, not campaign content.</p>",
  "replacement": true,
  "displayRoll": true,
  "results": [
    "Nothing unusual",
    {"name": "Discovery", "description": "<p>A small discovery.</p>", "weight": 2}
  ]
}
```

Strings have weight 1. Weights must be positive integers. The example creates ranges `[1, 1]`, `[2, 3]` and formula `1d3`. Optional result fields: `name`, `description`, `img`, `weight`. Each result needs a nonempty name or description. Unknown fields are rejected to catch misspellings.

### Explicit dice ranges

```json
{
  "name": "Example combined-dice table",
  "formula": "d12 + d8",
  "results": [
    {"range": [2, 10], "description": "First outcome"},
    {"range": [11, 20], "description": "Second outcome"}
  ]
}
```

- Ranges are inclusive integer pairs. With explicit ranges, weight defaults to 1, matching the reference exports; the formula and ranges determine draw probabilities. Do not normalize in Foundry unless you intend to change the ranges/formula.
- Formula can be omitted for tables starting at 1; it becomes `1d<highest endpoint>`.
- Supported formulas: sums/differences of ordinary dice and integer constants, e.g. `1d100`, `d12 + d8`, `1d20 + 3`. No dice modifiers, parentheses, data references, or descriptive skill labels. Resolve a skill modifier to its actual number and cover the resulting total range, or ask the DM how it should work.
- Every possible total must be covered, and ranges cannot extend outside the formula bounds. Overlaps fail unless the spec explicitly sets `allow_overlaps: true`. An overlap can return multiple matching results, not a priority/override.
- The urn reference has overlapping ranges at 1 and 20 and the descriptive formula `1d20 + Wisdom (Religion)`. Do not copy this formula as executable dice syntax or assume "Natural 1/20" labels implement special handling. A natural die result and a modified total are distinct; this builder does not automate that distinction.
- Optional table fields: `description`, `img`, `formula`, `replacement`, `displayRoll`, `allow_overlaps`. Result `drawn` is always reset to false; no world ownership or folder IDs are copied.

## Validation

```powershell
python -B -m unittest discover -s .github\skills\foundry-rolltable -p "test_*.py" -v
```
