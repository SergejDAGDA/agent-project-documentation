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
- existing maintained documentation when present
- source code, tests, configuration, schemas, manifests, and related project evidence
- external operational evidence supplied by the user or observed directly in the current task when materially relevant
- project-memory or coordination artifacts only when required by local instructions or materially relevant
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
- out-of-scope coordination findings
- completion evidence describing verified and unresolved areas
- explicit evidence provenance, confidence, temporal role, or revision/state identity when those distinctions materially affect a claim

### Modes

The skill defines `init`, `audit`, `update`, `presentation`, `internal`, `release`, `extract`, `skill-docs`, `reconcile`, `continuation`, and `contamination` workflows.

Mode selection is intent-driven rather than tied to a required command syntax. Ambiguous requests default to read-only audit rather than write-capable update.

### Capability discovery

The workflow groups meaningful behavior into capabilities instead of treating every source file or framework component as a separate feature.

Capabilities can be marked `verified`, `partial`, or `unverified` based on evidence appropriate to the claim domain.

Those values describe verification confidence. Historical or proposed/planned state is a separate temporal role.

`unverified` behavior must not be presented as implemented.

### Evidence semantics

When a claim crosses repository, runtime, or time boundaries, the workflow keeps separate:

- evidence provenance
- verification confidence
- temporal role
- materially distinct revision or state identities

Repository HEAD, implementation/source baseline, released or deployed source revision, artifact/build identity, runtime identity, and documentation/coordination revision may differ without constituting drift by themselves.

Authority is determined per claim domain. A repository, runtime record, historical marker, or coordination snapshot can be valid evidence without being authoritative for the same thing.

### Adaptive structure

The workflow creates only documentation that fits the repository.

For example, a project with no API should not receive empty API documentation solely because a template contains such a file.

### Update behavior

When documentation exists, the workflow should preserve deliberate authored content and update the smallest affected documentation surface.

Coordination artifacts are identified by purpose as well as location. Handoff/checkpoint documents, exact status/decision/session-log files, primary coordination headings, and clearly identified project-memory directories remain outside ordinary documentation mutation unless the user explicitly includes them.

Broken links or stale statements inside those artifacts are reported rather than silently repaired by ordinary `update`.

### Failure and uncertainty behavior

When code, tests, existing docs, configuration, external operational evidence, or coordination evidence conflict, the workflow reports the disagreement instead of silently converting one version into fact.

Unknown historical rationale must remain unknown unless supported by evidence.

The workflow must not imply that an external system was independently checked in the current task when the evidence was only supplied by the user or inherited from prior coordination material.

## Current implementation

### Skill entrypoint

`skills/project-documentation/SKILL.md`

Defines purpose, modes, discovery, capability analysis, output rules, coordination ownership, verification, update safety, quality gates, and completion evidence.

### Supporting references

- `documentation-model.md` defines presentation and internal documentation levels
- `evidence-semantics.md` defines evidence provenance, verification confidence, temporal role, revision/state identity, and authority by claim domain
- `repository-analysis.md` defines broad-to-narrow repository discovery
- `feature-documentation.md` defines capability documentation and reuse notes
- `quality-gates.md` defines acceptance checks
- `skill-profile.md` defines Agent Skill and plugin specialization
- `evolution-reconciliation.md` defines plan-versus-implementation traceability
- `continuation-audit.md` defines project-residue analysis
- `contamination-audit.md` defines accidental context-coupling analysis
- `diagnostic-output.md` defines safe local diagnostic output

### Deterministic helpers

`repository_inventory.py` builds a compact repository inventory when discovery needs it.

`documentation_audit.py` performs lightweight Markdown and skill-structure checks on maintained documentation surfaces while excluding data-like and coordination Markdown by default. `--all-markdown` opts into a broader scan.

`repository_diagnostics.py` emits conservative continuation and contamination signals while redacting credential-like literals. It is not a routine quality gate for ordinary documentation updates.

The helpers do not generate project prose and do not replace agent reasoning.

## Reuse notes

The core reusable idea is the separation of four concerns:

1. source-grounded capability discovery
2. functional contract independent from implementation
3. current implementation map with explicit reuse boundaries
4. evidence semantics that keep provenance, confidence, temporal role, and materially distinct identities separate when needed

A future implementation can replace the helper scripts, agent platform, or packaging while preserving this contract.

Do not copy platform-specific plugin manifests into environments that use different extension formats.

## Known limitations

The deterministic helpers intentionally perform structural checks only. They do not parse arbitrary programming languages deeply and cannot independently prove semantic documentation correctness.

Coordination detection in the Markdown helper is deliberately conservative and based on strong path, filename, and primary-heading signals; ambiguous files still require agent judgment.
