# Week 03 — Effectively-once under adversarial restarts

## Outcome

By Sunday I can replay one task event 100 times with process kills injected at
random points and prove that exactly one domain state transition, one recorded PR-intent and one
dedup row resulted.

## Time budget

- Theory: 2.5 h
- Building: 6.0 h
- Testing/evaluation: 3.0 h
- Customer discovery: 3.5 h

Start with what this week does not claim. Exactly-once delivery over an
unreliable network is impossible: a sender receiving no acknowledgement cannot
tell a lost message from a lost acknowledgement, so it resends and risks
duplicates, or stays silent and risks loss. The achievable property is the
outcome — at-least-once delivery plus idempotent processing gives
effectively-once results, state after N deliveries equalling state after one.
Duplicates are absorbed, not prevented, and that distinction is the lesson rather
than a footnote to it. T-w03-5 makes stating it assessed work.

The week is built failure-first for the same reason. USI-10's operation-weak
half is not repaired by being told duplicates happen; it is repaired by watching
them accumulate in your own replay log, so the naive handler is built first on
purpose. Canon calls this the tightest week in the programme — four deliverables
at the cap, two subsystems, two failure exercises, the thinnest business slack
anywhere — and audits its budget for that reason. Metered spend is EUR 0.00
against a cap of 30 agent runs; the 100 replays are local and consume no model
quota, the external call being fully stubbed for 80 replays and routed through the
real outbox relay for 20 — but in both cases the destination is a **local
recording sink**, never GitHub or Notion. S2 opens a real pull request at W04 and
S8 writes to Notion at month 04; neither exists yet. What this week proves is
at-most-once *delivery*, and the sink is what makes that assertion checkable.
S1b extends S1a,
so BOA-S0 is the only new subsystem and no cap exception is priced.

Compressed week, 8.0 h: T-w03-2 at 3.0 h, then T-w03-4 at 2.5 h —
non-negotiable, because it *is* the week — with T-w03-8, T-w03-9 and T-w03-10
whole and T-w03-11 cut to 0.4 h. The outreach tasks stay intact and the workflow
rehearsal is the one shortened, because discovery has to reach 2.5 h and this is
the arrangement that gets there. T-w03-1, T-w03-3 and T-w03-5 defer to
[week 04](week-04.md), and BOA-S0 with them, which pushes assisted prospect
research out to W05; record that as a funnel delta rather than absorbing it
quietly. Only D-w03-4 ticks. D-w03-1 carries — the replay runs, the retry truth
table and the written duplicate classification do not, and the assessed sentence
travels with T-w03-5 — alongside D-w03-2 and an unfinished D-w03-3.
DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| idempotency | B | P0 | T-w03-2's dedup table under a unique constraint → D-w03-1 |
| transactions | B | P0 | the dedup insert riding the state transition in T-w03-2 |
| consistency | B | P0 | the three dedup mechanisms from T-w03-1, each exercised in T-w03-4 |
| retries | B | P0 | T-w03-3's error-classification truth table → D-w03-1 |
| resumability | A | P0 | resume-from-last-step, proved across T-w03-4's 100 replays |
| failure recovery | B | P0 | EX-FAIL-03's reconciliation path → D-w03-4 |
| structured outputs | C | P0 | T-w03-6, then BOA-S0's extraction schema in T-w03-7 → D-w03-2 |
| outreach | E | P0 | T-w03-9 and T-w03-10 → D-w03-4 |
| discovering repetitive workflows | E | P0 | T-w03-11 → D-w03-3 |

Every row resolves to a canon concept carrying P0, so none needs the earn-it or
competency fallback. Two rows want care. Retries is carried twice by canon, once
in [Track B](../tracks/system-design.md) and once in
[Track A](../tracks/agentic-engineering.md), which also homes resumability; the
row above follows T-w03-3's primary track. And the two Track E rows do not share
a home: outreach belongs to [the outreach file](../business/outreach.md) while
discovering repetitive workflows belongs to
[Track E's own file](../tracks/consulting.md). Structured outputs is
[Track C](../tracks/ai-application-engineering.md). T-w03-1 and T-w03-3 reinforce
[Track D](../tracks/ai-security.md), the business tasks reinforce
[Track F](../tracks/micro-saas.md), and T-w03-7 reinforces Track E in the other
direction — the extractor exists to serve the funnel. Tasks, hours and acceptance are owned here; S1b is owned by
[the platform file](../projects/engineering-agent-platform.md) and BOA-S0 by
[the business operations agent](../projects/business-operations-agent.md).

## Tasks

### Task 1

`T-w03-1` — 1.0 h, Track B, theory, reinforcing D. Reading: `RES-13`. Separate
delivery, execution and outcome, then enumerate the three dedup mechanisms and
say which of your external effects each one covers. Shared-transaction dedup —
effect and dedup row in one database under a unique constraint — is the only
place a strong once-only claim is honest. A supplied idempotency key inherits
the remote system's guarantee and no stronger one. A natural key or
conditional create, one pull request per branch name, is the one to reach for
first.

### Task 2

`T-w03-2` — 3.0 h, Track B, building. Build S1b: idempotent steps, a dedup
table under a unique constraint committed in the same transaction as the state
transition, and resume-from-last-step. The constraint does the work; the
application does not check first and then act, because between the check and
the act is precisely where the second delivery arrives.

### Task 3

`T-w03-3` — 1.0 h, Track B, building, reinforcing D. Retries with jitter, an
explicit error-classification truth table — retryable, permanent,
already-applied — and a retry budget that aggregates across layers. Aggregate
is the operative word: three retries at three independent levels is
twenty-seven calls, and the layers that agreed to it separately will all look
reasonable in review.

### Task 4

`T-w03-4` — 2.5 h, Track B, testing. Build the naive handler first and replay
one event 100 times, recording every duplicate it produces. Then make it
effectively-once and replay again with `kill -9` injected at random
instruction boundaries, at least 20 of the 100 interrupted, including between
the commit and each external call. That last placement is the one that
matters: it is the window where the effect happened and the record of it did
not.

### Task 5

`T-w03-5` — 0.5 h, Track B, testing. Classify in writing every duplicate the
naive version produced and name the mechanism that would have absorbed each
one. Then write the sentence: why what was proved is effectively-once
processing under at-least-once delivery, and not the stronger claim.
Converting a wording error into an assessed answer is the review posture this
programme is trying to build.

### Task 6

`T-w03-6` — 1.5 h, Track C, theory, reinforcing A. Reading: `RES-04`.
Structured outputs as a validated retryable contract. A schema-forced
extraction that fails validation is a retry signal, not an exception. Raising
instead throws away the one place a generated response can be mechanically
refused.

### Task 7

`T-w03-7` — 2.0 h, Track C, building, reinforcing E. Build BOA-S0: structured
extraction over company websites into a Pydantic schema, retrying on
validation failure and recording a reason for every rejection. A rejection
with no recorded reason is indistinguishable from a site that was never
visited, and the rejection log is what tells you next week whether the schema
or the corpus is wrong.

### Task 8

`T-w03-8` — 0.9 h, Track E, business, reinforcing F. Research 6 prospects by
hand from public sources — the last manual batch, closing the 24 researched by
hand across the opening three weeks before BOA-S0 takes the volume.

### Task 9

`T-w03-9` — 1.0 h, Track E, business, reinforcing F. Write and send 5 cold
emails by hand. These five plus W02's four are what WATCH-1 will be reading a
fortnight from now, and it trips at 65.2% on the midpoint band. Trips, logs,
changes nothing.

### Task 10

`T-w03-10` — 0.2 h, Track E, business. Send 8 follow-ups, each carrying new
information. Four sends have matured by this Sunday: too few to read anything
from, and reading a trend into four is what the pre-announced thresholds exist
to prevent.

### Task 11

`T-w03-11` — 1.4 h, Track E, business, reinforcing F. The Stage-1 workflow
rehearsal: document a repetitive workflow at a public company entirely from
public information, using [the interview
template](../templates/discovery-interview.md), and write the discovery script
for the first real call. Load-bearing, and never cut. Zero calls is the
programme's modal outcome at 53.9%, which makes the simulated Stage-1 track
the *expected* path for at least one of W07's first workflow document, W08's
ROI calculation and W09's second — and this is the only place that path is
practised rather than improvised.

## Deliverables

- [ ] D-w03-1 — Replay harness and passing suite proving effectively-once outcomes under 100 killed replays, plus the written classification of every duplicate the naive version produced and the one-sentence statement of what was actually proved — at `agentplat/replay.py`, `tests/test_replay_100.py`, `docs/w03/duplicate-classification.md`
- [ ] D-w03-2 — BOA-S0 structured extractor with a Pydantic schema, retry-on-validation-failure, and recorded rejection reasons — at `agentplat/boa/extract.py`, `docs/w03/extraction-rejections.jsonl`
- [ ] D-w03-3 — Stage-1 workflow rehearsal document against a public company, plus the discovery script in the interview template — at `docs/w03/workflow-rehearsal.md`, `templates/discovery-interview.md`, `discovery-script.local.md`
- [ ] D-w03-4 — Combined failure report, partial tool failure and model timeout, with all five parts for each: detection, safe failure behaviour, recovery, logging, and a test proving the mitigation — and 6 prospects / 5 sends / 8 follow-ups logged — at `docs/w03/partial-failure-and-timeout-report.md`, `send-log.local.md`

## Acceptance criteria

- [ ] AC-w03-1a — after 100 killed replays: exactly one domain state transition, one recorded PR-intent, one recorded Notion-intent, one dedup row per key, and a terminal-correct final state (T-w03-2, T-w03-4)
- [ ] AC-w03-1b — the naive version's duplicate count is recorded and greater than zero, and the post-fix duplicate count is zero (T-w03-4, T-w03-5)
- [ ] AC-w03-1c — the dedup record and the state transition commit in the SAME transaction, with no application-level check-then-act, and no sleep or retry used anywhere to mask a race (T-w03-2)
- [ ] AC-w03-1d — the write-up names, for at least one external effect, a NATURAL KEY that made the create idempotent by construction rather than by bookkeeping (T-w03-5)
- [ ] AC-w03-2a — BOA-S0 extracts a valid schema instance from at least 8 of 10 real company sites, every rejection records a reason rather than failing silently, and a validation failure is retried against the schema instead of being raised as an exception (T-w03-7, T-w03-6)
- [ ] AC-w03-3a — the rehearsal document describes a workflow with named steps, an estimated frequency and an estimated time cost, and could be shown to a stranger as evidence of the documentation skill; the discovery script it produced is the one W04's call slot uses (T-w03-11)
- [ ] AC-w03-4a — both failure reports contain all five named sections and each proving test fails against the pre-mitigation code; the three dedup mechanisms are enumerated with the external effect each one covers; the retry budget is aggregate across layers and its truth table classifies every error as retryable, permanent or already-applied; and the week's funnel row is logged in SCOREBOARD — 6 prospects researched, 5 sends, 8 follow-ups — with `evidence_source` marked (T-w03-1, T-w03-3, T-w03-8, T-w03-9, T-w03-10)

## Stretch goal

Never financed from acceptance work, and reached only after the four
deliverables tick. Extend the fault injector to hit every boundary between the
commit and the last external call rather than a random sample, then enumerate
the distinct inconsistent states the naive version can reach. The count is the
output worth having: it sizes the space your unique constraint collapses to
one.

## Failure exercise

Two exercises, and they divide the week's failure surface cleanly. One is about
a step that half-succeeded; the other is about a step that may not have started.
Both bodies live in [the agent-failure set](../exercises/agent-failures.md), and
both reports are collected in D-w03-4.

### EX-FAIL-03 — partial tool failure

- **Detection.** One external write in a multi-write step succeeds while another fails, leaving recorded state and observable effects divergent. It is caught by comparing the recorded effect set against the observed effect set at step exit, which is why the step has to declare its effects up front rather than discover them.
- **Safe failure behaviour.** The step is not marked complete unless all of its recorded effects are confirmed. A partially applied step stays in flight instead of being reported as done — a false completion is the one state the resume path cannot repair, because it will never look at that step again.
- **Recovery.** Retry the step. Already-applied effects are absorbed by their natural keys or dedup rows rather than repeated, which is the return on T-w03-1's mapping. Where no natural key exists, reconcile by querying for the effect before re-attempting, and treat that path as residue.
- **Logging.** Record which effects were confirmed, which were not, and the classification of each failure as retryable, permanent or already-applied. That third class is the one people omit, and it is the one that decides whether a retry is safe.
- **Test proving the mitigation.** Inject a failure into the second of three writes, then assert exactly one of each effect exists after the retry and that the step's terminal state is correct. It fails against a version that marks the step complete after the first success.

### EX-FAIL-04 — model timeout

- **Detection.** The harness subprocess exceeds its wall-clock budget with no terminal event. A slow-but-alive run is told from a dead one by the absence of streamed events rather than by elapsed time, which cannot distinguish thinking from hanging.
- **Safe failure behaviour.** Kill the subprocess and treat the attempt as failed-retryable, never as a task failure. A timeout is a statement about the harness, not about the task, and recording it as a task failure poisons every later pass-rate the evaluation harness computes.
- **Recovery.** Start a new attempt carrying prior state rather than replaying: the work unit is nondeterministic, so the retry will do something different by construction. The retry budget is aggregate across layers, so three retries at three levels cannot quietly become twenty-seven calls.
- **Logging.** Record the timeout, the elapsed time, the last event received, and whether the aggregate budget was consumed. Tag the sample so it can be excluded from average task duration: a quota-distorted run left in that average corrupts a mandated harness metric.
- **Test proving the mitigation.** A stubbed harness that hangs triggers a kill inside the budget and exactly one retry, and a third timeout dead-letters instead of looping. It fails against a version with a per-layer retry count and no aggregate budget.

## Reflection

1. Which duplicate class was hardest to eliminate, and why?
2. Which effects became idempotent via a NATURAL KEY rather than via
   bookkeeping? Would you now prefer that everywhere, and what does it cost you
   when no natural key exists?
3. If an agent had written this handler from the original ticket, would any test
   you would plausibly have asked for have caught the defect? What does your
   answer imply about how you specify work from now on?

## Evidence

- `make demo-s1b-replay N=100` — this stage's demo command — with the output showing the naive duplicate count and the post-fix zero.
- Path to the duplicate classification write-up and its one-sentence statement.
- `make demo-boa-s0 URL=<company-url>`, plus the extractor and its rejection log.
- Path to the Stage-1 rehearsal document and the discovery script.
- Path to the combined failure report.

Log actual hours below as one line, planned first:
`Theory 2.5 / <actual> · Building 6.0 / <actual> · Testing 3.0 / <actual> ·
Discovery 3.5 / <actual>`. Canon already suspects this week of being underpriced, so
the gap between plan and actual is the most informative figure M1's
recalibration will read. Funnel counts go to
[the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W03" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- Effectively-once outcomes proved under 100 killed replays — 35
- Every duplicate the naive version produced is classified in writing — 15
- BOA-S0 extracts from at least 8 of 10 real sites — 15
- The Stage-1 rehearsal document and discovery script exist — 15
- Both failure reports carry all five named parts — 10
- 5 sends and 8 follow-ups logged per touch — 10
