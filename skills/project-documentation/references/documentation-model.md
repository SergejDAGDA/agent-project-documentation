# Documentation Model

## Goal

Use two visible documentation levels and one optional agent-routing level.

## Level 1: Presentation

Primary surface:

- `README.md`

Optional supporting public documents:

- user guide
- installation guide
- contribution guide
- changelog
- security policy
- license

The presentation layer should let a new reader understand the project quickly without studying implementation details.

Recommended README topics when applicable:

1. Project identity and concise description
2. Visual preview or demo reference
3. Current capabilities
4. Typical use cases
5. Quick start
6. Installation
7. Configuration basics
8. Requirements
9. Project status
10. Documentation index
11. Contribution path
12. License

Do not force all sections into every repository.

## Level 2: Internal project knowledge

Recommended adaptive structure:

```text
docs/
  CAPABILITIES.md
  overview/
    PROJECT.md
  functionality/
    <capability>.md
  architecture/
    OVERVIEW.md
    COMPONENTS.md
    DATA_FLOW.md
  development/
    SETUP.md
    BUILD.md
    TESTING.md
    DEPLOYMENT.md
  reference/
    DATA_MODEL.md
    API.md
    CONFIGURATION.md
    DEPENDENCIES.md
  decisions/
    <recorded-decision>.md
  evolution/
    BASELINE.md
    TRACEABILITY.md
    IMPLEMENTATION_REVIEW.md
```

Only create documents with real content.

## Capability index

`docs/CAPABILITIES.md` should be the shortest path to reusable knowledge.

For each meaningful capability, record:

- name
- status such as verified, partial, or unverified
- short purpose
- canonical functionality document
- important implementation area when useful

Do not turn this into a file inventory.

## Agent routing layer

When the project uses `AGENTS.md` or `CLAUDE.md`, these files may route an agent to deeper knowledge.

Keep routing concise. Do not duplicate the internal documentation inside agent instruction files.

A useful routing pattern is:

```text
Product behavior: docs/functionality/
Architecture: docs/architecture/
Reference: docs/reference/
Development: docs/development/
Capability index: docs/CAPABILITIES.md
```

Project-local instructions remain authoritative.

## Internal evolution layer

When credible planning evidence exists and reconciliation is useful, `docs/evolution/` may contain durable internal records of what was intended, what exists now, and how the implementation diverged.

This layer is not part of the default public project presentation. Do not expose it from README merely because it exists.

## Local diagnostic layer

Continuation and contamination analysis should normally write temporary or potentially sensitive findings outside tracked documentation:

```text
.project-documentation/
  continuation-report.md
  contamination-report.md
  findings.json
```

The diagnostic directory should normally be ignored by version control. Promote only durable and safe conclusions into tracked `docs/`.
