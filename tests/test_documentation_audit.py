import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "project-documentation" / "scripts" / "documentation_audit.py"
spec = importlib.util.spec_from_file_location("documentation_audit", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class DocumentationAuditTests(unittest.TestCase):
    def test_reports_broken_local_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n\n[Missing](docs/missing.md)\n", encoding="utf-8")
            errors, warnings = module.audit(root)
            self.assertTrue(any("broken local link" in value for value in errors))
            self.assertEqual(warnings, [])

    def test_validates_skill_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            skill = root / "skills" / "demo"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
            errors, _ = module.audit(root)
            self.assertTrue(any("missing YAML frontmatter" in value for value in errors))


if __name__ == "__main__":
    unittest.main()
