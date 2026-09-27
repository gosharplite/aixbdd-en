# Rule 1 - `refactor` may only proceed under green-light protection

- Level: `MUST`
- Before entering `refactor`, the current slice or the slices to be tidied this round must already be protected by focused tests or a minimal representative test set.
- If there are still unclear red lights, intermittent failures, or test noise unrelated to the current refactor, go back to `red` or `green` first; do not force `refactor`.
- The precondition of `refactor` is "the behavior is established", not "the feature is almost done".

## Good Example

- This example is good because it first confirms a green light exists, then tidies the structure.

```md
Precondition:
- `--name "cannot submit again in the same turn after submission"` is a stable green light

Processing:
- Start extracting shared assertion helpers
- Rerun representative tests after each tidy-up
```

## Bad Example

- This example is bad because it starts moving structure before the behavior is solid.

```md
Precondition:
- Tests still have undefined steps
- The submit flow is occasionally red

Processing:
- Rename a bunch of helpers and fixtures first
```

# Rule 2 - `refactor` should prioritize cleaning up duplicate steps, type conversion boundaries, and supporting-layer naming

- Level: `SHOULD`
- If duplicate step wording, extractable parameter / data table types, hardcoded test data, unfocused naming, or broken thin glue already appear within the current scope, they should be prioritized for cleanup in the `refactor` phase.
- The goal of refactoring is to make subsequent slices in the same scope easier to advance, not to pursue large architectural tidying unrelated to this round's behavior.
- If a tidy-up only improves local readability but amplifies risk and the change surface, handle it conservatively.

## Good Example

- This example is good because it first tidies the duplication and unfocused boundaries just verified by this round's behavior.

```md
This round's refactor:
- Converge three similar submit steps into the same wording
- Extract a shared `GuessSelection` parameter type
- Rename `tmpBattleAssert` back to a domain name
```

## Bad Example

- This example is bad because it jumps into a large refactor with a very weak relation to the current scope.

```md
This round's refactor:
- While at it, rewrite the entire test framework initialization flow
- While at it, change all support directory naming rules
```

# Rule 3 - `refactor` must not rewrite approved business intent, nor modify upstream spec

- Level: `MUST`
- `refactor` may only tidy step definitions, helpers, fixtures, assertion helpers, product code structure, and naming; it must not quietly change approved business behavior.
- If during refactoring it is found that the current design actually needs to change `feature file` boundaries, `dsl.md` vocabulary, or acceptance results, stop and hand back upstream rather than redefining the spec locally.
- Refactoring improves how things land; it is not rewriting requirements.

## Good Example

- This example is good because it only changes the landing structure, not the behavior contract.

```md
Approved behavior:
- The player cannot submit again in the same turn after submission

Refactor handling:
- Extract a shared `turnStateHelper`
- Do not modify feature wording or acceptance results
```

## Bad Example

- This example is bad because it changes business outcomes under the name of refactoring.

```md
Approved behavior:
- The player cannot submit again in the same turn after submission

Refactor handling:
- Thinks redirecting to the price page is more reasonable
- Directly changes the assertion and flow behavior
```

# Rule 4 - If refactoring needs to step outside the specified scope, stop and report; do not expand opportunistically

- Level: `MUST`
- If `refactor` can be completed by tidying only within the current `feature file` or its clearly identified block, it must be limited to this round's scope.
- If refactoring requires synchronously changing multiple `feature files`, interface logic, or upstream DSL not authorized this round, stop and report the reason so the user can re-decide the scope.
- Do not turn refactor into unbounded cross-module, cross-interface tidying just because "it is most convenient right now".

## Good Example

- This example is good because it treats the scope guard as a hard limit of refactor.

```md
Observations:
- Tidying only the current frontend helper and assertion naming would eliminate duplication

Processing:
- Complete it within this frontend feature scope
```

## Bad Example

- This example is bad because it expands local tidying into unbounded systemic overhaul.

```md
Observations:
- Currently only refactoring a frontend feature

Processing:
- While at it, synchronously change backend steps, shared DSL, and acceptance wording
```
