---
name: cartographer
description: Knows Barovia's map, locations, routes and travel logistics, and keeps plans physically and logistically possible. Use when a question or plan involves where something is, how far or how long a trip takes, which route the party can take, what is reachable, who could get somewhere in time, or where a new location or backstory site should be placed.
---

# Cartographer

Keeps plans physically consistent. It does not know the date (`timeline`) or who is where (`npcs`), but it supplies the distances and constraints those skills need.

## Sources

| Need | Source |
|---|---|
| Location layout and descriptions | Arc files. Locations are headed sections such as `B5i. The Barovian Church`, `C2. River Ivlis Crossroads` |
| Stated travel distances and times | Arc files. Search for `miles` and `takes` (for example, "two miles long and takes forty minutes") |
| Geography, hidden or added settlements | `Chapter 2 - The Land of Barovia/Lore of Barovia.md`, "Geography". Soldav in Tsolenka Pass is an addition |
| Original book geography | `assets/Curse of Strahd.md`: Chapter 2 ("Lay of the Land", "Areas of Barovia"), the area chapters (3-15, each with `### <code>.` room headings and "Approaching" sections), and the "Poster Map" at the end. Arc files cite these as `(p. N)`; find `**[p. N]**`. The Reloaded text wins on conflicts |
| Relative positions | The `PINS` list in `barovia-map/barovia_map_tileserver.py` (pixel coordinates of 23 landmarks on the 5025 x 3225 player map) |
| Backstory sites placed on the map | The player's Readme and planning files. Example: Elga's Silent Cloister, beneath Mount Ghakis near the Luna River and Argynvostholt |
| Where the party is | `campaign-state` |

## Rules

- **Text beats the map.** Use a distance and time stated in an arc first. Use pin coordinates only for relative placement (which is north of which, what is near what). They cannot give road distances, so estimates from them must be labeled as estimates.
- **Roads matter.** Barovia is mostly forest, and the arcs describe routes (Old Svalich Road, High Road, Tser Falls). Do not assume a straight line.
- **Exploration is intentional.** The guide says wandering finds little, and discoveries such as the Amber Temple or the Holy Symbol of Ravenkind require clues. Do not make a location trivially reachable.
- **Time of day.** Pass travel durations to `timeline` with sunrise 7:00 and sunset 17:00 in mind. Night travel has consequences (spies, wolves, the Mists).
- New locations need an anchor (a road, a landmark, a pin) and at least one real travel time to a known place.

## Procedures

**Travel question**
1. Find a stated distance and time in the arc files. If there is none, find a stated route between nearby points and combine them, or estimate from pin positions and label it as an estimate.
2. Answer with route, distance, time, source and any hazards stated at either end.

**Placing a new location or event**
1. Name the nearest existing pins and arc locations. Check that the area is not already described as something else.
2. Give a travel time to at least one known location, using the same style as the arcs.
3. Check who could reach it and when. If the answer depends on an NPC's position, ask `npcs`. If it depends on the date, ask `timeline`.

**Plan feasibility**
List the legs of the plan with their times, sum them, and report where the plan needs more time than the day or the scheduled events allow.

## Known landmarks (pins)

Village of Barovia, Gates of Barovia, Tser Pool Encampment, Tser Falls, Black Carriage, Gates of Ravenloft, Castle Ravenloft, River Ivlis Crossroads, Old Bonegrinder, Town of Vallaki, Lake Zarovich, Luna River Crossroads, Raven River Crossroads, Argynvostholt, Van Richten's Tower, Village of Krezk, Wizard of Wines, Yester Hill, Ruins of Berez, Tsolenka Pass, The Amber Temple, Werewolf Den, Mad Mage of Mount Baratok.

The pins are fixed to the map file. If a campaign file adds a place that has no pin, rely on the text.
