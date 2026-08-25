# Distributed systems exercises

## How to use these

Five exercises, each proving a property of the platform that no amount of reading
establishes. They exist because the learner's own competency record says
*concept-strong, operation-weak*: the concepts here are already understood, and
none of them has been shipped and operated under real failure. Nothing below
explains what a concept is. Every one asks what happened when you ran it.

Each carries the seven-part shape, and each names the difficulty-ladder rungs it
climbs. The rung that matters most in this set is **break** (`DL-3`): four of the
five require the wrong version to be built and run first. That is not
ceremony. Being told that duplicates accumulate is what the learner already has;
watching them accumulate against a counter is the thing being bought.

One framing correction governs the whole set, and it is not optional wording.
What these exercises prove is **effectively-once processing under at-least-once
delivery** — duplicates absorbed, not prevented. Exactly-once delivery cannot be
built over an unreliable network at all: silence tells the sender nothing about
whether its message or the reply went missing, so it resends or it gives up, and
no engineering supplies a third option. Exactly-once execution is likewise
unachievable in general, since an effect and the record of that effect are not
atomic unless one transaction holds both. An exercise report claiming
exactly-once has claimed something false and fails on that ground alone.

Hours, weekly sequencing and acceptance for the weeks that run these live in
[weeks/](../weeks/week-03.md). Stage definitions and demo commands live in
[the platform file](../projects/engineering-agent-platform.md). This file owns
the bodies.

## Exercises

### Replay and kill — proving effectively-once (D-w03-1)

Rungs: `DL-2` implement, `DL-3` break.

#### Objective

Establish, with a number rather than an argument, that the platform's task
handler absorbs duplicate deliveries — and that a process death between a local
commit and an external call cannot produce two of anything.

#### Task

Build the naive handler first and run it: replay one event one hundred times
against it and count every duplicated effect it produces. Only then rebuild it
with idempotent steps, a dedup table under a unique constraint, and
resume-from-last-step, committing the dedup row in the same transaction as the
state transition. Replay again, this time with `kill -9` injected at random
instruction boundaries. Finish by classifying in writing every duplicate the
naive version produced, naming which of the three dedup mechanisms would have
prevented each, and writing the single sentence that states what was actually
proved.

#### Constraints

- The naive version must be built and executed before the correct one. Skipping it forfeits the exercise, because the classification has nothing to classify.
- Kills land at random instruction boundaries, not at step boundaries, and at least 20 of the 100 replays must be interrupted — including between the commit and each external call.
- The dedup row commits inside the same transaction as the state transition. A second connection, a second commit or a post-hoc reconciliation pass is a different exercise and does not satisfy this one.
- No `sleep` may be used to make a race reproducible.

#### Deliverable

`D-w03-1` — a **test suite** (`DT-06`): the replay harness and its passing
assertions, plus the written duplicate classification and the one-sentence claim
statement committed alongside it.

#### Acceptance criteria

- Across 100 replays, exactly one state transition, one PR, one page and one dedup row exist per key.
- At least 20 of the 100 replays were interrupted, and the interruption points are recorded.
- The suite fails when run against the pre-mitigation naive handler.
- 100% of the duplicates the naive run produced are classified, and each classification names exactly one of the 3 dedup mechanisms.

#### Metrics

- Duplicate rate: duplicated effects divided by 100 replays, reported for the naive run and the corrected run separately.
- Failure rate: replays reaching a non-terminal state divided by 100.

#### Reflection questions

1. Which of your steps are genuinely idempotent by construction, and which are idempotent only because no one has yet called them concurrently?
2. Your dedup key is a choice. What input would produce two legitimate operations that collide on it, and what would that cost?

### The crash window — outbox against fault injection (D-m04-2)

Rungs: `DL-3` break, `DL-7` operate.

#### Objective

Close the gap between committing locally and calling the outside world, and show
by exhaustive injection rather than by sampling that no kill point loses an
effect or leaves state and effects disagreeing.

#### Task

Take the platform's external-effects surface — by month 04 it writes to a
repository host, a workspace and an error tracker from a single task — and build
an outbox: a pending-effect row written in the same transaction as the state
transition, plus a separate relay process that delivers pending effects
at-least-once. Then build a fault injector that kills the process at *every*
boundary between the local commit and the last external call, not a sample of
them, and record the resulting inconsistency at each point before the outbox
existed and after.

#### Constraints

- Every boundary is injected, exhaustively. A sampled injection cannot support the claim this exercise makes.
- The relay is a separate process. A relay running inside the committing transaction's process has not proved the property under a process death.
- Handlers must stay correct when the relay delivers the same effect twice, and this must be asserted rather than assumed.
- The proof that the outbox row shares the transaction is an assertion that no row survives a rolled-back transaction — not a code reading.

#### Deliverable

`D-m04-2` — a **test suite** (`DT-06`): the outbox, its relay, the exhaustive
fault-injection harness, and the recorded inconsistency map for the naive
commit-then-call version.

#### Acceptance criteria

- Zero kill points produce a lost effect or a state-versus-effect divergence after the outbox lands.
- A deliberately rolled-back transaction leaves zero outbox rows.
- The double-delivery assertion passes for every handler on the surface.
- The harness reproduces at least one concrete inconsistency against the pre-outbox implementation.

#### Metrics

- Commit-to-effect latency, p50 and p99, over the full injection run.
- Failure rate: kill points producing an inconsistency divided by total kill points, before and after.

#### Reflection questions

1. The outbox moved the problem rather than removing it. Where does the remaining risk now live, and what would make you notice it?
2. Which external effect on your surface would be hardest to make safe under double delivery, and why is it the hard one?

### The chaos run — concurrency, leases and orphans (D-w08-1)

Rungs: `DL-7` operate.

#### Objective

Run the queue under real contention with workers dying mid-task, and demonstrate
that no task is stranded and no effect is duplicated — from telemetry, not from
recollection.

#### Task

Build the queue as a lease rather than a list: claiming with a skip-locked
select, leases that expire, orphan reclaim for work whose holder died,
dead-lettering after N failures, and one isolated worktree per worker. Then run
N concurrent workers with at least 30% of them killed mid-task at random, and
prove every task reaches a terminal state. Exercise the dead-letter path
deliberately rather than waiting to see whether it happens.

#### Constraints

- At least 30% of workers are killed mid-task, at random, during the run.
- No `sleep` may be used to dodge or to provoke a race. If a race needs timing to reproduce, the reproduction is not evidence.
- Terminal state must be asserted for every task, including the dead-lettered ones. "No errors observed" is not a terminal-state claim.
- Worker isolation is per worktree; two workers sharing a checkout invalidates the run.

#### Deliverable

`D-w08-1` — a **demo** (`DT-09`) with a runnable chaos command, plus the run's
telemetry: the queue with lease-based claiming, orphan reclaim, dead-lettering
and worktree isolation, evidenced by the chaos-run output.

#### Acceptance criteria

- Zero tasks stranded and zero duplicated effects across the run.
- 100% of enqueued tasks reach a recorded terminal state, dead-letters included.
- The dead-letter path was exercised at least once and its entries carry a reason.
- Orphan reclaim fired at least once, and the reclaim is visible in telemetry.

#### Metrics

- Success rate: tasks reaching a successful terminal state divided by tasks enqueued.
- Failure rate: tasks dead-lettered divided by tasks enqueued.
- Latency: time from lease expiry to orphan reclaim, p50 and p95.

#### Reflection questions

1. You partitioned before you locked wherever you could. Name the surface where partitioning stopped being available, and say what you did instead.
2. What breaks first at ten times this worker count — the database, the quota, or the disk — and what measurement from this run supports your answer?

### Compensation that fails (D-m04-3)

Rungs: `DL-3` break, `DL-8` explain.

#### Objective

Treat the task-lifecycle teardown as a saga and find out what the system does
when a compensation — the thing that exists to clean up after a failure — fails
permanently itself.

#### Task

Model teardown as a saga with explicit compensations, then inject permanent
failures into the compensations themselves. Establish that each compensation is
independently idempotent by invoking it twice in the suite. Fix an order for
compensations and defend it in writing, releasing the lease last. Identify at
least one effect on the surface that **cannot** be compensated at all, and state
what is done instead of pretending it can. Finish with a one-page classification
defending which platform surfaces are saga-shaped and which are outbox-shaped.

#### Constraints

- Every compensation is invoked twice by the suite. Idempotence asserted in a docstring is not asserted.
- A permanently failing compensation must reach a defined terminal state with an operator-visible alert. A hang and a silent swallow are both failures of this exercise.
- The compensation order is justified in prose, and the lease is released last.
- At least one non-compensable effect must be named. A surface where everything is reversible has been described inaccurately.

#### Deliverable

`D-m04-3` — an **ADR** (`DT-04`): the saga-versus-outbox classification with its
defence, accompanied by the compensation-failure suite and the honest record of
which compensations were not idempotent when first written.

#### Acceptance criteria

- Double-invoked compensations produce zero additional effects.
- A permanently failing compensation reaches a defined terminal state in 100% of injections, and at least 1 operator-visible alert is present in the run output.
- At least one non-compensable effect is named with its stated alternative handling.
- 100% of the platform surfaces listed in the classification are assigned exactly one of saga or outbox, each with a stated reason.

#### Metrics

- Failure rate: compensations that were non-idempotent on first implementation divided by compensations written.
- Success rate: injected compensation failures reaching a defined terminal state divided by injections.

#### Reflection questions

1. Which compensation did you write incorrectly the first time, and what does its shape have in common with the others you might have got wrong?
2. If a compensation fails permanently at three in the morning, what does the person who is woken up actually see, and is it enough to act on?

### Boundary regeneration (D-w02-2)

Rungs: `DL-3` break, `DL-8` explain.

#### Objective

Find out empirically which of your module boundaries are real, by deleting the
implementations and asking an agent to rebuild them from the contract alone.

#### Task

Choose three modules. Delete each implementation, leaving the interface, the
docstring and the tests in place. Have an agent regenerate each one with **no
repository context** and a single attempt. Trace every failure to a specific
piece of out-of-module knowledge the deleted implementation had silently depended
on. Then repair at least one boundary in light of what the failure named, and run
the regeneration again.

#### Constraints

- No repository context, one shot per module. A retry with more context measures a different thing.
- A failure is not closed until it is traced to a *named* implicit dependency. "The model misunderstood" is not a finding.
- The tests are not modified to accommodate a regeneration. The contract is what it was.
- The repaired boundary must be re-regenerated, or the repair is untested.

#### Deliverable

`D-w02-2` — an **ADR** (`DT-04`): the boundary post-mortem carrying the three
regeneration transcripts, the deep-module ratio per module, and the named
out-of-module dependency behind every failure.

#### Acceptance criteria

- Of the 3 modules, at least 1 rebuilds from its contract alone and goes green on attempt 1, with zero repository context supplied.
- 100% of regeneration failures name at least 1 specific implicit dependency.
- At least one boundary is repaired and its regeneration retried successfully.
- The deep-module ratio — public symbols against implementation size — is recorded for all 3 modules.

#### Metrics

- Success rate: modules regenerating and passing on the first attempt divided by 3.
- Test coverage: proportion of each contract's assertions exercised by the surviving tests, since a thin test set makes a passing regeneration meaningless.

#### Reflection questions

1. Which module did you *believe* was well-bounded before you ran this, and what did the failure name that a code review would not have surfaced?
2. Does the deep-module ratio predict regeneration success across your three samples — and with three points, what would you need before you would state that as a finding?
