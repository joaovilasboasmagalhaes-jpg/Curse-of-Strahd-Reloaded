"""Generate a forest road chase map (the layout the DM approved as forest_chase_road_mesh).

    python forest_chase.py TEMPLATE_MAP OUT_MAP [--config CONFIG.json] [--seed N] [--preview PNG]
    python forest_chase.py --print-config          # show the defaults to copy into a config

TEMPLATE_MAP supplies terrain textures and tree/shrub objects (only its assets are reused); its
objects are replaced. It needs terrain slots named moss and dirt (swamp, gravel, grass, rocky
are used when present). OUT_MAP must not exist.

Layers, in order (all keep the road, shortcut trails and mud shoulders clear):
1. terrain: curved dirt road at ~30 degrees off vertical, wheel ruts, road-to-road shortcut trails
   across bends, mud in the ruts, mossy forest floor;
2. edge band: large overlapping trees within the side/top-bottom margins (deep forest);
3. singles beside the road;
4. flank clusters: groups along both sides of the road and the shortcut trails;
5. mesh: elongated clusters in staggered rows parallel to the road, each at least `gap` squares
   from any other group (walkable lanes), merging only into the edge band.
Then reports the feet each shortcut saves (5 ft diagonals, mud x2) and validates the map.
"""
import argparse
import copy
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ddmap  # noqa: E402

DEFAULTS = {
    "width": 120, "height": 160, "seed": 73530,
    # road centre x(y) = top_x + (bottom_x - top_x) * y / height
    #                    + amplitude * sin(pi y / height) * sin(2 pi y / wavelength)
    "road": {"top_x": 106, "bottom_x": 14, "amplitude": 20, "wavelength": 70, "half_width": 1.85},
    "shortcuts": [[40, 85], [95, 145]],  # road rows joined by a deer trail across a bend
    "mud_rows": [66, 137],  # rut mud centred on the road at these rows
    "clearance": {"road": 2.05, "trail": 1.0, "mud_rows": 8, "mud_shoulder": 6},
    "edge": {"sides": 12, "top_bottom": 7, "trees": 330, "scale": [1.6, 2.5], "separation": 0.46},
    "singles": {"count": 110, "max_road_distance": 14.5, "scale": [1.0, 1.65], "separation": 0.8},
    "flanks": {"row_step": 8, "offset": [7, 14], "members": [9, 14], "spread": [4.5, 3.2],
               "scale": [1.25, 2.0]},
    "mesh": {"rows": [18, 29, 40, 51, 62, 73, 84], "row_factor": 0.8, "spacing": [12, 14],
             "members": [8, 12], "spread": [2.7, 1.3], "scale": [1.25, 1.95], "gap": 1.0},
}


def smoothstep(v):
    v = max(0.0, min(1.0, v))
    return v * v * (3 - 2 * v)


def merge(base, override):
    out = copy.deepcopy(base)
    for key, value in override.items():
        out[key] = merge(out[key], value) if isinstance(value, dict) and isinstance(out.get(key), dict) else value
    return out


class Layout:
    def __init__(self, cfg):
        self.cfg, self.W, self.H = cfg, cfg["width"], cfg["height"]
        r = cfg["road"]
        self._road = lambda y: (r["top_x"] + (r["bottom_x"] - r["top_x"]) * y / self.H
                                + r["amplitude"] * math.sin(math.pi * y / self.H)
                                * math.sin(2 * math.pi * y / r["wavelength"]))

    def road(self, y):
        return self._road(y)

    def slope(self, y):
        return (self._road(y + 0.01) - self._road(y - 0.01)) / 0.02

    def road_distance(self, x, y):
        return abs(x - self.road(y)) / math.hypot(1, self.slope(y))

    def trail_x(self, y, a, b):
        t = max(0, min(1, (y - a) / (b - a)))
        return self.road(a) * (1 - t) + self.road(b) * t + 1.1 * math.sin(math.pi * t)

    def trail_distance(self, x, y):
        best = math.inf
        for a, b in self.cfg["shortcuts"]:
            if a <= y <= b:
                dx = (self.road(b) - self.road(a)) / (b - a)
                best = min(best, abs(x - self.trail_x(y, a, b)) / math.hypot(1, dx))
            else:
                c = max(a, min(b, y))
                best = min(best, math.hypot(x - self.trail_x(c, a, b), y - c))
        return best

    def mud(self, x, y):
        across = (x - self.road(y)) / 3.4
        edge = 0.08 * math.sin(x * 1.4 + y * 1.6)
        return max((smoothstep((1 + edge - math.hypot(across, (y - cy) / 4.7)) / 0.38)
                    for cy in self.cfg["mud_rows"]), default=0)

    def in_edge(self, x, y):
        e = self.cfg["edge"]
        return min(x, self.W - x) < e["sides"] or min(y, self.H - y) < e["top_bottom"]

    def blocked(self, x, y, r):
        c = self.cfg["clearance"]
        return (self.road_distance(x, y) < r + c["road"] or self.trail_distance(x, y) < r + c["trail"]
                or any(abs(y - my) < c["mud_rows"] and abs(x - self.road(y)) < r + c["mud_shoulder"]
                       for my in self.cfg["mud_rows"]))


def paint_terrain(level, lay):
    names = ddmap.terrain_slots(level)
    index = {}
    for slot, name in sorted(names.items(), reverse=True):  # lowest slot wins for duplicates
        index[name] = slot - 1
    missing = {"moss", "dirt"} - index.keys()
    if missing:
        raise SystemExit(f"Template terrain lacks {missing}; slots are {names}")
    fallback = {"swamp": "dirt", "gravel": "dirt", "grass": "moss", "rocky": "moss"}
    slot = {n: index.get(n, index.get(fallback.get(n, n))) for n in ("moss", "dirt", "swamp", "gravel", "grass", "rocky")}

    def weights(parts):
        w = [0.0] * 8
        for name, value in parts.items():
            w[slot[name]] += value
        return w

    s, hw = ddmap.SAMPLES, lay.cfg["road"]["half_width"]
    samples = []
    for py in range(lay.H * s):
        y = (py + 0.5) / s
        for px in range(lay.W * s):
            x = (px + 0.5) / s
            rd = lay.road_distance(x, y)
            cover = smoothstep((hw + 0.08 * math.sin(y * 2.3) + 0.04 * math.cos(x * 3) - rd) / 0.5)
            trail = smoothstep((0.85 - lay.trail_distance(x, y)) / 0.35)
            noise = (math.sin(x * 0.35 + y * 0.21) + math.cos(y * 0.47 - x * 0.15)) / 2
            damp = 0.08 * max(0, math.sin(x * 0.13 + y * 0.09)) ** 4
            rut = math.exp(-((rd - 0.65) / 0.17) ** 2)
            forest = weights({"moss": 0.72, "dirt": 0.06 + trail * 0.72, "swamp": damp,
                              "grass": 0.16 + noise * 0.04, "rocky": 0.02})
            road = weights({"dirt": 0.92 - rut * 0.06, "swamp": 0.03 + rut * 0.06, "gravel": 0.05})
            mud = weights({"dirt": 0.18, "swamp": 0.82})
            m = lay.mud(x, y)
            samples.append([(1 - m) * ((1 - cover) * f + cover * r) + m * u for f, r, u in zip(forest, road, mud)])
    ddmap.write_terrain(level, samples)


class _All:
    def __contains__(self, item):
        return True


def generate(template, cfg):
    lay, rng = Layout(cfg), random.Random(cfg["seed"])
    data = copy.deepcopy(template)
    world = data["world"]
    level = ddmap.level(data)
    objects = level["objects"]
    trees = [o for o in objects if ddmap.is_tree(o)]
    shrubs = [o for o in objects if ddmap.is_canopy(o) and not ddmap.is_tree(o)]
    if not trees:
        raise SystemExit("Template has no tree objects to reuse.")
    busy = [k for k in ("walls", "paths", "portals", "lights", "patterns", "texts") if level.get(k)]
    if busy:
        print(f"Warning: template layers kept as-is and may sit outside the new layout: {busy}")
    world["width"], world["height"] = lay.W, lay.H
    ddmap.resize_empty_arrays(data)
    data["header"]["editor_state"]["camera_position"] = ddmap.vector(lay.W * ddmap.GRID / 2, lay.H * ddmap.GRID / 2)
    level["objects"] = []
    paint_terrain(level, lay)

    placed = []  # (x, y, r, group): -2 edge band, -1 singles/flanks, >= 0 mesh clusters

    def scatter(count, where, scale, separation, group, pool):
        for _ in range(count):
            template_obj = rng.choice(pool)
            bush = "/shrubs/" in template_obj["texture"]
            sc = rng.uniform(0.9, 1.45) if bush else rng.uniform(*scale)
            if "massive" in template_obj["texture"]:
                sc *= 0.65
            r = sc * (ddmap.CROWN["/shrubs/"] if bush else ddmap.DEFAULT_CROWN)
            for _ in range(12000):
                x, y = where()
                if not lay.blocked(x, y, r) and all(math.hypot(x - ox, y - oy) >= (r + orr) * separation
                                                    for ox, oy, orr, _ in placed):
                    break
            else:
                continue
            ddmap.add_object(data, template_obj, x, y, sc, rng.uniform(-math.pi, math.pi),
                             mirror=rng.random() < 0.5)
            placed.append((x, y, r, group))

    e = cfg["edge"]

    def edge_point():
        side = rng.randrange(4)
        if side < 2:
            return (rng.uniform(0, e["sides"]) if side == 0 else rng.uniform(lay.W - e["sides"], lay.W)), rng.uniform(0, lay.H)
        return rng.uniform(0, lay.W), (rng.uniform(0, e["top_bottom"]) if side == 2 else rng.uniform(lay.H - e["top_bottom"], lay.H))

    scatter(e["trees"], edge_point, e["scale"], e["separation"], -2, trees)

    s = cfg["singles"]

    def near_road():
        while True:
            y = rng.uniform(3, lay.H - 3)
            x = lay.road(y) + rng.uniform(-s["max_road_distance"], s["max_road_distance"])
            if 3 < x < lay.W - 3 and not lay.in_edge(x, y) and lay.road_distance(x, y) <= s["max_road_distance"]:
                return x, y

    scatter(s["count"], near_road, s["scale"], s["separation"], -1, trees + shrubs)

    f = cfg["flanks"]
    inside = lambda x, y, r: lay.in_edge(x, y) or lay.blocked(x, y, r)  # noqa: E731
    centres = []
    for y in range(f["row_step"], lay.H - 6, f["row_step"]):
        n = math.hypot(1, lay.slope(y))
        for side in (-1, 1):
            off = rng.uniform(*f["offset"])
            centres.append((lay.road(y) + side * off / n, y - side * off * lay.slope(y) / n))
    for a, b in cfg["shortcuts"]:
        for t in (0.2, 0.4, 0.6, 0.8):
            y = a + t * (b - a)
            for side in (-1, 1):
                centres.append((lay.trail_x(y, a, b) + side * rng.uniform(3.5, 6), y))
    flank_count = 0
    for c in centres:
        flank_count += len(ddmap.place_cluster(data, rng, placed, -1, c, (0, 1), rng.randint(*f["members"]),
                                               trees, shrubs, blocked=inside, spread=f["spread"],
                                               scales=f["scale"], merge_groups=_All()))

    m = cfg["mesh"]
    mesh_centres = []
    for i, off in enumerate(m["rows"]):
        for side in (-1, 1):
            y = 4 + (i % 2) * 6.5 + rng.uniform(-1, 1)
            while y < lay.H - 4:
                n = math.hypot(1, lay.slope(y))
                cx = lay.road(y) + side * off * m["row_factor"]
                if 9 < cx < lay.W - 9 and 5 < y < lay.H - 5:
                    mesh_centres.append(((cx, y), (lay.slope(y) / n, 1 / n)))
                y += rng.uniform(*m["spacing"])
    mesh_count = 0
    for group, (c, tangent) in enumerate(mesh_centres):
        mesh_count += len(ddmap.place_cluster(data, rng, placed, group, c, tangent, rng.randint(*m["members"]),
                                              trees, shrubs, blocked=lay.blocked, gap=m["gap"],
                                              spread=m["spread"], scales=m["scale"], merge_groups=(-2,)))

    report = {"objects": len(level["objects"]), "edge": sum(1 for p in placed if p[3] == -2),
              "flank_objects": flank_count, "mesh_objects": mesh_count, "mesh_slots": len(mesh_centres),
              "shortcuts": shortcut_savings(lay)}
    return data, report


def shortcut_savings(lay):
    """Feet saved by each shortcut versus the road between its end rows (mud costs double)."""
    out = []
    for a, b in lay.cfg["shortcuts"]:
        start, end = (round(lay.road(a)), a), (round(lay.road(b)), b)
        bounds = lambda x, y: 0 <= x < lay.W and a <= y <= b  # noqa: E731
        on_road = lambda x, y: lay.road_distance(x, y) <= 1.1  # noqa: E731
        difficult = lambda x, y: lay.mud(x, y) > 0.5  # noqa: E731
        road = ddmap.route_cost(start, end, on_road, difficult, bounds)
        trail = ddmap.route_cost(start, end, lambda x, y: on_road(x, y) or lay.trail_distance(x, y) <= 0.6,
                                 difficult, bounds)
        out.append({"rows": [a, b], "road_ft": road, "trail_ft": trail, "saves_ft": road - trail})
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("template", nargs="?")
    parser.add_argument("out", nargs="?")
    parser.add_argument("--config", help="JSON overriding any DEFAULTS keys")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--preview")
    parser.add_argument("--print-config", action="store_true")
    args = parser.parse_args(argv)
    if args.print_config:
        print(json.dumps(DEFAULTS, indent=2))
        return
    if not (args.template and args.out):
        parser.error("template and out are required")
    cfg = merge(DEFAULTS, json.loads(Path(args.config).read_text(encoding="utf-8")) if args.config else {})
    if args.seed is not None:
        cfg["seed"] = args.seed
    if Path(args.out).exists():
        sys.exit(f"{args.out} exists; choose a new name (maps are never overwritten).")
    data, report = generate(ddmap.load(args.template), cfg)
    errors, warnings = ddmap.validate(data)
    if errors:
        sys.exit(f"Validation failed: {errors}")
    ddmap.save_new(data, args.out)
    print(json.dumps(report, indent=1))
    for w in warnings:
        print("Warning:", w)
    for s in report["shortcuts"]:
        if s["saves_ft"] < 30:
            print(f"Warning: shortcut {s['rows']} saves only {s['saves_ft']} ft (aim for 30+).")
    if args.preview:
        ddmap.preview(data, args.preview)


if __name__ == "__main__":
    main()
