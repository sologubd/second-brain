# Week 06 — Measuring retrieval, and attacking it

## Outcome

By Sunday every retrieval change I make is a diffable experiment against a
frozen labelled set, and I have poisoned my own index and measured how often it
worked.

## Time budget

- Theory: 2.5 h
- Building: 5.5 h
- Testing/evaluation: 3.5 h
- Customer discovery: 3.5 h

No new subsystem ships. SKA-S1 extends SKA-S0 and canon declines to count it, so
every building hour buys depth on an index that already answers. The pitch stays
at fundamentals: USI-08 places the retrieval baseline at Awareness and W05 was
the first hybrid index this learner had ever stood up. USI-09 puts security at
Awareness too, which is why T-w06-5 spends an hour on category definitions before
T-w06-6 sends a payload. Ceilings are EUR 0.00 and 60 agent runs, a count canon
derives as three techniques across five payload variants across four queries,
plus the control; metrics are deterministic and claim none of it, so the runs go
to the attack suite and the euros stay at zero. These are planned figures — canon
measures a week in work rather than time, so an overrun costs days, not scope.

Query rewriting is the week's bargain, folded into T-w06-3 beside reranking at no
incremental hour cost because one examinable boundary separates them: reranking
reorders what the retriever found, rewriting changes what is findable. Structured
output rides the same task, its cited-chunk schema being a constraint rather than
a component.

Compressed week, 8.0 h: T-w06-3, T-w06-4, T-w06-6, T-w06-7 cut to 0.8 h, and
T-w06-10 with T-w06-12 and T-w06-13. Discovery lands at 2.7 h, the cheapest of
this week's four business tasks that still clears the 2.5 h floor. Canon then
defers the chunking sweep and the entire Sentry corpus into
[week 07](week-07.md), where the outstanding 8 labels already live. The first
deferral sits badly beside the subset: T-w06-4 recomputes metrics *per
configuration*, and T-w06-2's sweep produces those configurations, so the
compressed week keeps the measurement and drops what it measures. Stated, not
resolved. Nothing ticks: D-w06-1 carries with the sweep, D-w06-2 with T-w06-5's
category distinctions, D-w06-3 whole, D-w06-4 short of its follow-up batch.
DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| chunking | C | P1 | T-w06-2's three-configuration sweep → D-w06-1 |
| reranking | C | P1 | T-w06-3's cross-encoder over the hybrid top-20 → D-w06-1 |
| query rewriting | C | P1 | folded into T-w06-3 at no extra hours → D-w06-1 |
| metadata filtering | C | P0 | T-w06-2, layered on the permission pre-filter → D-w06-1 |
| evaluations | C | P0 | T-w06-1 settles the metrics, T-w06-4 computes them → D-w06-1 |
| RAG poisoning | D | P0 | T-w06-5's category work, then T-w06-6 → D-w06-2 |
| prompt injection | D | P0 | the three techniques seeded in T-w06-6 → D-w06-2 |
| misleading code comments | A | exercise EX-FAIL-08 | T-w06-9 → D-w06-3 |

Seven rows carry a canon concept's priority verbatim; the three P1s are marked
`implementation` in canon while every P0 here is marked `durable`, so the split
tracks kind rather than importance-this-week. The eighth row has no concept
row at all: canon holds misleading code comments only as failure exercise
EX-FAIL-08, reaching the week through T-w06-9, a Track A task. One naming
conflict is worth flagging rather than smoothing away — the tasks and D-w06-1
call the evaluation set the frozen W05 label set, while canon's chunking concept
calls the same object the frozen W06 eval set. This file renders the task wording
and picks no side.

Homes differ row by row, so check each. The five Track C rows reason from
[Track C](../tracks/ai-application-engineering.md); the two Track D rows from
[Track D](../tracks/ai-security.md), which also owns the verbatim distinctions
T-w06-5 reproduces, alongside
[the security exercise set](../exercises/ai-security.md). EX-FAIL-08's body
belongs to [the agent-failure set](../exercises/agent-failures.md); the Track A
tasks reason from [Track A](../tracks/agentic-engineering.md). The business split
matters: sends and research are homed in [outreach](../business/outreach.md), the
nine dimensions in
[the opportunity scorecard](../business/opportunity-scorecard.md), and the
practice around them in [Track E](../tracks/consulting.md), with three of those
four tasks reinforcing [Track F](../tracks/micro-saas.md). SKA-S1 belongs to
[the Secure Knowledge Agent](../projects/secure-knowledge-agent.md).

## Tasks

### Task 1

`T-w06-1` — 1.5 h, Track C, theory. Reading: `RES-07`. Chunk boundaries as a
retrieval ceiling, then the ranking metrics: precision@k, recall@k, MRR and
NDCG@k. The examinable point is why a rank-blind metric lets a system pass
while its reranker has parked the best answer at position 5. Settle which are
rank-blind before any number exists.

### Task 2

`T-w06-2` — 1.5 h, Track C, building, reinforcing D. Sweep three chunking
configurations — fixed 200-token, fixed 500-token, recursive-with-overlap —
holding everything else constant, and add metadata filters over the
permission-filtered index. Held constant means embedding model, fusion, k and
query set — one moving part, or the sweep measures nothing.

### Task 3

`T-w06-3` — 2.0 h, Track C, building. Rerank the hybrid top-20 with a local
CPU cross-encoder, add query rewriting, and force the answer through a schema
carrying cited chunk ids. Canon names bge-reranker-v2-m3 as primary and the
22.7M-parameter ms-marco-MiniLM-L6-v2 for the exercise, and hard-excludes
jina-reranker-v2-base-multilingual: non-commercial weights, against USI-05's
public-capable-later repository.

### Task 4

`T-w06-4` — 1.5 h, Track C, testing. Recompute NDCG@5, MRR and precision@5 for
each configuration against the frozen W05 label set, with no re-labelling in
between, and log p50 and p95 rerank latency. Re-labelling mid-sweep is the one
move that makes the whole table incomparable.

### Task 5

`T-w06-5` — 1.0 h, Track D, theory, reinforcing C. Reading: `RES-11`. Separate
corpus poisoning from memory poisoning and from goal hijack, using canon's
definitions verbatim and answering three questions per category: what is
retained, who writes it, when it is read. Canon draws the line at authorship —
poisoned documents arrive through a separate ingestion process, not from the
agent's unverified conversation.

### Task 6

`T-w06-6` — 1.0 h, Track D, building, reinforcing C. Seed an injection corpus
into your own index with at least three distinct techniques: instruction
override, persona or role-play override, and delimiter or format confusion.
Your own index is the point — a borrowed benchmark describes someone else's
pipeline.

### Task 7

`T-w06-7` — 1.0 h, Track D, testing. Measure attack success rate against a
control run, apply exactly one structural mitigation — retrieved content is
untrusted — and re-measure. One, because two together cannot be attributed.
Report against your own denominator, and cite no vendor effectiveness figure
near it.

### Task 8

`T-w06-8` — 1.0 h, Track A, building, reinforcing C. Build the commit-matcher
script: given a historical Sentry issue, find the commit that fixed it. Its
accuracy is a measurement, not a convenience.

### Task 9

`T-w06-9` — 1.0 h, Track A, testing. Label 12 real historical Sentry issues,
at least two carrying a code comment that misdescribes the code, run the agent
against them, and write the five-part report. These 12 open a ground-truth
corpus nothing else in the programme substitutes for.

### Task 10

`T-w06-10` — 1.15 h, Track E, business, reinforcing F. Research 22 prospects
using BOA-S0 assistance — the largest research block in the programme, and the
second half of its 32 assisted prospects.

### Task 11

`T-w06-11` — 0.8 h, Track E, business, reinforcing F. Nine cold emails, each
drafted on BOA-S0's extraction and approved individually before it leaves.
Their replies mature into next Sunday's rows, not this one's.

### Task 12

`T-w06-12` — 0.45 h, Track E, business. Twelve follow-ups, two per prospect
already written to. Canon rates the follow-up multiplier its best-supported
figure, whose consequence is that a second touch is nearer necessary than
optional, provided it carries what the first did not.

### Task 13

`T-w06-13` — 1.1 h, Track E, business, reinforcing F. Score one automation
opportunity across all nine scorecard dimensions, citing per-dimension
evidence rather than intuition. OS-8, willingness to pay, is where wishful
scoring is most fatal; OS-7, buyer access, is what generic automation
literature omits by presuming a captive internal buyer, and USI-03 records
this pipeline at zero.

With that pipeline at zero, OS-8 is the one dimension a conversation would
normally supply and none is expected. The prospect counts need no substitute;
OS-8 does. Canon's fallback names four observable signals — a published
competitor price, a public job posting for the role this work would displace, a
paid tool already in the stack doing part of the job, or a written reply naming
a budget — each recorded with a link or local path. It names the near-misses
too, since they are what the escape clause otherwise absorbs: expressed
interest, a booked-but-unheld call, inbound curiosity, your own estimate of the
work's worth. With none of the four, score OS-8 NULL and
ship the dimension explicitly unscored — a passing deliverable. A scorecard able
to return *no evidence for willingness to pay* is what makes the first kill
criterion observable rather than decorative.

## Deliverables

- [ ] D-w06-1 — SKA-S1 with chunking, reranking, metadata filters, query rewriting and a cited-answer schema — definition of done is a MEASURED NDCG@5 and MRR result per configuration against the frozen W05 label set, with rerank latency recorded — at `agentplat/ska/`, `docs/w06/retrieval-metrics.md`
- [ ] D-w06-2 — RAG-poisoning attack report: at least three injection techniques, attack success rate before and after one structural mitigation, and the verbatim distinction between corpus poisoning, memory poisoning and goal hijack — at `docs/w06/rag-poisoning-report.md`
- [ ] D-w06-3 — Sentry corpus part 1: commit-matcher script plus 12 labelled historical issues, including the five-part misleading-code-comments failure report — at `agentplat/sentry/match.py`, `evals/sentry-corpus.jsonl`, `docs/w06/misleading-comments-report.md`
- [ ] D-w06-4 — 22 prospects, 9 sends, 12 follow-ups logged, and one opportunity scored on all nine dimensions with per-dimension evidence — at `send-log.local.md`, `docs/w06/opportunity-01.md`

## Acceptance criteria

- [ ] AC-w06-1a — a metrics table exists with one row per chunking configuration and one column per metric, the same labelled queries used for every row with no re-labelling, and the write-up names which of precision@k, recall@k, MRR and NDCG@k are rank-blind and what a rank-blind pass would have concealed (T-w06-2, T-w06-4, T-w06-1)
- [ ] AC-w06-1b — at least one CONCRETE example is named where a chunk boundary caused a relevant answer to be missed or truncated, and a metadata-filtered query is shown running through the permission pre-filter rather than beside it (T-w06-2, T-w06-4)
- [ ] AC-w06-1c — the reranking write-up states whether reranking reordered an already-correct top-5 or pulled in a relevant document from outside it, and explains why it can never do the latter; it names one failure query rewriting fixed that reranking structurally could not, reports p50 and p95 rerank latency, and shows an answer whose schema carries its cited chunk ids (T-w06-3, T-w06-4)
- [ ] AC-w06-2a — at least three distinct injection techniques were attempted — instruction override, persona or role-play override, and delimiter or format confusion — each seeded into the learner's own index rather than borrowed from a published benchmark, and the report documents both successes AND failures (T-w06-6, T-w06-7)
- [ ] AC-w06-2b — attack success rate is reported as a measurement against the learner's OWN system with a stated denominator, before and after the single structural mitigation. No industry effectiveness percentage appears anywhere in the report (T-w06-7)
- [ ] AC-w06-2c — the report names the architectural change that eliminates the class, distinguishes it from a prompt-level patch, and reproduces canon's distinction between corpus poisoning, memory poisoning and goal hijack, each answered on what is retained, who writes it and when it is read (T-w06-5, T-w06-7)
- [ ] AC-w06-3a — 12 issues are labelled with issue id, fixing commit sha and a difficulty note; the commit-matcher's accuracy on those 12 is stated as a number (T-w06-8, T-w06-9)
- [ ] AC-w06-3b — the misleading-comments report contains all five named sections and its proving test fails against the pre-mitigation code (T-w06-9)
- [ ] AC-w06-4a — the scored opportunity cites evidence per dimension, with buyer access and willingness to pay backed by an actual conversation or observable signal rather than assumption, and the week's funnel row reaches SCOREBOARD — 22 prospects, 9 sends, 12 follow-ups — each carrying `evidence_source` (T-w06-13, T-w06-10, T-w06-11, T-w06-12)

## Stretch goal

Outside the 15 hours. Bucket the scored opportunity into the industry
value-by-feasibility 2x2 as well, and state which framing you trust more where
they disagree. The nine map cleanly onto those axes except for buyer access and
willingness to pay, which canon judges a genuine adaptation rather than a gap, so
a disagreement is usually that adaptation talking. Run it once the four
deliverables hold, never instead of one.

## Failure exercise

One exercise, and it lands on the corpus built in T-w06-9 rather than on a
fixture. The full body lives in
[the agent-failure set](../exercises/agent-failures.md); D-w06-3 carries the
report.

### EX-FAIL-08 — misleading code comments

- **Detection.** A comment asserts behaviour the code does not have. Detect it by having the agent state the function's behaviour twice — once from the comment alone, once from the body alone — and comparing. Two independent readings that disagree localise the defect; one reading of both together silently merges them.
- **Safe failure behaviour.** Treat the CODE as ground truth and the comment as a claim about it. Generated code inherits a comment's error faithfully, because a comment is the highest-signal text in the context window: short, declarative, and positioned exactly where the model is looking.
- **Recovery.** Flag the divergence as a finding rather than quietly preferring one side. A wrong comment is a defect in its own right and deserves its own fix; suppressing it leaves the next reader, human or agent, misled identically.
- **Logging.** Record the file, the line, the comment's claim, the code's actual behaviour, and whether the agent's first answer followed the comment. That last field is the one that turns this from an anecdote into a rate you can watch across the corpus.
- **Test proving the mitigation.** At least two issues in the Sentry corpus carry a misdescribing comment; assert the agent flags the divergence instead of reproducing the comment's claim. The test must FAIL against the pre-mitigation version handed the comment as authoritative — passing on both means it measures nothing.

## Reflection

1. Did the largest chunk configuration win on recall and lose on precision? Which
   is worse in production for this system, a missed answer or a bloated
   low-precision context?
2. Reranking reordered your top-5. Explain why it can NEVER pull in a relevant
   document from outside the retriever's candidate set, and name the failure
   where query rewriting is the only structural fix.
3. Which injection payload style worked best against your own index, and what
   ARCHITECTURAL change would eliminate that class rather than patching the
   instance?

## Evidence

- `make demo-ska-s1 && make ska-metrics` — this stage's runnable demo command.
- The per-configuration metrics table with NDCG@5, MRR and precision@5.
- Rerank latency figures p50 and p95.
- Path to the injection corpus and the attack-success-rate report.
- Path to the commit-matcher script and the 12 labelled issues.
- Path to the misleading-comments failure report.
- The scored opportunity with per-dimension evidence.

No threshold row is sited at this Sunday and no call slot is budgeted; the next
reserve is W08's. Nine sends carry the matured total from 24 to 33, and both of
next Sunday's rows read that 33: WATCH-3 trips on one reply or fewer, 53.5%
likely at the band midpoint and 91.1% at its floor; WATCH-4 trips on no booked
call at 67.6%. Both are watch rows — record them on
[the scoreboard](../SCOREBOARD.md) and change nothing, because
[phase 01](../phases/phase-01-foundations.md#checkpoints) pre-announced both as
scheduled checkpoints with their likely outcomes attached.

Log the actual hours below as a single line, planned figure first:
`Theory 2.5 / <actual> · Building 5.5 / <actual> · Testing 3.5 / <actual> ·
Discovery 3.5 / <actual>`. Four identically shaped regions per week are what the
mandated recalibration reads. Funnel counts belong on the scoreboard.

<!-- user:actuals key="W06" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- A metrics table with NDCG@5 and MRR per chunking configuration — 25
- Reranker lift measured against the frozen label set — 15
- The attack suite run against your own index, before and after — 25
- 12 Sentry issues labelled and the commit-matcher scored — 15
- One opportunity scored on all nine dimensions — 10
- The misleading-comments report carries all five named parts — 10
