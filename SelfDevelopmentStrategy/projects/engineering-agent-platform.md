# Engineering Agent Platform

## What it is

`PRJ-01`, and the one project here that never finishes. Thirteen stages carry a
single codebase from an unattended single-task runner to a multi-workflow harness
with evaluation gates, cost accounting and enforced trust boundaries.

The governing rule is canon's own: *EVERY STAGE MUST BE RUNNABLE. Do not attempt
all functionality initially; build it incrementally. A stage with no runnable
demo command has not shipped.* **Every stage must be runnable.** That is the test
separating a programme from a roadmap, and why demo commands are defined here
rather than in a week file.

This file owns entry, exit, demo commands, capability claims and both ceilings.
Hours, tasks and acceptance predicates belong to
[the week files](../weeks/week-04.md); concept reasoning to
[Track A](../tracks/agentic-engineering.md) and
[Track B](../tracks/system-design.md).

## Pipeline

Four target workflows. Three have pipeline diagrams in the brief; the fourth does
not, and is enumerated anyway under `BR-148` so a reader who counts three cannot
conclude the workflow goal is covered.

**Notion, 12 stages.** Notion task → task ingestion → requirement extraction →
codebase research → ambiguity detection → implementation plan → isolated
worktree/environment → coding agent → tests/typecheck/lint → automated code
review → human approval if necessary → GitHub PR. Arrives at M04 with `S8`, last of
the four, because its twelve steps need the state machine, the verification gate
and the approval gate underneath them first.

**Sentry, 10 stages.** Sentry issue → issue/event investigation → codebase
correlation → reproduction → hypothesis → instrumentation → regression test →
fix → verification → PR. Arrives at W07 with `S3`.

**Architecture, 5 stages.** architecture request → codebase research →
alternatives → tradeoff analysis → ADR. Arrives across M05–M08 with `S9`.

**Multi-axis review, 2 stages.** PR → five-axis automated review. Arrives at M04
with `S2b`: five separately cited scores, not one aggregate verdict.

## Stages

Each stage names entry, exit, the command that demonstrates it, the capabilities
it adds, and its two ceilings.

### S0 — single-task runner (W01)

- **Entry.** A task file exists and a coding-agent CLI is logged in.
- **Exit.** A task file becomes a captured diff inside a git worktree via an unattended subprocess with a versioned permission policy.
- **Demo.** `make demo-s0 TASK=tasks/example.md`
- **Adds** isolated worktrees and agent permissions. **Ceilings:** EUR 0.0, at most 40 runs.

### S1a — durable task state machine and persistence (W02)

- **Entry.** S0 exits.
- **Exit.** Every step's completion is recorded durably before the next step starts; a restart resumes from the last recorded step.
- **Demo.** `make demo-s1a`
- **Adds** agent state and persistence. **Ceilings:** EUR 0.0, at most 25 runs.

### S1b — idempotency, retries and resume, extending S1a (W03)

- **Entry.** S1a exits.
- **Exit.** 100 replays with injected kills produce exactly one state transition, one PR, one Notion page and one dedup row per key.
- **Demo.** `make demo-s1b-replay N=100`
- **Adds** retries and resume after failure. **Ceilings:** EUR 0.0, at most 30 runs.

### S2 — verification gate, review, approval, PR, CI (W04)

- **Entry.** S1b exits and a GitHub repository is available.
- **Exit.** A task becomes a merged-ready PR with zero manual steps other than approval; the approval payload renders the literal diff and the literal proposed call; CI reports back into the task record.
- **Demo.** `make demo-s2 TASK=tasks/example.md`
- **Adds** GitHub integration, code review, human approval, CI integration and automated PR generation. **Ceilings:** EUR 0.0, at most 45 runs.

### S2b — multi-axis automated review (M04)

- **Entry.** S2 exits.
- **Exit.** A PR receives five independently scored, separately cited review outputs, one per axis, rather than one aggregate verdict.
- **Demo.** `make demo-s2b PR=<number>`
- **Adds** multi-axis automated review. **Ceilings:** EUR 2.0, at most 30 runs.

### S3 — Sentry diagnosis lane (W07)

- **Entry.** S2 exits and a Sentry project with real historical issues is connected.
- **Exit.** A real historical Sentry issue becomes a PR containing a regression test that fails on the parent commit and passes on the fix.
- **Demo.** `make demo-s3 ISSUE=<sentry-id>`
- **Adds** Sentry integration. **Ceilings:** EUR 0.0, at most 70 runs.

### S4 — queue, concurrency, worktree isolation, locks (W08)

- **Entry.** S1b exits.
- **Exit.** N workers with at least 30% killed mid-task leave zero tasks stranded and zero duplicated effects; the dead-letter path is exercised.
- **Demo.** `make demo-s4-chaos WORKERS=4 KILL_PCT=30`
- **Adds** multiple concurrent tasks and a task queue. **Ceilings:** EUR 0.0, at most 50 runs.

### S5 — observability and cost accounting (W09)

- **Entry.** S4 exits.
- **Exit.** One connected trace per run with correct nesting; token counts match provider-reported usage within rounding; the aggregate retry budget bounds spend under an induced failure storm.
- **Demo.** `make demo-s5 && make trace-view`
- **Adds** observability and cost accounting. **Ceilings:** EUR 0.0, at most 55 runs.

### S6 — evaluation harness and regression gates (W10)

- **Entry.** S5 exits.
- **Exit.** Three gate tiers run as separate checks; `RG-3` runs N=5 per task with environment reset and reports a pass-rate distribution against a justified threshold.
- **Demo.** `make gate-all`
- **Adds** automated evals. **Ceilings:** EUR 0.60, and a quota rate rather than a total — 100 agent executions per gate pass, which canon marks as the binding constraint.

### S7a — trust boundaries, provenance, output validation (W11)

- **Entry.** SKA-S1 and S6 exit.
- **Exit.** Retrieved content is structurally untrusted; a turn that touched untrusted input cannot invoke an external-send tool, enforced in code and logged.
- **Demo.** `make demo-s7a-attack`
- **Adds** security boundaries. **Ceilings:** EUR 0.0, at most 80 runs.

### S7b — least privilege, sandboxing, approval gates, audit log (W12)

- **Entry.** S7a exits.
- **Exit.** Every tool has a named profile; a call outside it is refused and logged; agent-executed code cannot reach the network; the audit log is append-only with provenance.
- **Demo.** `make demo-s7b-deputy`
- **Adds** security boundaries and failure reporting. **Ceilings:** EUR 0.0, at most 45 runs.

### S8 — Notion ingestion, requirement extraction, ambiguity detection (M04)

- **Entry.** S2 exits and a Notion workspace with an API token is connected.
- **Exit.** A Notion task becomes a reviewed PR through the full 12-stage pipeline; ambiguity detection flags an underspecified task rather than guessing.
- **Demo.** `make demo-s8 NOTION_TASK=<id>`
- **Adds** Notion integration. **Ceilings:** EUR 25.0, at most 120 runs including the 40-run cross-harness comparison, homed here so W10's deliverable cap holds.

### S9 — architecture and ADR lane, agent roles, skills, failure reporting (M05–M08)

- **Entry.** S8 exits.
- **Exit.** An architecture request becomes an ADR through the 5-stage pipeline: request, codebase research, alternatives, tradeoff analysis, ADR.
- **Demo.** `make demo-s9 REQUEST=<path>`
- **Adds** different agent roles, skills and failure reporting. **Ceilings:** EUR 20.0, at most 100 runs.

## Capabilities gained

Twenty progressive capabilities, each mapped to the stage that first delivers it,
and each runnable there.

| Capability | Stage | Capability | Stage |
|---|---|---|---|
| GitHub integration | S2 | agent state | S1a |
| Notion integration | S8 | persistence | S1a |
| Sentry integration | S3 | retries | S1b |
| isolated worktrees | S0 | resume after failure | S1b |
| multiple concurrent tasks | S4 | different agent roles | S9 |
| task queue | S4 | code review | S2 |
| CI integration | S2 | observability | S5 |
| human approval | S2 | cost accounting | S5 |
| security boundaries | S7a/S7b | evals | S6 |
| failure reporting | S7b/S9 | skills | contested |

The last row is a **canon contradiction, left unresolved here.**
`flagship_capabilities` maps `skills` to S2; the same block's note on S2 records
that skills were removed from it at gap `G5-01`, and S9's list claims them. Both
readings are live at once. This file names the conflict and takes no side; the
build lead resolves it. Until then, prose asserting either home runs ahead of
canon.

## Runnable demos

A demo command is not a screenshot. Each has a criterion, and the criterion is
what makes its stage claimable.

| Stage | Its demo counts as run when |
|---|---|
| S0 | an unattended subprocess leaves a diff in a worktree |
| S1a | a killed run resumes from its last recorded step |
| S1b | 100 replays yield one PR and one dedup row per key |
| S2 | a task file reaches an opened PR with approval as the only manual act |
| S2b | five axis scores appear separately, each with its own citation |
| S3 | the regression test fails on the parent commit, passes on the fix |
| S4 | a 30% kill rate strands nothing and duplicates nothing |
| S5 | one nested trace per run, token counts matching the provider |
| S6 | three tiers report separately and the pass-rate bound is stated |
| S7a | an untrusted-input turn is refused an external-send tool |
| S7b | an out-of-profile call is refused and appears in the audit log |
| S8 | a Notion task reaches a reviewed PR, ambiguity flagged not guessed |
| S9 | an architecture request reaches a written ADR |

Each command is named verbatim in the week or month that claims its stage, and
what it produces goes to [the portfolio](../reference/portfolio.md).

**The make target is the entry point; the module form is what it wraps.** Every
command above is a real `Makefile` target and every target is a thin wrapper —
`make demo-s0 TASK=...` shells `python -m agentplat.run $(TASK)`. One command to
type, one place the flags live, and no second spelling for a week file to drift
onto. A criterion naming the module form names it as the thing the target wraps,
never as an alternative.

**The package is `agentplat`, never `platform`.** `platform` is a Python
standard-library module, and a package of that name at the repository root
shadows it for every process started there. The failure does not arrive at the
call site: it surfaces as `ModuleNotFoundError: __path__ attribute not found on
'platform'` from inside unrelated library code that imported the stdlib module
for a version string. The project keeps its name; the importable package does
not.

**Which repository S0 operates against.** The task file's `target_repo` field,
never this one — this repository is prose, canon and seven checkers, with no
application code for an agent to change, so a runner aimed here has nothing to
do and every diff it produced would be a diff against the plan. W01's default is
`../agentplat-sandbox`: a throwaway repository initialised beside this one.
Sibling rather than nested, so a worktree the runner creates cannot land inside
the programme; throwaway, because the first unattended run is expected to fail
and nothing here may absorb that. From W02 any repository with real code works —
the field exists so the choice is written down per task rather than implied by
whichever directory the command was typed in.

**The task-file schema, consumed by both `S0` and `S2`.** YAML front matter
carrying the machine-readable contract, then a markdown body carrying what the
agent reads. `tasks/example.md` is the valid fixture; `tasks/ambiguous.md` is
the underspecified one `EX-FAIL-01`'s proving test must see refused.

```yaml
---
id: T-EX-001                       # stable id; the worktree branch name, and the
                                   # dedup natural key from S1b onward
target_repo: ../agentplat-sandbox  # the repository the run operates against
files:                             # declared file scope; EX-FAIL-10 partitions
  - src/sandbox/rates.py           # concurrent tasks on this list at W08
  - tests/test_rates.py
done_condition: >-                 # one sentence a human can evaluate
  convert_rate() rejects a negative amount with ValueError.
assertions:                        # at least one, each machine-evaluable
  - pytest tests/test_rates.py -q
---

Markdown body: context, constraints, background. Never the acceptance
predicate — that lives in `assertions`, where the pre-dispatch score can
find it.
```

The pre-dispatch specificity score reads exactly three of those fields — `files`
non-empty, `done_condition` present, `assertions` holding at least one entry —
and names each absent one in its refusal. That is why the shape is fixed here
rather than in a week file: two stages consume it, and a contract owned by
neither consumer is a contract nobody maintains.

## Constraints

**`AC-S0-1`: the harness adapter must shell out to the literal `claude` CLI
binary** as a subprocess, in non-`--bare` print mode, and must not import the
Agent SDK library. A print-mode session without bare mode reuses whatever login is already
present, including subscription OAuth; bare mode explicitly does not, and
requires an API key. The vendor's compliance page draws the same line from the
other side: developers building products or services that interact with Claude's
capabilities, including those using the Agent SDK, should authenticate with an
API key — while the same page states it does not prevent an end user signing in
to the unmodified binary with their own subscription. That is exactly this
build's pattern, and it is affirmatively permitted rather than merely tolerated.
Importing the SDK would move the programme onto metered billing and destroy the
zero-marginal-euro premise. `codex exec` officially reuses saved CLI
authentication and is the sanctioned counterpart on the second harness. Two
harnesses, one interface, one auth model each — which is what makes the adapter
boundary a real design decision rather than an exercise.

**A live compliance risk, not a blocker.** Advertised limits assume "ordinary,
individual usage", and unattended orchestration is not that in spirit even on the
same binary and login. Nothing published bans it outright — the explicit
prohibitions target reselling or intermediating subscription credentials for other
people's traffic — but the term is undefined and enforceable at the vendor's
discretion. Practical rule: do not schedule so many concurrent unattended runs
that the account stops resembling one developer's session pattern. One item stays
unresolved and must not be written up as settled: the second harness's terms page
returned HTTP 403 to direct fetch during research and was characterised from
secondary sources only. Re-check the primary before finalising that adapter.

**Quota binds, euros do not.** Metered ceilings across all thirteen stages total
EUR 47.0 against a EUR 200.0 twelve-month cap, and ten of thirteen sit at zero.
What is scarce is agent re-execution. Every quota figure above is
`measured_from: week_01`, never a constant: published limits are partly temporary
and partly unpublished, and it is undocumented whether one agent turn consumes
quota the way one typed prompt does. The bucket is shared with interactive use on
the same account, so a measurement taken alongside ordinary chat measures the
wrong thing.

**Effectively-once, not exactly-once.** S1b's exit claims *effectively-once
processing under at-least-once delivery*: duplicates are absorbed, not prevented.
Exactly-once delivery is impossible over an unreliable network: a sender
receiving no acknowledgement cannot distinguish a lost message from a lost
acknowledgement, so it must resend or not, and there is no third option.
Exactly-once execution is unachievable in general unless the effect and the record
of it share a transaction. `DX-06` and `DX-16` home this correction across four
files, this one among them: a partial correction leaves two contradictory claims
standing with no signal about which is canon.
