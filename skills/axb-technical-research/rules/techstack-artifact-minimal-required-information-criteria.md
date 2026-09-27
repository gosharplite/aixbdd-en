# Rule 1 - `techstack.md` must present a high-level technical stack overview, not rewrite research decisions item by item

- Level: `MUST`
- `techstack.md`'s responsibility is to summarize the final technical stack and main tool layering adopted for this feature — not to rewrite `research.md`'s `Decision`, `Rationale`, and `Alternatives considered` item by item.
- If some content has gone into detailed trade-offs, item-by-item alternatives, or long rationale passages, keep it in `research.md` instead of copying it into `techstack.md`.
- `techstack.md` should let downstream planning or implementation quickly understand "which technologies were finally adopted this time".

## Good Example

- This example is good because it keeps only the final adopted results and their purposes, without rewriting the detailed research process.

````md
### Backend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| HTTP framework | `Express` | API routing and server handling |
| Upload handling | `multer` | Multi-file photo upload |
````

## Bad Example

- This example is bad because it moves entire passages of `research.md`'s detailed research rationale over.

````md
### Backend

- `Express`: a minimal and mature HTTP API framework, superior to Koa, Fastify, and Hono, because...
- `multer`: chosen over other options for the following reasons...
````

# Rule 2 - `techstack.md` must include high-level categories, a technology list, and a purpose field

- Level: `MUST`
- `techstack.md` must contain at least `Tech Stack Overview` and `Technologies Not Introduced in This Development`.
- Every category within `Tech Stack Overview` must use a table with the same fields, containing at least the three columns `Category`, `Adopted Technology`, `Purpose`.
- If a high-level category has no content, the whole section may be deleted; but retained categories must maintain the same field structure.

## Good Example

- This example is good because it keeps the fixed fields and high-level categories.

````md
## Tech Stack Overview

### Frontend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Build tooling | `Vite` | Local development and frontend builds |
````

## Bad Example

- This example is bad because it lacks the fixed fields, making stable downstream comparison difficult.

````md
## Tech Stack Overview

- `Vite`
- `Express`
- `Prisma`
````

# Rule 3 - `techstack.md` should list only finally adopted and explicitly excluded technologies

- Level: `SHOULD`
- `techstack.md` should focus on the technologies finally adopted for this feature, and those explicitly decided not to be introduced this time.
- Do not mix undecided candidates, ones only briefly evaluated, or ones excluded without entering the final boundary into the adopted list.
- If a technology was only researched but not adopted, keep it in `research.md`'s `Alternatives considered` first, unless it is an explicit "technology not introduced in this development".

## Good Example

- This example is good because it lists only final adoptions and explicit exclusions.

````md
## Technologies Not Introduced in This Development

- `React` or other frontend frameworks
- Third-party drag-and-drop packages (e.g. `SortableJS`)
````

## Bad Example

- This example is bad because it stuffs undecided evaluation items into the adopted list.

````md
### Frontend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| UI technology | `React?` / `Native JavaScript?` | Still considering |
````

# Rule 4 - `techstack.md`'s `Testing & Verification` must show each end's BDD techstack

- Level: `MUST`
- `Testing & Verification` must not list only one generic test framework. For every confirmed existing end, write that end's BDD techstack and purpose.
- When the user has not changed the test strategy, each end should be written as E2E; do not list "full browser E2E" or backend E2E under `Technologies Not Introduced in This Development`.
- The frontend webapp's runner and the backend API's runner are listed separately. The purpose must state which end's Gherkin it runs, and whether it hits screens or API / authoritative state.

## Good Example

- This example is good because each end's BDD techstack is visible, and the default is E2E.

````md
### Testing & Verification

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Frontend BDD techstack | `Playwright` | webapp E2E, runs frontend Gherkin |
| Backend BDD techstack | `behave` | backend E2E, runs backend Gherkin, verifies API and authoritative state |
````

## Bad Example

- This example is bad because the per-end runners are not visible, and E2E is excluded.

````md
### Testing & Verification

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| API testing | `vitest` | Test execution framework |
| Manual verification | `quickstart.md` | Frontend operations |

## Technologies Not Introduced in This Development

- Full browser E2E test framework
````

# Rule 5 - `techstack.md`'s category and enumeration granularity should serve downstream handoffs

- Level: `SHOULD`
- `techstack.md`'s categories should be organized at the high-level perspective easiest for downstream planning or implementation to take over, e.g. frontend, backend, data & media handling, testing & verification.
- If a category has only 1 row but still clearly expresses responsibility, keep it; if some rows actually share the same purpose, avoid over-fragmenting.
- The goal is to quickly build a global stack view, not to turn every dependency untouched into a package list.

## Good Example

- This example is good because the categories and granularity both serve downstream handoffs.

````md
### Testing & Verification

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Frontend BDD techstack | `Playwright` | webapp E2E |
| Backend BDD techstack | `behave` | backend E2E |
````

## Bad Example

- This example is bad because it degrades a readable tech overview into a raw dependency dump.

````md
dependencies:
- vite
- express
- multer
- prisma
- exifr
- sharp
````

# Rule 6 - `techstack.md` must never record system behavior guarantees or internal invariants as technology items

- Level: `MUST`
- `techstack.md` may only record technology selections, tool frameworks, package dependencies, and purpose layering. It is **strictly forbidden** to write system behavior guarantees or internal invariants (such as "rollback has durability and atomicity", "a crash does not corrupt data", "no external network connections", "retries are idempotent", etc.) as `techstack.md` table rows or prose.
- Behavior guarantees and invariants belong to spec or interface truth (Spec / Interface Truth), not the technical stack:
  - If observable externally by users or interfaces: route them to Gherkin acceptance scenarios and interface features.
  - If they are internal invariants or non-observable NFRs: schedule `[WITNESS]` tasks to establish discriminating witnesses at the unit test or fault-injection layer, or record them as decisions on the project decision surface (ADR).
- Strictly forbidden is disguising unwitnessed behavior guarantees as technical specs in `techstack.md`, lest downstream engineering mistake prose guarantees for established facts.

## Good Example

- This example is good because `techstack.md` keeps only the technology itself, smuggling in no behavior guarantees.

````md
### Backend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Local storage | `os.File` + `syscall.Fsync` | History record file writing and flush-to-disk |
````

## Bad Example

- This example is bad because it records an unprotected behavior guarantee as a technology row in `techstack.md`.

````md
### Backend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Data durability | `Atomic rollback mechanism` | Rollback has atomicity and durability: temp file + fsync + atomic rename guarantee no corruption on crash |
````

