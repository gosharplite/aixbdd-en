---
name: axb-implement
description: Based on the plan package's `tasks.md`, execute unlocked tasks with don't stop until deliver / One-Shot. Exactly 1 task or a Parallel Hint batch per round; verify, immediately write back `[X]`, then continue until delivery. Steps must not be skipped.
disable-model-invocation: true
---

# Implement

`axb-implement` treats `tasks.md` as the single execution control plane, but the execution context must include the plan package and `truth-delta.md`. It is responsible for delivering the plan, not for redefining truth; if truth and tasks are found to be clearly contradictory, stop the affected tasks and report that upstream fixes are needed.

## Operating Principles

- By default it is don't stop until deliver / One-Shot: work from the first unlocked task until the target plan is fully `[X]`. The user does not need to say this again.
- A One-Shot round's task set is exactly 1 unlocked task; with a `Parallel Hint` it becomes the `[P]` batch listed by the Hint (scheduled per `rules/parallel-hint-subagent-and-same-file-scheduling-criteria.md`). One-Shot does not mean spreading out the subsequent sequential tasks at once.
- After finishing a task set, verify it, immediately write back the `[X]` in `tasks.md`, then recompute the next one. No next task set may start before the write-back.
- Strictly enforce that steps must not be skipped. `don't stop until deliver` is not permission to skip steps.
- The Feature phase is still sequential. Only `[BDD-GREEN]` and `[BDD-REFACTOR]` delegate to `/axb-bdd`, taking that phase's `Test Scope` as the scope.
- Phase 3's `[BDD-ALIGN]`, `[BDD-REMOVE]`, `[BDD-RED]` do NOT delegate to `/axb-bdd`; a subagent reads the `StepDef Implementation Semantics` of the corresponding `dsl.md` row and writes the test layer.
- `[WITNESS]` tasks do NOT delegate to `/axb-bdd` (they hit unit/fault-injection tests directly, executed per their Test Scope and Falsifier; the DoD requires passing the discriminating mutation, clear failure attribution, and revert-and-re-green).
- Before Phase 3 review passes, Feature Green must not be entered.
- After all tasks are `[X]`, ask whether to git commit; do not commit automatically.

# SOP

## Phase 1 -- Align the plan and start One-Shot

1. READ Read the user requirements, the target plan package, `tasks.md`, `truth-delta.md`, and the current task completion states; confirm the specified scope (if any) and the One-Shot starting point.
2. READ Read `rules/task-selection-and-continuous-resume-criteria.md` to confirm the selection of unlocked tasks, One-Shot, and stop conditions.
3. READ Read `rules/truth-delta-test-alignment-and-bdd-delegation-criteria.md` to confirm the ADD / MODIFY / DELETE execution strategies and which markers delegate to `/axb-bdd`.
4. THINK Based on the tasks and criteria read, converge the One-Shot starting point, whether a `Parallel Hint` is hit, and the owning phase; by default work through to delivery, not stopping at the first one.

## Phase 2 -- Reinforce repo hygiene and execution prerequisites

1. READ Read `rules/repo-hygiene-and-ignore-reinforcement-criteria.md` to confirm which ignore surfaces to check this time and which may only be appended to, not overwritten.
2. THINK Based on the current repo, toolchain, plan package, truth-delta, and `specs/truth/techstack.md`, converge the minimal hygiene reinforcement that must be done this round.
3. WRITE Only create or append ignore settings when actually relevant and a real gap exists; avoid expanding into unrelated toolchains.

## Phase 3 -- Converge this round's task set (steps must not be skipped)

1. READ Read `rules/strict-no-step-skipping-criteria.md` and `rules/parallel-execution-and-file-conflict-criteria.md` to confirm this round's task set boundary.
2. READ If the `tasks.md` current phase contains a `Parallel Hint`, read `rules/parallel-hint-subagent-and-same-file-scheduling-criteria.md`.
3. THINK Converge this round's task set: with a `Parallel Hint` it is the `[P]` batch listed by the Hint; otherwise exactly 1 unlocked task.
4. THINK Converge the execution mode: Setup and Foundational are implemented directly, stopping at that rule's "only-do / not-do"; Phase 3's ALIGN / REMOVE / RED go through the subagent test layer; review goes through the review loop; `[BDD-GREEN]` / `[BDD-REFACTOR]` delegate to `/axb-bdd`; `[CODE-REMOVE]`, `[REGRESSION]` are implemented or verified directly; `[WITNESS]` executes the unit/fault-injection test layer, proving the discriminating mutation can turn red with clear attribution and everything turns green after revert; or execute the demotion removal of prose.

## Phase 4 -- Load precise references and execute

1. READ Read `rules/technical-reference-loading-and-minimal-context-criteria.md` to confirm the loading boundaries of `Read`, phase-level `Shared Must Read`, `Extra Read`, truth-delta rows, and adjacent tasks / artifacts.
2. READ Load, per the current task set's precise references, the necessary plan artifacts, truth features, the same-module DSL, the actually-listed interface root shared DSL rows, and existing automated-test touchpoints; do not scan or preload other modules' DSL.
3. READ If this round modifies artifacts governed by the constitution or conflicts with truth specs, read `.agents/constitution/CONSTITUTION.md`, `.agents/constitution/shared.md`, and the corresponding constitution file.
4. READ Read `rules/autonomous-decision-and-blocker-handling-criteria.md` to confirm the decision priority order for spec gaps, local contradictions, or environment blockers.
5. DELEGATE If this round is a `Parallel Hint` batch, schedule subagents per `rules/parallel-hint-subagent-and-same-file-scheduling-criteria.md` (the prompt points to the corresponding task in that plan's `tasks.md`); after all return, run the review loop.
6. DELEGATE If this round is `[BDD-GREEN]` or `[BDD-REFACTOR]`, call `/axb-bdd` with a single requested step, passing `Test Scope`, action, truth rows, the module DSL, and the actually-used shared DSL rows.
7. WRITE If the task carries none of the above markers, complete this round's required code, config, documentation, or test changes per the task marker; do not step outside this round's task and phase boundary.

## Phase 5 -- Verify, write back, continue One-Shot until delivery

1. READ Read `rules/definition-of-done-verification-and-writeback-criteria.md` to confirm the task completion and write-back conditions.
2. THINK Converge the most direct verification method per the task type.
3. WRITE After this round's task set implementation and verification are both complete, immediately rewrite the corresponding task to `[X]`, keeping other task states unchanged.
4. THINK Recompute whether an unlocked, in-scope, unfinished task still exists; if so, return to Phase 3. This is the One-Shot default, not optional.
5. WRITE If the target plan package's tasks are all `[X]` and verification has passed, report to the user that this plan has been delivered, and ask whether to git commit deliver; do not commit before obtaining the user's consent.
