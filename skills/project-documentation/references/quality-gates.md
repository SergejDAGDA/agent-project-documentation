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

## Skill profile

For skill or plugin repositories, pass when trigger contract, workflows, resources, packaging, portability, and limitations are documented.
