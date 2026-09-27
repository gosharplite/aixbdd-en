---
name: axb-technical-research
description: Takes over the plan package's `spec.md`, produces the plan-side `research.md`, and acts as truth owner to update `specs/truth/techstack.md`. Every execution must inventory the techstack truth's ADD / MODIFY / DELETE / NOOP, then delegate `/axb-truth-delta` to update this plan's `truth-delta.md`.
disable-model-invocation: true
---

# Technical Research

`axb-technical-research` produces both the research process and the technical stack truth: `research.md` stays in the plan package, and `specs/truth/techstack.md` is the whole system's single current techstack truth.

# SOP

## Phase 1 -- Align plan and techstack truth

1. READ Read the user requirements, caller requests, the target plan package's `spec.md`, existing `research.md`, `truth-delta.md`, `specs/truth/techstack.md`, and the necessary codebase boundaries.
2. READ Read `templates/research.md`, `templates/research.example.md`, `templates/techstack.md`, and `templates/techstack.example.md` to confirm the responsibility boundaries of research and techstack.
3. READ Read `rules/research-output-placement-and-post-spec-continuation-criteria.md` to confirm `research.md` is written to the plan package and `techstack.md` to `specs/truth/techstack.md`.
4. READ Read `.agents/constitution/CONSTITUTION.md`, `.agents/constitution/shared.md`, `.agents/constitution/skills/axb-technical-research/research.md`, and `.agents/constitution/skills/axb-technical-research/techstack.md`.

## Phase 2 -- Converge research gaps and truth-change risks

1. READ Read `rules/aixbdd-mandatory-questions-and-initial-project-interface-clarification-criteria.md`; against `spec.md`, existing `techstack.md`, and the user's original words this round, mark the mandatory questions not yet decided.
2. DELEGATE If the BDD techstack, test strategy, or which ends the system has in an initial project is not yet decided, call `/axb-clarify`; stop before all are asked, do not enter Phase 3.
3. THINK Once the mandatory questions are decided, organize from `spec.md` and existing techstack truth the remaining core decisions to make, candidate options, known constraints, comparison dimensions, and success conditions.
4. READ If you need to judge whether the remaining gaps escalate to clarify, read `rules/clarify-escalation-threshold-and-research-question-budget-criteria.md`.
5. DELEGATE If the remaining gaps would change the decision set, candidate options, or technical boundaries, or high-impact modify/delete existing techstack truth, call `/axb-clarify`; stop before convergence.

## Phase 3 -- Produce research and update techstack truth

1. READ When the minimal required information of research and techstack needs confirmation, read `rules/research-artifact-minimal-required-information-criteria.md` and `rules/techstack-artifact-minimal-required-information-criteria.md`.
2. WRITE Write the decision-driven research content into `specs/plans/NNN-<slug>/research.md`.
3. WRITE Update `specs/truth/techstack.md` per existing truth and this round's decisions so it represents the system's complete current technical stack, keeping no scattered statements like "defer to plan 001/002".
4. THINK Organize the techstack truth changes into semantic-unit-level ADD / MODIFY / DELETE / NOOP rows.

## Phase 4 -- Update truth-delta and deliver

1. DELEGATE Call `/axb-truth-delta`, passing the plan package, truth root, owner `/axb-technical-research`, and this round's techstack truth change rows.
2. WRITE Report to the user `research.md`, `specs/truth/techstack.md`, `truth-delta.md`, the main technical decisions, and residual risks.
