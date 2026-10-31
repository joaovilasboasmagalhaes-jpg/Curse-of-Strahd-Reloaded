---
name: foundry-images
description: Finds the best Foundry VTT image (icon, token, avatar, portrait, default art) for actors, spells, items, feats and anything else that needs an image path. Use whenever creating or editing Foundry JSON (actor, spell, item, feat, token, scene) and an `img`, `token` or `texture.src` value is needed, or when asked where Foundry images live.
---

# Foundry images

Owner of every image path that goes into Foundry JSON. Any agent building an actor, spell or item must get its `img`/`token` from here instead of guessing a path. For statblocks, this includes an image for every embedded item, not only the actor portrait and token.

## Find an image

**Named items first**: Foundry already has an icon for many item names, so reuse the exact match before selecting a substitute.

```powershell
python .github\skills\foundry-images\find_image.py name Bite
```

This reads `item_icons.tsv` (2,263 item names harvested from the world's actors, items and packs, and the dnd5e monster/item packs; most-used local icon per name, Curse of Strahd icons first, plus alternatives). Parentheses are ignored (`Beak (Raven Form Only)` = `Beak`) and plural/singular both match. `build_actor.py` checks this map for every embedded item unless the spec provides an explicit `img`. It warns on stderr when an attack has no exact match; choose the closest icon with `python find_image.py attack <keywords>` and set `img` in the spec. For any other unmatched item, search the appropriate image category and set its `img` explicitly.

**Everything else** (or when no named item exists):

```powershell
python .github\skills\foundry-images\find_image.py <want> <keywords...> [-n 8]
```

`want` = `spell | feat | item | weapon | attack | armor | token | portrait | avatar | class | species | any`. It searches `index.tsv` (9,400 images: path, kind, keywords from file and folder names), ranks by keyword match, source priority and aliases (vampire to undead, necrotic to death/unholy, ...), and prints Foundry-ready paths. Examples: `token vampire spawn`, `spell necrotic ray`, `weapon sword`, `item ring`.

If the result is weak, try synonyms or a related word (`longsword` is matched as a compound; `sword` is safer), then `any`. The index is name-based, so confirm the top hit's name actually fits; do not pick a path that is not in the index.

For a Foundry statblock, make sure every `spec.items[]` entry resolves to an appropriate image: weapons and natural attacks, spells and spellcasting features, traits, actions, reactions, legendary/lair actions, equipment, and custom items. Explicit `img` values take priority; otherwise `build_actor.py` uses an exact Foundry item-name match when available. Choose and set an indexed image for each unmatched item; never accept a generic builder fallback. Generated activities inherit their owning item's image; use an activity-level `img` or spell-entry `img` override when distinct art is appropriate, then verify every generated activity has an image.

**Lookups need no live Foundry access**: `index.tsv` and `item_icons.tsv` are in the repo. Only rebuilding needs Foundry on this computer: `python build_index.py` (image files) and `python build_item_icons.py` (item-name map; copies the databases and reads them with Foundry's own Node, so Foundry can stay open). Rebuild after Foundry, systems or modules change or art is added. The generated files are ~0.9 MB and ~0.2 MB; watch the `git` skill's 1 MB guard.

## Which source to use (priority)

| Need | Look in (best first) | `want` |
|---|---|---|
| **Named campaign NPC/PC** portrait | `worlds/curse-of-strahd/assets/{creatures,players}`, `tokenizer/{npc,pc}-{avatars,images}`, `worlds/curse-of-strahd/obsidian-assets/images`, `modules/cosrl-escape-from-death-house/assets/actors` | `portrait`, `avatar` |
| **Actor `img` (sheet portrait)** | campaign art above, else the token art of the closest monster | `portrait` |
| **Token (`prototypeToken.texture.src`)** | `assets/srd5e/img/bestiary/tokens/CoS` (Curse of Strahd monsters), `systems/dnd5e/tokens/<type>` (`undead`, `beast`, `fiend`, `humanoid`, `heroes`, ...), `assets/srd5e/img/bestiary/tokens/<book>` | `token` |
| **Spell icon** | `modules/plutonium/media/icon/spell` (named by spell, e.g. `phb-fireball.webp`), then `icons/magic/<school-ish>` (`fire`, `death`, `unholy`, `holy`, `control`, `nature`, `light`, `lightning`, `water`, `air`, `earth`, `life`, `defensive`, `symbols`...) | `spell` |
| **Feat / monster ability icon** | `modules/plutonium/media/icon/feat`, `icons/creatures/{abilities,claws,magical,unholy}`, `icons/magic/*`, `icons/skills/*` | `feat` |
| **Weapons** | `icons/weapons/{swords,axes,bows,daggers,staves,...}` | `weapon` |
| **Armor / gear** | `icons/equipment/{chest,head,shield,hand,feet,finger,neck,back,...}` | `armor`, `item` |
| **Consumables, loot, containers, tools** | `icons/{consumables,commodities,containers,sundries,tools}` | `item` |
| **Class / subclass / species** | `systems/dnd5e/icons/{classes,species}`, `modules/plutonium/media/icon/{class,subclass}` | `class`, `species` |

Natural attacks (bite, claw): use `icons/creatures/{claws,mammals,reptiles,...}` via `any`.

## Path conventions

Foundry resolves paths relative to `Data/` (`C:\Users\João Magalhães\AppData\Local\FoundryVTT\Data`); core files come from the app's `public/` (`C:\Program Files\Foundry Virtual Tabletop\resources\app\public`) and are written as `icons/...`. Use forward slashes, no leading slash, and never a Windows path.

Full map of where images live: `paths.md`.

## Defaults and fallbacks

- dnd5e defaults (set in `DND5E.defaultArtwork`, `systems/dnd5e/dnd5e.mjs`): `systems/dnd5e/icons/svg/actors/{npc,character,group,vehicle,encounter}.svg`, `systems/dnd5e/icons/svg/items/{spell,weapon,equipment,feature,consumable,loot,tool,...}.svg`.
- Core fallbacks: `icons/svg/mystery-man.svg` (actor), `icons/svg/item-bag.svg` and the rest of `icons/svg/*`.
- `build_actor.py` uses `DEFAULT_ICON` for weapon/feat/spell/equipment when a spec gives no `img`; treat that fallback as a missing image, and set a curated `img` on every item in addition to actor `img` and `token`.
- The DM can generate custom art with the Tokenizer module (`tokenizer/` output). Say so when no good match exists (for named NPCs, suggest it) and use the closest token as the placeholder.

## Rules

- Pick the image from the index, then say in the answer which image was chosen for each actor/spell and why, so the DM can swap it.
- Prefer a specific match (same creature or spell) over a thematic one; use a thematic icon only when none exists.
- Keep a creature's `img` and token consistent (same subject); a token with a ring/frame is the DM's module setting, not part of the file.
- Campaign portraits can be spoilers (DM-only NPCs); do not reference them in player-facing text.
- Images outside the index (new uploads) are fine if the DM gives the path; add them by rebuilding.
