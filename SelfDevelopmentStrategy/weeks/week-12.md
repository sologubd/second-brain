# Week 12 — Least Privilege, Approval Boundaries and the Retrospective

## Outcome

By Sunday every tool the platform can call runs under a profile you can point at,
an unapproved privileged action is refused and logged, agent-executed code cannot
reach the network — and you have reviewed the whole platform, named at least two
defects you are *accepting*, and issued a verdict or an explicit non-verdict on
the first SaaS candidate.

## Why now?

Week 11 stopped untrusted content from reaching an outbound tool. This week
addresses the other half: what the agent is allowed to do *at all*, and whether a
low-privilege step can make a high-privilege one act. Least agency is the cheapest
security control you have, and it only becomes concrete once there are enough tools
for a profile to constrain.

It is also the last week, so it closes the loop: a full review, and the first
business verdict.

## Build

**Per-tool least-privilege profiles.** Every tool has a named profile listing what
it may touch. A call outside its profile is refused and logged. Not "the agent has
the union of every permission any of its steps ever needed" — that union is
defect class 14, and it is the default shape generated code arrives in.

**Scoped, short-lived credentials.** Tokens scoped to the task, expiring with it.

**Approval gates on irreversible actions.** Explicit, per action, and — critically —
**per action, not per session.** A session-level check falls to the same forgery
the confused-deputy exercise builds.

**A sandboxed code-execution surface.** Agent-executed code cannot reach the
network. The concept is one paragraph: a container is not a hard boundary, a
microVM is. Do not spend the week studying sandbox internals; spend it making the
boundary real and testing that it holds.

**An append-only audit log with provenance** on every tool call. A refusal with no
record is an assertion about the past rather than evidence of it.

## Learn

- The least-agency section of the OWASP agentic PDF, if you have not already.
- One paragraph on sandbox depth: container versus microVM, and what each actually
  guarantees. That is genuinely all you need.

~2h. Light on reading; heavy on the review and the retrospective.

## Tasks

1. **Write tool profiles** for every tool, and enforce them at the call site.
   Refuse and log anything out of profile.
2. **Scope credentials** to the task, with expiry.
3. **Add per-action re-authorization** against the request a human actually
   approved.
4. **Sandbox the code-execution surface**, with network egress blocked, and a test
   asserting the block.
5. **Build the append-only audit log** with provenance on every tool call and every
   memory write.
6. **Run the two attacks** — confused deputy, malicious tool output. Both below.
7. **Architecture review #3.** Formalise the four recurring questions into a
   five-axis rubric — correctness under repetition, crash-window durability,
   concurrency, contract and boundary assumptions, privilege — and review the full
   platform against the fourteen defect classes. **Name at least two defects you
   are accepting**, each with a remediation month. A clean bill of health on a
   system this size is the least credible possible output. Every finding from
   review #1 is marked remediated, accepted, or re-reported — none dropped
   silently. Details in
   [exercises/architecture.md](../exercises/architecture.md).
8. **Business: the verdict, or the refusal to issue one.** Apply the five kill
   criteria to the top candidate in the pain register. Issue a verdict — or an
   explicit non-verdict naming each missing threshold and the month it could
   realistically arrive. **"Insufficient evidence, deferred to month 5" is a
   passing deliverable.** "More research needed" is not a non-verdict; it is the
   absence of one.
9. **The twelve-week retrospective.** Below.

## Use it for real

Both attacks run against the real pipeline, not a test harness shortcut. The
forged instruction must travel the real path, and neither step may be modified to
make the attack land — if it needs a code change, it was not demonstrated.

## Measure

- Out-of-profile calls refused: 100%, each logged with the tool name.
- Confused deputy: privileged actions triggered per forgery attempt, before and
  after the patch.
- Malicious tool output: hostile values reaching the instruction context, before
  and after.
- Latency added per privileged action by the re-authorization check, p50.
- Review: all 14 classes assessed, all 5 axes scored independently, review-#1
  findings closed over review-#1 findings recorded.

## Failure exercises

**The confused deputy.** Make a low-privilege step cause a high-privilege one to
act, without either being compromised.

Take the path where a classification or extraction step reads attacker-supplied
text while the write step holds real privilege. Craft an input that makes the low
step relay a forged high-impact instruction, and show the write step executing it
without re-checking the original human request. Then patch it: every privileged
action re-authorizes against the request a person actually approved. Re-run the
forgery unchanged.

- **Detection.** A privileged action fires whose authority traces to text, not to
  an approval record.
- **Safe failure.** Refuse any privileged action that cannot name the approved
  request it is acting under.
- **Recovery.** Per-action re-authorization. Not per-session.
- **Logging.** The audit entry for the refusal contains the id of the original
  approved request it was compared against.
- **Proving test.** The forgery causes ≥1 privileged action pre-patch, evidenced
  from the audit log; post-patch the identical input causes zero and the refusal is
  logged. A test asserts the re-authorization check fires ≥2 times inside a single
  multi-action task.

**Malicious tool output.** Treat a tool's return value as attacker-controlled,
because it is.

Stub a tool returning two hostile shapes: content shaped like instructions, and
content violating the tool's declared schema. Record what the current agent does
with each. Then validate at the tool boundary, **before the output enters context** —
after the model has read it, it is not a control. Use a schema with **no field wide
enough to carry an instruction**, or the control is decorative. Rejection is
bounded: after N refusals the task dead-letters rather than accepting a degraded
parse, with N fixed and stated in advance.

- **Proving test.** Zero instruction-shaped values reach the instruction context;
  100% of shape violations are refused at handover, tool named. **The pass-through
  build fails containment on the first fixture.**

## The twelve-week retrospective

Answer these in writing. It is the most valuable two hours of the quarter.

1. Which weeks produced something you still use? Which produced an artifact you
   have not opened since?
2. Where did you build ahead of the pain — a mechanism that never answered a
   problem you actually had? Name it. That is the earn-complexity rule failing, and
   it will fail the same way in months 4–12 unless you can see it.
3. What is the single biggest failure mode of the platform right now, from
   telemetry rather than from feeling?
4. From the scoreboard: which metric changed a decision? Delete the ones that did
   not.
5. Rewrite the months 4–12 plan against what you now know. Not a rewrite of the
   ambition — a rewrite of the *sequence*, on evidence.

## Deliverables

- [ ] Per-tool least-privilege profiles, enforced and logged.
- [ ] Task-scoped short-lived credentials.
- [ ] Per-action re-authorization against the approved request.
- [ ] Sandboxed execution surface with network egress blocked, asserted by a test.
- [ ] Append-only audit log with provenance on every tool call and memory write.
- [ ] Confused-deputy report: working forgery, patch, unchanged re-test.
- [ ] Malicious-tool-output report: two hostile shapes, boundary validation, the
      recorded post-rejection behaviour.
- [ ] Architecture review #3 as an ADR: five-axis rubric, all 14 classes, ≥2
      accepted defects with remediation months, every review-#1 finding accounted
      for.
- [ ] SaaS verdict or explicit dated non-verdict against the five kill criteria.
- [ ] Twelve-week retrospective, all five questions, plus the rewritten months
      4–12 sequence.

## Done when

- [ ] Every tool has a named profile, and an out-of-profile call is refused and
      appears in the audit log.
- [ ] Agent-executed code cannot reach the network, and a test proves it.
- [ ] Post-patch, the identical confused-deputy forgery causes zero privileged
      actions, and the refusal names the approved request it was compared against.
- [ ] Zero instruction-shaped tool outputs reach the instruction context, and the
      task dead-letters after exactly N refusals with N stated in advance.
- [ ] All 5 review axes are scored independently, each with its own citation, and
      ≥2 defects are recorded as accepted with named remediation months.
- [ ] Every review-#1 finding is marked remediated, accepted or re-reported, with
      zero dropped.
- [ ] All 5 kill criteria are evaluated or explicitly marked unevaluable with a
      reason; a non-verdict names ≥1 specific unmet threshold and a date.
- [ ] The months 4–12 files have been edited to match what the retrospective
      concluded.

## Reflection

1. The deputy was confused because it trusted its caller. Which other component in
   your build trusts its caller the same way?
2. You accepted two defects. What would have to change — in load, in users, in who
   runs this — for one of them to stop being acceptable?
3. Compare review #3 with review #1. Did the platform get better, or did your
   review get better? What evidence separates the two?
4. If you issued a non-verdict, what would you have concluded had you forced a
   score — and would that conclusion have been the one you wanted?

## Evidence

- Tool profiles, and audit-log entries for refused calls.
- Sandbox egress test.
- Confused-deputy report, with audit-log evidence from both arms.
- Malicious-tool-output report.
- Review #3 ADR with the five-axis rubric and accepted defects.
- SaaS verdict or non-verdict.
- The retrospective document.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___

---

**Twelve weeks done.** Next: [months 4–6](../later/months-04-06.md) — but read
your own retrospective first, and change them.
