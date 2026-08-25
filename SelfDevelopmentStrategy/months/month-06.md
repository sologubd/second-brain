# Month 06 — Authorization a reviewer can read

## Outcome

Authorization on the knowledge agent is expressed as policy rather than as
scattered conditionals, and I can state which policy model each surface needs
and why.

The second clause is the harder one. Building role checks is a morning's work;
being able to defend, per surface, why roles are enough there and why one place
genuinely needs a context-dependent rule is the part that survives a design
review.

## Deliverables

- [ ] `D-m06-1` — Role-based access control across the knowledge agent's authorization surface, with attribute-based rules added only where an exercise genuinely needs a condition that depends on context, such as a value threshold.
- [ ] `D-m06-2` — The enforcement point and the decision point separated, implemented as a hand-written pre-execution check function, together with a written account of what standing up a real engine would buy and why that purchase is disproportionate here.
- [ ] `D-m06-3` — Track E scoping, proposals and pricing, landing as a productized offer with fixed scope and a stated payback period.
- [ ] `D-m06-4` — Agent roles and skills at `S9`, plus failure reporting.

Skills sit here rather than at `S2` deliberately. Canon moved them at G5 after
noticing that week 04 had put the packaging work in a stretch goal, and a
stretch goal is outside the fifteen hours and gone entirely under the reduced
week — so a stage claiming skills as a capability was claiming something a
permitted skip would erase. `S9` already pairs roles with skills, which is where
the brief pairs them too.

## Funnel targets

Deferred to the M2 delta, as for every calendar month. Canon carries a note in
place of numbers rather than a figure someone would later have to defend.

What does change this month is what the funnel is *for*. Through the twelve
detailed weeks it was a volume instrument: sends, follow-ups, matured touches.
`D-m06-3` prices an offer, and pricing needs qualification rather than reach —
fewer conversations that reach a budget question beat more that do not. The
counts still go to [the scoreboard](../SCOREBOARD.md) with `evidence_source`
recorded as real or simulated, and a priced offer built on simulated discovery
is a priced offer nobody has agreed to.

## Stages entered

`SKA-S2` and `S9`.

`SKA-S2` is the knowledge agent's tenant-isolation and policy-authorization
stage, and its exit condition is word-for-word what the two headline
deliverables above produce: role-based access enforced through one
pre-execution check, with attribute-based rules only where a context-dependent
condition genuinely needs them. Its window opened at month 04 beside tenant
isolation and closes here. `S9` has been running since month 05 and closes at
month 08, so both stages named this month span more than one — which is what
the field is for rather than an irregularity in it.

Entry and exit conditions, demo commands and ceilings belong to
[the knowledge agent](../projects/secure-knowledge-agent.md) and
[the engineering platform](../projects/engineering-agent-platform.md).

## Failure exercises

One, and it tests the thing this month builds rather than something adjacent to
it. The body lives in
[the agent-failure set](../exercises/agent-failures.md).

### `EXT-05` — authorization bypass through a policy gap

- **Detection.** A request reaches a resource that no role grants, not because a rule was written wrongly but because no rule was written at all. The check function has a hole where it should have had a floor.
- **Safe failure behaviour.** Refuse by default. An action matching no policy is denied, never permitted — which is the difference between a check function and a filter, and it has to be the structural default rather than a final `else`.
- **Recovery.** Add the missing rule, then add a test that asserts the refusal path itself. A test that only exercises the new permission proves the fix and leaves the class alive.
- **Logging.** Every decision writes down who asked, what was asked for, which rule answered — or that nothing did — and the outcome. The nothing-matched case deserves the loudest entry, because it is invisible in a log that records only refusals.
- **Test proving the mitigation.** A fuzz across action and role pairs finds zero actions permitted without an explicit allow. It has to fail against the pre-mitigation check, or the gap it claims to close was never open.

## Retrospective

All ten, answered from what the month produced rather than from how it felt.
Each carries a clause naming where the evidence for an answer is likely to sit.

1. What can I now build that I could not build 30 days ago? Authorization is the answer only if it is legible to someone else.
2. Which concept remains theoretical? Policy engines, by design — canon stands none up.
3. What broke in real usage? Look at the refusal path, not the allow path.
4. What did agents repeatedly fail at? `S9`'s ADR lane is four months old by now and has a record.
5. What should become a reusable skill? This is the month `D-m06-4` makes that question load-bearing.
6. What should become a deterministic tool instead of an LLM decision? An authorization decision is the canonical case.
7. Where did human approval prove necessary? Compare against where policy made approval unnecessary.
8. What business problems appeared repeatedly? `D-m06-3` prices whichever of them recurs.
9. What should I stop learning? Answered against the low-ROI table, where policy engines already sit with a verdict — that row is the shape any new entry has to take.
10. What should I double down on? The follow-up does the work — which of the last four weeks' deliverables taught you something you did not already know? Zero of four for any track forces a re-pitch in the delta.

`RQ-11` turns one of those answers into a canon edit. Run `make delta MONTH=06`,
fill the stub, edit canon, bump `meta.version`, regenerate and re-check.

## Mandated delta

**Type:** `competency_reassessment`.

Canon's procedure, verbatim: re-rate all four competency columns against
delivered evidence ids ahead of the M6 checkpoint. Any competency whose m6
target is unmet with no evidence id is either re-planned or downgraded, never
silently held.

Seventeen rows, four columns each, and the rule that governs them is that no
cell may be justified by study. The rows most likely to move down are the ones
whose evidence depends on other people: customer discovery from a cold start,
and opportunity valuation, which canon already calls the slowest-moving row in
the matrix precisely because it is gated on an input this programme cannot
manufacture. Downgrading those is the delta working, not the plan failing.

## Checkpoint

`CP-M6` closes here, the second of the four career checkpoints. The question is
canon's, and worth answering as asked rather than as summarised:

> Can I build production-grade AI workflows with evals, security and
> observability?

Seven deliverable ids answer it, in canon's order: `D-m02-1`, `D-w10-1`,
`D-w11-2`, `D-m03-1`, `D-m04-1`, `D-m05-2`, `D-m06-1`. Both the question and
the list are held in
[the portfolio file](../reference/portfolio.md#the-table).

They are spread across the programme rather than bunched at the gate, which is
the point of naming them a month early. Measured retrieval quality against a
frozen label set and the pre-filter proof came at month 02; the three-tier gate
with its justified statistical threshold and the first measured attack success
rates came from weeks 10 and 11; traces carrying cost and quota attribution and
the cross-harness comparison from months 03 and 04; the memory-poisoning
chapter from month 05. Only the last of the seven is produced here.
