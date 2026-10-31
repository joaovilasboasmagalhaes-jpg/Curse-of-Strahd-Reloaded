"""Harvest the icons Foundry already uses for items (Bite, Claw, Beak, Longsword, ...) into item_icons.tsv.

Run: python build_item_icons.py   (Foundry may stay open; the databases are copied first)
Sources: the world's items/actors and packs, and the dnd5e system monster/item packs. Only local paths
(no http links) are kept. The most used icon per normalised item name wins; icons from the Curse of
Strahd world and packs get priority so campaign monsters keep their look.
Output columns: name, img, count, alternatives (up to 3 other icons).
"""
import collections
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
APP = r"C:\Program Files\Foundry Virtual Tabletop\resources\app"
EXE = r"C:\Program Files\Foundry Virtual Tabletop\Foundry Virtual Tabletop.exe"
DATA = r"C:\Users\João Magalhães\AppData\Local\FoundryVTT\Data"
WORLD = os.path.join(DATA, "worlds", "curse-of-strahd")
SYSTEM = os.path.join(DATA, "systems", "dnd5e", "packs")
PRIORITY = ("world-", "pack-all-creatures", "pack-curse-of-strahd-creatures", "pack-custom-")
SOURCES = (
    [(os.path.join(WORLD, "data", p), "world-" + p) for p in ("actors", "items")]
    + [(os.path.join(WORLD, "packs", p), "pack-" + p) for p in
       ("all-creatures", "curse-of-strahd-creatures", "custom-creatures", "custom-items", "feats")]
    + [(os.path.join(SYSTEM, p), "sys-" + p) for p in
       ("monsters", "monsterfeatures", "monsterfeatures24", "actors24", "items", "feats24", "equipment24")]
)


def norm(name):
    """Lowercase, drop parenthetical notes ("Bite (Wolf Form Only)"), keep the rest."""
    name = name.lower()
    while "(" in name and ")" in name:
        a, b = name.index("("), name.index(")")
        name = name[:a] + name[b + 1:]
    return " ".join(name.split())


def main():
    tmp = tempfile.mkdtemp(prefix="fvtt-icons-")
    try:
        dirs = []
        for src, label in SOURCES:
            if os.path.isdir(src):
                dst = os.path.join(tmp, label)
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("LOCK"))
                dirs.append(dst)
        out = os.path.join(tmp, "rows.json")
        env = dict(os.environ, ELECTRON_RUN_AS_NODE="1", SRC_DIRS=";".join(dirs), OUT_FILE=out,
                   CLASSIC_LEVEL=os.path.join(APP, "node_modules", "classic-level").replace("\\", "/"))
        subprocess.run([EXE, os.path.join(HERE, "dump_items.js")], env=env, check=True)
        rows = json.load(open(out, encoding="utf-8"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    score = collections.defaultdict(collections.Counter)
    for r in rows:
        img = r.get("img") or ""
        if not r.get("name") or img.startswith("http") or img.endswith(".svg") or not img:
            continue
        w = 1000 if r["src"].startswith(PRIORITY) else 1
        score[norm(r["name"])][img] += w
    lines = ["name\timg\tcount\talternatives"]
    for name in sorted(score):
        ranked = score[name].most_common()
        total = sum(c % 1000 if c >= 1000 else c for _, c in ranked)
        lines.append("\t".join([name, ranked[0][0], str(total), "|".join(i for i, _ in ranked[1:4])]))
    path = os.path.join(HERE, "item_icons.tsv")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"{len(lines) - 1} item names -> {path} ({os.path.getsize(path) // 1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
