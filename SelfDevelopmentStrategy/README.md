# AI-Native Engineering Program

Twelve months. Twelve detailed week files covering months 1–3 at 180.0 planned
hours; months 4–12 carry deliverables and monthly outcomes rather than week
files. One repository you execute rather than read.
`canon/canon.yaml` is the source of truth; every file here expands a canon row and
none invents one. [ROADMAP.md](ROADMAP.md) is the month-by-month table,
[SCOREBOARD.md](SCOREBOARD.md) the 22 weekly metrics, and
[HOW-TO-EDIT.md](HOW-TO-EDIT.md) the only sanctioned way to change any of it.

## Objective

Not a list of things to study. An execution-oriented professional development
system — an *engineering program / operating system* rather than a learning
roadmap. The test of that claim is executability: every week names a runnable
demo command, a checkbox deliverable list, and acceptance criteria that are
binary predicates, numbers or artifact paths.

It is built around one success statement — *I can independently design, build,
evaluate, secure, operate and commercialize AI-native software systems, while
using coding agents to multiply my engineering throughput* — and against one
failure form, *I know AI tools.* That sentence names seven separately checkable
capabilities: design, build, evaluate, secure, operate, commercialize, and using
coding agents to multiply throughput. Each maps to deliverable ids. None is
satisfied by a claim.

## Target professional profile

The objective is **not** to become an "AI prompt engineer". The target is an
**AI-native Staff Engineer / Agent Systems Engineer / Technical Founder capable
of taking a problem from business intent to reliable production system.**

That phrase is the whole arc. Tracks E and F supply the business intent; A, B and
C supply the system; D and the evaluation harness supply the *reliable*. A
program stopping at *operate* could not claim the profile, which is why the
difficulty ladder ends at *sell*.

The reader is assumed to be a senior Python developer who already delegates real
work to coding agents. Nothing here explains what a concept is. This is a
one-year apprenticeship for someone who intends to remain highly valuable if
coding itself becomes increasingly automated.

## Philosophy

**ABILITY TO BUILD > KNOWLEDGE.** Every substantial topic ends in one or more
observable artifacts. *I watched/read/studied X* is never completion, and
**"I studied it" is never evidence** — a rule the
[competency matrix](reference/competency-matrix.md) and the
[portfolio](reference/portfolio.md) both enforce by demanding a deliverable id.

Four exercise framings this program refuses, beside the four it produces
instead. The pairing is what makes the philosophy checkable rather than
decorative:

| Refused | Why it fails | Produced instead | Homed at |
|---|---|---|---|
| learn LangGraph | Names a technology and no observable. It can be abandoned, not completed. | implement a resumable LangGraph workflow with persisted state and human approval | D-w02-1 and D-w04-1, built hand-rolled per the durable-execution triage |
| learn distributed systems | Names a field. No state of the world differs once it is done. | implement an idempotent event consumer and demonstrate duplicate delivery handling | D-w03-1, with the naive version built first and its duplicates counted |
| read about RAG | Names a consumption activity — the exact completion claim the philosophy bans. | compare BM25, vector and hybrid retrieval on a real dataset using an evaluation set | D-w05-1, a three-way bake-off against a label set frozen before any tuning |
| learn prompt injection | Names a threat with no attacked system, so nothing separates learning it from hearing of it. | build an indirect-prompt-injection attack suite and show which attacks are blocked | D-w11-2, three techniques, success rate before and after one structural mitigation |

Any exercise here must be rewritable into the right-hand column. One that can
only be stated on the left has not been designed yet.

## How to use this repository

0. Once only, before week 01: put the prerequisite floor in place per
   [SETUP.md](SETUP.md). Not a deliverable.
1. Open the current week file, starting at [week 01](weeks/week-01.md). Work its
   tasks. Tick its deliverables. Do not read ahead.
2. Log actuals into the `<!-- user:actuals -->` regions of the week file and
   [SCOREBOARD.md](SCOREBOARD.md). Weekly logging never requires touching YAML.
3. At the end of each month, answer the month file's ten retrospective questions
   and produce its eleventh output, RQ-11 — a canon delta. The procedure is in
   [HOW-TO-EDIT.md](HOW-TO-EDIT.md).
4. Consult a [track](#tracks) file for the reasoning behind an hour, a
   [phase](#progression-model) file for the arc, a
   [project](#flagship-projects) file for a stage definition.

**Templates** — copy, never edit in place:
[ADR](templates/adr-template.md) ·
[experiment](templates/experiment-template.md) ·
[weekly review](templates/weekly-review.md) ·
[discovery interview](templates/discovery-interview.md) ·
[automation audit](templates/automation-audit.md) ·
[case study](templates/case-study.md) ·
[week](templates/week-template.md).

**Reference shelf** — stable tables, edited only by a named retrospective:
[portfolio](reference/portfolio.md) ·
[maturity model](reference/maturity-model.md) ·
[competency matrix](reference/competency-matrix.md) ·
[difficulty ladder](reference/difficulty-ladder.md) ·
[low-ROI verdicts, the cut list and the glossary](reference/low-roi-and-cuts.md).

**Reading** — every theory task names a `RES-` id, and
[the resource list](resources/recommended-resources.md) resolves it to a
document with a URL or ISBN, the sections worth reading, and the deliverable
that proves you understood it. Dated ecosystem claims live in
[the snapshot](resources/ecosystem-snapshot-2026-08.md), each with a re-verify
date, so a volatile fact cannot age silently inside a week file.

## Time commitment

Baseline 15.0 h per week. Inside a week, theory is capped at 3.5 h and customer
discovery floored at 2.5 h. Across the program theory is 19.2% against the
brief's 25–30% ceiling, and active work is 80.8% against its 70% floor.

A week file is a **unit of work, not a unit of time.** You work about 15 hours
per calendar week; a week file whose real effort runs past 15 hours simply spans
more than one. The twelve week files therefore occupy roughly **18 calendar
weeks** — about sixteen of work plus two floating catch-up weeks, budgeted and
deliberately unassigned, so illness, a release, or a week that cost more than it
was priced at has somewhere to go.

That number was raised from fourteen on evidence. An auditor estimated week 4's
work before reading its budget and came back 46% over — except on customer
discovery, already costed from published unit rates, which landed within 7%. The
hour tables are the *planned* budget and still reconcile; the wrong claim was
about wall-clock, which nothing checked.

**Never double up after a missed week. Slip the calendar.** Each week file names
its 8-hour subset, what it leaves unticked, and where those ids go; sends are
never doubled, because the funnel has a lead time hours cannot compress.

## Tracks

Six parallel tracks, deliberately not sequential monthly themes. Every week
carries at least three of them, which is what makes the parallelism real rather
than declared: no week here is a security week and no month is an architecture
month.

| Track | Hours | Share | What the hours buy, in one line |
|---|---|---|---|
| [A — Agentic Engineering](tracks/agentic-engineering.md) | 43.0 | 23.9% | An unattended harness: runner, cross-harness adapter, verification and approval pipeline, Sentry lane, observability. |
| [B — Software Architecture & System Design](tracks/system-design.md) | 39.0 | 21.7% | A durable state machine proved under 100 killed replays, a lease-based queue, and three architecture reviews. |
| [C — Production AI Application Engineering](tracks/ai-application-engineering.md) | 33.5 | 18.6% | Permission-filtered hybrid retrieval, a frozen label set, measured metrics, and a three-tier regression gate. |
| [D — AI Security](tracks/ai-security.md) | 22.5 | 12.5% | Attack suites run against your own systems, with success rates measured before and after each structural mitigation. |
| [E — Consulting & Customer Discovery](tracks/consulting.md) | 34.0 | 18.9% | A cold-start funnel built from zero: prospects, personalised sends, follow-ups, workflow documents, a scored offer. |
| [F — Micro-SaaS Discovery](tracks/micro-saas.md) | 5.0 | 2.8% | The instruments only — a pain-scoring model, seven evidence thresholds, five kill criteria, and the right to return a non-verdict. |

A seventh pseudo-track, P, funds the three retrospectives at W04, W09 and W12 —
3.0 h, 1.7% of the programme, classified as `testing` by declaration rather than
by natural fit. A retrospective measures the programme rather than a system, and
the brief fixes the week template at four buckets, so there is nowhere better.
Stated rather than left implicit, because the theory/building/testing seam is the
one classification boundary nothing else here guards.

## Flagship projects

**The flagship is the Engineering Agent Platform**
([projects/engineering-agent-platform.md](projects/engineering-agent-platform.md)):
thirteen stages from S0 to S9, consuming real tasks and real incidents and
producing reviewed pull requests against a real repository. It is the only home
for stage definitions and runnable demo commands, and every stage must be
runnable — a stage with no demo command has not shipped.

Two secondary projects run beside it. The
[Secure Knowledge Agent](projects/secure-knowledge-agent.md) is an eight-step
pipeline from documents to a cited answer, with authorization inside the index
rather than after it. The
[Business Operations Agent](projects/business-operations-agent.md) is a
seven-step pipeline from an inbound document to a CRM update that cannot fire
without an approval record.

## Progression model

Progress is claimed against three instruments and four decisions.

- The [maturity model](reference/maturity-model.md) runs L0 to L5 with objective
  requirements per level and the week or month that claims each.
- The [difficulty ladder](reference/difficulty-ladder.md) runs understand →
  implement → break → debug → measure → secure → operate → explain → sell.
- The [competency matrix](reference/competency-matrix.md) rates every competency
  on five levels — Awareness, Working knowledge, Independent implementation,
  Production competence, Can design/review others' systems — with current,
  3-month, 6-month and 12-month targets and the evidence required for each.
- Four career checkpoints — CP-M3, CP-M6, CP-M9 and CP-M12 — sit at months 3, 6,
  9 and 12, each carrying a decision question and deliverable ids, never a
  self-assessment.

Five phases describe the arc. They own entry and exit conditions and
checkpoints; they never own topics, hours or tasks.

| Phase | Months |
|---|---|
| [01 — Foundations](phases/phase-01-foundations.md) | [M01](months/month-01.md) · [M02](months/month-02.md) · [M03](months/month-03.md) |
| [02 — Agent harness](phases/phase-02-agent-harness.md) | [M04](months/month-04.md) |
| [03 — Production AI](phases/phase-03-production-ai.md) | [M05](months/month-05.md) · [M06](months/month-06.md) |
| [04 — Consulting](phases/phase-04-consulting.md) | [M07](months/month-07.md) · [M08](months/month-08.md) |
| [05 — Productization](phases/phase-05-productization.md) | [M09](months/month-09.md) · [M10](months/month-10.md) · [M11](months/month-11.md) · [M12](months/month-12.md) |

## Definition of DONE

A week is DONE when all four hold. Nothing here is satisfied by a feeling of
having covered the material.

- [ ] Every deliverable checkbox is ticked, and each points at something that
      runs or at a measured number whose denominator is stated.
- [ ] Every acceptance criterion evaluates true, where each is a binary
      predicate, a number, or a path to an artifact that exists.
- [ ] The failure exercise names all five parts: detection, safe failure
      behaviour, recovery, logging, and a test proving the mitigation.
- [ ] `## Evidence` carries real links — commits, PRs, benchmarks, ADRs, demos,
      interview notes — and each business artifact carries its
      `evidence_source: real | simulated` tag.

A deliverable substituted for its fallback is still DONE, provided the
substitution is tagged. A simulated artifact honestly tagged passes. A simulated
artifact presented as real is a program failure.

A week run at the 8-hour budget closes **DONE-COMPRESSED**, a weaker and
different claim: the subset's deliverables are ticked, its criteria are true, and
every remaining id is listed with the week it is carried to. Nothing is ticked on
partial evidence, and the week becomes DONE once the carried ids land. The P0
rule below is a claim about the programme, which is why the 8-hour mode extends
the calendar rather than cutting scope.

## Weekly review process

One artifact, described at three levels. [templates/weekly-review.md](templates/weekly-review.md)
is the blank form; this section is the process; the week file's `## Weekly
score` is where that week's score lands, allocated by its own explicit scoring
rules summing to 100.

End of week, in order: fill the review template from the week file's evidence
section, not from memory; score the week 0–100 against its stated rules; update
the affected rows in [SCOREBOARD.md](SCOREBOARD.md) inside their keyed user
regions; and note anything that would change a canon row — hold it until the
month-end retrospective, which is the authorised mutation path.

**This sits outside the 15 hours and takes about 20 minutes.** Every week's tasks
total exactly 15.0 and pseudo-track P funds retrospectives at W04, W09 and W12
only, so the review has no hour behind it, and pricing it would cut engineering
from every week to pay for bookkeeping. The 15.0 is a budget for the work, and
the instrument that measures the work is not the work. Said plainly because an
unfunded obligation nobody names is how a weekly habit quietly stops happening.

## Adapting from 15h to 8h or 25h

Hours change **depth and calendar, never the P0 deliverable set.** The same P0
rows ship at every budget; what moves is how much of the stretch column you
reach and how long the twelve week files take in wall-clock time.

At **8h** a week: P0 rows only, no stretch goals, and the 2.5 h customer
discovery floor held regardless, because the funnel's lead time is not
compressible. The calendar extends — the same P0 set takes roughly **18 months**
rather than twelve. Said plainly, rather than pretending twelve months compresses
into a smaller budget.

At **25h** a week: the stretch goal becomes required, each week carries a second
failure exercise, Track F pulls forward out of its instruments-only posture, and
phase 01 compresses to about eight weeks.

The rule for a bad week is the same at every budget: run the named 8-hour subset
and let the calendar slip rather than stacking two weeks into one.
