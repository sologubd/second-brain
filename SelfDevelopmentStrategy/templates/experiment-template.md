# Experiment record

## When to use this

Open one whenever a change is supposed to make something measurably better and
the alternative is deciding by impression: one retrieval strategy against
another, a revised prompt, a chunk width, a model swap, a retry policy. The
discipline is three-part and none of the parts survives being skipped. Freeze
the baseline as a commit or tag before the first run, so the comparison cannot
drift underneath you. Change exactly one thing, because two changes and one
number tell you nothing about either. And state the metric as a fraction whose
denominator you wrote down in advance — a count with no denominator can be made
to rise by running more of whatever it counts.

Report the spread across reruns rather than a single figure. One run of a
non-deterministic system is an anecdote with a decimal point attached.

This file is also where the programme keeps its calibration for reflection
questions. These five are the shape every reflection is written against, not a
list to paste into one:

1. `XQ-1` — What failure mode did your original design miss?
2. `XQ-2` — What would fail under 10× load?
3. `XQ-3` — Which parts must be idempotent?
4. `XQ-4` — What authority should the agent not have?
5. `XQ-5` — What would you change before allowing this into production?

Each is answerable only by someone who built the thing. A question you could
answer from the reading alone has already failed the shape.

## Template

Copy the block. Number experiments in sequence and keep the discarded ones: an
experiment that failed to move its metric is the cheapest evidence you will ever
own, and deleting it guarantees someone repeats it in four months.

Fill the metric row before running anything. Writing the denominator down while
the result is still unknown is the whole control — chosen afterwards, it becomes
the denominator that makes the number look best, and you will not notice
yourself doing it. The decision line is likewise written to be uncomfortable:
adopt, discard, or rerun with one stated change, and nothing else counts as an
outcome. Recording a result without a decision is how a folder of experiments
turns into a folder of trivia.

```markdown
# Experiment NNN — <the single variable, named>

- **Date:** <YYYY-MM-DD>
- **Baseline:** <commit or tag, frozen before the first run>
- **Variable:** <the one thing that changed>

## Hypothesis

<A prediction that could come out false, with the expected direction of change.>

## Method

<What runs, over which inputs, how many times, and what is held constant.>

Sample: <n> items · Reruns: <n> · Held constant: <what>

## Metric

| Metric | Numerator | Denominator | Baseline | Result |
| --- | --- | --- | --- | --- |
| <name> | <what is counted> | <what it is counted over> | <value> | <value> |

## Result

<The figure, with its spread across the reruns. Note any run that errored.>

## Decision

<Adopt · discard · rerun with one stated change. Pick one and say why.>

## Reflection

1. <specific to this build>
2. <second>
3. <third>
```
