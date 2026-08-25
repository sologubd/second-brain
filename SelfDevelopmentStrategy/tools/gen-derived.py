#!/usr/bin/env python3
"""gen-derived — regenerate everything canon owns, and never touch what the user owns.

Generates `ROADMAP.md`, `SCOREBOARD.md`, `canon/CANON.md`, and derives
`months[].funnel_targets` for months 01-03 from the week-index mapping.

THE HARD CORRECTNESS REQUIREMENT
--------------------------------
`<!-- user:actuals key="..." -->` regions hold the user's own logged weekly
hours and metric readings. The month-01 retrospective reads exactly those
numbers to recalibrate weeks 05-12; they are the only uncorrelated instrument
in the programme. So:

  * generation writes ONLY outside those regions;
  * region bodies are preserved BYTE-FOR-BYTE, not re-rendered;
  * regions are reattached BY STABLE KEY, because later retrospectives rewrite
    the generated rows around them and position is not stable;
  * a region whose key no longer exists is emitted into `## Orphaned entries`,
    never dropped and never silently misaligned against the wrong metric.

`tools/fixtures/SCOREBOARD-user-entries.md` is the control that proves all four,
and `--selftest` is what runs it.

ON `months[].funnel_targets`
----------------------------
Months 01-03 map to week-files 01-04, 05-08 and 09-12, so their targets are a
sum of week targets and are DERIVED. This tool derives them, checks them against
canon, and renders them into `canon/CANON.md`. It does NOT rewrite
`canon/canon.yaml`: that file is hand-authored with several hundred lines of
reasoning in comments, and a YAML round-trip would silently delete all of it.
Canon stays authoritative and hand-edited; the derivation stays checked.
Months 04+ are set by the M2 delta and are not derivable from weeks.

Usage
    tools/gen-derived.py                  # write the generated files
    tools/gen-derived.py --check          # no-op diff over generated regions
    tools/gen-derived.py --delta 05       # scaffold a canon delta from M05
    tools/gen-derived.py --selftest       # run the fixture self-tests

Exit code is 0 on pass and 1 on any failure.
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = REPO_ROOT / "canon" / "canon.yaml"
FIXTURE_SCOREBOARD = REPO_ROOT / "tools" / "fixtures" / "SCOREBOARD-user-entries.md"
DELTA_DIR = REPO_ROOT / "canon" / "deltas"

USER_REGION_PLACEHOLDER = "_(not yet logged)_"
ORPHAN_MARKER = "<!-- orphans -->"

REGION_RE = re.compile(
    r"(?P<open><!--\s*user:actuals\s+key=\"(?P<key>[^\"]*)\"\s*-->[^\n]*\n)"
    r"(?P<body>.*?)"
    r"(?P<close>[ \t]*<!--\s*/user:actuals\s*-->)",
    re.S,
)

# Week funnel keys are summed into month targets. `calls` is the week-level name
# for what months call `calls_planned`. Two month keys are DELIBERATELY not
# derived: `calls_expected` and `replies_expected` are rates computed from
# matured sends, and a rate is not a sum of weekly rates.
FUNNEL_WEEK_TO_MONTH = {"calls": "calls_planned"}
FUNNEL_NON_DERIVED = frozenset({"calls_expected", "replies_expected", "note"})
WEEKS_PER_MONTH = 4
DERIVABLE_MONTHS = ("01", "02", "03")


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
        for path, line, message in self.failures:
            print(f"{self._where(path, line)}: {message}")
        if self.failures:
            print(f"\n{self.tool}: FAIL — {len(self.failures)} failure(s)")
            return 1
        print(f"\n{self.tool}: ok" + (f" ({len(self.warnings)} warning(s))" if self.warnings else ""))
        return 0


def load_canon(path: Path = CANON_PATH) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fmt_hours(value: float) -> str:
    text = f"{float(value):.2f}".rstrip("0")
    return text + "0" if text.endswith(".") else text


def clip(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


def cell(text: str) -> str:
    """Markdown table cells cannot contain a raw pipe or a newline."""
    return " ".join(str(text).split()).replace("|", "\\|")


# --------------------------------------------------------------------------
# user regions: parse, reattach, orphan
# --------------------------------------------------------------------------


def parse_regions(text: str) -> dict[str, str]:
    """{key: body} where body is the exact substring between the markers."""
    return {match.group("key"): match.group("body") for match in REGION_RE.finditer(text)}


def emit_region(key: str, body: str | None = None) -> str:
    inner = USER_REGION_PLACEHOLDER + "\n" if body is None else body
    return f'<!-- user:actuals key="{key}" -->\n{inner}<!-- /user:actuals -->\n'


def reattach(new_text: str, old_text: str) -> tuple[str, list[str]]:
    """Copy every existing region body into the freshly rendered text, by key.

    Returns the merged text and the keys that no longer have a home.
    """
    old = parse_regions(old_text)
    reused: set[str] = set()

    def substitute(match: re.Match[str]) -> str:
        key = match.group("key")
        if key in old:
            reused.add(key)
            return match.group("open") + old[key] + match.group("close")
        return match.group(0)

    merged = REGION_RE.sub(substitute, new_text)
    orphans = [key for key in old if key not in reused]

    if ORPHAN_MARKER in merged:
        if orphans:
            blocks = [
                "The keys below no longer exist in canon. Their contents are preserved verbatim.",
                "Move each one onto its replacement metric by hand, then delete it from here.",
                "",
            ]
            for key in orphans:
                blocks.append(f"**`{key}`** — no longer defined in canon.")
                blocks.append("")
                blocks.append(emit_region(key, old[key]))
            replacement = "\n".join(blocks).rstrip() + "\n"
        else:
            replacement = "_(none)_\n"
        merged = merged.replace(ORPHAN_MARKER + "\n", replacement)
    return merged, orphans


# --------------------------------------------------------------------------
# derivation: months[].funnel_targets
# --------------------------------------------------------------------------


def derive_month_funnel_targets(canon: dict) -> dict[str, dict[str, float]]:
    weeks = canon.get("weeks") or {}
    order = sorted(weeks)
    derived: dict[str, dict[str, float]] = {}
    for index, month_key in enumerate(DERIVABLE_MONTHS):
        window = order[index * WEEKS_PER_MONTH : (index + 1) * WEEKS_PER_MONTH]
        rolled: dict[str, float] = defaultdict(float)
        for week_key in window:
            for name, value in (weeks[week_key].get("funnel_targets") or {}).items():
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                target = FUNNEL_WEEK_TO_MONTH.get(name, name)
                if target in FUNNEL_NON_DERIVED:
                    continue
                rolled[target] += value
        derived[month_key] = dict(rolled)
    return derived


def check_derived_funnel(report: Report, canon: dict, derived: dict[str, dict[str, float]]) -> None:
    months = canon.get("months") or {}
    for month_key, rolled in derived.items():
        stated = months.get(month_key, {}).get("funnel_targets") or {}
        for name, value in sorted(rolled.items()):
            if name not in stated:
                report.fail("canon/canon.yaml", None,
                            f"months[{month_key}].funnel_targets is missing derived key `{name}` (weeks sum to {value:g})")
            elif abs(float(stated[name]) - value) > 1e-9:
                report.fail("canon/canon.yaml", None,
                            f"months[{month_key}].funnel_targets.{name} states {stated[name]} but weeks "
                            f"{DERIVABLE_MONTHS.index(month_key) * WEEKS_PER_MONTH + 1:02d}–"
                            f"{(DERIVABLE_MONTHS.index(month_key) + 1) * WEEKS_PER_MONTH:02d} sum to {value:g}")
        for name in stated:
            if name in FUNNEL_NON_DERIVED or name in rolled:
                continue
            report.warn("canon/canon.yaml", None,
                        f"months[{month_key}].funnel_targets.{name} is stated but not derivable from weeks")


# --------------------------------------------------------------------------
# renderers
# --------------------------------------------------------------------------


GENERATED_BANNER = (
    "<!-- GENERATED BY tools/gen-derived.py FROM canon/canon.yaml — DO NOT EDIT BY HAND.\n"
    "     Everything outside a <!-- user:actuals --> region is overwritten on `make regen`.\n"
    "     Edit canon/canon.yaml and regenerate. See HOW-TO-EDIT.md. -->\n"
)


def render_roadmap(canon: dict) -> str:
    months = canon.get("months") or {}
    schema = (canon.get("schemas") or {}).get("ROADMAP") or {}
    columns = schema.get("table_columns_in_order") or ["Month", "Major concepts", "Projects", "Business activity", "Measurable outcomes"]

    out = [GENERATED_BANNER, "# Roadmap", "", "## Overview table", "",
           "| " + " | ".join(columns) + " |",
           "|" + "|".join(["---"] * len(columns)) + "|"]

    for key in sorted(months):
        month = months[key]
        concepts = ", ".join(month.get("major_concepts") or []) or "—"
        stages = ", ".join(month.get("stages_entered") or []) or "—"
        targets = month.get("funnel_targets") or {}
        if "note" in targets:
            business = targets["note"]
        else:
            business = ", ".join(f"{name.replace('_', ' ')} {value:g}" if isinstance(value, (int, float)) else f"{name.replace('_', ' ')} {value}"
                                 for name, value in targets.items()) or "—"
        outcomes = "; ".join(f"{item['id']} {clip(item['text'], 70)}" for item in month.get("deliverables") or []) or "—"
        out.append("| " + " | ".join([
            f"**{month['id']}**", cell(clip(concepts, 130)), cell(stages), cell(clip(business, 120)), cell(outcomes),
        ]) + " |")

    out += [
        "",
        "## How to read this",
        "",
        f"One row per month across the {len(months)}-month horizon. `Major concepts` names what the month",
        "teaches, `Projects` the project stages it enters, `Business activity` the funnel targets it",
        "carries, and `Measurable outcomes` the deliverable ids that prove it happened. Deliverable text",
        "is clipped here; the month file holds it in full.",
        "",
        "Months 01–03 carry derived funnel targets — they are the sum of their four week files. Months 04",
        "onward are set by the month-02 delta and are deliberately thinner: a target set twelve months",
        "ahead of the evidence would be a guess wearing a number.",
        "",
        "This file is generated. To change a row, edit `canon/canon.yaml` and run `make regen`.",
        "",
    ]
    return "\n".join(out)


def render_scoreboard(canon: dict) -> str:
    metrics = canon.get("scoreboard_metrics") or {}
    rows = metrics.get("rows") or []
    groups = metrics.get("groups") or []
    row_format = metrics.get("weekly_row_format") or {}
    funnel = (canon.get("funnel") or {}).get("volumes") or {}
    reply = (canon.get("funnel") or {}).get("reply_rate_band") or {}
    to_call = (canon.get("funnel") or {}).get("reply_to_call_band") or {}
    counts = {group: sum(1 for row in rows if row["group"] == group) for group in groups}

    out = [GENERATED_BANNER, "# Scoreboard", "", "## How to update this", "",
           f"{metrics.get('count', len(rows))} metrics in {len(groups)} groups — "
           + " / ".join(f"{counts[group]} {group}" for group in groups) + ".",
           "",
           "Write your readings inside the `<!-- user:actuals -->` block under each metric and nowhere",
           "else; weekly logging never requires touching YAML. `make regen` rewrites every generated line",
           "here and copies your blocks across byte-for-byte, reattaching them by metric id, so a canon",
           "edit that reorders the metrics cannot misalign your numbers.",
           "",
           "Every business row carries `evidence_source: real | simulated`. A simulated reading logged as",
           "real is the one failure this scoreboard cannot detect. Paid pilots and revenue are NEVER simulated.",
           ""]

    if row_format:
        out += ["```text",
                row_format.get("format", ""),
                row_format.get("example", ""),
                "```",
                "",
                row_format.get("render_note", "").strip(),
                ""]

    out += [
           f"Funnel volumes for the twelve detailed weeks: {funnel.get('prospects_researched', '—')} prospects researched, "
           f"{funnel.get('sends', '—')} sends, {funnel.get('follow_ups', '—')} follow-ups, "
           f"{funnel.get('opportunities_scored', '—')} opportunities scored. Reply rate is expected in the",
           f"{reply.get('low', 0) * 100:g}–{reply.get('high', 0) * 100:g}% band and reply-to-call at "
           f"{to_call.get('low', 0) * 100:g}–{to_call.get('high', 0) * 100:g}%; both DIRECTIONAL, NOT PREDICTIVE, and the",
           "month-02 delta is expected to move them, plausibly by 2x either way.",
           ""]

    for group in groups:
        out += [f"## {group}", ""]
        for row in [r for r in rows if r["group"] == group]:
            out.append(f"### {row['id']} — {row['name']}")
            out.append("")
            out.append(f"- unit: {row['unit']}")
            out.append(f"- source artifact: {row['source_artifact']}")
            out.append(f"- cadence: {row['cadence']}")
            out.append(f"- evidence_source: {row['evidence_source']}")
            if row.get("note"):
                out.append(f"- note: {row['note']}")
            out.append("")
            out.append(emit_region(row["id"]).rstrip("\n"))
            out.append("")

    out += ["## Orphaned entries", "", ORPHAN_MARKER, ""]
    return "\n".join(out)


def render_canon_md(canon: dict, derived: dict[str, dict[str, float]]) -> str:
    meta = canon.get("meta") or {}
    out = [GENERATED_BANNER, "# Canon", "",
           f"A human-readable rendering of `canon/canon.yaml` v{meta.get('version')}, generated "
           f"{meta.get('generated_at')}, so canon is readable without a YAML parser. The YAML is",
           "authoritative; this file is not. Edit the YAML, bump `meta.version`, run `make regen`.", ""]

    out += ["## Meta", ""]
    for key in ("horizon_months", "detailed_weeks", "calendar_weeks", "baseline_hours_per_week",
                "total_planned_hours", "theory_cap_hours_per_week", "business_floor_hours_per_week",
                "deliverables_cap", "subsystems_cap"):
        if key in meta:
            out.append(f"- `{key}`: {meta[key]}")
    out += ["", "### Scaling modes", ""]
    for mode in meta.get("scaling_modes") or []:
        out.append(f"- **{mode['mode']}** — {mode['rule']}")
    out += ["", f"**In-flight recovery.** {meta.get('in_flight_recovery_rule', '')}", ""]

    activity = canon.get("activity_allocation") or {}
    out += ["## Hour model", "", "### Activity allocation", "",
            "| Activity | Hours | Share |", "|---|---|---|"]
    total = float(activity.get("total", 180.0))
    for key in ("theory", "building", "testing", "business"):
        if key in activity:
            hours = float(activity[key])
            out.append(f"| {key} | {fmt_hours(hours)} | {hours / total * 100:.1f}% |")
    out.append(f"| **total** | **{fmt_hours(total)}** | **100.0%** |")
    out += ["", f"Theory share {activity.get('theory_share')} against {activity.get('theory_cap_source')}",
            "", f"Active share {activity.get('active_share')} against {activity.get('active_floor_source')}", ""]

    allocation = canon.get("track_allocation") or {}
    out += ["### Track allocation", "", "| Track | Name | Hours | Share | Home |", "|---|---|---|---|---|"]
    for letter, track in (canon.get("tracks") or {}).items():
        out.append(f"| {letter} | {cell(track.get('name', ''))} | {fmt_hours(track.get('hours', 0))} | "
                   f"{track.get('share_of_180', '')} | `{track.get('home_file', '')}` |")
    out.append(f"| | **total** | **{fmt_hours(allocation.get('total', 0))}** | **100.0%** | |")
    out.append("")

    weeks = canon.get("weeks") or {}
    out += ["## Weeks", "", "| Week | Name | Theory | Building | Testing | Business | Stage | Maturity |",
            "|---|---|---|---|---|---|---|---|"]
    for key in sorted(weeks):
        week = weeks[key]
        hours = week.get("hours") or {}
        out.append(f"| {week['id']} | {cell(week.get('name', ''))} | " +
                   " | ".join(fmt_hours(hours.get(bucket, 0)) for bucket in ("theory", "building", "testing", "business")) +
                   f" | {week.get('stage', '—')} | {week.get('maturity_level_target', '—')} |")
    out.append("")

    months = canon.get("months") or {}
    out += ["## Months", "", "| Month | Outcome | Stages entered | Mandated delta |", "|---|---|---|---|"]
    for key in sorted(months):
        month = months[key]
        out.append(f"| {month['id']} | {cell(clip(month.get('outcome', ''), 110))} | "
                   f"{cell(', '.join(month.get('stages_entered') or []) or '—')} | "
                   f"{cell((month.get('mandated_delta') or {}).get('type', '—'))} |")

    out += ["", "### Derived funnel targets (months 01–03)", "",
            "Months 01–03 map to week-files 01–04, 05–08 and 09–12 — a week index, immune to the",
            "14-calendar-week float. These rows are the sum of their weeks and are DERIVED here.",
            "`calls_expected` and `replies_expected` are rates over matured sends, not sums, and stay",
            "hand-authored in canon. Months 04+ are set by the M2 delta.", ""]
    names = sorted({name for rolled in derived.values() for name in rolled})
    out += ["| Month | " + " | ".join(name.replace("_", " ") for name in names) + " |",
            "|" + "|".join(["---"] * (len(names) + 1)) + "|"]
    for month_key in DERIVABLE_MONTHS:
        rolled = derived.get(month_key, {})
        out.append(f"| M{month_key} | " + " | ".join(f"{rolled.get(name, 0):g}" for name in names) + " |")
    out.append("")

    anti = canon.get("anti_goals") or {}
    out += ["## Anti-goals", "", "| Id | Anti-goal | Conditional | Positive form |", "|---|---|---|---|"]
    for row in anti.get("rows") or []:
        out.append(f"| {row['id']} | {cell(row['anti_goal'])} | {'yes' if row.get('conditional') else 'no'} | "
                   f"{cell(clip(row['positive_form'], 150))} |")
    out += ["", f"**Conditional handling.** {anti.get('conditional_handling', {}).get('rule', '')}",
            f"{anti.get('conditional_handling', {}).get('implementation', '')}", ""]

    metrics = canon.get("scoreboard_metrics") or {}
    out += ["## Scoreboard metrics", "", "| Id | Group | Metric | Unit | Cadence |", "|---|---|---|---|---|"]
    for row in metrics.get("rows") or []:
        out.append(f"| {row['id']} | {row['group']} | {cell(row['name'])} | {cell(clip(row['unit'], 70))} | {row['cadence']} |")
    out.append("")

    manifest = canon.get("file_manifest") or {}
    out += ["## File manifest", "", f"{manifest.get('total')} files: {manifest.get('arithmetic')}", "",
            "| Schema | Files |", "|---|---|"]
    for name, count in (manifest.get("counts") or {}).items():
        out.append(f"| {name} | {count} |")
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------
# modes
# --------------------------------------------------------------------------


def targets(canon: dict, derived: dict) -> dict[str, str]:
    return {
        "ROADMAP.md": render_roadmap(canon),
        "SCOREBOARD.md": render_scoreboard(canon),
        "canon/CANON.md": render_canon_md(canon, derived),
    }


def generated_diff(rel: str, old: str, new: str) -> list[str]:
    """Unified diff with user-region bodies masked, so the diff is over
    generated regions only."""
    def mask(text: str) -> list[str]:
        masked = REGION_RE.sub(lambda m: m.group("open") + "<user region, preserved>\n" + m.group("close"), text)
        return masked.splitlines(keepends=True)

    return list(difflib.unified_diff(mask(old), mask(new), fromfile=f"a/{rel}", tofile=f"b/{rel}", n=1))


def run_generate(report: Report, canon: dict, derived: dict, check_only: bool) -> None:
    for rel, rendered in targets(canon, derived).items():
        path = REPO_ROOT / rel
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        merged, orphans = reattach(rendered, old)
        for key in orphans:
            report.warn(rel, None, f"user region key=\"{key}\" no longer exists in canon; "
                                   "preserved under `## Orphaned entries` — rehome it by hand")
        if not path.exists():
            if check_only:
                report.note(f"{rel}: not yet generated")
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(merged, encoding="utf-8")
            report.note(f"{rel}: written ({len(merged.splitlines())} lines)")
            continue
        if merged == old:
            report.note(f"{rel}: unchanged")
            continue
        if check_only:
            diff = generated_diff(rel, old, merged)
            report.fail(rel, None, "generated regions are out of date — run `make regen`:\n" + "".join(diff[:60]))
        else:
            path.write_text(merged, encoding="utf-8")
            preserved = len(parse_regions(old))
            report.note(f"{rel}: regenerated ({preserved} user region(s) preserved byte-for-byte)")


def run_delta(report: Report, canon: dict, month_key: str, force: bool) -> None:
    months = canon.get("months") or {}
    key = month_key.zfill(2)
    month = months.get(key)
    if month is None:
        report.fail("canon/canon.yaml", None, f"no month `{key}` in canon (expected one of {', '.join(sorted(months))})")
        return

    retro = (canon.get("question_sets") or {}).get("monthly_retrospective") or {}
    eleventh = retro.get("eleventh_output") or {}
    mandated = month.get("mandated_delta") or {}

    out = [f"# Canon delta — {month['id']}", "",
           "Scaffolded by `make delta`. This is a WORKING DOCUMENT, not canon. Fill it in from the",
           f"{month['id']} retrospective, then apply the edits to `canon/canon.yaml` yourself.", "",
           "## Procedure", "",
           f"{eleventh.get('procedure', 'answer -> record -> make delta -> edit canon.yaml, bump meta.version -> make regen -> make check')}",
           "",
           "- [ ] every question below answered from evidence, not from memory",
           "- [ ] the mandated delta below applied to `canon/canon.yaml`",
           "- [ ] `meta.version` bumped",
           "- [ ] `make regen` run",
           "- [ ] `make check` green",
           "",
           "## Mandated delta", "",
           f"**Type:** `{mandated.get('type', '—')}`", ""]
    for field in ("procedure", "plus_conditional", "why_here"):
        if mandated.get(field):
            out += [f"**{field.replace('_', ' ').capitalize()}.** {mandated[field]}", ""]
    out += ["**Edits to make:**", "", "```yaml", "# path.into.canon: old -> new", "```", "",
            "## Retrospective", ""]
    for question in retro.get("questions") or []:
        out += [f"### {question['id']} — {question['text']}", "", "_answer:_", ""]
    if eleventh:
        out += [f"### {eleventh['id']} — {eleventh['text']}", "",
                f"{eleventh.get('status', '')}", "", "_the edit this month produces:_", ""]

    DELTA_DIR.mkdir(parents=True, exist_ok=True)
    path = DELTA_DIR / f"{month['id']}-canon-delta.md"
    if path.exists() and not force:
        report.fail(str(path.relative_to(REPO_ROOT)), None, "already exists; pass --force to overwrite")
        return
    path.write_text("\n".join(out), encoding="utf-8")
    report.note(f"{path.relative_to(REPO_ROOT)}: scaffolded from {month['id']} "
                f"({len(retro.get('questions') or [])} questions + {eleventh.get('id', 'RQ-11')})")


def run_selftest(report: Report, canon: dict, derived: dict) -> None:
    """The control that proves the generator cannot eat the user's numbers."""
    if not FIXTURE_SCOREBOARD.exists():
        report.fail(str(FIXTURE_SCOREBOARD.relative_to(REPO_ROOT)), None, "fixture missing; the preservation guarantee is unproven")
        return

    fixture_text = FIXTURE_SCOREBOARD.read_text(encoding="utf-8")
    before = parse_regions(fixture_text)
    if not before:
        report.fail(str(FIXTURE_SCOREBOARD.relative_to(REPO_ROOT)), None, "fixture carries no user:actuals regions")
        return

    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "SCOREBOARD.md"
        shutil.copyfile(FIXTURE_SCOREBOARD, scratch)

        merged, orphans = reattach(render_scoreboard(canon), scratch.read_text(encoding="utf-8"))
        scratch.write_text(merged, encoding="utf-8")
        after = parse_regions(scratch.read_text(encoding="utf-8"))

        # 1. every body survives byte-for-byte
        for key, body in before.items():
            if key not in after:
                report.fail("selftest", None, f"user region key=\"{key}\" was DROPPED by regeneration")
            elif after[key] != body:
                report.fail("selftest", None,
                            f"user region key=\"{key}\" was MODIFIED by regeneration:\n"
                            f"    before: {body!r}\n    after:  {after[key]!r}")

        # 2. keys canon no longer defines land in Orphaned entries, not nowhere
        known = {row["id"] for row in (canon.get("scoreboard_metrics") or {}).get("rows") or []}
        expected_orphans = sorted(set(before) - known)
        if sorted(orphans) != expected_orphans:
            report.fail("selftest", None,
                        f"orphan detection wrong: expected {expected_orphans}, got {sorted(orphans)}")
        body = scratch.read_text(encoding="utf-8")
        orphan_section = body.split("## Orphaned entries", 1)[-1]
        for key in expected_orphans:
            if f'key="{key}"' not in orphan_section:
                report.fail("selftest", None, f"orphaned key=\"{key}\" is not under `## Orphaned entries`")

        # 3. the generator is not a no-op: generated lines really were rewritten
        if merged == fixture_text:
            report.fail("selftest", None, "regeneration changed nothing outside the user regions; "
                                          "a generator that never writes cannot be shown to preserve anything")

        # 4. regeneration is idempotent, so `--check` is a genuine no-op diff
        again, _ = reattach(render_scoreboard(canon), merged)
        if again != merged:
            report.fail("selftest", None, "regeneration is not idempotent; `gen-derived --check` would never be clean")

        # 5. the self-test must itself be able to fail. Render the regions
        #    empty — the destructive outcome this whole mechanism exists to
        #    prevent — and confirm the comparison above would have caught it.
        destroyed = parse_regions(
            REGION_RE.sub(lambda m: m.group("open") + USER_REGION_PLACEHOLDER + "\n" + m.group("close"),
                          render_scoreboard(canon)))
        if any(destroyed.get(key) == body for key, body in before.items()):
            report.fail("selftest", None,
                        "the preservation comparison cannot distinguish a preserved region from a destroyed one; "
                        "this self-test proves nothing")

    report.note(f"selftest: {len(before)} user region(s) preserved byte-for-byte, "
                f"{len(orphans)} orphan(s) rehomed, regeneration idempotent")


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate ROADMAP, SCOREBOARD, CANON.md and the derived funnel targets.")
    parser.add_argument("--check", action="store_true", help="verify the generated regions are up to date; write nothing")
    parser.add_argument("--delta", metavar="MONTH", help="scaffold a canon-delta stub from that month's retrospective")
    parser.add_argument("--force", action="store_true", help="overwrite an existing delta stub")
    parser.add_argument("--selftest", action="store_true", help="run the user-region preservation fixture self-tests")
    args = parser.parse_args()

    canon = load_canon()
    report = Report("gen-derived")
    derived = derive_month_funnel_targets(canon)

    if args.delta:
        run_delta(report, canon, args.delta, args.force)
        return report.finish()

    if args.selftest:
        run_selftest(report, canon, derived)
        return report.finish()

    check_derived_funnel(report, canon, derived)
    run_generate(report, canon, derived, args.check)
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
