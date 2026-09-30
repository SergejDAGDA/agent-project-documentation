#!/usr/bin/env python3
"""Run lightweight structural checks on repository Markdown documentation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)
FIRST_H1 = re.compile(r"^\s*#\s+(.+)$", re.MULTILINE)

EXCLUDED_DIRS = {
    ".git",
    ".project-documentation",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "tmp",
    "temp",
    "backups",
}

DATA_DIRS = {
    "fixture",
    "fixtures",
    "snapshot",
    "snapshots",
    "testdata",
    "test-data",
    "test_data",
    "runtime",
    "artifacts",
}

PROJECT_MEMORY_DIRS = {
    "project-memory",
    "project_memory",
    ".project-memory",
    ".project_memory",
}

ROOT_DOCUMENT_NAMES = {
    "README.md",
    "README.ru.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE.md",
}

COORDINATION_EXACT_NAMES = {
    "STATUS.MD",
    "DECISIONS.MD",
    "SESSION_LOG.MD",
}

COORDINATION_NAME_TOKENS = {
    "HANDOFF",
    "CHECKPOINT",
}

COORDINATION_HEADING_PATTERNS = (
    re.compile(r"\bhandoff\b", re.IGNORECASE),
    re.compile(r"\bsession\s+log\b", re.IGNORECASE),
    re.compile(r"\bdecision(?:s|\s+log)?\b", re.IGNORECASE),
    re.compile(r"\bproject\s+status\b", re.IGNORECASE),
    re.compile(r"\bcheckpoint\b", re.IGNORECASE),
)


def excluded(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    parts = {part.lower() for part in rel.parts[:-1]}
    if any(part in EXCLUDED_DIRS for part in parts):
        return True
    if any(part in DATA_DIRS for part in parts):
        return True
    return False


def is_coordination_artifact(path: Path, root: Path) -> bool:
    """Return True for strong project-memory or coordination signals.

    This intentionally uses conservative structural signals rather than trying to
    infer arbitrary document semantics. Coordination artifacts remain available
    through ``--all-markdown`` when a broad audit is explicitly requested.
    """

    rel = path.relative_to(root)
    parent_parts = {part.lower() for part in rel.parts[:-1]}
    if any(part in PROJECT_MEMORY_DIRS for part in parent_parts):
        return True

    upper_name = path.name.upper()
    if upper_name in COORDINATION_EXACT_NAMES:
        return True
    if any(token in upper_name for token in COORDINATION_NAME_TOKENS):
        return True

    try:
        prefix = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return False

    first_h1 = FIRST_H1.search(prefix)
    if first_h1 is None:
        return False
    heading = first_h1.group(1)
    return any(pattern.search(heading) for pattern in COORDINATION_HEADING_PATTERNS)


def is_documentation_surface(path: Path, root: Path) -> bool:
    if is_coordination_artifact(path, root):
        return False

    rel = path.relative_to(root)
    if len(rel.parts) == 1:
        name = rel.name
        return name in ROOT_DOCUMENT_NAMES or name.startswith("README.")

    top = rel.parts[0].lower()
    if top == "docs":
        return True

    if top == "skills":
        return path.name == "SKILL.md" or "references" in {part.lower() for part in rel.parts}

    return False


def markdown_files(root: Path, all_markdown: bool = False) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*.md"):
        if not path.is_file() or excluded(path, root):
            continue
        if not all_markdown and not is_documentation_surface(path, root):
            continue
        result.append(path)
    return sorted(result)


def is_external(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "tel:", "#"))


def normalized_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split("#", 1)[0]
    if not target or is_external(raw_target):
        return None
    target = target.replace("%20", " ")
    return (source.parent / target).resolve()


def audit(root: Path, all_markdown: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    files = markdown_files(root, all_markdown=all_markdown)

    if not (root / "README.md").exists():
        warnings.append("Root README.md is missing")

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        if text.strip() and not HEADING.search(text) and path.name.upper() not in {"LICENSE.MD"}:
            warnings.append(f"{rel}: no Markdown heading detected")

        for match in MARKDOWN_LINK.finditer(text):
            target = normalized_target(path, match.group(1))
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{rel}: broken local link -> {match.group(1)}")

    capability_index = root / "docs" / "CAPABILITIES.md"
    functionality = root / "docs" / "functionality"
    if functionality.is_dir() and any(functionality.glob("*.md")) and not capability_index.exists():
        warnings.append("docs/functionality contains capability documents but docs/CAPABILITIES.md is missing")

    skill_files = [path for path in files if path.name == "SKILL.md"]
    for skill in skill_files:
        text = skill.read_text(encoding="utf-8", errors="replace")
        rel = skill.relative_to(root).as_posix()
        if not text.startswith("---\n"):
            errors.append(f"{rel}: missing YAML frontmatter")
        if "name:" not in text[:2000]:
            errors.append(f"{rel}: frontmatter appears to lack name")
        if "description:" not in text[:4000]:
            errors.append(f"{rel}: frontmatter appears to lack description")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--all-markdown",
        action="store_true",
        help="Audit every Markdown file instead of documentation surfaces only",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors, warnings = audit(root, all_markdown=args.all_markdown)

    for message in warnings:
        print(f"WARN: {message}")
    for message in errors:
        print(f"ERROR: {message}")

    print(f"Audit complete: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
