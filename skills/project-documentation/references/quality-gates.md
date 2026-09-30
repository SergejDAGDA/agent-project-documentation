# Documentation Quality Gates

## Grounding

Pass when important claims can be traced to current repository evidence.

Fail when planned, commented, or historical behavior is presented as currently implemented without qualification.

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

Pass when project-memory and coordination artifacts can be read as evidence but are reported as out-of-scope inconsistencies unless the user explicitly includes their maintenance in scope.

Fail when ordinary documentation synchronization rewrites `HANDOFF.md`, `STATUS.md`, `DECISIONS.md`, `SESSION_LOG.md`, or equivalent memory artifacts without explicit scope.

## Helper discipline

Pass when bundled helper scripts are invoked directly using the documented command and repeated discovery probes are avoided.

Fail when the agent runs `--help` before routine execution without evidence of an interface mismatch or repeats the same `--help` probe.

## Markdown scope

Pass when the default Markdown audit covers documentation surfaces and ignores Markdown used as fixture, sample, QA, generated, or runtime data unless explicitly requested.

Fail when non-documentation Markdown produces noisy documentation warnings by default.

## Skill profile

For skill or plugin repositories, pass when trigger contract, workflows, resources, packaging, portability, and limitations are documented.

## Reconciliation quality

Pass when accepted planning evidence is distinguished from brainstorming, current implementation is independently verified, deltas are classified consistently, and unknown rationale remains unknown.

Fail when historical intent is presented as current behavior or when the agent invents reasons for divergence.

## Continuation audit quality

Pass when residue findings identify evidence, confidence, change risk, and dynamic-use uncertainty.

Fail when an unreferenced file is automatically labeled obsolete or when diagnostic findings are treated as direct change instructions.

## Project contamination quality

Pass when project-specific, user-specific, environment-specific, and example-derived context is separated from reusable logic and findings explain whether configuration or data extraction may be appropriate.

Fail when intentional project identity is automatically labeled contamination or when example-derived assumptions remain embedded without review.

## Sensitive-data handling

Pass when credential-like or private values are redacted from generated reports and only their category and location are recorded.

Fail when a discovered credential-like literal is copied into documentation or diagnostic JSON.
