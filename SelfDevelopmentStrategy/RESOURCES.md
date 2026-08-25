# Resources

Fifteen items, three of them books. Deliberately short: a fifty-item list signals
reading rather than building, and nobody finishes it.

Read in the order the weeks need them. For each: why it matters, what to read,
and which week consumes it.

## Agents and harnesses

**Your harness's CLI reference** — [Claude Code CLI](https://docs.claude.com/en/docs/claude-code/cli-reference) · [Codex](https://github.com/openai/codex)
Non-interactive invocation, permission-mode flags, and the authentication
boundary. Read the sections on print/headless mode, permission modes, and the
compliance page's credential section. Note where subscription sign-in parts from
key-based access — it shapes the CLI-versus-SDK decision you make later, and is
worth understanding before you need it. → **Week 1**, and again at weeks 7–9.

**[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** (Anthropic)
The control-flow ownership distinction: workflows route the model through code
paths you own, agents direct their own process. Own the branches and you get
replay, cheap debugging and predictable cost; hand the model its own process and
you trade all three for adaptability. Short — read all of it. → **Weeks 1, 3**.

**"Stop Comparing LLM Agents Without Disclosing the Harness"**
Search by title; the loop around a model changes outcomes more than the model
does — identical code quality at large cost spreads from harness differences
alone. Read it before any cross-harness comparison, so the comparison measures
the harness and not the model. → **Week 1 stretch, and the months.**

## Durability, state and failure

**[Designing Data-Intensive Applications](https://dataintensive.net)** — Kleppmann, ISBN 978-1-4493-7332-0
Chapter 8 first: unreliable networks and clocks, timeouts as the only failure
detector, process pauses, fencing tokens. Then chapter 7 on transactions. Then
*only* chapter 9's two-phase-commit section, to see why the outbox exists. Then
chapter 11's fault-tolerance section. Skip 5, 6, 10 and 12. Read for
calibration, not acquisition. → **Weeks 5, 6, 8**.

**[Temporal: activities and retry policies](https://docs.temporal.io/activities)**
How a mature system words its guarantee: an activity may physically run more than
once yet be observed as completed once, because the guarantee lives in the
durable log, not the function body. Read retry policies and idempotency; skip
every SDK chapter. Use it to check your hand-built state machine against a
reference — and to name what it solves that yours does not. → **Weeks 5, 6**.

**[Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)** — Nygard
The *operate* half, which no concept reading closes. Part I's antipatterns —
integration points, blocked threads, unbounded result sets, cascading failures,
slow responses — then its patterns: timeouts, circuit breaker, bulkheads, fail
fast, back pressure. Every one is cheap to state and means nothing until you have
watched the failure it prevents. → **Weeks 7, 8**.

**[A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php)** — Ousterhout
The deep-module thesis and information hiding, which get *more* load-bearing
under generated code, not less: the interface is the entire brief the generator
receives. Chapters 4, 5, 8, 11 and 13. Roughly two hours, unusually high
usable-ideas-per-page. → **Weeks 5, 8**.

## Retrieval and evaluation

**[Vector search filtering: pre- vs post-filter](https://qdrant.tech/articles/vector-search-filtering/)**
Why filtering after an approximate scan breaks correctness and leaks existence in
one move, and how filtered traversal is done properly. The *concept* transfers to
pgvector; the implementation does not — pgvector has no equivalent filtered
traversal, so read this for the failure mode and then compare pgvector's actual
options (iterative scan, exact search over the authorized subset, partial indexes,
partitioning) on your own data. → **Week 10**.

**[Offline retrieval evaluation](https://www.pinecone.io/learn/offline-evaluation/)** (Pinecone)
precision@k, recall@k, MRR, NDCG@k — and why rank-blind metrics let a system pass
while its reranker buries the best answer at position five. Plus freezing the
label set before you tune. → **Weeks 9, 10**.

**Embedding and reranker model cards** — [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) · [bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3)
How to pick and run pretrained retrieval models as black boxes with known
contracts, published scores **and licences**, on a laptop for nothing. Licence is
a selection criterion, not a footnote: one widely recommended multilingual
reranker is non-commercial and unusable here. → **Week 10**.

**LLM-as-judge reliability research**
Search for *llm-as-a-judge position bias chance-corrected agreement*. This is
several papers, not one. The point: reproducibility is not validity — a judge can
show high test-retest reliability and substantial position bias at once, and raw
agreement overstates chance-corrected agreement. Read for the minimum viable
validation protocol. → **Week 9**.

## Observability

**[OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)**
Operation-name vocabulary, agent/tool/model span shapes, token-usage attributes.
Check the stability badge on every attribute you use, and **pin a version in your
run metadata** rather than memorising today's names — this spec churns. → **Week
7**.

## Security

**[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/)** — download the PDF, not a vendor summary
The agentic threat categories this build touches: goal hijack, tool misuse,
identity and privilege abuse, memory and context poisoning — each with named
mitigations, so an attack report cites something rather than asserting
improvement. Plus the least-agency framing: autonomy where it is not needed
widens the attack surface for nothing. Cite by category name and re-check current
numbering against the PDF; the identifiers have been renumbered between editions.
→ **Weeks 11, 12**.

**[The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)** — Willison
Private data + untrusted content + an outbound channel = exfiltration risk
however carefully the prompt is written, so the fix removes a leg structurally
instead of filtering. Short. An independent framing widely adopted in practice,
not an OWASP identifier. → **Week 11**.

## Pattern catalogues — lookup only

The enterprise-application-architecture and enterprise-integration-patterns
catalogues are **reference, not reading**. Correct use is targeted lookup of a
named pattern — idempotent receiver, guaranteed delivery, competing consumers,
dead letter channel, correlation identifier, gateway, service layer, repository,
transaction script, optimistic offline lock — maybe 45 minutes across the whole
year. Reading either cover to cover would displace one of the three books above
and would not repay the trade. Which patterns matter and why is in
[exercises/architecture.md](exercises/architecture.md).

## Deliberately not doing

Named so the absence reads as a decision rather than an oversight.

| Not doing | Why |
|---|---|
| Memorising GoF patterns | Several are Python language features. Seven have real surfaces here; the rest are recognition-only vocabulary. |
| Becoming an expert in one vector database | Under ~10M vectors on one node with Postgres already present, what transfers is how filtering interacts with ANN structure — a security question. |
| Deep ML mathematics | The differentiating skill is evaluating and operating model-based systems, not training them. The rigour needed is experimental design. |
| Building an LLM from scratch | Teaches how a transformer works, not why your pipeline opened three PRs for one issue. Every failure prevented here sits above the model. |
| Kubernetes | Zero surface: one node, one Postgres, worktrees for isolation. If a client requires it, learn it then, with a real surface. Docker is used narrowly — Postgres, and the week-12 sandbox. |
| LangChain/LangGraph abstractions beyond what you use | The durable concept — checkpoint at step boundaries, resume, trade recovery granularity against latency — transfers wholly to the hand-built machine in weeks 5–6. |
| LeetCode | No cold-outreach buyer of engineering capability runs an algorithm screen. Revisit only if month 12 turns toward a role that does. |
| Kafka / RabbitMQ / SQS comparison | The lesson is semantic. Semantics transfer; products expire. |
| Redis and Redlock | Duplicates Postgres, and teaches the area's most contested lock. Advisory lock + lease + fencing token carries no asterisks. |
| Event sourcing and CQRS as architecture | High cost, no surface, hard to reverse — and seductive precisely here. |
| Consensus internals, CRDTs, CAP debates | You consume consensus through Postgres. You will never implement it. |
| Microservices decomposition | One service, one user. |
| Hexagonal / Clean Architecture as doctrine | Its useful tenth is taught by Gateway and Adapter. |
| TLA+ and formal methods | Genuinely well suited to verifying a state machine, but multi-week before it returns anything. On budget, not on merit. |
| Adopting an SDK or direct API *before* the CLI subprocess path has run | Not a permanent verdict against them. The subprocess is the smallest thing that works, so it goes first; weeks 7–9 re-evaluate all three on requirements that have actually appeared. |
| Reverse-engineering vendor quota behaviour | Unpublished, partly temporary, shared with your interactive use. Track tokens, cost and stalls; do not model the plan. This trains agent-system engineering, not subscription-plan archaeology. |
| Memorising tracing attribute names | Actively churning. Read the spec at instrumentation time and pin the version. |
| Numeric injection-defence percentages | No verified primary benchmark exists. Measure against your own system or say nothing. |
| Enterprise process-prioritisation frameworks | Built for hundreds of processes. Context mismatch. |

## A note on volatile facts

Model names, spec revisions, quota figures, pricing and security-list numbering
all have half-lives measured in weeks. Nothing in this repository states a dated
ecosystem fact — check the primary source when you reach the week that needs it.
That is cheaper than maintaining a snapshot file that ages invisibly.
