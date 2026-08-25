# Week 05 — Persistence, Restart and Resume

## Outcome

By Sunday every step's completion is recorded durably before the next step
starts, and a `kill -9` anywhere in the pipeline resumes from what was actually
written rather than from what a dead process believed. You also have a written
list of the places where your durable state and the outside world can still
disagree — the crash windows you are deliberately leaving open.

## Why now?

Four weeks of run logs should have produced this problem for you: a long run died
partway — the agent stalled, your laptop slept, you hit Ctrl-C on the wrong
terminal — and you had no way to continue it. You re-ran it from the top, spent
the tokens again, and possibly opened a second pull request.

**Check that this actually happened before you build it.** If your runs are short
enough that restarting from scratch is free, persistence is not yet earned. Say so
in the reflection and swap this week for week 7. The rule is pain → pattern.

## Build

A task lifecycle recorded in Postgres — stand it up now; it becomes the queue, the
lock and the vector index later.

Three pieces:

1. **An explicit state enum and a transition table.** `pending → running → …`
   written as data, not as `if` branches. A transition table is a
   machine-checkable specification, which means the invalid-transition test suite
   can be generated from it rather than written by hand — and that covers an error
   class no amount of reading finds. What stays a human decision is which states
   exist and what *done* means.
2. **Completion recorded before the next step starts** — with the transaction
   boundary stated precisely, because this is where the week is easy to get
   wrong. See below.
3. **Resume from the durable pointer, and nothing else.** On restart, read the
   pointer and continue. Where the pointer and the observable world disagree,
   **stop** — do not guess. A guess either repeats an external effect or skips
   one, and afterwards neither is visible.
4. **A disagreement detector.** On resume, reconcile the durable pointer against
   what you can actually observe in the outside world, and record every mismatch.
   That log is this week's most valuable artifact: it is the evidence that
   justifies the outbox work later.

Ask an agent for "a state machine" and you get the class-per-state form, which
dies with the process. The whole point here is state as data in a row you can
`SELECT`.

### What can and cannot share a transaction

The sentence *record completion in the same transaction as the effect* is true
only for effects inside the same transactional system. Split them explicitly:

**A — internal transactional effects.** A state transition plus rows your own
Postgres owns: an attempt record, an audit row, a result blob. These genuinely
share one transaction, and that is what makes repeating the step harmless — the
effect and the record of it commit or roll back together.

**B — external effects.** Creating a pull request, updating an issue, posting a
comment, writing to a tracker, sending an email. **These cannot participate in
your Postgres transaction at all.** There is no combination of ordering that
makes them atomic with it:

```
BEGIN
  mark step complete
COMMIT              ← process dies here: state says done, PR was never created
host.create_pr()

  ...or the reverse...

host.create_pr()
BEGIN               ← process dies here: PR exists, state says not started
  mark step complete
COMMIT
```

Both orderings have a window, and swapping them only chooses which
inconsistency you get.

> **External-effect atomicity is NOT solved this week.**

Do not build an outbox now. The crash window between a local commit and an
outward call is a **documented failure surface** you are deliberately leaving
open, and the disagreement log from piece 4 is what earns the outbox and relay in
[months 4–6](../later/months-04-06.md). Building the mechanism before you have
the log is exactly the pattern-before-pain failure this plan is arranged against.

So what this week actually claims: **durable internal task state, resume from
persisted state, and detection of disagreement between durable state and the
observable external world.** That is a real and useful property. It is not
end-to-end atomicity, and the write-up must not say it is.

**Not yet:** retries (week 6), idempotency keys (week 6), the outbox and relay
(months 4–6), queues (week 8). This week the pipeline resumes and *notices*
disagreement; it does not yet absorb duplicates or close the external-effect
window.

## Learn

- [DDIA](https://dataintensive.net) chapter 7 on transactions. Read-committed
  isolation and the lost update it permits; unique and partial indexes as the only
  reliable dedup primitive; and that external APIs offer no isolation at all.
- [Temporal's activity docs](https://docs.temporal.io/activities) — how a mature
  system words its guarantee: an activity may physically run more than once yet be
  observed as completed once, because the guarantee lives in the durable log.

~2.5h. Chapter 7 is the load-bearing read.

## Tasks

### Core — required (~15h: 3h learning, 9h building/testing, 3h business)

1. **Stand up Postgres and the task table.** State column, transition table,
   generated invalid-transition test suite.
2. **Move progress out of process memory.** Every step boundary commits before
   the next step begins. Nothing load-bearing lives in a variable that dies with
   the process.
3. **Classify every effect your pipeline produces** as internal-transactional or
   external, in a table. Two columns is enough. This is fifteen minutes of work
   and it is what stops the rest of the week overclaiming.
4. **Build the boundary-kill harness.** Kill the process at *every* step boundary
   in turn — not a sample — and assert the resumed run lands where an undisturbed
   run lands **for internal state**. This is the failure exercise.
5. **Log the external-effect disagreements.** For each kill point that leaves the
   durable state and the outside world disagreeing, record which effect, which
   direction (state ahead of the world, or world ahead of state), and what a
   person would have to do to fix it by hand. Do not fix it in code.
6. **Business: 9 sends, assisted.** Use the Business Operations Agent's
   extraction step ([BOA capability 1](../projects/business-operations-agent.md))
   to research prospects, and approve every draft before it leaves. Add the two
   follow-ups for earlier prospects; each must carry something the previous touch
   did not.

### Stretch — only after Core is DONE

- **Architecture review #1.** Write the generated-code review checklist around the
  four questions, version it, and apply it to the platform including this week's
  own diff. Instructions and the fourteen defect classes are in
  [exercises/architecture.md](../exercises/architecture.md). Genuinely valuable —
  and it is a 3–4 hour job that will not fit beside the state machine in the same
  fifteen hours. If it slips, run it in week 6 or 7; what matters is that it
  happens *before* review #2 in week 8, so the two are comparable.
- **Write the aggregate-and-invariant table**: what must always be true, which
  aggregate owns it, where it is enforced. Twenty minutes, and it makes the
  transaction boundaries obviously correct rather than memorised.
- **Compare against a reference.** Read Temporal's activity docs and write one
  paragraph naming what it solves that your hand-built version does not, and
  whether that gap matters at your scale.

## Use it for real

Run the week-3 and week-4 pipelines under the new persistence layer, on real
tasks, with real interruptions. Then kill it deliberately, everywhere.

## Measure

- Kill points exercised, and how many left **internal state** at the undisturbed
  terminal position. Target: 100% of boundaries.
- **External-effect disagreements**, counted and listed by kill point. Target is
  emphatically *not* zero — you expect a nonzero number here, and that number is
  the deliverable. A zero would mean either your pipeline has no external effects
  yet or your detector is not looking.
- Duplicate external effects observed across the sweep. Whatever this number is,
  it is week 6's justification.
- Kill-to-resume distance: how long work sat orphaned. p50 and worst case;
  without it "did it resume?" has only an anecdote as an answer.

## Failure exercise

**Agent context loss after restart.** Prove a restarted run continues from what
was durably written, never from what a dead process believed it had done.

- **Detection.** On resume, hold the stored pointer against the observable world.
  Two mismatches are possible and both are defects: a step marked unfinished
  whose effect exists, and one marked finished whose effect is missing.
- **Safe failure.** Continue from the durable pointer and nothing else. Where
  pointer and world disagree, stop.
- **Recovery.** Re-run from the stored pointer. For **internal** effects this is
  harmless *by design* rather than by discipline, because the transaction
  recording completion is the one that produced the effect. For **external**
  effects it is not harmless and you have no mechanism yet — a re-run may repeat
  them, and that is the open crash window this week documents rather than closes.
- **Logging.** The pointer at kill time and at resume, and the wall-clock distance
  between them. Plus, for every external effect, whether the resumed run repeated
  it — recorded, not prevented.
- **Proving test.** Kill at each boundary in turn and assert two different things,
  because they are different claims:
  - *Internal effects:* the resumed run reaches the undisturbed terminal state and
    nothing happened twice. **Point it at last week's in-memory version and it
    must break.**
  - *External effects:* every mismatch between durable state and the observable
    world is **detected and logged**. The assertion is that the detector fired and
    classified the mismatch — not that no duplicate occurred. A duplicate external
    effect here is an expected result, and asserting it away would be asserting a
    guarantee you have not built.

## Deliverables

- [ ] Task state machine on Postgres: state enum, transition table, generated
      invalid-transition suite.
- [ ] Durable step-completion committed with the **internal** effects it produced.
- [ ] Effect classification table: every effect marked internal-transactional or
      external.
- [ ] Resume path reading the durable pointer, stopping rather than guessing where
      it disagrees with the observable world.
- [ ] Boundary-kill harness covering 100% of boundaries, with the five-part
      report and its proving test red against the in-memory build.
- [ ] **External-effect disagreement log**: the crash windows you found and are
      deliberately leaving open, with the manual repair each would need.
- [ ] 9 sends and the follow-ups logged, with per-touch attribution.

## Done when

- [ ] Killing at every step boundary leaves **internal** state at the undisturbed
      terminal position.
- [ ] Every effect is classified internal-transactional or external, and the
      internal ones demonstrably share a transaction with their state transition
      (asserted by a rolled-back transaction leaving no rows).
- [ ] The external-effect disagreement log exists and is **non-empty**, with each
      entry naming the effect, the direction of the mismatch, and the manual
      repair.
- [ ] The write-up says plainly that external-effect atomicity is unsolved and
      names the month that closes it. It does **not** claim end-to-end atomicity.
- [ ] No load-bearing progress lives in process memory, and the kill harness
      proves it by failing against the previous build.
- [ ] The invalid-transition suite is generated from the transition table, not
      hand-written.

## Reflection

1. Did you actually lose state in weeks 1–4, or did you build this because it is
   the obvious next thing? Answer honestly; the answer changes week 6.
2. Which step's effect is hardest to *observe*, and how would you learn its
   pointer was wrong?
3. Of the crash windows you found, which one would hurt most in practice — and is
   that the same one that looks worst on paper?

## Evidence

- Path to the state machine, transition table and generated suite.
- Kill-sweep output: every boundary, internal terminal state, duplicates.
- The effect classification table.
- The external-effect disagreement log.
- Send log.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
