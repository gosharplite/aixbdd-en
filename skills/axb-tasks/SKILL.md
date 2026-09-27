---
name: axb-tasks
description: Based on the plan package's `spec.md`, `plan.md`, `research.md`, `ui/**`, as well as `truth-delta.md` and `specs/truth/**`, produce a directly executable `tasks.md`. Write Setup and Foundational first; the test layer concentrates in Phase 3 `Test Alignment & Implementation`; Feature phases keep Green / Refactor or CODE-REMOVE / REGRESSION; unobservable claims are scheduled as Phase 4W `[WITNESS]` pins.
disable-model-invocation: true
---

# Tasks Skill

`axb-tasks` is the plan-side execution planner. It does not modify truth; it only converts this plan, truth-delta, and current truth into a `tasks.md` that `/axb-implement` can execute step by step. New technology this round goes into Setup first; then Foundational; the test layer aligns with the latest truth in one pass before any product code is written. Inventorying existing automated tests happens only when writing Phase 3 and must not be output as implement tasks.

# SOP

## Phase 1 -- Converge the plan package, truth-delta, and this round's DSL list

1. READ Read the user requirements, the target plan package's `spec.md`, `plan.md`, `research.md`, `ui/**`, `truth-delta.md`, and the affected modules' truth features, module DSL, the interface root shared DSL rows actually referenced by truth-delta, relevant contracts/data, and `specs/truth/techstack.md`.
2. READ Read `.agents/constitution/CONSTITUTION.md` and `.agents/constitution/shared.md`, treating their rules as constraints above the local artifact standards.
3. READ Read `rules/truth-delta-impact-inventory-and-task-type-criteria.md` to confirm how ADD / MODIFY / DELETE / NOOP split into Phase 3's test layer and Feature's product layer, and the boundaries of Setup, Foundational, and Test Alignment.
4. THINK Inventory all DSL sentences used by this round's Feature: including sentences changed in truth-delta, and sentences used by this round's Feature that have no stepdef yet. If there are `MODIFY` or `DELETE`, also inventory existing stepdefs, helpers, fixtures, and product branches — used only to write subsequent tasks, not output as an independent phase. If any sentence lacks a unique DSL definition, stop the affected scope and hand back to `/axb-dsl-refine`.

## Phase 2 -- Produce Setup and Foundational

1. THINK If this round adds new technology, create Phase 1 `Setup`: write clearly the package names, configuration, technical environment, and the final smoke-test; write no DSL semantics and no product behavior.
2. THINK If this round adds no new technology, omit Setup; do not stuff helpers, fixtures, or touchpoint skeletons into Setup.
3. THINK Create Phase 2 `Foundational`: only establish the implementation code, test-shared components, entry points, fixtures, helpers, and touchpoint skeletons for later work; each rule writes "only-do / not-do"; test touchpoint skeletons should prefer an independent-file design (Zero Shared Edits principle), eliminating same-file conflicts for Phase 3 parallel dispatch.
4. THINK Setup and Foundational must not sneak in Phase 3's test layer or Feature Green.

## Phase 3 -- Create Test Alignment & Implementation

1. READ Read `templates/tasks.md` and `templates/tasks.example.md` to confirm Phase 3's fixed sections: `DSL Reference`, `Markers`, `Shared Must Read`, `Boundary`, `Parallel Hint`.
2. THINK Mark each inventoried sentence with `[BDD-ALIGN]`, `[BDD-REMOVE]`, or `[BDD-RED]`; one `[P]` task per DSL sentence; touchpoints prefer independent files to avoid parallel write conflicts; the last task is the subagent review.
3. THINK Write the `DSL Reference` (each sentence's authoritative `dsl.md` and the method for reading `StepDef 實作語意`), `Markers`, the sentences to read this round, `Boundary`, and `Parallel Hint`.
4. THINK This phase must not schedule product code tasks.

## Phase 4 -- Create Feature phases and Witness pins

1. THINK For `ADD` truth interface feature files, create `[BDD-GREEN] -> [BDD-REFACTOR]` and declare `Test Scope`.
2. THINK For `MODIFY` truth interface feature files, create `[BDD-GREEN] -> [BDD-REFACTOR]` and declare `Test Scope`.
3. THINK For `DELETE` truth interface feature files, Rules, Examples, or DSL sentences, create `[CODE-REMOVE] -> [REGRESSION]` and declare `Test Scope`.
4. THINK Fill in `Shared Must Read`, `Boundary`, and `Test Scope` for each Feature phase; omit the root DSL reference when no interface root shared DSL rows are used. Truth references must use `specs/truth/**` paths.
5. THINK If acceptance scenarios cannot be uniquely carried by existing truth features, the same-module DSL, and relevant shared DSL rows, stop the affected scope and hand back to `/axb-dsl-refine`.
6. THINK Inventory `spec.md`'s normative items and truth-surface text; schedule atomic effect claims not externally observable via Gherkin as Phase 4W `[WITNESS]` pins; mark `Dependencies: T###`, `Test Scope`, and `Falsifier`. If a witness cannot be established, per the anti-washing clause require the human decision maker's approval on the project decision surface, or thoroughly demote and remove from truth surfaces.

## Phase 5 -- Output and verify tasks.md

1. WRITE Output `specs/plans/NNN-<slug>/tasks.md` following the template skeleton.
2. READ Per `rules/pre-delivery-coverage-check-and-orphan-artifact-inventory-criteria.md`, run the full coverage scan (Pre-Delivery Orphan Coverage Sweep) and the Claim→Witness Coverage Sweep: confirm `truth-delta.md`'s non-NOOP items, `research.md`'s decided Decisions, and `specs/truth/techstack.md`'s changed sections this round all have task coverage; and output the `Claim→Witness Ledger`, confirming all of this round's normative items and truth-surface claims are bound to `[BDD-GREEN]`, `[WITNESS]`, or a legitimate `accepted-unwitnessed` record; anything non-conforming blocks delivery.
3. READ Re-check the format: tasks are all `- [ ] T###`, truth-delta is included in Core Inputs, there is no Impact Audit phase, Setup writes package names and smoke-test when new technology is added, Foundational has "only-do / not-do" per rule, Phase 3 concentrates ALIGN / REMOVE / RED, Feature phases contain no `[BDD-RED]` / `[BDD-ALIGN]` / `[BDD-REMOVE]`, every Feature phase has `Test Scope`, unobservable claims are annotated `[WITNESS]` with `Dependencies` and `Falsifier`, the end has the `Claim→Witness Ledger`, and truth paths all point to `specs/truth/**`; fix any deviations immediately.
