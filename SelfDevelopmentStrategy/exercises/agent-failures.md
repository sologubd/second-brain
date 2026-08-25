# Agent failure exercises

Fourteen exercises whose purpose is to make an agent fail **on purpose, under
conditions you chose, while you are watching.**

Most curricula omit this, because a success demonstrates well and a failure does
not. The result is engineers who can build an agent that works and cannot say what
it does when the ticket is vague, the tool lies, the test is flaky, the document is
a year old, or the process dies halfway through. All five happen weekly in
production and none happens in a demo.

## The five parts

Every write-up names all five, and none of them is a sentence long:

1. **Detection** — how you know it happened.
2. **Safe failure behaviour** — what the system does instead of guessing.
3. **Recovery** — how it gets back to a good state.
4. **Logging** — the fields that make it *countable* across weeks, not just handled
   once.
5. **A test proving the mitigation.**

## The one rule that turns a report into evidence

**The proving test must go red against the code as it was before the fix.** Run it
on the parent commit first. If it does not fail there, you have not reproduced the
failure — you have written a test for behaviour you already had.

## The set

| # | Exercise | Week | Body |
|---|---|---|---|
| 1 | Ambiguous ticket | 01 | [week 01](../weeks/week-01.md#failure-exercise) |
| 2 | Flaky test | 02 | [week 02](../weeks/week-02.md#failure-exercise) |
| 3 | Partial tool failure | 03 | [week 03](../weeks/week-03.md#failure-exercise) |
| 4 | Misleading stack trace | 04 | [week 04](../weeks/week-04.md#failure-exercise) |
| 5 | Context loss after restart | 05 | [week 05](../weeks/week-05.md#failure-exercise) |
| 6 | Model timeout and nested retries | 06 | [week 06](../weeks/week-06.md#failure-exercise) |
| 7 | Cost exhaustion from a hostile input | 07 | [week 07](../weeks/week-07.md#failure-exercise) |
| 8 | Two agents on overlapping files | 08 | [week 08](../weeks/week-08.md#failure-exercise) |
| 9 | Conflicting requirements | 09 | [week 09](../weeks/week-09.md#failure-exercise) |
| 10 | Stale documentation | 10 | [week 10](../weeks/week-10.md#failure-exercise) |
| 11 | Indirect prompt injection | 11 | [ai-security](ai-security.md) |
| 12 | Confused deputy | 12 | [week 12](../weeks/week-12.md#failure-exercises) |
| 13 | Malicious tool output | 12 | [week 12](../weeks/week-12.md#failure-exercises) |
| 14 | Memory poisoning | M4–6 | [months 4–6](../later/months-04-06.md#security-exercises) |

Each body lives in the week that runs it, so the week file is self-contained. This
file exists for the four things below, which are true across all of them.

## Four extras, worth having anywhere

These did not fit a single week and are worth reaching for when you have spare
capacity or when a real incident suggests one.

**Unrelated CI failure.** Keep a red build that has nothing to do with your change
off the diff's record, and keep the agent from enlarging the change while hunting a
cause. Cross the changed file set with each job's declared input paths — computed,
not judged by eye. A job that went red touching none of them is a candidate. Forbid
edits outside the declared scope while any build is red: chasing an unrelated
failure produces a diff harder to review than the problem it was meant to solve.
Every job declares its inputs; a job declaring none is treated as related.

**Misleading code comments.** Find which source the agent believes when comment and
code disagree. Ask it to describe a function twice — once from the comment with the
body hidden, once the reverse — and diff the descriptions. Found this way a
disagreement is mechanical; looked for informally it is missed. Rank the body as
ground truth and the comment as an unverified assertion, and enforce that
deliberately: a comment is often the highest-signal text present, and its error is
inherited fluently and in full. Raise the disagreement as a *finding* rather than
quietly preferring a side.

**Crash between commit and external effect.** See
[months 4–6](../later/months-04-06.md). Inject at **every** point between the local
commit and the last outward call, not a sample.

**Compensation that fails.** Also months 4–6. Call every undo step twice in the
suite — repeatability claimed in a docstring is not asserted. Name at least one
effect that **cannot** be compensated, with what happens instead; a surface where
everything is reversible was described inaccurately.

## Two things that make a write-up worthless

**A summarised body.** A checker can only look for the five names once across a
document, so fourteen thin bodies would satisfy any mechanical check. Only a reader
catches it, and the reader is you in month 8 trying to remember what you actually
established.

**Detection by payload recognition.** A detector that only catches inputs it has
already seen is a denylist, and the next input walks past it. Detect *deviation from
a control*, not a known string. This applies well beyond the security exercises.

## What counts on the scoreboard

A failure scenario counts as *reproduced and mitigated* only when all five parts are
written **and** its proving test fails against the pre-mitigation code. A five-part
write-up with no red test is a document.
