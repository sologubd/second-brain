# Track D — AI Security

## What these hours buy

22.5 h, 12.5% of the programme, and every hour points at systems the learner
built. Nothing here is attacked in a lab.

An indirect-prompt-injection suite of at least three distinct techniques, seeded
into your own retrieval index, with the attack success rate measured before and
after one structural mitigation. A data-exfiltration attempt including at least
one covert channel — data encoded into a helpful-looking URL parameter —
reported against the legs of the trifecta it exploits. A confused-deputy
demonstration, patched with per-action re-authorization and re-tested. Per-tool
least-privilege profiles with scoped short-lived tokens. An append-only
provenance audit log. And a sandboxed code-execution surface. Portfolio item #5,
the security attack and evaluation report, opens at W11 and closes at month 05.

The measurement is the point, and it constrains what this file may say. Every
number here is an attack success rate against your own system, before and after.
This track states **no percentage for how effective any injection defence is**:
no independently verified primary benchmark met the sourcing bar, and a borrowed
industry figure would be exactly the unearned authority these exercises replace.

The same discipline governs identifiers. The Agentic Top 10 categories ASI01 to
ASI10 were verified against the source PDF and may be cited by identifier;
prefer that PDF to any vendor summary. The older category list is used by **name
only** — Prompt Injection, Excessive Agency — never numbered, because a newer
edition appears to renumber at least one category and that was never confirmed
against its primary source.

## Entry competency

Awareness, level one, user-supplied and joint-weakest in the programme. `CM-13`
records none of the three habits this track depends on: attacking a design
systematically, mapping where trust changes hands, or budgeting privilege
deliberately.

The consequence is a sequencing rule that reads as a concession and is not one.
Weeks 11 and 12 open on concepts rather than attacking from day one, because an
attack you cannot classify teaches nothing reusable — and what keeps that from
being slow is that the systems under attack already exist: the index from W05,
the approval gate from W04, the memory surface at BOA-S2.

22.5 h across 17 topics from level one is compressed, and canon says so. Months
04 to 06 carry the depth, and the month-05 delta reassesses whether they carry
enough. Evidence: `D-w06-2`, `D-w11-2`, `D-w11-3`, `D-w12-1`, `D-w12-2`,
`D-m05-2`.

## Concepts

Seventeen concepts, all homed here — fifteen at P0, each argued below. Rows give
priority, the week the concept becomes attackable, the surface it is attacked
on, and the deliverable recording the result.

| Concept | Priority | Week | Surface | Proved by |
|---|---|---|---|---|
| prompt injection (C-070) | P0 | W11 | the suite's direct-injection control arm | D-w11-2 |
| indirect prompt injection (C-071) | P0 | W11 | three payload styles in your own index | D-w11-2 |
| RAG poisoning (C-072) | P0 | W06 | poisoned documents in last week's index | D-w06-2 |
| memory poisoning (C-073) | P0 | M05 | BOA-S2's durable per-account memory | D-m05-2 |
| malicious tool output (C-074) | P0 | W12 | a tool returning attacker-shaped content | D-w12-2 |
| data exfiltration (C-075) | P0 | W11 | a covert channel plus a direct ask | D-w11-2 |
| insecure tool permissions (C-076) | P0 | W04 | per-tool profiles, hardened in S7b | D-w12-1 |
| confused deputy (C-077) | P0 | W12 | a forged instruction crossing a privilege step | D-w12-2 |
| excessive agency (C-078) | P0 | W12 | the audit of which steps need autonomy | D-w12-1 |
| privilege boundaries (C-079) | P0 | W12 | classification and CRM write, genuinely split | D-w12-2 |
| least privilege (C-080) | P0 | W04 | scoped short-lived tokens per tool | D-w12-1 |
| sandboxing (C-081) | P1 | W12 | restricted filesystem, no network | D-w12-1 |
| approval gates (C-082) | P0 | W04 | the placement audit on irreversible actions | D-w04-1 |
| secrets (C-083) | P1 | M04 | three credentials from one task context | D-m04-4 |
| audit logs (C-084) | P0 | W12 | append-only, provenance on every write | D-w12-1 |
| tenant isolation (C-085) | P0 | W05 | the permission-filtered index, then RBAC | D-w05-2 |
| output validation (C-086) | P0 | W11 | the trifecta break; citation rejection | D-w11-3 |

### Untrusted input

**prompt injection.** Generated agent code treats the whole context window as
one trusted blob, marking no boundary between what the operator typed and what a
retrieved document or tool response contained — so an instruction arriving in
the latter executes with the authority of the former. That missing boundary is
the *precondition* for goal hijack rather than a symptom, which is why the fix
is structural.

**indirect prompt injection.** The class where the attacker never touches your
prompt. Three payload styles are seeded and measured against a control:
instruction override, persona or role-play override, and delimiter or format
confusion. The examinable distinction is between a prompt-level patch — asking
the model to be careful — and an architectural change treating retrieved content
as untrusted by construction. Only the second removes the class, and only a
measured rate tells you which you built.

**RAG poisoning.** A corpus-level supply problem, overlapping memory poisoning
in one named sub-case and touching the agentic supply chain when the corpus is a
third-party feed. What separates the two is authorship: these documents arrive
through a separate ingestion process rather than being written by the agent from
unverified conversation.

**memory poisoning.** Mapped to ASI06, and validated by that document's own
worked example rather than invented here: an attacker repeatedly reinforces a
false price, the assistant stores it as truth, and later bookings are approved
against it. The chain runs from untrusted input, through a memory write with no
provenance or trust tier that mistakes repetition for corroboration, to a later
unrelated decision reading the entry as ground truth. Two properties must hold
or a reviewer can fairly reclassify the exercise as ordinary prompt injection:
the false fact must survive the triggering message and be read by a separate
later cycle, and the agent's own memory path must have written it.

**malicious tool output.** The trust boundary engineers forget most reliably,
because the tool is *ours*. It is not: a tool reading a GitHub issue, a Sentry
event body or a web page is a conduit for arbitrary attacker text arriving with
the authority of an internal component.

### What the agent is allowed to do

**insecure tool permissions.** Scaffolds default to broad scopes — read and
write across a whole CRM — because that is what wires up quickly in a demo, and
demo defaults survive into production unexamined. This is the named precondition
for both tool misuse and privilege abuse, ASI02 and ASI03.

**confused deputy.** Privilege spent on behalf of someone who did not have it,
by a component that did — a 1988 problem carrying a current identifier, ASI03,
and a primary citation. Model-written scaffolds routinely let a low-privilege
step forward an instruction to a high-privilege one *because it is internal*.
The examinable question is where else one component implicitly trusts another's
output.

**excessive agency.** Named, never numbered. The framing that matters is
least-agency: autonomy deployed where it is not needed expands the attack
surface and adds nothing. That runs straight back to Track A's
workflow-versus-agent boundary at [C-005](agentic-engineering.md) — the
classification you wrote in W01 was a security decision too, and W12 audits
whether you got it right.

**privilege boundaries.** A boundary that exists only in a diagram is not one.
The build-time check is whether the two steps are genuinely separate processes
holding separate credentials, or one process with a comment between them — and
the honest answer is what makes the confused-deputy exercise real.

**least privilege.** The version that survives contact with an agent is per-tool
and per-action, not per-service. A single broad credential quietly accumulates
whatever any step has ever required and never gives it back, and that
accumulation is the budget an injected instruction gets to spend.

**approval gates.** The gate's architecture is argued in Track A at
[C-015](agentic-engineering.md). The security addition is why the payload must
show the literal call: a gate that approves the summary is approving the
attacker's own description of the attack.

### What leaves, and what is recorded

**data exfiltration.** The lethal trifecta — access to private data, exposure to
untrusted content, and the ability to communicate externally — produces
exfiltration risk regardless of how carefully anything is prompted. A business
automation agent is close to a textbook instance: CRM records private, inbound
mail untrusted, outbound mail and CRM writes external. Generated code almost
never breaks the triangle; it adds instructions asking the model to be careful.
Removing a leg means a turn exposed to untrusted content loses its outbound
reach for the rest of that cycle — and the examinable question is whether you
removed a leg or merely filtered one.

**audit logs.** Provenance records where data came from *and at what trust
level*, attached at write time. Without that tag a generated memory-write looks
identical whether a fact arrived from a verified sync or an anonymous email, so
no read-time policy — *do not act on unverified facts for financial actions* —
can be expressed later at all. The log is not a compliance artifact; it is what
makes the mitigation sayable.

**tenant isolation.** The correctness-and-disclosure fusion is argued in Track C
at [C-052](ai-application-engineering.md). Track D adds sequencing: role-based
rules first, matching the per-tool profile shape already built in W04, and
attribute-based rules only where a check truly depends on context.

**output validation.** Where a hijacked turn stops if it stops anywhere, and the
one point at which the control is deterministic code rather than the model's
cooperation. An undeclared field with nowhere to land, and a citation check
rejecting an unsupported claim, both hold whether or not the model was fooled —
which is what separates a control from a mitigation.

## Priorities and what is deferred

Two concepts are P1 for the same reason: the depth belongs to a later month and
the recognition belongs here. Sandboxing is one paragraph and one diagram at
this baseline, and the whole lesson is that **a container is not a hard security
boundary** against a malicious workload — it is namespace and control-group
isolation sharing one kernel. Intercepting syscalls in user space buys escape
resistance and costs throughput; a dedicated kernel per workload buys more and
costs more still. Protocol-level study of any tier is low return at `LR-19`;
knowing which tier you are on is not. Secrets wait for month 04, when one task
first writes to three systems with three credentials. The agent-specific point
is that a secret leaks through the *model* and not only through logs, which
makes short lifetime a stronger control than careful redaction.

The triage narrows the rest. Container tooling is **LEARN ENOUGH TO USE** for
two things, Postgres and the W12 sandbox. Scoped tokens are **LEARN ENOUGH TO
USE** at the level of scopes and lifetimes, skipping protocol internals.
Role-based access control is **LEARN ENOUGH TO USE** at month 06; attribute
rules earn themselves only where a check truly depends on context. A policy
engine is **SKIP FOR NOW** — the enforcement-point and decision-point separation
is the right pattern and an engine is the wrong investment level inside 22.5 h,
so the month-06 deliverable is a hand-written pre-execution check that states
what an engine would have added. Published guidance is **LEARN ENOUGH TO USE**:
recognise the four categories this programme actually meets — goal hijack, tool
misuse, identity and privilege abuse, and memory and context poisoning — rather
than memorising ten.

One refusal is absolute. Numeric injection-defence effectiveness figures are
forbidden at `LR-21`, not discouraged. No verified primary benchmark exists, and
the substitute is not a better citation but your own measured rate against your
own system — which is what the brief asked for anyway.

## How this track is proved

Track D leads four weeks — W04, W06, W11 and W12 — and reinforces the other
eight, which is unusual enough to state plainly. That list is not decorative:
W01 the runner's permission surface, W02 what a crashed agent leaks, W03 retry
storms as an availability attack, W05 index permission filtering, W07 untrusted
stack-trace content, W08 lock abuse, W09 adversarial cost exhaustion, W10 eval
gaming. No week lacks the security lens, which is what stops this being a
security month.

Proof is adversarial throughout, and each deliverable names a rate or a refusal
rather than a document. `D-w06-2` seeds a corpus you built and reports what got
through. `D-w11-2` runs three techniques with success rates either side of one
structural change. `D-w11-3` proves an answer cannot cite what was never
retrieved. `D-w12-1` and `D-w12-2` prove a call outside a named profile is
refused and logged, and that the forgery stops once re-authorization exists.
`D-m05-2` closes the memory work.

Held elsewhere: the five named parts of every failure exercise — detection, safe
failure behaviour, recovery, logging, and a test proving the mitigation — are
the exercise set's to expand, and the attack bodies live with
[the security exercises](../exercises/ai-security.md). Tasks and hours belong to
the week files; trust-boundary stages to
[the knowledge agent](../projects/secure-knowledge-agent.md) and
[the platform](../projects/engineering-agent-platform.md).
