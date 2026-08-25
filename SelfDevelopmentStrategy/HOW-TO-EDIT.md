# How to edit this repository

## When to use this

Use this at a month boundary, after answering that month's ten retrospective
questions, when an answer implies a change to the plan itself. Do not use it
mid-week: weekly logging goes inside `<!-- user:actuals -->` regions and never
touches YAML.

Prose expands `canon/canon.yaml` and never contradicts it. So a change to the
plan is an edit to canon followed by a regeneration — never a hand-edit to a
generated file, and never a quiet correction in one file that leaves the other
seventy-six disagreeing with it. RQ-11, the eleventh output of every
retrospective, exists to force that: ten questions produce answers, and RQ-11
turns an answer into an edit. Without it the retrospective is a diary.

## Template

Copy this into the retrospective, one block per change.

```
Delta id:        <month>-<n>
Triggered by:    <RQ-nn, a threshold row, or a checkpoint>
Canon path:      <dotted path, e.g. weeks.05.hours.building>
From:            <current value>
To:              <new value>
Evidence:        <logged actuals, measured rate, deliverable id>
Downstream:      <rows this invalidates; cut_list ids drawn, if any>
```

## The control loop

Six steps, in order. Stopping early leaves canon and prose disagreeing, which is
worse than not editing at all.

1. **Answer** all ten questions in the month file. All ten, every month.
2. **Record what changed** — one delta block per change, using the template above.
3. **`make delta`** to scaffold the canon delta from those answers.
4. **Edit `canon.yaml`** and bump `meta.version`.
5. **`make regen`** to rewrite ROADMAP.md, SCOREBOARD.md, `canon/CANON.md` and
   the derived month funnel targets.
6. **`make check`** and clear every failure before you close the month.

## Which retrospective owns which edit

Each month has exactly one mandated delta, stated in its own file. M01
recalibrates hours against four weeks of logged actuals, invoking `cut_list[]`
above a 15% overrun in any bucket. M02 recalibrates the funnel against the
measured reply rate, and must state its sample size beside any revised band.
M03 re-verifies the dated ecosystem claims. Months 04 through 12 each carry
their own, from scope recalibration to the year-two rewrite.

## Rules that survive an edit

`make regen` preserves every `<!-- user:actuals -->` region byte-for-byte and
reattaches it by key. That is a hard precondition, not a nicety: the M01 hour
recalibration reads exactly those regions, so a regeneration that clobbered them
would destroy its own input. Regions whose key no longer exists land in
`## Orphaned entries` rather than being dropped.

Two rules are never edited away by a delta. The budget scales — 8h, 15h or 25h —
by changing depth and calendar, never the P0 deliverable set. And a missed week
is never doubled up: slip the calendar and run that week's named 8-hour subset.
An overrun is resolved from `cut_list[]`, never by compressing stated hours.
