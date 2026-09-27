# Rule 1 - Without a specified scope, scan top-down for the first unlocked task as the One-Shot starting point

- Level: `MUST`
- If the user explicitly specifies `T###`, `US#`, a phase, or another scope, tasks must be selected within the specified scope first.
- If the user does not specify a scope, scan `tasks.md` top-down and take the first "unfinished and unlocked" task as the One-Shot starting point.
- `Unlocked` must be judged by `Dependencies`, phase / story prerequisites, and current check states; do not skip still-blocked tasks on your own.

## Good Example

- This example is good because with no scope specified it still follows `tasks.md` order from the first unlocked task.

```md
The user only says "please implement".
The agent first reads `tasks.md`, finds `T001` and `T002` both unfinished but `T001` is the first unlocked task.
The agent starts from `T001` instead of jumping to the later `US2` tasks.
```

## Bad Example

- This example is bad because it skips earlier unfinished or still-locked tasks.

```md
The user only says "please implement".
The agent directly picks `T018` because it looks more interesting, without checking whether the earlier `Setup` and `Foundational` are done.
```

# Rule 2 - By default it is don't stop until deliver / One-Shot

- Level: `MUST`
- The default is not to stop after a single task. After verifying and writing back `[X]`, recompute the next unlocked, in-scope task and continue until delivery.
- The user does not need to write `don't stop until deliver` or One-Shot again. Writing it does not change one round's task set boundary.
- One-Shot is neither spreading out subsequent sequential tasks at once, nor skipping verification and write-back.
- Stopping is allowed only when the specified scope is complete, there is no technically feasible next step, or external limits make subsequent steps objectively unexecutable.
- When recomputing, the latest `tasks.md` check states and the actual code state must be the basis.

## Good Example

- This example is good because right after `T001` it checks the box and recomputes the next one.

```md
The agent completes and verifies `T001`, writes back `[X]`.
Then it re-reads `tasks.md`, determines `T002` is unlocked, and converges the next round's task set.
```

## Bad Example

- This example is bad because it turns One-Shot into one big spread-out, or into do-1-and-stop.

```md
After completing `T001` the agent directly reports "this session completed the next task", without recomputing.
Or it dispatches T005–T230 at once to two subagents and checks everything at the end.
```

# Rule 3 - A One-Shot round's task set is exactly 1; with a Parallel Hint it collects the whole `[P]` batch

- Level: `MUST`
- Each One-Shot round must select exactly 1 unlocked task as this round's task set; do not spread out the same phase or multiple sequential steps at once.
- If the current phase has a `Parallel Hint`, this round's task set must be the `[P]` batch listed by the Hint, not just the first unlocked task.
- Without a `Parallel Hint`, expansion into a same-round parallel batch is allowed only when multiple tasks explicitly carry `[P]`, their prerequisites are consistent, and `parallel-execution-and-file-conflict-criteria` permits it.
- Tasks not marked `[P]` must run sequentially even if all are unlocked.
- The detailed prohibitions on skipping steps follow `strict-no-step-skipping-criteria`.

## Good Example

- This example is good because with a Hint it collects the whole batch, while Feature remains single-task.

```md
Phase 3's Parallel Hint lists T008–T014.
This round's task set = {T008–T014}, not just T008.
T016 [BDD-GREEN] is not marked [P]; the next round does only T016.
```

## Bad Example

- This example is bad because it ignores the Hint, or bundles the entire Setup at once.

```md
Seeing Phase 3 has 7 [P]s, the agent still does only T008.
Or seeing Phase 1 Setup still has 3 tasks not marked [P], it does them all in one go.
```
