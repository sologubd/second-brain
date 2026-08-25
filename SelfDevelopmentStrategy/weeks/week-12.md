# Week 12 — Least privilege, the confused deputy, and the first verdict

## Outcome

By Sunday every tool the platform can call runs under a profile I can point at,
an unapproved privileged action is refused and logged, and I have issued a
verdict — or an explicit, defensible non-verdict — on the first SaaS candidate.

## Time budget

- Theory: 3.0 h
- Building: 6.0 h
- Testing/evaluation: 3.5 h
- Customer discovery: 2.5 h

Customer discovery sits exactly on its 2.5 h floor, the only week in the
programme that does, and buys no outreach at all: the last sends went out in W09
and the whole list had matured by the end of W10. Both business tasks are
judgement rather than volume — T-w12-12 assembles checkpoint evidence, T-w12-13
issues the verdict. The floor protects business *time*, not business *activity*.

Zero new subsystems: S7b extends S7a, so the one-subsystem cap goes unspent and
the 6.0 h of building widens an existing surface. Testing is at 3.5 h, the
highest figure any week in the phase carries. The run ceiling is 45 agent runs
against EUR 0.00 of metered
spend; canon attaches no reasoning to that count, so it is rendered and left.

Compressed week, 8.0 h: T-w12-3, T-w12-4, T-w12-6 halved to 0.5 h, T-w12-11 —
the M3 retrospective is never cut — and T-w12-12 with T-w12-13 at the 2.5 h
floor, then slip the calendar rather than doubling up. The sandbox, architecture
review #3 and the malicious-tool-output exercise defer to month 04. Record what
that costs: review #3 slipping means only two of the three phase-1 reviews were
completed, and that belongs in the M3 checkpoint rather than quietly dropped from
it. D-w12-4 and D-m03-4 tick. D-w12-1 carries without its sandboxed execution
surface, D-w12-2 at half depth on one half and untouched on the other, D-w12-3
whole. DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| least privilege | D | P0 | T-w12-3's per-tool profiles → D-w12-1 |
| privilege boundaries | D | P0 | the real differential T-w12-6 exploits → D-w12-2 |
| confused deputy problems | D | P0 | T-w12-6, pre-patch and post-patch → D-w12-2 |
| excessive agency | D | P0 | T-w12-3's approval gates on irreversible actions |
| sandboxing | D | P1 | T-w12-2 at concept level, T-w12-5 in the build |
| approval gates | D | P0 | T-w12-3, as the placement audit rather than the mechanism |
| secrets | D | P1 | T-w12-3's scoped short-lived tokens; depth waits for M04 |
| audit logs | D | P0 | T-w12-4 → D-w12-1 |
| malicious tool output | D | P0 | T-w12-7 → D-w12-2 |
| reviewing generated code | B | competency CM-17 | T-w12-8 → D-w12-3 |
| kill criteria | F | P0 | T-w12-13's five criteria → D-w12-4 |

Ten rows carry a P-priority; one does not. Reviewing generated code has no
concept row in canon — it exists as competency CM-17 — so the canon-sourced
string goes in the Priority column rather than a P-tag invented for it.
Sandboxing and secrets are the only P1 rows here.

Nine rows reason from [Track D](../tracks/ai-security.md), which closes its
phase-1 arc this week. Reviewing generated code belongs to
[Track B](../tracks/system-design.md), where the rubric lives; kill criteria is
a [Track F](../tracks/micro-saas.md) concept homed in
[the SaaS validation file](../business/saas-validation.md), beside the seven
thresholds W11 resolved. S7b is defined in
[the platform file](../projects/engineering-agent-platform.md), the 14 defect
classes and AR-03's mode in
[the review set](../exercises/architecture-reviews.md), and EX-FAIL-14 in
[the agent-failure set](../exercises/agent-failures.md). The M3 retrospective is
answered in [month 03](../months/month-03.md) rather than here. Tasks, hours and
acceptance are owned by this file.

## Tasks

### Task 1

`T-w12-1` — 1.0 h, Track D, theory. Reading: `RES-11`. Least privilege and the
confused deputy: a program holding more privilege than its caller, tricked
into misusing it on the caller's behalf. Canon dates it to Norm Hardy in 1988
and notes that OWASP's identity-and-privilege-abuse category cites the classic
reading directly.

### Task 2

`T-w12-2` — 1.0 h, Track D, theory. Reading: `RES-11`. Sandboxing tiers, at
concept level only. A container is namespace and cgroup isolation over a
shared kernel and is NOT a hard security boundary against a malicious
workload; a user-space kernel intercepts syscalls at an I/O cost; a microVM
gives hardware-enforced isolation with a dedicated kernel. Recognising which
tier you actually run is all the hour owes.

### Task 3

`T-w12-3` — 2.5 h, Track D, building, reinforcing A. Build S7b: a named
least-privilege profile per tool, scoped short-lived tokens for the CRM and
the repository, and an approval gate on every irreversible action. Per-tool
and per-action, never per-service: one broad token hands the agent the union
of every permission any step ever needed, permanently. Short lifetime does
work redaction cannot, since any credential in context can leave through the
output channel.

### Task 4

`T-w12-4` — 1.5 h, Track D, building. Build the append-only audit log,
carrying provenance on every tool call and memory write — where the input came
from and at what trust level, recorded at write time. Untagged, a write
function looks identical whether the fact came from a verified sync or an
anonymous message, and no read-time policy can be stated over it.

### Task 5

`T-w12-5` — 1.0 h, Track D, building. Sandbox the agent's code-execution
surface: restricted filesystem, no network, a dedicated working directory. One
hour buys the tier T-w12-2 named and an escape attempt that fails, not a
hardened platform.

### Task 6

`T-w12-6` — 1.0 h, Track D, testing. The confused-deputy exercise. Make the
low-privilege classification step relay a forged high-impact instruction that
the high-privilege write step executes without re-checking the original human
request. Then patch with per-action re-authorization and re-test. The
privilege differential between those steps is genuine rather than staged,
which is what makes it an exercise rather than a demonstration.

### Task 7

`T-w12-7` — 1.0 h, Track D, testing. The malicious-tool-output exercise: a
tool returns attacker-shaped content, and the report says what happened. Tool
output is the trust boundary engineers most reliably forget, because the tool
is "ours" — and a tool reading an issue or a web page is a conduit for
attacker text.

### Task 8

`T-w12-8` — 1.0 h, Track B, theory, reinforcing A and D. Reading: `RES-14`.
Formalise the generated-code review checklist into the five-axis rubric: AX-1
correctness-under-repetition, AX-2 crash-window durability, AX-3 concurrency
and AX-4 contract and boundary assumptions are the four questions T-w04-6
versioned, now named and scored separately. AX-5 is the addition — security:
which trust boundary, privilege or injection surface does this touch? Five
scored outputs, never one aggregate, because an aggregate hides the
disagreement worth reading. S2b automates this at M04; the hour writes the
instrument.

### Task 9

`T-w12-9` — 1.0 h, Track B, building. Architecture review #3, self-inspection
of the full platform through S7b against the 14 defect classes, conducted with
the rubric T-w12-8 just wrote. AR-03 is the last review of phase 1 and the
only one covering the whole platform.

### Task 10

`T-w12-10` — 0.5 h, Track B, testing. Write the AR-03 record naming at least
two ACCEPTED defects, each with a remediation plan and a target month.
Accepted, not fixed: a self-review returning a clean bill of health is the
least credible output available, and what you chose to live with is the part a
reader trusts.

### Task 11

`T-w12-11` — 1.0 h, Track P, testing. Answer the M3 retrospective in [month
03](../months/month-03.md): RQ-01 through RQ-10 in full, then RQ-11, the canon
delta. M03's mandated delta is ecosystem re-verification — every volatile
claim re-checked against its primary source in canon's priority order,
beginning with the OWASP LLM category numbering left deliberately unnumbered
at authoring time. The loop itself is documented in
[HOW-TO-EDIT](../HOW-TO-EDIT.md#the-control-loop): follow it, do not restate
it.

### Task 12

`T-w12-12` — 0.5 h, Track E, business, reinforcing F. Pull the CP-M3 evidence
pack: deliverable ids read against the competency matrix and the maturity
model. Half an hour, because the evidence already exists — but assembling it
is where a missing id becomes visible while a retrospective is still open to
record it.

### Task 13

`T-w12-13` — 2.0 h, Track F, business, reinforcing E. Apply the five kill
criteria to the top candidate on the pain register and issue a verdict — or an
explicit non-verdict naming what evidence is missing and when it could exist.
Canon makes the non-verdict a passing deliverable, and the reason holds: a
framework that always returns a score cannot kill anything, because a score
stays actionable in whichever direction its author already wanted. Under the
corrected funnel, "insufficient evidence, deferred to month 05" is the
expected outcome.

## Deliverables

- [ ] D-w12-1 — S7b security boundaries: per-tool least-privilege profiles, scoped short-lived tokens, approval gates on irreversible actions and a sandboxed code-execution surface — definition of done includes the append-only audit log carrying provenance on every tool call and memory write — at `agentplat/security/`, `policy/tool-profiles.v2.yaml`, `docs/w12/audit-log.jsonl`
- [ ] D-w12-2 — Combined attack and failure report, confused deputy and malicious tool output, with all five parts for each, including the per-action re-authorization patch and its re-test — at `docs/w12/deputy-and-tool-output-report.md`, `tests/attacks/test_deputy.py`
- [ ] D-w12-3 — Architecture review #3 (self, full platform): a record against the 14 defect classes conducted with the five-axis rubric, naming at least two accepted defects with a remediation month — at `docs/adr/adr-003-arch-review-3.md`
- [ ] D-w12-4 — SaaS verdict or explicit non-verdict against the five kill criteria, with the missing evidence named and dated if the verdict is deferred — at `docs/w12/saas-verdict.md`

## Acceptance criteria

- [ ] AC-w12-1a — every tool the platform can call has a named profile, and a call outside its profile is refused and logged, proved by a test; the profiles are per-tool rather than one shared token, and the sandbox tier the runner actually gets is stated in writing (T-w12-3, T-w12-1, T-w12-2)
- [ ] AC-w12-1b — tokens are scoped and short-lived, and a test asserts an expired token cannot be reused (T-w12-3)
- [ ] AC-w12-1c — the audit log is append-only and every entry carries provenance — where the input came from and at what trust level (T-w12-4)
- [ ] AC-w12-1d — agent-executed code cannot reach the network or the filesystem outside its working directory, proved by an attempt that fails (T-w12-5)
- [ ] AC-w12-2a — the unauthorized action demonstrably executes PRE-patch and is blocked POST-patch without breaking a legitimate flow; the attack is misuse of already-granted trust, not stolen credentials (T-w12-6)
- [ ] AC-w12-2b — the report names at least one OTHER place in the build where one component implicitly trusts another's output (T-w12-6)
- [ ] AC-w12-2c — both exercises have all five named sections; the malicious-tool-output proving test fails against the pre-mitigation code (T-w12-6, T-w12-7)
- [ ] AC-w12-3a — the rubric has five named axes, each producing an independently scored and separately cited output (T-w12-8)
- [ ] AC-w12-3b — the review record names at least two ACCEPTED defects with a remediation plan and a target month — not a clean bill of health — and cites the defect class behind each (T-w12-9, T-w12-10)
- [ ] AC-w12-4a — the verdict cites the pain register by row id and the resolved evidence thresholds by number, and if it is a non-verdict it names exactly which threshold lacks evidence and the month by which that evidence could exist; the M3 delta is written into `canon/canon.yaml` with `meta.version` raised, and the CP-M3 evidence pack maps each of its 8 deliverable ids to a competency row (T-w12-13, T-w12-11, T-w12-12)

## Stretch goal

Outside the 15 hours. Threat-model the approval gate itself: what does an
attacker who can influence the rendered approval payload achieve, and what would
detect it? The gate is the last human-readable surface in the system, which
makes it the most valuable thing to lie to. Attempt it only once all four
deliverables are ticked.

## Failure exercise

Two exercises, and both are about a component trusting something it should not:
one trusts a tool, the other trusts a peer. Bodies live in
[the agent-failure set](../exercises/agent-failures.md); D-w12-2 is the report.

### EX-FAIL-14 — malicious tool output

- **Detection.** Tool output carrying instruction-shaped content, or output failing its declared schema. Detected at the tool boundary by schema validation, before the output enters context — the placement is the control, since a check applied afterwards argues with a model that has already read the text.
- **Safe failure behaviour.** Tool output is untrusted input, not internal data. A schema with no field for an instruction cannot carry one, so validation holds without needing the model's cooperation.
- **Recovery.** Reject the output, record the rejection, re-invoke with a constrained variant, and dead-letter after N rejections rather than accept a degraded parse. The degraded parse is the tempting failure: it looks like resilience and is the attack's success path.
- **Logging.** Record the tool name, the raw output, the validation error and what the agent did next. The last field is the one usually dropped and the only one showing whether the rejection changed the run.
- **Test proving the mitigation.** A stubbed tool returning instruction-laden and schema-violating output is rejected at the boundary and never reaches the model's instruction context. It fails against a version passing tool output through as text.

### Confused deputy — a forged instruction crossing a real privilege boundary

- **Detection.** Put defect class DC-14 to the build: does a low-privilege step get to make a high-privilege one act on its say-so, the human's original request never consulted again? That is answered by attempting it, not by reading code — and the check beside it is whether the two steps run as separate processes under separate credentials.
- **Safe failure behaviour.** The high-privilege step re-authorizes per action against the human's original request rather than trusting an internal caller. Internal provenance is not authorisation: being "ours" says nothing about what a component relays.
- **Recovery.** Patch with per-action re-authorization and re-run the attack, then answer what the patch raises: the MINIMUM re-check that closes this without reimplementing authorization at every hop. The report names one other place in the build carrying the same implicit trust.
- **Logging.** The audit entry for the privileged call carries provenance — the instruction's origin and trust level — so a forged relay is distinguishable after the fact, not only during the exercise.
- **Test proving the mitigation.** The unauthorized action executes before the patch and is blocked after it, with a legitimate flow still passing. It fails against the pre-patch build — and a version blocking the legitimate flow has not passed either, since refusing everything is not a control.

## Reflection

1. Where ELSE in this build does one component implicitly trust another
   component's output?
2. What is the MINIMUM re-check that would have caught the confused deputy
   without reimplementing full authorization at every hop?
3. Review #3 named accepted defects rather than a clean bill of health. For each,
   state what evidence would move it from accepted to must-fix, and by when.

## Evidence

- `make demo-s7b-deputy` — this stage's runnable demo command — with a path to S7b and the per-tool profile definitions.
- The test showing a call outside its profile refused and logged.
- A sample of the append-only audit log showing provenance on a tool call.
- The sandbox escape attempt that fails.
- The confused-deputy pre-patch and post-patch runs.
- Path to the review #3 record naming its accepted defects.
- Path to the SaaS verdict or explicit non-verdict.
- The CP-M3 evidence pack and the M3 canon delta.

Log actual hours below as one line, planned first: `Theory 3.0 / <actual> ·
Building 6.0 / <actual> · Testing 3.5 / <actual> · Discovery 2.5 / <actual>`.
This closes the twelve-region series the recalibrations read: twelve weeks in
one shape is what lets the M3 delta say whether the M1 correction held or
drifted.

<!-- user:actuals key="W12" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- Every tool runs under a named profile and violations are refused — 20
- The audit log is append-only and carries provenance — 15
- The sandbox holds against an escape attempt — 10
- The confused deputy executes pre-patch and is blocked post-patch — 20
- Both failure reports carry all five named parts — 10
- Architecture review #3 is written with its accepted defects — 15
- A verdict or an explicit non-verdict is issued — 10
