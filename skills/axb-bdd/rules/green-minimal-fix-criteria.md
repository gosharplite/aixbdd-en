# Rule 1 - `green` must start from the current `red` failure; the failure signal must not be skipped

- Level: `MUST`
- The `green` phase may only patch code based on the failure currently observed by the focused test; entering `green` without a `red` signal is not allowed.
- If the current failure is unrelated to this round's slice, too far upstream, or masked by other errors, go back and fix `red` first instead of forcing code in.
- The minimal patch of `green` must correspond to the current failure, not to an imagined complete feature.

## Good Example

- This example is good because it makes the patch and the current failure a one-to-one correspondence.

```md
Current failure:
- The submit button stays disabled even after three numbers are selected

This round's patch:
- Only patch the button enable condition
- Do not do turn switching, scoring, or settlement yet
```

## Bad Example

- This example is bad because it does not really start from the current failure.

```md
Current failure:
- undefined step

This round's patch:
- Directly implement the entire submit flow, scoring, and turn switching
```

# Rule 2 - Each patch only resolves the current slice's failure; do not sneak in unselected behaviors

- Level: `MUST`
- The code needed by the current slice should only cover the minimal behavior corresponding to the current failure.
- Do not write in extra paths, roles, flags, or branches all at once just because the next slice will also need some capability.
- If the next slice will force a design adjustment of the current one, wait until the next round and drive it with a new `red` or new `green` signal.

## Good Example

- This example is good because it only patches the minimal condition needed by the current slice.

```md
This round's slice:
- The player can press submit after selecting three numbers

This round's patch:
- Only patch "enable submit when all three numbers are present"
- Do not add "lock after submission" or "disable during the opponent's turn" yet
```

## Bad Example

- This example is bad because it writes in the capabilities of multiple future slices at once.

```md
This round's slice:
- The player can press submit after selecting three numbers

This round's patch:
- Add enable / disable / lock / opponent turn / timeout / reconnect branches all at once
```

# Rule 3 - Step definitions must stay a thin layer; reuse should sink to helpers, fixtures, and domain abstractions

- Level: `MUST`
- A step definition should only match the step, parse parameters, enter assertions, or delegate to helpers; do not pile up bulk data setup, cross-page flows, and multiple assertions in a single step.
- If multiple steps share underlying behavior, extract helper methods, page objects, services, fixtures, or parameter / data table types instead of having step definitions call each other.
- Hard-splitting step definitions by feature filename is a high-risk signal; prioritize organizing by domain concept.

## Good Example

- This example is good because the step is thin and the reuse points stay at the bottom layer.

```js
When("player submits guess {string}", async function (guess) {
  await battlePage.submitGuess(guess);
});
```

## Bad Example

- This example is bad because the step definition itself becomes a complete test script.

```js
When("player submits guess", async function () {
  await openBattlePage();
  await clickCell(1);
  await clickCell(2);
  await clickCell(3);
  await clickSubmit();
  await expectBanner("submitted");
  await expectTurnSwitch();
});
```

# Rule 4 - A single invocation may consecutively turn multiple slices green within the scope, but each slice must have its own green light

- Level: `SHOULD`
- If the user-specified scope allows sequentially advancing multiple slices within the same invocation, the previous slice must obtain its own green light before switching to the next slice.
- Do not let multiple slices share one vague "mostly passing" signal.
- If a slice is green but leaves obvious duplicate steps, hardcoded data, or temporary code, do a minimal tidy-up first, then decide whether to continue to the next slice in the same invocation.

## Good Example

- This example is good because each green light corresponds to a single completed slice.

```md
Order:
1. `--name "the player can press submit after selecting three numbers"` goes green first
2. Extract shared helpers
3. Only then switch to `--name "cannot submit again in the same turn after submission"`
```

## Bad Example

- This example is bad because it declares multiple unstable behaviors done at once.

```md
Status:
- Several related tests seem to mostly pass
- But it is unclear which slice is actually green

Decision:
- Move straight on to the next batch of requirements
```
