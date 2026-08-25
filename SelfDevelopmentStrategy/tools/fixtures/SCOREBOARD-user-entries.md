<!-- FIXTURE (control, must SURVIVE `make regen` byte-identical).
     This is a partially generated SCOREBOARD carrying four user regions:
     three whose keys canon still defines, and one (SM-99) whose key it does
     not. `gen-derived --selftest` regenerates against this file and asserts
     that every body below is preserved BYTE-FOR-BYTE, that SM-99 lands under
     `## Orphaned entries` rather than being dropped or misaligned onto the
     wrong metric, and that a second regeneration is a no-op.

     These numbers are what the month-01 retrospective reads to recalibrate
     weeks 05-12. If a regeneration eats them, the programme's only
     self-correction mechanism loses its input. -->

# Scoreboard

## How to update this

22 metrics in 3 groups — 7 Engineering / 7 Agent harness / 8 Business.

## Engineering

### SM-01 — production-like projects completed

- unit: count
- cadence: monthly

<!-- user:actuals key="SM-01" -->
| week | value | evidence_source |
|---|---|---|
| W01 | 0 | real |
| W02 | 0 | real |
| W03 | 1 | real |
<!-- /user:actuals -->

### SM-05 — failure scenarios handled

- unit: count
- cadence: weekly

<!-- user:actuals key="SM-05" -->
W01: 1 (EX-FAIL-01, proving test red before the fix)
W02: 2   <- trailing spaces on this line are deliberate; byte-for-byte means bytes
W03: 2
<!-- /user:actuals -->

## Business

### SM-15 — prospects researched

- unit: count
- cadence: weekly

<!-- user:actuals key="SM-15" -->
W01: 10 real
W02: 8 real
W03: 6 real   (all hand-researched, no assisted extraction yet)
<!-- /user:actuals -->

## Orphaned entries

**`SM-99`** — a metric that used to exist and was removed by a canon delta.

<!-- user:actuals key="SM-99" -->
W01: 3
W02: 4
This body must survive verbatim even though canon no longer defines SM-99.
<!-- /user:actuals -->
