# Customer discovery — six checklists and an honest funnel

## Purpose

This file owns two things nobody else may state: the six discovery checklists,
and the funnel targets set against the brief's own illustrative ones with the
gap named rather than smoothed over.

The brief asks for scripts and checklists covering six activities. Four of them
already had a named artifact; two — researching a company, and deciding whether
to prototype — were being *performed* by tasks without ever being *written
down*, and the brief asks for the checklist, not the activity. Both are added
here, and neither costs new hours.

Checklist CL-1 earns its place twice over. It is what the brief asked for, and
it is also the specification BOA-S0 is built against in W03: the extractor
automates company research, and a procedure that was never written down cannot
be automated. Writing it first is not paperwork, it is the input.

## The instrument

### The six checklists

| Id | Activity | Where the artifact lives | First used |
|---|---|---|---|
| CL-1 | Researching a company | this file, [below](#company-research-checklist) | W01, alongside T-w01-11's 10 hand-researched prospects |
| CL-2 | Identifying likely operational pain | `templates/automation-audit.md` | W03, in the Stage-1 rehearsal |
| CL-3 | Conducting a discovery interview | `templates/discovery-interview.md` | The W04 call slot |
| CL-4 | Documenting the workflow | `templates/automation-audit.md` | W07, workflow documentation #1 |
| CL-5 | Estimating ROI | the ROI method in [the offer](consulting-offer.md) | W08, T-w08-14 |
| CL-6 | Deciding whether to prototype | the prototype-decision gate in [SaaS validation](saas-validation.md) | W10 (T-w10-11) and W12 (T-w12-13) |

CL-3 is written in W03, one week *before* the first call slot exists. The
ordering is deliberate. Someone running their first call without a script will
reach for a pitch, and pitching is how a live prospect becomes a courteous no.

### Company research checklist

Public sources only — no warm introduction, no referral, no contact already
known. Eight fields, each of which must be answerable from something published:

1. Legal name, size band, and the country whose employment costs apply.
2. One named repetitive operational process, in the company's own words where
   possible: what goes in, what comes out, who touches it.
3. The evidence for that process existing — a job advertisement describing it, a
   docs page, a filing, a public integration listing.
4. Estimated frequency of the process, with the basis for the estimate stated.
5. Systems involved, and whether each publishes an API.
6. The likely decision-maker's role, and whether that role is reachable at all.
7. One specific verifiable personalisation fact, quotable back to them.
8. A disqualifier check: anything that makes this a bad first client — a
   regulated workflow, an obvious incumbent tool, no reachable buyer.

A row missing field 3 or field 7 is not a prospect, it is a name. Field 8 exists
because the cheapest prospect to drop is the one dropped before the send.

## Exercises

### Exercise 1 — ten companies from public sources only

#### Objective

Turn a positioning statement into a list of real companies, so that the niche is
tested against what actually exists rather than against what sounds good.

#### Task

Write the positioning note first — who this is for, what problem, why you — then
research 10 companies by hand against the checklist above and record all eight
fields per company.

#### Constraints

Public sources only. No warm introduction, no referral, no contact already
known. No automated extraction: BOA-S0 does not exist until W03, and this list
is the specification it will be built against.

#### Deliverable

D-w01-3 — the positioning and niche note, plus a 10-row prospect table in
`prospects.local.md`, each row carrying a specific verifiable personalisation
fact.

#### Acceptance criteria

- 10 rows exist, and each of the 8 checklist fields is populated in every row.
- Every row cites at least 1 public source for the named process; 0 rows rest on inference alone.
- 0 rows name a warm introduction, a referral, or an existing contact.
- The disqualifier check is answered on all 10 rows, including the rows it does not disqualify.

#### Metrics

Yield = rows surviving the disqualifier check ÷ 10 researched. A yield near 1.0
means field 8 is being answered generously rather than honestly; a yield near
0.2 says the positioning note is aimed at companies that mostly do not qualify,
which is a finding about the niche and not about the research.

#### Reflection questions

1. Which field was hardest to answer from public sources, and what does that
   predict about the first question you will have to ask on a call?
2. Which two companies looked identical in the positioning note and turned out
   not to be? What distinguished them?
3. If BOA-S0 had to reproduce this list, which field would it get wrong most
   often, and what would you have to write down to stop that?

### Exercise 2 — document a workflow you have no access to

#### Objective

Separate the documentation skill from the client relationship, because that
separation is what makes progress possible from a standing start.

#### Task

Pick one public company from the prospect list and document one of its workflows
end to end from public information: named steps, estimated frequency, estimated
time cost per occurrence, and the systems each step touches.

#### Constraints

Public information only. Every estimate carries its basis. Placeholder identity
in the tracked copy — the real company name stays in the gitignored file. No
step may be asserted without something published behind it, and steps that
cannot be evidenced are recorded as gaps rather than guessed.

#### Deliverable

D-w03-3 — a Stage-1 workflow rehearsal document against a public company, in the
`templates/automation-audit.md` shape, tagged `evidence_source: simulated`.

#### Acceptance criteria

- The document names at least 5 discrete steps, each with a frequency estimate and its basis.
- Every unevidenced step is listed as a gap; 0 steps are asserted without a source or a gap marker.
- The artifact could be handed to a stranger as evidence of the documentation skill, which is CS-1's exit test.

#### Metrics

Number of documented workflows, against a programme target of 2 real or
simulated across twelve weeks. Coverage = evidenced steps ÷ total steps named,
stated per document rather than averaged across documents.

#### Reflection questions

1. Which step would you have got wrong if you had guessed, and how would the
   client have found out?
2. What does this document let you say to a prospect who asks who else you have
   done this for — and what does it not let you say?
3. Which of the nine scorecard dimensions could you already score from this
   document alone, and which need a conversation?

## Targets and thresholds

The brief supplies seven illustrative monthly targets and says plainly that
better-researched numbers may replace them, but that targets must exist. Both
sets are printed here, because a plan that quietly substitutes its own numbers
for the brief's has not made a decision, it has hidden one.

| Row | The brief, per month | This programme, across twelve weeks |
|---|---|---|
| Prospects researched | 50 | 56 |
| Personalised outreach | 30 | 52 |
| Replies | at least 5 | 0.78 – 4.16 expected, not targeted |
| Discovery calls | at least 3 | 0–1 expected, planned as 1 |
| Documented workflows | at least 5 | 2 |
| Automation opportunities scored | at least 3 | 2 |
| Prototype opportunities | at least 1 | 0 through phase 1, honestly |

The gap is large and it is deliberate. These figures are derived bottom-up from
a 15h week rather than adopted as aspirations: at the brief's volumes Track E
alone would consume most of the week, and the engineering depth this programme
exists to build would go with it. The user chose the derived set (USI-06) and it
is never quietly re-inflated. Behind the 52 personalised touches sit 104
follow-ups, two per prospect, which the table above does not show because the
brief sets no target for them at all.

Two rows changed kind rather than size, and that is the more important
difference. Replies and calls are stated as *expectations* with bands, not as
targets, because neither is under the sender's control — you control sends,
research quality and follow-up discipline, and nothing else. A target you cannot
miss through effort is not a target, it is a wish with a number on it. The
prototype row is the same admission made bluntly: through phase 1 the honest
answer is usually zero, which is why CL-6's gate carries an explicit no-branch.

Prospect research concentrates in W01, W02, W03, W04 and W06, and stops there —
56 researched against 52 sent leaves 4 rows dropped by the disqualifier check,
which is the intended attrition and not a shortfall.

## Evidence discipline

Every artifact named here carries `evidence_source: real | simulated` on its
scoreboard row. A workflow document written from public information is
*simulated* and passes; the same document presented as a client engagement is a
programme failure. Inventing evidence is the failure that the kill criteria and
the whole tagging scheme exist to prevent, and no volume target justifies it.

Under the corrected funnel the simulated path is the *expected* one for at least
one of W07's workflow document, W08's ROI calculation and W09's second document
— not a contingency to be embarrassed about. That is why W03's rehearsal is
load-bearing and may never be cut: it is where the fallback gets practised
instead of improvised.

Counts are logged weekly in [the scoreboard](../SCOREBOARD.md) — SM-15
prospects, SM-19 qualified pains, SM-20 prototypes — and the M2 delta reads
them. Identities are placeholders everywhere a file is tracked: no company name
and no contact detail, with `prospects.local.md` and the real rehearsal document
kept gitignored beside this one.
