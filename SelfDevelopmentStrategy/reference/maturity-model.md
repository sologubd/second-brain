# Coding-agent workflow maturity model

## What this is

Six levels describing how much of the engineering loop a coding agent actually
carries, from autocomplete to an integrated system that consumes tasks and
incidents and produces reviewed pull requests.

Each level states **objective requirements** — properties a reader can check by
running something — and each is claimed at a specific week or month by a named
deliverable. A level is not reached by feeling more fluent with a tool. It is
reached when its requirements hold and a deliverable id proves they hold.

The model starts below this learner's actual baseline, deliberately. L0 and L1
are recorded so the progression is honest about where the start line is rather
than flattering about how far it moves.

## The table

| Level | Milestones, each with the deliverable that claims it |
|---|---|
| L0 | before W01 — baseline, already held |
| L1 | before W01 — baseline, already held |
| L2 | W01 → D-w01-1 · W02 → D-w02-1 · W03 → D-w03-1 |
| L3 | W04 → D-w04-1 · W05 → D-w05-1 · W07 → D-w07-1 · M04 → D-m04-1 |
| L4 | W08 → D-w08-1 · W09 → D-w09-1 · W10 → D-w10-1 · W12 → D-w12-1 |
| L5 | M04 → D-m04-1 · M04 → D-m04-4 · M06 → D-m06-4 |

### Level 0 — Human codes, AI autocompletes.

The human writes the code and the model completes lines or blocks; no task is
delegated end to end. Stated as the floor, not a target — the competency
baseline already places coding-agent usage above it.

### Level 1 — Agent performs individual coding tasks.

The agent completes a bounded, well-specified task inside a session with the
human present and steering. Also already held, and recorded so the model is
complete rather than tactful.

### Level 2 — Agent can execute well-defined tickets.

A ticket in a file becomes a diff with no human keystrokes in between. Four
requirements, all checkable: the run is **unattended**, so no interactive prompt
can appear; **isolated**, happening in a worktree rather than the main checkout;
**repeatable**, so re-running produces no duplicate effect; and it ends in a
diff. D-w03-1 is what makes the third of those a proof rather than an intention.

### Level 3 — Agent can research and plan.

Three requirements: the agent locates the relevant code itself rather than being
handed it; it produces a hypothesis or plan a human reviews before execution;
and it detects that a task is underspecified and says so instead of guessing.
The third is the hard one, and D-m04-1's ambiguity detection is its strongest
evidence — which is why this level is not fully claimed until month 04.

### Level 4 — Multiple agents execute independently with verification.

Four requirements: several agents run concurrently without corrupting each
other's work; a verification gate decides whether output is acceptable, not the
human's impression of it; failures are detected and recovered from without a
human noticing first; and behaviour is measurable per run — cost, latency and
success rate. D-w08-1's chaos run covers the first and third, D-w10-1 the
second, D-w09-1 the fourth.

### Level 5 — Integrated engineering system consuming tasks/incidents and producing reviewed PRs.

Four requirements: tasks arrive from an external system and incidents from
another without manual transfer; output is a **reviewed** pull request,
multi-axis, not a diff on a branch; the system operates under a cost and quota
budget it enforces on itself; and a regression in agent behaviour is caught by a
gate before it merges. D-m04-4's five-axis review is what makes "reviewed" mean
what it is supposed to mean here.

## How to read it

Levels are cumulative and their requirements are conjunctions. A system that
runs six agents concurrently but decides acceptability by eye has not reached
L4; it has an impressive L2. Read the requirement list, not the level name.

The milestone column answers a different question from the requirement list: it
says which artifact carries the claim, so an auditor can go and run it. A level
with requirements met and no milestone evidence is unclaimed, and a milestone
that no longer runs retires the claim.

Two levels sit at the same month by design. L3 and L5 are both claimed at M04
because ambiguity detection and external task ingestion arrive in the same
build — S8 — but they are different properties, and a system could easily have
the second without the first by ingesting tasks and guessing at the ambiguous
ones.

Nothing in this model is a certification, and none of it transfers. It describes
one platform, built by one person, verified by artifacts that exist in this
repository.

## How it changes

The M01 retrospective is the first place this model can move, and it moves by
being contradicted: if the L2 requirements were not actually met in W01 through
W03, the honest response is a canon delta that re-times the milestone, not a
generous reading of "unattended".

Thereafter each checkpoint month may revise it. CP-M3 tests the L2 and L4 claims
directly, CP-M6 the L5 claim, since a level asserted without its evidence is
exactly what a checkpoint exists to catch. The M12 rewrite may extend the model
beyond L5 for year two, or record that L5 was not reached and why.

Edits go through canon's `maturity_model` block and the loop in
[HOW-TO-EDIT.md](../HOW-TO-EDIT.md) — never by editing this file directly.
Requirements may be added; they are not softened to fit what happened.
