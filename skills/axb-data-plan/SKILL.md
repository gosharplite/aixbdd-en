---
name: axb-data-plan
description: Truth owner skill. Based on the plan package, the axb-system-analysis handoff, and existing data truth, update `specs/truth/data/**`, support ADD / MODIFY / DELETE / NOOP data semantic units, and delegate `/axb-truth-delta` to record this round's data truth changes.
disable-model-invocation: true
---

# Data Plan

`axb-data-plan` is the truth owner of `specs/truth/data/**`. It maintains the system's single current data model truth, whether the underlying layer is a persistent database or an in-memory state model.

# SOP

## Phase 1 -- Align data truth and plan handoff

1. READ Read the user requirements, caller handoff, the plan package's `spec.md`, `research.md`, `plan.md`, `truth-delta.md`, `specs/truth/techstack.md`, existing `specs/truth/data/**`, and the specified data interface name.
2. READ Read `templates/data-model.dbml`, `templates/data-model.example.dbml`, and `templates/data-model.example.dbdiagram` to confirm the fixed structure, annotation density, and finished appearance of the data model artifact.
3. READ Read `.agents/constitution/CONSTITUTION.md`, `.agents/constitution/shared.md`, and `.agents/constitution/skills/axb-data-plan/data-model.md`.

## Phase 2 -- Inventory data ADD / MODIFY / DELETE

1. THINK Based on the requirements, handoff, existing DBML, and truth-delta, organize the tables, enums, refs, fields, indexes, life cycles, and storage responsibilities to add, modify, delete, or keep unchanged this round.
2. DELEGATE If high-impact MODIFY / DELETE changes existing data life cycles, unique keys, relation directions, public projections, or the storage model, and no explicit user decision exists yet, call `/axb-clarify`; stop before convergence.

## Phase 3 -- Update data truth

1. WRITE Directly update `specs/truth/data/**` so that data truth becomes the current complete system data model, leaving no scattered references like "reuse a plan's model".
2. READ Review whether data truth conforms to the loaded constitution, the specified data requirements, life cycles, and the existing API/feature truth; if not, fix immediately.
3. THINK Organize the data truth changes into semantic-unit-level ADD / MODIFY / DELETE / NOOP rows.

## Phase 4 -- Update truth-delta and deliver

1. DELEGATE Call `/axb-truth-delta`, passing the plan package, truth root, owner `/axb-data-plan`, and this round's data truth change rows.
2. WRITE Report to the user the updated data truth paths, main entity and life cycle changes, whether `/axb-clarify` was entered, the truth-delta update result, and whether it can be handed to downstream implementation or `/axb-tasks`.
