# Rule 1 - The same-module DSL and the actually-used shared rows must be taken over via the feature path

- Level: `MUST`
- For `{interface}/{module}/{capability}.feature`, the same `{interface}/{module}/dsl.md` must be used as the module DSL; do not guess other DSL sources from the capability name.
- The module DSL must be read completely; the interface root `{interface}/dsl.md` only supplements the shared DSL rows actually used by that feature; do not pre-load all shared rows for a single feature.
- When looking up each feature step, the candidate definition set must be formed by merging "the same-module DSL" and "the interface root shared rows actually used by that step".

## Good Example

- This example is good because it derives the DSL from the feature's own module and only supplements the actually-used shared row.

```md
Target:
- `features/backend/three-guess/three-guess-single-shot-and-turn-switch.feature`

Must read:
- `features/backend/three-guess/dsl.md`

Supplementally read based on feature steps:
- The "response contains error code {code}" row in `features/backend/dsl.md`

Not loaded:
- Room query and chat shared rows in the root DSL not used by this feature
```

## Bad Example

- This example is bad because it ignores the same-module DSL and treats the entire interface root DSL as the default context for all features.

```md
Target:
- `features/backend/three-guess/three-guess-single-shot-and-turn-switch.feature`

Processing:
- Do not read `features/backend/three-guess/dsl.md`
- Read only the complete `features/backend/dsl.md`
- Look for similar-looking sentence patterns in other modules
```

# Rule 2 - Merged lookup must yield a unique DSL definition

- Level: `MUST`
- After merging the same-module DSL and the actually-used interface root shared rows, each feature step must yield exactly one implementable definition.
- Zero definitions after merging means missing DSL; multiple definitions after merging means the DSL boundary or vocabulary is not unique. Both must stop the affected scope and hand back to `/axb-dsl-refine`.
- `/axb-bdd` must not add, rewrite, or arbitrarily pick one DSL definition to resolve zero or multiple definitions.

## Good Example

- This example is good because it only accepts a unique result, and stops and hands back when encountering zero definitions.

```md
Case A:
- step: `Then response contains error code "INVALID_GUESS"`
- Module DSL: 0 entries
- Root shared DSL actually-used rows: 1 entry
- Total: 1 entry
- Decision: enter `/axb-bdd red` per the unique DSL definition

Case B:
- step: `Then the opponent sees a new cipher`
- Module DSL: 0 entries
- Root shared DSL actually-used rows: 0 entries
- Total: 0 entries
- Decision: stop the affected scope and hand back to `/axb-dsl-refine`
```

## Bad Example

- This example is bad because it still picks one downstream on its own after encountering multiple definitions.

```md
step:
- `When the player submits a guess`

Merged lookup:
- Module DSL: 1 entry
- Root shared DSL: 1 entry
- Total: 2 entries

Decision:
- Pick the definition with fewer parameters and continue implementing
- Do not hand back to `/axb-dsl-refine`
```

# Rule 3 - Do not reclassify module and shared sentence patterns in BDD

- Level: `MUST`
- Whether a sentence pattern belongs to the module DSL or the interface root shared DSL has already been decided by the truth ownership of `/axb-dsl-refine`; `/axb-bdd` can only take over and must not reclassify.
- Even if a sentence pattern looks reusable by other modules, do not move it to the interface root DSL, copy it into another module DSL, or infer truth ownership from the sharing degree of step definitions in this round.
- If existing ownership causes omissions, duplication, or inability to land uniquely, it must be handed back to `/axb-dsl-refine`; downstream directory tidying must not replace upstream decisions.

## Good Example

- This example is good because it returns the DSL ownership question to the truth owner.

```md
Observations:
- "Reject empty messages" exists only in `room-chat/dsl.md`
- The new feature is in another module, and merged lookup yields zero definitions

Processing:
- Stop the affected scope
- Hand back to `/axb-dsl-refine` to decide whether the sentence pattern should stay module-specific or be promoted to root shared
```

## Bad Example

- This example is bad because it changes DSL truth ownership on its own for implementation convenience.

```md
Processing:
- `/axb-bdd` thinks the sentence pattern may be shared in the future
- Moves the row from `{interface}/{module}/dsl.md` to `{interface}/dsl.md`
- Continues writing step definitions
```

# Rule 4 - Truth symlinks project per module only when the project has adopted them

- Level: `MUST`
- Symlinks are a conditional project handover strategy; this Rule applies only when the project has adopted truth symlinks — do not require all projects to add symlinks.
- When adopted, functional truth must be projected per `{interface}/{module}` folder, so that module's feature files and `dsl.md` are carried over together.
- The interface root shared `dsl.md` may be projected independently, for multiple projected modules to carry over shared rows.
- Copying truth content, creating per-feature symlinks, or creating per-file links for features or `dsl.md` within an already-projected module folder is forbidden.

## Good Example

- This example is good because an existing symlink project keeps the feature and DSL within one truth boundary per module folder.

```md
Project status:
- The test tree has adopted `specs/truth/features/**` symlinks

Projection:
- `backend/features/three-guess` -> `specs/truth/features/backend/three-guess`
- `backend/features/dsl.md` -> `specs/truth/features/backend/dsl.md`

Result:
- The feature files within the module are projected together with the module `dsl.md`
- The root shared DSL stays single-source
```

## Bad Example

- This example is bad because it copies content and creates per-file links within the module, breaking the folder-level truth boundary.

```md
Projection:
- Copy `specs/truth/features/backend/three-guess/dsl.md` into the test tree
- Create a symlink for each `.feature` of three-guess separately
- After linking `backend/features/three-guess`, also link `dsl.md` inside it
```

# Rule 5 - The focused runner must support module, single feature, and scenario name

- Level: `MUST`
- A focused runner taking over modular truth must be able to run tests by module, by single feature, and by scenario name.
- All three entries must use the same project test tree and step definitions; do not copy features or build a parallel runner for focused reruns.
- If the existing runner lacks any level, that gap must first be recorded as a test-entry blocker or missing capability; do not claim that modular truth has been fully taken over.

## Good Example

- This example is good because the same runner can narrow the feedback scope level by level.

```md
Focused entries:
- Module: `./run-bdd.sh three-guess`
- Single feature: `./run-bdd.sh three-guess/three-guess-single-shot-and-turn-switch.feature`
- Scenario name: `./run-bdd.sh --name "player submits a single shot successfully"`
```

## Bad Example

- This example is bad because it only has an all-at-once entry, and uses feature copying to sidestep the runner capability gap.

```md
Status:
- The runner can only run all features

Processing:
- Copy the target feature into a temp directory
- Run only that copy with another set of commands
- Claim focused rerun is supported
```
