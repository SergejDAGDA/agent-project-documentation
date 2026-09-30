# Project Contamination Audit

## Purpose

Detect project-specific, user-specific, environment-specific, or example-derived data that may have leaked into reusable code or configuration.

The central question is whether a value represents product logic or accidental context from another project, user, customer, environment, fixture, or example.

## Candidate contamination

Inspect meaningful source, configuration, documentation, fixtures, scripts, and assets for candidates such as old project names, customer or organization names embedded in reusable logic, project-specific domains or source identifiers, local absolute paths, hardcoded installation IDs, demo or sample entities, and comments that still treat a legacy project as the current specification.

Use `legacy-example-contamination` when a previous project or example appears to have been treated as the specification for a new reusable implementation.

## Context labels

When useful, classify a candidate as `intentional`, `project-specific`, `user-specific`, `sensitive`, or `unknown`.

Do not label an intentional public project identity as contamination merely because it contains a name or email address. Evaluate role and context.

## Sensitive-data boundary

This skill does not replace a dedicated privacy, secret, or security scanner.

When ordinary analysis encounters a credential-like or confidential value, do not reproduce the literal in generated documentation or diagnostic output. Report only its category and location, redact evidence strings, and recommend dedicated review when appropriate.

## Architecture guidance

When a project-specific literal is actively used, determine whether it belongs in configuration, environment-specific settings, a content or dataset layer, fixtures, user-supplied data, or installation-specific metadata instead of reusable product logic.

## Output

Contamination reports should normally remain local and untracked under `.project-documentation/`.

Suggested files:

```text
.project-documentation/
  contamination-report.md
  findings.json
```

Do not publish a diagnostic report merely because the source repository is public.
