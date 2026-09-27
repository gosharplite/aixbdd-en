---
name: axb-specify
description: Turn natural-language functional requirements into a new plan package. Each execution creates the next `specs/plans/NNN-<slug>/`, produces `spec.md`, `checklists/requirements.md`, and initializes `truth-delta.md`; it must not rewrite old plan packages, nor write into `specs/truth/**`.
disable-model-invocation: true
---

# Specify

`axb-specify` is the plan starting point of each iteration. It only describes "what to change this time" and does not directly modify system truth. Even if this requirement modifies or deletes existing behavior, a new plan package is created, keeping old plans as history and letting `specs/truth/**` represent the current system truth.

# SOP

## Phase 1 -- Create a new plan package

1. READ Read the user requirements, caller requests, the existing numbering under `specs/plans/`, and the high-level status of `specs/truth/**`; confirm this feature's topic, scope, language requirements, and explicit constraints.
2. READ Read `templates/spec.template.md`, `templates/spec.example.md`, `templates/requirements-checklist.md`, and `templates/requirements-checklist.example.md` to confirm the fixed structure of the spec and checklist.
3. READ Read `rules/feature-directory-naming-and-output-placement-criteria.md` to confirm the naming and output placement of the next `NNN-<slug>` plan package.
4. READ Read `.agents/constitution/CONSTITUTION.md`, `.agents/constitution/shared.md`, `.agents/constitution/skills/axb-specify/spec.md`, and `.agents/constitution/skills/axb-specify/requirements-checklist.md`, treating their rules as constraints above the local artifact standards.
5. WRITE Create `specs/plans/NNN-<slug>/` and `checklists/`, and initialize the `truth-delta.md` skeleton; this phase does not create or modify `specs/truth/**`.

## Phase 2 -- Converge requirement gaps and the clarify strategy

1. THINK From the requirements and existing truth, organize the main user goals, core flows, explicit constraints, quality expectations, possible ADD / MODIFY / DELETE intents, and identifiable scope boundaries.
2. READ If you need to determine which gaps must be escalated to clarify, read `rules/clarify-escalation-threshold-and-question-budget-criteria.md`.
3. DELEGATE If gaps would change user story splitting, requirement attribution, main flows, formal acceptance criteria, or would high-impact modify/delete existing truth behavior, call `/axb-clarify` to interview the user first; stop before convergence, and do not assume answers on your own.

## Phase 3 -- Rebuild the spec's semantic skeleton

1. READ When stories need splitting or requirements need attribution, read `rules/user-story-splitting-and-priority-criteria.md` and `rules/fr-nfr-attribution-to-user-story-and-global-requirements-criteria.md`.
2. THINK Per the loaded rules, converge independently verifiable User Stories, Priority, acceptance scenarios, story-specific FR / NFR, global requirements, edge cases, key entities, success criteria, and assumptions.
3. THINK For requirements involving existing truth, explicitly mark whether they are expected to add, modify, or delete existing system behavior — but do not write truth in this skill.

## Phase 4 -- Produce plan artifacts and self-check

1. WRITE Write the spec to `specs/plans/NNN-<slug>/spec.md` and the checklist to `specs/plans/NNN-<slug>/checklists/requirements.md`.
2. READ Read `rules/spec-completeness-and-consistency-self-check-criteria.md` to check that User Stories, FR / NFR, acceptance scenarios, edge cases (EC-nnn), success criteria, each normative item's verification-intent annotation, assumptions, and remaining clarify gaps are consistent; fix any deviations immediately.

## Phase 5 -- Deliver and hand off follow-ups

1. WRITE Report to the user the plan package, spec, checklist, truth-delta paths, whether `/axb-clarify` was entered this time, the remaining `NEEDS CLARIFICATION` or assumptions, and whether this plan can proceed to `/axb-spec-by-example` or `/axb-technical-research`.
