# Rule 1 - Before implementing, first inventory the project's existing test entries and BDD touchpoints

- Level: `MUST`
- Before `/axb-bdd` enters `red`, `green`, or `refactor`, it must first confirm the project's existing `feature` directories, step definitions, support files, hooks, fixtures, product code touchpoints, and test launch methods.
- If the project already has established directory structures, naming conventions, or runners, prefer reusing them; do not start a parallel structure without reason.
- The purpose of the inventory is to land this round's scope on the real entries of existing tests and product code, rather than guessing from the spec layer where files should go.

## Good Example

- This example is good because it understands the existing structure first, then decides where to add or modify in this round.

```md
Inventory result:
- `frontend/features/steps/` already exists
- The existing runner supports `--name` focused rerun
- Shared helpers are in `frontend/features/steps/shared/`

Decision:
- New steps and helpers both reuse the existing tree
- Do not open a parallel `bdd/steps/` directory
```

## Bad Example

- This example is bad because it builds another test topology in the repo without checking the current state.

```md
Without inventorying the current state, directly adding:
- `bdd/features/`
- `bdd/step-definitions/`
- `bdd/support/`
```

# Rule 2 - The narrowest and repeatable test entry must be selected

- Level: `MUST`
- Each round must first find the currently available narrowest rerun strategy in the project, e.g. a single scenario name, a single `Rule`, a single feature file, a single spec file, or an equivalent means.
- If the test entry takes over modular truth, the necessary levels of the focused runner follow `modular-truth-on-demand-symlink-criteria.md`; this Rule is only responsible for selecting this round's narrowest scope from the entries the project already provides.
- If the runner itself cannot rerun precisely, the currently chosen minimal acceptable scope and the reason must be explicitly recorded.
- "Running the whole suite first to be safe" must not be the default practice.

## Good Example

- This example is good because it first confirms how narrow it can go, then binds that entry to this round's slice.

```md
Rerun strategy:
- Prefer `--name "player submits a single shot successfully"`
- If name filtering is unavailable, fall back to a single feature file

This round's test entry:
- `npm test -- --name "player submits a single shot successfully"`
```

## Bad Example

- This example is bad because it directly accepts a high-cost, low-signal feedback loop.

```md
Rerun strategy:
- Run all frontend, backend, and acceptance tests every time
```

# Rule 3 - Given preconditions should prefer the fastest and most stable existing technical entry

- Level: `SHOULD`
- If the project already has API fixtures, factories, seed helpers, test data builders, repository helpers, or test-only services, prefer these entries to establish Given state rather than defaulting to the full UI.
- Only when the `feature file` and `dsl.md` explicitly require accepting Given at the UI layer, or existing technical entries are insufficient to express the requirement, should slower end-to-end flows be considered for Given.
- This judgment directly affects the speed and stability of `/axb-bdd` sequentially advancing multiple slices within the scope.

## Good Example

- This example is good because it leaves slow interactions to the real Act and hands Given to a more stable entry.

```md
Given state setup:
- Use `roomFixture.createReadyMatch()` to establish the match state

When behavior:
- Execute "submit three guesses" via UI or API
```

## Bad Example

- This example is bad because even with a fast state-setup entry available, it still takes every precondition through the full flow.

```md
Given state setup:
- Open the home page first
- Create a room
- Enter the room
- Wait for matchmaking
- Then gradually adjust data into a testable state
```

# Rule 4 - Before adding a new abstraction, first confirm whether existing helpers, fixtures, and naming are sufficient

- Level: `SHOULD`
- Before implementation, first confirm whether existing page objects, service helpers, fixtures, parameter types, and assertion helpers can already carry this round's slice.
- If an existing abstraction can be reused with only minor extension, prefer extending it rather than inventing new terminology or duplicating layers.
- Only when the existing abstraction's responsibility boundary is clearly unsuitable should a new supporting layer be added.

## Good Example

- This example is good because it extends the existing supporting layer first instead of building a parallel one.

```md
Status:
- `guessFixture.createRoundState()` already exists
- `battlePage.submitGuess(values)` already exists

Decision:
- Extend the assertion helper
- Do not add another `guessDriver2`
```

## Bad Example

- This example is bad because it duplicates capabilities without evaluating existing resources.

```md
Status:
- `battlePage.submitGuess(values)` already exists

Decision:
- Add `turnSubmissionPortal`
- Add `guessWorkflowManager`
- Add `roundActionDriver`
```
