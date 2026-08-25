# Week 10 — The evaluation harness and three tiers of gate

## Outcome

By Sunday a prompt or harness change cannot merge without clearing three gates
— deterministic assertions, a judge rescore, and a five-rerun agent replay
against a pass-rate threshold I can defend.

## Time budget

- Theory: 2.5 h
- Building: 6.0 h
- Testing/evaluation: 3.5 h
- Customer discovery: 3.0 h

Testing takes 3.5 h, and for once that bucket is the point of the week rather
than its tax: T-w10-5 alone is 2.5 h of running the gate and defending its
number. The scarce input is not money. Judge inference runs a fraction of a
cent per item, which puts the whole 80-item judged load inside a EUR 0.60
ceiling against a EUR 12.00 monthly cap — twenty to four hundred passes. What
is scarce is agent re-execution: 20 tasks at five reruns is 100 agent
executions per gate pass, and canon names that the binding constraint on the
week, not the euro figure. Every quota figure the sizing rests on is measured
from week 01 rather than assumed, and the formula branches on it: five reruns
over twenty tasks needs a measured ceiling of at least 100 runs a week; at 60
to 99 the rerun count drops to three and the pass-rate bound widens, with the
widening stated; at 36 to 59 the suite drops to twelve tasks at three reruns,
the difference drawn from the cut list; below 36 the gate takes the metered
fallback at roughly EUR 15 to EUR 60. Check W01's measurement before Monday —
it decides which branch this week is on.

Compressed week, 8.0 h: T-w10-2, T-w10-4, T-w10-5 run at three reruns instead of
five for 1.5 h, T-w10-3, and T-w10-10 with T-w10-11 at the 2.5 h floor. Trace
evaluation, the conflicting-requirements exercise, T-w10-1 and T-w10-9 all defer
to [week 11](week-11.md). Three is canon's floor rather than a shortcut, so the
compressed week still ships a real gate — a smaller sample under a wider bound,
stated as such — but not the deliverable, which names an N=5 rerun policy.
Nothing ticks: D-w10-1 carries with its threshold provisional, D-w10-2 and
D-w10-3 whole, D-w10-4 without its second scored opportunity. DONE-COMPRESSED,
not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| evaluations | C | P0 | T-w10-2's 20-task suite → D-w10-1 |
| trace evaluation | C | P0 | T-w10-6, then T-w10-7 over the S5 spans → D-w10-2 |
| hallucination analysis | C | P1 | T-w10-3's lexical and NLI tiers → D-w10-2 |
| agent feedback loops | A | P1 | the gate result feeding back into the prompt, via T-w10-5 |
| pain scoring | F | P0 | T-w10-11's instrument → D-w10-4 |
| problem discovery | F | P0 | T-w10-11's register, assembled from W04–W09 |
| willingness to pay | F | P0 | one of the nine dimensions T-w10-10 scores |
| reachability | F | P0 | the buyer-access dimension in T-w10-10 |
| frequency | F | P0 | the multiplier dimension in T-w10-10 |

Every row resolves to a canon concept carrying a priority, so none needs the
earn-it or competency fallback. Homes differ inside a single track, though, and
the Track F rows are where that bites: problem discovery, willingness to pay,
reachability and frequency reason from
[Track F](../tracks/micro-saas.md), while pain scoring — also Track F — is homed
in [the opportunity scorecard](../business/opportunity-scorecard.md), which owns
the nine dimensions T-w10-10 scores against and the instrument T-w10-11 builds
from them.

The three evaluation rows reason from
[Track C](../tracks/ai-application-engineering.md); agent feedback loops from
[Track A](../tracks/agentic-engineering.md), which also owns T-w10-6's
trace-as-unit argument. T-w10-8 reinforces
[Track D](../tracks/ai-security.md), and the two Track E tasks reason from
[Track E](../tracks/consulting.md) with their follow-ups logged against
[outreach](../business/outreach.md). S6 belongs to
[the platform](../projects/engineering-agent-platform.md) and EX-FAIL-12's body
to [the agent-failure set](../exercises/agent-failures.md). This file owns the
tasks, the hours and the acceptance criteria; concept reasoning lives in the
track files and stage definitions in the project files.

## Tasks

### Task 1

`T-w10-1` — 1.5 h, Track C, theory. Reading: `RES-10`. Judge reliability:
position bias, chance-corrected agreement against raw exact-match agreement,
and the consistency-bias paradox in which a judge is highly reproducible and
still invalid. Reproducibility is not validity: a judge that agrees with
itself every time is measuring something, just not necessarily the thing in
the rubric.

### Task 2

`T-w10-2` — 2.0 h, Track C, building, reinforcing A. Build S6: the evaluation
harness and its 20-task suite, with a sandboxed environment reset before every
trial. The reset is not hygiene, it is the experiment: without it trial two
runs against a world trial one edited, and the rerun spread measures
contamination rather than variance.

### Task 3

`T-w10-3` — 1.0 h, Track C, building. Build the free-tier hallucination
analysis: lexical citation-presence checking plus a local NLI entailment
score, both offline, both at zero marginal cost. Reserve the paid judge for
cases where the two disagree — where the interesting failures live, and the
only place judge spend is proportional to genuine ambiguity.

### Task 4

`T-w10-4` — 1.0 h, Track C, building. Build all three regression tiers as
SEPARATE checks. Deterministic assertions with no model call catch a malformed
tool argument, a wrong tool selected, an illegal state transition, a missing
dedup key. `judge_regression` rescores a cached corpus against the rubric and
catches rubric and scorer drift. `agent_regression` re-executes the harness,
prompt, tool layer and retrieval as deployed. Each gate must declare which of
the three it is, because that distinction is the design: rescoring a cached
corpus tests the JUDGE, not the agent, and by construction cannot see a new
model version, a tool timeout or a changed index.

### Task 5

`T-w10-5` — 2.5 h, Track C, testing. Run `agent_regression` at five reruns per
task, report pass-rate distributions rather than a binary verdict, set the
threshold as a statistical bound against last-known-good, and justify the
number in writing. Trajectories are stochastic even at temperature zero — tool
latency, index drift and provider-side nondeterminism all move — so a binary
gate here is a coin flip wearing a badge. Then prove the split: a rubric-only
change caught by `judge_regression` alone, a tool-timeout change caught only
by `agent_regression`.

### Task 6

`T-w10-6` — 1.0 h, Track A, theory, reinforcing C. Reading: `RES-09`. The
trace as the unit of analysis: why scoring the final string discards where the
orchestration went wrong, and what two runs with the same answer but different
retry behaviour tell you. They are not the same run and should not score
alike, and no final-string metric sees the difference.

### Task 7

`T-w10-7` — 2.0 h, Track A, building. Build trace evaluation over the S5
spans, with the per-run metadata making quota-distorted samples excludable.
Last week's `quota_stall_seconds` and pinned model id exist for this: a trial
straddling a quota stall is not evidence about the agent, and it has to be
removable rather than merely regrettable.

### Task 8

`T-w10-8` — 1.0 h, Track A, testing, reinforcing D. The
conflicting-requirements exercise, measured on FLAG-VERSUS-SILENTLY-PICK
rather than on output quality, written up in five parts. Detection turns
mechanical once the agent must restate both criteria as assertions before
implementing: two assertions that cannot both hold are visible as a pair in a
way two sentences of prose are not.

### Task 9

`T-w10-9` — 0.5 h, Track E, business. Send 12 follow-ups. This Sunday all 52
sends have matured and ACT-2 reads them: zero replies across the programme's
entire outbound volume. It trips 8.5% of the time at the band midpoint, 1.6%
at the ceiling and 45.8% at the floor — the second and last activation row,
and like ACT-1 it changes something rather than being logged and left. Its
response is the same three moves: re-pitch the funnel in an out-of-cycle canon
delta, extend the Stage-1 simulated track across the remaining business
deliverables, and draw the reclaimed hours from the cut list. [Phase
01](../phases/phase-01-foundations.md#checkpoints) pre-announced this row in
week 1 with its probabilities attached.

### Task 10

`T-w10-10` — 1.0 h, Track E, business, reinforcing F. Score a second
automation opportunity against all nine dimensions, with evidence cited per
dimension rather than an intuition converted into a digit. The second score is
where the instrument becomes one: a single score is an opinion with arithmetic
attached, while two can disagree and be examined.

### Task 11

`T-w10-11` — 1.5 h, Track F, business, reinforcing E. Build the pain-scoring
model: turn the nine-dimension scorecard into a repeatable instrument, then
assemble the pain register from every call and workflow document produced
between W04 and W09, each row tagged by `evidence_source`. Under the corrected
funnel the register may hold no real rows at all, sourced entirely from
Stage-1 simulated engagements and public research. Canon is explicit that such
a register still passes, and that it feeds the kill criteria in [SaaS
validation](../business/saas-validation.md) rather than excusing invented
evidence. This is Track F's first task as a primary track.

## Deliverables

- [ ] D-w10-1 — S6 evaluation harness and 20-task suite; done includes all three regression tiers as separate checks, a five-rerun policy, and a pass-rate threshold stated as a statistical bound against last-known-good with a written justification — at `agentplat/gates/`, `evals/agent-tasks.jsonl`, `docs/w10/threshold-justification.md`
- [ ] D-w10-2 — Trace-evaluation and hallucination-analysis report over the S5 spans, using the free lexical and local-NLI tiers, with the judge reserved for cases where the two disagree — at `docs/w10/trace-eval-report.md`
- [ ] D-w10-3 — Failure report, conflicting requirements, with all five parts, scored on whether the agent flagged the conflict or silently picked — at `docs/w10/conflicting-requirements-report.md`
- [ ] D-w10-4 — Pain-scoring model and pain register, plus a second opportunity scored on all nine dimensions and 12 follow-ups logged — at `docs/w10/pain-scoring-model.md`, `pain-register.local.md`, `docs/w10/opportunity-02.md`, `send-log.local.md`

## Acceptance criteria

- [ ] AC-w10-1a — a rubric-only change is caught by `judge_regression` alone; a tool-timeout or prompt change is caught only by `agent_regression`; a malformed tool argument is caught by the deterministic tier with no model call at all (T-w10-4, T-w10-5)
- [ ] AC-w10-1b — `agent_regression` runs each task 5 times with the environment reset per trial and NEVER asserts single-run exact match; the reported figure is a pass-rate distribution (T-w10-5, T-w10-2)
- [ ] AC-w10-1c — the threshold is a stated number with a stated minimum sample size and a written justification, plus a stated condition under which it must be re-baselined (T-w10-5)
- [ ] AC-w10-1d — `judge_regression` adds ZERO new generation cost: it rescores a cached corpus, and the gate's own write-up names which of the three tiers it is and what that tier structurally cannot catch (T-w10-4)
- [ ] AC-w10-2a — the free tier costs EUR 0 in marginal spend and flags a deliberately-injected unfaithful answer in a test fixture; the trace-evaluation report scores the trace rather than the final string, names what two same-answer runs with differing retry behaviour reveal, and excludes quota-distorted samples using the per-run metadata (T-w10-3, T-w10-6, T-w10-7)
- [ ] AC-w10-2b — measured judge cost per item is compared against the planned range and any deviation is explained, with the comparison run against the tier the judge-reliability read settled on (T-w10-1, T-w10-3)
- [ ] AC-w10-3a — the conflicting-requirements report contains all five named sections; the metric reported is the rate at which the agent flagged the conflict, not the quality of what it produced, and each proving test fails against the pre-mitigation code (T-w10-8)
- [ ] AC-w10-4a — the pain register has at least six rows, each tagged `evidence_source` real or simulated, and the scoring instrument produces the same score twice for the same input; the second opportunity is scored on all nine dimensions with evidence cited per dimension, and 12 follow-ups are logged in SCOREBOARD with `evidence_source` marked (T-w10-10, T-w10-11, T-w10-9)

## Stretch goal

Outside the 15 hours. Set a target chance-corrected agreement figure the judge
must reach against a small hand-labelled subset before it is trusted inside
the gate at all, and write down what you would do if it missed — because the
honest answer might be that the judge tier is removed from the gate rather
than tolerated inside it. Attempt it only once the four deliverables are
ticked.

## Failure exercise

One exercise, and it is the only one in the programme whose metric explicitly
ignores the quality of what the agent produced. The body lives in [the agent-failure set](../exercises/agent-failures.md); D-w10-3
is the report.

### EX-FAIL-12 — conflicting requirements

- **Detection.** Two acceptance criteria in one task cannot both hold. It is detected by requiring the agent to restate the criteria as assertions before implementing, at which point the contradiction is mechanical rather than a matter of reading comprehension.
- **Safe failure behaviour.** FLAG THE CONFLICT rather than silently picking one. The metric is the flag rate, NOT the quality of what was produced — a beautiful implementation of one arbitrarily chosen requirement is the failure, and it is the failure precisely because it passes review. This is the exercise most likely to be scored wrongly by a well-meaning reader.
- **Recovery.** Return the task to `needs_clarification`, naming both criteria and why they conflict. Naming both is the requirement: a task returned with "requirements unclear" has moved the work to a human without moving any information with it.
- **Logging.** Record both criteria, whether the agent flagged or picked, and which one it picked when it picked. The last field is what turns a flag rate into a diagnosis — a consistent bias toward the first-stated criterion is a prompt problem, and a random one is not.
- **Test proving the mitigation.** Across the 20-task suite, fixtures carrying a deliberate contradiction are flagged above the declared threshold rate, and a silent pick scores as a failure even where the output satisfies one criterion cleanly. It fails against a version with no restate-as-assertions step, where the fixtures complete and look correct.

## Reflection

1. What is your pass-rate threshold, and why that number rather than a
   neighbouring one? What observation would tell you it needs re-baselining?
2. What does the free hallucination tier MISS that needs an LLM judge, and is
   that miss rate acceptable given the budget?
3. Your gate cannot catch a regression whose trigger is absent from the 20-task
   suite. Name one such regression you consider likely, and say what it would
   cost to cover it.

## Evidence

- `make gate-all` — this stage's runnable demo command — plus a path to the eval harness and its 20-task suite.
- The three gate scripts and a recorded run of each.
- The five-rerun pass-rate distribution and the written threshold justification.
- The free-tier faithfulness report over the 60 retrieval items.
- Path to the conflicting-requirements failure report with its flag rate.
- Path to the pain-scoring model and the pain register.

Log actual hours below as one line, planned first: `Theory 2.5 / <actual> ·
Building 6.0 / <actual> · Testing 3.5 / <actual> · Discovery 3.0 / <actual>`.
Four identically shaped regions per week are what the mandated recalibration
reads. Funnel counts belong on [the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W10" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- The three tiers run as genuinely separate checks — 25
- The five-rerun policy holds with a per-trial environment reset — 15
- The pass-rate threshold is stated and justified — 15
- The free hallucination tier flags an injected unfaithful answer — 10
- Trace evaluation runs over the S5 spans — 10
- The conflicting-requirements report carries all five named parts — 10
- The pain model is built and a second opportunity scored — 15
