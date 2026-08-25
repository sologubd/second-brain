# AI security attack suites

## How to use these

Six attack exercises, every one run **against the learner's own system**, every
rate measured on this build. No industry percentage appears in this file or in
any report produced from it: a borrowed number proves nothing about the thing you
shipped.

Each suite has the same skeleton: control run, attack, measure, apply **one
structural mitigation**, re-measure against that same control. The word
structural is doing the work. A prompt-level patch asks the model to be careful
and moves the rate a little; a structural change removes the class, and which of
the two you did is the examinable question every time.

The learner's security baseline is awareness — no prior structured attack
thinking, no trust-boundary analysis, no least-privilege design as deliberate
practice. Rungs are named per exercise; the set is anchored at **secure**
(`DL-6`), which canon defines as attacking your own system and reporting the
rate before and after.

### Three categories that get collapsed into one

Corpus poisoning, memory poisoning and goal hijack are routinely collapsed into
one thing. Three axes separate them — **what is retained, who writes it, and when
it is read** — and a report that cannot place its own attack on this table has
not understood what it ran.

| | What is retained | Who writes it | When it is read |
|---|---|---|---|
| **RAG / corpus poisoning** | documents in a searchable index | a separate ingestion process, over content the attacker planted upstream | at query time, whenever retrieval selects the poisoned chunk |
| **Memory poisoning** | a claim the agent formed about an account or a person | the agent's own memory-write path, from input nobody verified | by a later, unrelated decision cycle that treats stored facts as ground truth |
| **Goal hijack** | nothing — it lives and dies inside one context window | whoever controls any text the model reads in that turn | immediately, in the same turn it arrives |

Two consequences, both examinable. Corpus poisoning is a data-supply problem, so
its fix lives at ingest and at trust tiering rather than in the model. And goal
hijack has a precondition rather than a cause: generated agent code treats the
whole context window as one undifferentiated trusted blob, and that missing
boundary is what makes hijack possible at all.

Weekly hours and acceptance live in [weeks/](../weeks/week-11.md); the systems
under attack in [retrieval](../projects/secure-knowledge-agent.md) and
[operations](../projects/business-operations-agent.md); defensive five-part
handling in [the failure set](agent-failures.md). This file owns the offensive
bodies.

## Exercises

### Corpus poisoning against your own index (D-w06-2)

Rungs: `DL-6` secure, `DL-5` measure.

#### Objective

Establish how far a poisoned document moves your retrieval agent's answers, and
whether treating retrieved content as untrusted removes the class or only shrinks
the number.

#### Task

Seed an injection corpus into the index you built the week before — your own,
not a fixture — using at least three distinct techniques: instruction override,
persona/role-play override, and delimiter/format confusion. Run a fixed
query set against a clean control index and against the poisoned one. Measure the
difference. Apply exactly one structural mitigation, treating retrieved content
as untrusted rather than as instruction, and run the identical query set again.
Write the three-way category distinction as part of the report, placing your own
attack on it.

#### Constraints

- Three techniques minimum, and genuinely distinct mechanisms rather than three phrasings of one.
- The query set is fixed before the first run and untouched between arms; a query added after seeing results is a new experiment.
- Exactly one mitigation separates the two arms; two produce a number you cannot attribute.
- Detection means deviation from the control output, never recognition of a payload: a detector that only catches payloads it has already seen is not one.

#### Deliverable

`D-w06-2` — an **attack report** (`DT-07`) carrying the three seeded techniques,
the measured rate from each arm either side of the single structural change, and
the written three-way category placement.

#### Acceptance criteria

- Attack success rate is reported per technique with its denominator stated, for at least 3 techniques.
- The post-mitigation rate is measured against the identical fixed query set, with 0 queries added or removed.
- The report contains 0 industry-sourced percentages.
- The category distinction places this attack in exactly 1 of the 3 rows and says why not the other 2.

#### Metrics

- Attack success rate: successful hijacks divided by queries in the fixed set, per technique, before and after.
- Retrieval precision: relevant chunks divided by chunks returned, to show whether the mitigation cost ordinary quality.

#### Reflection questions

1. Did your mitigation remove the class or reduce a rate? Name the property that makes your answer true rather than hopeful.
2. Which technique was cheapest for the attacker, and does your defence cost more than that technique does?

### Indirect injection against the retrieval agent (D-w11-2)

Rungs: `DL-6` secure.

#### Objective

Attack the class where the attacker never touches your prompt, and show the gap
between asking a model to be careful and making the injection unable to act.

#### Task

Build the untrusted-content boundary first: provenance tagging at ingest,
trust-tiered retrieval, and a hard separator between operator instructions and
document content. Then run the indirect-injection suite against a fixed query set
with at least three payload styles, in both arms. Record, for every attempt,
whether an external-send tool was reached.

#### Constraints

- Payloads live in documents the retrieval layer selects on their own merits; one pasted into the prompt tests a different class.
- The boundary is enforced in code. Telling the model to ignore document instructions is the prompt-level patch this exercise exists to discredit.
- Control and treatment arms differ in exactly one thing: whether the boundary is enabled.
- Every attempt is recorded, failures included, or the denominator is unknown.

#### Deliverable

`D-w11-2` — an **attack report** (`DT-07`): at least three injection techniques
against a fixed query set, with attack success rate before and after the
structural change, and the per-attempt record of external-send attempts.

#### Acceptance criteria

- At least 3 payload styles are run against the same fixed query set in both arms.
- Attack success rate is reported with its denominator for each of the 2 arms.
- 0 turns that touched untrusted input successfully invoked an external-send tool after the mitigation.
- The refusal is demonstrated to come from code, by an assertion that fails when the boundary is disabled.

#### Metrics

- Attack success rate: attacks changing agent behaviour divided by attempts, per style, per arm.
- Failure rate: attempts reaching an external-send tool divided by attempts, before and after.

#### Reflection questions

1. What authority should this agent not have, and where in your code is that absence enforced rather than requested?
2. If an attacker read your entire mitigation, which payload would they write next?

### Exfiltration and the trifecta break (D-w11-2)

Rungs: `DL-6` secure, `DL-8` explain.

#### Objective

Get private data out of your own agent by a channel that does not look like one,
then remove a structural leg rather than filtering the attempt.

#### Task

Attempt exfiltration against your retrieval agent by at least two routes: a
direct request for private content, and at least one covert channel where the
data rides inside something helpful-looking, such as a URL parameter in a link
the agent offers. Then break the trifecta structurally by stripping external-send
capability from any turn that touched untrusted input in that cycle, and re-run
both routes. State explicitly, in the report, which leg you removed — private
data access, untrusted-content exposure, or outbound communication — and which
you merely filtered.

#### Constraints

- At least one channel must be covert. A direct ask alone tests refusal training, not architecture.
- The fix must remove a leg. A regex over outbound URLs is a filter and must be labelled as one if that is what you built.
- The leg-removal claim is defended in writing against the alternative reading, and re-runs use the same payloads rather than improved ones.

#### Deliverable

`D-w11-2` — an **attack report** (`DT-07`) extended with the exfiltration arm:
the covert channel, the before and after rates, and the written leg-removal
argument.

#### Acceptance criteria

- At least 2 routes are attempted and at least 1 is covert.
- Exfiltration success rate is reported per route with its denominator, for both of the 2 arms.
- The report names exactly 1 of the 3 legs as removed, with the reasoning stated.
- The covert route is re-run post-fix and its rate measured directly, with at least 1 recorded attempt.

#### Metrics

- Attack success rate: successful extractions divided by attempts, per route, per arm.
- Token usage per attempt, since a covert channel that costs an attacker very little is a different risk from one that costs a lot.

#### Reflection questions

1. Your agent holds private data, reads untrusted content and can reach the network. Which of those three is genuinely required by the product, and what would the product lose without it?
2. Name the one change you would insist on before this agent was allowed anywhere near a real user's data.

### The confused deputy (D-w12-2)

Rungs: `DL-6` secure, `DL-3` break.

#### Objective

Make a low-privilege step cause a high-privilege one to act, without either being
compromised, then close the gap with per-action re-authorization.

#### Task

Take the pipeline where classification reads attacker-supplied text and the write
step holds real privilege. Craft an input that makes classification relay a forged
high-impact instruction, and show the write step executing it without re-checking
the original human request. Then patch it: every privileged action re-authorizes
against the request a person actually approved. Re-run the forgery unchanged.

#### Constraints

- Neither step may be modified to make the attack land; if it needs a code change, it was not demonstrated.
- The forged instruction must travel through the real pipeline, not through a test harness shortcut.
- The patch re-authorizes per action, not per session: a session-level check falls to the same forgery.

#### Deliverable

`D-w12-2` — an **attack report** (`DT-07`): the working forgery, the
per-action re-authorization patch, and the re-test showing the same input
refused.

#### Acceptance criteria

- The forgery causes at least 1 privileged action pre-patch, evidenced from the audit log.
- Post-patch, the identical input causes 0 privileged actions and the refusal is logged.
- A test asserts the re-authorization check fires at least 2 times inside a single multi-action task.
- The audit entry for the refusal contains the id of the original approved request it was compared against.

#### Metrics

- Attack success rate: privileged actions triggered divided by forgery attempts, before and after.
- Latency added per privileged action by the re-authorization check, p50.

#### Reflection questions

1. The deputy was confused because it trusted its caller. Which other component in your build trusts its caller in the same way?
2. What failure mode did your original approval design miss, and would any review have caught it without this attack?

### Malicious tool output at the boundary (D-w12-2)

Rungs: `DL-6` secure.

#### Objective

Treat a tool's return value as attacker-controlled, because it is, and prove
instruction-shaped content cannot cross into the model's instruction context.

#### Task

Stub a tool returning two kinds of hostile output: content shaped like
instructions, and content violating the tool's declared schema. Record what the
pre-mitigation agent does with each. Then validate at the tool boundary, before
the output enters context, using a schema with no field wide enough to carry an
instruction. Re-run both shapes and record what happens after a rejection.

#### Constraints

- Validation runs at the boundary, before context assembly; after the model has read the output it is not a control.
- The schema must have no free-text field wide enough to carry an instruction, or the control is decorative.
- Rejection is bounded: after N the task dead-letters rather than accepting a degraded parse.
- The hostile stub is fixed before the first run and never softened.

#### Deliverable

`D-w12-2` — an **attack report** (`DT-07`) covering the tool-output arm: the two
hostile shapes, the boundary validation, and the recorded post-rejection
behaviour.

#### Acceptance criteria

- 0 instruction-shaped tool outputs reach the model's instruction context after the mitigation.
- 100% of schema violations are rejected at the boundary, each logged with the tool name and the validation error.
- The task dead-letters after exactly N rejections, with N fixed at a stated number before the run.
- The suite fails against the pre-mitigation version that passed tool output through as text.

#### Metrics

- Attack success rate: hostile outputs reaching context divided by hostile outputs returned, before and after.
- Failure rate: tasks dead-lettered on repeated rejection divided by tasks run against the hostile stub.

#### Reflection questions

1. Your tools are "yours". Which of them is actually a conduit for text a stranger wrote, and what does that change about its return type?
2. Which parts of this rejection path must be idempotent, and what happens if a rejection is itself retried?

### Memory poisoning against durable account memory (D-m05-2)

Rungs: `DL-6` secure, `DL-7` operate.

#### Objective

Write a false fact into durable account memory through an untrusted inbound
channel, have a **later and unrelated** decision act on it, then block that path
without breaking legitimate writes.

#### Task

Send an inbound message that drives the agent's own memory-write path to store a
false claim about an account. Let the cycle end. In a separate, later cycle,
trigger a decision that reads stored facts as trusted input and watch it act on
the false one. Apply one mitigation — provenance scoring, write-time validation,
or a time-to-live on unverified entries — and re-run the sequence, reporting the
false-positive cost on legitimate writes beside the blocked attack.

#### Constraints

- At least one full pipeline cycle separates the poisoning message from the exploiting decision, never one context window. Without that gap this is ordinary prompt injection under another name, and a reviewer may say so.
- The false fact must be written by the agent's own memory-write path from unverified input, not inserted into the store directly.
- Repetition is never corroboration: if reinforcing a claim raises its trust, the mitigation failed whatever the measured rate says.
- The false-positive rate on legitimate writes is measured, never estimated.

#### Deliverable

`D-m05-2` — an **attack report** (`DT-07`): the poisoning path, the later
decision that acted on it, the mitigation, before-and-after re-runs, and the
false-positive cost.

#### Acceptance criteria

- The exploiting decision occurs at least 1 full pipeline cycle after the poisoning message, evidenced by two separate session records.
- Pre-mitigation, the poisoned fact changes at least 1 decision the agent proposes.
- Post-mitigation, the identical sequence produces 0 acted-on poisoned facts, or the entry is flagged before the decision reads it.
- False-positive rate on legitimate memory writes is reported over at least 10 legitimate writes, with its denominator.

#### Metrics

- Attack success rate: poisoned facts acted on divided by poisoning attempts, before and after.
- Failure rate: legitimate writes blocked or quarantined divided by legitimate writes attempted.

#### Reflection questions

1. Your memory store now distrusts some writes. What is the oldest entry in it that would not pass today's rules, and what depends on that entry?
2. What would fail if this agent's memory grew ten times larger — the storage, the retrieval, or your ability to audit where any given belief came from?
