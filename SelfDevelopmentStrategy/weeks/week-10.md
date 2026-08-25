# Week 10 — Retrieval: the Secure Knowledge Agent

## Outcome

By Sunday you have a second system: question answering over a private corpus where
*who is asking changes what may be retrieved*, and retrieval quality is a measured
number — three of them, one per configuration — against a label set you froze
before you tuned anything. You have also reproduced the authorization failure that
the obvious implementation contains.

## Why now?

Three reasons this is week 10 and not week 2. It needs a database, which week 5
stood up. It needs an evaluation discipline, which week 9 built — retrieval tuned
by feel is the single most common way a demo-quality system degrades invisibly.
And week 11's security work needs a retrieval surface to attack: you cannot build
a trust boundary around retrieved content before you have retrieval.

This is also the steepest climb in the twelve weeks if you have never shipped
search. Budget accordingly, and if it overruns, carry it into week 11 rather than
compressing it.

## Build

Pipeline as the user sees it: documents → ingestion → chunk/index → hybrid
retrieval → reranking → permission filtering → LLM → cited answer.

**The build deliberately violates that order.** The diagram puts permission
filtering after reranking; implemented that way it is a disclosure vulnerability.
The diagram describes the data a user sees. It is not an execution order, and
treating it as one is the exact mistake this project exists to teach.

**Authorization must constrain the searchable candidate universe.** That is the
requirement. *How* you satisfy it is the engineering, and this is where the
common shorthand is wrong.

### What a `WHERE` clause does and does not buy you

**A SQL `WHERE tenant_id = ...` beside a vector-index scan is not automatically
pre-filtered ANN.** With a global HNSW or IVFFlat index, the planner may run the
approximate scan over the whole index first and apply your predicate to the rows
that come back. You wrote a filter that reads like a pre-filter and got
post-filter behaviour, and nothing in the query text says so — you have to read
the plan.

The failure it produces is the same one post-filtering always produces:

- *Correctness.* The ANN scan returns its top candidates from the **whole** index,
  the predicate discards the unauthorized ones, and an authorized but
  lower-ranked chunk is never considered at all. The user gets fewer than k
  results — sometimes zero — from a corpus that genuinely contained a good match.
- *Security.* Result count, latency and partial scores **leak the existence of
  documents the user may not see**, even when no forbidden text is returned.
- *Why it bites here.* Ask an agent to add access control and it emits exactly
  this shape, because it is the readable one. It compiles, it passes a happy-path
  test, and it fails precisely when it matters. A test asserting only "no
  unauthorized content was returned" passes over both halves — which is why your
  test asserts the **count**: exactly k authorized results whenever k exist.

### The five approaches to compare

There is no single correct answer, and finding out which one your data wants is
the exercise. Run the same authorized queries through each and record recall
against the frozen set, latency, and whether the guarantee is structural or
best-effort.

| Approach | How authorization constrains the candidates | Cost |
|---|---|---|
| **Global ANN + filter** | It does not, reliably — the predicate applies to what the scan already returned. The baseline you are measuring *against*. | Fast, and wrong at the tail |
| **Iterative scan** | Keep scanning the ANN index and discarding until k authorized results are found, or the scan is exhausted. Correctness improves; the guarantee is still probabilistic and the cost is unbounded when the authorized subset is sparse. | Variable, sometimes badly |
| **Exact search over the authorized subset** | Fully structural: fetch the authorized rows, then do exact nearest-neighbour over just those. Correct by construction. | Fine for small subsets, degrades with size |
| **Partial indexes** | One index per authorized partition, so the scan cannot see outside it. Structural, and only workable when the partition set is small and stable. | Index proliferation |
| **Tenant partitioning / separate tables** | Strongest separation: the unauthorized rows are not in the object being searched. | Operational overhead; wrong for fine-grained per-document ACLs |

**Read the query plan for each.** The whole lesson is that the SQL text does not
tell you which of these you got.

**Lexical first, then embeddings.** BM25 before vectors, because it is cheap,
deterministic, and its failure modes — synonymy, vocabulary mismatch — are exactly
what motivates everything built after it. Starting at the vector store produces a
system that demos well and degrades invisibly on the queries real users type: error
codes, SKUs, names, acronyms, negation — all of which embeddings compress near
their opposites.

**One store, hand-written fusion.** Vectors in pgvector beside the lexical index.
Fusion is Reciprocal Rank Fusion, hand-implemented in about twenty lines, k fixed
at 60 and not hand-tuned. Adding lexical and cosine scores directly, or
normalising them separately, is unsound: the scales are incomparable and the result
is silently dominated by whichever signal happens to have the wider numeric range
that day.

**Scope warning.** This week can absorb unlimited time. Core is the retrieval
comparison and the authorization comparison; reranking, chunking sweeps, citation enforcement and
metadata experiments are all real work and all Stretch. Getting BM25 → vector →
hybrid measured honestly against a frozen set is worth more than a half-finished
system with five techniques in it.

**Everything runs locally for nothing.** A small open-weights embedding model, and
a CPU cross-encoder reranker if you reach the Stretch item. Check the licence
before the benchmark score — one widely recommended multilingual reranker is
non-commercial and unusable.

**Chunking bounds what can ever be retrieved.** A boundary that separates a claim
from its qualifier is unrecoverable downstream no matter how good the embedding or
the reranker. Pick one sensible default now — fixed or recursive, both cheap and
deterministic — and note that the sweep is Stretch. Tuning chunking by feel is the
thing to avoid; skipping the sweep for a week is not.

## Learn

- [Pre- vs post-filtering in vector search](https://qdrant.tech/articles/vector-search-filtering/).
  The concept transfers to pgvector; the operational burden of a second store does
  not.
- [Offline evaluation metrics](https://www.pinecone.io/learn/offline-evaluation/):
  precision@k, recall@k, MRR, NDCG@k — and why rank-blind metrics let a system
  pass while its reranker buries the best answer at position five.
- Embedding and reranker model cards: parameters, disk size, benchmark mean, and
  **licence**.

~3h. Heavy week; that is expected.

## Tasks

### Core — required (~15h: 3h learning, 9h building/testing, 3h business)

The proof this week must deliver, and nothing more: **I can compare retrieval
approaches against a frozen dataset, and I can demonstrate a real
authorization/correctness failure in the naive design.**

1. **Freeze a label set first.** 15–20 labelled query/relevant-chunk pairs over a
   real corpus, frozen with a digest **before any tuning**. Do this on day one.
   Everything else this week is measured against it.
2. **Build lexical retrieval and measure it.** BM25 over the corpus. Record
   NDCG@5 and MRR against the frozen set. This is your baseline and it is the one
   step you must not skip — its failure modes are what motivate everything after.
3. **Add embeddings, then RRF fusion**, re-measuring at each step. Report per
   configuration — lexical, vector, hybrid — never as one blended number. Use one
   default chunking strategy; do not sweep yet.
4. **Reproduce the global-ANN-plus-filter failure.** Build it, read the query
   plan to confirm the predicate is applied after the scan, and show it silently
   returning fewer authorized results than exist. This is the baseline, and the
   structural approaches are only *demonstrably* better once it has been
   reproduced. **This is the week's second headline and it is not optional.**
5. **Compare at least two more approaches from the table** against it — one of
   iterative scan, exact search over the authorized subset, partial indexes, or
   tenant partitioning, plus whichever second one suits your data. Record recall,
   latency, and whether each guarantee is structural or best-effort. Then write
   the test asserting your chosen approach returns exactly k authorized results
   whenever k exist.
6. **Business: assemble the pain register.** Every pain you have heard or inferred,
   scored, with an evidence tag per row. Instructions in
   [consulting-and-saas.md](../business/consulting-and-saas.md).

### Stretch — only after Core is DONE

Ranked by value. Each is genuinely worth doing; none of them is needed to claim
the capability above, and all of them together are another full week.

- **Add a reranker** and measure the lift against the frozen set, with p50/p95
  latency on CPU. The single most valuable item here — and remember what it cannot
  do: reranking can lift a correct answer from position 5 to position 1 and can
  never pull in a document the retriever did not return. Recall is set upstream.
- **Force cited answers by schema**: an answer whose citation is absent from
  retrieved context is rejected, proved against a deliberately unfaithful fixture.
  Cheap to build, and week 11 will want it — but week 11 can also build it.
- **Sweep chunking strategies** against the frozen set. Fixed versus recursive
  first; semantic chunking adds ingest cost and belongs to a third pass. Worth
  doing eventually because a boundary that separates a claim from its qualifier is
  unrecoverable downstream — but a single sensible default does not block the
  comparison Core is about.
- **Metadata filters** beyond what authorization already needs.
- **Stale-document handling** — provenance timestamps, trust-tier demotion, and an
  answer that presents an old chunk *with its age*. This is the failure exercise
  below; run it if the week allows, and carry it to week 11 if not.
- **Re-score the week-6 opportunity** from the recorded evidence alone, originals
  covered, classifying every movement as new evidence or scorer drift.

## Use it for real

A real corpus — your own documentation, notes, or a real project's docs — and at
least two tenants or roles with genuinely different entitlements. A single-tenant
demo cannot exhibit the defect this week is about.

## Measure

- NDCG@5 and MRR, **per configuration** — lexical, vector, hybrid — against the
  frozen set. Three numbers side by side is the deliverable.
- Authorized results returned when k exist, **per approach**. The gap between
  global-ANN-plus-filter and the structural options is the finding.
- Latency per approach, and whether each guarantee is structural or best-effort.
- Cost per answer, in tokens.
- *(Stretch)* Reranking lift, and what it could not fix because recall was already
  lost. Rerank latency p50/p95 on CPU.

## Failure exercise

Run this if Core finished with room. If not, carry it into week 11 — an honest
carry beats a rushed five-part write-up.

**Stale documentation.** Stop retrieval ranking a year-old document like a current
one, and make the answer admit when it could not tell.

- **Detection.** At retrieval, compare each chunk's provenance timestamp against
  the modification time of whatever it describes. A document materially older than
  its subject is a candidate; so is one contradicting the current source.
  Staleness comes from provenance, never from an impression of writing style.
- **Safe failure.** Pass staleness up as its own signal instead of ranking normally
  and hoping. An agent that cannot separate current from obsolete states the
  obsolete version with identical confidence, and the confidence does the damage.
- **Recovery.** Push stale chunks down by trust tier. Where an answer genuinely
  rests on one, present it *with its age* so a person can weigh it. **Silently
  suppressing an old document fails this exercise rather than satisfying it.**
- **Logging.** Chunk id, its age, the age of what it describes, and whether the
  answer leaned on it. That fourth field converts an index statistic into a measure
  of real harm.
- **Proving test.** A corpus holding one deliberately obsolete document yields an
  answer that either avoids it or presents it with its age. **Relevance-only
  ranking breaks that assertion and states the obsolete claim flatly.**

## Deliverables

- [ ] Frozen 15–20 pair label set with a digest, dated before any tuning.
- [ ] Lexical baseline with metrics; vector; hybrid with RRF — metrics reported per
      configuration.
- [ ] The reproduced global-ANN-plus-filter failure, with the query plan showing
      the predicate applied after the scan.
- [ ] At least three approaches compared on recall, latency and guarantee kind,
      with the chosen one implemented and its exactly-k test.
- [ ] Pain register with per-row evidence tags.
- [ ] *(Stretch, if reached)* reranking with measured lift and latency;
      cited-answer schema; chunking sweep; stale-documentation report.

## Done when

- [ ] The same query under two tenants returns two different result sets.
- [ ] NDCG@5 and MRR are reported for lexical, vector and hybrid separately,
      against a set provably frozen before the first tuning change.
- [ ] The global-ANN-plus-filter failure is **reproducible**, evidenced by the
      query plan rather than by assumption.
- [ ] At least three approaches are compared, and a test asserts the chosen one
      returns exactly k authorized results whenever k exist.
- [ ] The write-up says which guarantees are structural and which are best-effort;
      nothing equates a SQL `WHERE` with pre-filtered ANN.
- [ ] The label set's digest and freeze date are recorded, and no tuning change
      predates them.
- [ ] The pain register exists with an evidence tag on every row.

## Reflection

1. Which queries did lexical get right and hybrid get wrong? What does that say
   about the fusion?
2. Before you measured, which configuration did you expect to win? What did the
   frozen set say instead?
3. The broken version passes a test asserting "no unauthorized content was
   returned". Which other tests in your codebase pass for a similarly wrong
   reason?
4. Which approach did you choose, and at what corpus size or ACL granularity would
   you have to change it?

## Evidence

- Frozen label set, its digest and freeze date.
- Metrics table: lexical, vector, hybrid, side by side.
- The global-ANN-plus-filter reproduction, with its query plan.
- The approach comparison table, and the exactly-k test for the chosen one.
- Pain register.
- Anything from Stretch that was actually reached, and a note of what was not.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
