# Scoreboard

Eight metrics. Edit this file by hand. Add a metric only when it would change a
decision; delete one that never has.

Business rows carry `real` or `simulated`. Paid pilots and revenue are **never**
simulated — their whole value is that politeness cannot produce them.

## Weekly — harness and engineering

One row per week. Leave a cell blank rather than guessing.

| Week | Tasks run | Autonomous success | Interventions / task | PR acceptance | Tokens / task | Artifacts shipped | Failures reproduced + mitigated |
|---|---|---|---|---|---|---|---|
| W01 | | | | — | | | |
| W02 | | | | | | | |
| W03 | | | | | | | |
| W04 | | | | | | | |
| W05 | | | | | | | |
| W06 | | | | | | | |
| W07 | | | | | | | |
| W08 | | | | | | | |
| W09 | | | | | | | |
| W10 | | | | | | | |
| W11 | | | | | | | |
| W12 | | | | | | | |

**Autonomous success** — task reached its done-condition with no human writing
code. Report it as a fraction with the denominator visible (`3/5`), not a
percentage, until the denominator is large enough for a percentage to mean
something.

**Interventions / task** — an *approval is not an intervention*; it is the
design. An intervention is a human editing the agent's output or unblocking a
stall.

**PR acceptance** — PRs you would merge, over PRs opened. Starts at W02.

**Tokens / task** — tokens, always. Add a euro figure only if you ever run on a
metered path. Exclude runs stalled by rate limiting, or this measures your
billing plan rather than your system.

**Failures reproduced + mitigated** — counts only when the proving test goes red
on the parent commit. A five-part write-up with no red test is a document.

## Monthly — business

Actual numbers only. Compute rates when the denominator is large enough to
support one; until then, leave the rate column empty. Do not model a funnel
probabilistically before there is a sample.

| Month | Prospects researched | Messages sent | Replies (declines separate) | Discovery calls | Qualified pains | Paid pilots | Revenue | Evidence |
|---|---|---|---|---|---|---|---|---|
| M01 | | | | | | 0 | 0 | |
| M02 | | | | | | | | |
| M03 | | | | | | | | |
| M04 | | | | | | | | |
| M05 | | | | | | | | |
| M06 | | | | | | | | |

**Replies** — log declines separately. A polite no is not progress, and counting
it as one makes a stalled funnel look like a slow-but-working one.

**Qualified pains** — a named person confirmed a specific process is painful,
can state its frequency unprompted, and there is a budget signal. Enthusiasm
without a budget signal is not a qualified pain.

**Evidence** — `real` or `simulated`, plus a path. A workflow document written
from public information is *simulated* and passes.

## Rates, once there is a sample

Fill this in when the denominators are big enough to divide. Not before.

- Reply rate = replies ÷ messages sent (needs ≥30 sends before it means much)
- Reply → call rate = calls ÷ replies
- Autonomous success rate, rolling over the last 20 tasks

## What is not measured, on purpose

Average task duration, retry rate, test-failure recovery rate, ADR count,
workflow count, eval-suite count, prototype count. All were collected in an
earlier version of this plan and none of them ever changed a decision. Duration
and retry rate are mostly noise on a rate-limited plan; the count metrics
reward volume over evidence.
