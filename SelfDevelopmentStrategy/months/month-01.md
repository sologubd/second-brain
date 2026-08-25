# Month 01 — Task file to approved pull request

## Outcome

A coding agent runs unattended from a task file to an approved pull request, and
every step it takes is durably recorded before it happens.

Read "month 01" as week-files 01 through 04, not as four calendar weeks. The
programme measures a week in work: a file whose real effort runs past its 15.0 h
budget spans extra days rather than losing scope, and the twelve of them span
roughly 18 calendar weeks in total — sixteen working, two left floating — a
figure raised on audit evidence rather than on preference. M1 is
anchored to week-file 04 and to no date, so under that longer calendar it lands
nearer calendar week five or six. That is strictly better for the job it has,
because it reads more logged hours before it corrects anything.

## Deliverables

- [ ] `D-m01-1` — Engineering Agent Platform through S2: runner, durable state machine, effectively-once proof, verification and approval gates, real PRs.
- [ ] `D-m01-2` — Business Operations Agent through BOA-S1: structured extraction plus draft-only outreach with an approval gate and audit trail.
- [ ] `D-m01-3` — Architecture review #1 ADR and the versioned generated-code review checklist, the instrument and the result delivered together.
- [ ] `D-m01-4` — M1 retrospective: all ten questions plus `RQ-11`, the mandated canon delta — the hour recalibration against four weeks of logged actuals.

## Funnel targets

Summed from week-files 01 through 04: 34 prospects researched, 15 sends, 17
follow-ups, 1 discovery-call slot planned, 1 workflow rehearsed, 0 workflows
documented and 0 opportunities scored. Expected replies are 0.22 – 1.20,
midpoint 0.71, against 15 matured sends.

One key is deliberately not a sum. Expected calls is recomputed from this
period's own sends — 0.178 at the band midpoint, or 15 × 0.011875 — because only
two week-files carry a week-level figure and adding those two gives 0.071
instead. Canon writes the exception down rather than leaving a later reader to
discover that the published number and the visible arithmetic disagree.

Nothing documented and nothing scored is a schedule rather than an omission: W03
rehearses the interview, and the workflow documents themselves land in the two
months after this one. Counts go to [the scoreboard](../SCOREBOARD.md), every
artifact tagged `evidence_source` as real or simulated.

## Stages entered

Six: `S0`, `S1a`, `S1b` and `S2` on the platform, `BOA-S0` and `BOA-S1` on the
operations agent. Two of those extend their predecessor rather than opening new
ground — `S1b` on `S1a`, `BOA-S1` on `BOA-S0` — so six stages arrive across four
genuinely new surfaces.

Entry and exit conditions, runnable demo commands, cost and quota ceilings all
belong to [the platform](../projects/engineering-agent-platform.md) and
[the operations agent](../projects/business-operations-agent.md). The hours that
reach them belong to the week-files.

## Failure exercises

Six, more than any other month carries: `EX-FAIL-01` the ambiguous ticket at W01;
`EX-FAIL-02` context loss after restart at W02; `EX-FAIL-03` partial tool failure
and `EX-FAIL-04` model timeout, both at W03; then `EX-FAIL-05` the flaky test and
`EX-FAIL-06` a CI failure unrelated to the change, both at W04.

Fourteen exercises cannot sit one per week across twelve weeks. Canon resolves
that by doubling up W03 and W04 and recording the distribution, so the invariant
that each of the fourteen appears in exactly one week row survives. Bodies live
in [the agent-failure set](../exercises/agent-failures.md) and the five-part
reports in the week-files that run them.

## Retrospective

All ten are answered here, at week-file 04, and the note after each is a prompt
rather than a substitute for an answer.

1. What can I now build that I could not build 30 days ago? Answer with a demo command someone else could run.
2. Which concept remains theoretical? Name it against the concept tables, not from memory.
3. What broke in real usage? The killed-replay work will have found things the tests did not.
4. What did agents repeatedly fail at? Six failure reports already exist; read across them.
5. What should become a reusable skill? A procedure repeated identically in three weeks is the candidate.
6. What should become a deterministic tool instead of an LLM decision? Anything already expressible as a rule qualifies.
7. Where did human approval prove necessary? The approval-gate placement audit answers this with evidence.
8. What business problems appeared repeatedly? Fifteen sends is thin; say so if nothing recurred.
9. What should I stop learning? Answered against the low-ROI table; a new stop becomes a row there with its verdict.
10. What should I double down on? Canon attaches a follow-up: of the last four weeks' deliverables, which taught you something you did not already know? A track scoring nothing out of four earns a delta re-pitching it.

`RQ-11` is the eleventh output and this programme's own addition: the ten answers
produce findings and the eleventh turns one into an edit. Run
`make delta MONTH=01`, fill the stub, edit canon, raise `meta.version`, then
regenerate and re-check. Without it the retrospective is a diary.

## Mandated delta

**Type:** `hour_recalibration`.

The procedure canon fixes: compare four weeks of logged actual hours in the
`user:actuals` regions against plan, per bucket; rewrite the hours for week-files
05 through 12; and above a 15% overrun in any bucket, draw on the cut list.

This is the programme's only self-correction instrument, and its placement is
argued rather than assumed. The learner's own clock is the one measurement in
the whole design that is uncorrelated with the estimates, and week-file 04 is the
first moment it has said anything at all. What it cannot yet speak to is the
funnel: 15 matured sends is far too thin a sample, which is exactly why the
funnel recalibration waits for M2 and this delta touches hours alone.

One conditional rides along. If W01's headroom measurement came in below twice
the planned weekly run count, and no out-of-cycle delta was raised at the time,
quota is recalibrated here too.

The regions this reads are preserved byte-for-byte when the generated files are
rewritten, which is the whole reason the shape is fixed. Four identically shaped
buckets can be parsed and corrected; four narratives cannot, and a week never
logged cannot be corrected at all.

## Checkpoint

No career checkpoint closes this month — `checkpoint_refs` is empty for M01. The
gate it feeds is `CP-M3`, landing at the end of week-file 12, and three of that
gate's eight evidence ids are produced here: `D-w01-1`, `D-w03-1` and `D-w04-1`.

That is the job this section does in a month with no gate of its own. Someone
opening month 01 partway through the programme should be able to see how far the
next decision point is and what is already accumulating toward it, rather than
find a heading standing over nothing.
