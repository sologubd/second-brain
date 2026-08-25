#!/usr/bin/env python3
"""check-hours — the seven hour assertions over canon.

Per-task `{primary_track, activity_class, hours}` is authoritative. The
activity split and the track allocation are projections of it. Two of the seven
assertions only prove that those projections agree with the tasks they are
computed from; they cannot detect an underpriced or a misclassified task. They
are printed with a `definitional` label so no reader mistakes bookkeeping for
verification.

  1  substantive    sum(week.tasks[].hours) == 15.0
  2  DEFINITIONAL   sum(tasks by activity_class) == week.hours{}
  3  DEFINITIONAL   activity_class == "business"  <=>  primary_track in {E, F}
  4  substantive    sum(tasks by primary_track over W01..W12) == track_allocation
  5  substantive    week.hours.theory <= 3.5      (classification-dependent)
  6  substantive    week.hours.business >= 2.5
  7  substantive    no track absent for more than 2 consecutive weeks as
                    primary_track or reinforces; the pseudo-track P is exempt

Assertion 5 is the live risk. Nothing mechanical distinguishes a `building`
task that is really reading, so a passing rule 5 means the *stated*
classification respects the cap, not that the classification is right.

Usage
    tools/check-hours.py                     # canon/canon.yaml
    tools/check-hours.py --canon FIXTURE.yaml

Exit code is 0 on pass and 1 on any failure.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"

TOLERANCE = 1e-9
WEEKLY_HOURS = 15.0
BUSINESS_TRACKS = frozenset({"E", "F"})
COVERAGE_EXEMPT_TRACKS = frozenset({"P"})
MAX_CONSECUTIVE_ABSENCE = 2

DEFINITIONAL = "definitional"
SUBSTANTIVE = "substantive"


class Report:
    """Collects failures per assertion so the summary names which rule failed."""

    def __init__(self, tool: str) -> None:
        self.tool = tool
        self.failures: list[tuple[str, int | None, str]] = []
        self.notes: list[str] = []
        self.results: list[tuple[int, str, str, int]] = []

    def fail(self, path: str, line: int | None, message: str) -> None:
        self.failures.append((str(path), line, message))

    def note(self, message: str) -> None:
        self.notes.append(message)

    def record(self, number: int, kind: str, statement: str, failures_before: int) -> None:
        self.results.append((number, kind, statement, len(self.failures) - failures_before))

    @staticmethod
    def _where(path: str, line: int | None) -> str:
        return f"{path}:{line}" if line else f"{path}"

    def finish(self) -> int:
        for message in self.notes:
            print(f"note: {message}")
        for path, line, message in self.failures:
            print(f"{self._where(path, line)}: {message}")
        print()
        for number, kind, statement, count in self.results:
            status = "ok  " if count == 0 else f"FAIL"
            label = f"[{kind}]".ljust(15)
            print(f"  rule {number}  {status}  {label} {statement}" + (f"  ({count} failure(s))" if count else ""))
        if self.failures:
            print(f"\n{self.tool}: FAIL — {len(self.failures)} failure(s)")
            return 1
        print(f"\n{self.tool}: ok — 5 substantive assertions, 2 definitional")
        return 0


def canon_line(canon_text: list[str], needle: str) -> int | None:
    """Best-effort line number for a canon key, so failures are navigable."""
    for index, line in enumerate(canon_text):
        if needle in line:
            return index + 1
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="The seven hour assertions over canon.")
    parser.add_argument("--canon", default=str(CANON_PATH), help="canon file to check (default canon/canon.yaml)")
    args = parser.parse_args()

    canon_path = Path(args.canon)
    rel = str(canon_path.resolve().relative_to(REPO_ROOT)) if canon_path.resolve().is_relative_to(REPO_ROOT) else str(canon_path)
    raw = canon_path.read_text(encoding="utf-8")
    canon = yaml.safe_load(raw)
    lines = raw.splitlines()

    report = Report("check-hours")
    weeks = canon.get("weeks") or {}
    if not weeks:
        report.fail(rel, None, "canon defines no weeks[]")
        return report.finish()

    meta = canon.get("meta") or {}
    theory_cap = float(meta.get("theory_cap_hours_per_week", 3.5))
    business_floor = float(meta.get("business_floor_hours_per_week", 2.5))
    order = sorted(weeks)

    # --- rule 1 ------------------------------------------------------------
    before = len(report.failures)
    for key in order:
        week = weeks[key]
        total = sum(float(task["hours"]) for task in week["tasks"])
        if abs(total - WEEKLY_HOURS) > TOLERANCE:
            report.fail(rel, canon_line(lines, f'id: "{week["id"]}"'),
                        f"{week['id']}: tasks sum to {total:g}h, expected {WEEKLY_HOURS:g}h "
                        f"(off by {total - WEEKLY_HOURS:+g}h)")
    report.record(1, SUBSTANTIVE, "sum(week.tasks[].hours) == 15.0", before)

    # --- rule 2 ------------------------------------------------------------
    before = len(report.failures)
    for key in order:
        week = weeks[key]
        rolled: dict[str, float] = defaultdict(float)
        for task in week["tasks"]:
            rolled[task["activity_class"]] += float(task["hours"])
        stated = week.get("hours") or {}
        for bucket in sorted(set(rolled) | set(stated)):
            computed, declared = rolled.get(bucket, 0.0), float(stated.get(bucket, 0.0))
            if abs(computed - declared) > TOLERANCE:
                report.fail(rel, canon_line(lines, f'id: "{week["id"]}"'),
                            f"{week['id']}: tasks classified `{bucket}` sum to {computed:g}h but week.hours.{bucket} states {declared:g}h")
    report.record(2, DEFINITIONAL, "sum(tasks by activity_class) == week.hours{}", before)

    # --- rule 3 ------------------------------------------------------------
    before = len(report.failures)
    for key in order:
        week = weeks[key]
        for task in week["tasks"]:
            is_business = task["activity_class"] == "business"
            on_business_track = task["primary_track"] in BUSINESS_TRACKS
            if is_business != on_business_track:
                report.fail(rel, canon_line(lines, f'id: "{task["id"]}"'),
                            f"{task['id']}: activity_class `{task['activity_class']}` and primary_track "
                            f"`{task['primary_track']}` break the business <=> {{E, F}} identity")
    report.record(3, DEFINITIONAL, 'activity_class == "business" <=> primary_track in {E, F}', before)

    # --- rule 4 ------------------------------------------------------------
    before = len(report.failures)
    by_track: dict[str, float] = defaultdict(float)
    for key in order:
        for task in weeks[key]["tasks"]:
            by_track[task["primary_track"]] += float(task["hours"])
    allocation = canon.get("track_allocation") or {}
    tracks = sorted(set(by_track) | {k for k, v in allocation.items() if isinstance(v, (int, float)) and len(k) == 1})
    for track in tracks:
        computed, declared = by_track.get(track, 0.0), float(allocation.get(track, 0.0))
        if abs(computed - declared) > TOLERANCE:
            report.fail(rel, canon_line(lines, "track_allocation:"),
                        f"track {track}: tasks over W01–W12 sum to {computed:g}h but track_allocation states {declared:g}h "
                        f"(off by {computed - declared:+g}h)")
    grand = sum(by_track.values())
    if abs(grand - WEEKLY_HOURS * len(order)) > TOLERANCE:
        report.fail(rel, canon_line(lines, "track_allocation:"),
                    f"track totals sum to {grand:g}h over {len(order)} weeks, expected {WEEKLY_HOURS * len(order):g}h")
    report.record(4, SUBSTANTIVE, "sum(tasks by primary_track over W01–W12) == track_allocation", before)

    # --- rule 5 ------------------------------------------------------------
    before = len(report.failures)
    at_cap = []
    for key in order:
        week = weeks[key]
        theory = float((week.get("hours") or {}).get("theory", 0.0))
        if theory > theory_cap + TOLERANCE:
            report.fail(rel, canon_line(lines, f'id: "{week["id"]}"'),
                        f"{week['id']}: theory is {theory:g}h, above the {theory_cap:g}h weekly cap")
        elif abs(theory - theory_cap) <= TOLERANCE:
            at_cap.append(week["id"])
    if at_cap:
        report.note(f"rule 5: {', '.join(at_cap)} sit exactly at the {theory_cap:g}h theory cap — "
                    "no headroom, and the cap is only as good as the classification behind it")
    report.record(5, SUBSTANTIVE, f"week.hours.theory <= {theory_cap:g}  (classification-dependent)", before)

    # --- rule 6 ------------------------------------------------------------
    before = len(report.failures)
    for key in order:
        week = weeks[key]
        business = float((week.get("hours") or {}).get("business", 0.0))
        if business < business_floor - TOLERANCE:
            report.fail(rel, canon_line(lines, f'id: "{week["id"]}"'),
                        f"{week['id']}: business is {business:g}h, below the {business_floor:g}h weekly floor")
    report.record(6, SUBSTANTIVE, f"week.hours.business >= {business_floor:g}", before)

    # --- rule 7 ------------------------------------------------------------
    before = len(report.failures)
    all_tracks = sorted({t for t in (canon.get("tracks") or {})} - COVERAGE_EXEMPT_TRACKS)
    for track in all_tracks:
        absent_since: str | None = None
        run = 0
        for key in order:
            week = weeks[key]
            present = any(task["primary_track"] == track or track in (task.get("reinforces") or [])
                          for task in week["tasks"])
            if present:
                run, absent_since = 0, None
            else:
                run += 1
                absent_since = absent_since or week["id"]
                if run == MAX_CONSECUTIVE_ABSENCE + 1:
                    report.fail(rel, canon_line(lines, f'id: "{week["id"]}"'),
                                f"track {track}: absent as primary_track and reinforces for {run} consecutive weeks "
                                f"({absent_since} through {week['id']}); the limit is {MAX_CONSECUTIVE_ABSENCE}")
    report.record(7, SUBSTANTIVE,
                  f"no track absent > {MAX_CONSECUTIVE_ABSENCE} consecutive weeks (pseudo-track P exempt)", before)

    report.note(f"{len(order)} week(s), {sum(len(weeks[k]['tasks']) for k in order)} task(s), "
                f"{grand:g}h total across tracks {', '.join(sorted(by_track))}")
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
