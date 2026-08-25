# Secure Knowledge Agent

A question-answering service over a private corpus where **who is asking changes
what may be retrieved**, and where every answer is forced to cite the chunks it
stood on.

Small on purpose. Its job is to be correct, measured and attackable rather than
large. It is also where retrieval, evaluation and the AI-security work live —
building retrieval and attacking it are the same project seen twice, and the second
view is the one that decides whether the first was built properly.

Main build: **week 10** (retrieval), **week 11** (attack and trust boundary),
**months 4–6** (policy-based authorization).

## Pipeline, and why the build violates it

As the user sees it: documents → ingestion → chunk/index → hybrid retrieval →
reranking → **permission filtering** → LLM → cited answer.

Read that carefully, because the build deliberately violates it. The diagram places
permission filtering after reranking. Implemented that way it is a disclosure
vulnerability, so the actual system pulls authorization **ahead of the search**. The
diagram describes the data a user sees; it is not an execution order, and treating
it as one is the exact mistake this project exists to teach.

## Capability backlog

### 1. Permission-filtered hybrid retrieval · week 10

**Why.** Authorization inside the index is both the correctness and the security
crux, and it is the thing an agent gets wrong by default.

**Build.** BM25 lexical index first and measured on its own. Then local embeddings
in pgvector. Then Reciprocal Rank Fusion, hand-implemented in ~20 lines with k
fixed at 60. Then the **pre-filter** authorization step, ahead of the vector
search. Then reproduce the post-filter failure, and write the test that asserts
exactly k authorized results whenever k exist.

**Demo counts when.** The same query under two tenants returns two different result
sets, **and** the post-filter test fails as designed. The exit condition names a
test of the *wrong* implementation deliberately: the pre-filter is only
demonstrably better once the post-filter failure has been reproduced.

**Done.** A 15–20 pair labelled query set exists, frozen with a digest **before any
tuning**. Lexical, vector and hybrid each measured against it separately.

**Metrics.** NDCG@5 and MRR per configuration — lexical, vector, hybrid, reported
separately. Authorized results returned when k exist, pre-filter versus post-filter
— the gap is the finding.

Everything past this — reranking, chunking sweeps, citation enforcement, metadata
experiments — is capability 2 and it is Stretch. The proof week 10 owes is the
comparison against a frozen set plus the reproduced authorization failure. A
half-finished system with five techniques in it is worth less than three honest
numbers.

### 2. Chunking, reranking, metadata filters, cited answers · week 10 *(Stretch)*

**Why.** Retrieval tuned by feel degrades invisibly; retrieval tuned against a
frozen set is a diffable experiment.

**Build.** In value order: a CPU cross-encoder reranker with its lift measured
against the frozen set; a cited-answer schema that rejects an answer whose citation
is absent from the retrieved context; a chunking sweep; metadata filters. Take them
one at a time and stop when the week runs out.

**Demo counts when.** Metrics print per configuration against the frozen set, and a
deliberately unfaithful answer is rejected.

**Metrics.** Reranking lift — and what it could not fix. Rerank latency p50/p95 on
CPU. Cost per answer in tokens.

### 3. Trust boundary · week 11

**Why.** Everything retrieved here crosses a trust boundary before it reaches a
model. This project supplies the surface the security exercises attack.

**Build.** Provenance tagging at ingest, trust-tiered retrieval and a delimiter
between operator instructions and document content — all **defense in depth**,
none of them a boundary. Then the actual control: code, outside the model, that
removes the external-send tool from any turn that consumed untrusted content.

**Demo counts when.** An untrusted-input turn cannot reach an external-send tool,
and the refusal is proved to come from code by an assertion that fails when the
control is disabled. A demo where the model merely declined has demonstrated
today's model, not your system.

**Metrics.** Attack success rate per technique, per arm, with denominators. Retrieval
precision before and after — to show whether the boundary cost ordinary quality.

### 4. Policy-based authorization · months 4–6

**Why.** A policy scattered across handlers is a policy with holes.

**Build.** RBAC enforced through a **single** pre-execution check function, with
ABAC added only where a decision genuinely depends on request context. The
role-based layer carries the weight; every attribute added is another dimension the
deny-by-default fuzz has to cover.

**Demo counts when.** A role with no matching policy is denied, **and the denial came
from one function.**

**Done.** A cross-product fuzz over actions and roles allows nothing without an
explicit rule. Every new rule ships with a refusal-path assertion, not only a
permission assertion.

## Constraints

**Filter before you search, not after.** The correctness half: post-filtering runs
the ANN search first and then discards unauthorized hits from that k, so an
authorized but lower-ranked chunk is pushed out entirely and the user receives fewer
than k results — sometimes zero — from a corpus that genuinely contained a good
match. The security half is worse: **result count, latency and partial scores leak
the existence of documents the user may not see**, even when no forbidden text is
ever returned.

Ask an agent to add access control and it generates the post-filter form by default,
because that is the readable form. It compiles, it passes a happy-path test, and it
fails precisely when it matters. A test asserting only *no unauthorized content was
returned* passes over both halves — which is why the test asserts the **count**.

**Lexical first, then embeddings.** The retrieval order is the learning order. BM25
is cheap, deterministic, and its failure modes — synonymy, vocabulary mismatch — are
exactly what motivates everything built after it. Starting at the vector store
produces a system that demos well and degrades invisibly on the queries real users
type: error codes, SKUs, names, acronyms and negation, all of which embeddings
compress near their opposites.

**One store, hand-written fusion.** Vectors in pgvector beside the lexical index. No
second or third vector store operated. RRF hand-implemented, k fixed at 60, not
hand-tuned. Adding lexical and cosine scores directly, or normalising them
separately, is unsound: the two scales are incomparable, and the result is silently
dominated by whichever signal happens to have the wider numeric range that day.

**Embeddings and reranking run locally, for nothing.** A small open-weights
embedding model (~0.5–1GB on disk) and a CPU cross-encoder. **Check the licence
before the benchmark score** — one widely recommended multilingual reranker is
non-commercial and unusable here. Paying buys marginal quality and hosting
convenience, not a capability that is otherwise unavailable.

**Chunking bounds what can ever be retrieved.** A boundary that separates a claim
from its qualifier is unrecoverable downstream no matter how good the embedding or
the reranker, so the sweep runs early and against the frozen set rather than tuned
by feel. Fixed and recursive strategies are cheap deterministic defaults; semantic
chunking adds ingest cost and belongs to a second pass.

**A reranker reorders; it cannot rescue.** A cross-encoder scores query and document
together in one pass, which models their interaction directly and is far too slow to
run over a whole corpus — so it only ever sees the retriever's top-N. The examinable
consequence: reranking can lift a correct answer from position 5 to position 1, and
can never pull in a relevant document the retriever did not return at all. **Recall
is set upstream, and no amount of reranking raises it.**

**Freeze the label set before you tune.** Record a digest and a date. A metric
measured against a set that moved during tuning is a preference with a number on it.

**The corpus is untrusted input.** Everything retrieved crosses a trust boundary
before it reaches a model. This is a property of the project, not a caveat about the
security week.

## Demos, and why each is a comparison

| Capability | Its demo counts as run when |
|---|---|
| Permission-filtered retrieval | the same query under two tenants returns two different result sets, and the post-filter test fails as designed |
| Measured retrieval | metrics print per configuration against a provably frozen set |
| Trust boundary | an untrusted-input turn is refused an external-send tool, by code |
| Policy authorization | a role with no matching rule is denied, from one function |

A demo that returns plausible answers proves nothing here. Every criterion is a
**comparison** — two tenants, three configurations, an allow against a deny —
because a retrieval system with no contrast is indistinguishable from one that is
quietly broken.
