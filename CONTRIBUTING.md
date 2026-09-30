# Contributing

Changes should preserve the skill's platform-neutral core and avoid project-specific examples in normative instructions.

## Principles

- Keep `SKILL.md` focused on workflow and constraints.
- Put conditional detail in `references/`.
- Use scripts only where deterministic processing materially improves reliability.
- Do not add fixed documentation files that are irrelevant to many repository types.
- Keep functional behavior separate from current implementation details.
- Do not introduce examples tied to a private or unrelated legacy project.
- Keep Codex and Claude Code packaging version-consistent with the portable skill core.

## Before publishing

Run:

```bash
python -m unittest discover -s tests -v
python skills/project-documentation/scripts/repository_inventory.py --root . --format markdown
python skills/project-documentation/scripts/documentation_audit.py --root .
```

Update `CHANGELOG.md` and both plugin manifests when the public version changes.
