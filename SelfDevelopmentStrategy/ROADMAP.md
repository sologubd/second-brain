# Roadmap

One row per period. Editable by hand; nothing here is generated.

## Months 1–3 — the twelve week files

| Period | Main capability | Project milestone | Business milestone | Evidence |
|---|---|---|---|---|
| [W01](weeks/week-01.md) | Drive a coding agent unattended, task file to captured diff | Platform: minimal harness runs 5 real tasks | Niche chosen, 10 prospects researched by hand | Run log with duration and tokens; positioning note |
| [W02](weeks/week-02.md) | Verification and human approval before anything merges | Platform: task → verified PR | First 4 cold sends, hand-written | 5 tasks, ≥4 PRs, verification output per task |
| [W03](weeks/week-03.md) | Requirement extraction, research, ambiguity detection | Platform: feature workflow · BOA: structured extraction | 5 sends; workflow documented from public info | 5 feature PRs; ambiguity log; workflow document |
| [W04](weeks/week-04.md) | Investigate, reproduce, regression-test, fix | Platform: bug workflow · BOA: draft-only outreach with approval | 6 sends; first discovery call slot held open | 5 historical bugs; root-cause and fix rates |
| [W05](weeks/week-05.md) | Durable state; restart resumes from what was written | Platform: persistence and resume | 9 sends, assisted by the extractor | Kill-at-every-boundary suite; architecture review #1 |
| [W06](weeks/week-06.md) | Retries, idempotency, effectively-once processing | Platform: replay-safe task handler | 9 sends; one automation opportunity scored | 100 replays → one effect per key; duplicate classification |
| [W07](weeks/week-07.md) | Answer *what did it do* from telemetry, not memory | Platform: tracing and cost accounting | 8 sends; workflow document #2 | Nested traces; cost per task; retry budget under a storm |
| [W08](weeks/week-08.md) | Concurrency that strands and duplicates nothing | Platform: queue with leases and dead-lettering | 6 sends; ROI calculation from a measured baseline | Chaos run telemetry; architecture review #2 on supplied system |
| [W09](weeks/week-09.md) | A change cannot merge without clearing a gate | Platform: eval harness, 3 gate tiers | 5 sends; funnel rates computed from actuals | 20-task suite; pass-rate threshold with justification |
| [W10](weeks/week-10.md) | Hybrid retrieval with authorization inside the index | SKA: permission-filtered retrieval, measured | Pain register assembled | NDCG@5 and MRR per configuration; pre-filter leak test |
| [W11](weeks/week-11.md) | Attack your own agent; break a leg structurally | SKA: trust boundary and cited answers | Offer sketch from the qualified pain register | Attack report: 3 techniques, rates before and after |
| [W12](weeks/week-12.md) | Least privilege, sandboxing, approval boundaries | Platform: per-tool profiles and audit log | Verdict — or explicit non-verdict — on the SaaS candidate | Confused-deputy report; architecture review #3; 12-week retro |

## Months 4–12 — direction, not schedule

| Period | Main capability | Project milestone | Business milestone | Decision point |
|---|---|---|---|---|
| [M04–M06](later/months-04-06.md) | External-effect durability; agent memory; policy-based authorization | Platform: outbox + relay, Notion/tracker ingestion, multi-axis review · BOA: durable account memory · SKA: RBAC | First free or cheap pilot, strictly scoped, if the funnel produces one | Is the harness good enough to sell time on, or does it need another month? |
| [M07–M09](later/months-07-09.md) | Delivering to someone else; packaging a repeatable offer | Platform: architecture → ADR lane · operate all three systems | Paid fixed-scope work; repeatable offer; SaaS candidate scored on evidence | Consulting, productized offer, micro-SaaS, or staff-engineer track? |
| [M10–M12](later/months-10-12.md) | Operating rather than building; evidence that survives a skeptic | All three systems in sustained operation | Revenue if it exists; honest zero if it does not | The 12-month direction, chosen on measured evidence |
