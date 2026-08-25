<!-- FIXTURE (control): a week file that SHOULD PASS check-schema --schema week.
     It exists so the failing fixtures below prove something. A checker that
     rejects everything is as useless as one that rejects nothing. -->

# Week 01 — Harness anatomy and the first unattended run

## Outcome

By Sunday I can drive a coding agent unattended from a task file to a captured diff inside an isolated worktree.

## Time budget

- Theory: 2.5h
- Building: 6.0h
- Testing/evaluation: 2.5h
- Customer discovery: 4.0h

## Topics

- coding agents
- agent harness architecture

## Tasks

### Task 1

`T-w01-1` — 1.0h, Track A, theory. Classify each of the 29 workflow-pipeline stages as workflow-shaped or agent-shaped (RES-03).

### Task 2

`T-w01-3` — 3.5h, Track A, building. Build S0: task file to git worktree to `claude -p` subprocess to captured diff.

## Deliverables

- [ ] D-w01-1 — S0 single-task runner, evidenced by a JSON transcript from a run with no TTY attached
- [ ] D-w01-2 — HarnessAdapter contract and Claude strategy with contract tests

## Acceptance criteria

- [ ] `make demo-s0 TASK=tasks/example.md` exits 0 and writes a diff file (T-w01-1, T-w01-3)
- [ ] The captured JSON transcript parses and contains a session id and a pinned model id (T-w01-3)

## Stretch goal

Run the same task through a second harness and record where the approval-triggers-failure behaviour surfaces.

## Failure exercise

EX-FAIL-01, the ambiguous ticket. Detection: the agent's plan names no file path. Safe failure behaviour: the run halts before any write. Recovery: the task returns to a needs-clarification state. Logging: the transcript records the halt reason and the offending prompt. Test proving the mitigation: a regression test feeds an ambiguous ticket and asserts zero diffs are produced.

## Reflection

1. Which flag did you remove first when the unattended run broke?
2. Name the step where a process death would leave the world inconsistent.
3. Did the measured quota match the published figure, or diverge?

## Evidence

- Path to the S0 runner and the captured diff

<!-- user:actuals key="W01" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- s0_runner_works — 30
- adapter_contract_tested — 20
- quota_measured — 15
- failure_report_complete — 15
- positioning_and_10_prospects — 20
