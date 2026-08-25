# Track A — Agentic Engineering

## What these hours buy

43.0 h, 23.9% of the programme and its largest single allocation. They buy six
things a stranger can be shown running. A single-task runner driving the
unmodified `claude` binary as an unattended subprocess, inside a throwaway
worktree, handing back a captured diff. A typed cross-harness adapter built to
*expose* the two harnesses' differences rather than smooth them away. A
verification, automated-review, human-approval, pull-request and CI pipeline
opening real pull requests against your own repository. A diagnosis lane
pointed at 20 real labelled historical Sentry issues. An observability and
cost-accounting layer emitting spans per run. And one measured number — weekly
quota headroom, taken in [W01](../weeks/week-01.md) — from which every later
sizing decision derives rather than being guessed.

None of that is knowledge, and the ordering is the point. The learner already
delegates real work to coding agents. What is missing is evidence that the
delegation survives being unattended, restarted, run four-wide and metered.

One constraint holds all six up, and anyone touching the adapter has to see it.
Canon's S0 architectural constraint requires shelling out to the literal CLI
binary in print mode and forbids importing the vendor's agent library. That is
not a taste in dependencies: the library route is the one the vendor's own
compliance guidance points at key-based authentication, which converts a
flat-rate subscription into metered billing and removes the zero-marginal-cost
premise the cost architecture stands on. Stage semantics, demo commands and the live compliance
risk belong to
[the flagship project file](../projects/engineering-agent-platform.md).

## Entry competency

Independent implementation — user-supplied, and the joint-highest starting
level in [the competency matrix](../reference/competency-matrix.md), where
`CM-01` records it as a relative strength. That fixes the pitch of every hour
below: nothing here explains what a coding agent is or argues that you should
use one. W01 opens on harness anatomy and an S0 build.

The row targets Production competence at month 3 and holds it at month 6 — flat
by design, because those months deepen operation rather than widen scope — then
*Can design and review others' systems* at month 12, on the evidence of
`D-w01-1`, `D-w01-2`, `D-w04-1` and `D-m04-1`. A level held with no deliverable
behind it is downgraded, never quietly retained.

## Concepts

Twenty-two concepts, every one homed here: week files link to this reasoning
rather than restate it. Sixteen are P0 and each carries its own argument below.
The table gives priority, the week the concept stops being an idea, the surface
where that happens, and the deliverable proving it.

| Concept | Priority | Week | Surface | Proved by |
|---|---|---|---|---|
| coding agents (C-001) | P0 | W01 | S0 invokes the CLI, no TTY | D-w01-1 |
| harness architecture (C-002) | P0 | W01 | the adapter Protocol, two strategies | D-w01-2 |
| tool calling (C-003) | P0 | W01 | S0's allowed-tool policy; S2's gate | D-w01-1 |
| skills (C-004) | P1 | W04 | packaged procedures under `.claude/skills/` | D-m06-4 |
| agents vs workflows (C-005) | P0 | W01 | classification enforced by S1a | D-w01-4 |
| context engineering (C-006) | P0 | W01 | per-run context in the adapter | D-w01-2 |
| task decomposition (C-007) | P0 | W01 | the task-file schema S0 consumes | D-w02-1 |
| multi-agent orchestration (C-008) | P1 | W08 | S4's worker pool, one queue | D-w08-1 |
| parallel work (C-009) | P0 | W08 | S4 with 30% of workers killed | D-w08-1 |
| worktrees and isolation (C-010) | P0 | W01 | every S0 run; S4 reclaims orphans | D-w01-1 |
| model routing (C-011) | P1 | W01 | pinned model ids in run metadata | D-w01-2 |
| retries (C-012) | P0 | W03 | S1b's truth table; S5's budget | D-w03-1 |
| resumability (C-013) | P0 | W03 | S1b resumes at the last boundary | D-w03-1 |
| checkpoints (C-014) | P1 | W02 | S1a records before the effect | D-w02-1 |
| human approval (C-015) | P0 | W04 | S2's gate; BOA-S1's draft-only path | D-w04-1 |
| long-running tasks (C-016) | P1 | W02 | S1a's waiting state; S4's leases | D-w02-1 |
| task queues (C-017) | P0 | W08 | S4's queue, leases, dead-letter path | D-w08-1 |
| agent permissions (C-018) | P0 | W01 | the versioned per-run policy file | D-w01-1 |
| cost and token budgets (C-019) | P0 | W01 | the headroom figure; S5's accounting | D-w01-2 |
| automated PR generation (C-020) | P0 | W04 | S2 and S3 open real pull requests | D-w04-1 |
| automated review (C-021) | P0 | W04 | S2 single-axis, five axes at S2b | D-w04-3 |
| agent feedback loops (C-022) | P1 | W10 | S6's gates feed the harness layer | D-w10-1 |

### Delegation, context and decomposition

**coding agents.** The unit of work stopped being a keystroke and became a
delegated task. What survives automation is not knowing agents exist but
knowing what a task must carry to be delegable: a bounded contract, a
verification command, an acceptance predicate a machine can evaluate.
Interactive use hides the gap, because a confused agent can ask. Unattended,
nobody answers.

**harness architecture.** The loop around a model moves outcomes more than
swapping the model does; the literature documents a 32x cost spread at
identical code quality. Hard-coding one vendor's invocation bakes a procurement
decision into business logic. The classic adapter failure is an interface
flattened to a lowest common denominator, erasing the very differences it was
built to observe — so this one carries them in its types.

**tool calling.** A tool call is where a language model acquires the ability to
change the world, and therefore where every reliability and security property
is settled. Generated orchestration treats the tool list as configuration. It
is the system's whole authority surface, and the shortest route from a hostile
instruction to an unsanctioned effect.

**agents vs workflows.** The highest-leverage architectural decision in the
pipeline. A workflow drives the model through branches you own; an agent
directs its own process while you own the goal and the guardrails. A generating
model makes everything an agent loop because that shape saturates its training
data, forfeiting replayability and cheap debugging across the 90% of the
pipeline that never needed model-driven branching.

**context engineering.** Default print mode loads hooks, skills, servers and
project instructions from wherever the process stands, so context is ambient
and directory-dependent. Generated orchestration assuming the agent knows your
conventions depends on state no test reproduces. Behaviour you can gate a merge
on requires context to be an explicit per-run input, assembled by the caller.

**task decomposition.** The bottleneck moved from producing code to specifying
it, and decomposition is the specification skill — also the most durable human
advantage, because it needs to know what *done* means in this codebase. A task
split into verifiable units is cheap to execute and cheap to check; one saying
*implement the feature* is neither, and no harness improvement rescues it.

### Surviving failure

**parallel work.** The right answer to contention is usually partition rather
than a lock: one worktree, one branch, disjoint ownership, contention that
cannot arise needing no coordination. Ask an agent for a distributed lock and
you get a lock-shaped object that acquires and releases convincingly while
saying nothing about a lease expiring with the holder still working.

**worktrees and isolated environments.** Any pipeline running concurrent agents
against one checkout is racing itself, and the second-write-wins defect appears
only under load. The primitive is a single git command; the payoff is a defect
class deleted rather than defended against, whichever harness runs inside it.

**retries.** A model emits three attempts and a flat one-second sleep because
that is the modal retry loop in its training distribution, and it is wrong
three ways: no jitter, no error classification, no aggregate budget. None is a
typing problem. Only you know that *a pull request already exists for this
branch* is a success. The human supplies the truth table; the agent supplies
the loop.

**resumability.** An agent pipeline has two amnesias, process death and context
death, and one persisted state machine answers both. A resume is not a rerun:
it is a fresh attempt carrying prior state, and because the work unit is
nondeterministic the second attempt does something different from the first.
That distinction has no textbook; it is worked out here against a real machine.

**task queues.** Agents build queue plumbing well and decide whether you need a
queue badly. Adopting one is not an infrastructure choice; it is a decision to
make every downstream handler idempotent, because at-least-once delivery is
what a queue offers. That link is the most under-taught thing in the area, and
it is why the queue lands after the idempotency work.

### Authority, cost and irreversible effect

**human approval.** The gate is an architectural control, not a piece of user
experience. It belongs where a state change becomes irreversible or
high-impact, and must render the literal proposed call beside its evidence.
Generated gate code approves the agent's *summary* of its intent, and an
injected instruction can produce a truthful-looking summary over a different
underlying call.

**agent permissions.** Both harnesses treat a permission prompt in unattended
mode as a hard failure or a hang, so code assuming the agent can quietly ask
and wait passes in development and stalls in production. The policy has to be a
versioned per-run input — which also makes it reviewable and diffable, the step
that turns an operational convenience into a security control.

**cost and token budgets.** Here the failure mode of a naive retry loop is a
bill rather than an exception — and under a flat-rate subscription not even a
bill but a stall, which is worse because nothing alerts on it. The binding
resource is quota, not euros, and measuring headroom in week one is what makes
every later size decision derived rather than asserted.

**automated PR generation.** The pull request is the first effect reaching a
human inbox, and therefore the first that cannot be compensated by a correcting
row later. *One pull request per branch name* makes the create idempotent by
construction; preferring a natural key over idempotency bookkeeping is the
lesson, because the cheapest way to be idempotent is to have nothing to
reconcile.

**automated review.** Your reading habits were trained on the defects a hurried
human leaves behind: inconsistency, a skimmed branch, an edge case nobody had
time for. Model output does not fail there. It is clean, idiomatic and well
named, and it breaks at the seams instead — on the second delivery, under a
concurrent caller, in a partial failure, at a boundary nobody specified. The
correlates of bad code moved and the habits did not follow, so the checklist
has to be rebuilt against the new distribution rather than inherited. That
rewrite is the highest-leverage artifact in the programme, and it is versioned
because a checklist you cannot diff cannot be shown to have improved.

## Priorities and what is deferred

The six P1 rows are not weaker ideas; each waits on a surface. Checkpoints and
long-running tasks sit inside the W02 machine, below resumability, which earns
the deliverable. Model routing is a pinning discipline before it is a policy,
and its fallback half moves to [month 04](../months/month-04.md) with the
second harness. Multi-agent orchestration sits below parallel work: the pool is
mechanism, the proof that nothing strands or duplicates is the lesson. Skills
are a W04 stretch, a claimed capability only at S9. Feedback loops wait because
a loop with no frozen baseline is a rumour mill.

The technology triage decides the rest, in four verdicts. Harness design is the
one **LEARN DEEPLY** entry: its auth, context and permission semantics are the
mechanism the cost architecture rests on. Worktrees, skills and queues are
**LEARN ENOUGH TO USE** — shallow primitives with high payoff, and for the
queue, building it *is* the lesson, which is why nothing adopts a broker.
Durable-workflow frameworks and third-party orchestration are **UNDERSTAND
CONCEPT ONLY**: checkpoint-and-resume transfers wholly to the hand-built
machine and the interfaces do not, so each is read once, afterwards, as a check
on the design. Redis is **SKIP FOR NOW**, because introducing it to teach
locking means teaching an unsafe lock and then its caveats. The verdicts in
full sit in [the low-ROI list](../reference/low-roi-and-cuts.md).

Two exclusions are decisions, not gaps. Chasing published quota figures is
refused at `LR-16` — they are temporary or unpublished, so you measure. The
agent library is refused on billing grounds at `LR-15`, which is that same S0
constraint seen from the budget side.

## How this track is proved

Track A leads nine of the twelve weeks, standing down as primary in W03, where
durable execution is Track B's to lead, and across W11 and W12, where security
takes the front. Those are coverage facts rather than lapses: the harness is
still the thing being attacked.

Proof is the deliverable ids in the table and nothing else. `D-w01-1` through
`D-w01-4` establish that an unattended run happens at all — isolated, under a
policy, with the workflow boundary written down first. `D-w02-1` and `D-w03-1`
move the claim from *runs* to *survives being killed*; `D-w04-1` and `D-w04-3`
to *produces a reviewed effect a human sanctioned*. `D-w08-1` adds concurrency
under deliberate chaos, `D-w10-1` a gate that can fail a change, and `D-m04-1`
closes it at [phase 02](../phases/phase-02-agent-harness.md) with work arriving
from outside the system.

Absent by ownership: weekly tasks, hours and acceptance predicates, which are
the week files', and stage entry and exit conditions with their demo commands,
which are the project files'. Two Track A items are homed later and named here
so their absence from phase 01 reads as a decision — model fallbacks and
routing, and the multi-axis review that makes *reviewed pull request* mean what
the brief means, both at month 04. If a bucket overruns, the recorded relief
here narrows W09's spans to the agent and tool layers and defers W02's
call-graph attribution to W08, at a stated cost to `D-w02-4`.
