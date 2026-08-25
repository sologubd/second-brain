# Consistency tooling for the AI-native engineering programme.
#
#   make check      every checker, plus `gen-derived --check`, plus the fixtures
#   make regen      rewrite the generated files from canon
#   make delta      scaffold a canon-delta stub from a month's retrospective
#   make fixtures   prove each checker can actually fail
#   make demo-s0    a stage demo; one target per canon runnable_demo_command
#
# Canon (`canon/canon.yaml`) is the single source of truth. Prose expands it and
# never invents. The generated files are rewritten from it, outside the
# `<!-- user:actuals -->` regions, which are preserved byte-for-byte.
#
# The monthly loop is: answer the retrospective -> `make delta` -> edit canon
# -> bump `meta.version` -> `make regen` -> `make check`. `make delta` is the
# only target that helps you WRITE canon rather than only check it, and it
# exists because a retrospective with no path into canon is a diary.

PYTHON ?= python3

CHECKERS = \
	check-schema \
	check-links \
	check-canon \
	check-hours \
	check-dupes \
	check-antigoals \
	coverage-report

# Each entry is `name:argv`. The command MUST exit non-zero. A checker that
# cannot fail is worse than no checker, and this table is the control that
# proves each one can.
FIXTURES_MUST_FAIL = \
	"check-schema / missing section:tools/check-schema.py --schema week tools/fixtures/week-missing-section.md" \
	"check-schema / hours sum 14.5:tools/check-schema.py --schema week tools/fixtures/week-bad-hours.md" \
	"check-schema / unreferenced task:tools/check-schema.py --schema week tools/fixtures/week-unreferenced-task.md" \
	"check-links / three link defects:tools/check-links.py tools/fixtures/broken-link.md" \
	"check-canon / numeric disagrees:tools/check-canon.py --as weeks/week-01.md tools/fixtures/canon-numeric-mismatch.md" \
	"check-hours / week sums to 14.5:tools/check-hours.py --canon tools/fixtures/canon-bad-hours.yaml" \
	"check-dupes / shared 12-gram span:tools/check-dupes.py tools/fixtures/dupe-a.md tools/fixtures/dupe-b.md" \
	"check-antigoals / AG-08, AG-09:tools/check-antigoals.py tools/fixtures/antigoal-leetcode.md" \
	"check-antigoals / AG-12, AG-02:tools/check-antigoals.py tools/fixtures/antigoal-vague.md" \
	"coverage-report / unmapped rows:tools/coverage-report.py --quiet --canon tools/fixtures/canon-uncovered.yaml"

# The controls. These MUST exit zero. Without them a checker could pass its
# failing fixtures by rejecting everything it is ever shown.
FIXTURES_MUST_PASS = \
	"check-schema / a valid week:tools/check-schema.py --schema week tools/fixtures/week-valid.md" \
	"check-canon / a valid week:tools/check-canon.py --as weeks/week-01.md tools/fixtures/week-valid.md" \
	"check-antigoals / both answered:tools/check-antigoals.py tools/fixtures/antigoal-justified.md" \
	"gen-derived / user entries survive:tools/gen-derived.py --selftest"

.PHONY: help check regen delta fixtures
.DEFAULT_GOAL := help

help:
	@echo 'make check      run every checker, gen-derived --check, and the fixture suite'
	@echo 'make regen      regenerate ROADMAP.md, SCOREBOARD.md and canon/CANON.md from canon'
	@echo 'make delta MONTH=05 [FORCE=1]'
	@echo '               scaffold canon/deltas/M05-canon-delta.md from that retrospective'
	@echo 'make fixtures   prove every checker can fail, and that none fails everything'
	@echo 'make demo-s0 TASK=tasks/example.md'
	@echo '               a stage demo; every canon runnable_demo_command is a target here,'
	@echo '               and each one wraps the `python -m agentplat.<module>` form'

check: fixtures
	@failed=''; \
	for tool in $(CHECKERS); do \
		printf '\n=== %s ===\n' "$$tool"; \
		$(PYTHON) tools/$$tool.py || failed="$$failed $$tool"; \
	done; \
	printf '\n=== gen-derived --check ===\n'; \
	$(PYTHON) tools/gen-derived.py --check || failed="$$failed gen-derived"; \
	echo; \
	if [ -n "$$failed" ]; then echo "make check: FAILED —$$failed"; exit 1; fi; \
	echo 'make check: all green'

regen:
	@$(PYTHON) tools/gen-derived.py

delta:
	@if [ -z "$(MONTH)" ]; then \
		echo 'usage: make delta MONTH=05   (add FORCE=1 to overwrite an existing stub)'; \
		exit 2; \
	fi
	@$(PYTHON) tools/gen-derived.py --delta $(MONTH) $(if $(FORCE),--force,)

fixtures:
	@echo '=== fixtures: each checker against a deliberately malformed input ==='
	@broken=''; \
	for spec in $(FIXTURES_MUST_FAIL); do \
		name=$${spec%%:*}; argv=$${spec#*:}; \
		printf '  %-40s ' "$$name"; \
		if $(PYTHON) $$argv >/dev/null 2>&1; then \
			echo 'BROKEN — the checker PASSED a malformed input'; broken="$$broken [$$name]"; \
		else \
			echo 'ok — fails as designed'; \
		fi; \
	done; \
	for spec in $(FIXTURES_MUST_PASS); do \
		name=$${spec%%:*}; argv=$${spec#*:}; \
		printf '  %-40s ' "$$name"; \
		if $(PYTHON) $$argv >/dev/null 2>&1; then \
			echo 'ok — passes as designed'; \
		else \
			echo 'BROKEN — the checker FAILED a valid input'; broken="$$broken [$$name]"; \
		fi; \
	done; \
	if [ -n "$$broken" ]; then echo "make fixtures: FAILED —$$broken"; exit 1; fi

# ---------------------------------------------------------------------------
# RUNNABLE DEMOS — one target per stage in canon `projects.*.stages[]`.
#
# THE MAKE TARGET IS THE CANONICAL ENTRY POINT. Canon's
# `stages[].runnable_demo_command` is always the `make` form, and every target
# below is a thin wrapper around the module form it shells — so there is one
# command to type, one place the flags live, and no second spelling for prose
# to drift onto. `canon.projects.platform.demo_target_rule.wrapped_forms` maps
# each target to the module invocation it wraps, and this file is what proves
# the mapping is real rather than described.
#
# The package is `agentplat`, never `platform`: a repo-root package named
# `platform` shadows the Python standard library for every process started
# here, and the resulting ModuleNotFoundError surfaces from inside unrelated
# library code rather than at the call site. See
# `canon.projects.platform.python_package`.
#
# A target fails with ModuleNotFoundError until the week that builds its stage.
# That is the intended reading: a stage with no runnable demo command has not
# shipped, and a demo command with nothing behind it has not either.
# ---------------------------------------------------------------------------

PKG ?= agentplat

# `$(call need,VAR,make demo-s0 TASK=tasks/example.md)` — fail with the usage
# line rather than with a module traceback about an empty argument.
need = @if [ -z "$($(1))" ]; then echo 'usage: $(2)'; exit 2; fi

.PHONY: demo-s0 demo-s1a demo-s1b-replay demo-s2 demo-s2b demo-s3 demo-s4-chaos \
        demo-s5 trace-view gate-all demo-s7a-attack demo-s7b-deputy demo-s8 demo-s9 \
        demo-ska-s0 demo-ska-s1 ska-metrics demo-ska-s2-authz \
        demo-boa-s0 demo-boa-s1 demo-boa-s2-memory

demo-s0:                       ## S0 (W01) — wraps: python -m agentplat.run $(TASK)
	$(call need,TASK,make demo-s0 TASK=tasks/example.md)
	@$(PYTHON) -m $(PKG).run $(TASK)

demo-s1a:                      ## S1a (W02) — wraps: python -m agentplat.run --resume-demo
	@$(PYTHON) -m $(PKG).run --resume-demo

demo-s1b-replay:               ## S1b (W03) — wraps: python -m agentplat.replay --n $(N)
	$(call need,N,make demo-s1b-replay N=100)
	@$(PYTHON) -m $(PKG).replay --n $(N)

demo-s2:                       ## S2 (W04) — wraps: python -m agentplat.run --gate --pr $(TASK)
	$(call need,TASK,make demo-s2 TASK=tasks/example.md)
	@$(PYTHON) -m $(PKG).run --gate --pr $(TASK)

demo-s2b:                      ## S2b (M04) — wraps: python -m agentplat.review --pr $(PR)
	$(call need,PR,make demo-s2b PR=<number>)
	@$(PYTHON) -m $(PKG).review --pr $(PR)

demo-s3:                       ## S3 (W07) — wraps: python -m agentplat.sentry --issue $(ISSUE)
	$(call need,ISSUE,make demo-s3 ISSUE=<sentry-id>)
	@$(PYTHON) -m $(PKG).sentry --issue $(ISSUE)

demo-s4-chaos:                 ## S4 (W08) — wraps: python -m agentplat.chaos --workers .. --kill-pct ..
	$(call need,WORKERS,make demo-s4-chaos WORKERS=4 KILL_PCT=30)
	$(call need,KILL_PCT,make demo-s4-chaos WORKERS=4 KILL_PCT=30)
	@$(PYTHON) -m $(PKG).chaos --workers $(WORKERS) --kill-pct $(KILL_PCT)

demo-s5:                       ## S5 (W09) — wraps: python -m agentplat.run --trace
	@$(PYTHON) -m $(PKG).run --trace

trace-view:                    ## S5 (W09) — wraps: python -m agentplat.trace --view
	@$(PYTHON) -m $(PKG).trace --view

gate-all:                      ## S6 (W10) — wraps: python -m agentplat.gates --all
	@$(PYTHON) -m $(PKG).gates --all

demo-s7a-attack:               ## S7a (W11) — wraps: python -m agentplat.attack --suite trust-boundary
	@$(PYTHON) -m $(PKG).attack --suite trust-boundary

demo-s7b-deputy:               ## S7b (W12) — wraps: python -m agentplat.attack --suite confused-deputy
	@$(PYTHON) -m $(PKG).attack --suite confused-deputy

demo-s8:                       ## S8 (M04) — wraps: python -m agentplat.notion --task $(NOTION_TASK)
	$(call need,NOTION_TASK,make demo-s8 NOTION_TASK=<id>)
	@$(PYTHON) -m $(PKG).notion --task $(NOTION_TASK)

demo-s9:                       ## S9 (M05-M08) — wraps: python -m agentplat.adr --request $(REQUEST)
	$(call need,REQUEST,make demo-s9 REQUEST=<path>)
	@$(PYTHON) -m $(PKG).adr --request $(REQUEST)

demo-ska-s0:                   ## SKA-S0 (W05) — wraps: python -m agentplat.ska.retrieve --query .. --tenant ..
	$(call need,QUERY,make demo-ska-s0 QUERY='...' TENANT=a)
	$(call need,TENANT,make demo-ska-s0 QUERY='...' TENANT=a)
	@$(PYTHON) -m $(PKG).ska.retrieve --query $(QUERY) --tenant $(TENANT)

demo-ska-s1:                   ## SKA-S1 (W06) — wraps: python -m agentplat.ska.answer
	@$(PYTHON) -m $(PKG).ska.answer

ska-metrics:                   ## SKA-S1 (W06) — wraps: python -m agentplat.ska.metrics
	@$(PYTHON) -m $(PKG).ska.metrics

demo-ska-s2-authz:             ## SKA-S2 (M04-M06) — wraps: python -m agentplat.ska.authz --demo
	@$(PYTHON) -m $(PKG).ska.authz --demo

demo-boa-s0:                   ## BOA-S0 (W03) — wraps: python -m agentplat.boa.extract --url $(URL)
	$(call need,URL,make demo-boa-s0 URL=<company-url>)
	@$(PYTHON) -m $(PKG).boa.extract --url $(URL)

demo-boa-s1:                   ## BOA-S1 (W04) — wraps: python -m agentplat.boa.outreach --prospect $(PROSPECT)
	$(call need,PROSPECT,make demo-boa-s1 PROSPECT=<id>)
	@$(PYTHON) -m $(PKG).boa.outreach --prospect $(PROSPECT)

demo-boa-s2-memory:            ## BOA-S2 (M05) — wraps: python -m agentplat.boa.memory --account $(ACCOUNT)
	$(call need,ACCOUNT,make demo-boa-s2-memory ACCOUNT=<id>)
	@$(PYTHON) -m $(PKG).boa.memory --account $(ACCOUNT)
