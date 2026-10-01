# Project Documentation

[Русская версия](README.ru.md)

A reusable Agent Skill for turning source repositories into structured, maintainable, and reusable project knowledge.

Repository name: `agent-project-documentation`

Installed Agent Skill name: `project-documentation`

Invoke it as: `$project-documentation`

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
- plan-versus-implementation reconciliation
- continuation audits before further development
- detection of accidental legacy or project-specific coupling
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
|   |-- reuse notes
|   `-- optional evolution traceability
|
|-- Local diagnostics
|   `-- .project-documentation/
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
- evidence provenance and temporal identity separation when claims cross repository, runtime, or history boundaries
- documentation audit
- targeted documentation updates after code changes
- release documentation checks
- Agent Skill and plugin documentation profile
- plan-versus-implementation reconciliation for internal traceability
- continuation analysis for development residue and incomplete transitions
- project contamination analysis for legacy examples and project-specific data
- safe redaction of credential-like diagnostic signals
- lightweight deterministic repository inventory, Markdown checks, and repository diagnostics

## Safe default behavior

If the request does not name a mode or clearly request file changes, the skill starts with repository discovery plus a read-only audit.

Finding stale documentation does not automatically authorize an `update`.

Project-memory and coordination artifacts are recognized by purpose as well as directory. Strong signals include filenames such as `*HANDOFF*.md` and `*CHECKPOINT*.md`, exact files such as `STATUS.md`, `DECISIONS.md`, and `SESSION_LOG.md`, primary headings that identify a handoff/checkpoint/status/log, and clearly identified project-memory directories.

Those artifacts can be read as evidence when repository-local instructions require them or when they materially help establish current context, but ordinary documentation maintenance does not automatically rewrite them. Conflicts are reported under `Out-of-scope coordination findings` unless their maintenance is explicitly included in the request.

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

reconcile
  Compare accepted project intent with current implementation

continuation
  Identify development residue that deserves review before more work

contamination
  Detect accidental coupling to previous projects, users, environments, or examples
```

## Prompt examples

### General first pass

Use this when you want the skill to inspect an existing repository without assuming that files should be changed.

```text
Use $project-documentation on the current repository.
Start with repository discovery and a read-only audit.
Tell me which documentation modes are applicable and what needs attention.
Do not change files unless I explicitly approve an update.
```

### Update documentation after code changes

```text
Use $project-documentation in update mode.
Inspect the current Git diff and implementation changes.
Update only maintained documentation that is actually affected.
Treat handoff, status, decisions, session-log, checkpoint, and project-memory artifacts as separately owned coordination evidence unless I explicitly include their maintenance.
Report out-of-scope coordination findings separately.
```

### Build full internal documentation

```text
Use $project-documentation in internal mode.
Document the current repository as maintainable project knowledge.
Separate functional contracts from implementation details and include reuse notes for meaningful capabilities.
```

### Improve the GitHub presentation

```text
Use $project-documentation in presentation mode.
Audit and improve the GitHub-facing documentation so a new reader can quickly understand what the project is, what it does, how to start, and where deeper documentation lives.
Do not turn the README into an internal architecture dump.
```

### Compare plan with implementation

```text
Use $project-documentation in reconcile mode.
Compare accepted project requirements, MVP documents, and recorded decisions with the current implementation.
Classify the delta and keep unknown reasons explicitly unknown.
Keep the result internal rather than adding it to the public README.
```

### Inspect the project before continuing development

```text
Use $project-documentation in continuation mode.
Inspect the repository for abandoned, superseded, stale, orphaned, compatibility, or incomplete-migration residue.
Treat every finding as a review candidate, not as permission to delete code.
```

### Check for legacy-project contamination

```text
Use $project-documentation in contamination mode.
Look for accidental coupling to old projects, example data, user-specific paths, customer-specific values, or environment-specific assumptions.
Do not reproduce credential-like or private literal values in the report.
```

### Extract reusable functionality

```text
Use $project-documentation in extract mode.
Identify capabilities that can be reused in another project.
For each useful capability, separate the functional contract, current implementation, dependencies, assumptions, limitations, and reuse notes.
```

### Document another Agent Skill

```text
Use $project-documentation in skill-docs mode.
Document this Agent Skill repository for users and maintainers.
Cover its trigger contract, workflows, references, scripts, packaging, portability boundaries, and maintenance contract.
```

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
      evidence-semantics.md
      feature-documentation.md
      quality-gates.md
      repository-analysis.md
      skill-profile.md
      evolution-reconciliation.md
      continuation-audit.md
      contamination-audit.md
      diagnostic-output.md
    scripts/
      repository_inventory.py
      documentation_audit.py
      repository_diagnostics.py

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

Create a compact repository inventory when discovery needs it:

```bash
python skills/project-documentation/scripts/repository_inventory.py --root . --format markdown
```

Run lightweight Markdown and skill-structure checks on maintained documentation surfaces:

```bash
python skills/project-documentation/scripts/documentation_audit.py --root .
```

The default audit excludes Markdown used as data and separately owned coordination artifacts such as handoffs and project-memory files. Audit every Markdown file only when that broader scope is intentional:

```bash
python skills/project-documentation/scripts/documentation_audit.py --root . --all-markdown
```

Collect conservative residue and contamination signals only for continuation, contamination, explicitly requested broad diagnostics, or a narrowly justified investigation:

```bash
python skills/project-documentation/scripts/repository_diagnostics.py --root . --format markdown
```

Known legacy or project-specific names can be supplied with repeated `--marker` arguments. Diagnostic output should normally stay under `.project-documentation/`, which is ignored by version control.

`repository_diagnostics.py` is not a routine quality gate for normal `init`, `audit`, `update`, `presentation`, or `release` work.

These scripts assist the agent. They do not replace source inspection, factual verification, language-specific static analysis, secret scanning, or security review.

## Design principles

### Evidence before prose

Important documentation claims should be supported by evidence appropriate to their claim domain. When provenance, confidence, time, or revision identity materially affects the claim, keep those dimensions explicit rather than implying more verification than occurred.

### Behavior before implementation

Reusable functionality is documented as a functional contract before describing its current framework-specific implementation.

### Adaptive output

The repository determines the documentation structure, not a fixed template.

### Minimal destructive editing

Existing deliberate documentation is preserved when possible. Update mode should modify only the knowledge affected by the implementation change.

### Coordination stays separately owned

Handoffs, checkpoints, project status, decisions, session logs, and project-memory artifacts may inform the audit but remain outside ordinary documentation mutation unless explicitly included.

### Reuse without cargo culting

Reuse notes identify portable behavior, boundaries, assumptions, dependencies, and limitations instead of recommending blind source copying.

## Status

Version 0.2.3 clarifies external evidence provenance, separates verification confidence from temporal role, and prevents materially different repository, implementation, release/runtime, and documentation identities from being collapsed into one ambiguous current revision.

## License

MIT.
