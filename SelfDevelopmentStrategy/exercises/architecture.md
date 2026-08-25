# Architecture reviews

Three reviews across the twelve weeks, in two modes. Two are **self-inspection** —
you review what you built. One works on a **deliberately bad system somebody else
wrote**, because reviewing your own code only ever demonstrates that you can
describe your own choices favourably, and finding a defect somebody else planted is
the harder and more transferable skill.

## The four questions

The instrument is a set of questions, not a set of names. Asked of any function:

- **Repeat it.** Call it twice and say what differs.
- **Interrupt it.** Kill the process between two adjacent statements and say what
  survives.
- **Collide it.** Run two copies concurrently and say who wins.
- **Name its assumptions.** State what this code believes about a system it does not
  control, that nothing in the file records.

None of the four can be answered by reading for style, and that is the entire point.
**Generated code is syntactically clean, idiomatic, well-named and consistently
formatted, so every signal a reviewer habitually leans on now reports green.** The
defects moved; they did not disappear. They sit at repetition, at crash windows, at
concurrency and at unstated external contracts — precisely where reading does not
look and where these four questions do.

## What a finding looks like

Four parts, and it is worthless without any of them: the **class**, the
**location**, the **evidence**, and the **consequence** if nobody fixes it.

Evidence is ranked, and the ranking matters more than it looks:

1. **A reproduction** — a second call that produces a second effect, an injected
   process death that loses one, two concurrent runs that disagree. The strongest,
   and the only kind that cannot be argued with.
2. A line-level citation with an argument.
3. An impression. Not evidence. Does not enter the record, however experienced the
   reviewer.

The same discipline applies to a class you mark **absent**. Absence has two very
different causes — the defect genuinely cannot occur because of something you built,
or the surface where it would appear does not exist yet. Those are not the same
claim, and a review that conflates them reports a system getting safer when it is
only staying small.

## The two modes fail differently

**Self-inspection fails by charity.** You know why every decision was made, so a
defect reads as a tradeoff and the review becomes a justification with headings. The
counter is the checklist: a question you must answer *in writing* has no room for
the reason you already believe.

**The supplied-system review fails by fluency.** The code reads well, so the
reviewer's confidence rises while their evidence does not, and the review converges
on style notes. The counter is the reproduction requirement: at least two findings
must survive being *run*, not merely being argued.

Both modes are here rather than either. They are not two difficulty levels of one
exercise; they are two failure modes of the same reviewer, and each is invisible from
inside the other.

## The fourteen defect classes

Each carries a **detection question**, and the question is the usable part. Several
shifted meaning under generated code, and where they have, the shift is stated.

| # | Class | Detection question |
|---|---|---|
| 1 | Unnecessary abstractions | Does this interface have exactly one implementation and no second one in prospect? Speculative generality used to be justified by *changing it later is expensive*; later is now cheap, so the rule of three got **stronger**, not weaker. |
| 2 | Accidental coupling | If I deleted this module and regenerated it from its contract alone, what would the regeneration get wrong? Every answer names a coupling the type system does not show. |
| 3 | Shallow modules | What is the ratio of public symbols to implementation size? A module whose interface is as large as its body has hidden nothing. |
| 4 | Wrong boundaries | Does a single behaviour change require edits in two modules? Then the boundary is misplaced however clean each side looks. |
| 5 | Primitive obsession | Is a domain concept carried as a bare `str` or `int`? This costs more than it used to: a frozen newtype carries semantics to an agent at the call site, and a bare string carries none. |
| 6 | Duplicated logic | Is the duplicated thing an **implementation** or a **decision**? Duplicated implementations are cheap now and often preferable. Duplicated *decisions* — a business rule, a key format, a transition table, a retry classification — are more dangerous than ever, because three copies get regenerated separately and drift silently. |
| 7 | Incorrect state modeling | Is there a state the code can reach that the transition table does not list? Is there a listed transition no code performs? Both are defects and only the first is usually looked for. |
| 8 | Non-idempotent operations | What happens on the second call? Ask it of **every** side-effecting function, because the test suite asked it of none. |
| 9 | Hidden distributed transactions | Does any path commit locally and then call an external system? That is a crash window, and no test that does not kill the process between those two statements will ever find it. |
| 10 | Race conditions | What happens if two of these run at once — specifically, is there a read-modify-write with no conditional update, version column or row lock? An agent writes read-modify-write by default, because it is the readable form. |
| 11 | Failure recovery problems | If the process holding this work dies, who notices and how? If the answer is a timeout, what distinguishes slow from dead, and what happens when that guess is wrong? |
| 12 | Unbounded retries | Is there an **aggregate** budget, or only per-layer counts? Three layers retrying three times each is twenty-seven calls to a service already failing — and on a flat-rate plan the failure mode is a silent stall, not an error. |
| 13 | Authorization leaks | Is the permission check applied **before or after** ranking, filtering or counting? Post-filtering leaks existence through result count, latency and ranking even when content is withheld, and a test asserting *no unauthorized content returned* passes anyway. |
| 14 | Excessive agent permissions | Does this agent hold the union of every permission any of its steps ever needed? Can a low-privilege step cause a high-privilege step to act without re-checking the original human request? |

## The three reviews

### Review #1 — self, the platform so far · week 5

Write the checklist **first**, built around the four questions, and version it so a
later review can be compared against this one. Then apply it to the platform as it
stands, including to that week's own diff. Record each of the fourteen classes as
present or absent, with the evidence that decided it.

*Done when:* the checklist is versioned and carries ≥4 question categories; the ADR
names ≥3 classes with cited evidence rather than ticks; applying the checklist to
the week's own diff produced ≥1 finding; 100% of findings name their class.

### Review #2 — the supplied bad system · week 8

Review `SUP-01` (below) against all fourteen classes. **Do not read its
planted-defect list until your review is written and committed.**

*Done when:* all 14 classes assessed as present or absent; ≥4 of its 6 planted
defects found before consulting the list; ≥2 findings supported by a
**reproduction** rather than reading; 100% of identified defects cite a line range.

### Review #3 — self, the full platform · week 12

Formalise the four questions into a **five-axis rubric** — correctness under
repetition, crash-window durability, concurrency, contract and boundary assumptions,
privilege — scored independently, each with its own citation. One aggregate verdict
is a different instrument and does not satisfy this.

**Name at least two defects you are accepting**, each with a remediation *month*,
not an intention. A clean bill of health on a system this size is the least credible
possible output and fails on that ground alone. Every review-#1 finding is marked
remediated, accepted or re-reported — none dropped silently.

## The supplied systems

Two runnable Python files in [`supplied-systems/`](supplied-systems/), standard
library only, no environment needed.

**`sup01_task_runner.py`** — ~400 lines that read jobs from a table, call two
external services and write results back. Idiomatic, fully type-annotated,
well-named; would pass any linter. Broken in six of the fourteen ways.

```sh
python3 sup01_task_runner.py --init --seed 5
python3 sup01_task_runner.py --run     # expects two local HTTP stubs on the
                                       # ports named at the top of the file
```

Standing up two trivial stubs is itself part of the review, because **what the
runner does when those stubs misbehave is the question.**

**`sup02_knowledge_assistant.py`** — ~300 lines serving two tenants from one index.
Clean, readable, tested. Four defects, and it is deliberately the same shape as your
own retrieval agent seen from the outside — recognising in a stranger's code the
mistake you were shown in your own is a different and harder skill than avoiding it
once.

```sh
python3 sup02_knowledge_assistant.py --self-check
```

That prints the citations and result count for the same question asked by two
different users. **Record both numbers before forming any opinion.** They are data,
and one of them is a finding.

Neither file contains a mistake that *reads* as a mistake. No bare `except`, no
commented-out block, no obviously wrong name. Every defect survives a careful read by
someone looking for defects — which is the property that makes them worth the hours.

<details>
<summary><strong>Planted defect lists — do not open before your review is committed</strong></summary>

`sup01_task_runner.py`: classes 3, 6, 8, 9, 10, 12.

`sup02_knowledge_assistant.py`: classes 1, 5, 13, 14.

</details>

## Design patterns, as vocabulary

Not a memorisation goal. These seven are kept because of what they do to *generated*
code, and that distinction is load-bearing: it is easy to say why a pattern is
obsolete and hard to say what about one got more valuable.

| Pattern | Surface here | Why it matters when a machine writes the code |
|---|---|---|
| **Strategy** | the harness adapter, two implementations | It governs the size of an instruction. Asked to *add a second harness* with no seam present, an agent edits every call site, because nothing marks which are the vendor boundary. Named, the request is one file against one contract. |
| **Adapter** | typed invoke / capture / report | The sharpest constraint, and it runs against the model's instinct: asked to unify two APIs it **converges** them, because smoothing differences is what *unify* means in its training distribution and a smaller interface reads as cleaner in review. Here the differences **are** the measurement, so the instruction must be *expose these differences as typed fields* — otherwise you get a beautiful interface that silently deleted your experiment, and the deletion never shows up as a bug because everything still runs. |
| **State-as-data** | the task state enum and transition table | A transition table is a machine-checkable specification, so the invalid-transition suite is generated rather than written. Ask an agent for *a state machine* and you get the class-per-state form, which dies with the process. |
| **Command** | the task record as a reified, replayable command | Reification makes an agent's work auditable, which is what you need precisely when you did not write the code. Generated orchestration passes closures around because that is idiomatic Python — and a closure cannot be serialised, inspected in a database, rendered in an approval payload, or compensated after the fact. The work unit is also nondeterministic: *run it again* produces a different run; *replay this command* preserves the intent. |
| **Decorator** | the retry / timeout / limiting middleware chain | Cross-cutting concerns are what an agent bolts on inline, each addition locally correct. **Order is the entire semantics** — a limiter below the retry cannot bound a budget. |
| **Repository** | a typed collection-like boundary over persistence | A regeneration argument. Given raw ORM access an agent writes queries everywhere until the persistence contract is undiscoverable. Asked for *a repository* it returns a generic one over the ORM: an abstraction over an abstraction. |
| **Gateway** | one place per external API | Highest return of the enterprise set. Each external API's weirdness — retry semantics, idempotency story, rate limit, error taxonomy — lives nowhere unless a gateway holds it, and an agent writing calls inline re-derives it per site, differently wrong each time. |

Three more from the enterprise set, worth about two hours of targeted lookup:

- **Service Layer** — what makes the outbox *correct* rather than merely present.
  Generated code writes the outbox row and the transition in two transactions: both
  individually correct, and nothing in the diff signals they must be atomic.
- **Transaction Script** — the brave call, because its economics genuinely moved.
  Reaching for a rich domain model always rested on the cost of changing one
  afterwards, and that cost has largely gone while the comprehension it demands has
  not. A script is also the shape an agent edits most reliably: load, decide,
  transition, write, one sequence with no dispatch to chase.
- **Optimistic Offline Lock** — a version column turns the unanswerable question
  *did you think about concurrency?* into a mechanical check on the schema.

**Transaction boundaries** are not a pattern and carry the highest review value of
anything here: no code to write, and an agent cannot infer what must be atomic
because that is a domain fact — so it commits wherever the code reads tidily.

**Actively harmful to cargo-cult.** Singleton (global mutable state, and across
processes simply a lie — agents reach for it readily because it saturates the
training data). Abstract Factory (speculative generality whose justification
collapsed). Template Method (labour saving bought with coupling; the saving is gone,
the cost remains). Visitor, Mediator, Bridge, Flyweight, Prototype, Interpreter.

**Observer, cut to recognition only** — and worth stating why, because an agent asked
for *an event system* produces exactly this shape and it looks right until the first
consumer crash: in-process Observer is synchronous, in-memory, unretried, unbounded,
and propagates consumer exceptions to the publisher. A durable queue is none of
those.

**Recognition only, zero hours:** Iterator, Facade, Proxy, Composite, Builder, Chain
of Responsibility, Memento. Three already appear here under other names — Chain of
Responsibility *is* the middleware chain, Proxy is part of the adapter, Memento is
subsumed by *persist your state*. Recall value is near zero; recognition value is
undiminished, because recognition is what lets you name a thing in a prompt and
notice its absence in a review.

**Domain-driven design, concept only** — for a categorical reason rather than a
budgetary one. Strategic DDD is an *organisational* technology: bounded contexts,
context maps and a ubiquitous language exist because several teams disagree about
what a word means, and a solo builder has no such disagreement, so most of its value
is structurally unavailable however well it is taught. Three exceptions have real
surfaces and cost minutes: **aggregate boundary = transaction boundary = consistency
boundary**, which makes the outbox obviously correct rather than a memorised recipe;
the **anti-corruption layer**, named once so it is recognisable in `SUP-01`; and
**value objects as newtypes**, the one part whose worth has clearly risen.

## ADR shape

Four headings. That is the whole template.

```markdown
# ADR-00N — <decision, stated as a decision>

## Context
What is true that forces a choice. Include the measurement if there was one.

## Decision
What you are doing. Present tense, active.

## Alternatives considered
Each with the reason it lost. An ADR with no rejected alternative recorded a
preference, not a decision.

## Consequences
What gets harder. Name at least one. Defects you are accepting go here, with a
remediation month.
```
