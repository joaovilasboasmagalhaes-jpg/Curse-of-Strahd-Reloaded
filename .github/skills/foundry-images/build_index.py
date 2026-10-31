"""Scan the Foundry install and user data, write index.tsv (Foundry-relative path, kind, keywords).

Run: python build_index.py
Paths are the ones Foundry resolves: core files as `icons/...`, user files relative to Data/.
"""
import os
import re
import sys

APP = r"C:\Program Files\Foundry Virtual Tabletop\resources\app\public"
DATA = r"C:\Users\João Magalhães\AppData\Local\FoundryVTT\Data"
EXT = {".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif"}

# (root, subfolder, foundry prefix, [(regex on lowercase relative path, kind)]); first match wins
SOURCES = [
    (APP, "icons", "icons", [(r"^svg/", "core-svg"), (r"^magic/", "item-icon-magic"), (r"^", "item-icon")]),
    (DATA, r"systems\dnd5e\icons", "systems/dnd5e/icons", [(r"^svg/", "dnd5e-svg"), (r"^classes/", "class-icon"),
        (r"^species/", "species-icon"), (r"^spell-tiers/", "spell-tier-icon"), (r"^", "dnd5e-icon")]),
    (DATA, r"systems\dnd5e\tokens", "systems/dnd5e/tokens", [(r"^thumbs/", "token-thumb"), (r"^heroes/", "token-hero"),
        (r"^", "token-monster")]),
    (DATA, r"assets\srd5e\img\bestiary", "assets/srd5e/img/bestiary", [(r"^tokens/cos/", "token-cos"), (r"^", "token-srd")]),
    (DATA, r"modules\plutonium\media\icon", "modules/plutonium/media/icon", [(r"^spell/", "spell-icon"),
        (r"^feat/", "feat-icon"), (r"^class/", "class-icon"), (r"^subclass/", "subclass-icon"), (r"^", "plutonium-icon")]),
    (DATA, r"modules\tokenizer-2\img", "modules/tokenizer-2/img", [(r"^masks/", "token-mask"), (r"^", "token-frame")]),
    (DATA, "tokenizer", "tokenizer", [(r"^npc-avatars|^pc-avatars", "avatar-campaign"),
        (r"^npc-images|^pc-images|^pasted", "portrait-campaign")]),
    (DATA, r"worlds\curse-of-strahd\assets", "worlds/curse-of-strahd/assets", [(r"^creatures/|^players/", "portrait-campaign"),
        (r"^macro-icons/", "macro-icon"), (r"^handouts/", "handout"), (r"^scenes/|^maps/|^backgrounds/", "scene"), (r"^", "world-asset")]),
    (DATA, r"worlds\curse-of-strahd\obsidian-assets\images", "worlds/curse-of-strahd/obsidian-assets/images", [(r"^", "portrait-campaign")]),
    (DATA, r"modules\cosrl-escape-from-death-house\assets", "modules/cosrl-escape-from-death-house/assets",
        [(r"^actors/", "portrait-campaign"), (r"^items/", "item-icon-campaign"), (r"^", "world-asset")]),
]
SKIP_FOLDERS = {"_cache", "_masks", "masks"}
STOP = {"webp", "png", "jpg", "jpeg", "svg", "gif", "img", "icons", "icon", "assets", "tokens", "token", "media"}


def words(text):
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return [w for w in re.split(r"[^a-zA-Z]+", text.lower()) if len(w) > 1 and w not in STOP]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.tsv")
    rows = []
    for root, sub, prefix, rules in SOURCES:
        base = os.path.join(root, sub)
        for dirpath, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]
            for f in files:
                if os.path.splitext(f)[1].lower() not in EXT:
                    continue
                rel = os.path.relpath(os.path.join(dirpath, f), base).replace("\\", "/")
                kind = next((k for rx, k in rules if re.search(rx, rel.lower())), None)
                if kind is None:
                    continue
                kw = []
                for part in rel.split("/"):
                    for w in words(os.path.splitext(part)[0]):
                        if w not in kw:
                            kw.append(w)
                rows.append((f"{prefix}/{rel}", kind, " ".join(kw)))
    rows.sort()
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("path\tkind\tkeywords\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    print(f"{len(rows)} images -> {out} ({os.path.getsize(out)//1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
