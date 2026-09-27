# Rule 1 - Clarification answers must be written back to the section with the most responsibility

- Level: `MUST`
- Each confirmed answer must be written back to the spec section that best carries its semantic responsibility; do not only append it in a unified notes area or meeting minutes area.
- The writeback location must converge at least according to the following mapping:
  - Story boundary, role differences, main flow changes: update the corresponding `User Story`, its description, priority rationale, or acceptance scenarios
  - Story-specific functional requirements: update that story's `Functional Requirements (FR)`
  - Story-specific non-functional requirements: update that story's `Non-Functional Requirements (NFR)`
  - Cross-story rules or global constraints: update `Global Requirements`
  - Error handling, negative scenarios, disconnections, conflict resolution: update `Edge Cases`
  - Key terms, entity fields, relationships, states: update `Key Entities` or the corresponding story content
  - Measurable thresholds, acceptance completion conditions: update `Success Criteria`
  - Undecided items that belong only to premises and boundaries: update `Assumptions` or keep as explicitly deferred risks
- If an answer affects multiple sections at once, all affected sections should be updated, but each section carries only its own responsibility — do not paste the same passage repeatedly.

## Good Example

- This example is good because it writes the answer back to the correct section instead of leaving it only in supplementary notes.

```md
Clarification answer:
- The first player of a match is decided randomly

Writeback:
- Update User Story 3's acceptance scenarios
- Update the corresponding FR's first-move rule
- If necessary, add a Success Criterion verifying first-move assignment
```

## Bad Example

- This example is bad because it does not integrate the answer back into the spec's responsibility areas.

```md
Clarification answer:
- The first player of a match is decided randomly

Writeback:
- Only add a line at the very bottom of the document: "Note: the first player is random"
```

# Rule 2 - If a new answer overturns old statements, the old content must be replaced or deleted — they must not coexist

- Level: `MUST`
- If this round's clarification answer conflicts with existing statements in the original spec, the new answer must replace the old statement, or the overturned text must be deleted; contradictory claims must not coexist.
- Do not layer the new answer beside the old content as an "additional note", leaving later executors to guess which version is valid.
- If the conflict spans multiple sections, every affected spot must be cleaned up one by one — not just one place.
- If this round's answer is not yet fully final, only one explicit temporary state may be kept; two mutually exclusive options must not be kept at the same time.

## Good Example

- This example is good because it removes the overturned description, leaving the spec with exactly one valid version.

```md
Original text:
- The room owner goes first [NEEDS CLARIFICATION]

Clarification answer:
- The first player is now decided randomly

Processing:
- Delete the original "room owner goes first" statement
- Change it to "the system MUST randomly decide the first player when the match starts"
```

## Bad Example

- This example is bad because it keeps mutually exclusive conclusions together, making the spec messier.

```md
Original text retained:
- The room owner goes first

Additional note:
- After clarification, changed to a random first player
```

# Rule 3 - Terminology must be unified to canonical names to avoid synonym drift

- Level: `SHOULD`
- If after clarification the spec is found using multiple names for the same concept, a canonical term should be chosen and the wording unified in the affected sections.
- Only when keeping the old name aids transitional understanding may a cross-reference like "previously called X" be added at its first occurrence; do not mix names back and forth throughout the document.
- The scope of terminology unification covers at least User Stories, FR/NFR, Edge Cases, Key Entities, and Success Criteria.

## Good Example

- This example is good because it selects a single term and writes it back consistently.

```md
Observations:
- The same concept is written as "room code", "match code", and "entry code" at the same time

Processing:
- Unify as "match code"
- If necessary, add a note at first occurrence: "previously called room code"
```

## Bad Example

- This example is bad because it accepts the answer but still lets multiple names exist in parallel.

```md
Processing:
- User Story keeps "room code"
- FR changes to "match code"
- Success Criteria writes "entry code"
```

# Rule 4 - Unresolved high-impact gaps must have their status explicitly kept — never patched with imagination

- Level: `MUST`
- If high-impact gaps remain unresolved after this round's `/axb-clarify`, their current status must be explicitly stated in the spec or completion report, e.g. `NEEDS CLARIFICATION`, deferred risk, or to be judged by a follow-up skill.
- Do not fill in an unconfirmed answer on your own just to make the document look complete.
- If a gap is explicitly deferred to follow-up research, planning, or implementation design, the defer reason should be written down so follow-up skills know this is a deliberate retention, not an omission.

## Good Example

- This example is good because it keeps the true undecided status instead of pretending a decision was made.

```md
Status:
- Whether a disconnection pauses the match, forfeits it, or waits for reconnect is still undecided

Processing:
- Keep `NEEDS CLARIFICATION` in Edge Cases
- Explicitly state in the completion report that this gap still blocks readiness
```

## Bad Example

- This example is bad because it fills in an answer on its own without confirmation.

```md
Status:
- The disconnection rule is not yet confirmed

Processing:
- To make the spec complete, directly write "no reconnect within 30 seconds means forfeit"
```
