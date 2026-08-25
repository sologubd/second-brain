# Month 09 — Track F, applied rather than built

## Outcome

I can say, with evidence, whether a repeated pain across multiple buyers is
worth building a product against.

The instruments for that sentence already exist. A scoring model, seven evidence
thresholds resolved to concrete numbers, and five kill criteria with stated
detection rules were all built inside the twelve detailed weeks. What they have
never had is input. This month supplies it and runs them.

Thinness here is deliberate and it is the checkpoint's fault in the best sense:
`CP-M9` lands at the end of these four weeks and branches everything after them.
Writing month 10 or month 11 in task-level detail from this side of that branch
would be describing one of several futures as though the fork had already been
taken. What resolves the thinness is the checkpoint's own evidence pack, and
nothing earlier.

## Deliverables

- [ ] `D-m09-1` — Track F run for real rather than instrumented: competition analysis used as a kill instrument, a concierge delivery performed by hand, a landing-page test, and paid pilots or pre-sales wherever the evidence carries them.
- [ ] `D-m09-2` — `PF-10`, the opportunity scorecard, populated from the pain register that months 01 through 08 accumulated.

Competition analysis belongs on that list as a *kill* instrument, which is the
unusual framing and the correct one. `KC-5` fires when an existing product
already covers the workflow's main path at a price the buyer would accept, and a
survey run to reassure rather than to disqualify cannot fire it.

## Funnel targets

The M2 delta owns these numbers as it owns every month past 03. What canon does
fix here are thresholds rather than volumes, and thresholds are the harder test.

`ET-1` wants eight independent conversations, the count below which a pain
heard twice could as easily be chance as evidence. `ET-2`
wants that pain in three independent businesses — not three mentions by one
buyer, and not three businesses introduced by one source. `ET-3` wants three
parties willing to pilot, because two can be politeness. `ET-4` wants one
payment or a hard purchase commitment, and one is enough because money is
categorical rather than statistical. `ET-7` wants a single concierge delivery
done by hand, since an outcome you cannot deliver manually automates into an
automated way to deliver nothing. Every count carries `evidence_source`, and a
threshold met with simulated entries is not met.

## Stages entered

No project stage opens or closes here. `S9` finished with month 08 and the three
systems are feature-complete against the plan as written.

Consulting Stage 5 is what this month reaches for — recognising a pain shared
across buyers — and its criteria are the pain register plus the seven
thresholds. Whether it is entered is an evidence question rather than a calendar
one. The stage definitions belong to [Track E](../tracks/consulting.md), the
scoring dimensions to
[the opportunity scorecard](../business/opportunity-scorecard.md), and the
thresholds and kill criteria to
[the validation file](../business/saas-validation.md).

## Failure exercises

None assigned. The five extended rows the calendar months draw on were exhausted
at month 06 and the canonical fourteen were spent one per week much earlier, so
there is no unallocated exercise left to place. Canon leaves the slot empty
rather than inventing one, which is the same rule that keeps every canonical
exercise appearing exactly once.

The month's characteristic failure is not technical anyway. It is a scorecard
that has only ever returned yes. Canon's defence is structural: an explicit
"insufficient evidence, deferred to a named month" is a passing output, and a
framework able to return that is stronger than one that always produces a score,
because a score is always actionable in the direction its author already
preferred.

## Retrospective

All ten, and this month several of them are answered by other people's
behaviour rather than by the system's.

1. What can I now build that I could not build 30 days ago? Judgement counts here, if it is evidenced.
2. Which concept remains theoretical? Anything the register has no entry for.
3. What broke in real usage? The concierge delivery is where this surfaces.
4. What did agents repeatedly fail at? Read against the pilot and concierge runs, not the demo corpus.
5. What should become a reusable skill? The concierge steps done twice by hand are the candidate.
6. What should become a deterministic tool instead of an LLM decision? Scoring against fixed thresholds, plainly.
7. Where did human approval prove necessary? Anything touching a buyer's commitment.
8. What business problems appeared repeatedly? This is the month the question stops being rhetorical.
9. What should I stop learning? Answered against the low-ROI table, and a kill criterion that never fired in twelve months is itself a candidate row.
10. What should I double down on? With the follow-up that makes it answerable — which of the last four weeks' deliverables taught you something you did not already know? Any track at zero of four is re-pitched rather than excused.

`RQ-11` demands an edit rather than an observation. `make delta MONTH=09`
scaffolds it and canon carries it.

## Mandated delta

**Type:** `saas_verdict_review`.

Canon's procedure: read the evidence thresholds against the pain register and
the scored opportunities. Record the verdict, or the explicit non-verdict, since
canon marks a non-verdict as passing. Then rewrite any kill-criteria row that
experience has shown to be untestable, bump `meta.version`, regenerate and
re-check.

That last clause is narrower than it may look, and the distinction matters. A
criterion is untestable when its detection rule cannot be evaluated against
anything the programme collects — `KC-2` asking whether documented workflows
share half their steps needs documented workflows to exist. That is a repair.
Widening a threshold so the evidence finally clears it is not: canon permits the
numbers to be raised on evidence and never lowered without a delta arguing it in
the open.

## Checkpoint

`CP-M9` closes this month, the third career gate, and canon puts it in six
words more directly than any paraphrase manages:

> Can I solve a real company's automation problem end-to-end?

Four deliverable ids answer it, in canon's order: `D-m07-1`, `D-m07-2`,
`D-m09-1`, `D-m09-2`. The first pair arrived in month 07 — the pilot with its
measured baseline, and the agency channel. The second pair is produced here.
Question and list both live in
[the portfolio file](../reference/portfolio.md#the-table).

Of the four gates this is the one a thin funnel threatens most, and canon builds
its evidence bar so that simulation cannot clear it. Should no pilot have
landed, the answer given is *not yet*, carried by the reply rate actually
measured and the denominator it was measured over. A real number describing a
real shortfall is an answer; a demonstration wearing the clothes of a result is
not.
