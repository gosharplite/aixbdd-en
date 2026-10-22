---
name: axb-truth-delta
description: Maintains the `truth-delta.md` inside each plan package, letting truth owner skills record this round's ADD / MODIFY / DELETE / NOOP semantic-unit changes to `specs/truth/**` in a shared format. Use when a truth owner skill has inspected or changed truth specs and must initialize, append, update, or validate the current plan package truth delta handoff, or when `/axb-specify` creates a new plan package and needs its `truth-delta.md` scaffold initialized, or when `/axb-system-analysis` skips a planner by decision and must record that as a `NOOP` row for the skipped owner.
disable-model-invocation: true
---

# Truth Delta

`axb-truth-delta` is the shared handoff skill of the truth owner skills. It does not decide how to change truth, nor does it write OpenAPI, DBML, features, or DSL for the owner; it is only responsible for writing confirmed truth changes in a fixed format into the current plan package's `truth-delta.md`, letting downstream skills continue reasoning.

# SOP

This skill has three modes. Decide which one applies before doing anything else, because they take
different inputs and have different exit points.

- **Initialization mode** — the caller is `/axb-specify` creating a new plan package, and no truth
  owner has acted yet. Inputs: plan package path and truth root only. You create the scaffold and
  stop; Phases 2–4 do not apply.
- **Skip-record mode** — the caller is `/axb-system-analysis`, reporting one or more planners it
  deliberately skipped because no work of that kind exists this round (e.g. a plain line-oriented CLI
  has no API or data surface, so `/axb-api-plan` and `/axb-data-plan` are both skipped). Inputs: plan
  package, truth root, the **skipped** owners' names, and the analysis decision that skipped them —
  but no inspected specs, because nothing was inspected. You write one `NOOP` row per skipped owner,
  into each owner's own section. All four phases apply, as in owner mode.
- **Owner mode** — the caller is a truth owner skill (`/axb-technical-research`, `/axb-api-plan`,
  `/axb-data-plan`, `/axb-dsl-refine`) that has inspected or changed truth. Inputs: owner name and
  the truth specs it inspected or modified, in addition to the plan package and truth root. All
  four phases apply.

Skip-record mode is not a variant of owner mode: in owner mode the caller *is* the owner and has
inspected its scope, whereas here the caller decided the owner would not run. That is why the row it
writes must say "not applicable, by analysis decision" rather than "inspected, nothing needed"
(`rules/truth-change-classification-and-granularity-criteria.md` Rule 2).

## Phase 1 -- Align the plan package and truth owner

1. THINK Decide the mode first. `/axb-specify` at plan creation is **initialization mode**: go to
   step 2, then skip Phases 2–4 and finish at step 5. `/axb-system-analysis` reporting skips is
   **skip-record mode** and a truth owner skill is **owner mode**: both continue through the whole
   SOP — steps 2–5 and all four phases — with the mode's narrowed behaviour noted at each phase.
2. READ Read the caller handoff, the current plan package path, the truth root, and existing
   `truth-delta.md` content. In owner mode also read the truth owner name and the list of truth specs
   inspected or modified; in skip-record mode read the skipped owners' names and the analysis decision
   instead. Initialization and skip-record modes have no inspected specs — do not stop for them, and
   do not infer them.
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
   - **Owner mode and skip-record mode:** continue to Phase 2 to add this round's row(s) to the
     relevant section.

## Phase 2 -- Converge this round's truth change records

> Owner mode and skip-record mode. In skip-record mode the round's rows are exactly one `NOOP` per
> skipped owner, and steps 2–3 do not apply.

1. THINK Per the loaded rules, organize the caller-provided truth changes into semantic-unit rows; each row must contain `ADD`, `MODIFY`, `DELETE`, or `NOOP`, plus the truth spec, change summary, and reason.
2. THINK If the caller claims high-impact `MODIFY` or `DELETE` but the handoff does not state that `/axb-clarify` was completed or an explicit risk decision made, stop writing and require the caller to first supply the confirmation basis.
3. THINK If the same truth owner has no truth changes this round, converge one `NOOP` row, explicitly stating the inspected-but-unchanged truth scope and the reason.
4. THINK **Skip-record mode:** converge one `NOOP` row per skipped owner, each `Reason` naming the
   analysis decision and why no work of that kind exists this round
   (`rules/truth-change-classification-and-granularity-criteria.md` Rule 2). Do not record an
   "inspected, nothing needed" reason — nothing was inspected — and do not invent further rows for
   owners that did run.

## Phase 3 -- Update the owner section

> Owner mode and skip-record mode.

1. WRITE Append or update this round's table rows in `truth-delta.md`'s corresponding owner section; if that section is still a placeholder or an existing `NOOP` has been superseded by actual changes, clean up first and then write. In skip-record mode this is one `NOOP` row per skipped owner, each written into that owner's section and replacing its placeholder.
2. READ Review whether `truth-delta.md` still keeps one table per truth owner, and whether all rows conform to the fixed fields, action values, and semantic-unit granularity; fix any deviations immediately.

## Phase 4 -- Deliver downstream handoff

> Owner mode and skip-record mode.

1. WRITE Report to the caller the updated `truth-delta.md` path, owner section(s), and ADD / MODIFY /
   DELETE / NOOP counts; in owner mode also whether high-impact truth changes still need to return to
   `/axb-clarify`. In skip-record mode list every owner section that received a skipped-by-decision
   `NOOP`, so the caller can confirm the set matches what it actually skipped.

