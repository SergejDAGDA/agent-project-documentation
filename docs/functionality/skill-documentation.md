# Agent Skill Documentation

## Purpose

Document an Agent Skill or plugin repository without requiring the maintainer to manually restate the skill's design, resources, and workflows.

## Status and evidence

Status: verified

The workflow is defined in the `skill-docs` mode in `skills/project-documentation/SKILL.md` and detailed in `skills/project-documentation/references/skill-profile.md`.

## Functional contract

### Detection

Skill or plugin specialization becomes relevant when repository evidence includes structures such as `SKILL.md`, `skills/<name>/SKILL.md`, agent metadata, plugin manifests, MCP definitions, commands, hooks, or agents.

### Public view

The generated documentation should explain applicable items such as:

- what problem the skill solves
- when it should trigger
- non-goals
- supported workflows
- required capabilities
- installation or distribution model
- evidenced platform compatibility
- typical use
- limitations

### Internal view

The generated documentation should explain applicable items such as:

- trigger contract
- modes
- workflow phases
- stop conditions
- quality gates
- reference routing
- script behavior
- assets
- packaging
- portability boundaries
- maintenance contract

### Portability rule

Platform packaging is documented separately from the portable skill methodology.

Compatibility is not inferred from similar file names alone.

## Current implementation

The portable core is located under `skills/project-documentation/`.

Codex packaging currently uses:

- root `plugin.json`
- `.agents/plugins/marketplace.json`

Claude Code packaging currently uses:

- `.claude-plugin/plugin.json`
- the same root `skills/` directory

## Reuse notes

The skill-documentation profile can be used on a single skill, a multi-skill plugin, or a repository that contains skills alongside ordinary application code.

The methodology remains usable even if future agent platforms change manifest or marketplace formats because the platform-neutral contract is separated from packaging.
