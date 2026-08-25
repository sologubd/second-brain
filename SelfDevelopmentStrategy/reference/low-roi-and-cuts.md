# Low-ROI verdicts, the cut list and the glossary

## What this is

Three lists that exist to say no in advance.

The **low-ROI verdicts** answer the six conventional-curriculum challenges the
brief names, plus seventeen items research rejected. The **cut list** is where
hours go when a bucket overruns; an overrun is resolved from it, never by
compressing stated hours. The **glossary** fixes terms used precisely here,
including recognition-only concepts, so their absence reads as a decision.

## The table

### The six challenges

| # | Question | Verdict | Why |
|---|---|---|---|
| LR-01 | Do I really need to memorize every GoF pattern? | NO. | Several are Python language features — Strategy a function, Iterator a generator, Decorator `@`. Seven at real surfaces in W02 and W08; sixteen recognition-only. |
| LR-02 | Do I need to become an expert in one vector database? | NO. | Sub-10M vectors, one node, Postgres already the state store. What transfers is how filtering interacts with approximate-nearest-neighbour structure — a security question, not only performance. |
| LR-03 | Do I need deep ML mathematics for my objectives? | NO. | The differentiating skill is evaluating and operating model-based systems, not training them. The rigour here is experimental design. |
| LR-04 | Do I need to build an LLM from scratch? | NO. | It teaches how a transformer works, not why your pipeline opened three pull requests for one issue. Every failure prevented here is above the model. |
| LR-05 | Do I need Kubernetes? | NO — CONDITIONALLY, and not for the stated reason. | Zero surface: one node, one Postgres, worktrees for isolation. The brief bars it *merely because it is industry standard*, not absolutely — so if a client requires it, two weeks later with a real surface beats now without one. Docker is taught narrowly, for Postgres and the W12 sandbox. |
| LR-06 | Do I need LangChain abstractions beyond the parts I use? | NO. | The durable concept — checkpoint at step boundaries, resume, trade recovery granularity against latency — transfers wholly to W02 and W03's hand-built machine. Their investment is productionisation. |

### Seventeen further verdicts

| # | Item | Verdict | Reasoning |
|---|---|---|---|
| LR-07 | LeetCode | NO — CONDITIONALLY | No cold-outreach buyer of engineering capability runs a whiteboard algorithm screen. Left open: a month-12 turn toward a role with one justifies it. |
| LR-08 | Kafka / RabbitMQ / SQS comparison | NO | The lesson is semantic. Semantics transfer; products expire. |
| LR-09 | Redis and Redlock | NO | Duplicates Postgres; teaches the area's most contested lock. |
| LR-10 | Event sourcing and CQRS as architecture | NO | High cost, no surface, hard to reverse, seductive here. |
| LR-11 | Consensus internals, CRDTs, CAP debates | NO | You consume consensus via Postgres; never implement it. |
| LR-12 | Microservices decomposition | NO | One service, one user. |
| LR-13 | Hexagonal / Clean Architecture as doctrine | NO | Its useful tenth is taught by Gateway and Adapter. |
| LR-14 | TLA+ and formal methods | NO — ON BUDGET, NOT ON MERIT | Well suited to verifying a state machine, but multi-week before it returns anything, and Track B is at a hard floor. A month-06 stretch. |
| LR-15 | The SDK library instead of the CLI binary | NO | Requires key-based billing; defeats the zero-marginal-cost premise. |
| LR-16 | Chasing published quota numbers | NO | Unpublished or temporary. Measure empirically: W01's headroom task. |
| LR-17 | Eval-framework internals beyond niche-fit | NO | One framework built deep beats a four-tool survey. |
| LR-18 | Memorising tracing attribute names | NO | Actively churning. Read the spec at instrumentation time; pin it. |
| LR-19 | Protocol-level study of sandboxes | NO | The concept — container is not a hard boundary, microVM is — is one paragraph. |
| LR-20 | A policy engine for the intent gate | NO | Right pattern, wrong investment. A hand-written check teaches it. |
| LR-21 | Numeric injection-defense percentages | NO — AND FORBIDDEN | No verified primary benchmark. Measure against your own system. |
| LR-22 | Further channel benchmark research | NO | No source is independently verifiable; this programme is email-only. |
| LR-23 | Enterprise process-prioritisation frameworks | NO | Built for hundreds of processes. A context mismatch. |

### The cut list

| # | Week | Hours | Track | What is cut | What it breaks |
|---|---|---|---|---|---|
| CUT-01 | W06 | 0.45 | E | 22 assisted prospects to 14 | Prospects drop 56 to 48 |
| CUT-02 | W10 | 0.3 | E | Fold opportunity scoring into W11's offer sketch | Scored drop 2 to 1; PF-10 thins |
| CUT-03 | W05 | 0.5 | C | Hard-code the fusion constant | Nothing; tuning defers |
| CUT-04 | W06 | 1.0 | C | Chunking sweep, three configurations to two | Its result table thins |
| CUT-05 | W02 | 1.0 | A | Defer subagent call-graph work to W08 | D-w02-4 loses attribution |
| CUT-06 | W09 | 1.0 | A | Spans narrowed to agent and tool layers | W10 scores fewer span types |
| CUT-07 | W12 | 1.0 | D | Sandbox build moves to M04 | No sandbox evidence till M04 |
| CUT-08 | W10 | 1.0 | C | Regression reruns N=5 to N=3 | Widened bound must be stated; below 3 it stops gating |
| CUT-09 | M04 | 0.0 | A | Quota fallback: 40 runs to 10 per harness | Confidence weakens. Not an hour cut |
| CUT-10 | W07 | 0.5 | B | Failure taxonomy folded into S3 docs | D-w07-2 folds into D-w07-1 |
| CUT-11 | W12 | 1.0 | B | Review #3 narrowed to the security surface | CP-M3 thins; PF-04 loses a review |
| CUT-12 | W02 | 1.0 | B | Boundary regeneration, three modules to two | Two points cannot carry the claim |

Draw order: CUT-01 and CUT-02 first as business slack, then CUT-03, CUT-05,
CUT-06, CUT-04, CUT-07, CUT-08. **The three Track B rows are drawn only after
every other row is exhausted, and only with a written justification in the
retrospective that drew them** — Track B has lost roughly eighteen hours across
three revisions and a fourth cut is a hard stop. CUT-12 is last: it removes the
track's one distinctively AI-native exercise.

### Glossary

| Term | Definition |
|---|---|
| effectively-once processing | At-least-once delivery plus idempotent processing: state after N deliveries equals state after one. Duplicates absorbed. |
| exactly-once delivery | Impossible over an unreliable network: a sender with no acknowledgement cannot tell a lost message from a lost ack. |
| exactly-once execution | Unachievable unless effect and record share a transaction. |
| crash window | Between a local commit and an external effect. The bug class generated code never surfaces, since no agent injects a kill mid-sequence. |
| natural key | A domain property making a remote create idempotent: one PR per branch name. |
| fencing token | A rising value issued with a lease and checked by the resource, so an expired worker cannot write. |
| lease | A time-bounded claim on a work item; the primitive under visibility timeouts. |
| orphan reclaim | Recovering work from a dead worker. Slow and dead are indistinguishable, hence timeout plus token. |
| deep module | Small interface, large implementation. Under generated code a capability gate: the contract fits in context. |
| pre-filter | Restricting candidates to permitted documents before or during traversal, preserving recall. |
| post-filter | Search first, discard unauthorized hits after. A correctness bug and a disclosure vulnerability at once. |
| Reciprocal Rank Fusion | Score 1/(k + rank) per list, summed. Rank only, so no normalisation. |
| agent memory | Cross-session state the agent writes and later trusts as fact. Not history, task state, or corpus. |
| lethal trifecta | Private data, untrusted content, external communication. A practitioner's framing. |
| confused deputy | A program with more privilege than its caller, tricked into misusing it. |
| provenance | Where data came from *and at what trust level*, recorded at write time. Without it, no read-time policy. |
| quota_stall_seconds | Time a run spent blocked on quota, so distorted samples are excludable. |
| judge and agent regression | The first rescores a cached corpus, catching rubric drift; the second re-executes and alone tests what ships. |
| consensus, CRDTs, vector clocks, quorum replication | Recognition only, named so their absence is a decision. |
| event sourcing / CQRS | Recognition only. Real operational cost, no surface here. |
| non-verdict | "Insufficient evidence, deferred to a named month", with the threshold named. Passing. |
| deprecate-then-remove | Interface evolution with a stated support floor. The M08 rule. |

## How to read it

A verdict decides against *this* strategy; it is not a judgement of the subject.
LR-14 is the clearest case — rejected on budget, explicitly, so it can be
revisited when the budget changes rather than inherited as contempt.

Two verdicts are conditional and the condition is the content: LR-05 and LR-07
are barred on a *reason*, not a word, which is why both are named rather than
omitted.

Read the cut list in draw order. Each row states what it breaks, so a draw is a
trade with its cost visible, and each carries a track tag so the M01 value
question has an answer slot. Entries marked *recognition only* are exercised
nowhere.

## How it changes

**M01** may draw from the cut list when a bucket runs more than 15% over plan.
**M08** owns the cut-list review: which rows were drawn, what they broke, and
whether any never-drawn row should retire. **M09** answers the stop-learning
question against these verdicts rather than freehand — anything that should stop
and is not already a row becomes one, with its reasoning, in the same delta.

The glossary changes when a term is corrected, not when one is added. The
effectively-once correction is the model: a partial fix leaves two contradictory
claims with no signal about which is canon.

All three lists live in canon and are edited through
[HOW-TO-EDIT.md](../HOW-TO-EDIT.md).
