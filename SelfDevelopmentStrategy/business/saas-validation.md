# SaaS validation — seven thresholds, five kill criteria, and a passing non-verdict

## Purpose

This file owns the evidence thresholds and the kill criteria, and it owns the
one rule that makes both of them worth having: the framework is allowed to
return *no decision*. "Insufficient evidence, deferred to month 05" is a
**passing deliverable**, provided it says which threshold is short of evidence
and names the month in which that evidence could realistically arrive.

That permission is not softness. A framework obliged to produce a score will
produce one, leaning the way its author already wanted — which, after twelve
weeks of building toward a product, is forward. Saying "not enough to decide
yet" also removes the pressure to manufacture evidence when the funnel
underdelivers, and underdelivery is the expected case here.

The instruments are built in phase 1 and applied afterwards. Track F is thin on
purpose: it consumes evidence the consulting work is still producing, and a
scorecard built before that evidence exists is scored on assumptions — the exact
failure these criteria are for. The ordered chain from interviews to
productization is Track F's own; the two gates at the end of it live here.

## The instrument

### The seven evidence thresholds

Every N is resolved to a concrete number, because a parameterised N inside a
plan that must fit fifteen hours a week is an unmade decision. W11 may raise
these on evidence; lowering any of them requires a canon delta.

| Id | Threshold | N | Why that number |
|---|---|---|---|
| ET-1 | Customer interviews | 8 | Below 8 independent conversations, the same pain appearing twice is as likely to be coincidence as signal. 8 is also roughly what this funnel could plausibly produce by month 07 at a mid-range reply band — demanding without being unreachable |
| ET-2 | Problem observed repeatedly | 3 | The same shape of pain in 3 INDEPENDENT businesses. Not 3 mentions by one buyer, and not 3 businesses introduced by the same source |
| ET-3 | Users willing to pilot | 3 | Two can be politeness from a warm-ish contact. Three independent yeses is the smallest number where one no does not collapse the evidence |
| ET-4 | Payment or strong purchase commitment | 1 | Money is the only evidence in this framework that politeness cannot produce. One is enough because it is categorical, not statistical |
| ET-5 | Clear acquisition channel | no count | A named channel with a MEASURED cost per conversation, taken from this programme's own funnel — which is itself a reachability experiment. A channel that has not been measured is a hope |
| ET-6 | Estimated ROI | no count | Computed from a measured baseline by the fully-loaded method and expressed as a payback period in months. An industry-average percentage does not satisfy this |
| ET-7 | Manual workflow proven first | 1 | At least one concierge delivery, by hand. Fail to produce the outcome by hand for a single customer and all automation buys you is an industrialised way of failing |

ET-5 and ET-6 carry no count because a count is the wrong instrument: both are
satisfied by a measurement existing at all, and a number would invite repetition
rather than one measurement made properly.

### The five kill criteria

Each one is written with its detection rule attached, because a kill criterion
you cannot observe is a worry rather than a criterion.

| Id | Criterion | How it is detected |
|---|---|---|
| KC-1 | People say the problem is annoying but will not pay | Interview notes record enthusiasm and no budget signal across at least 3 conversations |
| KC-2 | The workflow differs completely between companies | The documented workflows share fewer than half their steps, so any product is really N bespoke builds |
| KC-3 | Acquisition cost is obviously too high | This programme's own measured funnel implies a cost per qualified conversation exceeding a plausible first-year contract value |
| KC-4 | Integration permissions make deployment impractical | Two or more prospects cannot or will not grant the access the automation requires |
| KC-5 | An existing product already solves 90% of the pain cheaply | Competition analysis finds a product at a price the buyer would accept, covering the workflow's main path |

### Prototype decision gate

CL-6, and the last gate before anything gets built. Three conditions, all
required at once:

1. The opportunity sits above the shortlist threshold on all nine scorecard
   dimensions, with evidence cited per dimension.
2. No kill criterion fires.
3. The buyer-access and willingness-to-pay scores rest on an actual conversation
   or an observable signal, not on an assumption.

The gate has an explicit **no** branch, and that branch is the likely one.
Prototype opportunities are the single funnel row where the honest answer
through phase 1 is usually zero, and a gate with no way to say no is a
formality with a checkbox on it.

## Exercises

### Exercise 1 — resolve every N

#### Objective

Replace each placeholder with a number you can defend against the number next to
it, so the thresholds become a decision instead of a template.

#### Task

Restate each N as a concrete figure and write one line per threshold saying why
that number rather than a neighbouring one. Where the default already holds, say
what evidence would justify raising it.

#### Constraints

No N drops without a canon delta. ET-5 and ET-6 stay countless and the write-up
says why. Every justification points at this programme's own funnel or a stated
piece of evidence, never at a general industry figure.

#### Deliverable

D-w11-4 — the seven thresholds resolved to concrete numbers alongside the offer
sketch, produced by T-w11-12.

#### Acceptance criteria

- All 7 thresholds carry either an integer or an explicit `no count`, and 0 placeholders remain.
- Each of the 7 carries a one-line justification naming why that figure rather than its neighbour.
- Any threshold raised above canon's default states the evidence that justified the raise; 0 thresholds are lowered.

#### Metrics

Attainment = thresholds currently met ÷ 7, recomputed at each application. A
fraction rather than a verdict is what lets month 05 see whether the evidence
moved at all.

#### Reflection questions

1. Which threshold would you most like to lower, and what does that impulse tell
   you about the evidence you actually have?
2. ET-4 asks for one payment. Why is one enough here when three conversations
   are needed for ET-2?
3. Which threshold will this programme's funnel probably never satisfy, and is
   that a fact about the niche or about the channel?

### Exercise 2 — issue a verdict, or refuse to

#### Objective

Practise the harder half of a decision framework: returning "not yet" with
enough precision that someone can act on it.

#### Task

Apply the five kill criteria to the top candidate in the pain register and issue
a verdict — or, where the evidence will not support one, an explicit non-verdict
naming each missing threshold and when it could be obtained.

#### Constraints

Specific thresholds and specific dates: "more research needed" is not a
non-verdict, it is the absence of one. No criterion is skipped for want of
evidence — an unevaluable criterion is recorded as unevaluable, with its reason.

#### Deliverable

D-w12-4 — the SaaS verdict, or the explicit non-verdict, issued against the five
kill criteria by T-w12-13. Where it defers, the absent evidence is both named
and given a date.

#### Acceptance criteria

- All 5 kill criteria are evaluated or explicitly marked unevaluable with a reason; 0 are silently skipped.
- If the output is a non-verdict, it names at least 1 specific unmet threshold and 1 date, and it passes on those terms.
- 0 register rows behind the decision lack an `evidence_source` tag, and the artifact states how many of them are simulated.

#### Metrics

Number of qualified pains in the register, and the fraction of register rows
tagged real rather than simulated. A verdict resting on a register that is
entirely simulated is reportable as exactly that, which is more useful than a
verdict that does not say.

#### Reflection questions

1. Which kill criterion came closest to firing, and what one piece of evidence
   would settle it either way?
2. If you issued a non-verdict, what would you have concluded had you forced a
   score — and would that conclusion have been the one you wanted?
3. What would have to be true in month 05 for this to become a verdict, and who
   would have to say it?

## Targets and thresholds

Phase 1 reaches link three of Track F's chain at best — scored opportunities
with per-dimension evidence — and links four to six live in months 05 through
09, contingent on the funnel. Saying plainly that the chain probably stalls
there is more useful than a plan assuming it does not.

Three artifacts are targeted: the pain-scoring model and register in W10, the
seven thresholds resolved in W11, the verdict or non-verdict in W12. CS-5 is not
reachable inside phase 1 and is not scheduled as though it were.

On the shortlist threshold the gate rests on: the shortlist is the top 3
candidates in the pain register, and the register is not assembled until W10. No
amount of promise in a W06 profile opens the gate early, and that ordering is
protection rather than delay.

## Evidence discipline

Every register row and every threshold assessment carries `evidence_source: real
| simulated`, and the counts are reported rather than blended. A register whose
rows are entirely simulated is a passing deliverable and a legitimate input to
these criteria; the same register presented as customer evidence is a programme
failure, and it is the one failure that would corrupt every decision downstream.

That is the whole reason the non-verdict exists. A framework forced to return a
score creates quiet pressure to upgrade a simulated row into a real one, and
nobody would see it happen. One that can answer "not enough to decide" removes
that pressure at its source.

SM-19 qualified pains and SM-20 prototypes are logged monthly in
[the scoreboard](../SCOREBOARD.md), both tagged. SM-21 and SM-22 — paid pilots
and revenue — are never simulated, and are expected to read zero well beyond
this file's horizon.

Real company names, quoted conversation and any price discussed live in
gitignored `*.local.md` files. The tracked register, thresholds and verdict all
use placeholder identities.
