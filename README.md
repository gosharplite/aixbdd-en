# aixbdd-en

**English translation of [aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)** — a set of AI
agent skills implementing a BDD (Behavior-Driven Development) workflow with clearly separated PM
and RD (developer) responsibilities.

> *PM defines acceptance criteria in Gherkin, RD turns them into automated tests, developing
> correct systems in one continuous flow.*

## What it is

A collection of **16 skill definitions** (each a `SKILL.md` plus supporting `rules/` and `templates/`
directories) that guide an AI through the full software development lifecycle — from requirements to
working code — using Gherkin as the shared contract language. The tagline: *"PM defines acceptance
criteria in Gherkin, RD turns them into automated tests, developing correct systems in one
continuous flow."*

## Core idea

Most AI dev workflows blur PM/RD responsibilities (e.g., developers end up "mind-reading" unclear
requirements). AIxBDD splits it:

- **PM side**: writes specs, acceptance Gherkin, and UI prototypes
- **RD side**: does technical research, API/data design, test planning, and implementation
- **Shared "truth"** (`specs/truth/**`): OpenAPI contracts, DBML data models, techstack, and
  interface feature/DSL files act as the single source of truth, tracked via `truth-delta.md` per
  plan package

## The workflow (skills in order)

1. `/axb-constitution` (PM/RD) — set artifact governance rules
2. `/axb-specify` (PM) — create a numbered plan package with spec.md + checklist
3. `/axb-clarify-over-specs` (PM) — (optional) interactive requirement clarification
4. `/axb-spec-by-example` (PM) — acceptance Gherkin
5. `/axb-ui-plan` (PM) — HTML prototypes for a web interface; rendered terminal frames for a CLI TUI
6. `/axb-technical-research` (RD) — technical research & update techstack truth
7. `/axb-system-analysis` (RD) — orchestrates `/axb-api-plan` (RD), `/axb-data-plan` (RD) via dependency waves
8. `/axb-dsl-refine` (RD) — split acceptance criteria into executable front/back-end Gherkin + DSL
9. `/axb-tasks` (RD) — generate BDD task list tasks.md
10. `/axb-implement` (RD) — One-Shot TDD execution, red → green → refactor via `/axb-bdd` (RD)

Supporting skills:
- `/axb-clarify` (PM/RD) — user interviews
- `/axb-truth-delta` (RD) — truth change tracking
- `/axb-gherkin-and-dsl` (PM/RD) — Gherkin/DSL standards + a Python topology audit script

### Developing CLI Applications

When developing a CLI application (no web frontend or HTTP/REST API), the workflow is streamlined:

1. **Skip `/axb-ui-plan` for a plain CLI**: For a line-oriented CLI (commands, flags, arguments,
   exit codes, stdin/stdout/stderr) no web UI or HTML mockups are created; terminal interactions are
   defined directly as Gherkin acceptance scenarios in `/axb-spec-by-example`. **Exception:** a CLI
   that ships a rich terminal UI (TUI) runs `/axb-ui-plan` in **terminal mode** — textual
   screens/keybindings under `ui/screens/*.txt`, still no HTML.
2. **Lean `/axb-system-analysis`**:
   - **`/axb-api-plan`** is skipped (standalone CLIs have no OpenAPI endpoints; marked as `NOOP` in
     `truth-delta.md`).
   - **`/axb-data-plan`** is conditional — invoked only if the CLI manages persistent configuration
     (e.g. `~/.config/...`), local storage (SQLite, JSON), or complex domain state. For stateless CLI
     tools, it is skipped.
3. **CLI Contract via `/axb-dsl-refine`**: The CLI end is a first-class truth-tree interface — a
   third `InterfaceKind`, `cli`, alongside `backend`/`frontend`. The executable Gherkin feature files
   (`specs/truth/features/cli/**`) and their step definitions (`dsl.md`) serve as the formal CLI
   contract and acceptance test runner. Since no API/data/UI planner applies, `/axb-system-analysis`
   records no planner for it and carries the CLI end forward to its contract owner `/axb-dsl-refine`.

### Resolving PR and Review Findings

When resolving architect or peer review findings on a pull request, modifying files under both implementation code and `specs/` is expected and required to prevent specification drift:

1. **Keep `specs/truth/**` synchronized with code**:
   - **Contracts**: Update `specs/truth/contracts/**` if endpoints, payloads, schemas, or status codes change.
   - **Data Models**: Update `specs/truth/data/**` if tables, relationships, fields, or indexes change.
   - **Techstack**: Update `specs/truth/techstack.md` if architectural choices or library selections change.
   - **Features & DSL**: Update `specs/truth/features/**` and `dsl.md` if business rules, step definitions, or acceptance assertions change.
2. **Log changes in `truth-delta.md`**: Record any changes made to `specs/truth/**` in the plan's `specs/plans/NNN-<slug>/truth-delta.md` (updating the corresponding truth owner's section with `MODIFY`, `ADD`, or `DELETE` and citing the review finding as the reason).
3. **Audit DSL changes**: If any feature or `dsl.md` files were modified, run the topology audit script to verify syntax and cross-references:
   ```bash
   python3 skills/axb-gherkin-and-dsl/scripts/audit_feature_dsl_topology.py --root specs/truth/features
   ```
4. **Code-only refactorings**: Internal refactorings, optimizations, or renames that do not alter external behavior or contracts do not touch `specs/` — update the production code and tests directly.

## Notes

- **Roles**: `roles/pm.yaml` and `roles/rd.yaml` role configs live in the upstream
  [aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg) repository (not translated here).
- **Decisions**: the workflow's own governed-artifact changes are recorded as short ADRs under
  `decisions/` in the upstream aixbdd-tmg repository.

## About this repository

This repository (**aixbdd-en**) originated as a faithful English translation of **[aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)**, which is itself an adapted derivative work of the original **[AIxBDD](https://github.com/Waterball-Software-Academy/aixbdd)**.

### Repository Lineage

```
[AIxBDD] (Upstream original by Waterball Agent Limited)
   │
   └──► [aixbdd-tmg] (Derivative: adds domain model, CLI guidance, role configs, axb- prefix)
          │
          └──► [aixbdd-en] (English edition: ongoing independent evolution)
```

1. **[AIxBDD](https://github.com/Waterball-Software-Academy/aixbdd)**: The upstream original BDD workflow created by Waterball Agent Limited (水球球特務有限公司), licensed under the **Apache License, Version 2.0**.
2. **[aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)**: A derivative work adapted from AIxBDD. **It is not identical to upstream AIxBDD** — it introduces several key architectural and workflow extensions:
   - **Prefix standard**: Skills are consistently renamed with an `axb-` prefix (e.g., `specify` → `axb-specify`, `bdd` → `axb-bdd`).
   - **Canonical Domain Model**: Introduces a formal domain model under `domain-model/` (`aixbdd.modelith.md` / `.yaml`).
   - **CLI Application Guidance**: Extends the workflow for command-line applications (the `cli` interface kind, terminal-mode UI plans, and streamlined analysis).
   - **Role configurations**: Adds PM and RD role definitions (`roles/pm.yaml`, `roles/rd.yaml`).
   - **Architecture Decision Records**: Tracks governance decisions under `decisions/`.
3. **[aixbdd-en](https://github.com/gosharplite/aixbdd-en)** (this repository): Began as the English translation of **aixbdd-tmg** (translated from aixbdd-tmg rather than original AIxBDD). Going forward, `aixbdd-en` maintains an **independent evolution path** — additional changes, English-native tooling, and workflow refinements are actively introduced here, so it is expected to deviate from upstream `aixbdd-tmg` over time.

### Baseline translation decisions

All initial files were translated from aixbdd-tmg's original Traditional Chinese; structure, semantics, and content are preserved as the baseline:

- Skill definition filenames (`SKILL.md`) and folder names are kept identical to the source.
- Rule filenames under `skills/*/rules/` have been renamed into English; internal cross-references
  were updated accordingly. Cross-skill references use the agreed English names (e.g. axb-bdd
  references `axb-implement`'s `rules/definition-of-done-verification-and-writeback-criteria.md`).
- Code identifiers, file paths, and skill names (e.g., `/axb-clarify`, `CONSTITUTION.md`) are kept
  as-is.
- The **default project language is flipped to English** (STANDARDS.md "Project Language" section and
  the §2/§3 defaults); it remains project-declarable, so projects may still declare any language.
- **Fixed DSL contract tokens are English**: `DSL Sentence`, `Gherkin Params`, `Data Table Params`,
  `Default Params`, `…Implementation Semantics`, `Not supported`/`Supported:`, and the §5.1/§5.2
  sub-labels (`How`, `State landing`, `Write-back`, `No-check`/`Must-check`, `Presented Result`,
  `Authoritative State`, `Re-read Confirmation`, `Cross-Perspective`, `Should Not Happen`). They were
  Chinese in upstream AIxBDD and are renamed in this repo; the audit script accepts both the English
  header `DSL Sentence` and the legacy Chinese header `DSL 句型`, so upstream-era DSL files still audit
  cleanly. These tokens remain fixed — do not translate them per project language. The Chinese Gherkin
  keywords in the audit script's `STEP_RE` are kept as parser locale support (Gherkin sentence language
  is project-declarable).

## Attribution & license

This repository is distributed under the **Apache License, Version 2.0** — see [LICENSE](LICENSE).

The upstream attribution notice is reproduced verbatim in [NOTICE](NOTICE), as required by
Apache-2.0 §4(d), together with a note describing this repository's modifications (the English
translation).

Five of the inherited skills — `axb-specify`, `axb-clarify-over-specs`, `axb-tasks`,
`axb-implement`, and `axb-technical-research` — were in turn derived by AIxBDD from
[GitHub Spec Kit](https://github.com/github/spec-kit) (MIT). Their per-skill `LICENSE` files are
retained alongside those skills; the original notices are preserved verbatim, with an unofficial
English translation appended for convenience (the original text is authoritative).

## Repository-level artifacts

- `domain-model/` — the canonical domain model (`aixbdd.modelith.md` + `.yaml`, generated by
  `modelith render`). The source is already English and is included verbatim, so downstream
  projects can use a single skill+model source of truth here.
