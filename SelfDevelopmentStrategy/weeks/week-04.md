# Week 04 — Bug Workflow

## Outcome

By Sunday a bug report becomes a reproduction, then a hypothesis, then a *failing*
regression test, then a fix that makes it pass, then a PR — without you writing
the diff. Five historical bugs whose real root cause you already know have been
through it, so you can score whether it was right rather than whether it sounded
right.

## Why now?

Features are the easy half. A feature has a stated goal, and success is visible
in the diff. A bug has a symptom and a hidden cause, and the tempting failure —
patching the symptom the trace points at — produces a diff that looks correct and
a system that is still broken. This is also the first workflow where you can grade
the agent against ground truth, because you already know the answer.

## Build

```
bug report / historical bug / tracker issue
  ↓
investigation (event, trace, logs)
  ↓
code correlation
  ↓
reproduction        ◄── no hypothesis is recorded before this runs
  ↓
hypothesis
  ↓
failing regression test
  ↓
fix
  ↓
passing test + verification
  ↓
pull request
```

**The rule that makes this work: no hypothesis is accepted without a working
reproduction behind it, and the harness enforces that ordering.** A remedy
derived from a stack trace is speculation shipped in the shape of a diagnosis,
and it gets reviewed as one.

**The regression test must fail on the parent commit.** That is the whole
deliverable. A fix with a test that passes both before and after has proved
nothing at all.

If you have a real error tracker with real historical issues, connect it — the
raw events are much better material than a synthesised report. If not, use closed
bug-fix commits from your own history: the commit message and the linked issue are
the report, and the fix commit is the ground truth you score against.

## Learn

- Your error tracker's API: fetching an issue, its events, and the stack frames.
- One short piece on why stack traces mislead — the top frame belongs to a
  decorator, a codec or a framework edge far more often than to the defect. If you
  cannot find a good write-up, generate the lesson from your own corpus instead:
  for each of the five bugs, record how far the real fault sat from the top frame.

~2h.

## Tasks

1. **Assemble a labelled corpus.** At least 5 historical bugs where the correct
   root cause and the actual fix are known. Record, per bug: the report, the real
   root cause, the fixing commit, and the file the fix touched. This is your
   answer key and you write it before running anything.
2. **Build the code-correlation step.** From a report or a stack trace, produce a
   ranked list of candidate modules and commits. Measure how often the real one
   is in the top few — that number is worth more than the feature itself.
3. **Build the reproduction gate.** A hypothesis cannot be recorded until a
   reproduction runs. Enforce it in code, not in the prompt.
4. **Build the regression-test step.** Write the failing test *before* the fix,
   and assert it fails on the parent commit. Make that assertion part of the
   pipeline, not a manual check.
5. **Score all five against the answer key.** Metrics below. Score root cause and
   fix separately — the agent will sometimes fix the right thing for the wrong
   reason, and sometimes explain the right cause and patch the wrong line.
6. **Business: 6 sends, and hold the call slot.** Reserve a slot in the calendar
   for a discovery call before a reply exists — handling a reply fast matters and
   a slot you have to find is a slot you find late. Write the discovery script
   this week too, *before* the first call: someone running their first call
   without a script reaches for a pitch, and pitching is how a live prospect
   becomes a courteous no. Script in
   [customer discovery](../business/customer-discovery.md).

## Use it for real

Five historical bugs from your own repository, with known correct fixes.
Deliberately include **at least one whose stack trace points away from the real
fault** — that is the failure exercise, and picking it out of your own history is
part of the work.

Do not fabricate bugs. A synthesised bug has its cause where you put it, which
means the pipeline is being scored against your intuitions rather than against
reality.

## Measure

Per bug, against the answer key:

- **Correct root cause**: identified the real cause, over 5.
- **Correct fix**: the fix is materially equivalent to the real one, over 5.
- **Regression test created**: a test that fails on the parent and passes on the
  fix, over 5.
- **Human intervention rate**: interventions per bug, and what each was.
- **Unrelated-change rate**: files touched that the fix did not need, per bug.
- Correlation precision: real fixing module in the top-k candidates, over 5.

Do not average root cause and fix into one number. They fail independently, and
the pair is the interesting reading.

## Failure exercise

**The misleading stack trace.** Break the habit of diagnosing from the top frame,
using issues where the fault is not there.

- **Detection.** The top frame belongs to a decorator, a codec or a framework
  edge rather than to the defect. You learn this when a reproduction built from
  it does not reproduce — which is the only reliable signal, and the reason the
  reproduction gate exists.
- **Safe failure.** Refuse a hypothesis with no working reproduction behind it.
- **Recovery.** Broaden from the trace to the commit correlated with the issue and
  to what research knows about the surrounding module, then rebuild the hypothesis
  on the reproduction rather than on the trace you started from.
- **Logging.** The topmost frame, the frame the reproduction accused, and how
  precisely correlation matched. Across a corpus that yields both how often traces
  mislead and what your correlation step is worth.
- **Proving test.** Diagnose a real historical issue whose trace points away from
  its fixing commit, then show the run that skips reproduction proposing the wrong
  remedy. The version that accepts the topmost frame fails the diagnosis
  assertion.

## Deliverables

- [ ] Bug pipeline: report → investigation → correlation → reproduction →
      hypothesis → failing test → fix → verification → PR.
- [ ] Labelled corpus of ≥5 historical bugs with root causes and fixing commits.
- [ ] Reproduction gate enforced in code, with a test proving a hypothesis cannot
      be recorded without one.
- [ ] Scorecard: all six metrics across the 5 bugs.
- [ ] Misleading-stack-trace report, five parts, proving test red on the parent.
- [ ] 6 sends logged; discovery script written; call slot held in the calendar.

## Done when

- [ ] 5 historical bugs ran end to end and produced PRs.
- [ ] Every regression test written was verified to fail on the parent commit.
- [ ] Zero hypotheses were accepted without a reproduction, and a test asserts it.
- [ ] Root cause and fix are scored separately, each with its denominator.
- [ ] At least one bug with an innocent topmost frame was diagnosed correctly.
- [ ] Unrelated-change rate is recorded per bug, not averaged away.

## Reflection

1. How deep did the real fault sit relative to the top frame, across five bugs?
   What would have got you there sooner?
2. Where the agent got the fix right but the cause wrong — what does that fix do
   the next time the same cause fires differently?
3. Four weeks in: which single step of these four pipelines fails most, and is
   that where you would have guessed in week 1?

## Evidence

- The five bug PRs, each with its regression test and proof the test failed on
  the parent.
- The labelled corpus and the scorecard against it.
- Correlation precision figures.
- Misleading-stack-trace report and its red-on-parent test.
- Send log; discovery script path.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___

---

**Four weeks done.** Before starting week 5, spend twenty minutes on this: from
your four run logs, list the failures you actually saw — not the ones you expect.
Weeks 5 through 8 add persistence, retries, tracing and concurrency, and each is
only worth building if it answers something on that list. If persistence is not
on it, say so, and reorder.
