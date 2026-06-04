import csv
import importlib.util
import json
import pathlib
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "generate-roadmap.py"
SOURCE_PATH = REPO_ROOT / "roadmap" / "roadmap.yaml"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_roadmap", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RoadmapGeneratorTest(unittest.TestCase):
    def test_loads_items_with_unique_ids_and_sorted_order(self):
        generator = load_generator()
        roadmap = generator.load_roadmap(SOURCE_PATH)
        items = generator.sorted_items(roadmap)
        ids = [item["id"] for item in items]

        self.assertGreaterEqual(len(items), 20)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([item["order"] for item in items], sorted(item["order"] for item in items))
        self.assertIn("obsidian-knowledge-layer", ids)
        self.assertIn("ray-hermes-health-monitor", ids)

    def test_generation_outputs_expected_files(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = pathlib.Path(tmp)
            written = generator.generate(SOURCE_PATH, out_dir)

            self.assertTrue((out_dir / "roadmap.json").exists())
            self.assertTrue((out_dir / "roadmap.csv").exists())
            self.assertTrue((out_dir / "roadmap.md").exists())
            self.assertTrue((out_dir / "index.html").exists())
            self.assertEqual({p.name for p in written}, {"roadmap.json", "roadmap.csv", "roadmap.md", "index.html"})

            data = json.loads((out_dir / "roadmap.json").read_text())
            self.assertIn("items", data)
            self.assertGreaterEqual(len(data["items"]), 20)

            with (out_dir / "roadmap.csv").open() as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), len(data["items"]))
            self.assertIn("next_action", rows[0])

            html = (out_dir / "index.html").read_text()
            self.assertIn("Ned End-to-End Roadmap", html)
            self.assertIn("ROADMAP_DATA", html)
            self.assertIn("Copy edited YAML", html)


if __name__ == "__main__":
    unittest.main()
