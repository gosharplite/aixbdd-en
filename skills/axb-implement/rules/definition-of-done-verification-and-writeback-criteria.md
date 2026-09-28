# Rule 1 - A task counts as done only after both implementation and its verification are complete

- Level: `MUST`
- A single task's completion conditions include at least: the required changes are implemented, the corresponding files are written, and the verification directly related to that task is complete.
- The verification method should converge by task type, e.g. targeted tests, lint, type checks, manual flow verification, contract comparison, or startup checks.
- "Code is written but not yet verified" must not be treated as done.

## Good Example

- This example is good because it only deems the task done after both implementation and verification are complete.

```md
After the agent finishes modifying `roomStore.js`, it runs the corresponding tests and startup checks.
Only after confirming the verification passes does it treat the task as done.
```

## Bad Example

- This example is bad because it only completed the code change without any completion evidence.

```md
After writing `gameHandler.js` the agent directly says "this task is done", but ran no tests, lint, or contract comparison.
```

# Rule 2 - After a task is done, `[X]` must be written back immediately; checking boxes early is forbidden

- Level: `MUST`
- Only when the task's implementation and verification are both complete may the corresponding task be rewritten from `- [ ]` to `- [X]`.
- Do not pre-check for tracking convenience, and do not also mark other tasks in the same batch that are not yet verified as done.
- When writing back, modify only the actually-completed tasks, leaving other unfinished tasks' states unchanged.

## Good Example

- This example is good because it updates only a single task's state after the completion conditions hold.

```md
The agent completes and verifies `T014`.
It only changes `T014` to `[X]`, while `T015` and `T016` remain `[ ]`.
```

## Bad Example

- This example is bad because it checks the box early, costing `tasks.md` its credibility as the execution control plane.

```md
As soon as the agent starts modifying `T014` it changes it to `[X]`, thinking it will verify everything at the end.
```

# Rule 3 - The completion report should leave traceable verification evidence and next-step state

- Level: `SHOULD`
- Each round's completion report should state: which tasks were done, what verifications were run, whether repo hygiene was reinforced, what the next unlocked task is or why things stopped.
- The report should focus on execution state and key decisions; it does not need to be a verbose changelog of every detail.

## Good Example

- This example is good because it lets the user quickly know the completion surface, evidence, and the next One-Shot item.

```md
Completed `T001`, `T002`.
Verification: frontend/backend workspace install and startup script checks passed.
Reinforced `.gitignore`.
Next unlocked task: `T003`.
```

## Bad Example

- This example is bad because it only says things are done, leaving neither verification nor the next One-Shot item.

```md
Did a lot of things today; it should be almost usable.
```

# Rule 4 - Setup, Foundational, Phase 3, and Feature use different completion conditions

- Level: `MUST`
- Setup's completion condition: the packages and configuration written in that rule are in place, and a smoke-test proves connectivity. Do not require this round's Feature to be all green, and do not write message-sending semantics into Setup.
- Foundational's completion condition: the implementation code, test-shared components, entry points, fixtures, helpers, or touchpoint skeletons "only-do" items of that rule exist, and nothing crosses the "not-do". Do not require DSL semantics to be aligned, and do not require product code to be green.
- Phase 3's `[BDD-ALIGN]` / `[BDD-REMOVE]` / `[BDD-RED]` completion condition: that sentence's test semantics are aligned with the `dsl.md` row's `StepDef Implementation Semantics` and can be run; failures may only be assertions or product behavior, never undefined steps. Do not require product code to be green.
- Phase 3 review's completion condition: running all of this round's Feature phases' `Test Scope` yields no undefined steps; the review subagent reports no issues.
- `[BDD-GREEN]`'s completion condition: that phase's `Test Scope` is all green.
- `[CODE-REMOVE]` / `[REGRESSION]`'s completion condition: the obsolete product behavior is removed, the `Test Scope` passes, and the old behavior is no longer protected by tests.
- `[WITNESS]`'s completion condition is in Rule 5: it must prove that a discriminating mutation triggers an attributably-clear red light, and that tests turn green again after revert; or thoroughly demote and remove the prose from truth surfaces and record it on the project decision surface.
- Do not leave tests that still protect old truth in the code and write back `[X]` just because newly-added tests pass.

## Good Example

- This example is good because Setup stops at connectivity, Phase 3 stops at a runnable red light, and only Green requires all green.

```md
Before T003 is done: `websockets.connect` can connect to the FastAPI `/ws`.
Before T004 is done: `chat_helpers.py` has function shells, no per-sentence stepdefs.
Before T012 [BDD-RED] is done: the empty-submit stepdef is written and reaches an assertion failure.
Before T015 review is done: all three of this round's Test Scopes have no undefined steps.
Before T016 [BDD-GREEN] is done: `single-player-waiting-and-empty-message-rejection.feature` is all green.
```

## Bad Example

- This example is bad because it demands focused tests be all green at Phase 3 ALIGN time.

```md
T008 [BDD-ALIGN] has no product code yet, tests still red, the agent refuses to write back, and everything deadlocks.
```

# Rule 5 - [WITNESS] tasks' Definition of Done (DoD) must prove discriminating falsification and failure attribution

- Level: `MUST`
- `[WITNESS]` tasks are responsible for witnessing normative items (NFR / SC / EC / internal invariants) that cannot be observed externally via Gherkin. Their completion conditions (DoD) must strictly satisfy the following three gates:
  1. **Discriminating Mutation**:
     - A single-point mutation break must be applied to the guaranteed mechanism being witnessed (e.g.: when claiming fsync durability, comment out `f.Sync()`; when claiming atomic replacement, change it to in-place overwrite); the mutation must turn the tests within `Test Scope` to failure (red).
     - If tests remain green after the mutation, the test is non-discriminating, has no protective power, and must not be counted as done. Each atomic effect claim must have at least one discriminating mutation.
  2. **Attributed Failure**:
     - The cause of the test failure must be directly and clearly attributed to the guarantee mechanism broken by the mutation (a matching expected failure shape / assertion failure), never masked by an unrelated syntax error, missing module, environment outage, or unrelated panic.
  3. **Revert-and-re-green**:
     - After reverting the mutation break back to normal implementation code, re-run `Test Scope`; the tests must all turn green again.
- **Terminal Outcomes & Demotion**:
  - Only those who pass all three gates above may write back `[X]`.
  - If during implementation it is found that the claim technically cannot have an automated witness established in the current environment: **pretending to pass or checking the box early is strictly forbidden**.
  - The only legitimate alternative terminal path is "**Demote**":
    1. Thoroughly delete the prose of that guarantee from all truth surfaces this round (`specs/truth/techstack.md`, `dsl.md` preambles, DBML notes, etc.); no unwitnessed affirmative sentence may remain;
    2. Report to the human decision maker, and record it as a decision or `accepted-unwitnessed` on the project's declared decision surface (e.g. the project ADR);
    3. Only after all truth prose is removed and the decision surface record is complete may that task be marked as demote-closed and `[X]` written back.
- Those who have neither completed the discriminating witness nor completed the demotion procedure are strictly forbidden from writing back `[X]`.

## Good Example

- This example is good because it completes the full path: discriminating mutation, attribution confirmation, and revert-and-re-green.

```md
T015 [WITNESS] rollback operation is atomic and a crash leaves no stray temp files
1. Implement unit test rollback_test.go::TestRollback_AtomicCrashSafety
2. Perform the discriminating mutation: change tempfile + rename to a direct truncate write into the original file
3. Run the test: TestRollback_AtomicCrashSafety fails, reporting "old history file corrupted", with clear failure attribution
4. Revert the implementation and rerun: the test turns green again
5. Confirm discriminating power is present, write back T015 as [X]
```

## Bad Example

- This example is bad because the test is green from start to finish — even with the key mechanism removed it stays green — yet the box is checked directly.

```md
T015 [WITNESS] rollback operation has fsync disk-persist durability
The agent wrote a test that only calls Rollback(), saw exit 0 all green, and checked the box.
In reality, commenting out f.Sync() in the code still leaves the test all green — that test cannot witness at all whether fsync is called.
```


