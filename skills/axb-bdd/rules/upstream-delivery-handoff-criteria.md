# Rule 1 - Only interface feature and the two-layer DSL are accepted as the single upstream source

- Level: `MUST`
- Before `/axb-bdd` starts, it must first confirm that this round has a user-specified interface `feature file` or its clearly identified block, the same module's `dsl.md`, and the interface root shared `dsl.md` rows actually used by that feature.
- If only acceptance Gherkin, requirement descriptions, or scattered implementation ideas are provided, without the interface feature and its required two-layer DSL, `/axb-bdd` must not fill in the spec itself.
- The `feature file` carries the behavior boundary; the module DSL together with the actually-used interface root shared rows carry step vocabulary, parameters, and implementation semantics. Their on-demand lookup and project projection are governed by `modular-truth-on-demand-symlink-criteria.md`.

## Good Example

- This example is good because it confirms before starting that all formal deliverables of `/axb-dsl-refine` are in place.

```md
Known inputs:
- `features/frontend/three-guess/battle-page-three-guess-selection-and-single-shot.feature`
- `features/frontend/three-guess/dsl.md`
- `features/frontend/dsl.md`

Processing:
- `/axb-bdd red` takes over the feature, the complete module DSL, and the root shared rows actually used by the feature
- Establishes the focused failure based on its behavior boundary and unique DSL vocabulary
```

## Bad Example

- This example is bad because it lacks the same-module DSL, yet `/axb-bdd` still guesses the implementation semantics.

```md
Known inputs:
- `features/frontend/three-guess/battle-page-three-guess-selection-and-single-shot.feature`
- Only `features/frontend/dsl.md`

Processing:
- `/axb-bdd` skips the same-module `features/frontend/three-guess/dsl.md`
- Guesses the implementation semantics of all steps directly from the root shared DSL
```

# Rule 2 - The user-specified scope must fall within a single interface `feature file` or a clearly identified block

- Level: `MUST`
- The working scope of `/axb-bdd` must converge to a single interface `feature file`, or a `Rule`, `Example`, scenario family, or equivalent block that can be clearly pointed out within that file.
- If the scope spans multiple interfaces, spans multiple unrelated `feature files`, or is described only by a vague capability name that cannot be stably mapped to a concrete block, clarify first — do not start implementation directly.
- Although a single invocation may sequentially advance multiple slices, all those slices must belong to the same specified scope.

## Good Example

- This example is good because it locks the scope into a clearly identified block of a single interface feature.

```md
This round's scope:
- `features/backend/three-guess/three-guess-single-shot-and-turn-switch.feature`
- Only the Rules and Examples related to "single shot submitted successfully"

Processing:
- `/axb-bdd green` processes the slices awaiting green only within this block, in order
```

## Bad Example

- This example is bad because it lets the scope drift to multiple interfaces and multiple unaligned specs.

```md
This round's scope:
- Frontend selection
- Backend turn switching
- Acceptance criteria too, if convenient

Processing:
- `/axb-bdd refactor` thinks about and changes code across three different-level features at once
```

# Rule 3 - When a spec gap is found, first distinguish whether it is a clarification gap or an upstream delivery gap

- Level: `MUST`
- If the gap is that the user has not made clear this round's scope, target entry, or which block to handle, it is a clarification gap that can be converged via `/axb-clarify`.
- If the gap comes from unclear boundaries of the `feature file`, module DSL, or interface root shared DSL, missing vocabulary, contradictory acceptance results, or no unique implementable definition after merging, it is an upstream delivery gap and should be handed back to `/axb-dsl-refine` or the user-specified upstream process.
- Do not disguise an upstream delivery gap as a downstream implementation detail and absorb it yourself in step definitions, helpers, or product code.

## Good Example

- This example is good because it distinguishes what should be asked of the user from what should be handed back upstream.

```md
Observations:
- The user only said "do the frontend first": this is unclear scope, use `/axb-clarify` first
- The same step has two definitions after merging module DSL and root shared DSL: this is an upstream delivery gap, hand back to `/axb-dsl-refine`
```

## Bad Example

- This example is bad because it secretly sinks a spec problem down to the implementation layer.

```md
Observations:
- The Then description in the `feature file` is inconsistent with the authoritative state definition in the module DSL

Processing:
- Do not stop
- Directly implement whichever version seems reasonable in an assertion helper
```

# Rule 4 - Do not rewrite upstream spec yourself in exchange for downstream progress

- Level: `MUST`
- `/axb-bdd` may report gaps, contradictions, and blockers in upstream spec, but must not rewrite the `feature file`, module DSL, or interface root shared DSL to get this round going.
- Even a mere wording adjustment counts as an upstream modification if it affects behavior boundaries, parameter semantics, authoritative state, or the unique implementability of the DSL.
- Only when the user explicitly requests switching back to the upstream process, or after the upstream skill's revision is completed, may `/axb-bdd` take over the updated deliverables again.

## Good Example

- This example is good because it would rather stop than invade upstream responsibilities.

```md
Observations:
- Both the module DSL and root shared DSL lack the parameter semantics for the When "player submits three guesses"

Processing:
- Report the gap
- Stop `/axb-bdd red`
- Ask the user to return to `/axb-dsl-refine` to fill it in before continuing
```

## Bad Example

- This example is bad because it directly modifies the upstream spec source to make implementation smooth.

```md
Observations:
- The Given wording in the `feature file` is too vague

Processing:
- `/axb-bdd` directly opens the feature file and writes more detailed preconditions
- Then continues writing step definitions
```
