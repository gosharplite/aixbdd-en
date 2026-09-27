---
name: axb-ui-plan
description: Executed by the PM after spec and acceptance Gherkin are confirmed; based on the plan package's `spec.md`, confirmed `features/acceptance/**`, and existing `ui/**`, it produces plan-side `ui/**` design and reviewable prototypes for the PM to review before handing off to RD. Choose the medium by interface kind and interaction surface: web／`frontend` goes HTML mode (`ui/*.html`); a `cli` shipping an interactive TUI goes terminal mode (`ui/screens/*.txt`, no HTML); a plain line-oriented `cli` is skipped, producing no ui-plan. `axb-ui-plan` is not a truth owner and writes nothing to `specs/truth/**`.
disable-model-invocation: true
---

# UI Plan

`axb-ui-plan` only produces this iteration's UI plan and reviewable prototypes. UI artifacts stay in the plan package as implementation reference and review material — they are not system truth.

## Medium selection (by interface kind and interaction surface)

`axb-ui-plan` first selects the medium per this round's interface kind and interaction surface, then produces the corresponding artifacts:

- **web／`frontend` → HTML mode**: keep current behavior; prototypes are `ui/*.html` (clickable, navigable high-fidelity static pages).
- **`cli` with a TUI → terminal mode**: when the CLI presents a **persistent, multi-block, stateful interaction surface** (screens/panels, keybindings, popups, live state, repainting on input), use terminal mode; prototypes are `ui/screens/*.txt` (frames consistent with the actual terminal rendering), **producing no HTML**.
- **`cli` plain → skipped**: a plain line-oriented CLI (commands, flags, stdout/stderr, exit codes — no persistent interaction surface) produces no ui-plan; its contract is carried by `/axb-dsl-refine` via `specs/truth/features/cli/**`.
- The criterion is the **interaction surface**, not whether the name contains CLI; if undecidable, call `/axb-clarify` first — do not assume.

# SOP

## Phase 1 -- Align spec, acceptance, medium, and UI scope

1. READ Read the user requirements, the plan package's `spec.md`, confirmed `features/acceptance/**`, existing `ui/**`, and the UI-related existing `specs/truth/contracts/**`, `specs/truth/features/**`.
2. THINK Select the medium per this round's interface kind and interaction surface (HTML mode / terminal mode / skipped); if skipped, report and stop — produce no ui-plan.
3. READ Per the selected medium, read the corresponding templates and rules to confirm the finished look of the plan-side UI artifact and prototype:
   - HTML mode: `templates/ui-plan.md`, `templates/ui-plan.example.md`, `templates/prototype-entry.html`, `templates/prototype-entry.example.html`, `templates/prototype-screen.html`, `templates/prototype-screen.example.html`, `rules/high-fidelity-prototype-splitting-and-flow-coverage-criteria.md`, and `rules/prototype-and-implementation-plan-boundary-criteria.md`.
   - terminal mode: `templates/ui-plan.terminal.md`, `templates/ui-plan.terminal.example.md`, `templates/prototype-terminal-entry.txt`, `templates/prototype-terminal-entry.example.txt`, `templates/prototype-terminal-screen.txt`, `templates/prototype-terminal-screen.example.txt`, `rules/high-fidelity-prototype-splitting-and-flow-coverage-criteria.md`, and `rules/prototype-and-implementation-plan-boundary-criteria.md`.
4. DELEGATE If gaps would change user-visible flows, screen responsibilities, interaction entries, error states, or the alignment with truth, call `/axb-clarify`; stop before convergence.

## Phase 2 -- Produce the UI plan and prototypes

1. THINK Per the requirements, confirmed acceptance Gherkin, and existing truth, converge screen scope, states, main flows, visible feedback, and error handling; and add medium-specific aspects: HTML mode converges accessibility and responsive behavior; terminal mode converges keybindings (operation mapping) and state transitions.
2. WRITE Write the UI planning into `specs/plans/NNN-<slug>/ui/ui-plan.md`, using the corresponding medium's section skeleton (HTML mode uses `Visual Direction`; terminal mode uses `Terminal Visual Direction`, `Screens & Flows`, `Keybinding Map`, and `State Transition List`).
3. WRITE Produce or update the corresponding medium's prototypes per the UI plan; neither medium may write to `specs/truth/**`:
   - HTML mode: `specs/plans/NNN-<slug>/ui/*.html` and necessary static assets.
   - terminal mode: `specs/plans/NNN-<slug>/ui/screens/entry.txt` (entry/startup frame) and `specs/plans/NNN-<slug>/ui/screens/NN-<name>.txt` (subsequent frames); **no** HTML may be produced.
4. READ Review whether the UI plan and prototypes align with the spec, acceptance, and relevant existing truth; fix any deviations immediately.

## Phase 3 -- Deliver downstream handoff

1. WRITE Report to the PM the UI plan, prototype paths, the medium selected this time, and residual risks, as the planning basis for the PM to hand off to RD after confirmation; this skill writes nothing to `specs/truth/**`.
