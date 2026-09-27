# Rule 1 - Each `red` slice must first explicitly declare its goal and focused test entry

- Level: `MUST`
- Before starting any `red` work, the single slice to drive this round and the narrowest test entry to run must be specified first, e.g. a single scenario, a single `Rule`, a single feature file, or an equivalent focused rerun strategy.
- If the current project cannot do single-slice reruns, the minimal acceptable scope should be chosen instead of running the whole suite.
- Test modifications without a clearly specified target slice do not count as valid `red`.

## Good Example

- This example is good because it aligns this round's goal with the narrowest execution entry first.

```md
This round's goal:
- Slice: the player can press submit after selecting three numbers

Focused test:
- `npm test -- --name "the player can press submit after selecting three numbers"`
```

## Bad Example

- This example is bad because it does not clearly specify which behavior should fail first.

```md
This round's goal:
- Do battle-page-related stuff first

Focused test:
- Run all tests once and see
```

# Rule 2 - `red` must first observe a reasonable failure corresponding to the current slice

- Level: `MUST`
- Implementing a new slice must first make the corresponding test fail in a reasonable way, confirming it is really driving this round's requirement, before entering `green`.
- Even if a skeleton already exists, the focused test must at least be rerun to confirm the current failure relates to this slice; do not patch implementation on gut feeling.
- Do not implement the entire feature without ever observing a failure and then claim you finished `red`.

## Good Example

- This example is good because it first confirms — through the failure signal — that what is hit is exactly this round's behavior.

```md
1. Add the corresponding step skeleton or assertion
2. Run the focused test
3. See an undefined step, missing assertion, or behavior-mismatch failure
4. Stay at red, ready to hand off to `green`
```

## Bad Example

- This example is bad because it treats `red` as a post-hoc verification instead of the driving entry.

```md
1. Write the entire submit flow first
2. Run tests once at the end
3. If it fails, say you were actually doing `red`
```

# Rule 3 - `red` only establishes failure signals; it does not implement product behavior ahead of time

- Level: `MUST`
- In the `red` phase, test skeletons, step definitions, fixtures, assertion hook-ups, and minimally necessary compile paths may be created or adjusted, but product behavior must not be filled in early to the point of turning green.
- If minimal boilerplate code must be added to make the test executable, its purpose can only be to expose a more real failure; do not sneak in business logic.
- The completion condition of `red` is "the failure signal is clear", not "the feature is almost done".

## Good Example

- This example is good because it does just enough to make the failure land on the current behavior.

```md
What this round's `red` adds:
- New step skeleton
- Wire up the existing fixture
- Get the test to an assertion failure

What this round does NOT do:
- Does not implement "switch turns after submission"
- Does not implement the real submission flow
```

## Bad Example

- This example is bad because it has already started absorbing `green`'s work.

```md
What this round's `red` adds:
- Implement the submit API, turn switching, and button disabling logic up front
- Only the last assertion is not passing yet
```

# Rule 4 - When doing multiple `red`s consecutively within the same scope, red lights must also be established one slice at a time

- Level: `SHOULD`
- If the user-specified scope allows sequentially advancing multiple slices within the same invocation, the previous slice should first form a stable red light before moving to the next slice.
- Do not bulk-add test skeletons for multiple unfinished slices at once, causing failure sources to interfere with each other.
- If the first slice's failure is still mixed, unattributable, or masked by a higher-level error, stop and fix the failure signal quality first instead of laying down the next `red`.

## Good Example

- This example is good because it keeps multi-slice `red`s in an attributable sequence.

```md
Order:
1. First make the "can press submit" slice a stable red light
2. Confirm the failure source is clear
3. Only then move to the "cannot submit again in the same turn after submission" slice's red light
```

## Bad Example

- This example is bad because it lays down too many skeletons at once, making every failure unidentifiable.

```md
Added at once:
- Three new scenarios
- Six undefined steps
- Two mutually overwriting assertions

Result:
- Not knowing which failure corresponds to which slice
```

# Rule 5 - Failure signals of non-Gherkin witness pins must be attributable and independent

- Level: `MUST`
- When unit tests or fault-injection witness pins (`[WITNESS]`) are created for atomic effect claims that cannot be observed externally via Gherkin, this RuleFile's "effective failure signal" principles apply equally:
  1. **Narrowest execution entry**: the single test case or function of that witness test must be specified; do not substitute the whole test suite with a blanket run.
  2. **Failure signal reality & attribution**: a witness pin's failure must directly stem from the target guarantee mechanism being broken (e.g., asserted data corruption or a specific exception), and must never be masked by syntax errors, missing packages, global timeouts, or unrelated crashes.
  3. **Two-Authority Split declaration**:
     - This RuleFile governs failure signal reality, narrowest entry, and failure attribution criteria (Signal-reality & Attribution).
     - Concrete task binding, discriminating mutation verification, full-green restore re-verification, and degraded-terminal handling are governed by `axb-implement`'s `rules/definition-of-done-verification-and-writeback-criteria.md`.

## Good Example

- This example is good because the unit test witness pin has the narrowest entry, and the failure signal is clearly attributed to a missing fsync.

```md
Focused test: `go test -run TestHistory_FsyncDurability ./internal/infrastructure/history`
Mutation break: remove `f.Sync()`.
Failure signal: `Expected file to be synced to disk before rename, but sync count was 0`.
Attribution is clear with no other masking errors.
```

## Bad Example

- This example is bad because the test fails on an import error but is mistaken for a witness red light.

```md
Mutation break: arbitrarily change the code.
Failure signal: `syntax error: unexpected newline, expecting comma or }`.
This is a syntax compile failure, not a behavioral falsification of the guarantee mechanism; it is not attributable.
```

