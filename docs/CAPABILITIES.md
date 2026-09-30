# Capabilities

## Repository documentation

Status: verified

Creates and maintains a two-level repository documentation model with a concise presentation layer and detailed internal project knowledge.

Canonical documentation: `functionality/repository-documentation.md`

## Reusable knowledge extraction

Status: verified

Separates functional contracts from current implementation details and records reuse boundaries, dependencies, assumptions, and limitations.

Canonical documentation: `functionality/repository-documentation.md`

## Documentation audit and update

Status: verified

Supports audit, targeted update, and release documentation workflows with source-grounding and maintenance-safety rules.

Canonical documentation: `functionality/repository-documentation.md`

## Agent Skill documentation

Status: verified

Documents Agent Skills and plugin repositories at both public and internal levels, including trigger contract, workflows, resources, packaging, and portability boundaries.

Canonical documentation: `functionality/skill-documentation.md`

## Deterministic repository inventory

Status: verified

Provides a Python helper that inventories repository shape, common source languages, documentation, manifests, tests, and Agent Skill files while excluding common dependency and build trees.

Implementation: `../skills/project-documentation/scripts/repository_inventory.py`

## Documentation structure audit

Status: verified

Provides a Python helper that checks Markdown local links, root README presence, capability index expectations, and basic Agent Skill frontmatter structure.

Implementation: `../skills/project-documentation/scripts/documentation_audit.py`
