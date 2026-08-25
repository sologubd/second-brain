# Week 09 — Agent Evals and Regression Gates

## Outcome

By Sunday a prompt change or a harness change cannot merge without clearing three
gates: deterministic assertions, a rescore, and a five-rerun replay against a
pass-rate threshold you can defend in writing.

## Why now?

Eight weeks of prompts, tool definitions, plan templates and classifiers, all
tuned by feel. You have no idea whether last Tuesday's prompt edit made things
better. The pipeline is nondeterministic, so a single green run proves nothing and
a single red run proves nothing — which means the only honest instrument is a
distribution over reruns.

This is the week that makes every earlier week's work defensible, and it is
deliberately placed after there is enough surface to regress.

## Build

**A 20-task suite** drawn from real tasks you have already run — the feature and
bug tasks from weeks 3 and 4, with their known-correct outcomes. Real tasks with
known answers, not synthesised ones.

**Three gate tiers, reported as separate checks.** One aggregate verdict throws
away which tier failed, and the tiers catch different things:

| Tier | What it is | What it cannot catch |
|---|---|---|
| 1 — deterministic | Assertions: did the test pass, did the PR open, was the file scope respected | Anything about quality |
| 2 — rescore | A cheap lexical/entailment check first; a model judge only where those disagree | Its own position bias |
| 3 — replay | The full task run, N=5, with environment reset between runs | Anything the suite does not cover |

**Report each tier's blind spot in the artifact.** Most published eval work asserts
a score; asserting a decision rule *and its blind spots* is what an engineer who
has run a flaky suite looks for.

**A threshold stated as a statistical bound, not a binary.** With N=5 per task,
you have a pass-rate distribution, and "everything must pass" is not a threshold —
it is a wish. State the bound against last-known-good, justify it in writing, and
state the condition under which you re-baseline.

**On the judge tier:** reproducibility is not validity. A judge can show very high
test-retest reliability and substantial position bias at the same time, and raw
agreement overstates chance-corrected agreement. Use it as the tie-breaker, not
the primary instrument, and record its agreement with your own labels on a subset.

## Learn

- [Offline retrieval/eval metrics](https://www.pinecone.io/learn/offline-evaluation/) —
  and, more importantly, the discipline of freezing a label set before tuning.
- LLM-as-judge reliability research: search *llm-as-a-judge position bias
  chance-corrected agreement*. Read for the minimum viable validation protocol.

~2.5h.

## Tasks

1. **Assemble the 20-task suite** from real historical tasks, each with its
   known-correct outcome. Freeze it, and record a digest so a later reader can
   prove it was frozen before tuning.
2. **Build tier 1**: deterministic assertions per task.
3. **Build tier 2**: cheap lexical/entailment check, with the judge invoked only
   on disagreement. Measure the judge's agreement with your own labels on a
   subset, and report chance-corrected agreement rather than raw.
4. **Build tier 3**: N=5 replay with environment reset between runs, reporting a
   pass-rate distribution.
5. **Set and justify the threshold.** A statistical bound against last-known-good,
   plus the re-baselining condition, written out.
6. **Wire the gate into the merge path** for changes to prompts, tool definitions
   and harness code — and demonstrate it blocking a change.
7. **Run a trace-evaluation pass** over the week-7 spans: sample completed runs
   and check the claimed reasoning against what the trace shows actually happened.
8. **Business: 5 sends, and compute your funnel rates.** You now have roughly
   50 sends of history. Divide. Reply rate, reply-to-call rate, actual numbers
   with denominators visible. This is the first week that division means anything;
   record what it says even if what it says is zero.

## Use it for real

The suite must contain real tasks whose correct outcome you know independently.
Then make a real change — edit the plan prompt, or swap the model — and let the
gate judge it. If the gate never blocks anything this week, you have not tested
the gate.

## Measure

- Suite pass-rate distribution over N=5, per task and aggregate.
- Threshold: the stated bound, and the current position relative to it.
- Judge agreement with your labels on the subset, chance-corrected.
- Gate blocks: at least one real change blocked, and whether the block was right.
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
- **Proving test.** Plant contradictions inside the 20-task suite. Raising rate
  must beat a threshold declared in advance, and a quiet choice scores as a
  failure whatever its output quality. **Remove the restatement step and the rate
  collapses.**

## Deliverables

- [ ] Frozen 20-task suite from real tasks, with a digest proving the freeze.
- [ ] Three gate tiers running and reporting as separate checks.
- [ ] Written threshold: statistical bound, justification, re-baselining condition.
- [ ] Each tier's blind spot stated in writing.
- [ ] Judge agreement measured on a labelled subset, chance-corrected.
- [ ] Gate wired into the merge path, with one real change demonstrably blocked.
- [ ] Trace-evaluation report over the week-7 spans.
- [ ] Conflicting-requirements report, five parts, proving test red without the
      restatement step.
- [ ] 5 sends logged; funnel rates computed from actuals with denominators.

## Done when

- [ ] Three tiers run as separate checks and report separately.
- [ ] Tier 3 runs N=5 per task with environment reset, and reports a pass-rate
      distribution rather than a single figure.
- [ ] The threshold is stated as a bound with a written justification and a
      re-baselining condition.
- [ ] Each tier's blind spot is named in the artifact.
- [ ] At least one real change was blocked by the gate, and you can say whether
      the block was correct.
- [ ] Raising rate on planted contradictions beats the pre-declared threshold over
      20 tasks, and 100% of quiet choices score as failures.
- [ ] The scoreboard's rate rows are computed from actuals, with denominators
      visible.

## Reflection

1. When the agent chose rather than raised, which criterion won — the first, the
   longest, the last? Is that stable across the suite?
2. What does the raising rate tell you about your task-writing that a pass rate
   cannot?
3. Which tier would you drop if you had to run this gate ten times a day, and what
   would you stop being able to see?

## Evidence

- Frozen suite and its digest.
- Per-tier gate output and the pass-rate distribution.
- Threshold document with justification.
- Judge agreement figures.
- The blocked change.
- Trace-evaluation report.
- Conflicting-requirements report and its red-on-parent test.
- Send log and the computed rates.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
