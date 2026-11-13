"""Build a Foundry v14 RollTable from a compact JSON spec. See SKILL.md."""

import argparse
import json
from pathlib import Path
import re
import secrets
import string


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ICON = "icons/svg/d20-grey.svg"
TERM = r"(?:\d*[dD]\d+|\d+)"


def text(value, label, nonempty=False):
    if not isinstance(value, str) or (nonempty and not value.strip()):
        raise ValueError(f"{label} must be a {'nonempty ' if nonempty else ''}string")
    return value


def integer(value, label, minimum=None):
    if type(value) is not int or (minimum is not None and value < minimum):
        suffix = f" >= {minimum}" if minimum is not None else ""
        raise ValueError(f"{label} must be an integer{suffix}")
    return value


def boolean(value, label):
    if type(value) is not bool:
        raise ValueError(f"{label} must be true or false")
    return value


def check_keys(value, allowed, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    unknown = value.keys() - allowed
    if unknown:
        raise ValueError(f"{label}: unknown fields: {', '.join(sorted(unknown))}")


def formula_bounds(formula):
    """Bounds for sums/differences of ordinary dice and integer constants."""
    compact = re.sub(r"\s+", "", text(formula, "formula", nonempty=True))
    if not re.fullmatch(rf"[+-]?{TERM}(?:[+-]{TERM})*", compact):
        raise ValueError("formula supports only ordinary dice and integer +/- terms "
                         "(e.g. d12 + d8 or 1d20 + 3); resolve skill modifiers to numbers")
    low = high = 0
    for sign, term in re.findall(rf"([+-]?)({TERM})", compact):
        if "d" in term.lower():
            count, sides = term.lower().split("d")
            count = integer(int(count or "1"), "dice count", 1)
            sides = integer(int(sides), "die sides", 1)
            term_low, term_high = count, count * sides
        else:
            term_low = term_high = int(term)
        if sign == "-":
            low, high = low - term_high, high - term_low
        else:
            low, high = low + term_low, high + term_high
    return low, high


def result_id():
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))


def build_table(spec):
    check_keys(spec, {"name", "description", "img", "formula", "results",
                      "replacement", "displayRoll", "allow_overlaps"}, "table")
    name = text(spec.get("name"), "name", nonempty=True)
    entries = spec.get("results")
    if not isinstance(entries, list) or not entries:
        raise ValueError("results must be a nonempty array")
    entries = [{"description": entry} if isinstance(entry, str) else entry for entry in entries]
    for index, entry in enumerate(entries, 1):
        check_keys(entry, {"name", "description", "img", "range", "weight"}, f"result {index}")
    explicit = any("range" in entry for entry in entries)
    if explicit and not all("range" in entry for entry in entries):
        raise ValueError("results must either all specify range or all omit it")

    results = []
    cursor = 1
    for index, entry in enumerate(entries, 1):
        label = f"result {index}"
        weight = integer(entry.get("weight", 1), f"{label} weight", 1)
        if explicit:
            span = entry["range"]
            if not isinstance(span, list) or len(span) != 2:
                raise ValueError(f"{label} range must be [minimum, maximum]")
            low, high = [integer(n, f"{label} range endpoint") for n in span]
            if low > high:
                raise ValueError(f"{label} range minimum exceeds maximum")
        else:
            low, high = cursor, cursor + weight - 1
            cursor = high + 1
        result_name = text(entry.get("name", ""), f"{label} name")
        description = text(entry.get("description", ""), f"{label} description")
        if not result_name.strip() and not description.strip():
            raise ValueError(f"{label} needs a name or description")
        results.append({
            "_id": result_id(),
            "type": "text",
            "name": result_name,
            "description": description,
            "img": text(entry.get("img", DEFAULT_ICON), f"{label} img", nonempty=True),
            "weight": weight,
            "range": [low, high],
            "drawn": False,
            "documentUuid": None,
            "flags": {},
        })

    spans = sorted(result["range"] for result in results)
    formula = spec.get("formula")
    if formula is None:
        if spans[0][0] != 1:
            raise ValueError("formula is required when ranges do not start at 1")
        formula = f"1d{max(high for _, high in spans)}"
    minimum, maximum = formula_bounds(formula)
    allow_overlaps = boolean(spec.get("allow_overlaps", False), "allow_overlaps")
    covered = minimum - 1
    for low, high in spans:
        if low < minimum or high > maximum:
            raise ValueError(f"range [{low}, {high}] is outside formula bounds [{minimum}, {maximum}]")
        if low > covered + 1:
            raise ValueError(f"ranges leave a gap at {covered + 1}")
        if low <= covered and not allow_overlaps:
            raise ValueError(f"ranges overlap at {low}; set allow_overlaps only if intentional")
        covered = max(covered, high)
    if covered != maximum:
        raise ValueError(f"ranges leave a gap at {covered + 1}")

    return {
        "name": name,
        "description": text(spec.get("description", ""), "description"),
        "img": text(spec.get("img", DEFAULT_ICON), "img", nonempty=True),
        "formula": formula,
        "results": results,
        "replacement": boolean(spec.get("replacement", True), "replacement"),
        "displayRoll": boolean(spec.get("displayRoll", True), "displayRoll"),
        "folder": None,
        "ownership": {"default": 0},
        "flags": {},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="compact table spec JSON")
    parser.add_argument("output", nargs="?", type=Path, help="optional destination JSON")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8-sig"))
        table = build_table(spec)
        slug = re.sub(r"[^a-z0-9]+", "-", table["name"].lower()).strip("-") or "table"
        output = args.output or ROOT / "assets" / "rollable_tables" / f"fvtt-RollTable-{slug}.json"
        if output.resolve() == args.spec.resolve():
            raise ValueError("output must not overwrite the input spec")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w" if args.force else "x", encoding="utf-8") as handle:
            handle.write(json.dumps(table, ensure_ascii=False, indent=2) + "\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"error: {error}\n")
    print(output.resolve())


if __name__ == "__main__":
    main()
