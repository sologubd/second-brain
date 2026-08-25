# Month 05 — Memory, and the first attack that outlives a session

## Outcome

The Business Operations Agent remembers things about an account across sessions
— and I have poisoned that memory and watched a later decision act on the false
fact.

The brief asks for agent memory in three places and the programme had nowhere
honest to put it: task state is bookkeeping, a corpus is written by an ingestion
job. Building the surface first is what makes the attack genuine.

## Deliverables

- [ ] `D-m05-1` — `BOA-S2`, durable per-account agent memory: what the agent learns about a contact survives the session that learned it, and every write carries its origin and a trust tier.
- [ ] `D-m05-2` — The memory-poisoning attack report. A false fact arrives on an untrusted channel, lands in durable memory, and is read as ground truth by an unrelated decision a cycle later; one structural mitigation — provenance, write-time validation or expiry — blocks it, measured either side of the patch. This closes `PF-05`.
- [ ] `D-m05-3` — Malformed-input handling for the business agent, beside the malicious-input work, plus a written statement of which sandboxing tier the code-execution surface runs at.
- [ ] `D-m05-4` — The first fixed-scope free or cheap pilot, if the funnel produced one. If not, the simulated track continues and the retrospective records the funnel position as it stands.

Three further topics are homed here without deliverable ids: Track F competition
analysis, spread across months 05 to 09; the Track E subcontracting side-quest,
across months 04 to 07; and case study production. What each can say turns on
`D-m05-4`.

## Funnel targets

Canon states no volumes here. The row reads, in full: set by the M2 delta — a
deferral with a reason. Months 01 through 03 derive targets from the week index
because the weeks underneath enumerate every send; from month 04 there are none
underneath, and volumes follow measured rates rather than assumed ones.

Whatever it sets, counts land in [the scoreboard](../SCOREBOARD.md) and each
artifact is tagged `evidence_source` as real or simulated — the tag `D-m05-4`
most needs, since a simulated substitute logged as real corrupts the one
instrument the M9 gate cannot fake.

## Stages entered

`BOA-S2` and `S9`.

`BOA-S2` is the business agent's memory stage. `S9` opens the architecture and
ADR lane, which also carries agent roles, skills and failure reporting and runs
through month 08. Entry and exit conditions, demo commands and ceilings belong
to [the business agent](../projects/business-operations-agent.md) and
[the engineering platform](../projects/engineering-agent-platform.md).

One precondition matters more than the rest: the poisoning message and the
decision acting on it must be separated by a full pipeline cycle, not a context
window. Without that gap a reviewer may fairly reclassify the exercise as
ordinary prompt injection — the line OWASP draws between the classes — while
with it the shape matches the worked example published under `ASI06`.

No week files sit beneath this month by design: the detailed weeks cover months
01 through 03, and the month is the unit thereafter.

## Failure exercises

Two of them, taken from the extended rows that the calendar months use — which
is precisely what leaves each of the fourteen canonical exercises sitting in
exactly one week. Their bodies are in
[the agent-failure set](../exercises/agent-failures.md), and `D-m05-2` and
`D-m05-3` are what they produce.

### `EXT-03` — memory poisoning of durable per-account memory

- **Detection.** Every write records its origin and the read path scores it. The signal is an entry pointing at an untrusted channel whose claim has been reinforced unusually often.
- **Safe failure behaviour.** Repetition is not corroboration. An entry able to move a high-impact decision surfaces on two factors: a provenance score and a human-verified tag. Unverified entries expire.
- **Recovery.** Quarantine the entry, re-derive every decision that read it, and close the loop letting the agent's own output back into trusted memory.
- **Logging.** Keep the origin channel, the trust tier, the reinforcement count, the later decision that read the entry, and its outcome — five fields that make the report evidence rather than anecdote.
- **Test proving the mitigation.** The attack succeeds before the patch and is measurably blocked or flagged after it, poisoning and exploitation a cycle apart. Report the false-positive rate on legitimate writes too: a filter quarantining ordinary mail has bought safety with a useless agent.

### `EXT-04` — malformed input to the operations agent

- **Detection.** An inbound document either fails schema extraction or yields an instance that validates and is implausible anyway.
- **Safe failure behaviour.** A validation failure is a retry signal with a recorded reason, never a silent default. A valid-but-implausible extraction escalates.
- **Recovery.** Re-extract against a narrowed schema; past a bounded attempt count the document routes to a human.
- **Logging.** Retain the raw input, the violated constraint, the retry count and the disposition, so the corpus replays against a later parser.
- **Test proving the mitigation.** A corpus of deliberately broken documents yields zero silent defaults and zero acted-on implausible extractions, and fails against the pre-mitigation extractor.

## Retrospective

All ten are answered, in a light month as much as a heavy one; a skipped
question turns this section into a diary. Each carries a clause saying where in
this month the answer is likely to be found, because a question asked twelve
times gets a lazier answer each time unless it is pointed somewhere.

1. What can I now build that I could not build 30 days ago? Point at the demo command, not at hours.
2. Which concept remains theoretical? Sandboxing tiers, probably.
3. What broke in real usage? The memory write path is new; start there.
4. What did agents repeatedly fail at? Read against what `EXT-04` logged.
5. What should become a reusable skill? `S9` is where the answer lands.
6. What should become a deterministic tool instead of an LLM decision? Trust scoring qualifies: scoring by model invites being argued out of the rule.
7. Where did human approval prove necessary? Every high-impact memory write qualifies.
8. What business problems appeared repeatedly? These feed the register `CP-M9` scores.
9. What should I stop learning? Answered against the low-ROI table, never freehand. Sandboxing depth is the likely entry this month, since `D-m05-3` states a tier rather than studying all of them.
10. What should I double down on? Asked with its operationalised follow-up: which of the last four weeks' deliverables taught you something you did not already know? A track scoring zero of four triggers a delta re-pitching it.

`RQ-11` — a canon delta — is this programme's addition, not the brief's: ten
answers produce findings, the eleventh turns one into an edit. Run
`make delta MONTH=05`, fill the stub, edit canon, bump `meta.version`, then
regenerate and re-check.

## Mandated delta

**Type:** `security_arc_recalibration`.

Canon's procedure, verbatim: 22.5h of Track D across 17 topics from an Awareness
baseline is compressed. Assess after the memory-poisoning work whether months
06–08 need to carry more of Track D than currently stated, and rewrite if so.

`USI-09` fixed that baseline at Awareness before week one: threat modelling and
privilege design had never been deliberate practice. Seventeen topics against
that start was called compression at the time, not discovered here. This month
supplies the first evidence to judge it on — an attack conceived, run and
mitigated on a surface built the same month.

## Checkpoint

No gate closes this month. The one it feeds is `CP-M6`, landing at the end of
month 06 and asking whether AI workflows can be shipped production-grade rather
than merely working. Seven deliverable ids answer it. This month supplies one of
them — `D-m05-2`, the attack report — and it is the only item on that list
measured against a memory surface rather than against a corpus, a retrieval path
or a tool call.

`D-m05-1` is what makes that contribution possible: without a memory surface
there is nothing to poison, and the evidence would be an argument instead of a
measurement. Nor can it be back-filled at the gate — an attack report needs a
before as well as an after.
