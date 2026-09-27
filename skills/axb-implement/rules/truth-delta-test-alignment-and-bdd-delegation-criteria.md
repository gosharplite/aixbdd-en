# Rule 1 - The truth delta action must be determined before execution

- Level: `MUST`
- Before `/axb-implement` starts a task, it must determine from `truth-delta.md` and `tasks.md` whether the current task corresponds to `ADD`, `MODIFY`, `DELETE`, or `NOOP`.
- If the task is not explicitly linked to a truth-delta row but belongs to a phase affected by truth changes, the action must be inferred from the phase's `Shared Must Read` and `Boundary`.
- A `[BDD-RED]` used by this round's Feature that has no stepdef yet and thus is not in truth-delta has its action treated as `ADD`.
- If the action cannot be determined and would affect tests or product behavior, stop and report that `tasks.md` needs explicit references added.

## Good Example

- This example is good because axb-implement first determines the current task is MODIFY.

```md
T008 [BDD-ALIGN]
truth-delta: /axb-dsl-refine MODIFY `When: "{player}" sends message "{content}"`
action: MODIFY
```

## Bad Example

- This example is bad because it looks only at the task marker without reading back truth-delta.

```md
Seeing [BDD-GREEN] it changes the product code directly, without confirming whether it is ADD or MODIFY.
```

# Rule 2 - Before changing product code, Phase 3 must have aligned the tests

- Level: `MUST`
- Before Feature Green / `CODE-REMOVE` starts changing product code, Phase 3 review must have passed.
- If existing tests still express old truth, they must be handled in Phase 3 first via `[BDD-ALIGN]` or `[BDD-REMOVE]`; do not opportunistically change tests in Green to force it green.
- If no existing test touchpoint can be found, the search scope must be recorded, and stepdefs covering the new version of truth must be created in Phase 3.

## Good Example

- This example is good because product code is only touched after the test layer is aligned.

```md
Only after T015 review passes does T018 [BDD-GREEN] adjust the message-sending implementation.
```

## Bad Example

- This example is bad because the product code is changed while old tests still verify the wrong spec.

```md
Only a new-version test is added and made to pass, without handling the step definitions that still expect the old behavior.
```

# Rule 3 - DELETE must clean tests first, then product behavior

- Level: `MUST`
- Phase 3's `[BDD-REMOVE]` must remove or rewrite feature scenarios, step definitions, fixtures, helpers, or assertions that no longer hold.
- The Feature phase's `[CODE-REMOVE]` must remove or disable product branches supporting old truth.
- `[REGRESSION]` must run that phase's `Test Scope`, proving the new version of truth holds and the old behavior is no longer protected by tests.
- Do not merely stop supporting old behavior in the product code while leaving tests that still protect old truth.

## Good Example

- This example is good because tests and product behavior are separated by phase.

```md
Phase 3 BDD-REMOVE: remove old step assertions
Phase 4C CODE-REMOVE: remove old product code branches
Phase 4C REGRESSION: run Test Scope
```

## Bad Example

- This example is bad because it only deletes product branches.

```md
Delete the API field, but keep the old feature file and step definition.
```

# Rule 4 - Only Green / Refactor delegate to /axb-bdd, and always with Test Scope

- Level: `MUST`
- `/axb-implement` calls `/axb-bdd` only on `[BDD-GREEN]` or `[BDD-REFACTOR]`.
- When calling, it must explicitly provide `Test Scope`, truth delta action, affected truth rows, the same-module `dsl.md`, the interface root shared DSL rows actually used by that feature, and the requested step.
- If that feature uses no interface root shared DSL rows, it must explicitly state "none".
- `/axb-implement` only passes the precise DSL references already bound in `tasks.md`; it does not re-judge whether a sentence belongs to a module or shared.
- Phase 3's `[BDD-ALIGN]`, `[BDD-REMOVE]`, `[BDD-RED]` do not delegate to `/axb-bdd`.

## Good Example

- This example is good because Green carries the Test Scope.

```md
Call /axb-bdd
- requested step: green
- Test Scope: `specs/truth/features/backend/room-chat/single-player-waiting-and-empty-message-rejection.feature`
- action: ADD
- module dsl: `specs/truth/features/backend/room-chat/dsl.md`
- shared dsl rows: none
```

## Bad Example

- This example is bad because it treats Phase 3 ALIGN as `/axb-bdd`'s single-feature red.

```md
Call /axb-bdd, requested step=red, please handle the clear-after-leaving feature.
```
