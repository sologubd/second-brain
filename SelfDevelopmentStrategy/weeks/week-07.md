# Week 07 — The Sentry lane on real misleading data

## Outcome

By Sunday a real historical Sentry issue becomes a reproduction, a hypothesis, a
regression test, a fix and a pull request without me writing the diff — and I
know how the lane behaves when the stack trace lies.

## Time budget

- Theory: 3.0 h
- Building: 6.0 h
- Testing/evaluation: 3.0 h
- Customer discovery: 3.0 h

S3 is the week's one new subsystem, and it enters on two preconditions: S2 has
exited, and a Sentry project holding real historical issues is connected. USI-02
supplies the second, and it is the asset the week is built around — issues that
already happened, each with the commit that actually fixed it, which makes them a
labelled ground-truth corpus rather than a demo.

The lane sits here rather than at month 04 for one reason, worth stating because
the position looks premature: correlating a stack trace with the source that
caused it **is retrieval**. T-w07-5 builds no second search system, it reuses the
SKA layer from weeks 05 and 06 against a new query shape. At month 04 the
correlation step would have had to be improvised; here it inherits a measured
retriever — which is why W06 built the first 12 labels and W07 spends its testing
hours completing and consuming them.

T-w07-2 at 4.0 h is the largest single task in the programme; canon prices no
other above 3.5 h. Ceilings are EUR 0.00 and 70 agent runs, derived as the
20-issue corpus at roughly three lane attempts each — canon offers no rationale
beyond that count, so the count is what this file states. These are planned
figures: an overrun costs calendar, never scope. One deferral arrives from last
week and must not be assumed away. W06's compressed subset pushes its chunking
sweep here, but this week is already full at 15.0 h and carries no chunking work:
it absorbs the Sentry half of that deferral through T-w07-6 and not the chunking
half. If the sweep slips, it slips into the calendar.

Compressed week, 8.0 h: T-w07-2, T-w07-3 cut from 1.5 h to 1.0 h, and the
discovery block of T-w07-10, T-w07-11 and T-w07-12 whole at 3.0 h — workflow
documentation #1 is a portfolio input with no cheaper substitute. T-w07-1,
T-w07-4, T-w07-5 and T-w07-6 — corpus completion — and the failure-mode taxonomy
all defer to [week 08](week-08.md), where canon notes Track B holds 9.0 h. What
survives is the lane itself, which is the right floor: a Sentry lane that cannot
open a PR is not a reduced lane but a different one. D-w07-4 ticks. D-w07-1
carries without its 20-issue corpus or its correlation figure, D-w07-2 whole, and
D-w07-3 is written from one issue rather than the corpus and finished in W08.
DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| automated PR generation | A | P0 | T-w07-2's final stage → D-w07-1 |
| context construction | C | P0 | T-w07-4 settles the split, T-w07-2 spends it → D-w07-1 |
| retries | A · B | P0 | T-w07-1's nondeterministic retry, then T-w07-9 → D-w07-2 |
| domain modeling | B | P0 | T-w07-7 names the classes → D-w07-2 |
| failure recovery | B | P0 | T-w07-8 and T-w07-9's three-way mapping → D-w07-2 |
| trace evaluation | C | P0 | AC-w07-3a judges the whole lane run, not the final fix → D-w07-3 |
| malicious tool output | D | P0 | T-w07-3's Track D reinforcement — a Sentry event body is attacker-reachable text → D-w07-3 |
| outreach | E | P0 | T-w07-10 and T-w07-11 → D-w07-4 |

Every row resolves to a canon concept carrying P0, so none needs the earn-it or
competency fallback. Two deserve a word. `retries` is double-homed on purpose:
canon carries it once under Track A and once under Track B, the second row
deferring explicitly to the first, and this is where the halves meet — a retry
that cannot reproduce the previous attempt, and a taxonomy deciding which errors
are worth retrying at all. `malicious tool output` is not attacked here; canon
names a Sentry event body among the conduits for attacker-supplied text arriving
with an internal component's authority, and T-w07-3 reinforces Track D on exactly
that surface.

Homes split four ways. Automated PR generation reasons from
[Track A](../tracks/agentic-engineering.md), which also owns the Track A half of
retries; context construction and trace evaluation from
[Track C](../tracks/ai-application-engineering.md); domain modeling, failure
recovery and the Track B half of retries from
[Track B](../tracks/system-design.md); malicious tool output from
[Track D](../tracks/ai-security.md). Outreach is homed in
[the outreach file](../business/outreach.md) rather than its own track, while the
workflow-documentation practice and its consulting stage belong to
[Track E](../tracks/consulting.md), two of the three business tasks reinforcing
[Track F](../tracks/micro-saas.md). S3 belongs to
[the platform](../projects/engineering-agent-platform.md), and the retrieval layer
T-w07-5 borrows to
[the Secure Knowledge Agent](../projects/secure-knowledge-agent.md).

## Tasks

### Task 1

`T-w07-1` — 1.5 h, Track A, theory, reinforcing B. Reading: `RES-03`. The lane
as a workflow with agent-shaped steps, and hypothesis-driven debugging when
the work unit is NONDETERMINISTIC. The consequence is sharper than it sounds:
a retry is a new attempt carrying prior state, not a replay, so it does
something different and the previous failure cannot be assumed reproducible.

### Task 2

`T-w07-2` — 4.0 h, Track A, building, reinforcing C. Build S3 across its ten
stages, which run from the Sentry issue through event investigation and
codebase correlation to a reproduction, then a hypothesis, then
instrumentation, a regression test, the fix, verification, and the PR.
Reproduction sits ahead of hypothesis deliberately — swap them and the lane
argues a fix from a trace.

### Task 3

`T-w07-3` — 1.5 h, Track A, testing, reinforcing D. Run the lane against a
REAL historical issue whose stack trace points away from the true cause, and
write the five-part report. Pick it from the labelled corpus, where the fixing
commit is known, so the lane's answer can be marked rather than admired.

### Task 4

`T-w07-4` — 1.0 h, Track C, theory, reinforcing A. Reading: `RES-01`. Context
construction for the diagnosis step: what the agent must be GIVEN against what
it must RETRIEVE, and what getting the split wrong costs. Too little and it
retrieves noise; too much and the signal it needed is buried in what you
supplied.

### Task 5

`T-w07-5` — 1.5 h, Track C, building, reinforcing A. Reuse the SKA retrieval
layer to correlate a stack trace with the source files that matter. A frame
list is a query with unusual shape, not a new retrieval problem — which is the
whole argument for the lane arriving in week 7 rather than month 4.

### Task 6

`T-w07-6` — 1.0 h, Track C, testing. Complete the labelled corpus to 20 issues
and measure correlation precision@k against it — the programme's first
retrieval number computed over data that was never constructed for the
purpose, which is what makes it worth more than the frozen set.

### Task 7

`T-w07-7` — 0.5 h, Track B, theory, reinforcing A. Reading: `RES-15`. Build
the production failure-mode taxonomy as DOMAIN MODELLING — name the classes of
thing that actually go wrong in this codebase. Canon's argument for domain
modelling applies directly here: the vocabulary you supply is the compression
scheme for every later instruction, and a taxonomy of generic categories
compresses nothing.

### Task 8

`T-w07-8` — 0.5 h, Track B, building. Encode the taxonomy into the task state
machine's error classification, so a class is a value the machine records
rather than a document beside it.

### Task 9

`T-w07-9` — 0.5 h, Track B, testing. Assert that every class maps to exactly
one retry decision — retry, dead-letter, or escalate to a human. Exactly one:
a class with two decisions is two classes, and a class with none is a silent
hang.

### Task 10

`T-w07-10` — 0.7 h, Track E, business, reinforcing F. Eight cold emails
assisted by BOA-S0, reviewed and approved individually. These do not reach
this Sunday's rows — the 33 they read is already fixed by W06's nine. These
eight mature into W08's 41, which is where ACT-1 sits.

### Task 11

`T-w07-11` — 0.4 h, Track E, business. Twelve follow-ups, two per prospect
written to. Canon's best-evidenced conversion figure puts a large share of
replies here rather than on the first touch, so a follow-up carrying nothing
new wastes one of the two.

### Task 12

`T-w07-12` — 1.9 h, Track E, business, reinforcing F. Workflow documentation
#1: from a real discovery call if one has happened, otherwise from a Stage-1
simulated engagement, documented end-to-end from public information. Canon is
explicit that the simulated route is the EXPECTED path here and not a
concession — with 0.12 to 1.46 calls expected across all 52 sends, no call by
week 7 is ordinary. W03 rehearsed this exact substitution so it would be
practised rather than improvised, and [the interview
template](../templates/discovery-interview.md) carries the script. Tag the
artifact `evidence_source: simulated` and it is a passing deliverable; present
it as real and it is a programme failure.

## Deliverables

- [ ] D-w07-1 — S3 Sentry lane producing a real PR from a real historical issue — definition of done includes a 20-issue labelled corpus and a measured correlation precision@k on it — at `agentplat/sentry/`, `evals/sentry-corpus.jsonl`, `docs/w07/correlation-precision.md`
- [ ] D-w07-2 — Production failure-mode taxonomy wired into the state machine's error classification, with every class mapped to exactly one retry decision — at `docs/w07/failure-taxonomy.md`, `agentplat/state/errors.py`
- [ ] D-w07-3 — Failure report — misleading Sentry stack trace, from the real corpus — with all five parts — at `docs/w07/misleading-stack-trace-report.md`
- [ ] D-w07-4 — Workflow documentation #1, tagged evidence_source: real or simulated, plus 8 sends and 12 follow-ups logged — at `workflow-01.local.md`, `send-log.local.md`

## Acceptance criteria

- [ ] AC-w07-1a — at least one PR exists that the lane produced end-to-end from a Sentry issue id, carrying a regression test that fails on the parent commit and passes once the fix is applied; the write-up classifies each of the ten stages as workflow-shaped or agent-shaped and states what a retry does when the step cannot be replayed, names for the diagnosis step what the agent was GIVEN against what it RETRIEVED, and shows the correlation step running through the SKA retrieval layer rather than a fresh search built for the occasion (T-w07-2, T-w07-1, T-w07-4, T-w07-5)
- [ ] AC-w07-1b — the corpus contains 20 labelled issues; correlation precision@k is reported as a number with a stated k (T-w07-6)
- [ ] AC-w07-2a — every error the state machine can record maps to exactly one of retry, dead-letter or escalate; an unmapped error class fails a test; and each class in the taxonomy is traceable to something that has actually gone wrong in this codebase rather than to a generic category list (T-w07-8, T-w07-9, T-w07-7)
- [ ] AC-w07-3a — the misleading-stack-trace report contains all five named sections and states what the lane did BEFORE the mitigation, not only after, and each proving test fails against the pre-mitigation code (T-w07-3)
- [ ] AC-w07-4a — workflow documentation #1 names the steps, the frequency, the current time cost and at least one automatable segment, and carries an evidence_source tag; and the week's funnel row reaches SCOREBOARD — 8 sends and 12 follow-ups, with the workflow document counted and its `evidence_source` marked (T-w07-12, T-w07-10, T-w07-11)

## Stretch goal

Outside the 15 hours. Measure whether the lane's hypothesis step is doing work:
run it with the hypothesis stage removed and compare fix correctness across the
20-issue corpus. The corpus is what makes this answerable at all: 20 issues with
known fixing commits is a scoreable set, so the ablation returns a number rather
than an impression. Attempt it only once the four deliverables hold.

## Failure exercise

One exercise, and it runs on real data rather than a fixture — the lying stack
trace was chosen from the corpus, not written to mislead. The full body lives in
[the agent-failure set](../exercises/agent-failures.md); D-w07-3 is the report.

### EX-FAIL-09 — Sentry event with misleading stack trace

- **Detection.** The top frame is not the fault site — it is a wrapper, a serialiser, or a framework boundary that caught something thrown elsewhere. Detected when a reproduction built from the top frame does not reproduce. That is the only reliable signal available: the trace itself looks equally plausible either way.
- **Safe failure behaviour.** Require a REPRODUCTION before any hypothesis is accepted. A fix proposed from a trace alone is a guess with a diff attached, and it is a convincing guess, because the model will happily write a defensible-looking change against the wrong frame.
- **Recovery.** Widen from the trace to the correlated commit and to the retrieval layer's view of the surrounding module, then re-derive the hypothesis from the reproduction rather than from the trace. The trace becomes one input among several instead of the premise.
- **Logging.** Record the top frame, the frame the reproduction actually implicated, and the correlation precision of the retrieval step for that issue. The gap between the first two fields is the measurable form of this failure, and the third says whether retrieval or reasoning was at fault.
- **Test proving the mitigation.** Take a real historical issue from the labelled corpus whose trace points away from the fixing commit, and assert the lane diagnoses it correctly while the run that skips reproduction produces the wrong fix. It must FAIL against the version that accepts the top frame — that version is what S3 is until this exercise lands.

## Reflection

1. The stack trace pointed away from the fault. What made the reproduction step
   non-optional rather than merely good practice?
2. What did the agent need to be GIVEN versus what could it RETRIEVE — and what
   did getting that split wrong cost you in this week's runs?
3. Every error class now maps to retry, dead-letter or escalate. Which mapping
   are you least confident in, and what evidence would change it?

## Evidence

- `make demo-s3 ISSUE=<sentry-id>` — this stage's runnable demo command.
- Link to the PR the Sentry lane produced end-to-end.
- The regression test failing on the parent commit and passing on the fix.
- Correlation precision@k on the 20-issue corpus.
- Path to the failure-mode taxonomy and its retry-decision mapping.
- Path to the misleading-stack-trace failure report.
- Path to workflow documentation #1 with its evidence_source tag.

Both remaining watch rows land this Sunday, against 33 matured sends. WATCH-3
trips on one reply or fewer — canon calls it the median row, 53.5% likely at the
band midpoint and 91.1% at the floor. WATCH-4 trips on no booked call at 67.6%,
and canon demoted it out of the activation set precisely because a zero-call
result at this volume is an expected outcome rather than an anomaly. Log both to
[the scoreboard](../SCOREBOARD.md) and take no action; they were pre-announced in
[phase 01](../phases/phase-01-foundations.md#checkpoints) with these likely
outcomes attached. No call slot is budgeted this week — the next reserve is
W08's — so a week with no call loses no hours, and D-w07-4 substitutes its
fallback automatically for this week only.

Record the hours actually spent as one line below, plan first:
`Theory 3.0 / <actual> · Building 6.0 / <actual> · Testing 3.0 / <actual> ·
Discovery 3.0 / <actual>`. Four regions of identical shape are what the mandated
recalibration parses. Funnel counts go to the scoreboard.

<!-- user:actuals key="W07" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- The lane produces a real PR from a real Sentry issue — 30
- The corpus reaches 20 issues with correlation precision@k reported — 20
- Every taxonomy class maps to exactly one retry decision — 15
- The misleading-stack-trace report carries all five named parts — 15
- Workflow documentation #1 delivered with its evidence_source — 20
