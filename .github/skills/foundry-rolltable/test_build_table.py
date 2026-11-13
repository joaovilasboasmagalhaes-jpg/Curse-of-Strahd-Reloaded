import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from build_table import ROOT, build_table


class TableTests(unittest.TestCase):
    def test_weighted_results_and_clean_import_shape(self):
        table = build_table({
            "name": "Weighted",
            "replacement": False,
            "displayRoll": False,
            "results": ["One", {"name": "Two", "description": "<p>[[/r 1d6]]</p>", "weight": 3}],
        })
        self.assertEqual(table["formula"], "1d4")
        self.assertEqual([r["range"] for r in table["results"]], [[1, 1], [2, 4]])
        self.assertEqual(table["results"][1]["description"], "<p>[[/r 1d6]]</p>")
        self.assertFalse(table["replacement"])
        self.assertFalse(table["displayRoll"])
        self.assertIsNone(table["folder"])
        self.assertNotIn("_stats", table)
        ids = [r["_id"] for r in table["results"]]
        self.assertEqual(len(set(ids)), 2)
        for result in table["results"]:
            self.assertRegex(result["_id"], r"^[A-Za-z0-9]{16}$")
            self.assertEqual(result["type"], "text")
            self.assertFalse(result["drawn"])
            self.assertIsNone(result["documentUuid"])

    def test_reference_ranges_and_descriptions_survive_conversion(self):
        references = (
            "fvtt-RollTable-nighttime-random-encounters-in-barovia-7qWQ39iTOdPen72X.json",
            "fvtt-RollTable-urn-of-soul-catching-FvwRFlpCvP1RiRdB.json",
        )
        for filename in references:
            path = ROOT / "assets" / "rollable_tables" / filename
            with self.subTest(path=path.name):
                source = json.loads(path.read_text(encoding="utf-8"))
                spec = {
                    "name": source["name"],
                    "formula": source["formula"],
                    "results": [
                        {key: r[key] for key in ("name", "description", "img", "weight", "range")}
                        for r in source["results"]
                    ],
                }
                if "Wisdom (Religion)" in spec["formula"]:
                    with self.assertRaisesRegex(ValueError, "resolve skill modifiers"):
                        build_table(spec)
                    spec["formula"] = "1d20"
                    with self.assertRaisesRegex(ValueError, "overlap"):
                        build_table(spec)
                    spec["allow_overlaps"] = True
                table = build_table(spec)
                for original, result in zip(source["results"], table["results"]):
                    for key in ("name", "description", "img", "weight", "range"):
                        self.assertEqual(result[key], original[key])
                    self.assertEqual(result["flags"], {})

    def test_offset_and_negative_dice_bounds(self):
        for formula, span in (("1d20 + 3", [4, 23]), ("1d6 - d4 - 2", [-5, 3])):
            with self.subTest(formula=formula):
                self.assertEqual(build_table({
                    "name": "Offset", "formula": formula,
                    "results": [{"description": "All", "range": span}],
                })["results"][0]["range"], span)

    def test_invalid_specs_are_rejected(self):
        cases = [
            ({"name": ""}, "nonempty"),
            ({"results": []}, "nonempty"),
            ({"results": [""]}, "needs a name or description"),
            ({"results": [{"description": "A", "weight": True}]}, "weight"),
            ({"results": [{"description": "A", "weight": 0}]}, "weight"),
            ({"results": [{"description": "A", "range": [2, 1]}]}, "exceeds"),
            ({"results": [{"description": "A", "range": [1, 1]}, "B"]}, "all specify"),
            ({"formula": "1d3", "results": [
                {"description": "A", "range": [1, 1]},
                {"description": "B", "range": [3, 3]}]}, "gap at 2"),
            ({"formula": "1d3"}, "gap at 2"),
            ({"formula": "1d1", "results": [
                {"description": "A", "range": [1, 2]}]}, "outside formula"),
            ({"formula": "1d0"}, "die sides"),
            ({"formula": "0d6"}, "dice count"),
            ({"formula": "1d20 + @abilities.wis.mod"}, "formula supports"),
            ({"formula": "1d6kh1"}, "formula supports"),
            ({"formula": ""}, "nonempty"),
            ({"replacement": "false"}, "true or false"),
            ({"allow_overlaps": "false"}, "true or false"),
            ({"resuts": ["A"]}, "unknown fields"),
            ({"results": [{"description": "A", "wieght": 2}]}, "unknown fields"),
        ]
        for overrides, message in cases:
            with self.subTest(overrides=overrides):
                spec = {"name": "Invalid", "results": ["A"]}
                spec.update(overrides)
                with self.assertRaisesRegex(ValueError, message):
                    build_table(spec)

    def test_cli_writes_json_and_protects_existing_files(self):
        script = Path(__file__).with_name("build_table.py")
        with tempfile.TemporaryDirectory() as directory:
            spec = Path(directory) / "spec.json"
            output = Path(directory) / "nested" / "table.json"
            spec.write_text(json.dumps({"name": "Example", "results": ["A", "B"]}),
                            encoding="utf-8-sig")
            command = [sys.executable, "-B", str(script), str(spec), str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["formula"], "1d2")
            previous = output.read_bytes()
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("error:", second.stderr)
            self.assertEqual(output.read_bytes(), previous)
            forced = subprocess.run(command + ["--force"], capture_output=True, text=True)
            self.assertEqual(forced.returncode, 0, forced.stderr)
            same_path = subprocess.run(
                [sys.executable, "-B", str(script), str(spec), str(spec), "--force"],
                capture_output=True, text=True,
            )
            self.assertNotEqual(same_path.returncode, 0)
            self.assertIn("must not overwrite", same_path.stderr)


if __name__ == "__main__":
    unittest.main()
