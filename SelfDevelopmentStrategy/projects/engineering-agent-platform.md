# Engineering Agent Platform

The flagship, and the one project here that never finishes. A single codebase
carrying real tasks and real incidents from an unattended single-task runner to a
multi-workflow harness with evaluation gates, cost accounting and enforced trust
boundaries.

**Every capability must be runnable.** One command that demonstrates it, with a
criterion that says when the demo counts. A capability with no runnable
demonstration has not shipped — that is the test that separates this from a
reading list.

This file is a **backlog**, not a schedule. The week files say when; this says
what and why. Reorder it freely on evidence.

## Ground rules

**Weeks 1–4: shell out to the CLI binary.** Run the harness as a subprocess in
non-interactive print mode. The reason is simplicity and fast feedback — a
subprocess boundary is the smallest thing that works, it has no library surface
to learn, and it reuses whatever login is already present. Secondary benefit: it
keeps early experimentation off metered billing while you are running a lot of
throwaway tasks.

**Later: choose deliberately.** The CLI is the right *first* execution path, not
a permanent architectural commitment. Somewhere around weeks 7–9 — when tracing,
structured tool calls and cancellation start mattering — re-evaluate CLI against
SDK against direct API on the requirements that have actually appeared:

| Requirement | Why it may force the decision |
|---|---|
| Event streaming | Parsing a subprocess's output stream versus receiving typed events |
| Structured tool calls | Whether you can define and dispatch tools without reparsing text |
| Cancellation | Killing a subprocess is coarse; a client may cancel a turn cleanly |
| Telemetry | Whether spans and token usage arrive as data or must be scraped |
| Credentials | Interactive-session credentials versus a credential a service can hold |
| Model routing | Switching models per step without respawning a process |
| Production isolation | What a deployed service needs versus what a laptop needs |
| Cost | Metered per-token versus flat-rate, at your actual volume |

**Moving to the SDK or the API later is a deliberate architecture decision, not a
failure of the original design.** Write it up as an ADR when you make it, with
the requirement that forced it. Durable learning outranks current vendor pricing:
the pricing will change, and the reasoning about execution boundaries will not.

*One compliance note, stated rather than hidden:* consumer subscription terms
assume ordinary individual usage, and heavy unattended orchestration is not
obviously that. Practical rule: do not schedule so many concurrent unattended
runs that the account stops resembling one developer's session pattern. If the
volume you want exceeds that, it is a signal to move to a metered path — which is
the deliberate decision above, arriving from a different direction.

**Track cost, do not reverse-engineer the plan.** Record tokens per task,
approximate cost per task, wall clock, and note when a run stalls on rate
limiting. That is enough to make architecture decisions with. **Do not build a
model of the vendor's quota system** — it is unpublished, partly temporary, and
shared with your interactive use, so any number you derive is stale before it is
useful. The roadmap trains agent-system engineering, not subscription-plan
archaeology. The one architecturally relevant fact is coarse: *roughly how many
runs can I get in an evening?*, which tells you whether to build for concurrency
or for patience.

**Do not name your package `platform`.** It shadows a Python standard-library
module for every process started in that directory, and the failure does not
arrive at your call site — it surfaces as a `ModuleNotFoundError` from inside
unrelated library code that imported the stdlib module for a version string. The
project keeps its name; the importable package does not.

**Point it at a real repository, never at this one.** This repository is prose;
a runner aimed here has nothing to do and every diff it produced would be a diff
against the plan. Week 1's default is a throwaway sandbox initialised *beside*
this one — sibling rather than nested, so a worktree the runner creates cannot land
inside the plan, and throwaway because the first unattended run is expected to
fail. From week 2 onward, any repository with real code.

## The task file

The contract both the runner and the verification gate consume. YAML front matter
for the machine-readable part, a Markdown body for what the agent reads.

```yaml
---
id: T-EX-001                      # stable id; the worktree branch name, and the
                                  # dedup natural key from week 6 onward
target_repo: ../my-sandbox        # the repository this run operates against
files:                            # declared scope; week 8 partitions concurrent
  - src/rates.py                  # tasks on this list
  - tests/test_rates.py
done_condition: >-                # one sentence a human can evaluate
  convert_rate() rejects a negative amount with ValueError.
assertions:                       # at least one, each machine-evaluable
  - pytest tests/test_rates.py -q
---

Context, constraints, background. Never the acceptance predicate — that lives in
`assertions`, where the pre-dispatch check can find it.
```

The pre-dispatch specificity check reads exactly three fields — `files` non-empty,
`done_condition` present, `assertions` holding at least one entry — and names
every absent one in its refusal. The shape is fixed here rather than in a week
file because two stages consume it, and a contract owned by neither consumer is a
contract nobody maintains.

## Capability backlog

### 1. Task → diff · week 1

**Why.** You cannot improve a pipeline you have not run once end to end.
**Build.** Task file → git worktree → unattended subprocess with no TTY → captured
diff → test run. Permission policy in a versioned file, read per run.
**Demo counts when.** An unattended subprocess leaves a diff in a worktree, the
main checkout untouched, with allowed tools and permission mode taken from the
policy file and no interactive prompt reachable at any point.
**Done.** 5 real tasks run, ≥3 complete with no human writing code.
**Metrics.** Tokens and wall clock per run; rate-limit stall seconds; interventions
per task; a coarse sense of how many runs fit in an evening.
**Failure modes discovered.** _(fill this in)_

### 2. Task → verified PR · week 2

**Why.** A diff is not a deliverable. Verification converts *the agent did
something* into *the agent did something that holds*.
**Build.** Verification commands from the task or repo config — never chosen by the
agent. Review payload rendering the **literal diff**, the per-command verification
output, and declared-versus-actual file scope. Approval recorded. Branch and PR.
**Demo counts when.** A task file reaches an opened PR with approval as the only
manual act, and a test proves the default branch is unreachable.
**Done.** 5 tasks, ≥4 PRs, verification on 5 of 5, zero commits to `main`.
**Metrics.** PR acceptance rate; out-of-scope files per task; gate failures by
command.
**Failure modes discovered.** _(fill this in)_

### 3. Feature → PR · week 3

**Why.** Writing a machine-shaped task file was most of the work. Move that
boundary.
**Build.** Issue ingestion → requirement extraction → codebase research →
ambiguity detection → plan → implementation → verification → review → PR. The
ambiguity classifier splits *technical questions the agent should answer from the
codebase* from *product ambiguities that genuinely need a human*.
**Demo counts when.** A real human-written issue reaches a reviewed PR, and an
underspecified one is parked with the specific incompatibility named — not
guessed.
**Done.** 5 real features through the pipeline, each with a written plan artifact.
**Metrics.** Autonomous completion; **unnecessary human questions** (answer was in
the repo); **missed ambiguities**; unnecessary changes; PR acceptance.
**Failure modes discovered.** _(fill this in)_

### 4. Bug → regression test → fix → PR · week 4

**Why.** The first workflow you can grade against ground truth.
**Build.** Report → investigation → code correlation → **reproduction gate** →
hypothesis → failing regression test → fix → verification → PR. No hypothesis is
recorded before a reproduction runs, enforced in code.
**Demo counts when.** A real historical issue becomes a PR whose regression test
fails on the parent commit and passes on the fix.
**Done.** 5 historical bugs with known root causes, scored against the answer key.
**Metrics.** Correct root cause; correct fix (scored **separately** — they fail
independently); regression test created; interventions; unrelated changes;
correlation precision@k.
**Failure modes discovered.** _(fill this in)_

### 5. Persistence and resume · week 5

**Why.** A long run died and you had to start over.
**Build.** State enum plus transition table as data in Postgres; completion
recorded in the same transaction as the **internal** effects it produced; resume
from the durable pointer, stopping where pointer and world disagree; a detector
that logs every such disagreement.
**Scope precisely.** Only effects inside your own transactional system can share
that transaction. Creating a PR, updating a tracker, sending mail — none of these
can participate in a Postgres transaction, and no ordering makes them atomic with
it. **External-effect atomicity is not solved here**; the crash window is a
documented failure surface, and the disagreement log is what earns the outbox in
capability 11.
**Demo counts when.** A killed run resumes from its last recorded step for internal
state, and the kill sweep covers every boundary rather than a sample.
**Done.** 100% of boundaries killed, all landing at the undisturbed **internal**
terminal state; the external-effect disagreement log exists and is non-empty.
**Metrics.** Kill points passing; external-effect disagreements by kill point;
kill-to-resume distance.
**Failure modes discovered.** _(fill this in)_

### 6. Idempotency and retries · week 6

**Why.** A resumed run re-executes the step it died inside — and if that step
opened a PR, you now have two.
**Build.** Naive handler **first**, with its duplicates counted. Then dedup table
under a unique constraint, its row committed in the transition's transaction;
three-verdict failure classification (retryable / permanent / already-applied); one
retry budget shared across every layer. Then a table classifying every **external**
effect by the idempotency mechanism the provider actually offers — key, natural
unique key, query-before-create, or none — with the remaining crash window stated
per row.
**Demo counts when.** 100 replays with injected kills yield exactly one state
transition and one dedup row per key, and every external effect is asserted only
to what its mechanism actually guarantees.
**Done.** ≥20 of 100 replays interrupted; the suite fails against the naive
handler; every external effect appears in the table with a mechanism or an explicit
**unresolved** marker.
**Metrics.** Duplicate rate, naive and corrected, per effect. External effects with
a working mechanism over external effects total — this will not be 1.
**Claim carefully.** Effectively-once *processing* under at-least-once execution,
**for the effects where a mechanism exists**. Never exactly-once, and never a
guarantee a stub provided that the real API does not.
**Failure modes discovered.** _(fill this in)_

### 7. Observability and cost accounting · week 7

**Why.** You are debugging code you did not write, doing nondeterministic work,
across a boundary you cannot step through. Single-run reasoning stopped working.
**Build.** Nested run/step/model/tool spans against a **pinned** convention
version; token counts reconciled to provider usage; `stall_seconds` as a
first-class attribute; token bucket **above** the retry layer; aggregate per-task
spend budget checked before each unit of work.
**Demo counts when.** One connected trace per run with correct nesting, token
counts matching the provider within rounding, and the budget bounding spend under
an induced failure storm.
**Done.** Slowest step, costliest step and most-retried step answerable from
telemetry alone.
**Metrics.** Tokens per task by step; undefended versus defended spend on a
hostile input, measured on a real run.
**Failure modes discovered.** _(fill this in)_

### 8. Parallel tasks · week 8

**Why.** Serialising runs wastes your evening — and week 6 made duplicate
execution safe, which is the precondition for running two of anything at once.
**Build.** Queue as a **lease**, not a list: skip-locked claiming, expiry, orphan
reclaim, dead-lettering with reasons, one worktree per worker. Declared file scope
used as a **scheduler hint** for predicting collisions; the **actual changed-file
set** inspected after every run as the only truth. Re-verification when the merge
base moved. Version column and rebuild-on-conflict for real overlaps.
**Demo counts when.** N workers with ≥30% killed mid-task strand nothing and
duplicate nothing; the dead-letter path is exercised deliberately; and a collision
visible only in the *actual* diffs is caught before merge, rebuilt and re-verified.
**Done.** 100% of tasks reach a recorded terminal state; reclaim visible in
telemetry; nothing treats declared scope as proof of independence.
**Metrics.** Stranded and duplicated counts; lease-expiry-to-reclaim latency; scope
prediction accuracy (actual set inside declared, which will not be 100%); collisions
the prediction missed.
**Failure modes discovered.** _(fill this in)_

### 9. Evals and regression gates · week 9

**Why.** Eight weeks of prompts tuned by feel, and no idea whether last Tuesday's
edit helped.
**Build.** ≥10 real tasks with known outcomes, frozen with a digest. Two tiers
reported separately: deterministic assertions, and N=5 replay with environment
reset. Baseline recorded, candidate compared on the identical suite. Threshold as a
bound against last-known-good, with a written re-baselining condition. A rescore
tier — cheap check first, model judge only on disagreement — is a later refinement,
and a judge you have not calibrated is a number you cannot use.
**Demo counts when.** Tiers report separately, the pass-rate bound is stated, and a
**real regression is caught**.
**Done.** Baseline recorded and candidate compared on the identical frozen suite;
each tier's blind spot named in one line.
**Metrics.** Pass-rate distribution; regressions caught and whether each was real.
**Failure modes discovered.** _(fill this in)_

### 10. Security boundaries · weeks 11–12

**Why.** The system now holds private data, reads text strangers wrote, and can
reach the network.
**Build.** Provenance at ingest, trust tiers and an operator/document delimiter —
defense in depth. Then the controls: code outside the model that removes the
external-send tool from any turn that consumed untrusted input; per-tool
least-privilege profiles enforced at the call site; per-action re-authorization
against a stored approval record; a sandbox with no network egress; an append-only
audit log with provenance.
**Demo counts when.** An untrusted-input turn cannot reach an external-send tool,
and an out-of-profile call is refused *and appears in the audit log*.
**Done.** Every refusal is proved to come from code by an assertion that fails when
the control is disabled. **separator ≠ security boundary; model refusal ≠ security
guarantee.**
**Metrics.** Attack success rate per technique, per arm, with denominators.
Latency added by re-authorization.
**Failure modes discovered.** _(fill this in)_

### 11. External-effect durability · months 4–6

**Why.** `db.commit(); host.create_pr()` has a crash window, and no test that does
not kill the process between those two statements will ever find it. You have had
the evidence since week 5's disagreement log and week 6's unresolved rows; this is
where they get closed.
**Build.** Outbox row written in the transition's transaction; a **separate relay
process** delivering at least once; handlers correct under double delivery. Then
teardown as a saga, with permanent failures injected into the compensations
themselves.
**Demo counts when.** Exhaustive injection at every boundary between commit and
last external call loses no effect and produces no state/effect disagreement — and
a rolled-back transaction leaves zero outbox rows.
**Done.** Every compensation invoked twice adds nothing the second time; at least
one **non-compensable** effect is named with what happens instead.
**Metrics.** Commit-to-effect latency, p50 and tail; inconsistency rate per kill
point, before and after.
**Failure modes discovered.** _(fill this in)_

### 12. Task-source integration and multi-axis review · months 4–6

**Why.** The long-form pipeline needs a real upstream, and one review verdict hides
which axis failed.
**Build.** Ingestion from your real task source. Five independently scored,
separately cited review outputs per PR.
**Demo counts when.** A real task from the tracker reaches a reviewed PR with
ambiguity flagged rather than guessed, and five axis scores appear separately, each
with its own citation. **One aggregate verdict fails.**
**Failure modes discovered.** _(fill this in)_

### 13. Architecture → ADR · months 7–9

**Why.** The only workflow whose output is a document, which makes it the sharpest
test of whether research and planning actually work.
**Build.** Request → codebase research → alternatives → tradeoff analysis → ADR.
**Demo counts when.** A real architecture request reaches a written ADR that names
alternatives it rejected and why.
**Note.** This is the first place different agent roles have a plausible case. The
bar is *measurably better than one agent*, not *architecturally tidier*.
**Failure modes discovered.** _(fill this in)_

## What this project deliberately does not do

No Kubernetes, no message broker, no Redis, no second vector store, no policy
engine, no distributed anything beyond one Postgres and worktrees. Each is a
mechanism with no surface here; if one acquires a surface, build it then. Reasons
are in [RESOURCES.md](../RESOURCES.md#deliberately-not-doing).
