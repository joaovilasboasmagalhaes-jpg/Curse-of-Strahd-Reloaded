---
name: dungeondraft-maps
description: Reads, validates, previews and generates Dungeondraft (.dungeondraft_map) battlemaps - terrain painting, object placement (trees, clusters, obstacles), roads, mud, shortcuts and map resizing - designs maps for chases and encounters, and converts maps into Foundry scenes with walls, difficult terrain and an overhead tree canopy that tokens show through. Use when the DM asks to review, edit, duplicate, repair or build a Dungeondraft map, when a map stays stuck loading, when planning a map's layout, size or route choices, or when adding Foundry walls, tree trunks, difficult-terrain regions or a canopy/overhead tile for a map.
---

# Dungeondraft maps

[ddmap.py](ddmap.py) has the format helpers (load, save, validate, preview, terrain weights, objects, clusters, movement costs). For a forest road chase, run [forest_chase.py](forest_chase.py) (see "Quick recipes" at the end). For anything else, write a short generator script in the session workspace that imports `ddmap`. Python 3 plus Pillow; `foundry_scene.py` also needs `shapely` (numpy comes with it).

```powershell
python .github/skills/dungeondraft-maps/ddmap.py info     "<map>"
python .github/skills/dungeondraft-maps/ddmap.py validate "<map>"
python .github/skills/dungeondraft-maps/ddmap.py preview  "<map>" out.png
python .github/skills/dungeondraft-maps/ddmap.py fix-arrays "<map>" "<new map>"
```

## Ground rules

- The DM's maps live in `E:\Users\João Magalhães (HDD)\Documents\DnD\Dungeondraft\`, outside the repository. Never commit them (they are several MB).
- **Never overwrite a map.** Write a new, descriptively named copy (`ddmap.save_new` refuses to overwrite). Name the base file you started from. The DM deletes old variants, so check what exists before referring to one.
- Python on Windows: the path has non-ASCII characters. Pass it as a script argument or import it from a `.py` file. Piping a script to `python -` that contains the path, or `open()`-ing a literal path, can fail with `Errno 22`.
- Reuse only asset paths already in the map (or in a DM map) by deep-copying an existing object. The asset pack manifest disallows third-party reading, so do not inspect `.dungeondraft_pack` files.
- You cannot see a native render. The preview is schematic: terrain blend plus estimated circles for crowns. Say so, and ask the DM to open the file and confirm it loads and looks right.
- Prefer the DM's exported image or `.dd2vtt` for review of hand-made art; read the `.dungeondraft_map` JSON for exact positions, terrain and counts.

## File format (format 3, build 1.2.0.1)

- JSON with Godot value strings: `"Vector2( x, y )"`, `"PoolByteArray( ... )"`, `"PoolIntArray( ... )"`.
- `world.width/height` in squares; **256 map units per square**. Foundry exports default to 70 px per square here.
- `world.levels["0"]` holds `terrain`, `objects`, `cave`, `tiles`, `walls`, `paths`, `portals`, `lights`, `water`, etc.
- **Terrain:** `texture_1..8` name the slots (`ddmap.terrain_slots`). `splat` holds weights for slots 1-4 and `splat2` for 5-8, RGBA bytes, 4 samples per square edge: each is `width*4 * height*4 * 4` bytes. Native files sum the 8 weights to 252-255; use `encode_weights` for 255. Feather edges over about 0.3-0.5 squares to avoid hard lines.
- **Cave masks must match the size even when empty:** `bitmap` and `entrance_bitmap` are `((width*4+3)*(height*4+3)+7)//8` bytes. A wrong size makes Dungeondraft load forever. `tiles.cells` and `tiles.colors` need `width*height` entries (`-1` / `ffffffff` when empty). After resizing, run `fix-arrays` (only for empty caves/tiles).
- **Objects:** `position` (map units), `rotation` (radians), `scale`, `mirror`, `texture`, `layer`, `shadow`, `node_id` (hex). New objects need unique IDs, and `world.next_node_id` must exceed all of them (`ddmap.add_object` handles this).
- Estimated crown radius in squares: about `scale * 1.35` for trees and `scale * 0.85` for shrubs. "Massive" trees look large at about `0.65x` scale. These are estimates for spacing checks, not the art's exact size.
- Dungeondraft does not export walls or lights here unless they are drawn. Foundry vision blockers and difficult terrain are added in Foundry afterwards.

## Procedure

1. Run `info` and `validate` on the source. Note size, terrain slots, objects and empty layers.
2. Agree the layout in words with the DM if it is not given: direction of travel, what is on and off the map, and what each route choice is for.
3. Write a generator script in the session `files/` folder: load the source, change only what is needed, then assert that other fields are unchanged, IDs are unique, and the route clearances and gaps you promised hold.
4. `save_new`, then `validate`, then `preview`. Look at the preview yourself before reporting. Fix sparse or crowded areas, blocked routes and straight lines.
5. Report the new file, the base it came from, what changed, measured route savings and what still needs native confirmation. Keep a working version the DM confirmed as the next base.

## Map design lessons (DM preferences)

- **Natural, not geometric.** Curves, not angles. Use sums of sines for roads and borders, smooth feathered terrain, random rotation, mirroring and scale. Roads should loosely follow the real direction of travel (for example, about 30° off vertical, north-east to south-west).
- **Every obstacle must be in the way, and every off-road route needs a mechanical reason**: a shortcut that saves real movement, a bypass around mud, cover or a hiding line. Measure it with `route_cost` (5 ft squares, diagonals 5 ft, difficult terrain counts double) and report the feet saved. A route should save at least about 30 ft (one move), and preferably a Dash or more.
- **Shortcut trails must rejoin the road** (road to road across a bend), not lead off sideways into the forest. Under 5 ft diagonals, only bends that reverse direction save distance.
- **Mud sits where traffic churns it**: wheel ruts in the middle of the road, with the shoulders kept passable as a slower bypass. Treat it as difficult terrain.
- **Forest density:** dense, larger and overlapping trees at the map edges suggest deep forest. Avoid barren open stretches beside the road. Group trees in clusters, not evenly spread singles.
- **The layout the DM approved** (`forest_chase_road_mesh`): elongated clusters of 8-12 trees and shrubs, aligned with the road (`ddmap.place_cluster`). They form staggered rows parallel to it, offset sideways by about 11-square steps, with clusters about 12-14 squares apart along each row. Every new cluster keeps **at least one clear 5 ft square** from every other cluster (`gap=1.0`), giving parallel lanes and cross lanes. The outermost row merges into the dense edge forest (`merge_groups`). Lone scattered trees between rows were removed because they block the gaps.
- Rejected variants: very high object counts (about 2,400) and solid edge infill felt too much, and trails that only ran sideways out of the map were useless. Gravel-painted trails are optional; gaps between tree clusters can read as paths on their own.
- Preserve the road clearance, shortcut clearance and mud shoulders whenever you add vegetation.

## Chase maps (DMG 2014 chase rules)

- Size the map from movement. Eliza (spy, 30 ft, Cunning Action Dash) covers 60-90 ft per turn. A chase of about 8-10 rounds needs about 800 ft of route, for example 160 squares. A wide map such as 120 × 160 leaves room for flanking and loops.
- Reaching the map edge is not automatically an escape. Escape uses the DMG Stealth check against the pursuers' passive Perception, while out of sight.
- A mapped obstacle or shortcut should give a choice (risk versus speed). Do not add mandatory fixed checks on top of the random complications table. That table lives at `assets/rollable_tables/fvtt-RollTable-eliza-chase-complications.json` (see `foundry-rolltable`).
- For rules details, use `dnd-rules` (DMG "Chases", PHB Dash and difficult terrain).

## Foundry walls and difficult terrain

[foundry_scene.py](foundry_scene.py) turns a map into an importable Foundry v14 scene (dnd5e), using the same grid as the image the DM exports from Dungeondraft. It needs `shapely` (`pip install shapely`).

```powershell
python .github/skills/dungeondraft-maps/foundry_scene.py "<map>" assets/scenes/<base scene>.json assets/scenes/fvtt-Scene-<name>.json --ppi 70 --name "<Scene name>" --background "worlds/curse-of-strahd/assets/maps/<image>.webp" --preview <session files>/check.png --preview-image "<local copy of the exported image>"
```

- **The base scene is a Foundry export with one sample wall and one region with the dnd5e difficult-terrain behavior** (currently `assets/scenes/fvtt-Scene-scene-NYNlrBcYUXgqaUzp.json`). Copy their schema instead of guessing it; v14 added `levels` to walls and regions. Region polygons are `{"type": "polygon", "points": [x0, y0, x1, y1, ...], "hole": false, "origin": null}`: flat pixel pairs, the ring not closed by repeating the first point, `hole: true` subtracting from the region.
- **What the DM chose:**
  - Trees become **trunk walls**: an octagon of radius `clamp(0.25 × crown, 0.35, 0.65)` squares, about one 5 ft square across for a typical tree (`--trunk-scale` adjusts it). The first version, at 0.18-0.35 squares, was too small. Trunks block movement, sight and light but not sound. Tokens still pass under canopy rims and between trunks, and players can break line of sight in the woods. Shrubs get no wall.
  - **Difficult terrain follows the shape of the trees**: the union of canopy circles, smoothed into polygons (`plants`). The painted swamp is traced into polygons the same way (`mud`). `CANOPY_FACTOR` 1.2 × the `ddmap` crown estimate was checked against the exported image: it covers the dark outer rim of the drawn canopy while keeping the lanes between clusters open.
  - Canopy near the border, connected to it, becomes one smoothed **solid edge band**: walls on its inner boundary, with unreachable pockets filled. Check that tokens can reach the border only through the road exits.
- **Wall budget:** shapely's `buffer(r, quad_segs=n)` makes 4n sides, so use `quad_segs=2` for an octagon. The default gave 21,000 walls instead of about 5,500.
- **Coordinates:** canvas pixel = `ceil(map_px × padding / grid) × grid + square × ppi`. With padding 0.25, a 120 × 160 map at 70 ppi is offset by 2100/2800 px.
- **Regions:** `visibility` 0 (shown on the region layer only, so the art stays clean), and wall `restriction` disabled, because thousands of trunk walls would carve up the shapes.
- **Check against the art:** the DM's world is in `%LOCALAPPDATA%\FoundryVTT\Data\worlds\curse-of-strahd`. Exported maps are in `assets\maps`. Draw the result over that image (`--preview-image`) and view a close-up before delivering.
- **Import:** the DM creates a scene (or reuses one) and uses **Import Data** with the JSON. `--background` sets the level image, which is the Dungeondraft export at the same pixels per square with no extra padding. Trunk positions assume each tree image is centred on its trunk.

## Overhead canopy (tokens under the trees)

Foundry cannot tint or mask a token. Instead, split the art: the background holds only the ground, and a full-scene **overhead tile** holds only trees and shrubs above the tokens. The tile has elevation 10 and Radial occlusion (`occlusion.modes [4]`), so the foliage thins (to `--canopy-alpha`, default 0.35) in a circle around a token underneath it. It is locked, lets light through and blocks weather. Its `alphaThreshold` of 0.75 means tokens on the open road do not trigger it. Change the leaf opacity in Foundry under the tile's Overhead tab. **In v14, a tile's `x, y` is its texture anchor point, not its corner.** With the default anchor of 0.5, store the centre (`offset + size / 2`). Storing the corner centres the tile on the background's top-left corner, so it looks smaller and shifted up-left.
- **Hover-fade:** Foundry also fades any Fade/Radial tile entirely while the mouse is over it, for players too, which would reveal everything under the canopy. Nothing in the tile settings turns this off. The DM's own Foundry module `local-scripts` (`%LOCALAPPDATA%\FoundryVTT\Data\modules\local-scripts\scripts\canopy.mjs`) changes this for tiles flagged `flags["local-scripts"].noHoverFade` (which `foundry_scene.py` writes) or named "Canopy". The module must be enabled in the world.
  - For everyone, a radial hole of `MOUSE_RADIUS_SQUARES` (1.5) follows the mouse. It patches `CanvasOcclusionMask#_updateOcclusionMask` to draw one more circle (`0xFF01FF`: green 1/255 = radial occlusion below every elevation) and refreshes the mask on mouse move.
  - The GM holding **Shift** gets Foundry's whole-tile hover-fade back. Otherwise `mesh.hoverFade` is forced to false on `refreshTile`.
  - Check its syntax with Foundry's Electron: `$env:ELECTRON_RUN_AS_NODE=1; & "C:\Program Files\Foundry Virtual Tabletop\Foundry Virtual Tabletop.exe" --check <file>.mjs`.

1. `ddmap.py strip-canopy "<map>" "<map>_ground.dungeondraft_map"` copies the map without trees and shrubs. Canopy is recognised by texture folder (`/trees/`, `/more_trees/`, `/shrubs/`; `ddmap.is_canopy`), not by layer: Dungeondraft put every object on layer 100.
2. Export both maps from Dungeondraft with **identical settings**. Current settings: Export → WEBP, quality 100, Grid on, Lighting on, Grid PPI 70 (8400 × 11200 for 120 × 160). Save them to the world's `assets\maps` as `<name>-full.webp` and `<name>-ground.webp`. Each takes 1-2 minutes; wait until the file size stops growing.
3. `canopy_tile.py "<full>" "<ground>" "<name>-canopy.webp"` diffs the two exports. The diff includes foliage, trunks and their shadows, binarises the mask so crowns are fully opaque, and fills enclosed holes up to `--max-hole` squares (foliage close to grass colour diffs as ground). Only the outline is feathered. The default output is at half scale (4200 × 5600) and takes about 15 s. Check it composited over magenta: crowns should be solid, and the road and lanes empty.
4. `foundry_scene.py ... --background worlds/.../<name>-ground.webp --canopy-tile worlds/.../<name>-canopy.webp` builds the scene. Pass the **full** export to `--preview-image`.

## Example scripts

Do not rewrite these pipelines from scratch. Run the scripts and change only parameters.

- [forest_chase.py](forest_chase.py) generates a complete forest road chase map: the approved `forest_chase_road_mesh` layout.
  - Layout: a curved road about 30° off vertical, wheel ruts, road-to-road shortcut trails, rut mud, a dense edge band, flank clusters and a road-aligned cluster mesh with 5 ft lanes.
  - The template map supplies the terrain textures and the tree/shrub assets. Its own objects are replaced.
  - Change the layout with a JSON `--config` that overrides any key from `--print-config`: size, road curve, shortcut rows, mud rows, clearances, edge band, cluster rows and spacing.
  - It prints object counts and the feet each shortcut saves (warning below 30 ft), validates the map, and refuses to overwrite.
  - About one minute for 120 × 160. A different `--seed` gives a fresh variant of the same design.
- `ddmap.place_cluster` adds clusters to an existing map. For a one-off density pass, write a short session script: `placed_from(data)` → `place_cluster(...)` → `save_new`.

## Quick recipes

| Request | Command |
|---|---|
| New forest chase map | `python .github/skills/dungeondraft-maps/forest_chase.py "<template map>" "<new map>" --preview <session files>/check.png [--seed N] [--config cfg.json]` |
| See configurable values | `python .github/skills/dungeondraft-maps/forest_chase.py --print-config` |
| Inspect, check or repair a map | `ddmap.py info`, `ddmap.py validate`, `ddmap.py fix-arrays` (map stuck loading after a resize) |
| Schematic look at a map | `ddmap.py preview "<map>" out.png` |
| Foundry scene with trunk walls and difficult terrain | `foundry_scene.py` (command above) |
| Check walls against the art | `foundry_scene.py ... --preview-image "<exported image>" --closeup X0,Y0,X1,Y1 closeup.png` (window in squares, 24 px per square) |
| Tokens visible under the trees | `ddmap.py strip-canopy` → two exports → `canopy_tile.py` → `foundry_scene.py --canopy-tile` (see "Overhead canopy") |

`foundry_scene.py` stats include `border_exits`: the walkable squares on each border, which should be only the road ends. They also include `cut_off_sq`, the walkable squares sealed off from the main area. If an exit shows up away from a road, the edge band leaks; if many squares are cut off, trunks seal off pockets.

Viewing images on Windows: save previews to the session `files\` folder using a path built from `$env:USERPROFILE`, and use a new file name for each check, because the image viewer can show a cached older version.
