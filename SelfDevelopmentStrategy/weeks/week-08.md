# Week 08 — Parallel Tasks: Queues, Leases and Worktree Conflicts

## Outcome

By Sunday several workers process tasks concurrently against one queue, with at
least a third of them killed mid-task, and nothing is stranded or lost — and
nothing duplicated among the effects week 6 gave you a mechanism for, with the
rest detected and classified. You also know how often a task's *actual* changed files exceeded what
you predicted — and your safety no longer depends on that prediction being right.

## Why now?

Two things should have converged by now. Your runs are slow enough that
serialising them wastes your evening. And week 6's replay work made duplicate
execution safe, which is the precondition for ever running two of anything at
once. Coordination before idempotency would have been coordination on top of a
race.

**Check the first half is true.** If you have never wanted two tasks running at
once, a queue is not earned yet. Say so and move week 9 forward.

## Build

**A queue that is a lease, not a list.** A worker claims a task for a bounded
time; it must acknowledge before that window closes or another worker may take it.
Generated consumer code omits both halves — it omits the lease, which is invisible
until a worker can crash mid-task, and it omits dead-lettering, so one poison
message loops forever and starves everything behind it.

Four parts:

1. **Claim with a skip-locked select.** Not read-modify-write. Read-modify-write
   is the form an agent reaches for first because it reads most clearly, and it is
   correct single-threaded, broken concurrently, and indistinguishable between the
   two on the page.
2. **Leases that expire, plus orphan reclaim.** A worker dies holding a task in
   `running` and nothing distinguishes slow from dead. Timeout is the only failure
   detector you have; leases, heartbeats and reclaim are the entire answer, and
   each one trades false reclaim against slow reclaim.
3. **Dead-lettering after N failures**, with a reason on every entry.
4. **One isolated worktree per worker.** Two workers sharing a checkout
   invalidates everything.

### Declared scope is a hint, not the truth

This is the part that is easy to get wrong, and getting it wrong makes your
concurrency safety a fiction.

| | What it is | What it is good for |
|---|---|---|
| **Declared file scope** | an *estimate*, written before the work happened | a scheduler hint: predict conflicts, avoid obvious collisions cheaply |
| **Actual changed-file set** | the diff, observed after the run | the only truth about what the task touched |

**A coding agent will legitimately need files nobody predicted.** The rate
conversion lives in a helper you forgot about; the fix needs a new test fixture;
the type change ripples into a caller. Treating that as a violation trains the
agent to do the wrong thing — and treating declared scope as *proof of
independence* means two tasks can be scheduled apart, both wander outside their
estimates, and collide anyway with nothing watching.

So safety has three points, not one:

**Before execution — predict.** Use declared scopes to avoid scheduling two tasks
that obviously collide. Cheap, and it dissolves most contention before any lock
exists. This is *partition before you lock*, and it remains a genuinely good
design principle — it just does not prove anything.

**After execution — observe.** Inspect the actual diff. Did it touch paths another
in-flight or just-completed task also touched? Did the merge base move underneath
it? If either, re-run verification on the updated base before the result is
allowed to count. A verification result computed against a base that no longer
exists is stale, and staleness here looks exactly like success.

**Before merge — reconcile.** Detect conflicts introduced while the task was
running. Rebase or rebuild, re-run verification, and only then merge. Merging
unchecked is the failure this whole section exists to prevent: it succeeds
quietly and leaves a tree nobody authored.

Where two actual changed-sets do overlap, order writers on a version column and
make the loser rebuild its diff on the new base.

If you need a lock, use a Postgres advisory lock with a lease and a fencing token.
Do not stand up Redis to demonstrate locking — you would be shipping the area's
most contested primitive and then annotating it.

## Learn

- [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)
  on bulkheads and back pressure.
- [DDIA](https://dataintensive.net) chapter 8's fencing-token section, again,
  now that you have a lease that can expire while its holder is still working.
~2h. Both are short and directly load-bearing this week.

## Tasks

### Core — required (~15h: 2h learning, 10h building/testing, 3h business)

1. **Build the lease-based queue**: skip-locked claiming, expiry, orphan reclaim,
   dead-lettering with reasons.
2. **Worktree per worker**, with the isolation asserted rather than assumed.
3. **Use declared scope as a scheduling hint.** Avoid claiming two tasks whose
   declared scopes obviously collide. A task with no declared scope is still
   claimable — it just gets no prediction, so treat it as colliding with
   everything until its diff exists.
4. **Inspect the actual changed-file set after every run**, and compare it against
   other in-flight and recently-completed tasks. Record how often the actual set
   exceeded the declared one, and how often that overrun was legitimate.
5. **Re-verify on a moved base.** If the merge base changed while a task ran,
   re-run verification against the new base before the result counts. Assert this
   in a test — a stale pass is the dangerous case because it looks identical to a
   real one.
6. **Add the version column and rebuild-on-conflict path** for actual overlaps.
7. **Run the chaos run.** N workers, ≥30% killed mid-task at random, every task
   asserted to reach a terminal state — dead-letters included. Exercise the
   dead-letter path deliberately rather than waiting to see whether it happens.
   **No `sleep` to dodge or provoke a race.**
8. **Business: 6 sends, and the ROI calculation.** Take the week-7 workflow
   document, measure or source the current time cost per occurrence, and express
   the result as a payback period in months with every input and its source shown.
   Method in [consulting-and-saas.md](../business/consulting-and-saas.md).

### Stretch — only after Core is DONE

- **Architecture review #2 — the supplied bad system.** `SUP-01` in
  [exercises/architecture.md](../exercises/architecture.md), reviewed against all
  fourteen defect classes before reading the planted-defect list, with at least
  two findings evidenced by a *reproduction* rather than by reading. This is one
  of the highest-value exercises in the twelve weeks and it is a solid 4 hours —
  it will not fit beside the queue. **Schedule it deliberately rather than
  dropping it:** a quiet week, or the gap before month 4. What it must not do is
  happen *after* review #3, since the whole point is the comparison.
- **Compose the middleware chain** — retry, timeout, rate limiting as decorators,
  with the ordering justified in writing. Order is the entire semantics: a limiter
  below the retry cannot bound a budget.
- **Double the workers** and find out what breaks first. You will have a
  prediction from the reflection question below; check it.

## Use it for real

Run the chaos run against real tasks that really open pull requests. Include two
deliberate cases:

- **A predicted collision** — two tasks whose *declared* scopes intersect, so the
  scheduler has something to keep apart.
- **An unpredicted collision** — two tasks whose declared scopes are disjoint but
  which you know will both end up touching a shared helper. This is the case that
  matters, and it is the one a declared-scope-only design misses entirely.

## Measure

- Tasks stranded: zero.
- **Duplicated effects: zero — for internal effects, and for the external effects
  week 6's table marked guaranteed.** External effects still marked *unresolved*
  may duplicate; those must be detected and classified, and their count reported
  separately. Folding them into one "zero duplicates" figure would claim a
  guarantee no mechanism supports.
- Tasks reaching a recorded terminal state: 100%, dead-letters included. "No
  errors observed" is not a terminal-state claim.
- Dead-letter path exercised at least once; orphan reclaim fired at least once,
  visible in telemetry.
- Lease-expiry to orphan-reclaim latency, p50 and worst case.
- **Scope prediction accuracy**: how often the actual changed-file set stayed
  inside the declared one. Expect this to be well under 100%, and expect most of
  the overruns to be legitimate. That is the finding — it is why declared scope is
  a hint.
- **Collisions the prediction missed**: overlaps that appeared only in the actual
  diffs. Every one of these is a case the pre-execution check could not have
  caught, and it is what justifies the post-execution inspection.
- Separation versus version-conflict ratio: how often scheduling avoided the
  problem versus how often the version check had to settle it.

## Failure exercise

**Two agents modifying overlapping files.** Show that concurrent workers cannot
quietly overwrite each other — including when the overlap was *not* predicted.

- **Detection.** Two layers. *Predicted:* two claimed tasks declare intersecting
  scopes — cheap, and catches the obvious cases before any work happens.
  *Observed:* two worktrees emit diffs over a shared path, or a task's merge base
  moved while it ran. The second layer is the one that matters, because it is the
  only one that sees a collision nobody forecast.
- **Safe failure.** Prefer separation where the prediction allows it. Where the
  overlap appears only in the actual diffs, refuse the *merge*, not the work —
  the task did legitimate work against a base that has since moved.
- **Recovery.** Order writers on a version column and make the loser rebuild on
  the new base, **then re-run verification**. A rebuilt diff whose verification was
  never re-run is a stale pass, and a stale pass is indistinguishable from a real
  one at the merge button.
- **Logging.** Both task ids, both declared scopes, both actual changed-sets, the
  intersection, whether it was predicted or observed, and what settled it. The
  predicted-versus-observed field is the interesting one: it tells you what your
  hint is actually worth.
- **Proving test.** Two cases. (a) Two tasks with a *predicted* intersection are
  never claimed together. (b) Two tasks that pass the pre-check and then both
  wander into a shared file are caught at merge, with the loser rebuilt and
  re-verified. **Case (b) must go red against a build that trusts declared scope**
  — that is the whole point of the exercise.

## Deliverables

- [ ] Queue with lease-based claiming, expiry, orphan reclaim, dead-lettering,
      worktree-per-worker isolation.
- [ ] Declared scope used as a scheduling hint; actual changed-set inspected after
      every run; version-column conflict path for real overlaps.
- [ ] Re-verification on a moved merge base, asserted in a test.
- [ ] Chaos run: ≥30% of workers killed, telemetry showing zero stranded and zero
      duplicated among guaranteed effects, duplicates of unresolved external
      effects detected and classified, dead-letter and reclaim both exercised.
- [ ] Scope-prediction log: declared versus actual per task, with overruns marked
      legitimate or not.
- [ ] Overlapping-files report, five parts, with the *observed*-collision case red
      against a build that trusts declared scope.
- [ ] 6 sends logged; ROI calculation with its measurement method shown.

## Done when

- [ ] Zero tasks stranded across the chaos run, and zero duplicated effects among
      internal effects and the external effects week 6 marked guaranteed.
- [ ] Duplicates of *unresolved* external effects are detected and classified
      rather than absent, and counted separately from the figure above.
- [ ] 100% of enqueued tasks reached a recorded terminal state.
- [ ] The dead-letter path and orphan reclaim each fired at least once, visible in
      telemetry.
- [ ] Zero simultaneous claims occurred on task pairs with *predicted* overlap.
- [ ] A collision visible only in the **actual** diffs is caught before merge, the
      loser rebuilt, and verification re-run against the new base.
- [ ] Nothing in the code or the write-up treats declared scope as proof that two
      tasks are independent.
- [ ] The scope-prediction log records declared versus actual for every task.
- [ ] The ROI calculation states a payback period in months, every input carries a
      source, the loaded-cost multiplier is stated, and it contains zero
      industry-average percentages.

## Reflection

1. How often did the actual changed-file set exceed the declared one — and of
   those, how many were the agent being right rather than careless?
2. Where did scheduling separation stop being available, and what ended it?
3. What breaks first if you double the workers — the database, the rate limit, or
   the disk? Which measurement from this run supports that answer?

## Evidence

- Chaos-run telemetry: workers, kills, terminal states, reclaims, dead-letters.
- Scope-prediction log and the separation-versus-conflict ratio.
- The moved-base re-verification test.
- Overlapping-files report, with the observed-collision case red on the parent.
- Send log; ROI calculation.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
