# Phase 01 — Foundations

## Arc

Phase 01 covers months [M01](../months/month-01.md), [M02](../months/month-02.md)
and [M03](../months/month-03.md) — the twelve detailed week files, spread across
roughly eighteen calendar weeks.

Entering, there is a senior Python engineer who delegates real work to coding
agents *interactively* and has never operated an idempotent consumer or a
lease-based queue under load, has never shipped or measured retrieval, has done
no structured attack thinking, and has no consulting pipeline whatsoever.

Leaving, there is a system. A task file becomes a reviewed pull request without a
human keystroke; the run survives `kill -9` at any step boundary; several workers
share one queue while a third of them are killed mid-task; answers come from an
index that filters by permission before ranking, scored against a label set
frozen before any tuning; the whole thing has been attacked by its own author
with the success rates written down; and a cold funnel exists that did not exist
in week one.

The phase is not themed by subject and does not own topics, hours or tasks. Every
week here carries at least three tracks at once — that is what makes the
parallelism real rather than declared. The hours live in the week files, the
reasoning lives in the track files.

| | | | |
|---|---|---|---|
| [W01](../weeks/week-01.md) | [W02](../weeks/week-02.md) | [W03](../weeks/week-03.md) | [W04](../weeks/week-04.md) |
| [W05](../weeks/week-05.md) | [W06](../weeks/week-06.md) | [W07](../weeks/week-07.md) | [W08](../weeks/week-08.md) |
| [W09](../weeks/week-09.md) | [W10](../weeks/week-10.md) | [W11](../weeks/week-11.md) | [W12](../weeks/week-12.md) |

Twelve week files, roughly eighteen calendar weeks: a week file is a unit of
work rather than a unit of time, and two floating catch-up weeks absorb what is
left over. **After a missed week, never double up — slip the calendar
instead.** Run that week's named 8-hour subset and let the end date move. Sends
are the one thing that can never be stacked, because replies arrive on a lead
time that additional hours do not shorten.

## Entry conditions

- [ ] A GitHub repository an agent may open pull requests against, with write
      scope confined to it.
- [ ] A Notion workspace API token and a Sentry project holding real historical
      issues — not fixtures.
- [ ] Two coding-agent subscriptions, both drivable as unattended CLI
      subprocesses, plus roughly EUR 200 of metered budget held in reserve for
      the whole twelve months.
- [ ] Postgres running locally. It is the state store, the queue, the lock, the
      outbox and the vector index; nothing else is introduced to duplicate it.
- [ ] Baseline levels recorded in the
      [competency matrix](../reference/competency-matrix.md) before W01, because
      every later target is a delta against them.
- [ ] The four volatile-fact classes read once in
      [the dated snapshot](../resources/ecosystem-snapshot-2026-08.md), and the
      reading order taken from
      [the resource list](../resources/recommended-resources.md).

## Exit conditions

- [ ] D-w03-1 holds: one event replayed 100 times with kills injected produces
      exactly one state transition, one pull request and one dedup row.
- [ ] D-w04-1 holds: a real pull request exists that a verification gate, an
      automated review and a human approval gate all had to pass.
- [ ] D-w08-1 holds: the chaos run strands, loses and duplicates nothing at a
      30% kill rate.
- [ ] D-w06-1 holds: NDCG@5 and MRR are reported per configuration against the
      W05 frozen label set.
- [ ] D-w10-1 holds: three regression tiers gate a merge, with the pass-rate
      threshold stated as a defended statistical bound over N=5 reruns.
- [ ] D-w11-2 and D-w12-2 hold: attack success rate measured against this
      author's own systems, per technique, before and after each structural
      mitigation.
- [ ] D-w12-4 holds: a SaaS verdict, or an explicit non-verdict naming the
      missing threshold and its date. The non-verdict passes.
- [ ] All three retrospectives are closed with their mandated canon deltas
      applied — hours at M01, funnel at M02, ecosystem at M03.

## Checkpoints

Three retrospectives sit inside the phase, at W04, W09 and W12, each producing a
canon delta rather than a diary entry. They are the whole of Track P, the
program pseudo-track, whose hours README states and which is classified as testing by
declaration because a retrospective measures the program rather than a system.
This is the one figure a phase file owns, and it is overhead, not subject
matter.

The phase ends on **CP-M3**, whose decision question and eight evidence ids are
held in [the portfolio file](../reference/portfolio.md) — the unattended
pipeline from D-w01-1 onward, the killed-replay proof, the chaos run and the
regression gate. What belongs *here* is the pass rule: **CP-M3 passes on process
executed, not on calls booked.** The business column at M3 is expected to show
roughly 2.5 replies and probably zero calls. That is the plan working as
predicted.

That expectation is pre-announced now, in week one, rather than discovered in
week eight. Across 52 sends at a 1.5–8% reply band and a 15–35% reply-to-call
band, the programme expects 0.78–4.16 replies and **0–1 calls, planned as 1.**
Zero calls is the *modal* outcome: 53.9% likely at the band midpoint and 23.3%
likely even at the band ceiling. The full derivation lives in
[customer discovery](../business/customer-discovery.md) and the branch itself in
[outreach](../business/outreach.md).

Two classes of threshold follow from that, and the difference between them is
the point. **Watch rows are expected to trip and change nothing** — log the
event to the scoreboard and carry on. **Activation rows sit genuinely below the
band** and trigger a program-level response: an out-of-cycle canon delta
re-pitching the funnel, the Stage-1 simulated track extended for the remaining
business deliverables, and any reclaimed hours drawn from the cut list.

| Row | Condition | Likely outcome | Response |
|---|---|---|---|
| WATCH-1 | 0 replies after 9 matured sends, end of W04 | Trips 65.2% of the time at the band midpoint, 87.4% at its floor | Log only |
| WATCH-2 | 0 booked calls by end of W05, 15 matured sends | Trips 83.7% at the midpoint; still 65.7% at the ceiling | Log only |
| WATCH-3 | ≤1 reply after 33 matured sends, end of W07 | The median row — 53.5% at the midpoint, 91.1% at the floor | Log only |
| WATCH-4 | 0 booked calls by end of W07, 33 matured sends | Trips 67.6% at the midpoint. An expected outcome, not an anomaly | Log only |
| ACT-1 | 0 replies after 41 matured sends, end of W08 | 14.3% at the midpoint, 3.8% at the ceiling, 54.1% at the floor | Activate the branch |
| ACT-2 | 0 replies after all 52 sends have matured, end of W10 | 8.5% at the midpoint, 1.6% at the ceiling, 45.8% at the floor | Activate the branch |

Both activation rows count replies, never calls. A call-count threshold is
structurally impossible here: since zero calls is the median result, a zero-call
event carries almost no information about whether performance is below band, and
a threshold that fires on the median trains its reader to ignore it.

## Security arc

Track D opens late inside this phase and deliberately so: the baseline is
Awareness, and there is nothing worth attacking until an index and a tool surface
exist. W11 provenance-tags ingestion, tiers retrieval by trust, and breaks one
leg of the lethal trifecta structurally rather than filtering for it; D-w11-2
then measures indirect injection and exfiltration against that system. W12 adds
per-tool least-privilege profiles, scoped short-lived tokens and a sandboxed
execution surface, and demonstrates a confused deputy in D-w12-2. The attack
bodies live in [the security exercise set](../exercises/ai-security.md); the
five-part failure reports live in
[the agent-failure set](../exercises/agent-failures.md).

The arc does not close here. It continues into
[phase 03](phase-03-production-ai.md) — tenant isolation and secrets at M04,
memory poisoning against a real memory surface at M05, and authorization
expressed as policy at M06 — and the M05 delta exists precisely to reassess
whether the later months carry enough of it.

## What this phase does not cover

The brief's first-listed flagship workflow — a Notion task through to a reviewed
pull request — **is not built here. It arrives at M04.** Its twelve steps need
the durable state machine, the verification gate and the approval gate
underneath them; building the Notion end first would produce a demo with nothing
behind it. See [phase 02](phase-02-agent-harness.md).

Four other capability areas are deliberately absent and homed forward: the outbox
and the saga teardown at M04, agent memory and its poisoning at M05, policy-based
authorization at M06, and Track F applied rather than merely instrumented at M09.
Schema migrations and API evolution stay at M08. Track E's scoping and pricing
work has no surface until an engagement exists, so it is homed at M04 through
M06 rather than pretended at here.

Also absent by ownership rather than by sequencing: every concept inventory and
every reasoning paragraph, which belong to the track files; every stage
definition and demo command, which belong to the project files; and every
architecture-review body, which belongs to
[the review exercise set](../exercises/architecture-reviews.md) alongside
[the distributed-systems set](../exercises/distributed-systems.md). Phases link;
they do not restate.
