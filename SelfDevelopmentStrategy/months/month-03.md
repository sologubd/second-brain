# Month 03 — Telemetry, gates, and the agent under attack

## Outcome

The platform can be asked what it did and answer from telemetry; a change cannot
merge without clearing three regression tiers; and the agent has been attacked,
by me, with the results written down.

Phase 1 ends here. What closes is not a feature set but a claim: that the
systems built over twelve week-files can be observed, gated and attacked by
their own author, and that each of those three verbs produced an artifact
somebody else could re-run.

## Deliverables

- [ ] `D-m03-1` — Engineering Agent Platform through `S7b`: observability, cost accounting, evaluation harness with three regression tiers, and security boundaries with a provenance audit log.
- [ ] `D-m03-2` — AI security attack and evaluation report, part 1 of `PF-05`: indirect injection, exfiltration, confused deputy, malicious tool output — all measured against the learner's own system.
- [ ] `D-m03-3` — Architecture review #3 ADR with the five-axis rubric, plus workflow documentation #2 and the SaaS verdict or explicit non-verdict.
- [ ] `D-m03-4` — M3 retrospective: all ten questions, `RQ-11` the mandated canon delta — ecosystem re-verification — and the `CP-M3` evidence pack.

`D-m03-2` carries a constraint worth restating where a reader meets it: every
figure in that report measures this system and carries its own denominator, and
not one industry effectiveness percentage for injection defence appears,
because none of them met a citable standard.

## Funnel targets

Summed from week-files 09 through 12: 0 prospects researched, 5 sends, 39
follow-ups, 0 discovery-call slots planned, 1 workflow documented, 1 opportunity
scored, 1 offer sketched and 1 verdict issued. Cumulative expected replies across
all 52 matured sends are 0.78 – 4.16, midpoint 2.47.

Expected calls attributable to this period is 0.059, and it is the lowest of the
three derived months while cumulative sends are at their highest. That looks
wrong and is not: the figure attributes a call to the period whose sends earned
it, and this period makes only 5 sends. An earlier draft of canon had these
numbers rising through the year and was corrected precisely because the shape
gave it away.

The month's outputs are judgements rather than volume — a documented workflow, a
scored opportunity, a sketched offer, a verdict. All four log to
[the scoreboard](../SCOREBOARD.md) with `evidence_source` marked, and under the
corrected funnel the expected tag on most of them is simulated.

## Stages entered

Four, all on the platform: `S5` observability and cost accounting, `S6` the
evaluation harness and regression gates, then `S7a` and `S7b` for security
boundaries. `S7b` extends `S7a` rather than adding a surface, so the security
work is one arc across two week-files.

`S6` carries the phase's only genuinely binding ceiling: 100 agent executions per
gate pass, which canon names as the constraint rather than euros. Stage
definitions, demo commands and ceilings live in
[the platform file](../projects/engineering-agent-platform.md).

## Failure exercises

Four, closing the canonical fourteen: `EX-FAIL-11` a malicious GitHub issue at
W09, `EX-FAIL-12` conflicting requirements at W10, `EX-FAIL-13` indirect prompt
injection inside a retrieved document at W11, and `EX-FAIL-14` malicious tool
output at W12.

W12 additionally runs the confused-deputy attack, which has no exercise id of
its own and reports through `D-w12-2`. All the bodies live in
[the agent-failure set](../exercises/agent-failures.md), the attack shapes in
[the security exercise set](../exercises/ai-security.md), and the five-part
reports in [week 11](../weeks/week-11.md) and [week 12](../weeks/week-12.md).

## Retrospective

All ten, answered at week-file 12. This is the last retrospective with detailed
weeks underneath it, so the answers are unusually well evidenced.

1. What can I now build that I could not build 30 days ago? Point at the gate and the attack report together.
2. Which concept remains theoretical? Sandboxing was covered at concept level by design; say whether that held.
3. What broke in real usage? The evaluation harness will have found flakiness the tests hid.
4. What did agents repeatedly fail at? Fourteen failure reports now exist; answer across the whole set.
5. What should become a reusable skill? Whatever the attack suite repeated by hand three times.
6. What should become a deterministic tool instead of an LLM decision? Output validation already made this move; name the next one.
7. Where did human approval prove necessary? The approval gates added at `S7b` are the evidence.
8. What business problems appeared repeatedly? The pain register is the input, and its rows carry their own tags.
9. What should I stop learning? Answered from the low-ROI table; anything new becomes a row with a verdict.
10. What should I double down on? Answer it with canon's follow-up in hand, and remember the rule attached: a track that taught nothing across four weeks earns a delta re-pitching it.

`RQ-11` makes the difference between a finding and an edit. Run
`make delta MONTH=03`, then edit canon, raise `meta.version`, regenerate and
re-check.

## Mandated delta

**Type:** `ecosystem_re_verification`.

Re-verify every volatile claim in the dated ecosystem snapshot against its
primary source and record what moved. Canon fixes the priority order: first the
OWASP LLM category numbering, deliberately left unnumbered at authoring time
because a newer list appears to have renumbered one category and was never
refetched from its own PDF; then the OpenTelemetry GenAI convention stability
status; then the subscription quota figures, whose boost carried a published
expiry inside this programme's first year; then the MCP spec revision; then
model pricing.

The reason it can be one pass is that the volatile facts were quarantined into
one dated file at authoring time rather than scattered. Facts with half-lives
measured in weeks age invisibly when they live in seventy-seven places, and no
checker can see them go stale.

Note what this delta does not do. It does not revisit hours — M1 did that — and
it does not revisit the funnel — M2 did. Each of the three phase-1 retrospectives
corrects exactly one class of thing, which is what keeps a retrospective from
becoming a rewrite.

## Checkpoint

`CP-M3` closes phase 1 — the first of the four career checkpoints, and the one
asking whether coding agents can be operated materially better here than an
ordinary senior developer manages. The verbatim question and its evidence list
are held in [the portfolio file](../reference/portfolio.md#the-table). They
divide evenly across the phase: three from month 01 — `D-w01-1`, `D-w03-1` and
`D-w04-1` — two from month 02, `D-w07-1` with `D-w08-1`, and three from this
month: `D-w09-1`, `D-w10-1` and `D-w12-1`.

Between them they show an unattended pipeline taking a real issue to
a reviewed PR, a durable state machine proved effectively-once under a hundred
killed replays, concurrent agents that neither strand nor duplicate under a 30%
kill rate, and a gate that blocks a merge on a justified statistical threshold.

What belongs here is the pass rule. The gate passes on process executed rather
than on calls booked, and the arithmetic is why: the programme expects 0–1 calls
across all 52 sends, with zero the single most likely result. A checkpoint
scored on calls would therefore fail a learner who is precisely on plan, which
is the opposite of what a checkpoint is for. It was pre-announced this way in
week one rather than softened here.

The business column at this gate is expected to read roughly two and a half
replies and no booked call. Record it as measured, tagged, and beside the
prediction it matched.
