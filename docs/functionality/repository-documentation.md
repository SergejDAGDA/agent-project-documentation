# Repository Documentation Workflow

## Purpose

Create, audit, update, or extract documentation from a source repository while preserving enough knowledge for maintenance and later reuse.

## Status and evidence

Status: verified

Primary behavior is defined in `skills/project-documentation/SKILL.md` and supporting references.

Structural helpers are covered by unit tests in `tests/`.

## Functional contract

### Inputs

- a source repository or project directory
- repository-local instructions when present
- existing documentation when present
- source code, tests, configuration, schemas, manifests, and related project evidence
- a user intent such as initial documentation, audit, update, release check, presentation work, or knowledge extraction

### Outputs

Depending on repository needs and requested mode:

- updated or created `README.md`
- capability index
- functional capability documents
- architecture documentation
- development documentation
- technical reference documentation
- reuse notes
- audit findings
- completion evidence describing verified and unresolved areas

### Modes

The skill defines `init`, `audit`, `update`, `presentation`, `internal`, `release`, `extract`, and `skill-docs` workflows.

Mode selection is intent-driven rather than tied to a required command syntax.

### Capability discovery

The workflow groups meaningful behavior into capabilities instead of treating every source file or framework component as a separate feature.

Capabilities can be marked `verified`, `partial`, or `unverified` based on current repository evidence.

`unverified` behavior must not be presented as implemented.

### Adaptive structure

The workflow creates only documentation that fits the repository.

For example, a project with no API should not receive empty API documentation solely because a template contains such a file.

### Update behavior

When documentation exists, the workflow should preserve deliberate authored content and update the smallest affected documentation surface.

### Failure and uncertainty behavior

When code, tests, existing docs, or configuration conflict, the workflow reports the disagreement instead of silently converting one version into fact.

Unknown historical rationale must remain unknown unless supported by repository evidence.

## Current implementation

### Skill entrypoint

`skills/project-documentation/SKILL.md`

Defines purpose, modes, discovery, capability analysis, output rules, verification, update safety, quality gates, and completion evidence.

### Supporting references

- `documentation-model.md` defines presentation and internal documentation levels
- `repository-analysis.md` defines broad-to-narrow repository discovery
- `feature-documentation.md` defines capability documentation and reuse notes
- `quality-gates.md` defines acceptance checks
- `skill-profile.md` defines Agent Skill and plugin specialization

### Deterministic helpers

`repository_inventory.py` builds a compact repository inventory.

`documentation_audit.py` performs lightweight Markdown and skill-structure checks.

The helpers do not generate project prose and do not replace agent reasoning.

## Reuse notes

The core reusable idea is the separation of three concerns:

1. source-grounded capability discovery
2. functional contract independent from implementation
3. current implementation map with explicit reuse boundaries

A future implementation can replace the helper scripts, agent platform, or packaging while preserving this contract.

Do not copy platform-specific plugin manifests into environments that use different extension formats.

## Known limitations

The deterministic helpers intentionally perform structural checks only. They do not parse arbitrary programming languages deeply and cannot independently prove semantic documentation correctness.
