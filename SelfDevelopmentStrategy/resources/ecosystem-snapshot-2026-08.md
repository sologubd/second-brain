# Ecosystem snapshot — August 2026

## How to use this list

This file is a quarantine. Every claim in this repository about the *current
state* of a product, specification or price lives here and nowhere else, with
its date, a supporting span from the source, and a date by which it must be
re-checked. No week file, track file or project file may state a dated ecosystem
fact; they link here instead.

The reason is arithmetic, not tidiness. This programme rests on facts with
half-lives measured in weeks — a specification revision three weeks old when
recorded, a telemetry convention set with no stable release, a quota boost with
a published expiry, a security document that may already be superseded.
Scattered across seventy-odd files those facts age invisibly and the repository
becomes confidently wrong; gathered here they are re-checked in one pass.

That pass is the M3 mandated delta, scheduled rather than hoped for, in a fixed
priority order: security-list numbering, telemetry conventions, quota figures,
specification revision, pricing. Each entry also carries the four standard
resource fields, because a volatile fact you cannot tie to a deliverable is not
worth tracking — the fourth field names what breaks if the claim has moved.

**Recorded 2026-08-25. Re-verify by 2026-11-30 unless an entry says otherwise.**

## Resources

### Model Context Protocol — the revision to pin

**Claim:** the specification revision current at recording is dated 2026-07-28.
It retires the initialize handshake and the session-id header; requests are
stateless and self-contained with per-request capability negotiation, and
application state persists through explicit handles passed in tool arguments.
**Supporting span:** "the initialize handshake and Mcp-Session-Id are retired"
while "explicitly still allowing application-level state via opaque handles
passed as arguments".
**Re-verify by:** 2026-11-30, fourth in the M3 delta's priority order.
**What exactly to learn from it:** statefulness belongs in inspectable
application data, not in the transport.
**Which chapters or sections matter:** the stateless-request change and the
feature-lifecycle policy.
**Which roadmap project uses the knowledge:** whatever carries task state
across a restart — here, the S1a machine.
**What exercise proves I understood it:** D-w02-1. If the revision has moved,
re-read only the lifecycle policy — the discipline the exercise teaches survives
a wire-format change.

### OWASP agentic threat categories, and the numbering that is forbidden

**Claim:** ASI01 through ASI10 were verified verbatim against OWASP's own PDF,
linked from a landing page dated 2025-12-09, and may be cited. The separate LLM
list must be cited **by category name with no identifier number at all**. A
newer LLM edition appears to have been published on 2026-08-04 and reportedly
renumbers Excessive Agency, and it was not refetched from its primary PDF — so
no numbering is verified, including the agentic PDF's own internal
cross-references to the older scheme.
**Supporting span:** the ten agentic categories run Agent Goal Hijack, Tool
Misuse and Exploitation, Identity and Privilege Abuse, Agentic Supply Chain
Vulnerabilities, Unexpected Code Execution, Memory and Context Poisoning,
Insecure Inter-Agent Communication, Cascading Failures, Human-Agent Trust
Exploitation, Rogue Agents.
**Re-verify by:** 2026-11-30, and **first** in the M3 delta's priority order.
**What exactly to learn from it:** the four categories this build touches, plus
the least-agency framing.
**Which chapters or sections matter:** ASI01, ASI02, ASI03, ASI06, and the
leads' letter.
**Which roadmap project uses the knowledge:** the trust boundaries built at
S7a, then S7b, and the memory surface at BOA-S2.
**What exercise proves I understood it:** D-w11-2 and D-w12-2. If the numbering
moved, what breaks is the mapping from each mitigation to its named category —
not the mitigation. Cite the PDF, never a vendor summary.

### OpenTelemetry GenAI semantic conventions — a moving target

**Claim:** these conventions are **entirely Development status; none are
Stable.** They were extracted into a dedicated repository on 2026-06-12 with no
tagged stable release. Agent and tool coverage is real — invoke_agent,
execute_tool and the MCP conventions folded in at v1.42.0 — but under an
unstable specification, and recent churn includes `gen_ai.system` becoming
`gen_ai.provider.name` and `prompt_tokens` becoming `input_tokens`. Coding
agents emit this telemetry today, but span and trace support remains in beta.
**Supporting span:** "ENTIRELY Development status; NONE are Stable", recorded as
of July 2026.
**Re-verify by:** 2026-11-30, second in the M3 delta's priority order.
**What exactly to learn from it:** teach and use this as a moving target against
a pinned version, never as a settled convention. The plan overstated its
stability; this entry is the correction.
**Which chapters or sections matter:** the operation-name vocabulary, the agent
and tool span shapes, token-usage attributes — and the stability badge on every
attribute used.
**Which roadmap project uses the knowledge:** the exporter configuration inside
S5, and whatever reads those traces at S6.
**What exercise proves I understood it:** D-w09-1 — a connected trace exported
against a **pinned** convention version recorded in run metadata, which is what
makes a silent upstream rename detectable rather than merely confusing.

### Subscription quota — measured, never quoted

**Claim:** no published quota figure is usable as a constant. One vendor's
weekly-limit boost ran with an announced expiry of 2026-08-31; the other's
five-hour cap was temporarily lifted with no announced end and its weekly cap is
not published at all. It is also undocumented whether one agent turn consumes
quota the same way one typed prompt does. The quota bucket is shared across the
coding CLI, the chat interface and every other surface on the account.
**Supporting span:** every quota field in canon reads `MEASURED_FROM_WEEK_01`
rather than a number.
**Re-verify by:** 2026-11-30, third in the M3 delta's priority order. There is
also an early trigger: if W01 measures fewer than two runs of headroom for every
run the plan schedules, a canon delta is authorised at once rather than held for
the retrospective.
**What exactly to learn from it:** that the binding constraint on evaluation
size is quota rather than euros, which inverts the plan's original framing.
**Which chapters or sections matter:** the advertised-limit page, read only to
confirm the figures still carry expiry dates.
**Which roadmap project uses the knowledge:** S6's evaluation sizing, whose
formula is driven by measured runs.
**What exercise proves I understood it:** the W01 quota measurement itself,
taken with other interactive use isolated — otherwise it measures the wrong
thing.

### Model pricing, used only for imputation

**Claim:** the imputation rate is USD 2.00 and USD 10.00 per million input and
output tokens, priced through 2026-08-31, converted at 0.925 EUR per USD. It
exists only to impute a euro figure for cost per task, whose realised marginal
cost under flat-rate execution is zero.
**Supporting span:** canon marks the basis `[VOLATILE], priced through
2026-08-31`.
**Re-verify by:** 2026-11-30, fifth in the M3 delta's priority order.
**What exactly to learn from it:** that an imputed number needs a declared rate
or it means nothing.
**Which chapters or sections matter:** the provider's current pricing page only.
**Which roadmap project uses the knowledge:** S5 cost accounting.
**What exercise proves I understood it:** SM-12's composite cost metric, which
reports tokens, an imputed euro figure and the metered figure separately rather
than collapsing them into one misleading number.

### The subscription execution lane and its compliance risk

**Claim:** two things here can move, and the architectural rule that depends on
them is stated in the platform's project file rather than restated here. What is
volatile is the *wording on the vendor's pages*: the compliance page's
distinction between key-authenticated products and an end user's own signed-in
binary, and the phrase "ordinary, individual usage" attached to advertised
limits, which is undefined and enforceable at the vendor's discretion.
**Supporting span:** the second harness's documentation confirms its execution
mode reuses saved CLI authentication.
**Re-verify by:** 2026-11-30, and again before the second adapter is finalised.
**What exactly to learn from it:** where the authentication boundary sits today,
and that crossing it silently changes the cost model of the whole programme.
**Which chapters or sections matter:** the credential-use section, re-read in
full rather than recalled.
**Which roadmap project uses the knowledge:** the adapter at S0, plus the
metered lane held open behind the same interface.
**What exercise proves I understood it:** D-w01-1. Treat the undefined-usage
wording as a live risk to monitor rather than a blocker, and keep the account's
run pattern recognisably that of one working developer.

### Licences on local retrieval models

**Claim:** at least one widely recommended multilingual reranker ships under a
non-commercial licence, which rules it out of a public-capable repository and
out of client work regardless of how it scores.
**Supporting span:** canon records this constraint as hard, taken from the model
card itself.
**Re-verify by:** 2026-11-30, and again before any client engagement — licences
change more quietly than benchmarks do.
**What exactly to learn from it:** read the licence before the benchmark table.
A model winning on score and losing on terms was never a candidate.
**Which chapters or sections matter:** the licence line on every card
considered, not only the one chosen.
**Which roadmap project uses the knowledge:** the local retrieval stack — first
its embeddings, then its reranking step.
**What exercise proves I understood it:** D-w06-1, whose write-up names the
licence of every model it benchmarked.

### Judge model availability

**Claim:** one cheap judge tier already carries a published retirement date
inside this programme's horizon, so a judge must be pinned **with a documented
fallback**. Judge inference runs roughly USD 0.0004 to 0.0075 per item — near
free against the monthly cap, confirming judge cost never sizes an eval set.
**Supporting span:** canon marks the judge policy volatile and requires a
documented fallback.
**Re-verify by:** 2026-11-30.
**What exactly to learn from it:** never make a deprecating model the sole check
where deterministic ground truth exists.
**Which chapters or sections matter:** the provider's deprecation schedule.
**Which roadmap project uses the knowledge:** S6's three regression tiers.
**What exercise proves I understood it:** D-w10-1, whose threshold survives a
judge swap because it is stated as a bound with a re-baselining condition.

## Deliberately excluded

Four claims were considered and are **kept out of this repository entirely**,
which is a different act from recording them with a date. Each failed the
sourcing bar, and naming the failure is what stops it being rediscovered and
quietly admitted later.

**Numbered identifiers from the OWASP LLM list.** Two live editions, no primary
refetch, and a reported renumbering. Category names carry the whole teaching
value; the numbers carry only the risk of citing a stale one.

**Any percentage for prompt-injection defence effectiveness.** No independently
verified primary benchmark met the bar. The programme measures attack success
rate against its own systems instead, which is the brief's requirement anyway
and is a stronger claim than a borrowed figure.

**Specific terms of the second harness's service agreement.** That page returned
an HTTP 403 to direct fetch and could only be characterised from secondary
sources, so nothing about it is stated as verified.

**Any figure for the reply-rate uplift of one outreach channel over another.**
Every available number comes from vendors selling tooling for the channel they
are promoting, with no independent corroboration. The honest statement is that
upside may be going unclaimed and that it cannot be sized.
