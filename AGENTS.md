# Repository Guidance

This repository contains one portable Agent Skill named `project-documentation` plus platform-specific packaging around that shared core.

Canonical skill instructions:

`skills/project-documentation/SKILL.md`

Detailed skill references:

`skills/project-documentation/references/`

Internal project documentation:

`docs/`

Keep Codex and Claude Code packaging version-consistent. Do not duplicate the skill body into platform-specific directories.

When changing public behavior, update `CHANGELOG.md` and applicable manifests together.
