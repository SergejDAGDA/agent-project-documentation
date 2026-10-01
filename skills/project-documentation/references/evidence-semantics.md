# Evidence Semantics

## Purpose

Keep evidence origin, verification strength, time, and state identity distinct when those differences affect whether documentation is true.

This reference is cross-cutting. It applies when claims cross repository, release, runtime, coordination, or historical boundaries. Do not force this vocabulary onto ordinary claims when the distinction is immaterial.

## Evidence provenance

Provenance describes where the evidence came from and, when relevant, how it entered the current task. Common useful labels are:

- `repository-derived` — read from the current repository, its history, tests, configuration, schemas, or maintained documentation
- `current-task-external` — observed directly from an external system during the current task
- `user-supplied` — supplied explicitly by the user, including operational facts that the current task did not independently query
- `prior-or-coordination` — carried from an earlier task, handoff, checkpoint, project-memory artifact, or other coordination record

These labels describe origin or acquisition, not verification confidence. Do not imply direct external observation when the current task did not perform it.

When volatile external state matters, preserve an as-of time, event, revision, or equivalent freshness context when available.

## Verification confidence

Use one canonical confidence vocabulary:

- `verified` — direct or sufficiently strong evidence supports the claim
- `partial` — evidence supports part of the claim, but a material uncertainty or boundary remains
- `unverified` — the claim or signal exists, but current evidence does not substantiate it

Confidence is independent of provenance. User-supplied evidence can be clearly attributed without being described as independently verified, and repository-derived evidence can still be partial.

## Temporal role

Temporal role is separate from confidence. When useful, distinguish:

- `current`
- `historical`
- `proposed/planned`

`historical` is not a confidence value. A historical claim can be verified.

## Revision and state identities

A project can have several simultaneously valid identities, for example:

- repository HEAD
- implementation or source baseline
- released or deployed source revision
- artifact or build identity
- runtime identity
- documentation or coordination revision

Do not collapse materially different identities into a generic `current revision` when that would make a claim false or ambiguous.

A repository HEAD may advance because of documentation-only or coordination-only changes while an implementation or deployed source baseline remains unchanged.

## Authority by claim domain

Authority follows the claim domain, not physical location, recency, or a generic `current` marker.

For each materially distinct state or claim domain, identify the authoritative source when authority matters. Examples of domains include implementation state, released or deployed identity, persistent application state, operational configuration, accepted decisions, and coordination state.

Historical markers, runtime records, repository state, and coordination snapshots can all be valid evidence without being authoritative for the same domain.

Do not impose one universal authority across unrelated domains.

## Reporting rule

Make provenance, confidence, temporal role, or precise identity explicit when omitting that distinction could mislead the reader. Do not require all dimensions for every finding or documentation claim.

For machine-readable diagnostics, prefer separate optional fields rather than one overloaded status field.
