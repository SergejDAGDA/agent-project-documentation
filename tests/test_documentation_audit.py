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

    def test_ignores_markdown_data_outside_documentation_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            qa = root / "qa"
            qa.mkdir()
            (qa / "result.md").write_text("plain fixture payload without heading\n", encoding="utf-8")
            errors, warnings = module.audit(root)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_all_markdown_opt_in_includes_non_documentation_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            payload = root / "samples"
            payload.mkdir()
            (payload / "result.md").write_text("plain payload without heading\n", encoding="utf-8")
            _, warnings = module.audit(root, all_markdown=True)
            self.assertTrue(any("samples/result.md" in value for value in warnings))

    def test_ignores_handoff_outside_project_memory_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            docs = root / "docs"
            docs.mkdir()
            (docs / "TESTSERVER_DEPLOYMENT_HANDOFF.md").write_text(
                "# Testserver deployment handoff\n\n[Missing](missing.md)\n",
                encoding="utf-8",
            )
            errors, warnings = module.audit(root)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_all_markdown_can_include_handoff_when_explicitly_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            docs = root / "docs"
            docs.mkdir()
            (docs / "TESTSERVER_DEPLOYMENT_HANDOFF.md").write_text(
                "# Testserver deployment handoff\n\n[Missing](missing.md)\n",
                encoding="utf-8",
            )
            errors, _ = module.audit(root, all_markdown=True)
            self.assertTrue(any("TESTSERVER_DEPLOYMENT_HANDOFF.md" in value for value in errors))

    def test_primary_heading_can_mark_coordination_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            docs = root / "docs"
            docs.mkdir()
            (docs / "deployment-notes.md").write_text(
                "# Deployment Handoff\n\n[Missing](missing.md)\n",
                encoding="utf-8",
            )
            errors, warnings = module.audit(root)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_project_memory_directory_is_outside_default_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            memory = root / "docs" / "project-memory"
            memory.mkdir(parents=True)
            (memory / "STATUS.md").write_text(
                "# Status\n\n[Missing](missing.md)\n",
                encoding="utf-8",
            )
            errors, warnings = module.audit(root)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
