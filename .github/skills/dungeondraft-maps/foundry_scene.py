"""Build an importable Foundry VTT v14 scene (walls + difficult terrain) from a Dungeondraft map.

    python foundry_scene.py MAP.dungeondraft_map BASE_SCENE.json OUT.json --ppi 70 [--name NAME]
        [--background FOUNDRY_PATH] [--canopy-tile FOUNDRY_PATH] [--canopy-alpha 0.35]
        [--trunk-scale 1.0] [--preview PNG] [--preview-image EXPORT] [--closeup X0,Y0,X1,Y1 PNG]

BASE_SCENE.json is a scene exported from the DM's world containing at least one wall and one region
with a dnd5e difficult-terrain behavior; their schema is reused so the output matches the world's
Foundry/dnd5e version. The scene image must be the Dungeondraft export at the same --ppi.
Needs shapely (pip install shapely).

Produces:
* trunk walls: a round wall per tree, about one 5 ft square across for a typical tree (blocks
  movement, sight and light, not sound); overlapping trunks are merged, canopy rims stay walkable;
* edge band: canopy-covered squares near the border, connected to it, walled off as one smoothed mass;
* regions: smoothed canopy outline -> difficult terrain "plants"; painted swamp -> "mud".
"""
import argparse
import copy
import json
import math
import random
import string
import sys
from collections import deque
from pathlib import Path

from shapely.geometry import MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).parent))
import ddmap  # noqa: E402

_ID_CHARS = string.ascii_letters + string.digits
CANOPY_FACTOR = 1.2  # checked against an exported image: covers the dark outer rim of the drawn canopy


def new_id(rng):
    return "".join(rng.choice(_ID_CHARS) for _ in range(16))


def canopy_coverage(data, lvl="0", sub=4):
    """Fraction of each square under any estimated crown, as cov[gy][gx]."""
    width, height = data["world"]["width"], data["world"]["height"]
    hits = [[0] * width for _ in range(height)]
    for obj in ddmap.level(data, lvl)["objects"]:
        x, y = ddmap.to_squares(obj["position"])
        r = ddmap.crown_radius(obj)
        for gy in range(max(0, int(y - r)), min(height, int(y + r) + 1)):
            for gx in range(max(0, int(x - r)), min(width, int(x + r) + 1)):
                for sy in range(sub):
                    for sx in range(sub):
                        bit = 1 << (sy * sub + sx)
                        if not hits[gy][gx] & bit and math.hypot(gx + (sx + .5) / sub - x, gy + (sy + .5) / sub - y) <= r:
                            hits[gy][gx] |= bit
    return [[bin(v).count("1") / sub ** 2 for v in row] for row in hits]


def edge_mass(cov, margin=(12, 7), threshold=0.6):
    """Squares near the border (within margin=(sides, top/bottom)) under canopy and connected to it,
    plus band pockets the play area cannot reach."""
    height, width = len(cov), len(cov[0])
    neighbours = lambda gx, gy: ((nx, ny) for nx, ny in ((gx + 1, gy), (gx - 1, gy), (gx, gy + 1), (gx, gy - 1))  # noqa: E731
                                 if 0 <= nx < width and 0 <= ny < height)

    def eligible(gx, gy):
        near = min(gx, width - 1 - gx) < margin[0] or min(gy, height - 1 - gy) < margin[1]
        return near and cov[gy][gx] >= threshold

    mass = [[False] * width for _ in range(height)]
    queue = deque((gx, gy) for gy in range(height) for gx in range(width)
                  if (gx in (0, width - 1) or gy in (0, height - 1)) and eligible(gx, gy))
    for gx, gy in queue:
        mass[gy][gx] = True
    while queue:
        for nx, ny in neighbours(*queue.popleft()):
            if not mass[ny][nx] and eligible(nx, ny):
                mass[ny][nx] = True
                queue.append((nx, ny))
    inner = lambda gx, gy: margin[0] <= gx < width - margin[0] and margin[1] <= gy < height - margin[1]  # noqa: E731
    reach = {(gx, gy) for gy in range(height) for gx in range(width) if inner(gx, gy) and not mass[gy][gx]}
    queue = deque(reach)
    while queue:
        for nx, ny in neighbours(*queue.popleft()):
            if (nx, ny) not in reach and not mass[ny][nx]:
                reach.add((nx, ny))
                queue.append((nx, ny))
    for gy in range(height):
        for gx in range(width):
            if (gx, gy) not in reach:
                mass[gy][gx] = True
    return mass


def mask_geometry(mask, cell=1.0):
    """Union of the True cells of a 2D mask (cell size in squares), built from row runs."""
    boxes = []
    for gy, row in enumerate(mask):
        gx = 0
        while gx < len(row):
            if row[gx]:
                start = gx
                while gx < len(row) and row[gx]:
                    gx += 1
                boxes.append(box(start * cell, gy * cell, gx * cell, (gy + 1) * cell))
            gx += 1
    return unary_union(boxes)


def smooth(geom, radius=0.5, tolerance=0.15):
    """Round off grid steps (closing then opening) and drop needless vertices."""
    return geom.buffer(radius, quad_segs=3).buffer(-2 * radius, quad_segs=3).buffer(radius, quad_segs=3) \
        .simplify(tolerance)


def terrain_mask(data, name, threshold=0.5, lvl="0"):
    """Quarter-square samples where the named terrain texture dominates."""
    width = data["world"]["width"] * ddmap.SAMPLES
    level = ddmap.level(data, lvl)
    slots = [i - 1 for i, n in ddmap.terrain_slots(level).items() if n == name]
    flags = [sum(w[k] for k in slots) >= threshold * 255 for w in ddmap.read_terrain(level)]
    return [flags[i:i + width] for i in range(0, len(flags), width)]


def polygons(geom):
    if geom.is_empty:
        return []
    return list(geom.geoms) if isinstance(geom, MultiPolygon) else [p for p in getattr(geom, "geoms", [geom])
                                                                    if isinstance(p, Polygon)]


def trunk_radius(crown, scale=1.0):
    """About one 5 ft square across for a typical tree (crown 2 squares)."""
    return min(0.65, max(0.35, crown * 0.25)) * scale


def build(data, base, ppi, name, background=None, trunk_scale=1.0, seed=1, canopy=None, canopy_alpha=0.35):
    rng = random.Random(seed)
    width, height = data["world"]["width"], data["world"]["height"]
    pad = base.get("padding", 0)
    off_x = math.ceil(width * ppi * pad / ppi) * ppi
    off_y = math.ceil(height * ppi * pad / ppi) * ppi
    px = lambda sx, sy: [round(off_x + sx * ppi, 1), round(off_y + sy * ppi, 1)]  # noqa: E731

    wall_template = base["walls"][0]
    region_template = next(r for r in base["regions"] if r.get("behaviors"))
    level_ids = wall_template.get("levels", [])
    bounds = box(0, 0, width, height)

    band = smooth(mask_geometry(edge_mass(canopy_coverage(data)))).intersection(bounds)
    trees, canopies = [], []
    for obj in ddmap.level(data)["objects"]:
        x, y = ddmap.to_squares(obj["position"])
        crown = ddmap.crown_radius(obj)
        canopies.append(Point(x, y).buffer(crown * CANOPY_FACTOR, quad_segs=4))
        if ddmap.is_tree(obj) and not band.contains(Point(x, y)):
            trees.append(Point(x, y).buffer(trunk_radius(crown, trunk_scale), quad_segs=2))  # octagon
    trunks = unary_union(trees).difference(band)
    blocked = unary_union([band, trunks]).intersection(bounds)

    walls = []

    def on_border(a, b):
        return any(abs(a[i] - v) < 1e-6 and abs(b[i] - v) < 1e-6 for i, v in ((0, 0), (0, width), (1, 0), (1, height)))

    for poly in polygons(blocked):
        for ring in [poly.exterior, *poly.interiors]:
            coords = list(ring.coords)
            for a, b in zip(coords, coords[1:]):
                if not on_border(a, b):
                    w = copy.deepcopy(wall_template)
                    w.update(_id=new_id(rng), c=px(*a) + px(*b), dir=0, door=0, ds=0, flags={},
                             move=20, sight=20, light=20, sound=20 if band.intersects(Point(a)) else 0)
                    walls.append(w)

    mud = smooth(mask_geometry(terrain_mask(data, "swamp"), 1 / ddmap.SAMPLES), 0.25, 0.1)
    mud = mud.difference(band).intersection(bounds)
    plants = smooth(unary_union(canopies)).difference(band).difference(mud).intersection(bounds)

    def region(label, kind, geom, color):
        reg = copy.deepcopy(region_template)
        behavior = reg["behaviors"][0]
        behavior.update(_id=new_id(rng), name="Difficult Terrain", disabled=False)
        behavior["system"]["types"] = [kind]
        reg.update(_id=new_id(rng), name=label, color=color, visibility=0, levels=level_ids, flags={})
        reg["restriction"]["enabled"] = False  # trunk walls would otherwise carve the shapes
        reg["behaviors"] = [behavior]
        reg["shapes"] = []
        for poly in polygons(geom):
            for ring, hole in [(poly.exterior, False)] + [(r, True) for r in poly.interiors]:
                if Polygon(ring).area < 0.25:  # smoothing slivers
                    continue
                points = [v for xy in list(ring.coords)[:-1] for v in px(*xy)]
                reg["shapes"].append({"type": "polygon", "points": points, "hole": hole, "origin": None})
        total_w, total_h = width * ppi + 2 * off_x, height * ppi + 2 * off_y
        reg["_shapeConstraints"] = [[0, 0, total_w, 0, total_w, total_h, 0, total_h]]
        return reg

    regions = [region("Undergrowth", "plants", plants, "#3a6b35"), region("Mud ruts", "mud", mud, "#6b4f2a")]

    scene = copy.deepcopy(base)
    tiles = [canopy_tile(new_id(rng), canopy, width * ppi, height * ppi, off_x, off_y, level_ids, canopy_alpha)] \
        if canopy else []
    scene.update(name=name, width=width * ppi, height=height * ppi, walls=walls, regions=regions,
                 drawings=[], tokens=[], lights=[], notes=[], sounds=[], tiles=tiles)
    scene["grid"]["size"] = ppi
    scene.pop("_id", None)
    for lvl in scene.get("levels", []):
        lvl["background"]["src"] = background
    stats = {"trees": len(trees), "walls": len(walls), "band_walls": sum(1 for w in walls if w["sound"]),
             "trunk_blobs": len(polygons(trunks)),
             "undergrowth_shapes": len(regions[0]["shapes"]), "mud_shapes": len(regions[1]["shapes"]),
             "undergrowth_sq": round(plants.area), "mud_sq": round(mud.area, 1),
             **leak_check(blocked, width, height)}
    return scene, (band, plants, mud, trunks), stats


def canopy_tile(ident, src, width, height, x, y, levels, alpha):
    """Full-scene overhead tile above tokens (elevation 10 > 0) with Radial occlusion
    (CONST.OCCLUSION_MODES.RADIAL = 4): a circle around each revealing token shows the ground,
    with the leaves at `alpha` opacity over it. `x, y` is the top-left corner.

    In v14 a tile's x/y is its texture anchor point, not its corner, so with anchor 0.5 the
    stored position is the tile centre."""
    x, y = x + width // 2, y + height // 2
    return {
        "_id": ident, "name": "Canopy",
        "texture": {"src": src, "anchorX": 0.5, "anchorY": 0.5, "offsetX": 0, "offsetY": 0, "fit": "fill",
                    "scaleX": 1, "scaleY": 1, "rotation": 0, "tint": "#ffffff", "alphaThreshold": 0.75},
        "width": width, "height": height, "x": x, "y": y, "elevation": 10, "levels": levels, "sort": 0,
        "rotation": 0, "alpha": 1, "hidden": False, "locked": True,
        "restrictions": {"light": False, "weather": True},
        "occlusion": {"modes": [4], "alpha": alpha},
        "video": {"loop": True, "autoplay": True, "volume": 0},
        # Read by the DM's local-scripts module (canopy.mjs) to turn off Foundry's whole-tile hover-fade.
        "flags": {"local-scripts": {"noHoverFade": True}},
    }


def leak_check(blocked, width, height):
    """Walkability of square centres (8-way moves). Reports the largest walkable area's exits
    along the map border, as square ranges per side (should be only the road ends), and the
    walkable squares cut off from it (pockets inside the walls)."""
    import numpy as np
    import shapely

    ys, xs = np.mgrid[0:height, 0:width]
    free = ~shapely.contains_xy(blocked, xs.ravel() + 0.5, ys.ravel() + 0.5).reshape(height, width)
    seen = np.zeros_like(free, dtype=int)
    label, sizes = 0, {}
    for sy in range(height):
        for sx in range(width):
            if free[sy, sx] and not seen[sy, sx]:
                label += 1
                seen[sy, sx], queue, size = label, deque([(sx, sy)]), 0
                while queue:
                    x, y = queue.popleft()
                    size += 1
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < width and 0 <= ny < height and free[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = label
                                queue.append((nx, ny))
                sizes[label] = size
    main = max(sizes, key=sizes.get) if sizes else 0

    def runs(cells):
        out, start = [], None
        for i, ok in enumerate(list(cells) + [False]):
            if ok and start is None:
                start = i
            elif not ok and start is not None:
                out.append(f"{start}-{i - 1}")
                start = None
        return out

    main_area = seen == main
    exits = {side: r for side, r in (("top", runs(main_area[0])), ("bottom", runs(main_area[-1])),
                                     ("left", runs(main_area[:, 0])), ("right", runs(main_area[:, -1]))) if r}
    return {"border_exits": exits, "cut_off_sq": int(free.sum() - sizes.get(main, 0))}


def overlay(data, geoms, out, scale=8, image=None, ppi=None, crop=None):
    """Preview: edge band (red), undergrowth (green), mud (brown), trunk walls (black).
    With image/ppi the shapes are drawn over the exported map image (downscaled to `scale` px/square).
    crop=(x0, y0, x1, y1) in squares saves only that window (use a larger scale for close-ups)."""
    from PIL import Image, ImageDraw

    width, height = data["world"]["width"], data["world"]["height"]
    if image:
        Image.MAX_IMAGE_PIXELS = None
        img = Image.open(image).convert("RGBA").resize((width * scale, height * scale))
    else:
        tmp = Path(out).with_suffix(".base.png")
        ddmap.preview(data, tmp, scale=scale)
        img = Image.open(tmp).convert("RGBA")
        tmp.unlink()
    layer = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(layer)
    styles = ((200, 40, 40, 110), (60, 220, 60, 60), (170, 110, 40, 150), (0, 0, 0, 255))
    for geom, fill in zip(geoms, styles):
        for poly in polygons(geom):
            draw.polygon([(x * scale, y * scale) for x, y in poly.exterior.coords], fill=fill,
                         outline=fill[:3] + (255,))
            for ring in poly.interiors:
                draw.polygon([(x * scale, y * scale) for x, y in ring.coords], fill=(0, 0, 0, 0))
    result = Image.alpha_composite(img, layer)
    if crop:
        result = result.crop(tuple(round(v * scale) for v in crop))
    result.save(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("map")
    parser.add_argument("base_scene")
    parser.add_argument("out")
    parser.add_argument("--ppi", type=int, required=True, help="pixels per square used for the image export")
    parser.add_argument("--name")
    parser.add_argument("--background", help="Foundry path of the exported map image (else set it in Foundry); "
                        "with --canopy-tile use the ground-only export")
    parser.add_argument("--canopy-tile", help="Foundry path of the canopy tile from canopy_tile.py")
    parser.add_argument("--canopy-alpha", type=float, default=0.35,
                        help="leaf opacity left over a token under the canopy (0 = fully cut out)")
    parser.add_argument("--trunk-scale", type=float, default=1.0)
    parser.add_argument("--preview")
    parser.add_argument("--preview-image", help="local copy of the exported map image to draw the preview on")
    parser.add_argument("--closeup", nargs=2, metavar=("X0,Y0,X1,Y1", "PNG"),
                        help="also save a 24 px/square close-up of this window (in squares)")
    args = parser.parse_args(argv)

    data = ddmap.load(args.map)
    base = json.loads(Path(args.base_scene).read_text(encoding="utf-8"))
    if not base.get("walls") or not any(r.get("behaviors") for r in base.get("regions", [])):
        sys.exit("Base scene needs one sample wall and one region with a difficult-terrain behavior.")
    scene, geoms, stats = build(data, base, args.ppi, args.name or Path(args.map).stem, args.background,
                                args.trunk_scale, canopy=args.canopy_tile, canopy_alpha=args.canopy_alpha)
    with Path(args.out).open("x", encoding="utf-8") as handle:
        json.dump(scene, handle, indent=2)
    print(json.dumps(stats))
    if args.preview:
        overlay(data, geoms, args.preview, image=args.preview_image, ppi=args.ppi)
    if args.closeup:
        window = [float(v) for v in args.closeup[0].split(",")]
        overlay(data, geoms, args.closeup[1], scale=24, image=args.preview_image, ppi=args.ppi, crop=window)


if __name__ == "__main__":
    main()
