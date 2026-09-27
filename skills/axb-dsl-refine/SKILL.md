---
name: axb-dsl-refine
description: Truth owner skill. Takes over the plan package's acceptance Gherkin and axb-system-analysis outputs, splits business Journeys into interface-level executable feature files and DSL, and updates `specs/truth/features/backend/**`, `specs/truth/features/frontend/**`, `specs/truth/features/cli/**`. When done, delegate `/axb-truth-delta` to record the feature/dsl truth changes.
disable-model-invocation: true
---

# DSL Refine

`axb-dsl-refine` is the truth owner of interface features and DSL. Acceptance Gherkin stays in the plan package; the decomposed executable front/back-end interface features/dsl are written into `specs/truth/features/**`, representing the current system's test spec truth.

# SOP

## Phase 1 -- Align acceptance, system interfaces, and feature truth

1. READ Read the user requirements, the target plan package's `features/acceptance/**`, `plan.md`, `truth-delta.md`, `specs/truth/techstack.md`, the relevant UI plan, and — for the affected interfaces — the existing functional modules, features, module DSL, and interface root shared DSL.
2. THINK Identify from `plan.md`, truth-delta, and existing feature truth which of the frontend, backend, CLI, or other system interfaces are involved this round, and whether each interface's existing feature/dsl needs ADD / MODIFY / DELETE.
3. WRITE Report to the user the interfaces identified this round and the planned scope of truth feature files and DSL to add / modify / delete.

## Phase 2 -- Dispatch acceptance rules and handle high-impact changes

1. READ Read `rules/interface-gherkin-atomization-and-single-act-criteria.md` to confirm the interface Gherkin atomization and single-Act boundaries.
2. THINK Inventory the acceptance Rules, Examples, key Given / When / Then, and `# [need clarification]` one by one, dispatch them to the relevant interfaces, and confirm every acceptance rule is carried by at least one interface truth.
3. DELEGATE If high-impact MODIFY / DELETE rewrites existing interface behavior, removes existing acceptance, or weakens the DSL verification contract, and no explicit user decision exists yet, call `/axb-clarify`; stop before convergence.

## Phase 3 -- Update interface feature truth

1. READ Read `../axb-gherkin-and-dsl/SKILL.md` and `../axb-gherkin-and-dsl/STANDARDS.md` to take over their mounted Gherkin, DSL, and unique-ownership criteria.
2. WRITE Create, modify, move, or delete the affected interface features and DSL rows at their unique authoritative locations per the loaded rules.
3. DELEGATE Call `/axb-gherkin-and-dsl` to check the affected interfaces, obtaining topology mechanical audit, DSL unique ownership, acceptance coverage, and Gherkin structure results; fix immediately if non-conforming.
4. THINK Organize the feature/dsl truth changes into semantic-unit-level ADD / MODIFY / DELETE / NOOP rows.

## Phase 4 -- Update truth-delta and deliver

1. DELEGATE Call `/axb-truth-delta`, passing the plan package, truth root, owner `/axb-dsl-refine`, the affected modules, features, module DSL, relevant shared DSL rows, and this round's truth change rows; when a DSL row only moves its authoritative location without semantic change, explicitly state the old location, new location, and "semantics unchanged".
2. WRITE Report to the user the updated interface feature/dsl truth, the truth-delta update results, clarified decisions, remaining blocking gaps, and whether it can be handed to `/axb-tasks` or `/axb-bdd`.
