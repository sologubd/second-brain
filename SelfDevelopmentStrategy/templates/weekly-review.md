# Weekly review

## When to use this

Fill one at the close of every week, before the next week opens. It is the blank
form; [README.md](../README.md) describes the process around it and the week
file's own scoring section is where the number lands. Filling it sits outside the
15 hours and takes about twenty minutes: the week's tasks total 15.0 exactly, and
the instrument that measures the work is not the work. Work from the week file's
evidence — commits, pull requests, benchmark output, interview notes — rather
than from recollection. Memory reliably scores a week by how it felt on Friday,
which is uncorrelated with what shipped.

The hours line is the part with a consumer downstream. Four buckets, plan and
actual, in one shape that does not vary between weeks, because the first
retrospective's hour recalibration reads four weeks of these and rewrites the
remaining budgets from them. Freeform notes give it nothing to work with. Log
the actual even when it embarrasses the plan, and especially then: an overrun
above fifteen per cent in any bucket is what draws from the cut list, and a
bucket quietly rounded down cannot draw.

Reserved time that went unused is logged, never spent elsewhere. A budgeted call
slot with no call on the other end is the ordinary case rather than a failure —
across the whole programme the most likely number of calls in any given week is
zero — so the hours return as recorded slack. Silently absorbing them into
building work destroys the only signal that the discovery budget was ever real.

## Template

Copy the block into a note, an issue, or a file kept outside version control. It
is deliberately short: everything in it is either copied from the week file or is
a number, and a review that takes longer than twenty minutes stops being written
by week nine.

One rule governs the last section. Anything the week taught you that would change
a plan row is written down here and acted on nowhere — not in canon, not in the
week files, not as a quiet correction. It waits for the month boundary and the
loop in [HOW-TO-EDIT.md](../HOW-TO-EDIT.md), which is the only sanctioned way the
plan mutates. Weekly editing of the plan is how a programme becomes a record of
its own drift.

```markdown
# Week NN review

- **Dates:** <YYYY-MM-DD> to <YYYY-MM-DD>
- **Outcome sentence:** <met / partly met / not met> — <one line of evidence>

## Hours

Theory <plan> / <actual> · Building <plan> / <actual> · Testing/evaluation <plan> / <actual> · Customer discovery <plan> / <actual>

Bucket over plan by more than fifteen per cent: <bucket, or none>
Reserved and unused: <hours> — <what reserved them; logged as slack, not re-spent>

## Deliverables

| Id | Shipped | Evidence |
| --- | --- | --- |
| `D-wNN-1` | <yes / partial / no> | <path, commit or link> |

## Acceptance criteria

| Id | Met | What proves it |
| --- | --- | --- |
| `AC-wNN-1a` | <yes / no> | <the number or the artifact path> |

## Score

| Component | Allocated | Earned |
| --- | --- | --- |
| <component> | <n> | <n> |
| **Total** | **100** | <n> |

## Funnel row for the week

Researched <n> · sent <n> · follow-ups <n> · replies <n> · calls held <n>

## Scoreboard rows to update

- [ ] `SM-NN` — <new value, written inside its keyed region>

## Carried to the month-end retrospective

<What would change a plan row. Recorded here; edited nowhere until the boundary.>
```
