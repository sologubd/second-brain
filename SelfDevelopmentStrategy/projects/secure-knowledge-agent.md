# Secure Knowledge Agent

## What it is

`PRJ-02`. A question-answering service over a private corpus where **who is
asking changes what may be retrieved**, and where every answer is forced to cite
the chunks it stood on. Three stages, not thirteen: this is a secondary project
and its job is to be correct, measured and attackable rather than large.

It is also the programme's steepest climb. The learner's retrieval competency is
recorded as awareness — never having shipped lexical, vector or hybrid search,
and never having measured retrieval quality at all — so weeks 05 and 06 start
from zero vocabulary rather than from a refresher. Budget accordingly; W05 is
flagged in canon as the week most likely to overrun.

Two other projects depend on it. `S7a` cannot enter until `SKA-S1` exits, because
you cannot build a trust boundary around retrieved content before you have
retrieval. And the second supplied bad system in
[the review set](../exercises/architecture-reviews.md) is deliberately shaped
like this project's own worst version — recognising in a stranger's code the
mistake you were shown in your own is a different and harder skill than avoiding
it once.

The retrieval order is also the learning order. Lexical search comes first,
before embeddings, because it is cheap, deterministic, and its failure modes —
synonymy and vocabulary mismatch — are precisely what motivates everything built
after it. Starting at the vector store instead produces a system that demos well
and degrades invisibly on the exact-match queries real users type: error codes,
SKUs, names, acronyms and negation, all of which embeddings compress near their
opposites.

## Pipeline

Eight stages, in canon's order: documents → ingestion → chunk/index → hybrid
retrieval → reranking → permission filtering → LLM → cited answer.

Read that order carefully, because **the build deliberately violates it.** The
diagram places permission filtering after reranking. Implemented that way it is a
disclosure vulnerability, so the actual system pulls authorization forward, ahead
of the vector search. The diagram describes the data a user sees; it is not an
execution order, and treating it as one is the exact mistake the project exists
to teach.

Six things the project must carry, each with a home:

| Must include | Where it is proved |
|---|---|
| real evaluation dataset | `D-w05-1` — 15–20 labelled pairs, frozen before tuning |
| retrieval metrics | `D-w06-1` — NDCG@5, MRR, precision@5 per configuration |
| authorization | `D-w05-2` — the pre-filter build and its leak-proof test |
| prompt-injection tests | `D-w06-2` and `D-w11-2` |
| observability | `D-w09-1` — spans over retrieval and answer generation |
| cost and latency | `D-w06-1` p50/p95 rerank latency; `D-w09-1` cost per answer |

## Stages

### SKA-S0 — permission-filtered hybrid retrieval (W05)

- **Entry.** Postgres is running from W02 and a document corpus exists.
- **Exit.** Hybrid BM25-plus-embedding retrieval with a PRE-FILTER authorization step, and an automated test proving post-filter silently drops authorized results.
- **Demo.** `make demo-ska-s0 QUERY='...' TENANT=a`
- **Adds** hybrid retrieval and permission filtering. **Ceilings:** EUR 0.0, at most 20 runs.

The exit condition is unusual in naming a test of the *wrong* implementation. That
is deliberate: the pre-filter is only demonstrably better if the post-filter
failure has been reproduced first.

### SKA-S1 — chunking, reranking, metadata filters, cited answers (W06)

- **Entry.** SKA-S0 exits.
- **Exit.** A measured NDCG@5 and MRR per configuration against the frozen label set, plus a schema-forced cited answer.
- **Demo.** `make demo-ska-s1 && make ska-metrics`
- **Adds** chunk/index, reranking and cited answer. **Ceilings:** EUR 0.0, at most 60 runs.

This stage extends SKA-S0 rather than replacing it. The label set is frozen
*before* any tuning, which is what makes the three-configuration sweep a
measurement instead of a preference.

### SKA-S2 — tenant isolation and policy-based authorization (M04–M06)

- **Entry.** SKA-S1 and `S7a` exit.
- **Exit.** RBAC enforced through a single pre-execution check function, with ABAC only where a context-dependent rule is genuinely needed.
- **Demo.** `make demo-ska-s2-authz`
- **Adds** authorization. **Ceilings:** EUR 0.0, at most 30 runs.

One check function, not a check per call site. A policy scattered across handlers
is a policy with holes, and `DC-13` is the defect class that names them. The
role-based layer carries the weight; attribute-based rules are added only where a
decision genuinely depends on request context, because every attribute added is
another dimension the deny-by-default fuzz has to cover.

## Capabilities gained

| Capability | Stage first delivering it |
|---|---|
| hybrid retrieval | SKA-S0 |
| permission filtering | SKA-S0 |
| chunk/index | SKA-S1 |
| reranking | SKA-S1 |
| cited answer | SKA-S1 |
| authorization | SKA-S2 |

Ingestion, the LLM call and the documents themselves are pipeline positions
rather than capabilities: they exist from the first day and gain nothing across
the three stages. Canon lists six capabilities against eight pipeline steps for
that reason, and the gap is not an omission.

## Runnable demos

| Stage | Its demo counts as run when |
|---|---|
| SKA-S0 | the same query under two tenants returns two different result sets, and the post-filter test fails as designed |
| SKA-S1 | `make ska-metrics` prints NDCG@5 and MRR per configuration against the frozen set |
| SKA-S2 | a role with no matching policy is denied, and the denial came from one function |

A demo that returns plausible answers proves nothing here. Each criterion is a
comparison — two tenants, three configurations, or an allow against a deny —
because a retrieval system with no contrast is indistinguishable from a system
that is quietly broken.

## Constraints

**Filter before you search, not after.** This is the correctness and security
crux of the whole project. Post-filtering runs the approximate-nearest-neighbour
search first and then discards unauthorized hits from that k, so an authorized
but lower-ranked chunk is pushed out entirely and the user receives fewer than k
results — sometimes zero — from a corpus that genuinely contained a good match.
That is the correctness half. The security half is worse: **result count, latency
and partial scores leak the existence of documents the user may not see**, even
when no forbidden text is ever returned. An agent asked to add access control
generates the post-filter form by default, because it is the readable form; it
compiles, it passes a happy-path test, and it fails precisely when it matters.
A test asserting only that no unauthorized content was returned passes over both
halves, which is why the W05 test asserts the *count* instead: exactly k
authorized results whenever k exist.

**Embeddings run locally at EUR 0.** The primary model is
Qwen3-Embedding-0.6B — Apache-2.0, 0.6B parameters, about 1.5GB on disk, with a
multilingual MTEB mean of 64.33. Documented alternates are nomic-embed-text
(roughly 0.3GB via Ollama, the easiest single-command start, lower MTEB),
BAAI/bge-m3, and gte-multilingual-base. Reranking is likewise unpaid: a CPU
cross-encoder is the primary path, and paying buys marginal quality and hosting
convenience rather than a capability that is otherwise unavailable.

**One store, hand-written fusion.** Vectors live in pgvector beside the lexical
index, and no second or third vector store is operated. Qdrant is read once, at
concept level, for the clearest published account of pre-filtering done properly
at the ANN layer — the concept transfers to pgvector; the operational burden does
not. Fusion is Reciprocal Rank Fusion, hand-implemented in roughly twenty lines
with k fixed at 60 and not hand-tuned. Adding lexical and cosine scores directly,
or normalising them separately, is unsound: the two scales are incomparable, and
the result is silently dominated by whichever signal happens to have the wider
numeric range that day.

**Chunking bounds what can ever be retrieved.** A boundary that separates a claim
from its qualifier is unrecoverable downstream no matter how good the embedding
or the reranker is, so the chunking sweep is run early and against the frozen set
rather than tuned by feel. Fixed and recursive strategies are cheap deterministic
defaults; semantic chunking adds ingest cost and belongs to a second pass.

**A reranker reorders; it cannot rescue.** A cross-encoder scores query and
document together in one pass rather than encoding each independently, which
models their interaction directly and is far too slow to run over a whole corpus.
It therefore only ever sees the retriever's top-N. The examinable consequence is
that reranking can lift a correct answer from position 5 to position 1, and can
never pull in a relevant document the retriever did not return at all. Recall is
set upstream, and no amount of reranking raises it.

**The corpus is untrusted input.** Everything retrieved here crosses a trust
boundary before it reaches a model, and this project supplies the surface that
[the security exercises](../exercises/ai-security.md) attack — first as corpus
poisoning in W06, then as indirect injection and exfiltration in W11. Building
retrieval and attacking it are the same project seen twice, and the second view is
the one that decides whether the first was built properly.
