import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "project-documentation" / "scripts" / "repository_diagnostics.py"
spec = importlib.util.spec_from_file_location("repository_diagnostics", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class RepositoryDiagnosticsTests(unittest.TestCase):
    def test_redacts_secret_literal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.py").write_text('api_key = "super-secret-value"\n', encoding="utf-8")
            data = module.collect(root)
            secret = [item for item in data["findings"] if item["type"] == "potential-secret"]
            self.assertEqual(len(secret), 1)
            serialized = str(secret[0])
            self.assertNotIn("super-secret-value", serialized)

    def test_detects_user_path_and_known_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "settings.ts").write_text(
                'const root = "/home/alice/old-project"\nconst source = "LegacyCustomer42"\n',
                encoding="utf-8",
            )
            data = module.collect(root, ["LegacyCustomer42"])
            kinds = [item["type"] for item in data["findings"]]
            self.assertIn("user-specific-path", kinds)
            self.assertIn("known-context-marker", kinds)

    def test_excludes_generated_dependency_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dep = root / "node_modules" / "pkg"
            dep.mkdir(parents=True)
            (dep / "config.js").write_text('password = "should-not-scan"\n', encoding="utf-8")
            data = module.collect(root)
            self.assertEqual(data["finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
