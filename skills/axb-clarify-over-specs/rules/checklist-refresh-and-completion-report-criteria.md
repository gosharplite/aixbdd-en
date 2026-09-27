# Rule 1 - The checklist only updates items whose actual status changed

- Level: `MUST`
- If `CHECKLIST_FILE` exists, refreshing may only switch checkboxes whose actual status has changed; unchanged lines, headings, order, descriptions, and whitespace must be kept as-is — no cosmetic rewrites.
- When refreshing, first re-judge whether each checkbox passes against the updated `spec.md`, then decide whether `[ ]` / `[x]` needs to switch.
- If an item still fails after the update, keep it unchecked and explain in the completion report why it still fails.
- If there is no checklist this round, skip the file update but still explicitly state "no checklist to refresh this round" in the completion report.

## Good Example

- This example is good because it only changes the checkboxes whose status really changed.

```md
Before update:
- [ ] Remaining `NEEDS CLARIFICATION` items have been marked whether they block downstream planning

After update:
- [x] Remaining `NEEDS CLARIFICATION` items have been marked whether they block downstream planning

All other checklist content untouched
```

## Bad Example

- This example is bad because it rewrites the entire checklist with new wording, creating a large amount of unrelated diff.

```md
Processing:
- Casually reorder the checklist
- Adjust the wording of all entries
- Also switch a few checkbox states
```

# Rule 2 - The ready judgment must consider the checklist and the remaining high-impact gaps together

- Level: `MUST`
- When judging whether `/plan` can proceed, do not look only at whether the spec has been updated, nor only at part of the checklist's checked state; the following must be evaluated together:
  - Are there still unresolved high-impact requirement gaps?
  - Would these gaps change formal acceptance, data boundaries, NFR commitments, or the planning direction?
  - Does the checklist still have failing items corresponding to the above high-impact gaps?
- If high-impact gaps remain that would change the downstream planning direction, judge it as not yet ready, even if the rest of the spec is largely complete.
- If the remaining failing items are only low-risk deferred details that will not overturn downstream planning, readiness for `/plan` may still be granted after explicitly stating the risk in the completion report.

## Good Example

- This example is good because it does not mistake "has updates" for "is ready".

```md
Observations:
- The first-move rule and latency threshold have been added
- But disconnection handling is still undecided and affects game state transitions and acceptance

Judgment:
- Not yet ready
- Recommend running `/axb-clarify-over-specs` again
```

## Bad Example

- This example is bad because it ignores the remaining high-impact gaps and declares completion prematurely.

```md
Observations:
- The spec has some updates
- Two more checklist items are checked

Judgment:
- Proceed directly to `/plan`
```

# Rule 3 - The completion report must fully account for this round's clarification effects and residual risks

- Level: `MUST`
- The completion report must state at least:
  - The target `SPEC_FILE` and `CHECKLIST_FILE` (or its absence status)
  - Whether `/axb-clarify` was entered this round, and how many high-impact gaps were actually handled
  - Which sections were updated
  - Checklist before / after status, or that there is no checklist to refresh
  - Which high-impact gaps are resolved, which remain deferred or outstanding
  - Whether it is ready, and whether the recommended next step is `/plan` or running `/axb-clarify-over-specs` again later
- The point of the completion report is to let both the user and follow-up skills know: which risks were cleared this round, and what remains that must not be pretended away.
- If `/axb-clarify` was not entered this round, also explain why, e.g. all high-impact gaps are clear, or only low-risk deferred details remain.

## Good Example

- This example is good because it reports the handling results as well as the remaining risks and next steps.

```md
Completion report:
- Target spec: `specs/001-online-pvp-1a2b/spec.md`
- Entered `/axb-clarify`: yes, 2 questions
- Updated sections: User Story 3, Edge Cases, Success Criteria
- checklist: 12/16 -> 14/16
- deferred: disconnection recovery strategy
- ready: no
- Recommended next step: run `/axb-clarify-over-specs` again
```

## Bad Example

- This example is bad because it only says "updated", without letting anyone know the results and remaining problems.

```md
Completion report:
- spec has been updated
- please continue to the next step
```

# Rule 4 - Checklist absence or deferred gaps must not be hidden

- Level: `SHOULD`
- If `CHECKLIST_FILE` does not exist, the completion report should explicitly state that no checklist was refreshed this round, rather than letting the user mistakenly believe complete verification was done.
- If high-impact gaps were deliberately deferred, the completion report should explain the defer reason and its impact on downstream `/plan`, not just write a vague "there are still some issues to confirm".
- If no questions are needed at all this round, the completion report should also state that it is because all high-impact gaps are `Clear`, rather than omitting the clarification strategy judgment.

## Good Example

- This example is good because it makes the absence and defer status fully visible.

```md
Report:
- checklist: no corresponding file this round, so not refreshed
- deferred: whether third-party notification channels are included in the first version; low impact, kept for `/plan`
```

## Bad Example

- This example is bad because it covers up verification gaps with vague wording.

```md
Report:
- mostly all good
- some places, we'll see later
```
