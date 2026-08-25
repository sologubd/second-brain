# Outreach — cold sends from a standing start

## Purpose

This file owns the sending machine — message shapes, follow-up cadence, and the
branch that fires when replies do not arrive.
[Track E](../tracks/consulting.md) reasons about acquisition; canon homes C-093
here, not in its track.

The starting position is a recorded fact. USI-03 captures it in the learner's
own words — *"nothing, i gonna build it."* No warm network, no referral path, no
case study. All 52 first touches go to a stranger found through public sources.
ZP-2 and ZP-3 make that checkable: no warm introduction and no pre-existing
contact may enter the list, and every message records its own per-touch outcome
against a stated expectation that most return nothing.

The unanswered objection is the missing case study, and it is not argued away.
ZP-4 answers it with a named artifact — D-w03-3, a workflow documented end to
end at a public company from public information. That is what gets shown when a
prospect asks who else this has been done for.

## The instrument

### Where a prospect comes from

Public sources only: company sites, job ads, filings, product documentation,
meetup listings. Checklist CL-1 lives in
[customer discovery](customer-discovery.md) and doubles as the specification
BOA-S0 is built against — a procedure nobody wrote down cannot be automated. 24
of the 56 prospects are researched by hand before that extractor exists, the
other 32 with its help, every draft approved before it leaves.

### The three message shapes

Templates carry placeholder identities so the repository can be made public
without a scrub. Real prospect data belongs in a gitignored `*.local.md` file.

```text
FIRST TOUCH — subject: [specific process] at [Company]
  [First name] — [public signal: job ad / docs page / filing] suggests
  [named manual step] is still done by hand.
  I build Python automation for exactly that step.
  Have I read it right? Twenty minutes would tell us.

FOLLOW-UP 1 (+4 days) — new information, not a reminder
  Adds a second observed signal, or the concrete before/after
  from the Stage-1 rehearsal document.

FOLLOW-UP 2 (+9 days) — narrower ask, then stop
  Replaces the meeting request with one answerable question,
  and says plainly that this is the last message.
```

### The cadence

Two follow-ups per prospect sent to. Not a guess: 58% of replies land on the
first touch, 42% on a follow-up, with independent datasets giving a 42–65%
range — the best-supported figure in the model, and why 104 follow-ups are
budgeted against 52 sends. Each must carry new information; a bare check-in
costs goodwill and buys nothing.

| Week | First touches | Follow-ups | Sends matured by Sunday |
|---|---|---|---|
| W02 | 4 | 0 | — |
| W03 | 5 | 8 | 4 |
| W04 | 6 | 9 | 9 |
| W05 | 9 | 10 | 15 |
| W06 | 9 | 12 | 24 |
| W07 | 8 | 12 | 33 |
| W08 | 6 | 14 | 41 |
| W09 | 5 | 17 | 47 |
| W10 | 0 | 12 | 52 |
| W11 | 0 | 10 | 52 |

Maturation assumes a send made in week N is answerable by the end of week N+1,
the fast end of a 1.5 to 3.0 week band. On the slower read every branch row
below fires a week later — recorded, not hidden.

### Handling a reply

Reserve the slot before the reply exists: handling inside four hours reportedly
doubles conversion, on low-confidence evidence, so the W04 and W05 call slots
sit in the calendar in advance. A reply is not progress on its own — declines,
unsubscribes and gatekeeper messages land in the same column — so declines get
their own count.

Email only. Vendors selling LinkedIn tooling report it beating cold email, none
of it independently corroborated, so this design plausibly leaves upside
unclaimed and puts no number on it.

## Exercises

### Exercise 1 — the first cold batch

#### Objective

Send cold email to strangers and survive the silence, so the funnel becomes a
measured object rather than an intention.

#### Task

Pick 4 prospects from the W02 public-sources list, write each first touch by
hand against the shapes above, send them, and open a send log with one row per
touch.

#### Constraints

Hand-written only — BOA-S0 does not exist yet. No warm introduction, no
referral, no contact already known. One quoted public signal per message, no
attachment, no calendar link.

#### Deliverable

D-w02-3 — a send log at `send-log.local.md`, one row per touch, six fields in
this order: placeholder prospect id, date, shape, signal cited, outcome,
`evidence_source`. Every rate computed from it states its denominator, which is
what `DT-10` requires of a metrics report and is the only sense in which this log
is one. The weekly roll-up into SCOREBOARD is a different shape, fixed by
`scoreboard_metrics.weekly_row_format` and rendered in
[the scoreboard](../SCOREBOARD.md) itself.

#### Acceptance criteria

- 4 first touches are sent and exactly 4 rows exist in `send-log.local.md`.
- Every row cites a public source, and 0 rows name a warm introduction.
- Each outcome is one of 4 permitted values: no reply, decline, reply, call booked.

#### Metrics

Response rate = replies ÷ first touches sent, denominator beside it. Over a
batch of 4 the expected reply count is below 1, so the number is logged, not
interpreted.

#### Reflection questions

1. Which signal did you cite, and what would you have written had that company
   published nothing?
2. Which sentence reads as a pitch rather than a question?
3. What changes for the next batch, and how would the log tell you it worked?

### Exercise 2 — the follow-up ladder

#### Objective

Prove per-touch attribution: 42% of replies arrive after the opening message,
and an aggregate count hides which touch earned them.

#### Task

For every prospect contacted in W03 through W05, send two follow-ups, each
carrying something the previous touch did not, and attribute every reply to the
touch that produced it.

#### Constraints

Two per prospect, no more, no bare check-ins. Each takes a different angle: a
second observed signal, a before/after from the Stage-1 rehearsal, or a
narrower ask.

#### Deliverable

D-w05-3 — the send log extended with a touch index and an attribution column,
plus the call-slot outcome and its `evidence_source`.

#### Acceptance criteria

- 27 follow-ups are logged across those three weeks, matching 8 + 9 + 10.
- Every reply row names the touch index that produced it; 0 replies are unattributed.
- 0 follow-ups repeat the previous touch's ask verbatim.

#### Metrics

Follow-up share = replies attributed to touches 2 and 3 ÷ all replies received.
The prior is 0.42, and against an expected 0.78 to 4.16 replies programme-wide
that sample can neither confirm nor refute it — which is why the prior is
written down before measuring starts.

#### Reflection questions

1. Which touch would you drop if the hours halved, and what does the log say
   rather than your memory?
2. What did the third touch carry that the first could not?
3. If the follow-up share reads 0 programme-wide, what do you conclude, and what
   would you need before changing the cadence?

## Targets and thresholds

Volumes are the user's own choice under USI-06 and are never quietly
re-inflated: 56 prospects researched, 52 sends, 104 follow-ups, 2 workflow
documents, 2 scored opportunities, across twelve weeks.

Conversion is where the honesty lives. Every percentage below comes from
vendor-published cold-email marketing, written by firms that profit from
outreach looking winnable, and none of it separates a solo operator with no
network from a sales team holding a case-study library.

| Quantity | Value | Confidence |
|---|---|---|
| Reply rate | 1.5–8%, midpoint 4.75% | Moderate at 3–6%; low above 8% |
| Reply to booked call | 15–35%, midpoint 25% | Low — the model's weakest number |
| Replies from follow-ups | 42% (range 42–65%) | Moderate-high; converging datasets |
| Replies from 52 sends | 0.78 – 4.16 (midpoint 2.47) | Poisson, at those bands |
| Calls from 52 sends | 0.12 – 1.46 (midpoint 0.62) | 0–1 expected, planned as 1 |

Stated plainly rather than buried: no call at all, across the whole programme,
is the single most likely result — 53.9% at the midpoint, 23.3% even at the top
of the band.

**The branch carries two classes of row, and they differ in kind.**

| Row | Trips when | Likelihood at the midpoint | Class |
|---|---|---|---|
| WATCH-1 | 9 matured sends, still no reply (end of W04) | 65.2%; 87.4% at floor | Watch |
| WATCH-2 | 15 matured sends, no call booked (end of W05) | 83.7%; 65.7% at ceiling | Watch |
| WATCH-3 | 33 matured sends, at most one reply (end of W07) | 53.5%, the median row; 91.1% at floor | Watch |
| WATCH-4 | 33 matured sends, no call booked (end of W07) | 67.6% — expected, not anomalous | Watch |
| ACT-1 | 41 matured sends, still no reply (end of W08) | 14.3%; 54.1% floor, 3.8% ceiling | Activation |
| ACT-2 | 52 matured sends, still no reply (end of W10) | 8.5%; 45.8% floor, 1.6% ceiling | Activation |

Watch rows are *expected* to trip. Log the event to the scoreboard and change
nothing; they are pre-announced in
[phase 01](../phases/phase-01-foundations.md#checkpoints) at week one precisely
so a trip reads as the model behaving as designed. Activation rows sit genuinely
below the band, and tripping one escalates to three programme-level moves: the
funnel is re-pitched in an out-of-cycle canon delta, the simulated Stage-1 track
extends across whatever business deliverables remain, and any hours reclaimed
come from the cut list. Both count replies; neither counts calls, because a
zero-call event says almost nothing when zero is the median, and a row firing on
the median teaches its reader to ignore it.

Substitution runs underneath both classes, automatically and *partially*: a
deliverable whose real-evidence precondition is missing in its due week swaps in
its fallback for that week alone, tagged simulated. One at a time, never a
wholesale flip, so PF-07 — the one real external case study — survives a weak
funnel as long as any single deliverable stays real.

## Evidence discipline

Every artifact here carries `evidence_source: real | simulated` on its
scoreboard row, so a substitution stays visible and can never inflate the funnel.
Real means an outside party genuinely replied, spoke or paid; simulated means
the Stage-1 rehearsal path stood in.

Inventing evidence is the failure the kill-criteria framework exists to prevent.
An honestly tagged simulated artifact is a passing deliverable; the same
artifact presented as real is a programme failure. There is no third category.
SM-21 paid pilots and SM-22 revenue are never simulated at all — both are
expected to read zero through month 06 and quite possibly past it, and both are
recorded anyway, because a board that drops its hardest measure has stopped
measuring.

Counts live in [the scoreboard](../SCOREBOARD.md), not here: SM-15 prospects,
SM-16 sends, SM-17 replies with declines held separate, SM-18 calls. The M2
recalibration reads those rows and re-pitches the bands above from measured
data, so a week that never logged its counts leaves that delta nothing to read.

Placeholder identities throughout: no client name and no prospect PII in a
tracked file, and the real send log gitignored beside this one.
