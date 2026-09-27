# Rule 1 - Research stays in the plan package

- Level: `MUST`
- `/axb-technical-research`'s decision-driven research process must be output to `specs/plans/NNN-<slug>/research.md`.
- `research.md` describes how technical decisions are made this iteration, and may include alternatives, adoption rationale, and residual risks.

## Good Example

- This example is good because the research process stays in this plan.

```text
specs/plans/004-room-game-chat/research.md
```

## Bad Example

- This example is bad because it puts this research process into truth.

```text
specs/truth/research.md
```

# Rule 2 - techstack is a truth artifact

- Level: `MUST`
- `/axb-technical-research` must output or update the system's currently adopted technical stack to `specs/truth/techstack.md`.
- `specs/truth/techstack.md` must be the complete current state; it must not describe only this increment, nor write "the rest defer to 001/002".
- After completion, `/axb-truth-delta` must be delegated to record `/axb-technical-research`'s ADD / MODIFY / DELETE / NOOP.

## Good Example

- This example is good because the techstack truth is the whole system's current state.

```text
specs/truth/techstack.md
```

## Bad Example

- This example is bad because each plan package keeps its own copy of techstack truth.

```text
specs/plans/004-room-game-chat/techstack.md
```
