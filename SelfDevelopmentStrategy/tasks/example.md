---
id: T-EX-001
target_repo: ../agentplat-sandbox
files:
  - src/sandbox/rates.py
  - tests/test_rates.py
done_condition: >-
  convert_rate() rejects a negative amount with ValueError instead of returning
  a negative result, and the existing callers still pass.
assertions:
  - pytest tests/test_rates.py -q
  - python -c "import src.sandbox.rates as r; r.convert_rate(-1, 'EUR')" exits non-zero
---

# Reject negative amounts in `convert_rate()`

`convert_rate(amount, currency)` currently multiplies whatever it is handed by a
stored rate, so a negative amount produces a negative converted figure and the
caller reports a refund as income. The rate table itself is correct and must not
be touched.

Raise `ValueError` on a negative amount, at the top of the function, before the
lookup. Add one test for the rejection and leave the existing tests as they are:
this is the first task the runner dispatches unattended, and a diff that also
rewrites the suite is a diff nobody can review against the ticket.

The front matter above is the contract the runner reads. The body is what the
agent reads. The acceptance predicate lives in `assertions`, never here — the
pre-dispatch specificity score looks for it in the front matter and cannot find
a criterion buried in prose.
