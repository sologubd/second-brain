# Phase 03 — Production AI

## Arc

Phase 03 spans [M05](../months/month-05.md) and [M06](../months/month-06.md).

Two capabilities that the programme has been careful not to fake finally get
their surface here, and the order matters.

The first is memory. Until now the platform has had task state — deterministic
process bookkeeping — and a retrieval corpus written by a separate ingestion
process. Neither is agent memory, and treating them as if they were is the
category error this phase exists to prevent. BOA-S2 gives the business agent
durable per-account memory: facts it writes about a contact and that a later,
unrelated decision cycle reads back as trusted. The moment that exists, a new
threat class exists with it, and the month spends its security hours writing a
false fact into memory through an untrusted inbound message, watching a separate
decision act on it, then blocking it with one structural mitigation and
re-running the attack to measure the difference.

The second is authorization as policy. The knowledge agent's rules have
accumulated as scattered conditionals; M06 expresses them as roles first, adding
attribute-based rules only where an exercise genuinely needs a context-dependent
condition such as a value threshold. The enforcement point and the decision
point are separated deliberately — implemented as a hand-written pre-execution
check, with a written statement of what a real policy engine would add and why
that is not worth its operating cost at this scale.

Entering, the system is integrated but its trust model is implicit. Leaving, it
can say which policy model each surface needs and why, and it has been attacked
at the one place where an attack persists across sessions.

The consulting track also stops being preparation in this window: M06 turns the
qualified pain register into a productized offer with fixed scope and a stated
payback period. A missed month here slips the calendar; the memory work in
particular is not compressible, because the attack is only meaningful once the
false fact has survived into a genuinely separate decision cycle.

## Entry conditions

- [ ] D-m04-2 and D-m04-3 hold, so external effects are already durable before
      a second writer — memory — is added to the same task lifecycle.
- [ ] The business agent's append-only audit trail from D-w04-2 is live, because
      provenance at write time is what any read-time memory policy is expressed
      against.
- [ ] The M04 scope recalibration is applied and months 05 through 12 have been
      re-costed against real logged hours.
- [ ] D-w11-1 holds — provenance tagging, trust-tiered retrieval and the
      structural trifecta break — since memory poisoning is the same argument
      applied to a surface the agent writes itself.
- [ ] The knowledge agent's tenant isolation from D-m04-4 is in place before
      authorization is refactored on top of it.

## Exit conditions

- [ ] D-m05-1 holds: durable per-account memory exists, written by the agent and
      read as trusted fact by a later, separate decision cycle.
- [ ] D-m05-2 holds: a poisoned memory is demonstrably acted on, then blocked by
      one provenance, write-time-validation or TTL mitigation, with before and
      after re-runs measured. This closes portfolio item PF-05.
- [ ] D-m05-3 holds: malformed input is handled beside the malicious-input work,
      and sandboxing depth is stated rather than assumed.
- [ ] D-m06-1 and D-m06-2 hold: role-based authorization on the knowledge agent,
      with the enforcement and decision points separated and the
      no-policy-engine decision written down.
- [ ] D-m06-3 holds: a productized offer with fixed scope and a stated payback
      period, and D-m06-4 adds agent roles, skills and failure reporting at S9.
- [ ] The M05 security-arc recalibration and the M06 competency reassessment are
      both written.

## Checkpoints

The phase closes on **CP-M6**, whose decision question and seven evidence ids
live in [the portfolio file](../reference/portfolio.md). What they amount to:
a retrieval system with measured metrics against a frozen label set and a
pre-filter authorization proof; an attack report with success rates before and
after structural mitigations, memory poisoning included; traces carrying cost
and quota attribution; and a three-tier regression gate.

Two mandated deltas gate the phase internally. The M05 delta reassesses the
security arc directly: Track D covers seventeen topics from an Awareness
baseline in a compressed allocation, and after the memory-poisoning work there
is finally enough evidence to say whether months 06 through 08 need to carry
more of it. The M06 delta re-rates every column of
[the competency matrix](../reference/competency-matrix.md) against delivered
deliverable ids ahead of the checkpoint. Any 6-month target unmet and unevidenced is
re-planned or downgraded rather than quietly carried forward.

## Security arc

This phase is the arc's centre of gravity. Phase 01 attacked a corpus the agent
only read; phase 02 widened the blast radius across three external systems; here
the agent's own writes become the attack surface, which is the one that
persists.

The distinction the month must hold precisely: memory poisoning is not corpus
poisoning and neither is goal hijack. Corpus poisoning contaminates documents an
ingestion process wrote. Memory poisoning contaminates facts the agent itself
wrote and later trusts, so the payload survives the session that delivered it
and fires in a decision that never saw the original message. The exercise bodies
and the verbatim distinctions live in
[the security exercise set](../exercises/ai-security.md); the concept inventory
and the identifier policy live in [Track D](../tracks/ai-security.md).

M06 then closes the least-privilege line phase 01 opened at D-w12-1. Per-tool
profiles and scoped tokens made privilege narrow; role-based policy makes it
*legible*, which is what allows a reviewer to check it rather than trace it.

Beyond this phase no further Track D topic is scheduled. That is a position, not
an omission, and the M05 delta is the mechanism that can revise it.

## What this phase does not cover

Ten brief topics land in these two months rather than going unassigned:
agent memory, memory poisoning, the business agent's malformed-input handling
and sandboxing depth at M05; policy engines and role- and attribute-based
authorization, plus Track E pricing and proposals, at M06. Three more are homed
at M05 because they depend on evidence phase 01 could not manufacture — Track F
competition analysis, the Track E subcontracting side-quest, and case study
production. Their specifics belong to the month files.

Not covered here: the first external pilot and its measured baseline, which
cannot be scheduled because it depends on a funnel; schema migrations and API
evolution; and Track F applied at scale. Those belong to
[phase 04](phase-04-consulting.md) and
[phase 05](phase-05-productization.md).

Also absent by ownership: hours, tasks and topic inventories. Nothing here says
what the reader studies; only what the system can do at each boundary.
