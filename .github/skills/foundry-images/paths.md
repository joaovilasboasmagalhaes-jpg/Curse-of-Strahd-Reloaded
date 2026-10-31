# Foundry image locations

`APP` = `C:\Program Files\Foundry Virtual Tabletop\resources\app\public` (served as the web root; core paths start `icons/`, `ui/`, ...)
`DATA` = `C:\Users\João Magalhães\AppData\Local\FoundryVTT\Data` (user data; paths start `systems/`, `modules/`, `worlds/`, `assets/`, `tokenizer/`)

Indexed = included in `index.tsv`. Counts are images on disk at the time of mapping.

## Core (APP)

| Foundry path | Count | Content | Indexed |
|---|---|---|---|
| `icons/weapons/<swords,axes,bows,crossbows,daggers,fist,guns,hammers,maces,polearms,sickles,slings,staves,thrown,wands,ammunition,artillery,clubs,misc>` | 900 | weapon icons | yes |
| `icons/equipment/<head,chest,body,back,feet,finger,hand,leg,neck,shield,shoulder,waist,wrist>` | 1267 | armor, clothing, rings, amulets | yes |
| `icons/magic/<acid,air,control,death,defensive,earth,fire,holy,life,light,lightning,movement,nature,perception,sonic,symbols,time,unholy,water>` | 1103 | spell and magic effect icons | yes |
| `icons/consumables/<drinks,eggs,food,fruit,grains,meat,mushrooms,nuts,plants,potions,vegetable>` | 582 | consumables | yes |
| `icons/commodities/<biological,bones,claws,cloth,currency,flowers,gems,leather,materials,metal,stone,tech,treasure,wood>` | 1239 | loot, crafting materials | yes |
| `icons/containers/<ammunition,bags,barrels,boxes,chest,kitchenware,misc>` | 301 | containers | yes |
| `icons/sundries/<books,documents,flags,gaming,lights,misc,scrolls,sports,survival>` | 429 | misc items | yes |
| `icons/tools/<cooking,fasteners,fishing,hand,instruments,laboratory,medical,nautical,navigation,scribal,smithing,tech>` | 326 | tools | yes |
| `icons/skills/<melee,movement,ranged,social,targeting,toxins,trades,wounds>` | 329 | ability/skill icons | yes |
| `icons/creatures/<abilities,amphibians,birds,claws,eyes,fish,invertebrates,magical,mammals,reptiles,slimes,tentacles,unholy,webs>` | 260 | creature parts, natural attacks, abilities | yes |
| `icons/environment/<cosmos,creatures,people,settlement,traps,vehicles,wilderness>` | 232 | scenery, tile and token props | yes |
| `icons/dice/`, `icons/pings/` | 7 | dice, ping icons | yes |
| `icons/svg/*.svg` | 120 | core default/status icons (`mystery-man.svg`, `item-bag.svg`, ...) | yes |
| `cards/` | 109 | poker deck card art | no |
| `ui/` | 37 | UI backgrounds, textures | no |
| `canvas/doors/` | 34 | door art | no |
| `nue/defaultscene/` | 3 | default scene art | no |

## dnd5e system (DATA)

| Foundry path | Count | Content | Indexed |
|---|---|---|---|
| `systems/dnd5e/icons/svg/actors/*.svg` | | default actor art (npc, character, group, vehicle, encounter) | yes |
| `systems/dnd5e/icons/svg/items/*.svg` | | default item art per type (spell, weapon, feature, ...) | yes |
| `systems/dnd5e/icons/svg/active-effects/*.svg` | | default active-effect art | yes |
| `systems/dnd5e/icons/classes`, `species`, `spell-tiers`, `currency`, `backgrounds` | ~56 | class/species/spell-level/currency icons | yes |
| `systems/dnd5e/tokens/<aberration,beast,celestial,construct,dragon,elemental,fey,fiend,giant,humanoid,monstrosity,ooze,plant,undead>` | ~460 | monster tokens by creature type, named like `VampireSpawn.webp` | yes |
| `systems/dnd5e/tokens/heroes` | 24 | player-type hero tokens (`ClericHuman.webp`) | yes |
| `systems/dnd5e/tokens/thumbs/<type>` | 180 | small thumbnails of the same tokens | yes |
| `systems/dnd5e/ui`, `ui/official` | 81 | sheet UI art | no |

## SRD / 5etools token art (DATA)

| Foundry path | Count | Content | Indexed |
|---|---|---|---|
| `assets/srd5e/img/bestiary/tokens/CoS/` | | Curse of Strahd monster tokens (`Strahd von Zarovich.webp`) | yes |
| `assets/srd5e/img/bestiary/tokens/<book>/` (MM, XMM, ...) | 206 total | monster tokens by source book | yes |
| `assets/srd5e/img/5etools-mirror-1/` | 102 | duplicate mirror of the same token subjects | no (duplicates) |
| `assets/srd5e/puck/` | 492 | numbered files, no usable names | no |

## Modules (DATA)

| Foundry path | Count | Content | Indexed |
|---|---|---|---|
| `modules/plutonium/media/icon/spell/` | 483 | spell icons named `<book>-<spell>.webp` | yes |
| `modules/plutonium/media/icon/feat`, `class`, `subclass` | 118 | feat, class, subclass icons | yes |
| `modules/plutonium/media/img` | 8 | module art | no |
| `modules/tokenizer-2/img/{omfg,thegreatnacho}` | 100 | token frame overlays | yes (as `token-frame`) |
| `modules/tokenizer-2/img/masks` | 7 | token masks | no |
| `modules/cosrl-escape-from-death-house/assets/{actors,items,images,scene,tiles,thumbnails}` | 58 | Death House adventure art (actors come as portrait and `-token`) | yes (actors, items, rest as world-asset) |
| `modules/fxmaster`, `tokenmagic`, `sequencer`, `tidy5e-sheet`, `levels`, `multi-token-edit`, others | ~500 | effects, UI | no |

## Campaign / user art (DATA)

| Foundry path | Count | Content | Indexed |
|---|---|---|---|
| `worlds/curse-of-strahd/assets/creatures`, `players` | ~23 | NPC and PC portraits (`Ireena.png`, `Avatar.Agni.webp`) | yes |
| `worlds/curse-of-strahd/assets/{macro-icons,handouts,scenes,maps,backgrounds,placeables}` | ~220 | macro icons, handouts, scene backgrounds | yes (kind `macro-icon`, `handout`, `scene`) |
| `worlds/curse-of-strahd/obsidian-assets/images` | 125 | images synced from the Obsidian vault | yes |
| `tokenizer/npc-avatars`, `npc-images`, `pc-avatars`, `pc-images`, `pasted` | ~30 | Tokenizer output: `Avatar.<Name>.webp` (portrait), `Token.<Name>.webp` (token) | yes |
| `tokenizer/_cache`, `_masks` | | Tokenizer scratch | no |

## Kinds in `index.tsv`

`item-icon`, `item-icon-magic`, `item-icon-campaign`, `spell-icon`, `feat-icon`, `class-icon`, `subclass-icon`, `species-icon`, `spell-tier-icon`, `core-svg`, `dnd5e-svg`, `dnd5e-icon`, `token-monster`, `token-hero`, `token-thumb`, `token-cos`, `token-srd`, `token-frame`, `portrait-campaign`, `avatar-campaign`, `macro-icon`, `handout`, `scene`, `world-asset`, `plutonium-icon`.
