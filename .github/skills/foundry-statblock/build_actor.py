"""Build a Foundry VTT dnd5e NPC actor JSON from a compact spec.

Usage: python build_actor.py spec.json [out.json]
Without out.json the actor is written to assets/stat_blocks/fvtt-Actor-<name>.json.
Target: Foundry v14, dnd5e system 6.0.x, rules 2014. See SKILL.md for the spec format.
Foundry computes attack bonuses, save DCs for spells and ability-mod damage by itself,
so the script only writes dice, types and explicit overrides.
"""
import json
import os
import random
import re
import string
import sys
import time

ABILITIES = ["str", "dex", "con", "int", "wis", "cha"]
SKILLS = {
    "acr": "dex", "ani": "wis", "arc": "int", "ath": "str", "dec": "cha", "his": "int",
    "ins": "wis", "itm": "cha", "inv": "int", "med": "wis", "nat": "int", "prc": "wis",
    "prf": "cha", "per": "cha", "rel": "int", "slt": "dex", "ste": "dex", "sur": "wis",
}
ACTIVATION = {"action": "action", "bonus": "bonus", "reaction": "reaction", "special": "special",
              "legendary": "legendary", "lair": "lair", "none": ""}
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
STAT_BLOCKS_DIR = os.path.normpath(os.path.join(SKILL_DIR, "..", "..", "..", "assets", "stat_blocks"))
SPELLS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "srd_spells_2014.json")
DEFAULT_ICON = {"weapon": "icons/weapons/swords/sword-guard-purple.webp",
                "feat": "icons/magic/symbols/rune-sigil-black-pink.webp",
                "spell": "icons/magic/symbols/star-solid-gold.webp",
                "equipment": "icons/equipment/chest/breastplate-scale-grey.webp"}
NOW = int(time.time() * 1000)


ITEM_ICONS_FILE = os.path.join(SKILL_DIR, "..", "foundry-images", "item_icons.tsv")
_ITEM_ICONS = None


def named_item_icon(kind, spec):
    """Reuse Foundry's existing icon for an exact item name when one is available."""
    global _ITEM_ICONS
    is_attack = kind == "weapon" or any(a.get("type") == "attack" for a in spec.get("activities", []))
    if _ITEM_ICONS is None:
        _ITEM_ICONS = {}
        if os.path.exists(ITEM_ICONS_FILE):
            with open(ITEM_ICONS_FILE, encoding="utf-8") as fh:
                next(fh)
                for line in fh:
                    k, img = line.split("\t")[:2]
                    _ITEM_ICONS[k] = img
    base = " ".join(re.sub(r"\([^)]*\)", "", spec["name"].lower()).split())
    for cand in (base, base[:-1] if base.endswith("s") else base + "s"):
        if cand in _ITEM_ICONS:
            return _ITEM_ICONS[cand]
        if is_attack:
          print(f"warning: no Foundry icon for attack '{spec['name']}'; set `img` from foundry-images "
              f"(python find_image.py attack <keywords>)", file=sys.stderr)
    return None


def rid():
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))


def roll_mode():
    return {"min": None, "max": None, "mode": 0}


def p(text):
    """Wrap plain text in <p> unless it already is HTML."""
    return text if text.lstrip().startswith("<") else f"<p>{text}</p>"


def stats():
    return {"coreVersion": "14.368", "systemId": "dnd5e", "systemVersion": "6.0.3",
            "createdTime": NOW, "modifiedTime": NOW, "compendiumSource": None,
            "duplicateSource": None, "exportSource": None}


def damage_part(d):
    """d: {"n":1,"d":6,"type":"slashing","bonus":""} (type may be a list)."""
    types = d.get("type", [])
    if "formula" in d:  # flat value such as healing "1"
        return {"custom": {"enabled": True, "formula": str(d["formula"])}, "number": None,
                "denomination": None, "bonus": "", "types": [types] if isinstance(types, str) else types,
                "scaling": {"number": 1}, "modifiers": []}
    return {"custom": {"enabled": False, "formula": ""}, "number": d.get("n"),
            "denomination": d.get("d"), "bonus": d.get("bonus", ""),
            "types": [types] if isinstance(types, str) else types,
            "scaling": {"number": 1}, "modifiers": []}


def consumption(a):
    """Legendary actions and Legendary Resistance spend the actor's resource pools, as in the CoS import."""
    if a.get("activation") == "legendary":
        return [{"type": "attribute", "target": "resources.legact.value",
                 "value": str(a.get("cost", 1)), "scaling": {}}]
    if a.get("legres"):
        return [{"type": "attribute", "target": "resources.legres.value", "value": "1", "scaling": {}}]
    return a.get("consumes", [])


def activity(a, default_activation, fallback_img=None):
    t = a["type"]
    aid = rid()
    act = {
        "_id": aid, "type": t, "name": a.get("name", ""), "sort": 0,
        "img": a.get("img", fallback_img),
        "activation": {"type": ACTIVATION[a.get("activation", default_activation)],
                       "value": a.get("cost", 1) if a.get("activation") in ("legendary", "lair") else None,
                       "override": False, "condition": a.get("condition", "")},
        "consumption": {"scaling": {"allowed": False}, "spellSlot": True, "targets": consumption(a)},
        "description": {"chatFlavor": "", "value": ""},
        "duration": {"units": "inst", "concentration": False, "override": False, "expiry": None},
        "range": {"units": "self", "override": False},
        "target": {"template": {"contiguous": False, "units": "ft", "stationary": False},
                   "affects": {"choice": False}, "override": False, "prompt": True},
        "uses": {"spent": 0, "recovery": [], "max": ""},
        "visibility": {"level": {}, "requireAttunement": False, "requireIdentification": False,
                       "requireMagic": False},
        "effects": [], "flags": {}, "behaviors": [],
    }
    if "range" in a:
        act["range"] = {"value": str(a["range"]), "units": "ft", "override": False}
    if t == "attack":
        kind = a.get("kind", "melee")  # melee | ranged
        act["attack"] = {"ability": a.get("ability", ""), "bonus": a.get("bonus", ""),
                         "critical": {"threshold": None}, "flat": bool(a.get("flat", False)),
                         "type": {"value": kind, "classification": a.get("classification", "weapon")}}
        act["damage"] = {"critical": {"bonus": ""}, "includeBase": a.get("include_base", False),
                         "parts": [damage_part(x) for x in a.get("damage", [])]}
        if "range" not in a:
            act["range"] = {"value": "5", "units": "ft", "override": False}
    elif t == "save":
        ability = a["ability"]
        act["save"] = {"ability": [ability] if isinstance(ability, str) else ability, "visible": True,
                       "dc": {"calculation": "", "formula": str(a["dc"])}}
        act["damage"] = {"onSave": a.get("on_save", "none"),
                         "parts": [damage_part(x) for x in a.get("damage", [])]}
    elif t == "damage":
        act["damage"] = {"critical": {"allow": False}, "parts": [damage_part(x) for x in a["damage"]]}
    elif t == "heal":
        act["healing"] = damage_part(a["heal"])
    elif t == "utility":
        act["roll"] = {"prompt": False, "visible": False}
    else:
        raise SystemExit(f"Unsupported activity type: {t}")
    if a.get("uses"):
        u = a["uses"]  # {"max": 3, "recover": "day"|"lr"|"sr"|"recharge", "formula": "5-6"}
        act["uses"] = {"spent": 0, "max": str(u["max"]), "recovery": uses_recovery(u)}
    return aid, act


def uses_recovery(u):
    if u.get("recover") == "recharge":
        return [{"period": "recharge", "formula": u.get("formula", "6")}]
    period = {"day": "day", "lr": "lr", "sr": "sr"}[u["recover"]]
    return [{"period": period, "type": "recoverAll"}]


def base_item(kind, spec):
    name = spec["name"]
    return {
        "_id": rid(), "name": name, "type": kind,
        "img": spec.get("img") or named_item_icon(kind, spec) or DEFAULT_ICON[kind], "effects": [], "folder": None, "sort": 0,
        "flags": {}, "_stats": stats(),
        "system": {"description": {"value": p(spec.get("description", "")), "chat": ""},
                   "source": {"custom": "", "book": spec.get("book", ""), "page": "",
                              "license": "", "rules": "2014", "revision": 1},
                   "identifier": name.lower().replace(" ", "-").replace(",", "")},
    }


def build_feat(spec):
    it = base_item("feat", spec)
    acts = {}
    for a in spec.get("activities", []):
        a = {"activation": spec.get("activation", "action"), "cost": spec.get("cost", 1), **a}
        aid, act = activity(a, a["activation"], it["img"])
        acts[aid] = act
    it["system"].update({
        "type": {"value": "monster", "subtype": ""}, "activities": acts,
        "uses": {"max": "", "spent": 0, "recovery": []}, "advancement": {},
        "prerequisites": {"items": [], "repeatable": False, "level": None},
        "properties": [], "requirements": "", "enchant": {}, "crewed": False})
    if spec.get("uses"):
        u = spec["uses"]
        it["system"]["uses"] = {"max": str(u["max"]), "spent": 0, "recovery": uses_recovery(u)}
    return it


def build_weapon(spec):
    """spec: base ("scimitar"), wtype ("martialM"), props ["fin","lgt"], reach/range, damage [...],
    plus optional rider activities (e.g. a save) and magical bonus."""
    it = base_item("weapon", spec)
    natural = spec.get("natural", False)
    ranged = bool(spec.get("ranged", False))
    main = {"type": "attack", "kind": "ranged" if ranged else "melee", "include_base": not natural,
            "bonus": spec.get("attack_bonus", ""), "ability": spec.get("ability", "")}
    if natural:  # dice live in the activity (as in the CoS import); first part adds the ability mod
        parts = [dict(x) for x in spec.get("damage", [])]
        if parts:
            parts[0].setdefault("bonus", "@mod")
        main["damage"] = parts
    if ranged:
        main["range"] = spec.get("range", 80)
    elif spec.get("reach"):
        main["range"] = spec["reach"]
    acts = {}
    for a in [main] + spec.get("activities", []):
        aid, act = activity(a, "action", it["img"])
        acts[aid] = act
    base = {} if natural else spec.get("damage", [{"n": 1, "d": 6, "type": "slashing"}])[0]
    versatile = spec.get("versatile")
    it["system"].update({
        "quantity": 1, "weight": {"value": spec.get("weight", 0), "units": "lb"},
        "price": {"value": spec.get("price", 0), "denomination": "gp"},
        "attunement": "", "equipped": True, "identified": True, "cover": None,
        "uses": {"max": "", "spent": 0, "recovery": []},
        "range": ({"value": spec.get("range", 80), "long": spec.get("long", 320), "units": "ft", "reach": None}
                  if ranged else {"value": None, "long": None, "units": "ft", "reach": spec.get("reach")}),
        "damage": {"base": damage_part(base) if base else
                   {"types": [], "custom": {"enabled": False}, "scaling": {"number": 1}, "modifiers": []},
                   "versatile": (damage_part(versatile) if versatile else
                                 {"number": None, "denomination": None, "bonus": "", "types": [],
                                  "custom": {"enabled": True, "formula": ""},
                                  "scaling": {"mode": "", "number": None, "formula": ""}, "modifiers": []})},
        "type": {"value": "natural" if natural else spec.get("wtype", "martialM"),
                 "baseItem": spec.get("base", "")},
        "properties": spec.get("props", []), "proficient": None,
        "magicalBonus": spec.get("magical_bonus"), "mastery": spec.get("mastery", ""),
        "activities": acts, "attuned": False, "unidentified": {"description": ""},
        "container": None, "rarities": [], "crew": {"value": []}})
    return it


_SPELLS = None


def spell_uuid(sp):
    """Cast activities resolve spell.uuid with fromUuid, so link to the SRD 2014 compendium (or a given uuid)."""
    global _SPELLS
    if sp.get("uuid"):
        return sp["uuid"]
    if _SPELLS is None:
        _SPELLS = json.load(open(SPELLS_FILE, encoding="utf8"))
    if sp["name"] not in _SPELLS:
        raise SystemExit(f"Spell '{sp['name']}' not in data/srd_spells_2014.json; give its Foundry uuid in the spec")
    return f"Compendium.dnd5e.spells.Item.{_SPELLS[sp['name']]}"


def build_spellcasting(spec):
    """Feat holding one `cast` activity per spell, linked to the compendium spell.
    spec: name ("Spellcasting"/"Innate Spellcasting"), description, spells [{name, per_day?, uuid?}]."""
    it = build_feat(spec)
    acts = {}
    for sp in spec["spells"]:
        aid, act = activity({"type": "utility", "img": sp.get("img", it["img"])}, "action", it["img"])
        act["type"] = "cast"
        act["name"] = ""
        act["spell"] = {"uuid": spell_uuid(sp), "spellbook": False, "properties": [],
                        "challenge": {"override": False}}
        if sp.get("per_day"):
            act["uses"] = {"spent": 0, "max": str(sp["per_day"]),
                           "recovery": [{"period": "day", "type": "recoverAll"}]}
        acts[aid] = act
    it["system"]["activities"] = acts
    return it


def build_equipment(spec):
    it = base_item("equipment", spec)
    it["system"].update({
        "quantity": 1, "weight": {"value": spec.get("weight", 0), "units": "lb"},
        "price": {"value": spec.get("price", 0), "denomination": "gp"}, "attunement": "",
        "equipped": True, "identified": True, "armor": {"value": spec["ac"], "dex": spec.get("dex_cap")},
        "type": {"value": spec.get("armor_type", "light"), "baseItem": spec.get("base", "")},
        "properties": [], "activities": {}, "attuned": False, "rarities": []})
    return it


BUILDERS = {"feat": build_feat, "weapon": build_weapon, "spellcasting": build_spellcasting, "equipment": build_equipment}


def build(spec):
    ab = {}
    for k in ABILITIES:
        ab[k] = {"value": spec["abilities"][k], "proficient": 1 if k in spec.get("saves", []) else 0,
                 "max": None, "check": {"roll": roll_mode()}, "save": {"roll": roll_mode()},
                 "attack": {"roll": roll_mode()}}
    skills = {k: {"ability": v, "roll": roll_mode(), "value": spec.get("skills", {}).get(k, 0),
                  "bonuses": {"passive": ""}} for k, v in SKILLS.items()}
    speeds = {k: "" for k in ("walk", "burrow", "climb", "fly", "swim")}
    speeds.update({k: str(v) for k, v in spec.get("speed", {"walk": 30}).items()})
    senses = {k: spec.get("senses", {}).get(k) for k in ("blindsight", "darkvision", "tremorsense", "truesight")}
    ac = spec.get("ac")  # None = derive from equipped armor, int = flat/natural AC
    ac_block = ({"flat": None, "calcs": ["unarmored", "armored"], "formulas": [], "override": None}
                if ac is None else {"flat": ac, "calcs": ["natural"], "formulas": [], "override": None})
    hp = spec["hp"]  # {"max": 180, "formula": "28d8 + 72"}
    t = spec.get("type", {})
    leg = spec.get("legendary_actions", 0)

    def traits(key):
        return {"value": spec.get(key, []), "custom": spec.get(key + "_custom", ""),
                **({"bypasses": spec.get(key + "_bypasses", [])} if key != "ci" else {})}

    items = [BUILDERS[i.get("kind", "feat")](i) for i in spec.get("items", [])]
    token = {"name": spec["name"], "displayName": 0, "actorLink": False, "width": 1, "height": 1,
             "depth": 1, "texture": {"src": spec.get("token", spec.get("img", "icons/svg/mystery-man.svg")),
                                     "anchorX": 0.5, "anchorY": 0.5, "fit": "contain", "scaleX": 1,
                                     "scaleY": 1, "tint": "#ffffff", "alphaThreshold": 0.75},
             "lockRotation": False, "rotation": 0, "alpha": 1, "disposition": -1, "displayBars": 0,
             "bar1": {"attribute": "attributes.hp"}, "bar2": {"attribute": None},
             "sight": {"enabled": False}, "flags": {}, "randomImg": False,
             "appendNumber": False, "prependAdjective": False}
    token["width"] = token["height"] = spec.get("token_size", 1)
    return {
        "name": spec["name"], "type": "npc", "img": spec.get("img", "icons/svg/mystery-man.svg"),
        "system": {
            "currency": {"pp": 0, "gp": 0, "ep": 0, "sp": 0, "cp": 0},
            "abilities": ab,
            "bonuses": {"spell": {"dc": ""}},
            "skills": skills, "tools": {},
            "spells": {f"spell{i}": {"value": spec.get("slots", {}).get(str(i), 0), "override": None}
                       for i in range(1, 10)}
                      | {"pact": {"value": 0, "override": None}},
            "attributes": {
                "ac": ac_block, "init": {"ability": "", "roll": roll_mode()},
                "movement": {"units": "ft", "hover": spec.get("hover", False), "ignoredDifficultTerrain": [],
                             "bonus": "", "special": "", "speeds": speeds},
                "attunement": {"max": 3},
                "senses": {"ranges": senses, "units": "ft", "special": spec.get("senses_special", "")},
                "spellcasting": spec.get("spellcasting", ""), "exhaustion": 0,
                "concentration": {"ability": "", "roll": roll_mode(), "limit": 1},
                "loyalty": {}, "hd": {"spent": 0},
                "hp": {"max": hp["max"], "temp": None, "tempmax": None, "value": hp.get("value", hp["max"]),
                       "formula": hp.get("formula", ""), "dt": None},
                "death": {"roll": roll_mode(), "success": 0, "failure": 0},
                "price": {"value": None, "denomination": "gp"}, "spell": {"level": 0}},
            "details": {
                "biography": {"value": spec.get("biography", ""), "public": ""},
                "alignment": spec.get("alignment", ""), "ideal": "", "bond": "", "flaw": "", "race": None,
                "type": {"value": t.get("value", "humanoid"), "subtype": t.get("subtype", ""),
                         "swarm": t.get("swarm", ""), "custom": ""},
                "habitat": {"value": [], "custom": ""}, "cr": spec["cr"], "treasure": {"value": []}},
            "resources": {"legact": {"max": leg, "spent": 0}, "legres": {"max": spec.get("legendary_resistances", 0), "spent": 0},
                          "lair": {"value": "lair" in spec, "initiative": spec.get("lair"), "inside": False}},
            "source": {"revision": 1, "rules": "2014", "custom": "", "book": spec.get("book", ""),
                       "page": str(spec.get("page", "")), "license": ""},
            "traits": {"size": spec.get("size", "med"),
                       "di": traits("di"), "dr": traits("dr"), "dv": traits("dv"),
                       "dm": {"amount": {}, "bypasses": []}, "ci": traits("ci"),
                       "languages": {"value": spec.get("languages", []), "custom": spec.get("languages_custom", ""),
                                     "communication": {"telepathy": {"value": spec.get("telepathy"), "units": "ft"}}},
                       "important": False},
            "identifier": spec["name"].lower().replace(" ", "-").replace(",", ""),
            "rolls": {},
        },
        "prototypeToken": token, "items": items, "effects": [], "ownership": {"default": 0},
        "flags": {}, "_stats": stats(),
    }


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf8"))
    out = sys.argv[2] if len(sys.argv) > 2 else None
    actor = build(spec)
    if not out:
        slug = spec["name"].lower().replace(",", "").replace(" ", "-")
        out = os.path.join(STAT_BLOCKS_DIR, f"fvtt-Actor-{slug}.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf8") as f:
        json.dump(actor, f, indent=2, ensure_ascii=False)
    print("wrote", out)
