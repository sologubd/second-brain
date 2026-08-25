# Months 7–9 — Evidence from someone else

Thinner still, and for a structural reason: the central deliverable here runs on a
clock nobody in this repository controls. A pilot arrives when a reply arrives, and
week-level tasks written against that would be a schedule for someone else's
calendar.

**Rewrite this file once month 6 has closed.**

## Capability

**Delivering to someone who is not you.** Every instrument up to here measures your
system against its own baseline. A hundred killed replays and a frozen label set are
real evidence, but they are all self-scored. This is the first time a number comes
from a process that was running before you arrived and is running differently
afterwards.

**Architecture → ADR as a workflow.** The fifth pipeline: architecture request →
codebase research → alternatives → tradeoff analysis → ADR. The one workflow whose
output is a *document* rather than a diff, which makes it the sharpest test of
whether the research and planning steps you built in week 3 actually work. Also the
first place a genuine case for different agent roles appears — and the bar is
*measurably better than one agent*, not *architecturally tidier*.

**Schema migration and internal API evolution.** Two rules, one ADR: expand,
backfill, switch reads, contract; and deprecate-then-remove rather than
yank-and-break. This is deliberately small — you have one repository, no external
consumers and one deployment, so the surface is weak and the residue is a written
rule rather than a build.

**Packaging.** The move from *I did this once* to *this is the thing I sell.* Same
shape of work delivered at least twice, then a fixed-scope fixed-price description
a buyer can accept without a bespoke proposal.

## Project milestones

**Platform** — the architecture/ADR lane. Then stop adding capabilities and start
*operating*: three systems running, telemetry watched, the eval gate actually
gating. Operating is the rung after building and it does not feel like progress
while you are doing it.

**All three systems** — sustained operation with the scoreboard filled weekly. This
is where the observability work either pays for itself or is revealed as
decoration.

**Portfolio pass** — for each artifact, write the sentence that makes it credible to
a stranger who has never met you. Not what it is; why anyone should believe it.
Answers that work: *it survives `kill -9` at any step boundary, here is the replay
demo* · *the permission pre-filter ships with a reproducible case where the naive
version silently drops authorized results* · *every attack number is a measurement
of my own system with its denominator stated, and there is not one borrowed
industry percentage anywhere.* Answers that don't: a screenshot, a certificate, a
description.

## Business goal

The consulting ladder, entered on **evidence, never on elapsed time**. A stage whose
exit criteria are unmet stays unexited however many months pass. The calendar does
not promote.

| Stage | Exits when |
|---|---|
| Paid fixed-scope automation | Money changed hands; the delivered outcome matches a written scope; you can state and defend a payback period in months |
| Repeatable offer | The same shape of work has been delivered at least twice, and a fixed-scope fixed-price description exists that a buyer can accept without a bespoke proposal |
| Productization candidate | One shape of pain across enough independent buyers to meet the evidence thresholds — or the framework returns an explicit non-verdict |

**The agency side-quest**, now and not earlier: contact 3–5 niche automation
agencies and write down what each one asks for. Every account of how you get in says
entry runs through warm channels, and an agency wants proof of work before putting
its own client relationships behind you. So the route swaps one cold audience for a
harder one, and what it demands at the door is the artifact you hoped to skip. A
channel that consumes proof of work is no alternative to building it — which is
exactly why it opens *after* a delivered pilot exists.

**The SaaS candidate, scored on evidence.** Competition analysis as a kill
instrument, a manual concierge delivery by hand before any automation, and the
scorecard applied for real. Rules in
[consulting-and-saas.md](../business/consulting-and-saas.md). **"No good
opportunity found" is a valid and complete outcome.**

## Measurable checkpoint

End of month 9, from artifacts:

- A pilot exists with a **measured** before/after baseline and a documented
  measurement method that survives *"how did you measure that?"* — or it provably
  does not exist, and the scoreboard says so.
- Payback stated in months, every input carrying its source, the loaded-cost
  multiplier named, and zero industry-average percentages anywhere.
- The architecture lane has produced at least one ADR from a real request.
- Three systems have run for a full month with the scoreboard filled weekly.
- Every portfolio artifact carries a credibility sentence that is **true as
  written** — those are two different tests, and a collection of ADRs recording only
  successful decisions passes the first and fails the second.
- The SaaS candidate has a verdict or a **dated** non-verdict with the missing
  threshold named.

## Decision point

**Consulting, productized offer, micro-SaaS, or the staff/AI-engineer track?**

Each option has its own bar, and the bars are deliberately not comparable — which is
what stops the decision collapsing into a preference with citations attached:

- **Consulting** needs at least one paid fixed-scope engagement actually delivered.
- **Productizing** needs work of one shape delivered twice.
- **Micro-SaaS** needs *all* the evidence thresholds met, not most of them.
- **Staff / AI engineer** needs the portfolio finished with its credibility
  statements holding.

Three of the four depend on other people. One does not — and it is a **first-class
result**, not the thing you settle for when the funnel disappoints. It is also the
only bar you can clear on your own effort, which is a fact about the evidence rather
than about ambition.
