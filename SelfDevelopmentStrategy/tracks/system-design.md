# Track B — Software Architecture & System Design

## What these hours buy

39.0 h, 21.7% of the programme, at a declared hard floor. The number fell from
roughly 57 to 42 to 39 across three revisions, each cut argued individually. A
fourth is not an available trade; an overrun draws on rows pre-tagged for other
tracks.

What the floor protects is six pieces of evidence. A durable task state machine
on Postgres, proved effectively-once across 100 replays with a kill signal
injected between the commit and each external call. A queue with lease-based
claiming, dead-lettering and worktree isolation, proved to strand nothing and
duplicate no effect under a chaos run. An aggregate and invariant table — what
must always be true, which aggregate owns it, where it is enforced. A versioned
checklist for reviewing generated code. A production failure-mode taxonomy wired
into the machine's error classification. And three architecture reviews against
14 named defect classes: AR-01 and AR-03 on your own platform, AR-02 on a
deliberately bad system handed to you, the only one where recognising your own
intent cannot flatter you.

Note what the first artifact does not claim. Exactly-once delivery over an
unreliable network is impossible; effectively-once processing via idempotency is
what is actually proved under one hundred replays. Every file here touching the
replay harness carries that correction, because fixing the phrasing in one place
and not another leaves the repository asserting both.

## Entry competency

Working knowledge of distributed systems, user-supplied — and the shape of the
gap matters more than the level. `CM-03` records it as concept-strong and
operation-weak: the learner can define idempotency and has never operated an
idempotent consumer, an outbox, or a distributed lock under load. `CM-04`
targets that seam, which is where the *prove effectively-once under 100 replays*
framing came from.

Nothing here explains what a concept is. Every hour proves one, operates one, or
decides which ideas survive when an agent writes the code. Evidence: `D-w02-1`,
`D-w02-2`, `D-w03-1`, `D-w08-1`, `D-w08-2`, `D-w12-3`, `D-m04-2`, `D-m04-3`.

## Concepts

Twenty-four concepts, all homed here. Twenty carry a P0 argument below; the
other four are handled next, with their demotion reasons. Columns: priority, the
first week with a real surface, that surface, and the id proving it.

| Concept | Priority | Week | Surface | Proved by |
|---|---|---|---|---|
| boundaries (C-023) | P0 | W01 | the adapter contract; W02's regeneration test | D-w02-2 |
| coupling and cohesion (C-024) | P0 | W02 | deep-module ratio, measured per module | D-w02-2 |
| deep modules (C-025) | P0 | W01 | one contract over two CLI surfaces | D-w01-2 |
| modularity (C-026) | P0 | W02 | six separately regenerable packages | D-w02-2 |
| domain modeling (C-027) | P0 | W02 | the aggregate and invariant table | D-w02-1 |
| state machines (C-028) | P0 | W02 | S1a: enum plus transition table | D-w02-1 |
| transactions (C-029) | P0 | W08 | dedup insert and transition, one commit | D-w03-1 |
| concurrency (C-030) | P0 | W08 | S4's chaos run, 30% of workers killed | D-w08-1 |
| consistency (C-031) | P0 | W03 | three dedup mechanisms, each shown | D-w03-1 |
| queues (C-032) | P0 | W08 | S4, built on Postgres, not adopted | D-w08-1 |
| event-driven systems (C-033) | P1 | W08 | the outbox relay, a separate process | D-m04-2 |
| caching (C-034) | P1 | W09 | analysis memoised by commit SHA | D-w09-1 |
| retries (C-035) | P0 | W03 | S1b's classification table | D-w03-1 |
| idempotency (C-036) | P0 | W03 | the dedup table, unique constraint | D-w03-1 |
| rate limiting (C-037) | P0 | W09 | a token bucket above the retry layer | D-w09-1 |
| distributed locks (C-038) | P0 | W08 | advisory locks, leases, a fencing token | D-w08-1 |
| outbox pattern (C-039) | P0 | W03 | the outbox row on the transition's commit | D-m04-2 |
| sagas (C-040) | P0 | W12 | task teardown with compensations | D-m04-3 |
| failure recovery (C-041) | P0 | W03 | S4's orphan reclaim; a terminal state | D-w08-1 |
| migrations (C-042) | P2 | M08 | one ADR on schema evolution | — |
| API evolution (C-043) | P2 | M08 | the same ADR, internal surfaces | — |
| multi-tenancy (C-044) | P0 | W05 | rehomed onto the knowledge agent | D-w05-2 |
| observability (C-045) | P0 | W09 | S5's spans, cost, stall seconds | D-w09-1 |
| reliability (C-046) | P0 | W09 | retry budget under an induced storm | D-w09-1 |

### Boundaries and the domain

**boundaries.** Two arguments, both stronger under agents. A module whose
contract fits in context while its implementation need not is the unit an agent
works inside reliably; across a leaky boundary it emits plausible code built on
wrong assumptions about the far side. Regenerating a module is safe only at
narrow-contract granularity. Boundary quality is now a capability gate.

**coupling and cohesion.** Measurable now, not aesthetic. W02 deletes an
implementation, hands an agent nothing but the interface, the docstring and the
tests, and records what comes back wrong. Every failure names a specific piece
of out-of-module knowledge the deleted code had silently depended on. That is a
coupling metric with an experiment behind it rather than a smell with a name,
and it can be rerun after any refactor that claims to have improved things.

**deep modules.** The case for a narrow interface over a large implementation
began as an argument about human cognitive load. Under an agent it turns
literal, because the interface is the entire brief the generator receives — so
the regeneration test makes a design opinion rerunnable.

**modularity.** Duplicate code freely; never duplicate a decision. *Do not
repeat yourself* was two arguments under one name: do not type the same thing
twice, do not encode the same choice twice. The first collapsed when typing got
cheap; the second did not move.

**domain modeling.** Your domain model is the compression scheme for your
instructions. With a real one a prompt is a single unambiguous sentence; with
`data`, `handle()` and `process()`, every prompt re-explains the domain and can
drift. Stated as a principle with its mechanism — no study establishes an effect
size, and claiming one would invent a number.

**state machines.** An enum plus a legal-transition table is a machine-checkable
specification of intent, so the invalid-transition suite is generated rather
than written — covering an error class review-by-reading never sees. What stays
human is which states exist and what *done* means.

### Correctness under failure

**transactions.** Taught small: read-committed and the lost update it permits,
skip-locked claiming, unique and partial indexes as the only reliable dedup
primitive, external APIs offering no isolation at all. Read-modify-write is the
form an agent reaches for first, because it is the one that reads most clearly —
and it is correct single-threaded, broken concurrently, and indistinguishable
between the two on the page. Demanding a conditional update, a version column or
a row lock is a review skill you cannot exercise by reading code in isolation,
only by reading it while holding a model of concurrent execution.

**concurrency.** Partition before you lock is Track A's argument, at
[C-009](agentic-engineering.md). Track B adds the residue once partitioning is
exhausted: a lease can expire while its holder is still working, and the holder
is never told. A lock with neither a fencing token nor an idempotent operation
underneath it is a comfort blanket — it makes the race rarer without making it
impossible, which is the worst of both outcomes because it also makes the race
harder to reproduce.

**consistency.** The honest version at this scale is small, and shrinking it
serves the learner. Linearizability, the CAP taxonomy and consensus internals
are recognition-only — you consume consensus through Postgres. What you must
state on demand is which effects share a transaction with their own record.

**queues.** A queue is not a list you pop from; the durable concept is a lease.
A worker claims a task for a bounded time, must acknowledge before that window
closes or another worker may take it, and repeated failure routes to a
dead-letter path rather than an unbounded loop. Generated consumer code omits
both halves. It omits the lease, which is invisible until a worker can crash
mid-task, and it omits dead-lettering, so a single poison message loops forever
and starves everything queued behind it. Building the thing is the lesson;
adopting a broker hides exactly these mechanics.

**retries.** The truth-table argument is Track A's, at
[C-012](agentic-engineering.md). Track B contributes placement: retries are
taught in the same week as idempotency, because a retry is safe only if the
operation is idempotent.

**idempotency.** The anchor concept. A test suite records the invocations
somebody thought to write down, and essentially every test invokes the handler
once. An agent optimises against the tests and the ticket, neither of which
mentions the second call, so it produces a handler that is locally correct and
globally wrong — invisible to the type checker, the linter, review-by-reading
and CI, and visible on the third retry as a duplicate pull request. The durable
skill is not writing the idempotent handler, which an agent does the moment you
ask; it is knowing the demand exists, stating the key, proving absorption.

**rate limiting.** The subscription quota is a global semaphore shared across
concurrent workers, so bounding concurrency usually beats bounding rate. It is
also the one place an adversary attacks you through your own automation — a
security concept wearing a reliability hat.

**distributed locks.** Redis is refused: standing it up to demonstrate locking
would mean shipping the area's most contested primitive and then annotating it.
An advisory lock with a lease and a fencing token carries no asterisks. The
examinable question is what happens when the lease expires with the model call
still in flight.

**outbox pattern.** You cannot atomically commit a transaction and perform an
HTTP call. Code shaped `db.commit(); github.create_pr()` has a crash window, and
crash-window bugs are the definitional class generated code never surfaces: the
naive version passes every test absent a crash, and no agent injects a kill
between two statements unprompted. Knowing the pattern exists is what makes you
write the test that kills the process at the right line.

**sagas.** The fan-out to GitHub, Notion and Sentry is not a saga, and calling
it one teaches a real confusion: if the Notion write fails after the pull
request exists you retry Notion forever rather than deleting the pull request,
because independent effects are handled completely by at-least-once fan-out over
an outbox. A saga is defined by compensation, and the genuine one is task
teardown — compensations that can fail, must be idempotent, are order-sensitive,
and include steps nothing can undo. Compensation is not rollback; intermediate
states were observed.

**failure recovery.** Timeout as the only failure detector, made concrete: a
worker dies holding a task in a running state and nothing distinguishes slow
from dead. Leases, heartbeats, visibility timeouts and orphan reclaim are the
entire answer, and every one of them is an operational choice trading false
reclaim against slow reclaim. This is the most under-appreciated item in the
platform, and exactly the operate-rather-than-explain material the entry
competency says is missing.

### Operating it

**multi-tenancy.** A single-user platform has no tenants, so teaching this on
the platform would be teaching a lens with no surface. Rehoming it onto the
knowledge agent's permission-filtered index does more than find it a home — it
sharpens the concept, because on a retrieval index a tenancy decision and a
security decision are literally the same decision. Getting it wrong therefore
produces a correctness bug and a disclosure bug simultaneously, which is why it
cannot be treated as configuration.

**observability.** The fastest-rising P0 here, and not for the usual reason.
When you write the code you carry a mental model of it and logs supplement that
model; when an agent writes it you hold only a review-derived approximation, so
the trace stops supplementing anything and becomes your primary instrument for
knowing what the system does. Two things amplify that. The work is
nondeterministic, which weakens single-run debugging and strengthens aggregate
observability. And reviewing generated code at volume is tractable only if you
can ask production what the code did, rather than reasoning from the diff about
what it should have done. Observability moved from operational hygiene to
epistemic infrastructure.

**reliability.** The stability antipatterns — integration points, cascading
failures, blocked threads, slow responses, unbounded result sets — are precisely
the shapes a three-integration platform acquires, and they are the half of the
entry gap that no amount of concept reading closes. The defences are cheap to
state and mean nothing until you have watched the failure they prevent, which is
why they arrive at W09 attached to an induced storm rather than at W01 attached
to a definition.

## Priorities and what is deferred

Four concepts sit below P0. Event-driven systems are P1 because the durable core
— at-least-once, consumer idempotency, ordering versus commutativity,
backpressure, poison messages, dead-lettering — is taught inside queues and the
outbox, leaving the relay process as the only new surface; ordering is taught as
*make handlers commutative or version them*, never as vector clocks. Caching was
demoted, and the demotion is the teaching point: write-through against
write-behind, invalidation and stampede protection all presume read-heavy
multi-user load this platform will never acquire. Its real surfaces are prompt
caching, which is Track A economics, and content-addressing by commit SHA. The
reclaimed hour went to the review checklist and the saga re-anchoring —
reallocation inside a hard floor, not a cut. Migrations and API evolution are P2
on a weak-surface finding: one repository, no external consumers, one
deployment. Their residue is a month-08 ADR carrying two rules — expand,
backfill, switch reads, contract; and deprecate-then-remove rather than
yank-and-break.

### The pattern triage

Seven patterns are kept, each for a reason about *generated* code rather than a
reason about fit, and that distinction is load-bearing. This block's first draft
argued the thesis forcefully for the patterns it cut and argued platform-fit for
most of those it kept. The asymmetry is a tell: it is easy to say why a pattern
is obsolete and hard to say what about one got more valuable. The brief asks for
the harder half.

| Pattern | Surface | Why it matters when a machine writes the code |
|---|---|---|
| Strategy | the adapter Protocol, two harness strategies | It governs the size of an instruction. Asked to *add Codex support* with no seam present, an agent edits every call site, because nothing marks which are the vendor boundary. Named, the request is one file against one contract. |
| Adapter | the typed invoke, capture, report vocabulary | The sharpest constraint in the set, and it runs against the model's instinct: asked to unify two APIs it converges them, because smoothing differences is what *unify* means in its training distribution and a smaller interface reads as cleaner in review. Here the differences *are* the measurement, so the instruction must be *expose these differences as typed fields* — otherwise you are handed a beautiful interface that silently deleted your experiment, and the deletion never shows up as a bug because everything still runs. |
| State-as-data | S1a's enum column and transition table | A transition table is a machine-checkable specification, so the invalid-transition suite is generated rather than written. And an agent asked for *a state machine* returns the class-per-state form, which dies with the process. |
| Command | the task record as a reified, replayable command | Reification makes an agent's work auditable, which is what you need precisely when you did not write the code. Generated orchestration passes closures and callbacks around because that is idiomatic Python, and a closure cannot be serialised, inspected in a database, rendered in an approval payload, or compensated after the fact. The work unit is also nondeterministic: *run it again* produces a different run, while *replay this command* preserves the intent. |
| Decorator | the middleware chain: retry, timeout, limiting | Promoted into Observer's slot. Cross-cutting concerns are what an agent bolts on inline, each addition locally correct. Order is the entire semantics — a limiter below the retry cannot bound a budget. |
| Repository | a typed collection-like boundary over persistence | A regeneration argument. Given raw ORM access an agent writes queries everywhere until the persistence contract is undiscoverable. Asked for *a repository* it returns a generic one over the ORM: an abstraction over an abstraction. |
| transaction boundaries | which operations are atomic, and why | No code to write and the highest review value — the profile of a skill whose worth rose. An agent cannot infer what must be atomic, because that is a domain fact, so it commits wherever the code reads tidily. |

Two of the brief's seven do not survive. **Observer** is cut to recognition
only: in-process Observer is synchronous, in-memory, unretried and unbounded and
propagates consumer exceptions to the publisher — a durable queue is none of
those. The cut is worth making rather than merely defensible, because an agent
asked for *an event system* produces exactly that shape and it looks right until
the first consumer crash. **Factory** is not promoted: naming a trivial function
after a pattern invites the hierarchy the name implies.

Seven more are actively harmful to cargo-cult, for reasons different enough to
separate.

| Pattern | Why cargo-culting it hurts now |
|---|---|
| Singleton | Global mutable state, hostile to testing and concurrency, and across processes simply a lie. Agents reach for it readily because it saturates the training data. |
| Abstract Factory | Speculative generality whose justification — changing it later is expensive — has collapsed. |
| Template Method | A labour saving bought with coupling. The saving is gone; the cost remains. |
| Visitor | Defensible in compilers, misapplied elsewhere. A dispatch dict says it plainly. |
| Mediator | Reliably degenerates into a god object. |
| Flyweight, Prototype, Interpreter | A memory cost that no longer binds; a deep copy; and *I am writing a language*, nearly always wrong solo. |
| Bridge | Indistinguishable from Strategy often enough that teaching both is hour tax. |

Eight are recognition-only at zero hours: Iterator, Facade, Proxy, Composite,
Builder, Chain of Responsibility, Memento and Observer. Three already appear
under other names — Chain of Responsibility *is* the middleware chain, Proxy is
part of the adapter, Memento is subsumed by *persist your state*. Recall value
is near zero while recognition value is undiminished, because recognition is
what lets you name a thing in a prompt and notice its absence in a review.

### The enterprise set and domain-driven design

Five enterprise patterns earn their place, at roughly two hours total, looked up
rather than read cover to cover.

| Pattern | Why it earns the hours |
|---|---|
| Gateway | Highest return. Each external API's weirdness — retry semantics, idempotency story, rate limit, error taxonomy — lives nowhere unless a gateway holds it, and an agent writing calls inline re-derives it per site, differently wrong each time. |
| Service Layer | What makes the outbox correct rather than merely present. Generated code writes the outbox row and the transition in two transactions: both are individually correct, and nothing in the diff signals they must be atomic. |
| Repository, narrow | A discoverable persistence contract keeps a module rebuildable; scattered inline queries make everything depend on everything. |
| Transaction Script | The brave call, because its economics genuinely moved. Reaching for a rich domain model always rested on the cost of changing one afterwards — a cost that has largely gone, while the comprehension it demands has not. A script is also the shape an agent edits most reliably: load, decide, transition, write, one sequence with no dispatch to chase. |
| Optimistic Offline Lock | Added, not on the brief's list. A version column turns the unanswerable question *did you think about concurrency?* into a mechanical check on the schema. |

Data Mapper and Unit of Work are concept-only, one rule each: keep domain
dataclasses distinct from ORM rows, because a type carrying both meanings gets
the harness edited when you asked for a persistence change; and the session
gives you the unit of work free. Domain Model is P2, earning itself where
invariants are real.

Domain-driven design is triaged to concept-only for a categorical reason rather
than a budgetary one. Strategic domain-driven design is an *organisational*
technology: bounded contexts, context maps and a ubiquitous language exist
because several teams disagree about what a word means, and a solo builder has
no such disagreement, so most of its value is structurally unavailable however
well it is taught. That argument survives scrutiny where a budget argument would
not. Three exceptions have real surfaces and cost minutes: aggregate boundary
equals transaction boundary equals consistency boundary, which makes the outbox
obviously correct rather than a memorised recipe; the anti-corruption layer,
named once so it is recognisable in the bad system at AR-02; and value objects
as newtypes, the one part whose worth has clearly risen. Concept-only treatment
collapses into *write some dataclasses* unless something forces the discipline,
which is what W02's aggregate and invariant table is for.

## How this track is proved

Track B leads eight of the twelve weeks, standing down across W05 and W06, where
retrieval takes the front, and across W10 and W11. Four hours are named outside
those weeks: 1.5 h at W07 for the Sentry lane's failure-mode taxonomy, which is
domain modelling wearing an operational hat, and 2.5 h at W12 for the third
review plus the multi-axis rubric formalising the W04 checklist.

The proof obligations divide cleanly. `D-w02-1` and `D-w02-2` are design
artifacts — the transition table, the aggregate and invariant table, the
regeneration test — and the only ones satisfiable by writing. Everything after
is behavioural: `D-w03-1` proves absorption under replay, `D-w08-1` that nothing
strands or duplicates under chaos, `D-w09-1` that the budget bounds spend under
an induced storm, and `D-m04-2` with `D-m04-3` that the outbox and the
compensations survive faults injected into themselves. `D-w08-2` and `D-w12-3`
carry the review work.

Ownership elsewhere: tasks and hours belong to the week files, stage definitions
and demo commands to the project files, the 14 defect classes to the review
exercise set. One absence is a decision, not an ownership line — formal methods
are refused at `LR-14` on budget, not on merit. Verifying a state machine is
what they are good for; they take weeks before returning anything, and this
track has none to give.
