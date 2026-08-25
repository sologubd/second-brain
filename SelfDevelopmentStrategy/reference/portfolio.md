# Portfolio

## What this is

The ten artifacts this programme exists to produce, and — for each one — what
makes it credible to a senior engineer or a potential client who has never met
the author.

The credibility column is the point of the file. A list of ten project names is
a claim; a list of ten reasons a skeptical reader would believe them is
evidence. Every item points at a runnable artifact or a measured number with its
denominator, never at a description of one. **"I studied it" is never evidence**
here, and neither is a screenshot. No certification appears in this file,
because none of them is a runnable artifact.

## The table

| # | Item | Complete by | Evidence | What makes it credible |
|---|---|---|---|---|
| PF-01 | Engineering Agent Platform | M04 | D-w01-1, D-w02-1, D-w03-1, D-w04-1, D-w08-1, D-w09-1, D-m04-1 | It survives `kill -9` at any step boundary and proves it: 100 replays with injected kills produce exactly one state transition, one pull request, one dedup row per key. A reader does not need to read the code — they run the replay demo and watch it hold. Almost no side project has a fault-injection suite; the ones that do were written by people who have operated something. |
| PF-02 | Secure Knowledge/RAG Agent | M03 | D-w05-1, D-w05-2, D-w06-1, D-w11-3 | It ships a test that fails on the obvious implementation. The permission pre-filter arrives with a reproducible case where the naive post-filter silently returns fewer authorized results than exist — the defect a reviewer expects to find, found already named, demonstrated and fixed. Plus NDCG@5 and MRR per configuration against a label set frozen before any tuning — provable from `evals/ska-labels.frozen.sha256`, a digest and freeze date re-verified against the set when the metrics are read, not from commit history, which this repo does not keep. |
| PF-03 | Business Operations Automation | M05 | D-w03-2, D-w04-2, D-m05-1, D-m05-3 | It cannot send. Every outbound action requires an approval record, a bypass attempt is refused *and* logged, and the approval payload renders the literal proposed call rather than the agent's summary of it. For a buyer that is the difference between an automation they would let near their CRM and one they would not. |
| PF-04 | Architecture ADR collection | M08 | D-w04-3, D-w08-2, D-w12-3, D-m08-1 | The ADRs name accepted defects with remediation months, not only decisions taken. Review #2 is conducted on a deliberately bad system supplied to the reviewer, so it demonstrates finding defects rather than describing one's own choices favourably. A clean bill of health would be the least credible possible output. |
| PF-05 | AI security attack/evaluation report | M05, begins W11 | D-w11-2, D-w12-2, D-m05-2 | Every number is a measurement of the author's own system with a stated denominator — attack success rate before and after a named structural mitigation — and there is not one borrowed industry effectiveness percentage anywhere, because none met a citable standard. The memory-poisoning chapter maps onto a worked example published by the standards body itself. |
| PF-06 | Agent evaluation suite | M03 | D-w10-1, D-w10-2 | It gates a merge, with three tiers and a threshold stated as a statistical bound over N=5 reruns rather than a binary pass. The report also states what each tier *cannot* catch. Most published eval work asserts a score; this asserts a decision rule and its blind spots, which is what an engineer who has run a flaky suite looks for. |
| PF-07 | At least one real external automation case study if possible | M07, contingent | D-m07-1 | A measured before-and-after baseline from someone else's business, with the measurement method documented well enough to survive "how did you measure that?". If the funnel produces none, the honest substitute is Stage-1 documented workflows tagged `evidence_source: simulated` — and that tag is itself credibility, because it shows the author separates evidence from demonstration. |
| PF-08 | Consulting offer page | M06 | D-w11-4, D-m06-3 | Fixed scope, fixed price, and a payback period computed from a measured baseline using fully-loaded cost — not an industry-average return percentage. A buyer recognises the difference immediately: one is a claim about them, the other is a claim about a survey. |
| PF-09 | Customer discovery notes | M03 | D-w03-3, D-w07-4, D-w09-3, D-w10-4 | Every note carries `evidence_source: real` or `simulated`, and the funnel figures beside them are actual sends and replies, not targets. A reader sees a first-timer's real conversion rate and the plan's own prediction side by side. Placeholder identities throughout, with real data in gitignored files — itself the discipline a client checks for. |
| PF-10 | Micro-SaaS opportunity scorecard | M09 | D-w10-4, D-w12-4, D-m09-2 | It has produced a NO, or an explicit "insufficient evidence, deferred", with the missing threshold named and dated. A scorecard that has only ever produced yeses is a rationalisation engine. This one scores against seven thresholds with concrete numbers and five kill criteria with stated detection rules. |

Four decision checkpoints read this table rather than a self-assessment.

| Checkpoint | Month | Decision question | Evidence |
|---|---|---|---|
| CP-M3 | M03 | Can I operate coding agents materially better than an ordinary senior developer? | D-w01-1, D-w03-1, D-w04-1, D-w07-1, D-w08-1, D-w09-1, D-w10-1, D-w12-1 |
| CP-M6 | M06 | Can I build production-grade AI workflows with evals, security and observability? | D-m02-1, D-w10-1, D-w11-2, D-m03-1, D-m04-1, D-m05-2, D-m06-1 |
| CP-M9 | M09 | Can I solve a real company's automation problem end-to-end? | D-m07-1, D-m07-2, D-m09-1, D-m09-2 |
| CP-M12 | M12 | Do I have enough repeated customer evidence to pursue consulting, productize an offer, build a micro-SaaS, or stay primarily on the Staff/AI Engineer path? | D-m09-2, D-m11-1, D-m12-1 |

## How to read it

Read the credibility column first and the item name second. The name tells you
what was built; only the credibility statement tells you why anyone should
believe it, and it is the column that fails an audit.

An item is complete when every deliverable id beside it is satisfied **and** its
credibility statement is true as written. Those are different tests. PF-04 with
three ADRs that record only successful decisions satisfies its ids and fails its
statement, because the statement demands named accepted defects.

Two items are contingent and say so. PF-07 depends on a funnel producing an
external party, and under this programme's own arithmetic that is not the
expected outcome; substitution is therefore partial and one deliverable at a
time, so that PF-07 is the last item to become simulated rather than the first.
PF-10 is contingent in a different way: it is satisfied by a NO or a dated
deferral, so it cannot be failed by the market — only by refusing to conclude.

CP-M12 offers four directions and the fourth, staying primarily on the Staff or
AI Engineer path, is a first-class outcome. It is the only one of the four whose
evidence this table can produce without anyone else's cooperation.

## How it changes

The M11 retrospective owns this file. Its mandated delta is a portfolio
credibility audit: every item is re-read as a stranger would read it, and any
credibility statement that has drifted from what the artifact actually
demonstrates is either repaired in the artifact or rewritten in canon — never
left standing as an aspiration.

Two earlier retrospectives may touch it indirectly. A cut drawn from the cut
list can thin an item — reducing the third architecture review to the security
surface leaves PF-04 with two reviews rather than three — and any such draw must
record the downstream effect here. The M02 funnel recalibration can change what
PF-07 and PF-09 can honestly claim.

Edits follow the loop in [HOW-TO-EDIT.md](../HOW-TO-EDIT.md): the table is
generated from `portfolio.items` in canon, so it is edited there and
regenerated, never patched in place.
