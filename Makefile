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

.PHONY: help check check-paths check-tokens check-refs check-params check-audit check-python test \
        install-hooks uninstall-hooks

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
	@$(RUN) $(CHECKER) --only paths --quiet-candidates

check-tokens: check-python ## Invariant 4: fixed-token registry vs definitions and naming surfaces
	@$(RUN) $(CHECKER) --only tokens --quiet-candidates

check-refs: check-python ## Invariants 5-6: candidate report for normative refs and asserted gates
	@$(RUN) $(CHECKER) --only refs

check-params: check-python ## STANDARDS §4.3: every Default Params cell conforms
	@$(RUN) $(SCRIPTS)/check_dsl_default_params.py

check-audit: check-python ## DSL topology audit of this repo's own example tree
	@$(RUN) skills/axb-gherkin-and-dsl/scripts/audit_feature_dsl_topology.py --root $(EXAMPLES)

check: check-paths check-tokens check-refs check-params check-audit ## Run everything (default gate)

test: check-python ## Run the checkers' own test suites
	@$(RUN) -m unittest discover -s $(SCRIPTS) -p 'test_*.py' -v
	@$(RUN) -m unittest discover -s skills/axb-gherkin-and-dsl/scripts -p 'test_*.py'

install-hooks: ## Point git at the tracked hooks, so `make check` runs before every commit
	@git config core.hooksPath $(SCRIPTS)/hooks
	@echo "core.hooksPath = $(SCRIPTS)/hooks"
	@echo "The invariant gate now runs before every commit. Bypass with: git commit --no-verify"

uninstall-hooks: ## Stop running the gate on commit
	@git config --unset core.hooksPath || true
	@echo "core.hooksPath unset; commits are no longer gated.
