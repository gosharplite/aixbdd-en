# Rule 1 - AIxBDD has three mandatory questions; research / techstack must not be written before all are asked

- Level: `MUST`
- This is the AIxBDD workflow. Before writing `research.md` or updating `specs/truth/techstack.md`, `/axb-technical-research` must first confirm all three of these questions are decided:
  1. **BDD techstack**: which runner each end uses to run Gherkin. Must clarify.
  2. **Test strategy**: how it is verified. Must ask. If unspecified, the default is E2E everywhere.
  3. **Which ends the system has**: in an initial project, when the system interface is suspected to have a backend or other ends, ask this too.
- All three questions go through `/axb-clarify`. Do not fill them in yourself in the `Rationale`, nor borrow the album example or agent inference as answers.
- If any mandatory question is not yet decided, stop and do not enter the phase that produces `research.md` / `techstack.md`.

## Good Example

- This example is good because all three questions are clarified first, then research is written.

````md
Initial project. `spec.md` has a workstation terminal, status board, and system settings; work-order status must be shared.

This round's `/axb-clarify`:
1. BDD techstack: frontend Playwright, backend behave
2. Test strategy: frontend E2E, backend behave hitting API and authoritative state
3. Which ends the system has: frontend webapp + backend API

Only then write `research.md`.
````

## Bad Example

- This example is bad because none of the three questions were asked; it directly assumes from spec and writes "no backend, no E2E".

````md
`spec.md` assumptions say pure frontend, no backend.

Directly write:
- Build no backend
- Test with vitest, introduce no E2E
- Never ask BDD techstack
````

# Rule 2 - Only the user's original words this round, this round's clarify, or existing techstack written out count as answered

- Level: `MUST`
- The following count as that question being decided, and re-asking may be skipped:
  - The user's original words this round already specified it, e.g. "the backend uses behave", "the frontend goes webapp", "the backend is python fastapi", "go straight to e2e test"
  - This round's `/axb-clarify` has obtained the answer to that question
  - Existing `specs/truth/techstack.md` already states that end, that end's BDD techstack, and the test strategy, with no change of decision this round
- The following do NOT count as answered; clarifying is still required:
  - `spec.md` assumptions or scope writing "pure frontend", "no backend", "no database", "no E2E"
  - The stacks of `research.example.md`, `techstack.example.md`, or any teaching example
  - Ends and test strategies the agent inferred itself from product stories, screen lists, or "minimal complexity for this version"
  - An empty `techstack.md`, one with only headings, or one with no adopted technology written yet

## Good Example

- This example is good because it takes the user's original words as answers, not spec assumptions.

````md
The user said this round: the backend is python fastapi, the backend uses behave, go straight to e2e test.

Judgment:
- BDD techstack backend = behave, decided
- Test strategy = E2E, decided
- The spec assumption "no backend" is not adopted; still ask which ends the system has, or follow the user's already-stated frontend webapp + FastAPI
````

## Bad Example

- This example is bad because it treats spec assumptions and example defaults as decided.

````md
`spec.md` says no backend; `research.example.md` says skip E2E for now.

Judgment:
- The system has no backend; no need to ask
- Test strategy follows vitest
````

# Rule 3 - BDD techstack must ask about the runner per end clearly

- Level: `MUST`
- BDD techstack asks: for each end that exists, which runner runs that end's Gherkin.
- The frontend webapp's BDD techstack and the backend API's BDD techstack must be asked or selected separately; do not gloss over it with "the whole project uses the same test framework".
- If an end's existence is not yet confirmed, first ask "which ends the system has", then ask that end's BDD techstack.
- When writing `research.md`, the BDD techstack must be an independent decision, or the runners must be listed per end in the test decision. When writing `techstack.md`, the `Testing & Verification` section must show each end's BDD techstack.

## Good Example

- This example is good because each end's runner is written separately.

````md
BDD techstack:
- Frontend webapp: Playwright
- Backend API: behave
````

## Bad Example

- This example is bad because it writes only one test framework, leaving it unclear how each end's Gherkin runs.

````md
Testing & Verification:
- vitest
- manual demo
````

# Rule 4 - The test strategy must be asked; if unspecified, the default is E2E everywhere

- Level: `MUST`
- The test strategy is a mandatory question; even if the agent thinks unit tests are cheaper, it must be asked first.
- When the user does not state a test strategy, the default is E2E everywhere: if there is a frontend, frontend E2E; if there is a backend, backend E2E. Backend E2E uses that end's BDD techstack to hit the API and authoritative state, not just domain functions.
- Do not write "vitest / pytest first, E2E later", "Quickstart manual verification", or "full browser E2E is too costly so it is not introduced" as defaults.
- Only when the user explicitly changes the decision to "this end skips E2E for now" may that end's E2E be excluded in `research.md` and `techstack.md`.

## Good Example

- This example is good because when unspecified it lands on E2E, changing only when stated.

````md
The user did not mention a test strategy.

Land on:
- Frontend webapp: E2E
- Backend API: E2E (behave)
````

## Bad Example

- This example is bad because it shrinks the default to unit tests on its own.

````md
The core risk is state and counts, so this version does not introduce browser E2E; use vitest only.
````

# Rule 5 - In an initial project, when the system interface is suspected to have a backend or other ends, ask which ends exist

- Level: `MUST`
- **Initial project** means this is the first plan, or `specs/truth/techstack.md` does not yet exist, is empty, or has no adopted technology written yet.
- In an initial project, as long as the system interface is *suspected* to have a backend or other ends, "which ends does this have" must be asked. Do not write it directly as frontend-only or backend-only.
- Any of the following holds means suspected of having a backend or other ends:
  - `spec.md` has multiple screens, and the screens share the same business state
  - There appear work orders, orders, inventory, approvals, to-dos, or status boards — states that need cross-terminal persistence or persistence across refresh
  - There appear commands like start/complete, first-come-first-served, available quantity, record tracing, or field settings
  - There appear API, database, backend, server, a second terminal, or a second role's dedicated screens
  - Success criteria require data not be wiped by refresh, or two operators seeing the same truth
- What is asked is the existence of ends, not framework details. Frameworks (e.g. FastAPI, Vite) can be supplemented in the same round or the next question, but "treat it as a pure frontend prototype for now" must not be used to skip the existence of ends.
- When it is not an initial project, and existing `techstack.md` already states which ends exist with no change of decision this round, this question need not be re-asked.

## Good Example

- This example is good because in the initial project, seeing multiple screens and shared work-order state, it asks which ends exist.

````md
Initial project. The spec has a workstation terminal, status board, and system settings; the same work order advances through them.

Must ask:
- Which ends does this have? Frontend webapp / Backend API / other
````

## Bad Example

- This example is bad because the initial project is clearly suspected of having a backend, yet spec assumptions are used to exclude it directly.

````md
Initial project. Spec assumption 5 says no backend.

Judgment: follow pure frontend, do not ask which ends exist.
````
