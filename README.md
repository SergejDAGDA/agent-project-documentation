# Project Documentation

A reusable Agent Skill for turning source repositories into structured, maintainable, and reusable project knowledge.

The skill creates and maintains two documentation levels:

1. A presentation layer for people evaluating or starting with the project.
2. An internal knowledge layer for developers and agents who need functional, architectural, implementation, and reuse details.

It can also document Agent Skills and plugin repositories themselves.

## Why this exists

A README is not enough to preserve a project's knowledge.

Code explains implementation, but usually does not preserve the full functional contract, intended behavior, reusable boundaries, important constraints, or a concise map of capabilities.

`project-documentation` extracts that knowledge from the repository while keeping product behavior separate from framework-specific implementation.

The result is useful for:

- GitHub-ready project presentation
- onboarding
- maintenance
- documentation audits
- release preparation
- AI-assisted development
- knowledge transfer
- reuse of capabilities in later projects
- documentation of Agent Skills and plugins

## Documentation model

```text
Repository
|
|-- Presentation layer
|   `-- README.md and applicable public guides
|
|-- Internal knowledge
|   |-- capability index
|   |-- functional contracts
|   |-- architecture
|   |-- implementation reference
|   |-- development and operations
|   `-- reuse notes
|
`-- Optional agent routing
    `-- AGENTS.md or CLAUDE.md pointers to canonical docs
```

The generated structure is adaptive. The skill does not create empty API, database, deployment, or other documents when the repository does not need them.

## Core capabilities

- repository discovery and classification
- capability discovery
- presentation documentation
- detailed internal documentation
- functional contract extraction
- implementation mapping
- reusable knowledge extraction
- verified, partial, and unverified evidence states
- documentation audit
- targeted documentation updates after code changes
- release documentation checks
- Agent Skill and plugin documentation profile
- lightweight deterministic repository inventory and Markdown checks

## Modes

The skill supports these workflows:

```text
init
  First documentation pass for an existing repository

audit
  Inspect documentation quality and code-to-doc consistency

update
  Update only documentation affected by project changes

presentation
  Focus on GitHub-facing and reader-facing documentation

internal
  Focus on deep functional and technical documentation

release
  Validate repository documentation before release

extract
  Extract reusable capability knowledge for another project

skill-docs
  Document an Agent Skill or plugin repository
```

Modes are selected from the user's request. They are not tied to a command syntax.

## Agent Skill and plugin documentation

When the target contains Agent Skills, the skill analyzes applicable `SKILL.md` files and their supporting resources.

It can document:

- trigger contract
- workflows and modes
- references
- scripts
- assets
- agent metadata
- plugin manifests
- MCP assumptions
- platform-specific packaging
- portability boundaries
- maintenance contract

The same portable skill core can be packaged for more than one compatible agent environment without maintaining duplicate instruction bodies.

## Repository structure

```text
skills/
  project-documentation/
    SKILL.md
    agents/
      openai.yaml
    references/
      documentation-model.md
      feature-documentation.md
      quality-gates.md
      repository-analysis.md
      skill-profile.md
    scripts/
      repository_inventory.py
      documentation_audit.py

plugin.json
.claude-plugin/
  plugin.json
```

## Codex packaging

The repository includes a root `plugin.json` and exposes the portable skill from `skills/`.

The skill instructions themselves do not depend on Codex-specific project examples.

## Claude Code packaging

The repository also includes `.claude-plugin/plugin.json` and keeps the same `skills/` directory at plugin root, which allows the same skill body to be used without maintaining a second copy.

## Deterministic helpers

Create a compact repository inventory:

```bash
python skills/project-documentation/scripts/repository_inventory.py --root . --format markdown
```

Run lightweight Markdown and skill-structure checks:

```bash
python skills/project-documentation/scripts/documentation_audit.py --root .
```

These scripts assist the agent. They do not replace source inspection or factual verification.

## Design principles

### Evidence before prose

Important documentation claims should be supported by current repository evidence.

### Behavior before implementation

Reusable functionality is documented as a functional contract before describing its current framework-specific implementation.

### Adaptive output

The repository determines the documentation structure, not a fixed template.

### Minimal destructive editing

Existing deliberate documentation is preserved when possible. Update mode should modify only the knowledge affected by the implementation change.

### Reuse without cargo culting

Reuse notes identify portable behavior, boundaries, assumptions, dependencies, and limitations instead of recommending blind source copying.

## Status

Version 0.1.0 is the first working implementation of the skill architecture and deterministic helper scripts.

## License

MIT.
