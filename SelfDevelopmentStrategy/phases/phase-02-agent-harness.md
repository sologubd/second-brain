# Phase 02 — Agent harness

## Arc

Phase 02 is a single month, [M04](../months/month-04.md).

This is where the harness stops being a private tool and becomes an integrated
system. Entering it, the platform is complete but self-contained: work arrives
because a human wrote a task file, and effects land in one place, which is why
crash-consistency has so far been a single-database problem.

Leaving it, three things are true that were not. Work arrives from outside — S8
ingests a Notion task, extracts requirements and detects that a task is
underspecified rather than guessing. Effects land in several external systems
from one task, so the interval between the local commit and the last external
call is now a real surface, held by an outbox with its own relay process and by
a task-lifecycle teardown shaped as a saga with failures injected into the
compensations themselves. And a pull request is reviewed along five axes
automatically, at S2b, which is what makes *reviewed PR* mean what the brief
means by it.

The month also runs the same task through both harnesses behind one adapter, and
the comparison is designed so that it cannot secretly become a comparison of
models. The metered fallback path stays live behind that same interface.

The phase owns the arc only. Stage definitions, demo commands and the S0
subprocess constraint that the whole cost architecture rests on live in
[the flagship project file](../projects/engineering-agent-platform.md); the
reasoning behind the hours lives in
[Track A](../tracks/agentic-engineering.md).

**The brief's first-listed flagship workflow arrives here, at month 04 rather
than week 04, and that is deliberate.** Its twelve steps run from a Notion task
through ingestion, requirement extraction, codebase research, ambiguity
detection, an implementation plan, an isolated worktree, the coding agent,
tests, automated review and human approval to a GitHub pull request. Nine of
those steps are the durable state machine, the verification gate and the
approval gate that phase 01 spent twelve weeks building. Starting at the Notion
end would have produced a demo with nothing behind it — an integration that
looks like the diagram and cannot survive a restart.

As in every phase: a missed month slips the calendar. Nothing is doubled up to
catch back, because the failure modes this month exists to surface only appear
under unhurried fault injection.

## Entry conditions

- [ ] CP-M3 is answered with its evidence pack assembled, whatever the answer
      was.
- [ ] D-w08-1 holds — the queue survives its chaos run — because the saga work
      assumes orphan reclaim already behaves.
- [ ] D-w09-1 holds, so cost and quota attribution exist before a second harness
      doubles the run count.
- [ ] The M03 ecosystem re-verification is applied, since S8 and S2b both depend
      on interface facts with short half-lives.
- [ ] The M01 hour recalibration has been applied to the plan, and any bucket
      more than 15% over was resolved from the cut list rather than absorbed.

## Exit conditions

- [ ] D-m04-1 holds: a Notion task reaches a reviewed pull request unattended,
      and the cross-harness comparison is recorded with the model variable
      controlled.
- [ ] D-m04-2 holds: the outbox and its separate relay are fault-injected at
      every boundary between the commit and the last external call.
- [ ] D-m04-3 holds: the teardown saga survives failures injected into its own
      compensations, and a written classification defends which surfaces are
      outbox-shaped and which are saga-shaped.
- [ ] D-m04-4 holds: five-axis automated review runs on real pull requests, and
      the knowledge agent enforces tenant isolation with secrets handled outside
      the code.
- [ ] The M04 scope recalibration is written, re-costing months 05 through 12
      against three months of logged actuals.

## Checkpoints

No career checkpoint falls in this phase. It sits between CP-M3, which closed
the previous month, and CP-M6, which closes
[phase 03](phase-03-production-ai.md). That gap is intentional: a checkpoint
every month would measure noise, and the four checkpoints are decision points
rather than progress reports.

The month's own gate is its mandated canon delta — a scope recalibration. Three
months of logged actuals now exist, which is enough signal to re-cost the
remaining nine months honestly. The delta must also give Track E's scoping work
real hours or defer it explicitly; leaving it implied is how a plan quietly
stops being executable.

Two maturity milestones are claimed here and both are worth stating precisely.
D-m04-1 is the strongest evidence in the programme for level 3, because
ambiguity detection is the point at which the agent stops guessing and says the
task is underspecified. D-m04-1 and D-m04-4 together claim level 5: tasks
arriving from an external system, output that is a reviewed pull request rather
than a diff on a branch, under a budget the system enforces on itself. Check
both against
[the objective requirements](../reference/maturity-model.md) before claiming
either.

## Security arc

Track D continues here without a dedicated month. Two surfaces open and both are
addressed inside D-m04-4: tenant isolation on the knowledge agent, and secrets
handling now that one task writes to GitHub, Notion and Sentry with three
different credentials.

The reason this is a security concern rather than a configuration chore is that
the blast radius changed shape in this month. Until now a confused deputy could
only damage one repository. With three external systems reachable from one task
context and a second harness in the loop, an instruction that crosses a trust
boundary can be laundered into an action in a system that never saw the
untrusted input. The provenance audit log built in phase 01 is what makes that
traceable, and it must be extended to cover the new tool calls rather than left
pointing at the old ones.

The depth continues at [phase 03](phase-03-production-ai.md), where the memory
surface finally exists and can be poisoned.

## What this phase does not cover

Seven brief topics had no earlier surface and are homed at this phase's month
rather than left unassigned: model fallbacks and routing, the outbox build, the
saga re-anchored onto task teardown, automated multi-axis review at S2b, tenant
isolation on the knowledge agent, secrets handling, and Track E scoping. They
are homed at M04 and their specifics belong to
[the month file](../months/month-04.md), not here.

Not covered at all, and homed later: agent memory and memory poisoning, which
have no surface until BOA-S2 exists; policy-based authorization, which is worth
building only once several scattered conditionals prove the point; schema
migrations and API evolution; and everything in Track F beyond the instruments
phase 01 built.

Also absent by ownership: hours, tasks and concept inventories. This file states
the capability held on either side of the month; what the reader is doing during
it belongs to [the month file](../months/month-04.md).
