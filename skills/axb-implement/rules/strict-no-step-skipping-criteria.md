# Rule 1 - A One-Shot round's task set is exactly one unlocked task

- Level: `MUST`
- Each One-Shot round's executed task set must contain exactly 1 unlocked and unfinished task.
- If the current phase has a `Parallel Hint`, this round's task set becomes the `[P]` batch listed by the Hint; this does not count as skipping steps.
- Sequential tasks not marked `[P]` must not be bundled into one round of implementation even if all are unlocked.
- don't stop until deliver / One-Shot is not permission to skip steps. One-Shot only means: after finishing the current task set's verification and write-back, recompute the next task — it does not mean bundling sequential tasks into one round.

## Good Example

- This example is good because Phase 3 follows the Hint batch while Feature remains single-task.

```md
Phase 3: this round's task set = {T008–T014}.
Phase 4: this round's task set = {T016 [BDD-GREEN]}.
```

## Bad Example

- This example is bad because it bundles Phase 3 and Green into one go.

```md
The agent decides to do all of T008–T016 in one round this time and check all boxes at the end.
```

# Rule 2 - The following behaviors are all treated as skipping steps and are strictly forbidden

- Level: `MUST`
- When executing `/axb-implement`, the following behaviors are all treated as skipping steps and must be stopped immediately in favor of step-by-step execution:
  1. **Skipping prerequisites**: jumping over tasks that are still unfinished or still blocked by `Dependencies` / phase to do later tasks directly.
  2. **Merging sequential steps**: bundling multiple unlocked tasks that are neither marked `[P]` nor covered by a `Parallel Hint` into one round of implementation or one batch of write-backs.
  3. **Writing product code in Phase 3**: writing product behavior during ALIGN / REMOVE / RED / review.
  4. **Going Green before review passes**: starting Feature Green while Phase 3 review still has issues or has not been written back yet.
  5. **Crossing BDD steps**: completing `[BDD-GREEN]` and `[BDD-REFACTOR]` in the same round; or letting `/axb-bdd` continue swallowing other steps / subsequent Feature phases beyond the current task.
  6. **Pre-doing later deliveries**: while executing the current task set, opportunistically writing tests, implementation, refactoring, or integration content that only later tasks should deliver.
  7. **Continuing without the gate**: starting the next task set before the current one's verification is complete or `[X]` has been written back.
  8. **Early / batch checking**: changing to `[X]` before verification completes, or checking multiple tasks together before each is verified.
  9. **Out-of-bounds responsibility swallowing**: in Setup / Foundational / a single Feature task, sneaking in later story features or other tasks' completion conditions.
- Triggering any of the above "to be faster" is still a violation. Even if the user wrote `don't stop until deliver` or One-Shot, it is still a violation.

## Good Example

- This example is good because Phase 3 stops at the test layer and review.

```md
T008–T014 finished the stepdefs, T015 review passed.
Only after write-back does the agent recompute T016 [BDD-GREEN]; it does not write the message-sending API in Phase 3.
```

## Bad Example

- This example is bad because it compresses the test layer and Green into one round on efficiency grounds.

```md
RED is simple anyway, so let's finish the Green implementation along the way.
```

# Rule 3 - Feature's `[BDD-GREEN]` / `[BDD-REFACTOR]` must delegate to /axb-bdd single-step

- Level: `MUST`
- If the current task title contains `[BDD-GREEN]` or `[BDD-REFACTOR]`, this round may only delegate `/axb-bdd` to execute that single `requested step`, taking that phase's `Test Scope` as the scope.
- `/axb-bdd` must not be allowed to execute Green and Refactor consecutively in the same round, or advance other Feature phases.
- `[BDD-GREEN]` does only the minimal implementation to turn `Test Scope` green.
- `[BDD-REFACTOR]` does only behavior-preserving cleanup under a green light.
- Phase 3's `[BDD-ALIGN]`, `[BDD-REMOVE]`, `[BDD-RED]` do not follow this rule and do not delegate to `/axb-bdd`.

## Good Example

- This example is good because `/axb-bdd` is locked to the current Green and `Test Scope`.

```md
Current task: `T016 [BDD-GREEN]`
Delegate `/axb-bdd`: requested step=green, Test Scope=`single-player-waiting-and-empty-message-rejection.feature`.
This round ends at the green light and the `T016` write-back.
```

## Bad Example

- This example is bad because it turns one GREEN task into a whole round of BDD.

```md
The current task is `[BDD-GREEN]`.
The agent lets `/axb-bdd` also run Phase 3's RED and the subsequent REFACTOR in one go.
```

# Rule 4 - Deliverables outside the current task set boundary must never be pre-done

- Level: `MUST`
- This round may only modify and verify the files and content necessary for the "current task set" completion conditions.
- Do not pre-implement behaviors, test cases, abstraction layers, or integration wiring that only later tasks need, just because a shared module is convenient.
- A Setup task does only the packages, configuration, technical environment, and smoke-tests for this round's newly added technology; it must not write DSL semantics or product behavior.
- A Foundational task only establishes the implementation code, test-shared components, entry points, fixtures, helpers, and touchpoint skeletons for later work, stopping at that rule's "only-do / not-do"; it must not sneak in a complete Feature's functionality, nor write Phase 3's ALIGN / REMOVE / RED semantics.

## Good Example

- This example is good because the shared skeleton stays within the current task boundary.

```md
Current task: `T004` establishes the chat test-shared helper entry and skeleton.
The agent only confirms the touchpoints and function shells; it writes neither per-sentence stepdefs nor the message-sending API.
```

## Bad Example

- This example is bad because it pre-does later features under the Foundational banner.

```md
While doing `T004`, also finish the empty-rejection API and all of Phase 3's stepdefs.
```

# Rule 5 - Verify and write back first; only then recompute the next task set

- Level: `MUST`
- A single task (or every task in a `Parallel Hint` batch) must first complete its corresponding verification, then write back that task's `[X]`.
- Only after the current task set's write-back is complete may the task-selection flow be re-entered.
- A legitimate parallel batch must still be verified individually before individual write-backs; do not verify just one and check the whole batch.

## Good Example

- This example is good because the One-Shot gate is complete.

```md
1. T008–T014 each complete their test layer
2. T015 review passes
3. Write back T008–T015
4. Re-read `tasks.md`, then start T016
```

## Bad Example

- This example is bad because it writes Green while claiming Phase 3 is probably fine.

```md
The agent writes `T016` while saying it will catch up on T015's review later.
```
