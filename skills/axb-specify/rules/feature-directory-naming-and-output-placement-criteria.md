# Rule 1 - Every axb-specify run must create a new plan package

- Level: `MUST`
- Each `/axb-specify` execution must create a new `NNN-<slug>` plan package under `specs/plans/`.
- `NNN` is the highest existing plan package number plus one; existing packages must not be overwritten.
- Even if this requirement modifies or deletes existing behavior, create a new plan package, keeping old plans as history.

## Good Example

- This example is good because modifying existing match rules still creates a new iteration.

```text
specs/plans/004-change-match-rule/spec.md
```

## Bad Example

- This example is bad because it goes back and modifies an old plan package.

```text
specs/plans/001-online-pvp-1a2b/spec.md
```

# Rule 2 - axb-specify may only write plan artifacts

- Level: `MUST`
- `/axb-specify` may only write `spec.md`, `checklists/requirements.md`, and initialize `truth-delta.md`.
- `/axb-specify` must not add, modify, or delete `specs/truth/**`.
- Requirements involving existing truth may describe expected add / modify / delete intents in the spec, but the actual truth changes are handed to the truth owner skill.

## Good Example

- This example is good because all output stays inside the plan package.

```text
specs/plans/004-room-game-chat/spec.md
specs/plans/004-room-game-chat/checklists/requirements.md
specs/plans/004-room-game-chat/truth-delta.md
```

## Bad Example

- This example is bad because axb-specify modifies truth directly.

```text
specs/truth/contracts/openapi.yaml
```
