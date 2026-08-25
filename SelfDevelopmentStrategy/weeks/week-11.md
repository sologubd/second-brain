# Week 11 — AI Security and Adversarial Testing

## Outcome

By Sunday you have redirected your own agent using content it *retrieved* rather
than anything you typed, got private data out through a channel that does not look
like one, and then made both impossible **in code** — with an assertion that fails
when you switch the control off. You can state precisely which part of your
defence is a security boundary and which part is defense in depth.

## Why now?

You now have something worth attacking: an agent that holds private data, reads
content strangers wrote, and can reach the network. That is the whole risk
condition, and it did not exist in week 2. Attacking it before week 10 would have
meant attacking a fixture.

Building retrieval and attacking it are the same project seen twice, and the second
view is the one that decides whether the first was built properly.

## Build

### Where the security boundary actually is

This is the distinction the week exists to teach, and it is easy to state wrongly.

**Structural context separation** — provenance tags, trust tiers, a clear
delimiter between operator instructions and document content — is worth building.
It reduces instruction/data confusion, it gives you provenance you can log and
reason about, and it is genuine **defense in depth**.

**It does not make prompt injection impossible.** A separator is a convention the
model is *more likely* to respect, not a control it *cannot* cross. Treating it as
a boundary is the mistake, because it moves the guarantee inside the model — and
anything inside the model is a probability, not a property.

The real boundary lives outside the model's cooperation:

```
untrusted input observed
        ↓
code-enforced policy          ← a decision your code makes, not the model
        ↓
sensitive capability unavailable, or gated behind an explicit
trusted authorization path
```

Concretely: a turn that consumed untrusted retrieved content **cannot** invoke an
external-send capability. Not *should not* — the capability is not reachable from
that turn's tool set, and the code that decides this never reads the untrusted
content at all.

Three inequalities worth writing on the wall:

- **prompt instruction ≠ authorization control**
- **separator ≠ security boundary**
- **model refusal ≠ security guarantee**

A prompt-level patch asks the model to be careful and moves the rate a little; a
structural change removes the class. Which of the two you did is the examinable
question, every time — and "I added a separator" is the first answer.

### What to build

In this order. Build it before you run the second arm of each attack:

1. **Provenance tagging at ingest.** Every chunk records where it came from and
   what tier of trust that origin carries. *(Defense in depth, and the input the
   policy reads.)*
2. **Trust-tiered retrieval.** Retrieved content carries its tier through to
   context assembly. *(Defense in depth.)*
3. **A delimiter** between operator instructions and document content.
   *(Defense in depth — reduces confusion, guarantees nothing.)*
4. **The code-enforced capability restriction.** Track, outside the model, whether
   this turn has consumed untrusted content. If it has, the external-send tool is
   **not in the tool set**. This is the actual control, and it is the only item in
   this list that is one.
5. **Output validation** before anything leaves, as a second layer behind (4).

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
- **The security property must come from code, not model cooperation.** Prove it by
  disabling the control and watching the assertion fail. If the only evidence is
  that the model declined, you have measured today's model, not your system.
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

### Core — required (~15h: 2.5h learning, 9.5h building/testing, 3h business)

**One real indirect-injection path and one exfiltration path, each measured before
and after a code-enforced mitigation.** That is the week. Additional attack
classes are Stretch, or they belong to months 4–6.

1. **Attack 1 — indirect injection, one path done properly.** The payload lives in
   a document the retrieval layer selects **on its own merits** — one pasted into
   the prompt tests a different class. Use a frozen query set. Record, for every
   attempt, whether an external-send tool was reached: that field separates an
   attack that bent the answer from one that reached the network, and they are not
   equally bad.
2. **Attack 2 — exfiltration, one covert route.** The data rides inside something
   helpful-looking — a parameter in a URL the agent offers, for instance. A direct
   ask alone tests refusal training, not architecture.
3. **Build provenance tagging at ingest**, so origin and trust tier travel with
   every chunk.
4. **Build the code-enforced capability restriction** — the actual control. A turn
   that consumed untrusted content cannot reach the external-send tool, decided
   outside the model. **Write the assertion that fails when you disable it**: that
   assertion is the only thing that proves the refusal came from code rather than
   from the model's cooperation, and without it you have a hopeful system.
5. **Measure both attacks, both arms.** Same payloads, same frozen query set,
   exactly one mitigation between the arms. Report rates with denominators.
6. **State what you actually did to the trifecta** — which leg you removed
   (private data access, untrusted-content exposure, outbound communication) and
   what you merely *filtered*. A regex over outbound URLs is a filter and must be
   labelled as one. Defend the claim in writing against the alternative reading.
7. **Business: the offer sketch.** Run the qualification checklist against the pain
   register, pick the highest qualified pain, and write a one-paragraph
   fixed-scope, fixed-price offer with an explicit exclusions list — exclusions
   written *before* the price. In
   [consulting-and-saas.md](../business/consulting-and-saas.md).

### Stretch — only after Core is DONE

- **Add the delimiter and trust-tiered retrieval** as defense in depth on top of
  the code control, and measure whether they move the rate at all. Interesting
  either way: if they barely move it, that is the week's lesson made numeric.
- **Corpus poisoning as a separate attack**: seed your index with three genuinely
  distinct mechanisms — instruction override, persona override, delimiter/format
  confusion — against a clean control index. Three phrasings of one mechanism do
  not count.
- **A second and third payload style** on the injection path, to see whether your
  control holds shape or only holds against what you thought of.
- **A second exfiltration route**, including a direct request, for contrast with
  the covert one.
- **Write the three-way category distinction** — corpus poisoning versus memory
  poisoning versus goal hijack — and place your own attacks on it, saying why not
  the other rows. Table in
  [exercises/ai-security.md](../exercises/ai-security.md). Cheap and clarifying;
  do this one even if you skip the rest.
- **Resolve the SaaS evidence thresholds** to concrete numbers with a line of
  justification each.
- **Retrieval precision before and after** the mitigation, to show whether the
  control cost you ordinary answer quality.

## Use it for real

Your own index, your own agent, your own corpus. Not a fixture, not a public demo
target. The whole value of these numbers is that they describe the thing you
shipped.

## Measure

Per attack, per arm, with the denominator stated:

- **Attack success rate** = attempts that changed agent behaviour ÷ attempts in the
  frozen set.
- **External-send rate** = attempts that reached an external-send tool ÷ hostile-text
  turns. Before and after. **This is the headline number**, because it is the one
  your code control is responsible for.
- **Exfiltration success rate** for the covert route, both arms, re-run post-fix
  with the same payload and measured directly.
- *(Stretch)* retrieval precision before and after, and token cost per attempt.

## Failure exercise

The attacks above *are* this week's failure work, and the indirect-injection arm
carries the five-part write-up:

- **Detection.** Hold the run against a twin over a clean corpus and look for
  divergence. You detect a difference between two outputs, not a known string.
- **Safe failure.** Give retrieved text no standing. The load-bearing part is the
  last one: **denied the power to authorise a call, in code.** Origin tagging and
  the delimiter help and are not the control — a defence consisting only of those
  two has asked the model nicely.
- **Recovery.** Remove outbound capability from any turn that read hostile text in
  that cycle. That removes a leg rather than screening it, and telling those apart
  is the skill being examined.
- **Logging.** The style, the query, both outputs, and whether an outbound call was
  attempted.
- **Proving test.** Three or more styles over one frozen query list, rates from both
  arms with denominators, zero borrowed figures. **The version that folds document
  text into the instruction context fails outright.**

## Deliverables

- [ ] Provenance tagging at ingest, with origin and trust tier on every chunk.
- [ ] **The code-enforced capability restriction**, plus the assertion that fails
      when it is disabled.
- [ ] Attack report covering the injection path and the covert exfiltration route:
      rates before and after, denominators stated, per-attempt records including
      failures.
- [ ] A written statement of which parts of your defence are security boundaries
      and which are defense in depth.
- [ ] The trifecta leg-removal argument, defended against the alternative reading,
      with anything that is a filter labelled as one.
- [ ] Offer sketch from the qualified pain register.
- [ ] *(Stretch, if reached)* delimiter and trust tiers with their measured effect;
      corpus poisoning; extra payload styles; the category distinction.

## Done when

- [ ] The injection payload was selected by retrieval **on its own merits**, not
      pasted into the prompt.
- [ ] Both arms ran against the identical frozen query set, with zero queries added
      or removed and exactly one mitigation between them.
- [ ] Attack success rate and external-send rate are reported per arm, each with
      its denominator.
- [ ] **Zero** turns that touched untrusted input reached an external-send tool
      after the mitigation.
- [ ] The refusal is demonstrated to come from **code**, by an assertion that fails
      when the control is disabled. Nothing rests on the model having declined.
- [ ] The write-up states plainly that the delimiter and trust tiers are defense in
      depth, not a boundary — and names what the boundary actually is.
- [ ] The exfiltration route was covert, and it was re-run post-fix with the same
      payload and measured directly.
- [ ] The report contains zero industry-sourced percentages.
- [ ] The offer names exactly one outcome, lists ≥3 explicit exclusions, and the
      qualification checklist is answered on all 6 items with ≥4 yes.

## Reflection

1. Did your mitigation remove the class or reduce a rate? Name the property that
   makes your answer true rather than hopeful — and if the honest answer is "the
   model complied", say so.
2. If an attacker read your entire mitigation, which payload would they write next?
   Would your **code** control still hold, or only your delimiter?
3. Your agent holds private data, reads untrusted content and can reach the
   network. Which of the three is genuinely required by the product, and what would
   the product lose without it?
4. Which exclusion would you have forgotten if you had written the offer during a
   call rather than before one?

## Evidence

- Attack report: both attacks, both arms, all rates with denominators.
- Per-attempt records, failures included.
- **The control-disabled assertion**, and proof it fails when the control is off.
- The boundary-versus-defense-in-depth write-up and the leg-removal argument.
- Offer sketch.
- Anything from Stretch that was reached, and a note of what was not.

**Hours logged:** learning ___ / building ___ / testing ___ / business ___
