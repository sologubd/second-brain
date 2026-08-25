# Week 05 — Persistence, Restart and Resume

## Outcome

By Sunday every step's completion is recorded durably before the next step
starts, a `kill -9` anywhere in the pipeline resumes from what was actually
written rather than from what a dead process believed, and you have reviewed your
own platform against a real defect checklist for the first time.

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
2. **Completion recorded before the next step starts.** The transaction that
   records a step's completion is the same transaction that produced its effect.
   Not two commits, not a reconciliation pass afterwards.
3. **Resume from the durable pointer, and nothing else.** On restart, read the
   pointer and continue. Where the pointer and the observable world disagree,
   **stop** — do not guess. A guess either repeats an external effect or skips
   one, and afterwards neither is visible.

Ask an agent for "a state machine" and you get the class-per-state form, which
dies with the process. The whole point here is state as data in a row you can
`SELECT`.

Also this week: **write down the aggregates and invariants.** What must always be
true, which aggregate owns it, and where it is enforced. Three columns, one table.
It takes twenty minutes and it is the document that makes the transaction
boundaries obviously correct rather than memorised.

**Not yet:** retries (week 6), idempotency keys (week 6), the outbox (months 4–6),
queues (week 8). This week the pipeline resumes; it does not yet absorb duplicates.

## Learn

- [DDIA](https://dataintensive.net) chapter 7 on transactions. Read-committed
  isolation and the lost update it permits; unique and partial indexes as the only
  reliable dedup primitive; and that external APIs offer no isolation at all.
- [Temporal's activity docs](https://docs.temporal.io/activities) — how a mature
  system words its guarantee. Then write one paragraph naming what it solves that
  your hand-built version does not, and whether that gap matters at your scale.
- [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php)
  chapters 4 and 5, for the architecture review below.

~3h. This is the heaviest reading week of the twelve.

## Tasks

1. **Stand up Postgres and the task table.** State column, transition table,
   generated invalid-transition test suite.
2. **Move progress out of process memory.** Every step boundary commits before
   the next step begins. Nothing load-bearing lives in a variable that dies with
   the process.
3. **Write the aggregate-and-invariant table.** Three columns: invariant, owning
   aggregate, where enforced.
4. **Build the boundary-kill harness.** Kill the process at *every* step boundary
   in turn — not a sample — and assert the resumed run lands where an undisturbed
   run lands. This is the failure exercise.
5. **Architecture review #1.** Write the generated-code review checklist first,
   then apply it to the platform as it stands, including to this week's own diff.
   Instructions and the fourteen defect classes are in
   [exercises/architecture.md](../exercises/architecture.md).
6. **Business: 9 sends, assisted.** Use the Business Operations Agent's
   extraction step ([BOA capability 1](../projects/business-operations-agent.md))
   to research prospects, and approve every draft before it leaves. Add the two
   follow-ups for earlier prospects; each must carry something the previous touch
   did not.

## Use it for real

Run the week-3 and week-4 pipelines under the new persistence layer, on real
tasks, with real interruptions. Then kill it deliberately, everywhere.

## Measure

- Kill points exercised, and how many produced the undisturbed terminal state.
  Target: 100% of boundaries, all landing correctly.
- Effects that occurred twice across the kill sweep. Target zero — and if it is
  not zero, you have just found week 6's justification, which is a good outcome.
- Kill-to-resume distance: how long work sat orphaned. Record p50 and the worst
  case; without it "did it resume?" has only an anecdote as an answer.
- Review findings: defect classes assessed with evidence, over 14.

## Failure exercise

**Agent context loss after restart.** Prove a restarted run continues from what
was durably written, never from what a dead process believed it had done.

- **Detection.** On resume, hold the stored pointer against the observable world.
  Two mismatches are possible and both are defects: a step marked unfinished
  whose effect exists, and one marked finished whose effect is missing.
- **Safe failure.** Continue from the durable pointer and nothing else. Where
  pointer and world disagree, stop.
- **Recovery.** Re-run from the stored pointer. The transaction recording
  completion is the one that produced the effect, so repeating is harmless *by
  design* rather than by discipline — the only kind of safety that holds at four
  in the morning.
- **Logging.** The pointer at kill time and at resume, and the wall-clock distance
  between them.
- **Proving test.** Kill at each boundary in turn; assert the resumed run reaches
  the undisturbed terminal state and that nothing happened twice. **Point it at
  last week's in-memory version and it must break.**

## Deliverables

- [ ] Task state machine on Postgres: state enum, transition table, generated
      invalid-transition suite.
- [ ] Durable step-completion recorded in the same transaction as the effect.
- [ ] Resume path reading the durable pointer, with the disagreement case
      stopping rather than guessing.
- [ ] Aggregate-and-invariant table.
- [ ] Boundary-kill harness covering 100% of boundaries, with the five-part
      report and its proving test red against the in-memory build.
- [ ] Architecture review #1: versioned checklist plus the review written as an
      ADR.
- [ ] 9 sends and the follow-ups logged, with per-touch attribution.

## Done when

- [ ] Killing at every step boundary yields the undisturbed terminal state.
- [ ] Zero effects occurred twice across the kill sweep — or the duplicates are
      counted and classified, and week 6 is scoped against them.
- [ ] No load-bearing progress lives in process memory, and the kill harness
      proves it by failing against the previous build.
- [ ] The invalid-transition suite is generated from the transition table, not
      hand-written.
- [ ] The review checklist is versioned and carries at least 4 question
      categories; the ADR names ≥3 of the 14 defect classes with cited evidence
      rather than ticks.
- [ ] Applying the checklist to this week's own diff produced at least one
      recorded finding.

## Reflection

1. Did you actually lose state in weeks 1–4, or did you build this because it is
   the obvious next thing? Answer honestly; the answer changes week 6.
2. Which step's effect is hardest to observe, and how would you learn its pointer
   was wrong?
3. You marked several defect classes absent. Which absences rest on evidence, and
   which on the fact that you have not built the surface where they would appear?
   Those are not the same claim.

## Evidence

- Path to the state machine, transition table and generated suite.
- Kill-sweep output: every boundary, terminal state, duplicates.
- Aggregate-and-invariant table.
- The versioned checklist and the review ADR.
- Send log.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
