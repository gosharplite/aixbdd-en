# Rule 1 - Every research decision in `research.md` must fully retain the title, Decision, Rationale, and Alternatives considered

- Level: `MUST`
- Every decision block in `research.md` must contain a decision title, `Decision`, `Rationale`, and `Alternatives considered`.
- Do not list only conclusions without adoption rationale, nor only pros/cons notes without a clear adopted option.
- `Alternatives considered` should list at least 1 alternative with comparison value.

## Good Example

- This example is good because it retains the minimal information needed to make and review the decision.

````md
## Decision 1: Drag-and-drop sorting adopts the browser-native Drag and Drop

- **Decision**: Use the native Drag and Drop API within the same date album.
- **Rationale**: The requirement only covers in-album reordering; the native API suffices and has a lower learning cost.
- **Alternatives considered**:
  - `SortableJS`
  - Fully custom with `Pointer Events`
````

## Bad Example

- This example is bad because it does not clearly account for adoption rationale and alternatives.

````md
## Decision 1: Drag-and-drop sorting

- Use the native API.
````

# Rule 2 - `research.md` must focus on decisions supporting downstream planning or implementation, not become a general tutorial article

- Level: `MUST`
- `research.md` should focus on this feature's technical decisions to be made, option trade-offs, and constraints; the artifact must not become generic technical tutorials or encyclopedia collections disconnected from the current feature.
- Every decision should tie back to `spec.md`'s requirements, scope, success conditions, or the design judgments needed by downstream handoffs — not shift detailed research rationale onto `techstack.md`.
- If some content cannot support this feature's next-step planning or implementation, it should be deleted or condensed into a passing note.

## Good Example

- This example is good because every decision directly supports that feature's downstream planning.

````md
Research topic: photo date-album organization

Decisions:
- Whether the frontend adopts a framework
- Whether images are stored in MySQL BLOB or the filesystem
- How to model sorting persistence
````

## Bad Example

- This example is bad because it leaves the current feature and becomes generic tech notes.

````md
Research topic: the evolution of JavaScript history

Content:
- A complete summary of ECMAScript version evolution
- The origins of the JavaScript language
````

# Rule 3 - `research.md`'s `Alternatives considered` must be real alternatives with comparison value

- Level: `SHOULD`
- `Alternatives considered` should list options genuinely selectable under the current decision that would lead to different trade-offs, not mere near-synonym restatements padded for form.
- If a clear reason exists for an alternative not being adopted, briefly state its rejection reason.
- When there is only 1 reasonable alternative, listing just 1 is fine, but it must still have comparison value.

## Good Example

- This example is good because it lists options that would actually change architectural trade-offs.

````md
- **Alternatives considered**:
  - `mysql2` writing SQL directly: fewer dependencies, but worse schema evolution and teaching readability
  - `Knex`: closer to SQL, but type integration less direct than Prisma
````

## Bad Example

- This example is bad because it lists alternatives without substantive differences.

````md
- **Alternatives considered**:
  - A better way
  - Another roughly similar method
````

# Rule 4 - Unverified assumptions and residual risks in `research.md` must be disclosed, not disguised as confirmed facts

- Level: `SHOULD`
- If a decision still relies on unverified capacity, performance, compatibility, or operational assumptions, state them explicitly in `research.md`'s `Rationale`, or list them as follow-up spike / verification items at delivery.
- Do not write unmeasured numbers, unconfirmed boundaries, or speculative constraints directly as decided facts.
- This lets downstream `/plan-with-class-diagram` or the implementation stage clearly take over the remaining risks.

## Good Example

- This example is good because it retains the capacity risk awaiting verification.

````md
- **Rationale**: Storing originals and thumbnails in MySQL BLOB simplifies teaching and consistency; actual capacity and backup time still need verification at the implementation stage.
````

## Bad Example

- This example is bad because it writes an unverified conclusion as absolute fact.

````md
- **Rationale**: MySQL BLOB can definitely provide the best performance and lowest cost in all deployment scenarios.
````
