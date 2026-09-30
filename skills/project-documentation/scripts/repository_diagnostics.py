#!/usr/bin/env python3
"""Collect conservative continuation and project-contamination signals.

The scanner is intentionally heuristic. It reports candidates for agent or human
review and never claims that a match is removable code or a confirmed secret.
Sensitive literal values are not included in output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".project-documentation",
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

TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env",
    ".sh", ".ps1", ".html", ".css", ".scss", ".xml", ".sql", ".go", ".rs",
    ".java", ".kt", ".rb", ".php", ".cs", ".cpp", ".c", ".h", ".hpp",
}

SOURCE_OR_CONFIG_SUFFIXES = TEXT_SUFFIXES - {".md", ".txt"}

MAINTENANCE_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)
LEGACY_RE = re.compile(r"\b(legacy|deprecated|obsolete|temporary|workaround|old[_ -]?(?:path|flow|impl|implementation|api))\b", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
WIN_USER_PATH_RE = re.compile(r"[A-Za-z]:\\(?:Users|Documents and Settings)\\[^\\\s]+", re.IGNORECASE)
UNIX_USER_PATH_RE = re.compile(r"/(?:Users|home)/[^/\s]+")
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret|client[_-]?secret)\b"
    r"\s*[:=]\s*[\"']([^\"']{6,})[\"']"
)
EXAMPLE_RE = re.compile(r"\b(example|sample|demo|fixture|placeholder)\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)

COMMON_URL_HOSTS = {
    "agent-plugins.org",
    "github.com",
    "api.github.com",
    "raw.githubusercontent.com",
    "npmjs.com",
    "www.npmjs.com",
    "pypi.org",
    "crates.io",
    "packagist.org",
    "maven.apache.org",
    "schemas.openxmlformats.org",
    "json-schema.org",
    "www.w3.org",
}


def iter_text_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        current_path = Path(current)
        for name in sorted(files):
            path = current_path / name
            if path.is_symlink():
                continue
            if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Dockerfile", "Gemfile"}:
                yield path


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def finding(kind: str, confidence: str, path: str, line: int, summary: str, context: str, recommendation: str) -> dict:
    return {
        "type": kind,
        "confidence": confidence,
        "path": path,
        "line": line,
        "summary": summary,
        "context": context,
        "recommendation": recommendation,
    }


def host_from_url(url: str) -> str:
    without_scheme = url.split("://", 1)[-1]
    return without_scheme.split("/", 1)[0].split(":", 1)[0].lower()


def is_test_like(path: Path, root: Path) -> bool:
    relative = path.relative_to(root).as_posix().lower()
    name = path.name.lower()
    return "/tests/" in f"/{relative}/" or name.startswith("test_") or name.endswith(".test.js") or name.endswith(".test.ts")


def scan_file(path: Path, root: Path, markers: list[str]) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    relative = rel(path, root)
    suffix = path.suffix.lower()
    results: list[dict] = []
    test_like = is_test_like(path, root)

    if path.resolve() == Path(__file__).resolve():
        return results

    if LEGACY_RE.search(path.stem):
        results.append(finding(
            "legacy-named-artifact", "suspected", relative, 0,
            "Filename contains a legacy or temporary marker",
            "historical",
            "review whether this artifact is still required",
        ))

    if EXAMPLE_RE.search(path.stem) and suffix in SOURCE_OR_CONFIG_SUFFIXES:
        results.append(finding(
            "example-artifact", "suspected", relative, 0,
            "Source or configuration filename looks example-derived",
            "unknown",
            "verify that example data has not become a production assumption",
        ))

    marker_patterns = [(marker, re.compile(re.escape(marker), re.IGNORECASE)) for marker in markers if marker.strip()]

    for number, line in enumerate(text.splitlines(), 1):
        if MAINTENANCE_RE.search(line) and suffix in SOURCE_OR_CONFIG_SUFFIXES and not test_like:
            results.append(finding(
                "maintenance-marker", "suspected", relative, number,
                "TODO, FIXME, HACK, or XXX marker found",
                "unknown",
                "review marker against the current implementation and project plan",
            ))

        if LEGACY_RE.search(line) and suffix in SOURCE_OR_CONFIG_SUFFIXES and not test_like:
            results.append(finding(
                "legacy-reference", "suspected", relative, number,
                "Legacy, deprecated, obsolete, temporary, or workaround reference found",
                "historical",
                "verify whether the referenced path or compatibility layer is still needed",
            ))

        if (WIN_USER_PATH_RE.search(line) or UNIX_USER_PATH_RE.search(line)) and not test_like:
            results.append(finding(
                "user-specific-path", "likely", relative, number,
                "User-specific absolute filesystem path found, value redacted",
                "user-specific",
                "move installation-specific paths into configuration or runtime discovery when appropriate",
            ))

        if (PRIVATE_KEY_RE.search(line) or SECRET_ASSIGNMENT_RE.search(line)) and not test_like:
            results.append(finding(
                "potential-secret", "likely", relative, number,
                "Credential-like value found, literal intentionally omitted",
                "sensitive",
                "review immediately with a dedicated secret or security scanner",
            ))

        if EMAIL_RE.search(line) and suffix in SOURCE_OR_CONFIG_SUFFIXES and not test_like:
            results.append(finding(
                "email-literal", "suspected", relative, number,
                "Email address literal found in source or configuration, value redacted",
                "unknown",
                "verify whether the address is intentional project identity, configuration, or user-specific data",
            ))

        if EXAMPLE_RE.search(line) and suffix in SOURCE_OR_CONFIG_SUFFIXES and not test_like:
            results.append(finding(
                "example-data-candidate", "suspected", relative, number,
                "Example, sample, demo, fixture, or placeholder marker found in source or configuration",
                "unknown",
                "verify that example context is not coupled to reusable production logic",
            ))

        if suffix in SOURCE_OR_CONFIG_SUFFIXES and not test_like:
            for url in URL_RE.findall(line):
                host = host_from_url(url.rstrip(".,)"))
                if host and host not in COMMON_URL_HOSTS and not host.endswith(".githubusercontent.com"):
                    results.append(finding(
                        "project-url-candidate", "suspected", relative, number,
                        "Non-common URL or domain literal found, literal omitted",
                        "unknown",
                        "verify whether the endpoint belongs in configuration or is intentionally part of product logic",
                    ))
                    break

        for marker, pattern in marker_patterns:
            if pattern.search(line):
                results.append(finding(
                    "known-context-marker", "likely", relative, number,
                    f"Known legacy or project-specific marker found: {marker}",
                    "project-specific",
                    "review whether this context should remain in the current project",
                ))

    return results


def collect(root: Path, markers: list[str] | None = None) -> dict:
    findings: list[dict] = []
    for path in iter_text_files(root):
        findings.extend(scan_file(path, root, markers or []))

    counts: dict[str, int] = {}
    for item in findings:
        counts[item["type"]] = counts.get(item["type"], 0) + 1

    return {
        "root": str(root.resolve()),
        "finding_count": len(findings),
        "counts_by_type": dict(sorted(counts.items())),
        "findings": findings,
        "notice": "Heuristic candidates only. Review before changing or removing code.",
    }


def to_markdown(data: dict) -> str:
    lines = [
        "# Repository Diagnostic Signals",
        "",
        data["notice"],
        "",
        f"Findings: {data['finding_count']}",
        "",
    ]
    if not data["findings"]:
        lines.append("No heuristic signals found.")
        return "\n".join(lines) + "\n"

    for item in data["findings"]:
        location = item["path"]
        if item["line"]:
            location += f":{item['line']}"
        lines.extend([
            f"## {item['type']}",
            "",
            f"- Confidence: {item['confidence']}",
            f"- Location: `{location}`",
            f"- Context: {item['context']}",
            f"- Signal: {item['summary']}",
            f"- Suggested action: {item['recommendation']}",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="Write output instead of stdout")
    parser.add_argument(
        "--marker",
        action="append",
        default=[],
        help="Known legacy, user, customer, source, or project marker to locate. Repeat as needed.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"Repository root does not exist: {root}")

    data = collect(root, args.marker)
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
