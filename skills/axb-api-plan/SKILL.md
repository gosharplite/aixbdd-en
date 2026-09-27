---
name: axb-api-plan
description: Truth owner skill. Based on the plan package, the axb-system-analysis handoff, and existing API truth, update `specs/truth/contracts/**`, support ADD / MODIFY / DELETE / NOOP API semantic units, and delegate `/axb-truth-delta` to record this round's API truth changes.
disable-model-invocation: true
---

# API Plan

`axb-api-plan` is the truth owner of `specs/truth/contracts/**`. It no longer produces package-local contracts; it directly maintains the system's single current API truth.

# SOP

## Phase 1 -- Align API truth and plan handoff

1. READ Read the user requirements, caller handoff, the plan package's `spec.md`, `research.md`, `plan.md`, `truth-delta.md`, `specs/truth/techstack.md`, existing `specs/truth/contracts/**`, and the specified backend / API interface name.
2. READ Read `templates/openapi.yaml` and `templates/openapi.example.yaml` to confirm the contract artifact's fixed structure and finished look.
3. READ Read `.agents/constitution/CONSTITUTION.md`, `.agents/constitution/shared.md`, and `.agents/constitution/skills/axb-api-plan/openapi.md`.

## Phase 2 -- Inventory API ADD / MODIFY / DELETE

1. THINK Based on the requirements, handoff, existing OpenAPI, and truth-delta, organize the operations, schemas, fields, responses, error codes, and state-transition semantics to add, modify, delete, or keep unchanged this round.
2. DELEGATE If high-impact MODIFY / DELETE changes existing external contracts, request/response shapes, error models, or state transitions, and no explicit user decision exists yet, call `/axb-clarify`; stop before convergence.

## Phase 3 -- Update API truth

1. WRITE Directly update `specs/truth/contracts/**` so that API truth becomes the current complete system contract, leaving no scattered references like "still defer to a plan's contract".
2. READ Review whether the contract conforms to the loaded constitution, the specified interface requirements, and compatibility with existing truth; if not, fix immediately.
3. THINK Organize the API truth changes into semantic-unit-level ADD / MODIFY / DELETE / NOOP rows.

## Phase 4 -- Update truth-delta and deliver

1. DELEGATE Call `/axb-truth-delta`, passing the plan package, truth root, owner `/axb-api-plan`, and this round's API truth change rows.
2. WRITE Report to the user the updated API truth paths, main operation and schema changes, whether `/axb-clarify` was entered, the truth-delta update result, and whether it can be handed to downstream implementation or `/axb-tasks`.
