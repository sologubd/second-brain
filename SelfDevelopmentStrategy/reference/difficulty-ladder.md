# Difficulty ladder

## What this is

Nine rungs that every exercise in this repository is pitched against:
**understand → implement → break → debug → measure → secure → operate → explain
→ sell.**

The ladder is a vocabulary, not a schedule. Exercises name the rungs they cover
so that "I did the retrieval work" resolves into something checkable — whether
it was implemented, whether it was measured against a frozen baseline, whether
anyone attacked it.

This file also carries a second list of nine that must not be confused with the
first: the **closing design questions**, which are an outcome requirement rather
than a progression. They are the questions the programme must be able to answer
*against the built systems* by month 12, and each one names the deliverables
that make its answer evidenced rather than asserted.

## The table

| # | Rung | What it means | Exemplar |
|---|---|---|---|
| DL-1 | understand | State the mechanism and the failure it prevents, without code. Most concepts start here already for this reader, which is why almost nothing in this programme stops here. | W01, D-w01-4 |
| DL-2 | implement | Build the thing so it works on the happy path. | W02, D-w02-1 |
| DL-3 | break | Build the *wrong* version first and watch it fail. For a concept-strong, operation-weak learner, seeing the duplicates accumulate is the entire value; being told about them is what they already have. | W03, D-w03-1 |
| DL-4 | debug | Find the cause when the evidence lies — a stack trace pointing away from the fault, a comment describing code that no longer exists. | W07, D-w07-3 |
| DL-5 | measure | Attach a number to a change and prove it moved. A change with no frozen baseline is unfalsifiable. | W06, D-w06-1 |
| DL-6 | secure | Attack it yourself and report the success rate against your own system before and after a structural mitigation. | W11, D-w11-2 |
| DL-7 | operate | Run it under contention and failure and know what it did from telemetry rather than memory. The rung this baseline most needs, and the one most curricula skip. | W09, D-w09-1 |
| DL-8 | explain | Write the ADR, name the accepted defects, and defend the threshold you chose to someone who will push back. | W12, D-w12-3 |
| DL-9 | sell | Convert the capability into a payback period a buyer accepts, or into an honest non-verdict. | W08, D-w08-4 |

The ladder ends at *sell* deliberately. A capability nobody will pay for is a
hobby, and a programme that stops at *operate* cannot tell the difference.

### Closing questions

Nine questions, each with the deliverables that make its answer evidenced. CP-M12
tests all nine against the built systems.

| # | Question | Answerable from |
|---|---|---|
| CQ-1 | Why is this architecture correct? | D-w01-4, D-w04-3, D-w12-3, D-m04-3 — the workflow-versus-agent classification, three architecture reviews, and the saga-versus-outbox defence |
| CQ-2 | What happens when it fails? | D-w03-1, D-w08-1, D-m04-1, D-m04-2 — 100 killed replays, a 30%-kill chaos run, and a compensation-failure suite reaching a defined terminal state rather than hanging |
| CQ-3 | How do we know it works? | D-w06-1, D-w10-1 — retrieval metrics against a frozen label set, and a three-tier gate with a justified statistical threshold |
| CQ-4 | How do we know it remains correct? | D-w10-1, D-w09-1 — the agent regression tier re-executes what ships; a pinned convention version and per-run metadata make a silent upstream change detectable |
| CQ-5 | What can an attacker do? | D-w11-2, D-w12-2, D-m05-2 — measured attack success rate against this author's own system, per technique, before and after each structural mitigation |
| CQ-6 | What should require human approval? | D-w04-1, D-w04-2, D-w12-1 — the placement audit for irreversible or high-impact state changes, with the gate rendering the literal proposed call |
| CQ-7 | What happens at 10× scale? | D-w08-1, D-w09-1 — bounded by what was measured. The chaos run and the quota model say what breaks first: database, quota or disk |
| CQ-8 | How much does it cost? | D-w01-2, D-w09-1, D-w10-1 — measured quota headroom, a composite cost-per-task metric, and a measured judge cost per item, plus the finding that the binding constraint is quota rather than euros |
| CQ-9 | What measurable business value does it create? | D-w08-4, D-w12-4, D-m07-1 — **the weakest-evidenced of the nine, and stated as such.** A return calculation from a measured baseline and a scorecard verdict are real instruments, but under this funnel the baseline may be a simulated Stage-1 one through month 07 |

## How to read it

Rungs are not a syllabus order and no exercise is required to climb all nine. An
exercise names the rungs it covers; that naming is what makes coverage
auditable.

Two floors apply. Every P0 concept must be covered to at least **implement** — a
concept with no build behind it is a P2 or a P3 with a stated reason, not a P0.
And every P0 concept in tracks A, B and D whose failures are invisible to a
generate-and-test loop must be covered to at least **break**, because those are
precisely the failures a model will never surface unprompted.

The exemplar column names the earliest week where a rung is exercised at full
depth, not the only one. *Operate* appears again in every month from 09 onward;
*sell* recurs at every consulting stage transition.

Keep the two lists of nine apart. The rungs describe how hard an exercise is;
the closing questions describe what the finished system must be able to answer.
CQ-9 is marked weak on purpose — averaging it into the other eight would be the
kind of quiet rounding this repository exists to avoid.

## How it changes

The rungs are stable. Nothing in the monthly loop is expected to add or remove
one, and a delta that did would be redefining the vocabulary the whole exercise
set is written against.

The closing questions change only in their `answerable_from` lists, and only
when a deliverable moves. The **M12 retrospective owns that pass**: it tests all
nine against the systems and records, per question, whether the answer is
evidenced, partial or absent. CQ-9's answer in particular must name its
evidence-source tag rather than presenting a simulated baseline as a measured
one.

Edits go through canon's `difficulty_ladder` and
`question_sets.closing_design_questions` blocks, via the loop in
[HOW-TO-EDIT.md](../HOW-TO-EDIT.md).
