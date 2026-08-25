#!/usr/bin/env python3
"""coverage-report — what the brief asked for, and what canon actually covers.

Two diffs:

  1. **`brief_requirements[]` against `brief_requirement_coverage.rows`.**
     R8 enumerated the brief's 150 requirements from the brief alone, without
     seeing canon. This tool DIFFS that enumerated list; it must never
     re-extract requirements from the brief, because seven requirement blocks
     live in fenced code blocks and are invisible to list extraction. Every
     BR id needs a coverage row, every `satisfied_by` reference must resolve
     inside canon, and the two build-process requirements must carry an empty
     `satisfied_by` with a stated reason — marking them satisfied by content
     would be false.

  2. **`file_manifest` against `schemas`.** Every manifest file maps to a prose
     schema or to one of the `non_prose_file_classes`, which are SATISFIED BY
     EXCLUSION — canon, tool and build files have no prose schema, and
     reporting them as twelve unmapped rows would be noise. Every prose schema
     must own at least one file, and the manifest's own arithmetic must hold.

Files that do not exist yet are reported as "not yet generated", never as
uncovered: this report is meant to be usable while the repository is still
being built.

Usage
    tools/coverage-report.py            # human-readable report
    tools/coverage-report.py --quiet    # failures only

Exit code is 0 when nothing is unmapped and 1 otherwise.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"

# Directories holding runtime artifacts rather than manifest files.
UNTRACKED_DIRS = ("tools/fixtures/", "canon/deltas/", ".omc/", ".claude/", ".git/")


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
            print(f"\n{self.tool}: FAIL — {len(self.failures)} unmapped row(s)")
            return 1
        print(f"\n{self.tool}: ok" + (f" ({len(self.warnings)} warning(s))" if self.warnings else ""))
        return 0


def load_canon(path: Path = CANON_PATH) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def id_index(canon: dict) -> set[str]:
    ids: set[str] = set()

    def collect(node):
        if isinstance(node, dict):
            value = node.get("id")
            if isinstance(value, str) and value:
                ids.add(value)
            for child in node.values():
                collect(child)
        elif isinstance(node, list):
            for child in node:
                collect(child)

    collect(canon)
    return ids


# `satisfied_by` uses a compact path notation: `weeks[].tasks[].hours` descends
# into every element, `tracks.*.concepts[]` wildcards a mapping's values, a
# trailing annotation such as " (30)" or " SM-01..SM-07" is commentary, and a
# bare id like `checkpoints.CP-M3` is looked up by id anywhere beneath the node.
# `VERIFICATION section N` points at the build plan rather than at canon, and
# `C-047..C-069` names an inclusive id range.
EXTERNAL_REFERENCE_PREFIXES = ("VERIFICATION",)


def _expand(node):
    if isinstance(node, list):
        return list(node)
    if isinstance(node, dict):
        return list(node.values())
    return [node]


def _find_by_id(node, wanted: str, depth: int = 0):
    if depth > 6:
        return None
    if isinstance(node, dict):
        if node.get("id") == wanted or node.get("name") == wanted:
            return node
        for child in node.values():
            found = _find_by_id(child, wanted, depth + 1)
            if found is not None:
                return found
    elif isinstance(node, list):
        for child in node:
            found = _find_by_id(child, wanted, depth + 1)
            if found is not None:
                return found
    return None


def resolves(canon: dict, ids: set[str], reference: str) -> bool:
    """True when a satisfied_by entry names something that exists in canon."""
    text = reference.strip()
    if not text or text in ids:
        return True
    if text.startswith(EXTERNAL_REFERENCE_PREFIXES):
        return True  # the build plan's verification sections, satisfied outside canon
    if ".." in text and " " not in text:  # a bare id range, e.g. `C-047..C-069`
        first, _, last = text.partition("..")
        return first.strip() in ids and last.strip() in ids

    head = text.split(" ", 1)[0].rstrip(",;")
    nodes = [canon]
    for part in head.split("."):
        if not part:
            return False
        if part == "*":
            nodes = [value for node in nodes for value in _expand(node)]
            nodes = [n for n in nodes if n is not None]
            if not nodes:
                return False
            continue
        explode = part.endswith("[]")
        key = part[:-2] if explode else part
        found = []
        for node in nodes:
            if isinstance(node, dict) and key in node:
                found.append(node[key])
            elif isinstance(node, list):
                for item in node:
                    if isinstance(item, dict) and key in item:
                        found.append(item[key])
            if not found:
                match = _find_by_id(node, key)
                if match is not None:
                    found.append(match)
        if explode:
            found = [value for node in found for value in _expand(node)]
        nodes = [node for node in found if node is not None]
        if not nodes:
            return False
    return True


def check_brief_requirements(report: Report, canon: dict, ids: set[str], quiet: bool) -> None:
    requirements = canon.get("brief_requirements") or []
    coverage = canon.get("brief_requirement_coverage") or {}
    rows = {row["id"]: row for row in coverage.get("rows") or []}
    build_process = set(coverage.get("build_process_requirements") or [])

    declared = coverage.get("count")
    if declared is not None and declared != len(requirements):
        report.fail("canon/canon.yaml", None,
                    f"brief_requirement_coverage.count is {declared} but brief_requirements[] holds {len(requirements)}")

    for requirement in requirements:
        rid = requirement["id"]
        row = rows.get(rid)
        if row is None:
            report.fail("canon/canon.yaml", None,
                        f"{rid} ({requirement['section']}) has no brief_requirement_coverage row: "
                        f"\"{requirement['requirement'][:90]}\"")
            continue
        satisfied_by = row.get("satisfied_by") or []
        if rid in build_process:
            if satisfied_by:
                report.fail("canon/canon.yaml", None,
                            f"{rid} is a build-process requirement and must carry an empty satisfied_by; it lists {satisfied_by}")
            if not row.get("note") and not row.get("reason"):
                report.fail("canon/canon.yaml", None, f"{rid} is a build-process requirement with no stated reason")
            continue
        if not satisfied_by:
            report.fail("canon/canon.yaml", None,
                        f"{rid} ({requirement['section']}) is UNMAPPED — satisfied_by is empty: "
                        f"\"{requirement['requirement'][:90]}\"")
            continue
        for reference in satisfied_by:
            if not resolves(canon, ids, reference):
                report.fail("canon/canon.yaml", None,
                            f"{rid}: satisfied_by `{reference}` does not resolve to a canon id or path")

    orphan_rows = set(rows) - {requirement["id"] for requirement in requirements}
    for rid in sorted(orphan_rows):
        report.fail("canon/canon.yaml", None, f"brief_requirement_coverage row {rid} has no brief_requirements[] entry")

    if not quiet:
        by_section = Counter(requirement["section"] for requirement in requirements)
        print(f"brief requirements: {len(requirements)} row(s), "
              f"{len(build_process)} build-process, {len(requirements) - len(build_process)} content")
        for section, count in by_section.most_common():
            print(f"    {count:>4}  {section}")


def check_file_manifest(report: Report, canon: dict, quiet: bool) -> None:
    manifest = canon["file_manifest"]
    schemas = canon["schemas"]
    non_prose = {cls["name"]: cls for cls in schemas["non_prose_file_classes"]["classes"]}
    prose_schemas = {name for name, value in schemas.items()
                     if isinstance(value, dict) and "sections_in_order" in value}

    used: Counter[str] = Counter()
    missing_files: list[str] = []
    for entry in manifest["files"]:
        rel, schema = entry["path"], entry["schema"]
        used[schema] += 1
        if schema in non_prose:
            continue
        if schema not in prose_schemas:
            report.fail(rel, None, f"schema `{schema}` is neither a prose schema nor a non_prose_file_class — UNMAPPED")
            continue
        if not (REPO_ROOT / rel).exists():
            missing_files.append(rel)

    for schema in sorted(prose_schemas):
        if used[schema] == 0:
            report.fail("canon/canon.yaml", None, f"schema `{schema}` owns no file in file_manifest — UNMAPPED")

    declared_total = manifest.get("total")
    if declared_total is not None and declared_total != len(manifest["files"]):
        report.fail("canon/canon.yaml", None,
                    f"file_manifest.total is {declared_total} but files[] holds {len(manifest['files'])}")
    counted = sum(manifest.get("counts", {}).values())
    if manifest.get("counts") and counted != len(manifest["files"]):
        report.fail("canon/canon.yaml", None,
                    f"file_manifest.counts sums to {counted} but files[] holds {len(manifest['files'])}")

    for name, cls in non_prose.items():
        if used[name] != cls["files"]:
            report.fail("canon/canon.yaml", None,
                        f"non_prose_file_classes `{name}` declares {cls['files']} file(s) but file_manifest assigns {used[name]}")

    tracked = {entry["path"] for entry in manifest["files"]}
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel = str(path.relative_to(REPO_ROOT))
        if rel in tracked or rel.startswith(UNTRACKED_DIRS):
            continue
        report.warn(rel, None, "markdown file on disk with no file_manifest row")

    if not quiet:
        print(f"\nfile manifest: {len(manifest['files'])} file(s) = "
              f"{sum(used[s] for s in prose_schemas)} prose across {len(prose_schemas)} schema(s) + "
              f"{sum(used[n] for n in non_prose)} non-prose (satisfied by exclusion)")
        for schema in sorted(prose_schemas):
            present = sum(1 for entry in manifest["files"]
                          if entry["schema"] == schema and (REPO_ROOT / entry["path"]).exists())
            print(f"    {used[schema]:>4}  {schema:<12} {present} present")
        for name in sorted(non_prose):
            print(f"    {used[name]:>4}  {name:<12} excluded: {non_prose[name]['validated_by']}")

    for rel in missing_files:
        report.note(f"{rel}: not yet generated")


def main() -> int:
    parser = argparse.ArgumentParser(description="Diffs brief_requirements[] and file_manifest x schemas.")
    parser.add_argument("--quiet", action="store_true", help="print failures only, no coverage tables")
    parser.add_argument("--canon", default=str(CANON_PATH), help="canon file to report on (default canon/canon.yaml)")
    args = parser.parse_args()

    canon = load_canon(Path(args.canon))
    report = Report("coverage-report")
    ids = id_index(canon)

    check_brief_requirements(report, canon, ids, args.quiet)
    check_file_manifest(report, canon, args.quiet)
    print()
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
