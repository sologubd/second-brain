# Architecture decision record

## When to use this

Reach for this when a choice will be costly to reverse and easy to forget you
made: a storage engine, a boundary drawn between two services, an authorization
model, the span of an agent's permissions. Each architecture review ends in one
— `AR-01` against the platform at its second stage, `AR-02` against a system you
did not write and did not choose, `AR-03` against the finished platform — and
the migration decision in month eight is the fourth. Together they form the
collection that `PF-04` points at.

A record written afterwards is a justification wearing the costume of a
decision. Draft it while the options are still live and you can still say what
you did not know at the time. Where the answer is already obvious the record
runs short, which is fine; what it must never do is stage a weighing whose
result was settled before the file was opened.

The defect checklist is the part that earns the file its place. Fourteen
classes, each with a detection question stated in full in
[the architecture reviews](../exercises/architecture-reviews.md). Run them at the
decision you just took rather than at the system in general, and log what they
turn up rather than marking fourteen rows clean. `AR-03` is blunt about this: a
review finding nothing is the least believable result it could return.

Not every choice deserves one. A decision that a single afternoon could undo,
or that only one file can see, belongs in a commit message. The test is whether
someone arriving in four months would ask why, and whether the answer would cost
them a day to reconstruct from the code. If both, write the record.

## Template

Copy the block. One record per decision, one file per record, numbered in the
order they were taken and never renumbered — a superseded record stays where it
is and points forward, because the reasoning that was later overturned is
usually the most instructive part of the collection.

Two habits are worth forming while the template is still blank. Put the cost of
the chosen option in `Why chosen` rather than in `Alternatives considered`,
where it is easy to leave out; a record whose selected option has no stated
price has not finished thinking. And date the follow-ups against a week or a
month rather than leaving them open, since an undated follow-up is how an
accepted defect quietly becomes a permanent one.

```markdown
# ADR NNN — <the decision as a noun phrase>

- **Status:** <proposed | accepted | superseded by ADR NNN>
- **Date:** <YYYY-MM-DD>
- **Decides for:** <the system, stage or module this binds>

## Decision

<One sentence, active voice, saying what will be done.>

## Drivers

<What forced a choice now — the constraint, the load, the failure, the deadline.>

## Alternatives considered

| Option | What it buys | What it costs | Verdict |
| --- | --- | --- | --- |
| <option> | <benefit> | <price> | <rejected because …, or chosen> |

## Why chosen

<The trade, named as a trade. What you gave up belongs in this section.>

## Consequences

<What is now true that was not before, the unwelcome parts included.>

<What this forecloses, and what it makes harder for whoever comes next.>

## Follow-ups

- [ ] <action> — <owner> — <the week or month it lands>

## Defect checklist

Run against this decision, not the whole system. Record findings; do not clear rows.

- [ ] `DC-01` unnecessary abstractions — <finding, or not applicable>
- [ ] `DC-02` accidental coupling — <finding, or not applicable>
- [ ] `DC-03` shallow modules — <finding, or not applicable>
- [ ] `DC-04` wrong boundaries — <finding, or not applicable>
- [ ] `DC-05` primitive obsession — <finding, or not applicable>
- [ ] `DC-06` duplicated logic — <finding, or not applicable>
- [ ] `DC-07` incorrect state modeling — <finding, or not applicable>
- [ ] `DC-08` non-idempotent operations — <finding, or not applicable>
- [ ] `DC-09` hidden distributed transactions — <finding, or not applicable>
- [ ] `DC-10` race conditions — <finding, or not applicable>
- [ ] `DC-11` failure recovery problems — <finding, or not applicable>
- [ ] `DC-12` unbounded retries — <finding, or not applicable>
- [ ] `DC-13` authorization leaks — <finding, or not applicable>
- [ ] `DC-14` excessive agent permissions — <finding, or not applicable>
```
