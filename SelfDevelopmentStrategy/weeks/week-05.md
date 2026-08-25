# Week 05 — Retrieval from zero, with authorization in the index

## Outcome

By Sunday the Secure Knowledge Agent answers from a hybrid index that filters by
permission BEFORE ranking, and I have an automated test proving the naive
alternative silently drops results the user was entitled to see.

## Time budget

- Theory: 3.5 h
- Building: 6.0 h
- Testing/evaluation: 2.5 h
- Customer discovery: 3.0 h

Canon calls this the highest-risk week in the programme, and the reason is the
starting point, not the size. USI-08 records the retrieval baseline as
Awareness: no BM25, vector or hybrid search ever shipped, no retrieval quality
ever measured. Nine hours of Track C run from zero, in a week also carrying
3.0 h of Track A. Fundamentals are the right pitch here, and this is the only
week where that is true. Theory sits exactly on the 3.5 h cap with no headroom:
move half an hour of building into that bucket and the week breaks the cap.
T-w05-1, T-w05-2, T-w05-3 and T-w05-8 are theory because reading and writing is
all they are, not because the bucket had room.

Check the W02 dependency before Monday. Canon declares it hard and the costing
rests on it: pgvector is priced at 0.5 h — an extension, a table and an index on
the Postgres instance running as the task state store since W02 — not the 2.5 h
a first-time database setup absorbs. If Postgres is not already up, that premise
fails and the week runs about two hours heavier with no slack. The independent
bottom-up estimate is 8.0 h against the 9.0 h Track C allocation, leaving 1.0 h
of slack in the week that estimate called tightest. Ceilings are EUR 0.00 of
metered spend and 20 agent runs; canon's reason for a count that low is that
retrieval evaluation consumes none of it, the metrics being deterministic, and
embeddings run locally at EUR 0.

Compressed week, 8.0 h: T-w05-4, T-w05-5, T-w05-7, and the discovery block of
T-w05-11, T-w05-12 and T-w05-13 whole at 3.0 h — then slip the calendar instead
of doubling up. T-w05-13 stays whole because it is the call slot, and a call has
calendar lead time that working faster cannot compress. The cut order above that
subset is fixed: hold k at 60 rather than tuning it, and stand up no second store
to compare against. T-w05-1, T-w05-2 and T-w05-3, T-w05-6's write-up, and
T-w05-8, T-w05-9 and T-w05-10 defer to [week 06](week-06.md). The permission
pre-filter is never cut. D-w05-3 ticks; D-w05-1 carries without its bake-off
write-up, D-w05-2 without its written pre-versus-post argument, D-w05-4 whole.
DONE-COMPRESSED, not DONE.

## Topics

| Topic | Track | Priority | Where it surfaces this week |
|---|---|---|---|
| BM25 | C | P0 | T-w05-4 → D-w05-1 |
| embeddings | C | P0 | T-w05-5 → D-w05-1 |
| semantic search | C | P0 | the embedding-only arm of T-w05-6 → D-w05-1 |
| vector retrieval | C | P0 | T-w05-5's pgvector table and HNSW index → SKA-S0 |
| hybrid retrieval | C | P0 | T-w05-3, then T-w05-6 → D-w05-1 |
| metadata filtering | C | P0 | T-w05-7 → D-w05-2 |
| multi-tenancy | B | P0 | T-w05-7's two-tenant index → D-w05-2 |
| tenant isolation | D | P0 | T-w05-2, then T-w05-7 → D-w05-2 |
| outreach | E | P0 | T-w05-11 and T-w05-12 → D-w05-3 |
| discovery calls | E | P0 | T-w05-13 → D-w05-3 |

Every row resolves to a canon concept carrying P0, so none needs the earn-it or
competency fallback — but the reasoning is not all in one place. The first six
rows belong to [Track C](../tracks/ai-application-engineering.md).
Multi-tenancy is a [Track B](../tracks/system-design.md) concept rehomed onto
this project rather than the platform, which is why an authorization surface
appears in a retrieval week; tenant isolation shares that surface from
[Track D](../tracks/ai-security.md). Discovery calls are
[Track E](../tracks/consulting.md); outreach is homed in
[the outreach file](../business/outreach.md), not in its track. The three Track
A tasks reason from [Track A](../tracks/agentic-engineering.md), and the send
and call tasks reinforce [Track F](../tracks/micro-saas.md). SKA-S0 — entry,
exit and demo command — belongs to
[the Secure Knowledge Agent](../projects/secure-knowledge-agent.md). This file
owns tasks, hours and acceptance.

## Tasks

### Task 1

`T-w05-1` — 1.0 h, Track C, theory. Reading: `RES-07`. Lexical against
semantic matching: why BM25 survives the arrival of vectors, and the exact
query classes on which embeddings fail silently — error codes, SKUs, names,
acronyms, negation. Write that list down first; the bake-off is read against
it.

### Task 2

`T-w05-2` — 1.0 h, Track C, theory, reinforcing D. Reading: `RES-06`.
Pre-filter against post-filter authorization. Post-filtering is a correctness
bug and a disclosure vulnerability at once, and the second is the easy one to
miss: name the observables — result count, latency, error shape — that leak
the existence of a document the asker may not see.

### Task 3

`T-w05-3` — 0.5 h, Track C, theory. Reading: `RES-07`. Reciprocal Rank Fusion:
why fusing on rank needs no score normalisation between two systems whose
scores mean unrelated things, and what an off-by-one in rank indexing, or a
corpus-independent k, does to the ordering.

### Task 4

`T-w05-4` — 1.5 h, Track C, building. Build the BM25 baseline over a real
corpus of roughly 30 to 40 documents with bm25s, and hand-label 15 to 20 query
and relevant-document pairs before any tuning. Tokenizer defaults and setup
friction are where the hour goes.

### Task 5

`T-w05-5` — 1.5 h, Track C, building. Smoke-test Qwen3-Embedding-0.6B on the
actual laptop, embed the corpus, then add the pgvector extension, its table
and an HNSW index to the Postgres running since W02. Smoke-test first: a model
that will not load here is better found in minute five than hour two.

### Task 6

`T-w05-6` — 1.5 h, Track C, building. Hand-implement RRF in about twenty lines
with k fixed at 60, then run the three-way bake-off — lexical only, embedding
only, hybrid — against the labelled set. Writing those lines is the point; a
library call hides the rank arithmetic T-w05-3 just covered.

### Task 7

`T-w05-7` — 2.0 h, Track C, testing, reinforcing D. Build the permission
pre-filter and prove the leak. Construct a two-tenant index and a query whose
raw top-k holds more of tenant B's documents than tenant A's, so
post-filtering demonstrably returns fewer than k authorized results. This is
the week's irreplaceable build: the authorization surface rehomed here, and
the whole security story of the Secure Knowledge Agent.

### Task 8

`T-w05-8` — 1.0 h, Track A, theory, reinforcing C. Reading: `RES-03`. Stale
retrieved context as an agent failure mode: an out-of-date document misleads
an agent with no way of knowing it is out of date. Settle the detection signal
in writing before EX-FAIL-07 asks for it.

### Task 9

`T-w05-9` — 1.5 h, Track A, building, reinforcing C and D. Build the SKA
ingest path: a document loader plus the metadata and permission schema every
chunk carries. Without that permission field, T-w05-7's pre-filter has nothing
to filter on.

### Task 10

`T-w05-10` — 0.5 h, Track A, testing. Run the stale-documentation exercise
against the SKA and write the five-part report.

### Task 11

`T-w05-11` — 0.8 h, Track E, business, reinforcing F. Send 9 cold emails
drafted with BOA-S0 assistance, each reviewed and approved before it leaves.
These open the 37 assisted sends among the programme's 52.

### Task 12

`T-w05-12` — 0.45 h, Track E, business. Send 10 follow-ups. Between 42% and
65% of replies arrive on a follow-up rather than a first touch — the funnel
model's best-evidenced figure — so each has to carry new information.

### Task 13

`T-w05-13` — 1.75 h, Track E, business, reinforcing F. The discovery-call slot
at the full all-in rate: 30 minutes of preparation, a 45-minute call, 30
minutes of notes. WATCH-2 trips this Sunday if no call is booked against 15
matured sends — 83.7% likely at the band midpoint, still 65.7% at the ceiling.
It is expected to trip. Log it to [the scoreboard](../SCOREBOARD.md) and
change nothing; it was pre-announced in [phase
01](../phases/phase-01-foundations.md#checkpoints) as a scheduled checkpoint,
and zero calls is the programme's modal result at 53.9%. Expected calls
attributable to this week's 9 sends are 0.107. With no call, the slot runs a
Stage-1 simulated interview against the W03 rehearsal target from [the
interview template](../templates/discovery-interview.md), tagged
`evidence_source: simulated` — a passing deliverable — and the leftover time
is logged as slack, never quietly re-spent.

## Deliverables

- [ ] D-w05-1 — SKA-S0: a permission-aware hybrid index over a real corpus — bm25s lexical, local Qwen3 embeddings in pgvector, hand-implemented RRF — with a 15–20 pair labelled query set frozen before any tuning — at `agentplat/ska/`, `evals/ska-labels.frozen.jsonl`, `evals/ska-labels.frozen.sha256`
- [ ] D-w05-2 — Permission-filter correctness and leak report: a reproducible failing post-filter case, the pre-filter fix, an automated test asserting pre-filter always returns exactly k authorized results when k exist, and a latency comparison — at `docs/w05/permission-filter-report.md`, `tests/test_prefilter_k.py`
- [ ] D-w05-3 — 9 assisted sends and 10 follow-ups logged, plus the call slot outcome recorded with `evidence_source` — at `send-log.local.md`, `discovery-notes.local.md`
- [ ] D-w05-4 — Combined failure report — stale documentation misleads the agent — with all five parts — at `docs/w05/stale-documentation-report.md`

## Acceptance criteria

- [ ] AC-w05-1a — all three retrieval strategies run against the SAME labelled query set, and precision@5, recall@5, MRR and NDCG@5 are computed per strategy (T-w05-4, T-w05-6)
- [ ] AC-w05-1b — hybrid beats at least one single signal on at least one metric, or the write-up explains why not and what that says about the chosen k; the same write-up names the query classes where the embedding arm failed silently, the embedding model and store the semantic arm ran on, and the permission and metadata fields every ingested chunk carried (T-w05-6, T-w05-1, T-w05-3, T-w05-5, T-w05-9)
- [ ] AC-w05-1c — the labelled set was frozen before the first tuning change, proved by `evals/ska-labels.frozen.sha256` holding the digest and ISO freeze date and still matching `evals/ska-labels.frozen.jsonl` when the metrics are read — not by commit history, which this repo does not have (T-w05-4)
- [ ] AC-w05-2a — a failing before-case exists in which post-filter returns fewer than k authorized results for a query where k authorized documents demonstrably exist (T-w05-7)
- [ ] AC-w05-2b — an automated test asserts that pre-filter always returns exactly k authorized results when k exist, and it fails against the post-filter implementation (T-w05-7)
- [ ] AC-w05-2c — the report names at least one observable — result count, latency or error shape — that leaks the existence of a document the user cannot see, and states why a test checking only that no unauthorized content was returned misses it (T-w05-2, T-w05-7)
- [ ] AC-w05-3a — 9 sends and 10 follow-ups are logged in SCOREBOARD with per-touch attribution, every business artifact carries `evidence_source` as real or simulated, and the call slot's outcome is logged there too — a booked call, or the simulated interview note with the unspent hours recorded as slack (T-w05-11, T-w05-12, T-w05-13)
- [ ] AC-w05-4a — the stale-documentation report contains all five named sections, its proving test fails against the pre-mitigation code, and its detection section states the signal T-w05-8 settled — chunk provenance against the referenced artifact's age — rather than an unexplained heuristic (T-w05-10, T-w05-8)

## Stretch goal

Outside the 15 hours. Rerun the bake-off against a hierarchical permission model
— team above user — in place of a flat tenant identifier, and check whether the
post-filter leak gets easier or harder to demonstrate. A hierarchy is where
pre-filtering stops being one equality predicate, which is what makes it the
honest next question. Attempt it only once all four deliverables hold.

## Failure exercise

One exercise, and it sits on the seam between the index being built here and the
agent that will read from it. Its full body lives in
[the agent-failure set](../exercises/agent-failures.md); D-w05-4 is the report.

### EX-FAIL-07 — stale documentation

- **Detection.** A retrieved document's last-modified date is materially older than the code it describes, or its claims contradict the current source. The check runs at retrieval time, comparing each chunk's provenance timestamp against the mtime of the artifact it refers to — staleness computed, not sensed.
- **Safe failure behaviour.** Surface staleness to the answer layer as a first-class signal instead of ranking the document normally and saying nothing. An agent that cannot tell fresh from stale asserts the stale version confidently, and the confidence does the damage.
- **Recovery.** Down-weight stale chunks by trust tier, and where an answer genuinely rests on one, cite it with its age so a human can judge whether the age matters for this question.
- **Logging.** Record the chunk id, its age, the referenced artifact's age, and whether the answer relied on that chunk. Those four fields make staleness countable across a corpus instead of arguable one document at a time.
- **Test proving the mitigation.** A corpus holding one deliberately outdated document yields an answer that either avoids that document or cites it with its age. The test fails against a version ranking purely on relevance — which is what SKA-S0 is until this exercise lands.

## Reflection

1. What observable — result count, latency, error shape — reveals that a
   document exists which the user cannot see? Would a test checking only 'no
   unauthorized content was returned' have caught it?
2. Which queries did BM25 win outright, and what do those queries share? What
   does that predict about the questions real users will ask?
3. You froze the label set before tuning. What would you have concluded this week
   if you had not — and would you have been able to tell that you were wrong?

## Evidence

- `make demo-ska-s0 QUERY='...' TENANT=a` — this stage's runnable demo command — plus a path to the index build and the frozen label set.
- The three-way metrics table.
- The failing post-filter case and the passing pre-filter test.
- Path to the leak report, and to the stale-documentation failure report.
- Send log entries, and the call or fallback note with its `evidence_source`.

Log actual hours below as one line, planned first:
`Theory 3.5 / <actual> · Building 6.0 / <actual> · Testing 2.5 / <actual> ·
Discovery 3.0 / <actual>`. The mandated hour recalibration reads these four
regions per bucket, so a week logged as freeform prose cannot be read and a week
never logged cannot be corrected. Funnel counts belong in
[the scoreboard](../SCOREBOARD.md) rather than here.

<!-- user:actuals key="W05" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

- The hybrid index answers end to end over a real corpus — 25
- The labelled set was frozen before the first tuning change — 15
- The permission pre-filter is built and sits in the query path — 25
- The leak-proof test fails on post-filter and passes on pre-filter — 15
- The stale-documentation report carries all five named parts — 10
- 9 sends and 10 follow-ups logged, with the call slot's outcome — 10
