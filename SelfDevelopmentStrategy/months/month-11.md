# Month 11 — Reading it as a stranger would

## Outcome

The portfolio reads as evidence to a senior engineer who has never met me.

That reader has no context, no goodwill and no patience for a description of
something. They open one item, look for the number or the command, and decide.
Every item in the collection was built to survive that, but none of them has
been read that way yet, because the person who built a thing cannot easily see
what it fails to say.

The month is thin by decision, and the reason is that an audit cannot be
specified before the artifacts it inspects exist in final form. Three mandated
deltas will have rewritten this plan by now — hours against logged actuals, the
funnel against a measured reply rate, the ecosystem against re-verified
sources — and three checkpoints will have branched it. Writing an inspection
checklist today for objects whose shape those branches determine would produce a
checklist that inspects the wrong things. What resolves the thinness is the
artifacts themselves, once months 01 through 10 have finished producing them.

## Deliverables

- [ ] `D-m11-1` — All ten portfolio items complete, each satisfying its own credibility statement, and each pointing at something that runs or at a number that was measured rather than at an account of either.

The credibility statements are per-item and they are not interchangeable, which
is what makes the audit real work rather than a checklist pass. One item earns
its place by surviving a kill signal at any step boundary; another by shipping a
test that fails against the obvious implementation; another by refusing to send
anything without an approval record. The statements live in
[the portfolio file](../reference/portfolio.md#how-to-read-it), and the audit's
job is to check each claim against the artifact rather than against the
intention behind it.

Two of the ten deserve particular scrutiny. `PF-07` is the external case study
and the item canon expects to be at genuine risk, which is precisely why
substitution in this programme happens one deliverable at a time — so that this
is the last thing to become simulated rather than the first. `PF-05` is the
attack report, and its credibility rests on every figure in it being a
measurement of this author's own systems with a stated denominator. The audit
confirms that no borrowed industry effectiveness figure has crept in to fill a
gap; canon states none because none met a citable standard.

## Funnel targets

The delta sets these; this file does not. But the funnel's numbers stop being a
target this month and become content, which is a change worth naming.

`PF-09` is the discovery-notes item, and its credibility comes from putting the
actual sends and replies next to the plan's own predictions, with each note
tagged `evidence_source` as real or simulated. A first-timer's true conversion
rate shown beside the forecast that preceded it is more persuasive than a good
rate would be, because it demonstrates that the author distinguishes what
happened from what was hoped for.

## Stages entered

None, and none remain. Every stage of the three systems closed by month 08 and
month 10 established that they still start.

What this month uses is not a stage but a property of them: each stage was
required to carry a runnable demo command, and a stage without one was defined
as not having shipped. Those commands are what let an audit test the word
"runnable" instead of asserting it. They belong to
[the engineering platform](../projects/engineering-agent-platform.md),
[the knowledge agent](../projects/secure-knowledge-agent.md) and
[the business agent](../projects/business-operations-agent.md).

## Failure exercises

None assigned. The extended set closed at month 06 and the canonical fourteen
were placed one to a week across the detailed weeks.

The audit does revisit them, from an angle no exercise applies to itself. Each
failure report carries five named parts, and the fifth is a test that proves the
mitigation by failing against the code before it. A report whose proving test no
longer runs, or which now passes against both versions because the surface moved
underneath it, has become a description of an old fix. Finding that is squarely
this month's work, and it is cheaper to find here than in front of the reader
the outcome describes.

## Retrospective

All ten, answered by someone trying to read their own year without sympathy.

1. What can I now build that I could not build 30 days ago? Nothing, probably. The audit month builds no capability and should not pretend otherwise.
2. Which concept remains theoretical? The audit surfaces these faster than any exercise, because an item with no artifact is a concept with a title.
3. What broke in real usage? Re-check month 10's log rather than recalling it.
4. What did agents repeatedly fail at? The accumulated failure reports are the record.
5. What should become a reusable skill? The audit itself, if it happens twice.
6. What should become a deterministic tool instead of an LLM decision? Checking that a demo command still exits cleanly is a script, not a judgement.
7. Where did human approval prove necessary? Publishing is the approval gate this month adds.
8. What business problems appeared repeatedly? The register answers this now; the portfolio has to show it.
9. What should I stop learning? Answered against the low-ROI table. A topic the audit could find no artifact for has largely answered this already.
10. What should I double down on? The follow-up — which of the last four weeks' deliverables taught you something you did not already know? — lands on an audit rather than a build, so a zero says something about the year rather than the month.

`RQ-11` is where an audit finding becomes a canon line. `make delta MONTH=11`
opens the stub.

## Mandated delta

**Type:** `portfolio_credibility_audit`.

Canon's procedure: read all ten credibility statements against the artifacts
that now exist. Rewrite every statement an outside senior engineer could not
verify from the repository alone, and mark any item whose evidence is still
simulated. Then bump `meta.version`, regenerate, re-check.

Note which direction that rewrite runs. The statement is amended to fit the
artifact, never the reverse — a claim that survives only because its author
explains it is the exact thing this audit exists to catch.

One further obligation belongs to this month because the audit is the last
practical moment for it. This repository is private now and capable of being
made public later, which is only true while no tracked file carries a client
name or a prospect's details. Real material lives in gitignored local files and
the tracked copies carry placeholders. Confirming that file by file is part of
the audit, and it is itself a discipline a buyer looks for.

## Checkpoint

The gate is one month away. `CP-M12` reads three deliverable ids and `D-m11-1`
is one of them, sitting beside `D-m09-2` from the scorecard and `D-m12-1`, which
is the decision itself.

That gives this month an unusual weight for a month that builds nothing. One of
the four options at `CP-M12` — remaining primarily on the Staff or AI Engineer
path — is answered almost entirely by `D-m11-1`, and canon is explicit that it
ranks as a first-class outcome and not a fallback. Alone among the four, its
evidence can be assembled here without anyone else agreeing to anything. An
audit that passes is therefore not a formality; it is one whole option kept
open.
