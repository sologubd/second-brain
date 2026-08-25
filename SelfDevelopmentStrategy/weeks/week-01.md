# Week 01 — Harness anatomy and the first unattended run

## Outcome

By Sunday I can drive a coding agent unattended from a task file to a captured
diff inside an isolated worktree, and I know how much weekly quota that costs
me.

## Time budget

- Theory: 2.5 h
- Building: 6.0 h
- Testing/evaluation: 2.5 h
- Customer discovery: 4.0 h

Nothing here is an on-ramp. USI-07 fixes the coding-agent baseline at
*Independent implementation* and marks it a relative strength: real work is
already delegated to agents, interactively, every day. What has never been built
is the machinery underneath that habit — the process boundary, the permission
file, the context assembled per invocation. The reading is harness anatomy, the
build is S0, and no hour is priced for explaining what an agent is.

Customer discovery takes 4.0 h, the largest business bucket of the opening three
weeks and well clear of the 2.5 h floor, because the funnel starts from nothing:
USI-03 records zero pipeline in the user's own words. Theory at 2.5 h sits a full
hour under the weekly cap: half of it went to building when T-w01-3 absorbed the
test suite D-w01-4 had always implied and nothing had ever paid for. Ceilings are
EUR 0.00 of metered spend and no more than 40 agent runs, the 10-run battery
included. That 40 is also the planned weekly run count T-w01-6's trigger reads
against. These are *planned* figures — a week-file measures work, not calendar
time.

Compressed week, 7.75 h: T-w01-3 (3.5), T-w01-4 (0.75), T-w01-6 (1.0) and
T-w01-10 (2.5), with discovery at its 2.5 h floor; the rest defers to
[week 02](week-02.md). The measurement is held at all costs and sits inside the
subset at its real 1.0 h, which is a trade worth stating: it and the permission
policy will not both fit beside T-w01-5, so the runner ships and its OAuth proof
does not. All four deliverables stay unticked and carried, AC-w01-1b travelling
with T-w01-5. The week closes DONE-COMPRESSED, and becomes DONE when the carried
ids land. Slip the end date; never stack this week onto the next.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| coding agents | A | P0 | T-w01-3's subprocess, run with no terminal attached → D-w01-1 |
| agent harness architecture | A | P0 | T-w01-8 → D-w01-2 |
| tool calling | A | P0 | the allowed-tool list inside T-w01-4's policy file |
| agents vs workflows | A | P0 | T-w01-1 → D-w01-4 |
| context engineering | A | P0 | T-w01-2's adapter contract sketch → D-w01-2 |
| task decomposition | A | P0 | the task-file schema S0 consumes in T-w01-3 |
| Git worktrees / isolated environments | A | P0 | T-w01-3 → D-w01-1 |
| agent permissions | A | P0 | T-w01-4 → D-w01-1 |
| cost/token budgets | A | P0 | T-w01-6 → D-w01-2 |
| boundaries | B | P0 | the adapter contract in T-w01-8 → D-w01-2 |
| deep modules | B | P0 | T-w01-7, applied in T-w01-8 → D-w01-2 |
| choosing a niche | E | P0 | T-w01-10 → D-w01-3 |

Every row resolves to a canon concept carrying P0, so none needs the earn-it or
competency fallback. Nine are homed in
[Track A](../tracks/agentic-engineering.md); boundaries and deep modules are
[Track B](../tracks/system-design.md), and choosing a niche is
[Track E](../tracks/consulting.md). Niche selection is market selection, which
makes week one a [Track F](../tracks/micro-saas.md) reinforcement rather than a
courtesy. Two tasks reinforce [Track D](../tracks/ai-security.md): the permission
policy and the sign-in boundary each decide how much authority a run holds. S0 —
entry, exit and demo command — belongs to
[the platform file](../projects/engineering-agent-platform.md). Hours, tasks and
acceptance criteria are what this file owns.

## Tasks

### Task 1

`T-w01-1` — 1.0 h, Track A, theory, reinforcing B. Reading: `RES-03`. Walk all
29 stages of the four target workflow pipelines — 12 Notion, 10 Sentry, 5
architecture, 2 multi-axis review — and mark each workflow-shaped or
agent-shaped on one question: who owns control flow. Own the branches and you
get replay, cheap debugging and a predictable cost; hand the model its own
process and you trade all three for adaptability. Name what each stage does on
failure — replayed, or re-prompted.

### Task 2

`T-w01-2` — 1.0 h, Track A, theory, reinforcing D. Reading: `RES-01`. Read the
headless-invocation semantics until you can state them without the page open:
print mode against bare mode, what each permission mode actually relaxes,
which context arrives ambient and which must be handed in, and where
subscription sign-in parts from key-based access. That last boundary is a cost
decision before it is an auth one. Output is the adapter contract sketch.

### Task 3

`T-w01-3` — 3.5 h, Track A, building. Build S0: a task file becomes a git
worktree, becomes a `claude -p` subprocess with no TTY attached, becomes a
captured diff. Use the worktree from the first attempt — your first unattended
failure should not also be a dirty tree. The runner shells out to the literal
CLI binary and never imports the library; that constraint is AC-S0-1, and [the
platform file](../projects/engineering-agent-platform.md) carries its reason
in full, along with the task-file schema, the package name and which
repository the run operates against. Half an hour of this task is the
pre-dispatch specificity scorer that sits in front of the runner, with both
task fixtures and the refusal test that goes red on the parent commit —
D-w01-4's suite, previously priced at nothing.

### Task 4

`T-w01-4` — 0.75 h, Track A, building, reinforcing D. Make the permission
policy — allowed tools, permission mode — a versioned file read per run, not
an interactive fallback reached when something prompts. An unattended process
has nobody to ask, so a policy that lives only as a habit becomes either a
hang or a silent widening.

### Task 5

`T-w01-5` — 0.75 h, Track A, testing. Prove subscription sign-in survives a
fully unattended invocation. Assert over the battery's ten transcripts that
each carries a session id, the pinned model id and a usage block, and that no
authentication failure appears in any system or retry event. It is half its
former size because it no longer captures its own evidence — T-w01-6 already
wrote those ten transcripts. The zero-euro premise of the next eleven weeks
rests on this behaviour, and it is cheaper to falsify now than in week 10 with
a gate waiting on it.

### Task 6

`T-w01-6` — 1.0 h, Track A, testing. Run the ten-dispatch S0 battery and
measure real weekly headroom on the actual plan. It was priced at 0.25 h
against a criterion demanding ten logged runs, which is an order of magnitude
out; the missing 0.75 h came from T-w01-5, whose evidence this task now
produces.

Method, because *what to log* is not *how to measure*. Put `tasks/example.md`
through S0 ten times in one contiguous session on one pinned model, recording per
run from the CLI's JSON output: harness, model, `usage.input_tokens`,
`usage.output_tokens`, start and end timestamps, wall clock, and
`quota_stall_seconds` — elapsed time owed to the rate limiter rather than to the
model or your own code, the field SM-10 and SM-11 exclude their stalled samples
by. Count the runs finishing before the first that stalls; call it *k*. The
published reset window is five hours, giving 33 whole windows in a 168-hour week,
so extrapolated weekly headroom is *k* × 33 — an upper bound, since the weekly
cap is unpublished and may bind first. If nothing stalls you have not found the
ceiling: record 10 as a floor, label it `floor`, and do not multiply it up.

Isolation is the same distinction. The bucket is shared with the chat surface and
everything else on the account, so list every interactive turn inside the
battery's window or record that there were none. Without isolation the number is
a floor, not a measurement, and carries the label — the label is the deliverable,
because a contaminated figure presented as a measurement is what this task exists
to prevent. A measurement below 80 runs a week, twice the 40 this week plans,
authorises an immediate out-of-cycle canon delta rather than queueing behind M1,
whose mandated slot already belongs to the hour recalibration. A `floor` below 80
does not trip it: a floor describes the battery, not the ceiling.

### Task 7

`T-w01-7` — 0.5 h, Track B, theory, reinforcing A. Reading: `RES-14`. Read the
deep-module and information-hiding chapters, then argue the case for your own
adapter: it publishes harness differences as typed fields rather than
smoothing them flat. An interface holding only what two harnesses share
deletes the signal a later comparison would read, and deletes it invisibly.

### Task 8

`T-w01-8` — 1.75 h, Track B, building, reinforcing A. Implement the
HarnessAdapter Protocol and its first strategy, with a typed surface for
events, cost and exit reason. Exit reason is the field that repays the effort:
completed, refused, timed out and quota-stalled are four situations a boolean
collapses into one.

### Task 9

`T-w01-9` — 0.75 h, Track B, testing. Write contract tests over the adapter
asserting that the differences survive, and run them against a deliberate
in-repo fake — a recorded-output stub behind the same Protocol. A test
checking only the shared subset passes happily on the day the abstraction
starts lying, which makes it worse than no test.

### Task 10

`T-w01-10` — 2.5 h, Track E, business, reinforcing F. Write the positioning
and niche statement: who this is for, what problem, why you. Every prospect
chosen over the next eleven weeks is chosen against this page, so vagueness
here bills later rather than now. Small tightly targeted lists are reported to
reply at roughly 5.8% against roughly 2.1% for large blasts — directional only
— and targeting is the one lever a sender with no network holds.

### Task 11

`T-w01-11` — 1.5 h, Track E, business, reinforcing F. Research 10 prospects by
hand, from public sources only: no warm introduction, no referral, no existing
contact. Record one verifiable fact per prospect that could only have come
from reading about that company. These are the first rows of the funnel
[outreach](../business/outreach.md) owns, and the 1.5 h is the manual baseline
W04's assisted research is measured against.

## Deliverables

- [ ] D-w01-1 — S0 single-task runner at `agentplat/run.py` under its policy at `policy/agent-policy.v1.yaml`: a task file becomes a captured diff inside an isolated worktree, driven by an unattended subprocess, evidenced by the transcript at `docs/w01/transcript-no-tty.json`
- [ ] D-w01-2 — HarnessAdapter contract and its first strategy at `agentplat/harness/`, contract tests at `tests/test_harness_contract.py` proving typed differences survive, the quota-headroom log at `docs/w01/quota-headroom.jsonl` and the adapter note at `docs/w01/adapter-contract.md`
- [ ] D-w01-3 — Positioning and niche note at `docs/w01/positioning.md`, plus 10 hand-researched prospects in `prospects.local.md`, each carrying a verifiable personalisation fact
- [ ] D-w01-4 — Classification note at `docs/w01/classification-note.md` and the combined ambiguous-ticket report at `docs/w01/ambiguous-ticket-report.md`, all five parts, with its proving test at `tests/test_specificity_score.py`

## Acceptance criteria

- [ ] AC-w01-1a — `make demo-s0 TASK=tasks/example.md` — the canonical entry point, which wraps `python -m agentplat.run tasks/example.md` — exits 0 and writes a diff file; the run occurred in a worktree rather than the main checkout, and it took its allowed tools and permission mode from the versioned policy file with no interactive prompt reachable at any point (T-w01-3, T-w01-4, T-w01-5)
- [ ] AC-w01-1b — the captured JSON transcript parses and contains a session id, a pinned model id and a usage block; no authentication failure appears in any system or retry event (T-w01-5)
- [ ] AC-w01-2a — a deliberate in-repo fake second strategy, a recorded-output stub behind the same Protocol rather than a second real harness, is substituted at the call site with no caller code changed, and the contract tests run green against both; at least three harness-specific fields are exposed as typed attributes rather than dropped (T-w01-8, T-w01-9)
- [ ] AC-w01-2b — `docs/w01/quota-headroom.jsonl` records at least 10 runs, each with model id, tokens in and out, wall clock and `quota_stall_seconds`, and states measured weekly agent-run headroom as one number carrying its `measurement` or `floor` label; the adapter contract sketch names which context those runs took ambient, which was passed in, and which side of the sign-in boundary they sat on; and the note beside it argues why the adapter exposes harness differences instead of flattening them (T-w01-6, T-w01-2, T-w01-7)
- [ ] AC-w01-3a — 10 prospect records exist in `prospects.local.md`, each naming a source URL and one fact that could not have come from a template, and the week's funnel reading is logged under SM-15 and SM-16 in the scoreboard's weekly row format — `W01 | <date> | 10 prospects researched, 0 sends | evidence_source: real` (T-w01-11)
- [ ] AC-w01-3b — the positioning note names one niche, one recurring workflow, and one reason a buyer in that niche would answer this sender specifically (T-w01-10)
- [ ] AC-w01-4a — `docs/w01/classification-note.md` assigns each of the 29 stages of the four target workflow pipelines to workflow or agent and, for each, names what happens on failure — replay or re-prompt (T-w01-1)
- [ ] AC-w01-4b — the ambiguous-ticket report contains all five named sections and its proving test fails against the pre-mitigation runner, which dispatched both fixtures alike; and its safe-failure section agrees with the behaviour the classification note assigned to the Notion pipeline's `ambiguity detection` stage, which the pre-dispatch scorer is the week-one instance of (T-w01-1, T-w01-3)

## Stretch goal

Outside the 15 hours, never financed from acceptance work, and attempted only
once the four deliverables are ticked. Put the same task through Codex `exec` and
record where the approval-triggers-failure behaviour actually surfaces — an exit
code, a line on stderr, or a JSON event — then answer whether your adapter could
currently tell that apart from a genuine task failure.

## Failure exercise

One exercise, sitting at the very front of the pipeline: everything S0 does
downstream is wasted if what was dispatched was never specific enough to execute.
The full body lives in
[the agent-failure set](../exercises/agent-failures.md); D-w01-4 is the report.

### EX-FAIL-01 — ambiguous ticket

- **Detection.** The task file carries no acceptance predicate a machine can evaluate. Before dispatch the runner computes a specificity check — is a file or module named, is a done-condition stated, is there at least one verifiable assertion — and the check fails rather than the task. Detection sits before the model call, which is what makes it cheap.
- **Safe failure behaviour.** Refuse to dispatch. Do not let the agent guess and return a plausible diff against a requirement nobody wrote down: that is the expensive failure precisely because it arrives looking like success and is found weeks downstream.
- **Recovery.** Emit every missing element by name — one, two or all three, not the first one found — and re-queue the task in a `needs_clarification` state that a human resolves. Never auto-fill an absent acceptance criterion — a generated criterion is a guess wearing the costume of a specification.
- **Logging.** Record the task id, which specificity element was missing, and the raw task text. Those three fields make ambiguity countable across weeks instead of handled one ticket at a time, and the count is what says whether the ticket writer or the checker needs fixing.
- **Test proving the mitigation.** `tasks/ambiguous.md`, which carries no done-condition and no assertions, is refused before any model call; `tasks/example.md`, which carries both, dispatches normally. The refusal names every element it found missing rather than only the first. The refusal test fails against the pre-mitigation runner, which dispatched both alike.

## Reflection

1. Which flag did you remove first when the unattended run broke, and what does
   that tell you about which part of the context was actually load-bearing rather
   than merely present?
2. S0 dispatches a task and captures a diff. Name the step where a process death
   would leave the world inconsistent, and say why nothing you built this week
   would detect it.
3. Did the measured quota match the published figure or diverge? If one agent
   turn spends quota like several typed prompts rather than one, which of this
   week's own runs — the battery, the contract tests, or the stretch on the
   second harness — would you have given up first, and what does that ordering
   say about which of them you actually believe is evidence?

## Evidence

- `make demo-s0 TASK=tasks/example.md` — this stage's runnable demo command, and the canonical one; it wraps `python -m agentplat.run` — with a path to the runner and the diff it captured.
- The JSON transcript from the run with no TTY attached.
- The 10-run battery: one contiguous session, ten dispatches, with every interactive turn that shared its window listed or declared absent.
- The quota-headroom log at `docs/w01/quota-headroom.jsonl`, carrying the measured weekly agent-run figure and its `measurement` or `floor` label.
- Path to the positioning note and the 10 prospect records.
- Path to the ambiguous-ticket report and its refusal test.

Log actual hours below as one line, planned first:
`Theory 2.5 / <actual> · Building 6.0 / <actual> · Testing 2.5 / <actual> ·
Discovery 4.0 / <actual>`. M1's mandated recalibration reads these regions bucket
by bucket across the first four weeks, and one logged as a paragraph cannot be
read by it. Prospect counts belong in [the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W01" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- S0 turns a task file into a captured diff, unattended — 30
- The adapter contract holds under its own tests — 20
- Weekly quota headroom measured and written as a number — 15
- The ambiguous-ticket report carries five named parts — 15
- Positioning note written, 10 prospects researched — 20
