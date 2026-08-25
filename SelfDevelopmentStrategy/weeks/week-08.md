# Week 08 — Parallel Tasks: Queues, Leases and Worktree Conflicts

## Outcome

By Sunday several workers process tasks concurrently against one queue, with at
least a third of them killed mid-task, and nothing is stranded, lost or duplicated
in effect. You also reviewed a deliberately bad system somebody else wrote, and
found defects in code that reads perfectly.

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

**Partition before you lock.** Tasks declare a file scope; two tasks whose scopes
intersect are never claimed at the same time. Contention that cannot occur needs
no coordination, and coordination you never need is coordination that never has a
bug. Where separation is genuinely unavailable, order writers on a version column
and make the loser rebuild its diff on the new base.

If you need a lock, use a Postgres advisory lock with a lease and a fencing token.
Do not stand up Redis to demonstrate locking — you would be shipping the area's
most contested primitive and then annotating it.

**Also this week: the middleware chain.** Retry, timeout and rate limiting as
composed decorators, with the ordering justified in writing. Order is the entire
semantics: a limiter below the retry cannot bound a budget.

## Learn

- [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)
  on bulkheads and back pressure.
- [DDIA](https://dataintensive.net) chapter 8's fencing-token section, again,
  now that you have a lease that can expire while its holder is still working.
- Skim [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php)
  chapter 8 (pull complexity downwards) before the review.

~2h.

## Tasks

1. **Build the lease-based queue**: skip-locked claiming, expiry, orphan reclaim,
   dead-lettering with reasons.
2. **Worktree per worker**, with the isolation asserted rather than assumed.
3. **Add file-scope declaration and scope-based partitioning.** A task without a
   declared scope is not claimable.
4. **Add the version column and rebuild-on-conflict path** for the cases
   partitioning cannot separate.
5. **Compose the middleware chain** and write the ordering justification.
6. **Run the chaos run.** N workers, ≥30% killed mid-task at random, every task
   asserted to reach a terminal state — dead-letters included. Exercise the
   dead-letter path deliberately rather than waiting to see whether it happens.
   **No `sleep` to dodge or provoke a race.**
7. **Architecture review #2 — the supplied bad system.** `SUP-01` in
   [exercises/architecture.md](../exercises/architecture.md). Review it against
   all fourteen defect classes before reading the planted-defect list. At least
   two findings must be evidenced by a *reproduction*, not by reading.
8. **Business: 6 sends, and the ROI calculation.** Take the week-7 workflow
   document, measure or source the current time cost per occurrence, and express
   the result as a payback period in months with every input and its source shown.
   Method in [consulting-and-saas.md](../business/consulting-and-saas.md).

## Use it for real

Run the chaos run against real tasks that really open pull requests. Include at
least one pair of tasks whose file scopes genuinely intersect, so partitioning has
something to refuse.

## Measure

- Tasks stranded: zero. Duplicated effects: zero.
- Tasks reaching a recorded terminal state: 100%, dead-letters included. "No
  errors observed" is not a terminal-state claim.
- Dead-letter path exercised at least once; orphan reclaim fired at least once,
  visible in telemetry.
- Lease-expiry to orphan-reclaim latency, p50 and worst case.
- Separation versus version-conflict ratio: how often partitioning avoided the
  problem versus how often the version check had to settle it. That ratio is the
  honest measure of how well separation works.
- Review: planted defects found over 6, and claimed defects that were not real
  over defects claimed.

## Failure exercise

**Two agents modifying overlapping files.** Show that concurrent workers cannot
quietly overwrite each other — and that separation dissolves most of the problem
before any lock.

- **Detection.** Two claimed tasks announce intersecting file scopes, or two
  worktrees emit diffs over a shared path. Both are visible *before* the collision,
  which is what makes prevention possible.
- **Safe failure.** Separate rather than lock: intersecting scopes are never
  claimed simultaneously.
- **Recovery.** Where separation is unavailable, order writers on a version column
  and make the loser rebuild on the new base. Merging unchecked is what this
  exposes — it succeeds quietly and leaves a tree nobody authored.
- **Logging.** Both task ids, both scopes, the intersection, and whether
  separation or a version conflict settled it.
- **Proving test.** Two tasks with a planned intersection are never claimed
  together; forced together, the second is refused by the version check rather
  than overwriting. **Without announced scopes both assertions break.**

## Deliverables

- [ ] Queue with lease-based claiming, expiry, orphan reclaim, dead-lettering,
      worktree-per-worker isolation.
- [ ] File-scope declaration, scope partitioning, version-column conflict path.
- [ ] Middleware chain with its ordering justified in writing.
- [ ] Chaos run: ≥30% of workers killed, telemetry showing zero stranded and zero
      duplicated, dead-letter and reclaim both exercised.
- [ ] Overlapping-files report, five parts, proving test red without announced
      scopes.
- [ ] Architecture review #2 as an ADR: all 14 classes assessed, ≥2 findings
      backed by a reproduction, every finding citing a line range.
- [ ] 6 sends logged; ROI calculation with its measurement method shown.

## Done when

- [ ] Zero tasks stranded and zero duplicated effects across the chaos run.
- [ ] 100% of enqueued tasks reached a recorded terminal state.
- [ ] The dead-letter path and orphan reclaim each fired at least once, visible in
      telemetry.
- [ ] Zero simultaneous claims occurred on intersecting task pairs; forced
      together, the losing write was refused in every trial.
- [ ] All 14 defect classes are assessed on `SUP-01`, at least 4 of its 6 planted
      defects were found before the list was consulted, and ≥2 findings are backed
      by a reproduction.
- [ ] The ROI calculation states a payback period in months, every input carries a
      source, the loaded-cost multiplier is stated, and it contains zero
      industry-average percentages.

## Reflection

1. Where did partitioning stop being available, and what ended it?
2. What breaks first if you double the workers — the database, the quota, or the
   disk? Which measurement from this run supports that answer?
3. `SUP-01` passes a linter and has decent coverage. Which planted defect did you
   miss, and what does that say about the signals you usually trust?

## Evidence

- Chaos-run telemetry: workers, kills, terminal states, reclaims, dead-letters.
- Separation-versus-conflict ratio.
- Middleware ordering justification.
- Overlapping-files report and its red-on-parent test.
- Review ADR for `SUP-01`, with reproductions attached.
- Send log; ROI calculation.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
