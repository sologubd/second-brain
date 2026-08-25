# Track C — Production AI Application Engineering

## What these hours buy

33.5 h, 18.6% of the programme, buying five artifacts — and unusually for this
repository, most of them are numbers rather than systems.

A permission-filtered hybrid retrieval layer: lexical scoring, local embeddings
and a fusion step written by hand in about twenty lines, with an automated test
proving that the obvious post-filter silently drops results the user was
entitled to see. A frozen labelled evaluation set, built before a single
parameter is tuned, reporting NDCG@5, MRR and precision@5 per configuration. A
local cross-encoder reranker with a measured quality lift and a measured latency
cost, so the trade is stated rather than assumed. A cited-answer contract that
rejects an answer whose citation is absent from retrieved context. And a
20-task evaluation harness behind three tiers of regression gate, rerunning each
task five times against a pass-rate threshold you had to justify.

The ordering is the discipline. Freezing the label set first is what makes every
later change a diffable experiment instead of an opinion; a retrieval layer with
no frozen set behind it cannot be improved, only altered.

## Entry competency

Awareness — level one, user-supplied. It shares the programme's lowest starting
point with Track D; neither is weaker than the other, and saying so of only one
would be false. `CM-07` is explicit: the learner has never shipped lexical, vector or
hybrid search, and has never measured retrieval quality at all. Weeks 05 and 06
are genuinely from zero.

This is therefore the one track that teaches from fundamentals: give the entry
runway and do not assume the vocabulary. The three-month target on `CM-07` is
Independent implementation, a two-level jump and the most aggressive claim in
[the matrix](../reference/competency-matrix.md). It is reachable only because
W05 and W06 spend 15.5 h of Track C on one continuous build, which is why
neither week can be thinned without moving the target. `CM-08`, `CM-09` and
`CM-10` follow that build. Evidence: `D-w05-1`, `D-w05-2`, `D-w06-1`, `D-w10-1`,
`D-w10-2`, `D-w11-3`.

## Concepts

Twenty-three concepts live here. Sixteen are P0 and argued below; the remaining
seven are sequencing decisions rather than lesser ideas, and are handled after.
Each row names its priority, the week it acquires a surface, that surface, and
the deliverable standing behind it.

| Concept | Priority | Week | Surface | Proved by |
|---|---|---|---|---|
| embeddings (C-047) | P0 | W05 | a local model, EUR 0, into a pgvector table | D-w05-1 |
| semantic search (C-048) | P0 | W05 | the embedding arm of the bake-off | D-w05-1 |
| BM25 (C-049) | P0 | W05 | the lexical arm, built with `bm25s` | D-w05-1 |
| vector retrieval (C-050) | P0 | W05 | pgvector: extension, table, HNSW index | D-w05-1 |
| hybrid retrieval (C-051) | P0 | W05 | rank fusion, hand-written, k fixed at 60 | D-w05-1 |
| metadata filtering (C-052) | P0 | W05 | the permission pre-filter and its leak test | D-w05-2 |
| chunking (C-053) | P1 | W06 | a three-configuration sweep, all else held | D-w06-1 |
| reranking (C-054) | P1 | W06 | a CPU cross-encoder over hybrid's top-20 | D-w06-1 |
| query rewriting (C-055) | P1 | W06 | folded into SKA-S1 at zero extra hours | D-w06-1 |
| context construction (C-056) | P0 | W06 | ordering, citation markers, truncation | D-w11-3 |
| structured outputs (C-057) | P0 | W03 | BOA-S0's schema; the cited-answer contract | D-w11-3 |
| tools (C-058) | P0 | W01 | the retrieval tool and the CRM lookup | D-w04-2 |
| agents (C-059) | P0 | W01 | classification and proposed-action steps | D-w01-4 |
| memory (C-060) | P0 | M05 | BOA-S2's durable per-account memory | D-m05-1 |
| state (C-061) | P0 | W02 | the per-message pipeline state | D-w02-1 |
| evaluations (C-062) | P0 | W06 | the frozen pair set and the 20-task suite | D-w06-1 |
| trace evaluation (C-063) | P0 | W10 | scoring whole traces, not final strings | D-w10-2 |
| hallucination analysis (C-064) | P1 | W10 | citation presence plus a local entailment score | D-w10-2 |
| observability (C-065) | P0 | W09 | cost and latency across the answer path | D-w09-1 |
| latency (C-066) | P1 | W09 | p50/p95 rerank latency; per-stage budgets | D-w09-1 |
| cost optimization (C-067) | P0 | W09 | per-run accounting; the cost-per-task metric | D-w09-1 |
| model routing (C-068) | P1 | M04 | routing policy beside the harness comparison | D-m04-1 |
| fallbacks (C-069) | P1 | M04 | the metered path, live behind one interface | D-m04-1 |

### Retrieval, from zero

**embeddings.** What is needed is the ability to select, run and evaluate a
pretrained model as a black box with a known contract and published scores — not
to train one. Deriving contrastive loss or attention internals is low return for
this profile: the gap is systems integration, and mathematics hours come
straight out of the build-and-measure hours that would close it.

**semantic search.** Vector retrieval fails silently and specifically — on error
codes, part numbers, proper names, acronyms and negation, because an embedding
compresses those close to their opposites. A generated layer that wires up a
vector store and stops is correct in the demo and degraded on exactly the
queries real users type.

**BM25.** The baseline everything else is measured against: cheap,
deterministic, and the thing whose failures — synonymy, vocabulary mismatch —
motivate the rest of the track. Knowing *why* it exists is what makes you keep
it after adding vectors instead of deleting it as legacy.

**vector retrieval.** What matters operationally is how filtering interacts with
approximate-nearest-neighbour traversal, not how the index is built. Iterative
index scans exist precisely to fix the *returned fewer than k rows* problem —
the metadata-filtering bug reappearing one layer down, inside the index.

**hybrid retrieval.** Generated hybrid search commonly adds lexical and cosine
scores together, or normalises each independently. Both are unsound: the scales
and distributions are not comparable, so the output is silently dominated by
whichever signal had the wider numeric range that day. Fusing on rank position
sidesteps this entirely, which is why it is the default in every major engine —
though a generated implementation still needs checking for off-by-one rank
indexing and a constant hard-coded independently of corpus size.

**metadata filtering.** The correctness and security crux of the track, and the
load-bearing concept beneath Track B's rehomed multi-tenancy. Filter after the
search and the discards come out of a fixed candidate set, so a permitted
document ranked eleventh is simply gone and the query returns three results, or
none, from a corpus that holds a good match. Asked to *add access control* an
agent writes exactly that: it compiles, it passes the happy path, and it fails
precisely where it matters. The disclosure half is worse and less obvious —
timing, and how many rows come back, are both functions of records the caller
was never allowed to know about. A test asserting only that nothing forbidden
was returned catches neither half.

### Answering, and its contracts

**context construction.** How ranked chunks are assembled — order, citation
markers, truncation under a token budget — decides whether a claim can be
attributed to a source at all. Attribution is not presentation: it is the
precondition for the free hallucination check at W10 and for any security claim
about what the model was actually told.

**structured outputs.** Forcing the answer through a schema turns *cited answer*
from a prompting hope into a validated, retryable contract. The security
consequence is separate and larger: fields the schema does not declare have
nowhere to land, so a whole channel closes by construction rather than by the
model agreeing to ignore it.

**tools.** The authority-surface argument is Track A's, at
[C-003](agentic-engineering.md). An application adds one narrower point: the
tool's schema is the only contract the model has, so an under-specified argument
is a silent behaviour change no test names.

**agents.** The workflow-versus-agent boundary is Track A's, at
[C-005](agentic-engineering.md). The application-level difference is that the
question is asked per *step*: a pipeline running task, coding agent, tests,
review and pull request is mostly a workflow with an agent embedded at two
steps.

**memory.** Agent memory is not conversation history, not task state and not a
retrieval corpus, and the distinctions carry weight. History is one session's
ephemeral transcript. Task state is bookkeeping about where a pipeline is —
deterministic process state, not a belief. A corpus is written by a separate
ingestion process. Agent memory is persistent cross-session state *the agent
itself writes* and later treats as trusted fact, and that defining property is
exactly what makes it poisonable — which is why no memory surface existed here
until BOA-S2 created one.

**state.** Protocol-level session state is being retired from the interfaces
this platform touches: handshakes and session headers give way to opaque handles
passed as arguments. The pattern generalises past any one protocol — push
statefulness out of the transport into explicit, inspectable application data.
Generated code assuming a long-lived stateful connection does not survive being
run twice at once.

### Measuring it

**evaluations.** The highest-leverage concept in the track from a level-1
baseline, because it converts retrieval from taste into a discipline with a
number attached. Build the labelled set before touching chunk size, reranker
choice or fusion weights, and treat every later change as a diffable experiment
against it. Without one, *improving* retrieval is unfalsifiable — and generated
code regresses recall while looking healthy on the single demo query used to
sanity-check it.

**trace evaluation.** An agent test is a whole multi-span trace — plan, tool
calls, retries, answer — and scoring only the final string discards the part
where the generated orchestration went wrong. Two runs can produce identical
answers at wildly different cost, latency and retry behaviour, and only one is a
system you would ship.

**observability.** The epistemic argument is Track B's, at
[C-045](system-design.md). Track C's instance is narrower and mandated: cost and
latency measured across the answer path, so the knowledge agent's economics are
a record rather than an estimate.

**cost optimization.** The instructive inversion of this programme. Judge
inference is nearly free — a full pass over the evaluation load costs well under
one euro — while quota binds, because agent re-execution consumes a resource
money cannot immediately buy back. A cost model denominated in the resource that
is not scarce measures nothing, and sizing an evaluation set to a euro budget
would shrink it for no reason.

## Priorities and what is deferred

The seven P1 rows are sequencing calls. Chunking, reranking and query rewriting
sit downstream of a frozen label set, so measuring them earlier would measure
noise — and each carries an examinable boundary that is the real content. Chunk
edges bound what can *ever* be retrieved, so a boundary splitting a claim from
its qualifier is unrecoverable however good the reranker. A cross-encoder can
reorder an already-correct top-5 and can never pull in a document the retriever
did not return. Rewriting fixes the failure reranking structurally cannot,
because it changes what is retrievable rather than what is ranked. Hallucination
analysis is P1 because its two cheap methods are nearly free and its expensive
one is not: sampling for self-consistency costs full generations rather than
judge calls, and that ordering is what keeps a constrained programme from
reaching for the costly method first. Latency is P1 because it is a distribution
over a nondeterministic path, contaminated by stalls belonging to the billing
plan rather than the code. Routing and fallbacks wait for month 04 and the
second harness — and a fallback that has never executed is a hypothesis, so
keeping the metered path behind one interface means quota exhaustion exercises
it by construction.

The technology triage keeps this track narrow on purpose. Lexical scoring is
**LEARN DEEPLY**; the embedding model and the vector store are **LEARN ENOUGH TO
USE** and no more, because Postgres has been running since W02 as state store,
queue, lock and outbox, so retrieval adds an extension, a table and an index
rather than a component to operate. Deep specialisation in any one vector
database is **UNDERSTAND CONCEPT ONLY** — what transfers is how filtering meets
approximate search, and one clear published account of filtered traversal
teaches that without a second system to run. Lexical search engines are
recognition-only. Evaluation frameworks are **UNDERSTAND CONCEPT ONLY**, one
paragraph on the niche each fills, because a harness built deep gates a merge
and a four-tool survey gates nothing. Memorising tracing attribute names is
refused at `LR-18`, those conventions being actively in flux; the skill is
reading the current spec at instrumentation time and pinning the version. Model
mathematics is refused at `LR-03`.

One exclusion is a licence constraint rather than a preference. A widely
recommended multilingual reranker ships under non-commercial terms and is
excluded from every recommendation here, because this repository is
public-capable and may be used for client work. The rerankers canon does name
are permissively licensed and CPU-runnable — which is the evidence for a claim
worth stating plainly: reranking does not require paying. Paying buys marginal
quality and hosted operations, not a capability.

## How this track is proved

Track C leads six of the twelve weeks and is absent as primary from the first
four, from W08 and W09, and from W12. That is not a gap: weeks 01 to 04 build
the harness this track later instruments, and a retrieval stack laid down before
a durable state machine exists has nothing behind it.

Proof falls in three stages. `D-w05-1` and `D-w05-2` establish that retrieval
happens and that authorization runs in the right place, with a test that fails
against the naive ordering. `D-w06-1` converts the build into measurements —
metrics per configuration against a set frozen the week before, plus the rerank
lift and its latency price. `D-w10-1`, `D-w10-2` and `D-w11-3` close it: a gate
that can fail a change, traces scored as traces, and an answer that cannot cite
what it was never given.

Elsewhere by ownership: stage definitions and demo commands sit with
[the knowledge agent](../projects/secure-knowledge-agent.md), tasks and hours
with the week files, and the attack work against this same index with
[Track D](ai-security.md) — the pre-filter here and the injection suite there
are two views of one index, and only the second measures what an adversary can
do to it.
