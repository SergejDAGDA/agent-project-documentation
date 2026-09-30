# Project Overview

## Purpose

`project-documentation` is a portable Agent Skill for converting a source repository into maintainable project documentation and reusable knowledge.

The repository intentionally separates the portable skill core from Codex and Claude Code packaging.

## Documentation levels

The skill produces two primary levels.

### Presentation

A concise GitHub-facing or reader-facing layer that explains what the project is, what it can do, how to begin using it, and where deeper documentation lives.

### Internal project knowledge

Detailed functional, architectural, development, reference, and reuse documentation intended for developers and AI agents.

## Primary design goals

- remain independent from a specific product or legacy project
- work across languages and frameworks
- avoid template-driven empty documentation
- ground important claims in current repository evidence
- preserve authored documentation when possible
- extract capabilities rather than merely listing files
- separate functional contracts from current implementation
- make useful solutions easier to transfer to future projects
- support documentation of Agent Skills themselves
- compare accepted project intent with current implementation for internal traceability
- identify development residue that deserves review before further work
- detect accidental coupling to previous projects, users, environments, or examples

## Repository layout

The canonical portable skill lives in `skills/project-documentation/`.

The root `plugin.json` and `.agents/plugins/marketplace.json` provide Codex-oriented packaging.

`.claude-plugin/plugin.json` provides Claude Code plugin metadata around the same shared `skills/` directory.
