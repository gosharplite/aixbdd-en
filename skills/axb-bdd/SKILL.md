---
name: axb-bdd
description: Takes over the interface feature files and dsl.md already delivered by /axb-dsl-refine, and advances BDD/TDD implementation via three entry points — red, green, refactor — within a user-specified single interface feature file or a clearly identified block of it. It is not responsible for producing feature files; if a spec gap affects acceptance intent or DSL boundaries, it must stop and hand back upstream.
disable-model-invocation: true
---

# BDD

Convert the interface `feature files` and `dsl.md` already delivered by `/axb-dsl-refine` into executable step definitions, test implementations, and product code changes:

- The `feature file` and `dsl.md` are the single upstream source of truth for this skill.
- `/axb-bdd` only advances work within a user-specified single interface `feature file` or a clearly identified block of it.
- `/axb-bdd` has three entry points: `red`, `green`, and `refactor`; only one entry point is used per invocation.
- A single invocation may sequentially advance multiple slices within the specified scope, but only one slice is handled at a time.
- If `/axb-bdd` is delegated by a single task of `/axb-implement`, it must obey that task's single `slice`, single `requested step`, and current scope, and must not swallow subsequent tasks along the way.
- If a high-impact gap is found in the `feature file` or `dsl.md`, work must stop and be handed back to `/axb-dsl-refine` or the user-specified upstream process.

# SOP

## Phase 1 -- Align upstream deliverables, test entry, and this round's scope

1. READ Read the user requirements, the specified interface `feature file` or its clearly identified block, the same module's `dsl.md`, the interface root shared `dsl.md` rows actually used by that feature, the relevant test code and product code; confirm whether this round's entry is `red`, `green`, or `refactor`, and the scope the user has delimited; if delegated by `/axb-implement`, additionally confirm that the current task authorizes only a single `slice` and a single `requested step`.
2. READ If you need to confirm how modular truth is carried over or the project's existing symlink policy, read `rules/modular-truth-on-demand-symlink-criteria.md`.
3. READ If you need to confirm which upstream deliverables this skill can accept, when work must stop, or which gaps should be handed back upstream, read `rules/upstream-delivery-handoff-criteria.md`.
4. THINK If this round's scope, loaded DSL, interface boundaries, or upstream deliverables still have high-impact gaps, first converge the minimal necessary clarification points.
5. DELEGATE If high-impact gaps remain that would change slice boundaries, acceptance results, or DSL handover, call `/axb-clarify` and stop the affected scope; if the gap comes from the `feature file` or any layer of the DSL itself, hand back instead to `/axb-dsl-refine` or the user-specified upstream process — do not write spec yourself.
6. READ If you need to confirm focused reruns, the Given state-setup entry, or whether existing helpers / fixtures / abstractions can be reused, read `rules/test-entry-and-abstraction-inventory-criteria.md`.
7. THINK Based on the information and rules loaded this round, converge the scope that can be advanced this round, the narrowest test entry, and candidate slices.

## Phase 2 -- Start the specified entry and select the advancement order

1. THINK If you need to determine which slice within the specified scope to advance first, when to continue to the next slice, how Scenario Outline should maintain verifiable granularity, or when the current slice counts as done, first read `rules/slice-selection-and-ordering-criteria.md`, then select the next advanceable slice according to the user-specified entry and this round's scope.
2. READ If this round's entry is `red`, read `rules/red-failure-signal-criteria.md`.
3. READ If this round's entry is `green`, read `rules/green-minimal-fix-criteria.md`.
4. READ If this round's entry is `refactor`, read `rules/refactor-green-protection-criteria.md`.
5. THINK Based on the loaded rules, converge the order of slices to advance one by one under this entry, the stop conditions, and the expected test or implementation touchpoints.

## Phase 3 -- Advance slices within the specified scope

1. WRITE Process the current slice according to the specified entry: `red` first establishes an effective failure signal, `green` only adds the minimum code needed for the current failure, `refactor` only tidies existing structure under green-light protection.
2. DELEGATE Run the corresponding focused tests or the minimal representative test set, observe the failure or pass signals, and keep fixing the current slice until the entry's completion conditions are met.
3. THINK If after the current slice is done there is still a next slice within this round's scope that can be advanced under the same entry, and no stop condition has been triggered, return to step 1 of this phase; if upstream spec needs changing, the work would leave the specified scope, or focused feedback is lost, stop this phase and organize the blocking reasons.

## Phase 4 -- Report results and next steps

1. WRITE Report to the user the slices completed or blocked this round, the test or product code touchpoints, test results, any gaps needing handoff upstream, and a recommendation on whether the next round should continue from the `red`, `green`, or `refactor` entry.
