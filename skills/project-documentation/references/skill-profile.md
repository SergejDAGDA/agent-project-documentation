# Agent Skill and Plugin Documentation Profile

## Detection

Treat a repository as a skill or plugin repository when evidence includes one or more of:

- `SKILL.md`
- `skills/<name>/SKILL.md`
- `agents/openai.yaml`
- root `plugin.json`
- `.claude-plugin/plugin.json`
- MCP configuration
- plugin commands, hooks, or agents

A repository can contain several skills. Document each skill separately when their purposes differ.

## Public documentation

For every skill, explain when applicable:

- problem solved
- trigger scenarios
- non-goals
- supported modes
- required tools or external capabilities
- installation or distribution paths
- platform compatibility supported by evidence
- typical invocation examples
- important limitations
- relationship to other bundled skills

Keep examples generic unless the repository itself intentionally targets a specific product or domain.

## Internal documentation

Document:

### Trigger contract

- `name`
- `description`
- important activation boundaries
- explicit invocation behavior when relevant

### Workflow

- phases
- mode routing
- stop conditions
- verification gates
- completion evidence

### Resources

For each `references/` file, explain what decision or workflow it supports.

For each `scripts/` file, explain inputs, outputs, side effects, dependencies, and failure behavior.

For each `assets/` item, explain how it participates in generated output.

### Packaging

Document platform-specific manifests separately from the portable skill core.

Portable core normally consists of:

```text
skills/<skill-name>/
  SKILL.md
  references/
  scripts/
  assets/
```

Codex or OpenAI plugin packaging and Claude Code plugin packaging may coexist around the same core when each manifest is valid for its platform.

### Portability

Identify:

- portable instructions
- portable scripts
- tool-specific instructions
- platform-specific manifests
- MCP assumptions
- shell or operating-system assumptions

Do not claim cross-platform compatibility based only on identical file names.

## Skill documentation as reusable knowledge

When the skill itself encodes a reusable methodology, document the method independently from platform packaging.

This makes it possible to port the workflow while replacing installation, tool, or manifest details.
