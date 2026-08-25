# AI security attack suites

Six attacks, every one run **against your own system**, every rate measured on your
own build. No industry percentage appears in this file or in any report produced
from it: a borrowed number proves nothing about the thing you shipped.

**Two are Core, four are not.** Weeks 11 and 12 require *indirect injection* and
*the confused deputy* — one attack each, done properly, with the mitigation
enforced in code. Corpus poisoning, exfiltration beyond the single covert route,
malicious tool output and memory poisoning are Stretch or belong to months 4–6.
You do not need every class of agent security in two calendar weeks; you need one
attack you can prove you actually defeated.

## The method, every time

Control run → attack → measure → apply **exactly one structural mitigation** →
re-measure against the same control.

The word *structural* is doing the work. A prompt-level patch asks the model to be
careful and moves the rate a little; a structural change removes the class. **Which
of the two you did is the examinable question**, and a report that cannot answer it
has not finished.

Non-negotiables:

- The query set is **frozen before the first arm** and identical in the second. A
  query added after seeing results is a new experiment.
- **Exactly one** mitigation separates the arms. Two produce a number you cannot
  attribute.
- Every attempt is recorded, **failures included**, or the denominator is unknown.
- Detection means **deviation from the control output**, never recognition of a
  payload.
- Techniques must be genuinely distinct **mechanisms**, not three phrasings of one.
- Zero borrowed figures.

## Three categories that get collapsed into one

Corpus poisoning, memory poisoning and goal hijack are routinely treated as one
thing. Three axes separate them — **what is retained, who writes it, and when it is
read** — and a report that cannot place its own attack on this table has not
understood what it ran.

| | What is retained | Who writes it | When it is read |
|---|---|---|---|
| **RAG / corpus poisoning** | documents in a searchable index | a separate ingestion process, over content the attacker planted upstream | at query time, whenever retrieval selects the poisoned chunk |
| **Memory poisoning** | a claim the *agent* formed about an account or a person | the agent's own memory-write path, from input nobody verified | by a later, unrelated decision cycle that treats stored facts as ground truth |
| **Goal hijack** | nothing — it lives and dies inside one context window | whoever controls any text the model reads in that turn | immediately, in the same turn it arrives |

Two consequences, both examinable. Corpus poisoning is a **data-supply** problem, so
its fix lives at ingest and at trust tiering rather than in the model. And goal
hijack has a *precondition* rather than a cause: generated agent code treats the
whole context window as one undifferentiated trusted blob, and that missing boundary
is what makes hijack possible at all.

## The six attacks

### 1. Corpus poisoning against your own index · week 11 *(Stretch)*

Seed an injection corpus into the index you built the week before — **your own, not
a fixture** — using at least three distinct techniques: instruction override,
persona/role-play override, delimiter/format confusion. Run a fixed query set
against a clean control index and against the poisoned one. Measure the difference.
Apply one structural mitigation — treating retrieved content as untrusted rather
than as instruction — and run the identical set again.

*Report:* attack success rate per technique with its denominator, both arms; the
post-mitigation rate measured against the same fixed set with zero queries added or
removed; the three-way category placement, saying why not the other two rows.

*Also measure retrieval precision*, to show whether the mitigation cost you ordinary
answer quality.

### 2. Indirect injection against the retrieval agent · week 11 **(Core)**

Build the defence first, and be clear about which part of it is which.
**Provenance at ingest, trust tiers and a delimiter between operator instructions
and document content are defense in depth** — they reduce instruction/data
confusion and give you provenance to reason about, and they guarantee nothing,
because a delimiter is a convention the model is more likely to respect rather
than a control it cannot cross. **The boundary is the code-enforced capability
restriction**: a turn that consumed untrusted content cannot reach an
external-send tool, decided outside the model.

Then run the suite against a fixed query set with at least three payload styles,
in both arms. Payloads live in documents the retrieval layer selects **on their own
merits** — one pasted into the prompt tests a different class. Telling the model to
ignore document instructions is the prompt-level patch this exercise exists to
discredit.

*Record, for every attempt, whether an external-send tool was reached.* That field
separates an attack that bent the answer from one that reached the network, and they
are not equally bad.

*Prove the refusal came from code* with an assertion that fails when the control is
disabled. This is not a formality — it is the only evidence that separates a
security property from a model that happened to comply. **separator ≠ security
boundary · model refusal ≠ security guarantee · prompt instruction ≠ authorization
control.**

### 3. Exfiltration and the trifecta break · week 11 **(one covert route: Core)**

Get private data out by at least two routes: a direct request, and at least one
**covert** channel where the data rides inside something helpful-looking — a
parameter in a URL the agent offers, for instance. A direct ask alone tests refusal
training, not architecture.

Then break the trifecta **structurally**: strip external-send capability from any
turn that touched untrusted input in that cycle. Re-run both routes with the *same*
payloads, not improved ones.

*State explicitly which leg you removed* — private data access, untrusted-content
exposure, or outbound communication — and which you merely **filtered**. A regex over
outbound URLs is a filter and must be labelled as one if that is what you built.
Defend the claim in writing against the alternative reading.

*Also measure token cost per attempt:* a covert channel that costs an attacker very
little is a different risk from one that costs a lot.

### 4. The confused deputy · week 12 **(Core)**

Make a low-privilege step cause a high-privilege one to act, without either being
compromised.

Take the pipeline where classification reads attacker-supplied text and the write
step holds real privilege. Craft an input that makes classification relay a forged
high-impact instruction, and show the write step executing it without re-checking the
original human request. Then patch it: every privileged action re-authorizes against
the request a person actually approved. Re-run the forgery **unchanged**.

*Constraints:* neither step may be modified to make the attack land — if it needs a
code change, it was not demonstrated. The forged instruction travels the real
pipeline, not a test-harness shortcut. **The patch re-authorizes per action, not per
session** — a session-level check falls to the same forgery.

*Report:* privileged actions triggered per forgery attempt, both arms, evidenced
from the audit log. The refusal's audit entry contains the id of the original
approved request it was compared against. A test asserts the check fires ≥2 times
inside a single multi-action task.

### 5. Malicious tool output at the boundary · week 12 *(Stretch, or month 4)*

Treat a tool's return value as attacker-controlled, because it is.

Stub a tool returning two hostile shapes: content shaped like instructions, and
content violating the tool's declared schema. Record what the current agent does with
each. Then validate **at the tool boundary, before the output enters context** —
after the model has read it, it is not a control. Use a schema with **no field wide
enough to carry an instruction**, or the control is decorative.

*Rejection is bounded:* after N refusals the task dead-letters rather than accepting
a degraded parse, with N fixed and stated before the run. Settling for a lossy parse
is how a hard edge quietly becomes a soft one.

*Log the value exactly as returned.* It is the only artifact from which a refused
attack can be reconstructed later.

### 6. Memory poisoning against durable account memory · months 4–6

Write a false fact into durable account memory through an untrusted inbound channel,
have a **later and unrelated** decision act on it, then block that path without
breaking legitimate writes.

**At least one full pipeline cycle must separate the plant from the exploitation,
never one context window.** Without that gap this is ordinary prompt injection under
another name, and a reviewer may say so. The false fact must be written by the
agent's own memory-write path from unverified input, never inserted into the store
directly.

Mitigate with one of: provenance scoring, write-time validation, or a TTL on
unverified entries. **Repetition is never corroboration** — if reinforcing a claim
raises its trust, the mitigation failed whatever the measured rate says.

*Report the false-positive cost on legitimate writes* beside the blocked attack,
over at least 10 legitimate writes, with its denominator. **Measured, never
estimated.**

## Reflection questions worth asking after any of them

1. Did your mitigation remove the class or reduce a rate? Name the property that
   makes your answer true rather than hopeful.
2. Which technique was cheapest for the attacker, and does your defence cost more
   than that technique does?
3. If an attacker read your entire mitigation, which payload would they write next?
4. What authority should this agent not have, and where in your code is that absence
   *enforced* rather than requested?
5. Name the one change you would insist on before this agent went anywhere near a
   real user's data.

## Reading

The OWASP agentic PDF and the lethal-trifecta essay, both in
[RESOURCES.md](../RESOURCES.md#security). Cite the PDF, never a vendor summary of
it, and cite categories **by name** — the identifiers have been renumbered between
editions, so a number you did not verify against the current primary source is a
number you should not print.
