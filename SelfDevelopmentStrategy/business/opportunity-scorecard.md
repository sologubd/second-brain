# Opportunity scorecard — nine dimensions, scored on evidence

## Purpose

This file owns the nine scored dimensions and the instrument built around them.
Nine is a mandated count, not a preference: the brief names them, and canon
enforces the count, so nothing gets folded in and nothing gets quietly dropped.
Three further dimensions that research surfaced are documented below as a
supplement and are deliberately left unscored — adding them would break the
count the brief fixed.

The scorecard is applied twice in phase 1 — one opportunity in W06, a second in
W10 — and W10 turns it into a repeatable instrument rather than a re-derivation.
That distinction is the whole point. A scorecard rebuilt from memory on every
use is an opinion with a table around it, so what makes it examinable is
repeatability: score one opportunity twice, a month apart, and the two profiles
should land in the same place — any gap between them tracing to evidence that
arrived in between, never to a change of mood.

## The instrument

### The nine scored dimensions

Scored 0 to 5. Every score cites the evidence used, never intuition alone.

| Id | Dimension | Axis | What the score answers |
|---|---|---|---|
| OS-1 | Pain severity | value | What does the current process cost in money, error rate or missed opportunity? 0 is a mild annoyance; 5 is a named person's job measurably worse every week |
| OS-2 | Frequency | value | How often does it happen? The multiplier in every ROI calculation, and the most common place a plausible automation turns out worthless |
| OS-3 | Labor cost | value | Hours per occurrence times fully loaded hourly cost — salary times roughly 1.3 to 1.5. Buyers discount unloaded estimates as naive |
| OS-4 | Process predictability | feasibility | How rule-based and standardised is it? A process that differs every time is not automatable at this scale |
| OS-5 | Data availability | feasibility | Is the input machine-readable and reachable, or does it live in someone's inbox and head? |
| OS-6 | Integration feasibility | feasibility | Do the systems have APIs, and can the buyer actually grant access? Permission friction kills more pilots than technical difficulty |
| OS-7 | Buyer access | adaptation | Can you reach the person who decides? |
| OS-8 | Willingness to pay | adaptation | Is there an actual conversation or an observable signal behind it? Never an assumption |
| OS-9 | Market repetition | value | How many other businesses have this same shape of problem? The bridge from consulting to product |

OS-7 and OS-8 carry the `adaptation` axis because they are this programme's
addition to generic practice, and they are the two most likely to be scored
wishfully. OS-8 is what kill criterion KC-1 is written about: a problem called
annoying and then not paid for is the commonest way a promising score empties
out.

### How to score

1. Read the workflow document first. A dimension scored before the workflow
   exists is scored against a memory of a conversation.
2. Write the evidence beside the number — a quotation, a document reference or
   an observed signal, one line per dimension.
3. With no evidence, still score it, and mark it `assumed`. An assumed score is
   legitimate; an assumed score dressed as an evidenced one is not.
4. Never average the nine. The profile's shape carries the decision, and a mean
   hides a 0 on OS-6 behind four 4s.
5. Re-score rather than adjust, and keep both scorings.

### Three supplementary dimensions, documented and not scored

These came out of research, they are real, and they are **not** part of the
scored nine. They are recorded here so that a reader who notices their absence
finds a decision rather than an oversight.

| Supplement | Why it is worth naming | Why it is not scored |
|---|---|---|
| Exception-handling burden | How many edge cases the manual process carries, and how much judgement it needs, is usually its own criterion in automation practice rather than being folded into predictability | Folding it in would change what OS-4 means; adding it would make ten |
| Change and maintenance risk | Whether the target process or its underlying systems are likely to change soon decides whether the automation stays valuable, which is a different question from whether it works | Same. It is a durability question, and the nine are a viability set |
| Compliance and risk sensitivity | Some processes are automation-unfriendly regardless of value, because an error carries regulatory or reputational cost | It does not appear in the nine at all, so folding it anywhere would be an invention rather than a refinement |

Use them as a written sanity note beside the scored profile. If a supplement
would have changed the decision, say so in the note — that is exactly the signal
worth having when the scorecard is next revised.

### The industry cross-check

Established automation practice distils many sub-criteria into two axes, usually
drawn as a two-by-two: business value — volume and frequency, labour cost, error
rate, strategic importance — against feasibility — rule-based-ness,
standardisation, a stable environment, data availability, low exception-handling
need. The brief's nine map onto it cleanly, and buyer access plus willingness to
pay is a genuine adaptation rather than a gap: that body of practice assumes an
in-house team whose buyer is already in the building.

## Exercises

### Exercise 1 — score one opportunity on all nine

#### Objective

Produce a scored profile whose every number can be defended by pointing at
something, so that the decision rests on evidence rather than on enthusiasm.

#### Task

Take one automation opportunity from the W06 workflow material, score all nine
dimensions with an evidence line each, then bucket the same opportunity into the
value-by-feasibility two-by-two and say which framing you trust where they
disagree.

#### Constraints

Evidence per dimension, cited rather than recalled. No aggregate score, no
industry-average figure standing in for a measured one, placeholder identity in
the tracked copy.

#### Deliverable

D-w06-4 — one opportunity scored on all nine dimensions with per-dimension
evidence, produced by T-w06-13 alongside that week's send log.

#### Acceptance criteria

- All 9 dimensions carry a score in the 0 to 5 range and an evidence line; 0 dimensions are left blank.
- 0 unevidenced scores lack the `assumed` marker, and the artifact states how many of the 9 are assumed.
- The artifact contains 0 aggregate or averaged scores.
- The two-by-two placement is recorded, and 0 disagreements with the nine-dimension profile are left unnamed.

#### Metrics

Evidence coverage = dimensions carrying cited evidence ÷ 9, reported as a
fraction so the denominator stays visible. A first scoring at 4 of 9 is normal,
and it names the five questions the next conversation has to answer.

#### Reflection questions

1. Which dimension did you most want to score high on thin evidence, and what
   would earn that score honestly?
2. Where the two-by-two and the nine disagreed, what would have to be true for
   the framing you rejected to be the right one?
3. Which single dimension, scoring 0, would make the other eight irrelevant —
   and did you check it first?

### Exercise 2 — the reproducibility test

#### Objective

Prove the scorecard is an instrument by showing that two people, or the same
person a month later, reach the same profile from the same evidence.

#### Task

Re-score the W06 opportunity in W10 from the recorded evidence alone, without
looking at the original scores, then compare and account for every dimension
that moved.

#### Constraints

The original scores stay covered until the re-score is done. Movements caused by
new evidence are recorded apart from movements with none behind them — those are
the instrument failing, not the opportunity changing.

#### Deliverable

D-w10-4 — the pain-scoring model and pain register, with a second opportunity
scored and the reproducibility comparison attached.

#### Acceptance criteria

- Both scorings exist as separate artifacts, and all 9 dimensions are compared pairwise.
- Every dimension that moved names its cause as new evidence or as scorer drift; 0 movements stay unclassified.
- At most 2 of 9 dimensions move without new evidence, or the scoring rubric is rewritten and the rewrite is recorded.

#### Metrics

Number of qualified pains in the register, and drift = dimensions moving without
new evidence ÷ 9. Both are reported per opportunity rather than pooled, because
pooling two opportunities hides which one the instrument struggled with.

#### Reflection questions

1. Which dimension's wording caused the drift, and how would you rewrite it so
   the next scorer cannot read it two ways?
2. Does the profile change if you exclude every row sourced from simulated
   Stage-1 work?
3. What would a second person need, beyond this file, to land in the same place?

## Targets and thresholds

Two opportunities are scored across the twelve weeks, in W06 and W10. That is
derived rather than lowered: a third scoring would need a third documented
workflow, and the funnel does not produce one inside the hours available.

The prototype gate that consumes these scores is not owned here — it is CL-6, in
[SaaS validation](saas-validation.md), which states its three conditions and its
refusal branch in full. What matters on this side is what the gate demands of
the scorecard: a top-3 placement earned across all nine dimensions with cited
evidence, and OS-7 and OS-8 grounded in something a person actually said or did.
Ranking requires the pain register, which is not assembled until W10, so no
amount of promise in a W06 profile can open the gate early.

## Evidence discipline

Every scored opportunity carries `evidence_source: real | simulated` at artifact
level and, more usefully, per dimension. A score from a real discovery call and
one from a Stage-1 simulated workflow document are not the same evidence, and a
profile mixing them silently overstates itself. SM-19 in
[the scoreboard](../SCOREBOARD.md) carries the qualified-pain count with the tag
attached.

Inventing evidence is the failure this instrument exists to prevent, and OS-8 is
where the temptation concentrates. A dimension marked `assumed` is an honest
deliverable that tells the next conversation what to ask; the same dimension
carrying a fabricated quotation is a programme failure no later measurement
undoes, because the register it poisons is what the SaaS verdict reads.

Company names, quoted conversation and prices stay in gitignored `*.local.md`
files. The tracked scorecard uses a placeholder identity, and
`templates/automation-audit.md` is written the same way so a filled-in audit can
be committed without a scrub.
