# Diagnostic Output Contract

## Default location

Diagnostics from `continuation` and `contamination` modes should default to `.project-documentation/`.

The directory should normally be ignored by version control.

Read `evidence-semantics.md` when provenance, confidence, temporal role, or revision identity materially affects a finding.

## Finding schema

A machine-readable finding should contain only fields useful for follow-up, such as type, path, line, summary, context, related capability, recommendation, and the following optional evidence fields when they materially affect interpretation:

- `evidence_provenance`
- `verification_confidence`
- `temporal_role`

Do not require all evidence fields for every finding. Keep provenance, confidence, and temporal role separate rather than overloading one generic status field.

Do not store confidential literal contents in findings. Credential-like values must be omitted.

## Human report

For each material finding include the finding type, location, concise evidence without confidential literal disclosure, current implementation relationship, risk if left unchanged, risk if modified, and suggested next action.

Include evidence provenance, verification confidence, temporal role, or precise revision/state identity when omitting that distinction could mislead the reader.

Separate facts from interpretation.

## Relationship to tracked documentation

`docs/` contains durable project knowledge.

`.project-documentation/` contains analysis artifacts that may be temporary, sensitive, noisy, or unsuitable for public presentation.

Promote a diagnostic conclusion into `docs/` only when it is durable, safe to track, and useful to future maintainers.
