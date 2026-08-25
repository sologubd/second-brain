# Week 03 — Feature Workflow

## Outcome

By Sunday the input is no longer a task file you wrote for the agent — it is a
real issue written for a human. The harness extracts the requirement, researches
the codebase, decides what it can answer itself and what genuinely needs you,
plans, implements, verifies and opens a PR. Five real features through it.

## Why now?

Weeks 1 and 2 required you to write a machine-shaped task file. That is the
bottleneck: writing a good task file is most of the work. This week moves the
boundary — the agent takes the human-shaped input and does the specification work
itself, except where it genuinely cannot. Finding out where that line actually
falls is the point of the week.

## Build

```
GitHub issue / Notion-like task
  ↓
requirement extraction
  ↓
codebase research
  ↓
ambiguity detection  ──────► needs a human? park it
  ↓
implementation plan
  ↓
implementation
  ↓
verification (week 2's gate)
  ↓
pull request              ← automated review is Stretch this week
```

**The load-bearing distinction, and the whole learning objective of the week:**

| Technical question | Product ambiguity |
|---|---|
| The agent answers it from the codebase. *Which module owns rate conversion? What does the existing test fixture look like? Which of these two call sites is dead?* | A human must answer it. *Should an expired discount error or silently apply zero? Do partial refunds notify the customer?* |
| Asking you is a **defect** — the answer was in the repository. | Guessing is a **defect** — the answer was not knowable from code. |

Route the first kind to a research step. Route the second kind to a parked state
that names the specific ambiguity — not "this is unclear" but which pair of
readings, and why code cannot settle it. An agent that asks about everything is
useless, and one that asks about nothing is dangerous; the interesting engineering
is the classifier between them.

An automated review step before the PR is **Stretch**, not Core. Week 2's
verification gate is what keeps bad diffs out this week, and the classifier above
is the thing actually being learned. If you do build the review pass, keep it to
one pass over a few named axes, each citing lines — the five-axis scored version
belongs to months 4–6.

## Learn

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents),
  re-read with a specific question: which of these nine stages should own its own
  control flow, and which should be a code path you own? Write the answer down
  per stage, and for each say what failure means — replay, or re-prompt.
- Your issue tracker's API: reading an issue body, comments, and labels.

~2h.

## Tasks

### Core — required (~15h: 2h learning, 10h building/testing, 3h business)

1. **Ingest a real issue.** Fetch an issue by id, and extract structured
   requirements from its prose body. Keep the raw body — you will need it in week
   11 when it becomes untrusted input.
2. **Build the codebase research step.** Given a requirement, locate the relevant
   modules, tests and call sites, and produce a written finding the plan step
   consumes. This is where a technical question gets answered rather than asked.
3. **Build the ambiguity classifier.** Every question the agent wants to ask gets
   labelled *answerable from the codebase* or *needs a human*. The first kind goes
   back to the research step. The second parks the task with the named
   incompatibility.
4. **Build the plan step.** A written implementation plan before any code: files
   to touch, the approach, and what will verify it. The plan is an artifact you
   read, not a thought the agent has.
5. **Run five real features and score them.** Metrics below.
6. **Business: 5 sends, and document one workflow.** Pick one company from the
   prospect list and document one of its workflows end to end from public
   information: named steps, estimated frequency, estimated time cost per
   occurrence, systems touched. Every unevidenced step is recorded as a gap
   rather than guessed. Tag it `simulated`. This is the artifact you show when a
   prospect asks who else you have done this for.

### Stretch — only after Core is DONE

- **Add the automated review step**: one pass over the diff against a short
  checklist, findings cited by line, reported separately from the verification
  result. Useful, and not needed to claim the feature workflow — the verification
  gate from week 2 is what actually keeps bad diffs out this week. If you do build
  it, keep it to one pass and a handful of named axes; the five-axis scored
  version belongs to months 4–6.
- **Run a sixth feature with the research step disabled** and compare the
  unnecessary-question count. That is the cheapest way to find out whether
  research is earning its place or just adding a stage.

## Use it for real

Five genuine feature requests from your own project — the kind you would
actually assign. Write them as you would write them for a person: prose, no
acceptance-criteria block, no file list. If you find yourself softening one to
help the agent, stop; that softening is the measurement.

Deliberately include **one ambiguous feature** whose ambiguity you know about.
You need to find out whether the classifier catches it.

## Measure

- Autonomous completion: features reaching a PR with no human answering a
  question, over 5.
- **Unnecessary human questions**: questions the agent asked whose answer was in
  the repository. This is the metric that matters most this week.
- **Missed ambiguities**: genuine product ambiguities the agent guessed at
  instead of parking. Count the deliberate one.
- Unnecessary changes: files touched that the plan did not name **and** that the
  task did not turn out to need. Those are two different things — see week 8.
- PR acceptance: PRs you would merge, over PRs opened.

## Failure exercise

**Partial tool failure.** Handle the step that half-worked: one write landed, one
did not, and your stored state now describes a world that never existed. Your
pipeline now calls out to an issue tracker and a Git host, so this is a real
surface rather than a hypothetical one.

- **Detection.** At step exit, hold the effects the step *claims* against those
  you can *observe*. A step claiming three writes but confirming two has not
  finished, whatever its return value said.
- **Safe failure.** Withhold completion until every claimed effect is confirmed;
  a half-applied step stays in flight. The pull toward reporting success on the
  first confirmation is strong precisely because the happy path never separates
  the two.
- **Recovery.** Re-run the whole step. Effects already present must be absorbed —
  and where an effect has no natural key you have to query before re-attempting.
  Read that as a missing key, not a solution. (Week 6 makes this systematic; this
  week you just meet the problem.)
- **Logging.** The confirmed set, the unconfirmed set, and a verdict per failure:
  retryable, permanent, or already-applied. That third verdict is the one most
  implementations lack, and the one that decides whether repeating is safe.
- **Proving test.** Break the second of three writes and assert that after retry
  exactly one of each effect exists and the terminal state is right. The
  complete-on-first-success version fails immediately.

## Deliverables

- [ ] Feature pipeline: issue → requirement extraction → research → ambiguity
      detection → plan → implementation → verification → PR.
- [ ] Ambiguity classifier with the two-way distinction implemented, and the
      parked state naming the specific incompatibility.
- [ ] Written implementation plan artifact per task.
- [ ] Feature run log: 5 features with all five metrics above.
- [ ] Partial-failure report, five parts, proving test red on the parent commit.
- [ ] 5 sends logged; one workflow document from public information, tagged
      `simulated`.

## Done when

- [ ] 5 real feature issues ran through the full pipeline.
- [ ] Every run produced a written plan before any code was generated.
- [ ] The deliberately ambiguous feature was parked, not guessed — and the parked
      record names the two incompatible readings.
- [ ] Unnecessary human questions are counted, and every one is traced to what
      the research step should have found.
- [ ] The partial-failure injector produces exactly one of each effect after
      retry, across at least 3 injection points.
- [ ] The workflow document names ≥5 discrete steps, each with a frequency
      estimate and its basis, and every unevidenced step is marked as a gap.

## Reflection

1. Of the questions the agent asked, how many were answerable from the codebase?
   What would the research step have needed to answer them?
2. Did it miss the planted ambiguity? If it caught it, would it have caught a
   subtler one — and what specifically makes you think so?
3. Which of your five issues would you now write differently, and is that a
   finding about the agent or about you?

## Evidence

- The five feature PRs, and the plan artifact for each.
- The ambiguity log: every question raised, its classification, and whether the
  classification was right.
- The parked task record for the ambiguous feature.
- Partial-failure report and its red-on-parent test.
- Send log; path to the workflow document.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
