#!/usr/bin/env python3
"""check-links — relative links resolve, anchors stay on the spine, nothing orphans.

Three checks, in canon's own words (schemas.universal_rules and the
file_manifest entry for this tool):

  1. Every relative link resolves to a file that exists or is a declared
     file_manifest path not yet generated.
  2. Anchor links are permitted only into SPINE files — the G4 wave's output,
     whose heading text canon fixes: README, ROADMAP, SCOREBOARD, HOW-TO-EDIT,
     `phases/*.md`, `reference/*.md` and `canon/CANON.md`. A same-file anchor
     is always permitted; you own your own headings. Anchoring into any other
     file couples prose to headings canon does not fix, and is flagged.
  3. No prose file is more than two hops from README.md.

No link may point outside the repository. Cited URLs (http, https, mailto) are
citations rather than repo links and are left alone; an absolute filesystem
path or a `../` escape is a failure.

Usage
    tools/check-links.py                 # the whole manifest
    tools/check-links.py FILE...         # arbitrary files (fixtures)

Exit code is 0 on pass and 1 on any failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"

MAX_HOPS = 2
ROOT_FILE = "README.md"

# `[text](target)` — the target stops at whitespace or the closing paren.
INLINE_LINK_RE = re.compile(r"\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")
SPINE_SCHEMAS = frozenset({"README", "ROADMAP", "SCOREBOARD", "phase", "reference"})
SPINE_EXTRA = frozenset({"HOW-TO-EDIT.md", "canon/CANON.md"})


class Report:
    """Collects failures, warnings and notes and renders them one per line."""

    def __init__(self, tool: str) -> None:
        self.tool = tool
        self.failures: list[tuple[str, int | None, str]] = []
        self.warnings: list[tuple[str, int | None, str]] = []
        self.notes: list[str] = []

    def fail(self, path: str, line: int | None, message: str) -> None:
        self.failures.append((str(path), line, message))

    def warn(self, path: str, line: int | None, message: str) -> None:
        self.warnings.append((str(path), line, message))

    def note(self, message: str) -> None:
        self.notes.append(message)

    @staticmethod
    def _where(path: str, line: int | None) -> str:
        return f"{path}:{line}" if line else f"{path}"

    def finish(self) -> int:
        for message in self.notes:
            print(f"note: {message}")
        for path, line, message in self.warnings:
            print(f"{self._where(path, line)}: warning: {message}")
        for path, line, message in sorted(self.failures, key=lambda f: (f[0], f[1] or 0)):
            print(f"{self._where(path, line)}: {message}")
        if self.failures:
            print(f"\n{self.tool}: FAIL — {len(self.failures)} failure(s)")
            return 1
        print(f"\n{self.tool}: ok" + (f" ({len(self.warnings)} warning(s))" if self.warnings else ""))
        return 0


def load_canon() -> dict:
    with CANON_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fenced_lines(lines: list[str]) -> set[int]:
    inside: set[int] = set()
    open_fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            inside.add(index)
            open_fence = not open_fence
            continue
        if open_fence:
            inside.add(index)
    return inside


def slug(text: str) -> str:
    """GitHub's heading anchor slug: lowercase, punctuation dropped, spaces hyphenated."""
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text).strip("-")


def heading_slugs(path: Path) -> set[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    skip = fenced_lines(lines)
    slugs = set()
    for index, line in enumerate(lines):
        if index in skip:
            continue
        match = re.match(r"^#{1,6}\s+(.*?)\s*$", line)
        if match:
            slugs.add(slug(match.group(1)))
    return slugs


def spine_paths(canon: dict) -> set[str]:
    paths = set(SPINE_EXTRA)
    for entry in canon["file_manifest"]["files"]:
        if entry["schema"] in SPINE_SCHEMAS:
            paths.add(entry["path"])
    return paths


def links_in(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    skip = fenced_lines(lines)
    found = []
    for index, line in enumerate(lines):
        if index in skip:
            continue
        # Strip inline code spans so `[foo](bar)` inside backticks is not a link.
        stripped = re.sub(r"`[^`]*`", "", line)
        for match in INLINE_LINK_RE.finditer(stripped):
            found.append((index + 1, match.group(1)))
    return found


def check_file(report: Report, rel: str, manifest: set[str], spine: set[str],
               graph: dict[str, set[str]]) -> None:
    path = REPO_ROOT / rel
    graph.setdefault(rel, set())
    for line, target in links_in(path):
        if target.startswith(EXTERNAL_SCHEMES):
            continue
        if target.startswith("#"):
            anchor = target[1:]
            if anchor and anchor not in heading_slugs(path):
                report.fail(rel, line, f"same-file anchor `{target}` matches no heading in this file")
            continue
        if target.startswith("/") or target.startswith("file:"):
            report.fail(rel, line, f"link `{target}` is an absolute path; links must be relative and inside the repository")
            continue

        file_part, _, anchor = target.partition("#")
        if not file_part:
            continue

        resolved = (path.parent / file_part).resolve()
        try:
            target_rel = str(resolved.relative_to(REPO_ROOT))
        except ValueError:
            report.fail(rel, line, f"link `{target}` resolves outside the repository ({resolved})")
            continue

        if not resolved.exists():
            if target_rel in manifest:
                report.note(f"{rel}:{line}: link target `{target_rel}` is a declared manifest file, not yet generated")
            else:
                report.fail(rel, line, f"link `{target}` resolves to `{target_rel}`, which does not exist and is not a file_manifest path")
                continue
        elif resolved.is_dir():
            report.fail(rel, line, f"link `{target}` resolves to a directory; link to a file")
            continue

        graph[rel].add(target_rel)

        if anchor:
            if target_rel not in spine:
                report.fail(rel, line,
                            f"anchor link `{target}` points into `{target_rel}`, which is not a spine file — "
                            "anchors are permitted only into files whose heading text canon fixes")
            elif resolved.exists() and anchor not in heading_slugs(resolved):
                report.fail(rel, line, f"anchor `#{anchor}` matches no heading in `{target_rel}`")


def check_orphans(report: Report, manifest_prose: list[str], graph: dict[str, set[str]]) -> None:
    if ROOT_FILE not in graph:
        report.note(f"{ROOT_FILE} not yet generated — the orphan check is deferred")
        return
    reachable = {ROOT_FILE}
    frontier = {ROOT_FILE}
    for _ in range(MAX_HOPS):
        nxt: set[str] = set()
        for node in frontier:
            for neighbour in graph.get(node, ()):
                if neighbour not in reachable:
                    reachable.add(neighbour)
                    nxt.add(neighbour)
        frontier = nxt
    for rel in manifest_prose:
        if rel == ROOT_FILE:
            continue
        if not (REPO_ROOT / rel).exists():
            continue
        if rel not in reachable:
            report.fail(rel, None, f"orphan: not reachable from {ROOT_FILE} within {MAX_HOPS} hops")


def main() -> int:
    parser = argparse.ArgumentParser(description="Relative links resolve; anchors restricted to spine files; no orphans beyond two hops.")
    parser.add_argument("paths", nargs="*", help="explicit files to check (skips the orphan sweep)")
    args = parser.parse_args()

    canon = load_canon()
    report = Report("check-links")
    manifest = {entry["path"] for entry in canon["file_manifest"]["files"]}
    non_prose = {cls["name"] for cls in canon["schemas"]["non_prose_file_classes"]["classes"]}
    manifest_prose = [entry["path"] for entry in canon["file_manifest"]["files"] if entry["schema"] not in non_prose]
    spine = spine_paths(canon)
    graph: dict[str, set[str]] = {}

    if args.paths:
        for raw in args.paths:
            path = Path(raw)
            rel = str(path.resolve().relative_to(REPO_ROOT)) if path.is_absolute() else raw
            if not (REPO_ROOT / rel).exists():
                report.fail(rel, None, "file does not exist")
                continue
            check_file(report, rel, manifest, spine, graph)
        return report.finish()

    present = 0
    for rel in manifest_prose:
        if not (REPO_ROOT / rel).exists():
            report.note(f"{rel}: not yet generated")
            continue
        present += 1
        check_file(report, rel, manifest, spine, graph)

    check_orphans(report, manifest_prose, graph)
    report.note(f"{present} of {len(manifest_prose)} prose file(s) present; spine is {len(spine)} file(s)")
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
