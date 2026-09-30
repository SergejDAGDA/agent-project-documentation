import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "project-documentation" / "scripts" / "repository_inventory.py"
spec = importlib.util.spec_from_file_location("repository_inventory", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class RepositoryInventoryTests(unittest.TestCase):
    def test_detects_skill_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skills" / "demo").mkdir(parents=True)
            (root / "skills" / "demo" / "SKILL.md").write_text(
                "---\nname: demo\ndescription: demo\n---\n# Demo\n",
                encoding="utf-8",
            )
            data = module.build_inventory(root)
            self.assertIn("agent-skill", data["repository_types"])
            self.assertEqual(data["skill_manifests"], ["skills/demo/SKILL.md"])

    def test_excludes_dependency_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node_modules" / "pkg").mkdir(parents=True)
            (root / "node_modules" / "pkg" / "index.js").write_text("x", encoding="utf-8")
            (root / "main.py").write_text("print('ok')\n", encoding="utf-8")
            data = module.build_inventory(root)
            self.assertEqual(data["file_count"], 1)
            self.assertEqual(data["languages_by_file_count"], {"Python": 1})


if __name__ == "__main__":
    unittest.main()
