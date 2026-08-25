# Case study

## When to use this

This is the answer to the objection that ends most early consulting
conversations: no case studies. It is written after any engagement that produced
a measurable change, and it is written the same way whether the work was paid,
free, or a demonstration built against a realistic workflow — the difference goes
in the label at the top, honestly, and nowhere else. Simulated work that is
tagged as simulated is a legitimate artifact and clears the bar. Simulated work
dressed as a client engagement is a failure of the programme, not a shortcut
through it.

Two sections are not optional. The baseline must be measured before anything is
built, using a stated method over a stated number of runs, and the after figure
must be produced by that same method. Estimating either end and reporting the
difference produces a number that says more about your expectations than about
the work; the free-pilot stage will not exit on it, and a buyer who has seen a
few of these will find the seam in one question. Second, the scope has to be
recorded as it was agreed before work started, because a case study whose scope
was written afterwards always describes exactly what was delivered.

Identities stay out of tracked files. A placeholder, the sector and a rough size
are enough for a reader to judge relevance, and this keeps the repository ready
to be made public without an editing pass. The version with real names lives in
a file ending `.local.md`, which is ignored.

## Template

Copy the block per engagement. Aim for something a prospect reads in two minutes
and a peer cannot poke a hole in — those pull in opposite directions, and the
resolution is to keep the narrative short and the measurement section precise.

Keep the section on what did not work. It is the section every reader believes,
and its absence is what makes the rest read as advertising; naming a limitation,
a case the automation refuses, or an assumption that turned out wrong costs
almost nothing and buys the credibility the other sections are asking for. If
the engagement genuinely produced no friction, that itself is the finding worth
writing down, and it is rare enough to be worth a sentence explaining why.

```markdown
# Case study — <the outcome, as a noun phrase>

- **Client:** <Client A — a placeholder, in every tracked copy>
- **Sector and size:** <industry, rough headcount>
- **Basis:** <paid engagement / free pilot / demonstration against a realistic
  workflow — labelled plainly and never upgraded>
- **Evidence tag:** <real / simulated>
- **Period:** <YYYY-MM> to <YYYY-MM>

## The problem

<Their workflow in their vocabulary, in two or three sentences.>

## Baseline, measured before the build

| Measure | Before | Method | Runs | Date |
| --- | --- | --- | --- | --- |
| <e.g. minutes per run> | <n> | <timed / counted / from system logs> | <n> | <date> |

<A row reading "estimated" means this section is not finished.>

## Scope, as written before work began

<What was in. What was explicitly excluded. Where it was recorded.>

## What was built

<Enough for a reader to judge the difficulty. Not a tour of the architecture.>

## After, measured the same way

| Measure | After | Same method | Runs |
| --- | --- | --- | --- |
| <measure> | <n> | <yes / no — if no, say why> | <n> |

## Result

<The change, with the sample it rests on, then the payback period in months.>

## What did not work

<At least one honest item: a refused case, a wrong assumption, a limit hit.>

## In their words

<A verbatim line, cleared for use, attributed to a role rather than a person.>
```
