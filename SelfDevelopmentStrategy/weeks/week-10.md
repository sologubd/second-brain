# Week 10 — Retrieval: the Secure Knowledge Agent

## Outcome

By Sunday you have a second system: question answering over a private corpus where
*who is asking changes what may be retrieved*, every answer cites the chunks it
stood on, and retrieval quality is a measured number against a label set you froze
before you tuned anything.

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
filtering after reranking; implemented that way it is a disclosure vulnerability,
so authorization moves *ahead of the search*. The diagram describes the data a
user sees. It is not an execution order, and treating it as one is the exact
mistake this project exists to teach.

**Filter before you search, not after.** This is the correctness and security crux
of the whole project:

- *Correctness.* Post-filtering runs the approximate-nearest-neighbour search
  first and then discards unauthorized hits from that k. An authorized but
  lower-ranked chunk gets pushed out entirely, and the user receives fewer than k
  results — sometimes zero — from a corpus that genuinely contained a good match.
- *Security.* Worse: result count, latency and partial scores **leak the existence
  of documents the user may not see**, even when no forbidden text is ever
  returned.
- *Why it matters here.* Ask an agent to add access control and it generates the
  post-filter form by default, because that is the readable form. It compiles, it
  passes a happy-path test, and it fails precisely when it matters. And a test
  asserting only "no unauthorized content was returned" passes over both halves —
  which is why your test asserts the **count**: exactly k authorized results
  whenever k exist.

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

**Everything runs locally for nothing.** A small open-weights embedding model and a
CPU cross-encoder reranker. Check the licence before the benchmark score — one
widely recommended multilingual reranker is non-commercial and unusable.

**A reranker reorders; it cannot rescue.** A cross-encoder scores query and
document together in one pass, which models their interaction directly and is far
too slow to run over a whole corpus — so it only ever sees the retriever's top-N.
The examinable consequence: reranking can lift a correct answer from position 5 to
position 1, and can never pull in a relevant document the retriever did not return
at all. **Recall is set upstream.**

**Chunking bounds what can ever be retrieved.** A boundary that separates a claim
from its qualifier is unrecoverable downstream no matter how good the embedding or
the reranker. So sweep chunking early, against the frozen set, rather than tuning
it by feel. Fixed and recursive strategies are cheap deterministic defaults;
semantic chunking adds ingest cost and belongs to a second pass.

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

1. **Freeze a label set first.** 15–20 labelled query/relevant-chunk pairs over a
   real corpus, frozen with a digest **before any tuning**. Do this on day one.
   Everything else this week is measured against it.
2. **Build lexical retrieval and measure it.** BM25 over the corpus. Record
   NDCG@5, MRR and precision@5 against the frozen set. This is your baseline and
   it should not be skipped.
3. **Add embeddings and RRF fusion**, and re-measure. Report per configuration —
   lexical, vector, hybrid — never as one blended number.
4. **Build the pre-filter authorization.** Authorization ahead of the search.
5. **Reproduce the post-filter failure.** Build the wrong version, show it silently
   returning fewer authorized results than exist, then write the test asserting the
   pre-filter returns exactly k when k exist. The pre-filter is only *demonstrably*
   better once the post-filter failure has been reproduced.
6. **Add chunking sweep, reranking and metadata filters**, measuring each against
   the frozen set. Record rerank latency, p50 and p95.
7. **Force cited answers by schema.** An answer whose citation is absent from the
   retrieved context is rejected — proved against a deliberately unfaithful
   fixture.
8. **Business: assemble the pain register.** Every pain you have heard or inferred,
   scored, with an evidence tag per row. Then re-score the week-6 opportunity from
   the recorded evidence alone, without looking at the original scores, and account
   for every dimension that moved as *new evidence* or *scorer drift*. Instructions
   in [consulting-and-saas.md](../business/consulting-and-saas.md).

## Use it for real

A real corpus — your own documentation, notes, or a real project's docs — and at
least two tenants or roles with genuinely different entitlements. A single-tenant
demo cannot exhibit the defect this week is about.

## Measure

- NDCG@5, MRR and precision@5, **per configuration**, against the frozen set.
- Reranking lift: position change for known-relevant chunks, and what it could
  not fix because recall was already lost.
- Rerank latency p50 and p95, on CPU.
- Pre-filter versus post-filter: authorized results returned when k exist, for
  both. The gap is the finding.
- Cost per answer, in tokens.

## Failure exercise

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
- [ ] Lexical baseline with metrics; hybrid retrieval with RRF; metrics per
      configuration.
- [ ] Pre-filter authorization, plus the reproduced post-filter failure and the
      exactly-k test.
- [ ] Chunking sweep, reranking, metadata filters — each measured against the
      frozen set, with rerank latency.
- [ ] Cited-answer schema, with rejection proved against an unfaithful fixture.
- [ ] Stale-documentation report, five parts, proving test red against
      relevance-only ranking.
- [ ] Pain register with per-row evidence tags; week-6 opportunity re-scored with
      every movement classified.

## Done when

- [ ] The same query under two tenants returns two different result sets.
- [ ] NDCG@5 and MRR are reported per configuration against a set provably frozen
      before the first tuning change.
- [ ] The post-filter failure is reproducible, and a test asserts the pre-filter
      returns exactly k authorized results whenever k exist.
- [ ] An answer citing a chunk absent from retrieved context is rejected.
- [ ] 100% of retrieved chunks carry a provenance timestamp, and an answer resting
      on a stale chunk presents its age.
- [ ] Every dimension that moved in the re-score names its cause as new evidence or
      scorer drift, with zero movements unclassified.

## Reflection

1. Which failed queries did lexical get right and hybrid get wrong? What does that
   say about the fusion?
2. What is the oldest document your index would still rank first?
3. In the re-score: which dimension's *wording* caused the drift, and how would you
   rewrite it so the next reader cannot take it two ways?

## Evidence

- Frozen label set, its digest and freeze date.
- Metrics table per configuration; rerank latency figures.
- The post-filter reproduction and the exactly-k test.
- Cited-answer rejection test.
- Stale-documentation report and its red-on-parent test.
- Pain register; the two scorings and their comparison.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
