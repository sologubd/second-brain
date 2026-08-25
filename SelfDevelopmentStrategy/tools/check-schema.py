#!/usr/bin/env python3
"""check-schema — per-file structural conformance against canon.schemas.

Checks, per prose file in canon.file_manifest:

  * the required `sections_in_order`, in order, at the right heading level;
  * the schema's mechanically checkable `rules` (week files carry the most);
  * the per-schema word band, floor AND ceiling (the ceiling is the
    anti-padding control for AG-06 "motivational filler");
  * the placeholder lint: no TODO, no TBD, no `[[GAP:`, no empty section.

Files whose file_manifest schema is one of canon's `non_prose_file_classes`
(canon, tool, build) have no prose schema and are skipped by design, not
reported as unmapped.

Usage
    tools/check-schema.py                       # the whole manifest
    tools/check-schema.py --only weeks/         # a subset of the manifest
    tools/check-schema.py --schema week FILE... # arbitrary files (fixtures)
    tools/check-schema.py --build-time          # also: user regions are
                                                # placeholder-only

Exit code is 0 on pass and 1 on any failure. Failures print as
`path:line: message`.

This script deliberately depends on nothing but the standard library and
pyyaml, and shares no helper module with its siblings: canon's file_manifest
fixes the tool count at eight, and a ninth import target would make the
manifest arithmetic wrong. The small duplicated preamble is the price.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"
FIXTURE_DIR = "tools/fixtures/"

USER_REGION_OPEN = re.compile(r"<!--\s*user:actuals(?:\s+key=\"([^\"]*)\")?\s*-->")
USER_REGION_CLOSE = re.compile(r"<!--\s*/user:actuals\s*-->")
USER_REGION_PLACEHOLDER = "_(not yet logged)_"

PLACEHOLDER_TOKENS = ("TODO", "TBD", "[[GAP:")

TIME_BUDGET_LABELS = ("Theory", "Building", "Testing/evaluation", "Customer discovery")
TIME_BUDGET_TOTAL = 15.0

TASK_ID_RE = re.compile(r"\bT-[A-Za-z0-9]+-\d+\b")
TASK_HEADING_RE = re.compile(r"^Task\s+(\d+)\b")
CHECKBOX_RE = re.compile(r"^\s*-\s\[[ xX]\]\s")
LIST_ITEM_RE = re.compile(r"^\s*[-*+]\s")
NUMBERED_ITEM_RE = re.compile(r"^\s*(\d+)\.\s")
TRAILING_INT_RE = re.compile(r"(\d+)\s*$")

# The five named parts every failure-exercise body must contain. Each part is
# satisfied by any one of its patterns, so prose may phrase it naturally.
FAILURE_PARTS = (
    ("detection", (r"\bdetect(?:ion|s|ed|ing)?\b",)),
    (
        "safe failure behaviour",
        (r"safe\s+failure\s+behaviou?r", r"safe\s+behaviou?r", r"fail(?:s|ing)?\s+safe"),
    ),
    ("recovery", (r"\brecover(?:y|s|ed|ing)?\b",)),
    ("logging", (r"\blog(?:ging|s|ged)?\b",)),
    (
        "test proving the mitigation",
        (
            r"test\s+proving",
            r"proving\s+test",
            r"test\s+that\s+proves",
            r"proves\s+the\s+mitigation",
        ),
    ),
)


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
    """Indices of lines inside ``` fenced blocks, fences included."""
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


def user_regions(lines: list[str]) -> list[tuple[int, int, str]]:
    """(open_index, close_index, key) for each <!-- user:actuals --> region."""
    regions = []
    open_at: int | None = None
    key = ""
    for index, line in enumerate(lines):
        match = USER_REGION_OPEN.search(line)
        if match:
            open_at, key = index, match.group(1) or ""
            continue
        if USER_REGION_CLOSE.search(line) and open_at is not None:
            regions.append((open_at, index, key))
            open_at = None
    return regions


def user_region_line_indices(lines: list[str]) -> set[int]:
    covered: set[int] = set()
    for start, end, _ in user_regions(lines):
        covered.update(range(start, end + 1))
    return covered


class Heading:
    __slots__ = ("index", "level", "text")

    def __init__(self, index: int, level: int, text: str) -> None:
        self.index = index  # zero-based line index
        self.level = level
        self.text = text

    @property
    def line(self) -> int:
        return self.index + 1

    @property
    def marker(self) -> str:
        return f"{'#' * self.level} {self.text}"


def parse_headings(lines: list[str]) -> list[Heading]:
    skip = fenced_lines(lines)
    headings = []
    for index, line in enumerate(lines):
        if index in skip:
            continue
        match = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if match:
            headings.append(Heading(index, len(match.group(1)), match.group(2)))
    return headings


def body_of(heading: Heading, headings: list[Heading], lines: list[str]) -> tuple[int, int]:
    """Half-open line-index range of a heading's body, up to the next heading
    of the same or a shallower level."""
    position = headings.index(heading)
    for later in headings[position + 1 :]:
        if later.level <= heading.level:
            return heading.index + 1, later.index
    return heading.index + 1, len(lines)


def word_count(lines: list[str]) -> int:
    skip = fenced_lines(lines)
    text = " ".join(line for index, line in enumerate(lines) if index not in skip)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"[|#>*_`\[\]()]", " ", text)
    return len(text.split())


def is_fixture(path: str) -> bool:
    return path.replace("\\", "/").startswith(FIXTURE_DIR) or "/tools/fixtures/" in path.replace("\\", "/")


# --------------------------------------------------------------------------
# section-structure checks
# --------------------------------------------------------------------------


def check_sections(report: Report, rel: str, schema_name: str, schema: dict,
                   lines: list[str], headings: list[Heading]) -> dict[str, Heading]:
    """Verify sections_in_order and return {section marker: heading}."""
    required = schema.get("sections_in_order") or []
    if not required:
        return {}

    required_level = len(required[0].split(" ", 1)[0])
    found = [h for h in headings if h.level == required_level]
    found_markers = [h.marker for h in found]

    # Files that nest repeated sub-bodies (exercises) and the documented
    # HOW-TO-EDIT exception carry extra sections at the same level, so the
    # requirement there is order-preserving containment rather than equality.
    loose = bool(schema.get("per_exercise_sections_in_order")) or rel == "HOW-TO-EDIT.md"

    index = 0
    positions: dict[str, Heading] = {}
    for marker in required:
        while index < len(found_markers) and found_markers[index] != marker:
            index += 1
        if index == len(found_markers):
            report.fail(rel, None, f"schema `{schema_name}`: required section `{marker}` is missing or out of order")
            index = 0
            continue
        positions[marker] = found[index]
        index += 1

    if not loose:
        unexpected = [h for h in found if h.marker not in required]
        for heading in unexpected:
            report.fail(rel, heading.line, f"schema `{schema_name}`: unexpected section `{heading.marker}` (schema fixes exactly {len(required)} sections)")
        if len(found) == len(required) and found_markers != required and not report.failures:
            report.fail(rel, None, f"schema `{schema_name}`: sections are present but out of order")

    for heading in headings:
        if heading.level == required_level and heading.marker in required:
            start, end = body_of(heading, headings, lines)
            if not any(line.strip() for line in lines[start:end]):
                report.fail(rel, heading.line, f"empty section `{heading.marker}` (placeholder lint: no empty sections)")

    title = next((h for h in headings if h.level == 1), None)
    if title is None:
        report.fail(rel, 1, f"schema `{schema_name}`: no level-1 title (expected `{schema.get('title_pattern', '# Title')}`)")
    return positions


# --------------------------------------------------------------------------
# week rules
# --------------------------------------------------------------------------


def check_week(report: Report, rel: str, lines: list[str], headings: list[Heading],
               positions: dict[str, Heading], canon: dict) -> None:
    def section_lines(marker: str) -> tuple[int, int] | None:
        heading = positions.get(marker)
        if heading is None:
            return None
        return body_of(heading, headings, lines)

    # --- `## Time budget`: the brief's four literal labels, summing to 15.0
    span = section_lines("## Time budget")
    if span:
        start, end = span
        rows = []
        for index in range(start, end):
            match = re.match(r"^\s*-\s*([^:]+):\s*([0-9]+(?:\.[0-9]+)?)", lines[index])
            if match:
                rows.append((index + 1, match.group(1).strip(), float(match.group(2))))
        labels = [label for _, label, _ in rows]
        if labels != list(TIME_BUDGET_LABELS):
            report.fail(rel, positions["## Time budget"].line,
                        "`## Time budget` must render exactly the brief's literal labels "
                        f"{list(TIME_BUDGET_LABELS)} in that order; found {labels}")
        total = sum(value for _, _, value in rows)
        if rows and abs(total - TIME_BUDGET_TOTAL) > 1e-9:
            report.fail(rel, positions["## Time budget"].line,
                        f"`## Time budget` values sum to {total:g}, expected {TIME_BUDGET_TOTAL:g}")

    # --- `## Tasks`: `### Task N`, numbered, at least two, each with an id
    task_headings: list[Heading] = []
    span = section_lines("## Tasks")
    if span:
        start, end = span
        task_headings = [h for h in headings if start <= h.index < end and h.level == 3 and TASK_HEADING_RE.match(h.text)]
        if len(task_headings) < 2:
            report.fail(rel, positions["## Tasks"].line,
                        f"`## Tasks` has {len(task_headings)} `### Task N` heading(s); the week schema requires at least two")
        for expected, heading in enumerate(task_headings, start=1):
            number = int(TASK_HEADING_RE.match(heading.text).group(1))
            if number != expected:
                report.fail(rel, heading.line, f"task headings must be consecutive from 1; found `### {heading.text}` where `### Task {expected}` was expected")

    # --- `## Deliverables` / `## Acceptance criteria` are `- [ ]` lists
    deliverable_cap = int((canon.get("meta") or {}).get("deliverables_cap", 4))
    for marker, cap in (("## Deliverables", deliverable_cap), ("## Acceptance criteria", None)):
        span = section_lines(marker)
        if not span:
            continue
        start, end = span
        items = [(i + 1, lines[i]) for i in range(start, end) if LIST_ITEM_RE.match(lines[i])]
        if not items:
            report.fail(rel, positions[marker].line, f"`{marker}` must be a GitHub checkbox list using `- [ ]`; no list items found")
        for line_number, line in items:
            if not CHECKBOX_RE.match(line):
                report.fail(rel, line_number, f"`{marker}` items must use the `- [ ]` checkbox form; found `{line.strip()[:60]}`")
        if cap is not None and len(items) > cap:
            report.fail(rel, positions[marker].line, f"`{marker}` lists {len(items)} items; canon caps it at {cap}")

    # --- the Tasks-to-Acceptance reference rule
    acceptance_span = section_lines("## Acceptance criteria")
    if task_headings and acceptance_span:
        start, end = acceptance_span
        acceptance_text = "\n".join(lines[start:end])
        for heading in task_headings:
            t_start, t_end = body_of(heading, headings, lines)
            ids = TASK_ID_RE.findall("\n".join(lines[heading.index : t_end]))
            if not ids:
                report.fail(rel, heading.line,
                            f"`### {heading.text}` states no task id (expected a `T-wNN-K` id); the Tasks-to-Acceptance rule is enforced through the id")
                continue
            if not any(task_id in acceptance_text for task_id in ids):
                report.fail(rel, heading.line,
                            f"`### {heading.text}` ({', '.join(sorted(set(ids)))}) is referenced by no `## Acceptance criteria` line — "
                            "every task must be referenced by at least one acceptance criterion")

    # --- each task states its hours and its primary track
    for heading in task_headings:
        t_start, t_end = body_of(heading, headings, lines)
        body = "\n".join(lines[t_start:t_end])
        if not re.search(r"\b\d+(?:\.\d+)?\s*h\b", body, re.I):
            report.fail(rel, heading.line, f"`### {heading.text}` does not state its hours")
        if not re.search(r"\btrack\s+[A-FP]\b", body, re.I):
            report.fail(rel, heading.line, f"`### {heading.text}` does not name its primary track")

    # --- `## Reflection`: numbered, at least three
    span = section_lines("## Reflection")
    if span:
        start, end = span
        numbered = [i for i in range(start, end) if NUMBERED_ITEM_RE.match(lines[i])]
        if len(numbered) < 3:
            report.fail(rel, positions["## Reflection"].line,
                        f"`## Reflection` is a numbered list with at least three entries; found {len(numbered)}")

    # --- `## Weekly score`: allocations sum to 100
    span = section_lines("## Weekly score")
    if span:
        start, end = span
        allocations = []
        for index in range(start, end):
            if LIST_ITEM_RE.match(lines[index]) or NUMBERED_ITEM_RE.match(lines[index]):
                match = TRAILING_INT_RE.search(lines[index].rstrip().rstrip("."))
                if match:
                    allocations.append(int(match.group(1)))
        if not allocations:
            report.fail(rel, positions["## Weekly score"].line,
                        "`## Weekly score` must list explicit scoring rules, each ending in its point allocation")
        elif sum(allocations) != 100:
            report.fail(rel, positions["## Weekly score"].line,
                        f"`## Weekly score` allocations sum to {sum(allocations)}, expected 100 (found {allocations})")

    # --- `## Stretch goal` and `## Failure exercise` populated, five parts
    for marker in ("## Stretch goal", "## Failure exercise"):
        span = section_lines(marker)
        if span and not any(line.strip() for line in lines[span[0] : span[1]]):
            report.fail(rel, positions[marker].line, f"`{marker}` must be POPULATED in every concrete week file, not merely present")

    span = section_lines("## Failure exercise")
    if span:
        check_five_parts(report, rel, positions["## Failure exercise"].line, "\n".join(lines[span[0] : span[1]]),
                         "`## Failure exercise`")


def check_five_parts(report: Report, rel: str, line: int, text: str, label: str) -> None:
    lowered = text.lower()
    missing = [name for name, patterns in FAILURE_PARTS
               if not any(re.search(pattern, lowered) for pattern in patterns)]
    if missing:
        report.fail(rel, line, f"{label} is missing named part(s): {', '.join(missing)} — all five of "
                               "detection, safe failure behaviour, recovery, logging and a test proving the mitigation are required")


# --------------------------------------------------------------------------
# other schema-specific rules
# --------------------------------------------------------------------------


def check_month(report: Report, rel: str, lines: list[str], headings: list[Heading],
                positions: dict[str, Heading], canon: dict) -> None:
    heading = positions.get("## Retrospective")
    if heading is None:
        return
    start, end = body_of(heading, headings, lines)
    body = "\n".join(lines[start:end])
    retro = (canon.get("question_sets") or {}).get("monthly_retrospective") or {}
    for question in retro.get("questions") or []:
        if question["text"] not in body:
            report.fail(rel, heading.line,
                        f"`## Retrospective` does not reproduce {question['id']} verbatim: \"{question['text']}\"")
    eleventh = retro.get("eleventh_output") or {}
    if eleventh and eleventh.get("id") not in body:
        report.fail(rel, heading.line, f"`## Retrospective` does not carry {eleventh.get('id')}'s canon-delta output")


def check_resources(report: Report, rel: str, lines: list[str], headings: list[Heading],
                    positions: dict[str, Heading], schema: dict) -> None:
    heading = positions.get("## Resources")
    if heading is None:
        return
    start, end = body_of(heading, headings, lines)
    entries = [h for h in headings if start <= h.index < end and h.level == 3]
    if not entries:
        report.fail(rel, heading.line, "`## Resources` lists no resource entries (expected one `###` heading per resource)")
    for entry in entries:
        e_start, e_end = body_of(entry, headings, lines)
        body = "\n".join(lines[e_start:e_end]).lower()
        missing = [field for field in schema.get("per_resource_fields") or [] if field.lower() not in body]
        if missing:
            report.fail(rel, entry.line,
                        f"resource `{entry.text}` is missing mandated field(s): {'; '.join(missing)}")


def check_exercises(report: Report, rel: str, lines: list[str], headings: list[Heading],
                    positions: dict[str, Heading], schema: dict, skip_word_band: bool) -> None:
    heading = positions.get("## Exercises")
    if heading is None:
        return
    start, end = body_of(heading, headings, lines)
    bodies = [h for h in headings if start <= h.index < end and h.level == 3]
    if not bodies:
        report.fail(rel, heading.line, "`## Exercises` contains no exercise bodies (expected one `###` heading per exercise)")
    parts = [p.lstrip("# ").strip() for p in schema.get("per_exercise_sections_in_order") or []]
    band = schema.get("exercise_body_word_band")
    for body_heading in bodies:
        b_start, b_end = body_of(body_heading, headings, lines)
        body_text = "\n".join(lines[b_start:b_end]).lower()
        missing = [part for part in parts if part.lower() not in body_text]
        if missing:
            report.fail(rel, body_heading.line,
                        f"exercise `{body_heading.text}` is missing part(s): {', '.join(missing)} "
                        f"(all {len(parts)} parts of the exercise shape are required, in order)")
        if band and not skip_word_band:
            count = word_count(lines[b_start:b_end])
            if not band[0] <= count <= band[1]:
                report.fail(rel, body_heading.line,
                            f"exercise `{body_heading.text}` body is {count} words, outside the band {band[0]}–{band[1]}")
        if rel.endswith("agent-failures.md"):
            check_five_parts(report, rel, body_heading.line, "\n".join(lines[b_start:b_end]),
                             f"exercise `{body_heading.text}`")


def check_scoreboard(report: Report, rel: str, lines: list[str], canon: dict) -> None:
    metrics = (canon.get("scoreboard_metrics") or {}).get("rows") or []
    keys = {key for _, _, key in user_regions(lines)}
    for metric in metrics:
        if metric["id"] not in keys:
            report.fail(rel, None,
                        f"metric {metric['id']} ({metric['name']}) has no `<!-- user:actuals key=\"{metric['id']}\" -->` region — "
                        "weekly logging must never require touching YAML")


# --------------------------------------------------------------------------
# lints that apply to every prose file
# --------------------------------------------------------------------------


def check_placeholders(report: Report, rel: str, lines: list[str], build_time: bool) -> None:
    if is_fixture(rel):
        return  # canon.file_manifest.fixture_note: fixtures are excluded by design
    exempt = user_region_line_indices(lines)
    skip = fenced_lines(lines)
    for index, line in enumerate(lines):
        if index in skip or (index in exempt and not build_time):
            continue
        for token in PLACEHOLDER_TOKENS:
            if token in line:
                report.fail(rel, index + 1, f"placeholder token `{token}` is a blocking lint failure")

    if build_time:
        for start, end, key in user_regions(lines):
            inner = [line for line in lines[start + 1 : end] if line.strip()]
            if inner != [USER_REGION_PLACEHOLDER]:
                report.fail(rel, start + 1,
                            f"user region key=\"{key}\" must contain only the template placeholder "
                            f"`{USER_REGION_PLACEHOLDER}` at build time; found {len(inner)} other line(s)")


def check_word_band(report: Report, rel: str, schema_name: str, schema: dict,
                    lines: list[str], band_name: str) -> None:
    band = schema.get("sanity_band" if band_name == "sanity" else "word_band")
    if not band:
        if band_name == "sanity":
            band = schema.get("word_band")
        if not band:
            return

    # Per-file overrides beat the schema-wide band. A single band across every file of a
    # schema is the wrong shape when one file legitimately owns far more than its siblings:
    # reference/low-roi-and-cuts.md carries the low-ROI verdicts, the cut list AND the
    # glossary, and exercises/agent-failures.md carries 19 five-part exercise bodies.
    # Found at G5b: this block did not exist, so an override added to canon at G4 was read
    # by nothing and the compression it was meant to lift was still being enforced.
    overrides = schema.get("per_file_band_overrides") or {}
    override = overrides.get(rel)
    if override:
        if band_name == "sanity":
            # Keep the sanity band strictly wider than the word band so an exemplar can
            # never both set and fail its own ceiling.
            band = [min(band[0], override[0] - 200), max(band[1], override[1] + 300)]
        else:
            band = override

    count = word_count(lines)
    if count < band[0]:
        report.fail(rel, None, f"{count} words, below the `{schema_name}` {band_name} band floor of {band[0]}")
    elif count > band[1]:
        report.fail(rel, None,
                    f"{count} words, above the `{schema_name}` {band_name} band ceiling of {band[1]} — "
                    "the ceiling is the anti-padding control")


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------


def check_file(report: Report, canon: dict, rel: str, schema_name: str, schema: dict,
               build_time: bool, band_name: str) -> None:
    path = REPO_ROOT / rel
    if not path.exists():
        report.note(f"{rel}: not yet generated")
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    headings = parse_headings(lines)

    positions = check_sections(report, rel, schema_name, schema, lines, headings)
    check_placeholders(report, rel, lines, build_time)
    if not is_fixture(rel):
        check_word_band(report, rel, schema_name, schema, lines, band_name)

    if schema_name == "week":
        check_week(report, rel, lines, headings, positions, canon)
    elif schema_name == "month":
        check_month(report, rel, lines, headings, positions, canon)
    elif schema_name == "resources":
        check_resources(report, rel, lines, headings, positions, schema)
    elif schema_name == "exercise":
        check_exercises(report, rel, lines, headings, positions, schema, is_fixture(rel))
    elif schema_name == "SCOREBOARD":
        check_scoreboard(report, rel, lines, canon)


def main() -> int:
    parser = argparse.ArgumentParser(description="Per-file structural conformance against canon.schemas.")
    parser.add_argument("paths", nargs="*", help="explicit files to check (requires --schema)")
    parser.add_argument("--schema", help="schema name to apply to the explicit paths")
    parser.add_argument("--only", help="restrict the manifest sweep to paths starting with this prefix")
    parser.add_argument("--build-time", action="store_true",
                        help="also require that user:actuals regions contain only the template placeholder")
    parser.add_argument("--band", choices=("word", "sanity"), default="word",
                        help="which band to enforce; `sanity` is the wide band the exemplar is measured against")
    args = parser.parse_args()

    canon = load_canon()
    schemas = canon["schemas"]
    report = Report("check-schema")

    if args.paths:
        if not args.schema:
            parser.error("--schema is required when explicit paths are given")
        if args.schema not in schemas:
            parser.error(f"unknown schema `{args.schema}`; known: {sorted(k for k in schemas if isinstance(schemas[k], dict) and 'sections_in_order' in schemas[k])}")
        for raw in args.paths:
            path = Path(raw)
            rel = str(path.resolve().relative_to(REPO_ROOT)) if path.is_absolute() else raw
            check_file(report, canon, rel, args.schema, schemas[args.schema], args.build_time, args.band)
        return report.finish()

    non_prose = {cls["name"] for cls in schemas["non_prose_file_classes"]["classes"]}
    checked = 0
    for entry in canon["file_manifest"]["files"]:
        rel, schema_name = entry["path"], entry["schema"]
        if schema_name in non_prose:
            continue
        if args.only and not rel.startswith(args.only):
            continue
        if schema_name not in schemas:
            report.fail(rel, None, f"file_manifest assigns schema `{schema_name}`, which canon.schemas does not define")
            continue
        checked += 1
        check_file(report, canon, rel, schema_name, schemas[schema_name], args.build_time, args.band)

    report.note(f"{checked} prose file(s) in scope; {len(non_prose)} non-prose class(es) skipped by design: {', '.join(sorted(non_prose))}")
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
