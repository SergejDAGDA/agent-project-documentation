#!/usr/bin/env python3
"""Run lightweight structural checks on repository Markdown documentation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)

EXCLUDED = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv"}


def markdown_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in EXCLUDED for part in path.parts):
            continue
        if path.is_file():
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


def audit(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    files = markdown_files(root)

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
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors, warnings = audit(root)

    for message in warnings:
        print(f"WARN: {message}")
    for message in errors:
        print(f"ERROR: {message}")

    print(f"Audit complete: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
