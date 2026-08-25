# Week 11 — Attacking your own retrieval agent

## Outcome

By Sunday I have redirected my own agent using content it retrieved rather than
anything I typed, counted what fraction of those attempts actually changed its
behaviour, and broken one leg of the trifecta structurally rather than
filtering for it.

## Time budget

- Theory: 3.5 h
- Building: 5.5 h
- Testing/evaluation: 3.0 h
- Customer discovery: 3.0 h

Theory is at its ceiling with nothing spare: T-w11-1 at 1.5 h plus T-w11-2 and
T-w11-7 at 1.0 h each exhaust the allowance exactly. That turns a preference
into a rule — T-w11-9 is half an hour of testing and stays classified as
testing, because reclassifying it pushes the week past a cap canon checks
mechanically. USI-09 records the security baseline as Awareness: no structured
attack thinking, no trust-boundary analysis, no least-privilege design practised
deliberately, which is why two theory tasks precede the first line of S7a.

Ceilings are EUR 0.00 of metered spend and 80 agent runs. Canon publishes the
arithmetic behind that count instead of asserting it: three techniques across
five variants against four queries, run before and after the mitigation, plus
the control arm. EX-FAIL-13 detects an attack as deviation from control, so a
budget omitting that arm would fund the attack and not the detector.

Compressed week, 8.0 h: T-w11-3, T-w11-4, T-w11-5 trimmed to 1.4 h, and T-w11-11
with T-w11-12 at 2.6 h — the cheapest discovery pair above the floor — then slip
the calendar instead of doubling up. What defers is T-w11-1 and T-w11-2, the
exfiltration attempt, the cited-answer contract and T-w11-10, all to
[week 12](week-12.md). Record the consequence rather than absorbing it quietly:
part of portfolio item #5 moves into month 05, where the memory-poisoning chapter
that closes the item already lives. Nothing ticks. D-w11-1 carries without its
written trust-boundary argument, D-w11-2 without its covert exfiltration channel,
D-w11-3 whole, D-w11-4 without its 10 follow-ups. DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| prompt injection | D | P0 | the direct-injection control arm named in T-w11-2 → D-w11-2 |
| indirect prompt injection | D | P0 | T-w11-5's three payload styles run against S7a → D-w11-2 |
| data exfiltration | D | P0 | T-w11-6, including the covert channel → D-w11-2 |
| output validation | D | P0 | T-w11-4 → D-w11-1, and the citation rejection in T-w11-8 |
| structured outputs | C | P0 | T-w11-7, then the answer-plus-citation contract in T-w11-8 |
| context construction | C | P0 | T-w11-3's operator-against-document separator → D-w11-1 |
| kill criteria | F | P0 | T-w11-12 resolves the thresholds the W12 verdict will read |
| willingness to pay | F | P0 | the qualification pass over the pain register in T-w11-11 |

Every row resolves to a canon concept carrying P0, so none needs the earn-it or
competency fallback — but the reasoning sits in five files. The four security
rows belong to [Track D](../tracks/ai-security.md), the week's largest by hours.
Structured outputs and context construction are
[Track C](../tracks/ai-application-engineering.md), taken here as security
controls rather than parsing conveniences. Willingness to pay is a
[Track F](../tracks/micro-saas.md) concept, but kill criteria — also Track F —
is homed in [the SaaS validation file](../business/saas-validation.md), which
owns the seven thresholds T-w11-12 resolves; a track's topics do not all share a
home. The qualification checklist belongs to
[the consulting offer](../business/consulting-offer.md) and the follow-up
cadence to [outreach](../business/outreach.md), both tasks reasoning from
[Track E](../tracks/consulting.md). S7a is defined in
[the platform file](../projects/engineering-agent-platform.md); the cited-answer
contract extends
[the Secure Knowledge Agent](../projects/secure-knowledge-agent.md).

## Tasks

### Task 1

`T-w11-1` — 1.5 h, Track D, theory, reinforcing C. Reading: `RES-12`. Trust
boundaries and the lethal trifecta: private data, exposure to untrusted
content, and a channel that can communicate outward. Canon attributes the
framing to Simon Willison on 2025-06-16 and records it as independent rather
than a standards-body category. Generated agent code treats the context window
as one trusted blob, inserting no boundary between text the operator typed and
text a document carried, so an instruction in the latter executes with the
authority of the former. Write down which legs the knowledge agent holds
before touching any of them.

### Task 2

`T-w11-2` — 1.0 h, Track D, theory. Reading: `RES-11`. Indirect against direct
injection, and output validation as a structural control rather than a
prompt-level one. The examinable distinction is between asking the model to be
careful and changing the architecture so retrieved text cannot carry authority
at all; only the second eliminates the class. Settle the direct-injection arm
here: it is the control the indirect result is read against.

### Task 3

`T-w11-3` — 2.0 h, Track D, building, reinforcing C. Build S7a: retrieved
content becomes untrusted by construction. Provenance tagging at ingest,
retrieval tiered by trust, and a hard separator between operator instructions
and document content. The tag is attached at write time deliberately: no
read-time policy can be expressed over data whose origin was never recorded.

### Task 4

`T-w11-4` — 2.0 h, Track D, building. Build output validation and the
structural trifecta break: any turn that touched untrusted input in that cycle
loses its external-send capability. Leg removal rather than filtering, which
is what the week is graded on: a filter is a claim about payloads already
seen.

### Task 5

`T-w11-5` — 1.5 h, Track D, testing. Run the indirect-injection suite against
a fixed query set using at least three techniques — canon names instruction
override, persona or role-play override, and delimiter or format confusion —
and measure attack success rate against the control before and after the
mitigation. Write up the failed techniques beside the successful ones: a suite
publishing only its hits measures the author's taste in payloads, not the
system.

### Task 6

`T-w11-6` — 1.0 h, Track D, testing. Attempt exfiltration, including at least
one covert channel alongside the direct ask — data encoded into a
helpful-looking URL parameter is the canonical shape. Then state, per leg,
whether the fix broke it structurally or merely filtered. A mixed answer is
fine, an unstated one is not.

### Task 7

`T-w11-7` — 1.0 h, Track C, theory, reinforcing D. Reading: `RES-11`. Output
contracts and schema validation read as a security control, not a parsing
convenience: a schema with no field for an instruction cannot carry one. It is
the last place a hijacked turn can be stopped and the only one whose control
is deterministic code rather than the model's cooperation.

### Task 8

`T-w11-8` — 1.5 h, Track C, building, reinforcing D. Build the cited-answer
contract on the knowledge agent: the answer plus the chunk ids it rests on,
rejected when a cited id is absent from the retrieved context. Rejection
rather than a warning, because a warning obliges nobody downstream to act.

### Task 9

`T-w11-9` — 0.5 h, Track C, testing. Assert the citation check rejects a
deliberately unfaithful answer fixture. Half an hour buys the fixture and the
assertion, not a survey — what the check misses belongs to the third
reflection question.

### Task 10

`T-w11-10` — 0.4 h, Track E, business. Send 10 follow-ups. All 52 sends have
matured, so ACT-2 was evaluated at the close of [week 10](week-10.md): zero
replies across the fully matured list activates the branch. It trips 8.5% of
the time at the band midpoint and 1.6% at the ceiling, but 45.8% at the floor.
Activation means an out-of-cycle delta re-pitching the funnel, the simulated
Stage-1 track extended across the remaining business deliverables, and
reclaimed hours taken from [the cut list](../reference/low-roi-and-cuts.md).
If it did not trip, these touches carry the remaining chance: 42% to 65% of
replies come on a follow-up rather than a first touch.

### Task 11

`T-w11-11` — 1.1 h, Track E, business, reinforcing F. Apply the qualification
checklist to the pain register and write the offer sketch. The register was
assembled in [week 10](week-10.md), every row carrying its own evidence tag,
and under the corrected funnel most rows are expected to be Stage-1 simulated.
Canon's fallback says so without apology: the sketch is written against the
simulated register and tagged `evidence_source: simulated`. That is a passing
deliverable. A simulated row presented as real is not.

### Task 12

`T-w11-12` — 1.5 h, Track F, business, reinforcing E. Resolve the seven SaaS
evidence thresholds to concrete numbers and say why each number rather than a
neighbouring one. Canon carries defaults for all seven, ET-1 through ET-7;
this week may raise them on evidence but may not lower them without a delta.
Five take a count. The other two do not: ET-5 asks for a named acquisition
channel with a measured cost per conversation, ET-6 for a payback period
computed from a measured baseline using the fully-loaded method. Both resolve
to measurements the programme's own funnel produces, which is why an industry
ROI average satisfies neither.

## Deliverables

- [ ] D-w11-1 — S7a: provenance tagging at ingest, trust-tiered retrieval, a hard operator/document separator, output validation, and the structural trifecta break — at `agentplat/trust/`, `docs/w11/trust-boundary.md`
- [ ] D-w11-2 — Attack suite report against the learner's own system, covering indirect prompt injection and data exfiltration: at least three injection techniques, at least one covert exfiltration channel, attack success rate before and after, and a statement of which trifecta leg was broken structurally. It doubles as the five-part failure report and as the opening chapter of portfolio item #5 — at `docs/w11/injection-exfiltration-report.md`, `tests/attacks/test_injection.py`
- [ ] D-w11-3 — Cited-answer contract: the knowledge agent rejects an answer whose citation is absent from retrieved context, proved against a deliberately unfaithful fixture — at `agentplat/ska/answer.py`, `tests/test_cited_answer.py`
- [ ] D-w11-4 — Offer sketch drawn from the qualified pain register, the seven SaaS evidence thresholds resolved to concrete numbers, and 10 follow-ups logged — at `docs/w11/offer-sketch.md`, `docs/w11/saas-thresholds.md`, `send-log.local.md`

## Acceptance criteria

- [ ] AC-w11-1a — retrieved content is structurally marked untrusted at ingest with a provenance tag, and an ingest path omitting the tag fails a test; the same design note names all three trifecta legs, says which the tag alone does not remove, and says why validation sits in code rather than in the prompt (T-w11-3, T-w11-1, T-w11-2)
- [ ] AC-w11-1b — no turn that touched untrusted input during a cycle can reach an external-send tool; the refusal is enforced in code and written to the audit log, never requested in a prompt (T-w11-4)
- [ ] AC-w11-2a — at least three distinct injection techniques are attempted, successes and failures are both documented, and attack success rate is reported with a stated denominator (T-w11-5)
- [ ] AC-w11-2b — at least one covert-channel exfiltration technique is attempted in addition to a direct ask, and the report states explicitly whether the fix breaks a trifecta leg structurally or only filters (T-w11-6)
- [ ] AC-w11-2c — no industry effectiveness percentage for injection defence appears anywhere in the report; every number in it is a measurement of this system, with its denominator (T-w11-5, T-w11-6)
- [ ] AC-w11-2d — the indirect-injection exercise carries all five named sections, and each proving test fails when run against the pre-mitigation build (T-w11-5)
- [ ] AC-w11-3a — an answer citing a chunk id absent from the retrieved set is REJECTED rather than warned about, proved by the unfaithful fixture; and the contract's schema is documented field by field, showing no free-text slot an instruction could occupy (T-w11-8, T-w11-9, T-w11-7)
- [ ] AC-w11-4a — all seven evidence thresholds resolve with a one-line justification each and no placeholder left standing, the two taking no count resolving to named measurements rather than guesses; and the week's business row reaches SCOREBOARD — 10 follow-ups and the offer sketch, each marked `evidence_source` real or simulated (T-w11-12, T-w11-10, T-w11-11)

## Stretch goal

Outside the 15 hours. Test whether the trust-tier weighting can be inverted by
an attacker who controls document VOLUME rather than document content: flood the
corpus with individually harmless low-trust chunks and see whether ranking hands
them the top-k anyway. T-w11-3's tier is a weight, and a weight can be outvoted.
Attempt it only once all four deliverables are ticked.

## Failure exercise

One exercise, on the seam the whole build rests on: the index answers from
documents the learner does not fully control. Its body lives in
[the agent-failure set](../exercises/agent-failures.md) and the attack shapes in
[the security exercise set](../exercises/ai-security.md); D-w11-2 is the report.

### EX-FAIL-13 — indirect prompt injection inside retrieved document

- **Detection.** Compare behaviour against a control run over an unpoisoned corpus. A successful attack shows as deviation from that control, never as recognition of the payload — a detector that catches only payloads it has been shown is a signature list, and the next style is written by someone who has read it.
- **Safe failure behaviour.** Retrieved content is untrusted structurally: provenance at ingest, a hard boundary between operator instructions and document text that the model cannot be talked across, and no path by which a document alone authorises a tool call. All three hold without the model's cooperation.
- **Recovery.** Strip external-send capability from any turn that touched untrusted input during that cycle — a leg removed from the trifecta rather than a filter placed in front of it. The filter is defeated by a payload it has not seen; the removal is not.
- **Logging.** Record payload style, the query, the control output, the poisoned output, and whether an external-send tool was attempted. Those five fields turn the suite into a rate with a denominator rather than a pile of anecdotes, and are what a later month re-runs against.
- **Test proving the mitigation.** At least three payload styles across the fixed query set, attack success rate reported against control before and after, a stated denominator, and no industry percentage anywhere. It fails against the version that concatenates retrieved text straight into the instruction context — which is what the knowledge agent is until this exercise lands.

## Reflection

1. Could a purely prompt-based instruction have stopped the exfiltration?
   Explain why breaking a trifecta leg structurally is a different KIND of
   control from filtering for it.
2. Which of your mitigations survives an attacker who knows exactly which
   mitigation you deployed?
3. Your citation check rejects an unsupported claim. What class of unfaithful
   answer does it still let through, and what would catch that?

## Evidence

- `make demo-s7a-attack` — this stage's runnable demo command — with a path to S7a, its provenance tagging and its trust-tier configuration.
- The test proving an untrusted-input turn cannot invoke an external-send tool.
- The attack-suite report with per-technique success rate before and after.
- The exfiltration attempt log, including the covert-channel attempt.
- The unfaithful-answer fixture and the rejection it triggers.
- Path to the offer sketch and to the resolved evidence thresholds.

Log actual hours below as one line, planned first: `Theory 3.5 / <actual> ·
Building 5.5 / <actual> · Testing 3.0 / <actual> · Discovery 3.0 / <actual>`.
This is the week the M1 correction is furthest from its evidence, so the region
matters most here: eight weeks of drift is what the M3 delta reads against.
Funnel counts belong in [the scoreboard](../SCOREBOARD.md).

<!-- user:actuals key="W11" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- Provenance tagging lands at ingest and an untagged path fails — 20
- The trifecta leg is broken in code rather than filtered — 20
- The attack suite runs three techniques against a control — 20
- A covert exfiltration channel was attempted, not only a direct ask — 10
- The cited-answer contract rejects an absent citation — 15
- All seven evidence thresholds carry resolved numbers — 15
