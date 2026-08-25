# Business Operations Agent

An agent that reads inbound documents, extracts structure from them, looks the
sender up, proposes an action — and then **stops and waits for a person**.

The smallest of the three projects by code volume, and the only one whose failures
cost something outside the repository, because its outputs are addressed to real
strangers.

Its customer is you. The business track needs a cold-outreach funnel built from
nothing, and this agent is what builds it: it researches prospects, drafts the
messages, and hands each draft to a human who reads it and presses send. That is
not a safety compromise made reluctantly. **An agent that cannot send is a better
exercise than one that can**, because every fact the approver needs in order to
decide has to be in the payload — and no amount of trust in the model substitutes
for it.

It is also the only home for **agent memory**. Task state is bookkeeping about
where a pipeline got to, not a belief the agent holds; a poisoned document in a
corpus is not a poisoned memory. Capability 3 creates that surface deliberately,
which is what makes the months-4–6 attack against it real rather than contrived.

Main build: **week 3** (extraction), **week 5** (draft-and-approve),
**months 4–6** (memory, and the attack on it).

## Pipeline

email / document → classification → data extraction → CRM lookup → proposed action
→ **human approval** → CRM update / reply

The sixth step is load-bearing. Everything to its left is analysis and everything to
its right is an effect on the world, so the approval gate is not a step among seven
— it is the boundary the other six are arranged around.

## Capability backlog

### 1. Structured extraction over real company sites · week 3

**Why.** Company research is the checklist you wrote by hand in week 1, and a
procedure nobody wrote down cannot be automated. Writing it first is the input, not
paperwork.

**Build.** A target schema and an extractor that produces valid instances from real
company websites, with retry on validation failure.

**Demo counts when.** 10 real sites yield at least 8 valid schema instances, **and
100% of rejections carry a recorded reason.**

Note what that does *not* say: it does not require 10 of 10. Two failures out of ten
are expected. The requirement that each carries a reason is the part that matters —
a silent extraction failure is indistinguishable from a company with nothing to
extract.

**Metrics.** Valid instances over sites attempted. Rejections with a reason over
rejections.

### 2. Draft-only outreach with approval and audit trail · week 5

**Why.** The interesting assertion is about what the system **refuses**, and a
refusal that is not logged has not been proved.

**Build.** Proposed action → approval payload → recorded approval → send. No
outbound message leaves without an approval record naming a human, and there is no
configuration flag that relaxes it. The audit trail is append-only.

**Demo counts when.** A draft exists with no send, and a **forced bypass attempt
appears in the audit log as refused.**

**Metrics.** Drafts prepared; sends approved; bypass attempts refused and logged.

### 3. Durable per-account memory · months 4–6

**Why.** The one surface where a false belief can outlive the conversation that
planted it.

**Build.** Facts accumulated about an account persist **across sessions** and are
read by **later, separate** decision cycles as trusted input — with provenance and a
trust tier on every write.

Read that exit as a specification for the attack that follows it. Persistence across
sessions and a *later, separate* decision cycle are not descriptive flourishes; they
are the two properties that make this memory poisoning rather than ordinary prompt
injection. Provenance and trust tiering are the mitigation surface, and they must
exist before the attack, or the attack has nothing to defeat.

**Demo counts when.** A fact written in one session is read by a decision made in a
later one, with its provenance shown. This cannot be satisfied inside a single run:
a demo showing the fact written and read in the same breath has demonstrated a
variable, not a memory.

**Metrics.** Poisoned facts acted on, before and after mitigation. **False-positive
rate on legitimate writes**, over at least 10 legitimate writes, with its
denominator — measured, never estimated.

### 4. Malformed and malicious input · months 4–6

**Why.** They look alike at the parser and are completely different at the threat
model. Running them together forces the distinction to be stated rather than assumed.

**Build.** Plausibility rules that are explicit and testable — not the model's
opinion of its own output — separating *the parser could not read this* from *the
parser read it into something well-formed and wrong*. No default is substituted on a
validation failure, however reasonable. After N failures, a person.

**Demo counts when.** A corpus of deliberately broken documents produces zero
substituted defaults and zero acted-on improbable results.

## Constraints

**It never sends.** No outbound message leaves without an approval record naming a
human. The constraint holds through the memory capability and beyond: memory makes
the agent's proposals better informed, not more autonomous. The audit trail is
append-only, which means a bypass attempt is not merely blocked but permanently
visible — a refusal with no record is an assertion about the past rather than
evidence of it.

**The approval payload renders the literal proposed call**, not the agent's summary
of it. For a buyer, that is the difference between an automation they would let near
their CRM and one they would not.

**Memory is not task state, and neither is a corpus.** These three get collapsed
constantly and this project keeps them apart deliberately. Task state says which
pipeline step completed and is machine bookkeeping. A corpus is documents someone
else wrote, retrieved at query time. **Memory is a claim the agent formed and stored
about the world, written by its own path from input it did not verify** — and that
authorship is precisely why it is dangerous. Every write carries an origin channel
and a trust tier, and **repetition is never corroboration**: an attacker's cheapest
move is to say the same false thing many times.

**The classification step must not be able to command the write step.** This
pipeline is a textbook confused deputy: classification reads attacker-supplied text
and holds almost no privilege, while the CRM write holds a great deal and trusts what
reaches it. If the low-privilege step can relay an instruction the high-privilege step
executes without re-checking the original human request, every approval gate upstream
has been routed around rather than defeated. Week 12 builds exactly that forgery and
patches it with per-action re-authorization — and the patch is only credible because
the demonstration came first.

**Placeholder identities throughout.** No client name, no prospect name and no
personal data in a tracked file. Real prospect data lives in gitignored `*.local.md`
files. This constrains the code as well as the docs: the demos take an opaque
identifier rather than an address.

**Its numbers are business evidence and are tagged as such.** Counts this agent
produces — prospects researched, drafts prepared, sends approved — are logged with
`real` or `simulated`, and the two are never added together.
