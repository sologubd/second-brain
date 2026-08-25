# Week 02 — Task → Verified Pull Request

## Outcome

By Sunday the harness does not hand you a diff — it hands you a pull request that
has already run tests, lint and typecheck, on a branch, with a rendered diff for
you to approve. Five tasks through it, at least four reaching a valid PR, none of
them touching `main`.

## Why now?

Week 1 produced diffs. A diff is not a deliverable: nobody merges a diff, and you
cannot tell a good one from a plausible one by reading it, which is exactly the
failure mode of generated code. Verification is what converts *the agent did
something* into *the agent did something that holds*. Everything from week 5
onward is about protecting this pipeline; there is no point protecting it before
it produces something worth protecting.

## Build

Extend week 1's runner with the verification and delivery half:

```
captured diff
  ↓
verification: tests, lint, typecheck
  ↓
rendered diff for review
  ↓
human approval
  ↓
branch + pull request
```

Two rules that decide the shape. **The verification commands come from the task
file or the repo config, not from the agent** — an agent that chooses its own
verification will choose one that passes. And **the approval payload renders the
literal diff**, not the agent's summary of it: every fact you need to decide has
to be in front of you, and no amount of trust in the model substitutes for it.

Still not building: durable state, queues, retries, concurrency. The pipeline is
allowed to simply fail this week.

## Learn

- Your Git host's CLI or API for branch and PR creation — just enough to open a
  PR from a subprocess and read back its number.
- Skim [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)
  part I on integration points. You are about to acquire your first one, and the
  antipatterns chapter tells you what it will do to you.

~2h.

## Tasks

1. **Wire the verification gate.** Run the repo's test, lint and typecheck
   commands inside the worktree. Capture each one's output and exit code
   separately — a single pass/fail boolean throws away which gate failed and why.
2. **Render the review payload.** The literal diff, the verification output per
   command, the task's stated done-condition, and the files touched against the
   files the task declared. That last comparison is the cheapest signal you have.
3. **Add the approval step.** Nothing reaches the Git host without an explicit
   approval that gets recorded. One approval per task, and a refusal is a valid
   outcome that gets logged.
4. **Branch and PR.** Branch name derived from the task id. The task's file scope
   is the expected diff scope; anything outside it is called out in the PR body.
5. **Prove `main` is unreachable.** Write a test that fails if the pipeline can
   write to the default branch. Assert it, do not document it.
6. **Business: send the first four cold messages.** Hand-written, one quoted
   public signal each, against the prospects from week 1. Open a send log with one
   row per touch. Shapes in
   [customer discovery](../business/customer-discovery.md).

## Use it for real

Five more real tasks from the same repository. Include at least one you expect to
fail verification — a task whose tests you know are flaky, or one touching a
module with weak coverage. You want to see the gate stop something this week, not
in week 9 when a threshold depends on it.

## Measure

- Tasks run: 5. Reaching a valid PR: target ≥4.
- Verification ran on 5 of 5. This is binary and non-negotiable.
- PR acceptance: PRs you would actually merge, over PRs opened.
- Unrelated changes: files touched outside the task's declared scope, per task.
- Interventions per task, and what each was.

## Failure exercise

**The flaky test.** Stop the gate reading one red run as a verdict — and stop the
agent curing instability by asserting less.

- **Detection.** A test goes red, then green, on a tree nobody touched. Re-run
  any red test N times against the identical commit before classifying, with N
  fixed and stated *beforehand*. Choosing N after seeing results is fitting, not
  measuring.
- **Safe failure.** Never approve past an unclassified red, and never accept a
  weakened assertion as the remedy. Weakening is the characteristic generated
  response and is worse than the flake: the signal goes silent and nothing
  downstream reports the loss.
- **Recovery.** Classify it, quarantine it with a written reason, hand it to a
  person. The PR may proceed — but only with the quarantine spelled out in the
  approval payload, so continuing is a decision somebody took.
- **Logging.** Test id, the red-green sequence across re-runs, and the commit
  SHA. Instability then belongs to a named test with a history, rather than being
  something people say about the suite.
- **Proving test.** An unstable fixture is classified rather than failed, and an
  agent edit to a quarantined test's assertion is refused at the gate. Both
  assertions must go red against the one-red-is-final version.

## Deliverables

- [ ] Verification gate running tests, lint and typecheck with per-command output
      captured.
- [ ] Approval payload rendering the literal diff, the verification output, and
      the declared-versus-actual file scope.
- [ ] Branch-and-PR path from a task id, with the approval recorded.
- [ ] Test proving the pipeline cannot write to the default branch.
- [ ] Run log for 5 tasks: PR opened or not, gate results, interventions,
      out-of-scope files.
- [ ] Flaky-test report, five parts, with its proving test red on the parent
      commit.
- [ ] Send log with 4 hand-written first touches, one public signal cited each.

## Done when

- [ ] 5 tasks ran and at least 4 opened a pull request.
- [ ] Verification ran on all 5, with per-command results recorded.
- [ ] Zero commits reached the default branch, and a test asserts that.
- [ ] Every PR carries an approval record naming a human.
- [ ] A red test is re-run exactly N times before classification, N stated in
      advance, and an assertion-weakening edit to a quarantined test is refused.
- [ ] 4 first touches sent and logged, each citing a public source, with zero
      warm introductions.

## Reflection

1. Which verification command caught something the others missed? Which one has
   never caught anything, and would you still pay for it?
2. Looking at the approval payloads: which fact did you need that was not there,
   and how did you get it?
3. Of the tasks that failed, how many failed at the agent and how many at the
   task file you wrote?

## Evidence

- Links to the pull requests opened this week.
- Verification output per task.
- The approval records.
- The default-branch protection test.
- Flaky-test report and its red-on-parent proving test.
- Path to the send log.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
