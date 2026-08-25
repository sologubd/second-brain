# Week 04 — Verification, review and the human approval gate

## Outcome

By Sunday the platform opens a real pull request that a verification gate, an
automated review and a human approval gate all had to pass, and nothing reaches
a human inbox without an audit record.

## Time budget

- Theory: 2.5 h
- Building: 6.0 h
- Testing/evaluation: 3.0 h
- Customer discovery: 3.5 h

The densest week in the programme: two subsystems, two failure exercises,
architecture review AR-01, the M1 retrospective and the first discovery-call
slot. Ceilings are EUR 0.00 of metered spend and 45 agent runs, the highest run
count so far. These are *planned* figures: canon measures a week in work, not
calendar time, so one costing over 15.0 h spans extra days rather than losing
scope. T-w04-4 is probably underpriced — two exercises, five named parts each,
two fixtures to build. Log what it costs, not what it is priced at.

Compressed week, 8.0 h: T-w04-2, T-w04-1, T-w04-10, T-w04-12, T-w04-13 and
T-w04-14 — then slip the calendar rather than doubling up. Discovery runs at
3.0 h, above its floor and deliberately so: M1 reads the funnel this week, and a
funnel thinned to the floor makes the retrospective read noise. The retrospective
itself is never cut, being the programme's only self-correction instrument.
BOA-S1, AR-01, T-w04-4 and T-w04-11 defer to [week 05](week-05.md). D-w04-1 and
D-m01-4 tick. D-w04-2 and D-w04-3 carry whole, and D-w04-4 carries its two
five-part reports with AC-w04-4a while its funnel counts land. DONE-COMPRESSED,
not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| automated PR generation | A | P0 | T-w04-2 → D-w04-1 |
| automated review | A | P0 | T-w04-2's single-axis review → D-w04-3 |
| human approval | A | P0 | T-w04-1, T-w04-2, and BOA-S1's gate in T-w04-3 |
| skills | A | P1 | the stretch goal — a first taste; the capability is claimed by S9 |
| agent permissions | A | P0 | T-w04-9 resolves the per-run policy per tool |
| trust boundaries | D | P0 | T-w04-8; canon carries it as C-079, privilege boundaries |
| least privilege | D | P0 | T-w04-9 → D-w04-2, per-tool profiles over a union token |
| approval gates | D | P0 | T-w04-8's placement audit → D-w04-1 |
| insecure tool permissions | D | P0 | T-w04-9 against defect class DC-14 |
| Gateway | B | earn it | T-w04-5 → D-w04-3 |
| Service Layer | B | earn it | T-w04-5 → D-w04-3 |
| reviewing generated code | B | competency CM-17 | T-w04-6 → D-w04-3 |
| outreach | E | P0 | T-w04-12 and T-w04-13 → D-w04-4 |
| discovery calls | E | P0 | T-w04-14 → D-w04-4 |

Three rows carry no P-priority: canon holds no concept row for them. Gateway and
Service Layer are pattern-triage entries verdicted *earn it*; reviewing
generated code is a competency.

`skills` was contested and is now settled. S2 claimed the capability while the
stretch goal held the work — and stretch goals sit outside the 15 hours and
vanish entirely at 8 h, so skipping the stretch would have made S2's capability
list false. Canon moved skills to S9, where the brief already pairs it with
agent roles, and repointed the mastery check to `D-m06-4`. SKILL.md packaging
stays here as a genuine stretch: a first taste, not the capability claim.

Concept reasoning lives in [Track A](../tracks/agentic-engineering.md) — the
week's largest — [Track B](../tracks/system-design.md),
[Track D](../tracks/ai-security.md) and [Track E](../tracks/consulting.md).
Stages belong to
[the platform](../projects/engineering-agent-platform.md) and
[the business operations agent](../projects/business-operations-agent.md), sends
to [outreach](../business/outreach.md). This file owns tasks, hours and
acceptance.

## Tasks

### Task 1

`T-w04-1` — 1.5 h, Track A, theory, reinforcing D. Reading: `RES-03`.
Verification and human approval gates as *architectural* controls. Locate the
gate at the irreversible or high-impact state change, and require the payload
to render the literal proposed tool call plus its evidence, never a
paraphrase. A summary is a claim about a call; the call is what executes.

### Task 2

`T-w04-2` — 2.5 h, Track A, building, reinforcing B. Build S2: verification
gate (tests, typecheck, lint) → automated review → human approval → GitHub PR
→ CI integration. The approval payload renders the literal diff and the
literal proposed call, and CI status reports back into the task record.

### Task 3

`T-w04-3` — 1.5 h, Track A, building, reinforcing D and E. Build BOA-S1:
draft-only outreach on top of BOA-S0's extraction, with an approval gate and
an append-only audit trail. This is the week you become your own first
customer: the agent drafts, you send. It never sends autonomously, which is
both the safe design and the better exercise — an agent that cannot send
forces the payload to carry everything you need to decide.

### Task 4

`T-w04-4` — 1.0 h, Track A, testing. Run the flaky-test and
unrelated-CI-failure exercises against S2 and record how the gate behaved in
each, including where it did worse than expected.

### Task 5

`T-w04-5` — 0.5 h, Track B, theory. Reading: `RES-15`. Gateway as the
anti-corruption layer, Service Layer as the home of the transaction boundary.
Name where retry policy, rate limiting and idempotency keys belong. An agent
writing a GitHub call inline re-derives those semantics per call site,
differently wrong each time.

### Task 6

`T-w04-6` — 1.0 h, Track B, building, reinforcing A. Write the versioned
generated-code review checklist around the four questions — what happens on
the second call; what happens if the process dies between these two
statements; what happens if two of these run at once; what does this assume
about the external system that is stated nowhere — then apply it to S2's own
diff.

### Task 7

`T-w04-7` — 1.0 h, Track B, testing. Architecture review AR-01,
self-inspection of the platform through S2 against the 14 defect classes,
producing an ADR from [the template](../templates/adr-template.md). The
classes and their detection questions live in [the review exercise
set](../exercises/architecture-reviews.md).

### Task 8

`T-w04-8` — 0.5 h, Track D, theory, reinforcing A. Reading: `RES-11`. Trust
boundaries and least-agency: which platform steps genuinely need autonomy, and
where an approval gate must sit. The failure shape is DC-14: an agent holding
the union of every permission its steps ever needed.

### Task 9

`T-w04-9` — 1.0 h, Track D, building, reinforcing A. Give the runner a
per-tool least-privilege profile and an audit record per tool call: tool name,
arguments, and the profile that permitted it.

### Task 10

`T-w04-10` — 1.0 h, Track P, testing. The M1 retrospective in [the month
file](../months/month-01.md): all ten questions RQ-01 through RQ-10, plus
RQ-11, the mandated canon delta. M01's delta is the hour recalibration: four
weeks of logged actuals against plan, per bucket, rewriting weeks 05 through
12 and drawing on the cut list above a 15% overrun in any bucket. The six-step
loop lives at [HOW-TO-EDIT](../HOW-TO-EDIT.md#the-control-loop); run it, do
not restate it.

### Task 11

`T-w04-11` — 0.5 h, Track E, business, reinforcing F. Research 10 prospects
using BOA-S0 assistance. The 0.5 h against W01's 1.5 h for the same count is
BOA-S0's whole return, measured here rather than assumed.

### Task 12

`T-w04-12` — 1.2 h, Track E, business, reinforcing F. Write and send 6
hand-written cold emails, the last hand-written sends in the programme.
WATCH-1 trips this Sunday if 9 matured sends have produced no reply — 65.2%
likely at the band midpoint, 87.4% at its floor. Log it to [the
scoreboard](../SCOREBOARD.md) and change nothing: it is a checkpoint
pre-announced in [phase 01](../phases/phase-01-foundations.md#checkpoints),
not a signal.

### Task 13

`T-w04-13` — 0.3 h, Track E, business. Send 9 follow-ups, each adding
information. One that only checks in spends goodwill and buys nothing.

### Task 14

`T-w04-14` — 1.5 h, Track E, business, reinforcing F. The first discovery-call
slot, budgeted at 1.50 h against the 1.75 h all-in rate, because the script is
fresh from W03's rehearsal and sits in [the interview
template](../templates/discovery-interview.md). Expect 0 or 1 calls. The
programme plans for 1 across all 52 sends, but **the modal outcome there is no
call at all, 53.9% at the band midpoint** — and only 9 of those sends have
matured by Sunday. If no call happens the 1.5 h returns as slack and is logged
as slack, not silently re-spent.

## Deliverables

- [ ] D-w04-1 — S2 pipeline opening a real PR against your own repository; done includes the human approval gate rendering the literal diff and literal proposed call, and CI integration reporting back into the task record — at `agentplat/gate/`, `docs/w04/s2-evidence.md`
- [ ] D-w04-2 — BOA-S1 draft-only outreach with an approval gate, a per-tool least-privilege profile and an append-only audit trail — at `agentplat/boa/outreach.py`, `policy/tool-profiles.v1.yaml`, `docs/w04/audit-log.jsonl`
- [ ] D-w04-3 — Architecture review AR-01 (self): an ADR against the 14 defect classes, conducted with the versioned generated-code review checklist delivered alongside it — at `docs/adr/adr-001-arch-review-1.md`, `docs/w04/generated-code-checklist.v1.md`
- [ ] D-w04-4 — Combined failure report, flaky test and unrelated CI failure, with all five parts for each, plus 10 prospects / 6 sends / 9 follow-ups / 0–1 calls logged — at `docs/w04/flaky-and-unrelated-ci-report.md`, `send-log.local.md`

## Acceptance criteria

- [ ] AC-w04-1a — a task moves from task file to merged-ready PR with zero manual steps other than clicking approve, and the PR body links the verification and review outputs (T-w04-2)
- [ ] AC-w04-1b — the approval payload contains the literal diff and the literal proposed tool call; an automated test proves that changing the underlying call without changing the summary causes the approval to be rejected (T-w04-1, T-w04-2)
- [ ] AC-w04-1c — re-running the same task does not open a second PR; the branch name is the natural key (T-w04-2)
- [ ] AC-w04-2a — BOA-S1 cannot send: every outbound draft requires an approval record, and an attempt to bypass it is refused and logged (T-w04-3, T-w04-9)
- [ ] AC-w04-2b — every tool call the runner makes appears in the audit log with the tool name, arguments and the profile that permitted it (T-w04-9, T-w04-8)
- [ ] AC-w04-3a — the review checklist is versioned, has at least four question categories, and its application to S2's own diff produced at least one recorded finding (T-w04-6, T-w04-5)
- [ ] AC-w04-3b — the ADR names at least three of the 14 defect classes as present or absent with evidence, not as a checklist tick (T-w04-7)
- [ ] AC-w04-4a — both failure reports contain all five named sections and each proving test fails against the pre-mitigation code; the flaky-test report states how the gate distinguished flakiness from a real failure, or records that it could not; and the week's funnel rows are logged under SM-15 to SM-18 in the scoreboard's weekly row format — 10 prospects researched, 6 sends, 9 follow-ups, and calls booked recorded as 0 or 1, each line carrying `evidence_source` (T-w04-4, T-w04-11, T-w04-12, T-w04-13, T-w04-14)
- [ ] AC-w04-4b — the M1 delta exists as an edit to `canon/canon.yaml` with `meta.version` bumped, and states the per-bucket variance between logged and planned hours for weeks 01 through 04 (T-w04-10)

## Stretch goal

Outside the 15 hours. Package `how to run tests` and `how to
open a PR` as SKILL.md files, then prove S2 behaves identically when those
procedures are removed from the prompt entirely. Run it only once the four
deliverables are ticked; it is never financed from acceptance work.

## Failure exercise

Both exercises are about an agent's behaviour when the signal it depends on is
untrustworthy. Full bodies live in
[the agent-failure set](../exercises/agent-failures.md); the report is D-w04-4.

### EX-FAIL-05 — failing flaky test

- **Detection.** A test fails and then passes on an unchanged tree. The gate re-runs a failing test N times on the same commit before classifying it, so the verdict rests on a sequence rather than one observation.
- **Safe failure behaviour.** Do not auto-approve past a flaky failure, and do not let the agent "fix" it by weakening the assertion. The second is the characteristic generated-code response and is worse than the failure: it turns a noisy signal silent.
- **Recovery.** Classify as flaky, quarantine the test with a recorded reason, escalate to human review. The PR proceeds only with the quarantine visible in the approval payload.
- **Logging.** Record the test id, the pass/fail sequence across re-runs, and the commit sha, so flakiness is a tracked property of the test rather than an anecdote.
- **Test proving the mitigation.** A deliberately flaky fixture test is classified as flaky rather than failing, and an agent attempt to modify its assertion is rejected by the gate. It fails against a version that treats one failure as a verdict.

### EX-FAIL-06 — CI failure unrelated to the change

- **Detection.** CI fails on a job whose inputs the diff does not touch, found by intersecting the changed file set with each job's declared inputs.
- **Safe failure behaviour.** Do not attribute an unrelated failure to the change, and do not let the agent widen the diff trying to fix it. Scope creep against a red build is how a two-file change becomes a twenty-file one.
- **Recovery.** Mark the job unrelated-failing, surface it separately in the approval payload, and continue the task's own verification independently.
- **Logging.** Record the job name, the changed file set, its declared inputs and the intersection result, so misattribution can be audited later.
- **Test proving the mitigation.** A fixture PR touching one module, with a deliberately broken unrelated job, is classified unrelated while the task's own verification still reports independently. It fails against a version that treats any red CI as the task's failure.

## Reflection

1. Your approval gate renders the literal proposed call. What can an attacker who
   influences the *rendered payload* still achieve, and what would detect it?
2. Which S2 stage is a workflow step and which is an agent step — and did
   building it change the classification you wrote in W01? If it did, what did
   you originally get wrong?
3. The review checklist produced a finding on S2's own diff. Was that a finding
   your ordinary review instincts would have produced unaided?

## Evidence

- `make demo-s2 TASK=tasks/example.md`, and a link to the first PR it opened end to end.
- The approval-payload test proving a changed call is rejected.
- `make demo-boa-s1 PROSPECT=<id>`, and a path to the BOA-S1 audit trail sample.
- Path to the review checklist v1 and the AR-01 ADR.
- Path to the combined failure report.
- Path to the M1 canon delta and the bumped `meta.version`.

Log actual hours below as one line, planned first:
`Theory 2.5 / <actual> · Building 6.0 / <actual> · Testing 3.0 / <actual> ·
Discovery 3.5 / <actual>`. The M1 recalibration compares these regions per
bucket across weeks 01 through 04, so an unlogged week cannot be corrected
against. Funnel counts go to [the scoreboard](../SCOREBOARD.md), not here.

<!-- user:actuals key="W04" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- S2 runs end to end, task file to opened PR — 30
- The approval gate shows the literal call, proved by test — 15
- BOA-S1 refuses to send without an approval record — 15
- The review checklist is versioned and the AR-01 ADR written — 15
- Both failure reports carry all five named parts — 10
- The M1 delta is written and canon edited — 15
