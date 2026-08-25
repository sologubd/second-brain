# Month 10 — Operating, which is a different verb

## Outcome

The systems built in months 01 to 09 are operated rather than merely built, and
the operating record is the evidence.

Nine months of this programme measured whether something could be made to work
once, under a fault injected on purpose, with the author watching. This month
measures whether it keeps working when nobody is watching and nothing has been
injected. Those are different properties and only the second one is what a buyer
or a hiring engineer is actually asking about.

This is the thinnest month in the plan and the reason is definitional. Its
deliverable is a duration. There is no task list for "kept running", only a
record of having done so, and a task list written here would either invent work
that defeats the purpose or restate the systems that already exist. What would
resolve the thinness is not more planning but the log itself — which cannot be
written in advance, and which the three preceding checkpoints have already
reshaped by the time this month begins.

## Deliverables

- [ ] `D-m10-1` — Sustained operation of the engineering platform, the knowledge agent and the business agent, with the scoreboard filled in each week from what actually ran.

One deliverable, and the temptation it invites is to quietly add a second.
Resist that. A month that builds something new has not operated anything; it has
simply moved the question forward by four weeks. The scoreboard rows are the
artifact, and their value comes from being boring and continuous rather than
impressive and singular.

Business rows carry `evidence_source` as real or simulated throughout, with one
absolute: revenue and paid pilots are never simulated. A logged euro that did
not arrive corrupts every downstream verdict, including the one month 12 has to
make.

## Funnel targets

None are set here either — every calendar month defers to the M2 delta — and
this month the deferral is almost beside the point. An operating month does not
chase a target; it records what the funnel did.

That record has a specific use waiting for it. `ET-5` asks for an acquisition
channel with a measured cost per conversation, drawn from this programme's own
outreach rather than from a published benchmark, on the grounds that an
unmeasured channel is a hope. Ten months of logged sends, follow-ups and replies
is what turns that threshold from an assertion into an arithmetic problem.

## Stages entered

None — and for the first time in the programme that is the headline rather than
a footnote. Every stage of all three systems has been entered and exited by the
end of month 08. Nothing is scheduled to open here, this month or later.

Stage definitions and their demo commands remain where they have always lived,
with [the engineering platform](../projects/engineering-agent-platform.md),
[the knowledge agent](../projects/secure-knowledge-agent.md) and
[the business agent](../projects/business-operations-agent.md). The demo
commands matter more this month than they have since they were written: a system
that will not start from a clean checkout cannot be operated, and discovering
that in month 10 is far better than discovering it in month 11 while auditing a
portfolio.

## Failure exercises

None assigned; the extended set ran out at month 06 and the canonical fourteen
were placed one per week long before that.

The absence is less complete than it looks, though, because this is the month
the earlier exercises are actually tested. Each of them proved a mitigation
against a fault the author injected deliberately, on a day the author was
thinking about that fault. Sustained operation tests the same mitigations under
the condition they usually fail in, which is inattention — a quarantine rule
nobody reviews, a dead-letter queue nobody drains, an expiry nobody notices has
stopped firing. Anything that degrades silently over four unremarkable weeks was
never really mitigated, and this month is the only place in the plan where that
can be found out.

## Retrospective

All ten, answered from the operating log rather than from recollection, which is
the whole point of having kept one.

1. What can I now build that I could not build 30 days ago? Possibly nothing, and that is the correct answer in an operating month.
2. Which concept remains theoretical? Whatever the running systems never exercised.
3. What broke in real usage? This month has the largest sample of real usage in the programme.
4. What did agents repeatedly fail at? Four weeks of unattended runs answer this better than any exercise did.
5. What should become a reusable skill? Whatever operation required doing by hand more than twice.
6. What should become a deterministic tool instead of an LLM decision? Anything the log shows a model deciding identically every time.
7. Where did human approval prove necessary? Note also where it proved to be theatre.
8. What business problems appeared repeatedly? Ten months of discovery notes are now a register, not a pile.
9. What should I stop learning? Answered against the low-ROI table. Four weeks of continuous operation say plainly which knowledge went untouched.
10. What should I double down on? Follow-up: which of the last four weeks' deliverables taught you something you did not already know? A zero from the engineering tracks is expected here and means less than it would elsewhere.

`RQ-11` closes the loop by producing a canon change; `make delta MONTH=10`
writes the stub it goes into.

## Mandated delta

**Type:** `operating_evidence_review`.

Canon's procedure: read the operating evidence — agent-run success rate, human
interventions per task, retry rate and `quota_stall_seconds` from the
scoreboard — and rewrite the harness metric definitions that turned out not to
measure what they claimed. Then bump `meta.version`, regenerate, re-check.

Four metrics, and the rewrite clause is the interesting half. A definition fails
in a specific way: interventions per task counts differently once half of them
are habit rather than necessity, and a retry rate that folds quota stalls into
genuine failures reports a billing plan as a defect. Four weeks of continuous
running is the first sample large enough to show that, which is why the review
sits after an operating month and not before one.

## Checkpoint

Nothing gates month 10, and it is the last month of which that is true.

Its contribution to `CP-M12` is real but indirect. That gate reads `D-m11-1`,
which asserts that all ten portfolio items are complete and that each points at
a runnable artifact rather than at a description — and "runnable" is a claim
this month either substantiates or quietly refutes. An artifact that has been
operated for four weeks is demonstrably runnable. One that has not been started
since the week it was built is a description with a repository attached.
