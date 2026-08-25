# Setup — what must exist before week 01

## What this file is

The bridge between a repository that validates and a Monday you can start. Every
week file names artifacts under `agentplat/`, `tests/`, `evals/`, `docs/` and
`policy/`, and none of those directories ships here. That absence is deliberate:
the programme's first rule is that building is the evidence, so the platform is
yours to write. What was missing was the layer underneath — the interpreter, the
harness binaries, the credential boundary — which no week pays for and every
week assumes.

Nothing below is graded. It is the floor, not a deliverable, and it should cost
under an hour. Where a step edges into work a task already owns, this file stops
and says which task owns it.

## Prerequisites

**Python 3.12 or newer, in a virtual environment.** The system interpreter on
this machine is older than the platform code will want; create the environment
first and let every later command run inside it. `python3 -m venv .venv`, then
activate it, and set `PYTHON` when calling make if your shell resolves something
else.

**Git 2.35 or newer.** Week 01 drives `git worktree` from a subprocess, so
confirm `git worktree list` answers before the runner depends on it.

**Both harness CLIs, signed in.** Claude Code and Codex, each authenticated
through the subscription rather than a metered key. `RES-01` in
[the resource list](resources/recommended-resources.md) is where the invocation
semantics live, and the sign-in-versus-key boundary is a cost decision the whole
budget rests on — the week-01 ceiling is EUR 0.00 of metered spend, which only
holds while runs go through the subscription.

**A scratch repository the runner can operate on.** Week 01 needs a checkout to
open worktrees against; it does not need GitHub yet. Remote access first matters
at week 04, Sentry at week 06, Notion at month 04.

## Create the working directories

Five directories and one package marker, empty:

```sh
mkdir -p agentplat tests evals docs policy
touch agentplat/__init__.py
```

Add a minimal `pyproject.toml` naming the project and requiring Python 3.12, so
`python -m agentplat.run` resolves once week 01 writes that module. Dependencies
arrive when a week needs them — `bm25s` and `pgvector` at week 05, not now.
Installing a library ahead of the week that justifies it is how a stack grows
without a decision behind it.

`policy/` stays empty on purpose. `T-w01-4` versions the permission file into it,
and shipping the shape here would spend that task's 0.75 h before you reach it.

## Secrets and the public-capable rule

`.gitignore` already excludes `*.local.md`, and that pattern carries the entire
privacy boundary. Real prospect names, interview notes and client figures live
in files matching it; the tracked copies carry placeholders. `prospects.local.md`
and `send-log.local.md` appear in week deliverables for exactly this reason.

Add `.env` to `.gitignore` before writing anything into it. Keep API credentials
out of tracked files and out of the policy file, which is versioned by design.

The rule to hold: the repository must stay publishable at any moment with no
scrub pass. Anything that would need redacting before publication belongs behind
the local suffix on the day it is written, not retroactively.

## Verify the repository

```sh
make check
make help
```

`make check` runs eight checkers plus the fixture controls that prove each one
can fail. Green means canon and prose agree — it says nothing about your
progress, which lives in ticked deliverables and the
[scoreboard](SCOREBOARD.md).

`make help` lists every stage demo. All of them fail today with a module-not-found
error, which is the correct state: each becomes runnable in the week that builds
its stage, and `make demo-s0 TASK=tasks/example.md` passing is literally the
first acceptance criterion of week 01.

## What week 01 builds and this file does not

The runner, the permission policy, the harness adapter and its contract tests are
`T-w01-3`, `T-w01-4`, `T-w01-8` and `T-w01-9`. The task-file schema, the package
layout and the shell-out constraint are fixed in
[the platform file](projects/engineering-agent-platform.md), which is worth
reading before you start building rather than while.

With the floor in place, open [week 01](weeks/week-01.md) and do not read ahead.
The monthly mutation path is in [HOW-TO-EDIT.md](HOW-TO-EDIT.md).
