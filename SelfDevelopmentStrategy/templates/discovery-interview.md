# Discovery interview script

## When to use this

The script is written in week three and rehearsed there, which is what lets the
call budget in week four be priced light — by the time a real call lands, the
questions are not being invented on the phone. Having it in existence and having
run it once is one of the exit conditions on `CS-1`, the simulated stage.

Its single discipline is that it does not sell. The purpose of the call is to
find out whether a problem is worth solving and whether this person can buy a
solution to it, and a pitch contaminates both answers: once someone knows you
have something to offer, they start describing their situation in terms of your
offer. So the questions ask about what already happened rather than what might.
The last time it ran, not how often it usually runs. What the attempted fix cost,
not whether a fix would be worth paying for. Money already spent is evidence;
money someone says they would spend is a courtesy.

Four of the nine scorecard dimensions can only be filled from a conversation —
frequency, labour cost, process predictability and willingness to pay — and the
call exists to fill them. The remaining sections gather what makes those four
defensible later.

Names stay out. Roles, industry and rough size are enough to score against, and
the repository is written to be publishable without a scrubbing pass. Anything
identifying belongs in a file ending `.local.md`, which version control ignores.

## Template

Copy the block per call. Leave the questions in their order: the workflow walk
comes first because people describe a process accurately before they have worked
out what you want to hear, and the cost questions come after because a number
given in the middle of a story is more honest than one given in the abstract.

Write their phrasing down rather than your paraphrase of it. The exact words a
person uses for their own problem are what makes a later case study or a cold
email sound like it came from inside their industry, and a summary written an
hour afterwards has already replaced their vocabulary with yours. Score the
opportunity afterwards, elsewhere, against the sentence that produced each
score — never on the call, where the temptation is to score the person's
enthusiasm rather than their process.

```markdown
# Discovery call — <Prospect A, or another placeholder>

- **Date:** <YYYY-MM-DD> · **Role:** <job title, never a name>
- **Shape:** <industry, rough headcount, no identifying detail>
- **Arrived via:** <cold send / follow-up / referral>

## Opening

<Thirty seconds: why you asked, how long you will take, that nothing is being
sold today. Then stop talking and let them start.>

## The workflow

1. Walk me through the last time <process> ran, start to finish.
2. Who touched it, and in what order?
3. Where did it stall?

## Frequency

- How many times did that happen last month?
- Was last month typical?

## Effort

- How long does one pass take, door to door?
- Whose hours are those? <role and seniority; loaded cost is computed later>

## Predictability

- How much of it is identical every time?
- What was the last exception that broke the routine?

## Data and access

- Where does the input arrive, and in what form?
- Which systems would have to reach each other for this to change?

## Consequence

- What happens when it goes wrong?
- What did that cost the last time it did?

## Prior spend

- What have you already tried?
- What did trying cost you?

## Close

<Ask what you failed to ask. Ask who else has this. Propose nothing.>

## Their words

<Verbatim phrases, in quotation marks. Not your summary of them.>

## Carried into scoring

Frequency <0–5> · labour cost <0–5> · predictability <0–5> · willingness to pay <0–5>

<Every score cites the sentence it came from, recorded in the scorecard.>
```
