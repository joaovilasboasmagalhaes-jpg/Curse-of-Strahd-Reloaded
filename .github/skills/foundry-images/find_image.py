"""Search index.tsv for the best Foundry image.

python find_image.py name <item name>          exact icon Foundry already uses for that item (Bite, Beak, Longsword...)
python find_image.py <want> <keywords...> [-n 8]
  want: spell | item | weapon | armor | feat | token | portrait | avatar | class | species | any
Example: python find_image.py token vampire spawn
         python find_image.py spell necrotic ray
Prints Foundry-relative paths (best first). Use them directly as `img` / token `texture.src`.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# kinds searched per want, in priority order (earlier = small bonus)
WANT = {
    "spell": ["spell-icon", "item-icon-magic", "item-icon"],
    "feat": ["feat-icon", "item-icon-magic", "item-icon", "spell-icon"],
    "item": ["item-icon-campaign", "item-icon", "item-icon-magic"],
    "weapon": ["item-icon-campaign", "item-icon"],
    "attack": ["item-icon", "item-icon-magic"],
    "armor": ["item-icon-campaign", "item-icon"],
    "token": ["token-cos", "token-hero", "token-monster", "token-srd", "portrait-campaign", "item-icon"],
    "portrait": ["portrait-campaign", "token-cos", "token-hero", "token-monster", "token-srd"],
    "avatar": ["avatar-campaign", "portrait-campaign", "token-cos", "token-hero", "token-monster", "token-srd"],
    "class": ["class-icon", "subclass-icon"],
    "species": ["species-icon"],
    "any": None,
}
# creature/term aliases: query word -> extra words to try (lower weight)
ALIASES = {
    "vampire": ["undead", "ghoul"], "spawn": ["vampire"], "zombie": ["undead", "ghoul"], "skeleton": ["undead", "bones"],
    "ghost": ["specter", "undead"], "wolf": ["dog", "beast"], "werewolf": ["wolf", "lycanthrope"],
    "bat": ["beast"], "raven": ["crow", "bird"], "necrotic": ["death", "unholy"], "necromancy": ["death", "unholy"],
    "radiant": ["holy", "light"], "psychic": ["control", "perception"], "thunder": ["sonic"], "cold": ["frost", "ice", "water"],
    "healing": ["life", "heal"], "sword": ["swords"], "bow": ["bows"], "dagger": ["daggers"], "staff": ["staves"],
    "armor": ["chest", "breastplate"], "armour": ["chest", "breastplate"], "ring": ["finger"], "amulet": ["neck"],
    "necklace": ["neck"], "boots": ["feet"], "helmet": ["head", "helm"], "cloak": ["back"], "blood": ["biological", "red"],
    "potion": ["potions"], "book": ["books"], "scroll": ["scrolls"], "key": ["fasteners"], "fire": ["flame"],
    "dark": ["black", "shadow"], "curse": ["unholy", "death"], "poison": ["toxins", "acid"],
}


PATH_BONUS = {"attack": "/creatures/abilities/|/creatures/claws/|/skills/melee/|/weapons/",
              "weapon": "/weapons/", "armor": "/equipment/", "item": "/equipment/|/consumables/|/sundries/|/tools/|/containers/"}


def stem(w):
    return w[:-1] if len(w) > 3 and w.endswith("s") else w


def load():
    with open(os.path.join(HERE, "index.tsv"), encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p, k, kw = line.rstrip("\n").split("\t")
            yield p, k, kw.split()


def lookup_item(name):
    """Exact (then singular/plural) item-name match in item_icons.tsv -> (img, count, alternatives) or None."""
    base = " ".join(re.sub(r"\([^)]*\)", "", name.lower()).split())
    table = {}
    with open(os.path.join(HERE, "item_icons.tsv"), encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            k, img, cnt, alts = (line.rstrip("\n").split("\t") + [""])[:4]
            table[k] = (img, int(cnt), [a for a in alts.split("|") if a])
    for cand in (base, base[:-1] if base.endswith("s") else base + "s"):
        if cand in table:
            return table[cand]
    return None


def main(argv):
    if len(argv) >= 2 and argv[0] == "name":
        hit = lookup_item(" ".join(argv[1:]))
        if hit:
            print(f"{hit[0]}   (used {hit[1]}x in Foundry)")
            for a in hit[2]:
                print(f"  alt: {a}")
            return 0
        print("no item with that name in Foundry; use `attack <keywords>` / `weapon <keywords>` to pick the closest icon")
        return 2
    n = 8
    if "-n" in argv:
        i = argv.index("-n")
        n = int(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) < 2 or argv[0] not in WANT:
        print(__doc__)
        return 1
    want, terms = argv[0], [stem(t.lower()) for t in argv[1:]]
    kinds = WANT[want]
    extra = {a: 0.4 for t in terms for a in ALIASES.get(t, [])}
    scored = []
    for path, kind, kws in load():
        if kinds is not None and kind not in kinds:
            continue
        stems = [stem(k) for k in kws]
        fname = set(stem(w) for w in re.split(r"[^a-z]+", os.path.basename(path).lower()))
        score, hit = 0.0, 0
        for t in terms:
            if t in stems:
                hit += 1
                score += 3 + (2 if t in fname else 0)
            elif any(s.startswith(t) for s in stems):
                hit += 1
                score += 1.5
            elif any(len(s) >= 4 and t.endswith(s) for s in stems):
                hit += 1
                score += 1.5  # compound words: longsword -> sword
        for a, wgt in extra.items():
            if a in stems:
                score += wgt * 3
        if hit == 0 and score < 1:
            continue
        score += 1.0 * (hit == len(terms))
        if kinds:
            score += 0.5 * (len(kinds) - kinds.index(kind)) / len(kinds)
        if want in PATH_BONUS and re.search(PATH_BONUS[want], path):
            score += 3
        scored.append((-score, path, kind))
    scored.sort()
    if not scored and kinds is not None:
        print("(nothing in the preferred sources; searching everything)")
        return main(["any"] + argv[1:] + ["-n", str(n)])
    for s, path, kind in scored[:n]:
        print(f"{-s:5.1f}  {kind:18} {path}")
    if not scored:
        print("no match: broaden words, try a synonym, or use the fallback in SKILL.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
