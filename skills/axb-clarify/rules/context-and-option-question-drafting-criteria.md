# Rule 1 - `Context` must be sufficient to support the user's judgment

- Level: `MUST`
- Each question must first provide an understandable and sufficient `Context`, explaining why this question matters, what it affects, and the minimal background the user needs before answering.
- If the `Context` involves technical terms, process nodes, technical architecture, or role divisions, explain them in plain language first before posing the question.
- Do not write the `Context` as a vague opener, nor sneak unconfirmed assumptions in as established facts.
- If words alone struggle to explain a flow or structure, you may attach Mermaid directly in the conversation to help the user make a deep judgment.

## Good Example

- This example is good because it first explains which subsequent decisions the MVP and scope choice will affect, so the user knows what they are deciding.

```text
What you have made clear so far is "build a leave request system", but not yet how big the first version should be.
This directly affects the number of screens, table design, the permission model, and the development timeline.
MVP here means the minimal viable scope for the first version — getting the most core, must-not-fail flow right first.
```

## Bad Example

- This example is bad because it supplies no decision background at all; the user can only guess the real impact of this question.

```text
I need you to answer this question. It is very important.
```

# Rule 2 - The `Summary Question` must be a single directly-answerable question

- Level: `MUST`
- The `Summary Question` must continue from the preceding `Context` and condense it into one clear, natural question that directly leads into the options.
- The question itself should let the user know what they are deciding right after reading it; do not write it as multiple follow-ups, a vague probe, or colloquial fragments.
- If multiple questioning dimensions are needed, split them into multiple questions; do not mix multiple decision axes into a single question sentence.

## Good Example

- This example is good because the user can immediately understand that what is being chosen is the first-version delivery scope.

```text
Which scope do you want delivered first in the first version?
```

## Bad Example

- This example is bad because it mixes several things at once, and the sentence itself is not clear enough.

```text
So are you thinking of starting smaller first, or maybe including notifications and such together, or actually you haven't decided yet?
```

# Rule 3 - `Options` must be a comparable Markdown table

- Level: `MUST`
- The options section must use a Markdown table, and every option must be numbered.
- The table should contain at least `No.`, `Option`, and `Description` columns so the user can quickly compare differences.
- Each option's description should clearly state that option's boundary and how it differs from the other options in 1 to 2 sentences.
- Single-choice or multi-choice must be marked, and `Others` must always be present so the user can add input beyond the existing options.

## Good Example

- This example is good because the format is fixed and comparable, and `Others` is kept so the user can step outside the default answers.

```md
**Options (single choice)**

| No. | Option | Description |
| --- | --- | --- |
| 1 | Leave applications and manager approval only | Focus on the most core flow first; no HR back office or reports yet. |
| 2 | Leave application + manager approval + HR back office | Also covers HR's management needs, but the first-version scope will be larger. |
| 3 | Others | My need is neither of the above; I want to add the scope I really want. |
```

## Bad Example

- This example is bad because there is no table, no numbering, and no way to see how the options differ.

```text
A. Small version
B. Big version
C. Other
```

# Rule 4 - One option must be recommended with a stated reason

- Level: `MUST`
- Each question must recommend one most reasonable option, marking a short reason directly in the option text in the form `(Recommended: {{reason}})`.
- The recommendation reason should point to benefits, risk control, verification speed, or information completeness in the current context; do not just write "I think it's better".
- If the caller skill has specified decision preferences or constraints, the recommendation should align with that constraint first.

## Good Example

- This example is good because the recommendation reason directly echoes the need to verify the core flow first in the first version.

```text
Leave applications and manager approval only (Recommended: lock down the core flow first, verify requirements fastest)
```

## Bad Example

- This example is bad because it only states the recommendation without letting the user know the basis.

```text
Leave applications and manager approval only (Recommended)
```

# Rule 5 - clarify must ask questions directly in the conversation, not via the Ask Tool

- Level: `MUST`
- clarify's questions must be output directly as regular conversation messages, letting the user read the `Context`, Mermaid, question, and options in the same context.
- Do not substitute this output format with the Ask Tool or other form-style interactions.
- If Q&A records need to be kept, the record is organized after the user answers — the questions themselves are not converted into a tool form.
