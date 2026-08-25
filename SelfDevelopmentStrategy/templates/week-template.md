# Week file template

## When to use this

Reach for this when a week file has to be authored or re-authored by hand: the
calendar slipped and a week needs re-planning, a canon delta restructured one,
or work extends past the twelve that already exist. It is not for weekly
logging. Hours logged between Monday and Sunday go inside the
`<!-- user:actuals -->` region of the week file you already hold, and nothing
else in that file moves until a month boundary and the loop in
[HOW-TO-EDIT.md](../HOW-TO-EDIT.md).

Eleven sections, fixed order, none optional. Adding a twelfth fails the same
check that dropping one fails, so the block below is the whole permitted
surface. Four constraints inside it are mechanical rather than stylistic. The
time-budget labels are literal strings and their values total 15.0 h. Every
numbered task must be named by at least one acceptance criterion through its own
id — and the criterion may only carry an id whose work its predicate genuinely
tests, so where the predicate is too narrow, widen the predicate instead of
appending the id. Deliverables cap at four. Reflection runs at least three
numbered entries, each answerable only by whoever did the work.

Three further requirements are easy to skip and each exists because skipping it
broke something. A task line names its **budget bucket** — theory, building,
testing or business — not only its track letter, because actuals are logged per
bucket and the first retrospective's hour recalibration reads them bucket by
bucket. A theory task names the `RES-` id it reads; an hour of reading that names
no document is an hour the reader has to source. And a deliverable names **the
path it lands at**, because a deliverable with no path can be ticked by nobody
but its author.

The weekly review is not in the 15 hours. Filling
[the review form](weekly-review.md), scoring the week and updating the scoreboard
sits outside the budget and takes about twenty minutes — stated here and in
[the README](../README.md) so the obligation is not silently unfunded.

Two sections are routinely left thin, and in a real week both must be populated
rather than merely present. The failure exercise expands all five named parts
for every exercise the week carries: the structural check sweeps the section
once as a whole, so summarising a second exercise slips through and teaches
nobody anything. The weekly score states allocations explicit enough to be
recomputed by someone else, and they add up to 100.

## Template

Copy the block whole. It is blank on purpose: structure and placeholders, never
a filled specimen, because a worked example here would collide with the real
week it was lifted from and the duplicate gate would refuse both. Angle brackets
mark what you replace, and every replacement traces to a row in
`canon/canon.yaml` rather than to judgement at the keyboard.

Three details are worth reading before you type over them. The compressed-week
subset belongs in the time budget as a sentence, because any `- Label: number`
line there parses as a fifth budget row and fails the file. The topics grid
earns its fourth column: naming where a topic actually surfaces is what stops
the table becoming a list of technologies. And the evidence section carries the
per-bucket plan-versus-actual line immediately above the logging region, in the
same shape in every week, because the first retrospective's hour recalibration
reads those four figures and freeform prose gives it nothing to parse.

```markdown
# Week N — <name>

## Outcome

<One sentence naming a capability possessed by Sunday.>

## Time budget

- Theory: <n> h
- Building: <n> h
- Testing/evaluation: <n> h
- Customer discovery: <n> h

Compressed week: <the named subset run under the 8h mode, as prose: its hours,
what defers and where, and which deliverable ids stay unticked. It closes
DONE-COMPRESSED, not DONE.>

## Topics

| Topic | Track | Priority | Where it surfaces this week |
| --- | --- | --- | --- |
| <topic> | <track letter> | <priority, or the canon verdict string> | <task, stage or deliverable id> |

## Tasks

### Task 1

`T-wNN-1` — <n> h, Track <primary>, <bucket>, reinforcing <other>. Reading:
`RES-NN` (theory tasks only). <what it produces>

### Task 2

`T-wNN-2` — <n> h, Track <primary>, <bucket>, reinforcing <other>. <what it produces>

## Deliverables

- [ ] `D-wNN-1` — <artifact, with the path it lands at>

## Acceptance criteria

- [ ] `AC-wNN-1a` — <predicate carrying a number or an artifact path> (`T-wNN-1`)

## Stretch goal

<Optional, named, and never a prerequisite of any criterion above.>

## Failure exercise

### <EX-FAIL-NN> — <name>

- **Detection.** <how the failure becomes visible>
- **Safe failure behaviour.** <what happens instead of proceeding>
- **Recovery.** <how state is restored>
- **Logging.** <what is written, and where>
- **Test proving the mitigation.** <the test, and that it fails against the pre-mitigation code>

## Reflection

1. <answerable only by someone who did the work>
2. <second>
3. <third>

## Evidence

<commits, pull requests, benchmarks, decision records, interview notes>

Runnable demo: `<command>`

Theory <plan> / <actual> · Building <plan> / <actual> · Testing/evaluation <plan> / <actual> · Customer discovery <plan> / <actual>

<!-- user:actuals key="WNN" -->
_(not yet logged)_
<!-- /user:actuals -->

## Weekly score

| Component | Points |
| --- | --- |
| <component> | <n> |
| **Total** | **100** |
```
