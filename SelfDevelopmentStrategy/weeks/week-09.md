# Week 09 — Observability as the primary instrument

## Outcome

By Sunday I can answer what the platform did — per run, per span, per euro —
from telemetry rather than from memory, and an attacker cannot make it spend
without bound.

## Time budget

- Theory: 3.0 h
- Building: 5.5 h
- Testing/evaluation: 3.0 h
- Customer discovery: 3.5 h

Customer discovery takes 3.5 h, its joint highest in the programme, because the
M2 data pull sits alongside the usual sends and a second workflow document. The
engineering half assumes general tracing literacy and spends its hours on the
GenAI-specific conventions instead. That pitch rests on USI-11, the one
competency row canon did not ask the user for but inferred, and canon flags it
for confirmation at M1 precisely because an assumed level-2 already under-served
retrieval once. If the confirmation comes back lower, this is the week to say so
in the M2 retrospective rather than to discover it in W10. Ceilings are EUR 0.00
of metered spend and 55 agent runs; canon's stated reason for a count that
modest is that the failure-storm test drives a stubbed failing endpoint and
consumes no model quota at all.

Compressed week, 8.0 h: T-w09-2, T-w09-5 cut to 1.5 h, T-w09-7 at its full hour
because the M2 retrospective is never cut, and T-w09-9 with T-w09-10 whole at
2.5 h. T-w09-10 stays intact because it carries the M2 funnel data pull the
retrospective reads. The cost-exhaustion exercise and the OTel theory read both
defer to [week 10](week-10.md), with T-w09-4, T-w09-6, T-w09-8 and T-w09-11. The
retrospective survives every compression for the same reason it did at M1: it is
the only instrument that edits the plan. D-m02-4 ticks. D-w09-1 carries without
its pinned convention version or its proved retry budget, D-w09-2 whole, D-w09-3
without its 5 sends. DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| observability | B and C | P0 | T-w09-2's span tree → D-w09-1 |
| reliability | B | P0 | T-w09-5's latency budgets → D-w09-1 |
| rate limiting | B | P0 | T-w09-4, then T-w09-5's token bucket |
| caching | B | P1 | the middleware slot S4 left open, read here against cost |
| cost optimization | C | P0 | T-w09-5's cost accounting → D-w09-1 |
| latency | C | P1 | T-w09-5's per-stage budgets → D-w09-1 |
| cost/token budgets | A | P0 | T-w09-5's aggregate retry budget → AC-w09-1c |
| excessive agency | D | P0 | T-w09-3's adversarial issue → D-w09-2 |
| outreach | E | P0 | T-w09-8 and T-w09-9 → D-w09-3 |

Every row resolves to a canon concept carrying a priority, so none needs the
earn-it or competency fallback. One row resolves twice: observability is a
concept in both Track B and Track C, and this week uses both readings — the
operational one in T-w09-4 and the application one in the spans T-w09-2 emits.
The table names both rather than picking the convenient one.

Reliability, rate limiting and caching reason from
[Track B](../tracks/system-design.md); cost optimization and latency from
[Track C](../tracks/ai-application-engineering.md); token budgets from
[Track A](../tracks/agentic-engineering.md), which also owns the OTel reading in
T-w09-1; excessive agency from [Track D](../tracks/ai-security.md). Outreach is
homed in [outreach](../business/outreach.md) rather than in its own track, while
the discovery practice around it reasons from
[Track E](../tracks/consulting.md) and reinforces
[Track F](../tracks/micro-saas.md). S5 belongs to
[the platform](../projects/engineering-agent-platform.md); EX-FAIL-11's body to
[the agent-failure set](../exercises/agent-failures.md); the M2 retrospective to
[month 02](../months/month-02.md). This file owns the tasks, the hours and the
acceptance criteria; concept reasoning lives in the track files and stage
definitions in the project files.

## Tasks

### Task 1

`T-w09-1` — 1.5 h, Track A, theory. Reading: `RES-09`. The OTel GenAI semantic
conventions as a MOVING TARGET: the operation-name vocabulary, the agent and
tool span shapes, the token-usage attributes — and the discipline of pinning a
version rather than memorising today's attribute names. Which names are
current is a dated fact rather than a durable one, so it is quarantined in
[the ecosystem snapshot](../resources/ecosystem-snapshot-2026-08.md) under a
re-verify date of 2026-11-30, which is M3's mandated delta. Read the pinned
version; do not learn the vocabulary by heart.

### Task 2

`T-w09-2` — 3.0 h, Track A, building, reinforcing C. Build S5: wrap the
platform in agent, tool and model spans with correct parent-child nesting,
populate the provider, operation and token attributes, record
`quota_stall_seconds`, harness version and pinned model id per run, and export
over OTLP to a local collector. The per-run metadata is the part that pays
later — a silent convention upgrade mid-project becomes a detectable event
rather than a week of confusion.

### Task 3

`T-w09-3` — 1.5 h, Track A, testing, reinforcing D. Run the malicious GitHub
issue against your own platform: an issue body that drives unbounded work
through a huge input, a recursive instruction or a request that fans out.
Measure the spend and the quota it consumed, then write the five-part report.
The measured before-number is the deliverable; a defense with no number in
front of it cannot be shown to have done anything.

### Task 4

`T-w09-4` — 1.5 h, Track B, theory, reinforcing D. Reading: `RES-15`. Rate
limiting and quota as a SHARED FINITE RESOURCE. The subscription quota behaves
as a global semaphore across every worker S4 started, which is why bounding
concurrency usually beats bounding rate: a rate cap admits an unbounded number
of simultaneous holders, and the queue you built last week can produce them.
Close on why observability becomes epistemic infrastructure once you did not
write the code — telemetry stops being an operations nicety and becomes the
only route to knowing what happened.

### Task 5

`T-w09-5` — 2.5 h, Track B, building. Build cost accounting, per-stage latency
budgets and the unbounded-retry defense: one aggregate retry budget spanning
every layer, `Retry-After` honoured rather than ignored, and a token bucket
sitting ABOVE the retry layer. Above is the whole design. Three layers each
retrying three times is twenty-seven calls into a service that is already
failing, and per-layer counts cannot see that number.

### Task 6

`T-w09-6` — 0.5 h, Track B, testing. Prove the retry budget bounds total spend
under an induced failure storm, and that quota-stalled samples can be excluded
so average task duration and retry rate stay interpretable. A stall is not
slowness, and a metric that averages the two describes neither.

### Task 7

`T-w09-7` — 1.0 h, Track P, testing, reinforcing E. The M2 retrospective,
written into [month 02](../months/month-02.md). Ten questions, RQ-01 to RQ-10,
then RQ-11 — the canon delta canon mandates rather than invites. M2's is the
funnel recalibration: the measured reply rate against the planned 1.5–8% band,
and measured per-touch attribution against the 42–65% follow-up band. Canon
sites it here because 41 to 47 matured sends exist by W08 and W09, where M1
read only 15. Canon also attaches an honesty rule that matters more than the
arithmetic: at 41 matured sends the observable rates are 0%, 2.4%, 4.9% and
nothing between, so a band rewritten on one or two replies is noise dressed as
measurement. State the sample size beside the revised band, always. The
six-step loop lives at [HOW-TO-EDIT](../HOW-TO-EDIT.md#the-control-loop).

### Task 8

`T-w09-8` — 0.5 h, Track E, business, reinforcing F. Five cold emails, drafted
with BOA-S0 and approved individually. These close the 37 assisted sends, and
with them the programme's whole outbound volume: 52 sends, of which none
remain after this week.

### Task 9

`T-w09-9` — 0.6 h, Track E, business. Send 17 follow-ups, the largest single
follow-up block in the programme. It is large because the two-per-prospect
rule now has almost the entire send list behind it, and because the M2 pull
one task later reads per-touch attribution — a follow-up that goes unsent is a
data point the recalibration will not have.

### Task 10

`T-w09-10` — 1.9 h, Track E, business, reinforcing F. Workflow documentation
#2, from a real call if one has happened and otherwise as consulting Stage 1,
simulated, against [the automation-audit
template](../templates/automation-audit.md). Tag it `evidence_source` either
way. Canon calls the simulated route the expected path here rather than a
contingency, and the Stage-1 exit criteria are the standard to meet in either
case: named steps, an estimated frequency, an estimated time cost, and an
artifact a stranger could read as evidence of the skill.

### Task 11

`T-w09-11` — 0.5 h, Track E, business, reinforcing F. Pull the M2 funnel data:
sends, replies broken out by touch number, calls, and the measured reply rate
against the planned band. Per-touch is the part that is easy to skip and
impossible to reconstruct later. The funnel targets themselves are homed in
[customer discovery](../business/customer-discovery.md); this task produces
the measurement they get compared against.

## Deliverables

- [ ] D-w09-1 — S5 observability and cost accounting: correctly nested agent, tool and model spans with a PINNED convention version, per-run harness and model metadata, `quota_stall_seconds`, latency budgets, and an aggregate retry budget proved to bound spend under an induced failure storm — at `agentplat/telemetry/`, `docs/w09/trace-evidence.md`
- [ ] D-w09-2 — Failure report, malicious GitHub issue causing adversarial cost exhaustion, with all five parts, including the measured spend and quota consumed before the defense — at `docs/w09/cost-exhaustion-report.md`
- [ ] D-w09-3 — Workflow documentation #2 tagged `evidence_source`, plus 5 sends, 17 follow-ups and the M2 funnel data pull — at `workflow-02.local.md`, `send-log.local.md`, `docs/w09/m2-funnel-pull.md`

## Acceptance criteria

- [ ] AC-w09-1a — one connected trace per run with correct parent-child nesting across a multi-tool-call task, and span token counts match provider-reported usage within rounding; the rate-limiting write-up states the concurrency bound the quota semaphore enforces and why bounding concurrency beats bounding rate (T-w09-2, T-w09-4)
- [ ] AC-w09-1b — the exporter records the convention version, the harness version and the pinned model id per run, so a silent convention upgrade is detectable rather than merely survivable (T-w09-1, T-w09-2)
- [ ] AC-w09-1c — under an induced failure storm, total attempts across all layers stays under the declared aggregate budget, and a run that would exceed it is refused rather than throttled silently (T-w09-5, T-w09-6)
- [ ] AC-w09-1d — quota-stalled samples are identifiable and excludable from the average-task-duration and retry-rate metrics (T-w09-6)
- [ ] AC-w09-2a — the cost-exhaustion report states the spend and quota consumed BEFORE the defense as measured numbers, all five named sections are present, and each proving test fails against the pre-mitigation code (T-w09-3)
- [ ] AC-w09-3a — workflow documentation #2 carries an `evidence_source` tag, and the M2 data pull states the measured reply rate with its denominator and compares it to the planned band (T-w09-10, T-w09-11)
- [ ] AC-w09-3b — the M2 delta lands as an edit to `canon.yaml` with `meta.version` bumped, and either rewrites `funnel.reply_rate_band` or explicitly records that the measurement was too thin to justify a change, with the sample size stated beside it; and 5 sends and 17 follow-ups are logged in SCOREBOARD with per-touch attribution and `evidence_source` marked (T-w09-7, T-w09-8, T-w09-9)

## Stretch goal

Outside the 15 hours. Instrument the free-tier hallucination check as a span
attribute, so faithfulness rides the same trace as cost and latency rather than
arriving as a separate report a week later. Doing it here rather than in W10
means the trace-evaluation work lands on spans that already carry the signal.
Run it only once the three deliverables are ticked.

## Failure exercise

One exercise, and it is the first in the programme where the adversary is
outside the system rather than inside it. The body lives in
[the agent-failure set](../exercises/agent-failures.md); D-w09-2 is the report.

### EX-FAIL-11 — malicious GitHub issue

- **Detection.** An issue body drives unbounded work — a huge input, a recursive instruction, or a request that fans out. It is detected by the aggregate retry and token budget tripping before the task completes, which means detection is a property of the budget existing rather than of anyone recognising the issue as hostile.
- **Safe failure behaviour.** The budget is enforced BEFORE the spend, not observed after it. A task that would exceed its budget is refused outright rather than throttled quietly, because under a flat-rate plan a silent throttle is indistinguishable from the system being slow — and slowness is the one symptom nobody escalates.
- **Recovery.** Dead-letter the task with the budget breach recorded, and from here an issue body counts as untrusted content wherever the W11 trust boundary applies. This exercise is where that boundary stops being a Track D abstraction and acquires a concrete first instance.
- **Logging.** Record tokens consumed, retries attempted at each layer, `quota_stall_seconds`, and which budget tripped. Per-layer retry counts alongside the aggregate is what lets you tell a runaway inner loop from a genuinely failing dependency after the fact.
- **Test proving the mitigation.** An adversarial fixture issue trips the aggregate budget and is refused, and the spend measured before the defense is recorded as a number for comparison. It fails against a version carrying per-layer retry counts only, where the fixture completes and the spend is discovered afterwards.

## Reflection

1. You now have no mental model of code you did not write, only telemetry. Name
   one question about the system you can answer today that you could not answer
   in week 8.
2. Which convention attributes changed since the version you pinned? What breaks
   if the SDK silently upgrades conventions mid-project, and how would you find
   out?
3. The cost-exhaustion attack consumed a measured amount before the defense
   fired. Under a flat-rate plan the failure mode was a stall rather than a bill
   — what signal would have told you it was an attack rather than slowness?

## Evidence

- `make demo-s5 && make trace-view` — this stage's runnable demo command — and an exported trace showing the full span tree with correct nesting.
- The recorded convention version, harness version and pinned model id.
- The failure-storm run showing total attempts bounded by the aggregate budget.
- Path to the cost-exhaustion failure report with its measured spend.
- Path to workflow documentation #2 and its `evidence_source` tag.
- The M2 funnel data pull, and the M2 canon delta with the bumped `meta.version`.

No threshold is sited at this week's boundary. Five sends carry the matured
total from 41 to 47, and the next row reads the 52 that mature at the close of
[week 10](week-10.md): ACT-2, which trips on zero replies across every send the
programme makes, 8.5% likely at the band midpoint and 45.8% at its floor. No
call slot is budgeted this week either, so nothing here returns as slack.

Log actual hours below as one line, planned first:
`Theory 3.0 / <actual> · Building 5.5 / <actual> · Testing 3.0 / <actual> ·
Discovery 3.5 / <actual>`. Four identically shaped regions per week are what the
mandated recalibration reads. Funnel counts belong on
[the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W09" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- Agent, tool and model spans nest correctly across a real run — 25
- The convention version is pinned and recorded per run — 10
- The aggregate retry budget bounds spend under the storm — 20
- Quota-stalled samples are excludable from the metrics — 10
- The cost-exhaustion report carries all five named parts — 15
- Workflow document #2 and the M2 funnel pull are delivered — 20
