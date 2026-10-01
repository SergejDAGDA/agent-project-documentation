import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills" / "project-documentation" / "SKILL.md"
REFERENCES = ROOT / "skills" / "project-documentation" / "references"
EVIDENCE = REFERENCES / "evidence-semantics.md"
CONTINUATION = REFERENCES / "continuation-audit.md"
DIAGNOSTIC = REFERENCES / "diagnostic-output.md"
PLUGIN = ROOT / "plugin.json"
CLAUDE_PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
CHANGELOG = ROOT / "CHANGELOG.md"
README = ROOT / "README.md"
README_RU = ROOT / "README.ru.md"


class SkillContractTests(unittest.TestCase):
    def test_evidence_semantics_keeps_dimensions_separate(self):
        text = EVIDENCE.read_text(encoding="utf-8")
        self.assertIn("## Evidence provenance", text)
        self.assertIn("## Verification confidence", text)
        self.assertIn("## Temporal role", text)
        self.assertIn("## Revision and state identities", text)
        self.assertIn("## Authority by claim domain", text)
        for provenance in (
            "repository-derived",
            "current-task-external",
            "user-supplied",
            "prior-or-coordination",
        ):
            self.assertIn(f"`{provenance}`", text)
        for value in ("verified", "partial", "unverified"):
            self.assertIn(f"`{value}`", text)
        self.assertIn("`historical` is not a confidence value", text)
        self.assertIn("These labels describe origin or acquisition, not verification confidence", text)

    def test_core_skill_links_evidence_semantics_and_temporal_identity(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/evidence-semantics.md", text)
        self.assertIn("evidence provenance, verification confidence, and temporal role", text)
        self.assertIn("Repository HEAD", text)
        self.assertIn("implementation or source baseline", text)
        self.assertIn("generic `current revision`", text)
        self.assertIn("authoritative source", text)

    def test_continuation_uses_canonical_confidence_vocabulary(self):
        text = CONTINUATION.read_text(encoding="utf-8")
        self.assertIn("## Verification confidence", text)
        for value in ("verified", "partial", "unverified"):
            self.assertIn(f"`{value}`", text)
        self.assertNotIn("Use `confirmed`, `likely`, `suspected`, or `historical`", text)
        self.assertIn("Do not use `historical` as a confidence value", text)

    def test_diagnostic_output_has_independent_optional_evidence_fields(self):
        text = DIAGNOSTIC.read_text(encoding="utf-8")
        for field in (
            "evidence_provenance",
            "verification_confidence",
            "temporal_role",
        ):
            self.assertIn(f"`{field}`", text)
        self.assertIn("Do not require all evidence fields for every finding", text)

    def test_evidence_semantics_is_generic(self):
        text = EVIDENCE.read_text(encoding="utf-8").lower()
        for project_specific_literal in (
            "timeline-tool",
            "current.json",
            "10.0.0.99",
            "legacy-ba80b286",
            "docker",
        ):
            self.assertNotIn(project_specific_literal, text)

    def test_release_version_metadata_is_consistent(self):
        plugin_version = json.loads(PLUGIN.read_text(encoding="utf-8"))["version"]
        claude_version = json.loads(CLAUDE_PLUGIN.read_text(encoding="utf-8"))["version"]
        self.assertEqual(plugin_version, "0.2.3")
        self.assertEqual(claude_version, plugin_version)
        self.assertIn("## 0.2.3", CHANGELOG.read_text(encoding="utf-8"))
        self.assertIn("Version 0.2.3", README.read_text(encoding="utf-8"))
        self.assertIn("Версия 0.2.3", README_RU.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
