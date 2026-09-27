---
name: axb-truth-delta
description: Maintains the `truth-delta.md` inside each plan package, letting truth owner skills record this round's ADD / MODIFY / DELETE / NOOP semantic-unit changes to `specs/truth/**` in a shared format. Use when a truth owner skill has inspected or changed truth specs and must initialize, append, update, or validate the current plan package truth delta handoff.
disable-model-invocation: true
---

# Truth Delta

`axb-truth-delta` is the shared handoff skill of the truth owner skills. It does not decide how to change truth, nor does it write OpenAPI, DBML, features, or DSL for the owner; it is only responsible for writing confirmed truth changes in a fixed format into the current plan package's `truth-delta.md`, letting downstream skills continue reasoning.

# SOP

## Phase 1 -- Align the plan package and truth owner

1. READ Read the caller handoff, the current plan package path, truth root, truth owner name, the list of truth specs inspected or modified, and existing `truth-delta.md` content.
2. READ Read `rules/truth-change-classification-and-granularity-criteria.md` to confirm owner sections, action classification, semantic-unit granularity, and NOOP record rules.
3. READ If `truth-delta.md` does not exist yet, read `templates/truth-delta.md` and `templates/truth-delta.example.md` to confirm the initialization skeleton and finished look.
4. WRITE If `truth-delta.md` does not exist yet, create the file in the current plan package and fill in the plan package, truth root, and the four truth owner sections.

## Phase 2 -- Converge this round's truth change records

1. THINK Per the loaded rules, organize the caller-provided truth changes into semantic-unit rows; each row must contain `ADD`, `MODIFY`, `DELETE`, or `NOOP`, plus the truth spec, change summary, and reason.
2. THINK If the caller claims high-impact `MODIFY` or `DELETE` but the handoff does not state that `/axb-clarify` was completed or an explicit risk decision made, stop writing and require the caller to first supply the confirmation basis.
3. THINK If the same truth owner has no truth changes this round, converge one `NOOP` row, explicitly stating the inspected-but-unchanged truth scope and the reason.

## Phase 3 -- Update the owner section

1. WRITE Append or update this round's table rows in `truth-delta.md`'s corresponding owner section; if that section is still a placeholder or an existing `NOOP` has been superseded by actual changes, clean up first and then write.
2. READ Review whether `truth-delta.md` still keeps one table per truth owner, and whether all rows conform to the fixed fields, action values, and semantic-unit granularity; fix any deviations immediately.

## Phase 4 -- Deliver downstream handoff

1. WRITE Report to the caller the updated `truth-delta.md` path, owner section, ADD / MODIFY / DELETE / NOOP counts, and whether high-impact truth changes still need to return to `/axb-clarify`.
