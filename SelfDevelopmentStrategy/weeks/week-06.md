# Week 06 — Retries, Idempotency and Duplicate Effects

## Outcome

By Sunday you can replay a task a hundred times, with kills injected at random
instruction boundaries, and end with exactly one state transition, one pull
request and one dedup row per key. You built the naive version first, counted the
duplicates it produced, and classified every one.

## Why now?

Week 5 made restarts survivable. It did not make them *safe*: a resumed run
re-executes the step it died inside, and if that step already opened a pull
request you now have two. Week 3's partial-failure exercise met the same problem
from the other side. This week makes duplicate execution harmless instead of
merely rare.

## Build

Three mechanisms, in this order:

1. **A dedup table under a unique constraint**, keyed by the task's natural key.
   The dedup row commits **in the same transaction as the state transition**. A
   second connection, a second commit, or a reconciliation pass afterwards is a
   different design that does not have this property.
2. **Retry with an explicit failure classification.** Every failure gets exactly
   one verdict: retryable, permanent, or already-applied. Three verdicts, explicit
   in code, never inferred from exception classes. Most implementations lack the
   third, and it is the one that decides whether repeating is safe.
3. **One retry budget shared across every layer.** Three layers retrying three
   times each is twenty-seven calls to a service that is already failing — and on
   a flat-rate plan the symptom is a silent stall, not an error, so nobody
   investigates. Assert the sharing in a test; do not document it.

**Build the naive handler first and run it.** Replay one task a hundred times
against it and count every duplicated effect. This is not ceremony: being *told*
duplicates accumulate is what you already have. Watching them accumulate against
a counter is the thing being bought, and the classification afterwards has
nothing to classify without it.

**Say what you proved, precisely.** What you have is **effectively-once
processing under at-least-once delivery** — duplicates absorbed, not prevented.
Exactly-once *delivery* over an unreliable network is impossible: a sender that
gets no acknowledgement cannot distinguish a lost message from a lost
acknowledgement, so it resends or it does not, and there is no third option.
Exactly-once *execution* is unachievable in general unless the effect and the
record of it share one transaction. A report claiming exactly-once has claimed
something false.

## Learn

- [DDIA](https://dataintensive.net) chapter 8: unreliable networks and clocks,
  timeouts as the only failure detector, process pauses, fencing tokens. Then
  chapter 9's two-phase-commit section only — enough to see why the outbox exists,
  which is a months-4–6 build.
- [Temporal retry policies](https://docs.temporal.io/activities), read as a
  reference implementation of the classification you are about to write.

~2.5h.

## Tasks

1. **Build and run the naive handler.** Replay 100 times, count duplicates per
   effect type. Keep the numbers.
2. **Add the dedup table.** Unique constraint, natural key, row committed in the
   transition's transaction. Prove it by asserting that a rolled-back transaction
   leaves zero dedup rows — an assertion, not a code reading.
3. **Write the failure classification table.** Every error your pipeline can
   produce, mapped to exactly one of the three verdicts.
4. **Implement the shared retry budget**, with a test asserting the total call
   count under nested failure.
5. **Replay 100 times with `kill -9` at random instruction boundaries** — not step
   boundaries — with at least 20 of the 100 interrupted, including between a
   commit and each external call. Assert exactly one of each effect per key.
6. **Classify every duplicate the naive run produced**, naming which of the three
   mechanisms would have prevented each. Then write the one sentence that states
   what you actually proved.
7. **Business: 9 sends, and score one automation opportunity.** Nine dimensions,
   evidence cited per dimension, no aggregate score. Instrument in
   [consulting-and-saas.md](../business/consulting-and-saas.md).

## Use it for real

Replay real tasks — ones that genuinely open pull requests and write to your
tracker. A replay harness pointed at a stub proves your stub is idempotent.

**No `sleep` may be used to make a race reproduce.** If a race needs timing to
reproduce, the reproduction is not evidence.

## Measure

- Duplicate rate for the naive run and the corrected run, separately, over 100
  replays each. Both numbers, or the second one means nothing.
- Replays interrupted: ≥20 of 100, with interruption points recorded.
- Calls issued per failing task, before and after the shared budget.
- Duplicates classified: 100%, each naming exactly one mechanism.

## Failure exercise

**Model timeout.** Tell a stalled harness from a hard task, and stop nesting
turning three retries into twenty-seven calls.

- **Detection.** The subprocess passes its wall-clock allowance with no terminal
  event. Separate a hang from a slow-but-living run by whether *events still
  arrive* — on a clock alone, a long task and a dead one are identical. Timeout
  classification may not take elapsed time as its only input.
- **Safe failure.** Kill it and mark the *attempt* failed-but-retryable, not the
  task failed. A timeout describes your harness, not the work; conflating them
  dead-letters tasks that were never wrong.
- **Recovery.** Open a fresh attempt carrying prior state. Deliberately not a
  replay: the unit is nondeterministic and the new attempt will diverge. The
  shared retry allowance spans every layer so nesting cannot multiply it.
- **Logging.** Elapsed time, the last event seen, and whether the shared allowance
  was spent. Mark the sample excludable — a quota-stalled run distorts mean
  duration, retry rate and cost per task all at once.
- **Proving test.** A stub that hangs is killed inside its allowance and retried
  once; a third timeout dead-letters with zero further calls. **Against per-layer
  counting the call-count assertion must break.**

## Deliverables

- [ ] Naive handler run: 100 replays with duplicated effects counted per type.
- [ ] Dedup table with a unique constraint, its row committed in the transition's
      transaction, proved by the rolled-back-transaction assertion.
- [ ] Failure classification table: every error → exactly one of three verdicts.
- [ ] Shared retry budget with its call-count test.
- [ ] 100-replay kill harness: exactly one effect per key, ≥20 interrupted.
- [ ] Duplicate classification document plus the one-sentence claim of what was
      proved.
- [ ] Timeout report, five parts, proving test red against per-layer counting.
- [ ] 9 sends logged; one opportunity scored on nine dimensions with per-dimension
      evidence.

## Done when

- [ ] Across 100 replays, exactly one state transition, one PR and one dedup row
      exist per key.
- [ ] At least 20 replays were interrupted, and the interruption points are
      recorded.
- [ ] The suite fails against the naive handler.
- [ ] 100% of the naive run's duplicates are classified, each naming exactly one
      of the three mechanisms.
- [ ] The written claim says *effectively-once processing under at-least-once
      delivery*, and nothing stronger.
- [ ] A third timeout dead-letters, issuing zero further calls.
- [ ] The scored opportunity carries an evidence line on all 9 dimensions, with
      unevidenced ones marked `assumed`, and no aggregate score anywhere.

## Reflection

1. Which of your steps are genuinely idempotent by construction, and which are
   idempotent only because nothing has called them concurrently yet?
2. Your dedup key is a choice. What input would produce two *legitimate*
   operations that collide on it, and what would that cost?
3. Your timeout detector reads silence. Which legitimate operation in your
   pipeline goes quiet longest?

## Evidence

- Naive-run duplicate counts and corrected-run counts, side by side.
- The 100-replay harness output with interruption points.
- Failure classification table; shared-budget call-count test.
- Duplicate classification document and the claim sentence.
- Timeout report and its red-on-parent test.
- Send log; scored opportunity.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
