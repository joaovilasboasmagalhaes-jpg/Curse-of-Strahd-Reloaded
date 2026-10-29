---
name: foundry-statblock
description: Creates importable Foundry VTT actor JSON (NPC stat blocks) for the dnd5e system from a campaign stat block or a design. Use when asked to make, convert, export or fix a stat block for Foundry, to turn a Bestiary or NPC appendix entry into a Foundry actor, or to build a new monster/NPC for the VTT.
---

# Foundry stat blocks

Turns a stat block into a Foundry actor JSON the DM can import (right-click Actor directory > Import Data, or drop into a compendium). Numbers come from the `combat` skill sources. This skill only handles the Foundry format.

**Target:** Foundry v14, dnd5e system 6.0.x, rules 2014 (see `_stats` in the example).

## Folders

| Folder | Contents |
|---|---|
| `examples/` | Real Foundry exports used as format reference (learning). Add every new example the DM provides |
| `data/srd_spells_2014.json` | Spell name to Foundry `_id` for the dnd5e SRD 2014 spell pack (329 spells, release 5.3.3). Used to link spells |
| `output/` | The `.spec.json` inputs of the stat blocks created by this skill |
| `assets/stat_blocks/` (workspace root) | The importable `fvtt-Actor-<name>.json` files the builder generates |
| `build_actor.py` | Builder: `python build_actor.py <spec.json> [out.json]`. Default output is `assets/stat_blocks/fvtt-Actor-<name>.json` |

## Procedure

1. Get the numbers from the campaign (`Appendices/Bestiary.md`, `Appendices/Non-Player Characters.md`, arc files) or the original book via `combat`. Never invent stats; if a number is missing, ask the DM.
2. If the monster is unchanged from its default source stat block, tell the DM its source and confirm whether they still want a Foundry actor before proceeding. Do not build the actor until they confirm.
3. Write a spec file in `output/<name>.spec.json` (format below).
4. Run `python build_actor.py output/<name>.spec.json` (the actor goes to `assets/stat_blocks/`; the file name comes from the actor's name, so pass an explicit second argument to control it).
5. Check the JSON loads and compare totals with the source block (AC, HP, CR, attack bonus, DCs). Foundry computes the attack bonus (ability mod + proficiency from CR) and save DCs for spells itself, so confirm that the spec's abilities give the source's numbers. Where they do not (for example a fixed DC), set `bonus` or an explicit `dc`.
6. Tell the DM the file path and what was approximated. Ask for the import result so the format can be corrected from errors.

## Spec format

```json
{
  "name": "Rahadin, Kinslayer", "cr": 14, "size": "med",
  "type": {"value": "humanoid", "subtype": "dusk elf"}, "alignment": "lawful evil",
  "abilities": {"str": 14, "dex": 22, "con": 17, "int": 15, "wis": 16, "cha": 18},
  "saves": ["dex", "wis"], "skills": {"itm": 2, "ste": 2, "prc": 1},
  "ac": null, "hp": {"max": 180, "formula": "28d8 + 72"},
  "speed": {"walk": 35}, "senses": {"darkvision": 60}, "languages": ["common", "elvish"],
  "di": [], "dr": [], "dv": [], "ci": [], "legendary_actions": 3, "legendary_resistances": 0,
  "spellcasting": "int", "img": "", "token": "", "token_size": 1, "biography": "",
  "items": [ ... ]
}
```

- `size`: `tiny sm med lg huge grg`. `skills`: 1 proficient, 2 expertise (keys `acr ani arc ath dec his ins itm inv med nat prc prf per rel slt ste sur`).
- `ac`: `null` derives AC from an equipped `equipment` item; a number sets natural AC (`calcs: ["natural"]`, `flat`), as in the CoS import.
- `legendary_resistances`, `legendary_actions`, `lair` (initiative count; omit if no lair actions), `slots` (`{"1": 4, "3": 3}`), `book`, `page`, `dr_bypasses` (`["mgc"]`; also `di_`/`dv_`).
- Damage types, conditions and languages use Foundry keys (`slashing`, `fire`, `poisoned`, `common`).

Items (`kind` defaults to `feat`):

| kind | Fields |
|---|---|
| `feat` | `name`, `description` (plain text or HTML), `activation` (`action bonus reaction special legendary lair none`), `cost` (legendary), `uses` `{max, recover: day/lr/sr/recharge, formula}`, `activities` |
| `weapon` | `name`, `base` (`scimitar`), `wtype` (`martialM`), `props` (`fin lgt`), `damage` `[{n,d,type}]`, `reach` or `ranged: true` + `range`/`long`, `attack_bonus`, `activities` for riders. `natural: true` (bite, claw, unarmed): type natural, dice in the activity, `ability` set, `@mod` added to the first part |
| `spellcasting` | `name` ("Spellcasting" or "Innate Spellcasting"), `description`, `spells` `[{name, per_day?, uuid?}]`. One `cast` activity per spell, linked to the compendium spell |
| `equipment` | `name`, `ac`, `armor_type`, `base`, `dex_cap` |

Activities: `attack` (`kind`, `bonus`, `damage`), `save` (`ability`, `dc`, `on_save`: none/half, `damage`, `range`), `damage` (`damage`), `heal` (`heal`, e.g. `{"formula": "1", "type": "healing"}` or dice), `utility`. Legendary Resistance: activity `{"type": "utility", "activation": "special", "legres": true}` (spends `resources.legres`). Legendary actions: feat `activation: "legendary"`, and the cost is taken from `resources.legact`. Lair actions: `activation: "lair"`. Damage parts are `{n, d, type, bonus}`.

## Rules for good output

- **Write the full rules text in `description`**, including the DC and dice, so the sheet reads like the printed block. Activities make it clickable.
- Leave weapon damage as dice only (`1d6`): Foundry adds the ability modifier. Use `bonus` only for fixed extras.
- **Spells link to the compendium** (`Compendium.dnd5e.spells.Item.<id>`), because the cast activity resolves `spell.uuid` with `fromUuid`. The CoS exports link to `Actor.<id>.Item.<id>`, which only works inside the DM's own world, so do not copy that. On first use Foundry copies the spell onto the actor. Use the spec's `uuid` for a non-SRD or house spell. Add `slots`, and set `spellcasting` so DCs and attack bonuses compute.
- Multiattack stays a description-only feat; Foundry has no automation for it.
- Legendary actions: set `legendary_actions` and give each feat `activation: "legendary"` with `cost`.
- Reloaded changes win over the original book. Mention the source file in the answer, not in the actor.
- For significant fights, check the design principles in `combat` before finalizing the numbers.

## Open questions

Two examples are on file: Rahadin (hand-made, `examples/`) and Strahd (official CoS import, natural AC, legendary and lair actions, spells). Still unverified against a real import: that the generated cast links resolve in the DM's world, recharge activities, summon/transform activities, token ring and lighting. Ask the DM for the import result and for exports of those cases.
