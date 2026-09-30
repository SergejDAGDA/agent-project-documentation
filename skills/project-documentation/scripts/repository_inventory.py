#!/usr/bin/env python3
"""Create a compact, deterministic inventory of a source repository."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Iterable

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    ".venv",
    "venv",
    "target",
}

DOC_NAMES = {
    "readme.md",
    "agents.md",
    "claude.md",
    "contributing.md",
    "changelog.md",
    "security.md",
    "license",
    "license.md",
}

MANIFEST_NAMES = {
    "package.json",
    "pyproject.toml",
    "cargo.toml",
    "go.mod",
    "composer.json",
    "gemfile",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "requirements.txt",
    "plugin.json",
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}

EXTENSION_LANG = {
    ".py": "Python",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".h": "C/C++ header",
    ".hpp": "C++ header",
    ".swift": "Swift",
    ".dart": "Dart",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".sh": "Shell",
    ".ps1": "PowerShell",
}


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        current_path = Path(current)
        for name in sorted(files):
            path = current_path / name
            try:
                if path.is_symlink():
                    continue
            except OSError:
                continue
            yield path


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def classify_repository(paths: list[str]) -> list[str]:
    lower = [p.lower() for p in paths]
    kinds: list[str] = []

    if any(p.endswith("skill.md") for p in lower):
        kinds.append("agent-skill")
    if ".claude-plugin/plugin.json" in lower:
        kinds.append("claude-code-plugin")
    if "plugin.json" in lower:
        kinds.append("openai-or-generic-plugin")
    if any(p == "package.json" or p.endswith("/package.json") for p in lower):
        kinds.append("javascript-or-typescript-project")
    if any(p == "pyproject.toml" or p.endswith("/pyproject.toml") for p in lower):
        kinds.append("python-project")
    if any(p == "cargo.toml" or p.endswith("/cargo.toml") for p in lower):
        kinds.append("rust-project")
    if any(p == "go.mod" or p.endswith("/go.mod") for p in lower):
        kinds.append("go-project")
    if any("/migrations/" in f"/{p}/" for p in lower):
        kinds.append("persistent-data-project")
    if any(p.startswith(".github/workflows/") for p in lower):
        kinds.append("github-actions")

    return kinds or ["unclassified"]


def build_inventory(root: Path) -> dict:
    files = list(iter_files(root))
    paths = [relative(path, root) for path in files]
    language_counts: Counter[str] = Counter()
    extension_counts: Counter[str] = Counter()

    for path in files:
        ext = path.suffix.lower()
        if ext:
            extension_counts[ext] += 1
        language = EXTENSION_LANG.get(ext)
        if language:
            language_counts[language] += 1

    docs = [p for p in paths if Path(p).name.lower() in DOC_NAMES or p.lower().startswith("docs/")]
    manifests = [p for p in paths if Path(p).name.lower() in MANIFEST_NAMES or p == ".claude-plugin/plugin.json"]
    skills = [p for p in paths if Path(p).name == "SKILL.md"]
    tests = [p for p in paths if "test" in Path(p).name.lower() or "/tests/" in f"/{p.lower()}/"]

    top_level = sorted({Path(p).parts[0] for p in paths if Path(p).parts})

    return {
        "root": str(root.resolve()),
        "repository_types": classify_repository(paths),
        "file_count": len(paths),
        "top_level_entries": top_level,
        "languages_by_file_count": dict(language_counts.most_common()),
        "extensions_by_file_count": dict(extension_counts.most_common(20)),
        "documentation_files": docs,
        "manifest_and_build_files": manifests,
        "skill_manifests": skills,
        "test_like_files": tests[:200],
    }


def to_markdown(data: dict) -> str:
    lines = [
        "# Repository Inventory",
        "",
        f"Files: {data['file_count']}",
        "",
        "## Detected types",
        "",
    ]
    lines.extend(f"- {value}" for value in data["repository_types"])

    lines.extend(["", "## Languages", ""])
    if data["languages_by_file_count"]:
        lines.extend(f"- {name}: {count}" for name, count in data["languages_by_file_count"].items())
    else:
        lines.append("- No common source language detected")

    for title, key in [
        ("Documentation", "documentation_files"),
        ("Manifests and build files", "manifest_and_build_files"),
        ("Agent Skills", "skill_manifests"),
    ]:
        lines.extend(["", f"## {title}", ""])
        values = data[key]
        if values:
            lines.extend(f"- `{value}`" for value in values)
        else:
            lines.append("- None detected")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="Write output to this path instead of stdout")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"Repository root does not exist: {root}")

    data = build_inventory(root)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else to_markdown(data)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
