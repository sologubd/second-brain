# Business Operations Agent

## What it is

`PRJ-03`. An agent that reads inbound documents, extracts structure from them,
looks the sender up, proposes an action, and then **stops and waits for a
person**. Three stages across the programme, and the smallest of the three
projects by code volume — but the only one whose failures cost something outside
the repository, because its outputs are addressed to real strangers.

Its customer is the learner. Track E needs a cold-outreach funnel built from
nothing, and this agent is what builds it: it researches prospects, drafts the
emails, and hands each draft to a human who reads it and presses send. That
arrangement is not a safety compromise made reluctantly. **An agent that cannot
send is a better exercise than one that can**, because every fact the approver
needs to decide has to be in the payload, and no amount of trust in the model
substitutes for it.

It is also the programme's only home for agent memory. The brief asks for memory
three times and nothing else in the build could carry it: task state is
bookkeeping about where a pipeline has got to, not a belief the agent holds, and
a poisoned document in a corpus is not a poisoned memory. `BOA-S2` creates that
surface deliberately, which is what makes the month-05 attack against it a real
exercise rather than a contrived one.

## Pipeline

Seven stages, in canon's order: email/document → classification → data extraction
→ CRM lookup → proposed action → human approval → CRM update / reply.

The sixth step is the load-bearing one. Everything to its left is analysis and
everything to its right is an effect on the world, so the approval gate is not a
step among seven — it is the boundary the other six are arranged around. `S7b`
later hardens it with per-tool profiles and provenance; the placement is decided
here.

Seven things the project must demonstrate, each with a home:

| Must demonstrate | Where it is proved |
|---|---|
| workflow orchestration | `BOA-S1` — `D-w04-2` |
| external tools | `BOA-S0` — `D-w03-2` — and `BOA-S1` |
| retries | retry-on-validation-failure in `BOA-S0`, `D-w03-2` |
| approval gates | the draft-only send path in `BOA-S1`, `D-w04-2` |
| audit trail | the append-only trail in `D-w04-2`, given provenance in `S7b` |
| handling malformed input | month 05, `D-m05-3` |
| handling malicious input | month 05 memory poisoning, `D-m05-2` |

Malformed and malicious input sit side by side in the same month on purpose. They
look alike at the parser and are completely different at the threat model, and
running them together is what forces the distinction to be stated rather than
assumed.

## Stages

### BOA-S0 — structured extraction over company sites (W03)

- **Entry.** A prospect list and a target schema exist.
- **Exit.** A valid schema instance is extracted from at least 8 of 10 real company sites, with every rejection recording a reason.
- **Demo.** `make demo-boa-s0 URL=<company-url>`
- **Adds** data extraction. **Ceilings:** EUR 0.0, at most 20 runs.

Note what the exit does *not* say: it does not require ten of ten. Two failures
out of ten are expected, and the requirement that each carries a recorded reason
is the part that matters. A silent extraction failure is indistinguishable from a
company with nothing to extract.

### BOA-S1 — draft-only outreach with approval and audit trail (W04)

- **Entry.** BOA-S0 exits.
- **Exit.** Nothing sends without an approval record; an attempt to bypass is refused and logged.
- **Demo.** `make demo-boa-s1 PROSPECT=<id>`
- **Adds** proposed action and human approval. **Ceilings:** EUR 0.0, at most 25 runs.

This stage extends BOA-S0. The exit is written as a prohibition rather than a
capability because that is how it is testable: the interesting assertion is about
what the system refuses, and a refusal that is not logged has not been proved.

### BOA-S2 — durable per-account agent memory (M05)

- **Entry.** BOA-S1 exits.
- **Exit.** Facts accumulated about an account persist ACROSS sessions and are read by LATER, SEPARATE decision cycles as trusted input — with provenance and a trust tier on every write.
- **Demo.** `make demo-boa-s2-memory ACCOUNT=<id>`
- **Adds** memory. **Ceilings:** EUR 5.0, at most 40 runs.

Read the exit as a specification for the attack that follows it. Persistence
across sessions and a *later, separate* decision cycle are not descriptive
flourishes; they are the two properties that make `EXT-03` memory poisoning
instead of ordinary prompt injection. Provenance and trust tiering are the
mitigation surface, and they must exist before the attack, or the attack has
nothing to defeat.

## Capabilities gained

| Capability | Stage first delivering it |
|---|---|
| data extraction | BOA-S0 |
| proposed action | BOA-S1 |
| human approval | BOA-S1 |
| memory | BOA-S2 |

Four capabilities against seven pipeline steps. Classification, CRM lookup and
the CRM write exist from BOA-S0 onward and are not staged: they are tool calls
whose difficulty is in their permissions rather than in their behaviour, and
`S7b` is where that difficulty is addressed.

## Runnable demos

| Stage | Its demo counts as run when |
|---|---|
| BOA-S0 | 10 real sites yield at least 8 valid instances and 100% of rejections carry a reason |
| BOA-S1 | a draft exists with no send, and a forced bypass attempt appears in the audit log as refused |
| BOA-S2 | a fact written in one session is read by a decision made in a later one, with its provenance shown |

The BOA-S2 criterion cannot be satisfied inside one run. Demonstrating it takes
two invocations separated by a full cycle, and a demo that shows the fact being
written and read in the same breath has demonstrated a variable, not a memory.

## Constraints

**It never sends.** No outbound message leaves this system without an approval
record naming a human, and there is no configuration flag that relaxes this. The
constraint holds through `BOA-S2` and beyond: memory makes the agent's proposals
better informed, not more autonomous. The audit trail is append-only, which means
a bypass attempt is not merely blocked but permanently visible — a refusal with
no record is an assertion about the past rather than evidence of it.

**Memory is not task state, and neither is a corpus.** These three are routinely
collapsed into one and the programme keeps them apart deliberately. Task state
says which step of a pipeline has completed and is machine bookkeeping. A corpus
is documents someone else wrote, retrieved at query time. Memory is a claim the
agent formed and stored about the world, written by its own path from input it
did not verify — and that authorship is precisely why it is dangerous. Every
write therefore carries an origin channel and a trust tier, and **repetition is
never treated as corroboration**: an attacker's cheapest move is to say the same
false thing many times.

**The classification step must not be able to command the write step.** This
pipeline is a textbook confused deputy: classification reads attacker-supplied
text and holds almost no privilege, while the CRM write holds a great deal and
trusts what reaches it. If the low-privilege step can relay an instruction the
high-privilege step executes without re-checking the original human request,
every approval gate upstream has been routed around rather than defeated. The
`W12` exercise builds exactly that forgery and patches it with per-action
re-authorization, and the patch is only credible because the demonstration came
first.

**Placeholder identities throughout.** The repository is private now and
public-capable later, so no client name, no prospect name and no personal data
appears in a tracked file. Real prospect data lives in gitignored local files.
This is a constraint on the project and not only on its documentation: the demo
commands above take an opaque identifier rather than an address for that reason.

**Its numbers are business evidence and are tagged as such.** Counts produced by
this agent — prospects researched, drafts prepared, sends approved — are logged
with an `evidence_source` marking of real or simulated, and the two are never
added together. The funnel recalibration reads those counts, so a count logged
without its tag is worse than a count not logged at all.
