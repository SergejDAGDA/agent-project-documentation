# Repository Analysis

## Discovery order

Use a broad-to-narrow pass.

### 1. Repository control files

Inspect as applicable:

- `AGENTS.md`
- `CLAUDE.md`
- README files
- contribution guidance
- workspace manifests
- package manifests
- build files
- lock files
- CI configuration
- deployment configuration
- plugin manifests
- environment examples

### 2. Repository shape

Identify:

- source roots
- test roots
- public assets
- schemas
- migrations
- generated output
- vendored dependencies
- documentation roots
- scripts and tooling
- examples

Ignore dependency caches and large generated trees unless they are the product being documented.

### 3. Entrypoints

Find the smallest set of files that establish the runtime or package entrypoints.

Examples include application bootstrap, exported package entrypoints, CLI commands, route registration, plugin manifests, skill manifests, service startup, and build exports.

### 4. Behavioral surfaces

Identify surfaces that reveal what the project can do:

- routes
- commands
- user interfaces
- exported APIs
- event handlers
- tests
- schemas
- permissions
- integrations

### 5. Capability grouping

Group related behavior into capabilities rather than documenting implementation fragments independently.

Prefer a stable product concept over a framework-specific component name when they describe the same thing.

### 6. Evidence map

For each capability, record the most useful evidence:

- implementation source
- behavioral test
- configuration or schema
- public surface
- current documentation

The documentation may summarize this map instead of storing a machine-generated database unless the repository needs one.

## Monorepos

For a monorepo, first identify workspace boundaries and shared packages.

Decide whether documentation belongs at repository level, package level, or both.

Do not flatten unrelated products into one capability index.

## Generated and vendored code

Do not use generated or vendored code as the primary explanation when a source definition is available.

If generated artifacts are user-facing or operationally important, document their role and regeneration path.
