# Month 04 — The Notion pipeline, and the first real multi-write surface

## Outcome

The platform ingests a Notion task and produces a reviewed PR, and the same task
run through two different harnesses can be compared without the comparison
secretly being about the models.

This is phase 2, and it is one month long. It opens with the workflow the brief
names first and the twelve detailed week-files deliberately did not build. The
reason is dependency rather than preference: that pipeline is twelve steps long
and most of them rest on machinery months 01 through 03 paid for — durable
state, the verification gate, the approval gate. Shipped first, it would have
been an ingestion endpoint with nothing behind it.

## Deliverables

- [ ] `D-m04-1` — `S8`: Notion ingestion, requirement extraction and ambiguity detection, completing the brief's first-listed flagship pipeline; plus the cross-harness comparison, model routing and the metered fallback path kept live behind the same adapter interface.
- [ ] `D-m04-2` — The outbox and its separate relay process, fault-injected at every boundary between commit and last external call — the external-effects surface the single-user platform did not have until GitHub, Notion and Sentry were all written to from one task.
- [ ] `D-m04-3` — Task-lifecycle teardown as a saga, with failures injected into the compensations themselves, plus a one-page classification defending which platform surfaces the outbox fits and which need a saga instead.
- [ ] `D-m04-4` — `S2b`: the five-axis automated multi-axis review capability, and knowledge-agent tenant isolation plus secrets handling.

Seven residual topics are homed here and six sit inside those deliverables: the
outbox build and the saga re-anchored onto task teardown, the automated review,
model fallbacks and routing, then tenant isolation with secrets handling. The
seventh is Track E scoping, which has no engineering deliverable at all — so it
gets real hours here or an explicit deferral in the delta below, never a quiet
hold.

## Funnel targets

Canon carries no volumes for this month and flags the row `derived: False`.
Months 01 through 03 derived their targets by summing the week-files beneath
them; from here there are no week-files, and the numbers come instead from the
M2 recalibration against measured reply and per-touch rates.

That is a deferral with a reason rather than a gap: a count written here would
guess ahead of a measurement already scheduled to arrive, and would then have to
be defended against it. Whatever M2 sets, counts land in
[the scoreboard](../SCOREBOARD.md) with `evidence_source` on every artifact.

## Stages entered

Two: `S8` on the platform and `S2b`, the multi-axis review that extends `S2`.
Both are defined — entry, exit, demo command, cost and quota ceilings — in
[the platform file](../projects/engineering-agent-platform.md), and the
knowledge agent's authorization stage runs alongside them from
[its own file](../projects/secure-knowledge-agent.md).

`S8` is where the metered budget is first genuinely spent, and where the
cross-harness comparison lives — which kept W10 inside its deliverable cap.
`S2b` is the smaller stage and the sharper requirement: a pull request comes
back with five independently scored, separately cited outputs, one per axis, and
a single aggregate verdict fails the gate. The rubric was written by hand at
W12; this month automates it.

## Failure exercises

Two, and both come from the extended set rather than the canonical fourteen —
months draw from there precisely so each of the fourteen keeps its single week.
The bodies are in [the agent-failure set](../exercises/agent-failures.md); these
two report through `D-m04-2` and `D-m04-3`.

### `EXT-01` — crash between commit and external effect

- **Detection.** A fault injector takes the process down at each boundary in turn, from the local commit through to the final external call — every one of them, not a sample — recording the inconsistency observed at each.
- **Safe failure behaviour.** The outbox row is written inside the same transaction as the state transition, so a rolled-back transaction can leave no pending effect behind it.
- **Recovery.** Pending effects go out through a separate relay, at-least-once, with handlers that stay correct if the same effect arrives twice. Correctness under redelivery is the property being bought, because a relay that fires exactly once is not on offer.
- **Logging.** Record the kill point, the inconsistency observed there, and commit-to-effect latency at p50 and p99 — the pair that says whether the relay is a mechanism or a queue quietly growing.
- **Test proving the mitigation.** After the outbox, no kill point produces a lost effect or a state-and-effect divergence, and asserting that no outbox row survives a rolled-back transaction proves the shared transaction. It fails against the naive commit-then-call version.

### `EXT-02` — compensation that fails

- **Detection.** A compensation inside the task-lifecycle teardown saga fails, and fails permanently rather than transiently.
- **Safe failure behaviour.** Every compensation is independently idempotent, and the suite invokes each twice to prove it rather than assert it. They run in a defined order with the lease released last, and that ordering is defended in writing.
- **Recovery.** A permanently failing compensation reaches a defined terminal state plus an operator-visible alert — never a hang, never a silent swallow. At least one effect must be named that cannot be compensated at all, with a statement of what happens instead.
- **Logging.** Record, honestly, which compensations were non-idempotent on first implementation; the states reachable after one fails; and the non-compensable effects found.
- **Test proving the mitigation.** Double-invoked compensations produce no second effect, and a permanently failing one lands in a defined terminal state. The surface-by-surface classification is defended in that same document.

## Retrospective

All ten, answered at month end rather than at a week-file boundary: this is the
first month with no detailed weeks beneath it.

1. What can I now build that I could not build 30 days ago? The Notion demo command, run in front of someone.
2. Which concept remains theoretical? Saga ordering, most likely, since only teardown exercised it.
3. What broke in real usage? Every kill point the fault injector found is a row here.
4. What did agents repeatedly fail at? Read it against whichever review axis scored lowest.
5. What should become a reusable skill? Whatever the second harness forced you to redo by hand.
6. What should become a deterministic tool instead of an LLM decision? Ambiguity detection; part of it is a rule.
7. Where did human approval prove necessary? The Notion path added irreversible actions — say which earned a gate.
8. What business problems appeared repeatedly? Scoping conversations, if scoping got its hours.
9. What should I stop learning? Against the low-ROI table, with a verdict for anything not already a row.
10. What should I double down on? Canon pairs it with a follow-up about which deliverables taught something genuinely new; a track that taught nothing earns a delta re-pitching it.

`RQ-11` is what makes the difference between a finding and a change. Run
`make delta MONTH=04`, edit canon, raise `meta.version`, regenerate, re-check.

## Mandated delta

**Type:** `scope_recalibration`.

Re-cost months 05 through 12 against three months of logged actuals. Track E
scoping, pricing and the subcontracting side-quest are homed across months 04 to
07 and must be given real hours here or explicitly deferred.

Three deltas have fired by now, each correcting one thing: M1 the hours, M2 the
funnel, M3 the volatile facts. This one differs in kind — it is the first to
re-cost work with no week-file underneath it, so it re-costs estimates rather
than corrects measurements. The instruction that matters most is the second
sentence. Business work carrying no engineering deliverable is the easiest thing
in a plan to carry forward untouched, and canon closes that route: hours, or an
explicit deferral, with nothing in between.

## Checkpoint

No career checkpoint closes month 04 — `checkpoint_refs` is empty. `CP-M6` is two
months out, and this month contributes exactly one of its seven evidence ids:
`D-m04-1`.

The heading renders because the schema fixes eight sections per month file even
while its own rules describe this one as conditional. Both cannot operate; the
checker decides which does, and the space carries a forward reference rather
than standing empty.
