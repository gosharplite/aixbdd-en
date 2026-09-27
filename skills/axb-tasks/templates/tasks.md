# Tasks: {{FEATURE_NAME}}

**Plan Package**: `{{PLAN_PACKAGE}}`
**Core Inputs**: `spec.md`, `plan.md`, `research.md`, `truth-delta.md`, `specs/truth/techstack.md`, `specs/truth/contracts/**`, `specs/truth/data/**`, `specs/truth/features/**`, `ui/**`

## Task Binding Contract

- Every **development task** must correspond to an ADD / MODIFY / DELETE / NOOP semantic in `truth-delta.md`.
- This round's `research.md` decided Decisions and `specs/truth/**` non-NOOP items must be fully covered in the tasks' `Read` or delivery targets, leaving no orphaned artifacts (Pre-Delivery Orphan Coverage Sweep).
- Unobservable atomic effect claims (Atomic Effect Claims) derived from every normative item (FR / NFR / SC / EC) must be scheduled for `[WITNESS]` task coverage, or recorded as `accepted-unwitnessed` on the project decision surface; anything unwitnessed must never be promoted to truth surfaces in prose guarantee form (Claim→Witness Obligation).
- When tasks have ordering dependencies, the ordering constraint must be explicitly declared with `Dependencies: T###`.
- Setup / Foundational build or verification tasks derived from `research.md` Decisions (e.g. build parameters, version, make targets) need not correspond to `truth-delta.md` rows.
- Phase 1 `Setup` does only this round's new-technology infrastructure, technical environment, and final smoke-test; writes no DSL semantics and no product behavior.
- Phase 2 `Foundational` only establishes the implementation code, test-shared components, entry points, fixtures, helpers, and touchpoint skeletons for later work.
- Phase 3 `Test Alignment & Implementation`'s purpose: before writing product code, align the automated tests of all affected DSL this round with the latest truth first.
- Truth references must use `specs/truth/**` paths; only plan references use relative paths within the current plan package.

## Phase 1: Setup

**Goal**: {{SETUP_GOAL}}

- [ ] T{{SETUP_PACKAGE_TASK_ID}} {{SETUP_PACKAGE_TASK_TITLE}}
  - Read:
    - `specs/truth/techstack.md` -> {{SETUP_PACKAGE_TECHSTACK_SECTION}}
  - {{SETUP_PACKAGE_DEPENDENCY_ACTION}}
  - {{SETUP_PACKAGE_CONFIG_ACTION}}

- [ ] T{{SETUP_ENV_TASK_ID}} {{SETUP_ENV_TASK_TITLE}}
  - Read:
    - `specs/truth/techstack.md` -> {{SETUP_ENV_TECHSTACK_SECTION}}
    - `{{SETUP_ENV_APP_PATH}}` -> {{SETUP_ENV_MOUNT_POINT}}
  - {{SETUP_ENV_ENABLE_ACTION}}
  - {{SETUP_ENV_BOUNDARY}}

- [ ] T{{SETUP_SMOKE_TASK_ID}} {{SETUP_SMOKE_TASK_TITLE}}
  - Read:
    - `specs/truth/techstack.md` -> {{SETUP_SMOKE_TECHSTACK_SECTION}}
  - {{SETUP_SMOKE_VERIFY_ACTION}}
  - {{SETUP_SMOKE_BOUNDARY}}

## Phase 2: Foundational

**Goal**: {{FOUNDATIONAL_GOAL}}

- [ ] T{{FOUNDATIONAL_HELPER_TASK_ID}} {{FOUNDATIONAL_HELPER_TASK_TITLE}}
  - Read:
    - `truth-delta.md` -> {{FOUNDATIONAL_HELPER_TRUTH_DELTA_ROWS}}
    - `{{FOUNDATIONAL_HELPER_PATH}}`
  - Only do: {{FOUNDATIONAL_HELPER_DO}}
  - Do not: {{FOUNDATIONAL_HELPER_DONT}}

- [ ] T{{FOUNDATIONAL_CONNECTION_TASK_ID}} {{FOUNDATIONAL_CONNECTION_TASK_TITLE}}
  - Read:
    - `specs/truth/techstack.md` -> {{FOUNDATIONAL_CONNECTION_TECHSTACK_SECTION}}
    - `{{FOUNDATIONAL_CONNECTION_HELPER_PATH}}`
  - Only do: {{FOUNDATIONAL_CONNECTION_DO}}
  - Do not: {{FOUNDATIONAL_CONNECTION_DONT}}

- [ ] T{{FOUNDATIONAL_LANDING_TASK_ID}} {{FOUNDATIONAL_LANDING_TASK_TITLE}}
  - Read:
    - `{{FOUNDATIONAL_LANDING_PATH}}`
  - Only do: {{FOUNDATIONAL_LANDING_DO}}
  - Do not: {{FOUNDATIONAL_LANDING_DONT}}

- [ ] T{{FOUNDATIONAL_FIXTURE_TASK_ID}} {{FOUNDATIONAL_FIXTURE_TASK_TITLE}}
  - Read:
    - `{{FOUNDATIONAL_FIXTURE_DATA_PATH}}` -> {{FOUNDATIONAL_FIXTURE_DATA_SECTION}}
    - `{{FOUNDATIONAL_FIXTURE_HELPER_PATH}}`
  - Only do: {{FOUNDATIONAL_FIXTURE_DO}}
  - Do not: {{FOUNDATIONAL_FIXTURE_DONT}}

## Phase 3: Test Alignment & Implementation

**Goal**: Align the automated tests of the DSL used by this round's Feature with the latest truth; including the sentences changed in truth-delta, and the sentences used by this round's Feature that have no stepdef yet. Write no product behavior.

**DSL Reference**:
- Each sentence belongs to exactly one authoritative `dsl.md`: the same-module `specs/truth/features/{interface}/{module}/dsl.md`, or the interface root `specs/truth/features/{interface}/dsl.md`. Do not scan other modules.
- This round's sentences all live in the same module `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/dsl.md`. {{PHASE3_ROOT_DSL_STATUS}}
- How to read: match the task title's sentence to that row in the file, taking `StepDef 實作語意` as the test code semantics. For Given / When read `怎麼做`, `權威狀態落地`, `回寫`; for Then read `必查` (`呈現結果`, `權威狀態`, `再讀確認`).
- `truth-delta.md` only tells whether this sentence is ADD / MODIFY / DELETE. Semantics follow that `dsl.md` row; do not invent from feature wording or old stepdefs.

**Markers**:
- `[BDD-ALIGN]`: `MODIFY`. The existing stepdef is still there but its semantics are old truth. Change the tests per that `dsl.md` row so they express the latest `StepDef 實作語意`.
- `[BDD-REMOVE]`: `DELETE`. This sentence is no longer truth. Remove or rewrite the stepdef / assertion still bound to this sentence, leaving no tests protecting old behavior.
- `[BDD-RED]`: `ADD`, or sentences used by this round's Feature with no stepdef yet. Write the stepdef per that `dsl.md` row. When done, this sentence can be run, with failures only from assertions or product behavior — never undefined steps.
- All three markers touch only the test layer, writing no product code.

**Shared Must Read**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/dsl.md`
  -> `{{PHASE3_MODULE_DSL_SENTENCE}}`
{{OPTIONAL_PHASE3_ROOT_DSL_SHARED_MUST_READ}}
- `truth-delta.md` -> the sentences where `/axb-dsl-refine` has corresponding ADD / MODIFY / DELETE
- `{{PHASE3_EXISTING_STEPDEF_PATH}}`

**Boundary**:
- One DSL sentence per task.
- Change only that sentence's stepdef / assertion / directly dependent helpers.
- Touchpoint files should as much as possible use independent files (Zero Shared Edits principle, SHOULD), eliminating parallel write conflicts.
- Write no product code.
- Review launches a subagent; all of this round's Test Scopes must no longer have undefined steps, failures only from assertions or product behavior. Fix issues and review again until there are none. Phase 4 stays locked until it passes.

**Parallel Hint**:
- T{{PHASE3_FIRST_DSL_TASK}}–T{{PHASE3_LAST_DSL_TASK}} each get one independent subagent (scheduled per `parallel-hint-subagent-and-same-file-scheduling-criteria.md`); T{{PHASE3_REVIEW_TASK}} starts its review subagent only after all return.

- [ ] T{{ALIGN_TASK_ID}} [P] [BDD-ALIGN] `{{ALIGN_DSL_SENTENCE}}`
  - Read: `{{ALIGN_EXISTING_STEPDEF_PATH}}` (prefer independent per-task touchpoints to enable parallel dispatch)

- [ ] T{{REMOVE_TASK_ID}} [P] [BDD-REMOVE] `{{REMOVE_DSL_SENTENCE}}`
  - Read: `{{REMOVE_EXISTING_STEPDEF_PATH}}` (prefer independent per-task touchpoints to enable parallel dispatch)

- [ ] T{{RED_TASK_ID}} [P] [BDD-RED] `{{RED_DSL_SENTENCE}}`
  - Read: `{{RED_STEPDEF_LANDING_PATH}}` (prefer independent per-task touchpoints to enable parallel dispatch)

- [ ] T{{PHASE3_REVIEW_TASK}} subagent review (phase quality gate)

## Phase 4A: ADD Feature File - {{INTERFACE_KIND}}/{{MODULE}}/{{ADDED_FEATURE_FILE_NAME}}.feature

**Goal**: {{ADD_FEATURE_PHASE_GOAL}}

**Shared Must Read**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/{{ADDED_FEATURE_FILE_NAME}}.feature` -> `Feature: {{ADDED_FEATURE_TITLE}}`
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/dsl.md` -> `{{ADDED_DSL_REQUIRED_SECTIONS}}`
- `truth-delta.md` -> `{{ADD_TRUTH_DELTA_ROWS}}`

**Boundary**:
- {{ADD_BOUNDARY_RULE}}

**Test Scope**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/{{ADDED_FEATURE_FILE_NAME}}.feature`

- [ ] T{{ADD_GREEN_TASK_ID}} [BDD-GREEN] Make the Test Scope all green
- [ ] T{{ADD_REFACTOR_TASK_ID}} [BDD-REFACTOR] {{ADD_REFACTOR_TASK_TITLE}}

## Phase 4B: MODIFY Feature File - {{INTERFACE_KIND}}/{{MODULE}}/{{MODIFIED_FEATURE_FILE_NAME}}.feature

**Goal**: {{MODIFY_FEATURE_PHASE_GOAL}}

**Shared Must Read**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/{{MODIFIED_FEATURE_FILE_NAME}}.feature` -> `Feature: {{MODIFIED_FEATURE_TITLE}}`
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/dsl.md` -> `{{MODIFIED_DSL_REQUIRED_SECTIONS}}`
- `truth-delta.md` -> `{{MODIFY_TRUTH_DELTA_ROWS}}`

**Boundary**:
- {{MODIFY_BOUNDARY_RULE}}

**Test Scope**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/{{MODIFIED_FEATURE_FILE_NAME}}.feature`

- [ ] T{{MODIFY_GREEN_TASK_ID}} [BDD-GREEN] Make the Test Scope all green
- [ ] T{{MODIFY_REFACTOR_TASK_ID}} [BDD-REFACTOR] {{MODIFY_REFACTOR_TASK_TITLE}}

## Phase 4C: DELETE Feature / DSL Truth - {{DELETED_TRUTH_UNIT}}

**Goal**: {{DELETE_PHASE_GOAL}}

**Shared Must Read**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/{{DELETED_FEATURE_FILE_NAME}}.feature` -> `Feature: {{DELETED_FEATURE_TITLE}}`
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/dsl.md` -> `{{DELETE_DSL_SECTIONS}}`
- `truth-delta.md` -> `{{DELETE_TRUTH_DELTA_ROWS}}`
- `{{OBSOLETE_PRODUCT_CODE_PATH}}` -> {{OBSOLETE_PRODUCT_BEHAVIOR}}

**Boundary**:
- {{DELETE_BOUNDARY_RULE}}

**Test Scope**:
- `specs/truth/features/{{INTERFACE_KIND}}/{{MODULE}}/{{DELETED_FEATURE_FILE_NAME}}.feature`

- [ ] T{{CODE_REMOVE_TASK_ID}} [CODE-REMOVE] {{CODE_REMOVE_TASK_TITLE}}
- [ ] T{{REGRESSION_TASK_ID}} [REGRESSION] Run the Test Scope, confirming the new version of truth holds

## Phase 4W: Witness Pins - {{WITNESS_GROUP_NAME}}

<!--
  Conditional Phase: create only when this round has normative claims not externally observable via Gherkin (NFR / SC / EC / internal invariants).
  If this round has no such claims, or all are observable Features, this Phase may be omitted.
-->

**Goal**: {{WITNESS_PHASE_GOAL}}

**Shared Must Read**:
- `specs/truth/techstack.md` -> {{WITNESS_TECHSTACK_SECTION}}
- `spec.md` -> {{WITNESS_SPEC_SECTIONS}}
- `truth-delta.md` -> {{WITNESS_TRUTH_DELTA_ROWS}}

**Boundary**:
- {{WITNESS_BOUNDARY_RULE}}

- [ ] T{{WITNESS_TASK_ID}} [WITNESS] {{WITNESS_CLAIM_EFFECT}}
  - Dependencies: T{{WITNESS_DEPENDS_ON_TASK_ID}}
  - Read:
    - `spec.md` -> {{WITNESS_SPEC_CLAIM_ID}}
    - `specs/truth/techstack.md` -> {{WITNESS_TECHSTACK_ITEM}}
  - Test Scope: `{{WITNESS_TEST_PATH}}`
  - Falsifier: {{WITNESS_DISCRIMINATING_MUTATION}}
  - Target: `{{WITNESS_TARGET_CODE_PATH}}`

## Pre-Delivery Inventory & Coverage Cross-Reference

### 1. Pre-Delivery Orphan Coverage Sweep (Orphaned Artifact Inventory)
- `truth-delta.md` non-NOOP items: fully allocated to tasks.
- `research.md` decided Decisions: fully referenced by task Reads or directly delivered.
- `specs/truth/techstack.md` changed sections: fully taken over by Setup/Foundational tasks.

### 2. Claim→Witness Ledger (Claim→Witness Inventory Cross-Reference)

| Claim ID | Source Spec / Truth Anchor | Claimed Effect (Atomic Effect Claim) | Witness Type (`[WITNESS]` / `[BDD-GREEN]` / `accepted-unwitnessed`) | Bound Task / Decision Record | Discriminating Falsifier | Status |
|---|---|---|---|---|---|---|
| CLM-{{CLAIM_ID}} | {{CLAIM_SOURCE}} | {{CLAIM_EFFECT}} | {{WITNESS_TYPE}} | T{{BINDING_TASK_ID}} / ADR-{{ADR_NUM}} | {{FALSIFIER_DESCRIPTION}} | {{STATUS}} |

