# Developer tooling for the aixbdd-en repository itself.
#
# These targets are for people editing THIS repository — not for users of the skills.
# A user's project is supposed to contain `specs/truth/**`, so the invariant checks below
# would be meaningless there. Skill-user invocations stay authoritative in their own skill
# (e.g. `axb-gherkin-and-dsl/SKILL.md` Phase 6 owns the DSL topology audit command).
#
# Why a Makefile: it is the one place that resolves the interpreter, so the three scripts
# and the audit are not documented with differently-drifting command lines (issue #12,
# acceptance criterion 5; cf. #1 finding 7).

SHELL := /bin/bash
.DEFAULT_GOAL := help

# The scripts carry PEP 723 headers (`requires-python >= 3.10`) that only `uv run` honours.
# A bare python3 below 3.10 fails to parse `str | None`. Prefer uv when it is installed;
# fall back to python3 and let check-python report a clear error rather than a SyntaxError.
# RUN must be a *complete* interpreter command, because recipes pass interpreter flags to it
# (`-c`, `-m`). `uv run` alone accepts neither — it needs `uv run python …`.
PYTHON ?= python3
UV := $(shell command -v uv 2>/dev/null)
ifeq ($(strip $(UV)),)
RUN := $(PYTHON)
else
RUN := uv run python
endif

SCRIPTS := scripts
CHECKER := $(SCRIPTS)/check_invariants.py
EXAMPLES := skills/axb-gherkin-and-dsl/examples/ecommerce/features

# `modelith` renders domain-model/aixbdd.modelith.yaml to its sibling .md. It is an
# external Go binary, and scripts/token_registry.json:16 records that this repository
# declined to depend on it — so this check is OPTIONAL and says so out loud when the tool
# is missing. A skipped check that prints nothing reads as a passing one; that is the
# "dropped-but-unprinted" failure the README's coverage rule exists to prevent.
#
# `?=` so a caller (or a test) can set MODELITH explicitly. That makes "the tool is
# absent" a state the suite can construct instead of a property of the machine it runs
# on — the previous version simulated absence by manipulating PATH, which both failed on
# machines with a system-wide install and could not reproduce absence at all once the
# lookup had already run at parse time.
MODELITH ?= $(shell command -v modelith 2>/dev/null)

# The tree the checkers inspect. Defaults to this worktree; the pre-commit hook points it
# at a snapshot of the git *index*, because a commit is built from the index, not from the
# files on disk. Tooling always comes from this worktree; only the inspected tree moves.
ROOT ?= .

# Recursive (`=`, not `:=`) and defined BELOW `ROOT`, both on purpose. The first version
# sat above the `ROOT ?= .` line with `:=`, so ROOT was undefined when it expanded: the
# path became `/domain-model/aixbdd.modelith.yaml`, the target reported the source as not
# found, and it exited 0 under a `NOT CHECKED` line — a passing skip on a tree where the
# check was perfectly possible. `scripts/test_make_targets.py` pins the positive statement
# ("up to date") rather than the absence of a failure, because only that distinguishes a
# real check from that shape of silent one.
MODEL_SOURCE = $(ROOT)/domain-model/aixbdd.modelith.yaml
MODEL_OUTPUT = $(ROOT)/domain-model/aixbdd.modelith.md

.PHONY: help check check-paths check-tokens check-names check-refs check-params check-ui-plan \
        check-model check-audit check-python test install-hooks uninstall-hooks

help: ## List targets
	@echo "Targets for developing aixbdd-en (not for skill users):"
	@echo
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo

check-python: ## Verify the interpreter the scripts need
	@$(RUN) -c 'import sys; assert sys.version_info >= (3, 10), f"python {sys.version.split()[0]} is too old; scripts need >= 3.10 (install uv or set PYTHON)"'
	@echo "interpreter OK: $(RUN) ($(shell $(RUN) -c 'import sys; print("python " + sys.version.split()[0])'))"

check-paths: check-python ## Invariants 1-3: specs/ roots, truth paths, plan-package prefix
	@$(RUN) $(CHECKER) --root $(ROOT) --only paths --quiet-candidates

check-tokens: check-python ## Invariant 4: fixed-token registry vs definitions and naming surfaces
	@$(RUN) $(CHECKER) --root $(ROOT) --only tokens --quiet-candidates

check-names: check-python ## Invariants 7-8: every slash command and §section reference resolves
	@$(RUN) $(CHECKER) --root $(ROOT) --only names --quiet-candidates

check-refs: check-python ## Invariants 5-6: candidate report for normative refs and asserted gates
	@$(RUN) $(CHECKER) --root $(ROOT) --only refs

check-params: check-python ## STANDARDS §4.3: every Default Params cell conforms
	@$(RUN) $(SCRIPTS)/check_dsl_default_params.py --root $(ROOT)

check-ui-plan: check-python ## #24 item 3: every frame/page a ui-plan refers to is declared
	@$(RUN) $(SCRIPTS)/check_ui_plan_outputs.py --root $(ROOT)

# No `check-python` dependency: this target runs a Go binary, not the interpreter, and
# depending on one it does not use would make its failure messages lie about the cause.
#
# Three states, and the middle one is the point:
#   tool absent                        -> NOT CHECKED, exit 0 (optional by design)
#   source absent AND no orphaned .md  -> NOT CHECKED, exit 0 (nothing exists to check)
#   source absent BUT the .md remains  -> FAIL,   exit 1 (a generated file with no source
#                                        is maintained by hand — the very defect this
#                                        target exists to catch, in its worse direction)
#
# `"$(MODELITH)"`, not bare `modelith`: the guard above resolved a path, so invoking the
# bare name looks it up a second time, and if the two shells disagree the guard reports
# installed while the recipe exits 127 with no NOT CHECKED line. One identity decision,
# used everywhere (#26's classifier lesson).
check-model: ## #22 shape 14: the generated domain-model .md still matches its .yaml
	@if [ -z "$(strip $(MODELITH))" ]; then \
		echo "NOT CHECKED: modelith is not installed, so the generated domain-model .md was NOT verified"; \
		echo "  install modelith, or run 'modelith render domain-model/aixbdd.modelith.yaml' by hand"; \
		exit 0; \
	fi; \
	if [ ! -f "$(MODEL_SOURCE)" ]; then \
		if [ -f "$(MODEL_OUTPUT)" ]; then \
			echo "FAILED: $(MODEL_OUTPUT) exists but its source $(MODEL_SOURCE) does not." >&2; \
			echo "  A generated artifact with no source is maintained by hand — restore the source" >&2; \
			echo "  or delete the generated file. This is #22 shape 14 in its worse direction." >&2; \
			exit 1; \
		fi; \
		echo "NOT CHECKED: neither $(MODEL_SOURCE) nor its generated .md exists, so there is nothing to render-check"; \
		exit 0; \
	fi; \
	"$(MODELITH)" render --check "$(MODEL_SOURCE)"

check-audit: check-python ## DSL topology audit of this repo's own example tree
	@$(RUN) skills/axb-gherkin-and-dsl/scripts/audit_feature_dsl_topology.py --root $(ROOT)/$(EXAMPLES)

check: check-paths check-tokens check-names check-refs check-params check-ui-plan check-model check-audit ## Run everything (default gate)

test: check-python ## Run the checkers' own test suites (every scripts/test_*.py, plus the audit's)
	@$(RUN) -m unittest discover -s $(SCRIPTS) -p 'test_*.py' -v
	@$(RUN) -m unittest discover -s skills/axb-gherkin-and-dsl/scripts -p 'test_*.py'

install-hooks: ## Install a stub into .git/hooks that runs the gate; survives branch switches
	@hooks_dir=$$(git rev-parse --git-path hooks); \
	dest=$$hooks_dir/pre-commit; \
	classify=$(SCRIPTS)/hooks/classify-hook; \
	stub=$(SCRIPTS)/hooks/pre-commit-stub; \
	state=$$(sh "$$classify" "$$dest"); \
	case "$$state" in \
		absent|legacy|managed|stale-managed) : ;; \
		foreign-symlink) \
			echo "refusing to overwrite a foreign symlink: $$dest -> $$(readlink "$$dest")" >&2; \
			echo "Move it aside first." >&2; exit 1 ;; \
		foreign-file) \
			echo "refusing to overwrite an existing hook: $$dest" >&2; \
			echo "Move it aside, or run 'git commit --no-verify' to skip the gate." >&2; exit 1 ;; \
	esac; \
	mkdir -p "$$hooks_dir"; \
	cp "$$stub" "$$dest.tmp" || { echo "could not copy the stub; leaving any existing hook untouched" >&2; rm -f "$$dest.tmp"; exit 1; }; \
	chmod +x "$$dest.tmp"; \
	mv -f "$$dest.tmp" "$$dest" || { echo "could not install the hook" >&2; rm -f "$$dest.tmp"; exit 1; }; \
	if [ "$$state" = "legacy" ]; then echo "replaced the pre-stub symlink at $$dest"; fi; \
	echo "installed: $$dest (a stub; the gate script is read from the current branch)"; \
	echo "Bypass with: git commit --no-verify"

uninstall-hooks: ## Remove the stub, leaving any other hooks untouched
	@hooks_dir=$$(git rev-parse --git-path hooks); \
	dest=$$hooks_dir/pre-commit; \
	classify=$(SCRIPTS)/hooks/classify-hook; \
	state=$$(sh "$$classify" "$$dest"); \
	case "$$state" in \
		absent) echo "nothing to remove: no hook at $$dest" ;; \
		legacy|managed|stale-managed) \
			rm -f "$$dest"; \
			if [ "$$state" = "legacy" ]; then echo "removed: $$dest (pre-stub symlink)"; else echo "removed: $$dest"; fi ;; \
		foreign-symlink) \
			echo "left alone: $$dest points at $$(readlink "$$dest")" >&2 ;; \
		foreign-file) \
			echo "left alone: $$dest is not this repository's hook" >&2 ;; \
	esac
