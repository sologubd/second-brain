# Week 12 — Least Privilege, Approval Boundaries and the Retrospective

## Outcome

By Sunday every tool the platform can call runs under a profile you can point at,
an unapproved privileged action is refused and logged, and agent-executed code
cannot reach the network. You have made a confused-deputy forgery work and then
made it fail. And you have issued a verdict — or an explicit non-verdict — on the
first SaaS candidate, and rewritten months 4–12 against what twelve weeks actually
taught you.

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

**Approval gates on irreversible actions.** Explicit, per action, and — critically —
**per action, not per session.** A session-level check falls to the same forgery
the confused-deputy exercise builds.

Note what makes these controls real, carrying week 11's distinction forward: a tool
profile is enforced **in code at the call site**, and re-authorization is a
comparison your code performs against a stored approval record. Neither depends on
the model agreeing. *Instructing* an agent to stay within its permissions is not a
permission system — **model refusal is not a security guarantee.**

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

~1.5h. Light on reading; the retrospective is where the hours go.

## Tasks

### Core — required (~15h: 1.5h learning, 8.5h building/testing, 2h business, 3h retrospective)

1. **Write tool profiles** for every tool, and enforce them at the call site.
   Refuse and log anything out of profile.
2. **Sandbox the code-execution surface**, with network egress blocked, and a test
   asserting the block.
3. **Add per-action re-authorization** against the request a human actually
   approved. Per action, never per session.
4. **Build the append-only audit log** with provenance on every tool call.
5. **Run the confused-deputy attack** — one attack, done properly, with the forgery
   working pre-patch and refused post-patch on the identical input. Below.
6. **Business: the verdict, or the refusal to issue one.** Apply the five kill
   criteria to the top candidate in the pain register. Issue a verdict — or an
   explicit non-verdict naming each missing threshold and the month it could
   realistically arrive. **"Insufficient evidence, deferred to month 5" is a
   passing deliverable.** "More research needed" is not a non-verdict; it is the
   absence of one.
7. **The twelve-week retrospective.** Below. Budget 3 hours and do not compress it
   — it is the input to everything after week 12, and it is the one task here whose
   value does not depend on any of the others being finished.

### Stretch — only after Core is DONE

- **The malicious-tool-output attack.** Below. Genuinely valuable, and a second
  full attack in the same week as the retrospective is not realistic. If it slips,
  run it in month 4 alongside the malformed-input work — they belong together.
- **Architecture review #3** with the five-axis rubric, all fourteen defect
  classes, and ≥2 accepted defects carrying remediation months. This is a 4-hour
  job. **Do not drop it — schedule it.** Its whole value is the comparison against
  review #1, and that comparison keeps just as well in month 4 as in week 12.
- **Scope credentials to the task**, short-lived, with expiry. Correct, and it
  needs a credential-issuing surface that a laptop build may not have yet.
- **Provenance on memory writes** as well as tool calls — relevant once the memory
  surface exists in month 5.

## Use it for real

Both attacks run against the real pipeline, not a test harness shortcut. The
forged instruction must travel the real path, and neither step may be modified to
make the attack land — if it needs a code change, it was not demonstrated.

## Measure

- Out-of-profile calls refused: 100%, each logged with the tool name.
- Confused deputy: privileged actions triggered per forgery attempt, before and
  after the patch. This is the week's headline pair.
- Latency added per privileged action by the re-authorization check, p50.
- *(Stretch)* hostile tool-output values reaching the instruction context, before
  and after; review-#1 findings closed over review-#1 findings recorded.

## Failure exercises

The confused deputy is Core. Malicious tool output is Stretch — run it if the week
allows, and carry it to month 4 if not.

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

**Malicious tool output** *(Stretch)*. Treat a tool's return value as
attacker-controlled, because it is.

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

- [ ] Per-tool least-privilege profiles, enforced at the call site and logged.
- [ ] Per-action re-authorization against the approved request.
- [ ] Sandboxed execution surface with network egress blocked, asserted by a test.
- [ ] Append-only audit log with provenance on every tool call.
- [ ] Confused-deputy report: working forgery, patch, unchanged re-test.
- [ ] SaaS verdict or explicit dated non-verdict against the five kill criteria.
- [ ] Twelve-week retrospective, all five questions, plus the rewritten months
      4–12 sequence.
- [ ] *(Stretch, if reached)* malicious-tool-output report; architecture review #3;
      task-scoped credentials. Anything not reached is **scheduled**, with a month
      named — not silently dropped.

## Done when

- [ ] Every tool has a named profile, and an out-of-profile call is refused **in
      code at the call site** and appears in the audit log.
- [ ] Agent-executed code cannot reach the network, and a test proves it.
- [ ] Pre-patch, the forgery causes ≥1 privileged action, evidenced from the audit
      log. Post-patch, the identical input causes zero, and the refusal names the
      approved request it was compared against.
- [ ] Nothing in the security write-up rests on the model having declined.
- [ ] All 5 kill criteria are evaluated or explicitly marked unevaluable with a
      reason; a non-verdict names ≥1 specific unmet threshold and a date.
- [ ] The retrospective is written, and **the months 4–12 files have been edited to
      match what it concluded.**
- [ ] Every Stretch item not reached has a named month, in writing.

## Reflection

1. The deputy was confused because it trusted its caller. Which other component in
   your build trusts its caller the same way?
2. Which of your security controls would still hold against a model that had been
   fine-tuned to be maximally compliant with whatever it read? The ones that would
   not are defense in depth, and that is fine — as long as you know which is which.
3. If you issued a non-verdict, what would you have concluded had you forced a
   score — and would that conclusion have been the one you wanted?
4. *(If you ran review #3)* Compare it with review #1. Did the platform get better,
   or did your review get better? What evidence separates the two?

## Evidence

- Tool profiles, and audit-log entries for refused calls.
- Sandbox egress test.
- Confused-deputy report, with audit-log evidence from both arms.
- SaaS verdict or non-verdict.
- The retrospective document, and the edited months 4–12 files.
- Anything from Stretch that was reached; the scheduled month for anything not.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___

---

**Twelve weeks done.** Next: [months 4–6](../later/months-04-06.md) — but read
your own retrospective first, and change them.
