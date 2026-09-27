# Rule 1 - During implementation, do not stop to ask the user for clarification over ordinary spec gaps

- Level: `MUST`
- If a gap can still be converged through the current task, the phase's `Shared Must Read`, the phase's `Boundary`, `Dependencies`, existing code, or toolchain boundaries, a professional judgment must be made on your own — do not stop to ask the user first.
- If the current task is in `Setup` / `Foundational` or another general phase, use that task's `Read`, `Dependencies`, existing code, and the minimal reversible option as the decision basis instead.
- Only when tools, permissions, missing files, or environment limits make subsequent steps objectively unexecutable may the run be stopped.

## Good Example

- This example is good because it converges on its own with known constraints instead of instantly escalating ordinary ambiguity to a user question.

```md
`FR-017` does not yet specify the first-move rule.
The agent first reads the current phase's `Boundary`, confirms the assumption must be confined to a single domain helper,
so it adopts a minimally replaceable default implementation and keeps the risk inside that boundary.
```

## Bad Example

- This example is bad because it still stops and waits for the user even though enough constraints exist to converge.

```md
Seeing the first-move rule unspecified, the agent immediately reports "should the room owner go first or is it random?" and aborts the whole implementation flow.
```

# Rule 2 - When ambiguity cannot be fully removed, choose the minimal-change, lowest-coupling, isolatable option

- Level: `MUST`
- If multiple options all satisfy the current information, prefer the option with the minimal change, lowest coupling, easiest verification, and highest reversibility.
- If the current phase's `Boundary` has designated which files, modules, or responsibility boundaries the uncertainty should concentrate in, the assumption must be confined to those boundaries and must not spread to other task surfaces.
- Do not hard-code still-unconverged rules into multiple handlers, pages, or state modules for short-term convenience.

## Good Example

- This example is good because it compresses the ambiguity into one replaceable boundary.

```md
The agent needs to decide the default source of `currentTurnPlayerId` first.
It concentrates the decision in a single helper in `game.js`, instead of scattering the same judgment across the socket handler, presenter, and frontend state.
```

## Bad Example

- This example is bad because it copies the unclarified rule into multiple layers, making future rule fixes a cleanup hunt.

```md
The agent writes its own first-move judgment in `gameHandler.js`, `roomStore.js`, and `main.js` at the same time, with the three logics not even fully consistent.
```

# Rule 3 - When perfect progress is impossible, still adopt the best feasible alternative and disclose residual risks

- Level: `SHOULD`
- If the ideal path is blocked by environment, tools, or external resources, but a feasible alternative path exists, adopt the alternative and keep moving instead of halting everything prematurely.
- The completion report should clearly disclose the alternative adopted, the limiting reasons, and the parts still pending external conditions.

## Good Example

- This example is good because it first completes what can be completed and states the real limitation clearly.

```md
The agent cannot run the full integration verification, but still completes targeted tests, lint, and manual verification script updates first,
finally noting in the report that integration verification is limited by the local environment.
```

## Bad Example

- This example is bad because it mistakes a partial limitation for an inability to move forward at all.

```md
Finding one verification tool temporarily unavailable, the agent stops all subsequent tasks outright without first completing the parts that can still be done independently.
```
