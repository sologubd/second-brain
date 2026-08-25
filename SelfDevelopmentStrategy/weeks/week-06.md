# Week 06 — Retries, Idempotency and Duplicate Effects

## Outcome

By Sunday you can replay a task a hundred times, with kills injected at random
instruction boundaries, and end with exactly one state transition and one dedup
row per key. Every *external* effect is classified by the idempotency mechanism
actually available for it — and the ones that have no such mechanism yet are
written down as unresolved rather than papered over. You built the naive version
first and counted the duplicates it produced.

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

### Internal idempotency is not external idempotency

Your dedup table makes **your own** state safe: the row and the transition commit
together, so replaying the step cannot produce a second transition. That is
internal idempotency and you can prove it outright.

An **external** effect is only idempotent if the external system gives you a
mechanism for it. There are four, and you must name which one applies to each
effect:

| Mechanism | What it looks like |
|---|---|
| Provider idempotency key | The API accepts a client-supplied key and dedupes server-side |
| Natural unique key | The resource has a uniqueness constraint you can collide with deliberately (a branch name, a slug, a tag) |
| Query-before-create on stable identity | You can look the resource up by something you control before creating it — with a race window you must state |
| Provider-side dedup | The provider collapses identical requests itself, documented |

**Build this table for every external effect your pipeline has**, and fill in the
last two columns honestly:

| Effect | Idempotency mechanism | Guaranteed? | Remaining crash window |
|---|---|---|---|
| Task state transition | dedup row in the same transaction | **yes** | none |
| Branch creation | natural unique key (branch name from task id) | yes | none |
| Pull request creation | query-before-create by head branch | **no — race window** | two workers can both see "no PR" and both create |
| Tracker comment | *(none available?)* | **no** | duplicate comment on replay |
| Email / outbound send | provider idempotency key, if the provider has one | depends | state it |

Where no mechanism exists, mark the row:

> **unresolved until external-effect durability / outbox work (months 4–6)**

That is a legitimate and expected answer. It is not a gap in your week; it is the
week's most useful finding.

**Do not fake a green test.** If you replace an external call with a stub that
dedupes, your suite is proving a property of your stub, not of the real API. Test
the internal path against the real invariant, and test the external path against
whatever the provider actually offers — and if the provider offers nothing, the
test asserts the *duplicate happens* and the row stays marked unresolved. A red
truth beats a green fiction.

**Build the naive handler first and run it.** Replay one task a hundred times
against it and count every duplicated effect. This is not ceremony: being *told*
duplicates accumulate is what you already have. Watching them accumulate against
a counter is the thing being bought, and the classification afterwards has
nothing to classify without it.

**Say what you proved, precisely.** What you have is **effectively-once
processing under at-least-once execution** — duplicates absorbed, not prevented,
*for the effects where a mechanism exists.* Exactly-once *delivery* over an
unreliable network is impossible: a sender that gets no acknowledgement cannot
distinguish a lost message from a lost acknowledgement, so it resends or it does
not, and there is no third option. Exactly-once *execution* is unachievable in
general unless the effect and the record of it share one transaction — which is
exactly why the table above splits into rows that can make the claim and rows
that cannot.

The claim must be no stronger than the mechanisms you actually implemented. "One
external effect under arbitrary process death" is only true where the provider
gave you a way to make it true.

## Learn

- [DDIA](https://dataintensive.net) chapter 8: unreliable networks and clocks,
  timeouts as the only failure detector, process pauses, fencing tokens. Then
  chapter 9's two-phase-commit section only — enough to see why the outbox exists,
  which is a months-4–6 build.
- [Temporal retry policies](https://docs.temporal.io/activities), read as a
  reference implementation of the classification you are about to write.

~2.5h.

## Tasks

### Core — required (~15h: 2.5h learning, 9.5h building/testing, 3h business)

1. **Build and run the naive handler.** Replay 100 times, count duplicates per
   effect type. Keep the numbers.
2. **Fill in the external-effect table** above: every external effect, its
   available mechanism, whether it is guaranteed, and the remaining window. Read
   the provider docs for each — this is research, and it is the part that stops
   you overclaiming. Mark the unresolved rows.
3. **Add the dedup table.** Unique constraint, natural key, row committed in the
   transition's transaction. Prove it by asserting that a rolled-back transaction
   leaves zero dedup rows — an assertion, not a code reading.
4. **Implement the mechanism that exists for each external effect** — an
   idempotency key where the provider takes one, a natural unique key where the
   resource has one, query-before-create where that is all you have (and record
   the race window). **Leave the unresolved rows unresolved.**
5. **Write the failure classification table.** Every error your pipeline can
   produce, mapped to exactly one of the three verdicts.
6. **Implement the shared retry budget**, with a test asserting the total call
   count under nested failure.
7. **Replay 100 times with `kill -9` at random instruction boundaries** — not step
   boundaries — with at least 20 of the 100 interrupted, including between a
   commit and each external call. Assert **exactly one state transition and one
   dedup row per key**, and for external effects assert whatever the table says is
   actually guaranteed. Where the table says *no*, assert the duplicate and record
   it.
8. **Business: 9 sends, and score one automation opportunity.** Nine dimensions,
   evidence cited per dimension, no aggregate score. Instrument in
   [consulting-and-saas.md](../business/consulting-and-saas.md).

### Stretch — only after Core is DONE

- **Classify every duplicate the naive run produced**, naming which mechanism
  would have prevented each, and write the one-sentence claim of what you proved.
  Do the one sentence even if you skip the full classification — it is thirty
  seconds and it is what keeps the claim honest.
- **Close one unresolved row** by finding a mechanism you did not know the
  provider had. Read the API reference properly rather than guessing; providers
  often support idempotency keys on endpoints where it is not obvious.
- **Measure the race window** on a query-before-create effect: run two workers at
  it deliberately and find out how often they collide. That number decides whether
  it is a real risk or a theoretical one.

## Use it for real

Replay real tasks — ones that genuinely open pull requests and write to your
tracker. **A replay harness pointed at a stub proves your stub is idempotent**,
which is the single easiest way to fake this week. Where you must stub for cost or
rate-limit reasons, the stub has to behave like the real API *including its lack
of guarantees* — a stub that dedupes when the real endpoint does not has
manufactured your result.

**No `sleep` may be used to make a race reproduce.** If a race needs timing to
reproduce, the reproduction is not evidence.

## Measure

- Duplicate rate for the naive run and the corrected run, separately, over 100
  replays each, **per effect**. Both numbers, or the second one means nothing.
- Replays interrupted: ≥20 of 100, with interruption points recorded.
- External effects with a working mechanism, over external effects total. This
  fraction is the honest headline, and it will not be 1.
- Calls issued per failing task, before and after the shared budget.

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
- [ ] **External-effect idempotency table**: effect · mechanism · guaranteed? ·
      remaining crash window, with unresolved rows explicitly marked.
- [ ] Dedup table with a unique constraint, its row committed in the transition's
      transaction, proved by the rolled-back-transaction assertion.
- [ ] The available mechanism implemented for each external effect that has one.
- [ ] Failure classification table: every error → exactly one of three verdicts.
- [ ] Shared retry budget with its call-count test.
- [ ] 100-replay kill harness: one state transition and one dedup row per key,
      ≥20 interrupted, external effects asserted only to what the table supports.
- [ ] The one-sentence claim of what was proved.
- [ ] Timeout report, five parts, proving test red against per-layer counting.
- [ ] 9 sends logged; one opportunity scored on nine dimensions with per-dimension
      evidence.

## Done when

- [ ] Across 100 replays, exactly one state transition and one dedup row exist
      per key.
- [ ] Every external effect appears in the table with a named mechanism or an
      explicit **unresolved** marker; zero effects are silently omitted.
- [ ] Every effect the table marks guaranteed is asserted against the **real**
      provider behaviour, not against a stub that dedupes on your behalf.
- [ ] At least 20 replays were interrupted, and the interruption points are
      recorded.
- [ ] The suite fails against the naive handler.
- [ ] The written claim says *effectively-once processing under at-least-once
      execution, for the effects with a mechanism* — and nothing stronger.
- [ ] A third timeout dead-letters, issuing zero further calls.
- [ ] The scored opportunity carries an evidence line on all 9 dimensions, with
      unevidenced ones marked `assumed`, and no aggregate score anywhere.

## Reflection

1. Which of your steps are genuinely idempotent by construction, and which are
   idempotent only because nothing has called them concurrently yet?
2. Your dedup key is a choice. What input would produce two *legitimate*
   operations that collide on it, and what would that cost?
3. Which external effect has no mechanism at all, and what is the cheapest thing
   the provider could add that would give you one?
4. Your timeout detector reads silence. Which legitimate operation in your
   pipeline goes quiet longest?

## Evidence

- Naive-run duplicate counts and corrected-run counts, side by side.
- The 100-replay harness output with interruption points.
- Failure classification table; shared-budget call-count test.
- Duplicate classification document and the claim sentence.
- Timeout report and its red-on-parent test.
- Send log; scored opportunity.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
