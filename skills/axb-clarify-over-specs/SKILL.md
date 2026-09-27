---
name: axb-clarify-over-specs
description: After `/axb-specify` produces `spec.md`, proactively scan the entire spec for high-impact requirement gaps; if there are still issues that affect spec correctness, acceptance criteria, or readiness, first delegate `/axb-clarify` to interview the user, then write the answers back into the spec, clean up contradictions, and refresh the checklist. Use when the user asks for post-spec requirement clarification, wants a generated spec professionally reviewed before `/plan`, or needs a spec-level clarify pass after `/axb-specify`.
disable-model-invocation: true
---

# Clarify Over Specs

With `spec.md` already existing, perform proactive requirement clarification on the existing spec artifact. First align the target `spec.md` and `checklists/requirements.md`, then inventory high-impact gaps via a whole-spec scan; escalate to `/axb-clarify` only the questions that genuinely change spec correctness, acceptance criteria, story boundaries, data model, NFR boundaries, or downstream readiness judgments. Once information converges, integrate the answers back into the spec, clean up contradictions and terminology drift, and update the checklist and completion report in sync.

# SOP

## Phase 1 -- Align the target spec and writeback scope

1. READ Read the user requirements, caller requests, current context, any explicit override parameters, and the current feature's `spec.md` and `checklists/requirements.md`; confirm the spec target to clarify this time, whether a checklist exists, and whether a detailed completion report is needed. If the target `spec.md` cannot be found, stop and ask the user to run `/axb-specify` first or explicitly specify the target spec path.
2. THINK If you need to decide the target `SPEC_FILE`, `CHECKLIST_FILE`, and override priority, first read `rules/target-spec-locating-and-override-priority-criteria.md`, then converge this round's target files and writeback scope as it requires.

## Phase 2 -- Scan the whole spec for high-impact gaps and the clarify strategy

1. THINK First inventory — across the entire `spec.md` — the ambiguities, contradictions, omissions, and undecided decisions that affect requirement correctness, acceptance verifiability, story splitting, data model, NFR boundaries, terminology consistency, or readiness judgments.
2. THINK If you need to determine which gaps must be escalated to `/axb-clarify`, which can be kept as deferred risks or stated explicitly in the spec, first read `rules/spec-high-impact-gap-scan-and-question-ordering-criteria.md`, then converge — as it requires — this round's 1 to 3 highest-impact gaps, the specified questioning dimensions, and the low-impact details that should not be pursued this round.
3. DELEGATE If high-impact gaps remain that would change spec correctness, formal acceptance criteria, cross-story requirement boundaries, key data constraints, NFR commitments, or readiness judgments, call `/axb-clarify` to interview the user first, specifying the priority questioning dimensions as this round's converged gaps, and requiring only 1 to 3 questions this round; stop before convergence, and do not assume answers on your own.

## Phase 3 -- Integrate the clarification results back into the spec

1. READ Read the confirmed decisions, user additions, and remaining risks produced by `/axb-clarify`; confirm which answers need to be written back into `spec.md` and which gaps should remain deferred or `NEEDS CLARIFICATION`.
2. THINK If you need to determine which sections the answers should be written back to, which old statements should be replaced or deleted, and which terminology should be unified, first read `rules/spec-writeback-placement-and-conflict-cleanup-criteria.md`, then converge — as it requires — the sections to update, the conflict cleanup method, and the terminology unification strategy.
3. WRITE Update `SPEC_FILE` per the thinking results: integrate confirmed answers into the corresponding sections, clean up old statements and terminology drift overturned by the new answers; if high-impact gaps remain unresolved, explicitly state their retained status and follow-up suggestions — do not fill in the blanks by imagination.

## Phase 4 -- Re-verify the spec and checklist

1. THINK If you need to determine which checklist items should switch status, which sections have reached ready, and what update results the completion report should present, first read `rules/checklist-refresh-and-completion-report-criteria.md`, then converge — as it requires — this round's checklist updates, ready judgment, deferred risks, and completion report highlights.
2. WRITE If `CHECKLIST_FILE` exists, update — per the thinking results — only the checkboxes whose actual status changed, leaving the rest untouched; if there is no checklist this round, skip this step but retain an explicit statement on the ready status.
3. READ Review whether `SPEC_FILE`, `CHECKLIST_FILE` (if present), and this round's confirmed answers are consistent, with no leftover old statements, duplicate specs, or conflicting conclusions overturned by this round's answers; fix any inconsistencies immediately.

## Phase 5 -- Deliver results and hand off follow-ups

1. WRITE First read `templates/clarify-over-specs-report.md` and `templates/clarify-over-specs-report.example.md`, then report to the user — as they require — this round's target `SPEC_FILE`, whether `/axb-clarify` was entered, the high-impact gaps actually handled, updated sections, checklist changes, still-deferred risks, and whether the recommended next step is to proceed directly to `/plan` or run `/axb-clarify-over-specs` again later.
