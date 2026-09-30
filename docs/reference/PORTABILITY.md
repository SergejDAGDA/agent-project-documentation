# Portability

## Portable knowledge

The portable core is the `project-documentation` skill directory and its platform-neutral methodology.

The central concepts are:

- adaptive repository discovery
- capability-based documentation
- source-grounded evidence states
- two-level presentation and internal documentation
- functional contract separated from implementation
- reuse notes
- targeted documentation maintenance
- Agent Skill documentation profile

## Platform-specific knowledge

The following are packaging details rather than core methodology:

- root OpenAI or Codex plugin manifest
- Codex marketplace metadata
- Claude Code plugin manifest
- platform-specific installation commands
- future platform-specific metadata

## Maintenance rule

Do not fork the core skill into separate Codex and Claude copies.

When platform behavior requires different instructions, isolate only the platform-specific section or resource and keep shared workflow rules canonical.
