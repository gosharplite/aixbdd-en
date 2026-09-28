# Rule 1 - The inventory is only for writing Phase 3; it must not be output as an Impact Audit phase

- Level: `MUST`
- When `truth-delta.md` contains `MODIFY` or `DELETE` rows, before writing Phase 3 you must inventory the affected truth feature/dsl, existing step definitions, fixtures, helpers, focused tests, product branches, and regression test surfaces.
- This inventory happens only during `/axb-tasks` convergence and task writing, used to decide ALIGN / REMOVE / RED, Foundational's `Read`, and Feature's product code touchpoints.
- Do not write the inventory as a `Truth Delta Impact Audit` phase, nor output T00x tasks for `/axb-implement` to do.
- Phase 1 `Setup` is created only when this round adds new technology: write clearly the package names, configuration, technical environment, and the final smoke-test; write no DSL semantics and no product behavior.
- If this round adds no new technology, omit Setup; do not stuff helpers, fixtures, or touchpoint skeletons into Setup.
- Phase 2 `Foundational` only establishes the implementation code, test-shared components, entry points, fixtures, helpers, and touchpoint skeletons for later work; each rule must write "only-do / not-do".
- Setup and Foundational must not sneak in Phase 3's test layer or Feature Green.

## Good Example

- This example is good because the inventory stays at task-writing time, output starts from Setup, and package names are explicit.

```md
Before writing Phase 3, inventory the existing `operations_and_assertions.py` first, used to mark `[BDD-ALIGN]`.
The first phase in `tasks.md` is Setup:

- [ ] T001 Add the `websockets` package and test connection configuration
```

## Bad Example

- This example is bad because it writes the inventory as a phase for implement to do.

```md
## Phase 1: Truth Delta Impact Audit

- [ ] T001 Inventory the chat MODIFY / DELETE impact on existing automated tests and product code
```

# Rule 2 - The test layer concentrates in Phase 3; Feature phases keep only product code tasks

- Level: `MUST`
- `ADD` sentences, or sentences used by this round's Feature with no stepdef yet: Phase 3 uses `[BDD-RED]`; the corresponding Feature phase keeps only `[BDD-GREEN] -> [BDD-REFACTOR]`.
- `MODIFY` sentences: Phase 3 uses `[BDD-ALIGN]`; the corresponding Feature phase keeps only `[BDD-GREEN] -> [BDD-REFACTOR]`.
- `DELETE` sentences: Phase 3 uses `[BDD-REMOVE]`; the corresponding Feature phase keeps only `[CODE-REMOVE] -> `[REGRESSION]`.
- A DSL row that only moves its unique authoritative location with unchanged semantics is still `MODIFY`; Phase 3 only aligns precise references and existing test entries, and must not split it into `[BDD-REMOVE]` and `[BDD-RED]`.
- Do not write `[BDD-RED]`, `[BDD-ALIGN]`, or `[BDD-REMOVE]` into Feature phases.
- Do not force DELETE into an addition-style RED, nor treat MODIFY as a completely new feature file.

## Good Example

- This example is good because the test layer is in Phase 3 and Feature keeps only Green.

```md
## Phase 3: Test Alignment & Implementation

- [ ] T008 [P] [BDD-ALIGN] `When: "{player}" sends message "{content}"`

## Phase 4B: MODIFY Feature File - backend/room-chat/realtime-chat-while-both-present.feature

- [ ] T018 [BDD-GREEN] Make the Test Scope all green
- [ ] T019 [BDD-REFACTOR] Tidy the chat write and re-read confirmation shared logic under the green light
```

## Bad Example

- This example is bad because ALIGN is still bound inside the Feature phase.

```md
## Phase 4B: MODIFY Feature File - backend/room-chat/realtime-chat-while-both-present.feature

- [ ] T010 [BDD-ALIGN] First change the existing tests to the new DSL semantics
- [ ] T011 [BDD-GREEN] Write the new feature
```

# Rule 3 - Phase 3 must list all pending DSL sentences used by this round's Feature

- Level: `MUST`
- Phase 3's list must include truth-delta's `ADD` / `MODIFY` / `DELETE` sentences, plus sentences used by this round's Feature that have no stepdef yet.
- One `[P]` task per DSL sentence; sentences whose semantics are unchanged and already have stepdefs are not listed.
- `[BDD-ALIGN]` only changes existing tests to express the latest `StepDef Implementation Semantics`, writing no product code.
- `[BDD-REMOVE]` only removes or rewrites tests still protecting old truth, writing no product code.
- `[BDD-RED]` writes the stepdef per that `dsl.md` row; when done, this sentence can be run, with failures only from assertions or product behavior.

## Good Example

- This example is good because sentences used by this round's Feature but not in truth-delta also enter Phase 3.

```md
- [ ] T011 [P] [BDD-RED] `Given: "{player}" is alone waiting in the room`
- [ ] T012 [P] [BDD-RED] `When: "{player}" attempts to send an empty message`
```

## Bad Example

- This example is bad because it lists only the sentences changed in truth-delta; Green gets stuck on the un-written Given.

```md
Phase 3 lists only `When: "{player}" attempts to send an empty message`.
The Given used by `single-player-waiting-and-empty-message-rejection.feature` has no stepdef and no task.
```

# Rule 4 - DELETE's product behavior stays in the Feature phase

- Level: `MUST`
- `[BDD-REMOVE]` completes the test layer cleanup in Phase 3.
- `[CODE-REMOVE]` removes or disables product branches, API projections, data fields, or UI behaviors supporting old truth in the Feature phase.
- `[REGRESSION]` must run that phase's `Test Scope`, proving the new version of truth holds and the old behavior is no longer protected by tests.

## Good Example

- This example is good because tests and product behavior are separated with the right order.

```md
Phase 3: [BDD-REMOVE] `Then: the opponent still sees messages sent before leaving the room`
Phase 4C: [CODE-REMOVE] Remove the product code branch retaining leave-room messages
Phase 4C: [REGRESSION] Run Test Scope
```

## Bad Example

- This example is bad because it deletes only product code, leaving obsolete tests behind.

```md
- [ ] T020 [CODE-REMOVE] Remove the old feature
```

# Rule 5 - Phase 3 parallel tasks should prefer independent touchpoint files (Zero Shared Edits principle)

- Level: `SHOULD`
- When Phase 2 `Foundational` reserves step definition touchpoint skeletons, and when Phase 3 plans pending DSL tasks, prefer an independent-file architecture (e.g. one task one file, leveraging Go `init()` auto-registration, pytest-bdd independent modules, or step file splitting) to achieve "Zero Shared Edits".
- Independent touchpoint files let Phase 3's `Parallel Hint` truly dispatch fully in parallel with no locking and no contention, maximizing parallel throughput.
- If language or existing architecture constraints force multiple DSL sentences into the same physical file, task planning must explicitly mark that shared file to facilitate `/axb-implement`'s same-file sequential scheduling, avoiding Lost Update.

## Good Example

- This example is good because touchpoints use one task one file, eliminating write conflicts for parallel dispatch.

```md
Foundational establishes the `features/steps/` directory skeleton.
Phase 3 tasks point to independent files:
- [ ] T008 [P] [BDD-ALIGN] `When: "{player}" sends message "{content}"` -> Read: `steps/when_send_msg.go`
- [ ] T009 [P] [BDD-ALIGN] `Then: the chat content is visible` -> Read: `steps/then_recv_msg.go`
Each subagent's target file is mutually exclusive; safe to dispatch fully in parallel.
```

## Bad Example

- This example is bad because despite having independent file-splitting conditions, it artificially stuffs many parallel tasks into the same physical file.

```md
The project uses Go and could clearly use `init()` for independent per-stepdef files, yet all 15 Phase 3 parallel tasks point to the same `chat_steps.go`, artificially creating file write contention.
```
