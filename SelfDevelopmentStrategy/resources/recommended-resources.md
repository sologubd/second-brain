# Recommended resources — fifteen, and why each one

## How to use this list

Fifteen items, three of them books; the rest primary documentation, papers,
model cards and two short essays. Fifteen tops a 12–15 band and is deliberately
small, because a fifty-book list signals reading rather than building and nobody
finishes it.

Every entry carries the same four fields, and the last two matter most: naming
the project that consumes a resource stops it becoming background reading, and
naming the exercise that proves it makes comprehension checkable. A resource
with no exercise behind it has been visited, not learned.

Each also opens with an address. Every theory task in the twelve weeks cites a
`RES-` id, so an id resolving to a title and nothing else would leave the finding
to the reader. Two entries give a search rather than a permalink and say why: an
identifier this repository has not verified is one it does not print.

Read in the order the weeks need them. Anything whose state could change mid-
programme keeps its dated claim in
[the snapshot](ecosystem-snapshot-2026-08.md), so this list stays durable while
the volatile half ages in one place.

## Resources

### RES-01 — Harness invocation primary documentation, both harnesses

**Where to find it:** https://docs.claude.com/en/docs/claude-code/cli-reference and https://github.com/openai/codex
**What exactly to learn from it:** non-interactive invocation semantics,
permission-mode flags, and the authentication boundary the cost architecture
rests on.
**Which chapters or sections matter:** basic usage; bare mode; the
authentication and credential-use section of the compliance page. For the second
harness, usage, authentication and its non-interactive limitation.
**Which roadmap project uses the knowledge:** the harness adapter at S0, and the
cross-harness comparison at S8.
**What exercise proves I understood it:** D-w01-1 — an unattended run with a
captured transcript, plus the W01 stretch surfacing where the second harness's
approval step fails.

### RES-02 — Stop Comparing LLM Agents Without Disclosing the Harness

**Where to find it:** Google Scholar, exact title: https://scholar.google.com/scholar?q=%22Stop+Comparing+LLM+Agents+Without+Disclosing+the+Harness%22
A search rather than a permalink: the arXiv identifier was never checked against a primary source, and this repository does not print an identifier it has not verified.
**What exactly to learn from it:** that the loop around a model changes outcomes
more than the model does — identical code quality at a 32x cost spread from
harness differences alone — and how to separate harness effect from model
effect.
**Which chapters or sections matter:** the empirical comparison holding the
model fixed and varying the harness.
**Which roadmap project uses the knowledge:** designing the month-04 comparison
so it measures the harness rather than re-measuring model choice.
**What exercise proves I understood it:** D-m04-1 — a comparison whose run
metadata proves the model id was pinned.

### RES-03 — Building Effective Agents

**Where to find it:** https://www.anthropic.com/engineering/building-effective-agents
**What exactly to learn from it:** the control-flow ownership distinction.
Workflows route the model through predefined code paths, so you own every
branch; agents direct their own process, so you own the goal and the guardrails.
**Which chapters or sections matter:** all of it; it is short.
**Which roadmap project uses the knowledge:** the W01 architecture decision,
which settles which stages get durable-state-machine treatment.
**What exercise proves I understood it:** D-w01-4 — a stage-by-stage
classification from which a reader can predict, for any stage, whether failure
means replay or re-prompt.

### RES-04 — Temporal documentation: activities and activity definition

**Where to find it:** https://docs.temporal.io/activities
**What exactly to learn from it:** how a mature system words its guarantee — an
activity may physically run more than once yet be observed as completed once,
because the guarantee lives in the durable log, not the function body.
**Which chapters or sections matter:** retry policies and idempotency. Skip
every SDK-specific chapter.
**Which roadmap project uses the knowledge:** validating the hand-built S1a and
S1b state machine against a reference implementation.
**What exercise proves I understood it:** D-w03-1, plus a mapping table naming
what the reference system solves that the hand-built one does not, and whether
that gap matters at this scale.

### RES-05 — Model Context Protocol specification, at its pinned revision

**Where to find it:** https://modelcontextprotocol.io/specification
**What exactly to learn from it:** the stateless-core discipline —
self-contained requests, per-request capability negotiation, and application
state carried by explicit handles in tool arguments. Read *after* building the
state machine.
**Which chapters or sections matter:** the stateless-request change, the
multi-round-trip pattern, the feature-lifecycle policy. Skip extension wire
formats; the revision to pin is in the snapshot.
**Which roadmap project uses the knowledge:** the hand-built queue's task-state
design, and any later tool-server integration.
**What exercise proves I understood it:** D-w02-1 — a state machine carrying
task state explicitly rather than leaning on a sticky session.

### RES-06 — Vector-search filtering: pre-filter against post-filter

**Where to find it:** https://qdrant.tech/articles/vector-search-filtering/
**What exactly to learn from it:** why post-filtering breaks correctness and
leaks existence in one move, and how filtered traversal is done properly, with
payload indexes keeping the walk inside the permitted subset.
**Which chapters or sections matter:** the filtering guide and the
pre-versus-post-filtering article.
**Which roadmap project uses the knowledge:** SKA-S0 and SKA-S1.
**What exercise proves I understood it:** D-w05-2 — a reproducible failing
post-filter case plus a test asserting the pre-filter returns exactly k
authorized results whenever k exist.

### RES-07 — Retrieval evaluation metrics

**Where to find it:** https://www.pinecone.io/learn/offline-evaluation/
**What exactly to learn from it:** precision@k, recall@k, MRR and NDCG@k, and
why rank-blind metrics let a system pass while its reranker buries the best
answer at position five. Plus freezing the label set first.
**Which chapters or sections matter:** offline evaluation measures in
information retrieval; metrics for search and recommendation.
**Which roadmap project uses the knowledge:** SKA-S0 and SKA-S1.
**What exercise proves I understood it:** D-w06-1 — metrics per configuration
against a set provably frozen before the first tuning change.

### RES-08 — Local embedding and reranker model cards

**Where to find it:** https://huggingface.co/Qwen/Qwen3-Embedding-0.6B and https://huggingface.co/BAAI/bge-reranker-v2-m3
**What exactly to learn from it:** how to pick, run and evaluate pretrained
retrieval models as black boxes with known contracts, published scores **and
licences**, under a zero-euro constraint on a laptop.
**Which chapters or sections matter:** the embedding model's card — parameters,
disk size, benchmark mean — the reranker's card and its licence, and the
cross-encoder efficiency notes.
**Which roadmap project uses the knowledge:** SKA-S0 embeddings and SKA-S1
reranking.
**What exercise proves I understood it:** D-w06-1 — measured reranking lift with
p50 and p95 latency from a local CPU run. Licence is a selection criterion, not
a footnote: one widely recommended multilingual reranker is non-commercial and
unusable here.

### RES-09 — OpenTelemetry GenAI semantic conventions

**Where to find it:** https://opentelemetry.io/docs/specs/semconv/gen-ai/
**What exactly to learn from it:** the operation-name vocabulary and the agent,
tool and model span shapes — and the discipline of pinning a version instead of
memorising today's attribute names.
**Which chapters or sections matter:** operation-name values, agent and tool
span structure, token-usage attributes — checking the stability badge on every
attribute used. [The snapshot](ecosystem-snapshot-2026-08.md) records what those
badges say.
**Which roadmap project uses the knowledge:** S5 instrumentation and S6 trace
evaluation.
**What exercise proves I understood it:** D-w09-1 — one connected trace per run
with correct parent-child nesting and token counts matching provider-reported
usage, exported against a pinned convention version recorded in run metadata.

### RES-10 — LLM-as-judge reliability research

**Where to find it:** Google Scholar, by topic: https://scholar.google.com/scholar?q=llm-as-a-judge+position+bias+chance-corrected+agreement
A topic search, deliberately. The reliability literature here is several papers rather than one, and naming a single identifier would misrepresent a body of work as a citation.
**What exactly to learn from it:** that reproducibility is not validity. A judge
can show very high test-retest reliability and substantial position bias at
once, and raw agreement overstates chance-corrected agreement.
**Which chapters or sections matter:** the minimum viable validation protocol.
**Which roadmap project uses the knowledge:** the W10 judge prompt and its
threshold design.
**What exercise proves I understood it:** D-w10-1 — a threshold stated as a
statistical bound with a justification and a re-baselining condition, not
"everything must pass".

### RES-11 — OWASP Top 10 for Agentic Applications, the PDF itself

**Where to find it:** https://genai.owasp.org/ — download the PDF, not a vendor summary of it
**What exactly to learn from it:** the agentic threat categories this build
touches — goal hijack, tool misuse, identity and privilege abuse, memory and
context poisoning — each with named mitigations, so an attack report cites
something rather than asserting improvement. Plus the least-agency framing:
autonomy where it is not needed widens the attack surface for nothing.
**Which chapters or sections matter:** ASI01, ASI02, ASI03 and ASI06, plus the
leads' letter.
**Which roadmap project uses the knowledge:** S7a, S7b and BOA-S2.
**What exercise proves I understood it:** D-w11-2, D-w12-2 and D-m05-2, each
mapping its mitigation to a named one. Cite the PDF, never a vendor summary, and
never number a category from the LLM list — that policy is in
[the snapshot](ecosystem-snapshot-2026-08.md).

### RES-12 — The lethal trifecta for AI agents

**Where to find it:** https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
**What exactly to learn from it:** private data plus untrusted content plus an
outbound channel equals exfiltration risk however carefully the prompt is
written — so the fix removes a leg structurally instead of filtering.
**Which chapters or sections matter:** the whole post; it is short.
**Which roadmap project uses the knowledge:** the answering path of both the
business agent and the knowledge agent.
**What exercise proves I understood it:** D-w11-2 — an exfiltration attempt
whose report states whether the fix broke a leg or merely filtered. It is an
independent framing widely adopted in practice, not an OWASP identifier, and is
attributed that way.

### RES-13 — Designing Data-Intensive Applications

**Where to find it:** https://dataintensive.net — ISBN 978-1-4493-7332-0
**What exactly to learn from it:** the operational reality of partial failure,
and precise vocabulary for delivery-versus-processing guarantees. Read for
calibration, not acquisition.
**Which chapters or sections matter:** chapter 8 first — unreliable networks and
clocks, timeouts as the only failure detector, process pauses, fencing tokens.
Then chapter 7 on transactions; then only chapter 9's two-phase-commit section,
to see why the outbox exists; then chapter 11's fault-tolerance section. Skip
chapters 5, 6, 10 and 12.
**Which roadmap project uses the knowledge:** S1a and S1b, and the month-04
outbox.
**What exercise proves I understood it:** D-w03-1 and the month-04 crash-window
exercise, EXT-01.

### RES-14 — A Philosophy of Software Design

**Where to find it:** https://web.stanford.edu/~ouster/cgi-bin/book.php
**What exactly to learn from it:** the deep-module thesis and information
hiding, which become *more* load-bearing under generated code, not less. Roughly
two hours, at an unusually high usable-ideas-per-page ratio.
**Which chapters or sections matter:** chapter 4 on deep modules, 5 on
information hiding and leakage, 8 on pulling complexity downwards, 11 on
designing it twice — noticing that designing twice is nearly free once
generation is cheap — and 13 on comments as design records.
**Which roadmap project uses the knowledge:** the harness adapter boundary and
the platform's module structure.
**What exercise proves I understood it:** D-w02-2 — the boundary regeneration
test, which is a direct empirical test of the book's central claim.

### RES-15 — Release It!

**Where to find it:** https://pragprog.com/titles/mnee2/release-it-second-edition/
**What exactly to learn from it:** how systems actually fail in production —
the *operate* half of the competency gap, which no concept reading closes.
**Which chapters or sections matter:** part I's antipatterns — integration
points, blocked threads, unbounded result sets, cascading failures, slow
responses — then its patterns: timeouts, circuit breaker, bulkheads, fail fast,
steady state, handshaking, back pressure.
**Which roadmap project uses the knowledge:** the three gateways at month 04,
and W09's rate limiting and unbounded-retry defenses.
**What exercise proves I understood it:** D-w08-1, the chaos run, and D-w09-2,
the cost-exhaustion exercise.

## Deliberately excluded

Two well-known catalogues are left out on purpose: the enterprise application
architecture catalogue and the enterprise integration patterns catalogue.

They are excluded because a catalogue is **reference, not reading**. The correct
use is targeted lookup of a named pattern — idempotent receiver, guaranteed
delivery, competing consumers, dead letter channel, correlation identifier;
gateway, service layer, repository, transaction script, optimistic offline
lock — perhaps forty-five minutes across the whole programme. Reading either
cover to cover inside a thirty-nine hour track would displace one of the three
books above and would not repay the trade.

Naming the exclusion is a stronger curation signal than a longer list: it says
the omission was decided rather than overlooked, and it tells a reader who
already owns those books how to use them here.
