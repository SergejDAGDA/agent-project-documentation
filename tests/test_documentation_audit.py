import importlib.util
import tempfile
import subprocess
import sys
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

    def test_project_knowledge_subtree_is_audited_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Project\n", encoding="utf-8")
            knowledge = root / "docs" / "project-knowledge" / "reusable"
            knowledge.mkdir(parents=True)
            (knowledge / "contract.md").write_text(
                "# Contract\n\n[Missing](missing.md)\n", encoding="utf-8"
            )
            errors, _ = module.audit(root)
            self.assertTrue(any("docs/project-knowledge/reusable/contract.md" in e for e in errors))

    def test_project_knowledge_missing_capability_index_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Project\n", encoding="utf-8")
            capabilities = root / "docs" / "project-knowledge" / "functionality"
            capabilities.mkdir(parents=True)
            (capabilities / "feature.md").write_text("# Feature\n", encoding="utf-8")
            errors, warnings = module.audit(root)
            self.assertEqual(errors, [])
            self.assertTrue(any("docs/project-knowledge/CAPABILITIES.md" in w for w in warnings))

    def test_external_export_requires_all_markdown_to_check_nested_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Export\n", encoding="utf-8")
            nested = root / "reusable-knowledge" / "contracts"
            nested.mkdir(parents=True)
            (nested / "broken.md").write_text("# Reuse\n\n[Missing](nothing.md)\n", encoding="utf-8")
            normal_errors, _ = module.audit(root)
            all_errors, _ = module.audit(root, all_markdown=True)
            self.assertEqual(normal_errors, [])
            self.assertTrue(any("reusable-knowledge/contracts/broken.md" in e for e in all_errors))

    def test_git_whitespace_check_catches_extra_blank_line_at_eof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Demo\n")
            target = root / "docs" / "project-knowledge" / "CAPABILITIES.md"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"# Capabilities\n\nText\n\n")
            ordinary_errors, _ = module.audit(root)
            checked_errors, _ = module.audit(root, check_git_whitespace=True)
            self.assertEqual(ordinary_errors, [])
            self.assertTrue(any("extra blank line at EOF" in x for x in checked_errors))

    def test_git_whitespace_check_catches_trailing_spaces_and_missing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Demo\n")
            doc = root / "docs" / "project-knowledge" / "README.md"
            doc.parent.mkdir(parents=True)
            doc.write_bytes(b"# Knowledge\nBad line  \nLast line")
            errors, _ = module.audit(root, check_git_whitespace=True)
            self.assertTrue(any("trailing whitespace" in x for x in errors))
            self.assertTrue(any("missing final newline" in x for x in errors))

    def test_git_whitespace_check_accepts_clean_crlf_without_reformatting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Demo\r\n")
            doc = root / "docs" / "project-knowledge" / "README.md"
            doc.parent.mkdir(parents=True)
            doc.write_bytes(b"# Knowledge\r\n\r\nBody\r\n")
            errors, warnings = module.audit(root, check_git_whitespace=True)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_git_whitespace_check_preserves_default_documentation_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Demo\n")
            memory = root / "docs" / "project-memory"
            memory.mkdir(parents=True)
            (memory / "STATUS.md").write_bytes(b"# Status\n\n")
            errors, _ = module.audit(root, check_git_whitespace=True)
            broad_errors, _ = module.audit(
                root, all_markdown=True, check_git_whitespace=True
            )
            self.assertEqual(errors, [])
            self.assertTrue(any("project-memory/STATUS.md" in x for x in broad_errors))

    def test_cli_git_whitespace_flag_rejects_new_untracked_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Demo\n")
            docs = root / "docs" / "project-knowledge"
            docs.mkdir(parents=True)
            (docs / "README.md").write_bytes(b"# Knowledge\r\n\r\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--check-git-whitespace",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("extra blank line at EOF", result.stdout)

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
