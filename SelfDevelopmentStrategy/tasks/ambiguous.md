---
id: T-EX-002
target_repo: ../agentplat-sandbox
files: []
---

# Clean up the rates module

The rates code has grown awkward and could do with a tidy-up. Make it better.

This file is a FIXTURE, and it is deliberately underspecified. Three of the
elements the pre-dispatch specificity score requires are absent: `files` is
empty, `done_condition` is missing, and there are no `assertions`. It exists so
EX-FAIL-01's proving test has something that must be refused before any model
call, alongside `example.md`, which must dispatch. A suite carrying only the
valid fixture passes against a runner that refuses everything, which is why the
pair is the smallest honest test.

Do not repair this file. Repairing it deletes the test.
