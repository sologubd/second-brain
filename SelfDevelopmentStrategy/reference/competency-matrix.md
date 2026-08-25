# Competency matrix

## What this is

Seventeen competencies, each with a current level, a 3-month, 6-month and
12-month target, and the deliverable ids that are the only admissible evidence
for the claim.

Five levels, in the brief's literal wording: **1. Awareness · 2. Working
knowledge · 3. Independent implementation · 4. Production competence · 5. Can
design/review others' systems.** Canon's machine-checked enum renders the fifth
as *Can design and review others' systems*; the table below uses the enum value
because that is the string every check compares against, and the difference is a
recorded choice rather than a drift.

**"I studied it" is never evidence.** Every column value maps to at least one
deliverable id. No certification appears here and none would count. A target
unmet at its checkpoint month with no evidence id behind it is re-planned or
downgraded — never silently held, which is the failure a self-rated matrix
invites.

Four of the current levels are supplied by the user, not inferred: coding agents
at *Independent implementation*, distributed systems at *Working knowledge* and
explicitly concept-strong / operation-weak, retrieval at *Awareness*, and
security and threat modelling at *Awareness*. The rest are inferred from those
four and from the senior-Python-developer self-identification, and one —
observability — was never asked.

## The table

| # | Competency | Current | 3-month | 6-month | 12-month | Evidence required |
|---|---|---|---|---|---|---|
| CM-01 | Coding agents and harness engineering | Independent implementation | Production competence | Production competence | Production competence | D-w01-1, D-w01-2, D-w04-1, D-m04-1 |
| CM-02 | Agent orchestration and parallel execution | Working knowledge | Independent implementation | Production competence | Production competence | D-w08-1, D-w02-4, D-m04-1 |
| CM-03 | Distributed systems in production (operating, not explaining) | Working knowledge | Independent implementation | Independent implementation | Independent implementation | D-w03-1, D-w08-1, D-m04-2, D-m04-3 |
| CM-04 | Idempotency and crash-consistency | Working knowledge | Production competence | Production competence | Production competence | D-w03-1, D-m04-2 |
| CM-05 | Software architecture, boundaries and modularity | Independent implementation | Independent implementation | Independent implementation | Independent implementation | D-w02-2, D-w04-3, D-w08-2, D-w12-3 |
| CM-06 | Domain modelling and naming | Independent implementation | Independent implementation | Independent implementation | Independent implementation | D-w02-1, D-w07-2 |
| CM-07 | Retrieval, embeddings and search | Awareness | Independent implementation | Independent implementation | Independent implementation | D-w05-1, D-w06-1, D-m02-1 |
| CM-08 | Retrieval evaluation and metrics | Awareness | Independent implementation | Independent implementation | Independent implementation | D-w05-1, D-w06-1 |
| CM-09 | Evaluation harness and LLM-judge design | Awareness | Independent implementation | Independent implementation | Independent implementation | D-w10-1, D-w10-2 |
| CM-10 | Production AI application engineering | Working knowledge | Independent implementation | Independent implementation | Independent implementation | D-w06-1, D-w11-3, D-m02-1 |
| CM-11 | Agent memory design | Awareness | Awareness | Independent implementation | Independent implementation | D-m05-1, D-m05-2 |
| CM-12 | Observability and tracing of agent workloads | Working knowledge | Independent implementation | Independent implementation | Independent implementation | D-w09-1, D-w10-2 |
| CM-13 | AI security and threat modelling | Awareness | Independent implementation | Production competence | Production competence | D-w11-2, D-w12-2, D-m03-2, D-m05-2 |
| CM-14 | Cost and quota engineering under a flat-rate subscription | Awareness | Independent implementation | Independent implementation | Independent implementation | D-w01-2, D-w09-1, D-w10-1 |
| CM-15 | Customer discovery and consulting from a cold start | Awareness | Working knowledge | Working knowledge | Production competence | D-w01-3, D-w03-3, D-w07-4, D-w08-4, D-m07-1 |
| CM-16 | Opportunity valuation and product validation | Awareness | Working knowledge | Working knowledge | Independent implementation | D-w10-4, D-w11-4, D-w12-4, D-m09-2 |
| CM-17 | Reviewing generated code | Working knowledge | Independent implementation | Production competence | Production competence | D-w04-3, D-w12-3, D-m04-4 |

## How to read it

Read across a row, then check the deliverable ids. A level is a claim about what
you can do unsupervised, and the ids are the receipts.

Five rows carry warnings worth reading before the table is used as a scoreboard.

**CM-07 is the most aggressive claim in the file.** Awareness to Independent
implementation inside three months is a two-level jump, and it is only plausible
because weeks 05 and 06 sit on one continuous retrieval build. If any row is
going to be wrong, this is the one.

**CM-11 is deliberately flat through month 3.** The memory surface does not
exist until BOA-S2 at month 05, and a matrix claiming progress against a surface
that does not exist would be exactly the unevidenced claim the rule above
forbids.

**CM-12 is inferred and was never asked.** Working knowledge is assumed on the
grounds that a senior Python developer has used tracing but likely has not
instrumented agent or model workloads. That assumption may under-serve W09 in
the same way an assumed level under-served retrieval. It is flagged for
confirmation at M01, where it is a one-question fix.

**CM-15's 3-month target is only one level up, and that is arithmetic rather
than modesty.** Starting from zero pipeline, the programme's own funnel model
expects roughly 2.47 replies and 0.62 calls by month 3. Claiming Independent
implementation there would be claiming a competency the plan predicts will lack
evidence.

**CM-17 is the thesis row.** Hand-written code fails in a distribution your
instincts were trained on; generated code is syntactically clean and wrong at
boundaries, under repetition, under concurrency and under failure. The
correlates moved and the heuristics did not. It is the competency the durable
concept set exists to build.

## How it changes

The **M06 retrospective owns this file.** Its mandated delta is a competency
reassessment: re-rate all four target columns against delivered deliverable ids
ahead of CP-M6, and downgrade or re-plan anything unevidenced.

Two earlier retrospectives touch it. M01 confirms the CM-12 baseline, which is
the one row resting on an unasked question. M02's funnel recalibration moves what
CM-15 and CM-16 can honestly claim, since both are gated on evidence other
people supply. The M12 rewrite re-baselines the whole table for year two.

Edits go through canon's `competencies.rows` and the loop in
[HOW-TO-EDIT.md](../HOW-TO-EDIT.md). Levels may be revised in either direction;
the evidence rule is not negotiable in either.
