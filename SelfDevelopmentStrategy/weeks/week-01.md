# Week 01 — Minimal Useful Harness

## Outcome

By Sunday you can hand a task file to a coding agent and get back a diff in an
isolated worktree, unattended, with tests run against it — and you know what that
costs in wall clock and tokens. Five real tasks have been through it. At least
three finished without you writing code. The failures are written down.

## Why now?

You already delegate work to agents interactively, every day. What you have never
built is the machinery underneath that habit: the process boundary, the
permission file, the context assembled per invocation, the captured result. This
week builds the smallest thing that has all four, on real work, so that every
later week has something concrete to break.

## Build

```
task.md
  ↓
isolated git worktree
  ↓
coding agent (unattended subprocess, no TTY)
  ↓
captured diff
  ↓
tests
```

One module. A task file in, a diff and a test result out. Details — the task-file
shape, why the CLI subprocess is the right *first* execution path, which
repository to point it at — are in
[the platform file](../projects/engineering-agent-platform.md), capability 1. The
subprocess is chosen for simplicity, not forever: whether to stay on it or move
to an SDK or the API is a deliberate decision you make around weeks 7–9, against
requirements that have actually appeared.

**Do not build yet:** a multi-harness abstraction, a durable state machine, a task
queue, concurrency, a quota model, a plugin architecture, a provider abstraction.
Every one of those arrives later, in the week where something has broken that
needs it. If you build them now you are practising speculative generality by
practising speculative generality.

## Learn

- Your harness's CLI reference: non-interactive invocation, permission modes,
  and where subscription sign-in parts from key-based access. Worth understanding
  now because it feeds the later CLI-versus-SDK decision — not because it settles
  it.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents).
  Short. The question it answers — who owns control flow — is the one you will
  answer per stage for the rest of the year.

That is it. Two items, ~2h.

## Tasks

### Core — required (~15h: 2h learning, 9h building/testing, 3h business)

1. **Build the runner.** Task file → worktree → unattended subprocess → captured
   diff. Use the worktree from the first attempt: your first unattended failure
   should not also be a dirty working tree.
2. **Make the permission policy a file.** Allowed tools and permission mode read
   from a versioned file per run, not an interactive fallback reached when
   something prompts. An unattended process has nobody to ask, so a policy that
   lives only as a habit becomes either a hang or a silent widening of authority.
3. **Run the tests.** After the diff, run the target repo's test command inside
   the worktree and capture the result. Do not gate on it yet — just record it.
4. **Add a pre-dispatch specificity check.** Before spending a token, verify the
   task file names a file or module, states a done-condition, and carries at
   least one machine-evaluable assertion. If any is absent, refuse. This is the
   failure exercise below.
5. **Run five real tasks and measure.** Per run: harness, model id, input and
   output tokens, wall clock, and seconds spent waiting on rate limits (log that
   separately — it is not your system being slow).
6. **Business: choose a niche and research 10 prospects.** Write the positioning
   note first — who this is for, what problem, why you. Then 10 companies from
   public sources only, no warm introductions. Checklist in
   [customer discovery](../business/customer-discovery.md).

### Stretch — only after Core is DONE

- **Put one task through a second harness** and record where the behavioural
  difference actually surfaces — an exit code, a line on stderr, a JSON event.
  Then answer: could your runner currently tell that apart from a genuine task
  failure? This is reconnaissance for the adapter decision, not the adapter.
- **A second pass on the specificity check**: find a task file that passes all
  three checks and is *still* ambiguous, and write down what a fourth check would
  have to look for.

## Use it for real

Five tasks from a real repository — your own project, or a throwaway sandbox
initialised beside this one if you would rather the first unattended run failed
somewhere it cannot hurt. Small but genuine: a validation rule, a bug you already
know how to fix, a missing test, a rename with call-site updates. Not toy tasks
invented to suit the runner.

## Measure

- Tasks run: 5. Completed with no human writing code: target ≥3.
- Human interventions per task, and what each one was.
- Wall clock and tokens per run. Record rate-limit stall time separately.
- Roughly how many runs fit in an evening before you start waiting. One coarse
  number is enough — it tells you whether later weeks should build for
  concurrency or for patience. **Do not try to reverse-engineer the vendor's
  quota system**: it is unpublished, partly temporary, and shared with your
  interactive use, so any model of it is stale before it is useful.

## Failure exercise

**The ambiguous ticket.** Make the runner decline an underspecified task rather
than emit a confident diff against a requirement nobody wrote down.

- **Detection.** Score the task file pre-dispatch on three things: a named file
  or module, a stated done-condition, one machine-evaluable assertion. Where any
  is absent, the *score* fails, not the task. Detection sits before the model
  call, which is what makes it free.
- **Safe failure.** Refuse to dispatch. Letting the model fill the gap yields
  something plausible aimed at an unstated requirement — the expensive outcome,
  because it arrives dressed as success and surfaces at review or later.
- **Recovery.** Name every missing element, not the first one found, and park the
  task where a person sees it. Never auto-fill an absent criterion: a generated
  acceptance criterion is a guess in the costume of a specification.
- **Logging.** Task id, which element was missing, and the raw task text. Those
  three fields make vagueness countable across weeks instead of handled one
  ticket at a time — and the count tells you whether the ticket writer or the
  checker needs fixing.
- **Proving test.** An underspecified fixture is refused before any model call; a
  complete one dispatches normally. **Run both against the pre-check runner
  first** — it dispatched them alike, so the refusal assertion must go red there.

## Deliverables

- [ ] Runner: task file → worktree → unattended agent → captured diff → test
      result, driven from one command.
- [ ] Versioned permission policy file, read per run, with no interactive prompt
      reachable at any point.
- [ ] Run log for 5 real tasks: outcome, interventions, tokens, wall clock, stall
      seconds.
- [ ] Pre-dispatch specificity check with its two fixtures and the refusal test
      that goes red on the parent commit.
- [ ] Positioning note and 10 hand-researched prospects (in a `*.local.md` file).

## Done when

- [ ] One command takes a task file and leaves a diff in a worktree, unattended,
      with no TTY attached — and the main checkout is untouched.
- [ ] Allowed tools and permission mode came from the policy file, not a prompt.
- [ ] 5 real tasks ran; at least 3 reached their done-condition with no human
      writing code.
- [ ] The run log has a token count and a wall-clock figure for every run.
- [ ] The underspecified fixture is refused with zero model calls, and the
      refusal names every missing element.
- [ ] The positioning note names one niche, one recurring workflow, and one
      reason a buyer in that niche would answer you specifically.

## Reflection

1. Which flag did you remove first when the unattended run broke? What does that
   say about which part of the context was load-bearing rather than merely
   present?
2. Your runner dispatches and captures. Name the step where a process death would
   leave the world inconsistent — and why nothing you built this week would
   notice.
3. Of the two tasks that needed you, was the failure in the agent, the task file,
   or the repository?

## Evidence

- Command and path to the runner; the diff it captured.
- The unattended transcript (no TTY), showing session id, pinned model id, usage.
- Run log: 5 tasks with tokens, wall clock, stall seconds, interventions.
- The refusal test, and proof it fails on the parent commit.
- Paths to the positioning note and prospect list.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
