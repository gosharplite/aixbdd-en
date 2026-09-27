# Rule 1 - Before implementing, first read the phase shared reference or the current task's `Read`

- Level: `MUST`
- If the current task is in the `Feature File` phase or the `NFR Refactoring` phase, before implementing you must first read the documents and specific sections designated by that phase's `Shared Must Read`.
- If the current task is in `Setup`, `Foundational`, or another general phase, before implementing you must first read the documents and specific sections designated by that task's `Read`.
- Reference requirements are precise loads; reading only other parts of the same file does not satisfy them.
- If the same round contains multiple legitimate `[P]` tasks, confirm separately that each task's necessary references are covered.

## Good Example

- This example is good because it reads the phase's or task's explicitly required references first, then starts coding.

```md
The agent is about to do `T012 [BDD-GREEN]`.
It first reads the current feature file phase's `Shared Must Read`, confirming the three-guess end-game semantics;
only then does it supplement with `contracts/openapi.yaml` and `data-model.dbml` when needed.
```

## Bad Example

- This example is bad because it only looks at the task title without reading the actually authorized reference surface.

```md
The agent is about to do `T012 [BDD-GREEN]`.
It does not read `Shared Must Read`; just knowing this is the three-guess end-game flow, it starts changing the handler directly.
```

# Rule 2 - `Extra Read` and other artifacts are read only when needed

- Level: `MUST`
- `Extra Read` is read only when the current task actually lists extra documents, or when shared-file constraints, visual details, verification methods, or integration decisions need supplementing.
- Do not preload `tasks.md`, `plan.md`, `research.md`, `contracts/`, `data/`, `ui/` in full before starting to act.
- If a solution can already converge from `Shared Must Read` or the current task's `Read` and existing code, do not expand the context further.

## Good Example

- This example is good because it completes the main judgment with the necessary references first, supplementing `Extra Read` only when needed.

```md
The agent is about to do `T009 [BDD-GREEN]`.
It first reads the phase's `Shared Must Read`;
only when aligning the screen with the data model does it read `ui/ui-plan.md` and the backend feature file.
```

## Bad Example

- This example is bad because it loads all artifacts at once, bloating the context without improving the current task's decision quality.

```md
The agent is about to do `T021`.
It first reads `spec.md`, `plan.md`, `research.md`, `techstack.md`, `contracts/openapi.yaml`, `data-model.dbml`, and all `ui/*.html` in full before judging the screen error feedback.
```

# Rule 3 - Read adjacent tasks only when a shared modification surface or integration risk exists

- Level: `SHOULD`
- If the current task modifies files, shared state models, or shared verification surfaces also touched by the preceding/following tasks, read the adjacent tasks' descriptions and references to avoid locally-correct-but-globally-mismatched results.
- If the current task is independent with clear boundaries, do not read adjacent tasks extra just for form's sake.

## Good Example

- This example is good because it extends the read to adjacent tasks only when a modification surface is truly shared.

```md
The agent is about to do the cross-end integration task on `frontend/src/main.js`.
Since the adjacent tasks in the same file all touch the same state-sync logic,
the agent reads the adjacent tasks to confirm the page flow and app state will not overwrite each other.
```

## Bad Example

- This example is bad because it turns "read adjacent tasks" into a full read-through of the entire story every time.

```md
The agent is about to do a setup task that only changes `backend/.env.example`.
It still reads the entire `US3` block, with no shared file or integration need at all.
```

# Rule 4 - MODIFY / DELETE must load existing automated-test touchpoints

- Level: `MUST`
- If the current task corresponds to truth-delta's `MODIFY` or `DELETE`, besides `Shared Must Read` and `Extra Read`, you must also load or locate the affected existing feature scenarios, step definitions, fixtures, helpers, focused tests, and product branches.
- If `tasks.md` already lists existing test touchpoints, the designated files must be read; if not listed, do a minimal-scope search first and report the `tasks.md` gap.
- Do not start implementing after reading only the latest truth feature/dsl, because old tests may still be protecting outdated truth.

## Good Example

- This example is good because it reads the existing step definitions in sync while modifying the DSL.

```md
Shared Must Read:
- `specs/truth/features/backend/room-chat/dsl.md`
- `backend/features/steps/modules/room-chat/operations_and_assertions.py`
```

## Bad Example

- This example is bad because it does not read the existing test touchpoints.

```md
Reads only `specs/truth/features/backend/room-chat/dsl.md` and modifies the product code directly.
```

