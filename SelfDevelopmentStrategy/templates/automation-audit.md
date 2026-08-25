# Automation audit

## When to use this

Use it to write down a real workflow in enough detail that it can be scored and
priced. Two things come out of a completed audit: a document that could be shown
to a stranger as evidence you can take a process apart, and the inputs to the
nine-dimension scorecard, which is useless when fed impressions. The simulated
stage requires at least one such document reconstructed from public information
alone, with steps named, frequency estimated and time cost estimated, so the
first of these is written before any real workflow is available to observe.

The step table does the load-bearing work. Time and money are computed from it
rather than guessed at the end, which is why every step carries who performs it,
what system it happens in and how long it takes. A workflow described in a
paragraph always sounds automatable; the same workflow in rows usually reveals
two steps that are judgement calls and one that depends on an inbox.

Loaded cost, not salary. Multiply by somewhere between 1.3 and 1.5 and say which
multiplier you used, because buyers discount unloaded estimates as the work of
someone who has never carried a payroll. State the source of every figure beside
it — observed, counted, or taken from what someone said — since the difference
between those three is the difference between a defensible payback period and a
number that collapses in the first conversation about it.

Three further considerations get recorded and deliberately not scored: how much
exception handling the process demands, how likely the surrounding systems are
to change, and whether errors carry regulatory or reputational weight. They sit
outside the nine because the count of nine is fixed, not because they are minor.

## Template

Copy the block per workflow. Score after the table is complete, never alongside
it, and cite the specific observation behind each score rather than reasoning
from the total. The scale runs zero to five in every row.

Run the quadrant crosscheck even when it feels redundant. Bucketing the same
opportunity into value against feasibility and then asking where the two
framings disagree catches the failure the nine dimensions are individually blind
to: a high total assembled from strong value scores and weak feasibility scores
describes an opportunity that is worth a great deal and cannot be built. When
they disagree, say which one you believe and what would settle it.

```markdown
# Workflow audit — <workflow name>

- **Date:** <YYYY-MM-DD> · **Subject:** <Company B, or a named public source>
- **Basis:** <observed / interviewed / reconstructed from public information>

## Steps

| # | Step | Who | System | Minutes | Where it stalls |
| --- | --- | --- | --- | --- | --- |
| 1 | <step> | <role> | <tool> | <n> | <stall, or none> |

## Volume

Runs per month: <n> — <counted how>
Minutes per run: <n> — <summed from the table above, or observed>

## Current cost

Loaded hourly rate: <amount> — <salary times the multiplier you chose>
Annual cost: <hours> h × <amount> = <amount>

## Score

| Dimension | Axis | Score | Evidence |
| --- | --- | --- | --- |
| `OS-1` pain severity | value | <0–5> | <observation> |
| `OS-2` frequency | value | <0–5> | <observation> |
| `OS-3` labour cost | value | <0–5> | <observation> |
| `OS-4` process predictability | feasibility | <0–5> | <observation> |
| `OS-5` data availability | feasibility | <0–5> | <observation> |
| `OS-6` integration feasibility | feasibility | <0–5> | <observation> |
| `OS-7` buyer access | adaptation | <0–5> | <observation> |
| `OS-8` willingness to pay | adaptation | <0–5> | <observation> |
| `OS-9` market repetition | value | <0–5> | <observation> |

## Crosscheck

Quadrant: <value high or low> × <feasibility high or low>
Disagreement with the nine: <where, which framing you trust, what would settle it>

## Return

Build estimate: <hours> · manual time remaining per run: <minutes>
Annual saving: <amount> · payback: <months>

## Recorded, not scored

<Exception handling the process demands. What in the surrounding systems is
likely to change. Regulatory or reputational exposure carried by an error.>

## Verdict

<Pursue / park / drop — and the threshold that decided it.>
```
