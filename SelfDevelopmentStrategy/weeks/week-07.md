# Week 07 — Observability and Tracing

## Outcome

By Sunday you can answer *what did the platform actually do* — per run, per step,
per token — from telemetry rather than from memory. And an attacker cannot make it
spend without bound, because you tried, measured the undefended cost, and then
capped it.

## Why now?

Six weeks in you have a pipeline of nine steps, a retry layer, a resume path and a
dedup table. When a run comes out wrong you are now debugging code you did not
write, doing work that is nondeterministic, across a boundary you cannot step
through with a debugger. Single-run reasoning has stopped working.

That is the real argument, and it is worth stating precisely: **when you write the
code you carry a mental model of it and logs supplement that model. When an agent
writes it you hold only a review-derived approximation, so the trace stops
supplementing anything and becomes your primary instrument.** Observability moved
from operational hygiene to epistemic infrastructure.

## Build

**Tracing.** One connected trace per run, with correct parent-child nesting:
run → step → model call → tool call. Attach per span: harness, pinned model id,
input and output tokens, and `stall_seconds` — time owed to the rate limiter
rather than to the model or your code. That last field is the one everybody omits
and the one that later makes a cost anomaly legible.

**Cost accounting.** Tokens per task, per step, per model. Token counts must match
provider-reported usage within rounding — if they do not, your accounting is
fiction. Report tokens as the primary unit; a euro figure at a declared imputed
rate is useful context, not the measurement, while you are on a flat-rate plan.

**A bounded budget.** An aggregate spend budget per task, checked **before each
unit of work**, not sampled on a timer. Then induce a failure storm and prove the
budget holds. A token bucket for rate shaping is Stretch — placement matters when
you build it (*above* the retry layer; a limiter below the retry cannot bound
anything), but the budget is what stops runaway spend.

Pin the semantic-convention version you instrument against, and record it in the
run metadata. The conventions churn; a trace whose attribute names you cannot date
is a trace you cannot compare next quarter.

## Learn

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):
  operation-name vocabulary, agent/tool/model span shapes, token-usage attributes.
  Check the stability badge on each attribute you use. Do not memorise names — pin
  the version.
- [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)
  part I: integration points, blocked threads, unbounded result sets, cascading
  failures, slow responses. Then its patterns: timeouts, circuit breaker,
  bulkheads, fail fast, back pressure. Your platform now has three integration
  points and is acquiring exactly these shapes.

~2.5h.

## Tasks

### Core — required (~15h: 2.5h learning, 9.5h building/testing, 3h business)

1. **Instrument the pipeline.** Spans for run, step, model call and tool call,
   correctly nested, against a pinned convention version.
2. **Reconcile token counts** against provider-reported usage. Assert the match
   within rounding, in a test.
3. **Add `stall_seconds`** as a first-class span attribute, and make the metrics
   that depend on duration exclude stalled samples.
4. **Add the aggregate per-task spend budget**, checked before each unit of work,
   and prove under an induced failure storm that it bounds total spend.
5. **Run the cost-exhaustion attack.** This is the failure exercise: measure the
   undefended spend first, on a real run.
6. **Business: 8 sends, and workflow document #2.** Second workflow documented end
   to end, tagged `real` or `simulated`.

### Stretch — only after Core is DONE

- **Add the token bucket above the retry layer**, with a test proving the ordering
  (a limiter placed below the retry fails it). The aggregate spend budget in Core
  is what actually stops the bleeding; rate shaping is refinement.
- **Reconcile `stall_seconds` across a week of runs** and see whether excluding
  stalled samples changes any conclusion you had drawn. If it changes nothing at
  your volume, say so and stop excluding.
- **Now do the CLI-versus-SDK evaluation.** You have just discovered what
  telemetry, cancellation and structured tool calls actually cost you through a
  subprocess. Write it up as an ADR against the requirements table in
  [the platform file](../projects/engineering-agent-platform.md#ground-rules).
  Deciding to stay on the CLI is a valid outcome — but decide it, do not default
  into it.

## Use it for real

Trace real runs of the week-3 feature pipeline and the week-4 bug pipeline. Then
answer three questions **from the traces alone, without looking at code**: which
step is slowest, which step burns the most tokens, and which step retries most.
If you cannot answer all three, the instrumentation is not done.

## Measure

- Runs with one connected, correctly nested trace: target 100%.
- Token-count agreement with provider-reported usage: within rounding.
- Cost per task, in tokens, broken down by step. This is the first week the
  scoreboard's tokens-per-task column can be filled honestly.
- Undefended spend on the hostile input, measured on a real run — never derived
  arithmetically.
- Total spend under the induced storm, with and without the budget.

## Failure exercise

**Malicious issue causing cost exhaustion.** Make a hostile input hit a ceiling
before it spends, and put a real number on the undefended cost.

- **Detection.** An issue body drives work without bound — an enormous
  attachment, a self-referential instruction, a request that fans out. It surfaces
  when the shared retry-and-token ceiling is hit first, which makes the ceiling the
  detector.
- **Safe failure.** Apply the ceiling *ahead* of the spend, not afterwards. Refuse
  work that would exceed it rather than quietly slowing down: on a flat-rate plan
  a slowdown reads as ordinary latency, and nobody investigates latency.
- **Recovery.** Dead-letter the task with the breach on record. From here, treat
  issue bodies as hostile content for the trust boundary you build in week 11 —
  the two mitigations compose and neither is sufficient alone.
- **Logging.** Tokens spent, retries per layer, seconds parked waiting on quota,
  and which ceiling was reached.
- **Proving test.** A hostile fixture issue hits the shared ceiling and is refused
  with zero further units dispatched, with the undefended spend recorded beside
  it. **Against per-layer counting it is never refused, and the spend assertion
  breaks.**

## Deliverables

- [ ] Tracing: nested run/step/model/tool spans against a pinned convention
      version recorded in run metadata.
- [ ] Cost accounting with token counts reconciled to provider usage, asserted in
      a test.
- [ ] `stall_seconds` per span, and duration-dependent metrics excluding stalled
      samples.
- [ ] Aggregate spend budget proved to bound spend under an induced failure storm.
- [ ] Cost-exhaustion report, five parts, carrying the measured undefended spend
      and the defended one.
- [ ] The three questions answered from traces alone, written down.
- [ ] 8 sends logged; workflow document #2 with its evidence tag.

## Done when

- [ ] Every run produces one connected trace with correct parent-child nesting.
- [ ] Token counts match provider-reported usage within rounding, proved by a
      test.
- [ ] You answered slowest step, costliest step and most-retried step from
      telemetry, without reading code.
- [ ] Under an induced failure storm, total spend stays inside the aggregate
      budget.
- [ ] The hostile fixture is refused with zero further units dispatched, and the
      undefended spend is a measured figure from at least one real run.
- [ ] The scoreboard's tokens-per-task column is filled from telemetry rather
      than estimated.

## Reflection

1. What did the traces tell you that you had believed the opposite of?
2. What is the cheapest hostile input that costs you the most, and does your
   ceiling catch it?
3. One attack costs you N tokens. Is N small enough to ignore — and what would
   have to change for the answer to flip?

## Evidence

- Trace exports showing nesting, and the pinned convention version.
- Token reconciliation test.
- Storm run: spend with and without the budget.
- Cost-exhaustion report with both spend figures.
- The three telemetry-only answers.
- Send log; workflow document #2.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
