#!/usr/bin/env python3
"""check-antigoals — canon's twelve anti-goals, two of them conditional.

Ten anti-goals are unconditional. Two are not, and getting them wrong in either
direction is a real failure:

  AG-08  LeetCode      — barred UNLESS justified for the objective.
  AG-09  Kubernetes    — barred ONLY when the reason is "industry standard".

Canon is explicit (`anti_goals.conditional_handling.rule`): this checker MUST
NOT hard-ban either string. The brief itself asks "Do I need Kubernetes?" as a
question the repository must ANSWER, and answering requires naming it. A flat
ban would make canon's own honest treatment of the question a lint failure.
So both are matched on the JUSTIFICATION PATTERN instead:

  * LeetCode is flagged when it appears with no justification or deferral
    statement in the same section.
  * Kubernetes is flagged when "industry standard" is the adjacent reason. A
    Kubernetes mention with no justification at all is a warning, per
    `conditional_handling.implementation`, not a hard failure.
  * The `low_roi[]` rows that answer both questions are registered as permitted
    occurrences and are never flagged.

Two further mechanical checks stand behind the unconditional anti-goals:

  AG-12  every `## Acceptance criteria` line carries a number, an artifact path
         or a binary predicate — never "I studied it".
  AG-02  no list longer than ten items without P0–P3 priority tags.
  AG-07  no certification in the portfolio or the competency matrix.

Usage
    tools/check-antigoals.py             # the whole manifest
    tools/check-antigoals.py FILE...     # arbitrary files (fixtures)

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

MAX_UNTAGGED_LIST_ITEMS = 10
PRIORITY_TAG_RE = re.compile(r"\bP[0-3]\b")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")
INDUSTRY_STANDARD_RE = re.compile(r"industry[- ]standard", re.I)

# A justification or deferral is any of these, in the same section.
JUSTIFICATION_RE = re.compile(
    r"\bunless\b|\bjustif\w*|\bdefer\w*|\bnot needed\b|\bno surface\b|\blow[- ]roi\b"
    r"|\bskip\b|\bconditional\w*|\bonly if\b|\bif a client\b|\bnot required\b"
    r"|\bwe do not\b|\bwe don't\b|\bexcluded\b|\bverdict\b|\bNO —|\bNO,",
    re.I,
)

# An acceptance criterion is binary when it asserts something checkable.
BINARY_PREDICATE_RE = re.compile(
    r"\bexits?\s+\d\b|\bexit code\b|\bpasses?\b|\bfails?\b|\breturns?\b|\bcontains?\b"
    r"|\bis (?:true|false|present|absent|empty|non-empty)\b|\bno\s+\w+\s+(?:appears|remains|is)\b"
    r"|\bat least\b|\bat most\b|\bexactly\b|\bzero\b|\bnone\b|[<>]=?|==|\bparses\b|\bresolves\b",
    re.I,
)
NUMBER_RE = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
ARTIFACT_PATH_RE = re.compile(r"`[^`]*[/.][^`]*`|\b[\w./-]+\.(?:md|py|ya?ml|json|jsonl|csv|sql|toml)\b|\b\w+/[\w./-]+")


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


def comment_lines(lines: list[str]) -> set[int]:
    """Indices of lines inside `<!-- ... -->` blocks. A comment is scaffolding,
    not prose: an id or a figure mentioned there is not a claim the file makes."""
    inside: set[int] = set()
    open_comment = False
    for index, line in enumerate(lines):
        if open_comment:
            inside.add(index)
            if "-->" in line:
                open_comment = False
            continue
        if "<!--" in line:
            inside.add(index)
            if "-->" not in line.split("<!--", 1)[1]:
                open_comment = True
    return inside


def sections(lines: list[str]) -> list[tuple[int, int, str]]:
    """(start, end, title) blocks delimited by consecutive headings."""
    skip = fenced_lines(lines)
    marks = [(index, re.match(r"^#{1,6}\s+(.*?)\s*$", line))
             for index, line in enumerate(lines) if index not in skip]
    headings = [(index, match.group(1)) for index, match in marks if match]
    blocks = []
    for position, (index, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        blocks.append((index, end, title))
    if not headings:
        blocks.append((0, len(lines), ""))
    elif headings[0][0] > 0:
        blocks.insert(0, (0, headings[0][0], ""))
    return blocks


def registered_occurrences(canon: dict) -> dict[str, tuple[str, str]]:
    """{token: (row id, home file)} for the low_roi rows canon registers as permitted."""
    low_roi = canon.get("low_roi") or {}
    home = low_roi.get("home_file", "")
    registry: dict[str, tuple[str, str]] = {}
    rows = list(low_roi.get("brief_challenges") or []) + list(low_roi.get("additional_rows") or [])
    for row in rows:
        blob = " ".join(str(value) for value in row.values())
        for token in ("LeetCode", "Kubernetes"):
            if token.lower() in blob.lower() and token not in registry:
                registry[token] = (row["id"], home)
    return registry


def check_conditional(report: Report, rel: str, lines: list[str], registry: dict[str, tuple[str, str]]) -> None:
    skip = fenced_lines(lines) | comment_lines(lines)
    for start, end, title in sections(lines):
        block = "\n".join(lines[start:end])
        justified = bool(JUSTIFICATION_RE.search(block))
        industry_standard = bool(INDUSTRY_STANDARD_RE.search(block))
        for index in range(start, end):
            if index in skip:
                continue
            line = lines[index]

            if re.search(r"\bleetcode\b", line, re.I):
                row_id, home = registry.get("LeetCode", ("", ""))
                if rel == home and row_id and row_id in block:
                    continue
                if not justified:
                    report.fail(rel, index + 1,
                                "AG-08: `LeetCode` appears with no justification or deferral statement in this section "
                                f"(`{title or 'preamble'}`). The ban is conditional on justification, not on the word — "
                                f"justify it for the objective or cite {row_id or 'the low_roi row'}.")

            if re.search(r"\bkubernetes\b", line, re.I):
                row_id, home = registry.get("Kubernetes", ("", ""))
                if rel == home and row_id and row_id in block:
                    continue
                if industry_standard:
                    report.fail(rel, index + 1,
                                "AG-09: `Kubernetes` is adjacent to the reason \"industry standard\" in this section "
                                f"(`{title or 'preamble'}`). That is the only reason canon bars — name a real surface instead.")
                elif not justified:
                    report.warn(rel, index + 1,
                                "AG-09: `Kubernetes` appears with no justification or deferral statement in this section "
                                f"(`{title or 'preamble'}`); canon's implementation clause expects one. Not a hard failure — "
                                "the ban is on the reason \"industry standard\", which does not appear here.")


def check_acceptance_criteria(report: Report, rel: str, lines: list[str]) -> None:
    for start, end, title in sections(lines):
        if title.strip().lower() != "acceptance criteria":
            continue
        for index in range(start + 1, end):
            line = lines[index]
            if not LIST_ITEM_RE.match(line):
                continue
            body = re.sub(r"^\s*(?:[-*+]|\d+\.)\s*(?:\[[ xX]\]\s*)?", "", line).strip()
            if not body:
                continue
            if NUMBER_RE.search(body) or ARTIFACT_PATH_RE.search(body) or BINARY_PREDICATE_RE.search(body):
                continue
            report.fail(rel, index + 1,
                        "AG-12: acceptance criterion carries no number, artifact path or binary predicate — "
                        f"\"{body[:90]}\"")


def check_untagged_lists(report: Report, rel: str, lines: list[str]) -> None:
    skip = fenced_lines(lines) | comment_lines(lines)
    run: list[int] = []

    def flush() -> None:
        if len(run) > MAX_UNTAGGED_LIST_ITEMS:
            tagged = sum(1 for index in run if PRIORITY_TAG_RE.search(lines[index]))
            if tagged < len(run):
                report.fail(rel, run[0] + 1,
                            f"AG-02: list of {len(run)} items with {len(run) - tagged} item(s) carrying no P0–P3 tag — "
                            f"a list longer than {MAX_UNTAGGED_LIST_ITEMS} needs priorities, or it is a giant list of technologies")
        run.clear()

    for index, line in enumerate(lines):
        if index in skip:
            flush()
            continue
        if LIST_ITEM_RE.match(line):
            run.append(index)
        elif line.strip():
            flush()
    flush()


def check_certifications(report: Report, rel: str, lines: list[str]) -> None:
    if not rel.endswith(("portfolio.md", "competency-matrix.md")):
        return
    skip = comment_lines(lines)
    for index, line in enumerate(lines):
        if index in skip:
            continue
        if re.search(r"\bcertif\w*", line, re.I) and not re.search(r"\bno certif|\bnever\b|\bnot a certif", line, re.I):
            report.fail(rel, index + 1,
                        "AG-07: a certification appears in the portfolio or competency matrix; "
                        "evidence is a runnable artifact or a measured number")


def main() -> int:
    parser = argparse.ArgumentParser(description="The twelve anti-goals, two of them conditional.")
    parser.add_argument("paths", nargs="*", help="explicit files to check (default: the whole manifest)")
    args = parser.parse_args()

    canon = load_canon()
    report = Report("check-antigoals")
    registry = registered_occurrences(canon)

    if args.paths:
        candidates = []
        for raw in args.paths:
            path = Path(raw)
            candidates.append(str(path.resolve().relative_to(REPO_ROOT)) if path.is_absolute() else raw)
    else:
        non_prose = {cls["name"] for cls in canon["schemas"]["non_prose_file_classes"]["classes"]}
        candidates = [entry["path"] for entry in canon["file_manifest"]["files"] if entry["schema"] not in non_prose]

    present = 0
    for rel in candidates:
        path = REPO_ROOT / rel
        if not path.exists():
            report.note(f"{rel}: not yet generated")
            continue
        present += 1
        lines = path.read_text(encoding="utf-8").splitlines()
        check_conditional(report, rel, lines, registry)
        check_acceptance_criteria(report, rel, lines)
        check_untagged_lists(report, rel, lines)
        check_certifications(report, rel, lines)

    permitted = ", ".join(f"{token} -> {row} in {home}" for token, (row, home) in sorted(registry.items()))
    report.note(f"{present} file(s) checked against {len(canon['anti_goals']['rows'])} anti-goals; "
                f"registered permitted occurrences: {permitted or 'none'}")
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
