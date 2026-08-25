# Week 11 — AI Security and Adversarial Testing

## Outcome

By Sunday you have redirected your own agent using content it *retrieved* rather
than anything you typed, counted what fraction of those attempts actually changed
its behaviour, got private data out through a channel that does not look like one,
and then broken a leg of the trifecta **structurally** rather than filtering for
it.

## Why now?

You now have something worth attacking: an agent that holds private data, reads
content strangers wrote, and can reach the network. That is the whole risk
condition, and it did not exist in week 2. Attacking it before week 10 would have
meant attacking a fixture.

Building retrieval and attacking it are the same project seen twice, and the second
view is the one that decides whether the first was built properly.

## Build

**The untrusted-content boundary, in code**, and in this order — build it before
you run the second arm of each attack:

1. **Provenance tagging at ingest.** Every chunk records where it came from and
   what tier of trust that origin carries.
2. **Trust-tiered retrieval.** Retrieved content carries its tier through to the
   context assembly.
3. **A hard separator** between operator instructions and document content, which
   the model cannot be argued across because it is not a request — it is structure.
4. **Output validation** before anything leaves.
5. **The structural trifecta break:** a turn that touched untrusted input in that
   cycle cannot invoke an external-send tool. Enforced in code, and logged.

**Telling the model to ignore instructions in documents is the prompt-level patch
this week exists to discredit.** A prompt-level patch asks the model to be careful
and moves the rate a little; a structural change removes the class. Which of the
two you did is the examinable question, every time.

## Method — the same shape for every attack

Control run → attack → measure → apply **exactly one** structural mitigation →
re-measure against the same control.

Non-negotiables, because they are what separate a measurement from a story:

- **The query set is frozen before the first arm and identical in the second.** A
  query added after seeing results is a new experiment.
- **Exactly one mitigation separates the arms.** Two produce a number you cannot
  attribute.
- **Every attempt is recorded, failures included**, or the denominator is unknown.
- **Detection means deviation from the control output, never recognition of a
  payload.** A detector that only catches payloads it has already seen is a
  denylist, and the next payload walks past it.
- **Zero borrowed industry percentages.** A number about somebody else's system
  proves nothing about yours. Measure your own or say nothing.

## Learn

- [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).
  Short. Private data + untrusted content + outbound channel.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/) — the PDF, not
  a vendor summary. Read goal hijack, tool misuse, identity and privilege abuse,
  memory and context poisoning, plus the least-agency framing: autonomy where it is
  not needed widens the attack surface for nothing. Cite by category *name*; the
  numbering has changed between editions.

~2.5h.

## Tasks

1. **Attack 1 — corpus poisoning.** Seed your own index with an injection corpus
   using at least three genuinely distinct mechanisms: instruction override,
   persona/role-play override, delimiter/format confusion. Three phrasings of one
   mechanism do not count. Run a fixed query set against a clean control index and
   the poisoned one. Measure the difference.
2. **Attack 2 — indirect injection.** Payloads live in documents that the
   retrieval layer selects **on their own merits** — one pasted into the prompt
   tests a different class. At least three payload styles, both arms, and record
   for every attempt whether an external-send tool was reached. That field
   separates an attack that bent the answer from one that reached the network, and
   they are not equally bad.
3. **Attack 3 — exfiltration.** At least two routes, at least one **covert** — the
   data riding inside something helpful-looking, such as a parameter in a URL the
   agent offers. A direct ask alone tests refusal training, not architecture. Then
   break a leg structurally and re-run both routes with the *same* payloads, not
   improved ones.
4. **Build the boundary** (the five pieces above), enforced in code, with an
   assertion that fails when the boundary is disabled — that assertion is how you
   prove the refusal came from code rather than from the model's cooperation.
5. **Write the three-way category distinction** and place your own attacks on it.
   Corpus poisoning, memory poisoning and goal hijack are routinely collapsed into
   one thing; the table is in
   [exercises/ai-security.md](../exercises/ai-security.md). A report that cannot
   place its own attack on it has not understood what it ran.
6. **State which trifecta leg you removed** — private data access, untrusted-content
   exposure, or outbound communication — and which you merely *filtered*. Defend it
   in writing against the alternative reading. A regex over outbound URLs is a
   filter and must be labelled as one if that is what you built.
7. **Business: the offer sketch.** Run the qualification checklist against the pain
   register, pick the highest qualified pain, and write a one-paragraph
   fixed-scope, fixed-price offer with an explicit exclusions list — exclusions
   written *before* the price. Also resolve the SaaS evidence thresholds to concrete
   numbers. Both in
   [consulting-and-saas.md](../business/consulting-and-saas.md).

## Use it for real

Your own index, your own agent, your own corpus. Not a fixture, not a public demo
target. The whole value of these numbers is that they describe the thing you
shipped.

## Measure

Per attack, per technique, per arm, with the denominator stated:

- **Attack success rate** = attempts that changed agent behaviour ÷ attempts in the
  fixed set.
- **External-send rate** = attempts that reached an external-send tool ÷ hostile-text
  turns. Before and after.
- **Exfiltration success rate** per route, both arms, including the covert route
  re-run post-fix and measured directly.
- **Retrieval precision** before and after the mitigation — to show whether the
  boundary cost you ordinary answer quality.
- Token cost per attempt: a covert channel that costs the attacker very little is a
  different risk from one that costs a lot.

## Failure exercise

The three attacks above *are* this week's failure work, and the indirect-injection
arm carries the five-part write-up:

- **Detection.** Hold the run against a twin over a clean corpus and look for
  divergence. You detect a difference between two outputs, not a known string.
- **Safe failure.** Give retrieved text no standing: origin tagged at index time,
  kept beyond a separator, and denied the power to authorise a call. All properties
  of code, not requests.
- **Recovery.** Remove outbound capability from any turn that read hostile text in
  that cycle. That removes a leg rather than screening it, and telling those apart
  is the skill being examined.
- **Logging.** The style, the query, both outputs, and whether an outbound call was
  attempted.
- **Proving test.** Three or more styles over one frozen query list, rates from both
  arms with denominators, zero borrowed figures. **The version that folds document
  text into the instruction context fails outright.**

## Deliverables

- [ ] Trust boundary: provenance at ingest, trust-tiered retrieval, hard operator/
      document separator, output validation, structural trifecta break — with the
      assertion that fails when the boundary is disabled.
- [ ] Attack report covering all three attacks: three techniques minimum each,
      rates before and after, denominators stated, per-attempt records including
      failures.
- [ ] The three-way category distinction written out, with your attacks placed on
      it and a reason for the rows you did *not* place them in.
- [ ] The trifecta leg-removal argument, defended against the alternative reading.
- [ ] Cited-answer contract hardened: an answer whose citation is absent from
      retrieved context is rejected.
- [ ] Offer sketch from the qualified pain register; SaaS evidence thresholds
      resolved to concrete numbers with one line of justification each.

## Done when

- [ ] At least 3 genuinely distinct techniques per attack, run against the same
      frozen query set in both arms, with zero queries added or removed between
      them.
- [ ] Attack success rate is reported per technique, per arm, with its denominator.
- [ ] Zero turns that touched untrusted input successfully invoked an external-send
      tool after the mitigation.
- [ ] The refusal is demonstrated to come from **code**, by an assertion that fails
      when the boundary is disabled.
- [ ] The report names exactly one trifecta leg as removed, with the reasoning
      stated, and labels anything else as a filter.
- [ ] At least one exfiltration route was covert, and it was re-run post-fix and
      measured directly.
- [ ] The report contains zero industry-sourced percentages.
- [ ] The offer names exactly one outcome, lists ≥3 explicit exclusions, and the
      qualification checklist is answered on all 6 items with ≥4 yes.

## Reflection

1. Did your mitigation remove the class or reduce a rate? Name the property that
   makes your answer true rather than hopeful.
2. If an attacker read your entire mitigation, which payload would they write next?
3. Your agent holds private data, reads untrusted content and can reach the
   network. Which of the three is genuinely required by the product, and what would
   the product lose without it?
4. Which exclusion would you have forgotten if you had written the offer during a
   call rather than before one?

## Evidence

- Attack report: three attacks, all arms, all rates with denominators.
- Per-attempt records, failures included.
- The boundary-disabled assertion.
- Retrieval precision before and after.
- Category-placement write-up and the leg-removal argument.
- Offer sketch; resolved thresholds.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
