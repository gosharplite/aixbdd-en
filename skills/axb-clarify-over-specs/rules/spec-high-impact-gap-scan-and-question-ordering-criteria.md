# Rule 1 - High-impact gaps must be scanned with a whole-spec taxonomy

- Level: `MUST`
- When scanning `spec.md`, a coverage viewpoint must be established first, rather than only chasing existing `NEEDS CLARIFICATION` markers.
- Inventory category by category at least according to the following taxonomy, and mark `Clear`, `Partial`, or `Missing` in mind:
  - Functional Scope & Behavior
    - Are the core user goals and success conditions clear?
    - Are out-of-scope items or non-goals explicitly stated?
    - Are roles, user types, or permission boundaries clearly separated?
  - Domain & Data Model
    - Are the key entities, fields, and relationships sufficient to support the requirements?
    - Are uniqueness, identification, state transitions, or life cycles clear?
    - Are important data volume assumptions or capacity boundaries missing?
  - Interaction & UX Flow
    - Are key flows, step sequences, and state switches replayable?
    - Are error / empty / loading / retry / interrupted states defined?
    - Are accessibility, locale, or interaction limits explicitly stated?
  - Non-Functional Quality Attributes
    - Performance: are latency, throughput, and response thresholds verifiable enough?
    - Scalability: are scale, concurrency, and growth limits assumed?
    - Reliability & Availability: do failure, recovery, and non-interruption requirements exist?
    - Observability: are logging, metrics, tracing, or debug signals needed?
    - Security & Privacy: are role restrictions, data protection, and abuse prevention missing?
    - Compliance: are regulations, audits, or governance constraints explicitly stated?
  - Integration & External Dependencies
    - Do external services, third-party APIs, notification channels, or sync dependencies exist?
    - Are import/export formats, protocols, or version assumptions missing?
    - Is the degradation behavior when external dependencies fail undefined?
  - Edge Cases & Failure Handling
    - Are negative scenarios, illegal inputs, and race conflicts covered?
    - Are rate limits, throttling, timeouts, disconnections, and resends missing?
    - Is the handling of simultaneous multi-user operations, state desync, or duplicate submissions undefined?
  - Constraints & Tradeoffs
    - Are known technical, deployment, storage, or environment constraints already in the spec?
    - Are explicit trade-offs, rejected alternatives, or deliberately deferred scopes explained clearly?
  - Terminology & Consistency
    - Is the same concept described with multiple names?
    - Do User Stories, FR/NFR, key entities, and success criteria contradict each other?
  - Completion Signals
    - Are the acceptance scenarios sufficient to verify the main flows?
    - Are the success criteria measurable, verifiable, and consistent with the requirements?
    - Could the checklist ready judgment be overturned by undecided gaps?
  - Misc / Placeholders
    - Do `TODO`, `TBD`, `NEEDS CLARIFICATION`, vague adjectives, or unquantified terms affect downstream planning?
- If a category is `Partial` or `Missing`, further judge whether it is sufficient to form a candidate question, rather than escalating every missing item directly.

## Good Example

- This example is good because it retains categories and sub-items, so the scan can be replayed without re-reading external sources.

```md
Scan results:
- Interaction & UX Flow: `Partial`
  - Main success path exists
  - Missing disconnection and retry scenarios
- Non-Functional Quality Attributes: `Partial`
  - Real-time sync is stated as needed
  - Missing acceptable latency threshold
- Terminology & Consistency: `Clear`
```

## Bad Example

- This example is bad because it compresses a highly instructive taxonomy into one vague slogan.

```md
Scan method:
- Systematically check whether the spec still has gaps
```

# Rule 2 - Only gaps that would change spec correctness or readiness escalate to candidate questions

- Level: `MUST`
- A `Partial` or `Missing` category should create a candidate question only if its answer would materially change the following:
  - User story splitting, boundaries, or priority order
  - FR / NFR attribution, requirement correctness, or spec consistency
  - Formal acceptance scenarios, success criteria, or ready judgment
  - Key entities, data constraints, state transitions, or external dependencies
  - Key decisions that would make `/plan`, follow-up research, or design head in visibly different directions
- If a gap only affects naming preferences, microcopy, local interaction wording, or low-risk details for which defaults can be safely adopted at planning or implementation time, keep it in the spec's assumptions, `NEEDS CLARIFICATION`, or deferred risks — do not escalate it to this round's questions.
- If a gap is already explicitly stated in the spec as deliberately deferred, not included in the first version, or carried by another skill, do not escalate it into a duplicate question.

## Good Example

- This example is good because the question would directly change acceptance and NFR boundaries.

```md
Gap:
- "State sync must complete within an acceptable time" but no latency threshold

Judgment:
- Affects NFR verification and readiness
- Create a candidate question
```

## Bad Example

- This example is bad because it escalates a low-risk wording preference into a formal question.

```md
Gap:
- Should the error message say "Retry" or "Try again"

Judgment:
- Create a candidate question
```

# Rule 3 - Candidate questions must be ordered by Impact × Uncertainty, and the question budget must be controlled

- Level: `MUST`
- After creating candidate questions, they must be ordered by a combined `Impact × Uncertainty` judgment, not by the order they appear in the spec or whichever gap is seen first.
- `Impact` should first consider its surface of effect on spec correctness, cross-section consistency, formal acceptance, data model, NFR commitments, and downstream `/plan`.
- `Uncertainty` should consider whether the current spec admits multiple reasonable interpretations, whether they contradict each other, and whether a unique derivable answer is missing.
- When delegating to `/axb-clarify` in a single round, carry at most 1 to 3 questions; the entire clarify session must accumulate no more than 5 questions.
- If there are more than 3 high-impact gaps, first keep the top 1 to 3 by ranking, and list the rest as deferred high-risk gaps in the completion report; do not dump all questions at once.

## Good Example

- This example is good because it first picks the gaps that genuinely pivot subsequent planning.

```md
Candidate question ranking:
1. First-card rule: changes the match flow and acceptance
2. Mid-match disconnection handling: changes state transitions and win/lose boundaries
3. Real-time sync latency threshold: changes NFR verification
4. Room list display style: defer
```

## Bad Example

- This example is bad because it has no ranking logic and no question budget control.

```md
Ask everything on sight:
1. First-move rule
2. Disconnection handling
3. Latency threshold
4. Error copy
5. Room naming
6. Hint colors
```

# Rule 4 - Do not ask for the sake of asking; when clear enough, proceed directly to writeback or reporting

- Level: `SHOULD`
- If the spec has local undecided details that are no longer sufficient to change high-impact judgments, do not delegate `/axb-clarify` again; keep them as assumptions, `NEEDS CLARIFICATION`, or deferred risks.
- If after this round's scan all high-impact categories are `Clear`, skip `/axb-clarify` directly and proceed to re-verification and the completion report.
- If a gap exists but the answer is better decided by follow-up research, a technical solution, or a planner skill, also explicitly state the defer reason in the completion report rather than prematurely disguising planning questions as requirement clarification.

## Good Example

- This example is good because it recognizes that low-risk undecided details are not worth interrupting the flow.

```md
Observations:
- Main flows, acceptance, and NFRs are clear enough
- Only the room list presentation detail remains undecided

Decision:
- Do not enter `/axb-clarify`
- List it as low-risk deferred in the completion report
```

## Bad Example

- This example is bad because it treats every undecided detail as a must-ask question.

```md
Observations:
- Only low-risk UI details remain undecided

Decision:
- Still require entering `/axb-clarify` to ask 3 more questions
```
