# Evolution Reconciliation

## Purpose

Compare evidenced project intent with the current implementation without turning historical plans into current product claims.

Use this reference for `reconcile` mode and when a full internal documentation pass has credible planning material.

Read `evidence-semantics.md` when provenance, confidence, temporal role, or revision identity materially affects a reconciliation claim.

## Evidence groups

Keep three evidence groups distinct.

### Planning evidence

Examples include accepted MVP specifications, requirements, roadmaps, issues, milestones, design documents, initial project briefs, and explicitly approved proposals.

Do not treat brainstorming, abandoned alternatives, or unaccepted notes as committed intent unless the repository or user context establishes that status.

### Implementation evidence

Use current source code, tests, configuration, schemas, routes, commands, UI surfaces, APIs, and current operational documentation.

### Evolution evidence

Use commits, pull requests, changelog entries, issues, decision records, migration notes, and other records that explain how the project changed over time.

## Reconciliation states

Classify material plan items with one of these states when evidence supports it.

- `planned-implemented` for intent implemented without a material functional change
- `planned-modified` for intent implemented with a material change in behavior or scope
- `planned-partial` for intent only partly implemented
- `planned-missing` for accepted intent with no current implementation found
- `deferred` when postponement is explicitly evidenced
- `superseded` when another solution explicitly replaced the original plan
- `unplanned-implemented` for current capability with no corresponding accepted planning item found
- `removed` for functionality that existed and was later removed
- `unknown` when the relationship or reason cannot be established reliably

Never infer the reason for a deviation merely from the fact that a deviation exists.

## Internal output

Reconciliation is internal project knowledge. Do not put plan-versus-implementation detail in the public README unless the user explicitly requests a public project history or worklog.

When tracked internal documentation is appropriate, use an adaptive location such as:

```text
docs/evolution/
  BASELINE.md
  TRACEABILITY.md
  IMPLEMENTATION_REVIEW.md
```

Do not create these files when credible planning evidence is absent.

## Traceability record

For each material item capture:

- original intent
- planning source
- current state
- current implementation evidence
- reconciliation state
- observed delta
- evidenced evolution context
- unknowns

When external, coordination, or time-sensitive evidence materially affects the result, also record the relevant evidence provenance, verification confidence, temporal role, and precise revision/state identity instead of collapsing them into a generic current state.

Keep `unknown` explicit instead of manufacturing rationale.
