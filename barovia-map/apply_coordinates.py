import json
import sys
from pathlib import Path

# Add barovia-map to path
sys.path.insert(0, str(Path(__file__).parent))
import barovia_map_tileserver

payload = json.loads(barovia_map_tileserver.pins_payload().decode("utf-8"))
pin_dict = {p["name"]: [p["latitude"], p["longitude"]] for p in payload["pins"]}

timeline_path = Path(__file__).parent.parent / "assets" / "curse-of-strahd.timeline"

with open(timeline_path, "r", encoding="utf-8") as f:
    tl = json.load(f)

# Define mapping from element id to pin coordinates (lat, lng)
mapping = {
    # Spans
    "span-amber-temple-wizards": pin_dict["The Amber Temple"],
    "span-dostron-occupation": pin_dict["Castle Ravenloft"],
    "span-abbey-markovia": pin_dict["Village of Krezk"],
    "span-abbey-sealed": pin_dict["Village of Krezk"],
    "span-order-silver-dragon": pin_dict["Argynvostholt"],
    "span-wow-wereraven": pin_dict["Wizard of Wines"],
    "span-battle-luna-river": pin_dict["Argynvostholt"],
    "span-wow-krezkov": pin_dict["Wizard of Wines"],
    "span-strahd-mortal-ruler": pin_dict["Castle Ravenloft"],
    "span-strahd-vampire-lord": pin_dict["Castle Ravenloft"],
    "span-revenants-argynvostholt": pin_dict["Argynvostholt"],
    "span-durst-cult": pin_dict["Village of Barovia"],
    "span-patrina-intrigue": pin_dict["The Amber Temple"],
    "span-madam-eva-pact": pin_dict["Tser Pool Encampment"],
    "span-strahd-retainers": pin_dict["Castle Ravenloft"],
    "span-baba-lysaga-coven": pin_dict["Ruins of Berez"],
    "span-cult-chernovog": pin_dict["Yester Hill"],
    "span-wow-martikov": pin_dict["Wizard of Wines"],
    "span-fiona-wachter": pin_dict["Town of Vallaki"],
    "span-izek-strazni": pin_dict["Town of Vallaki"],
    "span-abbot-tenure": pin_dict["Village of Krezk"],
    "span-keepers-feather": pin_dict["Wizard of Wines"],
    "span-strahd-reawakening": pin_dict["Castle Ravenloft"],

    # Events
    "event-devourer-slain": pin_dict["Yester Hill"],
    "event-amber-temple-founded": pin_dict["The Amber Temple"],
    "event-wizards-fall": pin_dict["The Amber Temple"],
    "event-kavan-whispering-wall": pin_dict["Yester Hill"],
    "event-kavan-bloodthorn": pin_dict["Yester Hill"],
    "event-gems-to-wereravens": pin_dict["Wizard of Wines"],
    "event-dostron-fortress": pin_dict["Castle Ravenloft"],
    "event-dostron-dies": pin_dict["Castle Ravenloft"],
    "event-markovia-begins-abbey": pin_dict["Village of Krezk"],
    "event-abbey-completed": pin_dict["Village of Krezk"],
    "event-argynvost-arrives": pin_dict["Argynvostholt"],
    "event-argynvostholt-built": pin_dict["Argynvostholt"],
    "event-wow-founded": pin_dict["Wizard of Wines"],
    "event-tsolenka-tower": pin_dict["Tsolenka Pass"],
    "event-luna-river-battle": pin_dict["Argynvostholt"],
    "event-argynvost-slain": pin_dict["Argynvostholt"],
    "event-valley-named-barovia": pin_dict["Castle Ravenloft"],
    "event-markovia-condemns-strahd": pin_dict["Castle Ravenloft"],
    "event-vallaki-krezk-founded": pin_dict["Town of Vallaki"],
    "event-wow-to-krezkov": pin_dict["Wizard of Wines"],
    "event-wachter-land-granted": pin_dict["Town of Vallaki"],
    "event-durst-settle": pin_dict["Village of Barovia"],
    "event-andral-dies": pin_dict["Town of Vallaki"],
    "event-lysaga-svalich": pin_dict["Ruins of Berez"],
    "event-patrina-amber-secrets": pin_dict["The Amber Temple"],
    "event-ravenloft-begins": pin_dict["Castle Ravenloft"],
    "event-ravenloft-completed": pin_dict["Castle Ravenloft"],
    "event-strahd-refuses-gifts": pin_dict["The Amber Temple"],
    "event-ravenovia-dies": pin_dict["Castle Ravenloft"],
    "event-sigil-of-the-sun": pin_dict["Castle Ravenloft"],
    "event-fanes-bound": pin_dict["Castle Ravenloft"],
    "event-sergei-tatyana-love": pin_dict["Village of Barovia"],
    "event-sergei-abdicates": pin_dict["Castle Ravenloft"],
    "event-wedding-tragedy": pin_dict["Castle Ravenloft"],
    "event-guards-slaughtered": pin_dict["Castle Ravenloft"],
    "event-katarina-madam-eva": pin_dict["Tser Pool Encampment"],
    "event-heart-of-sorrow": pin_dict["Castle Ravenloft"],
    "event-revenants-confront-eva": pin_dict["Castle Ravenloft"],
    "event-mirrors-removed": pin_dict["Castle Ravenloft"],
    "event-mists-confirmed": pin_dict["Gates of Barovia"],
    "event-beucephalus-nightmare": pin_dict["Castle Ravenloft"],
    "event-sasha-bride": pin_dict["Castle Ravenloft"],
    "event-patrina-death": pin_dict["Town of Vallaki"],
    "event-markovia-holy-war": pin_dict["Castle Ravenloft"],
    "event-wights-raised": pin_dict["Castle Ravenloft"],
    "event-brightblade-destroyed": pin_dict["Van Richten's Tower"],
    "event-mist-vision-homeland": pin_dict["Yester Hill"],
    "event-abbey-clergy-fall": pin_dict["Village of Krezk"],
    "event-argynvost-ghost": pin_dict["Argynvostholt"],
    "event-elisabeth-amber-shard": pin_dict["Village of Barovia"],
    "event-walter-bound": pin_dict["Village of Barovia"],
    "event-durst-cult-destroyed": pin_dict["Village of Barovia"],
    "event-khazan-family-dies": pin_dict["Van Richten's Tower"],
    "event-khazan-lich": pin_dict["The Amber Temple"],
    "event-sergei-tomb": pin_dict["Castle Ravenloft"],
    "event-marina-ulrich-death": pin_dict["Ruins of Berez"],
    "event-martikov-krezkov-marriage": pin_dict["Wizard of Wines"],
    "event-wow-inherited-martikov": pin_dict["Wizard of Wines"],
    "event-leo-dilisnya-hunted": pin_dict["Village of Krezk"],
    "event-leo-entombed": pin_dict["Town of Vallaki"],
    "event-baba-lysaga-berez": pin_dict["Ruins of Berez"],
    "event-khazan-demilich": pin_dict["Van Richten's Tower"],
    "event-ludmilla-bride": pin_dict["Castle Ravenloft"],
    "event-anastrasya-volenta-brides": pin_dict["Castle Ravenloft"],
    "event-ithuriel-abbot": pin_dict["Village of Krezk"],
    "event-grand-conjunction-foretold": pin_dict["Tser Pool Encampment"],
    "event-devourer-torn-free": pin_dict["Castle Ravenloft"],
    "event-fanes-bound-to-heart": pin_dict["Castle Ravenloft"],
    "event-hibernation-begins": pin_dict["Castle Ravenloft"],
    "event-sigil-recovered": pin_dict["Castle Ravenloft"],
    "event-keepers-founded": pin_dict["Wizard of Wines"],
    "event-baba-zelenna-cult": pin_dict["Yester Hill"],
    "event-chernovog-defeated": pin_dict["Yester Hill"],
    "event-fiona-runs-away": pin_dict["Ruins of Berez"],
    "event-fiona-ezra-pact": pin_dict["Town of Vallaki"],
    "event-radanavich-destroyed": pin_dict["Van Richten's Tower"],
    "event-ireena-dire-wolf": pin_dict["Lake Zarovich"],
    "event-izek-fire-arm": pin_dict["Town of Vallaki"],
    "event-roc-steals-gem": pin_dict["Wizard of Wines"],
    "event-blue-water-inn": pin_dict["Town of Vallaki"],
    "event-ezmerelda-leg": pin_dict["Werewolf Den"],
    "event-victor-spellbook": pin_dict["Town of Vallaki"],
    "event-nikolai-dies": pin_dict["Town of Vallaki"],
    "event-van-richten-enters-barovia": pin_dict["Village of Barovia"],
    "event-doru-recognizes": pin_dict["Village of Barovia"],
    "event-mob-attacks-ravenloft": pin_dict["Castle Ravenloft"],
    "event-escher-doru-turned": pin_dict["Castle Ravenloft"],
    "event-rahadin-confirms-date": pin_dict["Castle Ravenloft"],
    "event-patrina-contacts-kasimir": pin_dict["Town of Vallaki"],
    "event-rahadin-proclamation": pin_dict["Castle Ravenloft"],
    "event-vallaki-gates-closed": pin_dict["Town of Vallaki"],
    "event-abbot-harvests-remains": pin_dict["Village of Krezk"],
    "event-morgantha-settles": pin_dict["Old Bonegrinder"],
    "event-werewolf-loyalty": pin_dict["Werewolf Den"],
    "event-stella-severed": pin_dict["Town of Vallaki"],
    "event-kasimir-turned-back": pin_dict["Tsolenka Pass"],
    "event-zombie-siege": pin_dict["Village of Barovia"],
    "event-doru-torments-father": pin_dict["Village of Barovia"],
}

tl["file"]["mapTileUrl"] = "http://127.0.0.1:8765/tiles/{z}/{x}/{y}.png"

for elem in tl["elements"]:
    eid = elem["id"]
    if "coordinates" in elem:
        del elem["coordinates"]
    if eid in mapping:
        elem["lat"] = mapping[eid][0]
        elem["lng"] = mapping[eid][1]
    else:
        if "lat" in elem:
            del elem["lat"]
        if "lng" in elem:
            del elem["lng"]

with open(timeline_path, "w", encoding="utf-8") as f:
    json.dump(tl, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Successfully updated timeline with lat and lng fields on {len(mapping)} elements.")
