# Changelog

## 0.2.1

Behavioral routing and audit-scope refinement release.

- Default ambiguous invocations to repository discovery plus read-only `audit`
- Prevent stale findings from silently escalating an ambiguous request into `update`
- Clarify repository name `agent-project-documentation` versus installed skill name `project-documentation`
- Add project-memory ownership boundaries for handoff, status, decision, and session-log artifacts
- Report project-memory conflicts as out-of-scope inconsistencies unless maintenance is explicitly included
- Add bundled-helper discipline and forbid routine or repeated `--help` probing
- Limit the default Markdown audit to documentation surfaces
- Add `--all-markdown` for intentionally auditing Markdown used as data or test material
- Add regression tests for documentation-surface filtering
- Add practical usage prompts to both README languages

## 0.2.0

Internal evolution and continuation analysis release.

- Added `reconcile` mode for plan-versus-implementation traceability
- Added `continuation` mode for abandoned, superseded, stale, compatibility, and incomplete-migration residue
- Added `contamination` mode for project-specific, user-specific, environment-specific, and example-derived coupling
- Added `legacy-example-contamination` guidance
- Added local `.project-documentation/` diagnostic output contract and default Git ignore rule
- Added safe handling rules that prevent credential-like values from being copied into reports
- Added `repository_diagnostics.py` with redacted heuristic signals and explicit known-context markers
- Added tests for diagnostic redaction, project markers, user-specific paths, and dependency-tree exclusion
- Added internal documentation for project evolution and diagnostic workflows
- Kept public presentation separate from internal reconciliation and diagnostics

## 0.1.0

Initial working release.

- Added portable `project-documentation` Agent Skill
- Added two-level documentation model
- Added adaptive repository analysis workflow
- Added capability discovery and evidence states
- Added reusable functional contract and implementation separation
- Added `init`, `audit`, `update`, `presentation`, `internal`, `release`, `extract`, and `skill-docs` modes
- Added Agent Skill and plugin documentation profile
- Added repository inventory helper
- Added Markdown documentation audit helper
- Added Codex and Claude Code plugin packaging around one shared skill core
