---
name: axb-truth-delta
description: Maintains the `truth-delta.md` inside each plan package, letting truth owner skills record this round's ADD / MODIFY / DELETE / NOOP semantic-unit changes to `specs/truth/**` in a shared format. Use when a truth owner skill has inspected or changed truth specs and must initialize, append, update, or validate the current plan package truth delta handoff, or when `/axb-specify` creates a new plan package and needs its `truth-delta.md` scaffold initialized.
disable-model-invocation: true
---

# Truth Delta

`axb-truth-delta` is the shared handoff skill of the truth owner skills. It does not decide how to change truth, nor does it write OpenAPI, DBML, features, or DSL for the owner; it is only responsible for writing confirmed truth changes in a fixed format into the current plan package's `truth-delta.md`, letting downstream skills continue reasoning.

# SOP

This skill has two modes. Decide which one applies before doing anything else, because they take
different inputs and have different exit points.

- **Initialization mode** — the caller is `/axb-specify` creating a new plan package, and no truth
  owner has acted yet. Inputs: plan package path and truth root only. You create the scaffold and
  stop; Phases 2–4 do not apply.
- **Owner mode** — the caller is a truth owner skill (`/axb-technical-research`, `/axb-api-plan`,
  `/axb-data-plan`, `/axb-dsl-refine`) that has inspected or changed truth. Inputs: owner name and
  the truth specs it inspected or modified, in addition to the plan package and truth root. All
  four phases apply.

## Phase 1 -- Align the plan package and truth owner

1. THINK Decide the mode first. If the caller is `/axb-specify` at plan creation, this is
   **initialization mode**: go to step 2, then skip Phases 2–4 and finish at step 5. If the caller is
   a truth owner skill, this is **owner mode**: continue through all four phases.
2. READ Read the caller handoff, the current plan package path, the truth root, and existing
   `truth-delta.md` content; in owner mode also read the truth owner name and the list of truth specs
   inspected or modified. Initialization mode has no owner name and no inspected specs — do not stop
   for them, and do not infer them.
3. READ Read `rules/truth-change-classification-and-granularity-criteria.md` to confirm owner
   sections, action classification, semantic-unit granularity, and NOOP record rules.
4. READ If `truth-delta.md` does not exist yet, read `templates/truth-delta.md` and
   `templates/truth-delta.example.md` to confirm the initialization skeleton and finished look.
5. WRITE If `truth-delta.md` does not exist yet, create the file in the current plan package and fill
   in the plan package and truth root.
   - **Initialization mode:** also write the four truth owner section headings exactly as
     `templates/truth-delta.md` lays them out, leaving each table's rows as placeholders. Write no
     change rows and no `NOOP` rows — no owner has run, so there is nothing to record. Then report to
     the caller the `truth-delta.md` path and that it is initialized with placeholders, and stop.
   - **Owner mode:** continue to Phase 2 to add this round's rows to the caller's section.

## Phase 2 -- Converge this round's truth change records

> Owner mode only.

1. THINK Per the loaded rules, organize the caller-provided truth changes into semantic-unit rows; each row must contain `ADD`, `MODIFY`, `DELETE`, or `NOOP`, plus the truth spec, change summary, and reason.
2. THINK If the caller claims high-impact `MODIFY` or `DELETE` but the handoff does not state that `/axb-clarify` was completed or an explicit risk decision made, stop writing and require the caller to first supply the confirmation basis.
3. THINK If the same truth owner has no truth changes this round, converge one `NOOP` row, explicitly stating the inspected-but-unchanged truth scope and the reason.

## Phase 3 -- Update the owner section

> Owner mode only.

1. WRITE Append or update this round's table rows in `truth-delta.md`'s corresponding owner section; if that section is still a placeholder or an existing `NOOP` has been superseded by actual changes, clean up first and then write.
2. READ Review whether `truth-delta.md` still keeps one table per truth owner, and whether all rows conform to the fixed fields, action values, and semantic-unit granularity; fix any deviations immediately.

## Phase 4 -- Deliver downstream handoff

> Owner mode only.

1. WRITE Report to the caller the updated `truth-delta.md` path, owner section, ADD / MODIFY / DELETE / NOOP counts, and whether high-impact truth changes still need to return to `/axb-clarify`.

