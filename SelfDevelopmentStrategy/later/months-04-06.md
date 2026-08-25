# Months 4–6 — Durability outward, memory, and the first outside party

Deliberately thinner than the week files. A month here names a capability, a
project milestone, a business goal, a checkpoint and a decision — not a task list.
Detail arrives when evidence does.

**Rewrite this file after the week-12 retrospective.** It was written before you
had any of the data.

## Capability

**Durability at the boundary of your system, not just inside it.** By now the
platform writes to a Git host, an issue tracker and an error tracker from a single
task. You cannot atomically commit a transaction and perform an HTTP call. Code
shaped `db.commit(); host.create_pr()` has a crash window, and crash-window bugs
are the definitional class generated code never surfaces: the naive version passes
every test that does not include a crash, and no agent injects a kill between two
statements unprompted.

The answer is an **outbox** — a pending-effect row written in the same transaction
as the state transition, plus a **separate relay process** delivering pending
effects at least once, with handlers that stay correct when it delivers twice. Both
halves are load-bearing; a relay whose handlers are not twice-safe has relocated the
defect rather than fixing it.

Then the harder one: **compensation that fails.** Model task-lifecycle teardown as
a saga with explicit compensations, and inject *permanent* failures into the
compensations themselves. Note what a saga is and is not — the fan-out to three
external systems is **not** a saga. If the tracker write fails after the PR exists
you retry the tracker forever rather than deleting the PR, because independent
effects are handled completely by at-least-once fan-out over an outbox. A saga is
defined by compensation, and the genuine one here is teardown.

**Agent memory** — the third thing that is neither task state nor a corpus, and the
distinction matters because these three get collapsed constantly:

| | What is retained | Who writes it | When it is read |
|---|---|---|---|
| Task state | which pipeline step completed | your own code | by the resume path |
| Corpus | documents someone else wrote | an ingestion process | at query time |
| **Memory** | a claim the *agent* formed about the world | the agent's own write path, from input nobody verified | by a later, unrelated decision cycle |

That authorship is precisely what makes memory dangerous. Every write carries an
origin channel and a trust tier, and **repetition is never corroboration** — an
attacker's cheapest move is to say the same false thing many times.

**Authorization as policy**, on the knowledge agent: RBAC through a single
pre-execution check function, with ABAC only where a decision genuinely depends on
request context. One check function, not a check per call site. A policy scattered
across handlers is a policy with holes.

## Project milestones

**Platform** — outbox and relay, fault-injected at *every* boundary between commit
and last external call, exhaustively rather than by sampling. Saga teardown with
compensation-failure injection. Ingestion from a real task source (Notion, Linear,
Jira — whatever you actually use), completing the long-form feature pipeline.
Multi-axis automated review: five independently scored, separately cited outputs
per PR, never one aggregate verdict.

**Business Operations Agent** — durable per-account memory: facts persisting
*across* sessions, read by later, separate decision cycles as trusted input, with
provenance and a trust tier on every write. Then attack it (below). Also:
malformed-input handling beside the malicious-input work, deliberately in the same
month, because they look alike at the parser and are completely different at the
threat model.

**Secure Knowledge Agent** — RBAC on the authorization surface, plus tenant
isolation and secrets handling.

**Cross-harness comparison** — the first place a provider abstraction is *earned*,
because a second harness now genuinely exists. Design the comparison so it measures
the harness rather than re-measuring model choice: pin the model id, and prove it
was pinned from the run metadata.

## Security exercises

**Memory poisoning.** Write a false fact into durable account memory through an
untrusted inbound channel, let the cycle end, and in a **separate, later cycle**
trigger a decision that reads stored facts as trusted input and acts on the false
one. The gap is not a flourish — **at least one full pipeline cycle must separate
the plant from the exploitation, never one context window.** Without it this is
ordinary prompt injection under another name, and a reviewer will say so.

Then mitigate: provenance scoring, write-time validation, or a TTL on unverified
entries. Report the **false-positive cost on legitimate writes** beside the blocked
attack, measured over at least 10 legitimate writes, never estimated. And close the
loop by which the agent's own output returns as trusted material — that loop is how
one plant becomes self-sustaining.

**Authorization bypass through a policy gap.** Find the action your policy never
mentions and make silence mean refusal. Fuzz the whole cross-product of actions and
roles, not a sample — reading the policy surfaces the rules that exist, and this
defect is about the ones that never did. In code, the difference is a check that
ends in a returned `false` versus one that runs off the bottom returning nothing.
Every new rule ships with a **refusal-path** assertion, not only a permission
assertion.

**Malformed input.** Separate a document the parser cannot read from one it reads
into something well-formed and *wrong*. The second needs plausibility rules of its
own, explicit and testable — not the model's opinion of its own output. No default
is substituted on a validation failure, however reasonable, and after N failures it
reaches a person.

## Business goal

**The first free or cheap pilot, strictly scoped** — if the funnel produces one.
Exit criteria: a real external party's process is measurably different afterwards,
the before/after baseline was **measured rather than estimated**, and the scope was
fixed in writing before work started and was not exceeded.

If the funnel produces nobody, that is a result, not a failure. Extend the
documented-workflow path, tag everything `simulated`, and say plainly in the
scoreboard that no external party was reached. **Never manufacture a case study.**
An unverified time-savings claim is worse than no case study, because it is the one
document a buyer will check.

Also: recompute your funnel rates. By month 5 you have ~60–80 sends of history, and
that is enough to divide honestly for the first time.

## Measurable checkpoint

At the end of month 6, from artifacts rather than self-assessment:

- Zero kill points lose an effect or leave state and effects disagreeing, after the
  outbox lands. A rolled-back transaction leaves zero outbox rows.
- Every compensation is invoked twice by the suite and adds nothing the second
  time. At least one **non-compensable** effect is named, with what happens
  instead — a surface where everything is reversible was described inaccurately.
- The poisoned memory fact is acted on pre-mitigation and not post-mitigation, with
  two separate session records proving the cycle gap, and the false-positive cost
  reported with its denominator.
- Zero action/role pairs are allowed without an explicit rule, across the full
  cross-product.
- The cross-harness comparison's run metadata proves the model id was pinned.

## Decision point

**Is the harness good enough to sell time on, or does it need another month?**

Answer from the scoreboard, not from confidence. If autonomous success rate over
the last twenty tasks is below what you would be comfortable describing to a buyer,
the honest move is another month of engineering — and saying so is cheaper than
discovering it in front of a client.

The secondary question: **has anything in months 1–3 gone unused?** If the queue,
the sandbox or the eval harness has not earned its keep, that is information about
how you sequence months 7–12.
