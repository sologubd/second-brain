# Customer discovery

The starting position is worth stating plainly: **no warm network, no referral path,
no case study.** Every first touch goes to a stranger found through public sources.
That is the constraint the whole design works inside, and pretending otherwise would
make every number here meaningless.

For the first two months the only goals are **behaviours**, not outcomes:

- choose one test niche
- research prospects against a checklist
- send personalised messages
- have conversations when they happen
- document workflows
- score pains

You control sends, research quality and follow-up discipline. You do not control
replies or calls. A target you cannot miss through effort is not a target — it is a
wish with a number on it.

## Actual numbers, not modelled ones

Log what happened. Divide later.

```
messages sent:       30
replies:              4
declines:             2
discovery calls:      1
qualified pains:      1
```

**Do not model the funnel probabilistically before you have a sample.** An expected
call count of 0.178 is not rigour; it is precision manufactured because numbers look
serious. Once you have ~30 sends, compute a reply rate. Once you have ~10 replies,
compute a reply-to-call rate. Until then the cells stay empty and that is the honest
state.

Counts go in [SCOREBOARD.md](../SCOREBOARD.md), monthly. Real prospect names,
quoted conversations and any prices discussed live in gitignored `*.local.md` files.

**Zero calls for a long time is the normal outcome from a standing start.** Record it
and keep sending. Nothing about that says the plan is failing.

## Company research checklist

Public sources only — no warm introduction, no referral, no contact already known.
Eight fields, each answerable from something published:

1. Legal name, size band, and the country whose employment costs apply.
2. One named repetitive operational process, in the company's own words where
   possible: what goes in, what comes out, who touches it.
3. **The evidence that the process exists** — a job ad describing it, a docs page, a
   filing, a public integration listing.
4. Estimated frequency, with the basis for the estimate stated.
5. Systems involved, and whether each publishes an API.
6. The likely decision-maker's role, and whether that role is reachable at all.
7. **One specific verifiable personalisation fact**, quotable back to them.
8. A disqualifier check: anything that makes this a bad first client — a regulated
   workflow, an obvious incumbent tool, no reachable buyer.

A row missing field 3 or field 7 is **not a prospect, it is a name.** Field 8 exists
because the cheapest prospect to drop is the one dropped before the send.

This checklist doubles as the specification for the Business Operations Agent's
extraction step — a procedure nobody wrote down cannot be automated, so writing it
first is the input rather than paperwork.

## Message shapes

Placeholder identities in anything tracked.

```text
FIRST TOUCH — subject: [specific process] at [Company]
  [First name] — [public signal: job ad / docs page / filing] suggests
  [named manual step] is still done by hand.
  I build Python automation for exactly that step.
  Have I read it right? Twenty minutes would tell us.

FOLLOW-UP 1 (+4 days) — new information, not a reminder
  A second observed signal, or the concrete before/after from your
  documented-workflow artifact.

FOLLOW-UP 2 (+9 days) — narrower ask, then stop
  Replace the meeting request with one answerable question, and say
  plainly that this is the last message.
```

**Two follow-ups per prospect, no more, and each must carry something the previous
touch did not.** A bare check-in costs goodwill and buys nothing. A meaningful
fraction of replies arrive after the first message, so attribute every reply to the
touch that produced it — an aggregate count hides which touch earned them.

Email only, for now. Vendors selling social-outreach tooling report it beating cold
email, and none of that is independently corroborated. This design plausibly leaves
upside unclaimed, and puts no number on it.

**Handling a reply:** hold the slot before the reply exists. Handling one quickly
matters, and a slot you have to go find is a slot you find late. Keep a discovery
slot open in the calendar from week 4 onward.

## Send log

One row per touch, six fields, in one gitignored file:

```
prospect-id | date | shape | signal cited | outcome | real|simulated
```

Outcome is one of exactly four values: `no reply`, `decline`, `reply`,
`call booked`. **Declines are logged separately from replies** — a polite no is not
progress, and counting it as one makes a stalled funnel look like a slow-but-working
one.

## Discovery interview script

Write it in week 4, **before** the first call exists. Someone running their first
call without a script reaches for a pitch, and pitching is how a live prospect
becomes a courteous no.

The whole script is: get them describing a process, and shut up.

1. Walk me through how [process] works today, start to finish.
2. Who touches it, and at what point?
3. How often does it happen? *(If they cannot answer without checking, that is
   itself a finding.)*
4. What happens when it goes wrong? How do you find out?
5. What have you tried? What happened?
6. If this disappeared tomorrow, what would you do with that time?
7. Who else would have to be involved in changing it?

Do not describe your solution. Do not use the word "AI". If they ask what you do,
answer in one sentence and return to their process.

**Afterwards, immediately:** write down what they said in their words, not your
summary of it. Your summary is already the beginning of the pitch you want to give.

## Documenting a workflow you have no access to

The artifact you show when a prospect asks who else you have done this for. It
separates the documentation *skill* from the client *relationship*, which is what
makes progress possible from a standing start.

Pick one company from your prospect list and document one of its workflows end to
end from public information: named steps, estimated frequency, estimated time cost
per occurrence, and the systems each step touches.

**Rules.** Public information only. Every estimate carries its basis. **Every step
that cannot be evidenced is recorded as a gap, never guessed.** Placeholder identity
in the tracked copy. Tagged `simulated`.

*Done when:* ≥5 discrete steps, each with a frequency estimate and its basis; zero
steps asserted without either a source or a gap marker; and the artifact could be
handed to a stranger as evidence that you can document a workflow.

**A workflow document written from public information is `simulated` and it
passes.** The same document presented as a client engagement is a plan failure.
There is no third category, and the tag is the only thing separating them. For the
first several months the simulated path is the *expected* one, not a contingency to
be embarrassed about — which is why this artifact must never be cut.

## Automation audit shape

When you do get a real conversation, this is what you fill in. Placeholder identity
in the tracked copy.

```markdown
# Workflow: <name>   ·  evidence_source: real | simulated

## Steps
| # | Step | Who | System | Frequency | Time per occurrence | Basis |

## Gaps
Steps that could not be evidenced, listed rather than guessed.

## Current cost
Hours per week × fully loaded hourly rate. Every input with its source.

## Automation candidate
Which steps, and what stays human.

## Blockers
Access, permissions, incumbent tooling, regulation.
```

## Two things that end the exercise

**Inventing evidence.** The failure that every tag and every kill criterion in this
plan exists to prevent. An honestly tagged simulated artifact is a passing
deliverable; the same artifact presented as real corrupts every decision downstream,
and no volume target justifies it.

**Re-inflating volumes to feel productive.** Sends are cheap to add and expensive to
personalise. Thirty personalised messages to well-researched prospects beat two
hundred blasts, and the second is also how you learn nothing about the niche.
