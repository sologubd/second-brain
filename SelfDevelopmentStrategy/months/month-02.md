# Month 02 — Retrieval you can measure, and a queue that holds

## Outcome

Retrieval is measured rather than assumed, the platform diagnoses real
production incidents, and several agents work in parallel without losing or
duplicating anything.

Three unrelated-looking strands close together here, and they share one
property: each replaces a belief with a number. A retrieval configuration that
feels better becomes NDCG@5 against a frozen label set. A diagnosis lane that
looks plausible becomes twenty real labelled issues. A queue that seems safe
becomes a chaos run with a stated kill rate.

## Deliverables

- [ ] `D-m02-1` — Secure Knowledge Agent through `SKA-S1`: permission-filtered hybrid retrieval with measured NDCG@5 and MRR, reranking, and a RAG-poisoning attack report.
- [ ] `D-m02-2` — Engineering Agent Platform through `S4`: Sentry diagnosis lane on 20 real labelled issues, and a queue proved clean under a chaos run.
- [ ] `D-m02-3` — Architecture review #2 on the supplied deliberately bad system, plus workflow documentation #1 and an ROI calculation from a measured baseline.
- [ ] `D-m02-4` — M2 retrospective: all ten questions plus `RQ-11`, the mandated canon delta — the funnel recalibration.

Review #2 is the one conducted on somebody else's code. Finding planted defects
in a supplied system demonstrates something a self-review structurally cannot:
that the reviewer can find faults rather than describe their own choices
favourably.

## Funnel targets

Summed from week-files 05 through 08: 22 prospects researched, 32 sends, 48
follow-ups, 1 discovery-call slot planned, 1 workflow documented, 1 opportunity
scored and 1 ROI calculation. Expected replies are 0.62 – 3.28, midpoint 1.95,
on the 41 sends matured by the end of W08. Expected calls attributable to this
period's own sends are 0.380 — the largest of the three derived months, because
this is where most of the sending happens.

This is also the month the funnel stops being a plan and starts being data. The
watch rows sited at W05 and W07 will almost certainly have tripped by now and
changed nothing, exactly as pre-announced; the activation row at W08 is the
first that would change anything, and it is not expected to fire. Counts go to
[the scoreboard](../SCOREBOARD.md) with `evidence_source` on every artifact,
because the delta below reads those counts and cannot read intentions.

## Stages entered

Four: `SKA-S0` and `SKA-S1` on the knowledge agent, `S3` and `S4` on the
platform. `SKA-S1` extends `SKA-S0` and `S4` builds on `S1b` rather than on the
Sentry work, so the two projects advance independently through the month.

Definitions, demo commands and ceilings live in
[the knowledge agent](../projects/secure-knowledge-agent.md) and
[the platform](../projects/engineering-agent-platform.md). `S3` is the month's
dependency risk: it needs a Sentry project carrying real historical issues, and
the misleading stack traces the diagnosis exercise turns on are only available
because that access exists.

## Failure exercises

Four, one per week-file: `EX-FAIL-07` stale documentation at W05, `EX-FAIL-08`
misleading code comments at W06, `EX-FAIL-09` a Sentry event with a misleading
stack trace at W07, and `EX-FAIL-10` two agents modifying overlapping files at
W08.

The first three are a single theme approached from three directions — the
evidence the agent reads is wrong, and nothing in the text says so. The fourth
is different in kind: two correct agents interfering. Bodies live in
[the agent-failure set](../exercises/agent-failures.md); the five-part reports
belong to the week-files.

## Retrospective

All ten, answered at week-file 08. The notes are prompts; the answers are the
deliverable.

1. What can I now build that I could not build 30 days ago? Retrieval you can score is the honest answer here.
2. Which concept remains theoretical? Reranking cost models are a likely candidate.
3. What broke in real usage? The chaos run exists to produce this answer rather than to pass.
4. What did agents repeatedly fail at? Four reports plus the twenty-issue diagnosis corpus feed this.
5. What should become a reusable skill? Look at what the diagnosis lane repeats every time.
6. What should become a deterministic tool instead of an LLM decision? Retrieval metrics already are; ask what else could be.
7. Where did human approval prove necessary? Note where it was skipped and nothing went wrong, too.
8. What business problems appeared repeatedly? Workflow documentation #1 is the first real input to this.
9. What should I stop learning? Answered against the low-ROI table, with any new stop written in as a row.
10. What should I double down on? Canon's follow-up runs alongside it — which deliverables from these four weeks taught you anything you did not already have?

`RQ-11` turns one answer into an edit. Run `make delta MONTH=02`, fill the stub,
edit canon, raise `meta.version`, regenerate, re-check.

## Mandated delta

**Type:** `funnel_recalibration`.

The procedure canon fixes: compare the measured reply rate against the 1.5–8%
band and the measured per-touch attribution against the 42–65% follow-up band,
then rewrite the reply-rate band — or record that the sample was too thin to
support a change at all, stating its size beside that decision.

Why here and not at M1: 41 to 47 matured sends is reached across W08 and W09,
and M1 had only 15 to read. Why the escape hatch is written into the procedure
rather than left to judgement: at 41 matured sends the observable reply rates
are 0%, 2.4%, 4.9% and so on. The resolution is coarse, and a band rewritten on
the strength of one or two replies is noise wearing the clothes of measurement.
Canon therefore requires the denominator to travel with any revised band, which
is what stops a thin month being laundered into a confident number.

Every conversion figure in the model came from vendors selling sending
infrastructure, none of whom separate a solo operator with no case study from an
established team sending at scale. Canon expects this delta to move those
figures, plausibly by a factor of two in either direction.

## Checkpoint

No career checkpoint closes month 02 — `checkpoint_refs` is empty. `CP-M3` is one
month out, and the two evidence ids this month contributes to it are `D-w07-1`
and `D-w08-1`: the Sentry lane and the chaos run.

Both are engineering evidence, and that is the gate's design rather than an
accident of the calendar. This month's business output — a documented workflow,
a scored opportunity, an ROI figure — feeds the M2 delta instead, which is a
different instrument answering a different question.
