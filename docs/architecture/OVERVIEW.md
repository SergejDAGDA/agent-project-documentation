# Architecture Overview

## Portable core

The repository has one canonical skill implementation:

```text
skills/project-documentation/
  SKILL.md
  agents/
  references/
  scripts/
```

`SKILL.md` contains the core workflow and routing rules.

`references/` contains conditional detail loaded when applicable.

`scripts/` contains deterministic helpers where repeatable code materially improves reliability.

`agents/openai.yaml` contains OpenAI-facing interface metadata and is not the source of workflow behavior.

## Packaging layer

Platform-specific plugin metadata surrounds the shared skill core.

```text
Codex or OpenAI packaging
  plugin.json
  .agents/plugins/marketplace.json

Claude Code packaging
  .claude-plugin/plugin.json
```

No second copy of the skill instructions is maintained for Claude Code.

## Execution model

The agent performs semantic repository analysis and documentation authoring.

Deterministic scripts provide repository inventory and lightweight structural checks.

This division avoids pretending that a generic static parser can understand every project's product semantics while still reducing repetitive filesystem inspection and simple validation work.
