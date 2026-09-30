# Project Evolution and Diagnostic Workflows

## Purpose

Provide internal analysis that helps maintainers understand how the current implementation relates to earlier project intent and what repository residue or accidental project coupling deserves attention before further development.

## Status and evidence

Status: verified

The workflows are defined in `skills/project-documentation/SKILL.md` with dedicated references for reconciliation, continuation analysis, contamination analysis, and diagnostic output.

## Functional contract

### Reconcile

Inputs may include accepted MVP specifications, requirements, roadmaps, issues, milestones, design documents, current source code, tests, configuration, and version-control history.

The workflow separates planning evidence, implementation evidence, and evolution evidence. It classifies material items as planned-implemented, planned-modified, planned-partial, planned-missing, deferred, superseded, unplanned-implemented, removed, or unknown.

It must not invent historical rationale.

### Continuation

The workflow identifies review candidates such as abandoned implementation, superseded paths, incomplete migrations, stale references, compatibility residue, and other development archaeology signals.

Findings use explicit confidence and are advisory. The workflow does not automatically change candidate code.

### Contamination

The workflow identifies project-specific, user-specific, environment-specific, or example-derived context that may have leaked into reusable code or configuration.

It can flag potential legacy-example contamination, user-specific paths, source-specific literals, and values that may belong in configuration or data instead of product logic.

Credential-like literal values are not copied into reports.

## Output model

Durable reconciliation knowledge may be tracked under `docs/evolution/` when useful.

Continuation and contamination diagnostics default to the untracked `.project-documentation/` directory because findings may be temporary, noisy, private, or unsuitable for public presentation.

## Current implementation

Relevant skill references:

- `skills/project-documentation/references/evolution-reconciliation.md`
- `skills/project-documentation/references/continuation-audit.md`
- `skills/project-documentation/references/contamination-audit.md`
- `skills/project-documentation/references/diagnostic-output.md`

The helper `skills/project-documentation/scripts/repository_diagnostics.py` emits conservative heuristic signals and supports explicit known-context markers. It does not prove that a file is obsolete or removable.

## Reuse notes

The transferable principle is to keep three concerns separate:

1. durable project knowledge
2. historical reconciliation
3. temporary diagnostic findings

This separation allows another agent or tool to replace the heuristic scanner without changing the documentation contract.
