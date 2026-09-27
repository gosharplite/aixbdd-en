# Rule 1 - A single invocation may advance multiple slices, but only one slice may be handled at a time

- Level: `MUST`
- Although `/axb-bdd` may sequentially advance multiple slices within a user-specified single interface `feature file` or its clearly identified block, at any moment only one current slice may be locked on.
- Do not bundle multiple slices into one round of simultaneous coding and verification just because they seem to share the same batch of steps or pages.
- Only when the current slice has met that entry's completion conditions may the next slice be selected.

## Good Example

- This example is good because it allows continuous progress within the same scope, but each time only one slice drives the current change.

```md
This round's scope:
- `features/frontend/three-guess/battle-page-three-guess-selection-and-single-shot.feature`

Advancement order:
1. First handle the "player has selected three numbers" slice
2. After that slice completes this round's `green`
3. Only then switch to the "button disabled after submission" slice
```

## Bad Example

- This example is bad because it mixes multiple independent behaviors into one round, losing local feedback.

```md
This round handles:
- Patch all five slices under three Rules at once
- Run tests together at the end
```

# Rule 2 - The next slice must prioritize minimal and independent feedback

- Level: `MUST`
- When selecting the next slice within the specified scope, prioritize which behavior can form independent red-green feedback with the smallest increment, not which one can conveniently bring along the most capability at once.
- If a slice depends on prior foundational capability, first select the minimal driving slice that can establish that foundation.
- Do not lay down a large number of abstraction layers not yet driven by the current slice at the start, for the convenience of later slices.

## Good Example

- This example is good because it first lets the minimal behavior stand firm, then stacks the next difference.

```md
Slices under the same scope:
1. The player can press submit after selecting three numbers
2. Cannot submit again in the same turn after submission
3. After turn switching, the opponent can submit

Advancement order:
1 -> 2 -> 3
```

## Bad Example

- This example is bad because it builds a general framework first, without any slice getting an independent signal.

```md
Do first:
- A general turn engine
- A general submit policy matrix
- A general guess permission framework

Then come back to run the first slice
```

# Rule 3 - Do not step outside the user-specified scope to absorb adjacent requirements

- Level: `MUST`
- The current invocation may only advance slices belonging to the specified `feature file` or its clearly identified block.
- If during implementation it is discovered that an adjacent `Rule`, other interface files, or other `feature files` would also be affected, do not opportunistically expand scope unless the current slice cannot stand within the original scope.
- If cross-scope changes are genuinely required for the current slice to stand, stop and report the reason so the user can re-decide the scope or hand back upstream.

## Good Example

- This example is good because it treats the scope guard as a real stop condition.

```md
Observations:
- The current frontend slice can be completed under the existing API mock
- Another backend feature may also need work later, but it is not a blocker now

Processing:
- Only complete this frontend slice
- Do not proactively switch to the backend feature
```

## Bad Example

- This example is bad because it mistakes "might be needed later" for current scope authorization.

```md
Observations:
- Only asked to do one section of the frontend feature

Processing:
- Because the backend is expected to change too, directly expand to the backend feature and API spec in sync
```

# Rule 4 - `Scenario Outline` or data families must still maintain a single behavior family

- Level: `SHOULD`
- If the current scope includes a `Scenario Outline` or a data family, multiple slices may be sequentially advanced within the same invocation, provided they still belong to the same business rule or the same kind of behavioral difference.
- If different rows, Examples, or data lines actually represent different business rules, return to upstream spec for splitting first instead of force-feeding them in the `/axb-bdd` phase.
- If a Data Table contains both setup and assertion data, also confirm first that its core behavior is still only one.

## Good Example

- This example is good because it treats multiple data rows as multiple inputs to the same rule.

```gherkin
Scenario Outline: invalid guesses are rejected
  Given it is the player's turn
  When the player submits "<guess>"
  Then the system prompts "<reason>"
```

## Bad Example

- This example is bad because it force-fits different rules into the same data family.

```gherkin
Scenario Outline: shot outcomes
  Given a match
  When the player submits "<case>"
  Then the system handles it as "<result>"
```

# Rule 5 - The current slice's definition of done must include behavioral signal and local cleanliness

- Level: `SHOULD`
- A slice is only fit to move to the next one when it meets the current entry's completion conditions, the focused test signal is clear, and no obvious duplicate steps, temporary code, wrong naming, or unfocused abstraction is left behind.
- `red` requires an effective failure signal; `green` requires the current slice to have turned green; `refactor` requires representative tests still protecting after refactoring.
- The definition of done pursues "safe to continue to the next slice", not "looks about right, move on".

## Good Example

- This example is good because it handles locally visible debt before moving on after turning green.

```md
Current slice status:
- focused test is green
- shared assertion helper extracted
- debug prints removed

Decision:
- Move to the next slice
```

## Bad Example

- This example is bad because it only looks at whether the feature roughly runs, ignoring obvious local distortions.

```md
Current slice status:
- Tests are occasionally green, occasionally red
- `tmpGuessHelper2` kept around
- Step wording still mixes in UI operation details

Decision:
- Go straight to the next slice
```
