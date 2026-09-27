# Rule 1 - `Wave` execution order must obey `plan.md`

- Level: `MUST`
- When `axb-system-analysis` delegates to each planner skill, it must execute in the `Wave` order already defined in `plan.md`; do not skip the previous wave and start a later one just because some planner looks ready to go first.
- Parallel delegation within the same `Wave` is allowed, provided these interfaces have been judged parallelizable for analysis in `plan.md`.
- If a planner's analysis clearly depends on information only produced by the previous `Wave`, it must wait for the previous `Wave` to complete before delegation.

## Good Example

- This example is good because it converges the backend event contract first, then places the data state design that depends on that contract in the next wave.

```md
#### Wave 1

- Parallel analysis interfaces:
  - `Backend room & match API interface`

#### Wave 2

- Parallel analysis interfaces:
  - `Room & match state data interface`

Delegation order:
1. Call `/axb-api-plan` first
2. After Wave 1 completes, call `/axb-data-plan`
```

## Bad Example

- This example is bad because it ignores the `Wave` dependency and does data design first, letting the data model be assumed before the event contract.

```md
#### Wave 1

- Parallel analysis interfaces:
  - `Backend room & match API interface`

#### Wave 2

- Parallel analysis interfaces:
  - `Room & match state data interface`

Delegation order:
1. Call `/axb-data-plan` first
2. Add `/axb-api-plan` later
```

# Rule 2 - planner / contract-owner mapping must be decided by analysis responsibility boundaries

- Level: `MUST`
- `axb-system-analysis` must decide each system interface's delegation target or taker by its main analysis responsibility and artifact boundary, not merely by whether a technical word appears in its name.
- Player-visible flows, screen states, interaction rhythm, information disclosure, and error feedback are produced at the plan stage by the PM's `/axb-ui-plan` (`ui/ui-plan.md` and static prototypes); `axb-system-analysis` no longer delegates to `/axb-ui-plan`, instead reviewing whether the existing UI artifacts are implementable within current technical boundaries and reporting gaps when necessary.
- Entities, fields, state holding, life cycles, data relations, and storage responsibilities should be delegated to `/axb-data-plan`.
- API contracts, event protocols, request/response shapes, state-transition entries, and error-code semantics should be delegated to `/axb-api-plan`.
- Terminal-user / operator-visible commands, flags, stdout/stderr, and exit-code contracts (CLI interfaces) have no corresponding analysis planner: they are not taken over by `/axb-api-plan` or `/axb-data-plan`, but by the contract owner `/axb-dsl-refine`, explicitly handed off at delivery. If that CLI ships an interactive TUI, its terminal UX surface (screens, keybindings, state transitions) is handled like the frontend — already produced by the PM's `/axb-ui-plan` (terminal mode); `axb-system-analysis` only reviews its implementability, with no redo and no delegation.
- If an interface involves multiple kinds of responsibility at once, return to `plan.md`'s interface split to re-judge whether splitting is needed, rather than throwing the same interface to multiple planners at once.

## Good Example

- This example is good because it routes by analysis responsibility, not by technical names first.

```md
1. `Room & match state data interface`
   - Main interfaces: Room, Game, Guess state holding and life cycles
   - Delegate: `/axb-data-plan`

2. `Backend realtime event contract interface`
   - Main interfaces: join/create, ready, start, guess, broadcast
   - Delegate: `/axb-api-plan`

3. `Frontend matching & match interface`
   - Main interfaces: screen states, role indicators, operation feedback
   - Taken over by: PM already produced `ui/ui-plan.md` and static prototypes via `/axb-ui-plan`; `axb-system-analysis` does not delegate, only reviews implementability

4. `CLI command & exit-code interface`
   - Main interfaces: commands, flags, stdout/stderr, and exit-code contract
   - Taken over by: `/axb-dsl-refine` (CLI contract owner; no corresponding analysis planner)

5. `CLI interactive TUI interface`
   - Main interfaces: terminal screens, keybindings, state transitions
   - Taken over by: PM already produced `ui/ui-plan.md` and `ui/screens/*.txt` via `/axb-ui-plan` (terminal mode); `axb-system-analysis` does not delegate, only reviews implementability
```

## Bad Example

- This example is bad because it throws the same interface to multiple planners repeatedly, with routing reasons coming only from technical words, not responsibility boundaries.

```md
1. `Backend matching & match interface`
   - Delegate: `/axb-data-plan`, `/axb-api-plan`
   - Reason: it also has socket events in it
```

# Rule 3 - Same-wave interfaces sharing a main artifact boundary should prefer merged handoffs

- Level: `SHOULD`
- If multiple system interfaces within the same `Wave` would all write to the same main artifact, prefer merging them into one delegation, avoiding the same planner repeatedly overwriting the same file within one feature.
- When merging a handoff, the delegation content must list all merged interface names, their individual analysis focuses, and the artifact boundary they share.
- Only when two interfaces point to the same planner but their artifact boundaries are clearly independent is splitting into multiple delegations appropriate.

## Good Example

- This example is good because it merges two same-wave interfaces that both belong to the backend contract and hands them to one planner, producing the same `contracts/` artifact in one go.

```md
#### Wave 2

- Parallel analysis interfaces:
  - `Backend room event contract interface`
  - `Backend match event contract interface`

Delegation:
- Single call to `/axb-api-plan`
- The prompt lists both interfaces and their individual analysis focuses
- Shared main artifact: `contracts/openapi.yaml`
```

## Bad Example

- This example is bad because it has the same planner repeatedly overwrite the same artifact without any new boundary.

```md
#### Wave 2

- Parallel analysis interfaces:
  - `Backend room event contract interface`
  - `Backend match event contract interface`

Delegation:
1. Call `/axb-api-plan` to produce `contracts/openapi.yaml`
2. Call `/axb-api-plan` again to overwrite the same `contracts/openapi.yaml`
```
