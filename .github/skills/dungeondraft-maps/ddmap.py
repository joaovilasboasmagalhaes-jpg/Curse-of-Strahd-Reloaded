"""Helpers for editing Dungeondraft .dungeondraft_map files (format 3, Dungeondraft 1.2).

Library use (from a generator script):  sys.path.insert(0, <skill dir>); import ddmap
Command line:
    python ddmap.py info MAP
    python ddmap.py validate MAP
    python ddmap.py preview MAP OUT.png [--scale 8]
    python ddmap.py fix-arrays SOURCE DESTINATION
    python ddmap.py strip-canopy SOURCE DESTINATION   # copy without trees/shrubs (ground export)
"""
import argparse
import copy
import json
import math
from pathlib import Path
import re
import sys

GRID = 256  # map units per grid square
SAMPLES = 4  # terrain / cave samples per square edge
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
# Approximate crown radius, in squares per unit of scale, for previews and clearance checks.
CROWN = {"/shrubs/": 0.85}
DEFAULT_CROWN = 1.35
PREVIEW_COLORS = {
    "moss": (63, 81, 55), "dirt": (111, 87, 62), "swamp": (46, 50, 39), "gravel": (130, 120, 99),
    "grass": (81, 97, 59), "sandstone": (141, 122, 88), "rocky": (96, 93, 79),
}


# ---------- load / save ----------

def load(path):
    return json.loads(Path(path).read_bytes().decode("utf-8-sig"))


def save_new(data, path):
    """Write a new map; never overwrites (Dungeondraft maps are the DM's work)."""
    path = Path(path)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=4)
        handle.write("\n")
    assert load(path) == data
    return path


def level(data, index="0"):
    return data["world"]["levels"][index]


# ---------- value encoding ----------

def numbers(value):
    """Numbers inside 'Vector2( x, y )' / 'PoolByteArray( ... )' / 'PoolIntArray( ... )'."""
    return [float(n) for n in _NUMBER.findall(value[value.index("(") + 1:])]


def vector(x, y):
    return f"Vector2( {x:.4f}, {y:.4f} )"


def pool_bytes(values):
    return "PoolByteArray( " + ", ".join(map(str, values)) + " )"


def pool_ints(values):
    return "PoolIntArray( " + ", ".join(map(str, values)) + " )"


def to_squares(position):
    x, y = numbers(position)
    return x / GRID, y / GRID


def crown_radius(obj):
    scale = max(map(abs, numbers(obj["scale"])))
    factor = next((v for key, v in CROWN.items() if key in obj["texture"]), DEFAULT_CROWN)
    return scale * factor


# ---------- array sizes (wrong sizes make Dungeondraft hang on load) ----------

def terrain_bytes(width, height):
    return width * SAMPLES * height * SAMPLES * 4


def cave_bytes(width, height):
    # Padded quarter-square bit grid, required even when no cave is painted.
    return ((width * SAMPLES + 3) * (height * SAMPLES + 3) + 7) // 8


def resize_empty_arrays(data):
    """Resize tiles and cave masks after changing world width/height. Cave/tiles must be empty."""
    width, height = data["world"]["width"], data["world"]["height"]
    for lvl in data["world"]["levels"].values():
        for key in ("bitmap", "entrance_bitmap"):
            assert set(numbers(lvl["cave"][key])) <= {0}, "cave is painted; resize it in Dungeondraft"
            lvl["cave"][key] = pool_bytes([0] * cave_bytes(width, height))
        assert set(numbers(lvl["tiles"]["cells"])) <= {-1}, "tiles are painted; resize in Dungeondraft"
        lvl["tiles"]["cells"] = pool_ints([-1] * (width * height))
        lvl["tiles"]["colors"] = ["ffffffff"] * (width * height)


# ---------- terrain ----------

def terrain_slots(lvl):
    """{slot number: texture name} for texture_1 .. texture_8."""
    return {i: Path(lvl["terrain"][f"texture_{i}"]).stem.replace("terrain_", "")
            for i in range(1, 9) if f"texture_{i}" in lvl["terrain"]}


def read_terrain(lvl):
    """List of 8-weight tuples, row-major over (width*4) x (height*4) samples."""
    a = bytes(int(n) for n in numbers(lvl["terrain"]["splat"]))
    b = bytes(int(n) for n in numbers(lvl["terrain"]["splat2"]))
    return [tuple(a[i:i + 4]) + tuple(b[i:i + 4]) for i in range(0, len(a), 4)]


def encode_weights(weights):
    """Normalise 8 floats to integers summing to 255 (largest-remainder rounding)."""
    total = sum(max(w, 0) for w in weights) or 1
    raw = [max(w, 0) * 255 / total for w in weights]
    out = [int(r) for r in raw]
    for i in sorted(range(8), key=lambda i: raw[i] - out[i], reverse=True)[:255 - sum(out)]:
        out[i] += 1
    return out


def write_terrain(lvl, samples):
    """samples: iterable of 8 weights per sample (floats are normalised), row-major."""
    a, b = bytearray(), bytearray()
    for weights in samples:
        exact = all(isinstance(v, int) for v in weights) and sum(weights) == 255
        w = list(weights) if exact else encode_weights(weights)
        a += bytes(w[:4])
        b += bytes(w[4:])
    lvl["terrain"]["splat"], lvl["terrain"]["splat2"] = pool_bytes(a), pool_bytes(b)


# ---------- objects ----------

def next_id(data):
    objects = [o for lvl in data["world"]["levels"].values() for o in lvl["objects"]]
    used = max((int(o["node_id"], 16) for o in objects), default=-1)
    return max(int(data["world"]["next_node_id"], 16), used + 1)


def add_object(data, template, x, y, scale, rotation, lvl="0", mirror=None):
    """Copy an object already in the map (reuse only asset paths the map already has)."""
    ident = next_id(data)
    obj = copy.deepcopy(template)
    obj["node_id"] = format(ident, "x")
    obj["position"] = vector(x * GRID, y * GRID)
    obj["scale"] = vector(scale, scale)
    obj["rotation"] = rotation
    if mirror is not None:
        obj["mirror"] = mirror
    data["world"]["levels"][lvl]["objects"].append(obj)
    data["world"]["next_node_id"] = format(ident + 1, "x")
    return obj


CANOPY_FOLDERS = ("/trees/", "/more_trees/", "/shrubs/")  # drawn above tokens in Foundry


def is_canopy(obj):
    return any(folder in obj["texture"] for folder in CANOPY_FOLDERS)


def is_tree(obj):
    return is_canopy(obj) and "/shrubs/" not in obj["texture"]


def strip_canopy(data):
    """Remove trees and shrubs from every level (for the ground-only export); returns the count."""
    removed = 0
    for lvl in data["world"]["levels"].values():
        kept = [o for o in lvl["objects"] if not is_canopy(o)]
        removed += len(lvl["objects"]) - len(kept)
        lvl["objects"] = kept
    return removed


def placed_from(data, lvl="0", group=-1):
    """[(x, y, crown_radius, group)] for objects already in a level."""
    return [(*to_squares(o["position"]), crown_radius(o), group) for o in data["world"]["levels"][lvl]["objects"]]


def place_cluster(data, rng, placed, group, centre, tangent, count, trees, shrubs,
                  blocked=lambda x, y, r: False, gap=1.0, spread=(2.7, 1.3), scales=(1.25, 1.95),
                  merge_groups=(), lvl="0"):
    """Grow one elongated tree cluster; returns objects added.

    placed: shared list from placed_from(); each entry carries a group id. Members of the same
    group may overlap by half; any other group must stay `gap` squares away crown-to-crown
    (gap=1.0 leaves a walkable 5 ft lane), except groups in merge_groups (e.g. edge forest).
    tangent: unit (tx, ty) along which the cluster is stretched (usually the road direction).
    blocked(x, y, r): True where a crown of radius r would intrude on a road, trail or mud shoulder.
    """
    width, height = data["world"]["width"], data["world"]["height"]
    (cx, cy), (tx, ty) = centre, tangent
    added = []
    for member in range(count):
        bush = member % 4 == 0 and shrubs
        template = rng.choice(shrubs if bush else trees)
        scale = rng.uniform(0.9, 1.4) if bush else rng.uniform(*scales)
        if "massive" in template["texture"]:
            scale *= 0.65
        r = scale * (CROWN["/shrubs/"] if bush else DEFAULT_CROWN)
        for _ in range(500):
            along, across = rng.gauss(0, spread[0]), rng.gauss(0, spread[1])
            x, y = cx + along * tx + across * ty, cy + along * ty - across * tx
            if not (0.5 < x < width - 0.5 and 0.5 < y < height - 0.5) or blocked(x, y, r):
                continue
            if all(math.hypot(x - ox, y - oy) >= ((r + orr) * 0.5 if og == group or og in merge_groups
                                                  else r + orr + gap)
                   for ox, oy, orr, og in placed):
                break
        else:
            break
        added.append(add_object(data, template, x, y, scale, rng.uniform(-math.pi, math.pi), lvl,
                                mirror=rng.random() < 0.5))
        placed.append((x, y, r, group))
    return added


# ---------- validation ----------

def validate(data):
    """Return (errors, warnings). Errors are known to break loading or editing."""
    errors, warnings = [], []
    world = data["world"]
    width, height = world["width"], world["height"]
    ids = []
    for name, lvl in world["levels"].items():
        splats = [numbers(lvl["terrain"][key]) for key in ("splat", "splat2")]
        for key, values in zip(("splat", "splat2"), splats):
            if len(values) != terrain_bytes(width, height):
                errors.append(f"level {name} terrain {key}: {len(values)} bytes, "
                              f"expected {terrain_bytes(width, height)}")
        a, b = splats
        sums = [sum(a[i:i + 4]) + sum(b[i:i + 4]) for i in range(0, min(len(a), len(b)), 4)]
        # Native maps store sums of 252-255; anything else means the weights were miscomputed.
        odd = sum(1 for total in sums if not 250 <= total <= 255)
        if odd:
            errors.append(f"level {name}: {odd} terrain samples whose 8 weights are not about 255")
        for key in ("bitmap", "entrance_bitmap"):
            n = len(numbers(lvl["cave"][key]))
            if n != cave_bytes(width, height):
                errors.append(f"level {name} cave {key}: {n} bytes, expected "
                              f"{cave_bytes(width, height)} (causes a permanent loading screen)")
        cells = len(numbers(lvl["tiles"]["cells"]))
        if cells != width * height or len(lvl["tiles"]["colors"]) != width * height:
            errors.append(f"level {name} tiles: {cells} cells / {len(lvl['tiles']['colors'])} colors, "
                          f"expected {width * height}")
        outside = 0
        for obj in lvl["objects"]:
            ids.append(int(obj["node_id"], 16))
            x, y = to_squares(obj["position"])
            outside += not (-2 <= x <= width + 2 and -2 <= y <= height + 2)
        if outside:
            warnings.append(f"level {name}: {outside} objects more than 2 squares outside the map")
    if len(ids) != len(set(ids)):
        errors.append("duplicate object node_id values")
    if ids and int(world["next_node_id"], 16) <= max(ids):
        errors.append("world.next_node_id must be greater than every node_id")
    return errors, warnings


# ---------- preview ----------

def preview(data, out, scale=8, lvl="0", marks=()):
    """Schematic top-down PNG: blended terrain plus estimated crowns. Not a native render."""
    from PIL import Image, ImageDraw

    level_data = data["world"]["levels"][lvl]
    width, height = data["world"]["width"], data["world"]["height"]
    slots = terrain_slots(level_data)
    palette = [PREVIEW_COLORS.get(slots.get(i, ""), (90, 90, 90)) for i in range(1, 9)]
    pixels = [tuple(round(sum(w[i] * palette[i][c] for i in range(8)) / 255) for c in range(3))
              for w in read_terrain(level_data)]
    image = Image.new("RGB", (width * SAMPLES, height * SAMPLES))
    image.putdata(pixels)
    image = image.resize((width * scale, height * scale))
    draw = ImageDraw.Draw(image)
    for obj in level_data["objects"]:
        x, y = to_squares(obj["position"])
        r = crown_radius(obj)
        color = (79, 66, 49) if "dead_tree" in obj["texture"] else (43, 64, 43)
        draw.ellipse(((x - r) * scale, (y - r) * scale, (x + r) * scale, (y + r) * scale),
                     fill=color, outline=(23, 35, 25))
    for x, y in marks:
        draw.ellipse((x * scale - 5, y * scale - 5, x * scale + 5, y * scale + 5), outline=(230, 40, 40), width=2)
    image.save(out)
    return out


# ---------- movement check ----------

def route_cost(start, end, passable, difficult=lambda x, y: False, bounds=None):
    """Grid movement cost in feet (5 ft squares, diagonals 5 ft, difficult terrain x2).

    passable(gx, gy) / difficult(gx, gy) take square indices. Raises if disconnected.
    """
    import heapq

    queue, best = [(0, start)], {start: 0}
    while queue:
        cost, point = heapq.heappop(queue)
        if point == end:
            return cost
        if cost != best[point]:
            continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (point[0] + dx, point[1] + dy)
                if n == point or (bounds and not bounds(*n)) or not passable(*n):
                    continue
                updated = cost + (10 if difficult(*n) else 5)
                if updated < best.get(n, math.inf):
                    best[n] = updated
                    heapq.heappush(queue, (updated, n))
    raise ValueError("Disconnected route")


# ---------- CLI ----------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("info", "validate"):
        sub.add_parser(name).add_argument("map")
    p = sub.add_parser("preview")
    p.add_argument("map")
    p.add_argument("out")
    p.add_argument("--scale", type=int, default=8)
    for name in ("fix-arrays", "strip-canopy"):
        p = sub.add_parser(name)
        p.add_argument("source")
        p.add_argument("destination")
    args = parser.parse_args(argv)

    if args.command in ("fix-arrays", "strip-canopy"):
        data = load(args.source)
        if args.command == "fix-arrays":
            resize_empty_arrays(data)
        else:
            print(f"Removed {strip_canopy(data)} trees/shrubs")
        save_new(data, args.destination)
        print(f"Wrote {args.destination}")
        return 0
    data = load(args.map)
    if args.command == "info":
        from collections import Counter

        world, lvl = data["world"], level(data)
        print(f"{world['width']} x {world['height']} squares; build {data['header']['creation_build']}")
        print("Terrain slots:", terrain_slots(lvl))
        print("Objects:", len(lvl["objects"]))
        for texture, count in Counter(o["texture"] for o in lvl["objects"]).most_common():
            print(f"  {count:5}  {texture}")
        print("Non-empty layers:", [k for k in ("walls", "paths", "portals", "lights", "patterns", "texts")
                                    if lvl[k]])
        return 0
    if args.command == "validate":
        errors, warnings = validate(data)
        for line in errors:
            print("ERROR:", line)
        for line in warnings:
            print("WARNING:", line)
        if not errors:
            print("OK: array sizes, terrain weights and node IDs.")
        return 1 if errors else 0
    preview(data, args.out, args.scale)
    print(f"Wrote {args.out} (schematic, not a native render)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
