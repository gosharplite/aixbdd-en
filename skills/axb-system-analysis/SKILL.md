---
name: axb-system-analysis
description: Based on the plan package's `spec.md`, `research.md`, `truth-delta.md`, and `specs/truth/**`, inventory the system interfaces involved in this requirement and the analysis waves, produce the plan-side `plan.md`, and pass the plan package, truth root, and truth-delta path to `/axb-api-plan` and `/axb-data-plan`; the frontend does not redo `/axb-ui-plan` (UI is already produced by the PM) — it only reviews the implementability of the existing `ui/ui-plan.md` and prototypes; a CLI shipping an interactive TUI has its terminal UX surface handled like the frontend, likewise reviewed-only; a plain line-oriented CLI interface has no corresponding analysis planner and is instead handed to its contract owner `/axb-dsl-refine`.
disable-model-invocation: true
---

# System Analysis

`axb-system-analysis` is a planner orchestration skill. It does not modify truth itself, but must bring the differences between this round's plan and existing truth to the downstream owners, preventing API and data analysis from reasoning about different versions. Frontend UI planning is already done by the PM's `/axb-ui-plan`; this skill does not redo it and only reviews whether the existing UI artifacts are implementable within current technical boundaries; a CLI shipping an interactive TUI has its terminal UX surface handled like the frontend.

# SOP

## Phase 1 -- Align plan, truth, and the control plane

1. READ Read the user requirements, caller requests, the target plan package's `spec.md`, `research.md`, `truth-delta.md`, existing `plan.md`, `specs/truth/techstack.md`, and relevant `specs/truth/**`.
2. READ Read `templates/plan.md` and `templates/plan.example.md` to confirm the fixed structure and finished look of `plan.md`.
3. READ Read `.agents/constitution/CONSTITUTION.md`, `.agents/constitution/shared.md`, and `.agents/constitution/skills/axb-system-analysis/plan.md`.
4. WRITE If the plan package has no `plan.md` parent layer yet, create the necessary directories; this skill does not create or modify `specs/truth/**`.

## Phase 2 -- Converge the system interface inventory and clarify strategy

1. THINK From the requirement text, `spec.md`, `research.md`, `truth-delta.md`, and existing truth, organize this requirement's parts, external dependencies, data responsibilities, UI responsibilities, and technical endpoints.
2. READ When interface boundaries need judgment, read `rules/system-interface-inventory-and-endpoint-classification-criteria.md`.
3. DELEGATE If gaps would change the number of system interfaces, endpoint types, interface boundaries, truth owner responsibilities, or Wave splitting, call `/axb-clarify`; stop before convergence.

## Phase 3 -- Plan the analysis Waves and produce the plan

1. READ When ordering and parallel grouping need judgment, read `rules/wave-dependency-ordering-and-parallel-grouping-criteria.md`.
2. THINK Arrange Waves by interface dependency, truth-change risk, and parallelizability; confirm every interface has a clear downstream handover: API interfaces are taken over by `/axb-api-plan`, data interfaces by `/axb-data-plan`; frontend interfaces do NOT delegate to `/axb-ui-plan` and are instead taken over by reviewing the PM's existing `ui/**` artifacts; a CLI interface shipping an interactive TUI has its terminal UX surface (screens, keybindings, state transitions) already produced by the PM's `/axb-ui-plan` (terminal mode) and is handled like the frontend — review-only, no redo, no delegation; if it is a plain line-oriented CLI interface (no corresponding analysis planner, and the PM produced no ui-plan), hand off to its contract owner `/axb-dsl-refine` at delivery time.
3. WRITE Write the system interface inventory, Waves, analysis focus, and delegation rationale into `specs/plans/NNN-<slug>/plan.md`.

## Phase 4 -- Delegate planners and deliver

1. READ When planner correspondence needs judgment, read `rules/analysis-interface-delegation-and-planner-mapping-criteria.md`.
2. DELEGATE In Wave order, hand API interfaces to `/axb-api-plan` and data interfaces to `/axb-data-plan`; every handoff must include the plan package path, truth root, truth-delta path, interface name, and analysis focus. Frontend interfaces do NOT delegate to `/axb-ui-plan` (UI planning is already done by the PM): if the frontend is involved this time, only review the PM-delivered existing `ui/ui-plan.md` and prototypes, confirming implementability within current technical boundaries. A CLI interface shipping an interactive TUI is handled like the frontend, reviewing only its terminal-mode UI artifacts (`ui/ui-plan.md` and `ui/screens/*.txt`); a plain line-oriented CLI interface has no corresponding analysis planner and is not delegated in this phase — instead it is explicitly handed off at delivery to the next phase's contract owner `/axb-dsl-refine`.
3. WRITE Report to the user `plan.md`, the number of system interfaces, the number of Waves, which planners were delegated to (including the CLI TUI interface reviewed like the frontend, and the plain line-oriented CLI interface handed to `/axb-dsl-refine`), and whether it can proceed to `/axb-dsl-refine` or `/axb-tasks`.
