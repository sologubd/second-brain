# Month 12 — The decision, and what earned it

## Outcome

I choose a direction on evidence I collected rather than on a preference I
started with.

Twelve months earlier that preference existed and was probably strong. The
programme's entire instrumentation — logged hours, a measured reply rate, attack
success rates with denominators, a scorecard that can return no — was built so
that the preference and the evidence could be told apart at this point instead
of quietly merging.

This month is deliberately thin, and thin for a reason no other month shares:
its content is a decision, and specifying a decision in advance is making it. A
file that said today which of the four directions the year should end on would
be the exact failure the whole apparatus exists to prevent. What resolves the
thinness is the evidence pack, and the evidence pack is assembled from months
that have not happened.

## Deliverables

- [ ] `D-m12-1` — The `CP-M12` decision with its evidence pack: consulting, a productized offer, a micro-SaaS, or the Staff and AI Engineer route as the primary one.

Each option carries its own bar and the bars are not comparable, which is what
stops the decision collapsing into a preference with citations attached.
Consulting needs at least one paid fixed-scope engagement actually delivered.
Productizing needs work of one shape delivered twice over. Micro-SaaS needs all
seven evidence thresholds met, not most of them. The Staff and AI Engineer route
needs the ten portfolio items finished with their credibility statements
holding.

Three of those four depend on other people. One does not, and canon is direct
about what follows: the engineering route is a first-class result, not the
outcome you settle for when the funnel disappoints. It is also the only bar this
programme can clear on its own effort, which is a fact about the evidence rather
than about ambition.

## Funnel targets

Unset here, as in every calendar month past 03 — the M2 delta owns them.

This is the last month in which that matters, and the funnel's twelve-month
record has stopped being a target and become testimony. Two of the four options
are argued directly from it: whether money ever changed hands, and whether a
channel with a measured cost per conversation exists at all. Both readings are
only as good as the `evidence_source` tags applied along the way, which is why
the tag was never optional and why revenue was never allowed to carry a
simulated one.

## Stages entered

None. Nothing new begins in a month whose output is a judgement, and every stage
of the three systems closed at month 08.

What does get exercised one final time is the set of runnable demo commands,
because the decision's evidence pack points at artifacts and an artifact that
will not start is a claim. Those commands live with
[the business agent](../projects/business-operations-agent.md),
[the knowledge agent](../projects/secure-knowledge-agent.md) and
[the engineering platform](../projects/engineering-agent-platform.md).

## Failure exercises

Canon assigns none. Every extended row was spent by the end of month 06, and the
canonical fourteen went one to a week well before that.

The failure this month risks is not one an exercise could rehearse. It is
choosing the option that was always wanted and assembling the citations
afterwards, which produces something indistinguishable from evidence to everyone
including its author. Canon's defences against it are structural rather than
attitudinal: each option has a categorical bar rather than a score, so no amount
of partial progress on three of them adds up to one; and an explicit deferral,
naming the missing threshold and the month by which it could be met, is a
passing output. A framework that can return *not yet* is stronger than one that
always returns something, because something is always encouraging.

## Retrospective

All ten, for the twelfth time, and the comparison across twelve identical
askings is most of their value.

1. What can I now build that I could not build 30 days ago? Read this row across all twelve months at once; the shape of the year is in the sequence.
2. Which concept remains theoretical? Whatever is still theoretical after twelve months is a genuine finding, not a gap.
3. What broke in real usage? Compare against month 10's operating log rather than against impressions.
4. What did agents repeatedly fail at? Twelve months of failure reports answer this with a distribution.
5. What should become a reusable skill? Anything that recurred in every quarter.
6. What should become a deterministic tool instead of an LLM decision? The year-long answer is more interesting than any single month's.
7. Where did human approval prove necessary? And where did twelve months of evidence show it was ceremony?
8. What business problems appeared repeatedly? This feeds the decision directly.
9. What should I stop learning? Answered against the low-ROI table for the last time under this canon; year two inherits whatever the rows say.
10. What should I double down on? Asked for the twelfth time, with its follow-up: which of the last four weeks' deliverables taught you something you did not already know? Twelve answers read together are what the year-two rewrite works from.

`RQ-11` here is not one edit but the whole rewrite. `make delta MONTH=12`
scaffolds it.

## Mandated delta

**Type:** `year_two_canon_rewrite`.

Canon's procedure: read the four checkpoint decisions and twelve months of
logged actuals, then rewrite `meta`, `tracks`, `funnel` and `cut_list` for year
two against what the year measured rather than what it assumed. Canon calls this
the delta the whole control loop exists to make possible. Then bump
`meta.version`, regenerate, re-check.

Four top-level blocks is a different scale of edit from anything the eleven
earlier deltas attempted, and that is the point: this is not a correction to a
row, it is the successor plan. Three of those earlier deltas already
recalibrated the instruments it inherits — hours against a real clock, the
funnel against a real reply rate, the ecosystem against re-verified primary
sources — so year two opens from measurements rather than from the assumptions
this canon opened with. The one obligation it carries is the one every
checkpoint carries: it must not answer a question the evidence does not support,
and a named deferral with a date is always available instead.

## Checkpoint

`CP-M12` is this month, and the last of the four. Canon's wording, which names
all four directions inside the question itself:

> Do I have enough repeated customer evidence to: pursue consulting, productize
> an offer, build a micro-SaaS, or stay primarily on the Staff/AI Engineer path?

Three deliverable ids answer it, in canon's order: `D-m09-2`, `D-m11-1`,
`D-m12-1` — the opportunity scorecard with whatever verdict or deferral it
returned, the audited portfolio, and the decision itself with its pack. The
question and the list are held in
[the portfolio file](../reference/portfolio.md#the-table).

The month also puts the nine closing design questions to the built systems,
each answered from named deliverable ids rather than in the abstract — why the
architecture is correct, what happens when it fails, how anyone knows it works
and keeps working, what an attacker can do, what should need approval, what
happens at ten times the scale, what it costs, and what measurable business
value it creates. That last one, `CQ-9`, is the weakest-evidenced of the nine
and canon labels it so rather than averaging it quietly into the other eight.
The questions and their evidence ids live in
[the difficulty ladder](../reference/difficulty-ladder.md#closing-questions).
