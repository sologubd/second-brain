# Month 08 — Changing a running system on purpose

## Outcome

The platform's own schema and internal interfaces can evolve without a rewrite,
and the decision is recorded once rather than re-litigated.

Eight months of accumulated task tables and inter-stage calls is the point at
which "just change it" stops being free. The deliverable is not a migration
framework; it is a governing rule written down once so the next change argues
against a record instead of against memory.

This is also the point where the plan's thinness becomes visible, and it is
chosen. Migrations and interface evolution are both triaged at the third
priority band, and canon's coverage for them is exactly one architecture
decision record — not a topic list with an unstated ceiling. There is nothing
further to specify because the ceiling *is* the specification, and expanding it
into week-level work would be quietly promoting two deferred topics past better
ones.

## Deliverables

- [ ] `D-m08-1` — One decision record covering both schema migrations and internal API evolution, scoped to the task tables and the surface between stages, and applying deprecate-then-remove against a stated floor rather than removing on the spot. This is the fourth and final entry in the ADR collection, closing `PF-04`.
- [ ] `D-m08-2` — The repeatable offer: consulting Stage 4, meaning work of the same shape delivered at least twice and described tightly enough that a buyer can accept it without a proposal written for them alone.

Two deliverables is the whole month, which is unusual and deliberate. One is a
document that has to be right once; the other cannot be manufactured at all
unless the delivery history already exists.

## Funnel targets

None stated. Canon defers every month from 04 onward to the M2 delta, and no
number invented at authoring time would survive contact with a measured reply
rate.

The relevant threshold this month is not a funnel figure but a stage criterion:
Stage 4 requires the same shape of work delivered twice, and twice is a count of
completed engagements rather than of conversations. If only one exists, the
stage is not exited — canon is explicit that elapsed months never promote a
consulting stage. Discovery and delivery records continue to carry
`evidence_source` as real or simulated, and a packaged offer assembled from
simulated deliveries would be a brochure.

## Stages entered

None begins here. `S9` has been open since month 05 and closes at the end of
this one, which is what makes the architecture lane the right home for
`D-m08-1`: the ADR pipeline that turns a request into a decision record is the
mechanism, and this month gives it its last request.

Stage definitions, entry and exit criteria, demo commands and ceilings live with
[the engineering platform](../projects/engineering-agent-platform.md). Consulting
stage semantics belong to [Track E](../tracks/consulting.md), and the offer's
structure to
[the consulting offer file](../business/consulting-offer.md).

## Failure exercises

None. The extended set that the calendar months draw from contains five rows and
all five are spent by the end of month 06; the fourteen canonical exercises were
allocated one per week across the detailed weeks. Canon assigns nothing here
rather than manufacturing a row to fill a heading, which is the same discipline
that keeps each of the fourteen appearing in exactly one week.

There is a failure mode in this month all the same, and the ADR is what
addresses it. Removing an interface that something still calls, or migrating a
table without a floor beneath the old shape, breaks callers that no test in this
repository exercises. The governing rule exists because that failure is silent
and arrives later.

## Retrospective

All ten, answered against two deliverables rather than a busy month. A thin
month with honest answers beats a full one with remembered ones.

1. What can I now build that I could not build 30 days ago? Changing a schema safely counts as a capability.
2. Which concept remains theoretical? Most of the migration space, on purpose — one record is the whole coverage.
3. What broke in real usage? Interface changes break at the caller, so look outward.
4. What did agents repeatedly fail at? `S9` closes this month; its record is now four months long.
5. What should become a reusable skill? Whatever the ADR pipeline needed explaining twice.
6. What should become a deterministic tool instead of an LLM decision? Migration safety checks are a strong candidate.
7. Where did human approval prove necessary? Removal, more than addition.
8. What business problems appeared repeatedly? Repetition is precisely what `D-m08-2` packages.
9. What should I stop learning? Answered against the low-ROI table. Whatever the migration record proved safe to defer belongs there, with its reasoning rather than just its name.
10. What should I double down on? Follow-up attached: which of the last four weeks' deliverables taught you something you did not already know? A two-deliverable month makes a zero easier to score honestly and harder to wave away.

`RQ-11` is the eleventh output and it is an edit, not an observation. Scaffold
it with `make delta MONTH=08` and land it in canon before this month is
considered closed.

## Mandated delta

**Type:** `cut_list_review`.

Canon's procedure: read the cut list against what was actually cut in months 01
through 07. Drop rows the programme no longer needs, add rows the month-01 and
month-04 recalibrations created, and re-tag by track so the Track B rows stay
visible. Then bump `meta.version`, regenerate, re-check.

The list being read is twelve rows deep, each carrying the hours it reclaims and
the downstream dependencies drawing it would break, under a fixed draw order
that spends aggregate business slack before anything else.

The re-tagging clause is why three of the twelve are marked before anyone
considers them: they draw on the track already sitting at a declared hard floor
of 39.0 h after losing roughly eighteen hours across three earlier revisions.
Drawing one takes a written justification in the retrospective that drew it, and
that pre-tag has to survive the rewrite. A row that was never drawn in seven
months is a candidate for removal rather than a reserve — carrying it forward
records slack the programme does not actually have.

## Checkpoint

No gate falls in this month, and — unusually — none of its deliverables appears
in the next gate's evidence list either. `CP-M9` is answered by two ids from
month 07 and two from month 09; month 08 contributes neither.

That is not a hole. `D-m08-1` completes the ADR collection, and the collection
is one of the ten portfolio items whose completeness `D-m11-1` asserts — and
`D-m11-1` is one of the three ids answering `CP-M12`. The contribution is real
and it is one step longer than usual, which is worth stating plainly so that a
reader checking this month against `CP-M9` does not conclude the month was idle.
