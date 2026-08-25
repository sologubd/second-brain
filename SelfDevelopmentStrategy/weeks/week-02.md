# Week 02 — The durable task state machine

## Outcome

By Sunday the platform records every step's completion durably before the next
step starts, and I can prove which of my modules are well-bounded by deleting
them and regenerating from their contracts.

## Time budget

- Theory: 3.0 h
- Building: 6.0 h
- Testing/evaluation: 2.5 h
- Customer discovery: 3.5 h

USI-10 puts distributed systems at *Working knowledge* and splits it precisely:
concept-strong, operation-weak. The concepts behind a state machine are already
held. What has never been done is running one that a `kill -9` lands inside, so
nothing below explains what a state is. Everything below is about the operating
properties — what is durable at each instant, what a restart may assume, and
which invariant is enforced by which transaction. Building takes 6.0 h, the
first week where the build outweighs the reading by two to one.

The week spends EUR 0.00 on metered inference and is capped at 25 agent runs,
the three regeneration attempts being the only expensive ones. Those are *planned*
figures; a week-file measures work rather than calendar time. W01 is a hard
dependency and not a soft one: S1a starts where S0 exits, and the Postgres
instance stood up here becomes the queue, the lock, the outbox and the vector
index for the rest of the programme.

Compressed week, 8.0 h: T-w02-3 at 3.5 h, T-w02-5 at 1.0 h, T-w02-1 at 1.0 h,
and T-w02-10 whole with T-w02-11 and T-w02-12 trimmed to 4 prospects and 2 sends
— discovery lands on its 2.5 h floor exactly. T-w02-2, T-w02-4 and T-w02-6 push
into [week 03](week-03.md); T-w02-7, T-w02-8 and T-w02-9 go to W08, where
subagent attribution finally has a consumer, since until concurrent workers exist
nothing reads it. Nothing ticks. D-w02-1 carries because the invariant table is
unwritten and AC-w02-1c goes with it; D-w02-2 and D-w02-4 carry whole; D-w02-3
ships at half its volume, which is a funnel delta to record, not absorb. Sends
are never made up later, and the week closes DONE-COMPRESSED.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| state machines | B | P0 | T-w02-1's transition table, enforced by S1a → D-w02-1 |
| domain modeling | B | P0 | T-w02-4's aggregate and invariant table → D-w02-1 |
| boundaries | B | P0 | the three contracts under test in T-w02-6 → D-w02-2 |
| coupling/cohesion | B | P0 | the deep-module ratio measured per module in T-w02-6 |
| deep modules | B | P0 | T-w02-6's regeneration transcripts → D-w02-2 |
| modularity | B | P0 | the separately regenerable packages chosen in T-w02-6 |
| checkpoints | A | P1 | T-w02-3 writes each step record before its effect, not after |
| long-running tasks | A | P1 | the `waiting_on_input` state built in T-w02-3 |
| context engineering | A | P0 | T-w02-7 → D-w02-4 |
| task decomposition | A | P0 | T-w02-8's reconstructed subagent tree → D-w02-4 |
| outreach | E | P0 | T-w02-10 and T-w02-12 → D-w02-3 |

Every row resolves to a canon concept carrying a priority, so none needs the
earn-it or competency fallback; two of them are P1 rather than P0, and both are
Track A rows that this week touches through the state machine rather than
studies on their own. Six rows are homed in
[Track B](../tracks/system-design.md) and three in
[Track A](../tracks/agentic-engineering.md). Outreach is the exception that
catches people: it is a Track E concept homed in
[the outreach file](../business/outreach.md), not in
[Track E's own file](../tracks/consulting.md), which is nonetheless where the
three business tasks reason from. Those three reinforce
[Track F](../tracks/micro-saas.md), and T-w02-3 reinforces
[Track D](../tracks/ai-security.md), because a durable record of who did what is
the first half of an audit trail. S1a's entry, exit and demo command belong to
[the platform file](../projects/engineering-agent-platform.md); this file owns
only tasks, hours and acceptance.

## Tasks

### Task 1

`T-w02-1` — 1.0 h, Track B, theory, reinforcing A. Reading: `RES-04`. Treat
the machine as data. Enumerate the states, write the legal-transition table,
and argue why a durable machine is an enum column plus a table rather than a
class per state. The argument is operational: you cannot query a class
hierarchy for every task stuck in `running` for more than an hour, you cannot
migrate one, and you cannot diff what the table says against what production
did.

### Task 2

`T-w02-2` — 0.5 h, Track B, theory. Reading: `RES-13`. Aggregate boundary,
transaction boundary and consistency boundary are one boundary under three
names, and drawing it wrongly is the defect that survives every code review.
Then value objects as newtypes: a type that carries its own meaning tells an
agent at the call site what a bare string cannot.

### Task 3

`T-w02-3` — 3.5 h, Track B, building, reinforcing D. Build S1a on Postgres
over the states `pending`, `running`, `waiting_on_input`, `completed`,
`failed` and `cancelled`. The whole week turns on one implementation rule:
each step's completion commits in the same transaction as its effect. Write
the record after the effect and you have built a machine that is confidently
wrong after a crash — which is worse than one that is obviously broken.

### Task 4

`T-w02-4` — 1.0 h, Track B, building. Write the aggregate and invariant table:
one row per invariant, naming the aggregate it belongs to and the transaction
that enforces it. Naming the transaction is the point. An invariant that names
only a class is a comment, because nothing stops a second code path from
violating it.

### Task 5

`T-w02-5` — 1.0 h, Track B, testing. Generate the invalid-transition suite
from the transition table rather than writing it by hand, then add a smoke
test that kills the process between steps. A hand-written suite covers the
transitions you remembered, which is exactly the set that was never going to
surprise you.

### Task 6

`T-w02-6` — 1.0 h, Track B, testing, reinforcing A. The week's sharpest
instrument. Delete three module implementations, leaving the interface, the
docstring and the tests, then have an agent regenerate each one with no
repository context, in one shot. Every failure gets traced to a named implicit
dependency — the thing the deleted code silently knew about the rest of the
system. A module that cannot be rebuilt from its own contract was never
bounded, whatever the review said.

### Task 7

`T-w02-7` — 1.5 h, Track A, theory. Reading: `RES-05`. Context construction as
engineered state: what the adapter hands in per run against what it inherits
from wherever it happens to be running, and how a subagent keeps an identity
in a call graph. Settle in writing what it means for context to be lost,
because D-w02-4 is written against that definition.

### Task 8

`T-w02-8` — 1.5 h, Track A, building. Rebuild the subagent tree from the
harness's flat event stream using parent call ids. Flat is how the stream
arrives and nested is what happened; without the reconstruction, cost and
latency belong to the run as a whole and can never be charged to the
decomposition step that caused them.

### Task 9

`T-w02-9` — 0.5 h, Track A, testing. Assert the reconstructed tree matches a
known decomposition for a task with at least two nested subagents. Two levels
is the minimum that can expose a parent-id bug; one level cannot.

### Task 10

`T-w02-10` — 1.5 h, Track E, business, reinforcing F. Build the outreach
tooling: the prospect record schema, the send log, and per-touch attribution
fields. Attribute per touch from the very first row. Somewhere between 42% and
65% of all replies land on a follow-up instead of the opening message, and a
log unable to separate touch one from touch three cannot see that at all.

### Task 11

`T-w02-11` — 1.1 h, Track E, business, reinforcing F. Research 8 prospects by
hand from public sources, against the niche written in W01. Two fewer than
last week at roughly the same rate: the positioning note is doing work now, so
rejecting a poor fit should be faster than it was.

### Task 12

`T-w02-12` — 0.9 h, Track E, business, reinforcing F. Write and send 4 cold
emails by hand. Each opens with a diagnostic question rather than a pitch, and
each cites one verifiable fact about that prospect. These are the programme's
first sends, and together with W03's five they are the nine matured sends
WATCH-1 reads at the end of W04 — a row that trips on zero replies 65.2% of
the time at the band midpoint and 87.4% at its floor. Its response is to log
the event to [the scoreboard](../SCOREBOARD.md) and change nothing.

## Deliverables

- [ ] D-w02-1 — S1a durable task state machine on Postgres; done includes the legal-transition table, a generated invalid-transition suite, and the aggregate and invariant table naming each invariant, its owning aggregate and the enforcing transaction — at `agentplat/state/`, `agentplat/state/migrations/001_tasks.sql`, `docs/w02/transition-table.md`, `tests/test_invalid_transitions.py`, `docs/w02/invariants.md`
- [ ] D-w02-2 — Boundary post-mortem: three regeneration transcripts, the deep-module ratio per module, and for every failure the specific out-of-module knowledge the implementation had silently depended on — at `docs/w02/boundary-post-mortem.md`, `docs/w02/regeneration/`
- [ ] D-w02-3 — Outreach tooling and send log, with 8 researched prospects and 4 hand-written sends recorded per touch — at `agentplat/outreach/`, `send-log.local.md`, `prospects.local.md`
- [ ] D-w02-4 — Combined failure report, agent context loss after restart, with all five parts: detection, safe failure behaviour, recovery, logging, and a test proving the mitigation — at `docs/w02/context-loss-report.md`, `tests/test_kill_boundaries.py`

## Acceptance criteria

- [ ] AC-w02-1a — every state transition in the running system appears in the transition table, and a transition absent from the table raises rather than proceeding, proved by the suite generated from that table rather than by one written from memory (T-w02-1, T-w02-3, T-w02-5)
- [ ] AC-w02-1b — killing the process at any step boundary leaves the task in a state the table permits, and a restart resumes from the last recorded step (T-w02-3, T-w02-5)
- [ ] AC-w02-1c — the invariant table has at least six rows and every row names a transaction, not a class; each row's owning aggregate is the unit whose transaction encloses it, and at least one domain value reaches its call site as a newtype rather than a bare string (T-w02-4, T-w02-2)
- [ ] AC-w02-2a — at least one of the three modules regenerates and passes its tests on the first attempt with no repo context (T-w02-6)
- [ ] AC-w02-2b — every regeneration failure is traced to a NAMED implicit dependency, and at least one boundary is repaired and regeneration retried successfully (T-w02-6)
- [ ] AC-w02-3a — 4 sends logged with timestamp, prospect id and the personalisation fact used, and the send log distinguishes touch 1 from follow-ups; the week's funnel row is logged in SCOREBOARD — 8 prospects researched, 4 sends — with `evidence_source` marked (T-w02-10, T-w02-12, T-w02-11)
- [ ] AC-w02-4a — cost and token usage can be attributed to a specific subagent branch for a task with at least two nested subagents (T-w02-8, T-w02-9)
- [ ] AC-w02-4b — the context-loss report contains all five named sections and its proving test fails against the pre-mitigation code; its detection section names the disagreement T-w02-7 settled in writing — a recorded step pointer that contradicts the observable world — rather than an unexplained heuristic (T-w02-7)

## Stretch goal

Outside the 15 hours, attempted only once the four deliverables are ticked, and
never financed from acceptance work. Measure the deep-module ratio — public
symbols against implementation size — for every module in the platform, then
check whether it predicted regeneration success across your three samples. Three
points is far too few to conclude anything, which is itself the finding worth
writing down.

## Failure exercise

One exercise, and it is the direct adversary of everything built this week: a
restart is only safe if the record of progress and the world agree. Its body is
held in [the agent-failure set](../exercises/agent-failures.md), and D-w02-4 is
the report.

### EX-FAIL-02 — agent context loss after restart

- **Detection.** On resume, the recorded step pointer disagrees with the observable world state: a step is marked incomplete but its effect exists, or it is marked complete and the effect does not. The comparison is made at resume time, before any work restarts, because that is the only moment both readings are cheap.
- **Safe failure behaviour.** Resume from the last durably recorded step, never from an in-memory assumption about progress. Where the pointer and the world disagree, halt instead of proceeding on either — a process that picks the more convenient reading will pick it silently and be wrong at the worst moment.
- **Recovery.** Re-execute from the recorded step. Because each step's completion committed in the same transaction as its effect, re-execution is safe by construction rather than by care, and that distinction is the whole return on T-w02-3's implementation rule.
- **Logging.** Record the step pointer at kill time, the step pointer at resume, and the wall-clock gap between them. Those three fields make orphan-detection latency a measured quantity instead of an impression, and the gap is the figure W08's queue work will need.
- **Test proving the mitigation.** Kill the process at each step boundary in turn, then assert the resumed run reaches the same terminal state as an uninterrupted one and that no effect occurs twice. It fails against a version holding progress in memory.

## Reflection

1. Was the module you BELIEVED was well-bounded actually well-bounded? What did
   the regeneration failure name that a code review would not have surfaced?
2. Your transition table is a specification a machine can check. Which of its
   states exists because the domain demands it, and which because your
   implementation happens to need it?
3. Where did the invariant actually have to live — in the step code or in the
   transaction boundary? What breaks about that choice when a second worker
   appears in week 8?

## Evidence

- `make demo-s1a` — this stage's runnable demo command — with the commit or path for S1a and its migration.
- The invalid-transition test output, and the kill-between-steps smoke run.
- Three regeneration transcripts and the boundary post-mortem.
- Path to the aggregate and invariant table.
- Path to the outreach send log.

Log actual hours below as one line, planned first:
`Theory 3.0 / <actual> · Building 6.0 / <actual> · Testing 2.5 / <actual> ·
Discovery 3.5 / <actual>`. This is the second of the four weeks M1's mandated
recalibration reads, and it compares them bucket by bucket, so a week logged as
prose drops out of the sample. Send and prospect counts are recorded in
[the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W02" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- Every step's completion is durable before the next step starts — 35
- The aggregate and invariant table is written — 10
- The regeneration test ran against three real modules — 20
- The context-loss report carries all five named parts — 15
- Outreach tooling built and 4 sends logged per touch — 20
