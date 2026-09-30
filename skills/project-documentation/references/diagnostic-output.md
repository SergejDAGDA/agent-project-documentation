# Diagnostic Output Contract

## Default location

Diagnostics from `continuation` and `contamination` modes should default to `.project-documentation/`.

The directory should normally be ignored by version control.

## Finding schema

A machine-readable finding should contain only fields useful for follow-up, such as type, confidence, path, line, summary, context, related capability, historical status, and recommendation.

Do not store confidential literal contents in findings. Credential-like values must be omitted.

## Human report

For each material finding include the finding type, confidence, location, concise evidence without confidential literal disclosure, historical context when evidenced, current implementation relationship, risk if left unchanged, risk if modified, and suggested next action.

Separate facts from interpretation.

## Relationship to tracked documentation

`docs/` contains durable project knowledge.

`.project-documentation/` contains analysis artifacts that may be temporary, sensitive, noisy, or unsuitable for public presentation.

Promote a diagnostic conclusion into `docs/` only when it is durable, safe to track, and useful to future maintainers.
