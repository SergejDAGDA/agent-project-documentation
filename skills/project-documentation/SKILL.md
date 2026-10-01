---
name: project-documentation
description: Extract, create, audit, and maintain repository documentation as reusable project knowledge. Use when a user wants GitHub-ready presentation documentation, detailed internal functional or technical documentation, plan-versus-implementation reconciliation, continuation and project-contamination diagnostics, repository knowledge extraction for later reuse, documentation synchronization after code changes, release documentation checks, or documentation of an Agent Skill or plugin itself.
---

# Project Documentation

## Purpose

Turn an existing repository into a documented, reusable body of project knowledge.

The skill serves two audiences at the same time:

1. Presentation documentation for a person who wants to understand the project quickly.
2. Internal documentation for a developer or agent who needs to understand behavior, architecture, constraints, implementation, and reusable capabilities in depth.

The skill is not tied to a language, framework, repository type, or product category.

## Core principle

Document what the repository demonstrably contains.

Do not invent features, architecture, rationale, workflows, dependencies, or future plans.

Separate product or functional behavior from the current implementation so that useful capabilities can be reused in another project without copying framework-specific assumptions.

## Authority

Project-local instructions, source code, tests, configuration, existing documentation, schemas, and explicitly recorded decisions are authoritative within their scope.

Authority follows the claim domain. Repository implementation, external operational state, persistent data, accepted decisions, and coordination state may have different authoritative sources. Physical location, recency, or a generic `current` marker does not establish authority by itself.

When materially important claims cross repository, runtime, or time boundaries, keep evidence provenance, verification confidence, and temporal role separate. Do not imply independent external verification when the current task did not perform it. Read `references/evidence-semantics.md`.

When sources disagree, report the conflict instead of silently choosing the most convenient version.

Do not overwrite deliberate project documentation merely to force a preferred template.

## Invocation and routing

The repository or plugin package may be named differently from the installed skill. The canonical installed skill name is the YAML frontmatter `name` in this file: `project-documentation`.

If a user refers to this repository as `agent-project-documentation` and the installed skill is `project-documentation`, treat that as the same skill when the repository provenance matches. Do not describe `project-documentation` as a merely similar or fallback skill.

When the user explicitly names a mode or clearly asks for a write operation, use the corresponding mode.

When the request is ambiguous, for example "apply this skill to the current repository", default to repository discovery plus read-only `audit`. Do not select `update` merely because stale documentation is discovered. Report the applicable write-capable modes and findings, then wait for an explicit request before changing files.

Do not ask a clarifying question when read-only audit can safely make progress.

## Documentation ownership boundaries

Documentation can coexist with project-memory or coordination artifacts that have a different maintenance contract.

Determine ownership by purpose, not only by directory. Strong coordination signals include:

- a filename containing `HANDOFF` or `CHECKPOINT`
- exact files such as `STATUS.md`, `DECISIONS.md`, or `SESSION_LOG.md`
- a primary heading that clearly identifies the document as a handoff, checkpoint, decision log, session log, or project status artifact
- clearly identified project-memory directories
- an explicit repository-local rule saying the file is maintained as session, deployment, agent, or coordination state

A file can therefore be a coordination artifact even when it lives directly under `docs/` or another ordinary documentation directory.

Coordination and project-memory artifacts may be read as evidence, but ordinary `update`, `presentation`, or `internal` work does not automatically own them.

Read them when repository-local instructions require it or when they materially help establish current context. Do not treat project memory as the default documentation baseline when current code, tests, configuration, and maintained documentation are sufficient.

When a coordination artifact conflicts with current implementation:

1. verify the current implementation independently
2. report the conflict under `Out-of-scope coordination findings`
3. do not rewrite the coordination artifact unless the user explicitly includes its maintenance in scope
4. preserve historical handoff or checkpoint sections that intentionally describe an older state

If a dedicated project-memory workflow or skill is available, defer mutation of those artifacts to that workflow. Core project documentation must still work when no such skill exists.

## Modes

Infer the appropriate mode from the request. If the user names a mode, use it.

### init

Use for first-time documentation of a repository.

Perform repository discovery, classify the project, identify capabilities, design an adaptive documentation set, create the presentation layer, create the internal layer, and run the quality gates.

### audit

Use to inspect documentation without rewriting it by default.

Report missing coverage, stale claims, broken internal links, unsupported claims, duplicated knowledge, unclear ownership, and mismatches between documentation and implementation.

### update

Use after project changes when the user requests documentation synchronization or another write operation.

Identify changed implementation surfaces, map them to affected documentation, update only the impacted knowledge, and preserve unaffected authored material.

Do not edit separately owned coordination artifacts merely because they contain stale or broken content. Report those findings separately unless the user explicitly includes coordination maintenance.

### presentation

Focus on the public GitHub-facing layer such as README content, feature overview, quick start, screenshots or demo references, installation, status, documentation navigation, and licensing information.

Keep this layer concise and understandable without requiring the reader to study internal architecture.

### internal

Focus on detailed functional, architectural, development, and reference documentation.

### release

Check that documentation is release-ready. Include README accuracy, installation accuracy, current capabilities, changelog relevance when present, internal documentation consistency, links, and unsupported claims.

Do not declare release documentation ready when required evidence is missing.

### extract

Focus on reusable knowledge extraction.

Identify capabilities that can be transferred to another project. Document functional contracts separately from current implementation details and include reuse notes.

### skill-docs

Use when the target repository contains one or more Agent Skills or plugins.

Document the skill as a product and as an implementation. Read `references/skill-profile.md`.

### reconcile

Use for internal comparison of evidenced project intent with the current implementation.

Build a planning baseline only from credible accepted requirements or project records, compare it with current implementation evidence, classify the delta, and keep unknown rationale explicitly unknown. Read `references/evolution-reconciliation.md`.

Do not put plan-versus-implementation detail into the public presentation layer unless the user explicitly requests a public project history or worklog.

### continuation

Use when the user wants to know what deserves attention before further development or when a mature repository may contain abandoned, superseded, orphaned, or partially migrated implementation.

Treat findings as review candidates rather than deletion instructions. Read `references/continuation-audit.md` and `references/diagnostic-output.md`.

### contamination

Use to detect accidental coupling to a previous project, user, customer, environment, example dataset, source identifier, local path, or other context that should not be embedded in reusable logic.

This mode is not a replacement for a dedicated privacy, secret, or security scanner. Redact potentially sensitive literal values from reports. Read `references/contamination-audit.md` and `references/diagnostic-output.md`.

## Bundled helper invocation

Bundled helper commands are part of this skill contract. Use their documented invocation directly.

Do not probe bundled scripts with `--help` before normal execution. Use `--help` only when a documented invocation fails or the installed script demonstrably differs from this skill version. Never repeat the same `--help` probe in one task.

Canonical commands:

```text
python <skill-directory>/scripts/repository_inventory.py --root <project-root> --format markdown
python <skill-directory>/scripts/documentation_audit.py --root <project-root>
python <skill-directory>/scripts/repository_diagnostics.py --root <project-root> --format markdown
```

Use helpers according to the selected mode:

- `repository_inventory.py`: run when repository discovery benefits from a compact deterministic inventory
- `documentation_audit.py`: normal structural documentation check for maintained documentation surfaces
- `repository_diagnostics.py`: run for `continuation`, `contamination`, explicitly requested broad internal diagnostics, or a narrowly justified investigation that needs heuristic residue/contamination signals

Do not run `repository_diagnostics.py` as a routine quality gate for `init`, `audit`, `update`, `presentation`, or `release` merely because the helper exists.

The documentation audit excludes Markdown used as fixture, sample, QA, generated, runtime, project-memory, handoff, checkpoint, and similar coordination material by default. Use `--all-markdown` only when the user explicitly wants every Markdown file audited.

## Phase 1: Repository discovery

Before writing documentation:

1. Read project instructions such as `AGENTS.md`, `CLAUDE.md`, contributor guidance, and repository-local rules when present.
2. Inspect the repository tree.
3. Inspect package, build, dependency, workspace, plugin, deployment, schema, and test configuration that materially explains the project.
4. Identify source roots, entry points, boundaries, generated content, vendored content, and excluded directories.
5. Detect whether the repository is an application, library, CLI, service, plugin, Agent Skill, monorepo, documentation project, infrastructure project, or a combination.
6. Identify existing documentation and distinguish maintained documentation from generated/data Markdown and separately owned coordination artifacts.
7. Read project-memory or coordination artifacts only when repository-local instructions require them or when they materially help establish current context.
8. Run `scripts/repository_inventory.py` when local execution is available and its output will reduce guesswork.

Read `references/repository-analysis.md` for the discovery procedure.

## Phase 2: Capability discovery

Build a capability inventory before deciding the documentation structure.

A capability is a meaningful behavior, service, workflow, integration, or reusable project function. Do not equate every file, class, route, or component with a capability.

For each candidate capability, seek evidence from multiple relevant sources when practical:

- implementation
- tests
- routes or commands
- schemas and configuration
- UI or API surfaces
- existing documentation

Assign an evidence state:

- `verified` when current implementation or executable evidence supports the claim
- `partial` when only part of the described behavior is implemented or evidence is incomplete
- `unverified` when a claim exists in documentation, comments, or plans but current implementation was not found

These are verification-confidence values. Keep temporal roles such as `historical` or `proposed/planned` separate.

Never present `unverified` behavior as implemented.

## Phase 3: Design an adaptive documentation set

Do not create documents merely because they exist in a template.

Start from the model in `references/documentation-model.md`, then keep only sections that fit the repository.

Typical output may include:

```text
README.md

docs/
  CAPABILITIES.md
  overview/
  functionality/
  architecture/
  development/
  reference/
  decisions/
```

Rules:

- Do not create API documentation when there is no meaningful API surface.
- Do not create database documentation when there is no database or persistent data model.
- Do not create deployment documentation for a package that has no deployment process.
- Do not manufacture ADRs or historical decisions when rationale is not evidenced.
- Do not duplicate the same explanation across multiple files. Prefer a canonical document and link or reference it.
- Do not absorb coordination artifacts into the maintained documentation set merely because they are Markdown files under `docs/`.

## Phase 4: Build the presentation layer

The presentation layer answers, quickly:

- What is this project?
- Who or what is it for?
- What can it do now?
- How can someone try or install it?
- What are the important requirements?
- Where is deeper documentation?

Prefer an existing README structure when it is already deliberate and usable.

Improve inaccurate, incomplete, or difficult-to-navigate sections without turning the README into internal engineering documentation.

Presentation claims must be traceable to evidence appropriate to their claim domain. Implementation claims should be traceable to current repository evidence.

## Phase 5: Build the internal layer

Internal documentation should explain the product and the implementation at different levels.

For a meaningful capability, prefer a document structure that separates:

### Functional contract

- purpose
- user or caller behavior
- inputs and outputs
- states
- rules and constraints
- failure behavior
- edge cases
- security or permission implications when relevant
- interoperability expectations

### Current implementation

- responsible modules
- important components or services
- data flow
- storage
- APIs or commands
- dependencies
- configuration
- tests
- source references

### Reuse notes

- portable behavior that should be preserved
- implementation assumptions that should not be copied blindly
- required interfaces
- required data or state
- external dependencies
- known limitations

Read `references/feature-documentation.md` before creating capability documentation.

## Phase 6: Internal evolution and continuation analysis

Run these analyses only when requested or when a full internal pass has enough evidence to make them useful.

### Reconciliation

When credible planning material exists, compare accepted intent with the current implementation.

Keep planning, implementation, and evolution evidence separate. Use the states defined in `references/evolution-reconciliation.md`. Never invent why a planned item changed.

Tracked reconciliation documentation may live under `docs/evolution/` when it is durable and useful to maintainers. Keep it out of the public README by default.

### Continuation audit

Look for development residue such as abandoned implementation, superseded paths, incomplete migrations, stale references, compatibility layers, or planning residue.

Use source and history evidence before labeling anything removable. Dynamic loading, framework conventions, external consumers, and plugin discovery can make apparently unused code active.

When local execution is available, `scripts/repository_diagnostics.py` can provide conservative heuristic signals. Its output is evidence for review, not proof.

### Project contamination audit

Look for accidental project-specific, user-specific, environment-specific, or example-derived context embedded in reusable implementation. Pay special attention to values that should instead live in configuration, data, fixtures, content, or installation-specific metadata.

If a credential-like value or private contact datum is encountered, do not copy the literal into generated documentation or diagnostic output. Report only the category and location and recommend dedicated review when appropriate.

Diagnostic artifacts should normally remain local under `.project-documentation/`, which should be ignored by version control. Read `references/continuation-audit.md`, `references/contamination-audit.md`, and `references/diagnostic-output.md`.

## Phase 7: Agent Skill and plugin profile

When the repository is or contains Agent Skills, also inspect:

- every applicable `SKILL.md`
- YAML frontmatter
- `references/`
- `scripts/`
- `assets/`
- agent metadata such as `agents/openai.yaml` when present
- plugin manifests
- MCP definitions when present
- commands, hooks, and agents when part of the plugin

Document two distinct views:

1. Public view: what the skill solves, when it should trigger, installation or distribution model, supported workflows, requirements, limitations, and examples of appropriate use.
2. Internal view: trigger contract, modes, workflow phases, resource routing, scripts, dependencies, platform-specific packaging, portability boundaries, and maintenance contract.

Do not infer compatibility merely because two systems use a similar directory structure. State compatibility only when the repository structure and instructions support it.

Read `references/skill-profile.md`.

## Phase 8: Verification

Every important factual claim should be supported by evidence appropriate to its claim domain. Repository implementation claims should be grounded in current repository evidence.

External operational claims may rely on evidence verified directly in the current task, evidence explicitly supplied by the user, or prior/coordination evidence. Make provenance clear when the distinction matters, and never state or imply that an external system was independently checked when it was not.

Repository HEAD, implementation or source baseline, released or deployed source revision, artifact or build identity, runtime identity, and documentation or coordination revision may differ. Do not collapse materially distinct identities into one generic `current revision` when doing so would make a claim false or ambiguous.

For each materially distinct state or claim domain, identify its authoritative source when authority matters. Historical markers, coordination snapshots, runtime records, and repository state may all be valid evidence without being authoritative for the same domain.

Read `references/evidence-semantics.md` for provenance, confidence, temporal role, identity, and authority semantics.

Prefer source references that remain useful to future maintainers, such as repository-relative paths and relevant symbols or headings. Avoid fragile absolute line numbers as the only reference because they drift quickly.

For high-level capability claims, verify at least one implementation surface and, when available, one behavioral source such as a test, route, command, schema, or user-facing surface.

When evidence is conflicting or incomplete, mark the limitation in the documentation.

Do not claim that a test passes unless it was actually run successfully in the current task.

For write-capable modes, verify that the final diff does not include coordination artifacts unless their maintenance was explicitly in scope.

## Phase 9: Update safety

When documentation already exists:

1. Determine which parts are human-authored, generated, uncertain, data-like, or coordination-owned.
2. Preserve deliberate prose and project identity unless it is false or the user requested a rewrite.
3. Update the smallest affected documentation surface.
4. Do not erase unsupported historical context if it is clearly labeled as historical.
5. Do not convert uncertain rationale into fact.
6. Keep presentation and internal layers consistent without making them identical.
7. Keep separately owned project-memory and coordination artifacts outside ordinary documentation mutation unless explicitly included in scope.
8. If a coordination artifact contains a broken link or stale claim, report it rather than fixing it during ordinary `update`.

For update mode, use version control history or a diff when available to focus the review.

## Quality gates

Before completion, read `references/quality-gates.md` and check:

- factual grounding
- evidence provenance and authority by claim domain when materially relevant
- temporal identity separation when materially relevant
- capability coverage
- separation of functional contract from implementation
- presentation clarity
- navigation
- duplication
- broken internal references in maintained documentation surfaces
- adaptive structure
- portability of reusable knowledge
- skill profile coverage when applicable
- plan-versus-implementation traceability when reconciliation is requested
- conservative continuation findings with canonical verification confidence
- contamination findings that separate reusable logic from project-specific context
- sensitive literal redaction in diagnostics
- semantic ownership boundaries for coordination and project-memory artifacts
- absence of unnecessary helper probing
- mode-appropriate helper execution

Run `scripts/documentation_audit.py` when local execution is available.

## Completion evidence

Report:

- mode used
- repository type detected
- presentation files created or updated
- internal files created or updated
- capabilities documented
- unsupported or partial claims found
- reconciliation states when requested
- continuation or contamination findings when requested
- `Out-of-scope coordination findings` when relevant
- evidence provenance, verification confidence, temporal role, or precise revision/state identity when materially relevant
- validation scripts or tests actually run
- unresolved documentation gaps

Do not report documentation as complete when known material gaps remain.
