# Week 09 — Agent Evals and Regression Gates

## Outcome

By Sunday a prompt change or a harness change cannot merge without clearing a
gate: deterministic assertions plus a three-rerun replay over five real tasks,
against a pass-rate threshold you can defend in writing — and you have proved the
gate blocks by injecting a degradation you chose.

## Why now?

Eight weeks of prompts, tool definitions, plan templates and classifiers, all
tuned by feel. You have no idea whether last Tuesday's prompt edit made things
better. The pipeline is nondeterministic, so a single green run proves nothing and
a single red run proves nothing — which means the only honest instrument is a
distribution over reruns.

This is the week that makes every earlier week's work defensible, and it is
deliberately placed after there is enough surface to regress.

## Build

**A frozen suite** drawn from real tasks you have already run — the feature and
bug tasks from weeks 3 and 4, with their known-correct outcomes. Real tasks with
known answers, not synthesised ones. **Five for Core.** Five tasks at N=3 is
thirty runs per arm and sixty across baseline and candidate, which is what
actually fits beside everything else this week. Growing the suite to 10–20 at N=5
is Stretch — worth doing, and not what makes the gate work.

**Tiers, reported as separate checks.** One aggregate verdict throws away which
tier failed, and the tiers catch different things:

| Tier | What it is | What it cannot catch | |
|---|---|---|---|
| **Deterministic** | Did the test pass, did the PR open, was the done-condition met | Anything about quality | **Core** |
| **Repeated replay** | The full task run, N=3 over 5 tasks, environment reset between runs | Anything the suite does not cover | **Core** |
| Rescore | A cheap lexical/entailment check first; a model judge only where those disagree | Its own position bias | *Stretch* |

The first two are enough to build a working regression gate. The third improves
what it can see and is where most of the complexity lives.

**A threshold stated as a bound, not a binary.** With N=3 per task you have a
pass-rate distribution — a coarse one, and coarse is fine at this suite size.
"Everything must pass" is not a threshold; it is a wish. State the bound against
last-known-good, justify it in a paragraph, and state the condition under which
you re-baseline.

**If you build the judge tier, calibrate it.** Reproducibility is not validity: a
judge can show very high test-retest reliability and substantial position bias at
the same time, and raw agreement overstates chance-corrected agreement. Use it as
a tie-breaker, never the primary instrument.

## Learn

- [Offline retrieval/eval metrics](https://www.pinecone.io/learn/offline-evaluation/) —
  and, more importantly, the discipline of freezing a label set before tuning.
- LLM-as-judge reliability research: search *llm-as-a-judge position bias
  chance-corrected agreement*. Read for the minimum viable validation protocol.

~2.5h.

## Tasks

### Core — required (~15h: 2h learning, 10h building/testing, 3h business)

1. **Assemble the frozen suite** from real historical tasks, each with its
   known-correct outcome. Record a digest so a later reader can prove it was
   frozen before tuning. **Twenty tasks if you have twenty; ten is enough to start
   and honest about it** — a suite of ten real tasks beats twenty where half were
   invented to fill the count.
2. **Deterministic checks.** Per task: did the test pass, did the PR open, was the
   done-condition met. Binary, cheap, no model involved. This tier does most of
   the work and it is the one you must not skip.
3. **Repeated execution.** Run each of the 5 tasks **N=3** with the environment
   reset between runs, and report a **pass-rate distribution** rather than a
   single figure. The pipeline is nondeterministic, so one green run and one red
   run are both uninformative.
4. **Baseline versus candidate.** Record the current pass rates as
   last-known-good. Then make a real change — edit the plan prompt, swap the model
   — and compare candidate against baseline on the same frozen suite.
5. **State the threshold explicitly**, as a bound against last-known-good rather
   than "everything must pass", with a one-paragraph justification and the
   condition under which you re-baseline.
6. **Wire the gate into the merge path** for prompt, tool-definition and harness
   changes, then **prove it blocks by injecting a known degradation.** Deliberately
   break something you understand — truncate the plan prompt, remove the research
   step's output from context, downgrade the model — run the gate, and show it
   blocking. That is the week's proof, and it is repeatable on demand.
   **A naturally occurring regression is bonus evidence, not the requirement**:
   waiting for one to appear makes the week's completion depend on luck.
7. **Business: 5 sends, and compute your funnel rates.** You now have roughly
   50 sends of history. Divide. Reply rate, reply-to-call rate, actual numbers
   with denominators visible. This is the first week that division means anything;
   record what it says even if what it says is zero.

### Stretch — only after Core is DONE

- **Grow the suite to 10–20 tasks at N=5.** More statistical room and a threshold
  you can state more tightly. Do this once the gate is working, not before — a
  larger suite makes every iteration slower while you are still getting the gate
  right.
- **Add the rescore tier**: a cheap lexical or entailment check on output quality,
  with a model judge invoked *only* where the cheap checks disagree. Genuinely
  useful, and it is where most of the week's complexity lives — which is why it is
  not required to claim a working regression gate.
- **Calibrate the judge** if you built it: measure its agreement with your own
  labels on a labelled subset and report **chance-corrected** agreement rather than
  raw, because raw agreement overstates it. Also check position bias by swapping
  the order of the things being compared. A judge you have not calibrated is a
  number you cannot use.
- **Trace evaluation**: sample completed runs from the week-7 spans and check the
  claimed reasoning against what the trace shows actually happened. Excellent
  exercise, entirely separable from the gate.
- **Write each tier's blind spot** in one line. Cheap, and it is what separates
  asserting a score from asserting a decision rule — do this one even if you skip
  the rest.

## Use it for real

The suite must contain real tasks whose correct outcome you know independently.
Then make a real change — edit the plan prompt, or swap the model — and let the
gate judge it. Separately, inject a degradation you chose on purpose, so that the
gate's blocking behaviour is demonstrated rather than waited for.

## Measure

- Suite pass-rate distribution over N=3, per task and aggregate.
- Baseline versus candidate on the same frozen suite, per task.
- Threshold: the stated bound, and the current position relative to it.
- Gate blocks: **the injected known degradation was blocked**, and by how much it
  missed the bound. This is the week's headline. Any naturally occurring
  regression caught alongside it is bonus evidence.
- Business: actual reply rate and reply-to-call rate, denominators shown.

## Failure exercise

**Conflicting requirements.** Measure how often the agent notices two criteria
cannot both hold — and score an elegant implementation of one as a failure.

- **Detection.** Require the criteria restated as assertions before implementation
  begins. As assertions a contradiction is mechanical and decidable; as prose it
  depends on how carefully somebody read.
- **Safe failure.** Raise the conflict rather than quietly choosing. **What counts
  is the raising, not the quality produced** — a polished implementation of one
  arbitrarily chosen criterion is precisely the failure being measured, and this
  scoring rule surprises people.
- **Recovery.** Return the task to a waiting state naming both criteria and the
  specific incompatibility. Not "this is unclear" — which pair, and why they
  cannot both hold.
- **Logging.** Both criteria, whether the agent raised or chose, and which it
  chose. That distribution alone is informative: agents take the first, the
  longest, or the last, and knowing which tells you how to write tasks.
- **Proving test.** Plant contradictions inside the frozen suite. Raising rate
  must beat a threshold declared in advance, and a quiet choice scores as a
  failure whatever its output quality. **Remove the restatement step and the rate
  collapses.**

## Deliverables

- [ ] Frozen suite of 5 real tasks, with a digest proving the freeze.
- [ ] Deterministic tier and N=3 replay tier, reporting as separate checks.
- [ ] Baseline-versus-candidate comparison on the same frozen suite.
- [ ] Written threshold: bound against last-known-good, justification,
      re-baselining condition.
- [ ] Gate wired into the merge path, with **an injected known degradation shown
      to be blocked**.
- [ ] Conflicting-requirements report, five parts, proving test red without the
      restatement step.
- [ ] 5 sends logged; funnel rates computed from actuals with denominators.

## Done when

- [ ] The suite is frozen with a digest, and every task in it is a real task with
      a known-correct outcome.
- [ ] Tiers run and report separately; the replay tier runs N=3 with environment
      reset and reports a distribution rather than a single figure.
- [ ] Candidate is compared against a recorded baseline on the identical suite.
- [ ] The threshold is a stated bound with a written justification and a
      re-baselining condition — not "everything must pass".
- [ ] **A deliberately injected degradation was blocked by the gate**, with the
      degradation named and the margin recorded. A naturally occurring regression,
      if one appeared, is recorded as bonus evidence.
- [ ] Raising rate on planted contradictions beats the pre-declared threshold, and
      100% of quiet choices score as failures.
- [ ] The scoreboard's rate rows are computed from actuals, with denominators
      visible.

## Reflection

1. When the agent chose rather than raised, which criterion won — the first, the
   longest, the last? Is that stable across the suite?
2. What does the raising rate tell you about your task-writing that a pass rate
   cannot?
3. The degradation you injected: would a human reviewer have caught it? If yes,
   what did the gate buy you — speed, or the fact that a human would not have
   looked?

## Evidence

- Frozen suite and its digest.
- Per-tier gate output and the pass-rate distribution.
- Baseline and candidate results side by side.
- Threshold document with justification.
- The injected degradation, and the gate output blocking it.
- Conflicting-requirements report and its red-on-parent test.
- Send log and the computed rates.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
