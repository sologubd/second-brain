# Phase 04 — Consulting

## Arc

Phase 04 spans [M07](../months/month-07.md) and [M08](../months/month-08.md).

This is the phase where the evidence has to come from someone else. Every
instrument built so far measures the author's own system against the author's
own baseline. Consulting Stage 2 does not: it requires that a real external
party's process is measurably different after the work, that the before and
after baseline was *measured* rather than estimated, and that the scope was
fixed in writing before anything started and was not exceeded.

Entering, the programme holds a portfolio of systems and a funnel that has run
for twelve weeks. Leaving, one of two things is true and both are acceptable
outcomes provided they are stated honestly. Either someone outside this
repository has a measurably better week because of something built here — the
case study that becomes portfolio item PF-07, with real identities kept in a
gitignored local file and the tracked version carrying placeholders — or the
funnel did not produce a pilot, the Stage-1 simulated track continues, and the
month records the actual reply rate with its denominator instead of a
substitute presented as an answer.

That second branch is not a failure state. It is the modal one, and the
programme was designed with it in view: substitution happens one deliverable at
a time, automatically, tagged, precisely so that PF-07 is the last thing to
become simulated rather than the first.

The subcontracting side-quest also opens here, and only here. Contacting niche
automation agencies before a pilot artifact exists is a cold pitch with nothing
attached; after one exists it is a channel. Three to five agencies, with what
each asked for recorded — a small target, because it is a footnote to outreach
rather than a funnel of its own.

M08 turns the engineering side inward for one deliverable. The platform's own
schema and its inter-stage interfaces now have enough history to need governed
evolution, so one ADR covers both, applying deprecate-then-remove with a stated
floor rather than yank-and-break. And Stage 4 packages whatever has been
delivered twice into a fixed-scope, fixed-price offer a buyer can accept without
a bespoke proposal.

A slipped month here slips the calendar. Pilot lead times are external and no
amount of weekly hours compresses them.

## Entry conditions

- [ ] CP-M6 is answered with its evidence pack assembled.
- [ ] The M06 competency reassessment is applied, so any target claimed without
      a deliverable id has already been downgraded or re-planned.
- [ ] The productized offer from D-m06-3 exists — fixed scope, stated payback
      period — because a pilot negotiated without one becomes an open-ended
      favour.
- [ ] The qualification checklist and offer structure in
      [the consulting offer file](../business/consulting-offer.md) are current,
      and the discovery notes carry their evidence-source tags.
- [ ] The funnel position is stated as a number with its denominator, not as an
      impression, before any pilot is scoped.

## Exit conditions

- [ ] D-m07-1 holds, or its absence is recorded with the measured reply rate and
      denominator that explain it: a completed Stage-2 pilot with a measured
      before-and-after baseline, written up as PF-07 with placeholder
      identities in the tracked copy.
- [ ] D-m07-2 holds: three to five niche automation agencies contacted with a
      pilot artifact in hand, and what each asked for recorded.
- [ ] D-m07-3 holds: paid pilots or pre-sales where the evidence supports them,
      and an explicit non-verdict where it does not.
- [ ] D-m08-1 holds: one ADR covering schema migrations and internal API
      evolution for the task tables and the inter-stage surface, applying
      deprecate-then-remove with a floor.
- [ ] D-m08-2 holds: a repeatable offer, meaning the same shape of work
      delivered at least twice and describable without a bespoke proposal.
- [ ] The M07 offer recalibration and the M08 cut-list review are both written.

## Checkpoints

No career checkpoint closes this phase. CP-M6 opened it and CP-M9 closes
[phase 05](phase-05-productization.md), which is where the end-to-end question
is actually put. Siting it at the end of M09 rather than M08 gives a pilot begun
in M07 a full quarter to complete, which is roughly what an external engagement
takes.

Two mandated deltas gate the phase. M07 recalibrates the offer against whatever
the pilot or its absence revealed about scope and price. M08 reviews the cut
list itself — which rows were drawn, what they broke downstream, and whether
rows that were never drawn should be retired. Track B rows carry a pre-tag and a
written warning: that track sits at a declared hard floor, and drawing from it
requires an explicit justification recorded in the retrospective that drew it.
It is not an available trade.

Consulting stage progression is the phase's real instrument, and it does not
promote on elapsed time. A stage whose exit criteria are unmet is not exited
regardless of how many months have passed.

## Security arc

No new Track D topic is scheduled at M07 or M08. The arc's planned depth closes
at M06 with policy-based authorization, and that is a stated position rather
than an oversight.

What changes here is not the curriculum but the threat model's context. A pilot
puts someone else's data inside a system whose trust boundaries were designed
against the author's own corpus, and the least-privilege profiles from D-w12-1
and the provenance audit log now have to hold against an environment nobody
here controls. The scope document is part of that: a fixed written scope is also
a bounded blast radius. Any pilot that would require a new tool surface reopens
the threat model rather than inheriting one.

The M05 delta is the only sanctioned route to putting more Track D depth into
this window, and it is asked before this phase begins.

## What this phase does not cover

Two brief topics land in these two months rather than going unassigned: schema
migrations and API evolution, both at M08. Track E's remaining
progression — the case study, the subcontracting channel, and Stage 4 packaging
— is homed at M07 and M08 and belongs to those month files, not to this one.

Not covered here: the competition analysis, concierge build, landing-page test
and pre-sales work, all of which need the accumulated pain register this phase
is still filling. They are homed at M09.

Also absent by ownership: the scripts, the qualification checklist, the scored
dimensions and the kill criteria, which belong to the business files; the
concept inventory, which belongs to
[Track E](../tracks/consulting.md); and hours and tasks, which no phase file
carries.
