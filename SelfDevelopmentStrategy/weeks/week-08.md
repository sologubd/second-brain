# Week 08 — Concurrency, leases and the chaos run

## Outcome

By Sunday several agents work in parallel against one queue with at least a
third of the workers killed mid-task, and nothing is stranded, lost or
duplicated in effect.

## Time budget

- Theory: 3.0 h
- Building: 6.5 h
- Testing/evaluation: 2.5 h
- Customer discovery: 3.0 h

Building takes 6.5 h, the largest allocation any week gives it: a queue, a
lease, an orphan reclaimer, a dead-letter path and a worktree manager, all of
which must survive being killed. USI-10 records distributed systems as
concept-strong and operation-weak working knowledge, and canon's instruction
follows — emphasise operating and failure behaviour over concept exposition.
Nothing here explains what a lock is; everything is about holding one, losing
one, and what happens in the gap. Ceilings are EUR 0.00 of metered spend and
50 agent runs, and canon gives the reason for a count that low: the chaos run
drives stubbed work units on most trials, so quota never gates the concurrency
proof.

Compressed week, 8.0 h: T-w08-3, T-w08-6, T-w08-1, and T-w08-12 with T-w08-13
and T-w08-14 whole at 2.5 h — then let the calendar slip rather than doubling up.
T-w08-14 stays intact because the ROI calculation is the week's only business
deliverable, and half of one is not half as useful. Architecture review #2 and
the middleware chain both defer to [week 09](week-09.md), where Track B has
4.5 h, along with T-w08-4, T-w08-8, T-w08-9 and T-w08-10. The chaos run is never
cut: S4 without it is a queue nobody has evidence about. Nothing ticks —
D-w08-1 carries without its middleware ordering, D-w08-2 and D-w08-3 whole, and
D-w08-4 without its 6 sends, which is a funnel delta to record. DONE-COMPRESSED,
not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| queues | B | P0 | T-w08-1, then T-w08-3's claiming path → D-w08-1 |
| concurrency | B | P0 | T-w08-6's chaos run → D-w08-1 |
| distributed locks | B | P0 | T-w08-2's fencing tokens, leased in T-w08-3 |
| transactions | B | P0 | T-w08-2 on read-committed and its lost update |
| failure recovery | B | P0 | orphan reclaim, T-w08-3 and T-w08-9 → D-w08-1 |
| parallel work | A | P0 | T-w08-9's worktree isolation → D-w08-1 |
| multi-agent orchestration | A | P1 | T-w08-8 → D-w08-3 |
| Command | B | keep | T-w08-4's reified task record → D-w08-1 |
| Decorator | B | promoted | T-w08-4's middleware chain → D-w08-1 |
| Optimistic Offline Lock | B | earn it | T-w08-2's version column, used by T-w08-10 |
| ROI estimation | E | P0 | T-w08-14 → D-w08-4 |

Eight rows resolve to P-tagged concept rows. The other three are
pattern-triage verdicts, not gaps: Command is kept and rated better than it
looks, reification being what makes an agent's work auditable; Decorator was
promoted into Observer's slot, Observer having been cut to recognition-only
for installing a model hostile to at-least-once delivery; and Optimistic
Offline Lock is an addition to Fowler's list, verdicted earn it.

The five system-design rows and all three patterns reason from
[Track B](../tracks/system-design.md); parallel work and multi-agent
orchestration from [Track A](../tracks/agentic-engineering.md); ROI estimation
from [Track E](../tracks/consulting.md), though its sends and follow-ups log
against [outreach](../business/outreach.md). T-w08-2 reinforces
[Track D](../tracks/ai-security.md), and the two revenue tasks reinforce
[Track F](../tracks/micro-saas.md). S4 belongs to
[the platform](../projects/engineering-agent-platform.md); AR-02 and its
supplied system to
[the review set](../exercises/architecture-reviews.md); EX-FAIL-10 to
[the agent-failure set](../exercises/agent-failures.md). This file owns the
tasks, the hours and the acceptance.

## Tasks

### Task 1

`T-w08-1` — 1.0 h, Track B, theory, reinforcing A. Reading: `RES-13`. Queue
semantics as a LEASE, not a list: visibility timeout, ack, dead-letter. The
causal link is the lesson — adopting a queue is a decision to make every
downstream handler idempotent, because an expired lease re-delivers work whose
effects may already exist.

### Task 2

`T-w08-2` — 1.0 h, Track B, theory, reinforcing D. Reading: `RES-13`.
Partition before you lock. Then fencing tokens, the Optimistic Offline Lock
version column, and Postgres read-committed with the lost update it permits
under read-modify-write. That last deserves the time: read-modify-write is
correct on one worker, broken on four, and identical to read either way, so
the review question must become mechanical — conditional update, version
column or row lock?

### Task 3

`T-w08-3` — 3.0 h, Track B, building, reinforcing A. Build S4: a Postgres
queue claiming with SELECT ... FOR UPDATE SKIP LOCKED, leases with expiry,
orphan reclaim, dead-lettering after N failures, and one git worktree per
worker. No broker and no second datastore — TR-11 verdicts Redis SKIP FOR NOW
because teaching locking through it means teaching an unsafe lock first and
its caveats afterwards, while a lease, an advisory lock and a fencing token
cover the same ground safely and for less.

### Task 4

`T-w08-4` — 1.0 h, Track B, building, reinforcing A. Reify the task record as
a Command — serialised, durable, replayable — then the Decorator middleware
chain over it: retry, timeout, rate limit, cost accounting, tracing, ordering
justified in writing. Order is the semantics, not the presentation. A rate
limiter underneath the retry cannot bound spend; tracing underneath it hides
the attempts you most need to see.

### Task 5

`T-w08-5` — 1.0 h, Track B, building. Read SUP-01, the supplied deliberately
bad system: roughly 400 lines of idiomatic, fully type-annotated Python at 90%
coverage that passes every linter and is broken in at least six of the
fourteen ways. Reading for style finds none of them by design; each answers
instead to one of the four questions — second call, crash window, concurrency,
unstated external assumption.

### Task 6

`T-w08-6` — 1.5 h, Track B, testing. The chaos run: N concurrent workers, at
least 30% killed mid-task at random, no sleep anywhere used to dodge a race,
and proof that every task reaches a terminal state. A sleep that turns the
suite green buys a coincidence and costs the experiment.

### Task 7

`T-w08-7` — 0.5 h, Track B, testing. Write architecture review #2 against the
14 defect classes, naming which are present in the supplied system, with
evidence. AR-01 in W04 was self-inspection; this is the opposite mode, and the
harder skill, because a reviewer of their own system grades choices they
already called reasonable.

### Task 8

`T-w08-8` — 1.0 h, Track A, theory, reinforcing B. Reading: `RES-14`. Two
agents on overlapping files: why partitioning is the harness-level answer, and
where it stops being available. Scopes go stale, a task meets a file it never
declared, and there you are serialising again. Name that boundary before the
exercise needs it.

### Task 9

`T-w08-9` — 1.5 h, Track A, building. Build the worktree lifecycle manager:
create, claim, teardown, and reclaim the orphans a killed worker leaves
behind. Write teardown most carefully; it runs when nobody is watching.

### Task 10

`T-w08-10` — 0.5 h, Track A, testing. Run the overlapping-files exercise
against S4 and write the five-part report, including where the mitigation did
worse than expected.

### Task 11

`T-w08-11` — 0.5 h, Track E, business, reinforcing F. Six cold emails, drafted
with BOA-S0 and approved one by one before they go out. By Sunday 41 sends
have matured, which is where ACT-1 sits: zero replies against those 41. It
trips 14.3% of the time at the band midpoint, 3.8% at the ceiling, 54.1% at
the floor. Unlike the four watch rows behind it this one is not expected, and
it changes something — re-pitch the funnel in an out-of-cycle canon delta,
extend the Stage-1 simulated track across the remaining business deliverables,
and draw the hours that frees from the cut list. Log the outcome either way in
[the scoreboard](../SCOREBOARD.md).

### Task 12

`T-w08-12` — 0.5 h, Track E, business. Send 14 follow-ups. Fourteen against
six sends is the two-per-prospect rule catching up with the heavier weeks
behind it, so most land on prospects first contacted in W06 and W07. Each must
carry something the previous touch did not.

### Task 13

`T-w08-13` — 0.25 h, Track E, business. The no-show and reschedule reserve,
budgeted separately from call time and labelled as such, so a call that
evaporates cannot quietly consume hours booked for one that happens. This week
holds no call slot of its own, and zero calls remains the modal outcome at
53.9%. Unused, the reserve becomes slack and is recorded as slack rather than
absorbed into S4.

### Task 14

`T-w08-14` — 1.75 h, Track E, business, reinforcing F. The ROI calculation,
from a MEASURED before-and-after baseline: time saved per week times
fully-loaded hourly cost times 52, minus platform and maintenance cost, as a
payback period in months. Measured is the load-bearing word: the arithmetic is
trivial, the baseline is not. Absent a real process to time, the fallback is a
Stage-1 simulated baseline against W07's workflow documentation, tagged
`evidence_source: simulated` — canon's expected path under the corrected
funnel. Substitution stays per-deliverable, never a flip of the business
column.

## Deliverables

- [ ] D-w08-1 — S4 task queue with lease-based claiming, orphan reclaim, dead-lettering and worktree-per-worker isolation; done includes the chaos-run evidence and the Decorator middleware chain with its ordering justified in writing — at `agentplat/queue/`, `docs/w08/chaos-run.md`, `docs/w08/middleware-order.md`
- [ ] D-w08-2 — Architecture review #2 on the SUPPLIED deliberately bad system, against the 14 defect classes, with evidence per named defect — at `docs/adr/adr-002-arch-review-2.md`
- [ ] D-w08-3 — Failure report, two agents modifying overlapping files, with all five parts — at `docs/w08/overlapping-files-report.md`
- [ ] D-w08-4 — ROI calculation with its measurement method shown, plus 6 sends and 14 follow-ups logged — at `docs/w08/roi-calculation.md`, `send-log.local.md`

## Acceptance criteria

- [ ] AC-w08-1a — once the chaos run drains, zero tasks sit non-terminal and zero effects occur twice; duplicated ATTEMPTS are permitted and expected, and their count is recorded rather than minimised (T-w08-3, T-w08-6)
- [ ] AC-w08-1b — claiming uses SELECT ... FOR UPDATE SKIP LOCKED, with no advisory-lock-only claiming and no LIMIT 1 polling race in the path; and the queue note states the visibility-timeout, ack and dead-letter mapping, the idempotency obligation a lease imposes downstream, and the lost update read-committed permits under read-modify-write (T-w08-3, T-w08-1, T-w08-2)
- [ ] AC-w08-1c — an expired lease is reclaimable AND the reclaiming worker is safe even if the original holder is still alive; the write-up states whether that safety comes from a fencing token or from an idempotent protected operation, and why (T-w08-3, T-w08-6)
- [ ] AC-w08-1d — no two workers ever hold overlapping worktrees, asserted by the manager under the chaos run rather than by inspection; the dead-letter path is exercised at least once (T-w08-3, T-w08-9)
- [ ] AC-w08-1e — the ordering note states where the rate limiter sits relative to the retry and why retries must not bypass the budget, and places tracing so individual attempts stay visible (T-w08-4)
- [ ] AC-w08-2a — review #2 names at least six of the 14 defect classes as present or absent in the supplied system, carries a file-and-line citation behind every finding, and says which of the four questions surfaced each (T-w08-5, T-w08-7)
- [ ] AC-w08-3a — the overlapping-files report carries all five named parts, states the point at which partitioning stopped being available, and its proving test fails when run against the pre-mitigation code (T-w08-10, T-w08-8)
- [ ] AC-w08-4a — the ROI calculation rests on an ACTUAL measured baseline rather than an estimate, and documents its method well enough to survive a skeptical buyer asking how the before figure was obtained; the week's funnel row reaches SCOREBOARD with 6 sends and 14 follow-ups, the reserve marked used or returned as slack, and `evidence_source` set on every business artifact (T-w08-14, T-w08-11, T-w08-12, T-w08-13)

## Stretch goal

Outside the 15 hours. Scale the workers up until something gives, and identify
what gives first — the database, the quota, or the disk. Then reach the case
the chaos run does not: a lease expiring while an LLM call is still in flight,
where the holder is neither alive nor dead in any way the queue can observe.
Killing a worker is the easy failure, which is what makes that the honest next
question. Attempt it only once the four deliverables hold.

## Failure exercise

One exercise, sitting on the seam between the queue built here and the agents
that draw from it. The five parts below expand the body held in
[the agent-failure set](../exercises/agent-failures.md), and D-w08-3 is the
report.

### EX-FAIL-10 — two agents modifying overlapping files

- **Detection.** Two claimed tasks declare overlapping file scopes — or, later and more expensively, two worktrees produce diffs that touch one path. Both checks earn their place: the first is cheap and predictive, the second backstops a task whose real scope outgrew its declared one.
- **Safe failure behaviour.** PARTITION rather than lock. Tasks whose declared scopes intersect are never claimed concurrently, which is stronger than coordinating them well: contention that cannot arise needs no coordination, and no correct lock either.
- **Recovery.** Where partitioning is unavailable, serialise on a version column — the optimistic offline lock — and require the loser to re-derive its diff from the new base rather than merge blindly. Re-deriving is the part to state: merging two agent diffs yields a plausible file nobody designed.
- **Logging.** Record both task ids, both file scopes, the overlap set, and whether resolution came by partition or by version conflict. The partition-to-conflict ratio then says whether scope declarations are improving or the fleet is merely getting luckier.
- **Test proving the mitigation.** Two tasks with a deliberate overlap are never claimed concurrently; forced concurrent, the second is rejected by the version check instead of overwriting. It must fail against a build with no scope declaration, where both claims succeed and the last write wins.

## Reflection

1. Where did you PARTITION instead of locking, and could you have partitioned
   further? What made the remaining contention irreducible — the domain, or the
   way you happened to model the task?
2. What breaks first as workers scale — the database, the quota, or the disk?
   State your evidence, not your expectation.
3. If a lease expires while an LLM call is still in flight, what actually
   happens? Does your safety come from a fencing token or from the protected
   operation being idempotent — and why did you choose that one?

## Evidence

- `make demo-s4-chaos WORKERS=4 KILL_PCT=30` — this stage's runnable demo command — with output showing nothing stranded and no effect applied twice.
- The written fencing-choice note, naming which safety argument S4 relies on.
- Path to the middleware chain and to its ordering justification.
- Path to the architecture review #2 write-up, with a citation per named defect.
- Path to the overlapping-files failure report.
- Path to the ROI calculation, its measurement method and `evidence_source` tag.

Log actual hours below as one line, planned first: `Theory 3.0 / <actual> ·
Building 6.5 / <actual> · Testing 2.5 / <actual> · Discovery 3.0 / <actual>`.
The M1 hour recalibration rewrote this week's plan from four weeks of logged
actuals, so this region says whether that correction landed or overshot —
readable only where every week logs four buckets in one shape. Funnel counts
belong in [the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W08" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- The queue claims with leases, reclaims orphans and dead-letters — 25
- The chaos run comes back clean at a 30% kill rate — 25
- The middleware ordering is justified in writing — 10
- Architecture review #2 is written against the supplied system — 15
- The overlapping-files report carries all five named parts — 10
- The ROI figure rests on a measured baseline — 15
