# Rule 1 - When the current phase has a Parallel Hint, the batch of subagents must be dispatched at once (except for same-file conflicts)

- Level: `MUST`
- If the `tasks.md` current phase contains a `Parallel Hint`, this round's task set is the `[P]` tasks listed by the Hint — not just the first unlocked task.
- **Independent target files → fully parallel**: if the target files written by that batch of tasks are mutually independent (Zero Shared Edits principle), dispatch one independent subagent per listed `[P]` task and launch the whole batch in parallel at once.
- **Same-file conflicts → schedule by file**: if multiple `[P]` tasks write to the same target file, to avoid Lost Update and write races the orchestrator must schedule sequentially by target file (same-file tasks run one after another, ensuring the earlier write is flushed to disk before the later subagent starts reading), or merge the same-file tasks to be handled sequentially by a single subagent; multiple subagents must never concurrently write the same physical file in an unlocked state.
- The review task starts only after the whole batch returns; it must not run in parallel with the batch.

## Good Example

- This example is good because independent files get the whole batch at once, while same-file tasks are scheduled sequentially by file.

```md
Parallel Hint: T008–T014 each get one independent subagent; T015 reviews only after all return.
T008–T014's touchpoints are independent files (e.g. each writes its own `steps/step_*.go`): dispatch T008–T014 in parallel at once this round.
If T008 and T009 both write the same `operations_and_assertions.py`: the orchestrator dispatches T008 first, and T009 only after T008 is flushed to disk.
```

## Bad Example

- This example is bad because it ignores the Hint and stays fully sequential despite independent files, or blindly parallelizes same-file writes causing overwrites.

```md
T008–T014 write different files, yet the agent dispatches only one subagent for T008 and leaves T009–T014 for later sequential runs.
Or: T008 and T009 write the same file, and the agent dispatches two subagents in parallel to change that file, causing a Lost Update.
```

# Rule 2 - A subagent's prompt points only to that task in tasks.md

- Level: `MUST`
- Each subagent's prompt must contain: which plan's `tasks.md` to read, which task number, and that its responsibility is to develop that task.
- Conflict handling is written into the prompt: for same-file sequential tasks, read the latest flushed content first at execution time, then layer on this task's DSL changes.
- Do not paste a full prompt into `tasks.md` again. Do not rewrite DSL / Why / Read in the prompt; those already live in that task and the Phase `Shared Must Read`.

## Good Example

- This example is good because the prompt points at the task itself.

```md
Please read T008 in `specs/plans/004-room-chat-adjustment/tasks.md`.
Your responsibility is to develop this task.
If the target file already exists or has been changed by a preceding task, read the latest content first and add this DSL row's changes yourself.
```

## Bad Example

- This example is bad because it writes its own semantics instead of having the subagent read the task.

```md
Please change the send-message stepdef to verify the store. Do not look at tasks.md.
```

# Rule 3 - Write responsibility stays with subagents; uncoordinated same-file parallel overwrites are forbidden; review does not merge

- Level: `MUST`
- Multiple parallel subagents must not write the same physical file at the same time (this is the root cause of Lost Update).
- When two Phase 3 tasks write the same file, the orchestrator must schedule them sequentially: after the first subagent completes and flushes to disk, the later subagent first reads the latest file and then adds its own DSL row's stepdef.
- The review task only performs quality and coverage checks (confirming no undefined steps and that tests run properly); it does not merge diffs, nor write stepdefs on others' behalf.

## Good Example

- This example is good because writes are flushed to disk sequentially by subagents, and review only checks.

```md
T008 and T009 both write `operations_and_assertions.py`.
The orchestrator first dispatches T008 to complete and flush; then T009's subagent reads the latest content, adds its own Then stepdef, and flushes.
T015 only reviews the result, confirming no undefined steps.
```

## Bad Example

- This example is bad because it lets multiple subagents change the same file at once causing overwrites, or dumps the merge responsibility on review.

```md
T008 and T009 write `operations_and_assertions.py` in parallel at once, and T009 overwrites T008's code.
Or T008–T011 only submit patches and wait for T015 to merge.
```

# Rule 4 - If review has issues, fix them and review again until there are none

- Level: `MUST`
- Phase 3's review task must launch a subagent to review.
- Running all of this round's Feature phases' `Test Scope` must no longer produce undefined steps; failures may only be assertions or product behavior.
- Whenever there are issues, fix them, then launch the subagent review again; repeat until the subagent reports no problems at all.
- Before review passes, Feature-phase Green must not be unlocked.

## Good Example

- This example is good because it forms a loop gate.

```md
T015 review reports T012's stepdef did not read `權威狀態落地`.
After fixing, review again. Only with zero issues the second time is T016 [BDD-GREEN] unlocked.
```

## Bad Example

- This example is bad because it proceeds to Green despite issues in one review.

```md
T015 lists 3 issues.
The agent says it will fix them during Green later and starts T016 directly.
```
