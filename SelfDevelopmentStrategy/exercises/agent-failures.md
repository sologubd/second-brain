# Agent failure exercises

## How to use these

Nineteen exercises whose purpose is to make an agent fail on purpose, under
conditions you chose, while you are watching. Fourteen are the canonical set, one
per named failure mode, spread across the twelve week files. Five extend it into
the months, where the platform grows surfaces the weeks did not have.

Most curricula omit this, because a success demonstrates well and a failure does
not. The result is engineers who can build an agent that works and cannot say
what it does when the ticket is vague, the tool lies, the test is flaky, the
document is a year old, or the process dies halfway through. All five happen
weekly in production and none happens in a demo.

Every body carries all five parts, named: **detection**, **safe failure
behaviour**, **recovery**, **logging**, and **a test proving the mitigation**.
Seventy cells, none thin. The insistence is mechanical too: the schema checker
looks for the five names once across the whole section, so nineteen bodies would
satisfy it if one were complete. Only a reader catches a summarised body.

One rule turns a report into evidence: **the proving test must go red against the
code as it was before the fix.** Run it on the parent commit first. If it does
not fail there, you have not reproduced the failure.

Weekly hours live in [weeks/](../weeks/week-04.md); the offensive versions of the
security entries in [the attack suites](ai-security.md); the target systems in
[the platform](../projects/engineering-agent-platform.md),
[retrieval](../projects/secure-knowledge-agent.md) and
[operations](../projects/business-operations-agent.md).

## Exercises

### EX-FAIL-01 — ambiguous ticket (W01)

Rungs: `DL-3` break.

#### Objective

Make the runner decline an underspecified task rather than emit a confident diff
against an unwritten requirement.

#### Task

- **Detection.** Score the task file before dispatch on three things: a named file or module, a stated done-condition, and one assertion a machine could evaluate. Where any is absent it is the score that fails, not the task.
- **Safe failure behaviour.** Decline to dispatch. Letting the model fill the gap yields something plausible aimed at an unstated requirement — the costly outcome, because it arrives dressed as success and surfaces only at review, or later.
- **Recovery.** Say which of the three were missing — all of them, not the first one found — and park the task where a person sees it. Never invent the absent criterion: an obvious guess that is wrong beats a refusal only until somebody trusts it.
- **Logging.** Keep the task id, the missing element, and the submitted text unedited. Vagueness is a pattern rather than an incident, and counting it weekly turns a complaint into something actionable.
- **Test proving the mitigation.** One fixture without a done-condition is turned down before any model call; a complete one dispatches. Both run against the original runner, which dispatched either way, and the refusal assertion breaks there.

#### Constraints

- The score runs pre-dispatch, so a refusal costs zero tokens.
- No default criterion may be supplied, not even a conservative one.

#### Deliverable

`D-w01-4` — **test suite** (`DT-06`): pre-dispatch score, both fixtures, five-part report.

#### Acceptance criteria

- A task missing any of the 3 elements is declined, with 0 model calls.
- The refusal names every element it found missing — 1, 2 or all 3 — and names nothing else.
- The suite fails against the pre-mitigation runner.

#### Metrics

- Failure rate: tasks declined divided by tasks submitted.
- Token usage avoided: tokens not spent on declined tasks, against mean dispatched cost.

#### Reflection questions

1. Which of your own tickets failed the score, and was it right about them?
2. Describe a task passing all three checks that is still ambiguous.

### EX-FAIL-02 — agent context loss after restart (W02)

Rungs: `DL-3` break, `DL-7` operate.

#### Objective

Prove a restarted run continues from what was durably written, never from what a
dead process believed it had done.

#### Task

- **Detection.** On resume, hold the stored pointer against the observable world. Two mismatches are possible and both are defects: a step marked unfinished whose effect exists, and one marked finished whose effect is missing.
- **Safe failure behaviour.** Continue from the durable pointer and nothing else. Where pointer and world disagree, stop — a guess repeats an external effect or skips one, and afterwards neither is visible.
- **Recovery.** Re-run from the stored pointer. The transaction recording completion is the one that produced the effect, so repeating is harmless by design rather than by discipline — the only kind that holds at four in the morning.
- **Logging.** Keep the pointer at kill time and at resume, and the wall-clock distance between them. That distance is how long the work sat orphaned, and without it the question has only an anecdote as an answer.
- **Test proving the mitigation.** Kill at each boundary in turn; assert the resumed run lands where an undisturbed one lands and that nothing happened twice. Point it at the build tracking progress in memory and it breaks.

#### Constraints

- Progress may not live in process memory, nor in a cache only usually consistent with it.
- Every step boundary is killed in turn, never a sample.

#### Deliverable

`D-w02-4` — **test suite** (`DT-06`): boundary-kill harness, five-part report.

#### Acceptance criteria

- Killing at 100% of boundaries yields the undisturbed terminal state.
- 0 effects occur twice across the sweep.
- The suite fails against the in-memory build.

#### Metrics

- Failure rate: divergent terminal states divided by kill points exercised.
- Latency: kill-to-resume distance, p50 and p95.

#### Reflection questions

1. Which step's effect is hardest to observe, and how would you learn its pointer was wrong?
2. If a mismatch woke you weekly, would you change the stop or the cause?

### EX-FAIL-03 — partial tool failure (W03)

Rungs: `DL-3` break.

#### Objective

Handle the step that half-worked: one write landed, one did not, and stored state
now describes a world that never existed.

#### Task

- **Detection.** At step exit, hold the effects the step claims against those you can observe. A step claiming three writes but confirming two has not finished, whatever its return value reported.
- **Safe failure behaviour.** Withhold completion until every claimed effect is confirmed; a half-applied step stays in flight. The pull toward reporting success on the first confirmation is strong precisely because the happy path never separates the two.
- **Recovery.** Re-run the whole step. Effects already present are swallowed by natural keys or dedup rows. Where an effect has no natural key you must query before re-attempting — read that as a missing key, not a solution.
- **Logging.** Keep the confirmed set, the unconfirmed set, and a verdict per failure: retryable, permanent, or already-applied. That third verdict is the one most implementations lack and the one deciding whether repeating is safe.
- **Test proving the mitigation.** Break the second of three writes and assert that after retry exactly one of each effect exists and the terminal state is right. The build completing on first success fails immediately.

#### Constraints

- Effects are confirmed by observation, never by trusting a return value.
- The three verdicts are explicit in code, not inferred from exception classes.

#### Deliverable

`D-w03-4` — **test suite** (`DT-06`): partial-failure injector, five-part report.

#### Acceptance criteria

- After retry exactly 1 of each effect exists, over at least 3 injection points.
- Every failure carries exactly 1 of the 3 verdicts.
- The suite fails against the complete-on-first-success build.

#### Metrics

- Failure rate: steps left in flight divided by steps injected.
- Success rate: retried steps landing correctly divided by retries.

#### Reflection questions

1. Which effect here has no natural key, and what would giving it one cost?
2. Which parts of the retry path must themselves be repeatable?

### EX-FAIL-04 — model timeout (W03)

Rungs: `DL-3` break, `DL-7` operate.

#### Objective

Tell a stalled harness from a hard task, and stop nesting turning three retries
into twenty-seven calls.

#### Task

- **Detection.** The subprocess passes its wall-clock allowance with no terminal event. Separate a hang from a slow-but-living run by whether events still arrive, since on a clock alone a long task and a dead one are identical.
- **Safe failure behaviour.** Kill it and mark the attempt failed-but-retryable rather than marking the task failed. A timeout describes your harness, not the work; conflating them dead-letters tasks that were never wrong.
- **Recovery.** Open a fresh attempt carrying prior state. Deliberately not a replay: the unit is nondeterministic and the new attempt will diverge. Hold one retry allowance across every layer so nesting cannot multiply it.
- **Logging.** Keep elapsed time, the final event seen, and whether the shared allowance was spent. Mark the sample excludable — a quota-stalled run distorts mean duration, retry rate and cost per task, three harness metrics at once.
- **Test proving the mitigation.** A stub that hangs is killed inside the allowance and retried once; a third timeout dead-letters instead of looping. Against per-layer counting the call-count assertion breaks.

#### Constraints

- The retry allowance is shared across layers, and the sharing is asserted rather than documented.
- Timeout classification may not take elapsed time as its only input.

#### Deliverable

`D-w03-4` — **test suite** (`DT-06`): hanging stub, shared-allowance assertion, five-part report.

#### Acceptance criteria

- A hanging harness is killed inside its allowance with at most 1 retry.
- A 3rd timeout dead-letters, issuing 0 further calls.
- The suite fails against the per-layer build.

#### Metrics

- Cost: calls issued per failing task, before and after the shared allowance.
- Latency: stall onset to kill, p50 and p95.

#### Reflection questions

1. Your detector reads silence. Which legitimate operation goes quiet longest?
2. On a flat-rate plan the symptom is a stall. Where would it first show?

### EX-FAIL-05 — failing flaky test (W04)

Rungs: `DL-4` debug.

#### Objective

Stop the gate reading one red run as a verdict, and the agent curing instability
by asserting less.

#### Task

- **Detection.** A test goes red, then green, on a tree nobody touched. Re-run any red test N times against the identical commit before classifying, so the verdict stands on a sequence rather than one observation.
- **Safe failure behaviour.** Never approve past an unclassified red, and never accept a weakened assertion as the remedy. Weakening is the characteristic generated response and is worse than what it removes: the signal goes silent and nothing downstream reports the loss.
- **Recovery.** Classify it, quarantine it with a written reason, hand it to a person. The pull request may proceed, but only with the quarantine spelled out where approval happens, so continuing is a decision somebody took.
- **Logging.** Keep the test id, the red-green sequence across re-runs, and the commit sha. Instability then belongs to a named test with a history instead of being something people say about the suite.
- **Test proving the mitigation.** An unstable fixture is classified rather than failed, and an agent edit to its assertion is turned down at the gate. Both assertions break against a build treating one red as final.

#### Constraints

- N is fixed and stated beforehand; choosing it after seeing results is fitting, not measuring.
- Assertion edits to a quarantined test are refused by the gate.

#### Deliverable

`D-w04-4` — **test suite** (`DT-06`): unstable fixture, classifier, five-part report.

#### Acceptance criteria

- A red test is re-run exactly N times, N stated.
- 0 assertion weakenings are accepted on a quarantined test.
- The suite fails against the one-red-is-final build.

#### Metrics

- Failure rate: tests classified unstable divided by tests that went red.
- Latency: wall-clock added per gate pass, p50.

#### Reflection questions

1. How did the gate separate instability from a real intermittent bug?
2. What does a wrong quarantine cost, and who finds out?

### EX-FAIL-06 — CI failure unrelated to the change (W04)

Rungs: `DL-4` debug.

#### Objective

Keep an unrelated red build off the diff's record, and keep the agent from
enlarging the change while hunting a cause.

#### Task

- **Detection.** Cross the changed file set with each job's declared input paths. A job that went red touching none of them is a candidate, and the crossing is computed rather than judged by eye.
- **Safe failure behaviour.** Withhold the attribution, and forbid edits outside the declared scope while a build is red. Chasing an unrelated failure produces a diff harder to review than the problem it was meant to solve.
- **Recovery.** Label the job unrelated, present it apart from the task's own verdict, and let the task's verification finish and report on its own terms.
- **Logging.** Keep the job name, the changed set, the declared inputs and the crossing result. Mislabelling then becomes auditable, which matters because the classifier will sometimes be wrong and you want the rate.
- **Test proving the mitigation.** A fixture change in one module, with a knowingly broken job elsewhere, is labelled unrelated while its own verification reports separately. The independence assertion breaks on a build reading any red as failure.

#### Constraints

- Every job declares its inputs; a job declaring none is treated as related.
- The agent may not edit outside the declared scope while any build is red.

#### Deliverable

`D-w04-4` — **test suite** (`DT-06`): fixture change, crossing classifier, five-part report.

#### Acceptance criteria

- A job crossing the changed set at 0 paths is labelled unrelated.
- The task's verification reports separately, sharing 0 fields.
- The suite fails against the any-red-is-failure build.

#### Metrics

- Failure rate: jobs mislabelled divided by jobs labelled.
- Success rate: tasks finishing despite an unrelated red job, divided by tasks meeting one.

#### Reflection questions

1. Which job could not declare its inputs honestly, and what does that reveal?
2. What could an attacker do with a permanently unrelated-red job?

### EX-FAIL-07 — stale documentation (W05)

Rungs: `DL-4` debug.

#### Objective

Stop retrieval ranking a year-old document like a current one, and make the
answer admit when it could not tell.

#### Task

- **Detection.** At retrieval, set each chunk's provenance timestamp against the modification time of whatever it describes. A document materially older than its subject is a candidate, and so is one contradicting the current source.
- **Safe failure behaviour.** Pass staleness up as its own signal instead of ranking normally and hoping. An agent that cannot separate current from obsolete states the obsolete version with identical confidence, and the confidence does the damage.
- **Recovery.** Push stale chunks down by trust tier. Where an answer genuinely rests on one, present it with its age so a person can weigh it, rather than hiding it and leaving the question unanswered.
- **Logging.** Keep the chunk id, its age, the age of what it describes, and whether the answer leaned on it. That fourth field converts an index statistic into a measure of real harm.
- **Test proving the mitigation.** A corpus holding one obsolete document yields an answer that either avoids it or presents it with its age. Relevance-only ranking breaks that assertion and states the obsolete claim flatly.

#### Constraints

- Staleness comes from provenance, never from an impression of writing style.
- Silently suppressing an old document fails this exercise rather than satisfying it.

#### Deliverable

`D-w05-4` — **test suite** (`DT-06`): seeded obsolete document, provenance comparison, five-part report.

#### Acceptance criteria

- 100% of retrieved chunks carry a provenance timestamp.
- An answer using a stale chunk presents its age, in at least 1 case.
- The suite fails against relevance-only ranking.

#### Metrics

- Retrieval precision: current relevant chunks divided by chunks returned, per arm.
- Failure rate: answers using a stale chunk without its age, divided by answers produced.

#### Reflection questions

1. What is the oldest document your index would still rank first?
2. Which is worse — an answer from an obsolete document, or none at all?

### EX-FAIL-08 — misleading code comments (W06)

Rungs: `DL-4` debug.

#### Objective

Find which source the agent believes when comment and code disagree, and make it
report rather than inherit.

#### Task

- **Detection.** Ask the agent to describe the function twice — once from the comment with the body hidden, once the reverse — and diff the descriptions. Found this way a disagreement is mechanical; looked for informally it is missed.
- **Safe failure behaviour.** Rank the body as ground truth and the comment as an unverified assertion. Enforce that deliberately: a comment is often the highest-signal text present, and its error is inherited fluently and in full.
- **Recovery.** Raise the disagreement as a finding rather than quietly preferring a side. Prose describing code that no longer exists is a defect with a fix; filed as noise it misleads whoever reads next.
- **Logging.** Keep the file, the line, both descriptions, and which one the agent's first unprompted answer matched. That final field measures the failure mode; the rest only records the incident.
- **Test proving the mitigation.** Two corpus issues carry prose misstating their code; assert the agent raises the disagreement rather than repeating it. Handed the comment as authoritative it repeats the claim and the assertion breaks.

#### Constraints

- The two descriptions are produced independently, neither visible while the other is written.
- At least 2 corpus issues carry a genuine misstatement, from real history where possible.

#### Deliverable

`D-w06-3` — **test suite** (`DT-06`): labelled corpus subset, five-part report.

#### Acceptance criteria

- At least 2 corpus issues carry prose that misstates their code.
- 100% of disagreements are raised as findings.
- The suite fails against the comment-as-authoritative build.

#### Metrics

- Success rate: disagreements raised divided by disagreements present.
- Failure rate: first answers matching the prose divided by disagreeing cases.

#### Reflection questions

1. Which comment in your codebase would fail this today?
2. If comments are unverified assertions, how should you write them?

### EX-FAIL-09 — Sentry event with misleading stack trace (W07)

Rungs: `DL-4` debug.

#### Objective

Break the habit of diagnosing from the top frame, using issues where the fault is
not there.

#### Task

- **Detection.** The top frame belongs to a decorator, a codec or a framework edge rather than to the defect. You learn this when a reproduction built from it does not reproduce — the only reliable signal.
- **Safe failure behaviour.** Refuse a hypothesis with no working reproduction behind it. A remedy derived from a trace is speculation shipped in the shape of a diagnosis, and it gets reviewed as one.
- **Recovery.** Broaden from the trace to the commit correlated with the issue and to what retrieval knows about the surrounding module, then rebuild the hypothesis on the reproduction instead of on the trace you started from.
- **Logging.** Keep the topmost frame, the frame the reproduction accused, and how precisely retrieval correlated that issue. Across a corpus this yields both how often traces mislead and what correlation is worth.
- **Test proving the mitigation.** Diagnose a real historical issue whose trace points away from its fixing commit; then show the run skipping reproduction proposing the wrong remedy. Accepting the topmost frame breaks the diagnosis assertion.

#### Constraints

- The corpus is real historical issues, never synthesised traces.
- No hypothesis is recorded before its reproduction runs; the harness enforces it.

#### Deliverable

`D-w07-3` — **test suite** (`DT-06`): reproduction-first lane, five-part report over the real corpus.

#### Acceptance criteria

- At least 1 issue with an innocent topmost frame is diagnosed correctly.
- 0 hypotheses are accepted without a reproduction behind them.
- The suite fails against the build that accepts the topmost frame.

#### Metrics

- Success rate: issues diagnosed correctly divided by issues attempted.
- Retrieval precision: correctly correlated commits divided by correlations attempted.

#### Reflection questions

1. How deep did the fault sit, and what would have sent you there sooner?
2. What defect class would still defeat reproduction-first?

### EX-FAIL-10 — two agents modifying overlapping files (W08)

Rungs: `DL-7` operate.

#### Objective

Show that concurrent workers cannot quietly overwrite each other, and that
separation dissolves most of the problem before any lock.

#### Task

- **Detection.** Two claimed tasks announce file scopes that intersect, or two worktrees emit diffs over a shared path. Both are visible before the collision, which is what makes prevention possible.
- **Safe failure behaviour.** Separate rather than lock: tasks whose scopes intersect are never claimed at the same time. Contention that cannot occur needs no coordination, and coordination you never need is coordination that never has a bug.
- **Recovery.** Where separation is unavailable, order writers on a version column and make the loser rebuild its diff on the new base. Merging unchecked is what this exposes: it succeeds quietly, leaving a tree nobody authored.
- **Logging.** Keep both task ids, both scopes, the intersection, and whether separation or a version conflict settled it. The ratio between those outcomes is the honest measure of how well separation works.
- **Test proving the mitigation.** Two tasks with a planned intersection are never claimed together; forced together, the second is turned away by the version check instead of overwriting. Without announced scopes both assertions break.

#### Constraints

- Every task announces a file scope; a task without one is not claimable.
- No `sleep` may be used to make the collision reproduce.

#### Deliverable

`D-w08-3` — **test suite** (`DT-06`): intersecting fixture, both resolution paths, five-part report.

#### Acceptance criteria

- 0 simultaneous claims occur on task pairs that intersect.
- Forced together, the losing write is refused in 100% of trials.
- The suite fails against the build with no announced scopes.

#### Metrics

- Failure rate: version conflicts divided by simultaneous claims.
- Success rate: tasks finishing without a rebuild, divided by tasks claimed.

#### Reflection questions

1. Where did separation stop being available, and what ended it?
2. What breaks first if you double the workers?

### EX-FAIL-11 — malicious GitHub issue (W09)

Rungs: `DL-6` secure, `DL-7` operate.

#### Objective

Make a hostile issue hit a ceiling before it spends, and put a number on the
undefended cost.

#### Task

- **Detection.** An issue body drives work without bound — an enormous attachment, a self-referential instruction, a request that fans out. It surfaces when the shared retry and token ceiling is hit first, making the ceiling the detector.
- **Safe failure behaviour.** Apply the ceiling ahead of the spend, not afterwards. Turn down work that would exceed it rather than quietly slowing: on a flat-rate plan a slowdown reads as ordinary latency, and nobody investigates latency.
- **Recovery.** Dead-letter the task with the breach on record, and from here treat issue bodies as hostile content for the trust boundary built later. The two mitigations compose and neither suffices alone.
- **Logging.** Keep tokens spent, retries per layer, seconds parked waiting on quota, and which ceiling was reached. Quota wait is the field most often omitted and the one that later makes a cost anomaly legible.
- **Test proving the mitigation.** A hostile fixture issue reaches the shared ceiling and is turned down, with the undefended spend recorded beside it. Per-layer counting never turns it down and the spend assertion breaks.

#### Constraints

- The undefended cost is measured on a real run, never derived arithmetically.
- The ceiling is checked before each unit of work, not sampled on a timer.

#### Deliverable

`D-w09-2` — **test suite** (`DT-06`): hostile fixture, shared ceiling, five-part report carrying both spends.

#### Acceptance criteria

- The hostile fixture is turned down, with 0 further units dispatched.
- Undefended spend is a measured figure from at least 1 real run.
- The suite fails against the per-layer build.

#### Metrics

- Cost: tokens and quota spent per hostile issue, per arm.
- Failure rate: tasks dead-lettered divided by hostile fixtures run.

#### Reflection questions

1. What is the cheapest issue that costs you most, and does the ceiling catch it?
2. What does one attack cost, and is that small enough to ignore?

### EX-FAIL-12 — conflicting requirements (W10)

Rungs: `DL-3` break, `DL-5` measure.

#### Objective

Measure how often the agent notices two criteria cannot both hold, and score an
elegant implementation of one as failure.

#### Task

- **Detection.** Require the criteria restated as assertions before implementation begins. As assertions a contradiction is mechanical, decidable without judgement; as prose it depends on how carefully somebody read.
- **Safe failure behaviour.** Raise the conflict rather than quietly choosing. The score surprises people: what counts is the raising, not the quality produced. A polished implementation of one arbitrarily chosen criterion is precisely the failure being measured.
- **Recovery.** Return the task to a waiting state naming both criteria and the specific incompatibility — not "this is unclear", but which pair and why they cannot both be satisfied.
- **Logging.** Keep both criteria, whether the agent raised or chose, and which it chose. That distribution alone is informative: agents take the first, the longest, or the last, and knowing which tells you how to write tasks.
- **Test proving the mitigation.** Across the twenty-task suite, planted contradictions are raised above a pre-declared threshold, and a quiet choice fails even where its output satisfies one criterion perfectly. Remove the restatement and the rate collapses.

#### Constraints

- The restatement precedes implementation and is kept, or detection is unattributable.
- Output quality never substitutes for the raising rate in the score.

#### Deliverable

`D-w10-3` — **test suite** (`DT-06`): planted contradictions inside the twenty-task suite, five-part report.

#### Acceptance criteria

- Raising rate on planted contradictions beats the pre-declared threshold, over 20 tasks.
- 100% of quiet choices score as failures, whatever the output quality.
- The suite fails against the build with no restatement step.

#### Metrics

- Success rate: contradictions raised divided by contradictions presented.
- Failure rate: quiet choices divided by contradictions presented.

#### Reflection questions

1. When it chose rather than raised, which criterion won, and is that stable?
2. What does the raising rate say about your task-writing that a pass rate cannot?

### EX-FAIL-13 — indirect prompt injection inside a retrieved document (W11)

Rungs: `DL-6` secure.

#### Objective

Defend the class where nobody touches your prompt, structurally rather than by
asking for vigilance.

#### Task

- **Detection.** Hold the run against a twin over a clean corpus and look for divergence. You detect the difference between two outputs, not a known string: a matcher firing only on payloads it has met is a denylist, and the next payload walks past.
- **Safe failure behaviour.** Give retrieved text no standing. Tag its origin at index time, keep it beyond a separator the model cannot be argued across, and deny it power to authorise a call — all properties of code, not requests.
- **Recovery.** Take outbound capability away from any turn that read hostile text in that cycle. That removes a leg of the triangle rather than screening it, and telling those apart is the examinable skill.
- **Logging.** Keep the style, the query, both outputs, and whether an outbound call was attempted. That last field separates an attack that bent the answer from one that reached the network, and they are not equally bad.
- **Test proving the mitigation.** Three styles or more over one frozen query list, rates from both arms, a denominator on each, no borrowed figure standing in for a measurement. The folding build fails outright.

#### Constraints

- The separator is enforced in code; instructing the model to disregard document text is the patch this discredits.
- The query list is frozen before the first arm and identical in the second.

#### Deliverable

`D-w11-2` — **attack report** (`DT-07`): three styles, both arms, five-part report.

#### Acceptance criteria

- At least 3 styles run over 1 frozen query list in both arms.
- 0 hostile-text turns reach an outbound call after the mitigation.
- The report carries 0 borrowed figures.
- The suite fails against the folding build.

#### Metrics

- Attack success rate: divergences from the twin divided by frozen-list queries, per style, per arm.
- Failure rate: outbound attempts divided by hostile-text turns.

#### Reflection questions

1. Did you remove a leg or raise a screen, and what settles that?
2. What authority here should no document ever be able to reach?

### EX-FAIL-14 — malicious tool output (W12)

Rungs: `DL-6` secure.

#### Objective

Stop a tool's return value carrying instructions into the model, using a shape
with nowhere to put one.

#### Task

- **Detection.** Return values holding instruction-shaped prose, or breaking their declared shape, are caught where the tool hands back — ahead of context assembly, therefore ahead of any chance for the model to act.
- **Safe failure behaviour.** Rank a tool's output with inbound mail, not with internal state. A shape with no field able to hold an instruction cannot carry one, so the check is the control and the model's cooperation is not needed.
- **Recovery.** Turn the value away, record the refusal, call again with a narrower shape. After N refusals dead-letter rather than settling for a lossy parse — settling is how a hard edge quietly becomes a soft one.
- **Logging.** Keep the tool, the value exactly as returned, the check that rejected it, and the agent's next move. The raw value matters: it is the only artifact from which a refused attack can be reconstructed later.
- **Test proving the mitigation.** A stub returning both hostile shapes is refused at handover and never appears in the instruction context. A build passing values through as text fails containment on the first fixture.

#### Constraints

- The check runs at handover, ahead of context assembly.
- No field may be wide enough to hold free-form instructions.

#### Deliverable

`D-w12-2` — **attack report** (`DT-07`): hostile stub, handover check, five-part report.

#### Acceptance criteria

- 0 instruction-shaped values appear in the instruction context.
- 100% of shape violations are refused at handover, tool named.
- The task dead-letters after exactly N refusals, N stated beforehand.
- The suite fails against the pass-through build.

#### Metrics

- Success rate: hostile values refused divided by hostile values returned, per arm.
- Failure rate: tasks dead-lettered divided by tasks run against the stub.

#### Reflection questions

1. Which tool reads prose a stranger wrote, and does its return type admit it?
2. What would you surrender to close every tool's output shape?

### EXT-01 — crash between commit and external effect (M04)

Rungs: `DL-3` break, `DL-7` operate.

#### Objective

Remove the window between a local commit and an outward call, checking every
point rather than a sample.

#### Task

- **Detection.** An injector ends the process at each point separating the commit from the final outward call — all of them — and writes down the inconsistency produced at each.
- **Safe failure behaviour.** The pending-effect row is written by the transaction that moves the state, so a rollback leaves nothing owed. The safety is structural: no ordering of deaths yields a promise the system did not record.
- **Recovery.** A relay in its own process delivers pending effects at least once, and handlers stay correct when it delivers twice. Both halves are load-bearing; a relay whose handlers are not twice-safe has relocated the defect.
- **Logging.** Keep the death point, what was inconsistent there, and how long commits took to become effects at the median and the tail. That distribution reports a sick relay long before anything visibly fails.
- **Test proving the mitigation.** With the pending table in place, no death point loses an effect or leaves state and effects disagreeing; asserting that a rolled-back transaction leaves no pending row demonstrates the shared transaction directly.

#### Constraints

- Injection covers every point, never a sample.
- The relay runs in its own process, so the property survives that one dying.

#### Deliverable

`D-m04-2` — **test suite** (`DT-06`): pending table, relay, exhaustive injector, five-part report.

#### Acceptance criteria

- With the pending table in place, 0 death points lose an effect or disagree.
- A rolled-back transaction leaves 0 pending rows.
- The suite fails against the commit-then-call build.

#### Metrics

- Latency: commit to effect, median and tail.
- Failure rate: disagreements divided by death points exercised, per arm.

#### Reflection questions

1. What is the longest an effect has waited in the relay?
2. The pending table moved the risk. Where does it live now?

### EXT-02 — compensation that fails (M04)

Rungs: `DL-3` break, `DL-8` explain.

#### Objective

Discover what your teardown does when an undo step fails for good.

#### Task

- **Detection.** An undo step inside the lifecycle teardown fails, and fails permanently rather than briefly. Telling those apart is the detection, because the correct responses have nothing in common.
- **Safe failure behaviour.** Each undo step is independently repeatable, and the suite calls each twice to show it rather than asserting it in prose. They run in a fixed order, lease surrendered last, and that order is argued in writing.
- **Recovery.** A permanently failing undo step ends in a named terminal state with an alert a person sees — never a hang, never a swallowed exception. One effect admitting no undo must be named, with an account of what happens instead.
- **Logging.** Keep which undo steps proved not repeatable when first written — your own included — the states reachable after one fails, and the irreversible effects. The first is uncomfortable and the most useful.
- **Test proving the mitigation.** Twice-called undo steps add nothing the second time, and a permanently failing one lands in a named terminal state. The written defence of which surfaces are teardown-shaped ships beside it.

#### Constraints

- The suite calls every undo step twice; repeatability claimed in prose does not count.
- One irreversible effect must be named; a fully reversible surface was described wrongly.

#### Deliverable

`D-m04-3` — **ADR** (`DT-04`): surface classification with its argument, undo-failure suite, five-part report.

#### Acceptance criteria

- Twice-called undo steps add 0 further effects.
- 100% of planted permanent failures land in a named terminal state, with an alert.
- At least 1 irreversible effect is named with what happens instead.
- The suite fails against the build whose undo steps were called once.

#### Metrics

- Failure rate: undo steps not repeatable when written, divided by undo steps authored.
- Success rate: plants landing in a named terminal state, divided by plants.

#### Reflection questions

1. Which undo step did you write wrongly first, and what do the rest share?
2. At three in the morning, what does the alert say?

### EXT-03 — memory poisoning of durable per-account memory (M05)

Rungs: `DL-6` secure, `DL-7` operate.

#### Objective

Plant a false belief in durable account memory through a hostile channel, have a
much later unrelated decision act on it, and shut that path without destroying
ordinary writes. The most differentiated exercise here.

#### Task

- **Detection.** An entry's origin shows a hostile channel and its history shows one claim pushed again and again. Demand a source on every write and watch for recurrence, the cheapest lever an attacker owns.
- **Safe failure behaviour.** Never let recurrence stand in for confirmation. An entry able to move a consequential decision needs two independent things — an origin score and a person's tag — and anything unconfirmed ages out.
- **Recovery.** Retire or isolate the planted entry, recompute every decision that consulted it, and close the path by which the agent's own output returns as trusted material. That loop is how one plant becomes self-sustaining.
- **Logging.** Keep the channel it arrived on, its tier, how often it was pushed, the distant decision that read it, and what that decision did. The link between write and far-off decision is the evidence this was memory.
- **Test proving the mitigation.** At least one whole pipeline cycle must sit between plant and exploitation, never a single window. It works before the patch, is measurably stopped or flagged after, and the burden on ordinary writes is reported beside it. Without the gap this is ordinary injection.

#### Constraints

- The false belief arrives via the agent's own write path from unchecked input, never by a direct store write.
- The burden on ordinary writes is counted from real runs, not assumed.

#### Deliverable

`D-m05-2` — **attack report** (`DT-07`): the plant, the distant decision, the patch, both arms, five-part report.

#### Acceptance criteria

- The exploiting decision falls at least 1 cycle later, over 2 session records.
- Before the patch, the planted belief moves at least 1 proposed decision.
- After the patch, the same sequence produces 0 acted-on plants.
- The burden on ordinary writes is reported over at least 10, with its denominator.

#### Metrics

- Attack success rate: plants acted on divided by plants attempted, per arm.
- Failure rate: ordinary writes isolated divided by ordinary writes.

#### Reflection questions

1. Which stored belief would not survive today's rules, and what rests on it?
2. What gives way at tenfold — retrieval, storage, or traceability?

### EXT-04 — malformed input to the operations agent (M05)

Rungs: `DL-3` break.

#### Objective

Separate a document the parser cannot read from one it reads into something
plausible and wrong, then refuse the second.

#### Task

- **Detection.** An inbound document either defeats extraction outright or yields a well-formed but improbable result. The second needs plausibility rules of its own, because well-formed is not believable and only the first is caught for free.
- **Safe failure behaviour.** Treat a validation failure as a retry signal with a written reason, never a cue to substitute a default. Escalate the improbable case: acting on it produces an outcome that looks entirely ordinary downstream.
- **Recovery.** Extract again against a narrower shape, and after N failures route to a person instead of accepting a lossy parse. That threshold is chosen and stated, not whatever the loop settled on.
- **Logging.** Keep the input as received, the rule it broke, the retry count and the disposition. The raw input is what lets a class of bad document be recognised as a class.
- **Test proving the mitigation.** A corpus of deliberately broken documents yields no substituted defaults and no acted-on improbable results. The build filling in defaults produces both, and both counts are non-zero.

#### Constraints

- No default is substituted on a validation failure, however reasonable.
- Plausibility rules are explicit and testable, not the model's opinion of its own output.

#### Deliverable

`D-m05-3` — **test suite** (`DT-06`): broken corpus, plausibility rules, five-part report.

#### Acceptance criteria

- 0 defaults are substituted across the broken corpus.
- 0 well-formed-but-improbable results are acted on.
- A person is reached after exactly N failures, N stated beforehand.
- The suite fails against the default-substituting build.

#### Metrics

- Failure rate: extraction failures divided by documents submitted.
- Success rate: escalations confirmed correct divided by escalations raised.

#### Reflection questions

1. What does a well-formed but improbable extraction look like here?
2. Which rule would turn away a real, unusual, legitimate document?

### EXT-05 — authorization bypass through a policy gap (M06)

Rungs: `DL-6` secure.

#### Objective

Find the action your policy never mentions, and make silence mean refusal.

#### Task

- **Detection.** A request lands on a resource no role grants, because the check has a hole rather than a closed default. Fuzz action and role pairs: reading surfaces the rules that exist, and this defect is about the ones that never did.
- **Safe failure behaviour.** Refuse by default: an action matching no rule is turned away. In code that is the difference between a check ending in a returned false and one running off the bottom returning nothing.
- **Recovery.** Add the missing rule, and add an assertion for the refusal path rather than only for the permission you just introduced. Testing the new permission alone leaves the class exactly where it was.
- **Logging.** Keep the principal, the action, the rule that matched or the fact none did, and the outcome. The none-matched case is worth alerting on: it is either an attack or a policy behind the product.
- **Test proving the mitigation.** A fuzz across action and role pairs turns up nothing allowed without an explicit rule. Against the pre-patch check the fuzz walks into the hole and the assertion breaks.

#### Constraints

- The fuzz covers the whole cross-product of actions and roles, not a sample.
- Every new rule ships with a refusal-path assertion.

#### Deliverable

`D-m06-2` — **test suite** (`DT-06`): hand-written pre-execution check, cross-product fuzz, five-part report.

#### Acceptance criteria

- 0 actions are allowed without an explicit rule, across the cross-product.
- 100% of new rules ship with a refusal-path assertion.
- Unmatched requests record principal and action in 100% of cases.
- The suite fails against the pre-patch check.

#### Metrics

- Failure rate: allowed-without-rule pairs divided by pairs fuzzed.
- Test coverage: pairs exercised divided by pairs defined.

#### Reflection questions

1. How many action-role pairs exist, and did the number surprise you?
2. What breaks for a legitimate user when refusal-by-default lands?
