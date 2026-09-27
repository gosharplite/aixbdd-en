# Rule 1 - Only high-impact gaps should escalate to /axb-clarify

- Level: `MUST`
- Only when a gap would change user story splitting, requirement attribution, main flows, role permissions, scope boundaries, formal acceptance criteria, or success criteria should it escalate to `/axb-clarify`.
- If an undecided detail only affects local wording, secondary interactions, a single numeric threshold, or safely deferrable experience options, it should not be escalated to `/axb-clarify` directly.
- Do not throw every ambiguity at `/axb-clarify`, robbing the upstream skill of its responsibility to converge requirements first.

## Good Example

- This example is good because it escalates only the gaps that would change the core match rules to clarify.

````md
Requirement: fully online PVP 1A2B.

High-impact gaps:
- Whether the first-move rule is decided by the room owner, the joiner, or randomly
- On disconnection: pause, forfeit, or wait for reconnect

Decision:
- Escalate to `/axb-clarify`
````

## Bad Example

- This example is bad because it escalates low-risk presentation details to clarify as well.

````md
Requirement: fully online PVP 1A2B.

Low-impact details:
- Whether the waiting button says "Start" or "Start Game"
- Whether the room card's primary color leans blue or green

Decision:
- Escalate everything to `/axb-clarify`
````

# Rule 2 - This round's clarify converges only the 1 to 3 highest-impact questions

- Level: `MUST`
- Before delegating `/axb-clarify`, `axb-specify` must sort the gaps itself and hand over only this round's 1 to 3 highest-impact questions to `/axb-clarify`.
- If there are more than 3 high-impact gaps, keep the most critical 1 to 3 to ask first, leaving the rest for later rounds or disclosing them as residual risks in the spec.
- Do not dump an unorganized long list of questions at `/axb-clarify` as-is.

## Good Example

- This example is good because it sorts first, then hands clarify this round's most critical questions.

````md
This round's gap ranking:
1. First-version scope
2. Role permissions
3. Success criteria threshold
4. Error message copy

Delegation:
- Hand only the top 3 questions to `/axb-clarify` this round
````

## Bad Example

- This example is bad because it dumps all questions on the downstream skill at once without upstream convergence.

````md
Delegation:
- Hand all 8 questions of varying sizes to `/axb-clarify`
````

# Rule 3 - Low-risk undecided details stay in the spec; do not ask for the sake of asking

- Level: `MUST`
- If the whole spec's main stories, requirement attribution, and acceptance logic hold, but a few local details remain undecided, prefer `NEEDS CLARIFICATION` or assumption disclosures in the spec rather than adding a clarify round.
- Only when an undecided detail already affects the main flows, formal requirement logic, or success criteria should it escalate back to clarify.
- Do not launch interviews for every small gap just to make the document look complete on the surface.

## Good Example

- This example is good because it keeps details that do not block the main flow in the spec instead of over-asking.

````md
- **NFR-004**: The system MUST provide understandable progress feedback on homepage load [NEEDS CLARIFICATION: not yet specified whether skeleton screen, progress bar, or another presentation]
````

## Bad Example

- This example is bad because it escalates a local detail that could stay in the spec to a user interview.

````md
Gap:
- Whether the loading hint is a skeleton screen or a progress bar

Decision:
- Pause the spec and enter `/axb-clarify` immediately
````

# Rule 4 - When delegating clarify, the downstream skill's session budget must be respected

- Level: `SHOULD`
- When `axb-specify` delegates `/axb-clarify`, it should explicitly state that this round handles only the sorted high-impact questions, avoiding any implication that the downstream skill may extend questioning without limit.
- If previous rounds have already used part of the clarify question budget, this round's delegation should preserve the remaining budget; do not assume the downstream skill can still ask without limit.
- If the residual risk is already acceptable, prefer letting the spec continue rather than exhausting the clarify allowance in pursuit of perfect information.

## Good Example

- This example is good because it clearly accounts for this round's scope and the remaining budget awareness.

````md
Call `/axb-clarify`:
- This round handles only the two questions: story splitting boundaries and success criteria
- Other low-risk details stay in the spec
````

## Bad Example

- This example is bad because it treats clarify as an unlimited questionnaire with no budget awareness.

````md
Call `/axb-clarify`:
- As long as any ambiguity remains, keep asking until there are no questions at all
````
