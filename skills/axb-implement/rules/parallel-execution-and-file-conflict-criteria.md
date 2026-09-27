# Rule 1 - `[P]` is parallel permission; a Parallel Hint is a batch that must be dispatched at once

- Level: `MUST`
- Under the premise that `/axb-implement` One-Shot is exactly 1 task per round, a task marked `[P]` without a `Parallel Hint` only means it can theoretically run in parallel with other `[P]` tasks — it does not mean it must be bundled into one round.
- If the current phase has a `Parallel Hint`, the `[P]` batch listed by the Hint must be dispatched at once per `rules/parallel-hint-subagent-and-same-file-scheduling-criteria.md`.
- Sequential tasks not marked `[P]` must not be batched. The Feature phase is sequential by default.

## Good Example

- This example is good because Feature Green is still sequential while Phase 3 obeys the Hint.

```md
Phase 3 has a Parallel Hint: dispatch T008–T014 at once.
Phase 4A's T016 [BDD-GREEN] and T017 [BDD-REFACTOR] are not marked [P], still sequential.
```

## Bad Example

- This example is bad because it sees `[P]` and ignores the Hint scope, or parallelizes Feature Green too.

```md
Parallelize T016 [BDD-GREEN] and T018 [BDD-GREEN] at once, both changing the same store.
```

# Rule 2 - Shared files must be sequential; Parallel Hint dispatching is based on independent files (Zero Shared Edits)

- Level: `MUST`
- Feature-phase or non-Phase-3 tasks that would modify the same file, the same module's responsibility boundary, or depend on the same not-yet-stable verification result must run sequentially.
- Phase 3's `[P]` batch:
  - If the target files are mutually independent (Zero Shared Edits principle, one task one file), the whole batch must be dispatched at once as parallel subagents per the `Parallel Hint`.
  - If multiple `[P]` tasks write to the same physical file, to avoid Lost Update write conflicts they must run sequentially by target file (after the previous task's write is flushed to disk, the next task reads the latest content and layers its changes on top); multiple subagents must not write the same physical file concurrently. Details follow `parallel-hint-subagent-and-same-file-scheduling-criteria.md`.
- When a clear integration task exists, the preceding tasks should be converged by the integration task after they complete.

## Good Example

- This example is good because independent files are dispatched in parallel while shared files are safely sequential.

```md
Phase 3 independent files: T008 writes `when_send.go`, T009 writes `then_recv.go`, dispatched in parallel at once.
Phase 3 shared file: T008 and T009 both write `operations_and_assertions.py`; the orchestrator runs them sequentially (only after T008 is flushed does T009 read the latest content and write).
```

## Bad Example

- This example is bad because it forces sequential execution despite independent files and a Parallel Hint, or blindly parallelizes same-file writes causing overwrites.

```md
T008–T011 each write independent files (e.g. `step_a.go`, `step_b.go`) and Phase 3 has a Parallel Hint, yet the parallel permission is ignored and forced into one-by-one execution.
Or: T008 and T009 write the same file, and the agent still dispatches two subagents in parallel to change that file, causing a Lost Update.
```

# Rule 3 - After a parallel batch completes, verify each first, then do the overall convergence verification

- Level: `SHOULD`
- If a parallel batch genuinely exists this round, first confirm each task's own local completion conditions, then do one overall convergence verification.
- Do not verify just one of the tasks and treat the whole batch as complete.
- Phase 3's overall convergence verification is carried by the review task.

## Good Example

- This example is good because it looks at the local results first, then at the review.

```md
After T008–T014 each report their alignment results, T015 review runs all of this round's Test Scopes, confirming no undefined steps.
```

## Bad Example

- This example is bad because it verifies just one item and checks the whole batch.

```md
Looking only at T008's diff, the agent marks T008–T014 all as `[X]`.
```
