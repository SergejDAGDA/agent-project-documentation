# Capability Documentation

## Purpose

A capability document should preserve knowledge well enough that a future developer or agent can understand the behavior and, when appropriate, reproduce it in another project.

## Recommended structure

Use only applicable sections.

```text
# Capability name

## Purpose
## Status and evidence
## Functional contract
### User or caller behavior
### Inputs
### Outputs
### States
### Rules and constraints
### Failure behavior
### Edge cases
## Current implementation
### Components
### Data flow
### Persistence
### Interfaces
### Configuration
### Dependencies
### Tests
## Reuse notes
## Known limitations
## Source references
```

## Functional contract rules

Describe behavior independently from the current framework whenever possible.

Good functional knowledge explains:

- what must happen
- what may happen
- what must not happen
- state transitions
- validation rules
- permissions
- observable failure behavior

Avoid leaking implementation into the functional contract unless the implementation itself is part of the contract.

## Current implementation rules

Explain how the repository currently satisfies the contract.

Use repository-relative paths and stable identifiers such as module, class, function, command, route, or configuration names.

Do not dump every file that mentions the feature.

## Reuse notes

Reuse notes should help transfer a capability without accidental cargo-culting.

Record:

- behavior that should remain invariant
- boundaries that can be redesigned
- required interfaces
- data assumptions
- external services or packages
- security assumptions
- migration hazards
- known limitations

Do not state that code is portable when it is tightly coupled to project-specific infrastructure.
