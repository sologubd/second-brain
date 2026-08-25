#!/usr/bin/env python3
"""check-dupes — 12-gram shingled overlap between prose files.

Any run of 12 consecutive words shared by two prose files is a duplicated span.
Duplication is not always a defect: canon lists eleven facts the plan
deliberately repeats, because a reader who is falling behind needs the
never-double-up rule wherever they happen to be standing, not only in README.
Those live in `canon.check_dupes.exemptions[]`.

An exemption suppresses a span only when BOTH conditions hold:

  * both files match the exemption's `appears_in` globs, AND
  * the span shares at least two content words with the exemption's `fact`.

The second condition is what stops `README.md` + `phases/*.md` from becoming a
blanket licence to duplicate anything at all between those files.

Usage
    tools/check-dupes.py                   # the whole manifest
    tools/check-dupes.py FILE FILE ...     # arbitrary files (fixtures)
    tools/check-dupes.py --gram 12 --max-spans 0

Exit code is 0 on pass and 1 when non-exempt spans exceed the threshold.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from itertools import combinations
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"

DEFAULT_GRAM = 12
DEFAULT_MAX_SPANS = 0
MIN_SHARED_CONTENT_WORDS = 2

WORD_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = frozenset("""
a an and are as at be been but by for from had has have he her his if in into is it its
of on or that the their them then there these they this to was were what when which who
will with you your not no its it's do does did can could should would may might must
""".split())


class Report:
    """Collects failures, warnings and notes and renders them one per line."""

    def __init__(self, tool: str) -> None:
        self.tool = tool
        self.failures: list[tuple[str, int | None, str]] = []
        self.notes: list[str] = []

    def fail(self, path: str, line: int | None, message: str) -> None:
        self.failures.append((str(path), line, message))

    def note(self, message: str) -> None:
        self.notes.append(message)

    @staticmethod
    def _where(path: str, line: int | None) -> str:
        return f"{path}:{line}" if line else f"{path}"

    def finish(self) -> int:
        for message in self.notes:
            print(f"note: {message}")
        for path, line, message in sorted(self.failures, key=lambda f: (f[0], f[1] or 0)):
            print(f"{self._where(path, line)}: {message}")
        if self.failures:
            print(f"\n{self.tool}: FAIL — {len(self.failures)} duplicated span(s)")
            return 1
        print(f"\n{self.tool}: ok")
        return 0


def load_canon() -> dict:
    with CANON_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def tokenize(text: str) -> tuple[list[str], list[int]]:
    """Words and the 1-based source line of each, with code fences, HTML
    comments and link targets removed."""
    lines = text.splitlines()
    words: list[str] = []
    origins: list[int] = []
    open_fence = False
    for number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            open_fence = not open_fence
            continue
        if open_fence:
            continue
        cleaned = re.sub(r"<!--.*?-->", " ", line)
        cleaned = re.sub(r"\]\([^)]*\)", "] ", cleaned)
        for word in WORD_RE.findall(cleaned.lower()):
            words.append(word)
            origins.append(number)
    return words, origins


def shingle_positions(words: list[str], gram: int) -> dict[tuple[str, ...], list[int]]:
    table: dict[tuple[str, ...], list[int]] = {}
    for index in range(len(words) - gram + 1):
        table.setdefault(tuple(words[index : index + gram]), []).append(index)
    return table


def merge_runs(positions: list[int]) -> list[tuple[int, int]]:
    """Consecutive shingle positions become one span [start, end]."""
    spans: list[tuple[int, int]] = []
    for position in sorted(positions):
        if spans and position == spans[-1][1] + 1:
            spans[-1] = (spans[-1][0], position)
        else:
            spans.append((position, position))
    return spans


def content_words(text: str) -> set[str]:
    return {word for word in WORD_RE.findall(text.lower()) if word not in STOPWORDS and len(word) > 3}


class Exemption:
    __slots__ = ("id", "fact", "globs", "words", "reason", "whole_pair", "anchor")

    def __init__(self, row: dict) -> None:
        self.id = row["id"]
        self.fact = row["fact"]
        self.globs = [entry.split("#", 1)[0] for entry in row.get("appears_in") or []]
        self.words = content_words(self.fact)
        self.reason = row.get("reason", "")
        # `whole_pair: true` exempts EVERY span between the named files, not only spans
        # sharing content words with `fact`. Added at G6 for a collision class the
        # word-overlap test structurally cannot cover: exercises/agent-failures.md renders
        # all 14 failure-exercise bodies and schemas.week.rules requires every week to
        # render its own, so 31 spans exist whose only shared vocabulary is the body text
        # itself -- which varies per exercise and therefore matches no single `fact`.
        # Use sparingly: it is the blunt instrument, and every use must argue in `reason`
        # why ANY overlap between those files is legitimate.
        self.whole_pair = bool(row.get("whole_pair"))
        # `anchor` narrows `whole_pair` to pairs that INCLUDE the owning home file. Added at
        # G6 after lane L5 measured the blanket version: 448 of 2,080 prose file pairs (21.5%)
        # were exempt, including every week-to-week and month-to-month pair, so the checker
        # could no longer see copy-paste between siblings. All three motivating defects were
        # between an authored file and its owning home -- never between siblings -- and L5
        # demonstrated the cost by re-running with exemptions disabled and finding its own
        # stock clauses duplicated across eight month files, invisible behind the blanket.
        anchor = row.get("anchor")
        # A string or a list; fnmatch has no brace expansion, so multi-anchor rows pass a list.
        self.anchor = [anchor] if isinstance(anchor, str) else (anchor or [])

    def covers_pair(self, left: str, right: str) -> bool:
        if not (self._matches(left) and self._matches(right)):
            return False
        if self.whole_pair and self.anchor:
            # Sibling-to-sibling pairs are NOT exempt: the mandated collision is always
            # against the file that owns the text.
            return any(fnmatch.fnmatch(left, a) or fnmatch.fnmatch(right, a) for a in self.anchor)
        return True

    def _matches(self, path: str) -> bool:
        return any(fnmatch.fnmatch(path, glob) for glob in self.globs)

    def covers_span(self, span_text: str) -> bool:
        if self.whole_pair:
            return True
        return len(self.words & content_words(span_text)) >= MIN_SHARED_CONTENT_WORDS


def main() -> int:
    parser = argparse.ArgumentParser(description="12-gram shingled overlap between prose files.")
    parser.add_argument("paths", nargs="*", help="explicit files to compare (default: the whole manifest)")
    parser.add_argument("--gram", type=int, default=DEFAULT_GRAM, help=f"shingle length (default {DEFAULT_GRAM})")
    parser.add_argument("--max-spans", type=int, default=DEFAULT_MAX_SPANS,
                        help=f"non-exempt duplicated spans tolerated (default {DEFAULT_MAX_SPANS})")
    args = parser.parse_args()

    canon = load_canon()
    report = Report("check-dupes")
    exemptions = [Exemption(row) for row in (canon.get("check_dupes") or {}).get("exemptions") or []]

    if args.paths:
        candidates = []
        for raw in args.paths:
            path = Path(raw)
            candidates.append(str(path.resolve().relative_to(REPO_ROOT)) if path.is_absolute() else raw)
    else:
        non_prose = {cls["name"] for cls in canon["schemas"]["non_prose_file_classes"]["classes"]}
        candidates = [entry["path"] for entry in canon["file_manifest"]["files"] if entry["schema"] not in non_prose]

    corpus: dict[str, tuple[list[str], list[int], dict]] = {}
    for rel in candidates:
        path = REPO_ROOT / rel
        if not path.exists():
            report.note(f"{rel}: not yet generated")
            continue
        words, origins = tokenize(path.read_text(encoding="utf-8"))
        if len(words) < args.gram:
            report.note(f"{rel}: fewer than {args.gram} words, nothing to shingle")
            continue
        corpus[rel] = (words, origins, shingle_positions(words, args.gram))

    span_count = 0
    exempted = 0
    for left, right in combinations(sorted(corpus), 2):
        left_words, left_origins, left_table = corpus[left]
        _, right_origins, right_table = corpus[right]
        shared = set(left_table) & set(right_table)
        if not shared:
            continue
        positions = [position for shingle in shared for position in left_table[shingle]]
        for start, end in merge_runs(positions):
            text = " ".join(left_words[start : end + args.gram])
            applicable = [e for e in exemptions if e.covers_pair(left, right) and e.covers_span(text)]
            if applicable:
                exempted += 1
                continue
            span_count += 1
            other_line = right_origins[right_table[tuple(left_words[start : start + args.gram])][0]]
            preview = text if len(text) <= 140 else text[:137] + "..."
            report.fail(left, left_origins[start],
                        f"{end - start + args.gram} words shared with {right}:{other_line} — \"{preview}\"")

    if span_count and span_count <= args.max_spans:
        report.failures.clear()
        report.note(f"{span_count} duplicated span(s), within the tolerated threshold of {args.max_spans}")

    report.note(f"{len(corpus)} file(s) compared at {args.gram}-gram; "
                f"{exempted} span(s) exempt under {len(exemptions)} canon exemption(s)")
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
