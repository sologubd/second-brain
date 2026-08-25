# AI-Native Engineering Roadmap

A one-year apprenticeship for a senior Python developer who wants to stay the
person who *builds the systems* as coding itself gets automated.

Twelve detailed weeks, then nine months that get deliberately vaguer the further
out they go. Three real projects. Plain Markdown — edit any file directly.

## Objective

> I can independently design, build, evaluate, secure, operate and commercialize
> AI-native software systems, while using coding agents to multiply my
> engineering throughput.

The failure form to avoid is **"I know AI tools."** That sentence names no
artifact and cannot be checked.

## Principles

**Ability to build > knowledge.** Every topic ends in something that runs or a
measured number with its denominator stated. *I read/watched/studied X* is never
completion.

**Depth belongs in the projects, not in the roadmap.** This repository is
intentionally boring. If you need to understand its structure before you can
start a week, it has failed.

**Earn complexity.** Add a mechanism after a documented problem proves you need
it, not before. Pain → pattern, never pattern → invented pain.

| Mechanism | Introduce it after |
|---|---|
| Persistence | you lose useful state to a restart |
| Retries | you observe a recoverable failure |
| Idempotency | a duplicate execution causes a harmful effect |
| Queue | parallel tasks actually need coordination |
| Locks | you demonstrate a real conflicting access |
| Provider abstraction | you actually support a second harness |
| Vector database | retrieval scale or metadata queries justify it |
| Agent hierarchy | a single-agent workflow measurably underperforms |

**Climb the ladder, in order.** understand → build → break → debug → measure →
secure → operate → sell. Most curricula stop at *build*. The rungs after it are
where the value is.

**Attack what you built.** Every security topic ends in an attack against your
own system, with the success rate measured before and after one structural
mitigation. No borrowed industry percentages — a number about somebody else's
system proves nothing about yours.

**Tag your evidence.** Business artifacts are marked `real` or `simulated`. A
simulated artifact honestly tagged is a pass. A simulated artifact presented as
real is the one failure that corrupts everything downstream.

## The three projects

**[Engineering Agent Platform](projects/engineering-agent-platform.md)** — the
flagship, and the only one that never finishes. A capability backlog running from
"task file becomes a diff" to a multi-workflow harness with evals, tracing, cost
accounting and enforced trust boundaries. Weeks 1–9 and 12 all build here.

**[Secure Knowledge Agent](projects/secure-knowledge-agent.md)** — question
answering over a private corpus where *who is asking changes what may be
retrieved*, and every answer cites its chunks. Where retrieval, evaluation and
the AI-security work live. Weeks 10–11.

**[Business Operations Agent](projects/business-operations-agent.md)** — reads an
inbound document, extracts structure, proposes an action, then stops and waits
for a person. It builds your own outreach funnel, and it is the only home for
agent memory. Weeks 3, 4 and the months.

## The 12-week foundation

| Week | What you build |
|---|---|
| [01](weeks/week-01.md) | Minimal useful harness: task file → worktree → agent → diff → tests |
| [02](weeks/week-02.md) | Task → verified pull request |
| [03](weeks/week-03.md) | Feature workflow: issue → plan → implementation → review → PR |
| [04](weeks/week-04.md) | Bug workflow: report → reproduction → regression test → fix → PR |
| [05](weeks/week-05.md) | Persistence, restart and resume |
| [06](weeks/week-06.md) | Retries, idempotency and duplicate effects |
| [07](weeks/week-07.md) | Observability, tracing and cost accounting |
| [08](weeks/week-08.md) | Parallel tasks: queues, leases, worktree conflicts |
| [09](weeks/week-09.md) | Agent evals and regression gates |
| [10](weeks/week-10.md) | Retrieval: the Secure Knowledge Agent |
| [11](weeks/week-11.md) | AI security and adversarial testing |
| [12](weeks/week-12.md) | Least privilege, sandboxing, approval boundaries, retrospective |

Weeks 1–4 exist to prove the workflow is useful. Weeks 5–8 add infrastructure in
response to failures those weeks actually produced. Nothing durable, queued or
distributed is built before something breaks that needs it.

## After the twelve weeks

[Months 4–6](later/months-04-06.md) · [Months 7–9](later/months-07-09.md) ·
[Months 10–12](later/months-10-12.md)

Each carries a capability, a project milestone, a business goal, a measurable
checkpoint and a decision point — and nothing more. Detailed tasks for month 11
written today would be a guess wearing a schedule.

## How to work a week

1. Open the week file. Read the whole thing; it fits on a couple of screens.
2. Build. Use your own real project or a small sandbox repo — never toy tasks
   invented to suit the exercise.
3. Run the failure exercise. **The proving test must go red against the code as
   it was before the fix.** Run it on the parent commit first. If it does not
   fail there, you have not reproduced the failure.
4. Tick the deliverables. Fill in `## Evidence` with paths and links.
5. Update [SCOREBOARD.md](SCOREBOARD.md). Ten minutes.

**Roughly 15 hours a week**: 2–3h learning, 8–10h building and testing, 2–3h
business and discovery. A week file is a unit of work, not a unit of time.

**If unfinished, continue next week. Do not double the workload.** Slip the
calendar. Twelve week-files will probably take sixteen to eighteen calendar
weeks, and that is the plan, not a slip.

## How progress is measured

[SCOREBOARD.md](SCOREBOARD.md) — eight metrics, hand-edited Markdown. A metric
that does not change a decision gets deleted.

The harder test is credibility: for each artifact, why would a senior engineer or
a prospective client who has never met you believe it? Answers that work look
like *it survives `kill -9` at any step boundary and here is the replay demo*,
or *the permission pre-filter ships with a reproducible case where the naive
version silently drops authorized results*. Answers that don't: a screenshot, a
certificate, a description.

## Before week 1

- Python 3.12+ in a virtualenv; Git 2.35+ (`git worktree list` must answer).
- Your coding-agent CLI, signed in through the subscription rather than a
  metered API key. That boundary is the whole cost model.
- A repository the runner can operate on — your own real project, or a throwaway
  sandbox beside this one. Not this repository: there is no application code
  here for an agent to change.
- `.env` in `.gitignore`. Real prospect names, client figures and interview notes
  go in `*.local.md` files, already gitignored. **This repository must stay
  publishable at any moment with no scrub pass.**

Then open [week 01](weeks/week-01.md).

## Repository map

```
README.md ROADMAP.md SCOREBOARD.md RESOURCES.md
weeks/     week-01..12.md        the twelve detailed weeks
later/     months-04-06, 07-09, 10-12   thinner, further out
projects/  the three systems, as capability backlogs
exercises/ agent-failures, ai-security, architecture (+ two supplied bad systems)
business/  customer-discovery, consulting-and-saas
```

That is the whole structure. There is no schema, no generator, no canonical
source, no validation step. To change week 5, edit `weeks/week-05.md`.
