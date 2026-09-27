# Rule 1 - Ask about the gaps with the largest impact first

- Level: `MUST`
- clarify should prioritize inventorying gaps that would change the requirement scope, core flows, architecture boundaries, role permissions, data model, acceptance criteria, or irreversible decisions.
- If the caller skill has already specified questioning dimensions, follow those dimensions first; only when it does not violate the caller's requirements may other gaps be supplemented in general impact order.
- Do not ask first about low-impact details that only affect naming, minor UX tweaks, incidental formatting, or that can be deferred.

## Good Example

- This example is good because it first confirms the first-version scope and the approval flow, both of which directly affect subsequent system design and workload.

```text
Requirement: I want to build an internal company leave request system.
Ask first:
1. Should the first version only do leave applications and manager approval, or also include the HR back office?
2. Should the leave approval flow be single-level, dual-level, or condition-based switching?
```

## Bad Example

- This example is bad because it asks about button copy and colors first, before confirming how big the first version of the system should be at all.

```text
Requirement: I want to build an internal company leave request system.
Ask first:
1. Should the submit button say "Submit" or "Send"?
2. Should the primary color be blue or green?
```

# Rule 2 - Each question focuses on exactly one decision axis

- Level: `MUST`
- Each question should handle exactly one main decision axis, letting the user clearly compare options and make the call directly.
- If two doubts would lead to different option sets, split them into different questions; do not force multiple entangled decisions into a single question.
- You may supplement causes and consequences in the `Context`, but the `Summary Question` should ask the user to answer only one thing.

## Good Example

- This example is good because it splits "first-version scope" and "notification integration" into two questions, each answerable independently.

```text
Q1: Which scope do you want delivered first in the first version?
Q2: What level of notification and integration do you most want achieved in the first version?
```

## Bad Example

- This example is bad because it asks about scope, notifications, and timeline all at once; the user can hardly answer with a single answer.

```text
Should your first version include the HR back office, integrate with Slack, and go live within two weeks?
```

# Rule 3 - At most 3 questions per round, at most 5 per session

- Level: `MUST`
- Output at most 3 questions per round so the user can focus on answering; do not dump all uncertainty at once.
- The entire clarify session accumulates at most 5 questions; if convergence is still not reached within 5, explicitly state the remaining risks and blockers instead of asking without limit.
- If there are more than 3 high-impact gaps, first keep the most critical 1 to 3 questions and leave the rest for the next round.

## Good Example

- This example is good because it first converges the main decisions with 3 questions, then judges whether a second round is needed after the user answers.

```text
Round 1:
1. First-version scope
2. Approval flow
3. Notification integration
```

## Bad Example

- This example is bad because it lists 8 questions at once, forcing the user to handle all gaps without any rhythm.

```text
Round 1:
1. First-version scope
2. Approval flow
3. Notification integration
4. Role permissions
5. Leave type rules
6. Reporting needs
7. UI style
8. Launch timeline
```

# Rule 4 - Do not ask for the sake of asking when a gap is clear enough

- Level: `SHOULD`
- If the user has already explicitly decided something, or a unique reasonable interpretation can be directly inferred from the existing context, do not ask again.
- The purpose of clarify is to remove high-risk uncertainty, not to rewrite all information into a questionnaire.
- If remaining questions only involve low-risk defaults that can be safely adopted at implementation time, hand back to the caller skill to continue with explicit assumptions rather than adding another clarify round.
