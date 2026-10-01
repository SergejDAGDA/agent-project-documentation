# Documentation Quality Gates

## Grounding

Pass when important claims can be traced to evidence appropriate to their claim domain.

Repository implementation claims should be grounded in current repository evidence. External operational claims may rely on current-task external observation, user-supplied evidence, or prior coordination evidence when provenance is clear enough for the reader to understand what was and was not independently checked.

Fail when planned, commented, historical, or externally supplied behavior is presented as currently implemented or independently verified without qualification.

## Evidence provenance

Pass when evidence provenance is made explicit whenever the difference between repository-derived, current-task external, user-supplied, or prior/coordination evidence materially affects the truth of a claim.

Fail when documentation implies that an external system was checked in the current task when the claim was only supplied by the user or inherited from prior coordination evidence.

## Temporal identity

Pass when materially distinct repository, implementation, release or deployment, artifact/build, runtime, and documentation/coordination identities remain distinct where the difference matters.

Fail when several different identities are collapsed into one generic `current revision` and that wording can become false or ambiguous as repository history advances.

## Authority by claim domain

Pass when the authoritative source for each materially distinct claim domain is clear when authority matters.

Fail when historical markers, coordination snapshots, runtime records, and repository state silently compete as if they were authoritative for the same domain, or when physical location or recency alone is treated as proof of authority.

## Coverage

Pass when all material current capabilities are represented in the capability index or intentionally excluded with a reason.

Fail when the documentation only describes the most obvious entrypoint while important behavior remains undiscovered.

## Functional and implementation separation

Pass when reusable behavior can be understood without requiring the current framework.

Fail when capability documentation is only a tour of files and classes.

## Presentation quality

Pass when a new reader can quickly understand what the repository is, what it currently does, and how to begin using or evaluating it.

Fail when README content is either a marketing shell with no usable start path or a full internal architecture dump.

## Adaptive structure

Pass when every generated document has a meaningful repository-specific purpose.

Fail when empty or irrelevant template documents are created.

## Navigation

Pass when public documentation points to deeper material and internal documents have clear canonical locations.

Fail when similar information exists in several places with no clear source of truth.

## Reuse quality

Pass when reusable capabilities state functional invariants, implementation assumptions, dependencies, boundaries, and limitations.

Fail when reuse guidance means copying source files without explaining contracts or coupling.

## Maintenance safety

Pass when updates preserve deliberate authored material and limit changes to affected knowledge.

Fail when routine synchronization rewrites the entire documentation set without need.

## Ambiguous invocation safety

Pass when a vague request to apply the skill defaults to discovery plus read-only audit and does not mutate files merely because stale documentation is found.

Fail when the skill silently upgrades an ambiguous request into `update`, `init`, or another write-capable workflow.

## Ownership boundaries

Pass when project-memory and coordination artifacts are recognized by purpose as well as directory. Strong signals include handoff/checkpoint names or primary headings, exact status/decision/session-log files, and clearly identified project-memory directories.

Such artifacts may be read as evidence when project instructions require them or when they materially help establish current context, but ordinary documentation maintenance reports their conflicts under `Out-of-scope coordination findings` instead of rewriting them.

Fail when ordinary documentation synchronization rewrites `HANDOFF.md`, `*HANDOFF*.md`, `STATUS.md`, `DECISIONS.md`, `SESSION_LOG.md`, `*CHECKPOINT*.md`, or equivalent coordination artifacts without explicit scope, including when those files live outside a project-memory directory.

## Project-memory relevance

Pass when coordination or project-memory artifacts are loaded because repository-local instructions require them or because they are materially relevant to the current documentation question.

Fail when every documentation operation treats project memory as the default baseline even when ordinary repository evidence is sufficient.

## Helper discipline

Pass when bundled helper scripts are invoked directly using the documented command and only when their output is relevant to the selected mode.

`repository_inventory.py` is appropriate when discovery is needed. `documentation_audit.py` is the normal structural documentation check. `repository_diagnostics.py` is appropriate for `continuation`, `contamination`, explicitly requested broad internal diagnostics, or a narrowly justified investigation that needs its heuristic signals.

Fail when the agent runs `--help` before routine execution without evidence of an interface mismatch, repeats the same `--help` probe, or runs `repository_diagnostics.py` merely because it exists during routine `init`, `audit`, `update`, `presentation`, or `release` work.

## Markdown scope

Pass when the default Markdown audit covers maintained documentation surfaces while excluding Markdown used as fixture, sample, QA, generated, runtime, project-memory, handoff, checkpoint, or other coordination data unless that broader scope is explicitly requested.

Fail when non-documentation or separately owned coordination Markdown produces noisy ordinary-documentation errors by default.

## Skill profile

For skill or plugin repositories, pass when trigger contract, workflows, resources, packaging, portability, and limitations are documented.

## Reconciliation quality

Pass when accepted planning evidence is distinguished from brainstorming, current implementation is independently verified, deltas are classified consistently, and unknown rationale remains unknown.

Fail when historical intent is presented as current behavior or when the agent invents reasons for divergence.

## Continuation audit quality

Pass when residue findings identify evidence, canonical verification confidence, change risk, and dynamic-use uncertainty, with temporal role kept separate when relevant.

Fail when an unreferenced file is automatically labeled obsolete, when `historical` is treated as a confidence value, or when diagnostic findings are treated as direct change instructions.

## Project contamination quality

Pass when project-specific, user-specific, environment-specific, and example-derived context is separated from reusable logic and findings explain whether configuration or data extraction may be appropriate.

Fail when intentional project identity is automatically labeled contamination or when example-derived assumptions remain embedded without review.

## Sensitive-data handling

Pass when credential-like or private values are redacted from generated reports and only their category and location are recorded.

Fail when a discovered credential-like literal is copied into documentation or diagnostic JSON.
