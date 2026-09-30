# Continuation Audit

## Purpose

Identify repository residue and unfinished transitions that deserve attention before further development.

This is project archaeology, not a replacement for language-specific static analysis.

## Finding classes

Look for evidence of abandoned implementation, orphaned modules or assets, superseded paths, incomplete migrations, stale references, old compatibility layers, planning residue, and documentation that still describes replaced behavior.

## Confidence

Use `confirmed`, `likely`, `suspected`, or `historical`.

Do not classify code as unused solely because a text search finds no references. Account for dynamic imports, plugin discovery, reflection, framework conventions, filesystem discovery, external consumers, and build-time loading.

## Safety

Findings are advisory review candidates. Recommend review, verification, migration, consolidation, or cleanup as appropriate.

## Output

Diagnostic output should normally remain local and untracked under `.project-documentation/`.

Suggested files:

```text
.project-documentation/
  continuation-report.md
  findings.json
```

A safe summary may be promoted into tracked internal documentation only when the user wants it there and the content is suitable for repository history.
