---
name: axb-spec-by-example
description: Takes over the `spec.md` of a new plan package and converges the requirements into plan-side `features/acceptance/*.feature`. This skill writes only to `specs/plans/NNN-*/features/acceptance/**`, does not modify `specs/truth/**`, and does not update `truth-delta.md`.
disable-model-invocation: true
---

# Spec By Example

`axb-spec-by-example` produces PM-reviewable overall acceptance Gherkin. This layer still belongs to the plan: it describes the business journeys this iteration hopes to achieve, not the current system's interface truth.

# SOP

## Phase 1 -- Align the plan spec and output location

1. READ Read the user requirements, caller requests, the target plan package's `spec.md`, existing `features/acceptance/` content, and the necessary high-level status of `specs/truth/**`.
2. READ Read `rules/output-placement-and-acceptance-file-split-criteria.md` to confirm the acceptance feature files must be output to the current plan package.
3. WRITE If `specs/plans/NNN-<slug>/features/acceptance/` does not exist yet, create the directory.

## Phase 2 -- Converge acceptance journeys and requirement gaps

1. READ Read `rules/gherkin-acceptance-sentence-and-structure-criteria.md`, `templates/acceptance.feature`, `templates/acceptance.example.feature`, `templates/ecommerce-example/features/acceptance/order-placement-and-payment-timeout.feature`, `templates/ecommerce-example/features/acceptance/inventory-reservation-and-overselling-protection.feature`, `templates/ecommerce-example/features/acceptance/discount-stacking-and-mutual-exclusion.feature`, `templates/ecommerce-example/features/acceptance/threshold-gift-and-conditional-cancellation.feature`, and `templates/ecommerce-example/features/acceptance/shipping-zones-and-free-shipping.feature` to confirm the granularity, sentence patterns, Rule / Example boundaries, and finished look of acceptance Gherkin.
2. THINK Based on `spec.md`'s User Stories, Acceptance Criteria, edge cases, and global requirements, converge a small number of key Journey-type acceptance flows.
3. READ If the requirements have high-impact gaps that would change the Journey, rule ownership, acceptance results, or file splitting, read `rules/gap-marking-and-clarify-escalation-criteria.md`.
4. DELEGATE If high-impact gaps remain, call `/axb-clarify`; stop before convergence, and do not assume answers on your own.

## Phase 3 -- Produce acceptance Gherkin

1. WRITE Create or update feature files under the target plan package's `features/acceptance/`; keep the Gherkin in business language, do not split frontend / backend, and do not produce `dsl.md`.
2. WRITE Mark high-impact undecided items directly beside the corresponding feature's rule or step, with the fixed format `# [need clarification] ...`.
3. READ Review whether each feature is consistent with `spec.md`, directly readable by the PM, and not in obvious conflict with known truth; if not, fix immediately or escalate to clarify.

## Phase 4 -- Deliver and hand off follow-ups

1. WRITE Report to the user the acceptance feature files written, clarified decisions, remaining `# [need clarification]`, and whether it can proceed to `/axb-system-analysis` or `/axb-dsl-refine`.
