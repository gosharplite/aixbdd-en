# Rule 1 - Only high-impact gaps that would change the research conclusion should escalate to /axb-clarify

- Level: `MUST`
- Only when a gap would change the decision set, candidate option boundaries, comparison dimensions, inviolable constraints, recommendation direction, or downstream handoff judgment should it escalate to `/axb-clarify`.
- If an undecided detail only affects wording, secondary comparison angles, example content, or local assumptions that can be explicitly retained in the `Rationale`, it should not be escalated to `/axb-clarify` directly.
- Do not turn all research uncertainty into interviews, robbing the upstream skill of its responsibility to converge research questions first.

## Good Example

- This example is good because it escalates only the gaps that would change the recommended option to clarify.

````md
Research topic: image storage strategy for photo date-album organization.

High-impact gaps:
- Whether the first version allows originals on the filesystem instead of the database
- Whether offline backup constraints exist that must be supported

Decision:
- Escalate to `/axb-clarify`
````

## Bad Example

- This example is bad because it escalates local wording to clarify as well.

````md
Research topic: image storage strategy for photo date-album organization.

Low-impact details:
- Whether the title says "Research" or "Technical Research"
- Whether Alternatives considered lists 2 or 3 items

Decision:
- Escalate to `/axb-clarify`
````

# Rule 2 - Each research clarify round handles only the 1 to 3 highest-impact questions

- Level: `MUST`
- Before delegating `/axb-clarify`, `axb-technical-research` must sort the research gaps itself and hand over only this round's 1 to 3 highest-impact questions to `/axb-clarify`.
- If there are more than 3 high-impact gaps, keep the most critical 1 to 3 to ask first; the remaining risks can be disclosed in the artifact or left for the next round.
- Do not dump an unorganized long list of technical questions at `/axb-clarify` as-is.

## Good Example

- This example is good because it sorts first, then asks only the questions that most affect the research direction.

````md
This round's gap ranking:
1. Deployment boundaries allowed in the first version
2. Whether multi-tenancy must be supported
3. Data retention policy
4. Document title naming preference

Delegation:
- Hand only the top 3 questions to `/axb-clarify` this round
````

## Bad Example

- This example is bad because it throws out all questions of varying sizes at once.

````md
Delegation:
- Hand all 9 technical questions to `/axb-clarify`
````

# Rule 3 - Low-risk undecided details should stay disclosed within the research content

- Level: `MUST`
- If the main decisions, comparison dimensions, and recommendation direction hold, but a few local details remain undecided, prefer explicitly stating assumptions, constraints, or verification points in the corresponding decision's `Rationale` or `Alternatives considered`.
- Only when an undecided detail already affects the final adoption conclusion or the next handoff should it escalate back to `/axb-clarify`.
- Do not launch interviews for every local unknown just to make the document look complete.

## Good Example

- This example is good because it retains local uncertainty without blocking the main research conclusion.

````md
- **Rationale**: Adopting database BLOBs maintains transaction consistency; the actual capacity ceiling still needs stress verification with the acceptance dataset at the implementation stage.
````

## Bad Example

- This example is bad because it escalates a retainable local verification point into an interrupting question.

````md
Gap:
- Still unknown whether the average image size will be 4MB or 5MB

Decision:
- Pause research and enter `/axb-clarify` immediately
````

# Rule 4 - Decided product scope must not be re-asked; BDD techstack, test strategy, and which ends the system has are exceptions

- Level: `SHOULD`
- When `/axb-specify` has clearly decided the product feature boundaries, first-version do/don't, success criteria, or business constraints in `spec.md`, `axb-technical-research` should follow them directly and not hand the same product question to `/axb-clarify` again.
- The following three questions must still be handled per `rules/aixbdd-mandatory-questions-and-initial-project-interface-clarification-criteria.md` even if `spec.md` assumptions or scope already state answers; this rule must not be used to skip them:
  - BDD techstack
  - Test strategy
  - Which ends the system has, in an initial project
- `spec.md` writing "pure frontend", "no backend", "no database", or "no E2E" only represents product-draft assumptions; it does not mean these three questions are decided.
- Only when the user's latest instruction conflicts with `spec.md`'s product scope, or the product scope itself is still undecided, should product questions be re-asked.

## Good Example

- This example is good because the product scope follows spec while the three mandatory questions are still clarified.

````md
Known: `spec.md` clearly states:
- The first version only does single-level date albums
- Assumption: this version has no backend

Decision:
- Album nesting follows spec, no re-asking
- Still clarify BDD techstack, test strategy, and which ends the system has
````

## Bad Example

- This example is bad because it uses spec assumptions to skip the mandatory questions.

````md
Known: `spec.md` clearly states:
- Assumption: this version has no backend, no E2E

Decision:
- Follow pure frontend; do not ask which ends exist
- Follow vitest; do not ask test strategy or BDD techstack
````
