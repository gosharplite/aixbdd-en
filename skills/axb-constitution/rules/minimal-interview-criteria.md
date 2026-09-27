# Rule 1 - Only gaps that would change placement or strength escalate to an interview

- Level: `MUST`
- Only when a gap would change which file a rule should go to, whether a new file is needed, whether rule strength should be `MUST` /
  `SHOULD` / `MAY`, or would change the rule content itself, should it be escalated to an interview question.
- If the user has already explicitly stated the rule topic, target skill, and artifact, do not re-ask low-value questions.
- Do not interview every small detail for the sake of completeness; this skill only handles the high-impact gaps necessary for this round.

## Good Example

- This example is good because it only asks questions that truly affect rule placement and strength.

````md
Q1: Should this API response rule go into `shared.md` or `skills/axb-api-plan/openapi.md`?
Q2: Is this rule a hard `MUST`, or a `SHOULD` that allows reasoned deviation?
````

## Bad Example

- This example is bad because it escalates a tone preference that does not affect constitution placement into a formal interview.

````md
Q1: Should the rule title be more colloquial?
Q2: Should the Good Example use two blank lines?
````

# Rule 2 - Each round asks only the minimum necessary number of questions

- Level: `MUST`
- Each clarify round should ask only 1 to 3 questions, prioritizing the gaps that best avoid misplacing rules or over-expansion.
- If the first round of answers is sufficient to write the files, stop asking; do not add questions just to fill a quota.
- If questions have upstream/downstream dependencies, ask the upstream question first, then decide whether follow-up questions are needed.

## Good Example

- This example is good because it first confirms whether a new file should be created before deciding whether details need follow-up.

````md
Q1: Should this rule be added to the existing `skills/axb-tasks/tasks.md`, or should a new skill artifact file be created?
Q2: If a new file is created, what is the target artifact name?
````

## Bad Example

- This example is bad because it expands too many downstream details at once before the target file is confirmed.

````md
Q1: What is the rule title?
Q2: How many Good Examples?
Q3: Should the Bad Example include a code block?
Q4: Filename in English or Chinese?
Q5: Add supplementary notes?
````

# Rule 3 - After the interview, it must be possible to return directly to the minimal write set

- Level: `SHOULD`
- After the interview, the answers should map directly to "which files to modify, and what rules to add to each".
- If the question design cannot lead back to concrete files and rule content, the questions are too abstract and should be rewritten.

## Good Example

- This example is good because the answers directly determine placement and the change surface.

````md
Answer:
- Place in `skills/axb-data-plan/data-model.md`
- Strength is `MUST`

Follow-up writes:
- Modify only one file
- Add one Rule to that file
````

## Bad Example

- This example is bad because even after answering, it is still unclear which file to change.

````md
Answer:
- Want it to be a bit more rigorous
- Feels like it leans toward the data side
````
