#!/usr/bin/env python3
"""check-canon — prose expands canon and never invents.

Three checks:

  1. **Every canon id cited in prose exists.** The id families are derived from
     canon itself (BR-, D-, T-, AC-, SM-, LR-, AG-, DX-, RQ-, USI-, EX-FAIL-,
     and the week/month/stage id shapes), so a citation that *looks* like a
     canon id but resolves to nothing is a failure rather than a typo nobody
     notices.
  2. **Canon-owned numerics appear verbatim** in the files that own them: each
     week's four hour figures and their 15.0 total, each track's hours and
     share, the funnel volumes the user explicitly chose to keep, each month's
     funnel targets, and the programme-level figures README states.
  3. **Canon's own path references resolve** — `check_dupes.exemptions[].appears_in`
     (note the field name: `appears_in`, not the retired `must_appear_in`),
     plus every `home_file` and `retrospective_ref` in the document.

`<!-- user:actuals -->` regions hold the user's own logged prose. At runtime
they are exempt from all three checks. At build time (`--build-time`) they must
contain only the template placeholder, so the runtime exemption cannot become
an evasion hole.

Usage
    tools/check-canon.py                                   # the whole manifest
    tools/check-canon.py --build-time                      # build-time mode
    tools/check-canon.py --as weeks/week-01.md FIXTURE.md  # arbitrary file

Exit code is 0 on pass and 1 on any failure.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"

USER_REGION_OPEN = re.compile(r"<!--\s*user:actuals(?:\s+key=\"([^\"]*)\")?\s*-->")
USER_REGION_CLOSE = re.compile(r"<!--\s*/user:actuals\s*-->")
USER_REGION_PLACEHOLDER = "_(not yet logged)_"

# Week- and month-scoped ids (T-w01-3, D-m01-1, AC-w01-1a, REF-w01-2). Their
# family prefix can be a single letter, which is too short to key off safely,
# so they get their own shape.
SCOPED_ID_RE = re.compile(r"\b[A-Z]{1,4}-[wm]\d{2}-[0-9a-z]+\b")
WEEK_REF_RE = re.compile(r"\bW(\d{1,2})\b")
MONTH_REF_RE = re.compile(r"\bM(\d{1,2})\b")
# Stage ids: S0, S1a, BOA-S1, SKA-S2. The lookarounds are load-bearing and were added
# at G6 after lane L7 reported that the old `\b`-delimited form matched the SUBSTRING
# `AC-S0` inside `AC-S0-1` and failed it -- which made the id of the S0 architectural
# constraint the one id prose was forbidden to cite, and was already failing two files
# in another lane. A trailing hyphen or word character now means "this is part of a
# longer id, not a stage reference".
STAGE_REF_RE = re.compile(r"(?<![\w-])(?:[A-Z]{2,4}-)?S\d[a-z]?(?![\w-])")
PATH_REF_KEYS = ("home_file", "retrospective_ref")


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


def user_regions(lines: list[str]) -> list[tuple[int, int, str]]:
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


def fmt_hours(value: float) -> str:
    """Canon's hour figures as prose renders them: 3.0, 1.5, 0.75."""
    text = f"{float(value):.2f}".rstrip("0")
    return text + "0" if text.endswith(".") else text


# --------------------------------------------------------------------------
# canon id index
# --------------------------------------------------------------------------


def walk(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, f"{path}[{index}]")
    else:
        yield path, node


def id_index(canon: dict) -> tuple[set[str], set[str]]:
    """Every `id:` value in canon, plus the alphabetic families they form."""
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
    for key, week in (canon.get("weeks") or {}).items():
        ids.add(f"W{key}")
    for key, month in (canon.get("months") or {}).items():
        ids.add(f"M{key}")

    families = set()
    for value in ids:
        match = re.match(r"^([A-Z]{1,6}(?:-[A-Z]{2,6})?)-", value)
        if match and len(match.group(1)) > 1:
            families.add(match.group(1))
    return ids, families


# --------------------------------------------------------------------------
# canon-owned numerics
# --------------------------------------------------------------------------


class Claim:
    """One canon-owned figure that must appear verbatim in one file."""

    __slots__ = ("path", "literals", "description")

    def __init__(self, path: str, literals: list[str], description: str) -> None:
        self.path = path
        self.literals = literals
        self.description = description


def numeric_claims(canon: dict) -> list[Claim]:
    claims: list[Claim] = []

    for key, week in (canon.get("weeks") or {}).items():
        hours = week.get("hours") or {}
        # The 15.0 total is enforced structurally by check-schema (the four
        # rendered rows must sum to it), so requiring it verbatim here would
        # only duplicate that rule. What check-schema cannot see is whether the
        # four figures are CANON's four figures.
        claims.append(Claim(f"weeks/week-{key}.md", [fmt_hours(v) for v in hours.values()],
                            f"{week['id']} activity hours {hours}"))

    for letter, track in (canon.get("tracks") or {}).items():
        home = track.get("home_file")
        if not home:
            continue
        literals = [fmt_hours(track["hours"])]
        if track.get("share_of_180"):
            literals.append(track["share_of_180"])
        claims.append(Claim(home, literals, f"track {letter} allocation {track['hours']}h / {track.get('share_of_180')}"))

    volumes = (canon.get("funnel") or {}).get("volumes") or {}
    kept = [str(volumes[k]) for k in ("prospects_researched", "sends", "follow_ups", "opportunities_scored")
            if k in volumes]
    for home in ("business/customer-discovery.md", "business/outreach.md"):
        claims.append(Claim(home, kept,
                            "the funnel volumes the user chose to keep (USI-06) — never silently re-inflated"))

    for key, month in (canon.get("months") or {}).items():
        targets = month.get("funnel_targets") or {}
        # `not isinstance(v, bool)` is load-bearing: in Python `isinstance(True, int)` is
        # True, so a YAML boolean such as months["04"].funnel_targets.derived: false was
        # emitted as the canon-owned numeric "False" and the month file was required to
        # contain that literal string. Found at G6 by lane L4, which traced it only because
        # the failure message read like a tool bug rather than a rule.
        literals = [str(v) for v in targets.values() if isinstance(v, int) and not isinstance(v, bool)]
        if literals:
            claims.append(Claim(f"months/month-{key}.md", literals, f"{month['id']} funnel targets"))

    meta = canon.get("meta") or {}
    activity = canon.get("activity_allocation") or {}
    readme = [fmt_hours(meta["baseline_hours_per_week"]),
              fmt_hours(meta["theory_cap_hours_per_week"]),
              fmt_hours(meta["business_floor_hours_per_week"])]
    readme += [mode["mode"] for mode in meta.get("scaling_modes") or []]
    readme += [share for share in (activity.get("theory_share"), activity.get("active_share")) if share]
    claims.append(Claim("README.md", readme, "the programme-level hour figures and scaling modes"))

    metrics = canon.get("scoreboard_metrics") or {}
    if metrics:
        counts = {}
        for row in metrics.get("rows") or []:
            counts[row["group"]] = counts.get(row["group"], 0) + 1
        claims.append(Claim("SCOREBOARD.md",
                            [str(metrics.get("count"))] + [str(counts[g]) for g in metrics.get("groups") or []],
                            "the 22 metrics and their 7 / 7 / 8 group sizes"))
    return claims


# --------------------------------------------------------------------------
# per-file checks
# --------------------------------------------------------------------------


def visible_lines(lines: list[str], build_time: bool) -> list[tuple[int, str]]:
    """Lines outside fenced code and (at runtime) outside user regions."""
    skip = fenced_lines(lines) | comment_lines(lines)
    exempt = set() if build_time else user_region_line_indices(lines)
    return [(index + 1, line) for index, line in enumerate(lines)
            if index not in skip and index not in exempt]


def check_ids(report: Report, rel: str, lines: list[str], ids: set[str],
              families: set[str], build_time: bool) -> None:
    if not families:
        return
    family_re = re.compile(r"\b(?:" + "|".join(sorted(families, key=len, reverse=True)) + r")-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b")
    for line_number, line in visible_lines(lines, build_time):
        for token in family_re.findall(line):
            if token not in ids:
                report.fail(rel, line_number, f"cites `{token}`, which is not an id in canon")
        for token in SCOPED_ID_RE.findall(line):
            if token not in ids:
                report.fail(rel, line_number, f"cites `{token}`, which is not an id in canon")
        for match in WEEK_REF_RE.finditer(line):
            number = int(match.group(1))
            if not 1 <= number <= 12 and f"W{number:02d}" not in ids:
                report.fail(rel, line_number, f"cites week `{match.group(0)}`, which canon does not define")
        for match in MONTH_REF_RE.finditer(line):
            number = int(match.group(1))
            if not 1 <= number <= 12:
                report.fail(rel, line_number, f"cites month `{match.group(0)}`, which canon does not define")
        for token in STAGE_REF_RE.findall(line):
            if token not in ids:
                report.fail(rel, line_number, f"cites stage `{token}`, which is not a stage id in canon")


def check_numerics(report: Report, rel: str, lines: list[str], claims: list[Claim], build_time: bool) -> None:
    relevant = [claim for claim in claims if claim.path == rel]
    if not relevant:
        return
    text = "\n".join(line for _, line in visible_lines(lines, build_time))
    for claim in relevant:
        for literal in claim.literals:
            if not re.search(r"(?<![\w.])" + re.escape(literal) + r"(?![\d.])", text):
                report.fail(rel, None,
                            f"canon-owned numeric `{literal}` does not appear verbatim "
                            f"({claim.description}) — prose expands canon and never restates it differently")


def check_user_regions(report: Report, rel: str, lines: list[str], build_time: bool) -> None:
    for start, end, key in user_regions(lines):
        if not key:
            report.fail(rel, start + 1, "user:actuals region has no `key=\"...\"`; regions are reattached by stable key on regeneration")
        if build_time:
            inner = [line for line in lines[start + 1 : end] if line.strip()]
            if inner != [USER_REGION_PLACEHOLDER]:
                report.fail(rel, start + 1,
                            f"user region key=\"{key}\" must contain only `{USER_REGION_PLACEHOLDER}` at build time; "
                            f"found {len(inner)} other line(s)")


def check_canon_paths(report: Report, canon: dict, manifest: set[str]) -> None:
    exemptions = (canon.get("check_dupes") or {}).get("exemptions") or []
    for exemption in exemptions:
        for reference in exemption.get("appears_in") or []:
            target = reference.split("#", 1)[0]
            if "*" in target:
                if not any(fnmatch.fnmatch(path, target) for path in manifest):
                    report.fail("canon/canon.yaml", None,
                                f"check_dupes.exemptions {exemption['id']}: appears_in glob `{target}` matches no file_manifest path")
            elif target not in manifest:
                report.fail("canon/canon.yaml", None,
                            f"check_dupes.exemptions {exemption['id']}: appears_in path `{target}` is not a file_manifest path")

    for dotted, value in walk(canon):
        key = dotted.rsplit(".", 1)[-1].split("[", 1)[0]
        if key not in PATH_REF_KEYS or not isinstance(value, str):
            continue
        target = value.split("#", 1)[0]
        if not target.endswith((".md", ".yaml")):
            continue
        if "*" in target:
            if not any(fnmatch.fnmatch(path, target) for path in manifest):
                report.fail("canon/canon.yaml", None, f"{dotted}: `{target}` matches no file_manifest path")
        elif target not in manifest:
            report.fail("canon/canon.yaml", None, f"{dotted}: `{target}` is not a file_manifest path")


def check_file(report: Report, rel: str, actual: Path, ids: set[str], families: set[str],
               claims: list[Claim], build_time: bool) -> None:
    if not actual.exists():
        report.note(f"{rel}: not yet generated")
        return
    lines = actual.read_text(encoding="utf-8").splitlines()
    check_ids(report, rel, lines, ids, families, build_time)
    check_numerics(report, rel, lines, claims, build_time)
    check_user_regions(report, rel, lines, build_time)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prose expands canon and never invents.")
    parser.add_argument("paths", nargs="*", help="explicit files to check")
    parser.add_argument("--as", dest="as_path", help="evaluate the explicit files under the rules that apply to this manifest path")
    parser.add_argument("--build-time", action="store_true",
                        help="require user:actuals regions to contain only the template placeholder")
    args = parser.parse_args()

    canon = load_canon()
    report = Report("check-canon")
    ids, families = id_index(canon)
    claims = numeric_claims(canon)
    manifest = {entry["path"] for entry in canon["file_manifest"]["files"]}

    if args.paths:
        for raw in args.paths:
            actual = Path(raw) if Path(raw).is_absolute() else REPO_ROOT / raw
            rel = args.as_path or raw
            check_file(report, rel, actual, ids, families, claims, args.build_time)
        return report.finish()

    check_canon_paths(report, canon, manifest)
    non_prose = {cls["name"] for cls in canon["schemas"]["non_prose_file_classes"]["classes"]}
    present = 0
    for entry in canon["file_manifest"]["files"]:
        if entry["schema"] in non_prose:
            continue
        rel = entry["path"]
        actual = REPO_ROOT / rel
        if actual.exists():
            present += 1
        check_file(report, rel, actual, ids, families, claims, args.build_time)

    report.note(f"{len(ids)} canon ids indexed across {len(families)} families; "
                f"{len(claims)} numeric claim(s); {present} prose file(s) present")
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
